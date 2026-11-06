# Topology and block scheduling in Slurm

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling

# Topology and block scheduling in Slurm

> Configure topology and block scheduling in Slurm for optimized job placement on NVLink-connected GPU systems

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

CoreWeave's [GB200 and GB300 NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md) use NVIDIA's Grace Blackwell Superchip and NVLink Switch System, integrated within a single rack. Vera Rubin instances pair NVIDIA Vera Arm CPUs with Rubin GPUs in the same rack-scale NVLink design. The NVLink fabric enables direct memory access between GPUs, which allows high-speed communication and efficient data sharing.

To fully take advantage of the NVL72 architecture, CoreWeave recommends the Topology/Block Plugin with Slurm. This plugin improves job scheduling because it places nodes from the same job within the same rack whenever possible, which maximizes NVLink fabric performance. Optimized job placement within the NVLink domain increases resource efficiency and enhances GPU communication, critical for large-scale distributed workloads where minimal processing time is essential.

This guide is for SUNK cluster operators and users submitting jobs to NVL72-powered systems. It explains the concepts behind the Topology/Block Plugin, shows example job placement scenarios, describes how to identify idle nodes available for scheduling, and works through why a job that uses `--segment` can be rejected.

## Concepts

The Slurm Topology/Block Plugin adds new features for managing job placement within NVLink domains. Key concepts include **Blocks**, **Segments**, and the `--exclusive=topo` option.

Some of the behavior on this page depends on the Slurm version. By default, SUNK 8.0 and later run Slurm 25.11, and SUNK 7.x runs Slurm 25.05. For the full mapping, see [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md).

When SUNK auto-generates the topology file, it defines Blocks based on the `ds.coreweave.com/nvlink.domain` label on CKS Nodes. For [GB200, GB300, and Vera Rubin NVL72-powered nodes](https://docs.coreweave.com/platform/instances/nvl72.md), this label is a globally unique rack identifier, for example, `DH4-016-US-EAST-02A`.

In clusters with both NVLink-enabled multi-node systems and standard nodes, SUNK creates a topology.conf file that includes Block and switch definitions. This configuration doesn't affect behavior unless you explicitly enable the Topology/Block Plugin, which ensures safe integration and runtime flexibility.

### Blocks

A **Block** is a group of nodes in the same Slurm cluster, defined in the `topology.conf` file. SUNK automatically generates this file, so you don't need to create or manage it manually. It specifies which nodes belong to each Block and defines the **Block size**, the number of nodes in a Block.

Each Block has a unique ID and cannot overlap with others. CoreWeave dynamically updates the topology configuration to reflect changes in node availability. By default, each [GB200, GB300, or Vera Rubin NVL72-based](https://docs.coreweave.com/platform/instances/nvl72.md) system corresponds to a Block containing 18 nodes in the same NVLink domain. A node that is drained or down stays in the Block, so the Block size is unchanged and the Block simply has fewer nodes available to schedule. Run `scontrol show topology` to see the current `BlockSize` and node list for each Block.

### Segments

A Segment is a set of nodes within a Block that Slurm allocates together. Segments reduce resource fragmentation because they keep allocations intact. If a job spans multiple Blocks, Slurm schedules equal-sized Segments in each Block. A Block can hold multiple Segments if space allows.

Whether a Segment can be larger than a Block depends on the Slurm version. On SUNK 7.x and earlier, Slurm rejects a segment size larger than the Block size. SUNK 8.0 and later accept the request, but SUNK generates a topology with one Block size. Slurm has no larger Block for an oversized Segment, so it places the Segment anywhere in the cluster. The job then loses the NVLink locality that Segments provide. Keep the segment size at or below the Block size on every version.

If you don't set a segment size, Slurm applies no segment constraint and places the job by its total node count. A job no larger than one Block must fit within a single Block. A larger job is placed anywhere in the cluster, without NVLink locality. This is true on every version.

The following are best practices when configuring segment size:

* When you select a segment size for your job, default to `--segment=1`. This makes your job more flexible because it can run on any available nodes across all Blocks, which improves scheduling efficiency.

* On GB200 NVL72 systems, don't use a segment size larger than `--segment=16`. This gives a buffer for nodes to fail on a rack before it becomes unusable for your job.

* On GB200 NVL72 systems, balance segment sizes across jobs on your cluster with factors of 16 (8, 4, 2, 1). This minimizes the number of idle nodes on each rack left unavailable to your jobs.

* Always set the segment size explicitly. Without one, Slurm places the job by its total node count instead of by Segment. A small segment size constrains scheduling less.

For gang-scheduled Kubernetes workloads that the SUNK Pod Scheduler places, set the segment size with the `sunk.coreweave.com/segment` annotation on the Pod templates instead of `--segment`. See [Configure topology segments](https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling.md#optional-configure-topology-segments).

All examples in this guide follow these best practices by specifying the segment size to ensure reliable scheduling.

### Segment placement options in SUNK 8.0 and later

Slurm 25.11, which ships with SUNK 8.0, added two options that control how Slurm distributes a job's Segments across Blocks. Both require the Topology/Block Plugin, and both work with `srun`, `sbatch`, and `salloc`.

The [`--spread-segments`](https://slurm.schedmd.com/srun.html#OPT_spread-segments) option places each Segment on a separate Block. After Slurm places a Segment, it removes that Block from the candidates for the job's remaining Segments. A job with four Segments therefore lands on four different racks. Use this option to limit how much of a job a single rack failure can disrupt:

```bash theme={"system"}
srun --nodes=32 --segment=8 --spread-segments ...
```

The [`--consolidate-segments`](https://slurm.schedmd.com/srun.html#OPT_consolidate-segments) option places all of a job's Segments in one higher-level Block that aggregates several Blocks. That requires the topology configuration to define aggregate Block sizes, and SUNK generates a topology with one Block size. On a SUNK cluster, this option therefore has no aggregate Block to consolidate into once a job is larger than one rack.

For a job that requests a segment size, Slurm sets `SLURM_JOB_SEGMENT_SIZE` in the job environment to the segment size used for the allocation. Slurm doesn't set the variable for jobs that don't request a segment size.

To confirm which options a job uses, run `scontrol show job [JOB-ID]` and look for the `SegmentSize` field. The same line reports `SpreadSegments=Yes` and `ConsolidateSegments=Yes` when those options are set. A job that requested no segment size has no `SegmentSize` field.

### Exclusive option

The `--exclusive=topo` option ensures that only the job being submitted runs in a Block. The job won't share a Block with any other job, and no new jobs can be placed there until the original job completes. Unused nodes in the Block remain idle. Use this option for benchmarking or to avoid resource competition.

When `srun --exclusive` starts a new job and you set `--ntasks`, the job gets the whole node, but the job step gets only the CPUs those tasks request. A step started this way with `--ntasks=1` and no `--cpus-per-task` runs on a single core. See [Why does my exclusive Slurm job use only one CPU core?](https://docs.coreweave.com/support/sunk/articles/why-does-my-exclusive-slurm-job-use-only-one-cpu-core).

> [!WARNING]
>
> Using `--exclusive=topo` can result in idle nodes if your job doesn't fill the entire Block. To avoid wasting resources, apply this option only when needed, such as for benchmarking or when your workload requires exclusive access to a Block without sharing with other jobs.

## Example scenarios

The following scenarios show how to use the Topology/Block Plugin to optimize job placement within [GB200, GB300, and Vera Rubin NVL72-based systems](https://docs.coreweave.com/platform/instances/nvl72.md). Use them as reference patterns when sizing your own jobs and choosing segment sizes. Each diagram shows multiple 18-node NVL72 systems (Blocks). Node colors represent status:

* **Green**: nodes running the requested job (light green indicates a second job or Segment)
* **Gray**: Unavailable: drained, down, or running unrelated jobs
* **White**: Idle

### A job that fits in a Block

A job requests **10** nodes, which is less than the Block size. The segment size is set to **1**, following [best practice](#segments).

```bash theme={"system"}
srun --nodes=10 --segment=1 ...
```

The plugin allocates **10** nodes from Block 1. The rest of Block 1 and Block 2 remain idle.

![Job requests 10 nodes.](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-1.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=2d88f4c484546355bffbf28ffb0710e6)

Job requests 10 nodes.

### Jobs larger than the Block size

A job requests **20** nodes, which exceeds the Block size of **18**. The segment size is set to **1**, following [best practice](#segments).

```bash theme={"system"}
srun --nodes=20 --segment=1 ...
```

Two nodes are unavailable in Block 1, so the plugin allocates **16** nodes from Block 1 and **4** nodes from Block 2. The rest of Block 2 remains idle.

![Job requests 20 nodes](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-2.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=b9e89538b435ffa109c184aa08e30346)

Job requests 20 nodes

### Two jobs in a single Block

You submit two jobs. The first requests **8** nodes, and the second requests **4**. The segment size is set to **1** for both jobs, following [best practice](#segments).

```bash theme={"system"}
srun --nodes=8 --segment=1 ... && srun --nodes=4 --segment=1 ...
```

The plugin places both jobs in Block 1. The rest of Block 1 and Block 2 remain idle.

![Two jobs can fit in a single Block](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-3.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=03ab4146195b0beb9fe951032ba9af1b)

Two jobs can fit in a single Block

### Realistic training example: A job with two Segments

A job requests **32** nodes, divided into two Segments of **16** nodes each.

```bash theme={"system"}
srun --nodes=32 --segment=16 ...
```

The plugin places the first Segment in Block 1 and the second Segment in Block 2.

Two nodes are left idle in Block 1 because Segments cannot span Blocks.

![A job with two Segments](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-5.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=07289202c8c8539ab682e15a60475337)

A job with two Segments

### Exclusive jobs

A job requests **16** nodes with the `--exclusive=topo` option. The segment size is set to **1**, following [best practice](#segments).

```bash theme={"system"}
srun --nodes=16 --segment=1 --exclusive=topo ...
```

The plugin places the job in Block 2 because `--exclusive=topo` prevents it from running in Block 1 while a competing job (light green) is active. The rest of Block 2 remains idle, and no other jobs can run there until this job completes.

![Exclusive jobs](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-6.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=94154fc9dde02dec6b915809b929ecdb)

Exclusive jobs

### Combining Segments and the exclusive option

A job requests **16** nodes, divided into two **8**-node Segments, using `--exclusive=topo`.

```bash theme={"system"}
srun --nodes=16 --segment=8 --exclusive=topo ...
```

The plugin places both Segments (green and light green) in Block 2 because Block 1 is unavailable because of an existing job (dark green). The rest of Block 2 remains idle, and no other jobs can run there until both job Segments complete.

![Combining Segments and Exclusive jobs](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/topology-block-7.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=6590df6e3046e2e90de4dfa732cf521a)

Combining Segments and Exclusive jobs

## Identify idle nodes in a Block

Before you submit a job, you can check how many nodes are currently idle in each Block to choose a segment size that schedules promptly. Use the script at `/usr/share/sunk/bin/segment-calc.sh` on the Slurm login node to check for idle nodes within a Block. By default, it reports idle nodes per topology Block. You can optionally provide the `--segment N` argument to report only those Blocks with at least `N` idle nodes available.

### Example usage

```bash theme={"system"}
./segment-calc.sh --segment 6
```

Example output:

```text theme={"system"}
Block                                 IDLE / SIZE
----------------------------------- ------   -----
block_DH4-004-US-EAST-02A                8 / 18
block_DH4-012-US-EAST-02A                8 / 18
block_DH4-013-US-EAST-02A                8 / 18
block_DH4-017-US-EAST-02A                8 / 18
block_DH4-043-US-EAST-02A               18 / 18

Blocks with ≥ 6 idle nodes : 5
Whole segments schedulable             : 7
Total nodes those segments consume     : 42
```

This output shows the Blocks with at least 6 idle nodes, along with the total number of whole segments Slurm can schedule and the total nodes those segments would consume.

## Troubleshoot "Requested node configuration is not available" with `--segment`

A job that uses `--segment`, often combined with `--exclude`, can be rejected at submission or stay `PENDING` with the reason `Requested node configuration is not available`. A job whose segment math can't be satisfied gets a different message, `Requested topology configuration is not available`, so check for both strings. Either way, the usual cause is the request itself rather than a cluster that's out of capacity.

Work through these causes in order:

1. **You combined `--segment` with `--nodelist`.** On SUNK 7.x and earlier, Slurm rejects a job that requests both whenever the job has more than one Segment. On SUNK 8.0 and later, Slurm supports the combination as long as the requested node count is no larger than the number of unique nodes in the node list. On either version, you can steer a job toward particular hardware with `--constraint` instead of a node list. See the `--segment` entry in the [Slurm `srun` documentation](https://slurm.schedmd.com/srun.html#OPT_segment).

2. **You requested GPUs with `--gpus-per-task`.** `--gpus-per-task` combined with `--segment` is rejected even when enough nodes are idle. Use `--gpus-per-node` instead. To confirm this is the cause, submit the same job three ways with `--test-only`: with no GPU flag, with `--gpus-per-node`, and with `--gpus-per-task`. Only the last one fails.

3. **The segment size is larger than the available nodes in any single Block.** A drained or down node still counts toward the Block size, so drains don't change whether Slurm accepts the segment size. They reduce how many nodes each Block has available. If no Block has as many available nodes as your segment size, the job stays `PENDING` until a Block has room. On SUNK 7.x and earlier, a segment size larger than the Block size itself is rejected at submission, as described in [Segments](#segments). Check how many nodes are idle per Block with `/usr/share/sunk/bin/segment-calc.sh` as shown in [Identify idle nodes in a Block](#identify-idle-nodes-in-a-block), then choose a segment size that fits.

4. **`--exclude` removed nodes a Block needs to reach the segment size.** Excluding specific nodes can drop a Block below the requested segment size, leaving no Block able to satisfy the request. Relax or remove the `--exclude` list, or lower the segment size to fit the remaining nodes. If you need nodes kept out of scheduling for longer, ask an administrator for a reservation or a drain, which works with `--segment` where `--exclude` struggles.

5. **The total node count isn't divisible by the segment size.** Slurm applies this rule to every job that sets a segment size, even when the job fits in a single Block. Make sure `--nodes` is a multiple of `--segment`.

6. **You omitted the segment size.** Without `--segment`, Slurm places the job by its total node count, so a job no larger than one Block needs a single Block with room for every node it requests. See [Segments](#segments). Always set the segment size explicitly.

A request that started yesterday can wait today if nodes in the target Block were drained, because a drained node still counts toward the Block size but can't run your job.

## More information

To learn more about the Topology/Block Plugin for Slurm, including configuration options and advanced usage, see the [Slurm documentation](https://slurm.schedmd.com/topology.html). For help configuring the plugin on your [NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md), contact CoreWeave Support.
