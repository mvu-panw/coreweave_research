# General Purpose AMD Turin (Standard Memory)

Source: https://docs.coreweave.com/platform/instances/cpu/turin-gp-v2

# General Purpose AMD Turin (Standard Memory)

> Specifications, pricing, and availability for the General Purpose AMD Turin (Standard Memory) CPU instance

This instance type is powered by an AMD Turin CPU with a balance of core count and clock speed. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `turin-gp-v2` |
| **CPU model** | AMD Turin 9655P (2.60 GHz) |
| **Processor count** | 1 |
| **Core count per processor** | 96 |
| **Total core count** | 96 |
| **vCPUs**<sup>1</sup> | 192 |
| **RAM** | 768 GB |
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
