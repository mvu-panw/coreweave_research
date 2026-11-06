# Versioned buckets

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets

# Versioned buckets

> Manage versioned buckets with rclone and the AWS CLI.

Versioned buckets are a feature of CoreWeave AI Object Storage that lets you store multiple versions of the same object. This is useful for backups, version control, and audit trails. Rclone is a command-line tool for managing objects in CoreWeave AI Object Storage.

You'll also learn:

* When to use the AWS CLI instead of rclone.
* How rclone handles versioned objects differently than AWS CLI.
* Which command-line flags improve performance.
* When to contact CoreWeave Storage Engineering for help.

It's important to understand the specific behaviors of rclone commands and how they relate to the AWS CLI and underlying S3-compatible API. These concepts are particularly relevant when you use rclone to migrate data between versioned buckets. See [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md) for more information.

## Create a versioned bucket

This guide uses the AWS CLI to create the bucket and enable versioning, then uses rclone to manage its objects and versions. Although rclone supports bucket creation, this workflow sets `no_check_bucket = true` so rclone doesn't attempt to check or create buckets during operations.

Before you begin, [install and configure the AWS CLI](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools) to use the `cw` profile.

Creating a versioned bucket requires two API operations. You can't enable versioning in the `CreateBucket` request. Create the bucket first, then enable versioning with `PutBucketVersioning` before uploading objects.

To create a versioned bucket with the AWS CLI, follow these steps:

1. Create a bucket. Replace `[BUCKET-NAME]` with your bucket name and `[AVAILABILITY-ZONE]` with your Availability Zone (AZ) in uppercase, exactly as shown in the [Availability Zone list](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

   ```bash theme={"system"}
   aws s3api create-bucket \
     --bucket [BUCKET-NAME] \
     --region [AVAILABILITY-ZONE] \
     --create-bucket-configuration LocationConstraint=[AVAILABILITY-ZONE] \
     --profile cw
   ```

   > [accordion] Bucket naming rules
   >
   > Bucket names must be globally unique and adhere to the following rules:
   >
   > * **Length:** 3 to 63 characters.
   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
   > * **Prohibited patterns:** Cannot start with `xn--`.
   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

   The bucket name must be unique across CoreWeave AI Object Storage, including all Availability Zones.

   `LocationConstraint` is required. Use the same Availability Zone for `--region` and `LocationConstraint`.

2. Wait approximately one minute for the bucket's DNS name to propagate. If you try to use the bucket immediately after creating it, you may encounter errors.

3. Enable versioning on the bucket. Replace `[BUCKET-NAME]` with your bucket name.

   ```bash theme={"system"}
   aws s3api put-bucket-versioning \
     --bucket [BUCKET-NAME] \
     --versioning-configuration Status=Enabled \
     --profile cw
   ```

After you complete these steps, the bucket is ready to retain multiple versions of each object.

## Configure rclone

To set up rclone, configure your credentials, and set up Workload Identity Federation, first see [Configure rclone for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/rclone.md).

To configure rclone for versioned buckets, create an rclone **remote** in `~/.config/rclone/rclone.conf`. Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your AI Object Storage access key credentials.

```ini title="~/.config/rclone/rclone.conf" theme={"system"}
[default]
type = s3
provider = Other
access_key_id = [ACCESS-KEY-ID]
secret_access_key = [SECRET-ACCESS-KEY]
endpoint = http://cwlota.com
force_path_style = false
no_check_bucket = true
```

> <sup>1</sup>Rclone can use multiple remotes to define different storage providers, each with a unique name. The remote in this example is named `default`. Learn more about rclone remotes [in the rclone documentation](https://rclone.org/s3/).

For optimal performance, always use the [LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md#overview) (`http://cwlota.com`) when running inside a CoreWeave cluster. The primary endpoint (`https://cwobject.com`) is available when running outside a CoreWeave cluster.

These settings are critical when configuring rclone for AI Object Storage:

* **type**: Must be `s3`.
* **provider**: Must be `Other`.
* **force\_path\_style**: Must be `false`. This forces rclone to use [virtual-hosted style URLs](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md). Path-style addressing is not supported.
* **no\_check\_bucket**: Set to `true` for this workflow. The AWS CLI creates the bucket first, so this setting prevents unnecessary bucket creation and existence checks during rclone operations.

## List objects

This section describes the two main rclone listing commands and when to use each.

Use `rclone ls` to get a quick overview of the contents of a bucket or prefix. It provides a simple listing of objects, but not directories. It shows only their size and path, without modification times. It's recursive by default.

You can list objects in a versioned bucket using the `rclone ls` and `rclone lsl` commands.

### List commands

`rclone lsl` provides a more detailed listing than `rclone ls`, including modification times. Like `rclone ls`, it is recursive by default and does not include directories. Use it when you need to see when files were last modified.

```bash theme={"system"}
rclone ls [REMOTE]:[BUCKET-NAME]
```

## Performance tuning flags

Use the following flags to reduce API calls and speed up rclone operations against large versioned buckets.

### `--fast-list` flag

For better performance with large buckets, use the `--fast-list` flag to reduce the number of API calls required. This flag fetches more data in each call at the cost of increased memory usage. It can speed up the overall listing process, but the initial directory scan might take longer before transfers begin, especially if the transfers themselves are fast compared to the listing.

* You can use this flag with both `rclone ls` and `rclone lsl` to speed up listings.
* You can combine it with `--use-server-modtime` to optimize performance.

```bash theme={"system"}
rclone lsl [REMOTE]:[BUCKET-NAME] --fast-list
```

### List all versions

The rclone `--s3-versions` flag lists all versions of objects.

```bash theme={"system"}
rclone lsl [REMOTE]:[BUCKET-NAME] --s3-versions
```

* You can combine this flag with `--fast-list` to optimize performance.
* `--use-server-modtime` does not work in conjunction with this flag, because rclone still needs to make individual HEAD requests to retrieve version metadata.

For an authoritative listing, rely on the version IDs provided by the S3 API rather than rclone's filename conventions. See [Distinguish delete markers with the AWS CLI](#distinguish-delete-markers-with-the-aws-cli).

### `--s3-version-deleted` flag

When you use the `--s3-version-deleted` flag, rclone includes delete markers in the listing. You can combine this with the `--s3-versions` flag to see all versions along with delete markers.

```bash theme={"system"}
rclone lsl [REMOTE]:[BUCKET-NAME] --s3-versions --s3-version-deleted
```

rclone modifies filenames to include version information. It reports a versioned `filename.ext` as `filename-vDATE-TIME-SEQUENCE.ext`. For example, a version of `myreport.txt` can appear as `myreport-v2026-08-14-163000-000.txt`. If your bucket contains objects that follow the same naming pattern, this convention can cause ambiguous filenames when you copy files.

For an authoritative object version listing, rely on the version IDs provided by the S3 API instead of the filename conventions used by rclone. [Use the AWS CLI for authoritative information](#when-to-use-aws-cli).

When you use the `--s3-version-deleted` flag, rclone lists delete markers as zero-byte objects. These represent the delete markers but aren't actual objects that can be retrieved. If you issue a standard `GET` request for that object without providing a specific version ID, Object Storage returns a `404` error, even though older versions still exist. See [Delete markers and soft deletes](#delete-markers-and-soft-deletes) for more details.

### Remove versions and delete markers

For general cleanup of accumulated old versions and delete markers, use `rclone backend cleanup-hidden REMOTE:`. This removes all hidden versions and delete markers, leaving only the current versions intact.

> [!WARNING]
>
> Use this command with caution. It permanently deletes data and cannot be undone.

The following sections explain how rclone interacts with versioned bucket metadata and delete markers, and when to use the AWS CLI for authoritative results.

### Extra metadata requests

If you use `rclone lsl` without the `--use-server-modtime` flag, the S3 API does not return all possible metadata for every object in the list result. This forces rclone to make additional HEAD requests to retrieve the missing information, such as modification times. These extra HEAD requests can be slow and expensive, especially with a large number of files.

If you set the log level to `NOTICE` or `DEBUG`, or if you include the `-vv` (very verbose) flag, you'll see these extra requests in the output of `rclone lsl`.

```bash theme={"system"}
rclone lsl [REMOTE]:[BUCKET-NAME]/ -vv
```

Partial output:

```text theme={"system"}
...
2025/09/24 10:42:01 DEBUG : my-remote:my-bucket-name/: Listing with bucket_name="my-bucket-name" delimiter="/" prefix=""
2025/09/24 10:42:02 DEBUG : file1.txt: Sent HEAD request
2025/09/24 10:42:02 DEBUG : file1.txt: HEAD request succeeded with status code 200
2025/09/24 10:42:02 NOTICE: file1.txt: Retrieving metadata with an extra HEAD request
2025/09/24 10:42:02 DEBUG : file2.txt: Sent HEAD request
2025/09/24 10:42:02 DEBUG : file2.txt: HEAD request succeeded with status code 200
2025/09/24 10:42:02 NOTICE: file2.txt: Retrieving metadata with an extra HEAD request
...
```

This flag is incompatible with the `--s3-versions` flag, which requires individual head requests for each object to retrieve version metadata.

To reduce the number of HEAD requests and improve performance, use one of these options:

* Use the `--use-server-modtime` flag to get the server's modification time without a separate HEAD request for each object. Also consider combining `--use-server-modtime` with `--fast-list` to further improve performance.
* Use the `ls` command instead of `lsl`. The `ls` command doesn't retrieve the modification time, which avoids the extra HEAD requests.

However, these rclone optimizations **do not apply** if you use the `--s3-versions` flag, because rclone still needs to make individual HEAD requests to retrieve version metadata.

### Delete markers and soft deletes

When you delete a file in a versioned S3 bucket, the bucket does not permanently remove it. Instead, the bucket creates a special object called a delete marker. This delete marker indicates that the object has been deleted, but the bucket still retains all previous versions of the object. This behavior is known as a "soft delete." In contrast, a "hard delete" happens when you delete a specific version.

When you list a versioned bucket through rclone, use the `--s3-version-deleted` flag to include delete markers in the output. Rclone reports these delete markers as zero-byte objects. These zero-byte entries **represent the delete markers but are not actual files** that can be retrieved. If you issue a standard `GET` request for that object without providing a specific version ID, Object Storage returns a `404` error, even though the older versions are still there.

The difference between a delete marker and rclone's zero-byte representation of that marker is important to understand because the difference can lead to confusion. Seeing a zero-byte entry in the listing might suggest that the object is still accessible, but in reality, it is not retrievable without specifying a version ID of a previous version.

Deleting a delete marker with rclone restores access to the most recent version of the object prior to the deletion. Removing the delete marker makes the latest non-deleted version the current version again.

### When to use AWS CLI

The AWS CLI provides definitive information about delete markers and versioned objects. It directly exposes the S3 API's structured output, which clearly distinguishes between actual object versions and delete markers.

When you attempt to `GET` an object that has been soft deleted, the response includes the `x-amz-delete-marker: true` header, clearly indicating that the object is a delete marker. Additionally, if you attempt to `GET` the version of the delete marker itself, the `Last-Modified: timestamp` shows when the bucket created the delete marker. The header is a more reliable way to confirm the presence of a delete marker than relying on rclone's **404 Not Found** response.

The AWS CLI [`list-object-versions` command](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-object-versions.html) returns structured output that shows `Versions[]` (real object versions) and `DeleteMarkers[]` (soft deletes). The current state of an object is the item with `IsLatest=true`. If the latest is a DeleteMarker, the object is soft-deleted.

To test a single object with the AWS CLI, use either [`head-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/head-object.html#head-object) or [`get-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-object.html#get-object), specifying the version ID if needed.

* If used without a version ID, soft-deleted objects return **404 Not Found** with an `x-amz-delete-marker: true` header.
* If you specify a version ID that is a delete marker, you get **200 OK** with the `x-amz-delete-marker: true` header.
* If you specify a version ID that is a real version, you get **200 OK** and the object content.

### Distinguish delete markers with the AWS CLI

Rclone's zero-byte representation of a delete marker can be ambiguous. For an authoritative view of which entries are real object versions and which are delete markers, use the AWS CLI, which exposes the S3 API's structured output directly.

The [`list-object-versions`](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-object-versions.html) command returns separate `Versions[]` (real object versions) and `DeleteMarkers[]` (soft deletes) arrays. The current state of an object is the item with `IsLatest=true`. If the latest item is in `DeleteMarkers[]`, the object is soft-deleted.

To check a single object, use [`head-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/head-object.html#head-object) or [`get-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-object.html#get-object), optionally with a specific version ID:

* Without a version ID, a soft-deleted object returns `404 Not Found` with an `x-amz-delete-marker: true` header.
* With a version ID that points to a delete marker, the response is `200 OK` with an `x-amz-delete-marker: true` header.
* With a version ID that points to a real version, the response is `200 OK` and the object content.

The `x-amz-delete-marker: true` header is a more reliable signal than rclone's `404 Not Found` response when you need to confirm whether an object has been soft-deleted.

### Precise recovery

For many common recovery scenarios and day-to-day operational contexts, rclone offers a self-service interface that balances capability with ease of use. It's a good choice when you need to get a file back quickly or reset the bucket to a clean slate of active versions without worrying about an accumulation of older, potentially unnecessary versions cluttering things up.

For precise recovery, use the AWS CLI rather than rclone. This applies when you need to:

* Recover a specific version for compliance or audit purposes.
* Have precise control over which versions are restored.
* Handle scenarios where delete markers are involved.

For these situations, use the AWS CLI as your diagnostic tool. It allows you to confidently discern between different versions, including those explicitly marked as deleted, and to execute precise, auditable recovery actions.

* [`aws s3api list-object-versions`](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-object-versions.html) to identify the latest non-deleted version
* [`aws s3api copy-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/copy-object.html#copy-object) to restore it to a new location
* [`get-object`](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-object.html#get-object) to retrieve it, so you can then re-upload it

Removing policy-controlled delete markers may require assistance from CoreWeave's storage engineering team. If you encounter issues removing delete markers, contact [CoreWeave support](https://docs.coreweave.com/support.md).
