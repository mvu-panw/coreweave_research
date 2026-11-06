# CoreWeave Expands its NVIDIA Blackwell Fleet with Generally Available NVIDIA HGX B200 Instances

Source: https://www.coreweave.com/blog/coreweave-expands-its-nvidia-blackwell-fleet-with-generally-available-nvidia-hgx-b200-instances

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Today, we proudly announce the expansion of our NVIDIA Blackwell-based instances with the general availability of NVIDIA HGX B200-based instances on CoreWeave. Building upon our initial deployment of NVIDIA HGX B200 instances in February 2025, which supported a strategic customer with more than 10,000 NVIDIA Blackwell GPUs over NVIDIA Quantum-2 InfiniBand networking, this launch significantly broadens access. These generally available instances deliver incredible performance for AI training and real-time inference for enterprise AI workloads, achieving upwards of 2x faster performance per GPU compared to previous generation NVIDIA Hopper GPUs. CoreWeave’s AI-first cloud platform is purpose-built to maximize the performance and scalability of NVIDIA HGX B200 systems, so customers can scale their AI ambitions.

## Scaling AI ambitions with NVIDIA HGX B200 
The NVIDIA HGX B200 builds on the breakthrough technology of the Hopper generation to deliver leading performance for trillion-parameter LLM training, real-time inference, and enterprise-scale GenAI workloads. These instances are capable of achieving up to 15x faster inference on models like GPT-MoE-1.8T and 3x faster training compared to Hopper-generation H100-based instances.  A dedicated decompression engine accelerates data pipelines, achieving 2x faster query benchmarks than NVIDIA Hopper GPUs. With support for FP4/FP8 precisions with the second-gen Transformer Engine, this powerful combination positions HGX B200 as a premier accelerated x86 scale-up platform designed for the most demanding generative AI, data analytics, and high-performance computing workloads.

Each CoreWeave instance offers significant compute power with 8 NVIDIA B200 Blackwell GPUs (180GB HBM3e each) interconnected via NVIDIA NVLink and NVLink Switch and 2 Intel Emerald Rapids 8562Y+ CPUs, alongside 61.44TB of NVMe local storage for high-speed data access. Networking is facilitated by an NVIDIA BlueField-3 DPU and 8 NVIDIA ConnectX-7 InfiniBand host channel adapters (HCAs) for lossless scaling and high-throughput data transfer. These instances feature a high-speed 400G NDR non-blocking NVIDIA Quantum-2 InfiniBand fabric for seamless connectivity.

## Unlocking full B200 performance on CoreWeave
As the #1 Platinum-rated AI Cloud per SemiAnalysis’ ClusterMAX ranking, CoreWeave offers purpose-built infrastructure meticulously engineered to unlock the full power of NVIDIA’s Blackwell architecture. Our relentless focus on optimizing our infrastructure for AI helps to ensure our B200 instances achieve maximum performance, reliability, and resilience.
At the heart of our AI-first platform is CoreWeave SUNK, an integration of Slurm and Kubernetes that enables customers to both train and serve large models on the same B200-based cluster. SUNK dynamically scales resources and intelligently shares compute between workloads, eliminating the need for separate environments. For teams fine-tuning and serving LLMs with HGX B200, SUNK’s topology-aware scheduling places jobs for optimal GPU interconnect and data locality, significantly boosting Model FLOPs Utilization (MFU).
CoreWeave Kubernetes Service (CKS) complements SUNK by providing a managed Kubernetes solution designed specifically for AI workloads. By running HGX B200 instances directly on bare metal servers, CKS aims to deliver the lowest possible latency and highest throughput, critical for maximizing HGX B200’s performance. Security and operational isolation are ensured, as each HGX B200 cluster operates within its own private Virtual Private Cloud and leverages dedicated BlueField DPUs for offloading networking, security, and storage tasks. Customers can provision NVIDIA HGX B200-based instances using the Instance ID b200-8x in the US-WEST-01A Availability Zone starting today.

To provide customers with enhanced visibility and control over their B200 instances, CoreWeave Observe™ offers deep, per-GPU insights into system health and workload performance metrics such as GPU XID errors, memory usage, GPU utilization, power, temperature, and more. In addition, CoreWeave Mission Control combines automated monitoring with expert human oversight to provide enterprise-grade reliability and resilience, freeing your teams from infrastructure management so they can focus on innovating with their Blackwell clusters.

Together, these purpose-built technologies help CoreWeave to harness the full potential of the NVIDIA HGX B200 systems and the Blackwell architecture. This powerful combination delivers cutting-edge performance, scalability, and operational excellence, making CoreWeave the ideal partner for enterprises pushing the boundaries of generative AI, large-scale model training, and real-time inference.

## Ready to accelerate your AI journey?
With NVIDIA HGX B200 instances now generally available on CoreWeave, enterprises have unprecedented access to purpose-built AI infrastructure designed for maximum performance and resiliency. By combining cutting-edge hardware with intelligent orchestration and enterprise-grade reliability, CoreWeave empowers AI pioneers to power their innovations and confidently scale the most demanding AI workloads.
‍Contact CoreWeave today to reserve your NVIDIA HGX B200 instances and experience the #1 AI Cloud for yourself.

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
