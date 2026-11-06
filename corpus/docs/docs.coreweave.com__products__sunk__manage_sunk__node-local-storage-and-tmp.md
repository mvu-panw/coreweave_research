# Node-local storage and temporary files on Slurm nodes

Source: https://docs.coreweave.com/products/sunk/manage_sunk/node-local-storage-and-tmp

# Node-local storage and temporary files on Slurm nodes

> What backs /tmp on SUNK Slurm nodes and how to keep temporary files on NVMe instead of RAM

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page explains what backs the `/tmp` directory on SUNK Slurm nodes, how to keep temporary files on node-local NVMe instead of RAM, and why some commands fail with `Operation not permitted` inside a container. It's for SUNK administrators and users who run Slurm jobs, especially containerized jobs that write large amounts of temporary data.

CoreWeave SUNK runs Slurm on Kubernetes for batch and burst workloads. Each Slurm node runs in a Kubernetes Pod on a CoreWeave node, so it shares the same node-local NVMe storage described in [About local storage](https://docs.coreweave.com/products/storage/local-storage.md). The backing for `/tmp`, however, depends on whether the job runs inside a container.

## What backs the temporary directory

On a Slurm node, the directory that backs `/tmp` depends on whether the job runs inside an [Enroot](https://github.com/NVIDIA/enroot) or Pyxis container:

| Job environment | What backs `/tmp` |
| :- | :- |
| Bare `srun` (no container) | The node's local NVMe RAID array (`/dev/md127`). |
| Inside an Enroot or Pyxis container (`srun --container-image`) | `tmpfs` (RAM). The container root filesystem is an overlay on the same NVMe array, but `/tmp` is a separate `tmpfs` mount. |

Inside a container, `tmpfs` is sized to a fraction of the node's memory. For example, on a node with 2 TiB of RAM, `/tmp` is roughly 1 TiB. Because `tmpfs` is RAM, writing temporary data to `/tmp` in a containerized job consumes system memory rather than disk.

## Keep temporary files on NVMe

When `/tmp` is `tmpfs`, a job that writes large temporary files there consumes RAM. The job can fail with a "no space left on device" (`ENOSPC`) error even though node and volume disk-usage metrics look clean, because the data is filling memory rather than the NVMe array. Libraries that cache to a temporary directory (for example, some object-storage clients) are a common cause.

To keep temporary files on NVMe, set `TMPDIR` to an NVMe-backed path in your job script. Most programs and libraries honor `TMPDIR` when they create temporary files:

```bash theme={"system"}
export TMPDIR=/var/nvme/storage/${SLURM_JOB_ID}
mkdir -p "$TMPDIR"
```

> [!WARNING]
>
> Setting `TMPDIR` with `#SBATCH --export=TMPDIR=/tmp` doesn't help, because inside an Enroot container `/tmp` is still `tmpfs`. Point `TMPDIR` at an NVMe-backed path instead.

## Where Enroot stores container data

Enroot extracts and stores container data under the path set by `ENROOT_DATA_PATH`. On SUNK, this defaults to `/opt/sunk/tmp/enroot-data/user-$(id -u)`, an ephemeral directory backed by node-local storage (XFS). This keeps container extraction on local NVMe rather than on shared network storage.

If a job is preempted or requeued, leftover `pyxis_*` directories under this path can cause the next start to fail with `File already exists`. For details, see [Why does Pyxis report File already exists after a job is preempted?](https://docs.coreweave.com/support/sunk/articles/why-does-pyxis-report-file-already-exists-after-preemption).

## Operation not permitted inside an Enroot container

By default, Enroot runs container images in an unprivileged user namespace and remaps UIDs, so you aren't real root on the host. Commands that require host root, such as `chown` or `chmod` to another owner or `sudo`, fail with `Operation not permitted`. This default protects the shared node.

To work within the unprivileged namespace, use the following approaches:

* Build the image so files already have the right owner and permissions, rather than running `chown` inside the job.
* For tools that only check for UID 0, investigate Enroot's fakeroot support, which presents a fake root environment. It doesn't grant real host privileges.
* If you only need file ownership on mounted filesystems to match your own user, pass `--no-container-remap-root`. This turns off UID translation. `sudo` still fails, because you still aren't root.
* If a workflow needs capabilities the unprivileged namespace can't provide, ask your cluster administrator whether privileged containers can be enabled for your cluster before you redesign the workflow. Enabling them is a cluster-wide decision with security implications for every user on the shared nodes.

For the full list of symptoms and workarounds, see [Why do sudo, chown, and chmod fail inside a Pyxis container?](https://docs.coreweave.com/support/sunk/articles/why-do-permission-errors-occur-in-pyxis-enroot-containers).

## Verify what backs a path

To confirm what backs `/tmp` (or any path) on a node, check the mount source and filesystem type:

```bash theme={"system"}
findmnt -no SOURCE,FSTYPE /tmp
```

A `tmpfs` source means the path is RAM-backed. A device such as `/dev/md127` means it's on the node-local NVMe RAID array. You can also use `df -h /tmp` to see the backing device and available space.

## Related

* [About local storage](https://docs.coreweave.com/products/storage/local-storage.md): RAID layout, throughput, and benchmarking for node-local NVMe storage.
* [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md): mount Persistent Volume Claims for data that must persist or be shared across nodes.
* [`emptyDir` volumes](https://docs.coreweave.com/products/storage/local-storage#recommended-emptydir-volumes): NVMe-backed scratch space in a Kubernetes Pod, an alternative to `/tmp`.
* [Why does Pyxis report File already exists after a job is preempted?](https://docs.coreweave.com/support/sunk/articles/why-does-pyxis-report-file-already-exists-after-preemption): leftover Enroot directories after preemption.
