# Set endpoints

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints

# Set endpoints

> Set AI Object Storage endpoints with virtual-hosted style addressing

CoreWeave AI Object Storage requires virtual-hosted style URLs. Path-style addressing isn't supported, so you must configure your client accordingly. This guide explains how to set the virtual-hosted addressing style and a valid AI Object Storage endpoint URL in your S3 configuration.

In virtual-hosted style, the bucket name is part of the domain, such as `https://[BUCKET-NAME].cwobject.com`, instead of part of the path.
When you enable this, your S3 client prepends bucket names to the endpoint in the correct format for AI Object Storage: `https://[BUCKET-NAME].cwobject.com`.

Make sure your S3 client isn't using path-style addressing (for example, `https://cwobject.com/[BUCKET-NAME]/file`). This format is unsupported and causes errors.

> [!NOTE]
>
> **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
>
> The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).

## Configure CoreWeave credentials

We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.

> [!TIP]
>
> For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.

> [accordion] Configure CoreWeave credentials with static access keys
>
> 1. Create a `cw` profile:
>
>    ```bash title="Create a new profile" theme={"system"}
>    aws configure --profile cw
>    ```
>
> 2. When prompted, provide the following values:
>
>    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    * **Default output format**: Use `json` for JSON output.
>
> 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>
>    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>
>    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    aws configure set endpoint_url https://cwobject.com --profile cw
>    ```
>
> 4. Set the S3 `addressing_style` to `virtual`:
>
>    ```bash title="Set virtual addressing style" theme={"system"}
>    aws configure set s3.addressing_style virtual --profile cw
>    ```
>
> To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>
> If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.

> [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>
> If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>
> Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>
> ```bash title="Configure WIF OIDC credentials" theme={"system"}
> export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
> export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>
> aws configure set s3.addressing_style virtual
>
> export AWS_REGION="[AVAILABILITY-ZONE]"
> export AWS_ENDPOINT_URL_S3="https://cwobject.com"
> ```
>
> With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>
> Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.

## Set virtual addressing style

With the AWS CLI, set the virtual addressing style for your CoreWeave profile, then verify the setting:

```bash title="Configure the virtual addressing style" theme={"system"}
aws configure set s3.addressing_style virtual --profile cw
```

```bash title="Verify the setting" theme={"system"}
aws configure get s3.addressing_style --profile cw
```

Boto3 shares this AWS CLI configuration, unless overridden by a `Config` object or the environment. This Boto3 example shows where to set the S3 addressing style within the `Config` object:

```python theme={"system"}
boto_config = Config(
    region_name = 'US-EAST-04A',
    s3={'addressing_style':'virtual'}
)
```

## Set endpoint URL

Make sure you use valid AI Object Storage endpoint URLs:

* Use the primary endpoint, `https://cwobject.com`, when running outside of a CoreWeave cluster.
* Use the LOTA endpoint, `http://cwlota.com`, when running inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for better performance.

Set the default endpoint URL in your AWS config, and verify the setting:

```bash title="Set the endpoint URL" theme={"system"}
aws configure set endpoint_url "https://cwobject.com" --profile cw
```

```bash title="Verify the endpoint URL" theme={"system"}
aws configure get endpoint_url --profile cw
```

Alternatively, you can set it in your Boto3 client. Set your credentials as environment variables, then pass them to the client:

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
```

```python theme={"system"}
import os
import boto3
from botocore.client import Config

boto_config = Config(
    region_name='US-EAST-04A',
    s3={'addressing_style': 'virtual'}
)

s3_client = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)
```

## Full configuration examples

These configuration examples show how to set both the virtual-hosted addressing style and the AI Object Storage endpoint URL. Use one of these availability zones (AZs) for your region:

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

> [tab] AWS CLI
>
> If you use an S3 client that reads the AWS config file (`~/.aws/config`), such as the AWS CLI or the S3 SDKs, you can add the configuration directly to your CoreWeave profile:
>
> Named profile:
>
> ```ini theme={"system"}
> [profile cw]
> region = US-EAST-04A
> endpoint_url = https://cwobject.com
> s3 =
>    addressing_style = virtual
> ```
>
> To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE` before running them:
>
> ```bash title="Use the cw profile with a flag" theme={"system"}
> aws s3 ls --profile cw
> ```
>
> ```bash title="Use the cw profile with an environment variable" theme={"system"}
> export AWS_PROFILE=cw
> aws s3 ls
> ```
>
> If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of `cw`. In that case, omit `--profile cw` from your commands and don't set `AWS_PROFILE`.

> [tab] Boto3
>
> Boto3 uses the same configuration files that you set with the AWS CLI. You can override your AWS CLI configuration by setting the addressing style in the `Config` object, and the `endpoint_url` in the client:
>
> Set your credentials as environment variables, then pass them to the client. Replace `[BUCKET-NAME]`, `[LOCAL-FILE-PATH]`, and `[OBJECT-KEY]` with your values.
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> ```
>
> ```python theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> s3_client.upload_file('[LOCAL-FILE-PATH]', '[BUCKET-NAME]', '[OBJECT-KEY]')
> ```
>
> See [Boto3 Configuration](https://docs.aws.amazon.com/boto3/latest/guide/configuration.html) for details.

> [tab] Multi-Storage Client
>
> [Multi-Storage Client](https://github.com/NVIDIA/multi-storage-client) (MSC) wraps Boto3 with connection pool scaling, automatic multipart tuning, and a profile-based configuration system.
>
> The `s3` pass-through option requires MSC version 0.43.0 or later. Configure MSC with a YAML file or a Python dictionary. The `s3` option under `storage_provider.options` passes settings directly to `botocore.config.Config`, including `addressing_style`. Replace `[BUCKET-NAME]` with the name of your bucket and `[AVAILABILITY-ZONE]` with your bucket's Availability Zone:
>
> ```yaml theme={"system"}
> profiles:
>   cw:
>     storage_provider:
>       type: s3
>       options:
>         base_path: [BUCKET-NAME]
>         endpoint_url: https://cwobject.com
>         region_name: [AVAILABILITY-ZONE]
>         multipart_threshold: 52428800  # 50 MB
>         multipart_chunksize: 52428800  # 50 MB
>         s3:
>           addressing_style: virtual
>     credentials_provider:
>       type: S3Credentials
>       options:
>         access_key: ${AWS-ACCESS-KEY-ID}
>         secret_key: ${AWS-SECRET-ACCESS-KEY}
> ```
>
> When running inside a CoreWeave cluster, set `endpoint_url` to `http://cwlota.com` to use the [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) cache.
>
> See the [Multi-Storage Client documentation](https://nvidia.github.io/multi-storage-client/) for installation, Python dictionary configuration, and the full reference.

> [tab] s3cmd
>
> ```ini title="~/.s3cfg file" theme={"system"}
> # ~/.s3cfg
> host_base = cwlota.com
> host_bucket = %(bucket)s.cwlota.com
> use_https = False
> ```
