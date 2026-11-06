# NVIDIA H100 Benchmarks for Large-Scale Training | CoreWeave

Source: https://www.coreweave.com/blog/nvidia-h100-gpu-benchmark-results-what-we-learned-from-large-scale-gpu-testing

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### The real bottleneck isn't TFLOPs. It's maintaining both performance AND reliability at scale.
We all celebrate bigger model parameters and faster GPUs, yet production training runs fail not just from lack of compute but from the compound effect of interruptions and inefficiencies. 
When large-scale training runs crash every eight hours (0.33 days MTTF at 1,024 GPUs, according to a leading AI lab’s “Revisiting Reliability” paper), you lose days to reloads and wasted steps. And when Model FLOPs Utilization (MFU) drops to 35–45% (as is common) your effective speed is cut in half.

## A recent foundation model training report crystallized the challenge
When a leading AI lab published their training report, documenting hundreds of unplanned interruptions over 54 days at 16K GPUs, it offered rare transparency into large-scale training challenges. This level of openness underscored a critical industry need: infrastructure that delivers both power and stability under sustained, intense workloads.
The dual challenge of reliability and performance became our engineering mandate.

## Our six-week benchmarking study: Can purpose-built infrastructure solve both?
We designed a comprehensive benchmark to rigorously test our hypothesis. The study parameters:
- Model: 30-billion parameter Llama 3-style architecture
- Scale: Up to 1,024 NVIDIA H100 GPUs
- Dataset: 2 trillion tokens from Dolma v1.6
- Framework: Production Megatron-LM
- Metrics: MTTF, ETTR, MFU, checkpoint performance, tokenization throughput
This wasn’t a lab-only synthetic test. We ran production-scale training on a real model, with real training data, to measure real-world performance.

## The infrastructure architecture: Every layer optimized for AI
Our goal was to optimize GPU clusters to achieve superior speed, efficiency, and reliability—without cutting into performance. Our approach addressed known bottlenecks systematically:

#### Hardware layer
- Bare-metal NVIDIA H100 GPU clusters eliminating hypervisor overhead, with NUMA pinning under our control.
- Dual-fabric architecture: NVIDIA Quantum InfiniBand for all-reduce operations, separate NVIDIA BlueField DPU-offloaded Ethernet for storage traffic, preventing network contention.

#### Orchestration layer
- SUNK (Slurm on Kubernetes): Topology-aware scheduling with health probes that evict failing nodes before they impact jobs.
- Automated re-queue: Failed processes restart in ~90 seconds instead of 4+ minutes of manual triage.

#### Storage and checkpointing
- Tensorizer-based async checkpointing: Reduced save time from 129 seconds to 17 seconds while maintaining 99%+ compute utilization.
- Custom gpt_bpe tokenizer achieving 63M tokens/second—6–12x faster than HuggingFace Tokenizers.

## A defining moment: The 2:17 a.m. non-incident
During a 512-GPU run at 2:17 a.m., our on-call engineer’s phone stayed silent. SUNK had automatically:
- Detected a failing node via health probes
- Evicted it from the pool
- Rescheduled the workload
- Resumed training within 3 minutes

Grafana was showing green before anyone was even alerted. This is what infrastructure-level reliability looks like.

## The results: Validated performance at scale
Our study achieved:
- 51-52% MFU on NVIDIA H100 GPUs (vs. 35-45% typically reported)
- 3.66 days MTTF at 1,024 GPUs (10x improvement over 0.33 days baseline)
- 97.5% ETTR (Effective Training Time Ratio)
- 8x faster checkpointing via async Tensorizer implementation
- 43.7% MTTF improvement projected at 16,384 GPUs vs. Llama 3's reported numbers

### Third-party validation
 We validated against published configurations:
- Compared to another AI research group: 51.9% MFU vs. their 40.43% (28% improvement)
- Compared to another leading AI lab: 49.2% MFU vs. their 41.85% (18% improvement)
- Achieved performance and reliability parity with NVIDIA DGX Cloud Benchmarking recipes 

## Business impact: Every percentage point matters
For a 30-day, 1,024-GPU training run at $2.10/GPU-hour, improving total average MFU from 42% to 51% delivers ~6,000 GPU-hours of additional effective compute worth $12,600 without changing the invoice. Combined with 10x reliability improvements, this means:
- Models reach production weeks sooner
- Engineers iterate instead of debugging
- Predictable timelines for critical projects
Our 9 percentage point MFU improvement (from 42% to 51%) translates to completing training runs 18% faster, saving nearly a week on month-long jobs.

## What's next: Extending these results
We're already applying these optimizations to NVIDIA GB200 NVL72 clusters and building live MFU dashboards for customer workloads. Our full 30-page technical report, including methodology, survival model mathematics, and raw logs, is available now.

### Ready to test these results on your models?
The data proves that infrastructure architecture matters. Our benchmark demonstrates that with the right approach, you can achieve both speed and stability at thousand-GPU scale.
Download the technical report to read the whole story. If you’re interested, schedule a deep dive with our team to learn how to apply these benchmarks to your own clusters.
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

GPU Compute,

Copy code

Copied!

GPU Compute,
