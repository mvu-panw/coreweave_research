# Why Liquid Cooling Matters for AI Scale | CoreWeave

Source: https://www.coreweave.com/blog/why-you-need-liquid-cooling-for-ai-performance-at-scale

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

AI is a hot topic—literally. A typical AI server rack (~50kW) produces as much heat as 10-25 ovens running simultaneously (2-5kW) and would require the cooling power of 3-4 home central AC systems. 
Now imagine a large-scale training cluster that contains 50-100 of those server racks, but with a power density of 120+ kW, and things really start to heat up.
Today, most data centers cool GPU server racks with air cooling. However, traditional air cooling methods are often insufficient for the high-density racks of modern AI data centers. As AI demand scales, many cloud providers seek more energy-efficient accelerated computing platforms and liquid cooling systems to improve energy efficiency, increase rack power density, and enable access to the latest GPU hardware. 
The type of cooling system used to cool AI infrastructure can have benefits, like greater performance, power efficiencies, and a smaller footprint.
‍
Coolant bags attached to an NVIDIA GB200 NVL72 rack in a CoreWeave data center.
‍

## What’s driving AI data centers toward liquid cooling?
More power. More heat. Foundational models have ballooned in size over the past two years, especially considering cluster sizes and datasets. ChatGPT-4 represents over a 10-fold increase from GPT-3's 175 billion parameters. As we look into the future, we expect future foundation models to be larger than the current ones.  
Currently, an 8-GPU NVIDIA HGX H200 server supports up to 1.13TB of shared GPU memory. To accommodate a 10x increase in model sizes, systems will need to scale shared GPU memory beyond 10TB. Given there is a physical limit to the number of GPUs in a single server and because the memory size per GPU cannot keep up with the pace of foundational model size increases, we need to interconnect GPUs in a single high-speed NVLink domain. 
This has given rise to extremely dense GPU deployment architectures like the NVIDIA GB200 NVL72 with 13.5TB of shared GPU memory across 72 Blackwell GPUs interconnected via NVIDIA NVLink in a single rack-scale server.
Traditional data centers and air cooling technologies weren’t built for modern AI demands and rack-scale solutions. Plus, the pressure to be first to market with this infrastructure—without breaking the bank—presents a major challenge for AI companies.
Liquid cooling is essential to safely increase the number of GPUs per rack and rack power density. That’s a big reason why new AI data centers rolling out in 2025 are expected to be liquid-cooled.
To understand the need for more efficient cooling solutions, we first need to discuss rack power density, the limitations of air cooling, and the impact of the new, high-performance chips.
‍

### NVIDIA GB200 NVL72 and the impact of energy-efficient computing 
Thermal design power (TDP) of GPUs and performance per watt is rising—and quickly. Data center providers use this measurement to calculate the maximum amount of heat generated, measured in watts (W) or kilowatts (kW). If the cooling solution can’t handle the TDP in an AI server rack, the rack will overheat and degrade the performance of the whole system. 
Higher computational needs of GPUs necessitate higher power requirements. The increased power requirements are driving the demand for improved cooling technologies. For example, NVIDIA's GB200 NVL72 rack consumes roughly 130 kW per rack, making it one of the most power-dense racks in history, while using up to 25X less energy for massive model inference. See how that compares to previous generations:
Chart shows the evolution of performance and rack power density from the latest NVIDIA GPU architectures.

### Increasing rack power densities
This massive jump occurred in just over two years and is driving the immediate demand for increasing rack power densities. After all, it’s not as simple as stacking fewer servers in a rack to keep the power consumption at bay.
AI training clusters require hyper-connected servers linked together in a data center to better optimize speed and performance. For cloud providers, that means delivering more GPUs in a data center and keeping those GPUs closer together. 
In short, rack power density needs to increase to ensure access to the latest NVIDIA GPUs for training and inference. 
Chart shows how the average amount of GPUs and the rack power density in an AI server rack have increased over the past few years.

## What liquid cooling means for CoreWeave customers
While the method for cooling may not be top-of-mind for our clients, the benefits might pique their interest. Some of the most notable benefits include:

- More GPUs closer together: Bringing compute closer together means each individual part can talk to each other faster, improving the overall performance of your cluster. Larger models can be trained on a 72NVL setup, enabling more data to be processed faster.
- More GPUs across all data centers: Liquid cooling enables greater rack power density, which allows providers to stack more GPUs in each server rack without risking the cooling system falling short. This increases the overall amount of GPUs CoreWeave can deliver to our clients across the globe.
- Access to newer hardware generations: Liquid cooling plays a huge role in making NVIDIA Blackwell architecture available, as GB200 has a significantly higher TDP than previous generations.
- Improved power utilization: Liquid cooling provides up to 30% better power utilization than air-cooled systems; this improved use of available power improves CoreWeave customers' total cost of ownership (TCO).
In summary, cooling impacts the ultimate performance, energy efficiency, and footprint of your AI cluster. Rising TDPs from new GPUs and increasing rack power densities prove that liquid cooling is not only essential but extremely beneficial to the future of AI. 
‍
Data center technicians evaluating the liquid cooling system in a CoreWeave data center.
‍

## What will it take to bring liquid cooling to data centers in 2025?
Bringing liquid into the data center is a monumental task. A lot of work needs to be done to ensure that this technology is safe, reliable, and efficient.
Over 2025, the majority of CoreWeave’s new data center builds will be liquid-cooled. Liquid cooling as the standard deployment mode helps CoreWeave serve the increasing demands for compute and any new NVIDIA hardware through the rest of the decade.
So, what’s going to take to bring this technology to fruition, and how long before customers start to see the benefits from liquid cooling? A combination of new and old… plus extraordinary scale.

- Redesign > retrofit: Liquid cooling upends physical systems as we know them in legacy data centers. The simpler solution is, in fact, building from scratch. CoreWeave is working hand-in-hand with our data center providers, hardware engineers, and suppliers to build modern, liquid-cooled data centers that meet the incredible scale at which AI demands. 
- Air cooling: Yes, even with the latest GPU generation, air cooling still plays a vital role in the data center. CoreWeave’s current implementation of the NVIDIA GB200 clusters will be 85% liquid-cooled and 15% air-cooled. Air cooling best supports modern AI infrastructure in the less-intensive components. CPU servers and earlier NVIDIA GPU servers are still important for AI applications, and air cooling is a suitable solution.
- Scale and expertise: CoreWeave has been adding liquid cooling to our data centers for the past 18 months and is now expanding these large-scale liquid cooling solutions even more this year. Skilled professionals like data center technicians (DCTs) stand at the forefront of ensuring the efficient and reliable operation of liquid cooling infrastructure, enabling data centers to support the growing computational requirements of AI.
When it comes to meeting AI’s power demands, liquid cooling is the future. Implementing liquid cooling will help the industry continue to leverage next-gen technology that powers our world forward. For CoreWeave, bringing this technology to our customers is a testament to our mission to provide purpose-built cloud services, for which liquid-cooled data centers are a critical part of the foundational layer. See liquid cooling in action.
Learn how liquid cooling plays a key role for NVIDIA GB200 on CoreWeave, bringing groundbreaking advancements for generative AI and accelerated computing.

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
