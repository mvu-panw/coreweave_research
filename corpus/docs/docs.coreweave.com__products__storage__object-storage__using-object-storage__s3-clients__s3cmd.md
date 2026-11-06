# Configure s3cmd for AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/s3cmd

# Configure s3cmd for AI Object Storage

> How to configure s3cmd to use CoreWeave AI Object Storage

This guide shows you how to configure the `s3cmd` command-line tool to connect to CoreWeave AI Object Storage so you can manage buckets and objects from your terminal.

> [!NOTE]
>
> s3cmd doesn't natively support Workload Identity Federation. For production workloads, consider a tool that supports WIF, such as the [AWS CLI](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md) or [rclone](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/rclone.md).

s3cmd requires your Access Key, default Region, endpoint, and other information to use AI Object Storage. To start the interactive configuration:

```bash theme={"system"}
s3cmd --configure
```

When prompted, provide the following values:

| Field | Value |
| - | - |
| Access Key | The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) created by the AI Object Storage API. |
| Secret Key | The Secret Key created by the AI Object Storage API. |
| Default Region | The CoreWeave [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). |
| S3 Endpoint | `cwobject.com` is the primary endpoint. `cwlota.com` is the [LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). |
| DNS-style template | `%(bucket)s.cwobject.com` is the primary template. `%(bucket)s.cwlota.com` is the [LOTA template](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). |
| Path to GPG program | Defaults to `/usr/bin/gpg`. |
| Use HTTPS protocol | Boolean value indicating whether to use the HTTPS protocol. Defaults to `True`. Set to `False` for the LOTA endpoint, which uses HTTP. |
| HTTP Proxy server name | Name of the HTTP Proxy server, if applicable. |
| HTTP Proxy server port | Port number of the HTTP Proxy server, if applicable. |

Leave the remaining fields blank or press **Enter** to accept the default values. Test and save the configuration when prompted.

After the configuration is saved, s3cmd is ready to interact with AI Object Storage. By default, s3cmd stores its configuration in `$HOME/.s3cfg`.
