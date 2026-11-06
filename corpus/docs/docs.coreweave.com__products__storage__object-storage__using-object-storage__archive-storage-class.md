# Use the Archive storage class

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class

# Use the Archive storage class

> Store infrequently accessed objects at a lower cost with the Archive storage class

The **Archive** storage class stores infrequently accessed objects in CoreWeave AI Object Storage at a lower per-GiB rate than active storage. Typical workloads include long-term retention of training datasets, model checkpoints, processed datasets, experiment artifacts, system logs, and backups.

Archive preserves the object storage workflows you already use:

* Objects keep the same bucket and object address.
* Applications continue to use the S3-compatible API.
* Reads don't require a restore or rehydration step.
* Reads don't incur separate retrieval or early-deletion fees under the default configuration.

> [!NOTE]
>
> Archive is in limited availability. To request access for your organization, [contact CoreWeave support](https://docs.coreweave.com/support.md).

## How Archive works

AI Object Storage exposes two storage classes:

| Storage class | Purpose |
| - | - |
| `STANDARD` | The default for new objects. Optimized for frequent access and low-latency reads and writes. |
| `STANDARD_IA` | The Archive storage class, for infrequently accessed data. Specify `STANDARD_IA` to write or copy an object into Archive. |

Hot, Warm, and Cold are usage-based billing classifications within `STANDARD`, not separate storage classes. For how those classifications work, see [Cost management](https://docs.coreweave.com/products/storage/object-storage/about.md#cost-management).

Reading an object in `STANDARD_IA` doesn't move it back to `STANDARD`. To return an object to active storage, [move it out of Archive](#move-data-out-of-archive) explicitly.

## Data placement and residency

Archive changes where object data is stored. Objects in `STANDARD` stay within the bucket's data center. Objects in `STANDARD_IA` can be stored outside the bucket's data center, including on capacity outside CoreWeave data centers, which lets Archive use lower-cost storage. For buckets in US regions, Archive data remains within the United States. For buckets in other regions, Archive data can be stored in a different country than the bucket.

This is a statement about where data is stored, not about who can reach it. A principal with valid credentials and an applicable policy can read Archive objects from outside the region that stores them.

> [!WARNING]
>
> If your workload is subject to data residency requirements, confirm the placement model with your CoreWeave account team before you enable Archive or write objects to `STANDARD_IA`. For compliance purposes, use the commitments in your account agreement rather than this page.

## Before you begin

Confirm with your CoreWeave account team that Archive is enabled for your organization and available in your target region or Availability Zone, and that your quota and [provisioned performance limits](#archive-performance-expectations) cover what you plan to archive.

The examples on this page use the AWS CLI with a profile named `cw`. Archive works with any S3-compatible client. See [Configure endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md).

## Choose what to archive

Archive data that is read infrequently and isn't time-sensitive: completed training runs, superseded checkpoints, processed datasets, experiment artifacts, and logs kept for retention.

Keep data in `STANDARD` when reads are latency-sensitive or high-throughput. Archive isn't optimized for sustained high-throughput reads, and first-byte latency for uncached data is higher than in active storage. Move objects back to `STANDARD` before you run a workload against them.

Choose how data reaches Archive:

* **Already inactive at ingestion**: [write directly to Archive](#write-directly-to-archive).
* **Goes idle over time**: [enable Automated Archive](#enable-automated-archive) on the bucket.
* **A known set of existing objects**: [copy them into Archive](#move-an-existing-object-to-archive).

Before any bulk move, validate metadata, checksums, and performance against a test subset. Coordinate bulk reads and large-scale `CopyObject` migrations with CoreWeave support.

The [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) supports Archive objects: use the in-cluster LOTA endpoint and [pre-stage the datasets you need](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md) for predictable startup performance.

## Archive performance expectations

Archive performance is provisioned per geo, based on Archive capacity. On initial provisioning, the 0 to 10 PiB capacity range receives:

* 750 requests per second.
* 30 Gb/s of aggregate throughput.

These figures are default regional allocations for planning purposes and aren't service level agreements (SLAs). The limits apply to both ingestion and retrieval. Verify your allocation before you exceed 10 PiB or perform a bulk transfer.

At 30 Gb/s of aggregate throughput, transferring 10 PiB from Archive to `STANDARD` takes roughly 35 to 37 days, excluding operational overhead. Actual duration depends on provisioned bandwidth, request concurrency, and average object size.

## Write directly to Archive

Set the storage class to `STANDARD_IA` when you upload the object:

```bash title="Upload an object directly to Archive" theme={"system"}
aws s3api put-object \
  --bucket [BUCKET-NAME] \
  --key checkpoints/example-checkpoint.tar \
  --body example-checkpoint.tar \
  --storage-class STANDARD_IA \
  --profile cw
```

Verify the storage class:

```bash title="Check the storage class of an object" theme={"system"}
aws s3api head-object \
  --bucket [BUCKET-NAME] \
  --key checkpoints/example-checkpoint.tar \
  --profile cw
```

Limit direct ingestion to inactive datasets. Keep active data in `STANDARD` to maintain low access latency.

If the request returns `InvalidStorageClass`, either Archive isn't available in the bucket's Availability Zone, or your organization has no `STANDARD_IA` quota. Confirm availability and quota with your CoreWeave account team before you retry.

## Move an existing object to Archive

Copy the object over itself and set `STANDARD_IA` as the destination storage class:

```bash title="Copy an existing object into Archive" theme={"system"}
aws s3 cp \
  s3://[BUCKET-NAME]/checkpoints/old-checkpoint.tar \
  s3://[BUCKET-NAME]/checkpoints/old-checkpoint.tar \
  --copy-props default \
  --storage-class STANDARD_IA \
  --profile cw
```

Use the high-level `aws s3 cp` command rather than `aws s3api copy-object`. The low-level command can time out on large multipart objects because the gateway processes the parts serially.

An in-place copy has the following effects:

* In an unversioned bucket, the copy replaces the current object.
* In a versioned bucket, the copy creates a new current version. Existing noncurrent versions keep their original storage class.
* The operation updates object metadata, including the last-modified timestamp, and can change the ETag for multipart objects.
* Copying to a different destination key leaves the source object in place, and the source continues to accrue storage charges until you delete it.

## Enable Automated Archive

**Automated Archive** transitions eligible `STANDARD` object versions to `STANDARD_IA` after a period without access. You configure it per bucket, and your organization must be entitled to use it.

An object becomes eligible once it has gone unaccessed for the configured number of days, measured from creation if it has never been accessed. Transitions are evaluated asynchronously during background sweeps, which typically run every 24 hours. After you enable Automated Archive, expect up to 24 hours before the first objects begin moving.

> [!NOTE]
>
> Automated Archive is a control-plane setting, not an S3 Lifecycle transition. See [Archive and lifecycle policies](#archive-and-lifecycle-policies).

### Configure Automated Archive with the CoreWeave Intelligent CLI

Authenticate the CoreWeave Intelligent CLI with a principal that has bucket management permissions, then update the bucket:

```bash title="Enable Automated Archive after 60 days without access" theme={"system"}
cwic cwobject bucket update [BUCKET-NAME] \
  --archive-enabled=true \
  --archive-after-last-access-days=60
```

Use the same command to change the threshold:

```bash title="Change the inactivity threshold" theme={"system"}
cwic cwobject bucket update [BUCKET-NAME] \
  --archive-after-last-access-days=90
```

Or to turn Automated Archive off:

```bash title="Disable Automated Archive" theme={"system"}
cwic cwobject bucket update [BUCKET-NAME] \
  --archive-enabled=false
```

Disabling Automated Archive stops future transitions. It doesn't return existing `STANDARD_IA` objects to `STANDARD`.

### Automated Archive settings

| Setting | Description |
| - | - |
| `--archive-enabled` | Enables or disables Automated Archive. Requires an organization entitlement. |
| `--archive-after-last-access-days` | Days since last access, or since creation if the object has never been accessed. Required when Automated Archive is enabled. The default minimum is 60. Your organization's entitlement may permit a lower minimum, and the effective floor is validated server-side. |

Automated Archive applies to `STANDARD` object versions. Objects already in `STANDARD_IA` aren't reprocessed.

### Configure Automated Archive with Terraform

The CoreWeave Terraform provider exposes the same settings on the [`coreweave_object_storage_bucket_settings`](https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_settings) resource:

```terraform title="Enable Automated Archive on a bucket" theme={"system"}
resource "coreweave_object_storage_bucket_settings" "archive" {
  bucket                         = "[BUCKET-NAME]"
  archive_enabled                = true
  archive_after_last_access_days = 60
}
```

Confirm that your provider version supports these attributes before you apply the configuration.

## Read objects in Archive

Read Archive objects with an ordinary `GetObject` request. No restore step is required:

```bash title="Download an object from Archive" theme={"system"}
aws s3 cp \
  s3://[BUCKET-NAME]/checkpoints/old-checkpoint.tar \
  . \
  --profile cw
```

To see which objects are in which storage class, list the bucket:

```bash title="List objects with their storage class" theme={"system"}
aws s3api list-objects-v2 \
  --bucket [BUCKET-NAME] \
  --prefix checkpoints/ \
  --query 'Contents[].{Key: Key, StorageClass: StorageClass}' \
  --profile cw
```

## Move data out of Archive

Copy the object and set `STANDARD` as the destination storage class:

```bash title="Return an object to STANDARD" theme={"system"}
aws s3 cp \
  s3://[BUCKET-NAME]/checkpoints/old-checkpoint.tar \
  s3://[BUCKET-NAME]/checkpoints/old-checkpoint.tar \
  --copy-props default \
  --storage-class STANDARD \
  --profile cw
```

This is an in-place copy, with the same [effects on versioning and metadata](#move-an-existing-object-to-archive) as copying into Archive.

## Archive and lifecycle policies

Don't use S3 Lifecycle `Transition` actions to move objects into or out of Archive. AI Object Storage [doesn't support `Transition` actions](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies), and Automated Archive is a separate control-plane setting.

You can still use lifecycle policies for supported retention tasks on Archive objects, such as object expiration and cleanup of incomplete multipart uploads. See [Lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md).

## Monitor Archive usage

* **Grafana**: filter AI Object Storage metrics by `STANDARD_IA` to track Archive capacity and Automated Archive behavior. See [Managed Grafana](https://docs.coreweave.com/observability/managed-grafana.md#storage).
* **Inventory reports**: inspect the storage class of individual objects. See [Configure inventory reporting](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure.md).
* **Object metadata**: use `HeadObject` or an object listing to verify storage class during testing and migration.

## Pricing and billing

Archive capacity is billed at a lower per-GiB rate than active storage classes. Specific rates and quota terms are defined in your account agreement.

Under the default Archive fee structure:

* There are no separate retrieval fees.
* There are no early-deletion fees.
* There is no minimum object size.
* There is no minimum storage duration.
* Storage is billed on raw capacity consumed.

Data duplicated across keys remains billable until you delete the source objects or noncurrent versions.

## Encryption and security

Archive uses the same security model as `STANDARD`: AES-256 encryption at rest by default, TLS in transit, optional [SSE-C](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md), and the same [access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md). Moving an object into Archive changes nothing about how it's encrypted or who can read it. For details, see [Security](https://docs.coreweave.com/products/storage/object-storage/about.md#security).

## Permissions for Automated Archive

In addition to the object actions your workflow needs, configuring Automated Archive requires these control-plane actions:

* `cwobject:ConfigureBucketArchive`
* `cwobject:GetBucketInfo`

Scope policy statements for these global APIs according to the principal authorization hierarchy. See [Access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md).

## Next steps

* See [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md) to find and remove objects you no longer need, instead of archiving them.
