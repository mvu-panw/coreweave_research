# Manage memory with cache-dropper

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/cache-dropper

# Manage memory with cache-dropper

> Use cache-dropper to manage memory between exclusive Slurm jobs on a node

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

This page explains how to use the `cache-dropper` sidecar to flush the Linux page cache between exclusive Slurm jobs on a SUNK compute node. It's intended for cluster administrators and job authors who need to mitigate memory fragmentation in CPU-intensive training workloads.

Between exclusive jobs on a node, dropping the page cache can improve performance and lower memory access times caused by memory fragmentation. Memory fragmentation can lead to Out of Memory (OOM) errors and slowdowns in CPU-intensive training jobs.

SUNK includes a sidecar container, `cache-dropper`, to handle page cache flushes. [`compute.cacheDropper.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#compute--cacheDropper--enabled) defaults to `true`, so the sidecar is on unless an administrator disables it. The sidecar runs in privileged mode, which lets it drop the cache without requiring the main `slurmd` container to run as privileged. It checks for the presence of a [specific trigger file](#drop-the-page-cache-with-a-slurm-job) and drops the page cache if that file appears. The `cache-dropper` sidecar writes to the `drop_caches` [`sysctl`](https://www.kernel.org/doc/Documentation/sysctl/vm.txt) file to free both page cache and reclaimable slab objects.

The cache-dropper can't free shmem or tmpfs memory. If node pressure comes from pinned shmem (`Shmem` tracks `Cached` in `/proc/meminfo`), use [Diagnose unexplained memory pressure on a SUNK node](https://docs.coreweave.com/products/sunk/optimize_workloads/memory-accounting.md) instead.

Dropping the cache is a non-destructive operation, but it can incur additional CPU and I/O overhead as dropped objects are recreated.

## Configure the `cache-dropper` sidecar

The sidecar ships enabled by default. To disable it:

1. In the Slurm `values.yaml` file, find the [`compute.cacheDropper.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#compute--cacheDropper--enabled) parameter.
2. Set `.compute.cacheDropper.enabled` to `false`.
3. Save the file, and apply the changes to the cluster.

When enabled, `cache-dropper` is present in every `slurmd` Pod. It periodically checks for the existence of the `/run/enroot/drop_caches` file as a signal to proceed. If this file exists, it triggers the cache drop operation.

## Drop the page cache with a Slurm job

Individual Slurm jobs trigger a cache drop by creating the trigger file the sidecar watches for.

To use `cache-dropper`, add the following `touch` command to a Slurm job script:

```bash theme={"system"}
touch /run/enroot/drop_caches
```

The cache drops each time the job runs this command. With the sidecar enabled and the trigger in place, jobs that include this command release the page cache before subsequent work runs on the node.
