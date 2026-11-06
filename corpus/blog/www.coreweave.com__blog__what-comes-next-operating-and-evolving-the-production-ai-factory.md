# NVIDIA, CoreWeave, and AI Factory Operations at Scale

Source: https://www.coreweave.com/blog/what-comes-next-operating-and-evolving-the-production-ai-factory

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

This is the second in a series from CoreWeave and NVIDIA on the production AI factory lifecycle. In part one, “Why AI Factories Need Proof Before Production,” we explored how co-design and validation prepare the integrated stack for deployment. This post covers what comes next: operating at scale and preparing for the next generation of accelerated computing.
The same discipline that designs and validates the stack carries into what happens after a workload goes live, catching the health signals, holding the scheduling steady, keeping recovery ready before it's needed. This is where that discipline gets tested, starting with what changes once a system moves from validated to operational.
It's no longer about whether it works. It's about whether it keeps working, for the two-week run to simulate a production-ready environment.  A cluster that passes every benchmark can still lose real hours to interruptions, or a checkpoint that silently didn't save. What actually matters at that point isn't whether the hardware is fast. It's how much of that speed turns into finished work instead of recovery time.

## Operating at scale

### Day two starts the moment day one ends
Catching an issue before it costs a run is what day-two operations actually are. Continuous health signals, workload visibility, scheduling control, and fast response the moment something breaks. Long-running distributed training jobs don't leave room to notice an interruption a day late.

### Why goodput governs AI factory economics
At the scale these systems run, one number governs the economics. How much of the compute customers are paying for turns into workload progress. That's goodput, the share of time the system spends doing useful work rather than recovering from interruptions. On long-running, distributed training workloads, CoreWeave has demonstrated up to 96% goodput on NVIDIA Hopper GPUs, always as an upper bound rather than a guarantee. Everything below that line is lost productivity, useful work the system could not deliver because resources went to interruptions and recovery rather than model progress.

### The variables driving goodput
What drives that number comes down to two variables—throughput and resiliency—and a 1,024-NVIDIA Hopper cluster benchmark isolates both.
Throughput. Model FLOPs utilization (MFU) measures how much of a GPU's peak throughput actually turns into model progress. CoreWeave measured 20% higher MFU on Hopper-based systems than other  publicly reported benchmarks show. MFU only tells part of the story. What determines how fast a training run finishes is effective throughput, which multiplies that utilization rate against the GPU's peak capability.  MFU is also workload-dependent, it varies with model architecture (dense versus mixture-of-experts), sequence length, and parallelism, so this figure reflects its test context rather than a universal result.
Resiliency. Mean time to failure improved roughly 10x, with an effective training time ratio of up to 98 percent.  Restarts and lost checkpoints stop setting the timeline when interruptions drop by that much. On CoreWeave Cloud, those gains come from two layers working together. Reliability, availability, and serviceability (RAS) built into the GPU, CPU, and rack architecture, and CoreWeave's software layer that detects, contains, and recovers from issues. Those gains come from fewer interruptions and faster recovery; failures still happen, they just cost less time.

On the NVIDIA side, resiliency improves with each generation. NVIDIA Blackwell introduced a dedicated RAS engine that applies AI-based predictive maintenance across thousands of hardware and software data points.  Reliability that begins in silicon and compounds upward, working alongside topology-aware scheduling on rack-scale systems, is how the integrated stack keeps useful work flowing, rather than being added on after the fact. NVIDIA Vera Rubin carries that further with a second-generation RAS engine for proactive maintenance and real-time health checks without downtime.  Silicon can flag a degrading component. Something above it has to decide what to do about it.  At the system level, modular cable-free trays make Vera Rubin assembly 90x faster than Blackwell and simplifies serviceability, and software-defined NVLink routing reroutes around faults to keep operation continuous with less maintenance overhead.

### How unified software and silicon improve AI factory reliability
That decision layer is CoreWeave Mission Control, which provides reliability, transparency, and actionable insights for the teams running these clusters. Its job is to catch and contain infrastructure failures before they cost a customer the run, through straggler detection, automated node draining, fleet and rack lifecycle management, and recovery workflows. Doing that means processing over 200 million metrics samples per second across all customer environments, because a lag has to be seen before it can be drained.  SUNK, CoreWeave's Slurm on Kubernetes offering, dynamically reallocates GPUs across training and inference workloads on the same cluster as demand shifts, so freed capacity goes back to work the moment it's available, as detailed in our NVIDIA Vera Rubin NVL72 deep dive, rather than sitting idle between jobs. These are the capabilities behind CoreWeave's MLPerf Training v6.0 result on NVIDIA GB300 NVL72, where Mission Control held a consistent performance baseline and SUNK's NVIDIA NVLink-domain-aware placement kept communication local across the NVL72 domain.

## Preparing for the next generation 
Craig Falls, Head of Quantitative Research at Jane Street, put it this way: "Our research depends on infrastructure that's both powerful and reliable, and CoreWeave has delivered on this as we've scaled across NVIDIA Hopper and Blackwell. Their ability to deliver highly performant clusters with full cluster observability and a support team that engages deeply on hard problems gives us the confidence to partner with them on NVIDIA Vera Rubin."

### The lifecycle doesn't reset
That confidence rests on two companies, not one. And it gets tested every time NVIDIA ships a new generation. Each one unlocks more efficiency and higher performance. Reasoning and mixture-of-experts models are pushing deployments to unprecedented scale, and compute, networking, and operational demands climb with them. Through close collaboration, NVIDIA and CoreWeave prepare for these innovations by optimizing every layer of the stack. What doesn't change is the lifecycle. Design together, validate before deployment, operate with full visibility once it's live.

### Preparing for NVIDIA Vera Rubin NVL72
In June 2026, CoreWeave completed the industry-first bring-up and validation of NVIDIA Vera Rubin NVL72. Same readiness discipline, next platform. Customers inherit a validated system instead of becoming the ones who debug a new architecture in production.
NVIDIA normally redesigns 1–2 chips per generation, but the Vera Rubin platform redesigns every chip to keep up with the demands of AI. Six purpose-built chips are unified into a single supercomputer: Vera CPU, Rubin GPU, NVLink 6 Switch, ConnectX-9 SuperNIC, BlueField-4 DPU, and Spectrum-6 Ethernet Switch (combined with ConnectX-9 to deliver the next generation of the NVIDIA Spectrum-X Ethernet platform). By bringing together breakthrough advances in scale-up and scale-out networking, execution efficiency, security, and resiliency, the Vera Rubin platform addresses the core communication, memory, and compute bottlenecks, reducing the cost of training, post-training, reasoning, and agentic inference while enabling intelligence at scale.
That resiliency is where the generational jump is most visible. Rubin GPUs feature a dedicated second-generation RAS engine for proactive maintenance and real-time health checks without downtime, while Vera CPUs add SOCAMM LPDDR5X serviceability and in-system core testing. At the system level, modular cable-free trays make assembly up to 90x faster than Blackwell and simplifies serviceability, and software-defined NVLink routing reroutes around faults to keep operation continuous with less maintenance overhead.

### The operational layer underneath it
Six chips unified into one supercomputer still needs managing rack by rack, especially at 100% liquid cooling with no air-cooled option at this power density. CoreWeave built three systems for exactly that. Valvey and Racky are CoreWeave’s patent-pending innovations, purpose-built for Vera Rubin and available only on CoreWeave.
Valvey is a per-rack liquid-cooling valve assembly that turns cooling from a passive mechanical system into a software-defined control surface, watching flow rate, temperature, and pressure continuously, and isolating a rack automatically if something goes wrong, without taking down the racks next to it. The Rack LifeCycle Controller orchestrates the workflows running across all of it. Racky is the per-rack control point that ties the two together, aggregating power, cooling, and environmental sensors into one standardized surface, so a rack gets managed like any other cloud resource instead of a custom one-off build. Read more about Valvey and Racky here.

### Measuring Vera Rubin performance and efficiency
With Vera Rubin NVL72, CoreWeave shared the first measured performance results: up to 10x more tokens per second per megawatt than NVIDIA GB200 NVL72. How that number was measured is the more useful part. It came from the same DeepSeek R1 workload at a matched interactivity target, with every major optimization enabled: large-scale expert parallelism, NVFP4 precision, multi-token prediction, and disaggregated prefill and decode, using NVIDIA TensorRT-LLM and NVIDIA Dynamo. Full  Vera Rubin performance results here.
When CoreWeave brought up the Blackwell platform, benchmarks improved substantially over the following months as scheduling, networking, and the software stack were tuned around the hardware. Llama 3.1 405B time-to-train dropped 2.8x year over year on the same production infrastructure customers run. Similarly, Vera Rubin performance and economics will improve over time.

### Planning the next generation of AI factories
Together, CoreWeave and NVIDIA plan for the next generation of AI factories using reference designs from the NVIDIA DSX Platform. DSX MaxLPS applies intelligent optimizations and dynamically enforces power policies at the GPU, rack, and workload level, working within a fixed power budget. DSX Flex orchestrates power across grid, on-site renewables, and storage, adapting workloads in real time to grid signals like load shedding, demand response, and pricing events. CoreWeave uses NVIDIA DSX Air to construct high-fidelity digital simulations of its AI factories and data centers, validating hardware before it's deployed physically.

### The lifecycle, not the launch
Deploying a production-ready AI factory is more than a handoff. It's a lifecycle of planning, testing, validating, and learning. For CoreWeave, capacity is the starting point, not the finish line. NVIDIA brings the AI factory platform and CoreWeave provides the AI-native cloud software and operations layer, and together we validate the integrated stack that customers will run.
AI factories require extreme co-design across an entire ecosystem of partners. The network, storage, and software work in concert as one unified system to unlock leading performance.
Put plainly, from years inside these systems:  the hard part was never the silicon. It's the network, the storage, the scheduler, and the recovery path behaving as one while a run is live and the operations that keep them there day after day. That's why the lifecycle, not the launch, decides whether a factory delivers.

### Ready to go deeper?
Missed part one of this blog series? Check out Why AI Factories Need Proof Before Production. Find out how NVIDIA and CoreWeave co-design an integrated and optimized tech stack and validate it before customers deploy.
Explore NVIDIA Vera Rubin on CoreWeave to learn more about the most advanced rack-scale AI compute system available, built for the age of agentic AI and reasoning.
Read the CoreWeave innovations deep dive to get the real story behind Coreweave being the first cloud provider to bring up and validate NVIDIA Vera Rubin NVL72.

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

Mission Control,

Copy code

Copied!

Mission Control,
