# HPC Interconnect

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect

# HPC Interconnect

> High-performance InfiniBand and RoCE RDMA networking for GPU training workloads

CoreWeave Kubernetes Service (CKS) is designed for high-performance computing (HPC) workloads. CoreWeave GPUs and optimized networking fabrics provide the environment for parallel jobs, with thousands to tens of thousands of GPUs working together in areas such as neural net training, rendering, and simulation.

For highly parallel workloads, such as training large language models, the network fabric is a critical component. CoreWeave offers two high-performance RDMA-enabled fabrics: NVIDIA Quantum InfiniBand and NVIDIA Spectrum-X (RoCE). Both fabrics are optimized for high throughput and low latency, and they use a non-blocking, fat-tree architecture to support large-scale AI models.

This page introduces both fabrics and the supporting technologies, including GPUDirect RDMA and NVIDIA Mellanox SHARP, so you can choose the right interconnect for your workload.

## HPC over RDMA with InfiniBand (Quantum-X)

GPUDirect RDMA over InfiniBand provides low-latency, high-reliability communication for GPUs to exchange information in traditional HPC environments.

CoreWeave has partnered with NVIDIA to design CoreWeave's InfiniBand interconnected clusters using NVIDIA Quantum-2 and Quantum-X800 technology. These clusters use GPUDirect to let GPUs communicate directly with each other across the InfiniBand fabric, which bypasses the Node's CPU and kernel resources. InfiniBand is the industry standard for large-scale LLM training and scientific discovery models that require maximum memory fabric performance.

## HPC over RDMA with RoCE (Spectrum-X)

RDMA over Converged Ethernet (RoCE) through the NVIDIA Spectrum-X platform provides an Ethernet-native fabric designed for AI.

Available on [GB300-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb300-4x-e.md), Spectrum-X delivers high-performance RDMA using ConnectX-8 SuperNICs and BlueField-3 DPUs. [Vera Rubin instances](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) use next-generation ConnectX-9 SuperNICs and BlueField-4 DPUs, doubling per-GPU scale-out bandwidth. Both configurations provide InfiniBand-like performance, including performance isolation and congestion control, within a standard Ethernet ecosystem.

The following sections describe the underlying technologies that both fabrics rely on.

## About GPUDirect RDMA

GPUDirect Remote Direct Memory Access (RDMA) provides direct access between the main memory of two computers without involving the operating system, cache, or storage. This direct access supports high-throughput, low-latency data transfers with minimal CPU use.

In a typical IP data transfer, the kernel must handle data movement, which copies data across system memory multiple times and increases CPU load. RDMA bypasses the kernel and lets the host adapter store data directly in the application's memory space.

To learn more, see:

* [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md)
* [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md)

## About NVIDIA Mellanox SHARP

Traditionally, communication requirements scale proportionally with the number of Nodes in an HPC cluster. [NVIDIA® Mellanox® Scalable Hierarchical Aggregation and Reduction Protocol (SHARP)](https://networking-docs.nvidia.com/sharpum/270) moves collection operations from the individual Nodes into the network. This shift produces a flat scaling curve and improves the effective interconnect bandwidth.

NVIDIA Quantum switches process data as it traverses the network, which reduces the number of times that data traverses between server endpoints. The switches also aggregate large data vectors at wire speed, which is important for machine learning applications. CoreWeave's InfiniBand topology is fully SHARP compliant, and all components that use SHARP are implemented in the network control-plane, such as Adaptive Routing and Aggregation Managers.

> [!NOTE]
>
> SHARP can double the performance of a compliant InfiniBand network compared to similar networks without SHARP. For more information, see [Mellanox in-network computing for AI](https://on-demand.gputechconf.com/ai-conference-2019/T6-5__Qingchung%20Song\(Mellanox\)_Mellanox%20In-Network%20Computing%20for%20AI%20and%20the%20development%20with%20NVIDIA_Final.pdf).
