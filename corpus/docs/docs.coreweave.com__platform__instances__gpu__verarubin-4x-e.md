# Vera Rubin NVL72 Spectrum-X RoCE

Source: https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e

# Vera Rubin NVL72 Spectrum-X RoCE

> Specifications and availability for the Vera Rubin NVL72 Spectrum-X RoCE GPU instance

Powered by four NVIDIA Rubin GPUs paired with NVIDIA Vera Arm CPUs, these instances target the most demanding AI training and inference workloads. Each Rubin GPU provides up to 288 GB of next-generation HBM4 memory and connects over sixth-generation NVLink (NVLink 6) for a rack-scale, high-bandwidth memory fabric. These instances form part of a larger NVL72 rack architecture with 20.7 TB of total GPU memory. Compared to GB200, Vera Rubin delivers up to 5x inference and 3.5x training performance. For clustering, these instances use next-generation NVIDIA Spectrum-X RoCE (RDMA over Converged Ethernet) with BlueField-4 and ConnectX-9 SuperNICs for large-scale AI in Ethernet-based cloud environments.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | State-of-the-Art Compute |
| **Instance ID** | `verarubin-4x-e` |
| **GPU** | 4x NVIDIA Rubin |
| **GPU RAM** | Up to 288 GB HBM4 |
| **GPU connectivity** | Spectrum-X RoCE & NVLink 6 |
| **CPU model** | 2x NVIDIA 88-core Vera |
| **vCPUs** | 352 |
| **RAM** | Up to 1.5 TB LPDDR5 |
| **Usable storage**<sup>1</sup> | 30.72 TB |
| **Storage configuration** | 4x 15.36 TB RAID 10 |
| **NIC configuration** | Dual-port 200GbE |
| **Default GPU driver** | `620` |
| **Compatible GPU driver** | `620` |
| **Availability** | [**US-CENTRAL-09A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) |

> [!NOTE]
>
> <sup>1</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Training next-generation foundation models in the trillion-parameter class, massive-scale and high-fidelity inference on the most complex AI models, and memory-intensive scientific simulations that require maximum throughput.

## Recommended models

Next-generation frontier models (multi-trillion parameters), state-of-the-art multimodal systems, and large-scale scientific discovery models.
