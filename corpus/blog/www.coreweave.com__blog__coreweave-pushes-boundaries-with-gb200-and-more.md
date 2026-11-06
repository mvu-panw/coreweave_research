# Pushing Boundaries with NVIDIA GB200 Clusters | CoreWeave

Source: https://www.coreweave.com/blog/coreweave-pushes-boundaries-with-gb200-and-more

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Photo credit: Switch‍
Today, we are thrilled to announce several groundbreaking advancements that strengthen CoreWeave's position as one of the leading AI cloud services providers. CoreWeave is proud to be one of the first major cloud providers to bring up an NVIDIA GB200 NVL72 cluster, showcasing our continued commitment to pushing the boundaries of AI infrastructure. We'd like to give a special thank you to our partners at Switch, who were instrumental in enabling us to accomplish this exciting feat. 

Additionally, we’re introducing new GPU instance types, including the NVIDIA GH200 Grace Hopper Superchip and NVIDIA L40, and L40S GPUs, that are now generally available. Rounding out these innovations is the preview of CoreWeave AI Object Storage, a next-generation cloud storage solution purpose-built for accelerated computing workloads. These updates strengthen CoreWeave’s role as the AI Hyperscaler™ and deliver a comprehensive suite of cloud services to empower AI labs and enterprises to scale their AI development like never before. In this blog, we’ll dive into the technical highlights of these offerings and explain how they integrate with CoreWeave’s managed cloud services to help customers accelerate their AI initiatives.

## Background
This launch continues CoreWeave's tradition of bringing state-of-the-art accelerated computing cloud solutions to market at lightning-fast speed and scale. Our longstanding collaboration with NVIDIA and singular focus on serving the AI market helps enable us to deliver industry-leading technology to customers with cutting-edge speed and efficiency. Built from the ground up for computationally intensive workloads, CoreWeave's infrastructure is uniquely positioned to support the most ambitious AI and HPC projects with exceptional performance and reliability.

## Technical Overview and Performance
The GB200 NVL72-powered cluster, built on the NVIDIA GB200 Grace Blackwell Superchip,  fifth-generation NVIDIA NVLink with NVLink switch trays, and NVIDIA Quantum-2 InfiniBand networking, is engineered to meet the demands of next-generation AI workloads. Designed for applications such as training and deploying large-scale generative AI models, running advanced simulations, and performing real-time data analytics, this cluster delivers up to 1.4 exaFLOPS of AI compute power per rack—enabling up to 4x faster training and 30x faster real-time inference of trillion-parameter models compared with previous-generation GPUs. The architecture includes 13.5TB of high-bandwidth, NVLink-connected GPU memory per rack, optimized for massive datasets, and liquid cooling that reduces energy consumption and costs. At CoreWeave, we have completed the bring up of one of the industry’s first NVIDIA GB200 NVL72 clusters and are relentlessly focused on making the platform generally available in the near future. 
Customers who are keen to use the NVIDIA GB200 NVL72 cluster can get started with using GH200 Superchip-based instances on CoreWeave starting today. The NVIDIA Grace Hopper GH200 Superchip represents a revolutionary advancement in accelerated computing, combining an Arm-based NVIDIA Grace CPU with the NVIDIA Hopper architecture. Each NVIDIA GH200 Superchip features an impressive 96GB of HBM3 memory delivering 4TB/s of memory bandwidth, coupled with 480GB of CPU memory and 72 Arm CPU cores. This integrated CPU-GPU design eliminates traditional PCIe bottlenecks, helping to enable unprecedented performance for large-scale AI and HPC workloads. CoreWeave's NVIDIA GH200 instances combine these powerful superchips with cutting-edge networking, delivering up to 100 Gbps of Ethernet connectivity per superchip and over 7TB of local NVMe storage.
Complementing our NVIDIA GH200 offerings, we are also making NVIDIA L40 and L40S GPU-based instances generally available, providing an ideal balance of performance and cost for a diverse set of workloads. The L40 GPU, with 48GB of GDDR6 memory and fourth-generation Tensor Cores, excels at both AI inference and professional visualization tasks. The L40S GPU also offers 48GB of GDDR6 memory and delivers increased performance for AI workloads, featuring enhanced FP8 support that boosts training throughput by up to 1.4x compared with the standard L40 GPU. Both configurations are powered by Intel Sapphire Rapids CPUs, equipped with a terabyte of RAM, and feature over 7TB of local NVMe storage for high-speed data handling and storage.
Lastly, we are announcing a preview of AI Object Storage service which is a next-generation, exabyte-scale solution designed to accelerate data-intensive AI workflows. Optimized for high I/O and massive datasets, it leverages proprietary Local Object Transport Accelerator (LOTA™) technology to deliver industry-leading performance. By caching frequently accessed objects on GPU nodes’ local disks and bypassing traditional storage gateways, LOTA enables throughput of up to 2 GB/s per GPU—10x faster than previous storage solutions. With enterprise-grade features like S3 compatibility, encryption, role-based access control, and durability, CoreWeave AI Object Storage combines exceptional speed and scalability with the security and reliability required for cutting-edge AI workflows.

## Regional Availability
As part of our ongoing global infrastructure expansion, these instances have been deployed across a number of our US-based data centers. Our US-EAST-04 region provides immediate access to all NVIDIA GH200, L40, and L40S instance types, delivering low latency for east coast users. Our RNO2 region offers both NVIDIA GH200 and L40 instances, serving customers in the western United States. CoreWeave AI Object Storage is currently in preview and will be rolled out to select customers in designated regions. Additional regions will be brought online throughout 2024 and 2025 as we continue our data center expansion.

## Integration with CoreWeave Kubernetes Service
Customers can quickly deploy the new instances through CoreWeave Kubernetes Service (CKS), our managed Kubernetes solution built specifically for AI workloads. CKS leverages bare-metal nodes without a hypervisor, maximizing performance while maintaining security through NVIDIA BlueField DPU-based architecture. For customers requiring traditional HPC workflows, our integrated Slurm on Kubernetes (SUNK) solution provides seamless access to both burst and batch computing capabilities.

## Looking Forward
The bring up of one of the industry's first GB200 NVL72 clusters, new GH200, L40, and L40S instances, along with the preview of CoreWeave AI Object Storage, underscores our commitment to providing advanced accelerated computing and data solutions. As we continue to expand our global data center footprint and enhance our managed services platform, these innovations will help customers push the boundaries of what’s possible in AI, machine learning, and high-performance computing.
Ready to get started? Get in touch with us or learn more at our upcoming webinar.

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
