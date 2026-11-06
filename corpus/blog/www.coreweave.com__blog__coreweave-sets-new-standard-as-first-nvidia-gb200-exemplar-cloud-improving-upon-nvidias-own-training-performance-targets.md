# CoreWeave Becomes First NVIDIA GB200 Exemplar Cloud

Source: https://www.coreweave.com/blog/coreweave-sets-new-standard-as-first-nvidia-gb200-exemplar-cloud-improving-upon-nvidias-own-training-performance-targets

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Pioneers need the most performant and reliable AI cloud, and CoreWeave has become the first cloud provider in the world to be named an NVIDIA Exemplar Cloud for training workloads running on NVIDIA GB200 NVL72, optimized by CoreWeave Mission ControlTM, the operating standard for the AI cloud. In collaboration with NVIDIA, CoreWeave achieved groundbreaking results, consistently exceeding target performance across critical test cases. This landmark achievement validates CoreWeave’s purpose-built infrastructure for delivering unparalleled performance and reliability on the latest AI accelerators required by the most demanding AI models.
The NVIDIA Exemplar Cloud initiative was launched to provide rigorous, standardized benchmarking across cloud platforms, ensuring transparency and reproducibility. Earlier this year, CoreWeave became an NVIDIA Exemplar Cloud for NVIDIA H100 GPU using up to 1,024 GPUs and a 30 billion parameter Llama 2-style model.

## Why participating in the Exemplar Cloud Initiative matters  
By examining benchmark data, developers, researchers, and engineers are empowered to optimize their deployments with confidence and hold providers accountable for delivering on performance. This transparent approach to performance measurement is essential for running mission-critical AI workloads. 
The most recent results demonstrate how CoreWeave’s multi-generation approach to fine-tuned GPU performance with full stack observability and relentless automated performance optimizations yields consistent peak performance and reliability. This means having the ability to deploy demanding AI applications, such as large-scale pretraining or disaggregated multi-node inference with the confidence that the AI workloads will run efficiently and as expected. This minimizes guesswork and surprises with each generation of GPUs, providing the predictability and reproducibility AI pioneers need as they evolve models and scale training.

## Quantifiable performance: key benchmark results
GPU performance was measured using Model Flops Utilization (MFU), the independent gold standard for measuring efficiency in large model training. CoreWeave’s clusters demonstrated superior utilization compared to reference targets, validating the strength of our architecture and integrated software stack. Key results include:
- DeepSeek v3 (BF16): Achieved a 1.9% greater MFU than the NVIDIA reference target on 512 GPUs, confirming CoreWeave’s optimizations for unmatched performance.
- Grok-1 314B (BF16): Achieved 4.7% greater MFU than the NVIDIA reference target on 512 GPUs, underscoring superior compute stability.
- Llama 3.1 405B (FP8): Demonstrated 3.8% greater MFU on 512 GPUs, confirming the optimization of the high-speed NVIDIA NVLink fabric and storage I/O.
- Llama 3 70B (FP8): Posted a 2.4% greater MFU on 512 GPUs, proving enhanced efficiency even on widely adopted open-source models.
CoreWeave consistently exceeded NVIDIA’s benchmark target performance  

### Unlocking predictability for AI pioneers
This milestone affirms the performance customers consistently receive from CoreWeave’s platform across generations of software and hardware. Predictable, highly efficient performance is essential for today’s long running training workloads, and this commitment to excellence is how CoreWeave helps customers achieve results faster and accelerate development timelines.  
The certification process rigorously tests performance and stability under extreme load, focusing on:
- Cluster goodput and efficiency for optimal training: Maximizing the amount of useful work achieved by the GPU cluster, ensuring resources are not wasted on idle time or I/O bottleneck. 
- Performance scaling for faster training completion: Demonstrating predictable and efficient scaling across large, distributed GB200 NVL72 clusters.
- Hardware and system resilience for uninterrupted training: Validating the underlying infrastructure's ability to maintain stability during intense, prolonged training sessions.

### Deep dive into CoreWeave’s groundbreaking results
To achieve these groundbreaking results, we didn't rely on a "cherry-picked" performance lab environment. Instead, the Exemplar Cloud benchmarks were conducted on a standard CoreWeave cloud cluster. The environment consisted of 8 racks of NVIDIA GB200 NVL72 systems, seamlessly integrated via high speed NVIDIA Quantum-2 InfiniBand networking platform.
CoreWeave Mission Control was the key to operating the cluster with the utmost efficiency. It uses a massive dataset gathered from operating hundreds of thousands of NVIDIA GPUs to enable predictive failure detection and mitigation instead of passive monitoring. The system constantly tests and identifies suboptimal components, replacing them proactively before they can impact a customer's workload. This ensures that only the highest-performing, most reliable hardware is ever part of a cluster.
Our architecture is built to maximize performance, resiliency, and efficiency with deep integration between hardware and software. The runtime environment leverages a unified stack with performance optimizations across every layer from metal to model: 
- CoreWeave Bare Metal servers are fast, reliable, and performant, providing direct access to GPU computing resources without hypervisors that slow down processing, add overhead and latency. In addition, our network fabric enables high bandwidth memory and rapid data access for low latency, high throughput interconnects for the cluster.
- CoreWeave Kubernetes Service (CKS) provides the base runtime environment and is fully integrated with CoreWeaveMission Control to minimize overhead and maximize compute performance. 
- CoreWeave Slurm on Kubernetes (SUNK) enables topology aware scheduling which optimizes performance and utilization for large scale training clusters. Based on a battle-tested Slurm distribution scaled to handle tens of thousands of nodes and hundreds of thousands of concurrent jobs, SUNK is also fully integrated with CoreWeaveMission Control. This allows maintenance and predictive fault management to happen without interrupting active jobs. 
CoreWeave Cloud Platform 
During the training run, CoreWeave Cabinet Visualizer was used to monitor the health of our full rack systems. The dashboard displayed statistics and historical data of each cabinet, including its cooling system, node pools, and NVIDIA NVLink bandwidth usage.  
CoreWeave Cabinet Visualizer dashboard displays health status of each cabinet
CoreWeave Cabinet Visualizer dashboard displays health status and performance metrics for each NVIDIA GB200 NVL72 Rack. CoreWeave Mission Control constantly monitors signals, and determines an individual component as production quality in real time.
During the training run, jobs were tracked using CoreWeave Mission Control observability for infrastructure level monitoring, and Weights & Biases for job level monitoring. 
CoreWeave Mission Control dashboard correlating job-level metrics with infrastructure signals
During the displayed iteration of the Exemplar Cloud benchmark job, an underperforming component was intentionally added to the cluster to demonstrate always-on GPU straggler detection. 
Weights & Biases dashboard showing job level metrics
To ensure performance remained uniform across all 8 racks, we utilized a recently launched CoreWeave Mission Control feature, CoreWeave GPU Straggler Detection. This tool provides real-time collective metrics, including Bus Bandwidth, ensuring all GPUs and communication paths perform equally.  GPU Straggler Detection also automatically detects any hardware lockups and pinpoints the root cause. 
CoreWeave GPU Straggler Detection surfacing collective performance metrics
The continuous performance monitoring provided by CoreWeave Mission Control enabled the benchmark to complete successfully with no actions taken by the cluster administrators to isolate faults or underperforming components. When the system detected any potential hardware faults, CoreWeave Mission Control automatically isolated the issue, surfaced the data in the SUNK and Weights & Biases dashboards, and activated an automatic job restart on healthy nodes, providing an exceptional level of hardware and system resilience. 

## CoreWeave delivers the Essential Cloud for AITM 
CoreWeave’s commitment to a purpose-built AI cloud enables pioneers to uniquely capitalize on the latest architectures. Our focus is building a platform that delivers consistent reliability, efficient scaling, and predictable performance.
With CoreWeave Mission Control, the industry’s first operating standard for running AI at production scale, CoreWeave enables efficient fleet operations with full transparency, proven reliability, and deep insights. Utilizing the CoreWeave AI Cloud, you can deploy your most critical training workloads on a platform verified by NVIDIA to deliver:
- Reduced training time: Groundbreaking performance results that lower the overall time and cost required to train multi-billion parameter models
- Unrivaled reliability: Confidence that long-running jobs will complete without interruption, backed by a rigorously tested architecture
- Performance transparency: The highest level of performance transparency and reproducibility provided by NVIDIA Exemplar Cloud 
The most recent Exemplar Cloud results underscore our continued collaboration with NVIDIA and CoreWeave's ability to maximize efficiency for the most demanding training workloads reinforcing our position as the #1 AI cloud. 
Please see additional resources below and join us for a webinar to learn more: 
- AI Cloud Horizons: Expert insights on the future of GPU Infrastructure
- Purpose-Built Cloud for AI at Scale: Achieving 20% Higher MFU and 10x Reliability on Thousand-GPU Clusters
- The Technical Buyer’s Guide to Scaling AI
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

Training,

Copy code

Copied!

Training,
