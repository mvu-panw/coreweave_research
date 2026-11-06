# General Purpose Intel Ice Lake

Source: https://docs.coreweave.com/platform/instances/cpu/cd-gp-i96-icelake

# General Purpose Intel Ice Lake

> Specifications, pricing, and availability for the General Purpose Intel Ice Lake CPU instance

This instance type is powered by an Intel Ice Lake CPU with a balance of core count and clock speed. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance. The large RAM capacity provides ample memory for running large datasets.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `cd-gp-i96-icelake` |
| **CPU model** | Intel Ice Lake 6342 (2.80 GHz) |
| **Processor count** | 2 |
| **Core count per processor** | 24 |
| **Total core count** | 48 |
| **vCPUs**<sup>1</sup> | 96 |
| **RAM** | 384 GB |
| **Usable storage**<sup>2</sup> | 6.40 TB |
| **Storage configuration** | 3x 6.4 TB RAID 1 (3-way mirror) |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General compute workloads that require a mix of single-threaded and multi-threaded performance.
