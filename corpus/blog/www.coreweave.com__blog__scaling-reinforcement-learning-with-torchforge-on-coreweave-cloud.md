# Scaling Reinforcement Learning with torchforge on CoreWeave Cloud

Source: https://www.coreweave.com/blog/scaling-reinforcement-learning-with-torchforge-on-coreweave-cloud

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## Scaling RL on CoreWeave with torchforge
CoreWeave continues to make Reinforcement Learning (RL) easy to use and scalable for researchers and developers. After launching the first publicly available Serverless Reinforcement Learning capability to build reliable AI Agents, CoreWeave is excited to announce support for torchforge, a new PyTorch-scalable RL framework. torchforge simplifies RL by separating algorithm design from distributed infrastructure, enabling researchers to scale complex RL workloads to thousands of GPUs with minimal code and maximum efficiency. Researchers can use torchforge with CoreWeave’s industry-leading Slurm-on-Kubernetes (SUNK) for training and post-training workflows on CoreWeave Cloud. 
In a 3-way partnership, Meta, Stanford's Scaling Intelligence Lab, and CoreWeave conducted a large-scale post-training run of a state-of-the-art dense coding model on a cluster with 512 NVIDIA H100 GPUs on the CoreWeave Cloud Platform. The collaboration confirmed torchforge’s stability, performance, and production-grade functionality at scale on CoreWeave, helping move RL from research into robust and reproducible production pipelines.

### Reinforcement learning: Better model performance at lower cost
Reinforcement Learning (RL) is the leading post-training technique for improving model performance while reducing serving costs. Unlike supervised fine-tuning (SFT), which teaches a model to imitate patterns in labeled data, RL trains from outcomes using feedback and rewards. This approach has powered breakthroughs such as DeepSeek R1 and other state-of-the-art models, where RL enabled meaningful performance gains. In practice, it allows smaller models to match the performance of larger ones on specific tasks, while being more cost-effective and faster to run.

### torchforge reduces infrastructure complexity for researchers
RL workflows combine continuous inference and training in a tightly coupled loop, which includes generating responses to prompts, scoring them with a reward model, and updating the base model using those scores. At scale, this process is difficult to orchestrate. Researchers must manage separate inference and training stacks, shard models correctly across GPUs and nodes, handle failures gracefully, and transfer weights efficiently between the two phases. These infrastructure concerns are often embedded directly into the RL loop, consuming researcher time and compute that would otherwise go toward improving model quality.
torchforge solves this by separating algorithmic logic from infrastructure management, allowing researchers to focus entirely on the RL algorithm itself: data, rewards, losses, and environments, without the burden of managing infrastructure at scale. torchforge, which implements GRPO—a popular RL algorithm aimed at improving a model’s reasoning quality, allows researchers to write RL code almost as simply as pseudocode while managing scaling, routing, load balancing, and fault tolerance. 
Built on Monarch, a PyTorch-native distributed programming framework, torchforge can scale to thousands of GPUs with fast, fault-tolerant data movement through RDMA. This means researchers can run larger, more complex RL experiments faster and more reliably, turning what was once weeks of engineering overhead into repeatable, production-ready training workflows.

### SUNK enables torchforge to scale
CoreWeave offers the industry-leading solution for running torchforge because of its purpose-built AI cloud, infrastructure reliability, and delightful researcher experience with its Slurm on Kubernetes (SUNK) offering. CoreWeave ensures researchers and platform engineers can run torchforge with higher performance, efficiency, scale, and reliability.
The motivation for running torchforge on SUNK is the need for a scheduler that is reliable and efficient at scale. In a shared research cluster, improving utilization is hard because multi-node jobs must launch together, inference and training stress the network fabric in different ways, long generations and verifiers can slow down tasks, and frequent weight syncs can yield low performance in cases where network fabric topology is not optimized. Slurm addresses these scheduling challenges through features such as priorities, preemption, quotas, gang scheduling, and topology-aware scheduling. 
When the number of compute nodes grows into the thousands, managing Slurm itself becomes increasingly complex, and availability starts to limit throughput. To address this, CoreWeave offers SUNK, combining Slurm’s advanced scheduling with the orchestration power of our managed Kubernetes service, CKS, to support jobs spanning more than 32,000 GPUs. SUNK ensures high availability for Slurm components, scales compute nodes on demand, and replaces the Slurm controller API to handle hundreds of thousands of jobs. 
For RL workloads running with torchforge, this translates directly into faster job startup, more consistent cluster utilization, and higher end-to-end throughput across large asynchronous rollouts and training loops. Researchers can launch large-scale torchforge runs with reduced queuing delays and infrastructure interruptions, keeping GPUs busy and experiments progressing continuously.
SUNK also offers a unique researcher-centric experience through secure isolated environments with Individual Login Nodes, file systems mounted in-cluster, tooling to easily use and build container images, and IdP-federated cluster access management through Automated User Provisioning. Together, these features simplify day-to-day operations for researchers and platform teams alike, making large-scale RL experimentation on torchforge both seamless to manage and effortless to scale.

### Running torchforge on SUNK on CoreWeave
Running torchforge on SUNK feels familiar to anyone already using Slurm. Researchers can start by defining their torchforge job in a standard Slurm batch script and launch it using sbatch or srun. Once submitted, SUNK handles GPU allocation and node scaling automatically, while Kubernetes ensures health and restart of any failed components. 
Within the cluster, torchforge provides live visibility into rollouts, training throughput, and job health through standard monitoring tools and logs. If a node fails or a service restarts, the job progresses seamlessly thanks to Monarch’s fault-tolerant controller and torchforge’s built-in retry logic. 
The result is a simple, predictable workflow: researchers focus on their RL experiments while SUNK and torchforge manage the scale and reliability behind the scenes. In collaboration with Stanford’s Scaling Intelligence Lab, dozens of torchforge runs were executed on CoreWeave’s infrastructure, including full-scale experiments leveraging all 512 NVIDIA H100 GPUs.

### CoreWeave’s purpose-built AI stack
CoreWeave’s AI stack is purpose-built for performance, efficiency, and reliability. Our cutting-edge infrastructure features the latest NVIDIA GPUs, high-performance CPUs, and NVIDIA Quantum InfiniBand networking. CKS runs directly on bare metal without incurring a virtualization performance hit, and NVIDIA Data Processing Units (DPUs) offload networking and storage traffic, allowing GPUs to remain focused on training and generation. 
Mission Control helps ensure all compute resources operate at peak performance with advanced cluster validation, proactive health monitoring, and rapid node replacement. SUNK allocates work across the fleet, taking into account node health and topology, and quickly requeues jobs as needed. CoreWeave AI Object Storage with Local Object Transfer Accelerator (LOTA) sustains data loading and checkpointing at about 7 GB per GPU per second across thousands of GPUs simultaneously. Lastly, users can access deep observability across the stack through pre-built Managed Grafana Dashboards and through the integration with Weights and Biases.
The result of this efficient scheduling, improved researcher experience, and tight coupling of the CoreWeave stack is up to 10x better reliability (as measured by Mean-time-to-Failure), 20% higher MFU (Model FLOPs Utilization), and 96% Goodput (Effective Training Time Ratio). 

### Bringing scalable RL to life on CoreWeave
torchforge is supported on CoreWeave through SUNK. Use the instructions here to install it in a SUNK cluster, run a simple RL job, and monitor the results. This collaboration with Meta and Stanford’s Scaling Intelligence Lab marks the beginning of a broader partnership to advance large-scale RL on CoreWeave. 
We plan to work closely with Meta’s PyTorch team to continue improving performance, reliability, and developer experience for RL workloads, and to extend this collaboration into other areas of the PyTorch ecosystem. By combining torchforge with CoreWeave’s purpose-built AI cloud, we’re closing the gap between research and production — making scalable, reliable RL accessible to every developer.
Learn more about Monarch, torchforge, and other PyTorch projects here. Explore how CoreWeave powers high-performance AI model training and research here.

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

SUNK,

Copy code

Copied!

SUNK,
