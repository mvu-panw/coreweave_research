# About local storage

Source: https://docs.coreweave.com/products/storage/local-storage

# About local storage

> High-performance, encrypted NVMe-backed ephemeral storage on CoreWeave Nodes for scratch space and caching

CoreWeave GPU and CPU Nodes provide high-performance, Node-local ephemeral storage on NVMe RAID, mounted at `/mnt/local`. Use this storage for temporary data such as intermediate training artifacts, caches, render outputs, or logs. This page is for workload authors who need fast scratch space close to compute and want to understand how to request it safely on CoreWeave Kubernetes Service (CKS).

Pod container filesystems (the writable layer created by the container runtime) and Kubernetes `emptyDir` volumes are stored on this NVMe-backed storage by default, through kubelet and containerd directories under `/mnt/local`. As a result, most workloads benefit from local storage without any additional configuration.

> [!NOTE]
>
> This page's volume guidance applies to workloads running on CoreWeave Kubernetes Service (CKS). Data is non-persistent and does not survive a Node reboot (for example, during maintenance or failure). Its lifetime after Pod deletion depends on the volume type: Kubernetes removes `emptyDir` volumes automatically, while `hostPath` data can remain on the same Node until you remove it.

## Recommended emptyDir volumes

For most scratch-storage use cases, use `emptyDir` volumes. `emptyDir` is the standard Kubernetes mechanism for Node-local scratch space. An `emptyDir` volume is created when a Pod is scheduled onto a Node and is deleted automatically when the Pod is removed.

On CoreWeave, `emptyDir` volumes have the following characteristics:

* **Backed by NVMe**: Data is stored under the kubelet Pod directories on `/mnt/local`, an encrypted NVMe RAID array dedicated to ephemeral workload storage. This provides high throughput and low latency for scratch workloads.

* **Better for heavy writes**: Writes to an `emptyDir` volume go directly to the underlying filesystem, avoiding the copy-on-write overhead of the container image overlay filesystem. For large or write-heavy scratch data, use `emptyDir` instead of writing to arbitrary paths in the container root filesystem.

### Set the amount of local ephemeral storage

Size your `emptyDir` volume to match the scratch space your workload needs. This protects the Node from runaway usage and helps the scheduler place your Pod correctly.

The amount of available local ephemeral storage depends on the Node type. For information on ephemeral storage size per instance type, see [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU-only instances](https://docs.coreweave.com/platform/instances/cpu-instances.md).

For ephemeral storage above `20Gi`, include the size in the [workload's resource request](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#setting-requests-and-limits-for-local-ephemeral-storage). This lets the scheduler place the Pod on a Node with enough capacity.

The following example shows where to set the size limit for an `emptyDir` volume:

```yaml theme={"system"}
volumes:
  - name: scratch
    emptyDir:
      sizeLimit: 50Gi  # Recommended: set a limit matching your expected usage
```

## Advanced hostPath volumes

`hostPath` volumes mount a specific directory on the Node's filesystem directly into a Pod. Usually, `emptyDir` is the right choice for scratch storage. Use `hostPath` only when you explicitly need to access a specific path on the Node's filesystem (for example, a legacy application that expects a hard-coded directory under `/mnt/local`).

The following example shows where to set a `hostPath` volume:

```yaml theme={"system"}
volumes:
  - name: specialized-scratch
    hostPath:
      path: /mnt/local/my-unique-workload-id  # Always use a unique subdirectory
      type: DirectoryOrCreate
```

> [!WARNING]
>
> **Restrict paths to `/mnt/local/`.** Do not mount volumes outside of `/mnt/local/` (such as `/tmp/` or `/var/`). Paths outside `/mnt/local/` are on the Node's root filesystem, which is small and not intended for workload data. Filling it can destabilize the Node. The backing for a path like `/tmp` also varies by environment. For details, see [What backs the temporary directory](#what-backs-the-temporary-directory).

When you use `hostPath`, keep the following points in mind:

* **Understand the lifecycle**: Unlike `emptyDir` data, `hostPath` data remains after you delete the Pod. Another Pod on the same Node can access the data until you remove it.
* **Understand the trade-offs**: `hostPath` bypasses Kubernetes storage isolation and couples your Pod to a particular Node layout. Volumes aren't cleaned up automatically, and you're responsible for managing path uniqueness, cleanup, and avoiding conflicts with other workloads.
* **Remember data is Node-scoped**: Data on `/mnt/local` does not survive a Node reboot. For details on encryption and the data lifecycle, see [RAID layout and throughput](#raid-layout-and-throughput).

## RAID layout and throughput

Local storage is assembled from the Node's local NVMe drives into a software RAID array, formatted as XFS, and mounted at `/mnt/local`. The RAID layout depends on how many local NVMe drives the Node has, which varies by instance type:

| Local NVMe drives | RAID layout | Throughput characteristics |
| :- | :- | :- |
| 2 to 3 drives | RAID1 (mirror) | Reads can split across the drives. Writes are about the speed of a single drive, because data is mirrored rather than striped. |
| 4 or more drives | RAID10 (striped mirror) | High parallel read and write throughput that scales with the number of drives and the concurrency of the workload. |

Most GPU Nodes have eight local NVMe drives in an 8-drive [RAID10 (RAID 1+0)](https://en.wikipedia.org/wiki/Nested_RAID_levels#RAID_10_\(RAID_1+0\)) array, which delivers high parallel throughput. Many CPU Nodes and some GPU instance types have fewer drives and use RAID1. Some instance types provide a single local NVMe drive, which is presented as one device with no RAID. Because the drive count differs by instance type, usable local storage capacity and throughput also differ by instance type.

See [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU-only instances](https://docs.coreweave.com/platform/instances/cpu-instances.md) for their storage capacities and configurations. To check the layout on a running Node, run `cat /proc/mdstat` or `lsblk`.

> [!NOTE]
>
> Local storage is encrypted at rest with a key held only in memory. The key is discarded when the Node reboots, which crypto-shreds the data and makes it unrecoverable. Combined with the non-persistent nature of local storage, this means data never survives a reboot.

## What backs the temporary directory

The directory that backs `/tmp` depends on the environment, so do not assume `/tmp` is fast NVMe scratch space. The backing differs across CKS Pods and SUNK Slurm jobs:

| Environment | What backs `/tmp` |
| :- | :- |
| Generic CKS Pod | The container's writable layer (an overlay), which sits on the NVMe RAID under `/mnt/local`. |
| SUNK Slurm, bare `srun` (no container) | The Node's local NVMe RAID array (`/dev/md127`). |
| SUNK Slurm, inside an Enroot or Pyxis container (`srun --container-image`) | `tmpfs` (RAM), sized to a fraction of Node memory. Writing large amounts of data to `/tmp` consumes RAM, not disk, and can fail with `ENOSPC` even when disk-usage metrics look clean. |

To confirm what backs `/tmp` on a Node, run `findmnt -no SOURCE,FSTYPE /tmp` (or `df -h /tmp`). A `tmpfs` source means `/tmp` is RAM-backed.

For deterministic, NVMe-backed scratch space in a CKS Pod, use an [`emptyDir`](#recommended-emptydir-volumes) volume rather than `/tmp`. For SUNK Slurm jobs, including how to redirect temporary files off `tmpfs`, see [Node-local storage and `/tmp` on Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/node-local-storage-and-tmp).

## Benchmark local storage

When you benchmark local storage, target the actual NVMe-backed volume and use a concurrent workload. Two common mistakes make local storage look slower than it is:

* **Benchmarking `/tmp` instead of NVMe.** In a SUNK Enroot or Pyxis container, `/tmp` is `tmpfs` (RAM), which inflates results and does not represent NVMe. Point your benchmark at a default `emptyDir` (not `medium: Memory`) or a known path under `/mnt/local` instead. See [What backs the temporary directory](#what-backs-the-temporary-directory).
* **Using a single stream.** A single-stream tool such as `dd`, or `fio` with `numjobs=1`, is latency-bound and understates a striped RAID10 array, which needs many parallel I/Os to reach full bandwidth.

The following `fio` command measures write bandwidth with 12 concurrent jobs against a mounted scratch directory. Replace `/scratch` with the mount path of your `emptyDir` or NVMe-backed volume.

```bash theme={"system"}
fio -name=cwtest -directory=/scratch -direct=1 -ioengine=sync \
  -bs=4M -size=20G -numjobs=12 -runtime=60 -time_based \
  -group_reporting -refill_buffers -randrepeat=0 -rw=write
```

Expect lower single-stream numbers on Nodes with fewer drives (a single drive or a 2-drive RAID1 mirror) than on GPU Nodes with an 8-drive RAID10 array. For a fuller reference benchmark, see the CoreWeave [`runtests.sh`](https://cw-storage.cwobject.com/perf/runtests.sh) script, and point its target path at your NVMe-backed volume.

## Non-persistent storage

Because Node-local ephemeral storage is non-persistent, it doesn't persist through Node reboots and doesn't require a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). If you need data to survive Node reboots or be shared across Nodes, use a persistent storage option instead. To create a persistent filesystem volume that is independent of Node status, see [Create Distributed File Storage volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md).

## Persist results to Object Storage

There is no built-in mechanism that automatically copies `emptyDir` or `hostPath` data off the Node. To keep results from an ephemeral workload, write or periodically sync them from your Pod to a persistent target before the Pod terminates:

* **CoreWeave AI Object Storage (CAIOS)**: An S3-compatible service for checkpoints, model weights, datasets, and other artifacts. Use any S3 client or library (for example, `aws s3 sync`, `s5cmd`, or Boto3) from inside your Pod, targeting the `cwobject.com` endpoint. See [Get started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) and [Connect to Object Storage](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/about.md).
* **Distributed File Storage (DFS)**: A persistent, shared filesystem mounted as a PVC. Use DFS when you need POSIX file semantics or shared access across Pods. See [Create Distributed File Storage volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md).

For long-running jobs, write checkpoints to one of these targets on an interval rather than only at Pod exit, so that a Node reboot or eviction does not lose progress.
