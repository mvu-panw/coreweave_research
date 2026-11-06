# Configure rclone for AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/rclone

# Configure rclone for AI Object Storage

> How to manage CoreWeave AI Object Storage buckets and objects with rclone

This page shows how to configure [rclone](https://rclone.org/) to manage CoreWeave AI Object Storage buckets and objects. After you configure rclone, you can use it to list, copy, sync, and otherwise manage data in AI Object Storage from the command line.

rclone requires a config file. You can choose either of the following approaches:

1. Inherit the configuration from your AWS profile.
2. Use only the `rclone.conf` file.

Option 1 is usually recommended, as it simplifies the use of other tools such as the AWS CLI and boto3. The following sections describe each option in detail.

## Option 1: Use rclone with an AWS profile

rclone can inherit configuration from an [AWS profile](https://docs.aws.amazon.com/sdkref/latest/guide/file-format.html#file-format-profile), usually found in `~/.aws/config`. This means rclone and all other tools can share the same connection settings.

```ini theme={"system"}
[default]
type = s3
provider = AWS
env_auth = true
profile = default
no_check_bucket = true
```

In this example, the AWS profile is also named `default`. See [Configure AWS CLI and boto3](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md) for details on configuration, including how to use federated credentials.

> [!WARNING]
>
> Static Access Keys are not recommended for production use. Use [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) instead. See [Configure AWS CLI and boto3](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md) for how to set up federated credentials that rclone can inherit through an AWS profile.

Example `~/.aws/config` with static credentials:

```ini theme={"system"}
[default]
region = US-EAST-04A
endpoint_url = http://cwlota.com
aws_access_key_id = [ACCESS-KEY-ID]
aws_secret_access_key = [SECRET-ACCESS-KEY]
s3 =
    addressing_style = virtual
```

If you have permission to list buckets, test the configuration:

```bash theme={"system"}
rclone lsd default: -v
```

## Option 2: Use rclone with a standalone config

If you prefer to keep rclone's configuration separate from your AWS profile, you can define a dedicated rclone remote instead.

Create an rclone remote in `~/.config/rclone/rclone.conf`. Replace `[ACCESS-KEY-ID]` and `[SECRET-ACCESS-KEY]` with your actual values. Alternatively, you can pass sensitive credentials through [environment variables](https://rclone.org/docs/#environment-variables).

> [!WARNING]
>
> Static Access Keys are not recommended for production use. Use [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) instead. This is the primary advantage of Option 1.

```ini theme={"system"}
[default]
type = s3
provider = Other
access_key_id = [ACCESS-KEY-ID]
secret_access_key = [SECRET-ACCESS-KEY]
endpoint = http://cwlota.com
force_path_style = false
no_check_bucket = true
```

For best performance, always use the [LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) (`http://cwlota.com`) when running inside a CoreWeave cluster. The primary endpoint (`https://cwobject.com`) is available when running outside of a CoreWeave cluster.

These settings are critical when configuring rclone for AI Object Storage:

* **type**: Must be `s3`.
* **provider**: Must be `Other`.
* **force\_path\_style**: Must be `false`. This forces rclone to use [virtual-hosted style URLs](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md). Path-style addressing is not supported.
* **no\_check\_bucket**: Must be `true`. This prevents rclone from creating or verifying the bucket's existence during operations.

Test the configuration:

```bash theme={"system"}
rclone lsd default: -v
```
