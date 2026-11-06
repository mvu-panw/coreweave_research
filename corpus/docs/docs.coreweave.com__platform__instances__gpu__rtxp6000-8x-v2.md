# RTX PRO 6000 Blackwell Server Edition (Standard Memory)

Source: https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x-v2

# RTX PRO 6000 Blackwell Server Edition (Standard Memory)

> Specifications, pricing, and availability for the RTX PRO 6000 Blackwell Server Edition (Standard Memory) GPU instance

Powered by eight NVIDIA RTX PRO 6000 GPUs based on the Blackwell architecture, these instances provide a versatile and efficient solution for a mix of AI and professional graphics workloads. Each GPU has 96 GB of GDDR7 memory and connects via a high-speed PCIe interface. While they lack NVLink for memory pooling across GPUs, their large individual GPU memory makes them excellent for running multiple inference jobs in parallel or handling high-resolution rendering tasks.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `rtxp6000-8x-v2` |
| **GPU** | 8x NVIDIA RTX PRO 6000 |
| **GPU RAM** | 96 GB |
| **GPU connectivity** | PCIe |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 512 GB |
| **Usable storage**<sup>1</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**US-EAST-15A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

High-performance inference and fine-tuning for mid-sized models and high-fidelity rendering.

## Recommended models

Inference and fine-tuning of mid-sized models up to 70B, such as Gemma 4 31B and Qwen 3.6 35B-A3B, on a per-GPU basis.
