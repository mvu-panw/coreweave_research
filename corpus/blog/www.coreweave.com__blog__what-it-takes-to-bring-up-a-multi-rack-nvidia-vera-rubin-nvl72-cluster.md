# Multi-Rack NVIDIA Vera Rubin NVL72 Bring-Up | CoreWeave

Source: https://www.coreweave.com/blog/what-it-takes-to-bring-up-a-multi-rack-nvidia-vera-rubin-nvl72-cluster

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

A single NVIDIA Vera Rubin NVL72 rack is an extraordinarily co-designed computing system: 72 NVIDIA Rubin GPUs, 36 Vera CPUs, NVIDIA NVLink 6 scale-up fabric, ConnectX-9 SuperNICs, BlueField-4 DPUs, high-speed storage, power, and 45°C liquid cooling. 
Connect multiple racks, and the engineering challenge changes. Now you're building a distributed AI system where hundreds of Rubin GPUs, multiple NVLink domains, thousands of high-speed network connections, liquid cooling, power infrastructure, firmware, and software must all behave as one.
At multi-rack scale, every one of those systems becomes interdependent. A slow GPU can become a cluster-wide straggler. A marginal network link can affect collective performance. A cooling anomaly can lead to throttling or a complete shutdown. A configuration inconsistency can become difficult to diagnose once hundreds of GPUs are communicating simultaneously.
You learn where those problems hide by running systems and pressure-testing the infrastructure. We've spent years at CoreWeave building and operating large rack-scale accelerated computing infrastructure, operating at a speed and scale that has allowed us to be among the first to bring multiple NVIDIA GPU generations to market, including NVIDIA L40S, H200, GB200 NVL72, GB300 NVL72, and RTX PRO 6000. More recently, we were the first cloud provider to bring up and validate an NVIDIA Vera Rubin NVL72, and then delivered the system’s first-ever measured performance numbers. 
With NVIDIA Vera Rubin NVL72, we're continuing to apply those lessons for our multi-rack deployment to keep our breakneck pace.

## Automating and unifying racks as software-defined resources
Optimizing a distributed workload across a large cluster of compute depends on predictable, repeatable behavior from every rack. That means firmware, device configuration, network topology, cooling, power, and system performance all need to begin from a known state.
At CoreWeave, new infrastructure enters an automated lifecycle. After the hardware is plugged in and the liquid cooling loop has been provisioned, our automation takes over. New node baseboard management controllers are detected automatically, serial numbers are verified, credentials are bootstrapped, and nodes enter a staging environment. We verify physical hardware, update firmware, apply the required metadata, and validate systems before allowing them to advance toward production.
NVIDIA Vera Rubin requires managing the compute, power, cooling, and networking all as one. So we extended CoreWeave Mission Control® with Racky, our rack-management control layer, and Valvey, our programmable approach to liquid-cooling control, which work alongside CoreWeave's Rack LifeCycle Controller. Together they put power delivery, the cooling loop, and environmental sensing on the same software-defined lifecycle as compute. NVIDIA Vera Rubin NVL72 racks have more performance, compute, bandwidth, and power requirements than the previous generation, so automating the lifecycle is crucial for operations and scaling. 
Liquid cooling hoses connect each rack to the under-floor coolant loop. Valvey gives us programmatic control over what happens inside these lines.

## Finding performance outliers before they become stragglers
Any component can pass basic diagnostics and still be too slow for a large distributed workload. When hundreds of GPUs participate in collective operations, a single underperforming GPU, degraded scaling path, marginal PCIe connection, or thermal issue can force otherwise healthy GPUs to wait. So, we expanded the scope of our validation pipeline to test whether Vera Rubin performs within our expected envelope. 
At the node level, we make sure each system works correctly on its own before it joins a rack. We run hours of repeated GPU diagnostics, test how fast data moves between the CPU and GPU, and check that the high-speed connections between GPUs are performing as expected. We also run compute-intensive workloads on each GPU to see how it performs, including how it handles heat. Finally, we run realistic training workloads and watch how fast each GPU works and whether it's learning correctly along the way.
Once individual nodes check out, integrated rack-level testing looks at how the whole rack performs together. We run both standard and custom performance benchmarks, test how fast GPUs talk to each other through NVIDIA NVLink, push inference and training workloads that lean heavily on those GPU-to-GPU connections, and run tightly synchronized jobs across all 72 GPUs at once. This confirms the rack performs as one system, not just as a collection of working parts. 
Our automated validation can compare results against typical system performance with high accuracy. Because we’re looking for underperforming components that could stall overall system performance, a system that performs below the expected range goes into troubleshooting, not into production.

Once a rack passes these checks, we expand testing to the fabric and cluster level. We run distributed workloads across multiple racks and force traffic over the backend network to confirm that the connected system performs reliably at scale—not just as a collection of individual racks. Testing across these different levels ultimately helps our customers get up and running faster.
Every one of these paths gets measured. A connection that works but runs below its expected range is what can leave an otherwise healthy GPU sitting idle.

## Building a non-blocking RoCE fabric across racks
Inside the rack, NVLink 6 provides the scale-up fabric. Across racks, distributed workloads rely on the backend network. If network capacity doesn't scale with GPU capacity, adding more racks can actually make the system less efficient. More compute creates more communication, and congestion or uneven paths can leave GPUs waiting for data.
For Vera Rubin, CoreWeave's RoCE network architecture is designed as a two-tier, non-blocking, multi-rail, multi-plane network fabric. Each Rubin GPU is served by two ConnectX-9 SuperNICs, delivering up to 1.6 Tb/s of backend network connectivity per GPU. Our design distributes connectivity across multiple rails and planes, creating multiple paths through the fabric while maintaining a non-blocking architecture. The architecture is also designed to scale without continuously adding more tiers to the network; adding more tiers would lead to higher latency. Our current modular design increases spine capacity within each plane and can extend the two-tier architecture to approximately 128,000 GPUs.
CoreWeave’s multi-rail and multi-plane network fabric provides massive bandwidth and redundancy. 

Scale-out testing checks the network between racks, not just the GPUs. We deliberately turn off the fast GPU-to-GPU links and force traffic over the backend network, then measure how fast and how consistently data moves between every card, watching closely enough to catch brief slowdowns that would otherwise go unnoticed. 
We also check latency and response times under load, both on average and in the worst case, since a rare slow response can stall a whole training run. Alongside that, we continuously watch the physical network for early warning signs, like flaky connections, rising error rates, overheating hardware, uneven traffic, and any cabling that doesn't match the intended wiring map. The point is simple: just because the network link is up doesn't mean the network is actually ready to run AI workloads at full speed.

## Keeping compute, networking, power, and liquid cooling synchronized under load
Our multi-rack bring-up process moves from testing individual components to running workloads that push the entire system at once, the same way real AI training and inference does. We run tests that force GPUs to communicate together in sync, training-style workloads that stress compute and networking together, heavy computational workloads that push GPUs to their limits, custom performance benchmarks, and tests that deliberately route traffic over the network fabric instead of the fast internal GPU links. We also test workload patterns that reflect agentic applications, including sudden spikes in demand, changing levels of concurrency, and bursts of communication across the system.
These tests matter because failures often emerge only when compute, networking, power, cooling, and GPU-to-GPU communication are stressed together. That is the kind of coordinated and variable demand created by real-world AI workloads, whether training, post-training, or inference. The benefit is confidence: by the time a rack reaches production, it has already proven it can handle the same stress a customer's workload will put on it, so problems get caught in testing instead of during a live job.
At the same time, we're watching the physical system. This is where Valvey and Racky become particularly important. Liquid cooling at these power densities isn't simply a facilities function. We need software-defined visibility and control around the rack infrastructure so operating conditions can become part of how we understand system health.
It’s no longer a question of individual GPUs being healthy; it’s a question of whether compute, networking, power, and cooling are all behaving correctly across hundreds of GPUs in rack-scale systems operating together under sustained load. That's the standard a multi-rack system has to meet before we consider it ready for production.
A rack under sustained load has to keep networking, power, and cooling behaving correctly together, not just individually.

## The outcome: Multi-rack scale that simply works
Our goal is to give customers one validated, observable pool of Vera Rubin compute, with the boundaries between racks invisible to the workload. Turning NVIDIA Vera Rubin NVL72 specifications into multi-rack cloud infrastructure means: 
- Every rack performs in the same known-good state  
- Compute, networking, power, and cooling hold together under sustained load 
- Rack-scale systems stay optimized for sustained performance across evolving AI workloads, including dynamic reinforcement learning post-training loops 

### Start planning your NVIDIA Vera Rubin deployment. Request a briefing to cover capacity planning, onboarding timeline, and workload fit here. 

#### Want to go deeper? Explore our related resources:
- A Deep Dive on CoreWeave Innovations for NVIDIA Vera Rubin NVL72
- Liquid-Cooled Switching Doubles AI Network Bandwidth Per Rack
- 5 Lessons from Building a Multi-Plane Network Fabric for Agentic AI‍

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
