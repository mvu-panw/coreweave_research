# About Dedicated VAST Storage

Source: https://docs.coreweave.com/products/storage/dedicated-vast/about

# About Dedicated VAST Storage

> Capacity, performance, and high availability for single-tenant VAST storage on CoreWeave.

This page introduces Dedicated VAST Storage so you can decide whether it fits your workload before you ask CoreWeave to provision a cluster. It covers what the product is, its capacity and performance, and the high-availability options you can request at sizing time.

Dedicated VAST Storage is a single-tenant VAST cluster that CoreWeave provisions within the same data center as your GPU workloads. You get exclusive use of all physical cluster hardware, with no sharing of storage infrastructure with other CoreWeave tenants.

Dedicated VAST suits workloads that need petabyte-scale capacity, multi-protocol access (NFS, S3, NVMe/TCP, and SQL), full cluster management control through the VAST Management System (VMS), and advanced data services such as VAST Catalog, DataBase, DataEngine, and cross-cluster replication.

> [!NOTE]
>
> Dedicated VAST is a capacity-reserved product. Provisioning requires coordination with CoreWeave. [Contact Sales](https://www.coreweave.com/contact-us) to discuss sizing and availability.

If you don't need a dedicated cluster, CoreWeave also offers shared storage products:

* For S3-compatible object storage, see [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md).
* For a managed shared POSIX filesystem, see [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md).

## Capacity and performance

Dedicated VAST clusters support as much as 100 PB of usable capacity, terabytes per second of read throughput, and millions of IOPS. CoreWeave sizes clusters at provisioning time based on your workload requirements.

CoreWeave can help you determine the optimal configuration for your workload, and can scale your cluster as your needs change over time. [Contact support](https://docs.coreweave.com/support.md) for sizing and tuning guidance.

## High availability

CoreWeave recommends that you deploy Dedicated VAST in a high-availability (HA) configuration. In HA mode, the cluster can sustain the complete loss of a single storage component without data loss or service interruption. Discuss HA requirements with CoreWeave during the sizing process.
