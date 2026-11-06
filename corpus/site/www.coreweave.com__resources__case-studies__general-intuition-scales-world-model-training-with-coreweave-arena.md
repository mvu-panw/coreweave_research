# General Intuition Scale to Production | CoreWeave Case Study

Source: https://www.coreweave.com/resources/case-studies/general-intuition-scales-world-model-training-with-coreweave-arena

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Resources

Case Studies

General Intuition Scales World Model Training with CoreWeave ARENA

General Intuition Scales World Model Training with CoreWeave ARENA

Industry
AI lab

Headquarters
New York, United States

Use Cases

AI model training

#### Ready to get started?

Contact Sales

3
min read

Copied

 How General Intuition validated world model training at scale with CoreWeave ARENA — achieving 20–30% better multi-node performance

## Challenge
Used by gamers since 2015, Medal.tv houses one of the world's richest collections of real human gameplay data. Recognizing the value of this data, CEO and co-founder Pim de Witte launched General Intuition, an AI research lab dedicated to developing models capable of spatio-temporal reasoning.
However, training world models and policies is fundamentally different from training large language models. There are no established scaling laws, standard architectures, or proven infrastructure patterns that help determine how model size, data volume, and distributed training interact.
Working with a lean infrastructure team, General Intuition explored several proof of concepts with different cloud providers for processing massive video datasets and running long-lived, multi-node jobs.
Core Needs List
- Reliable long-running training: Support multi-day, distributed training jobs for world models and policies without frequent failures
- High-throughput video pipelines: Move and process massive datasets efficiently
- Expert-led infrastructure support: Resolve GPU, networking, and scheduling issues without pulling researchers away from research

## Solution
The team set out to determine which provider could reliably scale their model training jobs and remove the infrastructure management burden from their ML researchers. Having worked together for previous GPU capacity, General Intuition ran one of their benchmark evaluations with CoreWeave.
Through CoreWeave ARENA, they benchmarked real training pipelines (not simulations) on production-grade GPU clusters and observed distributed training behavior under load in a production-scale AI lab.
Combined with direct access to expert infrastructure engineers, this structured evaluation environment enabled General Intuition to understand how their jobs performed, cost, and scaled before committing to production.
- Real workload evaluation at production scaleThrough CoreWeave ARENA, General Intuition benchmarked their actual world-model training pipelines—not synthetic tests—on production-grade GPU clusters, allowing the team to observe real distributed training behavior under sustained load.
- Reliable multi-day distributed trainingCoreWeave provided an environment where long-running, multi-node training jobs could run for days without frequent interruptions, compared to multiple failures a day on other providers.
- Operational simplicity for researchersUsing SLURM on Kubernetes (SUNK), General Intuition ran large distributed training jobs without forcing researchers to manage complex orchestration systems. Jobs started easily, retried automatically when needed, and behaved predictably.
- Direct access to expert infrastructure supportGeneral Intuition worked directly with CoreWeave infrastructure engineers over Slack to troubleshoot performance issues, GPU behavior, and networking concerns.
- Visibility into infra health and model behaviorMission Control's provided baseline visibility into node availability and utilization during large-scale runs, while integrations with Weights & Biases allowed General Intuition to track iterations per second, loss curves, and performance trends across providers.

## Outcomes
By evaluating their model workloads through CoreWeave ARENA, General Intuition replaced uncertainty with actual model performance evidence. The team gained confidence in how their training pipelines performed at scale, reduced infrastructure friction for researchers, and moved from proof-of-concept evaluations into production training on CoreWeave without slowing research velocity.
Faster path from evaluation to productionGeneral Intuition was able to move from proof-of-concept testing into production training in weeks, not months. Clear performance and scaling visibility removed guesswork and shortened the time required to commit to large-scale GPU deployments.
Reliable large-scale training for all model typesMulti-node training runs on CoreWeave were 20-30% more performant than workloads on other providers. Fewer interruptions meant less wasted compute and allowed researchers to focus on advancing model capabilities instead of restarting jobs.
From firefighting to forward progressReal-time access to CoreWeave's infrastructure experts, seamless Slurm on Kubernetes with SUNK, and integration with Weights & Biases meant researchers could focus on research outcomes rather than infrastructure troubleshooting.
‍

### AI model training
Train AI models faster with purpose-built infrastructure and streamlined workflows

### Slurm on Kubernetes
Run Slurm on Kubernetes for scalable, managed AI training clusters

### GPU Compute
Rely on high-performance GPU compute built for the most demanding AI workloads

## Read more case studies

See all customer stories

### Cohere Accelerates Training of North, Agentic AI for Enterprise

Learn More

### Mistral AI Unlocks 2.5x Faster Training Speeds

Learn More

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
