# Storage Benchmarking: Distributed File Storage | CoreWeave

Source: https://www.coreweave.com/blog/storage-benchmarking-distributed-file-storage

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

CoreWeave Distributed File Storage benchmarking performance tests show that one GiB/s per GPU can be sustained when scaling up to hundreds of NVIDIA GPUs for simulated AI training workloads.
High-performance storage is critical to the success of AI model training workloads. As the complexity and size of AI models continue to grow, the demands on storage systems have intensified, creating unique challenges for data scientists and machine learning (ML) engineers. AI infrastructure must be equipped to handle the massive datasets required for training state-of-the-art models while ensuring low latency access and high throughput.
To address these challenges, CoreWeave provides customers with a cutting-edge distributed file storage system optimized for the demands of large-scale model training. We recently conducted storage benchmark tests of this solution to demonstrate our infrastructure's capabilities and provide valuable insights for teams looking to optimize their training workflows.
In this article, we cover:
- Storage patterns and CoreWeave’s architecture design
- The methodology used for the series of tests
- Benchmark results and discussion
These benchmarks are essential for evaluating and optimizing storage, allowing CoreWeave customers to accelerate model training time and overall efficiency through continuous monitoring and optimization of clusters. Our goal in providing these insights is to enable you to run your own benchmarks, evaluate storage performance, and identify areas for optimization to leverage the platform's capabilities for your AI workloads.

## Key Background on Storage for ML and CoreWeave’s Architecture
Measuring and evaluating storage performance can rarely (if ever) be compared 1:1 across platforms and solutions. Storage patterns, dataset size, and the architecture of the underlying infrastructure play a crucial role in determining storage performance. 
This section gives an overview of I/O patterns as they relate to large-scale training workloads and CoreWeave’s storage architecture design, which was built to balance security, performance, and stability.

### Understanding Machine Learning Storage Patterns
To understand storage requirements for large-scale training, let's examine the I/O patterns of a representative workload: training a multi-billion parameter model across 4096 NVIDIA H100 GPUs.
Graphic shows the I/O pattern of a multi-billion parameter model training workload. blue = read operations; red = write operations
The graph above illustrates I/O patterns during the initial two hours of training, with the blue line representing read operations and the red line showing write operations. The workflow exhibits two distinct patterns:
- Initial Data Loading: The model loads data into GPU memory at startup, causing an intense burst of read operations. This phase is characterized by high-volume, partially random read patterns. Part of optimizing the data is storing it to minimize the random reads and maximize the sequential reads.
- Checkpoint Operations: Periodic spikes in write traffic correspond to checkpoint operations, where the model state is written to storage. While some frameworks support asynchronous checkpointing, this example shows synchronous writes, creating distinct I/O peaks.
Analyzing the data rates provides additional insight into storage requirements:
Graphic shows the data rate of the I/O operations for a multi-billion parameter model training workload. blue = read operations; red = write operations
The workload demonstrates peak read rates of approximately 70 GiB/s and write spikes reaching 50 GiB/s. As we scale up, the checkpoint write rate is limited by the number of ranks checkpoints are written from and the connectivity of those hosts. Typically, these metrics scale with GPU count; as the number of GPUs increases, we expect more machines to be writing checkpoints. 
The pattern shown here remains consistent throughout the training cycle, with periodic checkpoint operations creating predictable I/O spikes. It's worth noting that the storage infrastructure supporting this cluster maintains substantial headroom above these observed peaks, ensuring consistent performance even under concurrent workloads.

### Storage Architecture Design
In addition to storage patterns, architecture design plays an important role in training efficiency, infrastructure scalability, and throughput. Storage systems must be specifically architected for ML workload patterns, and performance must scale linearly with infrastructure growth.
Model training represents a significant portion of CoreWeave's cloud workloads, with our CoreWeave Distributed File Storage throughput being critical for training efficiency. Our infrastructure utilizes VAST Data's storage architecture, which implements a disaggregated two-tier system:
- CNodes (Controller Nodes): Handle data management, I/O scheduling, and storage operations
- DNodes (Data Nodes): Provide the physical storage capacity and data persistence
The cluster used for the benchmark testing employs a 24x16 configuration (24 CNodes, 16 DNodes). This architecture allows independent scaling of performance (by adding CNodes) and capacity (by adding DNodes), enabling precise infrastructure optimization for specific workload requirements.
The diagram illustrates the fundamental architecture: CNodes are positioned at the top layer, and DNodes are at the bottom, interconnected via NVMe fabric. While simplified for clarity, this representation captures the essential structure of our production environment

### Performance Validation
As datasets used for training have grown, teams may see storage and I/O bottlenecks significantly impacting performance and efficiency. These bottlenecks occur when the storage system cannot keep up with the data demands of powerful GPUs, leading to underutilization of computational resources.
CoreWeave's comprehensive monitoring infrastructure provides detailed performance data for each workload, validating that storage doesn’t create such bottlenecks in our system. The GPU Core utilization graph below demonstrates sustained 100% core utilization with only minor dips during initial data loading and checkpoint operations—clear evidence that the GPUs operate at peak efficiency rather than waiting for data.
This graph demonstrates sustained 100% core utilization with only minor dips during initial data loading and checkpoint operations
CoreWeave optimizes our distributed file storage systems for these distinct phases (read operations and write operations) and leverages a scalable architecture design through our partnership with VAST Data. In doing so, customers can significantly improve the efficiency of AI model training, reduce costs associated with idle GPU time, and accelerate the development of cutting-edge AI models with a robust storage solution.

## Storage Benchmarks: Methodology 
Having established the characteristic I/O patterns of ML training workloads, we can now examine the underlying storage architecture and its performance characteristics in detail. 
To evaluate CoreWeave Distributed File Storage performance under these conditions, we employed the Flexible I/O (fio) tester, an industry-standard benchmarking tool for storage systems. Our testing methodology utilized CoreWeave's default Ubuntu 22.04 environment, with tests orchestrated through Slurm across our hybrid Slurm/Kubernetes infrastructure. The test suite comprises:
- Read tests: Simulating mixed sequential/random I/O patterns across varying block sizes. The test script tests sequential and random reads with various sizes varying from 32M to 1k. The results presented are an average of the sequential and random IO performance.
- Write tests: Focusing on sequential writes to replicate checkpoint operations. Just as in the read tests, various block sizes are tested, varying from 32M to 1k.
Complete test configurations and execution scripts are available in our public repository, enabling reproduction and validation of these results.

Before presenting the benchmark results, it's essential to understand the hardware configuration that shapes these workloads.
ML training operations typically process datasets that exceed single-GPU memory capacity by orders of magnitude. Current-generation training hardware commonly features eight GPUs per compute node, resulting in concurrent I/O operations from eight separate processes or threads per node. This parallel access pattern significantly influences storage system design and performance requirements.
The critical performance metric in this architecture is the achievable network throughput across eight concurrent processes. While the following benchmarks were conducted using CPU-driven I/O rather than GPU-direct storage access, they were performed on our NVIDIA H200 GPU compute nodes to maintain configuration consistency with production environments.
The base infrastructure configuration consists of compute nodes, each equipped with:
- 8 NVIDIA H200 GPUs for computation
- 1 NVIDIA BlueField-3 DPU with dual 100Gbps redundant network links for storage access
- 8 NVIDIA ConnectX-7 InfiniBand (IB) cards for inter-GPU communication

The base configuration for an NVIDIA HGXTM H200 supercomputer instance consists of:
- NVIDIA HGX H200 Platform built on Intel Emerald Rapids platform
- 1:1 Non-Blocking GPUDirect Fabric built rail optimized using NVIDIA Quantum-2 InfiniBand networking with ConnectX-7 400 Gbps HCAs and Quantum-2 Switches
- Standard 8 rail configuration
- Topology supports NVIDIA SHARP in-network collections
- NVIDIA BlueField-3 DPU Ethernet
CoreWeave Distributed File Storage connectivity in CoreWeave's infrastructure is facilitated through NVIDIA BlueField-3 Data Processing Units (DPUs). While these devices offer extensive functionality, their primary role in this context is providing networked storage access with robust tenant isolation, analogous to VLAN segmentation in traditional networks. Each DPU link supports 100 Gib/s (12.5 GiB/s) of network connectivity.
This architecture deliberately separates storage traffic from the NVIDIA Quantum-2 InfiniBand fabric used for inter-GPU communication. This separation is crucial for maintaining optimal performance, as the InfiniBand network experiences intense utilization during training operations. Segregating storage traffic ensures that neither storage access nor GPU-to-GPU communication becomes a bottleneck, supporting our primary objective of maintaining peak GPU utilization.
Now that we have a thorough understanding of the test configuration and CoreWeave’s node architecture, let’s take a look at the benchmark results for CoreWeave Distributed File Storage.

## Benchmark Results & Discussion
As a reminder, we conducted 4 tests of CoreWeave Distributed File Storage system using the Flexible I/O (fio) tester to examine the performance (throughput) and scalability from 8 servers up to 64 servers. 

### Test 1: Standard Node Performance Testing
The graph below illustrates read performance for eight concurrent processes on a single server. It demonstrates a balanced workload of 50% random access and 50% sequential reads across various block sizes. This synthetic workload, generated using fio, replicates the read patterns observed in our earlier training analysis.
Read performance for eight concurrent GPUs on a single server with various block sizes
As expected, the benchmark results demonstrate a clear correlation between block size and achievable throughput. Performance scales from modest rates with small block sizes (few KB) to peak throughput approaching 11 GiB/s with larger blocks (multiple MB). This achievement represents approximately 88% of the theoretical maximum throughput (12.5 GiB/s), a strong result for real-world conditions with mixed sequential/random access patterns. While these benchmarks utilize CPU-driven I/O rather than GPU-direct storage access, they provide a conservative baseline for system capabilities.
The performance characteristics of small-block operations are relevant for ML workloads, as they often involve frequent small reads interspersed with larger transfers.  Small block size has lower throughput performance but higher Input/Output Operations per Second (IOPS) performance by its nature, which is true for any platform. Small block size is common and highly parallelizable, but the most throughput-demanding workload, checkpointing, doesn’t need a small block size. 

### Test 2: Multi-Node Performance Scaling
Traditional HPC environments commonly employ parallel file systems such as Lustre, which excel at large-block I/O operations. However, ML workload characteristics diverge significantly from traditional HPC patterns. Lustre's architecture, while robust, requires a minimum of two communication steps for each data access: metadata lookup followed by data retrieval. This architectural choice introduces latency overhead that becomes significant with small-block operations.
For large-block transfers, where data movement time dominates, this metadata overhead is negligible. However, with small-block operations typical in ML workloads, minimizing access latency becomes critical. This requirement led to our adoption of VAST's implementation of NFS, which completes small-file operations in a single request, providing superior performance for ML-typical access patterns.
Production ML environments typically operate at a significant scale, ranging from tens to thousands of compute nodes. While the internal architecture of individual nodes remains consistent at scale, aggregate network utilization increases substantially. CoreWeave's network architecture is designed to sustain 1 GiB/s per GPU across the entire infrastructure. One GiB/s per GPU was chosen carefully, this is a design decision based on the available PCI bandwidth when multiple NVIDIA H100 and H200 servers are busy working on a large training job. The PCI layer is kept very busy with Infiniband traffic during training. 
If more performance was available at any point, say within the storage itself or in the network fabric, we would be unlikely to see any performance benefit. As newer architectures are released we expect this number to increase and to improve the network performance as needed.
To validate performance at scale, we conducted multi-node performance testing:
Read performance for 64 concurrent GPUs on eight interconnected servers with various block sizes
Initial scale testing with eight NVIDIA H200 GPU nodes demonstrates near-linear performance scaling. At 32 MiB block sizes, each node maintains 7.96 GiB/s throughput, representing only minimal degradation from single-node performance. This result validates our network architecture's capability to maintain consistent per-node performance as we scale out.

### Test 3: Large-Scale Performance Testing
Expanding the scale testing to 64 nodes provides insight into larger-scale deployment characteristics:
Read performance for 512 concurrent GPUs on 64 interconnected servers with various block sizes
The 64-node NVIDIA H200 GPU cluster achieves aggregate read throughput exceeding ~500 GiB/s, maintaining per-node performance at 7.94 GiB/s, which is remarkably close to our target of 8 GiB/s per node. This consistent per-node performance at scale validates our architecture's linear scaling capabilities. 
Additionally, with smaller block sizes, the VAST storage infrastructure demonstrates the capability to handle approximately 2 million IOPS, highlighting its ability to maintain high performance across varying access patterns.

### Test 4: Sequential Write Performance Scaling
Write performance analysis focuses on sequential operations, reflecting the checkpoint-driven nature of ML workloads:
Write performance for 64 concurrent GPUs on eight interconnected servers with various block sizes
Write performance testing demonstrates consistent throughput characteristics across scale, with single-node performance maintained even in multi-node deployments. As with read operations, larger block sizes yield higher bandwidth utilization, aligning with expected CoreWeave Distributed File Storage behavior. This consistency in write performance is particularly important for maintaining predictable checkpoint operation timing across large-scale training runs.

## Conclusion
Storage benchmarking is a critical part of CoreWeave’s commitment to delivering industry-leading NVIDIA GPU cluster performance for our customers. These benchmarks not only showcase the raw capabilities of CoreWeave's Distributed File Storage system but also highlight how optimized storage solutions can enable faster training time and scaling of AI workloads with minimal infrastructure bottlenecks.
Here’s a quick summary of the results:
- Single server NVIDIA H200 GPU cluster: 88% of the theoretical maximum throughput (12.5 GiB/s), a strong result for real-world conditions with mixed sequential/random access patterns.
- 8-node NVIDIA H200 GPU cluster: Each node maintains 7.96 GiB/s throughput, representing only minimal degradation from single-node performance.
- 64-node NVIDIA H200 GPU cluster: Achieved aggregate read throughput exceeding ~500 GiB/s, maintaining per-node performance at 7.94 GiB/s, which is remarkably close to our target of 8 GiB/s per node (1 GiB/s/GPU).
For teams training models on CoreWeave's platform, these benchmark results indicate tangible benefits. They can expect faster data loading, reduced I/O bottlenecks, and improved scalability for their training workloads. This enhanced performance allows CoreWeave customers to iterate more quickly, experiment with larger datasets, and ultimately accelerate the development of cutting-edge AI models—without being hindered by storage-related performance issues.
We encourage you to conduct your own storage benchmarks, as these tests also offer an opportunity to identify areas for optimization. Reach out to our team for more information on CoreWeave storage solutions.

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
