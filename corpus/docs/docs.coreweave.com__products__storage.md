# About CoreWeave Storage

Source: https://docs.coreweave.com/products/storage

# About CoreWeave Storage

> Overview of CoreWeave AI Object Storage, Distributed File Storage, Dedicated VAST Storage, Local Storage, and CoreWeave Database

# Storage built for AI and HPC

CoreWeave storage spans S3-compatible AI Object Storage, POSIX Distributed File Storage, single-tenant Dedicated VAST clusters, and high-speed Local Storage, tuned for training datasets, checkpoints, and model weights at scale.

High-performance computing (HPC) workloads, especially those involving AI and ML applications, typically use large training datasets, require data sharing between Nodes, and need fast, temporary storage for caching and logging purposes.

CoreWeave offers a variety of storage solutions designed to meet the demands of these intensive applications. Choose a storage product below to get started, or continue reading to compare the options based on your workload's requirements.

> [card] [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md)
>
> Purpose-built, S3-compatible object storage for training datasets, model weights, checkpoints, and other distributed bulk data.

> [card] [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md)
>
> POSIX-compliant shared filesystem with high throughput and low latency for multi-Node access.

> [card] [Dedicated VAST Storage](https://docs.coreweave.com/products/storage/dedicated-vast.md)
>
> Single-tenant VAST clusters co-located with your GPU infrastructure for petabyte-scale capacity and full cluster control.

> [card] [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md)
>
> High-performance, Node-local NVMe storage for temporary scratch space, caching, and logs.

> [card] [CoreWeave Database](https://docs.coreweave.com/products/storage/cwdb.md)
>
> Managed, PostgreSQL-compatible database service that runs inside your CKS cluster.

## Choose the right storage

Most workloads use more than one storage type. Choose storage based on data class and I/O profile: keep the active temporary working set on Local Storage, durable portable artifacts in Object Storage, and POSIX-active data in DFS.

**Does your data need to outlive the Node?**

If not, use [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md). Local Storage provides NVMe-backed scratch space for caches, logs, and intermediate artifacts, but it does not survive Node reboots.

If yes, continue.

**What interface and I/O pattern does your application use?**

Use [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/about.md) when your application uses an S3-compatible API and primarily reads or writes large objects with parallel, contiguous access, such as training datasets, model weights, checkpoints, backups, or data that must be accessible across clusters or availability zones. Use [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) from within CoreWeave clusters to cache hot objects on local Node NVMe.

Use [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md) when your application requires a POSIX filesystem, such as persistent home directories, shared workspaces, frequent file updates or directory listing, or small and random I/O.

> [!NOTE]
>
> DFS cannot be mounted from another cluster, availability zone, or region. If an application requires both POSIX access and multi-cluster data sharing, use Object Storage as the durable source of truth and stage data to DFS or Local Storage within each cluster.

The following table summarizes the three self-serve storage options:

| Storage type | Persistence | Access pattern | Best for |
| - | - | - | - |
| [Object Storage](https://docs.coreweave.com/products/storage/object-storage/about.md) | Persistent | [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) | Datasets, model weights, checkpoints, cross-cluster data sharing |
| [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md) | Persistent | POSIX filesystem | Home directories, workspaces, frequent file updates, small or random I/O |
| [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md) | Ephemeral | Node-local filesystem | Scratch space, caching, temporary files |

Distributed File Storage isn't suited to fsync-sensitive workloads that need a bounded p99 sync-write latency, such as etcd or ZooKeeper. See [Performance considerations](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md#performance-considerations).

**Need petabyte-scale capacity or full cluster control?**

[Dedicated VAST Storage](https://docs.coreweave.com/products/storage/dedicated-vast.md) provides a single-tenant VAST cluster co-located with your GPU infrastructure, with multi-protocol access (NFS, S3, NVMe/TCP, and SQL) and petabyte-scale capacity. Dedicated VAST is not self-serve: provisioning requires coordination with CoreWeave. [Contact Sales](https://www.coreweave.com/contact-us) to discuss sizing and availability.
