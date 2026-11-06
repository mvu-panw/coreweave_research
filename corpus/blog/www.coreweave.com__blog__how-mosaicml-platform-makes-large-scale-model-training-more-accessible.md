# How the MosaicML Platform Makes Large-Scale Model Training More Accessible

Source: https://www.coreweave.com/blog/how-mosaicml-platform-makes-large-scale-model-training-more-accessible

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### By giving users access to NVIDIA H100 Tensor Core GPUs deployed on CoreWeave Cloud, Mosaic ML puts the highest-performing NVIDIA GPUs within reach for more ML practitioners. 
‍
It’s an uphill battle for small- and medium-sized companies looking to train a machine learning (ML) model or serve inference. The process and infrastructure requirements are more expensive and more complex than ever—and the ballooning sizes of large language models (LLMs) make it all the more challenging. 
While the recent boom in generative AI has helped garner attention for innovations around AI, it has also increased demand for the infrastructure needed to support it. More fish swimming in a small pond, all competing for food. 
However, there’s a growing cohort of companies and nonprofits looking to expand access for smaller players in the AI industry. This requires new, cutting-edge hardware, infrastructure built for scale, and a platform that actually enables companies of all sizes to easily train and serve large AI models. A platform like the one built by MosaicML.
‍

## MosaicML: The generative AI foundry 
The MosaicML platform provides organizations with a high-performance ML model training interface and inference service that abstracts away the complexity of generative AI model development and deployment. With optimized builds, MosaicML enables developers to “skip the setup” and get training right the first time. 
The impact speaks for itself. The platform has 40%+ utilization out of the box with its tuned parallelism settings across model and compute scales. Users can train billion-parameter models in hours rather than days, with impressive scalability for models over 70B hyperparameters. That’s training 2x-7x faster, without changing any code. 
“MosaicML has helped us make the training of our large models so much faster.” 
— Aiden Lee, Co-Founder and CTO at Twelve Labs 
Before launching Mosaic ML, co-founders Naveen Rao and Hanlin Tang worked together at Nervana Systems, a pioneering AI chip startup acquired by Intel. After leading Intel’s AI products group, they left the company to focus on a new promising area of research and development: ML training efficiency through algorithmic improvements. 
They teamed up with Michael Carbin, a professor at MIT, and Jonathan Frankle, then one of his students, now a professor at Harvard, who had written The Lottery Ticket Hypothesis (Best Paper, ICLR 2019). This theory involves pruning a neural network to create a much smaller network capable of similar performance at lower computational cost—a theory that helped shape MosaicML into the platform it is today. 
‍

## Model training for all—no matter how small 
As the state of the art has driven model sizes exponentially larger, MosaicML’s mission to democratize access to scalable, efficient ML training and inference has proven itself to be increasingly relevant. Training large generative models has been too complex and expensive for many organizations, requiring specialized expertise and tooling. As a result, only a few companies have had the capability to build these models. 
However, MosaicML is changing this model. The MosaicML platform provides a large model training stack that “just works,” scaling to hundreds of GPUs by changing a single
configuration parameter, and efficient LLM training code and data streaming to remove the systems and infrastructure headaches. MosaicML has had good traction with a wide range of organizations, from startups such as Replit and Twelve Labs to large financial companies, with more organizations across segments coming on board each month. 
“We built the MosaicML platform to make large-scale model training more accessible. Now, organizations of all sizes can train their own industry-specific models with complete model ownership and data privacy.” 
— Hanlin Tang, co-founder and CTO at MosaicML. 
Mosaic ML’s commitment to democratizing access to GPUs and the exceptional performance of its platform are two reasons why CoreWeave was eager to partner with them. The two companies met while working on implementation for Stability AI and have expanded their partnership ever since. 
“The whole industry benefits from more people from a variety of companies and industries having access to the tools they need to train and serve models. MosaicML gets this, and they’re making it a reality for more companies. It’s one of the many reasons why we were excited to partner with them.” 
— Brian Venturo, Chief Technical Officer at CoreWeave 
‍

## MosaicML expands access to NVIDIA HGX H100 GPUs 
A big piece of the playbook: giving more companies access to the latest, cutting-edge technology. 
ML practitioners who use the MosaicML platform will soon have access to NVIDIA H100 Tensor Core GPUs, the highest-performing NVIDIA GPUs, deployed in CoreWeave Cloud. The NVIDIA H100 offers unprecedented performance, scalability, and security compared to previous hardware generations, which is key to accelerating training and inference of LLMs as well as the variety of innovations that stem from those. 
A key element of AI performance is scalability, and a key hardware element to scalability is fast, low-latency networking. To that end, CoreWeave’s H100 instances have implemented NVIDIA InfiniBand networking in every node as well as top-of-rack switches, which deliver 3.2 Tb/sec of bandwidth. 
“We easily added support for H100s to our platform via integration with the NVIDIA Transformer Engine library, and are undergoing the system optimization process. Customers who can get access to H100s will be able to leverage this integration to get excellent performance from H100s in CoreWeave Cloud servers.” 
—  Hagay Lupesko, VP of Engineering at MosaicML.
‍
Because of the performance enhancements, H100 GPUs are in high demand, which could leave little room for smaller startups and companies with less capital to access these supercomputers. MosaicML, in partnership with NVIDIA and CoreWeave, looks to change that. 
“Realizing AI’s full potential requires relentless innovation at every level, from algorithms to infrastructure and everything in between. CoreWeave’s H100 instance with NVIDIA InfiniBand networking—combined with  MosaicML’s ongoing work in algorithmic optimization—bring together performance, scalability and ease of use to a broader set of AI developers.” 
—  Dave Salvator, Director of Accelerated Computing Products at NVIDIA
MosaicML tested H100 clusters on CoreWeave Cloud to see what cost and performance implications the new supercomputers could have for training LLMs. The results were exciting: 
- Throughput: Training on H100 GPUs with FP8 was 3x faster out of the box than with NVIDIA A100 Tensor Core GPUs with BF16 for the MPT-7B model, a decoder-style LLM. 
- Cost: ~30% more cost effective, right out of the box. 
MosaicML is developing further optimizations that will continue to increase the performance margin, making H100 GPUs even more efficient for LLMs and large transformer-based models. 
‍

## A secure, multi-cloud platform for your data 
MosaicML is a multi-cloud platform, meaning that users can train and deploy their models how they’d like: across multiple cloud providers, on premises, or inside their virtual private clouds on public clouds. MosaicML’s multi-cloud orchestration allows users to take advantage of the GPUs that are available when they need them, regardless of location. 
This setup is optimized to help more clients looking to train large generative AI models in the most cost-effective way, with full control and customization. 
“More developers are employing a multi-cloud strategy to manage their workloads, and it’s important that the experience their users have is consistent no matter where the training or inference is taking place.” 
— Brian Venturo, Chief Technical Officer at CoreWeave 
While there are bountiful business opportunities that LLMs and other advanced AI models can bring, organizations with data privacy and security concerns cannot send their data to an unreliable third-party API. The MosaicML platform enables those organizations to pretrain, fine-tune, and then deploy models while keeping their custom data in-house.
This is made possible through the combination of a simple control plane/compute plane architecture, in which the control plane is responsible only for the metadata needed to orchestrate training and inference deployments, while the compute plane remains entirely within the customer’s secure environment. With this implementation, the company’s training data never leaves its network. 
“Our customers maintain full model ownership and data privacy.” 
— Naveen Rao, CEO at MosaicML 
To learn more about the MosaicML platform, visit their website or reach out to their team to schedule a free demo.

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

Training,

Copy code

Copied!

Training,
