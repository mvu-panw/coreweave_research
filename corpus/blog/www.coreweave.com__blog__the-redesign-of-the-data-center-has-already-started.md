# The Redesign of the Data Center Has Already Started | CoreWeave

Source: https://www.coreweave.com/blog/the-redesign-of-the-data-center-has-already-started

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In 2023, the world started to see the proliferation of AI applications across industries. What is powering that revolution? Data centers: the beating heart behind the AI boom. 
The explosive growth in artificial intelligence applications has demanded a complete reevaluation of the traditional data center. Existing infrastructure generally isn’t designed or equipped to handle the massive parallel processing power and memory that AI workloads require. In 2024 alone, the world is expected to generate 1.5x the amount of digital data it did just two years ago. 
Undoubtedly, demand from AI workloads will soon outpace traditional cloud computing, and a one-size-fits-all approach fails to meet the requirements of AI developers, who need custom-built solutions, for their immense and specific needs. 
‍

## The Problem with Traditional Data Centers
Traditional clouds were mainly built to support general-purpose applications, offering a balance of performance and cost. Most computing power was designed for workloads like web servers, ecommerce sites, and databases – not the processing power for training a Large Language Model (LLM). 
The challenge with traditional data centers is that they were built to: 
- Balance for cost performance: In other words, there aren’t special considerations put in place to optimize for specific types of workloads.
- Support fragmented use: Meaning, the workloads scale much more incrementally. There isn’t a need for massive parallel processing power, or large amounts of storage because these things can be provisioned as the applications slowly grow.
- Power CPU-first workloads: Which draw significantly less power and generate magnitudes less heat compared to GPUs.
AI developers demand custom-built solutions for immense and specific needs – i.e., enormous capacity, on demand, and instant high-level tech support.
Existing data centers don’t have the necessary architecture, cooling, and software to run AI, or accelerated computing workloads. 
Let’s break down these components: 
‍
Architecture
Power density per server has quadrupled compared to CPU servers. Traditional data centers are designed with five-to-10 KW per rack as an average density. The advent of AI now requires 60 or more KW per rack. With the same amount of power, only a fourth of the traditional data center can be equipped with GPU servers leading to wasted space. 
While AI data centers require 5-10x more power than traditional facilities, the amount of compute generated per GPU is significantly more energy-efficient than traditional CPU-based computing. Moreover, AI applications generate far more data than other types of workloads and thus require significant amounts of storage capacity.
‍
Cooling
Multi-GPU servers generate a ton more heat than a traditional server – which presents two challenges as a result: 
- The current air cooling solutions in place are stressed and need the GPU racks to be spread out to effectively cool them. 
- Next generation racks can consume up to 120kW of energy per cabinet, up 3-5x from regular racks, generating heat that cannot be air-cooled. 
The servers will need liquid cooling, which traditional data centers aren’t built to support.
But implementing direct-to-chip liquid cooling can be a significant challenge, as it requires a redesign of the existing infrastructure, including plumbing, pumps, and heat exchangers.
‍
Software
Traditional software accounts for redundancies and can fall back on other pieces of hardware if one fails. LLMs train as a cluster, with significant cost implications if the hardware fails. Unlike traditional data centers, losing GPUs is not efficient or affordable, so you need a purpose-built software stack to optimize your workload performance and auto-recover from interruptions.
‍

## Transitioning Legacy Data Centers for AI: A Comprehensive Retrofit
Retrofitting legacy data centers to transition into AI facilities involves substantial upgrades to hardware and even the building structure to prepare it for handling new types of workloads.
This transition requires significantly enhancing the data transfer capabilities, as AI and HPC applications rely on processing large volumes of data at high speeds. Specifically, some things that need to change include:
- Replacing the hardware with components that are capable of processing and transmitting large quantities of data in real time. Things like servers, switches, cables, and storage.
- Reconfiguring the existing network-backbone to support much higher bandwidth, ensuring efficient communication between densely packed GPU racks and remote storage systems. 
- Redesigning the layout, cooling, power and even cabling systems to accommodate the increased density and interconnectivity of GPU racks.
Doing this will enhance the data transfer capabilities significantly, as AI and HPC applications rely on processing large volumes of data at high speeds. 
‍
Reimagining the Data Center
We’ve been busy reimagining the data center from the ground up so they are optimized for AI workloads, and have a network of 17 data centers today. Let’s examine how we’ve done this. 
‍
Power
The first step is power. Redesigning the power to prepare for managing these workloads happens at the data center level and at the rack level. We design and implement power monitoring and management systems that can both monitor and dynamically adjust workload scheduling based upon power infrastructure optimization. We can predict workload spikes and adjust cooling and power distribution preemptively. In legacy enterprise data centers, the power system must be converted from “system plus system” (2N) to distributed redundant (N+1) to increase the capacity of the data center. This maximizes the power that can be drawn from existing data centers while maintaining a significant level of resilience. 
‍
Cooling 
In the future, liquid cooling will exist in every part of the data center and will require significantly less water than air-cool systems. Cooling a server with tomorrow’s advanced GPUs is not possible with just air. Incorporating liquid cooling into new data centers requires planning and investment in specialized plumbing and infrastructure. 
We’ve designed infrastructure that supports the circulation of cooling liquid, whether it's water or a specialized coolant, to and from the GPU servers.  Key components include pipes, pumps, heat exchangers, and reservoirs, all designed to handle the specific thermal load of the data center. Additionally, the infrastructure must ensure leak-proof and corrosion-resistant operation to protect the electronic equipment.
‍
Networking
Transforming data center connectivity is not just about connecting servers – it’s about facilitating high-speed, efficient communication between GPUs. This is crucial in an AI-driven environment where parallel processing is the standard. GPUs are like elite athletes in a relay race. The speed at which they pass the baton (data) determines the team’s overall performance. We’ve committed to building our supercomputer scale GPU clusters using technologies to optimize both performance and reliability for workloads that require tens of thousands of GPUs to operate simultaneously.
‍
Software
The secret weapon in CoreWeave’s service offering is our purpose-built software stack that handles the lifecycle of these massive scale GPU first data centers. From initial provisioning and hardware validation through passive and active health checking, all the way through custom intelligent orchestration and scheduling features, CoreWeave’s GPU-first data centers are controlled with one principle in mind: optimizing the FLOPs available for production workloads 24/7/365.
In addition to optimizing for the health, performance and availability of the GPU first data center, CoreWeave has also developed many tools to help optimize our partners’ workloads. Two examples of this are SUNK, our integration of Slurm on Kubernetes, and Tensorizer, a near-zero-copy model loading library to optimize the responsiveness of inference auto-scaling.
The result has been that we’re designing scalable supercomputers that have redundancy built in, resulting in:
- Faster, more performant applications that are more efficient than applications run on top of decades-old legacy structures.
- Serverless Kubernetes deployments, which allow us to provide the fastest spin-up times, responsive autoscaling, and the ability to “burst” across hundreds-to-thousands of GPUs per workload.
- Reliability, with infrastructure that is purpose built to solve for the challenges presented by these large-scale challenges. 

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
