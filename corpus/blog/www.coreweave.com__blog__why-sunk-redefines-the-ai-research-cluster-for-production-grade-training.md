# SUNK: Production-Grade AI Training at Scale

Source: https://www.coreweave.com/blog/why-sunk-redefines-the-ai-research-cluster-for-production-grade-training

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Slurm is the industry-standard interface for managing large-scale AI training resources, valued for fair allocation and strong job isolation. But as training infrastructure becomes more complex—and clusters need to evolve quickly—deploying and operating Slurm reliably can create significant configuration and operational overhead.
That’s why we built SUNK (Slurm on Kubernetes): a unified training system that brings cloud-native agility, operational ease, and scalable lifecycle management to Slurm-based AI training by running it with Kubernetes. SUNK is the industry’s first unified training system for the most demanding AI workloads. It helps your teams move faster while maintaining the operational discipline required for large, long-running training jobs through integrated health management and deep operational visibility.

Today, we’re extending that operational ease further with guided self-service (Preview)—an engagement model that provides an opinionated, streamlined experience to deploy and manage SUNK from the CoreWeave console, powered by a Kubernetes operator.

## SUNK: a production-ready, unified training system for AI
Designed and operated as a cohesive system rather than separate layers, SUNK enables production-grade AI training through:
- Intelligent, topology-aware scheduling optimized for large, synchronous training workloads
- Automated health management and failure mitigation that reduces disruption from hardware events and GPU stragglers
- Deep operational visibility from infrastructure health to job-level behavior
- Unified lifecycle management that keeps clusters consistent, upgradeable, and production-ready at scale
Together, these capabilities move teams beyond stitched-together infrastructure stacks toward a dependable, repeatable approach to large-scale AI training.
SUNK also makes it easier for researchers to get started without sacrificing security or operational control. Through SUNK User Provisioning (SUP), the system automates user onboarding and permissions and provides isolated login environments, allowing the right people to get the right level of access in a secure environment. That means teams can start working in minutes, not days, while the organization maintains clear boundaries and strong governance. It reduces onboarding friction, minimizes configuration drift and setup errors, and keeps training clusters aligned with enterprise security requirements (Learn more about SUNK user provisioning).

### Proven at scale. Built for real-world AI training.
This approach is well-grounded in experience. After years of operating research clusters across a wide range of scales and workload complexities, CoreWeave identified proven operational patterns that balance fast time-to-value with the strict controls that expert teams require. SUNK embeds those learnings into a production-ready training system, enabling organizations such as IBM and Cursor AI to scale AI training reliably without needing to assemble and maintain bespoke infrastructure of their own.
“With CoreWeave SUNK, we seamlessly manage clusters with thousands of GPUs. Researcher onboarding is automated, so we can grant and revoke access in under a minute without compromising security. On rack-scale GB200 systems, SUNK's topology-aware scheduling and custom dashboards enabled faster, more efficient training runs and higher cluster utilization. Integrated health checks, automated node remediation, and deep observability reduced interruptions, enabling researchers to iterate faster and platform engineers to spend less time firefighting.”
Brian Belgodere, Senior Technical Staff Member, IBM
“We needed infrastructure that scales without dragging operations along with it. SUNK delivered that out of the box: shared file systems, automated user provisioning, and customizable environments that let our researchers focus on research instead of fighting their tooling. Mission Control's node health checks and remediation alone have saved us significant operational overhead. It just works, and at our pace of growth, that is critical.”
Sam Kottler, ML Infra, Cursor AI
Last year, in their ClusterMAX 2.0 rating, SemiAnalysis recognized SUNK as the only premium, unified training system built to improve cluster utilization and researcher velocity that’s available on the market today.
“CoreWeave’s SUNK was first to market, is proprietary, and continues to be the only viable solution for running both Slurm and Kubernetes jobs on the same underlying cluster.” 
ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System, November 6, 2025

### What makes SUNK work at scale
Training systems can look stable at small scale, but today’s frontier AI workloads often stretch across tens of thousands of GPUs for days or weeks at a time. At that scale, small inefficiencies and routine failures can quickly compound into major slowdowns, reducing goodput and delaying time-to-results.
SUNK is engineered for that type of volatile environment. It is designed to maintain repeatable infrastructure behavior under sustained, synchronous load across multi-thousand GPU clusters supporting distributed model training at scale. In production deployments running long-duration training workloads, SUNK delivers:
- Up to 96% goodput means the vast majority of requested GPU time translates into useful training work rather than retries, stalls, or idle cycles
- 10x longer Mean Time to Failure (MTTF) for thousand-GPU clusters (approximately 3.66 days compared to roughly 8 hours in benchmark scenarios), reducing disruption frequency for multi-day jobs
- ~90 seconds to job restart when failures do occur, minimizing interruption time and preserving forward progress across distributed workloads

### Predictable performance. Production-grade results.
The outcome is faster job completion, more productive training time, and faster cycles of discovery that accelerate iteration and innovation. Large, multi-day training jobs maintain consistent behavior, tolerate routine hardware events, and recover quickly when failures occur, preserving productive training time across distributed workloads. These outcomes aren’t the result of isolated tuning or one-off optimizations; they reflect a unified training system designed around topology-aware scheduling, automated health management through CoreWeave Mission Control, and disciplined lifecycle control across compute, networking, and storage.
This operational maturity has been validated externally. CoreWeave was recently named one of the first NVIDIA GB200 Exemplar Cloud, exceeding NVIDIA’s own training performance targets under real-world conditions. That designation reflects not just peak performance, but predictable, repeatable behavior—representing the new industry standard for production-grade AI training at scale.

### Built on continuous health management and deep observability
Reliability at a thousand-GPU scale requires more than just intelligent scheduling. It requires continuous health management, repeatable infrastructure behavior, and automated remediation embedded directly into the training environment.
SUNK is designed to operate with CoreWeave Mission Control, which continuously evaluates node health, tracks GPU performance variance, and detects stragglers before they impact synchronized training workloads. Rather than reacting after failure, health telemetry proactively informs scheduling decisions in real time.
When users identify degradation with CoreWeave Mission Control, they can proactively drain unhealthy nodes, reschedule workloads, and isolate failure domains. This prevents single-node instability from cascading into cluster-wide disruption. By coordinating between scheduling, health signals, and automated recovery, SUNK reduces operational gaps common in stitched-together environments and maintains consistent behavior under sustained load.

### Visibility that keeps training moving at full speed
SUNK’s deep observability connects infrastructure telemetry directly to job-level performance. Platform teams gain visibility into communication bottlenecks, GPU variance, memory pressure, and distributed training state throughout the lifecycle of a run. Instead of reacting to stalled jobs, teams can anticipate performance degradation and intervene predictably.
The outcome is sustained forward progress. Large, multi-day training jobs maintain consistent behavior, tolerate routine hardware events, and recover quickly when failures occur—preserving productive training time across distributed workloads.
This operational discipline reflects years of running production-scale research clusters under real-world conditions with leading AI pioneers. And it is this maturity that enables the next step: giving teams flexible ways to engage with the same production-grade training system.
View of Running and Pending Jobs in Slurm Cluster Dashboard
GPU Straggler Detection view for hung Job in Slurm Job Metrics Dashboard

### Announcing today: guided self-service-accelerating get started
To make it even easier to launch a new SUNK environment, we are announcing today the addition of a new curated getting-started experience.  
Operational rigor is foundational to SUNK’s design and operation, ensuring fast onboarding and predictable operations. This new guided self-service experience provides a streamlined path to a production-ready SUNK cluster, built on proven operational patterns. CoreWeave manages deployment workflows, upgrades, and lifecycle controls, allowing teams to focus on training workloads rather than infrastructure coordination. It does this without impacting the reliability, observability, or performance characteristics of the underlying system.
This includes:
- Accelerated onboarding: Stand up a production-ready SUNK cluster in minutes using guided setup informed by safe, operationally validated defaults.
- Predictable upgrades: Defined release channels, coordinated upgrade windows, and versioning discipline reduce operational risk as clusters evolve.
- Reduced operational burden: CoreWeave manages lifecycle events and common failure scenarios, preserving cluster consistency over time.
- Researcher-aligned workflows: Researcher pods, shared environments, and self-service access gain the advantage of built-in support without compromising operational control
- Enterprise alignment: Programmatic user provisioning, permissions, and isolation are aligned with security and compliance requirements.
Together, these capabilities reflect CoreWeave’s continued investment in making SUNK faster to adopt and simpler to operate—while preserving the production-grade reliability and operational visibility that pioneers depend on at scale.

## From cluster complexity to predictable model progress 
As AI workloads continue to evolve, research clusters must also scale in both size and operational discipline. Training jobs now span thousands of GPUs and run for days at a time, meaning that small inefficiencies can compound into stalled progress and wasted compute.
At this scale, what matters most is faster job completion, more productive training time, and faster cycles of discovery. Researchers and AI platform teams need access to infrastructure that sustains reliable performance under sustained, synchronized load, not just peak throughput in controlled conditions.
SUNK is built for that evolving reality. By delivering a unified training system designed for large, long-running AI workloads, SUNK enables teams to move beyond reactive operations and fragmented infrastructure toward disciplined, scalable execution.
The result is sustained model progress, higher utilization, reduced operational burden, and more consistent outcomes at production scale.
Explore how SUNK runs large-scale AI training reliably at production scale. Contact our team to discuss your training environment, or dive deeper into the resources below:
- Read the SUNK Solution Brief: Get a comprehensive overview of how SUNK unifies the full AI training lifecycle, maximizes productive training time, and delivers production-grade reliability at scale.
- Explore the SUNK Documentation: See technical details on architecture, scheduling, observability, and operational workflows for teams evaluating or deploying SUNK.
- Learn about SUNK user provisioning: Automate SUNK user access and sync identities from your IdP or IAM securely in minutes.
‍

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
