# A100

Source: https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128

# A100

> Specifications and availability for the A100 GPU instance

These instances are powered by eight NVIDIA A100 Tensor Core GPUs, each providing 80 GB of high-bandwidth HBM2e memory. As a foundational accelerator for the previous generation of AI, these are versatile instances that deliver excellent performance for mixed-precision workloads. The GPUs are interconnected with NVIDIA NVLink, making them a powerful and proven choice for distributed training. Their configuration offers a cost-effective solution for a wide range of demanding AI and data analytics tasks.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `gd-8xa100-i128` |
| **GPU** | 8x NVIDIA A100 |
| **GPU RAM** | 80 GB |
| **GPU connectivity** | NVLink |
| **CPU model** | Intel Ice Lake 8358 (2.60 GHz) |
| **vCPUs** | 128 |
| **RAM** | 2048 GB |
| **Usable storage**<sup>1</sup> | 7.68 TB |
| **Storage configuration** | Single drive, no RAID |
| **NIC configuration** | Single-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

AI model training, high-performance inference, and various HPC applications including scientific simulations.

## Recommended models

Training models up to 40B parameters such as Gemma 4 31B; a standard choice for fine-tuning most mid-sized open-source models. For inference, they can handle models up to 40B, such as Qwen 3.6 35B-A3B, on a per-GPU basis or a single instance of a quantized larger model such as Qwen 3.5 397B-A17B utilizing tensor parallelism.
