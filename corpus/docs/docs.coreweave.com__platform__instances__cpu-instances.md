# About CPU instances

Source: https://docs.coreweave.com/platform/instances/cpu-instances

# About CPU instances

> Compare CoreWeave CPU instance types by processor and core counts, vCPUs, RAM, and storage

## CPU comparison

Use the following tables to compare CoreWeave's CPU compute instances:

* [Processor details](#processor-details): CPU model, speed, processor and core counts, and vCPU count.
* [Instance details](#instance-details): RAM, storage, and availability.

Click an instance type to view full specifications.

> [tab] Processor details
>
> | Instance | CPU Model | Speed | Processor Count | Core Count Per Processor | Total Core Count | vCPUs<sup>1</sup> |
> | :- | :- | :- | :- | :- | :- | :- |
> | [High Performance AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hp-a96-genoa.md) | AMD Genoa 9274F | 4.05 GHz | 2 | 24 | 48 | 96 |
> | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) | AMD Genoa 9454 | 2.75 GHz | 2 | 48 | 96 | 192 |
> | [General Purpose AMD Genoa (High Storage)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-l-a192-genoa.md) | AMD Genoa 9454 | 2.75 GHz | 2 | 48 | 96 | 192 |
> | [High Core AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384-genoa.md) | AMD Genoa 9654 | 2.40 GHz | 2 | 96 | 192 | 384 |
> | [High Core AMD Genoa (InfiniBand)](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384ib-genoa.md) | AMD Genoa 9654 | 2.40 GHz | 2 | 96 | 192 | 384 |
> | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) | AMD Turin 9655P | 2.60 GHz | 1 | 96 | 96 | 192 |
> | [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) | AMD Turin 9655P | 2.60 GHz | 1 | 96 | 96 | 192 |
> | [General Purpose AMD Turin (Standard Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-v2.md) | AMD Turin 9655P | 2.60 GHz | 1 | 96 | 96 | 192 |
> | [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Intel Emerald Rapids 8562Y+ | 2.80 GHz | 1 | 32 | 32 | 64 |
> | [General Purpose Intel Emerald Rapids (Standard Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids-v2.md) | Intel Emerald Rapids 8562Y+ | 2.80 GHz | 1 | 32 | 32 | 64 |
> | [General Purpose Intel Ice Lake](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i96-icelake.md) | Intel Ice Lake 6342 | 2.80 GHz | 2 | 24 | 48 | 96 |
>
> > [!NOTE]
> >
> > <sup>1</sup> vCPUs are logical CPU threads, not physical cores; in most CoreWeave CPU instances, vCPU count is typically 2× the physical core count due to SMT/hyper-threading.

> [tab] Instance details
>
> | Instance | CPU Model | RAM | Usable Storage<sup>1</sup> | Availability |
> | :- | :- | :- | :- | :- |
> | [High Performance AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hp-a96-genoa.md) | AMD Genoa 9274F | 768 GB | 7.68 TB | [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
> | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) | AMD Genoa 9454 | 1536 GB | 7.68 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-06A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [US-WEST-04A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) |
> | [General Purpose AMD Genoa (High Storage)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-l-a192-genoa.md) | AMD Genoa 9454 | 1536 GB | 30.72 TB | [US-EAST-08A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) |
> | [High Core AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384-genoa.md) | AMD Genoa 9654 | 1536 GB | 30.72 TB | [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
> | [High Core AMD Genoa (InfiniBand)](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384ib-genoa.md) | AMD Genoa 9654 | 1536 GB | 7.68 TB | [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
> | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) | AMD Turin 9655P | 1536 GB | 7.68 TB | [CA-EAST-01A](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [EU-SOUTH-03B](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-03b) [EU-SOUTH-04A](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-CENTRAL-06A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [US-CENTRAL-07A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [US-CENTRAL-09A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-06A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [US-EAST-13A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [US-EAST-14A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-14a) [US-EAST-15A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [US-WEST-09B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) [US-WEST-10A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |
> | [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) | AMD Turin 9655P | 1536 GB | 30.72 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-CENTRAL-09A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-15A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [US-EAST-17A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-17a) |
> | [General Purpose AMD Turin (Standard Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-v2.md) | AMD Turin 9655P | 768 GB | 7.68 TB | Contact sales for availability |
> | [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Intel Emerald Rapids 8562Y+ | 512 GB | 7.68 TB | [CA-EAST-01A](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [EU-SOUTH-03B](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-03b) [EU-SOUTH-04A](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [US-CENTRAL-06A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [US-CENTRAL-07A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-06A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [US-EAST-08A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [US-EAST-14A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-14a) [US-EAST-15A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [US-WEST-04A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [US-WEST-09B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) [US-WEST-10A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |
> | [General Purpose Intel Emerald Rapids (Standard Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids-v2.md) | Intel Emerald Rapids 8562Y+ | 256 GB | 7.68 TB | Contact sales for availability |
> | [General Purpose Intel Ice Lake](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i96-icelake.md) | Intel Ice Lake 6342 | 384 GB | 6.40 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) |
>
> > [!NOTE]
> >
> > <sup>1</sup> Total usable storage is shown. See each instance's details for its physical configuration.
