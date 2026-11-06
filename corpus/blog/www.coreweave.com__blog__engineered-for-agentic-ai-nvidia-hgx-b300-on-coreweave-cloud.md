# Introducing NVIDIA HGX B300 on the Essential Cloud for AI

Source: https://www.coreweave.com/blog/engineered-for-agentic-ai-nvidia-hgx-b300-on-coreweave-cloud

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

As demand for agentic AI accelerates the shift toward inference workloads, cloud infrastructure requirements are evolving significantly. Long context windows require expanded memory. Multi-reasoning drives sustained GPU utilization. Agent coordination depends on low-latency, high-bandwidth interconnects across large-scale clusters. Running agentic AI at scale requires powerful accelerators combined with an AI-native cloud that delivers consistent performance, operational visibility, and scalability.
Today, we are proud to announce that NVIDIA HGX B300 is now generally available on CoreWeave Cloud, with AI pioneers like Cursor already moving toward production workloads.
NVIDIA HGX B300 doubles interconnect speed with NVIDIA Quantum-X800 InfiniBand networking, NVIDIA BlueField-3 data processing units (DPUs), and 800 Gbps NVIDIA ConnectX-8 SuperNICs, enhancing NVFP4 inference performance, and increasing GPU memory capacity by 50% over the NVIDIA HGX B200. CoreWeave unlocks NVIDIA HGX B300 at scale, with our benchmarks demonstrating 3.42x faster token generation on Kimi K2.5 and 4.93x faster end-to-end request latency on DeepSeek-R1 (vs. NVIDIA HGX H200). 
This milestone marks another step forward in advancing agentic AI—powered by an AI cloud that unlocks the performance of the latest-generation GPUs and backed by our relentless commitment to trusted partnership, unmatched speed, and validated performance for every AI pioneer.

## Why AI pioneers like Cursor and Decart AI partner with CoreWeave for NVIDIA HGX B300
For organizations building agentic AI, where long-context inference, multi-step reasoning, and distributed coordination amplify infrastructure risk, a trusted partner is non-negotiable. CoreWeave provides direct-to-expert support that evolves alongside rapidly changing model architectures, across multiple generations of accelerators. Customers like Mistral have praised this hands-on support, noting that it allows their team to run jobs overnight with confidence and frees them to focus on building models.

Our support is why AI leaders such as Cursor and Decart AI choose CoreWeave Cloud for the latest NVIDIA GPUs:
"We’ve already run production workloads with CoreWeave on NVIDIA HGX B200, and that experience built real confidence in their ability to operate at scale. What mattered to us was predictable performance, operational reliability, and having a partner who could support us as our requirements evolved. As we move toward B300, that proven operating model and continuity in execution give us confidence to focus on building more capable AI code generation systems, rather than worrying about infrastructure risk." 
— Aman Sanger, Co-founder, Cursor
"At Decart, we transform video from a static medium into a living, responsive world experience. Our partnership with CoreWeave has enabled us to run NVIDIA HGX B200 at production scale and push the boundaries of training and inference, while delivering seamless interactive video experiences via the CoreWeave stack. With the NVIDIA HGX B300 and the upcoming NVIDIA Vera Rubin platform, we are effectively enabling a new level of massively scalable real-time generative and agentic AI." 
— Orian Leitersdorf, Chief Scientist, Decart
CoreWeave’s direct-to-expert support reduces uncertainty, accelerates deployment, and ensures performance scales as workloads grow more complex.

## Accelerated pace that drives breakthroughs
Agentic AI development is iterative: models must be evaluated, fine-tuned, and orchestrated across agents in continuous development loops. An infrastructure platform must reduce this friction across the entire cycle. 
Early, production-grade signals—along with the tools and operational visibility to act on them—are critical for reducing inefficiencies in agentic AI development. This is exactly what CoreWeave Mission Control™ provides, while shifting the responsibility for maintaining NVIDIA HGX B300 cluster health from your team to ours. NVIDIA HGX B300 instances are natively integrated with our advanced fleet lifecycle controllers. This ensures rapid, AI-native provisioning and orchestration, ensuring high availability that allows you to begin training or fine-tuning with NVIDIA HGX B300 within hours, not weeks. This reduces time lost to infrastructure setup and manual coordination. We also provide a real-time, deep view of NVIDIA HGX B300 instance performance, delivering actionable insights into NVIDIA NVLink performance, GPU utilization, and other key metrics.
To accelerate the development pace even further, CoreWeave provides a Kubernetes-native orchestration layer purpose-built for large-scale distributed AI systems, CoreWeave Kubernetes Service (CKS). CKS enables you to deploy, scale, and manage agent workflows with production-grade reliability and tight GPU integration. Slurm on Kubernetes (SUNK) extends this by allowing you to run more experiments in parallel while maximizing GPU efficiency.
For evaluation and debugging, W&B Weave provides the tooling needed to iterate on agentic AI systems. With end-to-end tracing of agent runs, developers can visualize and inspect the full agentic system to diagnose and remediate those failures that occur in intermediate reasoning steps. 
Agentic AI also needs fast, scalable, and predictable data access to execute multi-stage reasoning and frequent checkpoints. CoreWeave AI Object Storage offers just that, with speeds of up to 7 GB/s per GPU, keeping NVIDIA Blackwell Ultra GPUs fed so they aren’t idle waiting on networking or storage I/O. For agentic AI, pace is not just about faster provisioning, but about shortening the time between idea, experiment, validation, and production. CoreWeave’s AI-native platform ensures NVIDIA HGX B300 delivers not only raw capability but also the operational velocity required to capitalize on it with 96% goodput. This means nearly all requested compute translates directly into useful work, ultimately helping you outpace competitors and bring innovations to market faster.

## Engineered for performance
NVIDIA HGX B300 builds on the HGX B200 foundation with increased memory capacity, performance, and token economics. With 270 GB of memory (up from 180 GB on the HGX B200), the HGX B300 enables larger models and longer context windows to run directly in high-bandwidth memory. This reduces reliance on external memory tiers and minimizes latency for memory-intensive workloads.

For large-scale model training, higher-precision formats such as FP32, FP16, BF16, and FP8 remain essential to maintain accuracy and numerical stability. NVIDIA HGX B300 preserves the same high-precision performance profile as NVIDIA HGX B200, ensuring no trade-offs for teams training foundation models or fine-tuning domain-specific systems.

Agentic AI workloads, however, place different pressures on infrastructure. Long context inference, multi-step reasoning, and coordinated agent execution demand efficient memory utilization and high-throughput execution at scale. In these scenarios, lower-precision formats such as NVFP4 can dramatically improve efficiency without sacrificing output quality.

NVIDIA HGX B300 significantly increases NVFP4 performance from 9 PFLOPs to 14 PFLOPs, enabling higher-throughput inference and more efficient memory utilization for agentic systems operating in production. At the system level, both HGX B300 and HGX B200 provide 1.8 TB/s per-GPU interconnect bandwidth, 14.4 TB/s aggregate NVSwitch bandwidth, and 7.7 TB/s of memory bandwidth, ensuring the high-speed GPU-to-GPU communication required for distributed training and large-scale agentic AI execution.
Below is a detailed comparison of HGX B300 and its predecessor: 

 | Specification
 | NVIDIA HGX B300
 | NVIDIA HGX B200

 | FP4 Tensor Core
 | 144 PFLOPS | 108 PFLOPS
 | 144 PFLOPS | 72 PFLOPS

 | FP32
 | 600 TFLOPS
 | 600 TFLOPS

 | FP64 / FP64 Tensor Core
 | 10 TFLOPS
 | 296 TFLOPS

 | Total GPU Memory
 | 2.1 TB
 | 1.4 TB

 | Networking Bandwidth
 | 1.6 Tb/s
 | 0.8 Tb/s

 | Attention Performance
 | 2x
 | 1x

CoreWeave unlocks the performance of NVIDIA HGX B300 at scale first by eliminating the friction of network congestion, one of the most common constraints in large-scale clusters. For agentic AI workloads that span multiple nodes, GPU-to-GPU communication is often the limiting factor to efficient scaling. When large AI models run across many machines, they constantly send data back and forth between servers. If the network can’t handle that volume of inter-node traffic, it becomes congested, causing slowdowns and limiting overall system scalability. Our infrastructure is powered by non-blocking NVIDIA Quantum X-800 InfiniBand and RoCE (RDMA over Converged Ethernet) fabrics, designed with a fat-tree architecture, which provides 2x the node-to-node bandwidth across multi-thousand GPU clusters. This allows for full bidirectional bandwidth with no oversubscribed links, meaning every GPU can communicate at its maximum throughput without competing for shared bandwidth. 
Second, CoreWeave harnesses the potential of NVIDIA HGX B300 with our state-of-the-art liquid cooling, purpose-built for high-density systems. Long context inference, multi-step reasoning chains, and coordinated agent execution often keep GPUs running at high utilization for extended periods. In air-cooled environments, thermal buildup can lead to performance throttling, inconsistent throughput, and reduced scaling efficiency. CoreWeave’s liquid cooling infrastructure ensures:
- Sustained performance: Liquid cooling keeps GPUs at optimal, consistent temperatures, ensuring sustained peak performance, maximizing your compute investment.
- Operational stability: Minimizing thermal wear and stress improves hardware longevity and cluster reliability, minimizing performance degradation over time.
- ‍Efficiency at scale: Efficient heat removal supports dense cluster deployments while maintaining predictable GPU-to-GPU communication.
Operational telemetry from CoreWeave’s observability stack provides real-time insight into GPU utilization, thermals, and cluster health.

## Performance in practice
Raw specifications and architectural advances are only meaningful if they translate to measurable gains in real-world workloads. To evaluate real-world NVIDIA HGX B300 inference performance on CoreWeave, we conducted two benchmark experiments. 
First, we benchmarked our NVIDIA HGX B300-based instances using the DeepSeek-R1 model, one of the largest open-source, Mixture of Experts (MoE) models on the market. We used native NVFP4 quantization on NVIDIA HGX B300 compared to FP8 block scaling on NVIDIA HGX H200, representing a "best-vs-best" configuration for each architecture. CoreWeave also measured distributed communication performance, testing NVIDIA HGX B300 instances (with NVIDIA Quantum-X800 XDR InfiniBand) against NVIDIA HGX H200 instances (with NVIDIA Quantum-2 NDR InfiniBand) to see how they handle heavy collective operations, such as NCCL all-to-all.Second, we benchmarked our NVIDIA HGX B300-based instances on Kimi K2.5, an open-source, native multimodal agentic model, against NVIDIA HGX H200 and NVIDIA HGX B200. We drove the system at maximum load while increasing the number of concurrent users to observe how performance changed as demand grew. The tests measured total token throughput and latency metrics, including P99 time to first token (TTFT) and time per output token (TPOT), to understand how quickly responses start and how fast tokens are generated in the slowest cases users might see. These metrics were recorded across multiple concurrency levels to evaluate peak performance, scaling under load, and the consistency of response speeds during inference.
All together, the results of our benchmark testing demonstrate how NVIDIA HGX B300-based instances on CoreWeave meet the changing needs of agentic AI:
- CoreWeave’s NVIDIA HGX B300-based instances deliver 3.42x faster token generation on Kimi K2.5 and 2.61x faster on the DeepSeek-R1 (vs. NVIDIA HGX H200). With faster token generation, an agentic AI system can handle more reasoning steps, tool calls, and agent workflows at a time without slowing down the system. This allows larger and more scalable agentic systems to run more efficiently.
When running Kimi K2.5, NVIDIA HGX B300 delivers 3.42× higher token generation performance than HGX H200.
When running DeepSeek-R1, CoreWeave’s NVIDIA HGX B300 instances deliver 2.61× faster token generation than NVIDIA HGX H200.
- A 1.95x improvement in measured collective bandwidth on DeepSeek-R1 (vs. NVIDIA HGX H200) allows GPUs to share data with each other much faster. This reduces time GPUs spend waiting on synchronization during distributed inference, helping large reasoning models run more efficiently across thousands of GPUs and deliver more consistent performance for agentic workloads.
When running DeepSeek-R1, CoreWeave’s NVIDIA HGX B300 instances deliver 1.95× higher measured collective bandwidth than NVIDIA HGX H200.
- CoreWeave’s NVIDIA HGX B300-based instances also achieved a 4.93x faster end-to-end request latency on DeepSeek-R1 (vs. NVIDIA HGX H200), meaning each reasoning step completes faster, allowing an agent to iterate through cycles more quickly. This reduces delays that would otherwise compound across chains, enabling faster responses and greater scaling. 
When running DeepSeek-R1, CoreWeave’s NVIDIA HGX B300 instances deliver 4.93× faster end-to-end request latency than NVIDIA HGX H200.
- A 1.41x increase in concurrency on Kimi K2.5 (vs NVIDIA HGX B200) allows the system to handle more requests at the same time, measured by peak burst output (tokens/second). This reduces waiting under heavy load and lets more agents run simultaneously on the same deployment. When traffic spikes, agentic systems are better at handling them without queues or slowdowns.
When running Kimi K2.5, CoreWeave’s NVIDIA HGX B300 instances support 1.41× higher concurrency than NVIDIA HGX B200.

## Be ready for agentic AI with NVIDIA HGX B300
CoreWeave unlocks NVIDIA HGX B300 performance so teams building agentic AI can confidently deploy, operate, and scale.If you’re ready to get started, validate your real-world performance on NVIDIA HGX B300 with CoreWeave ARENA. Or if you want to learn more, register for our product briefing webinar and visit our NVIDIA HGX B300 product page.

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

GPU Compute,

Copy code

Copied!

GPU Compute,
