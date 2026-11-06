# CoreWeave Sets MLPerf® Training v6.0 Records | CoreWeave Blog

Source: https://www.coreweave.com/blog/coreweave-trains-deepseek-v3-in-two-minutes

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

CoreWeave ran the DeepSeek-V3 671B MLPerf® Training v6.0 benchmark in 2.02 minutes with 8,192 NVIDIA Blackwell Ultra GPUs connected with the NVIDIA Spectrum-X Ethernet networking platform, the largest cluster of its kind ever benchmarked.
In the latest MLPerf Training v6.0 round, CoreWeave set record breaking results and delivered high performance consistently across cluster sizes ranging from 64 to 8,192 GPUs using NVIDIA HGXTM B200 and NVIDIA GB300 NVL72. The benchmark was run on the same production infrastructure CoreWeave customers rely on every day, not a benchmark-only side cluster or specially tuned environment. That matters because real AI performance is not created by hardware alone. It comes from how every layer of the platform works together, from GPU infrastructure and high-speed networking to orchestration, storage, observability, and expert operations. 

## CoreWeave trains DeepSeek-V3 671B in two minutes 
No benchmark hits every layer of an AI cloud simultaneously like DeepSeek-V3. Dense matrix throughput, MoE routing efficiency, communication primitives, fault tolerance across multi-thousand GPU clusters, topology-aware sharding across NVLink, NVL72, and scale-out fabrics. It stresses all of it at once, and if your platform has a weak point, this workload finds it.

## CoreWeave submitted three GB300 NVL72 configurations on DeepSeek-V3 671B

 | Compute Platform
 | Nodes
 | GPUs
 | Time-to-train
 | Precision

 | NVIDIA GB300 NVL72
 | 2,048
 | 8,192
 | 2.02 min
 | MXFP8

 | NVIDIA GB300 NVL72
 | 1,024
 | 4,096
 | 3.09 min
 | MXFP8

 | NVIDIA GB300 NVL72
 | 512
 | 2,048
 | 5.54 min
 | MXFP8

CoreWeave scaled an 8,192-GPU GB300 NVL72 cluster connected with Spectrum-X Ethernet networking to achieve a breakthrough time-to-train of 2.02 minutes, the fastest DeepSeek-V3 671B training performance of all time, with the #1 spot across all Closed/Available-cloud submissions.
What makes this result remarkable isn't just the absolute wall clock time; it’s how our infrastructure sustained efficient performance at scale. CoreWeave was the only submitter in the v6.0 round to successfully scale a GB300 NVL72 platform beyond 2,048 GPUs on the DeepSeek-V3 benchmark. From there, we doubled the cluster size to 4,096 GPUs, and then doubled it again to 8,192 GPUs, all while maintaining an incredibly strong scaling efficiency. In practice that means customers using this popular open source model can achieve training faster and accelerate time-to-market for their AI application or agent.

## Efficient performance and scale for thousands of GPUs
CoreWeave performed benchmark testing with Llama-3.1-405B using 4,096 Blackwell Ultra GPUs and reached the reference quality target in 9.77 minutes, 2.8x faster compared to our own results from MLPerf® Training v5.0 using the same test. The result is a direct reflection of CoreWeave's full-stack engineering philosophy. The performance gain didn't come from adding more GPUs, it came from software optimizations made at every layer of the stack, from NVLink-domain aware scheduling in CoreWeave Kubernetes Service (CKS) and topology-aware workload placement in SUNK, to deep networking optimizations that keep thousands of GPUs in tight synchronization throughout a training run.

## CoreWeave’s performance with Llama-3.1-405B using 4,096 Blackwell Ultra GPUs

 | Compute Platform
 | Nodes
 | GPUs
 | Time-to-train

 | NVIDIA GB300 NVL72
 | 1,024
 | 4,096
 | 9.77 min

The run was built on NVIDIA NeMo Framework Release 26.04 and leveraged full CUDA Graphs to minimize CPU scheduling overhead and maximize GPU utilization throughout training. Tensor, pipeline, and context parallelism were carefully tuned to align with the GB300 NVL72 architecture. At the network layer, NVIDIA Spectrum-X Ethernet running RoCE provided the scale-out fabric, delivering the bandwidth, advance congestion control, and low latency communication required to maintain high efficiency during distributed training.
This GB300 NVL72 deployment achieved near-parity with larger NVIDIA GB200 NVL72 configurations while using 20% fewer GPUs. That efficiency gap of delivering comparable results with materially less hardware underscores a principle CoreWeave has built its platform around: raw compute capacity matters, but system-wide optimization is what determines real-world performance and economics. For customers training the industry's largest models at scale, that distinction translates directly into lower cost per training run, faster iteration cycles, and more efficient use of infrastructure investment.

## Consistent scaling efficiency for 64 GPU clusters  
To demonstrate that our software and infrastructure optimizations deliver results at every scale, we also submitted GPT-OSS-20B and Llama 3.1 8B benchmark results on a compact 64 GPU NVIDIA HGX B200 cluster connected via NVIDIA Quantum-2 InfiniBand. This  configuration is accessible to a much broader range of customers than frontier-scale deployments.
The results speak for themselves. GPT-OSS-20B reached the reference quality target in 26.98 minutes, while Llama 3.1 8B completed training in 16.54 minutes which was 9.7% faster than the next submitter with the same set up. 
These numbers matter because of what they reveal about where the performance is coming from. Through targeted enhancements in orchestration, communication libraries, networking, scheduling, and distributed training configuration, we extracted performance from the Blackwell platform that rivals larger or newer-generation deployments. This isn't about having access to more hardware, but it’s about making every GPU count more. 

## Under the hood: How CoreWeave platform holds efficiency at 8,192 GPUs
Building and operating a cluster of 8,192 GPUs is a different problem than running a few hundred. At this scale, performance depends on whether compute, networking, storage, scheduling, and orchestration work together as one connected platform. For MoE and dense workloads, efficient scaling requires coordinated optimizations across workload placement, fleet health, network topology, observability, and orchestration. CoreWeave Mission Control, SUNK and CKS each play key roles in making that possible. These are the areas that mattered most:

### Fleet-wide performance consistency
At 8,192 GPUs, performance requires a fleet-wide management strategy with meticulous execution. A small percentage of underperforming nodes, misconfigured NICs, a straggler GPU, or thermal anomalies can create stalls that reduce cluster-wide efficiency. This is where CoreWeave CKS matters. Providing the consistent AI substrate for large-scale training on CoreWeave, CKS provides a standardized orchestration surface for scheduling, placement, and operations, while CoreWeave Mission Control continuously validates the underlying fleet.
With CKS providing the AI substrate for workload orchestration, CoreWeave Mission Control continuously qualifies the infrastructure beneath it. By continuously performing health checks, validating hardware, firmware, network, and thermal health across the fleet, CoreWeave Mission Control ensures that large-scale training jobs run on a consistent, performance-qualified infrastructure baseline. Prior to MLPerf execution, CoreWeave Mission Control is used to:
- Verify firmware consistency across GB300 NVL72 systems, NICs, switches, and DPUs
- Confirm GPU clocks, power limits, and thermal profiles
- Identify hardware degradation or marginal links before jobs are scheduled
During operation, CoreWeave Mission Control provides fleet-wide telemetry that enables operators to detect:
- Thermal hotspots and power delivery anomalies
- Network congestion patterns
- GPU performance outliers
This becomes increasingly important for MoE workloads such as DeepSeek-V3, where synchronization latency and all-to-all communication patterns can amplify even small infrastructure inconsistencies.

### NVLink-domain-aware scheduling    
MoE workloads are extremely sensitive to communication latency and bandwidth. When expert-parallel groups are distributed across network boundaries with higher latency or oversubscribed links, all-to-all communication overhead can quickly dominate execution time, reducing scaling efficiency and overall throughput.
Running on CKS, CoreWeave SUNK is topology-aware by design. It understands the underlying NVLink, rack-scale design, and cluster fabric topology which then intelligently places workloads to maximize locality. For large-scale MoE training, SUNK preferentially co-locates expert-parallel groups within the same NVL72 domain, minimizing inter-rack communication and keeping the highest-frequency collective operations on the lowest-latency paths. The result is higher utilization, improved scaling efficiency, and more predictable performance as clusters scale from hundreds to thousands of GPUs.

### Optimized network performance
At multi-thousand-GPU scale, network performance becomes a primary determinant of overall training efficiency. Workloads such as DeepSeek-V3 generate massive volumes of latency-sensitive communication, particularly across expert-parallel groups where all-to-all exchanges occur continuously throughout training. To maximize performance, CoreWeave employs a rail-aware networking strategy that balances traffic across all available RoCE rails, ensuring bandwidth is utilized efficiently and preventing hotspots from developing within the fabric. Before large-scale jobs are launched, the team validates rail balance across the cluster and verifies that NCCL is correctly mapping GPUs to their associated host channel adapters, allowing collective communication operations to use the full available network bandwidth.

## What this means for customers
The benchmark was performed on the same connected platform our customers run on every day. So the speed, the scaling efficiency, and the consistent performance across cluster sizes are from production environments. 
For frontier-scale MoE models, CoreWeave's DeepSeek-V3 results show that our GB300 NVL72 system can maintain strong scaling efficiency even as clusters double in size  to thousands of GPUs. This means customers can accelerate training runs without seeing diminishing returns from communication bottlenecks or infrastructure constraints. Faster training translates into more experimentation, shorter development cycles, and quicker time-to-market.
For dense foundation models, our Llama 3.1 405B results show how intelligent infrastructure orchestration can materially improve training efficiency. CoreWeave reached the reference quality target in 9.77 minutes using 20% fewer GPUs than a larger GB200 NVL72 deployment, showing that performance at scale is not only about raw GPU count. For customers, that means training budgets can stretch further, GPU capacity can go further, and teams can get more value from every run.
For smaller AI models, our software stack was equally effective and came out ahead. The advantage is in how the platform runs the hardware, not the size of the cluster. Customers can leverage our performance for models and clusters of all sizes. 
To get started on CoreWeave Cloud, try CoreWeave ARENA where you can assess your workload performance and cost before committing to production. Run and evaluate your workloads in our AI lab for production readiness and gain concrete insights and recommendations designed to accelerate your path to innovation.
Find out more: 
SUNK: Scale AI Training Without Breaking Your Infrastructure
How to Maximize Resiliency with AI-Native Observability
Register to attend Fully Connected 2026‍

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
