# Rename objects

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects

# Rename objects

> Use the atomic server-side RenameObject API to rename objects within an AI Object Storage bucket

This page describes how to rename a single object within a CoreWeave AI Object Storage bucket using the S3-compatible [RenameObject API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#s3renameobject). Use this approach when you need to change an object's key without the cost and latency of a copy-and-delete workflow, such as promoting a temporary checkpoint or finalizing a staged artifact.

The RenameObject API is an atomic, server-side rename operation for a single object within the same bucket, with no data movement and metadata preserved.

This operation is more efficient than a copy and delete operation. Rename operations complete in milliseconds regardless of object size, because the operation updates index entries instead of copying object data. Because no data is copied, you don't incur temporary double storage usage during rename operations.

You can rename objects from the Cloud Console or with S3-compatible tools and SDKs, including the AWS CLI and Boto3.

## Prerequisites

Before you use RenameObject, make sure you have:

* An active [CoreWeave account](https://console.coreweave.com).
* A valid [API Access Key and Secret Token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md).
* `s3:PutObject` on the destination and `s3:DeleteObject` on the source. See [Ensure permissions](#ensure-permissions) for details.
* An unversioned bucket. A bucket is unversioned if it has never had versioning enabled. Versioning suspended isn't supported.
* Endpoint configured for [virtual-hosted addressing](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-virtual-addressing-style).

## How it works

The following sections describe how RenameObject behaves with respect to atomicity, metadata, consistency, and LOTA caching.

### Atomicity

RenameObject is atomic and performs a metadata-only remap of the object key. No data copy occurs and no temporary duplication of object data takes place. With copy and delete, a window exists where both keys may exist, and large objects incur additional latency for the copy step. RenameObject eliminates that window and avoids the extra data movement overhead.

### Metadata preservation

RenameObject preserves object metadata, including encryption settings, storage billing tier, checksums, and related attributes supported by AI Object Storage.

### Consistency

AI Object Storage maintains read-after-write consistency for RenameObject. After a successful response, reads to the destination key return the object. Reads that are concurrent with a successful rename return exactly one of the source or the destination (assuming no other writes).

### LOTA support

When LOTA is in use, rename updates the metadata or index mapping so that cached content, if present, is immediately associated with the new key. This preserves LOTA's performance benefits without requiring data re-caching.

## Limitations

The RenameObject API only supports renaming a single object within the same bucket. If you need to rename objects across buckets, continue to use copy and delete semantics.

| Limitation | Description |
| - | - |
| Same bucket only | The source and destination keys must be in the same bucket. |
| Versioning not supported | Rename isn't supported for buckets where versioning is enabled or has ever been enabled. Specifically, unversioned buckets are supported while versioning enabled and versioning suspended aren't supported. If versioning is currently enabled, or was previously enabled on the bucket, the RenameObject request fails with an error and the object isn't renamed. |
| Single object only | Each request renames one object key. Prefix-scale rename operations aren't yet supported, so you must implement this as client-side batches that call RenameObject once per object. |
| Rate limits and high-QPS workloads | High-QPS prefix-scale workflows may be subject to rate shaping or recommended batching guidance to avoid operational impact. Consult your CoreWeave contact if you plan large rename campaigns at scale. |

## Preconditions and safeguards

RenameObject supports conditional headers to help you guard against accidental overwrites and race conditions. Typical preconditions include ETag-based and time-based conditions. `PutObject`, `CompleteMultipartUpload`, and `CopyObject` also support conditional writes using the same `If-Match` and `If-None-Match` headers. See [Conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes) for details.

Preconditions ensure the rename only proceeds when the source or destination state matches your expectations. An idempotency token lets you safely retry the same operation without creating multiple conflicting renames.

Example ETag-based source conditions:

* Rename only if the source ETag matches the value you provide (`If-Match`).
* Rename only if the source ETag doesn't match a value you provide (`If-None-Match`).

Example ETag-based destination conditions:

* Rename only if the destination doesn't already exist.
* Rename only if the destination ETag matches or doesn't match a specific value.

Example time-based conditions:

* Rename only if the source has been modified since a specified time.
* Rename only if the source hasn't been modified since a specified time.

If any precondition fails, RenameObject returns a precondition failed error and doesn't rename the object.

## Rename an object

This section walks through the typical steps to use RenameObject safely with CoreWeave AI Object Storage. You confirm bucket eligibility, ensure the calling principal has the right permissions, run the rename, and verify the result.

Here's the HTTP request syntax for the RenameObject API. Reviewing the syntax first helps you understand which headers map to the precondition and idempotency options described in [Preconditions and safeguards](#preconditions-and-safeguards). Replace `[DESTINATION-KEY]`, `[BUCKET-NAME]`, and `[SOURCE-KEY]` with your destination key, bucket name, and source key. Include only the conditional headers and idempotency token you need, replacing each `[...-IF-...]` placeholder with the matching ETag or timestamp and `[IDEMPOTENCY-TOKEN]` with a client-generated token for safe retries. Make sure to use the correct endpoint URL for your CoreWeave AI Object Storage bucket.

```http theme={"system"}
PUT /[DESTINATION-KEY]?renameObject HTTP/1.1
Host: [BUCKET-NAME].cwobject.com
x-amz-rename-source: [SOURCE-KEY]
If-Match: [DESTINATION-IF-MATCH]
If-None-Match: [DESTINATION-IF-NONE-MATCH]
If-Modified-Since: [DESTINATION-IF-MODIFIED-SINCE]
If-Unmodified-Since: [DESTINATION-IF-UNMODIFIED-SINCE]
x-amz-rename-source-if-match: [SOURCE-IF-MATCH]
x-amz-rename-source-if-none-match: [SOURCE-IF-NONE-MATCH]
x-amz-rename-source-if-modified-since: [SOURCE-IF-MODIFIED-SINCE]
x-amz-rename-source-if-unmodified-since: [SOURCE-IF-UNMODIFIED-SINCE]
x-amz-client-token: [IDEMPOTENCY-TOKEN]
```

For API details, refer to [AI Object Storage S3 compatibility](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#s3renameobject).

### Confirm bucket eligibility

Before you run the rename, confirm the bucket supports RenameObject. The operation fails if any of the following requirements aren't met.

Make sure the bucket meets the following requirements:

* The bucket is a CoreWeave AI Object Storage bucket.
* Versioning has never been enabled on the bucket.
* Both the source and destination keys are in the same bucket.

### Ensure permissions

A rename operation removes the source key and creates the destination key, so the calling principal needs permissions covering both actions.

The principal calling RenameObject must be allowed to perform delete (`s3:DeleteObject`) on the source and put (`s3:PutObject`) on the destination for the relevant bucket and relevant key prefixes, according to your AI Object Storage organization access policies and bucket policies.

In many environments, this is combined with broader AI Object Storage permissions such as read and delete access to the source key and write or overwrite permissions on the destination key, as expressed in your policies.

#### Example policy

The following example shows a pattern for allowing rename operations within a single bucket:

Replace `[BUCKET-NAME]` with the name of your bucket, `[ORG-ID]` with your organization's ID, `[USER-ID]` with the console user's ID, and `[SAML-GROUP-ID]` with the SAML group ID.

```json title="Example bucket policy allowing rename operations within a single bucket" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRenameObjectWithinBucket",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    }
  ]
}
```

> [!WARNING]
>
> Include a `cw:PrincipalOrgID` condition as an extra safety measure when you grant bucket access to named principals.

If the source and destination require different permissions, you can use multiple statements in the bucket policy to allow the different permissions. Make sure that `s3:DeleteObject` is granted on the source and `s3:PutObject` is granted on the destination for the relevant bucket and relevant key prefixes, according to your AI Object Storage organization access policies and bucket policies.

For more information, see examples of [organization policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/examples.md) and [bucket policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md#example-policies).

### Run the rename operation

Use the Cloud Console, the AWS CLI, or Boto3 to rename an object. The CLI and SDK tabs accept optional precondition parameters (ETag or time-based conditions) and an idempotency token as needed.

> [tab] Cloud Console
>
> 1. In the [Cloud Console](https://console.coreweave.com/object-storage/buckets), open the bucket.
> 2. Select the object you want to rename.
> 3. Choose **Rename** and enter the new object key.
>
> Renames are performed within the same bucket. The bucket eligibility and permissions requirements described in this guide apply.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]` with the bucket name, `[DESTINATION-KEY]` with the new object key, and `[SOURCE-KEY]` with the current object key. The server URL-decodes the `--rename-source` value, so URL-encode the source key to safely transmit reserved characters such as `%`.
>
> ```bash theme={"system"}
> aws s3api rename-object \
>   --bucket [BUCKET-NAME] \
>   --key [DESTINATION-KEY] \
>   --rename-source [SOURCE-KEY]
> ```

> [tab] Boto3
>
> Replace `[BUCKET-NAME]` with the bucket name, `[DESTINATION-KEY]` with the new object key, `[SOURCE-KEY]` with the current object key, and `[AVAILABILITY-ZONE]` with your bucket's Availability Zone.
>
> ```python theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='[AVAILABILITY-ZONE]',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3 = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> response = s3.rename_object(
>     Bucket='[BUCKET-NAME]',
>     Key='[DESTINATION-KEY]',
>     RenameSource='[SOURCE-KEY]'
> )
>
> print(f"Object renamed. ETag: {response['ETag']}")
> ```

> [tab] HTTP
>
> Replace `[BUCKET-NAME]`, `[DESTINATION-KEY]`, and `[SOURCE-KEY]` with the appropriate values. The server URL-decodes the `x-amz-rename-source` value, so URL-encode the source key to safely transmit reserved characters such as `%`. The `If-Match` header is optional. If you include it, replace `[ETAG]` with the source object's current ETag to guard against a race condition.
>
> ```http theme={"system"}
> PUT /[DESTINATION-KEY]?renameObject HTTP/1.1
> Host: [BUCKET-NAME].cwobject.com
> x-amz-rename-source: [SOURCE-KEY]
> If-Match: [ETAG]
> ```

> [!NOTE]
>
> **s3cmd and s5cmd**
>
> The s3cmd `mv` command and s5cmd don't support the atomic RenameObject API. s3cmd `mv` performs a copy-and-delete operation instead. Use the AWS CLI or Boto3 for atomic RenameObject operations.

### Response

A successful rename returns HTTP `200` with the object's ETag:

```http theme={"system"}
HTTP/1.1 200 OK
ETag: "1b2cf535f27731c97434645a985325"
```

### Common errors

| Error | Cause |
| - | - |
| `PreconditionFailed` | ETag or time-based condition not met |
| `NoSuchKey` | Source object doesn't exist |
| `InvalidBucketVersion` | Bucket has versioning enabled or was previously enabled |
| `InvalidRequest` | The `x-amz-rename-source` value contains malformed percent-encoding |

### Verify the rename

After a successful response, the object is accessible under its new key and the old key is gone. To confirm this, read from both keys:

* A GET to the new key returns the object.
* A GET to the old key returns a not-found error (for buckets where rename is supported).

If you're using [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md):

* Use the LOTA endpoint (`http://cwlota.com`) for the rename request.
* The rename operation updates the metadata or index mapping so that cached content is immediately accessible through the new key.
* Cache entries under the old key are invalidated or remapped so that subsequent reads don't serve stale data from the old name.

## Example workflows

These examples illustrate how RenameObject fits typical AI Object Storage workflows. The following sections describe common patterns for checkpoints, media or batch outputs, and time-based data.

### Promote a temporary checkpoint to a final name

Pattern: rename `foo.ckpt.tmp` to `foo.ckpt` at the end of a training run.

Your training job writes checkpoints to a temporary key, such as `checkpoints/run-123/epoch-10.ckpt.tmp`. After you verify the checkpoint, call RenameObject to move it to `checkpoints/run-123/epoch-10.ckpt`. Downstream jobs and inference pipelines read from the stable, final key without any copy cost or latency.

### Finalize media or batch outputs

Pattern: rename final artifacts out of staging prefixes for media processing or ETL.

Write intermediate artifacts under a staging prefix, such as `media/staging/job-42/output.mp4`. When validation succeeds, rename to `media/final/output-2025-12-01.mp4`. Monitoring, distribution, or analytics systems are configured to watch the final prefix only.

### Rotate logs or time-based data

Pattern: lock an hourly or daily prefix by renaming to a final form.

Write logs under `logs/ingest/2025/12/12/10/`. When the ingest window closes, rename the prefix contents one object at a time into a finalized prefix such as `logs/final/2025/12/12/10/`. Consumers rely on the final prefix, with RenameObject ensuring each file appears atomically under its new name.

The RenameObject API doesn't support renaming an entire prefix at once. Use batch clients or pipeline logic to apply RenameObject per object for prefix-scale workflows.

## Support

If you need help with RenameObject, contact [CoreWeave support](https://docs.coreweave.com/support.md).

When you open a case, include the following information:

* The bucket name.
* The source and destination keys.
* Approximate timestamp of the request.
* Any relevant request IDs or error messages from your client or logs.
