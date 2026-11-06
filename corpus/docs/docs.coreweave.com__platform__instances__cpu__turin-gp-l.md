# General Purpose AMD Turin (High Storage)

Source: https://docs.coreweave.com/platform/instances/cpu/turin-gp-l

# General Purpose AMD Turin (High Storage)

> Specifications, pricing, and availability for the General Purpose AMD Turin (High Storage) CPU instance

This is a variant of the General Purpose AMD Turin instance with larger storage capacity. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance when larger storage is needed. The large RAM capacity provides ample memory for running large datasets.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `turin-gp-l` |
| **CPU model** | AMD Turin 9655P (2.60 GHz) |
| **Processor count** | 1 |
| **Core count per processor** | 96 |
| **Total core count** | 96 |
| **vCPUs**<sup>1</sup> | 192 |
| **RAM** | 1536 GB |
| **Usable storage**<sup>2</sup> | 30.72 TB |
| **Storage configuration** | 8x 7.68 TB RAID 10 |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**RNO2A**](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [**US-CENTRAL-09A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) [**US-EAST-02A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [**US-EAST-15A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [**US-EAST-17A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-17a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General compute workloads that require a mix of single-threaded and multi-threaded performance with larger storage needs.
