# Reflection’s Open-Weight Beam Model

Source: https://www.coreweave.com/blog/from-training-to-serving-reflections-beam-on-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Reflection’s first open-weight model, Beam, is available on Day 0 through Serverless Inference in CoreWeave Forge. Developers can call it through an OpenAI-compatible API, pay per token, and begin evaluating coding and agentic workloads without provisioning GPUs or operating a serving cluster.
Beam’s path on CoreWeave spans training, post-training, and serving. Reflection used Weights & Biases Models within Forge during training. We’ve validated a supervised fine-tuning (SFT) use case with Axolotl on CoreWeave infrastructure, and Serverless Inference in Forge provides Day 0 access to the released model.
This release adds a new model to the Western open-weight ecosystem, with an Apache 2.0 license and a specific focus: software engineering and long-horizon, tool-driven tasks.

## What Reflection built into the Beam open-weight model
Beam is a mixture-of-experts model with 501 billion total parameters and 23 billion active parameters per token. Each token activates a fraction of the model, reducing computation relative to activating every parameter. Serving still needs to account for the full model’s weights, so active parameter count alone does not determine memory requirements or latency.
Reflection built this release for text-native workloads: source code, tool calls, logs, documents, and structured outputs. Beam is built for two workloads: software engineering and long-horizon agentic tasks, including resolving GitHub issues, maintaining code, and completing workflows through repeated model calls and tool interactions.
Beam’s approximately one-million-token context window provides room for extensive code and task history. The context length exposed by an inference endpoint depends on the provider’s serving configuration, so developers should check the supported limit when designing their workflows.
Beam ships under Apache 2.0 without custom license terms. Developers and researchers can inspect the weights, fine-tune the model, and choose their deployment environment. The release advances the Western open-weight ecosystem with a model teams can adapt to their own coding and agentic workloads.

## From training to post-training Beam on CoreWeave
Reflection used Weights & Biases Models within Forge during Beam’s training. Open weights extend that development path to teams adapting the released model to their own workloads.
Together with Axolotl, we’ve validated a supervised fine-tuning (SFT) use case for Beam on CoreWeave infrastructure. SFT trains the model on examples of desired behavior, giving teams a way to adapt its responses to a specific task or domain. For coding and agentic applications, those examples could capture repository conventions, expected tool-call formats, or domain-specific instructions. The use case starts with Beam’s open checkpoint and applies supervised fine-tuning through Axolotl on CoreWeave. In the validated run, Axolotl  fine-tuned Beam-1.0-501B-A23B on GPU kernel generation, training it on about 84 million tokens of PyTorch-to-Triton and CUDA examples from the open KernelBook and AI CUDA Engineer datasets. Training used LoRA adapters with expert parallelism across 16 NVIDIA B200 GPUs on two CoreWeave nodes and finished in 73 minutes. For a second use case, medical question answering, Axolotl trained LoRA adapters directly on Beam's NVFP4 checkpoint on a single B200 node, using APO-Zero preference optimization on rubric-scored examples of Beam's own answers to patient questions. Because the adapters are trained to survive requantization, they fold back into an NVFP4 checkpoint that serves on Blackwell in the same format as the base NVFP4 model. On HealthBench, where scores across a year of frontier model releases sit within a few points of each other, the merged model's score rose from 49.0% to 52.7% across all 5,000 conversations (graded with GPT-6 Luna Decisions), and the improvement held up after length adjustment and under every grader tested. 
These were demo runs, the results illustrate what's possible and do not represent Beam's full potential with fine-tuning. CoreWeave is exploring broader support for fine-tuning and reinforcement learning with Beam, including further work with Axolotl on online RL. Enterprises interested in post-training Beam with their own data can contact CoreWeave to discuss their requirements.

## Beam benchmark results on CoreWeave
For coding assistants and agents, these measurements need to connect to completed work. Output speed and latency affect how long users wait across repeated model calls. Quality and token consumption affect the cost of completing a task. Together, they help teams assess Beam against the requirements of their application.

### Model quality
Reflection's model card reports the released NVFP4 checkpoint at 89.3 on GPQA Diamond, 78.7 on AA-LCR and 78.4 on Terminal-Bench 2.1 (BF16: 90.6, 78.2 and 80.1). These are Reflection's results on Reflection's evaluation setup. To confirm that CoreWeave's serving configuration preserves that quality, we re-ran two of the benchmarks against the production configuration with the CoreWeave Evals API: 91.4% on GPQA Diamond (198 questions) and 77.8% on AA-LCR (99 tasks), both single runs at Beam's recommended sampling settings. Both results sit within statistical error of Reflection's figures.

### Serving performance on CoreWeave
Measured by CoreWeave on October 16, 2026, on NVIDIA GB300 with the production serving configuration: the full 1,048,576-token context window, temperature 0.7 and top_p 0.99. Latency is measured at the serving endpoint inside the cluster, so it excludes the public gateway and the internet path.

 | Workload
 | Concurrent requests per replica
 | Time to first token, median / p99
 | Inter-token latency, median / p99
 | Output speed per request, tokens/s (median)

 | Chat-style requests, 15k to 22k input tokens, 250 to 320 output tokens
 | 1
 | 0.12 s / 0.17 s
 | 2.3 ms / 5.9 ms
 | 429

 | Same workload under load
 | 32
 | 0.20 s / 0.45 s
 | 9.2 ms / 26.6 ms
 | 108

 | Agentic sessions, about 91k input tokens and 840 output tokens per turn
 | 32 session trees
 | 0.31 s / 3.1 s
 | about 10 ms median
 | 100

 | Long generations, 8k input tokens and 4k output tokens, cold cache
 | 10
 | 0.21 s / 1.28 s
 | 7.3 ms / 8.9 ms
 | 137

In practical terms:
- Interactive use feels fast: with a few requests in flight, Beam streams about 430 tokens per second to a single user, and the first token arrives in under 0.2 seconds at p99.
- Under load, at 32 concurrent requests on one replica, each request still receives about 108 tokens per second and p99 first-token latency stays under half a second.
- Agentic long-context work, with prompts around 90k tokens, keeps first-token latency around 0.3 seconds at the median; the p99 of 3.1 seconds reflects uncached prompts at the start of a session.
Per-user speed varies with the content and with how much of a prompt repeats across turns: the chat and agentic workloads above are multi-turn and benefit from prompt caching, while the long-generation run starts from a cold cache.
‍

## Start building with Beam on Serverless Inference
Serverless Inference provides an OpenAI-compatible endpoint with per-token billing. That API compatibility simplifies integration with clients and frameworks that support the interface. Model behavior still needs evaluation: prompt conventions, tool calling, output formatting, and failure recovery can differ between models. Tracing, evaluations, and observability with CoreWeave Agent Lens help teams inspect Beam across application execution. For an agent, the useful unit of analysis is the complete task, including model calls, tool responses, retries, and final output.
For coding and agentic workloads, evaluate:
- Task success: whether the model produces a correct patch or completes the workflow, with results checked against tests or explicit acceptance criteria
- Tool-use reliability: whether it selects the appropriate tool, generates valid arguments, and recovers from errors
- Completion time: elapsed time across all model calls and tool interactions
- Cost per successful task: token spend across the workflow, including unsuccessful attempts and retries
These measurements distinguish a model that performs well on isolated prompts from one that works reliably inside your application. Start with the managed endpoint, evaluate Beam against your coding and agentic workloads, and identify where fine-tuning could improve performance for your application.
Get started with Beam on CoreWeave Serverless Inference

Try CoreWeave Forge with a 30 free trial of Pro
To explore fine-tuning Beam with your own data or reinforcement learning for your workload, contact the CoreWeave team to discuss your requirements  and for an evaluation through CoreWeave ARENA or on your CoreWeave cluster.
Contact Us
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

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

### Closing the Loop Between Inference and Post-Training

7
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

Inference,

Copy code

Copied!

Inference,
