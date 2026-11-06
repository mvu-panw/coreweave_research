# CoreWeave Drives 20% Higher GPU Cluster Performance | CoreWeave

Source: https://www.coreweave.com/blog/coreweave-leads-the-charge-in-ai-infrastructure-efficiency-with-up-to-20-higher-gpu-cluster-performance-than-alternative-solutions

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

At CoreWeave, we are dedicated to maximizing the performance and efficiency of our cloud infrastructure, and we've made investments across our portfolio to achieve that goal. This study highlights how our platform significantly narrows the AI infrastructure efficiency gap. Our analysis estimates that CoreWeave achieves a Model FLOPS Utilization (MFU) exceeding 50% on NVIDIA Hopper GPUs— driving up to 20% higher performance than public foundation model training benchmarks, which typically range from 35% to 45%.
In addition to our performance profiling work, we also collaborated with NVIDIA to run their DGX Cloud Benchmarking Recipes on our NVIDIA H100 GPU instances. Preliminary testing shows that CoreWeave’s Infrastructure is equally performant to the NVIDIA highly-optimized reference system.

## AI “Efficiency Gap” ‍
Model floating-point operations per second (FLOPS) utilization is a measure of the observed throughput compared to the theoretical system maximum if it were to operate at peak FLOPs. The complexity of managing AI infrastructure means that a majority of the compute capacity in GPUs can be lost to system inefficiencies, with empirical evidence suggesting observed levels of performance in the 35% to 45% range. 

Bridging the efficiency gap between the observed 35–45% and the theoretical 100% presents a major opportunity to unlock the full potential of AI infrastructure. Closing this gap can significantly enhance performance, improve model quality, accelerate development timelines, and reduce overall AI model costs.
Figure 1: The AI Efficiency Gap, the difference between theoretical maximum and actual MFU

## CoreWeave Helps Bridge the “Efficiency Gap”
Generalized clouds operated by traditional hyperscalers were not built to serve the specific requirements of AI. These clouds were created over a decade ago and were designed for general-purpose use cases such as search, e-commerce, web hosting, and databases. They relied on CPU-based web-scale compute, and thus are not optimal for the high compute intensity requirements for AI.
Given the high cost, time-to-market pressures, and critical importance of AI infrastructure, AI labs and enterprises require access to a specialized GPU-based computing environment explicitly designed for AI workloads. This infrastructure must demonstrate proven performance, scalability, and efficiency to effectively meet the demands of advanced AI applications. 
To achieve these goals, cloud platforms must be fundamentally reimagined, with every layer of the technology stack—including data center architecture, compute resources, networking, storage, and infrastructure management—specifically optimized for AI workloads. This comprehensive, purpose-built approach ensures the necessary capacity, performance, scalability, and efficiency, significantly increasing Model FLOPS Utilization (MFU) across the entire infrastructure.
CoreWeave Cloud Platform is a fully integrated solution specifically designed to maximize performance and efficiency for AI workloads, including model training and inference. Performance optimizations are built into every layer—Infrastructure, Managed Services, and Application Software Services—to enhance distributed training throughput.
We provide cutting-edge infrastructure with the latest GPU and CPU compute and highly performant networking with NVIDIA Quantum InfiniBand and NVIDIA Spectrum™ switches. This reduces the communication overhead of NCCL library calls, which typically dominates distributed training time, improving MFU. 
CoreWeave Cloud Platform’s advanced cluster validation, health monitoring, proactive node replacement, and deep observability mean your workloads can consistently run on healthy infrastructure, significantly reducing the likelihood of disruptions. By minimizing interruptions, we achieve a goodput rate as high as 96%, maintaining consistently high Model FLOPS Utilization (MFU) throughout your training runs. 
We run Kubernetes directly on high-performance bare-metal servers for maximum performance and efficiency with our CoreWeave Kubernetes Service (CKS). CoreWeave AI Object Storage provides data transfer speeds as high as 2 GB per second per GPU across hundreds of thousands of GPUs, reducing the impact of data transfers on MFU between checkpoints and for loading data.
CoreWeave’s Application Software Services build on top of our infrastructure and managed software services, integrating additional tools to further accelerate and improve training and inference for our customers. Our Slurm on Kubernetes (SUNK) offering allows customers to run Slurm-based workloads on more than 32K GPUs, optimizing distributed training performance through topology-aware scheduling to fully exploit the speed of the InfiniBand fabric for node-to-node communication, increasing MFU. 
CoreWeave Tensorizer delivers secure, industry-leading model loading performance, enabling asynchronous checkpointing and virtually eliminating any impact of checkpointing on MFU. CoreWeave also provides container images optimized for our platform, enabling customer workloads to extract maximum performance across every layer of the stack.
Through managed Grafana and pre-built dashboards, CoreWeave provides customers with total visibility into their infrastructure and managed service health and performance, such as Infiniband bandwidth, GPU temperature, power consumption, and real-time alerts. This level of visibility is cutting-edge and allows customers to troubleshoot and resolve issues faster and maximize the performance of their workloads on our platform.

Figure 2: CoreWeave’s Layered Architecture Stack

## Measuring the Impact of CoreWeave Architecture on AI Efficiency‍
To measure the performance improvements driven by the CoreWeave Cloud Platform, we launched Llama 3.1 training runs to compare a 128 NVIDIA H100 GPU (16 node) cluster against published results from other research (published by Aleph Alpha and MosaicML, two leading AI labs). 
In a paper, Aleph Alpha and the Hasso Platner Institute published an optimized MFU of 40.43% they achieved for the Llama 30B model with a context window of 8K tokens on 128 NVIDIA A100 GPUs. In a run of a dense 30B parameter model with the same parallelism hyperparameters, we achieved 51.9% MFU on 128 NVIDIA H100 GPUs, representing an MFU increase of 28%. Despite using different GPU types, the results of our runs are still comparable because MFU is not an absolute score but is instead a percentage of the accelerators’ theoretical FLOPs.
MosaicML achieved 41.85% MFU on a training run of their 30B MPT model with a context window of 2K tokens on 128 NVIDIA H100 GPUs. We achieved an MFU of 49.2%, an 18% increase for a model of the same size, context window size, micro-batch size, and parallelism hyperparameters on 128 NVIDIA H100 GPUs. The table below summarizes the details.
Table 1: CoreWeave leads against public benchmark with up to 20% higher MFU

## Top Tier Application Performance
As part of our ongoing commitment to maximizing performance and efficiency for AI workloads, we utilized NVIDIA's DGX Cloud Benchmarking Recipes to evaluate performance of CoreWeave’s NVIDIA Hopper platform for a suite of training and fine-tuning applications. Our results are on par with NVIDIA’s reference architecture performance across all tested workloads, for both BF16 and FP8. 
We are working with NVIDIA to further innovate and accelerate our platform, researching how to further close the AI Efficiency Gap and deliver the maximum possible performance to our users. 
"Achieving peak AI performance requires more than just powerful hardware - it takes a full stack approach,” said Alexis Bjorlin, VP of NVIDIA DGX Cloud, NVIDIA. “CoreWeave demonstrates performance excellence on par with our NVIDIA H100 cloud reference architecture. Working together, we aim to unlock new levels of productivity and innovation for our shared customers.
With the launch of our NVIDIA GB200 NVL72-based instances on CoreWeave, we continue our close collaboration with NVIDIA to drive observed performance toward theoretical performance.
These findings are well aligned with feedback that we have received from other customers. They see higher performance on the CoreWeave Cloud Platform in addition to better resilience and usability, and as such, customers consider our infrastructure services the “gold standard.” This is one of the main reasons why customers like Cohere, Mistral, and IBM are choosing CoreWeave as their AI Cloud provider of choice.

## An Optimized Stack
What's behind the magic of CoreWeave? Every element of our stack is optimized for AI workloads. That includes CoreWeave AI Object Storage—our performance-optimized, scalable, and secure storage solution.

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
