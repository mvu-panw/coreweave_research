# CoreWeave SUNK adds new capabilities for modern AI research clusters | CoreWeave Blog

Source: https://www.coreweave.com/blog/new-coreweave-sunk-capabilities-help-teams-build-modern-ai-research-clusters

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Modern AI research clusters are still too hard to build. Today, teams have to piece together Kubernetes primitives, schedulers, identity systems, and observability tools. But this piecemeal solution still doesn't give them a system ready for demanding training workloads. Kubernetes-native alternatives continue to require significant infrastructure setup and operational assembly before researchers can do what actually matters: train.
Managing scale shouldn't be a full-time job
GPU access was supposed to be the hard part. For most AI research teams, it isn't. The harder problem is everything that comes after: scheduling, access management, lifecycle operations, observability, cluster behavior across long-running jobs. Teams are still building this themselves. They shouldn't have to.
That’s why CoreWeave is expanding SUNK with new capabilities to address this problem, including self-service and SUNK Anywhere. This evolution makes our AI training system easier to adopt on CoreWeave and easier to extend anywhere you have infrastructure. 
Reducing infrastructure assembly for AI training
SUNK is the industry’s first unified training system purpose-built for your most demanding AI workloads such as months-long pretraining runs, large-scale reinforcement learning (RL) workloads, and agent environments. It enables valuable Slurm workflows while delivering the operational advantages of Kubernetes, giving your platform teams and researchers a more streamlined path from cluster bring-up to productive training. It’s also the market’s most proven Slurm-on-Kubernetes offering, shaped by the realities of running AI at scale.
Our goal is not to add more tooling around the edges of a research cluster. It’s to reduce time spent managing infrastructure while preserving the consistency, visibility, and control required for long-running training jobs. That is the logic behind SUNK self-service and SUNK Anywhere.
Customers reflect this. IBM highlights topology-aware scheduling and custom dashboards as enabling faster, more efficient training runs and higher cluster utilization on rack-scale GB200 systems. Cursor points to shared file systems, automated user provisioning, and customizable environments that let researchers focus on research instead of their tooling. These are the operating advantages of a more unified training system.

### A faster path to a working research cluster
SUNK self-service delivers real value by streamlining the path to production, leveraging CoreWeave best practices to bring SUNK clusters online faster. Reducing bring-up time is only part of the acceleration story. Reducing drift later in the process is just as important. Standardized and opinionated patterns make it easier to start from a production-ready baseline, simplify onboarding, and preserve more consistent cluster behavior over time.

The result? Researchers spend less time waiting on environment setup and encounter less friction between access and experimentation. And platform teams gain a more repeatable way to deploy and operate research clusters without rebuilding the same operating model cluster by cluster.
SUNK also simplifies and secures cluster access. Automated User Provisioning (AUP) uses SCIM to synchronize users and groups from an identity provider into CoreWeave IAM. And SUNK User Provisioning (SUP) automates the POSIX users, groups, SSH keys, and Slurm accounts required inside SUNK clusters. Together, these capabilities reduce manual onboarding work while keeping access aligned to how research environments actually operate.

CoreWeave SUNK Self-Service is a big improvement for customers who want easy deployments. Even if you've got a long term committed contract, there are lots of reasons to spin up clusters quickly in a self-service manner. At the end of the day, speed is the moat. CoreWeave recognizes this, and supports their customers by moving at the speed they need to be successful.
Dylan Patel; Founder, CEO, and Chief Analyst, SemiAnalysis

### Operate wherever you have infrastructure with SUNK Anywhere
Infrastructure flexibility is only valuable if it doesn’t create more fragmentation for the teams actually running training. As organizations expand across providers and customer-owned infrastructure, they shouldn’t have to adopt different training systems,  workflows, or operating practices every time the environment changes.
SUNK Anywhere extends the same unified training system beyond CoreWeave infrastructure. It enables teams to standardize on one way of running demanding AI workloads across environments, instead of splitting training across different stacks. This continuity matters to platform leaders who want portability without a brittle operating model, and to researchers who want familiar scheduling behavior and workflows as infrastructure footprints grow.
CoreWeave’s SUNK gives us the best of both: Slurm for our research scientists and Kubernetes for the observability and production-grade long-lived services our products need. It’s been impressive to see how many edge cases are already well handled. We’re running large distributed jobs across thousands of GPUs on both CoreWeave and non-CoreWeave providers, and deploying SUNK on our non-CoreWeave clusters requires very few configuration changes.
Xander Dunn, Member of Technical Staff, Periodic Labs

## Deeper visibility for AI research
We’re now expanding Mission Control observability with GPU straggler detection. In distributed training, the costly issue is not always a clean failure. Often a single GPU, node, or communication path begins to underperform, slowing the whole job. Extending observability into GPU-to-GPU communication behavior helps teams identify performance outliers earlier and understand distributed training behavior more clearly, all  while jobs are still running. Researchers can pinpoint the exact GPU causing the hang and restart  their job without it.

## What SUNK means in practice
Proof matters. SUNK is designed to maximize productive training time, with up to 96% goodput and 10x longer mean time to failure in benchmark scenarios. The right training system isn't just about peak hardware access, it's about how consistently useful work continues once the job is underway.

## Meeting the needs of modern AI training
AI teams shouldn’t have to choose between familiar research workflows and a performant training system.That’s the role SUNK plays in CoreWeave’s broader AI infrastructure: preserving what researchers need, while giving platform teams a more unified, operationally credible way to run your most complex AI workloads. Yes, research clusters are still too hard to create. And too many alternatives still ask customers to assemble the operating model themselves. That’s why we think teams need a more complete, proven solution: CoreWeave SUNK.
Learn about CoreWeave SUNK

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
