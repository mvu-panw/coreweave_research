# RTX PRO 6000 Blackwell Server Edition (High Memory)

Source: https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x

# RTX PRO 6000 Blackwell Server Edition (High Memory)

> Specifications and availability for the RTX PRO 6000 Blackwell Server Edition (High Memory) GPU instance

Powered by eight NVIDIA RTX PRO 6000 GPUs based on the Blackwell architecture, these instances provide a versatile and efficient solution for a mix of AI and professional graphics workloads. Each GPU has 96 GB of GDDR7 memory and connects via a high-speed PCIe interface. While they lack NVLink for memory pooling across GPUs, their large individual GPU memory makes them excellent for running multiple inference jobs in parallel or handling high-resolution rendering tasks.

This instance was previously called RTX PRO 6000 Blackwell.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | Professional AI & Graphics |
| **Instance ID** | `rtxp6000-8x` |
| **GPU** | 8x NVIDIA RTX PRO 6000 |
| **GPU RAM** | 96 GB |
| **GPU connectivity** | PCIe |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **vCPUs** | 128 |
| **RAM** | 1024 GB |
| **Usable storage**<sup>1</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**EU-SOUTH-04A**](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [**US-EAST-01A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [**US-EAST-06A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [**US-EAST-13A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [**US-EAST-14A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-14a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [**US-WEST-04A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [**US-WEST-09B**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) [**US-WEST-10A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

High-performance inference and fine-tuning for mid-sized models and high-fidelity rendering.

## Recommended models

Inference and fine-tuning of mid-sized models up to 70B, such as Gemma 4 31B and Qwen 3.6 35B-A3B, on a per-GPU basis.
