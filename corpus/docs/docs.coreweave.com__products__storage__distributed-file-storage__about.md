# About Distributed File Storage

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/about

# About Distributed File Storage

> High-performance distributed file storage with snapshot and efficient deletion features for CKS workloads

This page describes Distributed File Storage, its features, performance considerations, and billing model. Use it to decide whether Distributed File Storage fits your CKS workload before you provision volumes.

> [!NOTE]
>
> To compare the types of storage available in CoreWeave and find a storage type that fits your workload, see [Choose the right storage](https://docs.coreweave.com/products/storage.md#choose-the-right-storage) on the storage overview page.

**Distributed File Storage** delivers high write speeds, high IOPS for datapath-related operations, and higher read speeds in cases where block size and queue depth are low. Distributed File Storage is ideal for operations that require frequent synchronization between Pods.

> [!WARNING]
>
> **Scope of Distributed File Storage**
> Storage access across Regions (A region encompasses a broader geographic area, expanding service availability and meeting data residency requirements.) or Availability Zones (An Availability Zone (AZ) is a partition within a region that hosts one or more data halls. AZs are physically and operationally independent from each other.) is not supported. You can only access a Distributed File Storage volume from within the cluster where it's deployed.

## Features

The following sections describe the core capabilities of Distributed File Storage volumes.

### Encryption

All data stored in Distributed File Storage volumes is automatically encrypted at rest using AES-XTS 256-bit encryption with FIPS 140-3 validated encryption keys. Encryption is enabled by default with no configuration required.

VAST automatically generates and manages encryption keys and applies them at the cluster level. Keys aren't accessible to users or operators.

Distributed File Storage doesn't support encryption for data in transit between Pods and the storage backend.

### `.snapshot` folder

Every Distributed File Storage volume features a folder called `.snapshot`, which contains a snapshot in time of the volume. This folder is accessible in any directory on the volume.

Snapshots of Distributed File Storage volumes occur every 6 hours and persist for 72 hours.

### Trash directory

The trash directory allows asynchronous deletion of files and folders in bulk. Serial `rm -rf` on large directories is a slow and possibly blocking operation. Moving files marked for removal to the trash folder (`.vast_trash`) is much faster. For more information, see [Delete files with VAST trash](https://docs.coreweave.com/products/storage/distributed-file-storage/delete-files.md).

### Filename conventions

Distributed File Storage accepts POSIX-valid filenames, including names that contain characters such as `:` and `*`. Applications that generate ISO 8601 timestamps (for example, `2026-04-21T14:30:00.log`) or other filenames with special characters work without modification.

The `/` character is reserved as the path separator, and filenames can't be empty.

### Volume deletion and data recovery

When you delete a DFS PVC, the underlying data is not removed immediately. The [Persistent Volume Management Operator (PVMO)](https://docs.coreweave.com/products/storage/distributed-file-storage/about-pvmo.md) manages a soft-delete lifecycle:

1. When a PVC is deleted, the associated PV moves to a `Released` state. PVMO records a soft-delete timestamp on the PV.
2. A background watcher periodically checks for PVs that have exceeded the soft-delete window (24 hours by default).
3. After 24 hours, PVMO changes the PV's reclaim policy from `Retain` to `Delete`, and Kubernetes removes the backing DFS volume permanently.

This means there is approximately a 24-hour window after a PVC deletion during which the PV and its data still exist and can be recovered. Recovery is possible by creating a new PVC that binds to the existing PV, a process called rebinding. When the new PVC binds to the PV, PVMO automatically removes the soft-delete marker and stops the deletion countdown. If Kubernetes VolumeSnapshots were configured, you may also be able to restore from a snapshot taken before the deletion.

After rebinding, add the protect label to the PV to prevent PVMO from ever automatically deleting it. Replace `[PV-NAME]` with the name of the PV:

```bash theme={"system"}
kubectl label pv [PV-NAME] pv.storage.coreweave.com/protect=true
```

For step-by-step recovery instructions, see [Recover a deleted PVC](https://docs.coreweave.com/products/storage/distributed-file-storage/recover-deleted-pvc.md).

## Performance considerations

> [!WARNING]
>
> Distributed File Storage is a shared, multi-tenant filesystem with no per-tenant latency guarantee, so other tenants' activity can cause latency spikes. Don't use it for fsync-sensitive workloads that need a bounded p99 sync-write latency, such as etcd, ZooKeeper, or other consensus stores. Instead, use ephemeral, Node-local NVMe through [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md) or single-tenant block volumes on [Dedicated VAST Storage](https://docs.coreweave.com/products/storage/dedicated-vast.md).

Follow these guidelines to avoid performance issues when designing your workload's file layout.

### Directory structure

Avoid creating flat directories with many entries in a single directory. The recommended maximum is 500,000 to 1,000,000 entries per directory. Exceeding this limit can cause performance degradation and unpredictable behavior depending on the storage backend. It also makes operations such as listing or iterating over files in that directory slower.

If your workload naturally produces many files, organize them into a hierarchy of subdirectories to keep entry counts within this range.

## Billing

This section explains how CoreWeave calculates charges for Distributed File Storage so you can estimate costs for your provisioned volumes.

Unless stated otherwise in a customer contract, DFS is billed based on the total provisioned capacity of all customer [Persistent Volume Claims](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-volumes.md) (PVCs).

DFS is billed based on hourly total provisioned capacity. To calculate the hourly rate, DFS measures the total provisioned capacity of all customer PVCs every 30 seconds and then averages those capacity measurements across the hour.
