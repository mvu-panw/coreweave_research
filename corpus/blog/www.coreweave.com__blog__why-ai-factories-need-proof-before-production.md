# Co-designed AI factories for production AI | CoreWeave Blog

Source: https://www.coreweave.com/blog/why-ai-factories-need-proof-before-production

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

For a long time, getting the GPUs meant you were ready. Rack them, power them, cool them, and the dashboards go green. That was the whole test.
It isn't anymore. Real AI workloads don’t ask whether the compute exists. They ask whether compute, networking, storage, scheduling, and recovery can hold together for two weeks straight, without stalling somewhere at the seams. AI factories keep every layer of the stack working in sync to turn power into tokens, reduce training run times from days to hours and accelerate token throughput.

## The bar keeps rising
That list of supporting services only grows. Observability, health management, and the operations work in concert while jobs run in the background. And increasingly, some of the new jobs never really end. Due to the nature of agentic workloads, the end user doesn’t want to wait to see results. As agentic AI demand increases, so does token throughput. AI clouds cannot sacrifice reliability over speed. An agent calling tools or running a multi-step reasoning loop can spike demand at any hour, therefore teams must prepare their infrastructure to support variable demand.

## Delivering production AI
Here's what that looks like in practice. A stalled job can constrain GPU resources and delay project timelines. A lost checkpoint means redoing work that already happened once, on the same valuable hardware. And underutilized resources are still running up the bill whether they're producing tokens or not. In this fast pace environment, teams cannot afford to lose productivity or underutilize compute resources. NVIDIA and CoreWeave partner to co-design a full-stack platform for leading model builders, enterprises, and AI natives to deliver production-ready AI faster. 

## The work behind the partnership
Teams that depend on these systems need the whole stack to behave as one before a workload goes live. Our teams work together from concept and design to stand up and validation of the latest systems to optimize performance and efficiency of the entire stack. NVIDIA is the accelerated computing platform and CoreWeave provides the AI-native cloud software and operations layer. Together, we are making sure the full-stack behaves the same in  production as it did in validation.
That work started in January 2026, when NVIDIA and CoreWeave expanded their collaboration to deploy Vera Rubin platform on CoreWeave using the NVIDIA DSX platform. DSX is NVIDIA's reference design for how AI factories are planned, built, and operated at maximum efficiency and profitability. The goal is deeper interoperability assuring more resilient and performance AI Factory capability. As a result of this collaboration, CoreWeave recently shared early performance benchmarks: Vera Rubin NVL72 generated 10x tokens-per-second per megawatt compared to NVIDIA GB200 NVL72 on the same DeepSeek R1 workload. This milestone demonstrates how closely our teams work together to bring-up next generation AI compute.

## Track record, not talking points‍
Two results made that case in public. Last year, CoreWeave was the first AI cloud provider to deploy NVIDIA GB300 NVL72. And in MLPerf Training v6.0, CoreWeave completed the DeepSeek-V3 671B training benchmark in approximately two minutes on the largest NVIDIA GB300 NVL72 cluster in the round. That track record isn't accidental. It's what happens when every layer of the stack is designed to work together before a customer depends on it and proven under real workloads before it ships. That's the shape of the full collaboration. Co-designed, validated before deployment, operated with confidence at scale, and carried into the next generation of hardware.
Here's how we co-design and validate that stack, before turning to how it operates at scale and carries into the next generation in part two.
‍

## 1. Co-designed for production AI
PFLOPs may appear to be the obvious indication of performance, however it doesn’t tell the full picture. Extreme co-design across GPUs, CPUs, networking, and storage is required to achieve the highest performance possible. Every layer is designed in step with every other layer, before any of it reaches a customer.

### Planned before ground breaks
The NVIDIA DSX Platform brings together land, power, and cloud partners, CoreWeave among them, to plan AI factories before they're built. That's extreme co-design: the whole ecosystem agreeing on how every layer fits together before a customer ever depends on it. Before we break ground on a new data center, networking, cooling, storage, and software are planned together to ensure end-to-end efficiency and performance.
NVIDIA backs that up with hardware and software references designs built specifically to solve infrastructure problems at scale. Integration failures that only surface at large scale get caught by our engineers before onboarding, not in a customer's production run.

### Proven in Exemplar Cloud‍
NVIDIA Exemplar Cloud is where performance at scale gets tested. It's a validation initiative that measures performance per TCO against real workloads, not synthetic ones CoreWeave was among the first to achieve Exemplar Cloud status for training on NVIDIA GB200 NVL72. The validation ran on a standard NVIDIA GB200 NVL72 cluster of 576 Blackwell GPUs, interconnected with NVIDIA Quantum-2 InfiniBand and performance-optimized by CoreWeave Mission Control, and it met NVIDIA's performance reference targets for large-scale training. Meaning the result comes from a trusted configuration customers will actually use rather than a one-off build. On the inference side, CoreWeave achieved Exemplar Cloud validation for inference on Blackwell GPUs, across DeepSeek-R1, Llama 3.3, and GPT-OSS, using NVIDIA TRT-LLM and SGLang backends with NVIDIA Dynamo for multi-node serving. Same discipline, applied to the workload that runs every day, not just the one that runs once to set a benchmark.

### Carried into Next Generations‍
That discipline doesn't reset with each new generation. CoreWeave brought NVIDIA GB300 NVL72 systems, integrated with CoreWeave Kubernetes Service (CKS), SUNK, observability, and the Rack LifeCycle Controller, in a matter of weeks. CoreWeave’s agility and alignment to NVIDIA reference designs results in industry-leading bring up of new generations including Vera Rubin.

### Extended to network and storage‍
Co-design goes beyond the compute layer, it extends to the network fabric and the storage layer. CoreWeave uses both NVIDIA Spectrum-X Ethernet and NVIDIA Quantum InfiniBand for low-latency communication, and CoreWeave AI Object Storage with LOTA for high-throughput data delivery, so interconnect and storage keep the GPUs fed instead of becoming the bottleneck once a job spans many racks. Spectrum-X Ethernet pairs the new Spectrum-6 102.4T switch with ConnectX-9 SuperNICs, using adaptive routing and telemetry-based congestion control to hold bandwidth where off-the-shelf Ethernet degrades under load. In fact, CoreWeave was among the  first cloud providers to deploy NVIDIA Spectrum-X Ethernet SN6600-LD, the industry's first fully liquid cooled 102.4 Tb/s Ethernet switch. CoreWeave is also an early adopter of NVIDIA Photonics co-packaged optics networking, built to improve power efficiency, resiliency, and AI workload uptimes of multi-million GPU AI factories.

## 2. Validated before customer deployment
Designing the stack right isn't the same as proving it holds up under real load. Customers need to understand how their workloads will behave before they commit them to production. That means testing real models, real configurations, and real infrastructure behavior under conditions close to deployment, so that scaling characteristics and cost drivers are known in advance rather than discovered in production.
CoreWeave ARENA is built for exactly this. It's a production-scale validation lab. Teams run training jobs, inference workloads, and agent pipelines on production-grade infrastructure to surface bottlenecks and validate scaling and cost behavior before deployment, with reproducible results. The lab runs the same stack a customer would, including GPU compute, CKS, Slurm and SUNK, AI Object Storage with LOTA, networking, and Mission Control, so the behavior it surfaces is the behavior production will see.
While MLPerf and Exemplar Cloud validate the performance of CoreWeave, customers can also test a compute environment with ARENA.  In MLPerf Training v6.0, which measures the time to train a model to a defined quality target, CoreWeave completed the DeepSeek-V3 671B benchmark in 2.02 minutes on 8,192 Blackwell Ultra GPUs, the largest GB300 NVL72 cluster in the round, with completion time falling near-linearly as the cluster doubled.
This latest MLPerf result builds on the prior round. In MLPerf Training v5.0, CoreWeave, NVIDIA, and IBM submitted the largest NVIDIA GB200 NVL72 cluster benchmarked at the time, completing Llama 3.1 405B in 27.3 minutes, more than 2x faster than Hopper-based systems at the same cluster size.   Two consecutive rounds of record results, on GB200 NVL72 and then GB300 NVL72. What holds across both is the scaling. Completion time keeps falling predictably as the cluster grows, instead of tapering off the way it does when networking or orchestration becomes the bottleneck.

## What comes next, operating and evolving the factory
Co-design and pre-deployment validation get the stack to behave as one on day one. Keeping it that way is a different discipline. Coming up, part two of our series turns to operations, the health signals, scheduling control, and recovery paths that keep useful work flowing across runs that last days or weeks. It then follows the same readiness discipline into the next generation of NVIDIA accelerated computing, so customers inherit a validated system rather than debugging a new architecture in production.
Want to go deeper? Here’s where to look next:
- Want to see this thinking in person? Register for Fully Connected 2026, September 29 through October 1 in San Francisco, where the engineers and operators running AI in production share what's actually working. Early bird pricing ends July 29.
- Read part 2 of this blog series to learn how CoreWeave operates the AI factory stack at scale, from goodput to reliability, carrying that discipline into the industry-first NVIDIA Vera Rubin NVL72 bring-up.
- Before you commit a workload to production, you can test it the same way CoreWeave does. Explore CoreWeave ARENA to validate your own models and pipelines on production-grade infrastructure, before deployment instead of after.

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

CoreWeave ARENA,

Copy code

Copied!

CoreWeave ARENA,
