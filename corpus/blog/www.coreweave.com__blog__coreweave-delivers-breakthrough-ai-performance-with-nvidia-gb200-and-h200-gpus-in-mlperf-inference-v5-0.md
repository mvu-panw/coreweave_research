# CoreWeave Delivers Breakthrough AI Performance with NVIDIA GB200 and H200 GPUs in MLPerf Inference v5.0

Source: https://www.coreweave.com/blog/coreweave-delivers-breakthrough-ai-performance-with-nvidia-gb200-and-h200-gpus-in-mlperf-inference-v5-0

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## CoreWeave First CSP to Submit NVIDIA Grace Blackwell Results, Achieves Top-Tier Performance in MLPerf Inference v5.0 with NVIDIA GB200 Grace Blackwell Superchips and H200 GPUs
CoreWeave is proud to be the first cloud service provider (CSP) to submit MLPerf Inference v5.0 results for NVIDIA GB200 Grace Blackwell instances, achieving an impressive 800 tokens per second (TPS) on the Llama 3.1 405B model – a 2.86X per-chip performance increase over NVIDIA H200 GPUs. CoreWeave’s NVIDIA H200 GPU instances also delivered 33,000 TPS on the Llama 2 70B model, marking a 40% improvement in throughput compared to NVIDIA H100 instances. This milestone highlights our commitment to providing customers with early access to the latest NVIDIA GPUs and delivering industry-leading performance. ‍

## Continuing Our Track Record of MLPerf Milestones‍
MLPerf Inference is an industry-standard suite that measures machine learning performance across realistic deployment scenarios. The speed at which systems process inputs and generate outputs using a trained model significantly impacts performance and, thus, user experience, making the MLPerf Inference benchmark a critical metric for both CoreWeave and our customers. Historically, CoreWeave has set record-breaking MLPerf results, including our 2023 submission, which showed 29x faster training performance than the next best competitor. 

In this year’s submitted MLPerf results, CoreWeave's NVIDIA GB200 Superchip and CoreWeave’s NVIDIA H200 GPU instances showed impressive performance, summarized in the table below:
‍

Table 1: CoreWeave leads MLPerf benchmarks for NVIDIA H2007 and NVIDIA Blackwell GPUs8

## NVIDIA GB200 NVL72: CoreWeave Sets a New Benchmark for Industry-Leading Performance‍
The latest MLPerf release was the first to include the Llama 3.1 405B model — one of the largest open-source models. We achieved over 800 tokens per second in a GB200 instance featuring two NVIDIA Grace™ CPUs coupled with four Blackwell GPUs.
While some of the performance improvement can be attributed to the lower precision (FP4) of the NVIDIA Blackwell MLPerf Inference benchmark, we see a 2.86X speedup on a per-chip basis. We reached a normalized per-chip throughput of over 200 TPS compared to 70 TPS for NVIDIA’s H200 MLPerf Inference v5.0 submission.
Image 1: NVIDIA GB200 Instances on CoreWeave achieved a 2.86X speed-up over NVIDIA’s H200 MLPerf Inference v5.0 submission for the Llama 3.1 405B model on a per-GPU basis8

## NVIDIA H200 GPUs: CoreWeave Achieves Top-Tier Llama 2 70B Throughput
The latest MLPerf release continues to support Llama 2 70B. Unlike the larger Llama 3.1 405B model, its smaller memory footprint allows throughput comparisons between the NVIDIA H200 and H100 GPUs.
CoreWeave delivers top-tier Llama 2 70B throughput on NVIDIA H200 GPUs in the MLPerf Server scenario, which has tighter latency constraints. CoreWeave achieved 33,000 tokens per second — 40% higher throughput than the fastest NVIDIA H100 GPU inference submission for the same model in MLPerf Inference v4.1. 
‍
Image 2: NVIDIA H200 GPUs on CoreWeave achieved 40% higher throughput over NVIDIA’s H100 MLPerf Inference v4.1 submission for the Llama 2 70B model7

## How CoreWeave Cloud Optimizes AI Inference Performance‍
The CoreWeave Cloud Platform is purpose-built for AI inference, delivering industry-leading performance as demonstrated by our MLPerf Inference v5.0 results. Every layer of our stack — data centers, infrastructure, managed services, and application software services — is optimized to maximize throughput and efficiency.
Our cutting-edge infrastructure features the latest NVIDIA GPUs, high-performance CPUs, and NVIDIA Quantum InfiniBand networking, all of which help reduce communication overhead and accelerate large-model inference.
CoreWeave Mission Control helps ensure all compute resources operate at peak performance with advanced cluster validation, proactive health monitoring, and rapid node replacement, reducing hardware failures, and therefore sustaining higher inference throughput. CoreWeave Kubernetes Service (CKS) runs directly on bare metal, supporting any K8s-based inference engine.
For Application Software Services, Slurm on Kubernetes (SUNK) enables efficient scheduling across 32,000+ GPUs, optimizing node-to-node communication with topology-aware scheduling. The SUNK Scheduler enhances cluster utilization by dynamically scheduling Kubernetes pods and Slurm jobs side by side within the same cluster, increasing flexibility and reducing serving costs. CoreWeave Tensorizer further accelerates model loading, minimizing time-to-first-token for faster inference.
These optimizations drive best-in-class AI performance, resilience, and usability, which is why top AI companies like Cohere, Mistral, and IBM trust CoreWeave as their AI cloud provider.

## Looking Ahead
Performance and reliability are critical to AI labs and enterprises building world-changing technology. Today's MLPerf benchmarks demonstrate CoreWeave’s continued commitment to improving AI systems' performance and accelerating our clients’ AI ambitions. 
Results at a glance:
- CoreWeave is the first CSP to submit MLPerf results for NVIDIA Grace Blackwell Superchips, continuing our track record of providing early access to leading-edge technology, as demonstrated with the H100.
- 2.86X performance improvement per GPU for NVIDIA Grace Blackwell Superchips (compared to the previous generation of NVIDIA H200 GPUs) 
- 40% faster throughput for NVIDIA H200 GPUs (compared to the previous generation of NVIDIA H100 GPUs in the MLPerf Inference v4.1 submission for the Llama 2 70B model7)
‍
Learn more about how CoreWeave can support your AI needs with NVIDIA Blackwell and H200 GPUs.
‍
‍
1 Node with 8 x NVIDIA H200 GPUs, each with 141GB of HBM3e memory.
2 Node with 4 x NVIDIA Blackwell GPUs, as a part of 2 x NVIDIA GB200 Grace Blackwell Superchips each with 372GB of HBM3e memory.
3 Input/output tokens, precision, and batch sizes are defined by MLPerf for each benchmark.
4 H200 benchmark numbers are displayed for the Server scenario, and GB200 benchmark numbers are displayed for the Offline scenario respectively. 
5 The fastest Llama 2 70B Server scenario submission with H100s in MLPerf Inference v4.1 (Supermicro) achieved ~23,700 TPS at FP16 precision, compared to FP8 for our v5.0 submission.
6 The 2.86x speedup of GB200 over H200 for the Llama 3.1 405B model is measured on a per-GPU basis against NVIDIA’s MLPerf Inference v5.0 submission with 8 x NVIDIA H200 GPUs at FP8 precision.
7 Verified MLPerf® score of v5.1 Inference Closed Llama 2 70B server. Retrieved from https://mlcommons.org/benchmarks/inference, 2 April 2025, entry 5.0-0077. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.
8 Verified MLPerf® score of v5.1 Inference Closed Llama 3.1 405B offline. Retrieved from https://mlcommons.org/benchmarks/inference, 2 April 2025, entry 5.0-0076. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

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
