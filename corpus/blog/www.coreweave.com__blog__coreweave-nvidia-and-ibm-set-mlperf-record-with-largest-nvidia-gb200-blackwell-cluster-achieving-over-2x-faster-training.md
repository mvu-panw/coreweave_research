# CoreWeave, NVIDIA, and IBM Set MLPerf Record with Largest NVIDIA GB200 Blackwell Cluster, Achieving Over 2× Faster Training

Source: https://www.coreweave.com/blog/coreweave-nvidia-and-ibm-set-mlperf-record-with-largest-nvidia-gb200-blackwell-cluster-achieving-over-2x-faster-training

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

CoreWeave, NVIDIA, and IBM delivered the largest-ever MLPerf® Training v5.0 submission on NVIDIA Blackwell using 2,496 NVIDIA Blackwell GPUs, achieving more than 2x faster training performance than NVIDIA Hopper-based systems at the same cluster size1. By uniting NVIDIA’s cutting-edge GB200 NVL72 platform, CoreWeave’s purpose-built AI cloud platform, and IBM’s pioneering approach to advanced AI workloads, this collaboration established a new benchmark for speed and scalability in foundational model training. CoreWeave is proud to be the cloud services provider to submit the fastest training results on the Llama 3.1 405B benchmark and the largest NVIDIA Blackwell cluster submission, setting a new industry benchmark. These results build on CoreWeave’s industry-leading performance in MLPerf Inference v5.0, reinforcing the benefits of our AI-optimized infrastructure for customers building, fine-tuning, or deploying AI-powered applications.
‍

## CoreWeave’s leadership in MLPerf v5.0
MLPerf is an industry-standard benchmark suite developed by MLCommons to evaluate machine learning training and inference performance. It measures how quickly a system can train leading open-source models to a defined quality target and serves as a fair and transparent way to compare AI infrastructure across providers. In MLPerf Training v5.0, MLCommons introduced a new benchmark: Meta’s Llama 3.1 405B model, the largest and most complex foundational model in the benchmarking suite. 
‍

### The largest-ever NVIDIA Blackwell submission
The joint submission by CoreWeave, NVIDIA, and IBM achieved the largest MLPerf Training submission ever recorded, utilizing 2,496 NVIDIA Blackwell GPUs across 39 racks, each containing 64 active GPUs, hosted on CoreWeave’s infrastructure. This submission was over 34x larger than the only other submission on the NVIDIA GB200 Grace Blackwell instance from a cloud provider (single rack with 72 GPUs) and 4.8x larger than the next largest entry (NVIDIA’s solo submission with 512 Blackwell GPUs), shown in Image 1 below. This submission is equivalent in computing power to more than 5,000 NVIDIA H100 GPUs7, making it the largest training benchmark CoreWeave has delivered to date. It surpasses our previous MLPerf Training v3.1 3,584-GPU H100 submission, highlighting the exceptional scale and capacity of our cloud platform.
Image 1: CoreWeave, NVIDIA, and IBM published the largest NVIDIA Blackwell MLPerf submission at 2,496 NVIDIA Blackwell GPUs
In addition to superior performance, the GB200 NVL72 system provides significant advantages in infrastructure density. Our 2,496 Blackwell GPU submission required just 39 racks, whereas an equivalent H100 setup (based on comparable performance and a standard 32-GPUs-per-rack configuration) would have required around 156 racks. This represents a 4x reduction in physical space, highlighting not only the performance improvements delivered by GB200 NVL72 but also the substantial infrastructure efficiency and energy savings enabled by higher-density configurations.
This submission ran on the Carina cluster, a large NVIDIA Blackwell GPU cluster built and delivered by CoreWeave for IBM with technical expertise from NVIDIA for the benchmarking. CoreWeave’s AI infrastructure handled multiple training runs at scales above 1,000 GPUs with high reliability. At 2,496 GPUs, Carina is currently one of the largest operational Blackwell clusters in the world and demonstrates CoreWeave’s ability to deliver and run large-scale AI infrastructure at the production level.
‍

### The fastest cloud service provider submission
CoreWeave’s MLPerf Training v5.0 results show Blackwell GPUs deliver at least 2x faster training performance than Hopper systems at the same cluster size (see Image 2). Our largest submission achieved 91% scaling efficiency from 512 to 2,496 GPUs, enabling faster turnaround for large-scale training workloads. We anticipate further improvements in training performance through ongoing software and system-level optimizations, with GB200's performance advantages becoming even more pronounced for large-scale, multi-trillion parameter distributed training workloads.

Image 2: CoreWeave, NVIDIA, and IBM Blackwell GPU submissions are faster than all other comparable submissions by at least 2x
‍
When comparing similar-sized clusters, CoreWeave’s GB200 cluster delivered the fastest training times for Llama 3.1 405B not only in one configuration but also across five cluster configurations. Table 1 below summarizes these key results.
Table 1: CoreWeave leads MLPerf Training v5.0 for Llama 3.1 405B benchmark
‍

## History of setting MLPerf Records
Earlier this year, CoreWeave was the first cloud provider to submit MLPerf Inference v5.0 results using NVIDIA GB200 Grace Blackwell Superchips, achieving the fastest per-chip inference throughput of over 200 tokens per second (TPS) on the Llama 3.1 405B model, a 2.86X per-chip performance increase compared to NVIDIA H200 GPUs. Additionally, CoreWeave's NVIDIA H200 GPU instances delivered 33,000 TPS on the Llama 2 70B model, marking a 40% improvement over NVIDIA H100 GPUs in previous submissions.
With the launch of H100 GPUs in 2023, CoreWeave was among the first providers to offer NVIDIA H100 GPUs and achieved a record-breaking MLPerf Training v3.0 result by completing the GPT-3 175B model benchmark in under 11 minutes using more than 3,500 NVIDIA H100 GPUs. The result was 29 times faster and four times larger in scale than the next closest competitor, setting the stage for CoreWeave’s leadership in high-performance AI training at unprecedented scale.
‍

## Groundbreaking performance for your AI innovations 
CoreWeave delivered top MLPerf Training v5.0 results based on our singular focus on building the best cloud platform for AI workloads, with deep performance optimizations throughout the stack, coupled with rigorous attention to cluster reliability and resilience.
CoreWeave Kubernetes Service (CKS) and Mission Control deliver deep observability, bare-metal performance isolation, and proactive infrastructure management, maintaining up to 96% goodput for large-scale training workloads. Benchmarks ran on SUNK, CoreWeave’s Slurm-on-Kubernetes solution, which intelligently schedules jobs within GB200 NVL72 systems for optimal rack-level training efficiency over NVIDIA NVLink™.
With record-setting cloud performance on the Llama 3.1 405B benchmark and the largest-ever NVIDIA Blackwell GPU cluster submission, CoreWeave continues to redefine industry standards for AI infrastructure. These groundbreaking MLPerf results demonstrate our unmatched ability to deliver the scale, speed, and efficiency needed for next-generation AI workloads. 
Explore our detailed MLPerf Inference 5.0 results, or connect with our sales team today to discover firsthand the transformative power of the industry's best purpose-built AI cloud.‍
‍
‍
1Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.
2The IBM + CoreWeave + NVIDIA 2,496 Blackwell training submission for the Llama 3.1 405B benchmark completed in 27.33 minutes, 2.1x faster than NVIDIA’s larger 2,560 x H100 GPU submission.
3The IBM + CoreWeave + NVIDIA 2,048 Blackwell training submission for the Llama 3.1 405B benchmark, completed in 32.6 minutes, 2.15x faster than NVIDIA’s 2,048 x H100 GPU submission. 
4The IBM + CoreWeave + NVIDIA 1,536 Blackwell training submission for the Llama 3.1 405B benchmark completed in 42.46 minutes, 2.85x faster than our own 512 x Blackwell GPU submission.
5The IBM + CoreWeave + NVIDIA 1,024 Blackwell training submission for the Llama 3.1 405B benchmark completed in 62.1 minutes, 2x faster than the top 1,024 x NVIDIA H200 GPU submission. 
6The IBM + CoreWeave + NVIDIA 512 Blackwell training submission for the Llama 3.1 405B benchmark completed in 121.1 minutes, 2x faster than the top 512 x NVIDIA H200 GPU submission. 
7Assuming a training speed up of 2.15X2 for the Llama 3.1 405B benchmark on NVIDIA GB200 over the fastest NVIDIA H100 GPU submission.

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
