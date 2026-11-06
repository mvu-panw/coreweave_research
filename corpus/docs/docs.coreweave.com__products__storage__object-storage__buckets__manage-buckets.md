# Manage buckets

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets

# Manage buckets

> How to manage CoreWeave AI Object Storage buckets with popular S3 clients.

CoreWeave AI Object Storage stores data as objects consisting of the data itself, its metadata, and a unique identifier. These objects are organized into containers called **buckets**, which provide a namespace for objects to ensure that object names are unique within a bucket. Additionally, buckets can have specific configurations and policies to manage the data lifecycle and security.

You can create and delete buckets programmatically using the [S3-compatible Object Storage API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) or various S3-compatible tools.

This guide explains how to manage CoreWeave AI Object Storage buckets [with Cloud Console](#manage-buckets-with-cloud-console) and [using popular clients](#manage-buckets-programmatically): S3cmd, AWS CLI, Boto3, and s5cmd.

## Prerequisites

This guide assumes that you have followed the steps in [Get started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md). Before you begin, ensure that you have completed the following tasks:

* [Obtain Access Keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md) with OpenID Connect (OIDC) Workload Identity Federation for production or a CoreWeave API access token for development and testing.
* For the delete and usage-reporting examples, [create a bucket](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#create-a-bucket) to manage.
* [Set organization access policies](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#set-an-organization-access-policy) and, if needed, bucket access policies to control access, lifecycle, and auditing.
* [Configure your endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md) to use the required virtual-hosted addressing style and the correct AI Object Storage endpoints.

## About LOTA (Local Object Transport Accelerator)

To use [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), clients must point their requests to the **LOTA endpoint** instead of the **primary endpoint**. No other changes are required for S3-compatible clients.

* Use the LOTA endpoint, `http://cwlota.com`, when running inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
* Use the primary endpoint, `https://cwobject.com`, when running outside of a CoreWeave cluster.

Learn more [about LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). You can also [pre-stage objects into the LOTA cache](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md) to eliminate cold-start latency.

## Bucket considerations

The following requirements and constraints apply when creating and naming buckets in CoreWeave AI Object Storage.

### Bucket creation

**You can't create a bucket without a valid API access key**. Anonymous requests are never allowed to create buckets. To obtain an API access key, see [How-To: Manage Access Keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md).

**When you create a bucket**, you automatically become the bucket owner. The bucket owner has full control over the bucket and its contents.

### Bucket naming

Bucket names must be globally unique, and adhere to the following rules:

* **Length:** 3 to 63 characters.
* **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
* **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
* **Prohibited patterns:** Cannot start with `xn--`.
* **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. These are reserved for internal use.

If you try to create a bucket with a name that already exists in another location, or that doesn't adhere to these rules, you receive an error.

### Endpoint configuration

**All requests to CoreWeave AI Object Storage endpoints must be in DNS (virtual-hosted) style**, where the bucket name is part of the domain name in the URL.

* Use `http://[BUCKET-NAME].cwlota.com` **if using the LOTA endpoint**.
* Use `https://[BUCKET-NAME].cwobject.com` **if using the primary endpoint**.
* Set your S3 configuration to [specify a virtual addressing style](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-virtual-addressing-style).

## Manage buckets with Cloud Console

The [**Buckets** section](https://console.coreweave.com/object-storage/buckets) lets you manage your buckets. You can create and delete buckets, and view their total size and the number of objects in them. To [browse, upload, download, or delete the objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) within a bucket, select the bucket to open it.

The Grafana link at the top of the page leads to a Grafana dashboard for all buckets in your organization.

![Buckets page](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cloud-console-object-storage-buckets.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=b88f6bf26ce34732fa6e3b2ea2aa2119)

For each bucket, the vertical dot menu on the right allows you to view the Grafana dashboard for that bucket, or delete the bucket.

## Availability Zones

S3cmd, AWS CLI, and Boto3 use the term **"region"** to define the location of the object storage service. However, at CoreWeave, **Regions** (A region encompasses a broader geographic area, expanding service availability and meeting data residency requirements.) are larger constructs that are organized into **Availability Zones** (AZs) (An Availability Zone (AZ) is a partition within a region that hosts one or more data halls. AZs are physically and operationally independent from each other.). When configuring your client, use a CoreWeave [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) in place of the traditional AWS "region".

When you create a new bucket, specify the Availability Zone in which the bucket is created.

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

Use the following client-specific settings:

* When creating a bucket with **S3cmd**, use `--bucket-location` with the Availability Zone.
* When creating a bucket with **AWS CLI or Boto3**, use `LocationConstraint`.
* **s5cmd** doesn't support specifying an Availability Zone at bucket creation. Use the AWS CLI, s3cmd, or Boto3 if you need to create a bucket in a specific Availability Zone.

The examples that follow demonstrate proper use.

## Manage buckets programmatically

The following examples show how to manage buckets with the AWS CLI, s3cmd, and Boto3.

* The AWS CLI is a command-line tool that manages AWS services. It provides a consistent interface to interact with S3-compatible services, including CoreWeave AI Object Storage. Follow these steps to install and configure the AWS CLI, then use it to create and delete buckets in CoreWeave AI Object Storage.
* S3cmd is a command-line tool that manages objects in S3-compatible object storage services. You can use it to create, delete, and manage buckets, as well as upload, download, and manage objects within those buckets. S3cmd is available for Linux and macOS.
* Boto3 is the AWS SDK for Python. It lets you interact with AWS services programmatically using Python. Follow these steps to install and configure Boto3, then use it to create and delete buckets in CoreWeave AI Object Storage.
* s5cmd is a high-performance, parallel S3 CLI tool. Use the [CoreWeave fork of s5cmd](https://github.com/coreweave/s5cmd), which uses virtual-hosted addressing for AI Object Storage compatibility. Follow these steps to install and configure s5cmd, then use it to create and delete buckets in CoreWeave AI Object Storage. For bulk transfers, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).

### Install tools

> [tab] AWS CLI
>
> AWS CLI supports macOS, Linux, and Windows. See [the official installation procedures](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) for your operating system in the AWS CLI User Guide.

> [tab] s3cmd
>
> The preferred S3cmd installation method is to [download the latest version from GitHub](https://s3tools.org/download). Alternatively, you can install it with the package manager for your system. For example, **macOS** can use [Homebrew](https://brew.sh/).
>
> ```bash title="macOS Example" theme={"system"}
> brew install s3cmd
> ```
>
> **Linux** distributions can use their native package manager. For example:
>
> ```bash title="Debian example" theme={"system"}
> sudo apt install s3cmd
> ```
>
> The version of S3cmd available in these package managers may not be the latest version. If you require the latest version, download it from the [S3cmd GitHub repository](https://s3tools.org/download).

> [tab] Boto3
>
> Boto3 supports any platform that can run Python. To install Boto3, [follow the steps in the official documentation](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html#installation).

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> Download the latest release binary for your platform from the [CoreWeave s5cmd releases page](https://github.com/coreweave/s5cmd/releases). After downloading, make the binary executable and move it to a directory in your `PATH`:
>
> ```bash theme={"system"}
> chmod +x s5cmd && sudo mv s5cmd /usr/local/bin/
> ```
>
> Verify the installation:
>
> ```bash theme={"system"}
> s5cmd version
> ```

### Configure tools

> [tab] AWS CLI
>
> To set up your AWS configuration for CoreWeave AI Object Storage, create a `cw` profile. We recommend using a separate profile to avoid conflicts with your other AWS profiles and S3-compatible services.
>
> 1. Create a `cw` profile:
>
>    ```bash title="Create a new profile" theme={"system"}
>    aws configure --profile cw
>    ```
>
> 2. When prompted for information, provide the following values:
>
>    | Field | Value |
>    | - | - |
>    | AWS Access Key ID | The CoreWeave AI Object Storage [access key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md). |
>    | AWS Secret Key | The CoreWeave AI Object Storage secret key. |
>    | Default region name | Optional. To set a default region, see the [CoreWeave Availability Zones](#availability-zones). |
>    | Default output format | Use `json` for JSON output. |
>
> 3. Set the endpoint URL to the appropriate endpoint for your use case:
>
>    | Endpoint URL | Description |
>    | - | - |
>    | `https://cwobject.com` | The primary endpoint for CoreWeave AI Object Storage. Use this when running outside of a CoreWeave cluster. |
>    | `http://cwlota.com` | The [LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), which routes to the LOTA cache for best performance. Always use the LOTA endpoint when running inside a CoreWeave cluster. |
>
>    ```bash title="Set the LOTA endpoint URL" theme={"system"}
>    aws configure set endpoint_url http://cwlota.com --profile cw
>    ```
>
>    ```bash title="Set the primary endpoint URL" theme={"system"}
>    aws configure set endpoint_url https://cwobject.com --profile cw
>    ```
>
> 4. Set the default addressing style to `virtual`. This is required for CoreWeave AI Object Storage, as it uses virtual-hosted style URLs.
>
>    ```bash title="Set virtual addressing style" theme={"system"}
>    aws configure set s3.addressing_style virtual --profile cw
>    ```
>
> Pass `--profile cw` to each AWS CLI command to use these credentials, or run `export AWS_PROFILE=cw` before running commands.

> [tab] s3cmd
>
> S3cmd requires your API token, default Region, endpoint and other information to use CoreWeave AI Object Storage. To configure S3cmd, run the following command:
>
> ```bash title="Configure S3cmd" theme={"system"}
> s3cmd --configure
> ```
>
> When prompted, provide the following values:
>
> | Field | Value |
> | - | - |
> | Access Key | The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) created by the CoreWeave AI Object Storage API. |
> | Secret Key | The Secret Key created by the CoreWeave AI Object Storage API. |
> | Default Region | The CoreWeave **Availability Zone** is found in the [Availability Zones](#availability-zones) table. |
> | S3 Endpoint | • **`cwobject.com`** is the primary endpoint. • **`cwlota.com`** is [the LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). |
> | DNS-style template | • **`%(bucket)s.cwobject.com`** is the primary template. • **`%(bucket)s.cwlota.com`** is [the LOTA template](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). |
> | Path to GPG program | Defaults to `/usr/bin/gpg`. |
> | Use HTTPS protocol | Boolean value indicating whether you're using the HTTPS protocol. Defaults to `True`. |
> | HTTP Proxy server name | Name of HTTP Proxy server. |
> | HTTP Proxy server port | Port number of HTTP Proxy server. |
>
> When you use secure HTTPS protocol, all communication with Amazon S3 servers is protected from third-party eavesdropping. This method is slower than plain HTTP,
> and can only be proxied with Python 2.7 or newer.
>
> On some networks, all internet access must go through an HTTP proxy. Try setting the name and port here if you can't connect to S3 directly.
>
> Leave the remaining fields blank or press `Enter` to accept the default values. Test and save the configuration when prompted.
>
> By default, S3cmd stores its configuration in `$HOME/.s3cfg`.

> [tab] Boto3
>
> Boto3 uses the same configuration files as the AWS CLI. If you have already configured the AWS CLI, you can skip this step. Otherwise, configure Boto3 by following the steps in the AWS CLI Configuration tab within this section.
>
> Boto3 can also use a `Config` object or the environment to override the AWS CLI configuration. See [this example](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#full-configuration-examples) for more details.

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> s5cmd reads credentials from the standard AWS credential chain: environment variables or the shared credentials file used by the AWS CLI. If you've already configured the AWS CLI, s5cmd uses the same credentials.
>
> ```bash title="Set credentials as environment variables" theme={"system"}
> export AWS_ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export AWS_SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> ```
>
> Unlike the AWS CLI, s5cmd doesn't read `endpoint_url` from the AWS configuration file. Pass `--endpoint-url` on every command. Replace `[COMMAND]` with the s5cmd subcommand you want to run, such as `cp` or `ls`:
>
> ```bash title="Example command with endpoint URL" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com [COMMAND]
> ```

### Create a bucket

> [tab] AWS CLI
>
> Use the `aws s3api` command to create a new bucket. For example:
>
> Replace `[BUCKET-NAME]` with your desired bucket name and `[AVAILABILITY-ZONE]` with a CoreWeave [Availability Zone](#availability-zones).
>
> ```bash title="Create a bucket with AWS CLI" theme={"system"}
> aws s3api create-bucket \
>     --bucket [BUCKET-NAME] \
>     --region [AVAILABILITY-ZONE] \
>     --create-bucket-configuration LocationConstraint=[AVAILABILITY-ZONE] \
>     --profile cw
> ```
>
> > [!WARNING]
> >
> > * The `LocationConstraint` parameter is **required**.
> > * > [accordion] Bucket naming rules
> >   >
> >   > Bucket names must be globally unique and adhere to the following rules:
> >   >
> >   > * **Length:** 3 to 63 characters.
> >   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> >   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> >   > * **Prohibited patterns:** Cannot start with `xn--`.
> >   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

> [tab] s3cmd
>
> To create a bucket with S3cmd, use the `mb` (make bucket) command as shown below.
>
> Replace `[AVAILABILITY-ZONE]` with a CoreWeave [Availability Zone](#availability-zones) and `[BUCKET-NAME]` with a globally-unique name.
>
> ```bash title="Make a bucket with S3cmd" theme={"system"}
> s3cmd mb --bucket-location=[AVAILABILITY-ZONE] s3://[BUCKET-NAME]
> ```
>
> > [!WARNING]
> >
> > * The `--bucket-location` parameter is **required**.
> > * > [accordion] Bucket naming rules
> >   >
> >   > Bucket names must be globally unique and adhere to the following rules:
> >   >
> >   > * **Length:** 3 to 63 characters.
> >   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> >   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> >   > * **Prohibited patterns:** Cannot start with `xn--`.
> >   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

> [tab] Boto3
>
> 1. Set environment variables for your CoreWeave credentials:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
>    Alternatively, configure your CoreWeave credentials to work with the AWS CLI.
>
>    We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.
>
>    > [!TIP]
>    >
>    > For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.
>
>    > [accordion] Configure CoreWeave credentials with static access keys
>    >
>    > 1. Create a `cw` profile:
>    >
>    >    ```bash title="Create a new profile" theme={"system"}
>    >    aws configure --profile cw
>    >    ```
>    >
>    > 2. When prompted, provide the following values:
>    >
>    >    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    >    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    >    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    >    * **Default output format**: Use `json` for JSON output.
>    >
>    > 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>    >
>    >    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    >    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>    >
>    >    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    >    aws configure set endpoint_url https://cwobject.com --profile cw
>    >    ```
>    >
>    > 4. Set the S3 `addressing_style` to `virtual`:
>    >
>    >    ```bash title="Set virtual addressing style" theme={"system"}
>    >    aws configure set s3.addressing_style virtual --profile cw
>    >    ```
>    >
>    > To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>    >
>    > If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.
>
>    > [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>    >
>    > If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>    >
>    > Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>    >
>    > ```bash title="Configure WIF OIDC credentials" theme={"system"}
>    > export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
>    > export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>    >
>    > aws configure set s3.addressing_style virtual
>    >
>    > export AWS_REGION="[AVAILABILITY-ZONE]"
>    > export AWS_ENDPOINT_URL_S3="https://cwobject.com"
>    > ```
>    >
>    > With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>    >
>    > Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.
>
> 2. Use the `create_bucket` method to create a bucket. Replace `[BUCKET-NAME]` with your desired bucket name and `[AVAILABILITY-ZONE]` with a CoreWeave [Availability Zone](#availability-zones).
>
>    ```python title="Create a bucket with Boto3" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>
>    boto_config = Config(
>        region_name='[AVAILABILITY-ZONE]',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    response = s3.create_bucket(
>        Bucket='[BUCKET-NAME]',
>        CreateBucketConfiguration={
>            'LocationConstraint': '[AVAILABILITY-ZONE]',
>        },
>    )
>
>    print(response)
>    ```
>
> > [!WARNING]
> >
> > * The `LocationConstraint` parameter is **required**.
> > * > [accordion] Bucket naming rules
> >   >
> >   > Bucket names must be globally unique and adhere to the following rules:
> >   >
> >   > * **Length:** 3 to 63 characters.
> >   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> >   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> >   > * **Prohibited patterns:** Cannot start with `xn--`.
> >   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> To create a bucket with s5cmd, use the `mb` command. Replace `[BUCKET-NAME]` with your desired bucket name.
>
> ```bash title="Create a bucket with s5cmd" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       mb s3://[BUCKET-NAME]
> ```
>
> > [!WARNING]
> >
> > * s5cmd `mb` doesn't support specifying a `LocationConstraint`. To create a bucket in a specific Availability Zone, use the AWS CLI, s3cmd, or Boto3.
> > * > [accordion] Bucket naming rules
> >   >
> >   > Bucket names must be globally unique and adhere to the following rules:
> >   >
> >   > * **Length:** 3 to 63 characters.
> >   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> >   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> >   > * **Prohibited patterns:** Cannot start with `xn--`.
> >   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

### Delete a bucket

Only empty buckets can be deleted. Remove all objects, object versions, delete markers, and incomplete multipart uploads before deleting a bucket. See [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md) for the complete cleanup procedure.

> [tab] AWS CLI
>
> To delete a bucket, use the `delete-bucket` sub-command as shown. **Only empty buckets can be deleted**. Remove all objects, object versions, and delete markers before deleting a bucket.
>
> Replace `[BUCKET-NAME]` with the name of the bucket to delete.
>
> ```bash title="Delete a bucket with AWS CLI" theme={"system"}
> aws s3api delete-bucket --bucket [BUCKET-NAME] --profile cw
> ```

> [tab] s3cmd
>
> To delete a bucket with S3cmd, use the `rb` (remove bucket) command as shown below. **Only empty buckets can be deleted**. Remove all objects, object versions, and delete markers before deleting a bucket.
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Remove a bucket with S3cmd" theme={"system"}
> s3cmd rb s3://[BUCKET-NAME]
> ```

> [tab] Boto3
>
> To delete a bucket with Boto3, use the `delete_bucket` method. **Only empty buckets can be deleted**. Remove all objects, object versions, and delete markers before deleting a bucket.
>
> 1. Set environment variables for your CoreWeave credentials:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
>    Alternatively, configure your CoreWeave credentials to work with the AWS CLI.
>
>    We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.
>
>    > [!TIP]
>    >
>    > For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.
>
>    > [accordion] Configure CoreWeave credentials with static access keys
>    >
>    > 1. Create a `cw` profile:
>    >
>    >    ```bash title="Create a new profile" theme={"system"}
>    >    aws configure --profile cw
>    >    ```
>    >
>    > 2. When prompted, provide the following values:
>    >
>    >    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    >    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    >    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    >    * **Default output format**: Use `json` for JSON output.
>    >
>    > 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>    >
>    >    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    >    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>    >
>    >    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    >    aws configure set endpoint_url https://cwobject.com --profile cw
>    >    ```
>    >
>    > 4. Set the S3 `addressing_style` to `virtual`:
>    >
>    >    ```bash title="Set virtual addressing style" theme={"system"}
>    >    aws configure set s3.addressing_style virtual --profile cw
>    >    ```
>    >
>    > To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>    >
>    > If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.
>
>    > [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>    >
>    > If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>    >
>    > Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>    >
>    > ```bash title="Configure WIF OIDC credentials" theme={"system"}
>    > export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
>    > export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>    >
>    > aws configure set s3.addressing_style virtual
>    >
>    > export AWS_REGION="[AVAILABILITY-ZONE]"
>    > export AWS_ENDPOINT_URL_S3="https://cwobject.com"
>    > ```
>    >
>    > With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>    >
>    > Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.
>
> 2. Replace `[BUCKET-NAME]` with the name of the bucket to delete.
>
>    ```python title="Delete a bucket with Boto3" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>
>    boto_config = Config(
>        region_name='[AVAILABILITY-ZONE]',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    response = s3.delete_bucket(Bucket='[BUCKET-NAME]')
>
>    print(response)
>    ```

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> To delete a bucket with s5cmd, use the `rb` (remove bucket) command. **Only empty buckets can be deleted**. Remove all objects, object versions, and delete markers before deleting a bucket.
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Remove a bucket with s5cmd" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       rb s3://[BUCKET-NAME]
> ```

### Report usage

> [tab] AWS CLI
>
> To report the usage of a bucket, use `aws s3` with the `ls` sub-command. Use the `--recursive`, `--human-readable`, and `--summarize` parameters to view information in an easier-to-understand format.
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Report bucket usage with AWS CLI" theme={"system"}
> aws s3 ls s3://[BUCKET-NAME] --recursive --human-readable --summarize --profile cw
> ```

> [tab] s3cmd
>
> To report the usage of a bucket, use the `du` (disk usage) command. Use the `--human-readable-sizes` parameter to view information in an easier-to-understand format.
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Report bucket usage with S3cmd" theme={"system"}
> s3cmd du --human-readable-sizes s3://[BUCKET-NAME]
> ```

> [tab] Boto3
>
> 1. Set environment variables for your CoreWeave credentials:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
>    Alternatively, configure your CoreWeave credentials to work with the AWS CLI.
>
>    We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.
>
>    > [!TIP]
>    >
>    > For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.
>
>    > [accordion] Configure CoreWeave credentials with static access keys
>    >
>    > 1. Create a `cw` profile:
>    >
>    >    ```bash title="Create a new profile" theme={"system"}
>    >    aws configure --profile cw
>    >    ```
>    >
>    > 2. When prompted, provide the following values:
>    >
>    >    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    >    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    >    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    >    * **Default output format**: Use `json` for JSON output.
>    >
>    > 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>    >
>    >    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    >    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>    >
>    >    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    >    aws configure set endpoint_url https://cwobject.com --profile cw
>    >    ```
>    >
>    > 4. Set the S3 `addressing_style` to `virtual`:
>    >
>    >    ```bash title="Set virtual addressing style" theme={"system"}
>    >    aws configure set s3.addressing_style virtual --profile cw
>    >    ```
>    >
>    > To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>    >
>    > If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.
>
>    > [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>    >
>    > If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>    >
>    > Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>    >
>    > ```bash title="Configure WIF OIDC credentials" theme={"system"}
>    > export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
>    > export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>    >
>    > aws configure set s3.addressing_style virtual
>    >
>    > export AWS_REGION="[AVAILABILITY-ZONE]"
>    > export AWS_ENDPOINT_URL_S3="https://cwobject.com"
>    > ```
>    >
>    > With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>    >
>    > Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.
>
> 2. Use the `list_objects_v2` method to sum the size of all objects in the bucket. Replace `[BUCKET-NAME]` with the name of your bucket.
>
>    ```python title="Report bucket usage with Boto3" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>
>    boto_config = Config(
>        region_name='[AVAILABILITY-ZONE]',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    paginator = s3.get_paginator('list_objects_v2')
>    pages = paginator.paginate(Bucket='[BUCKET-NAME]')
>
>    bucket_size = 0
>    object_count = 0
>
>    for page in pages:
>        objects = page.get('Contents', [])
>        bucket_size += sum(obj['Size'] for obj in objects)
>        object_count += len(objects)
>
>    if object_count:
>        print(f"Total size: {bucket_size} bytes ({object_count} objects)")
>    else:
>        print("Bucket is empty.")
>    ```

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> To report the usage of a bucket, use the `du` (disk usage) command with the `--humanize` parameter.
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Report bucket usage with s5cmd" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       du --humanize 's3://[BUCKET-NAME]/*'
> ```

## Next steps

Now that you've installed and configured an S3-compatible client, and created a bucket, you can:

* [Add files and objects to buckets](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md).
* [Apply a bucket lifecycle policy](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md) to automate object expiration and prevent incomplete multipart uploads from accumulating.
* [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md) when you no longer need it.
