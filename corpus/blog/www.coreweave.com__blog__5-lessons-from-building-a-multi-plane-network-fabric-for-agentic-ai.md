# Multi-Plane Networking for Agentic AI: 5 Lessons | CoreWeave

Source: https://www.coreweave.com/blog/5-lessons-from-building-a-multi-plane-network-fabric-for-agentic-ai

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Training a foundation model is, from the east-west fabric's point of view, a well-behaved problem. Thousands of GPUs run the same collective at roughly the same time, over and over, for weeks. It's brutal on bandwidth, but it's rhythmic. You can design around that rhythm.
Agentic AI has a less predictable traffic pattern. An agent breaks a task into steps, calls a retriever, calls a tool, calls another model, sometimes calls another agent, and waits on each hop before it knows what the next one is. That serial path is an agent chain, and its latency is the sum of every hop rather than the worst one. Multiply that across thousands of concurrent chains running alongside training jobs and standard inference on the same fleet, and the traffic stops looking like a batch job. It starts looking like a latency-sensitive, many-hop conversation happening everywhere on the fabric at once.

## Agentic traffic breaks assumptions that training never tested
Unlike general-purpose clouds retrofitted for AI, CoreWeave designed and built its network for AI from the ground up. Agents themselves aren't new, but running them at fleet scale introduces networking demands that earlier AI workloads never made. Meeting those demands meant rebuilding the backend network from the topology up, so one fleet can carry sustained training collectives, steady inference, and bursty agent traffic without any one of the three degrading the others.
We built our network on the NVIDIA Spectrum-X Ethernet platform, BlueField-3 DPUs, and ConnectX-9 SuperNICs. We then paired that hardware with our own stack for telemetry, orchestration, scheduling, security, and observability through CoreWeave Kubernetes Service (CKS), SUNK, and CoreWeave Mission Control. Today that fabric connects fleets across more than 50 data centers.
Here's what building it, at fleet scale, taught us.

## 1. Non-blocking is what keeps your agents moving when training spikes
A fabric can pass every point-to-point bandwidth test you throw at it and still stall your agent chains. Oversubscription is usually why. When leaf switches carry less uplink capacity to the spine than the nodes beneath them can generate, the shortfall stays invisible until two traffic types want the same link at the same moment.
Training alone can tolerate some of that. A fabric mixing synchronized training bursts with thousands of small, sequential agent requests cannot, because it needs high aggregate bandwidth and low, predictable per-flow latency simultaneously. An oversubscribed link struggles to sustain both simultaneously.
The lesson we applied is: don't oversubscribe. Every leaf carries enough uplink capacity to sustain full line rate from every connected node, at every layer, at a 1:1 ratio. That discipline holds on every fabric we've built, and it's why CoreWeave operates some of the largest NVIDIA Quantum InfiniBand and RDMA over Converged Ethernet (RoCE) fabrics running today.

### Keep one tenant's burst off another tenant's chain
NVIDIA Spectrum-X Ethernet coordinates the switch and the SuperNIC as one fabric rather than treating congestion as a switch-level problem. Adaptive routing and telemetry-based congestion control keep one tenant's synchronized training burst from degrading another tenant's latency-sensitive agent chain. Congestion thresholds tuned for NVIDIA Collective Communications Library (NCCL) traffic reduce the packet loss that collective operations are prone to triggering, which matters for training runs and for the fan-out-then-synchronize pattern that an agent orchestration step often resembles.
We also move on new silicon early. CoreWeave was one of the first cloud providers to deploy the NVIDIA Spectrum-X SN6600-LD, the industry's first fully liquid-cooled 102.4 Tb/s Ethernet switch, running it as the switching fabric for NVIDIA Vera Rubin NVL72. That gives customers access to higher-capacity networking as new AI systems come online.

## 2. Multi-plane means your fleet can double without costing you a hop
Staying non-blocking as a fleet grows is harder than establishing it on day one. A flat, two-tier leaf-spine topology eventually runs out of radix, the number of ports a switch can practically support. The traditional fix is a third tier, which buys capacity by adding hops. More hops mean more places for jitter to accumulate, often when agentic workloads can least afford either.
Instead of adding another tier, multi-plane topology avoids the trade. Splitting each GPU's SuperNIC connectivity across two or more independent network planes gives the fabric scale without giving it depth. That's what lets a flat, two-tier design reach 128,000 GPUs, 64 times the reach of a single-plane fabric, with no redesign along the way.
Multi-plane operates at the scale of the fabric. Multi-rail applies the same discipline at the scale of the node. Each GPU connects through more than one SuperNIC, and in a rail-optimized design, every node's Nth SuperNIC connects to the same leaf switch as every other node's Nth SuperNIC. Traffic on a given rail never crosses into another leaf's domain to reach its destination.
The result is GPU-to-GPU paths that stay short and predictable instead of hashing across whichever leaf happens to be reachable. Multi-plane keeps the fabric from running out of room as it grows. Multi-rail keeps every individual GPU's path into that fabric short and consistent.

## 3. Hardware-accelerated load balancing gives you the bandwidth you already bought
Non-blocking bandwidth and a topology built to scale still don't guarantee that traffic uses all of the bandwidth. Left to static hashing, a handful of large flows pile onto the same path while other paths sit idle. That imbalance is how a well-designed fabric becomes congested under real collective and agentic traffic.
Load balancing has traditionally run in software, with NCCL deciding how to spread a collective's traffic across available links. While this approach works, it comes with two tradeoffs:
- Competes for the same host CPU cycles as everything else trying to get a packet out the door
- Reacts to congestion after the fact rather than routing around it as conditions change
NVIDIA ConnectX-9 SuperNICs, part of the Spectrum-X Ethernet platform, moves that job into hardware, changing both where the logic runs and how quickly it can respond. A dedicated hardware path reacts to live congestion telemetry at line rate, which a software scheduler sharing the host CPU can't match, and it does so without taking cycles from the workload the network exists to serve. Hardware load balancing responds faster to a congested path and spreads more concurrent flows across the fabric without overhead compounding as the fleet grows.
CoreWeave pairs ConnectX-9 SuperNICs, running up to 1,600 Gb/s per GPU on our NVIDIA Vera Rubin NVL72 deployment, with adaptive routing on the Spectrum-X switch fabric. The switch and the SuperNIC coordinate directly, using live congestion telemetry rather than static hashing to spread flows across every available path, plane, and rail as traffic shifts.

### Tune against real traffic, not textbook defaults
Getting that coordination right is tuning work, not configuration work. Priority flow control and explicit congestion notification have to be set against the actual traffic on the fabric rather than textbook defaults, since a network that pauses too aggressively under load trades packet loss for head-of-line blocking and its own tail-latency cost. Congestion thresholds need separate tuning for NCCL patterns, because collectives generate a synchronized, many-to-many burst, and that’s the traffic shape default Ethernet congestion settings handle worst. The payoff isn't a faster fabric. It's one that stays lossless when the traffic gets ugly.

## 4. An agent chain has no clean restart boundary
A training job that stalls for a few minutes is expensive, but it restarts from a checkpoint. An agent that stalls halfway through a 10-step chain, multiplied across thousands of concurrent chains, has no equivalent. There's no single point to resume from, which means resilience can't live in one place in the stack. Each layer has to hold on its own.
That means building resilience across five layers:
- Topology: Multi-plane and multi-rail shift traffic off a degraded plane or rail without the node absorbing the full hit.
- Silicon: NVIDIA BlueField-3 DPUs run networking, isolation, and policy enforcement on dedicated hardware instead of host CPUs, so tenant isolation holds independently of the host operating system, and provisioning, firmware validation, and policy enforcement never take cycles from the workload.
- Software: CKS removes the hypervisor entirely, so a virtualization fault can't become a tenant's problem in the first place.
- Operational: CoreWeave Mission Control replaces degraded nodes automatically once they cross a health threshold, backed by a dedicated FleetOps team watching for early signs of trouble around the clock.
- Geographic: CoreWeave's network backbone links data centers as a single fabric across regions, so a workload spanning more than one site doesn't depend on any single facility staying up.
The same principle applies at two of those layers: infrastructure work belongs on dedicated hardware, not on the resources you're paying to run your workload. No hypervisor sitting between you and the GPU, and no networking services competing with your job for host cycles.
Newer DPU generations extend that approach. BlueField-4 pairs a 64-core CPU with an integrated ConnectX-9 for 800 Gb/s of throughput and roughly six times the on-DPU compute of BlueField-3. More of the infrastructure layer moves off the host entirely: multi-tenant networking, rapid storage access, and runtime security. For agentic workloads, where the host CPU is already contending with orchestration and tool calls, every cycle the DPU absorbs is one the workload keeps.

## 5. You can't fix the hop you can't see
None of the above matters if a slow hop stays hidden. NVIDIA network observability tools trace flow-level performance from the GPU to the SuperNIC, mapping per-hop behavior across switch ports and RoCE queues. That turns a vague symptom like "this agent chain feels slow" into a specific link or queue an engineer can act on.
CoreWeave Mission Control turns that raw signal into something a fleet-wide operations team can work from, rather than another pile of dashboards. It continuously evaluates GPU, network, and storage health across the fleet, and its GPU Straggler Detection identifies performance bottlenecks automatically, isolating the affected node or GPU without an engineer combing through logs or a customer resubmitting a job.
For a synchronized training run, that catches the node dragging down the whole collective. For agentic traffic, it catches the node that would otherwise quietly add latency to every chain routed through it, one hop at a time, with no error message pointing at the cause. At fleet scale, finding that node in minutes instead of days is the difference between an incident and a non-event.

### Send the same signal to your own tools
Telemetry Relay gives you direct access to that visibility. It's a fully managed service that forwards CoreWeave's logs, metrics, and audit events into your own SIEM or observability stack over HTTPS, S3-compatible endpoints, or Prometheus Remote Write, with minimal setup on either side.
That matters more for agentic workloads than it would for a single training job. Instead of building a bespoke integration to reconstruct what happened across thousands of concurrent chains, the same telemetry CoreWeave's operations team uses shows up in the tools your team already runs.
Security visibility is built into the same operating layer as performance telemetry, rather than running as a separate system alongside it. Identity and access management, role-based access controls, and continuous audit logging all live there, and Telemetry Relay forwards those audit and security events to your SIEM already encrypted. Governance and compliance reviews work off the same real-time signal as everything else.
For agentic workloads specifically, where an agent may be acting across systems on a user's behalf, knowing who accessed what, when, and under which identity isn't a compliance afterthought. It's the same fleet-wide visibility applied to security instead of performance.

## Engineering the fabric for what AI does next
These lessons came out of close co-engineering between CoreWeave and NVIDIA, validated at a scale most of the industry hasn't reached yet.
CoreWeave operates some of the largest InfiniBand and RoCE fabrics running today. We were one of the first cloud providers to deploy the Spectrum-X SN6600-LD, and the first to bring up and validate NVIDIA Vera Rubin NVL72. We've deployed BlueField DPUs across what is, to our knowledge, one of the largest DPU rollouts in AI infrastructure to date.
That experience shows up at the workload level. Fleet-scale InfiniBand and RoCE, paired with the newest NVIDIA switching and NIC silicon validated in our fleet rather than on a data sheet, is what makes one fabric able to serve both ends of the spectrum: the rhythmic, bandwidth-hungry demands of large-scale training, and the unpredictable, many-hop, latency-sensitive demands of agentic AI, without picking one at the expense of the other.
Training got the industry to build fast networks. Agentic AI will determine which of those networks were built to last.
Ready to learn more about networking for AI?
See how CoreWeave doubles AI networking bandwidth per rack

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

CoreWeave Interconnect,

Copy code

Copied!

CoreWeave Interconnect,
