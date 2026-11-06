# B200 (InfiniBand)

Source: https://docs.coreweave.com/platform/instances/gpu/b200-8x

# B200 (InfiniBand)

> Specifications and availability for the B200 (InfiniBand) GPU instance

Powered by eight NVIDIA B200 Blackwell GPUs, each with 180 GB of HBM3e memory, these instances deliver outstanding performance for enterprise AI workloads, including training and real-time inference. They offer more than twice the performance per GPU compared to previous-generation NVIDIA Hopper GPUs. The GPUs are interconnected using NVIDIA NVLink and NVLink Switch to enable fast data transfer. For networking, B200 instances feature an NVIDIA BlueField-3 DPU and eight NVIDIA ConnectX-7 InfiniBand host channel adapters (HCAs), supporting high throughput and lossless scaling. A 400G NDR non-blocking NVIDIA Quantum-2 InfiniBand fabric ensures seamless, high-speed connectivity.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | State-of-the-Art Compute |
| **Instance ID** | `b200-8x` |
| **GPU** | 8x NVIDIA B200 |
| **GPU RAM** | 180 GB |
| **GPU connectivity** | InfiniBand & NVLink |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 2048 GB |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**EU-SOUTH-04A**](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [**US-CENTRAL-07A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [**US-EAST-13A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [**US-EAST-15A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [**US-WEST-09B**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training foundation models from scratch (100B+ parameters), massive-scale inference, and developing frontier AI systems.

## Recommended models

Deepseek V4 Pro, Kimi K2.6, GLM 5.1, and other future advanced GPT-5 class models, complex Mixture-of-Experts (MoE) models, and large multimodal systems built for coding and agentic workflows.
