# L40S

Source: https://docs.coreweave.com/platform/instances/gpu/gd-8xl40s-i128

# L40S

> Specifications and availability for the L40S GPU instance

These instances feature eight NVIDIA L40S GPUs, each with 48 GB of GDDR6 memory. The L40S is a compute-optimized version of the L40, specifically tuned to deliver higher performance for AI and data science workloads. Connected via PCIe, these GPUs are a cost-effective choice for scaling out inference and for fine-tuning mainstream models. They provide a strong balance of performance and value for enterprise AI deployment.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `gd-8xl40s-i128` |
| **GPU** | 8x NVIDIA L40S |
| **GPU RAM** | 48 GB |
| **GPU connectivity** | PCIe |
| **CPU model** | Intel Sapphire Rapids 8462Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 1024 GB |
| **Usable storage**<sup>1</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

High-throughput inference, efficient fine-tuning, video analytics, and other compute-focused AI tasks.

## Recommended models

Inference for models up to \~40B parameters like Gemma 4 26B or Qwen 3.6 27B; efficient fine-tuning of smaller sub-15B models.
