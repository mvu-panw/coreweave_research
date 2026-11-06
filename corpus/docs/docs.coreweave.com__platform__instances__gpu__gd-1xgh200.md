# GH200

Source: https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200

# GH200

> Specifications and availability for the GH200 GPU instance

Powered by a single NVIDIA GH200 Grace Hopper Superchip, this instance offers a unique architecture that combines a 72-core Grace CPU with a Hopper GPU. Its defining feature is the 576 GB unified memory pool (96 GB HBM3 + 480 GB LPDDR5X) connected via the high-speed NVLink-C2C interconnect. This design eliminates traditional PCIe bottlenecks and allows the GPU to access a massive memory space, making it unparalleled for running extremely large models on a single machine.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `gd-1xgh200` |
| **GPU** | 1x NVIDIA GH200 Grace Hopper |
| **GPU RAM** | 96 GB |
| **GPU connectivity** | N/A - NVLink-C2C to CPU |
| **CPU model** | NVIDIA Grace Arm v9 (3.10 GHz) |
| **vCPUs** | 72 |
| **RAM** | 480 GB |
| **Usable storage**<sup>1</sup> | 7.68 TB |
| **Storage configuration** | Single drive, no RAID |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Low-latency inference for models that are too large to fit in the memory of a standard GPU, large-scale graph analytics, and memory-intensive data science.

## Recommended models

Inference on heavily quantized versions of modern state-of-the-art models (500B - 1T parameters) like Kimi K2.6, GLM 5.1, as well as moderately quantized versions of other large models such as DeepSeek V4 Flash and MiniMax-M2.7 in the 100B-500B parameter range.
