# Achieve AI Infrastructure Goodput of up to 96% with 3 Key Strategies

Source: https://www.coreweave.com/blog/achieve-ai-infrastructure-goodput-of-up-to-96-with-3-key-strategies

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Goodput, or the amount of compute time spent doing meaningful work, is an essential metric indicating AI cluster performance. Training foundation models efficiently has become a critical challenge as we push the boundaries of model size and complexity—and aim to maximize hardware performance. As such, optimizing the training process to maximize goodput is paramount due to its direct impact on a team's ability to build, train, fine-tune, and deploy AI applications in a timely and cost-effective manner.
 
At CoreWeave, the AI Hyperscaler™, we’ve designed our cloud platform from the ground up to maximize the performance and efficiency of state-of-the-art infrastructure to minimize interruptions and recover quickly from interruptions to deliver a goodput as high as 96%. Higher goodput, in turn, helps enable leading AI labs and enterprises to innovate faster, maximize the utilization of their infrastructure, and lower overall model training and deployment costs. 

In this blog, we’ll explore three strategies we apply at CoreWeave to optimize resource utilization and deliver the higher goodput from AI infrastructure. 

## Why GPU reliability matters and challenges in training large models
Scaling laws represent empirical observations that state that the performance (i.e., quality) of foundational models gets better as you increase the size of the models and train them against a larger corpus of data. To achieve higher linear improvements in model quality, the model parameters and data set size grow exponentially, necessitating an exponential growth of compute required. 
Figure 1: Foundational model scaling laws necessitate more orders of compute
At the same time, the pace of innovation for new models has also accelerated, and the average time between launches has reduced to around 120 days, as shown in the chart below. 
Figure 2: Time reduction between new model launches
Leading AI Labs and enterprises are training the latest FMs using clusters with tens of thousands of GPUs and training jobs spanning days to multiple weeks. With new and evolving technologies and hardware (e.g., GPUs and system interconnects), job interruptions are common, even expected. 
Unlike traditional general compute workloads, GenAI workloads are more prone to job interruptions due to the massive parallelism applied across thousands of GPUs—where the failure of a single component (GPU, network, memory, cable, cooling, etc.) can result in the entire job failing for an unoptimized cluster. Diagnosing, troubleshooting, and recovering from these failures is critical to increasing infrastructure utilization and delivering faster time-to-market for new models. 
As such, a higher goodput is better for fast time-to-market. The ideal is 100%. A recent study showed that industry average goodput is close to 90%. But at CoreWeave, our customers experience a goodput of up to 96%. 

Here are three key strategies we use to make that a reality.

## 1. Start with high-performance hardware optimized for AI workloads
AI labs and enterprises require access to specialized GPU-based computing environments designed to handle the unique challenges of running AI workloads. Each layer of the technology stack—including data center architecture, compute resources, networking, storage, and infrastructure management —must demonstrate proven performance, scalability, and efficiency to run AI workloads reliably. 
For example, GPUs selected must be optimized for LLMs with high-bandwidth memory and rapid data access. Additionally, networking fabric should offer low-latency, high-throughput interconnects. 
At CoreWeave, we’ve created a purpose-built cloud with the latest infrastructure, offering resilient and reliable GPU clusters to power some of the world’s most compute-intensive AI workloads. We are first-to-market with the advanced NVIDIA GPUs, including the latest NVIDIA GB200 NVL72 systems. That allows our customers to take advantage of among the most cutting-edge chips that provide compute on the massive scale required for reliably running AI model training and experimentation. 
Additionally, we built our networking architecture with NVIDIA Quantum-2 InfiniBand fibers, which allows us to deliver a highly performant multi-node interconnect at supercomputing scale. We leverage NVIDIA BlueField-3 DPUs to offload, accelerate, and isolate networking from GPU nodes, allowing compute capacity to focus specifically on AI workloads. 
Our software stack is also purpose-built and optimized for running AI workloads. CoreWeave Kubernetes Service (CKS) runs Kubernetes directly on high-performance bare-metal servers for maximum performance and efficiency. With Slurm on Kubernetes (SUNK), customers can easily run Slurm-based workloads on more than 32K GPUs, helping to optimize distributed training performance through topology-aware scheduling, utilizing the speed of the InfiniBand fabric for node-to-node communication. 

## 2.  Identify and remediate interruptions proactively
Job interruptions are bound to happen. Our goal is to minimize interruptions and help enable quick recovery when they do occur. Rigorous health checking and remediation processes are critical to prevent hardware issues from snowballing into more significant interruptions. 
CoreWeave Mission Control provides advanced cluster validation, health monitoring, proactive node replacement, and deep observability. These capabilities help ensure your workloads run on healthy infrastructure, significantly reducing the likelihood of disruptions. By minimizing interruptions and recovering faster, we can help clients achieve a goodput rate as high as 96%. 
CoreWeave Fleet Lifecycle Controller performs rigorous AI infrastructure validation from initial deployment through the entire node and cluster lifecycle. It runs a series of sophisticated tests to validate node health, GPUs, and networking—along with end-to-end testing for the entire cluster before bringing capacity into the production fleet. 
Here’s why that’s important. AI workloads perform complex mathematical operations  at large scale. Silent data corruption can cause the results of these calculations to become slightly off, resulting in job restarts or lower quality results. Our stack works to detect issues as subtle as GPUs solving 1+1=1.999999, which can enable faster identification and remediation of these compounding issues. 
Meanwhile, CoreWeave Node Lifecycle Controller mitigates costly and time-consuming interruptions via continuous monitoring and proactive health checks for your cluster, ensuring nodes work in lockstep with enhanced performance. As soon as unhealthy nodes are detected, we swap out and replace problematic nodes. That allows us to proactively help make interruptions shorter and less frequent, which can enhance goodput. 
Additionally, customers have full transparency into their cluster health and performance not traditionally available due to a reliance on hypervisors. CoreWeave enables you to measure detailed hardware metrics for your cluster, including GPU health indicators and related low-level metrics (such as fan speed and temperature). Coupled with detailed job-level metrics, our observability platform helps measure, monitor, and diagnose interruption issues with greater speed, efficiency, and reliability.
As part of Mission Control, our FleetOps and CloudOps teams work 24/7 in tandem to monitor for signs of deterioration across our entire fleet, leveraging extensive know-how around cluster health and status. Our engineering teams partner closely with customers, operating as their extended team, to help optimize workload performance and improve overall cluster health. 
Figure 3: CoreWeave Mission Control 

## 3. Improve fault management with efficient checkpointing and fast model loading
When interruptions happen, AI teams need to reload models from checkpoints before resuming work. If loading times are slow, this can significantly delay experiments, increase iteration cycles, affect GPU optimization, and impact overall goodput. Frequent checkpointing and faster model loading help AI researchers and engineers resume model training or inference without excessive downtime, keeping projects on track and maintaining momentum.
CoreWeave Tensorizer delivers secure, industry-leading model loading performance, allowing for asynchronous checkpointing and virtually eliminating any impact of checkpointing. It helps enable efficient checkpointing and accelerates model load times post-checkpointing, which reduces post-interruption recovery time. CoreWeave Tensorizer’s fast model loading also helps reduce latency during inference. CoreWeave also provides container images optimized for our platform, enabling customer workloads to extract higher performance across every layer of the stack. In addition, CoreWeave AI Object Storage (CAIOS) provides data transfer speeds as high as 2 GB per second per GPU across hundreds of thousands of GPUs, reducing the impact of data transfers. 

Figure 4: CoreWeave Tensorizer reduces model load times

## Goodput in action
We trained a representative LLM foundation model on a CoreWeave cluster over 4,096 GPUs and observed an average of 0.96 interruptions/day and a goodput rate of 96%. In contrast, one of the leading AI labs recently published details of their infrastructure usage and saw 2.16 interruptions/day and a goodput of 90%.  Meanwhile, similar to our internal testing, CoreWeave customers observed 96% or higher goodput rates across clusters of 4K and 15K GPUs and observed 0.54 interruptions/day and 1.3 interruptions/day, respectively. 
Additionally, a study by an AI Lab found that mean time to failure (MTTF) for a 1K GPU job was 7.9 hours—whereas CoreWeave internal testing for the same size cluster showed MTTF range starting at 34 hours and ending at 104 hours, with an average MTTF of 69 hours. 
Lower interruptions, faster recovery and higher goodput ultimately result in faster training times and several millions of dollars in saved costs. These results are supported by CoreWeave’s purpose-built AI infrastructure, proactive monitoring, replacement of GPUs based on early indications of failure to minimize interruptions, and efficient checkpointing and model loading—driving overall goodput improvements.

## Get support for goodput and GPU optimization
Optimized goodput is fundamental for staying competitive in today’s innovative market. As GenAI models grow in complexity and scale, AI teams must leverage specialized and high-performance hardware, enable proactive fault management, and implement efficient checkpointing and model loading. 
All those needs can take up a lot of bandwidth that AI enterprises and labs simply don’t have left to spare. 
At CoreWeave, we’ve built a platform ready to provide solutions specialized for GenAI use cases, including enhanced goodput and GPU reliability. We act like a partner for AI enterprises, helping them focus on groundbreaking innovation while we handle the complexities of infrastructure.

### Watch our webinar to learn more‍
Whether you're building large language models, training cutting-edge multimodal systems, or optimizing inference pipelines, CoreWeave provides the foundation for AI-driven success.
Sign up for our webinar, led by CPO Chetan Kapoor and SVP, Engineering Chen Golderg, which will discuss one of our platform's most essential components: maximizing GPU performance.

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

Mission Control,

Copy code

Copied!

Mission Control,
