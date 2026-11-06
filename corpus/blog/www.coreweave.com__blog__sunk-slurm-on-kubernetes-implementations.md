# A Slurm on Kubernetes Implementation for HPC and Large Scale AI | CoreWeave

Source: https://www.coreweave.com/blog/sunk-slurm-on-kubernetes-implementations

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

This article was originally published on VMblog as part of KubeCon 2023.

## SUNK, an implementation of Slurm on Kubernetes. 
Learn how it works.
‍
In the HPC and AI world, there are two kings: Slurm for scheduling and orchestrating massively parallel jobs and Kubernetes for running production applications like Inference. 
However, many companies face making a choice between them or needing to manage two separate clusters. 
Developed by SchedMD, The Slurm Workload Manager (commonly called Slurm) is the defacto scheduler for many HPC workloads, used by leading researchers, academics, and AI companies across the world. However, it’s designed for batch jobs that have a finite lifespan.
Kubernetes on the other hand was built for long-running workloads, like inference. Therefore, the Kubernetes scheduler for batch workloads isn’t as popular as Slurm and lacks some functionality. Other Kubernetes-based schedulers, such as Volcano and YuniKorn, aim to provide Slurm-like scheduling capabilities for Kubernetes but face an uphill battle trying to unset the vast knowledge base around Slurm.
Some companies try to bridge this gap by running both Slurm and Kubernetes, but it’s a major challenge for companies today to leverage both. Each cluster runs with its own pool of compute to manage and operate, sometimes in different clouds with separate storage, too. 
While this helps companies be able to separate workloads by Slurm or Kubernetes, resource management is completely separate. So, any communication or collaboration between the two requires manual work, which can take significant time and effort. 
Two popular platforms. Two separate pools for compute.
Two separate solutions to manage and own.
To truly combine the strengths of both solutions, CoreWeave has been working on an implementation of Slurm on Kubernetes that effectively syncs the two. 
‍

## Introducing SUNK ("SlUrm oN Kubernetes")
SUNK brings Kubernetes containerized deployments and Git Ops to Slurm and integrates a Slurm scheduler plugin to Kubernetes. 
In essence, SUNK integrates Slurm as a Kubernetes scheduler and allows for Slurm jobs to run inside Kubernetes. This creates a more seamless experience, supports both burst and batch workloads on the same central platform, and allows developers to leverage the resource management of SLURM on Kubernetes.
Managing Slurm and Kubernetes separately reduces the overall complexity, but also greatly reduces the flexibility you have to choose what kinds of workloads run across all of your compute. AKA it’s more difficult to maximize utilization of GPU resources. 
By deploying a Slurm cluster on top of Kubernetes (SUNK), on top of the same pool of compute, you have the flexibility to seamlessly use that compute from the Kubernetes or Slurm sides.
Two solutions. One platform. One pool of compute.
“One ring to rule them all” kinda vibe.
‍

### Why did CoreWeave choose to create this?
The simple answer: Client efficiency. When you’re running very large and expensive HPC clusters, getting as close to 100% utilization is very important. Any times when you might not be using the compute you are paying for can be very costly.
CoreWeave is built entirely on top of Kubernetes, where clients each have a single point of entry and management for their cluster. But, we realized that many clients who preferred Slurm would manage it separately or ask us if we had an integration for Slurm. 
Coreweave Cloud is all about efficiency—it’s the reason why we say we’re purpose-built for GPU-intensive use cases. 
We wanted to enable clients to leverage the benefits of Slurm while maintaining the integrity of our system and the ease of use (aka no management of separate clusters). Since that solution didn’t exist, we decided to build it.
‍

### Features of SUNK
Configuration and deployment: By deploying a Slurm cluster as various Kubernetes resources, we are able to deploy it with a highly customizable helm chart. This unlocks the large ecosystem of Kubernetes-based GitOps workflows and all the features that come with it. Other benefits include:
- Easy tracking & configuration of prolog and epilog scripts
- Quickly deploy staging clusters
- Support for s6 scripts and services
- Configurable authentication schemes including Ldap through companion OpenLdap helm chart or third party solution (Authentik, GAuth, etc.)
‍Kubernetes Integration: Once you deploy SUNK, you get all the normal benefits from running on Kubernetes, like:
- Fast scheduling
- Containerization
- High availability of control plane services
- Dynamic node scaling 
- Resource management with request and limits
- Shared filesystem via PersistentVolumeClaim resources 
This also includes a custom Slurm Kubernetes scheduler (for scheduling native Kubernetes workloads via Slurm scheduler), which enables you to dynamically shift a single pool of compute between Slurm jobs (bursty workloads) and Kubernetes workloads (serverless workloads). 
State management: By running on top of Kubernetes, you also get more control over state management, including:
- Dynamic nodes with two-way syncing of state between k8s and Slurm
- Automatic topology generation
- Support for Pyxis container execution
- GRES support and auto-identification
‍

## How SUNK Works
To understand how SUNK effectively integrates Slurm and Kubernetes, let’s talk about the underlying structure.
The graphic below shows a high-level architectural diagram of SUNK. Let’s break it down piece by piece before we talk about a few important parts in more detail.
‍
How SUNK works, plus the Nodeset.
The first thing to call out is that all of these services are containerized in Kubernetes. At the top, you have resources that are deployed cluster-wide, and at the bottom, you have the components deployed for a single Slurm cluster.
Section A: All of the typical Slurm components are deployed within a pod, each with its own configurable resource requests. Not pictured here, but this also includes login nodes that users connect to in order to interact with the Slurm cluster. Once connected to these login nodes, Kubernetes is abstracted away, and you get the experience of a normal Slurm cluster. 
‍Section B: Slurm configuration is needed throughout many of these components. By deploying them as k8s ConfigMaps and Secrets, Slurm configuration files can be managed in a single place and mounted everywhere they’re needed. This includes Slurm configuration, topology, prolog/epilog scripts, and sensitive information like DB passwords.
‍Section C: The most important aspects of an HPC cluster are the compute nodes, which are shown in the middle as bare-metal Kubernetes nodes. The slurmd’s are run within compute pods shown above in a 1:1 mapping. The deployment of compute pods are managed by a CRD called a Nodeset, which has some special features we’ll get into later in this article.
Section D: Many of the features we’ve talked about require the state of compute from the Slurm and Kubernetes sides to be in sync. The Slurm syncer acts as a middleman between the two sides by sending and pulling information through Slurm’s REST API.
‍Section E: Once the syncer gets state information from Slurm into Kubernetes, there are many different places the information needs to be to stay consistent. The cluster-wide operators monitor different resources and make changes when appropriate, whether the change originates from Kubernetes or Slurm. 
Not present in the diagram, but with the ability to sync state, we are able to use a custom Kubernetes scheduler that allows you to schedule workloads onto the compute Kubernetes nodes based on the Slurm states.
Finally, since all of these components are running on Kubernetes we can expose metrics through Prometheus which can be used in a variety of different ways.
‍

### Nodeset, Syncer, and Scheduler
There are three aspects of SUNK that our team had to custom-build in order to make this integration possible: the Nodeset, Syncer, and Scheduler.
Nodeset
‍
The Nodeset
First is Nodeset (shown above and in Section F in the first chart). As mentioned, this is a CRD we developed that defines a Slurm node in the context of the Kubernetes environment. It’s defined similarly to a statefulset or deployment but has a 1 to 1 mapping with nodes more similar to a daemonset.
The Nodeset maintains a series of status fields representing the state in Slurm. This provides mechanisms for protected updates and scaling of Slurm nodes based on the states in both kubernetes and Slurm. 
The Nodeset pods run both slurmd and munged, mounting in shared configmaps for things like the Slurm config, the prolog and epilog, and shared filesystem volumes as PVCs.
The image below shows most of those status fields. As you can see, the Nodeset pod has an active understanding of how many possible nodes match an affinity, how many of those nodes are currently assigned as Slurm nodes, tracks readiness, running and drain conditions, etc. 
‍

‍
Syncer
A lot of the features of the Nodesets rely on the state of Slurm being known throughout the Kubernetes side and vice-versa. The Syncer accomplishes this with two parts: a Slurm client and a pod controller.
The Slurm client communicates with the Slurm REST API to push and pull information. As the size of a Slurm cluster grows to hundreds or even thousands of nodes, this communication will grow to a lot of traffic. The client efficiently caches results to handle large-scale clusters.
The Pod controller receives events from the client and reconciles the pod state based on any discrepancies. In case a change comes from the Kubernetes side, the pod controller will push an event to the client, which passes along that change to Slurm if required.
So, the flow of information goes in two directions. 
Say for example, a node in Slurm goes into drain. The Syncer will detect that state change and place an annotation on a pod. This annotation can be acted upon across the Kubernetes side, like starting an update only when a Slurm node is in drain.
On the other hand, changes can start from the Kubernetes side. Say you detect a hardware issue and cordon a node inside of Kubernetes. The Syncer will put the respective Slurm node in drain along with adding a nice reason explaining why it has been drained.
‍
The Syncer
‍
Scheduler
Now the real magic: The Scheduler is another service running within a namespace that allows for some very interesting functionality.
Let’s say you want to take a pool of reserved instances on CoreWeave and ensure that you are getting maximum utilization for those instances, in addition to instances you use from an on-demand pool. AKA: running inference and training at the same time.
When a pod is scheduled using this Scheduler in k8s, like an inference pod being driven by a serverless solution like Knative, a Slurm job is created, which has the ability to pre-empt low-priority tasks. When Slurm nodes are eventually allocated to the job in Slurm, the Scheduler then places the k8s pod onto the node and runs it there. 
In short, you can seamlessly use compute from a Slurm cluster in Kubernetes without having to actively maintain two separate pools of reserved compute, which aren’t dynamically allocated.
‍
The Scheduler
‍

## Conclusion
Companies can achieve the best of both worlds with SUNK, a forthcoming integration of Slurm as a Kubernetes scheduler. By allowing for Slurm jobs to run inside Kubernetes (with help from a few custom features), SUNK gives you the ability to use Slurm while maintaining the flexibility and performance benefits of Kubernetes. 
No more managing separate pools of compute. 
No more choosing between Slurm or Kubernetes.
Just greater efficiency for your workloads and better utilization of compute resources using the tools you know and love.

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
