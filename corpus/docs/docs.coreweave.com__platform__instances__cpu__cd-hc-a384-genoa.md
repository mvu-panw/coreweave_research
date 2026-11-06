# High Core AMD Genoa

Source: https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384-genoa

# High Core AMD Genoa

> Specifications, pricing, and availability for the High Core AMD Genoa CPU instance

This instance type is powered by an AMD Genoa CPU with a high core count. It's best for workloads that require good multi-threaded CPU performance. The large RAM capacity provides ample memory for running large datasets.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | High Core |
| **Instance ID** | `cd-hc-a384-genoa` |
| **CPU model** | AMD Genoa 9654 (2.40 GHz) |
| **Processor count** | 2 |
| **Core count per processor** | 96 |
| **Total core count** | 192 |
| **vCPUs**<sup>1</sup> | 384 |
| **RAM** | 1536 GB |
| **Usable storage**<sup>2</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

Workloads that require good multi-threaded CPU performance and large memory capacity.
