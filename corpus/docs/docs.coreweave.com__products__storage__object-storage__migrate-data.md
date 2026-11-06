# Migrate data to AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/migrate-data

# Migrate data to AI Object Storage

> Use s5cmd or Rclone to migrate data to AI Object Storage

This guide explains how to copy data between AI Object Storage buckets using s5cmd and Rclone. Use it to move datasets into CoreWeave AI Object Storage so that your workloads can read and write to a high-performance, S3-compatible store.

You can also use [s3cmd](https://s3tools.org/s3cmd) or [Cyberduck](https://cyberduck.io/) to copy data to CoreWeave AI Object Storage.

You can also use the same approaches to transfer data from any S3-compatible storage service, such as AWS S3, Azure Blob Storage, or Google Cloud Storage.

## Choose a migration tool

| Tool | Best for | Notes |
| - | - | - |
| **s5cmd** | High-performance parallel transfers, and transfers involving [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md) | Recommended for most use cases. High default concurrency (256 workers). |
| **Rclone** | Complex sync operations, and transfers between diverse cloud providers | Do not use with [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md) because of known kernel panic issues. Safe for AI Object Storage, [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md), and external systems. |

## Prerequisites

Before you start, ensure you have the following:

1. The primary endpoint for AI Object Storage, `https://cwobject.com`, requires TLS v1.3. Ensure your S3-compatible tools and OpenSSL support TLS v1.3.
2. An [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) configured.
3. An access key and secret key for each bucket.

   For CoreWeave AI Object Storage, use either of these methods:

   * Create keys with [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md).
   * Create keys with an [API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md).

   If a bucket is on a different S3-compatible platform, such as AWS S3, Azure Blob Storage, or Google Cloud Storage, refer to the respective documentation to generate access keys.

## Migrate data with s5cmd

s5cmd is a high-performance, parallel S3 and local filesystem execution tool. CoreWeave maintains a [fork of s5cmd](https://github.com/coreweave/s5cmd) that defaults to virtual-style addressing for `cwobject.com` and `cwlota.com`, which is required for AI Object Storage.

> [!WARNING]
>
> **Use the CoreWeave fork of s5cmd**
>
> The upstream s5cmd defaults to path-style addressing, which AI Object Storage doesn't support. You must use the [CoreWeave fork](https://github.com/coreweave/s5cmd) for compatibility with AI Object Storage.

### Install s5cmd

1. Download the latest release binary for your platform from the [CoreWeave s5cmd releases page](https://github.com/coreweave/s5cmd/releases).

   The CoreWeave fork is based on the latest upstream s5cmd and the only difference is that it defaults to virtual-style addressing for AI Object Storage. Other S3-compatible backends are unaffected, so this fork can safely replace any existing s5cmd installation.

2. After downloading, make the binary executable and move it to a directory in your `PATH`:

   ```bash theme={"system"}
   chmod +x s5cmd && sudo mv s5cmd /usr/local/bin/
   ```

3. Verify the installation:

   ```bash theme={"system"}
   s5cmd version
   ```

### Configure credentials

s5cmd reads credentials from environment variables or the AWS shared credentials file. Set the following environment variables with your AI Object Storage access keys:

Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your AI Object Storage access key credentials.

```bash theme={"system"}
export AWS_ACCESS_KEY_ID=[ACCESS-KEY-ID]
export AWS_SECRET_ACCESS_KEY=[SECRET-ACCESS-KEY]
```

If you've already configured credentials for AI Object Storage following the [Get started guide](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md), you can use your existing `cw` profile instead by passing `--profile cw` to your s5cmd commands, or by setting `AWS_PROFILE=cw` in your environment.

### Copy objects between buckets

Copy objects from a source bucket to a target bucket:

Replace `[SOURCE-BUCKET]` and `[TARGET-BUCKET]` with the names of your source and target buckets.

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      cp 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

This copies all objects from the source bucket to the target bucket.

s5cmd preserves the source directory structure by default. To flatten the source directory structure, use the `--flatten` flag.

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      cp --flatten 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

> [!TIP]
>
> **Escape wildcards in zsh**
>
> Shells like zsh treat the `*` character as a file globbing wildcard. Wrap wildcard expressions in single quotes to prevent unexpected behavior:
>
> ```bash theme={"system"}
> # Correct - wildcards are passed to s5cmd
> s5cmd cp 's3://bucket/*.gz' ./local-dir/
>
> # Incorrect - shell expands the wildcard first
> s5cmd cp s3://bucket/*.gz ./local-dir/
> ```

To copy a specific file:

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      cp s3://[SOURCE-BUCKET]/path/to/file.txt s3://[TARGET-BUCKET]/path/to/file.txt
```

To copy from a local directory to a bucket:

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      cp '/local/path/*' s3://[TARGET-BUCKET]/
```

### Optimize s5cmd performance

s5cmd provides two main options for tuning parallelism:

* `--numworkers`: Sets the size of the global worker pool (default: 256). This flag controls how many files transfer concurrently.
* `--concurrency`: A `cp` command option that sets the number of parts uploaded or downloaded in parallel for a single file (default: 5). This option is useful for large files that use multipart transfers.

> [!WARNING]
>
> **Lower concurrency for NFS-backed destinations**
>
> When the destination is an NFS-backed mount, such as Distributed File Storage, high `--numworkers` or `--concurrency` values can stall NFS writeback on the client and block every process that uses the mount. For NFS-backed destinations, start with lower concurrency, and run large transfers from a compute node instead of a shared [Slurm login node](https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes.md#login-nodes).

For many small files, increase `--numworkers` to maximize parallel file transfers:

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      --numworkers 512 \
      cp 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

For a few large files, keep `--numworkers` low and increase `--concurrency` to maximize multipart upload parallelism:

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      --numworkers 4 \
      cp --concurrency 16 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

For mixed workloads, balance both options:

```bash theme={"system"}
s5cmd --endpoint-url https://cwobject.com \
      --numworkers 64 \
      cp --concurrency 8 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

### Additional s5cmd operations

s5cmd supports many S3 operations beyond copy. Useful commands include (replace `[BUCKET-NAME]` with your bucket name and `[PREFIX]` with the object key prefix to remove):

```bash theme={"system"}
# List objects in a bucket
s5cmd --endpoint-url https://cwobject.com ls s3://[BUCKET-NAME]/

# Remove objects
s5cmd --endpoint-url https://cwobject.com rm 's3://[BUCKET-NAME]/[PREFIX]/*'

# Sync directories (copy only changed files)
s5cmd --endpoint-url https://cwobject.com sync 's3://[SOURCE-BUCKET]/*' s3://[TARGET-BUCKET]/
```

For the full list of commands, run `s5cmd --help`.

## Migrate data with Rclone

If s5cmd doesn't fit your workflow, or you need to sync across multiple cloud providers, use Rclone instead. Rclone manages files across cloud storage providers. It supports complex sync operations and works with many storage backends.

> [!WARNING]
>
> **Do not use Rclone with Local Storage**
>
> Rclone has known kernel panic issues when reading from and writing to [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md) volumes. To move data between Local Storage and AI Object Storage, use s5cmd, s3cmd, or `aws s3 cp` instead.
>
> Rclone is safe to use with AI Object Storage and other systems, including [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md), other Object Storage buckets, and external systems.

### Install Rclone

Follow the [Rclone installation guide](https://rclone.org/install/) to install Rclone. This guide uses Rclone version `v1.69`.

### Configure Rclone

1. Create source and destination profiles in your Rclone config. To locate the config file, run:

   ```bash theme={"system"}
   rclone config file
   ```

   If the config file doesn't exist, Rclone reports the default location where you should create the config file:

   ```text title="Example output" theme={"system"}
   Configuration file doesn't exist, but rclone will use this path:
   /home/username/.config/rclone/rclone.conf
   ```

   If an active config file exists, Rclone reports its actual location with a similar message.

2. Edit the config file with your preferred text editor and add the following profiles. Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your AI Object Storage access key credentials:

   ```ini title="~/.config/rclone/rclone.conf" highlight={4-5,13-14} theme={"system"}
   [source]
   type = s3
   provider = Other
   access_key_id = [ACCESS-KEY-ID]
   secret_access_key = [SECRET-ACCESS-KEY]
   endpoint = https://cwobject.com
   force_path_style = false
   no_check_bucket = true

   [target]
   type = s3
   provider = Other
   access_key_id = [ACCESS-KEY-ID]
   secret_access_key = [SECRET-ACCESS-KEY]
   endpoint = https://cwobject.com
   force_path_style = false
   no_check_bucket = true
   ```

3. Save and close the file.

   You now have two named Rclone profiles, `source` and `target`, that you can reference in subsequent commands to copy data between buckets.

### Copy objects between buckets

Copy objects from the source to the target:

Replace `[SOURCE-BUCKET]` and `[TARGET-BUCKET]` with the names of your source and target buckets.

```bash theme={"system"}
rclone copy source:[SOURCE-BUCKET] target:[TARGET-BUCKET] \
      --progress --stats 15s
```

This copies all objects:

* From the source bucket on the `source` profile.
* To the target bucket on the `target` profile.

The Rclone options `--progress --stats 15s` print a progress bar with estimated time to completion and detailed transfer statistics every 15 seconds.

For versioned buckets, Rclone copies the latest version of each object by default. See [Use Rclone with versioned buckets and objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md) for more details, including specific guidance on how to work with specific versions and delete markers.

### Optimize Rclone performance

To optimize Rclone throughput with AI Object Storage, use flags to fine-tune parallelism and chunking for large files. The main flags are:

* `--transfers`: Sets the number of concurrent file transfers. Adjust this flag to use the available network bandwidth between your environment and CoreWeave, or between CoreWeave regions.
* `--checkers`: Controls the number of concurrent file checks for equality. Adjust this flag when transferring many small files.
* `--s3-chunk-size`: Defines the chunk size used to upload files larger than the upload\_cutoff or files with unknown sizes. Larger chunks reduce HTTP requests but increase memory usage.
* `--s3-upload-concurrency`: Sets the level of concurrency for multipart uploads.

To check the default values for each flag, use `rclone help flags`. Rclone has many flags, so use `grep` to filter the output.

```bash theme={"system"}
rclone help flags | grep -E -- '--checkers|--transfers|--s3-chunk-size|--s3-upload-concurrency'
```

```text title="Example output" theme={"system"}
  --checkers int                Number of checkers to run in parallel (default 8)
  --transfers int               Number of file transfers to run in parallel (default 4)
  --s3-chunk-size SizeSuffix    Chunk size to use for uploading (default 5Mi)
  --s3-upload-concurrency int   Concurrency for multipart uploads and copies (default 4)
```

#### Optimization guidelines

Use these guidelines to optimize Rclone throughput when copying data to and from CoreWeave AI Object Storage:

* To maximize migration throughput, consider the combined effects of `--transfers` and `--s3-upload-concurrency` as multiplicative:

  **Total streams ≈ `--transfers` × `--s3-upload-concurrency`**

  * For transfers dominated by many small or medium-sized files (KBs to MBs), increase `--transfers` to a value between 8 and 32 to move multiple files in parallel, but keep `--s3-upload-concurrency` at a lower value, between 1 and 4, because small files don't benefit from multipart uploads.

  * For transfers with a few large files (hundreds of GB), do the opposite. Set `--transfers` to 1 or 2 to avoid initiating too many multipart uploads, and increase `--s3-upload-concurrency` to a large value, between 8 and 16, to upload multiple parts of each large file in parallel and saturate available bandwidth.

* Increase `--s3-chunk-size` to 50 MB for best performance. The default is 5 MB.

* Monitor memory use. Estimate Rclone's RAM needs with this calculation:

  **RAM ≈ `--transfers` × (`--s3-upload-concurrency` × (`--s3-chunk-size` + `--buffer-size`))**

  * Each active stream uses `--buffer-size` (the default 16 MB).
  * Each multipart chunk consumes `--s3-chunk-size`.

* Increase one flag at a time while monitoring with `rclone --progress --stats 15s`.

* Stop tuning when throughput plateaus or retries increase. This method ensures that you maximize the available bandwidth without overloading local I/O, system memory, or remote service limits.

#### Usage example

The following command copies data from the source bucket to the target bucket, using the recommended flags.

Use `--s3-chunk-size 50M` for best performance, and adjust the other flags based on your data size, number of files, and available bandwidth.

```bash theme={"system"}
rclone copy source:[SOURCE-BUCKET] target:[TARGET-BUCKET] \
      --progress \
      --stats 15s \
      --transfers 64 \
      --checkers 128 \
      --s3-chunk-size 50M \
      --s3-upload-concurrency 10
```

## Check bucket usage

If you have s3cmd installed, check the usage of the target bucket with (replace `[BUCKET-NAME]` with your bucket name):

```bash theme={"system"}
s3cmd du --human-readable-sizes s3://[BUCKET-NAME]
```

The output shows the total size of the bucket and the number of objects it contains.

```text title="Example output" theme={"system"}
238M    2303 objects s3://my-bucket/
```
