# CoreWeave Leads MLPerf 0.7 Endpoints | CoreWeave Blog

Source: https://www.coreweave.com/blog/coreweave-leads-mlperf-endpoints-benchmark-with-deepseek-r1

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## CoreWeave Leads MLPerf 0.7 Endpoints Benchmark with DeepSeek-R1
CoreWeave delivered leading results in the inaugural MLPerf® 0.7 Endpoints benchmark, running the frontier DeepSeek-R1 reasoning model on 68 NVIDIA Blackwell GPUs in a NVIDIA GB200 NVL72 system. CoreWeave sustained 441,740 output tokens per second of system throughput at 16,384 concurrent requests1, and  up to 6,496 tokens per second per GPU2. Throughput per GPU is the metric that most directly reflects the economics of a real inference service, because it maps to tokens served per accelerator and cost per GPU.

### What this means for inference
- Sustained performance, not a burst number: plan capacity and cost models around steady-state serving, not a best-case spike that won't hold in production
- Fewer GPUs, more throughput: customers can hit the same or higher token output with a smaller, less expensive GPU footprint
- Better GPU economics at peak concurrency: higher throughput per GPU at the highest concurrency tested means more tokens served per accelerator-hour as traffic scales up
- Less over-provisioning, more usable capacity: skip the extra GPU headroom and retry logic teams typically budget to compensate for dropped requests under load

### The inaugural MLPerf 0.7 Endpoints test
Endpoints is MLCommons' newest benchmark, built to measure what earlier training and inference test suites don't: how an inference service behaves under realistic, concurrent, online load. It reports the full throughput-versus-latency curve at scale, up to 16,384 concurrent requests, rather than a single data point.
The benchmark also raised the bar on model difficulty by including DeepSeek-R1, a 671-billion-parameter mixture-of-experts reasoning model that emits thousands of tokens per response and is the hardest serving workload in the suite.

### Tested on production infrastructure, not a lab environment
A benchmark number is only as credible as the environment it ran on. Instead of creating an isolated environment tuned to produce one clean number, CoreWeave validated its results the same way it validated NVIDIA GB200 NVL72 for training: following NVIDIA’s reference designs and on a standard production cluster.
DeepSeek-R1 ran on the same network fabric, scheduler, storage, and CoreWeave Mission Control orchestration that customers use for their own workloads, with no separate benchmark cluster spun up for the occasion. The reference configuration for this workload targets a full 18-node, 72-GPU rack; CoreWeave submitted results on 17 nodes, leveraging 68 Blackwell GPUs in a GB200 NVL72 rack.
CoreWeave Mission Control's continuous telemetry, predictive failure detection, and automated GPU straggler detection run under every production cluster, this one included, so the throughput numbers reflect what the cluster does over time, not what it can do once.

### Why per-GPU throughput and time per output token matter
DeepSeek-R1 is a reasoning model. A single response can run thousands of output tokens, and CoreWeave's runs averaged well over 2,000 tokens per request. For reasoning models, two metrics decide both the end-user experience and the cost to deliver it: throughput per GPU and time per output token (TPOT).
Throughput per GPU is the efficiency and cost story. TPOT is how fast the response streams once it starts; for long reasoning outputs, it dominates end-to-end latency, so it's what the user actually feels. Under maximum concurrency, CoreWeave held one of the lowest TPOTs in the round while carrying more load per GPU. MLPerf Endpoints scores the whole throughput-versus-latency curve for exactly this reason, not a single point on it.

### The CoreWeave Cloud behind these results
CoreWeave Cloud is built as a unified stack, with performance optimizations across every layer from metal to model. This benchmark ran on that same stack, not a separate configuration assembled to produce one clean number:
- CoreWeave Bare Metal servers provide direct access to GPU computing resources without a hypervisor layer, removing the overhead and latency a virtualized environment would add to the serving path.
- CoreWeave Networking built on NVIDIA Quantum-2 InfiniBand, ties every GPU in the rack together with the bandwidth multi-node serving required as concurrency and context length grow.
- CoreWeave Kubernetes Service (CKS) provides the base runtime environment for the cluster and is fully integrated with CoreWeave Mission Control to minimize overhead and maximize compute performance.
- CoreWeave SUNK enables topology-aware scheduling, so serving workloads land on GPUs positioned to minimize cross-node communication overhead.
- CoreWeave Distributed File Storage (DFS) delivers the high-throughput, low-latency shared filesystem access DeepSeek-R1's weight loading needs across all 68 GPUs, without the node-to-node contention a standard shared volume would introduce.
This same stack is also what runs CoreWeave AI Inference in production. Teams choose the execution path that matches the workload: 
- Serverless Inference for pay-per-token access to a curated open-source model catalog with no clusters to manage.
- Dedicated Inference for lifecycle-supported execution of custom weights with explicit GPU and runtime control.
- Inference on CKS for fully self-managed serving with complete Kubernetes-native control.

DeepSeek-R1 ran on the identical bare metal, networking, CKS, SUNK, and storage layers above, not a separate path spun up for the test. Because all three paths share that same foundation, teams get the same predictable performance whether they're testing a model on Serverless Inference or running it at this scale on Dedicated Inference, and they can move between paths as workloads grow without replatforming.
Read how CoreWeave Sets New AI Training Records in MLPerf Training v6.0
See why CoreWeave is the only AI cloud leading MLPerf 6.0 in training and inference
‍

1 MLPerf Endpoints v0.7 DeepSeek-R1 671B, published July 28, 2026; retrieved from Coreweave in July 2026. Result 0.7 6535925d-129c-42f5-b5a8-5fb6211e0e4c, Run ID 6646e4e5-afd0-4442-a52c-fd2f2aa06315. Result concurrency = 16,384 queries, TTFT P95 = 5.77 s, System TPS = 441,740 aggregate tokens/sec. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

2 MLPerf Endpoints v0.7 DeepSeek-R1 671B, published July 28, 2026; retrieved from Coreweave in July 2026. Result 0.7 6535925d-129c-42f5-b5a8-5fb6211e0e4c, Run ID 6646e4e5-afd0-4442-a52c-fd2f2aa06315: concurrency = 16,384 queries, unverified results 6,496 tokens per second per GPU. Throughput per GPU is an unverified metric derived by dividing System TPS by GPU count (68). The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

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
