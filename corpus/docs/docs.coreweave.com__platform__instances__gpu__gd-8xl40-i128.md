# L40

Source: https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128

# L40

> Specifications and availability for the L40 GPU instance

Powered by eight NVIDIA L40 GPUs, each with 48 GB of GDDR6 memory, these instances are designed for exceptional versatility across AI and visual computing. Connected via PCIe, they offer a balanced profile for workloads that include AI inference, rendering, and video processing. They are an ideal entry point for deploying AI-powered services that also have a significant graphics component.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `gd-8xl40-i128` |
| **GPU** | 8x NVIDIA L40 |
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
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General-purpose AI inference, small-scale model fine-tuning, high-resolution rendering, and virtual desktop infrastructure (VDI).

## Recommended models

Inference for models up to \~40B parameters like Gemma 4 26B or Qwen 3.6 27B; efficient fine-tuning of smaller sub-15B models.
