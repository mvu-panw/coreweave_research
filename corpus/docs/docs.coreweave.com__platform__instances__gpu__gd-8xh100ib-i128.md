# H100 (InfiniBand)

Source: https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128

# H100 (InfiniBand)

> Specifications and availability for the H100 (InfiniBand) GPU instance

These instances are powered by eight NVIDIA H100 Hopper GPUs, each with 80 GB of HBM3 memory. As the industry-defining accelerator of the previous generation, the H100 remains a powerful and reliable workhorse for a wide range of large-scale AI workloads. GPUs are fully connected with NVLink, and Nodes are linked with a 400G NDR InfiniBand fabric, providing a robust architecture for distributed training and inference.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Mid-large Size Model Training & Inference |
| **Instance ID** | `gd-8xh100ib-i128` |
| **GPU** | 8x NVIDIA H100 |
| **GPU RAM** | 80 GB |
| **GPU connectivity** | InfiniBand & NVLink |
| **CPU model** | Intel Sapphire Rapids 8462Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 2048 GB |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-CENTRAL-06A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [**US-EAST-01A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [**US-EAST-06A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [**US-WEST-02B**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-02b) [**US-WEST-04A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [**US-WEST-09B**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Large-scale AI training, high-performance inference serving, and a wide variety of HPC simulations.

## Recommended models

Quantized versions of the latest open-source models such as DeepSeek V4 Flash, Qwen 3.5 397B-A17B, Kimi K2.6, MiniMax M2.7 and other large models requiring substantial GPU memory for a single Node through the use of tensor parallelism.
