# GB200 NVL72-powered instances

Source: https://docs.coreweave.com/platform/instances/gpu/gb200-4x

# GB200 NVL72-powered instances

> Specifications and availability for the GB200 NVL72-powered instances GPU instance

Powered by NVIDIA GB200 GPUs with InfiniBand connectivity, these instances deliver a monumental leap in performance over the previous generation, setting the new standard for large-scale AI and high-performance computing. The GB200 instances are equipped with 13.4 TB of high-bandwidth GPU memory per rack and fifth-generation NVLink with up to 130 TB/s total bandwidth. Blackwell GPUs feature a second-generation Transformer Engine with new FP4 and FP6 precision, drastically accelerating LLM inference and training. The NVL72 architecture provides unprecedented memory capacity and ultra-fast GPU-to-GPU communication for distributed computing at the largest scale.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | State-of-the-Art Compute |
| **Instance ID** | `gb200-4x` |
| **GPU** | 4x NVIDIA GB200 |
| **GPU RAM** | 186 GB |
| **GPU connectivity** | InfiniBand & NVLink |
| **CPU model** | 2x NVIDIA Grace Arm v9 (3.10 GHz) |
| **vCPUs** | 144 |
| **RAM** | 960 GB |
| **Usable storage**<sup>1</sup> | 15.36 TB |
| **Storage configuration** | 4x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**CA-EAST-01A**](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [**US-EAST-01A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-08A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [**US-EAST-13A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training foundation models from scratch (500B+ parameters), massive-scale inference, and developing frontier AI systems.

## Recommended models

DeepSeek V4 Pro, Kimi K2.6, GLM 5.1, and other future advanced GPT-5 class models, complex Mixture-of-Experts (MoE) models, and large multimodal systems built for coding and agentic workflows.
