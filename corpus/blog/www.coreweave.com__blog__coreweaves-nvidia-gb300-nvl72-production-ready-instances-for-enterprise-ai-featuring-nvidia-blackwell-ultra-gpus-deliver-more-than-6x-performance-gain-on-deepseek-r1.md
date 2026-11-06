# 

Source: https://www.coreweave.com/blog/coreweaves-nvidia-gb300-nvl72-production-ready-instances-for-enterprise-ai-featuring-nvidia-blackwell-ultra-gpus-deliver-more-than-6x-performance-gain-on-deepseek-r1

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

For leaders in the generative AI space, the race to build more powerful and efficient models is relentless. Every percentage point of performance gained equates to faster innovation, better user experiences, and a stronger competitive edge. As we approach trillion-parameter models, memory and throughput become increasingly important in time-to-market.
This challenge is becoming even more pressing with the industry's pivot from simple generative models to more advanced reasoning models. Unlike models that merely predict the next word, reasoning models like DeepSeek R1 can perform complex, multi-step tasks, analyze data, and function as autonomous agents. This leap in capability is the key to unlocking the next wave of enterprise AI, from copilots that can debug code to systems that can conduct scientific research. However, these sophisticated 'thought processes' come at a steep computational cost, especially during inference. This is the critical bottleneck that new hardware and optimized platforms must address.
That's why CoreWeave is proud to put some of the most demanding AI workloads to the test on our new NVIDIA GB300 NVL72-accelerated instances, built on the latest generation NVIDIA Blackwell Ultra GPUs and integrated seamlessly across the entire CoreWeave AI Cloud Platform. The goal was to see if this advanced infrastructure, combined with our purpose-built AI cloud featuring industry-leading performance, resilience, and reliability, could improve existing performance benchmarks. The results were impressive, with a 6.5x performance improvement on inference on the DeepSeek R1 model. This achievement represents a transformational leap in computational power, redefining the speed and scale at which enterprises can deploy state-of-the-art AI.

### Diving into the numbers ‍
In a head-to-head benchmark of the Deepseek R1 reasoning model, CoreWeave tested a 16-GPU NVIDIA H100 system against just four GPUs on the new NVIDIA GB300 NVL72 infrastructure. The superior memory and interconnect bandwidth of the GB300 enabled the model to run with 4-way Tensor Parallelism (TP4) instead of the 16-way (TP16) required by the H100, slashing communication overhead. This architectural advantage produced a massive performance uplift, with CoreWeave observing over 6x higher raw throughput per GPU on the GB300. For customers, this translates directly into a faster, more efficient experience for token generation.

This efficiency is especially important for reasoning models. The "chain-of-thought" processes that allow these models to solve complex problems require multiple iterative steps, making them extremely sensitive to inference latency. A slow, high-latency experience can make an AI agent feel unusable. By drastically reducing communication overhead, the GB300 architecture allows these complex, thought-like processes to execute in a fraction of the time. This isn't just a quantitative speedup; it's a qualitative shift that makes real-time AI agents and sophisticated reasoning applications viable for the first time.‍

### Inside the NVIDIA GB300 NVL72‍
The foundation of this performance leap is the NVIDIA GB300 NVL72, a rack-scale system meticulously designed for the demands of frontier AI models. At its core, it represents a fundamental architectural shift in how large-scale models are run, addressing key bottlenecks with groundbreaking hardware innovations. The system's power is rooted in three key pillars:
- Massive memory space: With 37TB of total memory, the system allows for massive models to run seamlessly. For customers, this means that they can handle larger, more complex AI models with dramatically reduced latency.
- Blazing-fast interconnects: The platform features fifth-generation NVIDIA NVLink, delivering 130TB/s of bandwidth to the 72 interconnected NVIDIA Blackwell Ultra GPUs. This ultra-high bandwidth is critical for large training jobs, as it minimizes communication overhead and keeps the GPUs fed with data, directly translating to faster training times and higher throughput.
- Optimized end-to-end networking: Paired with NVIDIA Quantum-X800 InfiniBand scale-out compute fabric, the CoreWeave AI Cloud ensures that data flows efficiently across the entire cluster, eliminating the bottlenecks that plague large-scale deployments on commodity clouds.

### The CoreWeave advantage: turning raw potential into record performance
World-class infrastructure is only the first step in delivering leading AI performance. Translating the raw potential of the NVIDIA GB300 NVL72 into a stable, observable, and record-breaking platform requires a deeply integrated, purpose-built AI Cloud stack. This is how CoreWeave delivers a uniquely powerful experience that represents more than the sum of its parts. 
From the moment a NVIDIA GB300 NVL72 rack is deployed, our proprietary Rack LifeCycle Controller automates health verification, firmware provisioning, and system imaging to ensure every component from compute trays to NVLink switches is operating flawlessly. More importantly, this controller makes AI performance accessible and efficient. Our platform integrates seamlessly with Kubernetes (CKS) and Slurm on Kubernetes (SUNK), augmented with an important enhancement: our topology-aware scheduler. Using NVLink labels and a custom block plugin, CoreWeave’s control plane intelligently schedules workloads to run entirely within the same NVL72 domain whenever possible. This prevents jobs from being scattered across racks, which would reduce the performance benefits of the high-speed NVLink scale-up compute fabric. 
Finally, we provide unparalleled visibility through managed Grafana dashboards, offering real-time monitoring of GPU utilization, NVLink traffic, and rack availability. This level of observability is critical for optimizing performance and ensuring the reliability required for mission-critical AI applications. This end-to-end, engineered approach turns the NVIDIA GB300 NVL72 infrastructure into realized, record-breaking performance.

Snapshot of a GB300 NVL72 from one of our managed dashboards

### Leverage our AI performance to gain an AI advantage
The performance breakthrough achieved by CoreWeave is not an isolated success story, it's just another example of what’s now possible for your AI workloads on the CoreWeave AI Cloud. This measurable leap in performance translates directly into tangible business outcomes: 
- Accelerate innovation: Train larger, more complex models in a fraction of the time.
- Great experiences with reduced TCO: Achieve significantly more inference throughput and responsiveness for your budget, maximizing your AI investment.
- Deploy with confidence: Build on an enterprise-ready platform optimized for reliability and efficiency at frontier scale.
The era of trillion-parameter models and real-time, complex AI is here. These benchmarks are further evidence that the future of AI runs most efficiently on CoreWeave. Discover how CoreWeave's NVIDIA GB300 NVL72 instances can accelerate your AI innovation. 

Read the full story about how CoreWeave was the first to deploy the NVIDIA GB300 NVL72.
Learn more about the NVIDIA GB300 NVL72 running on the CoreWeave AI Cloud.
Ready to get started now? Get in touch with us today.

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
