# SkyPilot for Multi-Cloud Orchestration | CoreWeave Blog

Source: https://www.coreweave.com/blog/coreweave-adds-skypilot-support-for-effortless-multi-cloud-ai-orchestration

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

We’re excited to announce official support for SkyPilot, unlocking seamless, cloud-agnostic, AI open-source orchestration on CoreWeave’s highly performant and scalable GPU infrastructure. This support for SkyPilot adds an additional orchestration option alongside CoreWeave’s existing support for SUNK (Slurm on Kubernetes) and Kueue. 
SkyPilot, an open-source framework founded at the Sky Computing Lab at UC Berkeley, was designed to abstract cloud complexity and automate the selection, provisioning, and management of compute and storage on any infrastructure. CoreWeave, the Essential Cloud for AI, offers cutting-edge performance, reliability, and observability, making it the ultimate infrastructure backend for SkyPilot users who prioritize speed, efficiency, and flexibility at scale.
Whether you’re a fast-moving AI-native startup or an enterprise scaling to thousands of GPUs, SkyPilot on CoreWeave unlocks production workloads, and it’s already trusted by some of the most ambitious companies in the space.
What’s new and why it matters:
- Get AI running on CoreWeave at lightning speed. Get training, development, and serving workloads deployed on CoreWeave GPUs in minutes with ready-to-use examples and recipes, such as Llama 4 FT, vLLM , and more on the examples page.
- One‑line InfiniBand enablement on CoreWeave. Add <network_tier: best> to your SkyPilot resources to automatically configure InfiniBand, RDMA, and environment variables - no manual tuning. The official NCCL test example shows end‑to‑end setup and benchmark results demonstrating 3.6Tb/s interconnect bandwidth on CoreWeave.
- Native CoreWeave AI Object Storage integration in SkyPilot. SkyPilot now recognizes CoreWeave buckets and includes install/config steps and a cw:// scheme in its storage docs, making it straightforward to fuse mount data for easy access, and to achieve  throughput up to 7 GB/s per GPU, far beyond traditional object storage.
- Autoscaling support to maximize cluster utilization. SkyPilot automatically scales your CoreWeave clusters up or down based on demand,ensuring you pay only for what you use while maintaining peak GPU utilization across distributed clusters.
- First‑class visibility in SkyPilot install docs. CoreWeave is now included in the SkyPilot installation guide, with steps to connect your CoreWeave Kubernetes Service (CKS) cluster and optional CoreWeave AI Object Storage setup.

## Why run SkyPilot on CoreWeave?
By combining SkyPilot’s intelligent orchestration with CoreWeave’s purpose-built AI infrastructure, teams gain a streamlined way to launch, scale, and optimize workloads across clusters. Together, they remove the complexity of managing compute at scale so that AI engineers can focus on building, not babysitting infrastructure.
Running SkyPilot on CoreWeave means AI teams can:
- Get SLURM-like convenience with the reliability and flexibility of Kubernetes
- Easily manage multiple Kubernetes clusters to get a unified control plane
- Instantly provision hundreds (or thousands) of GPUs with a single command
- Optimize for price/performance thanks to CoreWeave’s kubernetes-on-bare-metal architecture
- Reduce time-to-market by leveraging the industry's fastest networking and storage for distributed workloads

‍

## How it works: From multi-cloud MLOps to scalable reality
SkyPilot’s open-source orchestration abstracts cluster management, auto-selects the best region/GPU (including spot/preemptible instances), and manages job submission for your ML training or inference workloads. With CoreWeave now supported as a backend, you can launch SkyPilot jobs on your CoreWeave cluster directly from your familiar SkyPilot YAML or CLI. 
This unlocks greater efficiency for ML researchers, including:
- Dynamic resource matching: SkyPilot will intelligently allocate the optimal GPU resources from CoreWeave based on your compute and storage needs and pricing targets. 
- Built-in failure handling, smart retries, and log streaming, essential for production MLOps and ease of debugging.
- Fully automated configuration of 3.2 Tb/s Infiniband interconnects
- Autoscaling support to maximize cluster utilization
- Tight integration with CoreWeave’s LOTA (Local Object Transfer Accelerator) storage layer; this makes large model checkpoints, datasets, and artifacts blazingly fast to distribute and access (up to 7GB/s throughput per GPU).

## Explore SkyPilot on CoreWeave, trusted by AI-native pioneers 
CoreWeave and SkyPilot already powers production workloads for a growing roster of customers, including multiple leading AI-native pioneers and startups running jobs across hundreds of GPUs. 
By combining SkyPilot’s multi-cloud orchestration with CoreWeave’s purpose-built AI infrastructure, teams can scale elastically and meet demand from thousands of end users, serving critical business applications. 

### Get started in minutes
- Install SkyPilot and follow the CoreWeave setup steps in the installation guide.
- Validate high-performance networking using the InfiniBand/NCCL example.
- Mount CoreWeave Object Storage using the cw:// scheme (example PR).
For a targeted hands‑on walkthrough to create dev pods, serving, and multi‑node training on CoreWeave infrastructure, see our internal guide Skypilot on CoreWeave.
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

CoreWeave Kubernetes Service (CKS),

Copy code

Copied!

CoreWeave Kubernetes Service (CKS),
