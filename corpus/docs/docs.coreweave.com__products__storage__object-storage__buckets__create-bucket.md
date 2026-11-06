# Create buckets

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket

# Create buckets

> Create CoreWeave AI Object Storage buckets with Cloud Console or CLI clients.

Buckets are the primary organizational unit that stores object data in CoreWeave AI Object Storage. They're similar to folders in a file system.

This guide explains how to create a bucket with the CoreWeave Cloud Console or CLI clients such as the AWS CLI, s3cmd, Boto3, and s5cmd. Use the [CoreWeave fork of s5cmd](https://github.com/coreweave/s5cmd). Upstream s5cmd uses path-style addressing, which AI Object Storage doesn't support.

## Prerequisites

* You must [generate an Access Key](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) before you create a bucket. When you use the Cloud Console, use an [API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md#static-access-keys) to generate the Access Key. [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md#workload-identity-federation) is supported with CLI clients.
* To create a bucket with the Cloud Console, you must have `s3:CreateBucket` and `cwobject:CreateAccessKey` permissions granted to your user or group by an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md).
* Make sure your configuration uses the [correct endpoint URL](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-endpoint-url) and [has virtual-hosted addressing enabled](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-virtual-addressing-style).

## Create a bucket with Cloud Console

To create a bucket with the CoreWeave Cloud Console, follow these steps:

1. In the Cloud Console, navigate to the [Buckets](https://console.coreweave.com/object-storage/buckets) page.
2. Click the **Create Bucket** button at the top right corner of the page.
3. In the dialog, enter a **Bucket Name**.

   > [accordion] Bucket naming rules
   >
   > Bucket names must be globally unique and adhere to the following rules:
   >
   > * **Length:** 3 to 63 characters.
   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
   > * **Prohibited patterns:** Cannot start with `xn--`.
   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.
4. Select an **Availability Zone**.

   ![Create Bucket](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/create-bucket-cloud-console.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=f1c83f8f773c8de0928e37c9d2ec0370)
5. Click **Create**.

   ![Create Bucket success](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/create-bucket-success-cloud-console.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=2b954175efd5b1e2d72d2eb2ee211681)
6. Click **More options** to view information in Grafana, or to delete the bucket.

   ![Bucket: More options](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/delete-bucket-console.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=2b582afe535ce49ea7d693e54101cc27)

## Create a bucket with CLI clients

CoreWeave AI Object Storage is compatible with S3-compatible clients, including S3cmd, the AWS CLI, Boto3, and the [CoreWeave fork of s5cmd](https://github.com/coreweave/s5cmd).

> [!NOTE]
>
> **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
>
> The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).

Before you create a bucket, [configure your client](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#configure-tools). The primary endpoint, `https://cwobject.com`, requires TLS v1.3. Make sure your S3-compatible tools and OpenSSL use TLS v1.3.

The following sections describe how to create a bucket with each supported CLI client. Replace these placeholders in the examples:

* `[BUCKET-NAME]`: A globally unique name for your bucket. Follow the naming rules:

  > [accordion] Bucket naming rules
  >
  > Bucket names must be globally unique and adhere to the following rules:
  >
  > * **Length:** 3 to 63 characters.
  > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
  > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
  > * **Prohibited patterns:** Cannot start with `xn--`.
  > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.
* `[AVAILABILITY-ZONE]`: A CoreWeave Availability Zone that supports AI Object Storage (for example, `US-EAST-04A`). S3-compatible tools use the term "region" to define the location of the storage service, but at CoreWeave, Regions are larger constructs organized into Availability Zones. Use a CoreWeave [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) that supports AI Object Storage:

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

> [!NOTE]
>
> **Bucket creation delay**
>
> When you create a bucket with an S3-compatible client, it takes about one minute before the bucket becomes available due to DNS caching. You might see the following error immediately after bucket creation: `An error occurred (InvalidRegion) when calling the ListObjects operation: Region does not match.` Wait one minute, then try again.
>
> This delay doesn't occur when you create buckets in the Cloud Console.

> [tab] AWS CLI
>
> To create a bucket with AWS CLI, use the `aws s3api` command. The `LocationConstraint` parameter is required.
>
> ```bash title="Create a bucket with AWS CLI" theme={"system"}
> aws s3api create-bucket \
>     --bucket [BUCKET-NAME] \
>     --region [AVAILABILITY-ZONE] \
>     --create-bucket-configuration LocationConstraint=[AVAILABILITY-ZONE]
> ```
>
> If you need to install or configure the AWS CLI for AI Object Storage, see [Manage buckets with AWS CLI](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools).

> [tab] s3cmd
>
> To create a bucket with S3cmd, use the `mb` (make bucket) subcommand. The `--bucket-location` parameter is required.
>
> ```bash title="Create a bucket with S3cmd" theme={"system"}
> s3cmd mb --bucket-location=[AVAILABILITY-ZONE] s3://[BUCKET-NAME]
> ```
>
> If you need to configure S3cmd for AI Object Storage, see [Manage buckets with S3cmd](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#configure-tools).

> [tab] Boto3
>
> To create a bucket with Boto3, use the `create_bucket` method. The `LocationConstraint` parameter is required.
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
> 2. Replace `[BUCKET-NAME]` with the name of the bucket and `[AVAILABILITY-ZONE]` with a CoreWeave Availability Zone.
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
> If you need to configure Boto3 for AI Object Storage, see [Manage buckets with Boto3](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#configure-tools).

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
> s5cmd `mb` doesn't support specifying a `LocationConstraint`. To create a bucket in a specific Availability Zone, use the AWS CLI, s3cmd, or Boto3.
>
> If you need to install or configure s5cmd for AI Object Storage, see [Manage buckets with s5cmd](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools).

## Versioned buckets

New AI Object Storage buckets have versioning disabled. The `CreateBucket` operation doesn't accept a versioning configuration, so creating a versioned bucket requires two operations: first `CreateBucket`, then `PutBucketVersioning`.

To version every object from its first upload, enable versioning immediately after creating the bucket and before uploading any objects. If the bucket already contains objects, versioning applies to new writes after you enable it. Existing objects retain their current single version until you overwrite or re-upload them.

To enable and manage versioning, see [Versioned buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md).

## Next steps

Your [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) controls who can access the bucket through the Object Storage S3-compatible API. To grant access to this bucket specifically, add a [bucket policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md).
