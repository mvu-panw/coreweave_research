# Kueue: Kubernetes-Native AI Workload Scheduling with CoreWeave

Source: https://www.coreweave.com/blog/kueue-a-kubernetes-native-system-for-ai-training-workloads

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### Background
Kueue is an open-source project that provides Kubernetes with additional job queueing capabilities, necessary for efficiently scheduling batch AI/ML workloads. 
At CoreWeave, a number of world-class AI labs use Kueue today on CoreWeave Kubernetes Service (CKS) for training AI workloads as well as batch-type inference workloads. 
This blog will take a deep dive into the core concepts around using Kueue, and the rationale behind why these game-changing innovators choose Kueue to elevate what they can do with Kubernetes workloads.

## The limits of traditional Kubernetes
Traditional Kubernetes workloads were not only assumed to be stateless and ephemeral, but serving traffic which would be variable during different times. This resulted in a strong focus on auto-scaling the size of a cluster, i.e. adding new nodes on higher demand and removing nodes during periods of low usage. Given the elasticity of cloud CPU nodes, this model worked quite well for traditional workloads.
However, training AI workloads differs in a couple key respects: 
- GPU nodes tend to be inelastic, even in the public cloud, since you can only truly rely on GPU capacity which has been reserved. In a private datacenter, you are generally working with a fixed number of instances.
- GPU training workloads (and batch inference workloads) require a minimum amount of compute at initialization unlike traditional deployments which start pods one at a time.
- GPU training workloads often require “all-at-once” semantics, which means all capacity must be available in order to start the workload, since pods need to run simultaneously for the job to progress.
These differences have some significant implications, for which Kueue provides answers that the standard Kubernetes scheduler does not. Kueue provides the ability to express:

#### 1. “All or Nothing” scheduling semantics
The standard Kubernetes scheduler will launch pods as soon as the deployment or service is created. While this works well in systems where there is extra capacity, or when it’s ok for a service to have some of its pods running, it works poorly in batch cases, where you require a minimum amount of capacity before the start of a job, and particularly poorly if you also want the job to start on all nodes at once.
Kueue allows users to submit jobs which remain queued until sufficient compute is available for the job. Using gang-scheduling, Kueue also provides a mechanism to start the job on all nodes simultaneously. 

#### 2. Fine-grained resource management
Unlike traditional Kubernetes workloads, where resources are generally modeled only as CPU and memory, AI/ML workloads can run on a staggering variety of hardware types. Some configurations include CPU nodes and GPU nodes, others further stratify GPU nodes by running different models and configurations (e.g. enabling InfiniBand). 
While it’s possible to leverage Kubernetes labels, taints, and tolerations to target workloads to the various machine types, it is difficult, tedious and often error-prone to do so. Kueue provides an explicit and expressive formalization of the computation resource by means of a ResourceFlavor. This allows administrators to model the properties of the instances that are relevant to their specific workloads, only allowing admission to nodes which match the needs of the corresponding workload. 

#### 3. Built-in multi-tenant resource sharing
A common complaint about Kubernetes is its lack of expressiveness for multi-tenancy. This is often attributed to the fact that CRDs and Nodes are cluster-scoped. 
Large organizations typically have multiple teams that require resources on the cluster, and Kueue provides helpful constructs to help fairly share them. But how do you ensure that the ML research team doesn't monopolize all GPU resources when the production inference team has SLA commitments to meet? And what happens when the research team's experiments finish early, do those expensive GPUs just sit idle?
Kueue solves this through ClusterQueues and LocalQueues, which allow administrators to create dedicated quotas for specific teams. These quotas can be defined by specific resource types. For example, you might guarantee that the research team always has access to GPUs with InfiniBand, while ensuring the inference team gets priority access to non-IB instances. 
To ensure efficient resource utilization of the cluster, Kueue allows for quota sharing, quota borrowing, and workload preemption. When one team's workloads are idle, other teams can temporarily consume unused resources, stabilizing overall cluster utilization despite fluctuation from team to team. 
Quota borrowing happens automatically and transparently, with resources returning to their original owners when needed. High priority jobs can preempt lower priority workloads, and the preemption evicts all pods in a job to maintain the "all or nothing" scheduling semantics that are crucial for AI workloads. This ensures that critical training runs get the resources needed without leaving jobs in a partially scheduled state.

### CKS and Kueue Integration 
CKS supports Kueue out of the box. To make it as easy as possible to get started, Coreweave provides a Helm Chart for installing Kueue. Kueue emits prometheus metrics for monitoring and troubleshooting the system, and CKS automatically ingests and renders these metrics on a custom, Kueue-specific dashboard in Coreweave Hosted Grafana. 
To learn more, see the CKS documentation. 

#### What’s next?
At Coreweave, we’re excited by the world-changing innovations that our customers develop on our platform. Our goal is to ensure that tooling in the AI ecosystem runs seamlessly on Coreweave Kubernetes Service, and Kueue is no exception. Keep an eye on this space for more content about Kueue and CKS, and if you’re at an organization that wants to use Kubernetes native tooling to run your AI workloads at high scale on CKS, we’d love to hear from you. 
Curious about the CoreWeave AI Cloud and how we can help you accelerate time-to-market for your latest AI innovations? Explore the possibilities of what we can do together.
Want to learn more about how our managed Kubernetes environment is purpose-built for building, training, and deploying AI applications? Read about our industry-leading performance, scale, and resilience.
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

CoreWeave Kubernetes Service (CKS),

Copy code

Copied!

CoreWeave Kubernetes Service (CKS),
