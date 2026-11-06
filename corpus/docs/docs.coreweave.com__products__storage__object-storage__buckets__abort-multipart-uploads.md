# Abort incomplete multipart uploads

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/abort-multipart-uploads

# Abort incomplete multipart uploads

> Find and abort incomplete multipart uploads to free storage and unblock bucket deletion.

A multipart upload (MPU) is an S3-compatible operation that uploads a large object in independent parts. If the client crashes, loses its connection, or otherwise stops before calling `CompleteMultipartUpload` or `AbortMultipartUpload`, the uploaded parts remain in the bucket as an **incomplete multipart upload**. Incomplete multipart uploads consume storage, do not appear in normal object listings, and prevent the bucket from being deleted.

Use this page when you need to:

* Free storage occupied by abandoned upload parts.
* Unblock a `DeleteBucket` call that fails with `BucketNotEmpty`.
* Reset upload state for a client that is stuck or misbehaving.

To prevent incomplete multipart uploads from accumulating in the first place, configure an [`AbortIncompleteMultipartUpload` lifecycle rule](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies#common-configurations). The procedures on this page handle uploads that already exist; the lifecycle rule prevents them from coming back.

## Prerequisites

Before you start, make sure you have:

* An [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) for the organization that owns the bucket.
* A configured [S3-compatible client](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#manage-buckets-programmatically) (AWS CLI, s3cmd, or Boto3).
* Permission to call [`s3:ListBucketMultipartUploads`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3listmultipartuploads) and [`s3:AbortMultipartUpload`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3abortmultipartupload) on the bucket.

## List incomplete multipart uploads

List the incomplete multipart uploads in a bucket. Each upload has a unique `UploadId` and is identified by the object key it was targeting.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="List incomplete multipart uploads with AWS CLI" theme={"system"}
> aws s3api list-multipart-uploads --bucket [BUCKET-NAME]
> ```
>
> The response includes an `Uploads` array. Each entry has a `Key` (the object key the upload targets), an `UploadId`, and an `Initiated` timestamp.
>
> ```text title="Example output" theme={"system"}
> {
>     "Uploads": [
>         {
>             "Key": "datasets/large-archive.tar",
>             "UploadId": "2~JZ8QkN9R-EXAMPLE-UPLOAD-ID",
>             "Initiated": "2026-04-15T20:14:03.000Z"
>         }
>     ]
> }
> ```
>
> If the bucket has no incomplete multipart uploads, the response is empty.

> [tab] s3cmd
>
> Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="List incomplete multipart uploads with s3cmd" theme={"system"}
> s3cmd multipart s3://[BUCKET-NAME]
> ```
>
> The output lists each in-progress upload with its initiation timestamp, target key, and upload ID.

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
> 2. Replace `[BUCKET-NAME]` with the name of your bucket.
>
>    ```python title="List incomplete multipart uploads with Boto3" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>
>    boto_config = Config(
>        region_name='US-EAST-04A',
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
>    paginator = s3.get_paginator('list_multipart_uploads')
>    for page in paginator.paginate(Bucket='[BUCKET-NAME]'):
>        for upload in page.get('Uploads', []):
>            print(f"{upload['Initiated']}  {upload['UploadId']}  {upload['Key']}")
>    ```

> [!NOTE]
>
> A single call returns up to 1000 uploads. To enumerate every incomplete upload in a bucket, paginate using `KeyMarker` and `UploadIdMarker` from the response (or use the Boto3 paginator shown above).

## Abort a specific multipart upload

Abort one incomplete multipart upload by its `UploadId`. All parts already uploaded for that ID are permanently removed.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]` with your bucket name, `[OBJECT-KEY]` with the upload's target key, and `[UPLOAD-ID]` with the `UploadId` from the listing.
>
> ```bash title="Abort a multipart upload with AWS CLI" theme={"system"}
> aws s3api abort-multipart-upload \
>     --bucket [BUCKET-NAME] \
>     --key [OBJECT-KEY] \
>     --upload-id [UPLOAD-ID]
> ```
>
> A successful call returns no output.

> [tab] s3cmd
>
> s3cmd identifies an upload by its `UploadId` and target object URI. Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[UPLOAD-ID]` with values from the listing.
>
> ```bash title="Abort a multipart upload with s3cmd" theme={"system"}
> s3cmd abortmp s3://[BUCKET-NAME]/[OBJECT-KEY] [UPLOAD-ID]
> ```

> [tab] Boto3
>
> ```python title="Abort a multipart upload with Boto3" theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
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
> s3.abort_multipart_upload(
>     Bucket='[BUCKET-NAME]',
>     Key='[OBJECT-KEY]',
>     UploadId='[UPLOAD-ID]'
> )
> ```

## Abort every incomplete multipart upload in a bucket

To clear every incomplete multipart upload at once, list them and abort each one in a loop. Use this when you are preparing a bucket for deletion or recovering from a large-scale client failure.

> [tab] AWS CLI
>
> This shell loop pages through `list-multipart-uploads` and aborts every upload it finds. Replace `[BUCKET-NAME]` with the name of your bucket.
>
> ```bash title="Abort all incomplete multipart uploads with AWS CLI" theme={"system"}
> BUCKET="[BUCKET-NAME]"
>
> aws s3api list-multipart-uploads --bucket "$BUCKET" \
>     --query 'Uploads[].[Key, UploadId]' \
>     --output text \
> | while read -r KEY UPLOAD_ID; do
>     [ -z "$KEY" ] && continue
>     aws s3api abort-multipart-upload \
>         --bucket "$BUCKET" \
>         --key "$KEY" \
>         --upload-id "$UPLOAD_ID"
>   done
> ```
>
> If the bucket has more than 1000 incomplete multipart uploads, run the loop again until `list-multipart-uploads` returns an empty response.

> [tab] s3cmd
>
> s3cmd does not have a built-in batch abort command. Use the AWS CLI tab or the Boto3 tab to abort uploads in bulk.

> [tab] Boto3
>
> This script paginates through every incomplete multipart upload in the bucket and aborts each one.
>
> ```python title="Abort all incomplete multipart uploads with Boto3" theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> BUCKET = '[BUCKET-NAME]'
>
> boto_config = Config(
>     region_name='US-EAST-04A',
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
> aborted = 0
> paginator = s3.get_paginator('list_multipart_uploads')
> for page in paginator.paginate(Bucket=BUCKET):
>     for upload in page.get('Uploads', []):
>         s3.abort_multipart_upload(
>             Bucket=BUCKET,
>             Key=upload['Key'],
>             UploadId=upload['UploadId'],
>         )
>         aborted += 1
>
> print(f"Aborted {aborted} incomplete multipart uploads in {BUCKET}.")
> ```

## Verify the bucket is clear

After aborting, re-run the [List incomplete multipart uploads](#list-incomplete-multipart-uploads) procedure. The response should be empty. If you were preparing the bucket for deletion, return to [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md) to finish the remaining cleanup steps.

## Prevent recurrence

Apply an [`AbortIncompleteMultipartUpload` lifecycle rule](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies#common-configurations) to every bucket that accepts large uploads. The rule automatically aborts uploads that have not completed within a number of days you specify, and removes the parts.

## Related

* [Bucket lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md): Automate cleanup of incomplete multipart uploads.
* [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md): Full procedure for removing a bucket and its contents.
* [`s3:ListMultipartUploads`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3listmultipartuploads): API reference.
* [`s3:AbortMultipartUpload`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3abortmultipartupload): API reference.
