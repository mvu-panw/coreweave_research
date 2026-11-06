# Optimize CPU binding and NUMA affinity for multi-GPU jobs

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/cpu-binding-numa-affinity

# Optimize CPU binding and NUMA affinity for multi-GPU jobs

> Fix Slurm cyclic task distribution that causes NUMA misalignment and slows multi-GPU jobs on SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page shows how to align CPU cores, memory, and GPUs on the same Non-Uniform Memory Access (NUMA) node so multi-GPU jobs run at full speed on SUNK. It's for training engineers whose chip-to-chip (C2C) heavy workloads run slower than expected, and for administrators who set cluster-wide scheduling defaults.

## Symptoms

A multi-GPU job runs more slowly than expected, even though the GPUs are healthy and the network is fine. The slowdown is largest on workloads that move large amounts of data between GPUs and CPUs (C2C-heavy workloads). NUMA misalignment from Slurm's default task distribution may cause this.

## Why the default distribution is slow

Slurm's default CPU distribution within a node is cyclic, meaning it allocates CPUs round-robin across sockets. On the instance types on this page, each socket is one NUMA node, so consecutive ranks alternate between NUMA nodes. This breaks CPU-to-GPU affinity. A process can land on CPU cores in one NUMA node while its GPU is attached to a different NUMA node, forcing every memory access to cross the NUMA boundary. This cross-NUMA traffic can cause a substantial slowdown on C2C-heavy workloads.

The problem appears in code like this:

```python theme={"system"}
torch.cuda.set_device(int(os.environ['LOCAL_RANK']))
```

With cyclic distribution, `LOCAL_RANK` maps a process to a GPU on a sub-optimal NUMA node. On a node with two NUMA nodes and four ranks, the result looks like this:

| Distribution | Rank 0 | Rank 1 | Rank 2 | Rank 3 | Result |
| - | - | - | - | - | - |
| Cyclic (default) | NUMA 0 | NUMA 1 | NUMA 0 | NUMA 1 | Interleaved (misaligned) |
| Block | NUMA 0 | NUMA 0 | NUMA 1 | NUMA 1 | Contiguous (aligned) |

## Use block distribution per job

To allocate cores contiguously and align ranks with NUMA nodes, add this directive to your job script:

```bash theme={"system"}
#SBATCH --distribution=block:block
```

The first `block` distributes tasks across nodes contiguously. The second `block` distributes each task's allocated CPUs across sockets, filling one socket before moving to the next. An optional third field controls distribution across the cores within a socket. When you omit it, Slurm uses the second field's method. This is a per-job setting and doesn't change cluster-wide behavior.

## Make block distribution the cluster-wide default

Administrators can make block distribution the default for every job so users don't have to set `--distribution=block:block` per job. Add `CR_CORE_DEFAULT_DIST_BLOCK` to `SelectTypeParameters` in the Slurm configuration:

```text theme={"system"}
SelectTypeParameters = CR_CPU_MEMORY,CR_CORE_DEFAULT_DIST_BLOCK
```

Set this in `slurmConfig.SelectTypeParameters`. On SUNK Standard, set it in the Slurm chart's values. On SUNK Self-Service, set it under `spec.slurmConfig` on the `SunkCluster` resource, which passes custom key-value pairs through to the Slurm configuration. Keep the consumable-resource base parameter your cluster already uses and append `CR_CORE_DEFAULT_DIST_BLOCK`. On SUNK v7.3.0 and later, the default base parameter is `CR_CPU_MEMORY`. Confirm your cluster's current value with the following `scontrol` command before you change it. For more information, see the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) and the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference).

Verify the default took effect:

```bash theme={"system"}
# Confirm CR_CORE_DEFAULT_DIST_BLOCK is present.
scontrol show config | grep SelectTypeParameters
```

## Per-instance NUMA topology

The exact CPU-to-GPU mapping depends on the instance type. Always confirm the topology on the node rather than assuming it. The following table lists the mappings for CoreWeave's GPU instance types.

| Instance | GPUs per node | NUMA 0 | NUMA 1 |
| - | - | - | - |
| GB200 | 4 | GPU 0-1, cores 0-71 | GPU 2-3, cores 72-143 |
| GB300 | 4 | GPU 0-1, cores 0-71 | GPU 2-3, cores 72-143 |
| GH200 | 1 | GPU 0, cores 0-71 | None |
| H100 | 8 | GPU 0-3, Slurm cores 0-31 | GPU 4-7, Slurm cores 32-63 |
| H200 | 8 | GPU 0-3, Slurm cores 0-31 | GPU 4-7, Slurm cores 32-63 |
| B200 | 8 | GPU 0-3, Slurm cores 0-31 | GPU 4-7, Slurm cores 32-63 |
| B300 | 8 | GPU 0-3, Slurm cores 0-47 | GPU 4-7, Slurm cores 48-95 |

On the Grace instances (GB200, GB300, GH200), each core is a single hardware thread, so the core IDs above match the machine's own numbering. GH200 has one Grace CPU and one GPU, so there's nothing to misalign.

On the x86\_64 instances (H100, H200, B200, B300), each core has two hardware threads, and Slurm presents abstract core IDs numbered sequentially by socket. Those differ from the machine's physical thread numbering, which also varies between nodes of the same type. Some nodes enumerate socket 0 as the even-numbered threads, others as a contiguous range. Both describe the same physical cores. Reason about placement with the Slurm IDs and with the `CPU Affinity` column of `nvidia-smi topo -m`, not with physical thread IDs copied from another node. The B300 row's GPU index order hasn't been confirmed on a node, so check it the same way before you rely on it.

To read the topology directly on a node:

```bash theme={"system"}
# Show the GPU-to-NUMA topology from inside a Slurm job.
nvidia-smi topo -m

# Show NUMA nodes and their CPU lists from the node directly.
numactl --hardware
cat /sys/devices/system/node/node0/cpulist
cat /sys/devices/system/node/node1/cpulist
```

On Grace instances, the kernel also exposes GPU memory as extra NUMA nodes with no CPUs, so `numactl --hardware` lists more than two nodes and the `NUMA Affinity` column of `nvidia-smi topo -m` can show IDs above 1. Use the `CPU Affinity` column.

## Verify the binding worked

After applying block distribution, confirm that processes and their memory landed on the expected NUMA node:

```bash theme={"system"}
# Show a process's CPU affinity mask.
taskset -p [PID]

# Show where a process's memory is allocated across NUMA nodes.
numastat -p [PID]
```

In `numastat` output, the process's heap and private memory should be predominantly on the NUMA node that owns its GPU. In Python, you can also read the affinity from inside the process with `os.sched_getaffinity(0)`.

When you cross-check core counts, `nproc` can underreport. If `OMP_NUM_THREADS` is set, `nproc` returns that value instead of the real CPU count, capped by `OMP_THREAD_LIMIT` when that's also set. Training frameworks and job environments commonly set `OMP_NUM_THREADS`, so inside an `srun` session `nproc` may report fewer CPUs than the step can run on. Check the job's allocation and the step's CPUs directly:

```bash theme={"system"}
# Show the CPUs Slurm allocated to the job.
scontrol show job $SLURM_JOB_ID | grep -E 'ReqTRES|AllocTRES'

# Show the CPUs the current step can run on.
grep Cpus_allowed_list /proc/self/status
```

`AllocTRES` reports the job's allocation, not the step's CPU binding. A step can be bound to fewer CPUs than the job holds, so use `Cpus_allowed_list` to see what the step can use.

## Memory binding follows the CPU

To prefer local NUMA memory, you can add `--mem-bind=local`:

```bash theme={"system"}
#SBATCH --mem-bind=local
```

In practice this is largely redundant once CPU affinity is correct. Slurm doesn't bind memory unless you ask it to, but the Linux kernel's default policy allocates each page on the NUMA node of the CPU that first touches it. Once a task's CPUs are pinned to one NUMA node, its memory lands there too, and `numastat` shows it. Fix the CPU distribution first. Memory binding is secondary.

On Grace-based instances (GB200, GB300, GH200), the Grace CPU and GPU share a high-bandwidth NVLink-C2C link with unified memory. On GB200 and GB300, the same rule applies. Align CPU and GPU on the same NUMA node first. GH200 has a single Grace CPU, so all of its cores share one NUMA node and this misalignment can't occur. For Grace-specific architecture and build considerations, see [Run jobs on Grace CPU instances](https://docs.coreweave.com/products/sunk/run_workloads/run-jobs-on-grace-cpu.md).

## What this is not

The following points clarify what NUMA alignment does and doesn't cover:

* **This isn't GPU binding.** CPU and NUMA alignment is separate from `--gpu-bind`, which controls which GPU a task receives. For GPU binding, see [Manage resource binding with task plugins](https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins.md).
* **Block distribution isn't a hardware fix.** It corrects a software scheduling default. It doesn't change the node's physical topology.
* **`--mem-bind=local` isn't a substitute for correct CPU distribution.** Fix the distribution first.

## Related pages

* [Manage resource binding with task plugins](https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins.md): cgroup task plugin and GPU binding.
* [Run jobs on Grace CPU instances](https://docs.coreweave.com/products/sunk/run_workloads/run-jobs-on-grace-cpu.md): Grace architecture and build guidance.
* [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md): rack-level placement on NVL72. Slurm's topology Blocks are groups of nodes and are unrelated to the block distribution described on this page.
