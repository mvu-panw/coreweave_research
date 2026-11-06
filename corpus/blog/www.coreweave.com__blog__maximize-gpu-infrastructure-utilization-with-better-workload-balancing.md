# How To Get Better Workload Balancing | CoreWeave

Source: https://www.coreweave.com/blog/maximize-gpu-infrastructure-utilization-with-better-workload-balancing

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Even heavy-hitter tech enterprises experience workload balancing as one of the most challenging paradoxes in getting AI solutions to market fast while balancing costs. In the current market, it’s an expectation—not a request—that teams quickly switch their use of AI Infrastructure between pre-training, fine-tuning, experimentations, and inference workloads. Sharing compute resources must be almost seamless to meet customer and business expectations.
Here’s the issue: Inference workloads are typically periodic, meaning compute usage fluctuates based on customer usage. Meanwhile, training workloads run in batch jobs that require massive amounts of compute. As such, inference and training traditionally run in two completely different cluster environments. 
For training, that’s typically Slurm; for inference, that’s typically Kubernetes. That’s two different teams. Two different specializations. Two different environments to manage—with less than ideal compute resource utilization and valuable GPU idle time when not managed properly.
At CoreWeave, we’re constantly looking for ways to improve client experience and match your needs as they shift and grow.  That’s why we developed SUNK—aka Slurm on Kubernetes—an implementation of Slurm deployed on Kubernetes that allows AI teams to handle training and inference jobs on the same cluster.
Three critical features in SUNK optimize production times and balance resource distribution between workloads, accelerating time to market.

## Workload balancing resource flexibility
Due to their distinct operational models, Slurm, a highly scalable workload manager primarily used for high-performance computing (HPC), and Kubernetes, an industry-standard platform for automating containerized applications, are typically managed separately. 
SUNK works to better integrate and layer Slurm and Kubernetes environments. By reducing the boundary between these two solutions, SUNK simplifies the orchestration of both training and inference workloads. That allows faster resource sharing between traditionally disparate workloads, minimizing downtime between training and inference jobs.
AI enterprises no longer have to manage two distinct clusters. Instead, resources across both systems are shared in one singular environment, one singular cluster.
Running jobs on one cluster helps optimize resource allocation, improve compute utilization, and simplify the overall workload management of AI projects. That means less time balancing GPU compute allocation across separate clusters and more time focused on developing and deploying the latest and greatest models.

## Simplified scale
Traditionally, scaling often involves time-consuming adjustments or over-provisioning of compute to ensure resources are available when needed. That can lead to a lot of waste and inefficiency. 
Running training and inference in an environment that readily shares resources helps simplify scaling. With SUNK, AI teams can easily allocate compute based on each workload’s unique immediate needs. For example, during periods of low inference demand, those resources can shift to support training—and vice versa. 
Additionally, AI enterprises can see more consistent product feature development throughput and a faster feedback loop between features development and customer feedback. This helps accelerate time-to-value for new features and capabilities by removing bottlenecks caused by poor infrastructure usage and efficient workload balancing.

## Support and ease-of-use

At CoreWeave, it’s one of our top priorities to ensure our customers feel supported. 
Our teams can deploy the bare version of SUNK within hours, enabling your organization to get started with better workload balancing ASAP.  We provide a highly involved onboarding phase and a team of engineers ready 24-7 for day-to-day support, so your teams will always have assistance on hand. CoreWeave solution architects are just a Slack message away, ready to help at a moment’s notice.
Plus, we made SUNK easy to use. It lowers the barrier to entry by layering a more familiar interface (Slurm) onto a more complex but necessary environment (Kubernetes). Instead of hiring two separate infrastructure teams to handle both Slurm and Kubernetes, AI enterprises can successfully utilize SUNK with just one. 

## Infrastructure purpose-built for AI
SUNK integrates training and inference jobs into a unified cluster by reducing the boundary between Slurm and Kubernetes. That means reduced resource strain and minimized idle time—all while maintaining high efficiency and performance. 
Paired with CoreWeave Tensorizer, which cuts down model and checkpoint load times by up to 40% on average, SUNK exponentially reduces resource costs and improves compute utilization. Our full suite of solutions lays the foundation for a highly performant, highly resilient infrastructure specialized for AI workloads. 
That makes us a true AI HyperscalerTM and a world-class partner for AI. With highly resilient and performant solutions, a 24/7 team of engineering experts, and greater observability, we empower AI enterprises to accelerate innovation, reduce overhead, and quickly and confidently get their models to market. 
At CoreWeave, we keep our finger on the pulse of the industry’s current and future needs. Read more about how training clusters might transform in 2025—and what we’re doing about it.

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

SUNK,

Copy code

Copied!

SUNK,
