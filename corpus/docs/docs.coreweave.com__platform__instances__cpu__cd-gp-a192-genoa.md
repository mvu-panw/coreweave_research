# General Purpose AMD Genoa

Source: https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa

# General Purpose AMD Genoa

> Specifications, pricing, and availability for the General Purpose AMD Genoa CPU instance

This instance type is powered by an AMD Genoa CPU with a balance of core count and clock speed. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance. The large RAM capacity provides ample memory for running large datasets.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `cd-gp-a192-genoa` |
| **CPU model** | AMD Genoa 9454 (2.75 GHz) |
| **Processor count** | 2 |
| **Core count per processor** | 48 |
| **Total core count** | 96 |
| **vCPUs**<sup>1</sup> | 192 |
| **RAM** | 1536 GB |
| **Usable storage**<sup>2</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-06A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [**US-WEST-04A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General compute workloads that require a mix of single-threaded and multi-threaded performance.
