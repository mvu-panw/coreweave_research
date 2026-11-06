# General Purpose Intel Emerald Rapids (Standard Memory)

Source: https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids-v2

# General Purpose Intel Emerald Rapids (Standard Memory)

> Specifications, pricing, and availability for the General Purpose Intel Emerald Rapids (Standard Memory) CPU instance

This instance type is powered by an Intel Emerald Rapids CPU with a balance of core count and clock speed. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `cd-gp-i64-erapids-v2` |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **Processor count** | 1 |
| **Core count per processor** | 32 |
| **Total core count** | 32 |
| **vCPUs**<sup>1</sup> | 64 |
| **RAM** | 256 GB |
| **Usable storage**<sup>2</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | Contact sales for availability |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General compute workloads that require a mix of single-threaded and multi-threaded performance.
