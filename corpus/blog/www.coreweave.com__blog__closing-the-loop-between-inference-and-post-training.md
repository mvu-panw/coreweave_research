# Closing the Inference to Post-Training Loop | CoreWeave Blog

Source: https://www.coreweave.com/blog/closing-the-loop-between-inference-and-post-training

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## Why post-training starts the day you ship
Shipping a model used to mark the end of the development cycle: train it, evaluate it, deploy it, then move on. Production AI works differently. Once a model starts serving real traffic, you start seeing what benchmarks and pre-deployment evals can’t fully show you: where the model fails, which edge cases matter, and what users actually need from it.
That production signal can improve both model quality and economics. It may show that a smaller model can reproduce the behavior of a more expensive one, that additional supervision would help, or that reinforcement learning is the better fit. If a model already has the capabilities the application needs, refining it for the workload can also be more efficient than treating every new model generation as another migration.
The hard part is closing the loop. Production traces have to become usable training data. Post-training needs compute and orchestration. The resulting model has to be evaluated and returned to serving. In reinforcement learning, inference becomes part of training itself: the current policy generates rollouts, training produces new weights, and those weights have to move back into serving throughout the run.
At Fully Connected 2026, we introduced three capabilities that address different parts of that lifecycle: CoreWeave Model Distillation, CoreWeave RL Rollouts on CoreWeave Inference, a programmable training API, now in preview with an official launch planned for later this year. Those workflows come together in CoreWeave Forge, giving teams a more direct path from what a model does in production to what they improve next.

## Start with the failure mode, not the tooling
Before choosing a post-training technique, determine whether the model is actually the thing that needs to change. Retrieval, missing context, prompts, tool failures, and serving behavior can all surface as apparent model-quality problems. Changing the weights will not fix a problem that sits elsewhere in the system.
When the model does need to change, the signal should determine the technique. 
- Model distillation fits when a stronger model already produces the desired behavior and you want to reproduce it in a smaller or more economical model. 
- Supervised fine-tuning (SFT) fits when you can provide high-quality examples and need more consistent behavior on a specific task. 
- Reinforcement learning (RL) is useful when you can evaluate the outcome reliably, but cannot easily specify the ideal response in advance. 
Teams may use more than one of these approaches over a model's lifecycle; the important part is that the choice starts with evidence from the workload, not with whichever technique the platform happens to make easiest.

## Turn production signal into a better model with CoreWeave Model Distillation
CoreWeave Model Distillation is the managed path through that loop. Inference traffic can be captured in CoreWeave Agent Lens and turned into training data as the application runs. From there, the workflow can improve weak outputs through relabeling, test different base models and hyperparameters, deploy candidates to Serverless Inference, and compare them against the model already running in production. 
That’s where the economics of the loop become tangible. The next improvement does not always require moving the workload to a newer or larger model. If a smaller model already has the right underlying capabilities, fresh production data can make it substantially better suited to the task while preserving a serving profile that’s already understood.
Method is an example of that lifecycle in practice. In 2024, it used the earlier OpenPipe product to train a Llama 3.1 8B model to navigate bank IVR systems using GPT-4o outputs. In August 2026, they revisited the same workload with fresh production data, relabeled it with GPT-5.6 Sol, and iterated on the model again. The resulting model won 57.5% of head-to-head evaluations against the version that had been running in production.
The base model had not changed. The production signal had and the new Model Distillation capability in Forge, made the iteration faster.

## Write the training loop, skip the infrastructure underneath it
Some teams want more control over how their models learn. They want to try different training methods, combine them in new ways, and adjust the recipe as they go without managing the infrastructure required to run the experiment.
The programmable training API for Serverless Training,  now in limited preview,  gives you that control. You write the training loop in Python; CoreWeave handles the compute and training infrastructure underneath it.
For example, you might use reinforcement learning to help an agent get better at completing tasks, then mix in supervised learning on verified demonstrations to reinforce good behavior:
learner = await training.create_learner(model=model, lora=lora)
sampler = await serving.create_adapter(name="sampler")
optimizer = AdamConfig(learning_rate=1e-5)

for step in range(num_steps):
 trajectories = await run_agent(sampler, tasks)
 update = learner.batch()
 update.forward_backward(
 build_rl_batch(trajectories), loss="importance_sampling"
 )
 update.optim_step(optimizer=optimizer)

 if (step + 1) % sft_interval == 0:
 update.forward_backward(next_demo_batch(), loss="cross_entropy")
 update.optim_step(optimizer=optimizer)

 update.publish_weights(to=sampler)
 await update.result()

await (await learner.save_state("final")).result()
await learner.close()

Rollout and batch preparation helpers are illustrative; they contain your agent logic, reward calculations, and data preparation.
You control how often to mix in demonstrations, how to reward successful attempts, and how the recipe evolves. SFT, RL, and distillation build on the same training primitives, giving you room to experiment without operating the distributed systems beneath them.
Willow offers an example of the programmable training API in practice. The team started with supervised learning, then built scorers for reinforcement learning to further improve the model. These scorers targeted specific behaviors reducing filler words, making outputs easier to read, removing self corrected phrases and were combined into a reward function to guide training.
I'm insanely impressed. This model genuinely has a much better grasp on text styling. What you guys have is a massive improvement over what we have in deployment. Emojis work, listens to commands well, you guys are awesome.
Lawrence Liu, CTO and Co-Founder of Willow

## The rollout bottleneck is inference
In RL, inference is part of the training loop itself. That creates a different set of constraints than production serving: generating enough rollouts, keeping serving aligned with the policy being trained, and moving new weights back into the serving layer quickly enough to keep training progressing.
CoreWeave Inference now supports RL rollouts built on NVIDIA Dynamo with vLLM support. Your trainer, reward logic, and environment stay where they are. When the trainer writes a new checkpoint, it can hot-load those weights onto a live deployment without impacting in-flight requests and endpoint availability, allowing rollout generation to continue against the policy you intend to sample from.

The serving layer is purpose-built for RL,  returning training-grade metadata—logprobs, token IDs, expert routing for MoE—instead of bolting these onto general-purpose inference. Checkpoints hot-load as full snapshots or incremental deltas, cutting synchronization time after your first upload. Every rollout uses the current policy weights, so deployments stay aligned with what the trainer recently  published, eliminating staleness and the redeployment lag that stalls training.
CoreWeave partnered with NVIDIA and you.com to validate RL Rollouts on a real workload: post-training NVIDIA Nemotron 3.5 Lightning for web search. Running SFT + RL with you.com's search tools integrated into the training loop, the team improved BrowseComp accuracy by 22.94% (from 36.97% baseline to 45.45%), while reducing average tool calls by 30.24%, a direct win on both quality and cost. On the infrastructure side, hot-loading checkpoints into a live deployment was approximately 15x faster than traditional redeploy cycles, freeing training time that would otherwise have been stalled waiting for infrastructure updates. The partnership demonstrates what becomes possible when rollout serving, RL infrastructure, and post-training search optimization align: the gains came from three distinct pieces working together -better search tooling, post-training refinement, and harness improvements.
For a team optimizing a smaller or  more efficient model to hold its own against models an order of magnitude larger, that time back in the loop mattered as much as any single benchmark score.

## Bringing the loop together in CoreWeave Forge
The larger shift here is not simply making individual training or inference tasks easier. It is making model improvement part of the production system itself.
CoreWeave Forge is where those workflows come together. Production inference generates the signal. Distillation or post-training turns that signal into an improved model. The model moves back into inference, where it starts generating the evidence for the next iteration. In reinforcement learning, the connection is tighter still: inference is already inside the training loop through rollout generation and weight updates.
These three capabilities announced at Fully Connected 2026 support different ways of working within that lifecycle. Model Distillation provides a managed path. The programmable training API gives researchers direct control over the training logic without requiring them to operate the underlying infrastructure. CoreWeave RL Rollouts let teams keep their own trainer while using CoreWeave for the inference side of the loop.
Models trained through serverless training are written back as artifacts and tagged so they can move into Serverless Inference without a separate registry handoff. Experiments remain logged alongside them, preserving the connection between the run, the resulting model, and what eventually serves in production.
The result is a model lifecycle in which training and inference are no longer separate operational islands. What happens in production can inform the next training run, and what comes out of training can return directly to the serving environment that produced the signal in the first place. 

## What's next for CoreWeave 
There is much more to unpack in each part of the loop. In the coming weeks, the engineers behind CoreWeave Model Distillation, the programmable training API, and CoreWeave RL Rollouts will go deeper on how each capability works and the design decisions behind it.
In the meantime, read the CoreWeave Forge blog and press release for the broader story behind what we launched at Fully Connected 2026 and stay tuned as we go deeper on the infrastructure connecting training, post-training, and inference.

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

Inference,

Copy code

Copied!

Inference,
