# CAIOS Achieves 7+ GB/s per GPU on NVIDIA Blackwell Ultra | CoreWeave

Source: https://www.coreweave.com/blog/caios-achieves-7-gb-s-per-gpu-on-nvidia-blackwell-ultra

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Earlier this year in March, we published the latest benchmarking results of CoreWeave AI Object Storage (CAIOS) on NVIDIA H100 GPU nodes, showing sustained throughput of over 2 GB/s per GPU across any number of GPUs. CAIOS is CoreWeave’s innovative AI-focused storage service, designed to deliver higher throughput per GPU than traditional object storage services and to be scalable to hundreds of thousands of GPUs. CAIOS includes the Local Object Transport Accelerator (LOTA), which transparently prestages and caches objects on GPU nodes for accelerated performance. Since the March benchmark testing, we’ve continued pushing the limits of CAIOS with new hardware configurations, transport layers, and optimizations.
CAIOS is purpose-built to accelerate the most data-intensive stages of AI. It streamlines the flow of massive training sets into GPUs, shortens checkpointing and restore cycles, speeds the loading of model weights, and powers high-throughput key-value caches for inference.

We’re excited today to share the breakthrough results of our latest tests on 16 NVIDIA Blackwell Ultra GPU nodes, where CAIOS achieved an average throughput of 7+ GB/s per GPU, representing a more than 3x improvement per GPU compared to our March benchmarks.

## Benchmark setup
- Test Harness: Warp S3 benchmarking tool, set up to run object read tests in CoreWeave Kubernetes Service (CKS).
- Objects: 10,000 objects at 50 MB each, with 15 MB parts
- Concurrency: 100 for Warp (100 goroutines making calls)
- Pipelining: Enabled (cache reads queued ahead across nodes rather than sequential calls)
- Transport: Both Ethernet (TCP) and RDMA (NVIDIA Quantum InfiniBand) tested
- Cluster Size: 16 x Blackwell Ultra nodes

## Comparing results across Ethernet and NVIDIA Quantum InfiniBand

### Ethernet (TCP)
- Sustained throughput capped at 180 GB/s across 16 nodes (11.25 GB/s/node or 2.81 GB/s/GPU). In this case, the Ethernet network in the lab where we conducted the testing limited our ability to hit the same per-node throughput as our previous test.

### RDMA (NVIDIA Quantum InfiniBand)
- Sustained throughput capped at 449 GB/s across 16 nodes (28.06 GB/s/node or 7.02 GB/s/GPU)
Unlike Ethernet, the NVIDIA Quantum InfiniBand fabric easily handled full-fleet concurrency, demonstrating the scale advantage of RDMA transport.
In the graph below, the sustained throughput of the 16 Blackwell Ultra nodes using InfiniBand is shown, with 10 of the nodes listed in the table on the right. The throughput increases over time as objects are staged on the LOTA cache. The “Max” column shows a range of 25.6-36.9 GB/s for each node. The average was 28.06 GB/s for each node. Since there are 4 GPUs in a GB300 node, this equates to an average of 7+ GB/s per GPU.
Accelerated Byte Rate by Pod

## Throughput gains since March
When comparing these new results to our NVIDIA H100 benchmarks, here’s how CAIOS performance has advanced from 2 GB/s/GPU:
- Fewer GPUs per node: 2 GB/s/GPU ➡ 4 GB/s/GPU 
The H100 nodes have 8 GPUs each, while Blackwell Ultra nodes have 4 GPUs each. With per-node throughput being the same or higher, this doubles the throughput per GPU.

- Moving to NVIDIA Quantum InfiniBand: 4 GB/s/GPU ➡ 6 GB/s/GPU
Because the LOTA cache in CAIOS is global across all nodes, increasing node-to-node throughput also increases overall CAIOS throughput. By moving this node-to-node data transfer to InfiniBand, we consistently saw an approximately 50% improvement in throughput. This was verified by separate H100 InfiniBand testing where we saw similar speed increases compared to our March testing of H100’s using Ethernet..

- LOTA pipeline optimizations: 6 GB/s/GPU ➡ 7+ GB/s/GPU
Since March, we have made a number of optimizations in the way that LOTA reads and writes data, which resulted in an approximately 17% performance improvement in throughput. This increase in throughput was verified by recent LOTA testing we did with H100 nodes to compare to our March H100 test results.
This cumulative progression highlights the scalability and adaptability of CAIOS across hardware generations and network fabrics.

## Key takeaways from the research
With CAIOS, workloads scale seamlessly across fleets of GPUs. On NVIDIA Blackwell Ultra nodes with NVIDIA Quantum InfiniBand and pipelining enabled, we’re now sustaining 7+ GB/s per GPU - performance that goes well beyond the 2 GB/s/GPU milestone we shared earlier this year. This new throughput further reduces training times, decreases inference Time to First Token (TTFT), and improves ETL efficiency.
As we continue to optimize CAIOS, the gap between GPU compute power and data availability will continue to shrink, ensuring that GPUs stay fully utilized even at extreme concurrency and scale seen in training and inference use cases.
Read the original blog that outlines our initial benchmark methodology and results.
Learn more about the CoreWeave AI Cloud and how it can help you simplify infrastructure complexity so your team can focus their energy on AI innovation
If you’re interested in learning more about CAIOS and how it can support your AI innovations, reach out and let’s talk.

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

CoreWeave AI Object Storage,

Copy code

Copied!

CoreWeave AI Object Storage,
