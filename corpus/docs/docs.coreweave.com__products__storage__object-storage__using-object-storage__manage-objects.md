# Manage objects

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects

# Manage objects

> Upload, list, delete, and rename objects in AI Object Storage buckets

This guide explains how to manage objects stored in CoreWeave AI Object Storage buckets using S3-compatible tools, including the AWS CLI, s3cmd, Boto3, and s5cmd. For high-performance or bulk transfers, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd) for s5cmd (use the [CoreWeave fork](https://github.com/coreweave/s5cmd) for AI Object Storage). Alternatively, you can [use Cyberduck](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/cyberduck.md) to manage your buckets and objects in a graphical interface. You can also manage objects in the [Cloud Console](https://console.coreweave.com/object-storage/buckets).

To manage versioned buckets with rclone, see [Versioned buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md).

## Prerequisites

This guide presumes you have the following:

* An active [CoreWeave account](https://console.coreweave.com).
* A valid [API Access Key and Secret Token key pair](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md).
* Adequate permissions to manage objects in CoreWeave AI Object Storage (for example, `s3:PutObject` and `s3:DeleteObject`). For more information, see [Object Storage S3 Permissions](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md).
* An [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) set.
* A properly configured SDK of your choosing.
* The primary endpoint, `https://cwobject.com`, requires TLS v1.3. Ensure your S3-compatible tools and OpenSSL use TLS v1.3.
* Make sure your S3 configuration uses the [correct endpoint URL](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-endpoint-url)
  and [has virtual-hosted addressing enabled](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-virtual-addressing-style).

> [accordion] Configure your endpoint
>
> Before running the commands in this guide, make sure your S3 client is configured with:
>
> * **Virtual-hosted addressing enabled** (`s3.addressing_style = virtual`). Path-style addressing is not supported. See [Set virtual addressing style](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#set-virtual-addressing-style).
> * **The correct endpoint URL**:
>   * `http://cwlota.com` when running inside a CoreWeave cluster (LOTA, best performance).
>   * `https://cwobject.com` when running outside a CoreWeave cluster.

## Add objects

Upload objects to a bucket so your data is available for downstream applications, sharing, or processing. Choose the tab that matches the tool you use.

> [tab] AWS CLI
>
> Ensure you have [the AWS CLI installed and configured](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools).
>
> Use the `s3 cp` command to copy a file into a bucket addressed using the `s3://` scheme.
>
> ```bash title="Example command" theme={"system"}
> aws s3 cp [LOCAL-FILE-PATH] s3://[BUCKET-NAME]
> ```
>
> ```text title="Example output" theme={"system"}
> upload: ./my-important-file.txt to s3://my-bucket-name/my-important-file.txt
> ```

> [tab] s3cmd
>
> Ensure you have [s3cmd installed, configured, and correctly credentialed](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools).
>
> Use the `put` command to copy an object into the bucket.
>
> ```bash title="Example command" theme={"system"}
> s3cmd put [LOCAL-FILE-PATH] s3://[BUCKET-NAME]
> ```
>
> This returns the following output, confirming your object is stored in your bucket:
>
> ```text title="Example output" theme={"system"}
> upload: 'my-important-file.txt' -> 's3://my-bucket-name/my-important-file.txt'
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
> 2. Use the following Python script to upload a file to your S3 bucket. Replace the following placeholders with the appropriate values for your request:
>
>    * `[BUCKET-NAME]`: The name of the bucket to upload the file to.
>    * `[LOCAL-FILE-PATH]`: The path to the local file to upload.
>    * `[OBJECT-NAME]`: The key (name) of the object in the bucket.
>    * `[AVAILABILITY-ZONE]`: Your CoreWeave Availability Zone (for example, `US-EAST-04A`). See [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).
>
>    ```python title="Upload a file to a bucket" theme={"system"}
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
>    bucket_name = '[BUCKET-NAME]'
>    object_name = '[OBJECT-NAME]'
>
>    with open('[LOCAL-FILE-PATH]', 'rb') as f:
>        s3.put_object(Bucket=bucket_name, Key=object_name, Body=f)
>
>    print(f'File uploaded to {bucket_name}/{object_name}')
>    ```
>
> If the upload succeeds, a confirmation message appears.
>
> ```text title="Example output" theme={"system"}
> File uploaded to my-bucket-name/my-important-file.txt
> ```

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> Ensure you have [s5cmd installed and configured](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools).
>
> Use the `cp` command to upload a file to a bucket. Replace `[LOCAL-FILE-PATH]` with the path to your file and `[BUCKET-NAME]` with your bucket name.
>
> ```bash title="Upload a file with s5cmd" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       cp [LOCAL-FILE-PATH] s3://[BUCKET-NAME]/
> ```

> [tab] Cloud Console
>
> The Cloud Console lets you upload objects to a bucket without installing a client.
>
> 1. In the [Cloud Console](https://console.coreweave.com/object-storage/buckets), navigate to **Object Storage** > **Buckets** and select the target bucket. The bucket opens to display its contents.
> 2. Navigate to the folder where you want to upload objects. To create a new folder, click **Create Folder**, enter a folder name, and confirm. The Cloud Console adds the corresponding prefix to the bucket.
> 3. Click **Upload** and select one or more files, or drag the files directly into the Cloud Console from your local file manager.
> 4. Monitor upload progress in the Cloud Console. When the upload completes, the new objects appear in the file list.
>
> The Cloud Console uses multipart upload and supports resumable uploads, so interrupted transfers can be retried without starting over. For large bulk transfers (hundreds of GB or more), use the AWS CLI, Boto3, or [s5cmd](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd) for better throughput.

### Verify object integrity

CoreWeave AI Object Storage supports checksum algorithms for verifying object integrity on upload and download. For the full list of supported algorithms, see [Checksum algorithms](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#checksum-algorithms).

### Quota limit errors

If you try to upload an object to a bucket in an Availability Zone where capacity quota limits have been reached, you receive an error message:

`<Message>The account is write suspended.</Message>`

To resolve this, you can [request a quota increase](https://docs.coreweave.com/products/storage/object-storage/manage-quotas.md).

## List buckets and their contents

Listing buckets and their contents helps you confirm which buckets exist in your account and verify which objects are stored in a given bucket. You can list buckets and their contents using S3-compatible tools such as the AWS CLI, s3cmd, Boto3, or s5cmd. If you're working with versioned buckets, you can [use rclone](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md#list-objects) to list buckets and their contents, including delete markers.

> [tab] AWS CLI
>
> To see all your available buckets, use the `ls` command:
>
> ```bash theme={"system"}
> aws s3 ls
> ```
>
> To list all the objects in a bucket, use the `ls` command to target a bucket path.
>
> ```bash theme={"system"}
> aws s3 ls s3://[BUCKET-NAME]
> ```
>
> The terminal returns a listing for your selected bucket showing each object, its size, and its last modified date.
>
> ```text title="Example file listing output" theme={"system"}
> 2024-10-14 15:35:10 123456 my-first-file.txt
> 2024-10-14 16:45:22 234567 another-file-of-mine.txt
> ```

> [tab] s3cmd
>
> To list all your available buckets, use the `ls` command:
>
> ```bash theme={"system"}
> s3cmd ls
> ```
>
> To see the contents of a specific bucket, target the bucket's path using the `s3://` scheme.
>
> ```bash title="Example command" theme={"system"}
> s3cmd ls s3://[BUCKET-NAME]/
> ```
>
> This command outputs a list of file paths including the bucket name and file name. For example:
>
> ```text title="Example output" theme={"system"}
> 2024-10-14 15:35 123456 s3://my-bucket-name/my-first-file.txt
> 2024-10-14 16:45 234567 s3://my-bucket-name/another-file-of-mine.txt
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
> 2. List all your buckets programmatically using the following script:
>
>    ```python title="List all buckets" theme={"system"}
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
>    response = s3.list_buckets()
>
>    print("Existing buckets:")
>    for bucket in response['Buckets']:
>        print(f'  {bucket["Name"]}')
>    ```
>
> 3. To view the contents of a specific bucket, replace `[BUCKET-NAME]` with the name of your bucket:
>
>    ```python title="List objects in a bucket" theme={"system"}
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
>    bucket_name = '[BUCKET-NAME]'
>
>    paginator = s3.get_paginator('list_objects_v2')
>    pages = paginator.paginate(Bucket=bucket_name)
>    object_count = 0
>
>    print(f"Objects in {bucket_name}:")
>    for page in pages:
>        for obj in page.get('Contents', []):
>            print(f'  {obj["Key"]} (Size: {obj["Size"]} bytes)')
>            object_count += 1
>
>    if object_count == 0:
>        print(f"No objects found in {bucket_name}.")
>    ```
>
> The resulting output looks similar to the following:
>
> ```text title="Example output" theme={"system"}
> Objects in my-bucket-name:
> my-first-file.txt (Size: 4500 bytes)
> another-file-of-mine.txt (Size: 5400 bytes)
> ```

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> To list all your available buckets:
>
> ```bash theme={"system"}
> s5cmd --endpoint-url https://cwobject.com ls
> ```
>
> To list the objects in a specific bucket, replace `[BUCKET-NAME]` with the name of your bucket:
>
> ```bash theme={"system"}
> s5cmd --endpoint-url https://cwobject.com ls 's3://[BUCKET-NAME]/*'
> ```

> [tab] Cloud Console
>
> 1. In the [Cloud Console](https://console.coreweave.com/object-storage/buckets), navigate to **Object Storage** > **Buckets** to see all the buckets in your organization.
> 2. Select a bucket to open it. The Cloud Console displays objects and folder prefixes in the bucket, along with each object's key, size, and created date.
> 3. Click a folder to navigate into it, or use the prefix path at the top of the page to navigate back to parent folders or the bucket root.
>
> To find a bucket by name, or to find an object by name within the current bucket, use the search bar in the Cloud Console.
>
> To download an object, select it and click **Download**. The Cloud Console can download objects in any storage class, including the Archive tier; no restore operation is required.

## Delete an object from a bucket

Delete objects you no longer need to free up capacity and keep your buckets organized. Deletions are permanent on buckets that don't have versioning enabled, so confirm the target object before you run these commands.

> [tab] AWS CLI
>
> To delete specific objects from a bucket, use the `rm` command with the AWS CLI.
>
> ```bash theme={"system"}
> aws s3 rm s3://[BUCKET-NAME]/[OBJECT-NAME]
> ```
>
> When this succeeds, a confirmation message like this one appears:
>
> ```text title="Example output" theme={"system"}
> delete: s3://my-bucket-name/my-important-file.txt
> ```

> [tab] s3cmd
>
> To delete an object from a bucket, use the `del` command.
>
> ```bash title="Example command" theme={"system"}
> s3cmd del s3://[BUCKET-NAME]/[OBJECT-NAME]
> ```
>
> If the deletion succeeds, a confirmation message appears:
>
> ```text title="Example output" theme={"system"}
> Object s3://my-bucket-name/my-important-file.txt deleted
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
> 2. Use the following script to delete an object from a bucket. Replace `[BUCKET-NAME]` with the name of the bucket and `[OBJECT-NAME]` with the key of the object to delete.
>
>    ```python title="Delete an object from a bucket" theme={"system"}
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
>    bucket_name = '[BUCKET-NAME]'
>    object_name = '[OBJECT-NAME]'
>
>    s3.delete_object(Bucket=bucket_name, Key=object_name)
>
>    print(f'Object {object_name} deleted from {bucket_name}')
>    ```
>
> If successful, a success message appears:
>
> ```text title="Example output" theme={"system"}
> Object my-important-file deleted from my-bucket-name
> ```

> [tab] s5cmd
>
> > [!NOTE]
> >
> > **Use the CoreWeave fork of `s5cmd` with AI Object Storage**
> >
> > The upstream [`s5cmd`](https://github.com/peak/s5cmd) uses path-style addressing with custom endpoint URLs. AI Object Storage doesn't support path-style addressing and requires virtual-hosted style URLs. Use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd), which is compatible with AI Object Storage and can safely replace any existing `s5cmd` installation. For setup and usage, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).
>
> To delete an object from a bucket, use the `rm` command. Replace `[BUCKET-NAME]` with the bucket name and `[OBJECT-NAME]` with the object key.
>
> ```bash title="Delete an object with s5cmd" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       rm s3://[BUCKET-NAME]/[OBJECT-NAME]
> ```
>
> To delete multiple objects matching a pattern, replace `[PREFIX]` with the object key prefix to match:
>
> ```bash title="Delete objects matching a pattern" theme={"system"}
> s5cmd --endpoint-url https://cwobject.com \
>       rm 's3://[BUCKET-NAME]/[PREFIX]/*'
> ```

> [tab] Cloud Console
>
> 1. In the [Cloud Console](https://console.coreweave.com/object-storage/buckets), open the bucket and navigate to the object's folder.
>
> 2. Select one or more objects or folders to delete. To delete every object under a prefix, select the folder itself.
>
> 3. Click **Delete**. The Cloud Console displays a confirmation dialog listing the items to delete.
>
> 4. Confirm the deletion. The objects are permanently removed from the bucket.
>
> > [!WARNING]
> >
> > Deleting a folder in the Cloud Console removes all objects under that prefix. Review the confirmation dialog before proceeding.

> [!NOTE]
>
> For more information about accessing and interacting with the contents of your buckets, see the [official Amazon documentation for S3 buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html).

To safely identify and remove objects your workloads no longer access, for example to reclaim capacity in a shared bucket, see [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md).

## Rename an object

Rename an object to change its key without re-uploading the underlying data. This is useful when you need to correct a typo, restructure a key prefix, or align object names with a new naming convention.

Make sure you have the following to rename an object:

* `s3:PutObject` and `s3:DeleteObject` permissions.
* A bucket that **does not** have versioning enabled, now or in the past.
* A request scoped to renaming a single object within the same bucket. The source and destination keys must be in the same bucket.

For more information, see [Rename Objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md).

> [!NOTE]
>
> s5cmd does not support the atomic `RenameObject` API. Use the AWS CLI or Boto3 for atomic renames.

> [tab] AWS CLI
>
> To rename an object, use the `aws s3api rename-object` command with the AWS CLI.
>
> Replace the following placeholders with the appropriate values for your request:
>
> * `[BUCKET-NAME]`: The name of the bucket containing the object.
> * `[SOURCE-OBJECT-NAME]`: The current name of the object.
> * `[DESTINATION-OBJECT-NAME]`: The new name for the object.
>
> ```bash title="Rename object" theme={"system"}
> aws s3api rename-object \
>   --bucket [BUCKET-NAME] \
>   --key [DESTINATION-OBJECT-NAME] \
>   --rename-source [SOURCE-OBJECT-NAME]
> ```
>
> When this succeeds, a confirmation message appears:
>
> ```text title="Example output" theme={"system"}
> rename: s3://my-bucket-name/my-important-file.txt -> s3://my-bucket-name/my-new-file.txt
> ```

> [tab] s3cmd
>
> To rename an object, use the `mv` command with s3cmd.
>
> > [!WARNING]
> >
> > **Copy and delete operation**
> >
> > The s3cmd `mv` command performs a copy and delete operation instead of an atomic rename operation. For atomic rename operations, use the AWS CLI or Boto3 with the `RenameObject` API.
>
> > [!TIP]
> >
> > To prevent accidental overwrites when uploading objects, use the `If-None-Match: *` header with `PutObject`. For details, see [Conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes).
>
> Replace the following placeholders with the appropriate values for your request:
>
> * `[BUCKET-NAME]`: The name of the bucket containing the source object.
> * `[SOURCE-OBJECT-NAME]`: The name of the source object to rename.
> * `[DESTINATION-OBJECT-NAME]`: The new name for the object.
>
> ```bash title="Rename object" theme={"system"}
> s3cmd mv s3://[BUCKET-NAME]/[SOURCE-OBJECT-NAME] s3://[BUCKET-NAME]/[DESTINATION-OBJECT-NAME]
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
> 2. Use the [`rename_object`](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/rename_object.html) method to rename an object. Replace `[BUCKET-NAME]`, `[SOURCE-OBJECT-NAME]`, and `[DESTINATION-OBJECT-NAME]` with the appropriate values for your request.
>
>    ```python title="Rename an object" theme={"system"}
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
>    response = s3.rename_object(
>        Bucket='[BUCKET-NAME]',
>        Key='[DESTINATION-OBJECT-NAME]',
>        RenameSource='[SOURCE-OBJECT-NAME]'
>    )
>
>    print('Object renamed successfully.')
>    ```

> [tab] Cloud Console
>
> 1. In the [Cloud Console](https://console.coreweave.com/object-storage/buckets), open the bucket.
> 2. Select the object you want to rename.
> 3. Choose **Rename** and enter the new object key. The rename is performed within the same bucket.
>
> The bucket must not have versioning enabled or have had versioning enabled in the past. See [Rename objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md) for the full list of restrictions.
