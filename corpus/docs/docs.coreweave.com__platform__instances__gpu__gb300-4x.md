# GB300 NVL72 Quantum-X InfiniBand

Source: https://docs.coreweave.com/platform/instances/gpu/gb300-4x

# GB300 NVL72 Quantum-X InfiniBand

> Specifications and availability for the GB300 NVL72 Quantum-X InfiniBand GPU instance

Powered by two NVIDIA GB300 Grace Blackwell Ultra Superchips (four Blackwell Ultra GPUs, each with an unprecedented 279 GB of memory), these instances represent the absolute pinnacle of our high-performance computing offerings. These instances form part of a larger NVL72 rack architecture which boasts 20.1 TB of total GPU memory, interconnected by 5th-generation NVLink for a seamless, rack-scale memory fabric. For clustering, they are equipped with next-generation NVIDIA Quantum-X800 InfiniBand and ConnectX-8 SuperNICs, delivering a groundbreaking 800 Gbps of network bandwidth, double that of the previous generation.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | State-of-the-Art Compute |
| **Instance ID** | `gb300-4x` |
| **GPU** | 4x NVIDIA GB300 |
| **GPU RAM** | 279 GB |
| **GPU connectivity** | Quantum-X800 InfiniBand & NVLink |
| **CPU model** | 2x NVIDIA Grace Arm v9 (3.10 GHz) |
| **vCPUs** | 144 |
| **RAM** | 960 GB |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 200GbE |
| **Default GPU driver** | `580` |
| **Compatible GPU driver** | `580`, `595`, `615` |
| **Availability** | [**CA-EAST-01A**](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [**US-CENTRAL-07A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [**US-CENTRAL-09A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training next-generation foundation models in the trillion-parameter class, massive-scale and high-fidelity inference on the most complex AI models, and scientific simulations requiring maximum memory capacity and the fastest data throughput.

## Recommended models

Next-generation frontier models (multi-trillion parameters), state-of-the-art multimodal systems, and large-scale scientific discovery models.
