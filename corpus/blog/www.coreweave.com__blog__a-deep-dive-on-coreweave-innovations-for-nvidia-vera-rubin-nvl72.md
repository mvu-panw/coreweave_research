# A Deep Dive on CoreWeave Innovations | CoreWeave Blog

Source: https://www.coreweave.com/blog/a-deep-dive-on-coreweave-innovations-for-nvidia-vera-rubin-nvl72

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Agentic AI is shifting to continuously learning systems capable of autonomous reasoning, orchestration, and self-improvement. Trillion-parameter models, million-token context windows, and always-on sessions are becoming the norm, and the infrastructure underneath it needs to evolve just as fast. In January, CoreWeave announced it would be among the first cloud providers to deploy the NVIDIA Vera Rubin platform, joining NVIDIA Ada Lovelace, Hopper, and Blackwell platforms on CoreWeave. Maintaining that pace is not easy: every new generation means re-engineering power, cooling, networking, and software from the rack up in lockstep with NVIDIA. Earlier this month, CoreWeave became the first cloud provider to validate and successfully run diagnostics on NVIDIA Vera Rubin NVL72. 

## 
Six innovations. One rack. Unmatched scale.
NVIDIA Vera Rubin NVL72 unifies leading-edge technologies from NVIDIA—72 Rubin GPUs, 36 Vera CPUs, ConnectX®-9 SuperNIC™s, and BlueField®-4 DPUs. It scales up intelligence in a rack-scale platform with the NVIDIA NVLink™ 6 switch and scales out with NVIDIA Quantum-X800 InfiniBand and Spectrum-X™ Ethernet to power the AI industrial revolution at scale. It delivers AI training with one-fourth the GPUs and AI inference at one-tenth the cost per million tokens versus NVIDIA Blackwell. 

“Our research depends on infrastructure that's both powerful and reliable, and CoreWeave has delivered on both as we've scaled across Hopper and Blackwell. Their ability to deliver highly performant clusters with full cluster observability and a support team that engages deeply on hard problems gives us the confidence to partner with them on Vera Rubin. We are excited about the efficiency gains at rack scale translating into faster training runs and shorter iteration cycles for our researchers." 
Craig Falls, Head of Quantitative Research, Jane Street
Today, 9 out of the 10 leading foundation model providers rely on CoreWeave. But we don’t take that for granted. With each new system, we engineer for deeper optimizations, sharper observability, more operational tooling from day zero to beyond that result in higher MFU, greater goodput, and longer MTTF. We took the same approach with Vera Rubin NVL72 and developed several new innovations across the full stack, from liquid cooling improvements to observability enhancements engineered into CoreWeave Mission ControlTM. The goal: unlock the full potential of the rack-scale system in a way that no other cloud can, so customers can skip the operational burden and get straight to what they do best—innovating.

### Patent-pending valve assembly that makes liquid cooling software-defined
Valvey, part of CoreWeave Mission Control, is a patent-pending programmable per-rack liquid-cooling valve assembly that transforms cooling from a passive mechanical system into a software-defined control surface. It monitors and controls every variable in the rack's liquid cooling loop including flow rate, temperature, pressure, and leak detection and is the single point through which every cooling decision is executed. When higher-level systems need to optimize cooling, isolate a rack for maintenance, or trigger an emergency shutdown, those actions run through Valvey automatically, without manual intervention.
This matters most at scale. In architectures where multiple racks share a remote CDU, Valvey enables true per-rack isolation; one rack can be serviced or drained without disrupting neighboring racks on the same cooling loop. The result is large-scale liquid-cooled infrastructure that contains failures faster, so customers get higher goodput even as their fleet grows.
Jacob Yundt, Sr. Director of Engineering, with Valvey, CoreWeave's patent-pending programmable liquid cooling management system. 

### Unified rack control: turning hardware into a managed cloud resource 
Racky is CoreWeave Mission Control's rack manager, designed to give every Vera Rubin NVL72 rack a standardized, software-addressable control surface. Sitting at the top of the rack, it aggregates power, cooling, and environmental sensors. This allows Racky to monitor rack health, control valves and power functions, and gather the right telemetry—including leak detection and flow and temperature data—while exposing a unified management interface to the broader CoreWeave infrastructure.
Racky works in concert with Valvey and the Rack LifeCycle Controller (RLCC) to form CoreWeave's full rack-scale control stack: Valvey executes cooling actions, RLCC orchestrates workflows, and Racky is the per-rack control point that ties it all together. This means CoreWeave can treat every NVIDIA Vera Rubin rack as a managed cloud resource rather than a custom one-off hardware installation, making fleet operations consistent, observable, and scalable from day one.
Racky, CoreWeave's unified rack manager, aggregates power, cooling, and environmental sensors to monitor and control the health of a Vera Rubin rack.

### Liquid-cooled ethernet network for agentic AI  
CoreWeave is one of the first cloud providers to deploy the 100% liquid-cooled NVIDIA Spectrum-X SN6600 Ethernet Switch. The Spectrum-X SN6600 delivers industry-leading 102.4 Tb/s of total switching capacity across 128 ports of up to 800 Gb/s, built on NVIDIA's Spectrum-6 switch architecture. It represents a generational step in Ethernet switching, purpose-built for the bandwidth and low-latency demands of large-scale AI. As the scale-out fabric for Vera Rubin, the Spectrum SN6600 is what stitches individual NVL72 racks into a single, unified cluster, extending the coherent compute domain beyond a single rack so thousands of GPUs can train and serve as one system rather than a collection of isolated pods.
What makes CoreWeave's Spectrum SN6600 deployment distinct goes beyond the switch itself;  it's how the full infrastructure stack is engineered around it. CoreWeave pairs the Spectrum-X SN6600 with Racky, our unified rack manager, and Valvey, our in-rack liquid-cooling valve assembly. Racky provides precise, real-time control over power delivery and the thermal environment, commanding Valvey to manage cooling at the rack level and make per-rack cooling software-defined. By managing power and cooling this tightly around the switch, CoreWeave keeps the Spectrum-X SN6600 operating at peak performance, delivering the high-bandwidth, low-latency scale-out networking within Vera Rubin clusters.

### Choice of fabric: multi-rail, multi-plane networking at scale
CoreWeave supports both NVIDIA Quantum-X800 InfiniBand and Spectrum-X Ethernet with RDMA over Converged Ethernet (RoCE) with Vera Rubin NVL72, giving customers a choice of highly scalable interconnect fabric for building large-scale training and inference clusters. Both fabrics are fully non-blocking and expose the same RDMA device interface to workloads running in Kubernetes or SUNK, meaning the user experience remains consistent regardless of which backend fabric is deployed. NVIDIA ConnectX-9 SuperNICs handle scale-out connectivity, operating over both NVIDIA Quantum-X800 InfiniBand and Spectrum-X Ethernet to deliver flexibility across fabric types and high bandwidth per GPU . 
While InfiniBand remains the default choice for most deployments, customers with larger-scale needs may prefer RoCE. CoreWeave designs and builds a multi-rail, multi-plane RoCE fabric providing high bandwidth connectivity. Each GPU is served by a ConnectX-9 module, supporting up to 800 Gb/s per port and delivering 1.6 Tb/s of backend bandwidth per GPU. This results in a modular, fully non-blocking topology that scales by incrementally adding spine switches per plane, supporting configurations of over 120K GPUs.
CoreWeave’s multi-rail and multi-plane network fabric provides massive bandwidth and redundancy.

### A stack engineered to maximize every FLOP
CoreWeave's software stack is built to optimize performance from the Vera Rubin NVL72 rack-scale architecture. Where most infrastructure layers treat scheduling, capacity management, and observability as separate concerns, CoreWeave unifies them all into a single operational plane so customers see the full picture of their fleet and get the most out of their GPUs.
High performance data delivery. CoreWeave AI Object Storage supports Local Object Transport Accelerator (LOTA) which is a rack-local, high-throughput storage acceleration layer that sits between remote object storage and the GPU compute fabric. By staging and serving training data locally within the cluster, LOTA eliminates the I/O bottlenecks that would otherwise leave GPUs stalled as they wait on data. 
NVIDIA NVLink-optimized orchestration. CoreWeave Kubernetes Service (CKS) uses topology-aware orchestration to intelligently place workloads within high bandwidth NVLink domains whenever possible. This minimizes cross-fabric communications and maximizes distributed AI performance. As a result, workloads consistently realize the full architectural innovations and performance NVIDIA Vera Rubin NVL72 was designed to deliver.
Dynamic capacity placement. CoreWeave's SUNK places workloads on the most efficient GPUs within a rack and continuously reduces fragmentation as capacity shifts mid-run. When inference traffic spikes, SUNK dynamically reallocates GPUs across training and inference workloads on the same cluster, so freed capacity goes back to work the moment it becomes available. 
Reliable, transparent, and actionable insights. CoreWeave Mission Control is CoreWeave’s operational layer across every Vera Rubin NVL72 system, unifying Racky, Valvey, and the lifecycle controllers. It brings rack-scale telemetry, observability, and lifecycle management into a single managed plane. 
CoreWeave Mission Control automatically detects and initiates the unhealthy node replacement, identifies GPU stragglers before they stall a job, and surfaces everything from GPU utilization to network behavior in one unified view. Purpose-built dashboards bring this down to the rack: Cabinet Visualizer renders each cabinet as a live rack diagram with per-Node NLCC, Kubernetes, GPU temperature, and NVLink telemetry, while Cabinet Wrangler rolls the fleet up into healthy production-GPU counts and schedulable rack capacity across every Vera Rubin NVL72 rack. This combination gives customers a production environment that continuously self-optimizes, keeping operational complexity flat even as cluster scale grows.

### Scaling through partnerships
Delivering Vera Rubin NVL72 at this pace takes a partner ecosystem moving in lockstep. Dell Technologies’ PowerEdge XE9812 servers provide a critical architectural backbone , co-engineered with CoreWeave's accelerated compute fabric to keep performance consistent across long training runs and sustained inference sessions. This milestone also features some of the industry’s first liquid-cooled NVMe storage solutions powered by Micron’s 7600 drives, so storage holds its throughput under peak thermal load during the moments that matter the most. We are also grateful to CSQUARE who collaborated on data center requirements to make this deployment possible.

## Save the date: tune in to “Scaling the Agentic Era with NVIDIA Vera Rubin NVL72 on CoreWeave Cloud” on June 30, 2026
Join CoreWeave and SiliconAngle on June 30 for a live session on running large-scale agentic AI on the NVIDIA Vera Rubin platform where experts will discuss what the hardware change means in practice, and how teams are planning their first deployments. Add a calendar reminder for our live broadcast with SiliconAngle here.

## Start planning your NVIDIA Vera Rubin deployment 
Interested in NVIDIA Vera Rubin NVL72? Request a briefing to cover capacity planning, onboarding timeline, workload fit, and how the platform maps to your roadmap. Just fill out our interest form here to get started.
Want to go deeper? Here’s where to continue:
- Fully Connected 2026: Join us at the AI infrastructure conference, September 29–October 1 in San Francisco. 
- SemiAnalysis ClusterMAX™: Learn why CoreWeave is the only AI cloud rated Platinum — twice. 
- CoreWeave Platform: Explore the AI-native stack from bare metal to model that powers pioneers’ most complex AI workloads.

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
