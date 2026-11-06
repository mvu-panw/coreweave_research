# Avoid stranding GPUs with CPU and memory requests

Source: https://docs.coreweave.com/products/sunk/run_workloads/avoid-stranded-gpus

# Avoid stranding GPUs with CPU and memory requests

> Size --cpus-per-task and --mem-per-cpu so Slurm jobs use every GPU on a SUNK node instead of stranding one.

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page is for Slurm users who submit GPU jobs on SUNK and find that a job uses fewer GPUs per Node than the Node has, for example, 7 of 8. It explains how per-task CPU and memory requests determine how many GPUs fit on a Node, why an oversized `--mem-per-cpu` or `--cpus-per-task` value strands a GPU, and how to size your requests so that every GPU is usable.

## How per-task requests cap GPUs per Node

A GPU job places one task per GPU when you request one GPU per task (for example, `--gres=gpu:1` array tasks, or `--gpus-per-task=1`). Slurm packs tasks onto a Node only while both CPU and memory are available. The Node fits one task per GPU only if the total CPU and memory those tasks request both fit within the Node's allocatable resources. If either runs out first, Slurm places fewer tasks, and the remaining GPUs sit idle.

The memory that Slurm can allocate is smaller than the Node's nominal SKU specification. On SUNK, the `slurmd` container runs inside Kubernetes, and CoreWeave reserves memory for the operating system, kubelet, and DaemonSets. SUNK reflects this by advertising a reduced `RealMemory` for the Node, lower than the raw hardware total. The CPU count (`CPUTot`) stays at the Node's full processor count. Size your requests against the live values Slurm reports, not the SKU datasheet.

## The memory-per-CPU ceiling

Each Node has a memory-per-CPU ceiling: its usable memory (`RealMemory`) divided by its CPU count (`CPUTot`). SUNK derives the partition's `DefMemPerCPU` value (the default memory assigned to each allocated CPU when a job doesn't set `--mem-per-cpu`) from this same ratio. A partition can also set `MaxMemPerNode`, which caps the memory any one job may use on a Node, but the ceiling that governs request sizing is `RealMemory / CPUTot`.

A job's memory request scales with the CPUs it's allocated, because Slurm reserves `--mem-per-cpu` for every CPU in the allocation. When you set `--mem-per-cpu` above the ceiling, a job that spans many CPUs requests more memory than the Node has. For an array that places one task per GPU, the tasks then can't all fit at once, so Slurm places fewer tasks than the Node has GPUs and leaves the remaining GPUs idle.

The same oversized request can also spread a single job across more Nodes than its GPU count requires. A GPU job's implicit memory request is its GPU count multiplied by the partition's `DefCpuPerGPU` and `DefMemPerCPU` (`nGPUs * DefCpuPerGPU * DefMemPerCPU`). When that product exceeds one Node's `RealMemory`, Slurm splits the job across multiple Nodes even though each Node has enough GPUs.

## Example stranded GPU

This example shows how an oversized `--mem-per-cpu` crosses the per-CPU ceiling and strands a GPU.

Consider a Node with 128 CPUs and 8 GPUs whose per-CPU memory ceiling (`RealMemory / CPUTot`) is about 15840 MB. A user submits an array job that places one task on each GPU:

```bash theme={"system"}
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=15
#SBATCH --mem-per-cpu=16G
#SBATCH --array=0-256
```

`--mem-per-cpu=16G` is 16384 MB per CPU, above the 15840 MB ceiling. When a request crosses this ceiling, a one-task-per-GPU array reserves more memory across its tasks than the Node has, so Slurm can't place a task on every GPU and leaves one or more idle. In the reported case, the array used only 7 of the 8 GPUs on each Node.

Two changes restore full GPU usage. Reducing `--mem-per-cpu` to 15840 MB or below brings each CPU's request within the ceiling. Reducing `--cpus-per-task` (the reported case used 12) lowers each task's total memory so all eight tasks fit. The exact number of GPUs a Node loses depends on its live `RealMemory` and the partition's `DefCpuPerGPU`, so confirm both with `scontrol`.

## Check your Node and partition limits

Before sizing requests, find the usable resources for your Node and partition.

Check a Node's allocatable CPU and memory. Replace `[NODE]` with the Node name:

```bash theme={"system"}
scontrol show node [NODE] | grep -E "CPUTot|RealMemory"
```

Check the partition's per-CPU and per-GPU defaults. Replace `[PARTITION]` with the partition name:

```bash theme={"system"}
scontrol show partition [PARTITION] | grep -E "DefMemPerCPU|DefCpuPerGPU|MaxMemPerNode"
```

The maximum memory per CPU you can request without over-committing the Node is `RealMemory` divided by `CPUTot`, rounded down.

## Size requests to use every GPU

Use the values from the previous section to choose `--cpus-per-task` and `--mem-per-cpu`:

* **Keep `--mem-per-cpu` at or below the ceiling.** Set it to no more than `floor(RealMemory / CPUTot)`. Requesting more over-commits the Node's memory and can strand GPUs.
* **Keep the total CPU footprint within usable CPUs.** Ensure `--cpus-per-task` multiplied by the number of GPUs per Node stays within `CPUTot`, with headroom for system overhead.
* **Request a fixed total memory per task when that's more convenient.** Setting `--mem` (rather than `--mem-per-cpu`) requests a fixed amount per task that doesn't scale with the CPUs Slurm allocates.

Watch for these symptoms of oversized requests:

* A job runs but uses fewer GPUs per Node than expected. This failure is silent, with no error message.
* A job fails to schedule with `Requested node configuration is not available`.
* A job spreads across more Nodes than its GPU count requires.

> [!WARNING]
>
> Don't size requests to consume every CPU and byte of memory on a Node. Topology-aware and block scheduling, the `slurmd` container, and SUNK operator system Pods all need resources to run.

On SUNK, the operator can derive partition defaults such as `DefMemPerCPU` and `DefCpuPerGPU` automatically from each NodeSet's configured resources rather than from the nominal SKU specifications. Always read the live values with `scontrol`, as shown in [Check your Node and partition limits](#check-your-node-and-partition-limits), rather than assuming the hardware datasheet numbers.
