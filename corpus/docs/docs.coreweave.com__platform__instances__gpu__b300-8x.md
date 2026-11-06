# B300 (InfiniBand)

Source: https://docs.coreweave.com/platform/instances/gpu/b300-8x

# B300 (InfiniBand)

> Specifications and availability for the B300 (InfiniBand) GPU instance

Powered by eight NVIDIA B300 Blackwell GPUs, these instances deliver outstanding performance for enterprise AI workloads, including training and real-time inference. Compared to B200 systems, they offer more performance per GPU, 50% greater GPU memory, and double the InfiniBand speed with 800G XDR non-blocking NVIDIA Quantum-X800 fabric.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | State-of-the-Art Compute |
| **Instance ID** | `b300-8x` |
| **GPU** | 8x NVIDIA B300 |
| **GPU RAM** | 270 GB |
| **GPU connectivity** | Quantum-X800 InfiniBand & NVLink |
| **CPU model** | 2 x Intel Granite Rapids (6747P) (2.70 GHz) |
| **vCPUs** | 192 |
| **RAM** | 4096 GB |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 200GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**US-CENTRAL-06A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [**US-EAST-13A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [**US-WEST-10A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training foundation models from scratch (130B+ parameters), massive-scale inference, and developing frontier AI systems.

## Recommended models

DeepSeek V4 Pro, Kimi K2.6, GLM 5.1, and other future advanced GPT-5 class models, complex Mixture-of-Experts (MoE) models, and large multimodal systems built for coding and agentic workflows.
