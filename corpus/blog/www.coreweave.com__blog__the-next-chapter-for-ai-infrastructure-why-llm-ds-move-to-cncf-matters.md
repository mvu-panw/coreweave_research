# Why llm-d in CNCF Matters for Production Inference | CoreWeave Blog

Source: https://www.coreweave.com/blog/the-next-chapter-for-ai-infrastructure-why-llm-ds-move-to-cncf-matters

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

The open source project llm-d, designed to orchestrate and scale distributed inference across accelerator infrastructure, is entering the Cloud Native Computing Foundation (CNCF) Sandbox. This marks an important step toward making production inference a standard, cloud-native capability.

Last May, CoreWeave joined Red Hat, IBM, Google, and NVIDIA as a founding contributor to llm-d because we believed production inference needed to be built in the open. That belief matters even more now. 

As llm-d moves into the CNCF Sandbox process, it marks a broader shift beyond project governance. More pioneers and established enterprises in the industry are treating production inference with the rigor, openness, and interoperability that modern AI  workloads demand. Distributed inference is now foundational cloud-native infrastructure, and building it well will require an open, multi-vendor coalition.

## Inference becomes the backbone of rapidly scaling AI
Inference at scale is fundamentally different from traditional cloud workloads. It is stateful, hardware-sensitive, and costly if operated inefficiently. The rise of AI agents is reshaping how enterprises think about inference. What was once a serving layer for discrete applications is becoming a real-time, always-on production requirement. Agent-driven workflows—from customer support to software development to internal operations—all depend on fast, reliable inference. 
Consequently, as those workloads multiply across the enterprise, so do the demands on the infrastructure that supports them. Two challenges follow. 
First, economics: production inference only works at scale when cost and performance are aligned to application value. Second, portability: enterprises want the flexibility to run models across public cloud, private data centers, and at the edge without being constrained to a single environment or tooling stack.
llm-d is designed to address both. It brings more intelligence to how inference workloads are placed and scaled, while giving teams the flexibility to deploy across different environments. As it moves through the CNCF Sandbox process, that work shifts to neutral ground where the broader ecosystem can adopt it, extend it, and contribute to its direction.

## AI serving needs its own orchestration layer
Kubernetes transformed how the industry deploys and manages software, but inference workloads at scale place new demands on infrastructure that conventional container orchestration was not designed to manage. 
In LLM inference, the cost and behavior of a request can vary significantly based on prompt length, cache locality, and whether the model lives in the compute-bound prefill phase or the memory-bound decode phase. Standard service routing is blind to those dynamics, which can lead to inefficient placement and unpredictable latency.
llm-d introduces a purpose-built orchestration layer between high-level serving frameworks and low-level inference engines, bringing more intelligence to how inference workloads are routed, placed, and scaled. It works with Kubernetes-native components such as KServe, Gateway API, LeaderWorkerSet, and Prometheus, helping transform complex distributed inference into a more manageable, observable cloud-native workload.

## Built in the open, informed by real-world inference
What makes llm-d compelling is not just the technology. It is the breadth of the coalition behind it. 
From its launch, the project brought together contributors, industry leaders, and academic supporters from across the AI infrastructure ecosystem around a shared conviction: production inference will advance fastest through open, interoperable infrastructure.
CoreWeave’s contribution to llm-d is grounded in operating production inference under real-world demand. We see that journey firsthand across a wide range of inference requirements, from early development to production deployment to large-scale distributed inference on Kubernetes. That experience informs a clear point of view: teams should be able to move toward more control, performance tuning, and operational ownership as requirements grow, without losing architectural continuity or visibility into cost and runtime behavior.
The CNCF is a natural home for that kind of effort. It offers transparent governance, a proven framework for growing open source communities, and neutral ground for infrastructure that the industry can develop together. Moving llm-d into the CNCF creates a broader path to share those contributions and to collaborate with more organizations working through the same production challenges.

## Looking ahead
Some layers of AI infrastructure are too important to remain fragmented or vendor-defined. Inference is one of them. The llm-d community has an opportunity to make production inference more accessible, portable, and efficient across the full range of AI infrastructure environments. We are proud to contribute to the project alongside a growing community of contributors and supporters.
Explore llm-d and be part of what comes next:
- Learn how to deploy llm-d with Red Hat AI inference on CoreWeave: https://docs.coreweave.com/products/cks/tutorials/redhat-inference
- Read more about the challenges llm-d seeks to solve and why CoreWeave was a founding member of the project: https://www.coreweave.com/blog/coreweave-joins-red-hat-open-source-ai-project 
- Learn about CoreWeave’s inference solution and the infrastructure essential for real-world inference at scale: https://www.coreweave.com/solutions/ai-inference
- Discover how CoreWeave is bringing elasticity back to the cloud with CoreWeave Flexible Capacity Plans that better support inference workloads: https://www.coreweave.com/blog/bring-flexibility-back-to-the-cloud-for-ai-innovation
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

Inference,

Copy code

Copied!

Inference,
