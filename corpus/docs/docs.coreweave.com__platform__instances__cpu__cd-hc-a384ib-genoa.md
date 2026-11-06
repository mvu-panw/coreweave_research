# High Core AMD Genoa (InfiniBand)

Source: https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384ib-genoa

# High Core AMD Genoa (InfiniBand)

> Specifications, pricing, and availability for the High Core AMD Genoa (InfiniBand) CPU instance

This instance type is an InfiniBand-enabled variant of the standard High Core AMD Genoa CPU instance, based on the same AMD Genoa 9654 platform with a very high vCPU count and large RAM capacity. It is intended for HPC and tightly coupled multi-node workloads that require strong multi-threaded CPU performance and access to an InfiniBand fabric for low-latency, high-throughput inter-node communication (for example, MPI-based simulations or CPU-heavy components of hybrid GPU/CPU HPC pipelines).

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | High Core |
| **Instance ID** | `cd-hc-a384ib-genoa` |
| **CPU model** | AMD Genoa 9654 (2.40 GHz) |
| **Processor count** | 2 |
| **Core count per processor** | 96 |
| **Total core count** | 192 |
| **vCPUs**<sup>1</sup> | 384 |
| **RAM** | 1536 GB |
| **Usable storage**<sup>2</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE & InfiniBand |
| **Availability** | [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

HPC workloads that need good multi-threaded CPU performance and large memory capacity, and access to an InfiniBand-based fabric for tightly coupled, latency-sensitive communication across Nodes.
