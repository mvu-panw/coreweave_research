# About GPU instances

Source: https://docs.coreweave.com/platform/instances/gpu-instances

# About GPU instances

> Compare CoreWeave GPU instance types by GPU count, GPU memory, vCPUs, RAM, and storage

## GPU comparison

Use the following table to compare the number of GPUs, RAM, and storage installed in CoreWeave's GPU compute instances. Select an instance type to view full specifications.

| Instance | GPUs | GPU RAM | vCPUs | RAM | Usable Storage<sup>1</sup> | Availability |
| :- | :- | :- | :- | :- | :- | :- |
| [Vera Rubin NVL72 Spectrum-X RoCE](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) | 4 | Up to 288 GB HBM4 | 352 | Up to 1.5 TB LPDDR5 | 30.72 TB | [US-CENTRAL-09A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) |
| [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) | 4 | 279 GB | 144 | 960 GB | 30.72 TB | [CA-EAST-01A](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [US-CENTRAL-07A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [US-CENTRAL-09A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-09a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) |
| [GB300 NVL72 Spectrum-X RoCE](https://docs.coreweave.com/platform/instances/gpu/gb300-4x-e.md) | 4 | 279 GB | 144 | 960 GB | 30.72 TB | - |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) | 4 | 186 GB | 144 | 960 GB | 15.36 TB | [CA-EAST-01A](https://docs.coreweave.com/platform/regions/ca-east.md#ca-east-01a) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-08A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [US-EAST-13A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) |
| [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) | 8 | 270 GB | 192 | 4096 GB | 30.72 TB | [US-CENTRAL-06A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [US-EAST-13A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [US-WEST-10A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) | 8 | 180 GB | 128 | 2048 GB | 30.72 TB | [EU-SOUTH-04A](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [US-CENTRAL-07A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-07a) [US-EAST-13A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [US-EAST-15A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) [US-WEST-09B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) |
| [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) | 8 | 141 GB | 128 | 2048 GB | 30.72 TB | [EU-SOUTH-03B](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-03b) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-08A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-08a) [US-WEST-04A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | 8 | 80 GB | 128 | 2048 GB | 30.72 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-CENTRAL-06A](https://docs.coreweave.com/platform/regions/us-central.md#us-central-06a) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-06A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [US-WEST-02B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-02b) [US-WEST-04A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [US-WEST-09B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) |
| [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | 8 | 96 GB | 128 | 1024 GB | 7.68 TB | [EU-SOUTH-04A](https://docs.coreweave.com/platform/regions/eu-south.md#eu-south-04a) [US-EAST-01A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-01a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) [US-EAST-06A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-06a) [US-EAST-13A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-13a) [US-EAST-14A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-14a) [US-WEST-01A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-01a) [US-WEST-04A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-04a) [US-WEST-09B](https://docs.coreweave.com/platform/regions/us-west.md#us-west-09b) [US-WEST-10A](https://docs.coreweave.com/platform/regions/us-west.md#us-west-10a) |
| [RTX PRO 6000 Blackwell Server Edition (Standard Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x-v2.md) | 8 | 96 GB | 128 | 512 GB | 7.68 TB | [US-EAST-15A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-15a) |
| [L40S](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40s-i128.md) | 8 | 48 GB | 128 | 1024 GB | 7.68 TB | [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
| [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) | 8 | 48 GB | 128 | 1024 GB | 7.68 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-EAST-02A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-02a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
| [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) | 1 | 96 GB | 72 | 480 GB | 7.68 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |
| [A100](https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128.md) | 8 | 80 GB | 128 | 2048 GB | 7.68 TB | [RNO2A](https://docs.coreweave.com/platform/regions/us-west.md#rno2a) [US-EAST-04A](https://docs.coreweave.com/platform/regions/us-east.md#us-east-04a) |

> [!NOTE]
>
> <sup>1</sup> Total usable storage is shown. See each instance's details for its physical configuration.

## Choose the right GPU for your workload

Not sure which GPU type fits your model? See [Select an instance](https://docs.coreweave.com/platform/instances/selecting-an-instance.md) for a decision guide that covers:

* GPU memory estimation by model size and precision (FP16, INT8, INT4)
* How inference memory overhead compares with training and fine-tuning
* Choosing between NVLink and InfiniBand for multi-GPU workloads
* Example models that fit each GPU type

To check which instances are offered in each region, see the [Instance availability matrix](https://docs.coreweave.com/platform/instances/availability-matrix.md).
