# General Purpose Intel Emerald Rapids (High Memory)

Source: https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids

# General Purpose Intel Emerald Rapids (High Memory)

> Specifications, pricing, and availability for the General Purpose Intel Emerald Rapids (High Memory) CPU instance

This instance type is powered by an Intel Emerald Rapids CPU with a balance of core count and clock speed. It's a good choice for general compute workloads that require a mix of single-threaded and multi-threaded performance. The large RAM capacity provides ample memory for running large datasets.

This instance was previously called "General Purpose Intel Emerald Rapids" and has been renamed "General Purpose Intel Emerald Rapids (High Memory)" to better reflect the memory capacity.

## Specifications

| Feature | Detail |
| :- | :- |
| **Category** | General Purpose |
| **Instance ID** | `cd-gp-i64-erapids` |
| **CPU model** | Intel Emerald Rapids 8562Y+ (2.80 GHz) |
| **Processor count** | 1 |
| **Core count per processor** | 32 |
| **Total core count** | 32 |
| **vCPUs**<sup>1</sup> | 64 |
| **RAM** | 512 GB |
| **Usable storage**<sup>2</sup> | 7.68 TB |
| **Storage configuration** | 2x 7.68 TB RAID 1 |
| **NIC configuration** | Dual-port 100GbE |
| **Availability** | [**CA-EAST-01A**](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [**EU-SOUTH-03B**](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-03b) [**EU-SOUTH-04A**](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [**US-CENTRAL-06A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [**US-CENTRAL-07A**](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [**US-EAST-01A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [**US-EAST-04A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [**US-EAST-06A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [**US-EAST-08A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [**US-EAST-14A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-14a) [**US-EAST-15A**](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [**US-WEST-01A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [**US-WEST-04A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [**US-WEST-09B**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) [**US-WEST-10A**](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |

> [!NOTE]
>
> <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.
>
> <sup>2</sup> Usable storage is less than the raw capacity when configured as RAID. See [RAID layout and throughput](https://docs.coreweave.com/products/storage/local-storage.md#raid-layout-and-throughput) to learn about RAID configurations and their performance characteristics.

## Primary use cases

General compute workloads that require a mix of single-threaded and multi-threaded performance.
