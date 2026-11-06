# Manage resource binding with task plugins

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins

# Manage resource binding with task plugins

> Optimize performance by binding tasks to common resources within a node

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Using task plugins, you can set Slurm parameters to bind a task to specific subsets of resources on a node, like CPU cores or GPUs. You can optimize the performance of a task in Slurm by selecting resources within a common Non-Uniform Memory Access (NUMA) node. Resources can access memory within their own NUMA node much more quickly than memory in a separate NUMA node, which can reduce data transfer latency and improve job performance.

This guide explains how to manage resource binding in SUNK with task plugins. It's intended for cluster administrators who configure Slurm and for users who submit jobs that benefit from CPU or GPU affinity. The following sections describe how to enable resource binding, configure the task cgroup plugin, and bind tasks to GPUs and CPU cores.

## Enable resource binding

SUNK enables resource binding by default. The operator sets `TaskPlugin` to `task/cgroup,task/affinity`, so you don't need to turn it on. Confirm the value on your cluster with the following command:

```bash theme={"system"}
scontrol show config | grep TaskPlugin
```

To override the default, set `TaskPlugin` as a top-level key under `slurmConfig`. On SUNK Standard, set it in the Slurm chart's values. On SUNK Self-Service, set it under `spec.slurmConfig` on the `SunkCluster` resource:

```yaml theme={"system"}
slurmConfig:
  TaskPlugin: "task/cgroup,task/affinity"
```

For the full list of operator defaults, see [`slurmConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) in the Slurm parameter reference.

The `task/affinity` and `task/cgroup` plugins work together to optimize resource allocations in the SUNK cluster.

* The `task/affinity` plugin controls how processes bind to CPU resources on a Compute node.
* The `task/cgroup` plugin uses the cgroup filesystem and its controllers to enforce the resource limits and binding policies specified by Slurm.

## Configure the task cgroup plugin

> [!WARNING]
>
> **cgroup v1 is deprecated in Slurm 25.05 and later**
>
> SUNK v7.0.0 upgrades to Slurm 25.05, where the cgroup v1 plugin is deprecated. Slurm does not add new cgroup v1 features and plans to remove cgroup v1 support in a future release. For details, see [Control Group in Slurm](https://slurm.schedmd.com/cgroups.html#overview) in the SchedMD documentation.
>
> `CgroupPlugin` must be set to `cgroup/v2` in `slurmConfig.cgroupConfig`, as shown in the following example. CKS clusters on Kubernetes v1.35 and later require cgroup v2 on all nodes. See [Cluster components](https://docs.coreweave.com/products/cks/reference/cluster-components.md) for cgroup version requirements by Kubernetes version.

Slurm enforces those bindings through Linux cgroups, which constrain the CPU, GPU, and memory available to each task. SUNK exposes the `cgroup.conf` settings through [`slurmConfig.cgroupConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig).

SUNK configures cgroups by default. Confirm that both of the following are in place on your cluster:

1. `TaskPlugin` includes `task/cgroup`, as shown in the [Enable resource binding](#enable-resource-binding) section.
2. `ProctrackType` is set to `proctrack/cgroup` as a top-level key under `slurmConfig`. If this parameter isn't set correctly, Slurm doesn't apply your Linux cgroups settings.

The operator sets the following cgroup defaults under the nested `cgroupConfig` key:

```yaml theme={"system"}
slurmConfig:
  cgroupConfig:
    CgroupPlugin: cgroup/v2
    ConstrainCores: "yes"
    ConstrainDevices: "yes"
    ConstrainRAMSpace: "yes"
    IgnoreSystemd: "yes"
```

The `Constrain` settings enforce binding and limits for different resources, as follows:

* `ConstrainCores` enforces CPU binding.
* `ConstrainDevices` enforces limits on GPU devices.
* `ConstrainRAMSpace` enforces memory limits.

## Bind tasks to GPUs

Once the task plugins and cgroup configuration are in place, you can control how Slurm assigns individual jobs to GPUs. Use the `--gpu-bind` parameter in your job script's `#SBATCH` directives to manage how Slurm assigns tasks to GPUs:

```bash theme={"system"}
#SBATCH --gpu-bind=single:1,verbose
```

To print information about which GPU resources each task binds to, add the `verbose` option to your other binding options, separated by a comma. This can be helpful when debugging or checking your binding strategy.

> [!TIP]
>
> **Performance optimization**
>
> To optimize performance, use the `--gpu-bind=single:1` option when starting your Slurm job. This binds each task to one GPU, chosen from the GPUs whose socket affinity matches the task's allocated CPU cores. Matching CPU and GPU NUMA affinities is important for performance. If you don't use the `--gpu-bind` parameter, Slurm could assign your task a GPU with a different NUMA affinity than the assigned CPU cores, which could lead to suboptimal performance. GPU binding doesn't change how Slurm spreads a job's CPU cores across NUMA nodes. For that, see [Align tasks with NUMA nodes for multi-GPU jobs](#align-tasks-with-numa-nodes-for-multi-gpu-jobs).

The `--gpu-bind` parameter supports multiple options, including:

| Option | Meaning |
| - | - |
| `none` | No GPU binding. Slurm doesn't enforce any specific binding between tasks and GPUs. This option may be suitable if your application handles GPU selection internally. |
| `single:<tasks_per_gres>` | Binds each task to one GPU, chosen from the GPUs whose socket affinity matches the task's allocated CPU cores. `<tasks_per_gres>` sets how many tasks share each GPU. The first `<tasks_per_gres>` tasks bind to the first matching GPU, the next `<tasks_per_gres>` to the second, and so on. |
| `closest` | Attempts to bind a task to the GPUs "closest" to the CPU cores the task runs on, based on the system topology. This setting may assign multiple GPUs to a task if they share the same NUMA node, regardless of what you've specified in the `--gpus-per-task` setting. |

For a complete list of available `--gpu-bind` options, see [SchedMD's Slurm documentation](https://slurm.schedmd.com/srun.html#OPT_gpu-bind).

### Run two jobs on one GPU node

Slurm can run multiple jobs on the same node when each job requests only the resources it needs. This example submits two jobs to one node with at least two available GPUs. Each job requests one GPU, one CPU, and 1 GB of memory. The node's remaining resources stay available to other jobs.

To submit the jobs, complete these steps:

1. Create a job script named `gpu-share.sh`:

   ```bash theme={"system"}
   #!/bin/bash
   #SBATCH --nodes=1
   #SBATCH --ntasks=1
   #SBATCH --gpus=1
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=1G
   #SBATCH --time=00:05:00
   #SBATCH --output=gpu-share-%j.out

   echo "Job ${SLURM_JOB_ID} is running on ${SLURMD_NODENAME}"
   echo "SLURM_JOB_GPUS=${SLURM_JOB_GPUS}"
   echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}"
   sleep 300
   ```

2. Submit the script twice to the same node. Replace `[NODE-NAME]` with the name of a node that has at least two available GPUs:

   ```bash theme={"system"}
   job_one=$(sbatch --parsable --job-name=gpu-share-one --nodelist=[NODE-NAME] gpu-share.sh)
   job_two=$(sbatch --parsable --job-name=gpu-share-two --nodelist=[NODE-NAME] gpu-share.sh)

   squeue --jobs="${job_one},${job_two}" --format="%.18i %.20j %.8T %.20N"
   ```

After both jobs start, `squeue` shows that both jobs run on the same node. Slurm's `gres/gpu` allocation sets `SLURM_JOB_GPUS` in each job's environment to the physical GPU it holds. The job output files, `gpu-share-${job_one}.out` and `gpu-share-${job_two}.out`, show a different `SLURM_JOB_GPUS` value for each job, confirming that Slurm assigned them separate GPUs.

`CUDA_VISIBLE_DEVICES` isn't a reliable way to tell the jobs apart. With `ConstrainDevices=yes`, Linux cgroups restrict each job to only its allocated GPU device file, and Slurm remaps `CUDA_VISIBLE_DEVICES` to a job-local index that starts at `0`. Because each job in this example holds a single GPU, both output files show `CUDA_VISIBLE_DEVICES=0`, even though the jobs run on different physical GPUs. Without `ConstrainDevices=yes`, a job can access every GPU on the node instead of only the one it was assigned, so `CUDA_VISIBLE_DEVICES` reports the real GPU index but doesn't restrict access to it. Either way, use `SLURM_JOB_GPUS` or `scontrol show job -d [JOB-ID]` to find a job's actual physical GPU.

Replace `[JOB-ID]` with either job ID captured in `job_one` or `job_two` by the submission commands.

## Bind tasks to CPU cores

In addition to GPU binding, you can pin tasks to specific CPU cores to improve cache locality and reduce contention. Use the `--cpu-bind` parameter in your job script's `#SBATCH` directives to control which CPU cores your tasks bind to. For example:

```bash theme={"system"}
#SBATCH --cpu-bind=map_cpu:1,verbose
```

To print information about which CPU resources each task binds to, add the `verbose` option to your other binding options, separated by a comma. This can be helpful when debugging or checking your binding strategy.

The `--cpu-bind` parameter supports multiple options, including:

| Option | Meaning |
| - | - |
| `none` or `no` | No CPU binding. The operating system schedules tasks on any available CPU resources. This can lead to suboptimal resource usage, and isn't generally recommended when performance is critical. |
| `map_cpu:<list>` | Lets you provide a comma-separated list of CPU IDs to specify the exact CPUs on which to run your task. |
| `mask_cpu:<list>` | Functions similarly to `map_cpu`, but uses a hexadecimal CPU mask for even more granular control. |

For a full list of available `--cpu-bind` options, see [SchedMD's Slurm documentation](https://slurm.schedmd.com/srun.html#OPT_cpu-bind).

## Align tasks with NUMA nodes for multi-GPU jobs

CPU binding controls which cores a task uses, but it doesn't by itself fix how Slurm spreads ranks across NUMA nodes. By default, Slurm distributes tasks cyclically (round-robin across sockets), which can place a task's CPU cores on a different NUMA node than its GPU. On multi-GPU nodes, this NUMA misalignment can cause a substantial slowdown on chip-to-chip (C2C) heavy workloads.

To align ranks with NUMA nodes, add block distribution to your job:

```bash theme={"system"}
#SBATCH --distribution=block:block
```

This allocates cores contiguously so consecutive ranks land on the same NUMA node as their GPU. For per-instance NUMA topology tables, verification commands, and how administrators make block distribution the cluster-wide default, see [Optimize CPU binding and NUMA affinity for multi-GPU jobs](https://docs.coreweave.com/products/sunk/optimize_workloads/cpu-binding-numa-affinity.md).
