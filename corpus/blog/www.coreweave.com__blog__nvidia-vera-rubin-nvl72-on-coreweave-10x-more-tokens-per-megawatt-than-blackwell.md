# First-Ever Measured Vera Rubin NVL72 Silicon Performance Stats | CoreWeave Blog

Source: https://www.coreweave.com/blog/nvidia-vera-rubin-nvl72-on-coreweave-10x-more-tokens-per-megawatt-than-blackwell

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In early June, CoreWeave completed the industry's first bring-up and validation of NVIDIA Vera Rubin NVL72, standing up the rack-scale system end-to-end, with power, cooling, networking, and compute all verified and running. That milestone showed the platform running at production scale. The next question everyone has asked: How does it perform? Today, we’re happy to share the first-ever measured silicon performance on Vera Rubin NVL72.
DeepSeek R1, one of the reasoning models driving the current surge in agentic AI, was run across both Vera Rubin NVL72 and NVIDIA Blackwell NVL72. In this evaluation, token throughput per megawatt was measured against interactivity (as TPS/user), which indicates the responsiveness a user or agent experiences while a model reasons through a task. At a matched interactivity target, Vera Rubin NVL72 generated 10x tokens-per-second per megawatt compared to NVIDIA GB200 NVL72 on the same DeepSeek R1 workload.

While delivering similar per-user interactivity, Vera Rubin NVL72 delivers up to 10x higher tokens per megawatt per unit of energy on Vera Rubin NVL72 at similar TPS/user compared to GB200 NVL72.

## What this performance improvement really means
This evaluation compares the performance on each platform with all major, state-of-the-art inference optimizations turned on. These include large-scale expert parallelism, NVFP4 precision, multi-token prediction, and disaggregated prefill and decode, all enabled using NVIDIA TensorRT-LLM and NVIDIA Dynamo.

At similar interactivity targets, Vera Rubin NVL72 delivers an order-of-magnitude improvement in token throughput per megawatt, empowering CoreWeave customers to run far more reasoning-model traffic within the same power budget or run the same traffic on far less power. That means lower cost-per-token and more room to scale at the same infrastructure investment, which is beneficial for agentic workloads that call tools and reason across many steps. 
Here's what this will look like in practice:
- A global cybersecurity company expects to run threat detection inference at 10x better performance per watt, letting them scale agentic security across more endpoints without growing their data center footprint.
- An autonomous coding agent company expects a similar jump in inference per GPU at a fraction of the token cost, letting agents stay on hard problems longer without breaking unit economics.
- An AI-native search engine already running on GB200 NVL72 expects a similar jump in inference throughput per GPU, letting them expand real-time, cited-answer search to more users without breaking response-time targets.

### Scaling agentic AI with NVIDIA Vera Rubin NVL72
Reasoning models like DeepSeek R1 don't answer in a single pass. They plan, check their own work, and revise, generating far more tokens per query than a typical response. Every one of those tokens has to move through memory and across the NVLink domain, which makes interactivity, not raw FLOPs alone, the number that decides whether an agent feels instant or sluggish. 
That's exactly the constraint NVIDIA Vera Rubin NVL72 was built to address. 72 NVIDIA Rubin GPUs and 36 NVIDIA Vera CPUs share a single rack connected by a 260 TB/s all-to-all NVLink 6 fabric, with native NVFP4 support built into the Transformer Engine.
We've invested heavily in the operational layer underneath it to make sure that these efficiency gains hold up once a customer's workload is running in production at scale. We've written before about how CoreWeave operates rack-scale AI as a cloud service, from the patent-pending liquid cooling in Valvey to the unified rack control in Racky, all coordinated by our Rack LifeCycle Controller.

### A foundation for even more performance gains
We've seen this pattern before. When CoreWeave brought GB200 NVL72 online, initial inference numbers improved substantially over the following months as we tuned scheduling, networking, and the software stack around the hardware. This work was reflected in results like our record-breaking MLPerf inference submissions and our two-minute DeepSeek-V3 training benchmark. We expect the same trajectory here: this measurement is a starting point on Vera Rubin NVL72,  and we'll continue to publish updated numbers as optimization work progresses. 
Ready to start planning your Vera Rubin NVL72 roadmap? Contact us here. 

Want to go deeper? Here’s where to look next:
- Go inside our engineering work for NVIDIA Vera Rubin NVL72 
- See what NVIDIA Vera Rubin looks like on CoreWeave Cloud
- Watch the replay: Scaling the Agentic Era with NVIDIA Vera Rubin NVL72, live with SiliconAngle's theCUBE

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

No items found.

Copy code

Copied!

No items found.
