# Agentic Inference: Prefix Caching and Routing | CoreWeave

Source: https://www.coreweave.com/blog/why-agentic-inference-needs-prefix-aware-routing-infrastructure

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In the first blog in this series, we explored how agentic applications create a fundamentally different infrastructure workload than traditional chat applications: each inference request reuses most of what came before, so the system prompt, tool definitions, and conversation history stay largely the same from call to call.
This article picks up where that discussion left off by examining what those repeated requests actually contain, including how infrastructure can avoid processing the same tokens over & over again.
If the infrastructure can recognize and reuse what the model has already processed, it can avoid recomputing large portions of the prompt, significantly reduce time-to-first-token (TTFT), and deliver more predictable inference for agents.
That's the promise of prefix caching, but realizing that benefit in production requires infrastructure that can prevent cache hits from turning into cache misses.

## The anatomy of an agentic prompt 
A prompt in an agentic workflow consists of two parts: the prefix and the new content.
- Prefix: the system prompt, tool definitions, and the conversation history built up so far
- New content: the new piece of the current call, usually the latest user message, tool result, or other newly appended context 
In many agent loops, successive inference requests share most of the same prefix.  The only new content is a small slice at the end: the latest tool result, or the model's next reasoning step.
Across an agent's tool-calling loop, each successive call carries the same system prompt, tool schemas, and accumulated history. Only the sliver at the end is new — but the prefix keeps growing.
This structure matters based on how attention works. Every token the model generates attends to the key/value state of every token before it, so that state has to exist before generation can begin. Even when much of the prompt is unchanged from the last call, the model rebuilds it from scratch.
A token's KV depends only on the tokens ahead of it, which is what makes an unchanged prefix reusable. It produces an identical KV no matter what is appended after it. But normally, the serving engine rebuilds all of it from scratch.
Each tool call in an agent's loop adds its result to the end of the context, so the prefix only gets longer as the session runs. For a long agentic workflow, this means more compute time spent on the same prefix again and again.
Longer latency. Longer TTFT.

## Prefix caching for accelerating agentic inference
Long-shared prefixes create significant overhead in agentic workflows, but there are opportunities to reduce it and generate responses faster.
Before a model can generate anything, it must first process the prefix and build the KV cache. This process is called prefill, and for long prompts, it can account for a significant portion of TTFT. Queueing, scheduling, and network overhead make up the rest. And under load, queueing is frequently the larger share. 
That's exactly where prefix caching comes into play. Prefix caching reuses cached KV state for matching prompt prefixes, allowing the serving engine to skip prefill computation for cached tokens and compute only the uncached suffix. It's a technique that significantly improves TTFT for exactly this kind of workload, with multi-turn chat and agentic tool-calling among the clearest cases. 
Without cache reuse, the engine recomputes KV state for the entire prompt before the first token appears. With it, cached tokens are skipped and prefill covers only the uncached suffix.
However, a warm cache sitting on one node is only useful if the next call actually lands there. Without prefix-aware routing, every inference request rebuilds the KV cache from the beginning of the prompt—even when nearly all of those tokens are identical.
To help speed up TTFT, you need more than good caching; you need efficient routing.

## Prefix caching needs prefix-aware routing
A basic load balancer sends each request to whichever replica is free, with no awareness of which session it belongs to or where its cache lives. That's a cache miss waiting to happen. 
Prefix-aware routing considers which workers already hold reusable KV state for a request's prefix and routes accordingly, while balancing cache reuse against current worker load. That's exactly why routing matters as much as caching does.
- Without it: Every turn triggers a full recompute of an ever-growing prefix, and TTFT gets worse the longer the session runs, not better. 
- With it: Requests are preferentially routed to a worker already holding a matching prefix, so prefill covers only the new tokens, and TTFT tracks the size of the new content rather than the length of the whole history.
Take a look at the diagram below to visualize the difference.
A load balancer with no view of cache state scatters an agent's turns across workers, forcing a full recompute each time. Prefix-aware routing sends each call to a worker already holding reusable KV state, so prefill covers only the new tokens.

## Infrastructure has to support that behavior at scale
Prefix caching and cache-aware routing reduce unnecessary computation in agentic inference. Now, the infrastructure supporting the agent in production must maintain those benefits as workloads grow, traffic fluctuates, and deployments scale.
Four things matter in practice:
- Route requests to cached prefixes
Prefix-aware routing considers which workers already hold reusable KV state for a request's prefix and routes accordingly. That's a different question than "which session is this?" What matters is which worker has the greatest useful prefix overlap.
- Preserve cache locality as the system scales out
As inference expands across more GPUs and nodes, cached prefixes become distributed across more workers. Infrastructure needs to know where reusable KV state lives and preserve locality as capacity changes, minimizing unnecessary recomputation and expensive cache movement.
- Balance cache locality against load
The worker with the most reusable KV state isn't always the best destination. If that worker is overloaded, waiting for it can cost more than recomputing part of the prefix elsewhere. Therefore, routing and scheduling need to balance cache affinity with queue depth and available capacity to optimize overall latency and throughput.
- Measure whether it’s working
Metrics like cache hit rate, TTFT, routing behavior, and latency percentiles help teams verify that requests are reaching warm replicas and identify where recomputation is occurring. Observability makes it possible to identify cache misses before they become user-visible performance problems.
None of this is optional at production scale. It's what separates infrastructure that happens to run agents from infrastructure built for how agents actually behave.

## What this means for agentic inference in production
Prefix caching can dramatically reduce the work required for agentic inference, but only when the infrastructure supports it as workloads scale and traffic patterns change. Routing, scheduling, scaling, and observability all contribute to whether cached prefixes are reused or recomputed.
As agent workflows become longer and context windows continue to grow, those infrastructure decisions have an increasingly direct impact on latency, GPU efficiency, and cost. That's why infrastructure built for agentic inference has to understand more than GPUs and load balancing. It has to understand the structure of the workload itself.
CoreWeave Inference is designed around these execution patterns, combining prefix-aware routing, efficient scheduling, and observability to maximize cache reuse across production agent workloads. In the next and final blog of this series, we’ll take a closer look into how CoreWeave Inference supports agentic workflows in production.
To learn more:
- Read the blog: Your Agent Is Only as Good as Your Infrastructure
- Read the blog: From Experimentation to Production: Why Inference Is the Defining Layer of AI
- Watch the demo: How Reinforcement Learning Improves AI Agent Reliability in Production
- Read the blog: Why Inference Latency and Availability Drift in Production

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
