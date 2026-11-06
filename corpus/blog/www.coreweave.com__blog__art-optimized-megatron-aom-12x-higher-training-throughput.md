# ART-Optimized Megatron (AOM): 12x higher training throughput

Source: https://www.coreweave.com/blog/art-optimized-megatron-aom-12x-higher-training-throughput

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

ART-Optimized Megatron (AOM) is a new backend for our open source training library, ART, that achieves 12X the training step throughput of our previous Unsloth backend, 12X that of another popular RL framework, Miles, and 7X compared to Vanilla Megatron on the same hardware.
Before we dive in, a sneak peek at the results:
Training backend trajectories per dollar
‍
Training backend throughput (footnote 1)
‍

## Background
We’re continuously working to make reinforcement learning training faster and more reliable. Given a fixed hardware budget, there are three ways to speed up RL training:
- Overlapping training and inference through AsyncRL
- Improving inference throughput for faster rollout generation
- Improving training throughput so each optimization step takes less time
Earlier this year, we introduced PipelineTrainer to support AsyncRL, allowing rollout generation and model training to run in parallel. In this post, we’ll focus on our recent work to significantly improve training throughput itself.
So what sorcery did we use to achieve this performance?
It turns out the answer is fairly simple, most of the gains come from shared prefix, followed by additional tuning to maximize GPU utilization and experimenting with different parallelism strategies.

## What is a shared prefix and why does it matter?
When optimizing LLM training, we usually focus on tokens per second. Tokens per second is a useful measure of GPU throughput, but for reinforcement learning trajectories per second is a better metric. We can think of this as:
trajectories/s = tokens/s × trajectories/token
In other words, training throughput depends not only on how many tokens we process per second, but also on how many trajectories we can represent per token. Shared prefix training improves that second term: trajectory density.
In standard GRPO-style RL, a single prompt is often used to generate multiple rollouts. Imagine we’re training a customer support agent. The prompt likely include a large system instruction with behavioral guidelines, guardrails, and tool definitions, followed by a relatively short back and forth between the user and the model.
For the purposes of illustration, let’s go ahead with 5,000 system prompt tokens and 16 short rollouts. By default, training treats each rollout as a separate sequence. That means the full prompt, including the large system instruction, gets processed for training 16 times: once for each rollout.
With shared prefix training, we instead structure the tokens as a tree. The shared system prompt is encoded once, and the 16 rollout branches are attached following the shared system prompt. This avoids repeatedly processing the same prefix and significantly increases the number of trajectories we can train on per token. This structural sharing dramatically decreases the amount of compute, memory, and memory bandwidth necessary per rollout, leading to faster training.
Here’s a preview of how shared prefix training increases trajectory density:
* Sequence length can be thought of as the product of batch size and sequence length/batch. In ART, we concatenate trajectory groups along the sequence dimension instead of splitting them into separate batch elements to minimize padding tokens.
That's a brief summary about the importance of shared prefix. Next, let's walk through how we implemented shared prefix training in ART.

## How do we implement shared prefix?
Most modern LLM training frameworks use FlashAttention to compute self-attention, and for good reason. It makes standard attention dramatically faster and more memory efficient, especially for the dense causal attention patterns used in most decoder only LLMs. Most of the speed up comes from highly specialized fused kernels. However, these kernels do not support custom attention masks such as our shared prefix.
To make shared prefix training work, we need an attention mechanism that can handle a non linear tree layout. PyTorch’s FlexAttention gives us the necessary flexibility, supporting custom attention masks and running with well-optimized Triton kernels. We replaced the standard attention layers with FlexAttention and build a mask that permits tokens to attend to the shared prefix while strictly isolating sibling rollout branches from each other. 

The self-attention layer is not the only component we had to modify. We also had to update the linear attention layer by modifying the Gated DeltaNet (GDN) layer for Qwen3.6.
GDN works by compressing the sequence context into a fixed size state matrix at each token position. If we simply used the default GDN implementation on a shared prefix sequence, the result would fail catastrophically where Rollout #2 would mistakenly start from the GDN state of Rollout #1 instead of the Shared prefix.
To support shared prefix, we implemented a custom forward and backward pass that’s built on top of Flash Linear Attention (FLA) kernel. For the forward pass, we first run the FLA Kernel to compute the GDN final states for the shared prefixes. Then we run them again for all rollout branches using the shared prefix GDN states as the initial states for their respective completions. This will ensure we have the right calculation while avoiding repeated computation over the shared prefix.
One additional detail is that the convolution layer in GDN depends on n previous tokens’ projected query, key, and values . To preserve exact equivalence with the default computation, we store these values at the end of the shared prefix and pass them as inputs to the GDN layer at the start of each rollout branch.

## How close are we with the ideal theoretical gain?
The theoretical upper bound gain for 5k prefix with 16 rollouts of [100-1000] tokens with mean of 400 tokens is approximately 8X over the non-shared prefix-implementation. We measure this by comparing AOM with shared prefix to AOM with no shared prefix using FlashAttention 3. We choose this baseline in particular to account for the cost of using a less optimized Flex Attention kernel.
In our profiling, shared prefix with Flex Attention achieved 15% lower token throughput but 6.8x higher trajectory throughput.

This is an encouraging result. Our shared prefix implementation achieves approximately 85% of the theoretical upper bound performance. We're optimistic that we can move closer to the theoretical upper bound by using FlexAttention with a FlashAttention 4 backend.

## Beyond the big win
Beyond the primary Shared prefix improvement, we also tune the configuration to further improve GPU utilization and training throughput.

### Maximizing packed sequence
We modified packed sequence length to maximize raw GPU throughput. Generally, we find the larger the sequence, the better the throughput, with the limit being GPU memory.
Packed sequence length throughput
From our profiling, we found that maximizing activation recomputation yields the best performance. Maximum recomputation reduces activation memory and allows us to pack more sequences, giving improved throughput.

### Parallel benchmarking
Finally, we benchmarked several parallelism configurations to identify which setup produces the best trajectories per second at each GPU count. You can use these results as a starting point for configuring your own runs.

## Correctness
Now that we have a configuration that maximizes trajectories per second, the next question is: how do we know the implementation is correct?
In machine learning, the most dangerous bugs are often not the ones that fail loudly. Rather, they're the silent bugs. The ones that compile, run, and produce reasonable-looking outputs, while introducing small numerical mismatches that compound over time.

### Comparing logprobs against Hugging Face
As a starting point, we compare our Megatron shared prefix implementation against a Hugging Face transformers reference implementation. Specifically, we compare logprobs across multiple prompts to build confidence that the shared prefix path is numerically aligned with the HuggingFace implementation.
We use a similar validation process when introducing new parallelism strategies. Each time we change the parallelism, we compare outputs against a trusted reference to reduce the chance of introducing numerical instability.

### Aligning the training and inference engines
Another challenge in RL is that training and inference often run on different engines. Even when they serve the same model, small numerical differences between engines can create KL drift and destabilize training. To address this, we measure and minimize the KL difference between the training and inference paths. We also recently introduced MoE routing replay to ART, which reduced the KL difference by 4× for Qwen3.6 35B-A3B with only a 2.5% throughput slowdown.

### Future work
This post is part of a series on our ongoing work to make RL training faster and more reliable. We hope it provides a useful starting point for others experimenting with similar systems.
Some areas we’re excited to explore next include:
- Extending shared prefix training across multiple trajectory groups, especially for multi-turn conversational agents
- Experimenting with context parallelism to better support long output sequences
- Optimizing end-to-end Async RL training pipeline, such as minimizing overhead between training and inference
Stay tuned!

## Learn more
All of the work described above is open source, with implementation details available in the ART library. We’d love to see others build on top of it, and you can find the code for this specific project here.
Give ART a try. If you’d like to build your project with a hosted solution, you can use our Serverless offering. Enterprises interested in training proprietary agents with our team can contact us to learn more. 

### Footnote: Benchmarking details
1: Training throughput and cost
In the first set of charts, we show training throughput using the default LoRA implementation for each backend. Miles and Megatron use a shared LoRA matrix, while the others use per expert LoRAs. Shared LoRA is simpler and faster to compute but less expressive. When we benchmark Miles and vanilla Megatron with per expert LoRAs, the throughput is 2-5X lower than the shared LoRA implementation.
Training backend throughput

### Tinker
We saw high variance in Tinker throughput, ranging from 4 to 19 trajectories/s.
‍

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
min read

### CoreWeave Builds the First Global Backbone Network Purpose-Built for AI

5
min read

### Post-Training at the Frontier

7
min read

### CoreWeave Powers Agentic AI, HPC, and Data Analytics Workloads with NVIDIA HGX Rubin NVL8

5
min read

### Introducing CoreWeave Physical AI Launchables: Run Workloads With One Command

min read

### CoreWeave Zero Trust AI Framework: Your Model. Your Data. Your Trust. 

8
min read

### From Training to Serving: Reflection’s Beam on CoreWeave

min read

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

- Contact us
- Login

### Products
- GPU Compute
- CPU Compute
- Storage Services
- Networking Services
- Managed Services
- Bare Metal Servers
- 
Platform
- Fleet LifeCycle Controller

- Node LifeCycle Controller
- Tensorizer
- Observability

### Solutions
- AI Model Training
- AI Inference
- VFX & Rendering
- Mission Control

### AI Infrastructure

### Why CoreWeave

### Resources
- Customer Stories
- Documentation
- Status
- Pricing
- Resource Center
- Events & Webinars

### About
- About Us
- Careers
- Life at CoreWeave
- 
- Newsroom
- Investors
- Supplier Code of Conduct
- GHG Emissions Statement
- Privacy Policy
- Terms of Service
- 
Do Not Sell or Share My Personal Information

© CoreWeave.
290 W Mt Pleasant Ave
Suite 4100
Livingston, NJ 07039 

- 

- 

CoreWeave Forge,

Copy code

Copied!

CoreWeave Forge,
