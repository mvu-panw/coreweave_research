# H200 (InfiniBand)

Source: https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128

# H200 (InfiniBand)

> Specifications and availability for the H200 (InfiniBand) GPU instance

Powered by eight NVIDIA H200 Hopper GPUs, each equipped with 141 GB of ultra-fast HBM3e memory, these instances are purpose-built for memory-intensive AI and HPC workloads. The significant memory per GPU allows for training larger models with bigger batch sizes and longer context windows compared to its predecessor. The GPUs are interconnected with NVIDIA NVLink for a high-speed, unified memory pool within the server. For clustering, they feature NVIDIA ConnectX-7 adapters providing a 400G NDR InfiniBand fabric, making them ideal for large, distributed training jobs that are memory-bound.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Mid-large Size Model Training & Inference |
| **Instance ID** | `gd-8xh200ib-i128` |
| **GPU** | 8x NVIDIA H200 |
| **GPU RAM** | 141 GB |
| **GPU connectivity** | InfiniBand & NVLink |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 2048 GB |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**EU-SOUTH-03B**](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-03b) [**US-EAST-01A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [**US-EAST-08A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [**US-WEST-04A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training and fine-tuning large models (\~70B parameters) with high precision, high-throughput inference with long context lengths, and memory-intensive scientific computing.

## Recommended models

Full precision versions of the latest open-source models such as DeepSeek V4 Flash, Qwen 3.5 397B-A17B, Kimi K2.6, MiniMax M2.7 and other large models requiring substantial GPU memory for a single Node.
