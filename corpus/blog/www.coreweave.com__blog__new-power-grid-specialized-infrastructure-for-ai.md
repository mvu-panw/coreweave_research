# Evaluating Specialized AI Infrastructure | CoreWeave

Source: https://www.coreweave.com/blog/new-power-grid-specialized-infrastructure-for-ai

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In Summary:
- AI companies looking to keep pace with the rapidly changing industry face a common challenge: How to plan for and access the GPU infrastructure needed to train and serve models.
- CoreWeave is a premium cloud provider purpose-built for AI and GPU-accelerated workloads; our solutions have been tested and trusted by leading AI companies.
- AI companies should start planning now for the level of compute they need in 2024, evaluating the availability of high-performance NVIDIA GPUs and the role of specialized infrastructure.
________________________________________________________________________________________
During his keynote at NVIDIA GTC last March, NVIDIA founder and CEO Jensen Huang described the time we’re living in as “AI’s iPhone moment.” Others have referred to it as the “AI Gold Rush” or an “AI arms race.” However you think about it, what’s clear is that the tools that will fundamentally change how we engage with AI technology are being built right in front of our eyes. 
AI businesses have an immense sense of urgency to train new models,  get their products to market faster, and serve surging end-user demand. The adoption of this technology is unprecedented: ChatGPT scaled to 100 million users in just two months after its launch—it took TikTok nine months to reach the same user base. However, alongside the excitement and innovation of this AI boom come challenges. 
AI requires sophisticated infrastructure at scale, built on top of a complicated supply chain, high-end data centers, and advanced networking. Given the complexities involved in building the cloud platforms that are powering the AI boom, it’s important to note that specialized infrastructure for AI and machine learning (ML) is not fungible, and performance matters: the faster you can train your models and serve end-user requests, the faster you’ll get your products to market and capture market share.
To acknowledge the elephant in the room, demand for this infrastructure has never been greater. AI is taking the world by storm, so companies that require access to GPUs to fuel their businesses need to be strategic in their approach. Current demand for this infrastructure has pushed the supply chain to the brink and overrun available data center capacity. Wait times for state-of-the-art training clusters can be as long as six to nine months, according to an WSJ report.
Given this situation, we’ve put together a guide to help businesses think through these challenges and navigate them effectively:
- Move past the “one size fits all” cloud model.
- Recognize that specialized AI/ML infrastructure isn’t fungible.
- Be strategic about your capacity planning.
- Prioritize availability.
‍

## 1. Move past the “one size fits all” cloud model. 
The hyperscale clouds built incredible businesses bringing infrastructure to the market that provided an on-ramp for the world to move to the cloud. Need to host a website? Move patient files from the back room of a doctor’s office to the cloud? Train a world-class AI model? You can do all of those things in legacy generalized clouds, but they all run on the same underlying infrastructure—each workload having vastly different requirements, needs, and levels of complexity.
Enter the modern, specialized cloud, purpose-built for GPU-intensive workloads: AI, VFX, and life sciences. CoreWeave’s base orchestration layer is a fully managed serverless Kubernetes infrastructure designed to give you the advantages of bare metal without the infrastructure overhead. This specialization delivers the performance needed to propel the industry forward. 
While other cloud providers offer a one-size-fits-all infrastructure for the broadest range of use cases with a limited variety of GPUs, it’s important to recognize that not every model has the same requirements. Many AI-powered apps deploy a variety of different models and product tiers: serving them all on the same type of GPU is expensive and scale-limiting. 
With a variety of GPUs ranging from 8GB to 48GB available on demand and at scale on CoreWeave Cloud, clients can “right size” the majority of their single-GPU training and inference workloads on the hardware that meets the requirement of their product. This empowers you to avoid getting crushed by user growth and achieve significantly better performance-adjusted costs.
Case Study: When NovelAI exploded in popularity with its beta launch, they went looking for a cloud computing solution that didn’t drown them in costs or latency. CoreWeave helped the team serve requests 3x faster, resulting in a much enhanced user experience and significantly better performance-adjusted cost.
‍

## 2. Recognize that specialized AI/ML infrastructure isn’t fungible.
With so much demand for the latest high-performance GPUs, getting your hands on GPUs may sound like the silver bullet. Many of the clients who come to us looking for high-performance GPUs assume if they have them, it will work. The reality is much more complex. 
You don’t just need the hardware and all the right pieces to create your own infrastructure. You need the expertise to put it together. 
Running tens of thousands of GPUs successfully is complicated—something CoreWeave knows first hand. You need complex health checking, plans for hardware failures, intricate monitoring systems, and performant networking and storage solutions. This expertise and know-how is extremely difficult to short-circuit. 
To keep pace with the market, you also need the best possible performance. We’ve committed to building our training clusters with state-of-the-art 3200 Gbps InfiniBand networking and SHARP support, instead of other lower-performing (and less complicated) Ethernet-based network topologies. For our clients, performance isn’t negotiable, and this year’s MLPerf results say it all: our commercially available networking architecture produced results that were 29x faster than the runner up. This infrastructure isn’t fungible, and who you get it from really matters.
‍

## 3. Be strategic about your capacity planning. 
To make sure your business is positioned to succeed in 2024, it’s imperative that you think about your accelerated computing strategy, especially when it comes to the most in-demand, high-performance GPUs.
We’re beginning to see forward-thinking businesses start to anticipate this, and plan, raise funds, and contract as needed for the level of compute they’ll need next year. This ensures they’ll have what they need when they need it (“If you wait, it will be too late”).
CoreWeave was among the first cloud providers to deliver NVIDIA H100 Tensor Core GPUs and will have tens of thousands online by the end of the year for early movers on this infrastructure. Not only that, but CoreWeave will also be the first cloud provider to offer the NVIDIA L40S GPU starting later this year, which delivers up to 1.7x the AI performance of the NVIDIA A100 Tensor Core GPU. While other clouds have started to deliver their first systems to clients in H2, CoreWeave is doing it at a meaningful scale.
Preparing now can ensure that you won’t be caught in the same place in 2024. Businesses that pick an infrastructure partner with a proven track record and work collaboratively to plan their capacity are going to be positioned well. 
Wherever you are in this process or whatever your goal—be that training a model on your own data or building a business plan for AI—there are steps you can take now to ensure you have the infrastructure and compute capacity you need. 
‍

## 4. Prioritize availability. 
At the end of the day, GPUs with the latest architecture are going to flat-out perform better than others. To train foundation models quickly, you need high-end GPUs with NVIDIA InfiniBand networking. But what happens if you can’t get it for months?
Plan ahead for the capacity you’ll need, but don’t sit on your hands in the meantime. For example, rather than waiting months to start training a model that will take you days to train on NVIDIA A100 or NVIDIA H100 GPUs, think outside the box to determine if you can start now on other GPUs. While your model may take twice as long to train on other infrastructure, if you can start now, you may get to market faster.
Case Study: Instead of waiting for NVIDIA A100 GPUs to become available to start training, Bit192 trained its 20B parameter Japanese language model from scratch on NVIDIA A40 GPUs, which allowed them to access the level of compute they needed immediately and bring their model to market faster.
Same thing for inference. If an NVIDIA A100 GPU is going to deliver lower inference latency than, say an NVIDIA A40 GPU or an NVIDIA RTX A5000 GPU, does it matter if you can’t get enough of them? Develop a plan to prioritize your preferred GPUs, and spill over to infrastructure that’s available in order to keep your business moving forward.
Case Study: Unsatisfied with legacy cloud offerings, including an underwhelming GPU selection and an unoptimized solution for inference workloads, Tarteel AI saw multiple growth opportunities with CoreWeave. Since migrating its inference service for its AI-powered Quron study app, Tarteel saw a 22% improvement in latency and ~56% cost reduction compared to its previous cloud provider.
Infrastructure is essential to your success in AI. With the flexibility and optionality CoreWeave provides, you’re empowered to make smarter decisions for your business, strategically plan your compute capacity, and leverage the GPUs that deliver the best performance-adjusted cost for you. 
To learn more or start a conversation about capacity planning, reach out to our team today. We look forward to helping you build incredible products and solutions.
‍
This blog post is also available for you to watch on-demand as Max Hjelm's session from Ai4 2023.

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
