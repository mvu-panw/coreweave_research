# AI Object Storage S3 compatibility

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3

# AI Object Storage S3 compatibility

> Supported S3-compatible features and calls for CoreWeave AI Object Storage

This reference lists the supported S3-compatible API features and calls for CoreWeave AI Object Storage. Use it to confirm which S3 operations and headers AI Object Storage accepts when you store, manage, retrieve, and manipulate objects in buckets. It's intended for developers and operators who integrate S3-compatible tools, SDKs, or custom clients with CoreWeave AI Object Storage.

> [!WARNING]
>
> CoreWeave AI Object Storage compatibility with S3 features and the S3 API are subject to change.

## Supported tools

CoreWeave AI Object Storage works with any S3-compatible client that supports Signature V4 and virtual-hosted style addressing. The following tools are tested and documented:

* [AWS CLI](https://aws.amazon.com/cli/): Standard S3 command-line interface. See [Manage buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools) for configuration.
* [s3cmd](https://s3tools.org/s3cmd): Command-line tool for S3-compatible services. See [Manage buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#configure-tools) for configuration.
* [Boto3](https://docs.aws.amazon.com/boto3/latest/): AWS SDK for Python. See [Configure endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#full-configuration-examples) for setup.
* [s5cmd](https://github.com/coreweave/s5cmd) (CoreWeave fork): High-performance, parallel S3 tool. See [Manage buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools) for installation.
* [Cyberduck](https://cyberduck.io/): Graphical file transfer client. See [Use Cyberduck](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/cyberduck.md).
* [rclone](https://rclone.org/): File sync tool with S3 support. See [Versioned buckets with rclone](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md).
* [CoreWeave Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs): Infrastructure-as-code support. See [Use the CoreWeave Terraform provider](https://docs.coreweave.com/products/storage/object-storage/use-terraform-aws-provider.md).

> [!NOTE]
>
> Upstream [s5cmd](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoints, which AI Object Storage doesn't support. Use the [CoreWeave fork](https://github.com/coreweave/s5cmd) instead.

## S3 features

CoreWeave AI Object Storage supports several features for object management.

### Authentication

Every interaction with CoreWeave AI Object Storage is either authenticated or anonymous. When authenticated, AI Object Storage uses Signature Version 4 authentication.

For details about using AWS CLI, Boto3, and s3cmd with Signature V4, see [Using Signature Version 4](#use-signature-v4-with-aws-cli). For more information, see the S3 [Authenticating Requests](https://docs.aws.amazon.com/AmazonS3/latest/API/) guide.

### Read after write consistency

CoreWeave AI Object Storage guarantees consistency. Objects can be read immediately after writing.

### Bucket lifecycles

A bucket lifecycle defines actions applied to a group of objects, such as expiring objects after a set period. Use these API calls to manage lifecycles:

* [`s3:PutBucketLifecycleConfiguration`](#s3putbucketlifecycleconfiguration)
* [`s3:GetBucketLifecycleConfiguration`](#s3getbucketlifecycleconfiguration)
* [`s3:DeleteBucketLifeCycle`](#s3deletebucketlifecycle)

For supported actions, examples, and apply procedures, see [Bucket lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md).

### Bucket access policy

A bucket access policy grants or denies permissions to the bucket and the objects within it. It defines which actions are allowed or denied on the bucket and its objects, and by whom. Bucket access policies consist of one or more statements attached to a bucket in JSON format.

Use these API calls to manage bucket access policies:

* [`s3:PutBucketPolicy`](#s3putbucketpolicy)
* [`s3:GetBucketPolicy`](#s3getbucketpolicy)
* [`s3:DeleteBucketPolicy`](#s3deletebucketpolicy)

### Versioning

Versioning keeps multiple variants of an object in the same bucket. When enabled, all objects are assigned a unique version ID. This lets you retrieve, restore, or delete specific versions of an object. Versioning is disabled by default. Use these API calls to manage versioning:

* [`s3:PutBucketVersioning`](#s3putbucketversioning)
* [`s3:GetBucketVersioning`](#s3getbucketversioning)
* [`s3:ListObjectVersions`](#s3listobjectversions)

Other API calls are also version-aware, as noted in their descriptions in the following sections. For more information, see the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html).

### Presigned URLs

Presigned URLs let you grant temporary access to an object in a bucket without requiring the user to have access credentials. You can generate a presigned URL for any S3 API call that requires authentication, such as `s3:GetObject` or `s3:PutObject`. When a user accesses the presigned URL, they can perform the specified action on the object without authenticating with their own credentials.

For more information, see [the S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html).

#### Generate a presigned URL with the AWS CLI

Replace `[BUCKET-NAME]` with your bucket name, `[OBJECT-KEY]` with the object key, and `[EXPIRES-IN]` with the number of seconds the URL remains valid.

```bash theme={"system"}
aws s3 presign s3://[BUCKET-NAME]/[OBJECT-KEY] --expires-in [EXPIRES-IN] --endpoint-url https://cwobject.com
```

#### Generate a presigned URL with Boto3

Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your CoreWeave AI Object Storage credentials, `[AVAILABILITY-ZONE]` with your bucket's Availability Zone, and `[BUCKET-NAME]` and `[OBJECT-KEY]` with the target bucket and object key.

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
```

```python theme={"system"}
import os
import boto3
from botocore.client import Config

boto_config = Config(
    region_name='[AVAILABILITY-ZONE]',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)

# Presigned URL for downloading an object
download_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': '[BUCKET-NAME]', 'Key': '[OBJECT-KEY]'},
    ExpiresIn=3600
)

# Presigned URL for uploading an object
upload_url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket': '[BUCKET-NAME]', 'Key': '[OBJECT-KEY]'},
    ExpiresIn=3600
)

print(download_url)
print(upload_url)
```

### Checksum algorithms

CoreWeave AI Object Storage supports the same checksum algorithms as AWS S3 for verifying object integrity on upload and download:

| Algorithm | Value to use in requests |
| - | - |
| CRC-64/NVME | `CRC64NVME` |
| CRC-32 | `CRC32` |
| CRC-32C | `CRC32C` |
| SHA-1 | `SHA1` |
| SHA-256 | `SHA256` |

For details on how to use checksums when uploading and downloading objects, see [Checking object integrity](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html) in the AWS S3 documentation.

### Conditional writes

CoreWeave AI Object Storage supports conditional writes for [`s3:PutObject`](#s3putobject), [`s3:CompleteMultiPartUpLoad`](#s3completemultipartupload), [`s3:CopyObject`](#s3copyobject), and [`s3:RenameObject`](#s3renameobject). Conditional writes use HTTP precondition headers to make writes atomic and to prevent accidental overwrites.

| Header | Accepted value | Behavior |
| - | - | - |
| `If-None-Match` | `*` | Write only if no object exists at the key. Returns `412 Precondition Failed` if the object exists. |
| `If-Match` | ETag string | Write only if the object's current ETag matches. Returns `412 Precondition Failed` if the ETag doesn't match. |

**Constraints:**

* `If-None-Match` only accepts the value `*`. Passing an ETag value returns `400 InvalidRequest`.
* When two concurrent requests use `If-None-Match: *` for the same key, one succeeds and the other returns `409 ConditionalRequestConflict`. Retry on `409`.

`s3:RenameObject` supports a richer set of conditional headers, including separate source and destination preconditions and time-based conditions, in addition to `If-None-Match` and `If-Match`. For details, see [Preconditions and safeguards](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md#preconditions-and-safeguards).

For the HTTP conditional request specification, see [RFC 7232](https://datatracker.ietf.org/doc/html/rfc7232). For usage examples, including the read-then-write workflow for `If-Match`, see [Use conditional requests](https://docs.coreweave.com/products/storage/object-storage/buckets/conditional-requests.md).

### Storage classes

CoreWeave AI Object Storage accepts the `x-amz-storage-class` header on `s3:PutObject`, `s3:CreateMultiPartUpLoad`, and `s3:CopyObject`, and reports the storage class of each object in `s3:HeadObject` and object listings.

| Value | Description |
| - | - |
| `STANDARD` | The default for new objects. Optimized for frequent access and low-latency reads and writes. |
| `STANDARD_IA` | The Archive storage class, for infrequently accessed data. Requires Archive availability in the bucket's Availability Zone and `STANDARD_IA` quota for the organization. |

Requests that specify `STANDARD_IA` return `InvalidStorageClass` if Archive isn't available in the bucket's Availability Zone, or if the organization has no `STANDARD_IA` quota.

Objects in `STANDARD_IA` are read with an ordinary `s3:GetObject` request; there is no restore or rehydration step, and reading an object doesn't return it to `STANDARD`. For guidance on moving data between storage classes, see [Use the Archive storage class](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md).

## S3 API compatibility notes

The following S3 behaviors differ from AWS S3 or are not supported:

* **S3 Batch Operations are not supported.** Use the AWS CLI, Boto3, or s3cmd to perform bulk operations. For deleting all objects in a bucket, see [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md).
* **S3 event notifications are not supported.** Bucket-level event triggers (such as `s3:ObjectCreated`) are not available.
* **`Transition` lifecycle actions are not supported.** Use `Expiration`, `NoncurrentVersionExpiration`, and `AbortIncompleteMultipartUpload` actions instead. Within the `STANDARD` storage class, Hot, Warm, and Cold billing classifications are applied automatically based on access patterns; see [Cost management](https://docs.coreweave.com/products/storage/object-storage/about.md#cost-management). To move objects into the Archive storage class (`STANDARD_IA`), set the storage class explicitly on a write or copy, or enable Automated Archive on the bucket; see [Use the Archive storage class](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md).
* **Lifecycle rules bypass `Deny` statements in bucket and organization access policies.** Lifecycle deletions run as a privileged service action. A `Deny` on `s3:DeleteObject` does not block lifecycle-initiated deletions. For more information, see [Understand automated deletion](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md#understand-automated-deletion).
* **Object Lock is not supported.** `s3:GetObjectLegalHold`, `s3:PutObjectLegalHold`, `s3:GetObjectRetention`, and `s3:PutObjectRetention` all return `NotImplemented`.
* **Access control list (ACL) write operations are not supported.** `s3:PutBucketAcl` and `s3:PutObjectAcl` return `NotImplemented`. `s3:GetBucketACL` and `s3:GetObjectAcl` are supported for reads.

## Object key guidance

An object key is the unique identifier for an object within a bucket. Because CoreWeave AI Object Storage is S3-compatible, object keys follow the same conventions as Amazon S3.

* **Encoding:** Object keys are treated as sequences of UTF-8 characters. Any UTF-8 string is a syntactically valid key.
* **Structure:** Object keys are flat strings, not directories. Slashes (`/`) are conventional prefix separators that S3-compatible tools and the Cloud Console render as folders, but they have no filesystem semantics on the server.
* **Case sensitivity:** Object keys are case sensitive. `Photos/tree.png` and `photos/tree.png` are two different objects.
* **Reserved and special characters:** Some characters have reserved meanings in URLs, shells, or XML responses (for example, `%`, `&`, `?`, `#`, `\`, `{`, `}`, `^`, `` ` ``, `[`, `]`, `"`, `<`, `>`, `|`, non-printable ASCII, and characters outside 7-bit ASCII). These characters are valid in keys but often need URL encoding by the client and can be awkward to handle across tools. Prefer ASCII letters, digits, and the safe punctuation characters `!`, `-`, `_`, `.`, `*`, `'`, `(`, `)`, and `/`.
* **Rename operations:** The server URL-decodes the `x-amz-rename-source` header, so when you call `s3:RenameObject` with a source key that contains reserved characters such as `%`, URL-encode it before sending. See [Rename objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md).
* **Prefix filters:** Access policies, lifecycle rules, and inventory reports match on raw key prefixes. A trailing slash in a prefix (for example, `projects/`) restricts the match to keys under that logical folder.

For the full character-class guidance that CoreWeave AI Object Storage follows, see the Amazon S3 [object key naming guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html).

For bucket name rules, which are stricter than object key rules, see [About buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/about.md).

## API calls

The following sections list the supported S3 API calls, the permissions each one requires, and any CoreWeave-specific behavior. Each API call requires permission to perform the related actions. The action names **don't always** match the API calls, and some perform **multiple** actions, which in turn require their related permission.

For example, copying an object requires permission to perform **both** `s3:PutObject` and `s3:GetObject` actions. When you plan bucket access policies, refer to the required permission listed in each API call description. For a complementary list of actions mapped to these API calls, see [Bucket Access Policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#required-policies-and-actions).

CoreWeave AI Object Storage supports standard S3 tools through the S3 API. For more information, see these resources:

* [s3api reference documentation](https://docs.aws.amazon.com/cli/latest/reference/s3api/)
* [S3 tools documentation](https://s3tools.org/usage)
* [Boto3 Python SDK for AWS documentation](https://docs.aws.amazon.com/boto3/latest/)

### `s3:AbortMultiPartUpLoad`

**Requires permission to**: `s3:AbortMultipartUpload`

Stop an in-progress multi-part upload (MPU).

No new parts can be uploaded to that MPU ID. Incomplete uploads are removed.

### `s3:CompleteMultiPartUpLoad`

**Requires permission to**: `s3:PutObject`

Complete a multi-part upload by listing all parts in the final object in ascending order.

Any parts that are uploaded but not specified in this call are discarded.

Conditional write headers (`If-None-Match`, `If-Match`) are supported. See [Conditional writes](#conditional-writes).

### `s3:CopyObject`

**Requires permission to**: `s3:GetObject`, `s3:PutObject`

Copy an object in object storage.

The following conditional write headers are supported:

* Source precondition headers (`x-amz-copy-source-if-match`, `x-amz-copy-source-if-none-match`, `x-amz-copy-source-if-modified-since`, `x-amz-copy-source-if-unmodified-since`)
* Destination conditional write headers (`If-Match`, `If-None-Match`)

For more information, see [Conditional writes](#conditional-writes).

### `s3:CreateBucket`

**Requires permission to**: `s3:CreateBucket`

Create a bucket with a valid CoreWeave AI Object Storage access key.

Anonymous requests aren't allowed. The bucket creator becomes the owner. **`LocationConstraint` must be supplied.**

Set `LocationConstraint` to an Availability Zone that supports AI Object Storage:

> [accordion] Availability Zones that support AI Object Storage
>
> > [tab] US-CENTRAL
> >
> > * `US-CENTRAL-05A`
> > * `US-CENTRAL-06A`
> > * `US-CENTRAL-07A`
> > * `US-CENTRAL-08A`
> > * `US-CENTRAL-08B`
>
> > [tab] US-EAST
> >
> > * `US-EAST-01A`
> > * `US-EAST-02A`
> > * `US-EAST-03A`
> > * `US-EAST-04A`
> > * `US-EAST-04B`
> > * `US-EAST-06A`
> > * `US-EAST-08A`
> > * `US-EAST-13A`
> > * `US-EAST-14A`
> > * `US-EAST-15A`
> > * `US-EAST-17A`
>
> > [tab] US-WEST
> >
> > * `RNO2A`
> > * `US-WEST-01A`
> > * `US-WEST-04A`
> > * `US-WEST-09B`
> > * `US-WEST-10A`
>
> > [tab] CA-EAST
> >
> > * `CA-EAST-01A`
>
> > [tab] EU-NORTH
> >
> > * `EU-NORTH-05A`
>
> > [tab] EU-SOUTH
> >
> > * `EU-SOUTH-03B`
> > * `EU-SOUTH-04A`
>
> Learn more about [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

> [accordion] Bucket naming rules
>
> Bucket names must be globally unique and adhere to the following rules:
>
> * **Length:** 3 to 63 characters.
> * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> * **Prohibited patterns:** Cannot start with `xn--`.
> * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

### `s3:CreateMultiPartUpLoad`

**Requires permission to**: `s3:PutObject`

Initiate a multi-part upload (MPU) and return an MPU ID. After starting a multi-part upload:

* Upload parts with `s3:UploadPart`
* Finalize the upload with `s3:CompleteMultipartUpload`
* Stop the upload with `s3:AbortMultipartUpload`

### `s3:DeleteBucket`

**Requires permission to**: `s3:DeleteBucket`

Delete a bucket.

The bucket must be completely empty without any object versions or delete markers.

### `s3:DeleteBucketLifeCycle`

**Requires permission to**: `s3:DeleteLifecycleConfiguration`

Delete the lifecycle configuration from a bucket.

### `s3:DeleteBucketPolicy`

**Requires permission to**: `s3:DeleteBucketPolicy`

Remove a bucket access policy from a bucket.

### `s3:DeleteBucketTagging`

**Requires permission to**: `s3:DeleteBucketTagging`

Delete tags from a bucket.

### `s3:DeleteObject`

**Requires permission to**: `s3:DeleteObject`, and `s3:DeleteObjectVersion` when a `versionId` is specified

Remove an object, or specific version of an object, from a bucket.

### `s3:DeleteObjects`

**Requires permission to**: `s3:DeleteObject`, `s3:DeleteObjectVersion`

Delete up to 1,000 objects per call.

Quiet mode returns only errors, while verbose mode returns a response for every object. Objects not found return `success`.

### `s3:DeleteObjectTagging`

**Requires permission to**: `s3:DeleteObjectTagging`

Remove all tags on an object.

### `s3:GetBucketACL`

**Requires permission to**: `s3:ListBucket`

Return the access control list of a bucket.

### `s3:GetBucketLifecycleConfiguration`

**Requires permission to**: `s3:GetLifecycleConfiguration`

Return the lifecycle configuration for a bucket.

### `s3:GetBucketLocation`

**Requires permission to**: `s3:GetBucketLocation`

Return the bucket's Region.

### `s3:GetBucketPolicy`

**Requires permission to**: `s3:GetBucketPolicy`

Return the policy for a bucket.

### `s3:GetBucketTagging`

**Requires permission to**: `s3:GetBucketTagging`

Get tags for a bucket.

### `s3:GetBucketVersioning`

**Requires permission to**: `s3:GetBucketVersioning`

Get the versioning state for the bucket, or empty if versioning is not enabled.

### `s3:GetObject`

**Requires permission to**: `s3:GetObject`

Retrieve an object.

Anonymous `GET` requests, [`Range` reads](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Range), and [`ETag`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag) matching are supported.

The [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) caches `GET` requests by default. To modify this behavior, use the [`Cache-Control`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) HTTP header:

* With `no-cache` (`Cache-Control: no-cache`), LOTA queries the cache for the object but doesn't cache the `GET` request.
* With `no-store` (`Cache-Control: no-store`), LOTA fetches the object directly from the storage backend and doesn't cache it.

### `s3:GetObjectAcl`

**Requires permission to**: `s3:GetObject`

Return the access control list of an object.

### `s3:GetObjectAttributes`

**Requires permission to**: `s3:GetObject`

Get the metadata of a specified object.

### `s3:GetObjectTagging`

**Requires permission to**: `s3:GetObjectTagging`

Return the set of tags associated with an object.

### `s3:HeadBucket`

**Requires permission to**: `s3:ListBucket`

Determine if a bucket exists and you have permission to access it.

#### Return codes

* `200 OK`: The bucket exists and permission is allowed.
* `400 Bad Request`: The bucket name is invalid.
* `403 Forbidden`: Permission is denied.
* `404 Not Found`: The bucket doesn't exist.

### `s3:HeadObject`

**Requires permission to**: `s3:GetObject`

Get the metadata for the specified object.

### `s3:ListBuckets`

**Requires permission to**: `s3:ListAllMyBuckets`

Return a list of all buckets owned by the authenticated sender of the request.

### `s3:ListObjectsV2`

**Requires permission to**: `s3:ListBucket`

List objects in a bucket.

Lists up to 1,000 objects in a bucket per call. Use `ContinuationToken` in the response to list more than 1,000 objects.

### `s3:ListObjectVersions`

**Requires permission to**: `s3:ListBucket`

Return metadata on all versions or subsets of an object.

### `s3:ListParts`

**Requires permission to**: `s3:ListMultipartUploadParts`

List the uploaded parts for a specific multi-part upload.

### `s3:ListMultiPartUploads`

**Requires permission to**: `s3:ListBucketMultipartUploads`

List parts of a multi-part upload.

List up to 1,000 in-progress multi-part uploads for a given bucket.

### `s3:PutBucketLifecycleConfiguration`

**Requires permission to**: `s3:PutLifecycleConfiguration`

Create or replace a new lifecycle configuration for a bucket.

This overwrites the previous configuration. It doesn't merge them.

### `s3:PutBucketPolicy`

**Requires permission to**: `s3:PutBucketPolicy`

Apply the provided policy to a bucket.

If no policy exists, access to create a new policy is granted when the user's Org ID matches the bucket's organization.

### `s3:PutBucketTagging`

**Requires permission to**: `s3:PutBucketTagging`

Set up to 10 tags for a bucket.

Keys can be up to 128 UTF-8 characters. Values can be up to 256 characters.

### `s3:PutBucketVersioning`

**Requires permission to**: `s3:PutBucketVersioning`

Enable or suspend versioning for a bucket.

> [!WARNING]
>
> If you use an object expiration lifecycle configuration on a non-versioned bucket and want to maintain the same permanent delete behavior after you enable versioning, you must add a separate lifecycle rule to delete noncurrent object versions.

### `s3:PutObject`

**Requires permission to**: `s3:PutObject`

Add an object to a bucket. The `x-amz-meta` and `Expires` headers are supported. An ETag is returned for every uploaded object.

Conditional write headers (`If-None-Match`, `If-Match`) are supported. See [Conditional writes](#conditional-writes).

### `s3:PutObjectTagging`

**Requires permission to**: `s3:PutObjectTagging`

Set up to 10 tags on an object.

### `s3:RenameObject`

**Requires permission to**: `s3:PutObject` and `s3:DeleteObject`

Rename an object, subject to the following constraints:

* The source and destination keys must be in the same bucket.
* The bucket must **not** have versioning enabled, either currently or in the past.
* Each request supports one rename operation for one object key. Bulk or prefix-level rename operations aren't supported.

| Parameter | Description |
| - | - |
| Bucket | The bucket contains both the source and destination keys. |
| Source key | The current object key, sent in the `x-amz-rename-source` header. The server URL-decodes it, so URL-encode keys with reserved characters such as `%`. |
| Destination key | The new object key in the same bucket (for example, `checkpoints/model.ckpt`). |
| Idempotency token | An optional client-supplied token that makes the operation idempotent across retries. The same token and parameters don't produce multiple renames. |

Conditional headers are supported, including ETag and time-based conditions for both source and destination. See [Conditional writes](#conditional-writes) for details.

Example HTTP request:

```http theme={"system"}
PUT /destinationname.txt?renameObject HTTP/1.1
Host: my-bucket
If-Match: "d41d8cd98f00b204e9800998ecf8427e"
x-amz-rename-source: sourcename.txt
```

For more information, see [Rename Objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md).

### `s3:UploadPart`

**Requires permission to**: `s3:PutObject`

Upload a part of a multi-part upload.

A multi-part upload can contain between 1 and 10,000 parts. A part number uniquely identifies each part and defines its position within the object. If you reuse a part number, it overwrites the previously uploaded part. Each part must be at least 5 MB, except the last part.

### `s3:UploadPartCopy`

**Requires permission to**: `s3:GetObject`, `s3:PutObject`

Upload part of a multi-part upload, using an existing object as the source instead of providing new data.

You can also specify a range for the copied object.

## Use Signature V4 with AWS CLI

To use Signature V4 with the AWS CLI, set the configuration with `aws`:

```bash title="AWS CLI" theme={"system"}
aws configure set default.s3.signature_version s3v4
```

## Use Signature V4 with Boto3

To configure Signature V4 with Boto3, set `signature_version = s3v4` on the client's `Config` object. Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your CoreWeave AI Object Storage credentials, and `[AVAILABILITY-ZONE]` with your bucket's Availability Zone (for example, `US-EAST-04A`).

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
```

```python theme={"system"}
import os
import boto3
from botocore.client import Config

boto_config = Config(
    signature_version='s3v4',
    region_name='[AVAILABILITY-ZONE]',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)
```

## Use Signature V4 with S3Cmd

Signature V4 is the default for S3cmd.

> [!WARNING]
>
> `s3cmd` often simplifies its process by mapping commands to multiple actions. For this reason, a single S3cmd command can map to multiple different required permissions.

## Server-side encryption with customer-provided keys (SSE-C)

CoreWeave AI Object Storage supports server-side encryption with customer-provided keys (SSE-C). SSE-C lets you encrypt your data using keys that you provide and manage. The following sections describe the required request headers, example requests for upload, download, and copy, and the response headers and error codes you can expect.

Before you use these examples, [generate a 32-byte key and store it securely](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/use-sse-c.md#generate-encryption-keys).

### SSE-C headers

When using SSE-C, include the following headers in your requests:

* `x-amz-server-side-encryption-customer-algorithm`: Must be set to `AES256`.
* `x-amz-server-side-encryption-customer-key`: Your 256-bit (32-byte) encryption key in base64-encoded format.
* `x-amz-server-side-encryption-customer-key-md5`: MD5 hash of your encryption key in base64-encoded format.

### Upload with SSE-C

Replace `$BASE64_KEY` with your base64-encoded encryption key. Replace `[BUCKET-NAME]` with the bucket name, `[OBJECT-KEY]` with the object key, and `[LOCAL-FILE-PATH]` with the path to the file you want to upload.

```bash theme={"system"}
# Upload an object with SSE-C
curl -X PUT \
  -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
  -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
  -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
  -T [LOCAL-FILE-PATH] \
  "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]"
```

### Download with SSE-C

```bash theme={"system"}
# Download an object with SSE-C
curl -X GET \
  -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
  -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
  -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
  "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]"
```

### Copy with SSE-C

Replace `[SOURCE-BUCKET-NAME]` and `[SOURCE-OBJECT-KEY]` with the source bucket name and object key. Replace `[DEST-BUCKET-NAME]` and `[DEST-OBJECT-KEY]` with the destination bucket name and object key.

```bash theme={"system"}
# Copy an object with SSE-C
curl -X PUT \
  -H "x-amz-copy-source: /[SOURCE-BUCKET-NAME]/[SOURCE-OBJECT-KEY]" \
  -H "x-amz-copy-source-server-side-encryption-customer-algorithm: AES256" \
  -H "x-amz-copy-source-server-side-encryption-customer-key: $BASE64_KEY" \
  -H "x-amz-copy-source-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
  -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
  -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
  -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
  "https://[DEST-BUCKET-NAME].cwobject.com/[DEST-OBJECT-KEY]"
```

### SSE-C response headers

When using SSE-C, the following headers are returned in responses:

* `x-amz-server-side-encryption-customer-algorithm`: The encryption algorithm used.
* `x-amz-server-side-encryption-customer-key-md5`: MD5 hash of the encryption key used.

### SSE-C error codes

Common SSE-C error codes:

* `InvalidArgument`: The encryption key is not 256 bits (32 bytes).
* `InvalidRequest`: The encryption key MD5 hash doesn't match.
* `AccessDenied`: The provided encryption key doesn't match the one used for upload.

For more information about SSE-C, see the [SSE-C concept guide](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md) and [how to implement SSE-C](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/use-sse-c.md).
