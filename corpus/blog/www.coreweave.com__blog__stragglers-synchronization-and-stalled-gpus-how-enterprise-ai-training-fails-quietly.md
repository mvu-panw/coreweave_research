# GPU Stragglers and Training Failures Explained

Source: https://www.coreweave.com/blog/stragglers-synchronization-and-stalled-gpus-how-enterprise-ai-training-fails-quietly

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Your dashboard says the GPUs are allocated. Your model progress says otherwise.
This is one of the most expensive failure modes in large-scale AI training. Nothing looks obviously broken, the cluster is up, the job is running—even the GPU utilization charts may look healthy at a glance. But step time creeps, throughput drifts, checkpoints take longer than expected, and your engineers spend more time triaging than improving the model.
The job may eventually finish, but that doesn’t mean it’s running at scale.
At enterprise scale, training is more than just compute. Every GPU, node, network path, data loader, storage system, and collective communication pattern has to stay aligned long enough for useful work to happen. When that coordination starts to degrade, the symptoms can be subtle: lower throughput, slower iteration, higher GPU-hour burn, and unstable performance.
That is what “quiet failure” looks like in AI training. The system appears healthy, but doesn’t deliver progress at the rate the business requires.

## The three conditions for quiet failure
Three patterns show up again and again in large-scale distributed training: stragglers, synchronization stalls, and stalled GPUs.
They’re different problems, but they create the same business outcome: expensive compute that’s allocated but not fully utilized.

### 1. Stragglers: the slowest rank sets the clock
In distributed training, a single slow rank can slow down the entire job. If one process falls behind, everything else has to wait for it to complete.
Stragglers can show up as step time creep, intermittent tail latency, or a throughput regression that seems to appear without a reason. The root cause might be: 
- A degraded GPU or node
- ECC errors
- Thermal throttling
- A NIC or PCIe anomaly
- Uneven data shards
- Dataloader jitter
- CPU contention during preprocessing.
The hard part is that many infrastructure monitoring systems are designed to check only whether or not a node is healthy. But when training at a large, distributed scale, the more important question is often: is this rank slowing the job?
Recent research on large-scale GPU training clusters from Ziteng Chen et al. illustrates the challenge1. The research found that NCCL has limited tolerance for certain NIC failures and that NCCL “lacks a native fault tolerant mechanism,” which can force relaunches of collective communication and waste GPU time when failures occur. NVIDIA has also continued to introduce NCCL capabilities aimed at runtime scaling and fault tolerance, which underscores how central collective communication resilience has become to modern AI workloads.
For platform teams, the practical signal isn’t just average utilization. It’s multiple signals taken in aggregate: per-rank step time, p50 and p95 latency, communication time versus compute time, GPU occupancy, memory copy behavior, and input pipeline stalls.

### 2. Synchronization stalls: when communication becomes the job
All-reduce, all-gather, reduce-scatter, and other collective operations are the heartbeat of large-scale training. As models grow and teams use more forms of parallelism, including data, tensor, and pipeline parallelism, communication becomes a larger share of the workload.
That makes jitter expensive.
A small amount of network variability can become a large amount of training inefficiency. Network oversubscription, topology mismatch, mis-tuned NCCL settings, cross-zone placement, shared fabric contention, or inconsistent routing can all show up as oscillating throughput or periodic hangs.
This is one reason generic cluster-level health can be misleading. GPUs may appear “utilized,” while spending too much time blocked on collective waits instead of advancing the training step.
A useful diagnostic lens is to break the job down into compute, communication, and input. If communication time rises while model code and data remain unchanged, the issue may not be the model. It may be the coordination fabric around it.

### 3. Stalled GPUs: allocated capacity that never becomes work
The third pattern is simpler to describe and painful to pay for: GPUs are allocated, but useful work is delayed.
This can happen before the job reaches steady state, during checkpointing, or whenever the data path can’t keep the accelerator fed. Storage latency spikes, metadata bottlenecks, small-file storms, checkpoint storms, scheduler backpressure, preemption behavior, or slow environment readiness can all create delays where capacity exists but progress pauses.
From an executive perspective, this is where cost starts to rise faster than model quality. The spend is increasing, but the progress isn’t.
The practical metrics are time to steady state, I/O latency during step spikes, checkpoint duration, checkpoint variance, and the frequency of pauses across the run.

## “It finishes” is not the same as “it scales”
Traditional infrastructure signals can create false confidence.
Cluster health doesn’t equal workload performance. A successful job doesn’t mean the job achieved its goodput, quality, or throughput target. And high allocation doesn’t mean high efficiency.
For AI leaders, three metrics help make the issue practical:
- Goodput: useful work delivered versus requested compute.
- Learning velocity: the rate of model-quality improvement per dollar of compute consumed.
- MFU: model FLOPs utilization, or the share of allocated compute that actually advances training.
These metrics translate technical performance into business outcomes. Goodput supports forecastability for finance. MFU supports repeatability for moving from POC to product. Learning velocity supports roadmap delivery because it shows how quickly spend becomes insight.
This is also where AI infrastructure becomes a board-level issue. When distributed training is inefficient, budget overflow isn’t the only red flag higher-ups see. Delayed experiments, slower model improvement, and wasted engineering cycles can all create grumbles about your AI initiative in the boardroom.

## Detection helps. Architecture matters more.
The industry is paying more attention to stragglers, stalls, and training hangs, and for good reason—they’re expensive, hard to isolate, and easy to miss until after you’ve already wasted GPU-hours. But detecting a slowdown after it appears isn’t the same as architecture running training predictably.
A detection-led approach can identify symptoms. Those signals are useful, but they often arrive after useful work has already been lost. The harder and more valuable problem is preventing localized issues from compounding across the training job.
This requires more than monitoring. It requires an environment designed to reduce the likelihood of coordination failures in the first place, with architectural control across:
- Placement
- Networking
- Storage
- Scheduling
- Observability
- Workload operations.

## CoreWeave Cloud: purpose-built to reduce coordination failures
CoreWeave Cloud is designed for the demands of AI workloads, with infrastructure, orchestration, operational control, storage, networking, observability, and developer workflows integrated across the AI lifecycle. For large-scale training, that integration matters because coordination failures rarely originate in one isolated layer. A slow rank, stalled collective, checkpoint delay, placement issue, or storage bottleneck can all send unpleasant ripple effects through your run.
CoreWeave Cloud addresses coordination as a platform-level challenge, helping reduce variance across the infrastructure and operational layers that determine training performance.
For large-scale training, that matters in three ways.

### Reliability: reduce variance before it compounds
Distributed training is sensitive to small anomalies. A degraded component does not have to fail outright to hurt performance. It only has to introduce enough latency, jitter, or inconsistency to slow the job.
CoreWeave’s purpose-built architecture gives platform teams more control over the conditions that shape training performance, including how: 
- Workloads are placed
- Failure domains are managed
- Resources are scheduled
- Storage and networking behave under load
- Remediation workflows are triggered when anomalies emerge
Rather than flagging a problem after it has drained GPU hours, we aim to mitigate the issues that cause coordination failures in the first place, identify degraded resources earlier, and contain localized issues before they spread across the run. For example, CoreWeave offers HPC Verification, a system that runs proactively on idle compute nodes to catch and fix issues like silent data corruption, performance regressions, and thermal deficiencies before they affect workloads.

### Transparency: see from metal to model
Infrastructure uptime is a must, but AI teams who want to train well and within budget need workload-level visibility.
A training slowdown is rarely explained by a single metric in a single dashboard. It may involve a node event, network jitter, NCCL slowdown, dataloader queue, storage latency spike, checkpoint variance, or placement decision. Without a correlated view across those layers, teams are left stitching together partial signals while the job continues to burn compute.
CoreWeave Cloud is built to provide deeper visibility across the infrastructure and workload stack. Capabilities like Grafana overlays and alert templates that point directly to the root cause of GPU stragglers, and Telemetry Relay, which streams audit and access logs from CoreWeave services into a customer’s SIEM or observability tools, help you connect what’s happening in your training loop with what’s happening at the compute, network, storage, and orchestration layers.
That cross-layer view is critical. It helps teams distinguish a system regression from a model regression, isolate the source of performance degradation faster, and understand whether allocated compute is actually turning into useful work.

### Insights: turn signals into action
The most valuable observability does not stop at “something is slow.” AI training teams need more specific answers: this rank is slow, this node is degraded, this data input pattern is starving GPUs.
CoreWeave’s operating model is designed to turn those signals into action. By connecting reliability, transparency, and workload operations, CoreWeave Cloud helps teams move from detection to diagnosis to remediation faster. Because the longer a coordination issue persists, the more it compounds across GPU-hours, checkpoints, reruns, engineering time, and roadmap delays.
That is the difference between monitoring infrastructure and operating AI. A detection-led model tells teams when training has slowed. A purpose-built AI cloud helps reduce the conditions that cause training to slow in the first place, and helps contain the impact when anomalies do occur.

## The real decision: consume compute or deliver progress?
For enterprise AI teams, provisioning compute is just the first step. After that, progress against your roadmap depends on running training predictably.
When teams are iterating on a prototype, they can absorb coordination failures. But as they scale, coordination failures become the primary bottleneck to predictable training. Stragglers slow down jobs. Synchronization stalls make a workload out of communication. Stalled GPUs turn allocated capacity into wasted spend. And every delay compounds across experiments, checkpoints, reruns, and releases.
With the right signals, teams can diagnose, measure, and mitigate these quiet failures. But why settle for solving the problem after the fact—the right platform, built from the ground up to address the coordination demands of AI, can stop them from happening in the first place.
CoreWeave Cloud helps AI teams deliver predictable training performance: more useful work from requested compute, higher utilization of the infrastructure already provisioned, and faster learning velocity from every dollar spent.
For more on how CoreWeave is built for real model progress, not just allocated capacity, watch our webinar, “Stragglers, Stalls, and Restarts: Why AI Training Throughput Breaks Down at Scale.”
Want to learn more about how CoreWeave is setting new industry standards for performance, reliability, and transparency? Find out why we were the only AI cloud provider to win SemiAnalysis’ coveted ClusterMAX™ Platinum rating—twice. If you’d like to learn more about our approach to distributed AI training at scale, visit our AI model training solution page.
1Ziteng Chen, et al. “An Efficient, Reliable and Observable Collective Communication Library in Large-scale GPU Training Clusters” arXiv, 2025. https://arxiv.org/html/2510.00991v1#S2

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

Training,

Copy code

Copied!

Training,
