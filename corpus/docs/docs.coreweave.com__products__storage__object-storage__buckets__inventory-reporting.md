# About Inventory Reporting for CoreWeave AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting

# About Inventory Reporting for CoreWeave AI Object Storage

> Understanding inventory reports for CoreWeave AI Object Storage buckets and objects

Inventory Reporting provides a scheduled, point-in-time listing of all objects in a bucket so you can audit, analyze, and manage bucket contents at scale without enumerating objects yourself. The output includes lists of objects with metadata for each object. You specify the source bucket whose objects to inventory and a destination bucket for the output. You can schedule the inventory listing to run daily or weekly, and you can configure the output to meet your analytics needs.

Inventory Reporting supports storage, data platform, security, and compliance teams that need object-level inventory for governance, analytics, lifecycle, and cost optimization. This page describes the available configuration options, the structure of the resulting reports, and the limitations to consider before you enable Inventory Reporting on a bucket.

## Configuration options

For your inventory reporting configuration, you can specify the following options:

* **Schedule**: How often you want the inventory report to run, either daily or weekly.
* **Source bucket**: Choose the bucket that you want to inventory. You can choose to list all of the objects in the bucket or only objects with a specified prefix. If you don't specify a prefix, the report inventories all objects.
* **Destination bucket**: Choose the bucket where you want to write the inventory reports, and optionally specify a prefix (subdirectory) to organize the reports.
* **Output formats**:
  * JSON, CSV, or TSV files compressed with [GZIP](https://www.gzip.org/).
  * [Parquet](https://parquet.apache.org/) files compressed with [Snappy](https://github.com/google/snappy).
  * [Optimized row columnar (ORC)](https://orc.apache.org/) files compressed with [ZLIB](https://zlib.net/).
* **Optional fields**: Choose the optional fields that you want to include in the inventory report. See the [detailed field reference](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure.md#configure-the-inventory-report) for all available configuration options.

To configure and enable inventory reports, see [Configure Inventory Reporting for CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure.md).

### Output fields

When you configure your inventory report, you can choose whether to include or exclude certain fields from the output.

The report always includes some fields, and includes optional fields only if you specify them in the `OptionalFields` configuration. The following fields are available:

| Field name | Description | When included in report |
| - | - | - |
| `BucketName` | Name of the bucket that contains the object | Always |
| `ObjectKey` | Unique key (path/name) that identifies the object within the bucket | Always |
| `VersionID` | Version identifier for the object, if versioning is enabled | Always included if `IncludedObjectVersions` is set to `All` |
| `IsLatest` | Indicates whether this is the latest version of the object | Always included if `IncludedObjectVersions` is set to `All` |
| `IsDeleteMarker` | Shows whether this entry is a delete marker | Always included if `IncludedObjectVersions` is set to `All` |
| `Size` | Size of the object in bytes | Optional |
| `LastModifiedDate` | Date and time when the object was last modified | Optional |
| `IsMultipartUploaded` | Indicates whether the object was uploaded as a multipart upload | Optional |
| `EncryptionStatus` | Encryption status or method used on the object | Optional |
| `StorageClass` | Storage class assigned to the object (see [Usage-Based Billing](https://docs.coreweave.com/products/storage/object-storage/about.md#usage-based-billing)) | Optional |
| `ChecksumAlgorithm` | Algorithm used to compute the checksum of the object | Optional |
| `LastAccessedDate` | Timestamp of the last access (read) of the object, in [RFC 3339](https://www.rfc-editor.org/info/rfc3339/) format, expressed in UTC. Example: `2026-05-20T12:00:00Z` | Optional |
| `ETag` | ETag of the object. You can use ETags with [conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes) to perform atomic updates. | Optional |

## Notes and limitations

Before you enable Inventory Reporting, review the following considerations:

* **No notifications**: You don't receive notifications when the inventory listing completes, so you must check the destination bucket to see whether the inventory reports have been written.
* **Pricing**: Inventory Reporting incurs charges for storage of the inventory reports in your destination bucket. Use `LastAccessedDate` to derive the [access tier (Hot, Warm, or Cold)](https://docs.coreweave.com/products/storage/object-storage/about.md#usage-based-billing) of the objects. For a workflow that uses `LastAccessedDate` to safely reclaim capacity, see [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md).
* **Consistency**: Inventory reports provide eventual consistency. A specific report might not reflect object changes during the scan, but changes converge across successive runs. Reports aren't transactional snapshots.
* **Not for billing**: Inventory reports are for governance and analytics, not billing reconciliation. Inventory reports don't match the audit logs or the billing data exactly.
* **Configuration limit**: You can set up to 1,000 inventory configurations per bucket.
* **Encryption**: [SSE-C](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md) for report files is not supported.

## Inventory report contents

After an inventory run completes, the destination bucket contains the following report artifacts:

* A **manifest file** (`manifest.json`) that describes the report and lists all inventory data files.
* One or more **inventory data files** that contain the object listings.

### Manifest file

The manifest file (`manifest.json`) describes the inventory report, and it's written to the root of the subdirectory specified in the inventory configuration. The manifest file is a JSON object with the following fields:

| Field | Description |
| - | - |
| `fileSchema` | Specifies which fields are included in the report |
| `sourceBucket` | Name of the source bucket |
| `destinationBucket` | Name of the destination bucket |
| `version` | Version of the inventory report |
| `creationTimestamp` | Creation date (start of inventory report generation) |
| `files` | List of the inventory files |
| `files.key` | Key that identifies the file path, always included in the report |
| `files.size` | Size of the inventory file in bytes |
| `files.md5checksum` | MD5 checksum of the inventory file |

The manifest file looks similar to this:

```json title="manifest.json" theme={"system"}
{
  "sourceBucket": "my-bucket",
  "destinationBucket": "arn:aws:s3:::my-destination-bucket",
  "version": "2016-11-30",
  "creationTimestamp": "1761777847000",
  "fileFormat": "JSON",
  "fileSchema": "Bucket,Key,VersionId,IsLatest,IsDeleteMarker,Size,StorageClass,LastAccessedDate",
  "files": [
    {
      "key": "inventory-reports/my-bucket/my-inventory-config/data/2025-10-29_2ead449d-ef16-5bb2-beb9-f3421d5c8af1.json.gz",
      "size": 183,
      "md5checksum": "6f7cbc70f083910058ac7d57615a304b"
    }
    ...
  ]
}
```

## Support

If you need help with Inventory Reporting, [contact CoreWeave support](https://support.freshdesk.com/support/home) or email `support@coreweave.com`.
