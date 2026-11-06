# Global Network Backbone Built for AI

Source: https://www.coreweave.com/blog/coreweave-builds-the-first-global-backbone-network-purpose-built-for-ai

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

CoreWeave is extending the reach of The Essential Cloud for AI® with a global network backbone purpose-built for the scale, speed, and data demands of AI workloads. Today, CoreWeave’s Global AI Network connects 51 active data centers across North America and Europe, including eight added in 2026. These facilities provide more than 1.5 gigawatts of active power, backed by approximately 4.2 gigawatts of contracted power*, and are linked through a high-capacity backbone spanning major AI infrastructure markets on both sides of the Atlantic. Operated as one global network, this footprint enables customers to optimize the data movement between CoreWeave locations, reach available compute, and deploy AI workloads closer to demand and maximize goodput.
CoreWeave’s current network backbone connects 51 active data centers across North America and Europe, representing more than 1.5 GW of active power and approximately 4.2 GW of contracted power.
Today we announced the deployment of a 22.5 megawatts (MW) data center powered sustainably by renewable energy in Copenhagen, Denmark. As CoreWeave expands into new regions, the backbone expands with it. Beginning in Q4 2026, new network points of presence (PoPs) come online in the United Arab Emirates, India, Indonesia, Singapore, Australia, South Korea, and Japan, connected over terrestrial and subsea fiber. In Indonesia, the new PoP will connect the three data center facilities we announced in August, putting local capacity on the same network as everything else we run. In India, the new PoP will expand our AI Cloud platform with 240 MW of data center capacity in Navi Mumbai.
With the larger network, CoreWeave is building the first global AI backbone network, purpose-built for AI workloads, at Petabit-scale, that connects locations in North America, Europe, the Middle East, and Asia Pacific. To put our network scale into perspective, a Petabit-scale network is capable of concurrently streaming a 4k movie to 66 million people. While most specialized providers remain limited to a small number of regions, CoreWeave will give customers one AI-native network with global reach.
The CoreWeave Global AI Network is expected to connect North America, Europe, the Middle East, and Asia Pacific through high-capacity terrestrial and subsea fiber-optic routes.
Global map showing CoreWeave regions and points of presence connected by backbone network routes across North America, Europe, Asia, and Australia.
‍

## AI-first network design: engineered for AI traffic patterns
General-purpose cloud networks were designed for different network traffic profiles: millions of small flows with predictable patterns, supporting web applications, databases, and transactional services. AI produces a fundamentally different network profile. Training and inference pipelines generate high-volume, long-lived “elephant flows” that can consume substantial bandwidth for hours or days while moving Petabytes of data across the broader workflow. A network optimized for small, predictable transactions is not automatically equipped to sustain that level of continuous large data movement.
Essential AI data flows are inherently global, often in bulk and continuous: preprocessing pipelines feed training clusters, datasets are replicated and staged near available GPUs, model artifacts are distributed to deployment locations, and inference services are positioned closer to users. Supporting these workflows requires a backbone designed around the performance, security, and resilience requirements of AI.
Three things are fundamental to our design approach: AI’s unpredictable traffic patterns demand high speed edge routers, a company's most sacred AI intellectual property should be encrypted end-to-end without sacrificing throughput, and the backbone must be highly resilient.

### 1) Performance. Move Petabytes without rationing the network
While 10 and 100 Gbps connectivity remains common across cloud networks and 400 Gbps is often limited to select edge locations, every CoreWeave PoP is deployed with multiple 400 Gbps connections over a unified optical IP network. Our Petabit-scale global backbone helps customers stage large datasets, distribute models, and reach available compute without turning network bandwidth into another constraint.

### 2) Security. All your data is encrypted in motion at line rate
AI datasets and model assets can represent some of an organization’s most valuable intellectual property. Protecting them should not create another performance bottleneck.
CoreWeave runs MACsec encryption (IEEE 802.1AE) in hardware, encrypting in-flight traffic at line rate on the network interface rather than in software, so protection doesn’t cost you throughput. The protection extends across:
- Backbone links connecting regions
- Direct Connect traffic arriving from your own network 
- Traffic inside CoreWeave data centers
Some cloud providers support MACsec encryption on the direct connect links today. However the encryption is not always supported end-to-end over the backbone network. As an AI Cloud, CoreWeave built in MACsec encryption from day 1 everywhere.
CoreWeave Global AI Network uses end-to-end MACsec encryption to always keep your data protected in-transit.

### 3) High availability. Redundant by design, resilient in operation
CoreWeave builds redundancy into every layer of the global backbone. Every CoreWeave PoP connects to at least two other PoPs across four physically diverse paths, and every region is dual-homed to two PoPs. No two regions depend on a single path between them, including the new Asia Pacific and Middle East routes back to Europe and North America.
The network is engineered to treat disruption as an expected operating condition with rapid detection and failover. If a link, terrestrial fiber route, or subsea cable becomes unavailable, built-in path intelligence can redirect traffic through another viable route in the global mesh, without requiring customers to intervene or manage their own failover. This helps prevent a single infrastructure failure from isolating a region and keeps datasets, model artifacts, and inference traffic moving. Customers can stage data near available GPUs with confidence that the resilience required to get it there is already built into the CoreWeave network.

## One AI network: Extending our AI goodput globally
CoreWeave’s network inside the data center is engineered to keep NVIDIA GPUs supplied with data and turn more accelerator time into useful work. In Purpose-Built Clouds for AI at Scale, we showed how this architecture can deliver 20% higher Model FLOPs Utilization (MFU) and 96% goodput. Our global backbone extends the same design philosophy beyond the data center: eliminate avoidable bottlenecks across the entire path from data to compute.
The backbone and the data center fabric operate as one AI network. Between regions, multiple 400 Gbps connections move datasets, checkpoints, and model artifacts at Petabit-scale. When that data reaches a CoreWeave data center, it flows directly into a non-blocking, multi-plane fabric in which every leaf has enough uplink capacity to sustain full line rate from the nodes beneath it. This two-tier architecture connects up to 128,000 GPUs with fewer hops, reducing the congestion, latency, and jitter that can leave accelerators waiting.
No network can overcome the speed of light. What CoreWeave can remove is the unnecessary delay and operational uncertainty surrounding it: congested transfers, manual data staging, network oversubscription, and replication jobs that must finish before AI work can begin. Once the data arrives, bare-metal infrastructure eliminates the hypervisor overhead, while LOTA in CoreWeave AI Object Storage reduces read latency by up to 8x. Together, these capabilities help keep data moving and GPUs fed, supporting higher MFU, greater goodput, and faster time to results.
The CoreWeave Global AI Network across North America and Europe is operating today, with Asia Pacific and Middle East PoPs scheduled to come online beginning in Q4 2026.
The Essential Cloud for AI is built on one AI-native system from the global backbone to the network fabric inside every region, designed to move data efficiently, reach available compute, and convert more GPU capacity into productive AI work.
If you already run on CoreWeave, you can see your own traffic in the Internet Transit dashboard in Managed Grafana. And if what's keeping your data away from your GPUs is storage latency rather than transport, you can read about our new CoreWeave AI Object Storage cross-region write acceleration in our recent blog.
* As of Q2 2026 earnings call on August 11, 2026

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
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

### Closing the Loop Between Inference and Post-Training

7
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

CoreWeave Direct Connect,

Copy code

Copied!

CoreWeave Interconnect,

CoreWeave Direct Connect,
