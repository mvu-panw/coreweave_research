# CoreWeave AI Object Storage Delivers 2+ GB/s per GPU

Source: https://www.coreweave.com/blog/benchmark-results-coreweave-ai-object-storage-delivers-2-gb-s-per-gpu-throughput-across-any-number-of-gpus

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## A new era of storage performance for AI
In March, CoreWeave announced the General Availability of CoreWeave AI Object Storage (CAIOS), an exabyte-scale, S3-compatible managed cloud storage service purpose-built for GPU-intensive AI model training. Seamlessly integrated with CoreWeave’s NVIDIA GPU compute clusters, CAIOS supports 2 GB/s per GPU and effortlessly scales to hundreds of thousands of GPUs. Central to this breakthrough is the Local Object Transport Accelerator (LOTA™), a cutting-edge feature that caches frequently accessed or pre-staged data on local NVMe disks within GPU nodes, which significantly reduces network latency and accelerates training workflows.
Today’s AI models continue to expand in scale and complexity, creating demand for high-performance, scalable storage. CAIOS addresses these demands head-on, ensuring data scientists and machine learning engineers can train larger state-of-the-art models with optimal throughput and low latency.
To validate our claims, we conducted benchmark tests to demonstrate CAIOS’s performance in real-world scenarios. In this article, we’ll detail our methodology, share our results, and provide insights to replicate these tests in your own environment.

## CAIOS architecture
CAIOS distinguishes itself from traditional cloud storage with horizontal scalability in throughput and request handling, ensuring GPU-intensive training and inference tasks remain unimpeded, even at massive scales. The cornerstone of this solution is its seamless integration with local NVMe drives, orchestrated automatically by LOTA. Simply direct your existing S3-compatible workloads to the dedicated cwlota.com endpoint, and experience immediate performance gains without additional coding required.

## Benchmarking methodology
To evaluate CAIOS performance, we deployed a test application on 20 CoreWeave GPU nodes in our US-WEST-04A Availability Zone. The application performed both write and read operations to CAIOS, enabling us to measure real-world throughput and latency. Below, we detail the key components of this testing environment: CAIOS architecture, GPU architecture, and the benchmarking application.
CAIOS architecture
For these benchmarks, we relied on our standard CAIOS  implementation, which features a gateway and index layer, an object repository, and LOTA proxies on each GPU node. Together, these elements established a global cache spanning all 20 GPU nodes.
- Endpoint: The cwlota.com endpoint was used to manage all reads and writes, automatically tapping into the LOTA cache.
- Cache Configuration: Each GPU node was assigned a 1 TiB local cache (adjustable up to the limit of the node’s local disk), resulting in a 20 TiB global cache across the cluster.
This architecture ensures applications benefit from LOTA’s caching features without requiring any custom code or complex setups.
GPU architecture
While the benchmark tests themselves leveraged CPU-driven I/O rather than direct GPU storage reads, testing was conducted on our NVIDIA H200 GPU compute nodes to align with real-world production environments.
Node Configuration: Each of the 20 GPU compute nodes is equipped with:
- 8 NVIDIA H200 GPUs
- 1 NVIDIA BlueField-3 DPU with dual 100Gbps redundant network links for storage access, with total bandwidth up to 200 Gbps
- 8 NVIDIA ConnectX-7 InfiniBand (IB) adapters for inter-GPU communication

The base configuration for an NVIDIA HGX H200 supercomputer instance consists of:
- NVIDIA HGX H200 Platform built on Intel Emerald Rapids platform
- 1:1 Non-Blocking Fabric built rail optimized using NVIDIA Quantum-2 InfiniBand networking with ConnectX-7 400 Gbps adapters and NVIDIA Quantum-2 Switches
- Standard 8-rail configuration
- Topology supports NVIDIA SHARP in-network computing for collectives
- NVIDIA BlueField-3 DPU Ethernet
Benchmark testing application
We used the open-source Warp S3 benchmarking tool, which simulates various read/write scenarios using randomly generated data. Warp allows fine-grained control over:
- Object size
- Number of objects
- Concurrency (threads)
- Test duration
In this test, each instance of Warp running on each GPU node wrote 10,000 objects, each sized at 50 MiB with 10 MiB parts, utilizing 100 concurrent threads. Warp then conducted random read operations across the 20 GPU nodes for 10 minutes. Repeated access to the same objects on multiple nodes allowed the LOTA cache to showcase its ability to accelerate subsequent reads.

## Performance results
To monitor performance in real time, we set up a Grafana dashboard that queried CAIOS metrics and visualized them in a series of interactive graphs. Users wishing to replicate this setup should ensure helm and kubectl are installed to start and stop the test environment.
We started the test by running the following command:
helm install warp -f my-values.yaml .
This command initiated the creation and upload of the 10,000 objects to CAIOS. Once all objects were uploaded, the read phase began, with each GPU node retrieving these objects randomly.
In the first minute, while the LOTA cache was still being populated, we observed an aggregate read throughput of approximately 24 GiB/s, or 1.2 GiB/s per node.
Within another minute, as shown below, the cache reached full capacity and delivered all subsequent reads from local NVMe storage. This stage saw a drastic jump in performance to 368 GiB/s total, translating to an average of 18.4 GiB/s per GPU node or 2.3 GiB/s per GPU. 

This test demonstrates that CAIOS can exceed 2 GiB/s of read performance per GPU, an achievement further corroborated by CAIOS customers who operate at scales of thousands of GPU nodes. Because the performance of the cached or pre-staged data being read is entirely driven by the performance of the GPU-node-local storage, this performance is expected to scale to any number of GPU nodes and GPUs.

## Real-world impact
In demanding AI workflows, especially those involving multi-model training with large media files, speed and reliability in data access directly impact productivity and costs. CAIOS meets this need by intelligently caching or pre-staging data on local NVMe disks with LOTA. As soon as any segment of an object is accessed, the entire object is cached for subsequent reads, ensuring faster retrieval in scenarios like autonomous vehicle video training or checkpoint restoration, where partial reads are common.
Additionally, users can proactively load datasets into the cache. This is particularly useful for large multimedia files, inference applications, and container registry images. Leveraging this pre-staging strategy keeps critical data ready for immediate GPU access, further streamlining training cycles, speeding up inference response times, and reducing overall compute costs.

## Paving the way for AI storage innovation
Our rigorous benchmark tests reaffirm the strong throughput, scalability, and caching prowess of CAIOS in even the most demanding AI workloads. By seamlessly integrating with GPU nodes and employing LOTA to accelerate data access, the platform ensures low-latency performance even at massive scale, enabling data scientists and ML engineers to train larger and more complex models faster. Our next phase of benchmarking efforts will expand to evaluating write performance, a critical capability for checkpoint operations. Given CAIOS’s horizontally scalable design, we anticipate a similarly robust write throughput that parallels our read-performance findings, further solidifying its role in handling massive datasets. With its ability to handle exabyte-scale workloads while maintaining exceptional speed and efficiency, CAIOS is poised to be a critical enabler of modern AI applications.If you’re interested in learning more about CAIOS and how it can support your AI innovations, contact us here.

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
