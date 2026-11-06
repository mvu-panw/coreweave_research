# Protocols and data access

Source: https://docs.coreweave.com/products/storage/dedicated-vast/protocols-and-access

# Protocols and data access

> Access Dedicated VAST clusters using NFS, S3, NVMe/TCP, or SQL protocols with Kubernetes CSI drivers

This page describes how workloads connect to a Dedicated VAST cluster. It covers the protocols VAST supports, how Views expose those protocols, how Kubernetes workloads consume Dedicated VAST through CSI drivers, and how you configure S3 and network access. Use it to choose the right access method for your workload and to understand how VAST handles authentication and network connectivity.

## Supported protocols

Dedicated VAST supports all built-in VAST protocols, including NFS, S3, NVMe/TCP, and SQL, so you can connect workloads that use different access patterns.

### NFS

Standard POSIX filesystem access. Suitable for most AI/ML training and inference workloads that read and write files directly.

Dedicated VAST supports multi-path NFS, which distributes NFS traffic across multiple network paths to increase throughput and resilience. For multi-path configuration details, see the [VAST NFS multi-path documentation](https://kb.vastdata.com/documentation/docs/nfs-features-for-enhanced-performance-1#multipath).

### S3

S3-compatible object storage access served directly by your Dedicated VAST cluster. This is the cluster's built-in S3 endpoint, separate from [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md). S3 credentials are tied directly to VAST VMS user accounts. The same user identity governs both file and object access.

For multi-tenant S3-compatible storage that does not require dedicated infrastructure, see [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md).

### NVMe/TCP (block)

High-performance block storage access using NVMe over TCP. Dedicated VAST lets you provision paths as block storage subsystems and partition cluster capacity as block storage volumes, without requiring specialized networking hardware such as Fibre Channel or InfiniBand. You provision block storage through VMS, the VMS REST API, or the VAST Block CSI Driver for Kubernetes.

For block storage configuration details, see the [VAST block storage documentation](https://kb.vastdata.com/documentation/docs/overview-of-block-storage-on-vast-cluster).

### SQL

Direct SQL query access to VAST DataBase. Lets analytics workloads query data stored on VAST without ETL or external data movement. For more information about DataBase, see [Data services](https://docs.coreweave.com/products/storage/dedicated-vast/data-services.md).

## VAST Views

A **View** is VAST's protocol abstraction layer. Each View maps a filesystem path (or path subtree) to one or more protocols and carries the configuration for how VAST exposes that path: mount options, access permissions, and protocol-specific settings.

Separate Views can expose a single path simultaneously over NFS, S3, SQL, and block, so different consumers can access the same underlying data through their preferred interface.

You manage View configuration in VMS. For configuration details, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Kubernetes and CSI drivers

Kubernetes PVCs on Dedicated VAST use the standard VAST CSI drivers. VAST provides separate drivers for file and block storage:

* **VAST CSI Driver**: Manages file-based PersistentVolumes (NFS). Deploys controller and node pods for volume lifecycle operations (create, delete, and resize) and mount handling. For more information, see the [VAST CSI Driver documentation](https://github.com/vast-data/vast-csi).
* **VAST Block CSI Driver**: Manages block-based PersistentVolumes (NVMe/TCP). For more information, see the [VAST block storage documentation](https://kb.vastdata.com/documentation/docs/overview-of-block-storage-on-vast-cluster).

Both drivers authenticate to VAST using customer-provided VAST credentials. You supply a VAST VMS user account when configuring each driver. That account must have appropriate permissions to create and manage Views and exports on the cluster.

## S3 access

VAST generates S3 credentials for Dedicated VAST and associates them with VAST VMS user accounts, the same user accounts that handle file (NFS) access. You can generate S3 access keys in VMS for a given user account so that user can authenticate to the cluster's S3 endpoint.

This unified user model means access control policies applied to a VMS user affect both NFS and S3 access for that identity. VAST Views configured for S3 export back bucket-style S3 access.

For S3 endpoint configuration and credential generation, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Network access

CoreWeave provisions network access to your Dedicated VAST cluster. As part of the provisioning process, CoreWeave grants your GPU cluster nodes network connectivity to the VAST cluster IPs. After CoreWeave establishes network access, you configure VAST credentials and the CSI drivers independently. Contact [CoreWeave support](https://docs.coreweave.com/support.md) if you need to adjust network access policies.
