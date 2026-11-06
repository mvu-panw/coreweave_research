# High Performance AMD Genoa

Source: https://docs.coreweave.com/platform/instances/cpu/cd-hp-a96-genoa

# High Performance AMD Genoa

> Specifications, pricing, and availability for the High Performance AMD Genoa CPU instance

This instance type is powered by an AMD Genoa CPU with a high clock speed. It's best for workloads that benefit from high single-threaded CPU performance.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | High Performance |
| **Instance ID** | `cd-hp-a96-genoa` |
| **CPU model** | AMD Genoa 9274F (4.05 GHz) |
| **Processor count** | 2 |
| **Core count per processor** | 24 |
| **Total core count** | 48 |
| **vCPUs**<sup>1</sup> | 96 |
| **RAM** | 768 GB |
| **Usable storage**<sup>2</sup> | 7.68 TB |
| **Storage configuration** | 1x 7.68, or 2x 7.68 RAID 1 (depending on SKU) |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

High-performance computing workloads that benefit from high single-threaded CPU performance.
