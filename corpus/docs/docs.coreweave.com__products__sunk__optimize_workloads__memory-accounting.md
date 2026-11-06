# Diagnose unexplained memory pressure on a SUNK node

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/memory-accounting

# Diagnose unexplained memory pressure on a SUNK node

> Tell reclaimable page cache from pinned shmem and system overhead when Pod metrics look fine but the node OOMs

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

When a SUNK compute node exhausts its memory, the kernel terminates the largest offending process to reclaim it. This is an out-of-memory (OOM) kill, and Slurm reports the job as failed. The metrics afterward may appear contradictory: the node's Kubernetes Pod metrics show modest memory use, and the node's Grafana panel shows ample available memory in the moments before the OOM event.

This page explains how to diagnose the source of memory pressure on a node by checking node-level memory instead of Pod metrics. Checking the right metrics helps you determine whether memory pressure comes from reclaimable page cache or pinned shmem and tmpfs. If necessary, cluster administrators can change `MemSpecLimit`, `ConstrainRAMSpace`, or the cache-dropper sidecar.

## Read node memory, not Pod metrics

Slurm's cgroup plugin creates its own cgroup hierarchy on the node, separate from the Kubernetes Pod's cgroup. Training job memory is charged to the Slurm hierarchy, not the Pod hierarchy. This separation has two consequences:

* cAdvisor and Kubernetes Pod metrics show only the `slurmd` daemon's small footprint, not the memory jobs use.
* A Pod memory limit on the `slurmd` container doesn't constrain the Slurm jobs themselves.

To diagnose the source of memory pressure, read node-level memory (`/proc/meminfo` or `node_memory_*` metrics), not Pod or container metrics. For the CPU side of the same split and the Slurm metrics the Syncer exports instead, see [Why do slurmd Pod metrics show almost no CPU or memory usage?](https://docs.coreweave.com/support/sunk/articles/why-do-slurmd-pod-metrics-show-almost-no-cpu-or-memory-usage).

The next section shows how to compare `Shmem` and `Cached` in `/proc/meminfo` to distinguish reclaimable page cache from pinned shmem and tmpfs.

### Compare `Shmem` and `Cached`

In `/proc/meminfo`, the `Shmem` field (shared memory and tmpfs, including `/dev/shm`) is counted inside `Cached`. The kernel's `MemAvailable` estimate treats cached memory as reclaimable. Shmem and tmpfs pages aren't reclaimable under pressure: unlike file-backed page cache, they have no backing file to evict to.

> [!NOTE]
>
> Don't compare `Shmem` against `Unevictable`. The kernel's unevictable list holds ramfs pages, tmpfs mounted with `noswap`, `SHM_LOCK`ed segments, and `mlock()`ed memory, so an ordinary `/dev/shm` leaves `Unevictable` near zero even when tens of gibibytes of shmem are pinned.

Use the ratio of `Shmem` to `Cached` to tell reclaimable cache from pinned shmem.

1. On the affected node, compare `Shmem` and `Cached` by running the commands below:

   ```bash theme={"system"}
   # Compare Shmem and Cached. Read-only.
   grep -E 'MemTotal|MemAvailable|^Cached|^Shmem' /proc/meminfo

   # Tmpfs shared memory in use. Read-only.
   df -h /dev/shm
   ```

2. In the output, look for the following node metrics:

   | `/proc/meminfo` field | Prometheus metric |
   | - | - |
   | `Shmem` | `node_memory_Shmem_bytes` |
   | `Cached` | `node_memory_Cached_bytes` |
   | `MemAvailable` | `node_memory_MemAvailable_bytes` |

3. Compare the two values and find your case in the table:

   | What you see | Source of the pressure | What frees it |
   | - | - | - |
   | `Shmem` is a small fraction of `Cached` | Reclaimable, file-backed page cache left between exclusive jobs. | The [cache-dropper sidecar](https://docs.coreweave.com/products/sunk/optimize_workloads/cache-dropper.md) can free it. [`compute.cacheDropper.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#compute--cacheDropper--enabled) defaults to `true`; a job triggers a drop by creating `/run/enroot/drop_caches`. The cache-dropper can't free shmem or tmpfs. |
   | `Shmem` accounts for most of `Cached` | Pinned shmem and tmpfs. A high `MemAvailable` reading isn't trustworthy here. | Nothing on the node frees it: neither the cache-dropper nor a manual `drop_caches`. Reduce shmem use in the job, or ask an administrator to scope per-job temp space and raise reserved system memory (see the following section). |

## Ask an administrator

Bring these items to the cluster administrator. Job authors can't set them.

**`MemSpecLimit`** reserves memory, in mebibytes, for system use so Slurm doesn't allocate it to jobs. Leave it unset and Slurm reserves nothing beyond what the node already holds back. It takes effect only when memory is a consumable resource, which the SUNK default `SelectTypeParameters=CR_CPU_MEMORY` satisfies.

On SUNK, CoreWeave already holds back memory for the operating system, kubelet, and DaemonSets, and Slurm advertises a reduced `RealMemory` to match. `MemSpecLimit` covers what that baseline misses: on-node sidecars and shmem peaks. See [Avoid stranded GPUs](https://docs.coreweave.com/products/sunk/run_workloads/avoid-stranded-gpus.md) for how `RealMemory` relates to what a job can request.

> [!WARNING]
>
> Don't put `MemSpecLimit` in `slurmConfig`. That block renders into global `slurm.conf` scope, where Slurm rejects the key with `_parse_next_key: Parsing error at unrecognized key: MemSpecLimit`. On SUNK that parse failure restarts every Pod in the Slurm cluster and disrupts running jobs. `MemSpecLimit` is a per-node parameter and belongs on the node configuration. The same applies to `CoreSpecCount` and other per-node keys.

The CoreWeave AI Object Storage proxy sidecar, when present, can consume 30 to 50 GiB under heavy object-storage workloads. That usage is invisible to cAdvisor and to Slurm cgroup accounting on cgroup v1. Account for it in `MemSpecLimit` on nodes that run object-storage-heavy jobs.

**`ConstrainRAMSpace=yes`** in `cgroup.conf` is what makes Slurm enforce per-job memory limits. SUNK sets it by default under [`slurmConfig.cgroupConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig). Two conditions make it effective:

* `SelectTypeParameters` must track memory. SUNK defaults to `CR_CPU_MEMORY`, so check this only when someone has overridden it. Without memory as a consumable resource, cgroup memory enforcement may not work even with `ConstrainRAMSpace=yes`.
* On cgroup v1, `ConstrainRAMSpace=yes` is the only thing bounding a Slurm job, because Pod limits don't constrain Slurm jobs. On cgroup v2, Slurm still manages its own memory cgroup slice, so `ConstrainRAMSpace=yes` is still required for Slurm-side enforcement.

Even with `ConstrainRAMSpace=yes`, heavy `/dev/shm` use can still cause a node-level out-of-memory event, because shmem allocations live in the host-level Slurm cgroup rather than the per-task cgroup that `ConstrainRAMSpace` bounds. For full cgroup configuration, see [Manage resource binding with task plugins](https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins.md).

```bash theme={"system"}
# cgroup2fs means cgroup v2; tmpfs means cgroup v1. Read-only.
stat -fc %T /sys/fs/cgroup/
```

**Per-job `/dev/shm` and `/tmp`** give each job its own shmem and temp space, which Slurm cleans up when the job ends. Whether they're on by default, and how to turn them on, depends on the SUNK version:

> [tab] SUNK 8.1 and later
>
> Per-job `/dev/shm` and `/tmp` are on by default. The SUNK operator enables Slurm's `namespace/linux` plugin, which gives each job a private `/tmp` and a fresh `/dev/shm` tmpfs. The operator also sets `NamespaceType=namespace/linux` and adds `Contain` to `PrologFlags`, which the plugin requires. Don't also set `JobContainerType`, because Slurm ignores it when `NamespaceType` is set.
>
> The operator doesn't enable the plugin in these cases:
>
> * The cluster pins `protocolVersion` to `25_05`. The plugin requires Slurm 25.11.
> * `PrologFlags` includes `NoHold`, which Slurm rejects alongside `Contain`.
> * `namespaceConfig.defaults.basePath` is one of the `namespaceConfig.defaults.dirs` directories, or inside one.
>
> In the last two cases, the operator emits a `NamespacePluginSkipped` Warning event.

> [tab] SUNK 8.0
>
> SUNK 8.0 doesn't turn on per-job `/dev/shm` and `/tmp`, and doesn't provide the configuration the Slurm plugin needs. To get them, upgrade to SUNK 8.1, which turns them on by default.
>
> SUNK 8.0 runs Slurm 25.11 by default, which replaced `JobContainerType` with `NamespaceType`. Slurm's `namespace/tmpfs` plugin, which `JobContainerType=job_container/tmpfs` also loads, requires a `job_container.conf` file that sets `BasePath`. SUNK 8.0 doesn't render that file, so `slurmd` fails to load the plugin.
>
> Per-job `/dev/shm` and `/tmp` are on by default in SUNK 7.6, so upgrading from 7.6 to 8.0 turns them off. If you set `JobContainerType` in your 7.6 overrides, remove it before you upgrade.

> [tab] SUNK 7.x and earlier
>
> In SUNK 7.6 and later 7.x releases, per-job `/dev/shm` and `/tmp` are on by default. The SUNK chart sets `JobContainerType=job_container/tmpfs`, renders `job_container.conf`, and adds `Contain` to `PrologFlags`. To turn them off, set `JobContainerType` to an empty string.
>
> In SUNK 7.5 and earlier, set `JobContainerType=job_container/tmpfs`, add `Contain` to `PrologFlags`, and provide a `job_container.conf` that sets `BasePath`. Slurm requires `PrologFlags=Contain` for this plugin. The SUNK default [`PrologFlags`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) is `Alloc,Serial`, so on these versions this is a change to make, not a default to rely on.

## When to file a support ticket

Open a ticket when a node runs out of memory and you've confirmed the pressure isn't reclaimable cache and have accounted for shmem and system overhead in `MemSpecLimit`. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include `/proc/meminfo` output, the cgroup version, and the job's memory pattern (especially `/dev/shm` use).

## Related pages

* [Manage memory with cache-dropper](https://docs.coreweave.com/products/sunk/optimize_workloads/cache-dropper.md): trigger the page cache dropper between jobs.
* [Manage resource binding with task plugins](https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins.md): cgroup configuration and constraints.
* [Avoid stranded GPUs](https://docs.coreweave.com/products/sunk/run_workloads/avoid-stranded-gpus.md): how `RealMemory` and `DefMemPerCPU` bound what a job can request.
* [Why do slurmd Pod metrics show almost no CPU or memory usage?](https://docs.coreweave.com/support/sunk/articles/why-do-slurmd-pod-metrics-show-almost-no-cpu-or-memory-usage): the same cgroup split, and which metrics to read instead.
* [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md): shared directory permissions and home directory hygiene.
