# About CoreWeave AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/about

# About CoreWeave AI Object Storage

> Highly reliable, performant Object Storage designed for AI workloads

**CoreWeave AI Object Storage** is a purpose-built, fully managed object storage service that is optimized for AI workloads and can be used as general-purpose cloud storage. AI Object Storage is built and operated by CoreWeave, and implements an S3-compatible API, which means it follows the S3 request/response model and works with standard S3 tools, while maintaining its own service behavior, limits, and feature set.

This page introduces the service's benefits, availability, security model, performance characteristics, cost structure, and observability options so you can decide how AI Object Storage fits your workloads before you begin using it.

> [!NOTE]
>
> To compare the types of storage available in CoreWeave and find a storage type that fits your workload, see [Choose the right storage](https://docs.coreweave.com/products/storage.md#choose-the-right-storage) on the storage overview page.

## Benefits

AI Object Storage provides the following benefits:

* Efficiently stores and serves training datasets and model artifacts.
* Supports non-AI data and standard cloud storage workflows. AI Object Storage implements an [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md), so you can reuse familiar tools and SDKs (such as the AWS CLI, Boto3, and s3cmd) by pointing them at CoreWeave endpoints. You can also [browse and manage objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) directly from the Cloud Console.
* Delivers data efficiently to CPU and GPU Nodes and integrates with model serializers such as [Tensorizer](https://github.com/coreweave/tensorizer).
* Includes [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) (Local Object Transport Accelerator), a Node-local connection that accelerates object reads and caches data on GPU and CPU Nodes to reduce load times.
* Automates retention with [bucket lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md) that expire objects and versions on a schedule and clean up incomplete multipart uploads.

## Availability

AI Object Storage is available in multiple regions across the CoreWeave platform.

See [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) for current information on where AI Object Storage is available.

## Durability

CoreWeave AI Object Storage is designed to lose fewer than one object in 100 billion per year to equipment failure, equivalent to 99.999999999% annual durability. This figure is a design target for the storage architecture, not a service commitment. The [AI Object Storage Service Level Agreement](https://docs.coreweave.com/policies/terms-of-service/coreweave-ai-object-storage-policy.md) covers availability, not durability.

AI Object Storage uses multiple layers of protection:

* Object data is encoded as data and parity fragments and distributed across independent storage servers. The service can reconstruct the original data when individual devices or servers fail.
* Object metadata and content-location information are replicated so that no single metadata instance is the sole record of an object.
* Background integrity checks validate the relationships between object records and stored content, and verify that referenced content is present in the storage layer.
* Storage servers are monitored for failures, and missing fragments are rebuilt from the remaining data and parity to restore the intended protection level.

When enabled, bucket versioning provides an additional recovery option for accidental overwrites and deletions. It complements the service's infrastructure-level durability protections. New buckets have versioning disabled. To enable it, see [Versioned buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md).

> [!WARNING]
>
> **Availability Zone scope**
>
> When you create a bucket, you select its Availability Zone. The durability architecture protects data from storage-server failures within that Availability Zone. AI Object Storage is not a multi-zone durability service: a bucket is not automatically replicated to another Availability Zone, and the service does not create off-site backups of object data.
>
> Objects in the Archive storage class (`STANDARD_IA`) are an exception to the data-placement model described here: Archive data can be stored outside the bucket's data center. For details, see [Data placement and residency](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md#data-placement-and-residency).
>
> If your workload requires data protection or recovery across multiple Availability Zones, [contact CoreWeave support](https://docs.coreweave.com/support/contact.md) to review and design an appropriate multi-zone architecture.

## Security

AI Object Storage is designed to safeguard data with encryption and access controls.

All data stored in AI Object Storage is encrypted at rest using an industry-standard encryption algorithm (AES-256). See the [Encryption](#encryption) section for more details.

AI Object Storage uses [organization, bucket, and lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md) to enforce access control and configure retention. The Object Storage Admin [IAM role](https://docs.coreweave.com/security/iam/access-policies.md) manages control plane aspects of Object Storage, such as creating access keys and organization access policies, in the Cloud Console. For more information, see [About organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md).

For production workloads, [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) is the recommended method for obtaining Access Keys. It exchanges short-lived OIDC tokens for temporary credentials with a 30-minute lifespan, which eliminates the need to store or rotate long-lived static keys.

### Encryption

AI Object Storage provides encryption at rest by default and supports encryption in transit through TLS. For additional control, you can supply your own encryption keys using SSE-C. Encryption has no additional cost.

#### Default encryption at rest

All object data stored within AI Object Storage is encrypted at rest by default, using the AES-256 algorithm. Default at-rest encryption is applied automatically to all objects. Only the object data itself is encrypted at rest. Object metadata is not encrypted by default. Customers must ensure confidential information is stored only in object payloads, not metadata fields (including bucket names, object keys, and tags).

For workloads that use the [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), cached object data on ephemeral storage is encrypted at the drive level using Linux Unified Key Setup (LUKS). Additionally, if you use S3 Server-Side Encryption with Customer Keys (SSE-C), LOTA encrypts and decrypts data directly on the client machine. This ensures that even host root users cannot access cached data without the customer key, which provides a layer of protection beyond disk-level encryption.

AI Object Storage supports [server-side encryption with customer-supplied keys (SSE-C)](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md). This feature lets you use your own encryption keys to encrypt data while CoreWeave handles the encryption and decryption process.

#### Encryption in transit

Connections to AI Object Storage endpoints support Transport Layer Security (TLS), with TLS version 1.2 or later required for HTTPS. Data transmitted through HTTPS is protected in transit from interception and tampering.

LOTA operates as an "untrusted daemon" running on each Node and is not deployed with any user or service secrets. Communication between client Pods and LOTA, as well as between LOTA instances (Pods), is not encrypted by default. The system relies on network segmentation to provide security in these internal communications. When LOTA forwards requests or data to external `cwobject.com` endpoints, encryption in transit depends on protocol selection: only connections using HTTPS ensure encrypted traffic.

## High performance

Data stored in AI Object Storage is available immediately after upload: clients can read data as soon as it's written. This is implemented as a "read-after-write" function, meaning any `read` operation after a `write` operation retrieves updated data. This allows for secure parallel access, higher performance, and improved scalability.

## Cost management

AI Object Storage includes automated cost optimization features designed for AI workloads with varying access patterns. Objects in the `STANDARD` storage class are automatically classified based on when they were last accessed. Archive is a separate storage class that you opt into:

| Pricing Tier | SKU | Description |
| - | - | - |
| **Hot** | `caios-high-perf` | Objects that are newly uploaded or accessed within the last 7 days |
| **Warm** | `caios-warm` | Objects that have been accessed within the last 7 to 30 days |
| **Cold** | `caios-inactive` | Objects that haven't been accessed for 30+ days |
| **Archive** (Limited Availability) | `caios-archive` | Objects stored in the `STANDARD_IA` storage class, for infrequently accessed data that tolerates lower performance |

### Usage-based billing

Usage-based billing is enabled by default and requires no configuration. Objects transition back to Hot tier pricing when accessed, which makes this ideal for ML datasets, model checkpoints, and training artifacts with irregular usage patterns. Data billed as Cold has the same performance as Hot or Warm data, with no retrieval delays. Unless stated otherwise in a customer contract, AI Object Storage is billed based on the actual consumed storage.

Billing calculations are based on hourly total capacity consumption. To calculate the hourly rate, AI Object Storage measures the capacity of the stored data at least once per hour and then averages those capacity measurements across the hour.

AI Object Storage has four pricing tiers, all based on actual consumed storage:

* Hot: Data accessed in the last 7 days.
* Warm: Data accessed in the last 7 to 30 days.
* Cold: Data not accessed in the last 30 days.
* Archive (Limited Availability): Data stored in the `STANDARD_IA` storage class.

Hot, Warm, and Cold apply to objects in the `STANDARD` storage class, and objects move between them automatically. Archive is different: objects enter `STANDARD_IA` only when you write or copy them with that storage class, or when you enable Automated Archive on the bucket, and reading an archived object doesn't return it to `STANDARD`. See [Use the Archive storage class](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md).

Billing for storage resources is calculated at the end of each hour, based on the average usage during that hour. Usage is aggregated across all storage resources in your account and billed according to the tier of each object. Each month has a variable amount of hours based on the number of days in the month. To convert the listed monthly pricing to hourly, divide the monthly pricing by 730.

These hourly charges are summed across all hours in the month to determine your total monthly charge. As `STANDARD` objects are accessed or left unaccessed, they automatically move between the Hot, Warm, and Cold tiers, so your hourly charges vary based on your actual access patterns.

To find and safely delete objects that have gone cold, for example to reduce cost or reclaim capacity, see [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md).

The [Storage panel of the Usage by Product and Zone dashboard](https://docs.coreweave.com/observability/managed-grafana/cost-usage/usage-product-zone.md#storage-panel) provides more information about storage usage.

### What counts as object access

During hourly billing cycles, the last access time is measured. The following actions reset the timer and bring objects back to the Hot tier:

| Action | API Method | Description |
| - | - | - |
| **Upload** | `PutObject`, `UploadPart` | When the object is first uploaded |
| **Read** | `GetObject` | When the object is downloaded or accessed |
| **Copy** | `CopyObject`, `UploadPartCopy` | When the object is copied, both source and destination are considered "accessed" |

## Metrics and logging

CoreWeave offers audit logging and other metrics for AI Object Storage. You can use [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md#storage) to view metrics for usage, LOTA, and more in the Grafana dashboard linked in the [Cloud Console](https://cks-grafana.coreweave.com/d/bebi5t788t6v4c/caios-usage). The panel group is **Auto Archive**, and it appears in the **CAIOS Usage** panel under the **Storage** dashboard. [Audit logging for buckets](https://docs.coreweave.com/products/storage/object-storage/auth-access/audit-logging.md) is available in limited access.

![Hot, warm, and cold storage.](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/storage/_media/auto-archive.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=2194ef65f9ad0fc5b4761b563719aa3d)

See the [Storage metric](https://docs.coreweave.com/observability/usage-monitoring.md#storage-usage) and the following examples:

* [AI Object Storage example](https://docs.coreweave.com/observability/usage-monitoring.md#example-billable-ai-object-storage-grouped-by-bucket-in-gib)
* [Distributed File Storage example](https://docs.coreweave.com/observability/usage-monitoring.md#example-distributed-file-storage-in-gib)

## Next steps

* See [Get started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) to learn how to create Access Keys, buckets, and policies, and how to use objects and buckets to store and retrieve data.
* See [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) to learn how to use OIDC for secure, automated credential management in production workloads.
