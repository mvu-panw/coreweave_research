# The Future of AI Clusters for Enterprise in 2025

Source: https://www.coreweave.com/blog/building-ai-clusters-for-enterprises-2025

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

The scale and pace of innovation around AI infrastructure is truly incredible. It’s fantastic, and I’m not just saying that because I’m a hardware guy. 
My teams focus on designing, testing, and validating the hardware for some of the largest supercomputers in the world. Over the past year at CoreWeave, we have seen so much change, especially with the rollout of the NVIDIA H100 Tensor Core GPUs last year and now preparing for NVIDIA Blackwell GPUs and H200  Tensor Core GPUs.
When it comes to building these clusters, the majority of the challenges we see boil down to two things: power and efficiency. How do we make sure that we are planning and building our data centers appropriately to handle the stuff for today but also for what’s coming a few years down the road? And, how do we make sure that it’s fast, performant, stable… all the things these supercomputers need to be?
As the hardware guy, some might think that solving these challenges starts at the hardware level. However, it goes far beyond that. We have to address power and efficiency at every level—from the data center to the hardware and software layer—to build a bigger, badder cloud.
‍

## Evolutions at the hardware level

### NVIDIA H100s, NVIDIA GB200, and more
When we think about advances in AI hardware, everyone’s first thoughts are the new NVIDIA GPUs. The NVIDIA H100 was a massive step forward in terms of performance for AI training and inference, and with that performance significantly increased. 
The latest GPUs from NVIDIA are expected to raise the performance even further. Right now, CoreWeave is gearing up for the release of NVIDIA Blackwell.  We’ve been working closely with our customers to understand the applications and workloads they want to run on these latest-generation machines. We’re proud to be among the first providers to deliver large-scale NVIDIA GB200 Grace Blackwell Superchip clusters, which will be interconnected via NVIDIA NVLink and NVIDIA Quantum-2 InfiniBand, to the market, and we can't wait to see what our customers will build with them.
That said, there are many other exciting advances in AI hardware that are helping to build larger and more efficient clusters, including NVIDIA DPUs.

### Data processing units (DPUs)
Data processing units (DPUs), like the NVIDIA BlueField-3 DPUs, are a new class of programmable Network Interface Cards (NICs), which many people are calling the third pillar of computing along with CPUs and GPUs. These NICs are exceptional at offloading tasks from the server CPUs and providing enhanced security for our customers. 
If you’re not familiar with DPUs, think of them like a standard server network card, but with a mini-server built into the actual network card. They are a core part of the glue that connects our server hardware to the rest of the network. Most of our new server deployments contain at least one DPU per server,  which helps us provide a reliable, scalable, and most importantly a modular deployment.
Personally, I’m really jazzed about DPUs. By offloading specific network and storage responsibilities to the DPU, we can continue to offer “bare metal access” to our customers while still maintaining control to help them better utilize our hardware. This allows us to offer the flexibility that cloud customers expect while offering all of the performance benefits of bare metal access.

### Baseboard management controller (BMC)
Finally, a key way to make infrastructure more efficient is by improving observability into the hardware. These systems will inevitably fail, and clients need to know when that happens and what went wrong so that we can fix it quickly.
One server component CoreWeave leverages heavily to enhance observability is the Baseboard Management Controller (BMC). All servers and their DPUs have a baseboard management controller (BMC), an out-of-band device that you can use to manage the server. Traditionally, it’s used to power on hardware, capture telemetry, power thermal information, and gather hardware health information. 
At CoreWeave, we’ve pushed the boundaries of expected uses for BMCs. We have invested heavily in custom automation and have been intentional in doing out-of-band monitoring and management so that we can offer a dedicated metal solution. This allows customers to “BYO” image without losing the monitoring, infrastructure, and tooling we’ve put in place to support these servers. 
‍

## Evolutions in the data center
Greater power demands… Higher expectations for cluster efficiency… These advancements at the hardware level are a major part of what’s propelling the redesign of the data center for AI. 

### Liquid cooling
One of the biggest advancements we’re seeing industry-wide is liquid cooling in the data center. This is a huge change from where data centers were a year ago, and—being in the midst of this transformation—it will mean data centers look and operate differently than they do a year from now.
Unless you’re also a hardware person, you probably don’t care about liquid cooling. Most people just want more GPUs, and it doesn’t matter how they’re cooled. However, I would contend that the reason the end user may care about liquid cooling is that it allows us to deliver more GPUs and the latest NVIDIA GPU products that require liquid cooling. 
In data centers today, you can’t fit the same number of NVIDIA H100 servers or GB200 Superchip compute trays in a cabinet as you could earlier GPU generations because of the higher power and cooling demands. Not only does liquid cooling enable more efficient heat dissipation of the latest chips, it also saves us the power that was earlier being spent on fans. The improved thermal efficiency and power savings allow us to be more generous with how many GPUs we can fit into a rack—which means more GPUs for our customers. 
CoreWeave has a Liquid Lab where we conduct extensive liquid cooling testing, and we’re getting ready to deploy our first “small” liquid deployment of 4,000 GPUs. (I realize that might be a large cluster for some people, but for us, that’s a small cluster.) Gearing up for this deployment is something I’m personally really excited about. It’s been an impressive effort between the hardware engineers on my team, the server manufacturers designing the solution, and our data center partners.
By the end of this year, all our new data centers will be liquid-enabled. So, the next time the new NVIDIA GPU is coming out, we will be good to go, and our clients will get their clusters even faster. 

### Data Center Technicians
In addition to power and efficiency, data centers face another major challenge: speed. Providers and builders are under enormous pressure to get things up and running as fast as possible, from the actual facility to the installation of the hardware. 
One way to do that is through automation, which CoreWeave has been aggressive in integrating into our pipeline, but you simply can’t automate everything. If you ever see a picture of one of our deployments, you see literally thousands of miles of cables all carefully connected and labeled. It takes forever to do that. It’s a very hard and complex task. 
As much as I say, “We’re going as fast as we can, and it’s all automated,” there’s a large group of people in a data center running cables, installing servers, powering things on, connecting systems, and testing stuff. Those are our wonderful Data Center Technicians (DCTs). We have an army of them, and each of them is the best at what they do.
I can talk about hardware all day, but it doesn’t matter how good your gear is if you don’t have the people to support it. With all the changes in the industry, the role of the DCT is more important than ever, and they will continue to be essential to the success of the data center.

### Closer collaboration with partners
For decades, clouds have tried to get water away from the data center. With the advent of liquid cooling, data centers have had to completely rethink this while still ensuring safety, reliability, and efficiency. I can’t stress enough how big of a change this is, and it means we’ve been working closely with our data center partners to create these solutions. 
But it’s not just liquid cooling that has demanded closer working relationships. As I mentioned before, CoreWeave spent a ton of hours with NVIDIA to get the DPUs to where they are today. 
Standardization around hardware and data centers is paramount, so we’ve been collaborating with standards bodies to ensure compliance and support around what we’re building. Redfish is a great example of this; it’s a DMTF-defined standard that provides a REST-ful interface for interacting with data center hardware. Using standards-compliant interfaces like Redfish has allowed us to increase our deployment velocity, and continue to add new monitoring and observability, without getting bogged down in vendor-specific changes.
‍

## Evolutions in software
All of these advancements at the hardware and data center level are intentional to deploy thousand-plus server clusters quickly and have it be seamless for our clients. Minimal effort, maximal scale. Everything is automated. Go as fast as you can. These efforts aren’t fully realized without a sophisticated software stack.

### A robust provisioning and automation pipeline
Large-scale AI clusters are more complex than ever, and now there’s an impossible amount of data to track and monitor. It requires so much time and effort to be an HPC as a service provider. As an LLM lab or an AI enterprise, you don’t want to do that management, and you probably don’t have the resources for it. You’d rather be focusing on perfecting your model or advancing your AI products.
At CoreWeave, we’re aggressively screening every machine to remediate any bugs or faulty hardware as fast as possible and ensure they don’t make their way to a customer. This process includes node lifecycle management and new automation.
We’ve heard from colleagues in the industry how difficult it is to deploy large-scale AI clusters on-premise. They are using the same hardware as us, but they ask, “Why is yours so much faster?” I know that the answer is that we’ve fine-tuned our stack and screened out all the potential performance inhibitors.
Everything is laser-focused on making sure that we have the highest level of observability in the system. The BMC and the DPUs are two primary ways that we do that, and we spend a lot of IP and engineering time to make sure that we are pushing them to their limits—and beyond sometimes.

### Smoother, faster deployments without abstractions
I generally don’t spend too much time up this far in the stack. However, this is where the rubber meets the road for many of our clients. There’s nothing seamless about building an AI cluster, but great software can make it feel that way—without sacrificing control.
NVIDIA has a bank of tools that help, like NVIDIA Triton™ Inference Server. Internally, CoreWeave has also created some unique software, like SUNK and Tensorizer, to improve the functionality, flow, and performance clients experience from the clusters we build for them.
Looking ahead, labs and enterprises will see software playing an even more critical role in their AI infrastructure.
‍

## Why these transformations matter
If you can’t tell, I’m really excited about the evolutions in hardware, data centers, and software we’re seeing at CoreWeave. This is fundamentally different from what users expect from a “traditional” cloud, which was designed to serve a broad range of use cases like hosting a website or storing your cat photos. Most importantly, the impact our clients will see from these changes is going to be huge.
CoreWeave is designing everything to be laser-focused on delivering best-in-class, GPU-optimized compute.  This includes increasing the power density of our racks, deploying liquid cooling for current and future NVIDIA GPU products, and how we execute our provisioning, testing, and validation of nodes.
We want to deploy as much hardware as fast as possible and have that hardware be the most reliable. Period.  By doing this, our clients get next-level performance from their clusters, efficiently test and build their AI products, and ultimately take those creations to market faster.

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

CoreWeave Cloud,

Copy code

Copied!

CoreWeave Cloud,
