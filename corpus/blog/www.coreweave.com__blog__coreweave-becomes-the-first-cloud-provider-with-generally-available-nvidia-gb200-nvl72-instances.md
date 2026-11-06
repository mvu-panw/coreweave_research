# GA NVIDIA GB200 NVL72 Instances | CoreWeave

Source: https://www.coreweave.com/blog/coreweave-becomes-the-first-cloud-provider-with-generally-available-nvidia-gb200-nvl72-instances

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Today, we’re proud to announce that CoreWeave is the first cloud provider to make NVIDIA GB200 NVL72-based instances generally available, setting a new benchmark for AI performance and scalability. This groundbreaking launch further solidifies CoreWeave’s leadership in providing cutting-edge NVIDIA GPUs and managed cloud services tailored for generative and agentic AI, as well as HPC workloads. Our instances deliver cutting-edge performance, enhanced scalability, and state-of-the-art technologies that empower organizations to rapidly train, deploy, and scale the world’s most complex AI models.

## A legacy of innovation and firsts 
CoreWeave’s journey as an industry leader in AI infrastructure has been marked by a series of firsts. From being among the first to offer NVIDIA H100 and H200 GPUs to training the fastest GPT-3 LLM workloads, and demoing one of the first NVIDIA GB200 systems in action, our continuous investment in our fleet lifecycle platform means we can quickly deliver the latest accelerated computing advancements to customers. 
With NVIDIA GB200 NVL72 instances, we’ve made investments across our stack, from CoreWeave Kubernetes Service and Slurm oN Kubernetes (SUNK) to our Mission Control platform to accelerate initial deployments, streamline large-scale workload scheduling, and provide continuous monitoring across the complete rack, including NVIDIA NVLink interconnect performance. Leveraging years of engineering excellence, CoreWeave delivers best-in-class infrastructure to meet the demands of enterprises building the world’s most advanced AI applications. This is why customers like IBM are excited to partner with CoreWeave to deliver one of the first GB200 NVL72-enabled AI supercomputers, empowering the next generation of AI advancements. 

## 
Next-gen GPU cloud infrastructure, for next-gen AI
As AI models continue to grow in size and complexity, the need for more powerful and efficient computing solutions has grown rapidly. The scalability of these models can be heavily constrained by memory capacity and inter-GPU communication. The NVIDIA Grace Blackwell architecture represents a major breakthrough in accelerated computing technology, purpose-built to overcome these hurdles and meet the demands of today’s and future AI workloads. When combined with CoreWeave’s AI-first approach that harnesses the full power of the world’s most powerful superchip, CoreWeave’s NVIDIA GB200 NVL72-based instances can provide a performant and reliable experience for the most complex AI workloads.
The NVIDIA GB200 NVL72-based instances on CoreWeave connect 36 NVIDIA Grace CPUs and 72 NVIDIA Blackwell GPUs in a liquid-cooled, rack-scale design and are available as bare-metal instances through CoreWeave Kubernetes Service (CKS). NVIDIA GB200 NVL72 Instances leverage NVIDIA Quantum-2 InfiniBand networking, delivering 400Gb/s bandwidth per GPU through a rail-optimized topology. Leveraging NVIDIA Quantum-2’s SHARP In-Network Computing technology, collective communication is offloaded, resulting in ultra-low latency and accelerated training speeds. Additionally, the CoreWeave platform features NVIDIA BlueField-3 DPUs, enabling multi-tenant cloud networking, accelerated data access, and elastic GPU computing. These instances accelerated by NVIDIA Blackwell provide massive computational power for the most complex AI tasks with high performance and reliability, with incredible results compared with previous generations:
- Up to 30X faster real-time large language model (LLM) inference
- Up to 25X lower Total Cost of Ownership and 25X less energy for real-time inference
- Up to 4x faster training LLM models

## 
Harness the true potential of the NVIDIA GB200 NVL72 via the CoreWeave Cloud Platform
The CoreWeave team has been working tirelessly over the last year to build a suite of services and tools that harness the true potential of GB200 NVL72’s incredible capabilities. These innovations help ensure our customers have everything they need to accelerate innovation, optimize resource utilization, and maintain efficiency at scale. 
CoreWeave Kubernetes Service simplifies workload orchestration across GB200 NVL72 instances with advanced scheduling options and rack and NVLink-aware labels that help make managing distributed jobs effortless. Customers can start provisioning NVIDIA GB200 NVL72 powered instances in our US-WEST-01 region using the gb200-4x instance ID. 
Additionally, the service exposes NVLink Domain IDs, enabling efficient scheduling of workloads within the same rack for optimized performance. Slurm on Kubernetes (SUNK) also now includes support for the Topology/Block plugin, enabling customers to schedule training and inference tasks intelligently across racks to leverage the full potential of GB200 architecture. The Topology/Block Plugin for Slurm introduces new concepts and command-line options to manage the placement of jobs within the NVLink domain. These concepts include Blocks, Segments, and the --exclusive=topo option for job submission. In addition, CoreWeave offers native support for IMEX (In-Memory Execution), which allows for more efficient memory sharing across nodes, boosting performance for memory-intensive workloads and reducing processing overhead. 
CoreWeave’s Observability Platform is now equipped with custom dashboards that provide a real-time, deep view into the performance of GB200 NVL72 instances, delivering actionable insights into NVLink performance, GPU utilization, temperature, and other key metrics. This level of transparency allows teams to identify and resolve issues faster, helping to ensure AI workflows remain uninterrupted and productive. The image below presents the Cabinet Visualizer dashboard that offers detailed statistics and historical data for each cabinet, including temperature and performance metrics. The Cabinet Visualizer dashboard also provides links to a more comprehensive node details dashboard for deeper insights.  

Going beyond the hardware, CoreWeave delivers a fully integrated, AI-first platform that empowers customers to make the most of their infrastructure investments. From advanced observability to seamless workload orchestration, CoreWeave provides the tools and services needed to meet the complexities of modern AI development head-on.

## Experience the future of AI innovation
The general availability of NVIDIA GB200 NVL72-based instances on CoreWeave marks a tremendous milestone for customers with large and complex AI workloads. We’re empowering them to build, train, and deploy their workloads with high performance, resilience, and reliability, driving transformation across industries.

If you’re ready to take your AI innovations to the next level, reach out to us here or join our upcoming webinar to learn more. 

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
