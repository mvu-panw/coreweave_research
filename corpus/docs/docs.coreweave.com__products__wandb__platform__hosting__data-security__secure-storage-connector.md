# Bring your own bucket (BYOB)

Source: https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector

# Bring your own bucket (BYOB)

> Store W&B artifacts and data in your own cloud storage buckets using the Bring Your Own Bucket (BYOB) feature.

> [!NOTE]
>
> **This guide applies to all W\&B deployment types:**
>
> * **Multi-tenant Cloud**: Team-level BYOB
> * **Dedicated Cloud**: Instance and team-level BYOB
> * **Self-Managed**: Instance and team-level BYOB
>
> The bucket provisioning instructions in this guide are the same regardless of your deployment type.

> [!WARNING]
>
> This page is for the W\&B platform secure storage connector or BYOB and does not apply to Weave. To render images and video that live in your own cloud bucket in Weave without importing the bytes into Weave, see the [Weave BYOB reference](https://docs.coreweave.com/products/wandb/weave/guides/tracking/byob-references.md#reference-media-in-your-own-bucket-byob-using-weave-op).

## Overview

Bring your own bucket (BYOB) lets you store W\&B artifacts and other sensitive data in your own cloud or on-premises infrastructure. For [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), Weights & Biases doesn't copy the data you store in your bucket to the Weights & Biases managed infrastructure. This page is for Weights & Biases administrators and platform engineers who need to retain ownership of artifact storage to meet data governance, residency, or compliance requirements.

> [!NOTE]
>
> * Communication between W\&B SDK / CLI / UI and your buckets occurs using [pre-signed URLs](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/presigned-urls.md).
> * Weights & Biases uses garbage collection and related processes to remove deleted **artifacts** and **run data** from your bucket over time. For artifact deletion, see [Delete an artifact](https://docs.coreweave.com/products/wandb/artifacts/delete-artifacts.md). Deleted run data on Dedicated Cloud and Self-Managed deployments also depends on `GORILLA_DATA_RETENTION_PERIOD` as described in [Configure environment variables](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md). Weights & Biases doesn't guarantee cleanup timing. For a single overview of bucket usage and costs, see [Manage bucket storage and costs](https://docs.coreweave.com/products/wandb/platform/hosting/managing-bucket-storage.md).
> * You can specify a sub-path when you configure a bucket, to ensure that Weights & Biases doesn't store any files in a folder at the root of the bucket. This helps you better conform to your organization's bucket governance policy.

### Data stored in the central database vs buckets

When you use BYOB functionality, Weights & Biases stores certain types of data in the Weights & Biases central database, and other types in your bucket. Use the following lists to understand which data remains in Weights & Biases-managed infrastructure and which data Weights & Biases writes to your own storage.

#### Database

The Weights & Biases central database stores the following data:

* Metadata for users, teams, artifacts, experiments, and projects.
* Reports.
* Experiment logs.
* System metrics.
* Console logs.

#### Buckets

Your storage bucket stores the following data:

* Experiment files and metrics.
* Artifact files.
* Media files.
* Run files.
* Exported history metrics and system events in Parquet format.

### Bucket scopes

You can configure your storage bucket to one of two scopes:

| Scope | Description |
| - | - |
| Instance level | In [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) and [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md), any user with the required permissions within your organization or instance can access files stored in your instance's storage bucket. Not applicable to [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md). |
| Team level | If you configure a Weights & Biases team to use a team level storage bucket, team members can access files stored in it. Team level storage buckets allow greater data access control and data isolation for teams with sensitive data or strict compliance requirements. Team level storage helps different business units or departments that share an instance to efficiently use the infrastructure and administrative resources. It also lets separate project teams manage AI workflows for separate customer engagements. Available for all deployment types. You configure team level BYOB when you set up the team. |

This design supports different storage topologies, depending on your organization's needs. For example:

* The same bucket can serve the instance and one or more teams.
* Each team can use a separate bucket, some teams can choose to write to the instance bucket, or multiple teams can share a bucket by writing to subpaths.
* Buckets for different teams can reside in different cloud infrastructure environments or regions, and different storage admin teams can manage them.

For example, suppose you have a team called Kappa in your organization. Your organization (and team Kappa) uses the instance level storage bucket by default. Next, you create a team called Omega. When you create team Omega, you configure a team level storage bucket for that team. Team Kappa can't access files that team Omega generates. However, team Omega can access files that team Kappa creates. To isolate data for team Kappa, you must also configure a team level storage bucket for them.

### Availability matrix

Before you begin, confirm that BYOB is available for your deployment type and storage provider. Weights & Biases can connect to the following storage providers:

* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md): High-performance, S3-compatible object storage service optimized for AI workloads.
* [Amazon S3](https://aws.amazon.com/s3/): Object storage service offering scalability, data availability, security, and performance.
* [Google Cloud Storage](https://cloud.google.com/storage): Managed service for storing unstructured data at scale.
* [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs): Cloud-based object storage solution for storing massive amounts of unstructured data like text, binary data, images, videos, and logs.
* S3-compatible storage such as [MinIO Enterprise (AIStor)](https://min.io/product/aistor) or other enterprise-grade solutions hosted in your cloud or on-premises infrastructure.

The following table shows the availability of BYOB at each scope for each Weights & Biases deployment type.

| Weights & Biases deployment type | Instance level | Team level | Additional information |
| - | - | - | - |
| Dedicated Cloud | ✓ | ✓ | Instance and team level BYOB are supported for CoreWeave AI Object Storage, Amazon S3, Google Cloud Storage, Microsoft Azure Blob Storage, and S3-compatible storage such as [MinIO Enterprise (AIStor)](https://www.min.io/product/aistor) hosted in your cloud or on-premises infrastructure. |
| Multi-tenant Cloud | Not applicable | ✓<sup>[1](#footnote_1)</sup> | Team level BYOB is supported for CoreWeave AI Object Storage, Amazon S3, and Google Cloud Storage. |
| Self-Managed | ✓ | ✓ | Instance and team level BYOB are supported for CoreWeave AI Object Storage, Amazon S3, Google Cloud Storage, Microsoft Azure Blob Storage, and S3-compatible storage such as [MinIO Enterprise (AIStor)](https://www.min.io/product/aistor) hosted in your cloud or on-premises infrastructure. |

<sup>1.</sup>Azure Blob Storage is not supported for team level BYOB on Multi-tenant Cloud.

The following sections guide you through the process of setting up BYOB.

## Provision your bucket

After you [verify availability](#availability-matrix), you're ready to provision your storage bucket, including its access policy and CORS. Provisioning creates the bucket that Weights & Biases writes to and grants the Weights & Biases platform the permissions it needs to generate pre-signed URLs on your behalf. Select a tab to continue.

> [tab] CoreWeave
>
> **Requirements**:
>
> * **Multi-tenant Cloud**, or
> * **Dedicated Cloud** v0.73.0 or later, or
> * **Self-Managed** v0.73.0 or later deployed with v0.33.14+ of the Helm chart
> * A CoreWeave account with AI Object Storage enabled and with permission to create buckets, API access keys, and secret keys.
> * Your Weights & Biases instance must be able to connect to CoreWeave network endpoints.
>
> For details, see [Create a CoreWeave AI Object Storage bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md) in the CoreWeave documentation.
>
> 1. **Forge**: Obtain your organization ID, which is required for your bucket policy.
>    1. Log in to the [Forge](https://wandb.ai/site).
>    2. In the left navigation, click **Create a new team**.
>    3. In the drawer that opens, copy the Weights & Biases organization ID, which appears above **Invite team members**.
>    4. Leave this page open. You use it to [configure Weights & Biases](#configure-weights-&-biases).
>
> 2. **Dedicated Cloud** / **Self-Managed**: Obtain your customer namespace, which is required for your bucket policy.
>    1. In the W\&B App, click your user profile icon, then click **System Console**.
>    2. Click the **Authentication** tab.
>    3. At the bottom of the page, copy the value for **Customer Namespace**. Keep this value for configuring the bucket policy.
>    4. You can close the System Console.
>
> 3. In CoreWeave, create the bucket with a name of your choice in your preferred CoreWeave availability zone. Optionally, create a folder for Weights & Biases to use as a sub-path for all Weights & Biases files. Make a note of the bucket name, availability zone, API access key, secret key, and sub-path.
>
> 4. Set the following cross-origin resource sharing (CORS) policy for the bucket:
>
>    ```json theme={"system"}
>    [
>      {
>        "AllowedHeaders": [
>          "*"
>        ],
>        "AllowedMethods": [
>          "GET",
>          "HEAD",
>          "PUT"
>        ],
>        "AllowedOrigins": [
>          "https://wandb.ai",
>          "https://forge.coreweave.com"
>        ],
>        "ExposeHeaders": [
>          "ETag"
>        ],
>        "MaxAgeSeconds": 3000
>      }
>    ]
>    ```
>
>    Set the allowed origins for your deployment type. Browsers fetch objects from the bucket through pre-signed URLs, so the bucket must allow the domain that serves the web UI.
>
>    * **Multi-tenant Cloud**: Keep both origins. `https://wandb.ai` redirects to the web UI at `https://forge.coreweave.com`.
>    * **Dedicated Cloud** or **Self-Managed**: Replace both origins with the URL of your Weights & Biases instance.
>
>    CoreWeave storage is S3-compatible. For details about CORS, see [Configuring cross-origin resource sharing (CORS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html) in the AWS documentation.
>
> 5. Configure a bucket policy that grants the required permissions for your deployment to access the bucket and generate [pre-signed URLs](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/presigned-urls.md) that AI workloads in your cloud infrastructure or user browsers use to access the bucket. See [Bucket Policy Reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) in the CoreWeave documentation.
>
>    ```json theme={"system"}
>    {
>      "Version": "2012-10-17",
>      "Statement": [
>      {
>        "Sid": "AllowWandbUser",
>        "Action": [
>          "s3:GetObject*",
>          "s3:GetEncryptionConfiguration",
>          "s3:ListBucket",
>          "s3:ListBucketMultipartUploads",
>          "s3:ListBucketVersions",
>          "s3:AbortMultipartUpload",
>          "s3:DeleteObject",
>          "s3:PutObject",
>          "s3:GetBucketCORS",
>          "s3:GetBucketLocation",
>          "s3:GetBucketVersioning"
>        ],
>        "Effect": "Allow",
>        "Resource": [
>          "arn:aws:s3:::<cw-bucket>/*",
>          "arn:aws:s3:::<cw-bucket>"
>        ],
>        "Principal": {
>          "CW": "arn:aws:iam::wandb:static/<wb-cw-principal>"
>        },
>        "Condition": {
>          "StringLike": {
>            "wandb:OrgID": [
>              "<wb-org-id>"
>            ]
>          }
>        }
>      },
>      {
>        "Sid": "AllowUsersInOrg",
>        "Action": "s3:*",
>        "Effect": "Allow",
>        "Resource": [
>          "arn:aws:s3:::<cw-bucket>",
>          "arn:aws:s3:::<cw-bucket>/*"
>        ],
>        "Principal": {
>          "CW": "arn:aws:iam::<cw-storage-org-id>:*"
>        }
>      }]
>    }
>    ```
>
>    The clause beginning with `"Sid": "AllowUsersInOrg"` grants users in your organization direct access to the bucket. If you don't need this ability, you can omit the clause from your policy.
>
> 6. In the bucket policy, replace placeholders:
>    * `<cw-bucket>`: your bucket name.
>    * `<cw-wandb-principal>`:
>      * **Multi-tenant Cloud**: `arn:aws:iam::wandb:static/wandb-integration-public`
>      * **Dedicated Cloud** or **Self-Managed**: `arn:aws:iam::wandb:static/wandb-integration`
>    * `<wb-org-id>`:
>      * **Multi-tenant Cloud**: The organization ID from [Provision your bucket](#provision-your-bucket).
>      * **Dedicated Cloud** or **Self-Managed**: The customer namespace from [Provision your bucket](#provision-your-bucket).
>
> 7. **Dedicated Cloud**: Contact [support](mailto:forge-support@coreweave.com) to complete additional steps.
>
> 8. Set environment variable**Self-Managed**: Update your deployment to set the environment variable `GORILLA_SUPPORTED_FILE_STORES` to the exact string `cw://` and restart Weights & Biases. Otherwise, CoreWeave doesn't appear as an option when you configure team storage.
>
> Next, [configure Weights & Biases](#configure-weights-&-biases).

> [tab] AWS
>
> For details, see [Create an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS documentation.
>
> 1. Provision the KMS key.
>
>    Weights & Biases requires you to provision a KMS key to encrypt and decrypt the data on the S3 bucket. The key usage type must be `ENCRYPT_DECRYPT`. Assign the following policy to the key:
>
>    ```json theme={"system"}
>    {
>      "Version": "2012-10-17",
>      "Statement": [
>        {
>          "Sid" : "Internal",
>          "Effect" : "Allow",
>          "Principal" : { "AWS" : "<Your_Account_Id>" },
>          "Action" : "kms:*",
>          "Resource" : "<aws_kms_key.key.arn>"
>        },
>        {
>          "Sid" : "External",
>          "Effect" : "Allow",
>          "Principal" : { "AWS" : "<aws_principal_and_role_arn>" },
>          "Action" : [
>            "kms:Decrypt",
>            "kms:Describe*",
>            "kms:Encrypt",
>            "kms:ReEncrypt*",
>            "kms:GenerateDataKey*"
>          ],
>          "Resource" : "<aws_kms_key.key.arn>"
>        }
>      ]
>    }
>    ```
>
>    Replace `<Your_Account_Id>` and `<aws_kms_key.key.arn>` accordingly.
>
>    If you use [Forge](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) or [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options.md#w%26b-dedicated-cloud), replace `<aws_principal_and_role_arn>` with the corresponding value:
>
>    * **Multi-tenant Cloud**: `arn:aws:iam::725579432336:role/WandbIntegration`
>    * **Dedicated Cloud**: `arn:aws:iam::830241207209:root`
>
>    This policy grants your AWS account full access to the key and also assigns the required permissions to the AWS account that hosts the Weights & Biases platform. Keep a record of the KMS key ARN.
>
> 2. Provision the S3 bucket.
>
>    Follow these steps to provision the S3 bucket in your AWS account:
>
>    1. Create the S3 bucket with a name of your choice. Optionally, create a folder that you can configure as a sub-path to store all Weights & Biases files.
>    2. Enable server-side encryption, using the KMS key from the previous step.
>    3. Configure CORS with the following policy:
>
>       ```json theme={"system"}
>       [
>         {
>             "AllowedHeaders": [
>                 "*"
>             ],
>             "AllowedMethods": [
>                 "GET",
>                 "HEAD",
>                 "PUT"
>             ],
>             "AllowedOrigins": [
>                 "https://wandb.ai",
>                 "https://forge.coreweave.com"
>             ],
>             "ExposeHeaders": [
>                 "ETag"
>             ],
>             "MaxAgeSeconds": 3000
>         }
>       ]
>       ```
>
>       Set the allowed origins for your deployment type. Browsers fetch objects from the bucket through pre-signed URLs, so the bucket must allow the domain that serves the web UI.
>
>       * **Multi-tenant Cloud**: Keep both origins. `https://wandb.ai` redirects to the web UI at `https://forge.coreweave.com`.
>
>       * **Dedicated Cloud** or **Self-Managed**: Replace both origins with the URL of your Weights & Biases instance.
>
>       > [!NOTE]
>       >
>       > If data in your bucket expires because of an [object lifecycle management policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html), you may lose the ability to read the history of some runs.
>    4. Grant the required S3 permissions to the AWS account that hosts the Weights & Biases platform, which requires these permissions to generate [pre-signed URLs](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/presigned-urls.md) that AI workloads in your cloud infrastructure or user browsers use to access the bucket.
>
>       ```json theme={"system"}
>       {
>         "Version": "2012-10-17",
>         "Id": "WandBAccess",
>         "Statement": [
>           {
>             "Sid": "WAndBAccountAccess",
>             "Effect": "Allow",
>             "Principal": { "AWS": "<aws_principal_and_role_arn>" },
>               "Action" : [
>                 "s3:GetObject*",
>                 "s3:GetEncryptionConfiguration",
>                 "s3:ListBucket",
>                 "s3:ListBucketMultipartUploads",
>                 "s3:ListBucketVersions",
>                 "s3:AbortMultipartUpload",
>                 "s3:DeleteObject",
>                 "s3:PutObject",
>                 "s3:GetBucketCORS",
>                 "s3:GetBucketLocation",
>                 "s3:GetBucketVersioning"
>               ],
>             "Resource": [
>               "arn:aws:s3:::<wandb_bucket>",
>               "arn:aws:s3:::<wandb_bucket>/*"
>             ]
>           }
>         ]
>       }
>       ```
>
>       Replace `<wandb_bucket>` accordingly and keep a record of the bucket name. Next, [configure Weights & Biases](#configure-weights-&-biases).
>
>       If you use [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) or [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), replace `<aws_principal_and_role_arn>` with the corresponding value.
>
>       * For [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md): `arn:aws:iam::725579432336:role/WandbIntegration`
>       * For [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md): `arn:aws:iam::830241207209:root`
>
> For more details, see the [AWS Self-Managed hosting guide](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options.md).

> [tab] Google Cloud
>
> For details, see [Create a bucket](https://docs.cloud.google.com/storage/docs/creating-buckets) in the Google Cloud documentation.
>
> 1. Provision the GCS bucket.
>
>    Follow these steps to provision the GCS bucket in your Google Cloud project:
>
>    1. Create the GCS bucket with a name of your choice. Optionally, create a folder that you can configure as a sub-path to store all Weights & Biases files.
>    2. Set encryption type to `Google-managed`.
>    3. Turn on soft deletion. See [Edit a bucket's soft delete policy](https://docs.cloud.google.com/storage/docs/use-soft-delete).
>    4. Set the CORS policy with `gsutil`. This is not possible in the UI.
>
>       1. Create a file named `cors-policy.json` locally.
>
>       2. Copy the following CORS policy into the file and save it.
>
>          ```json theme={"system"}
>          [
>            {
>              "origin": ["https://wandb.ai", "https://forge.coreweave.com"],
>              "responseHeader": ["Content-Type"],
>              "exposeHeaders": ["ETag"],
>              "method": ["GET", "HEAD", "PUT"],
>              "maxAgeSeconds": 3000
>            }
>          ]
>          ```
>
>          Set the allowed origins for your deployment type. Browsers fetch objects from the bucket through pre-signed URLs, so the bucket must allow the domain that serves the web UI.
>
>          * **Multi-tenant Cloud**: Keep both origins. `https://wandb.ai` redirects to the web UI at `https://forge.coreweave.com`.
>
>          * **Dedicated Cloud** or **Self-Managed**: Replace both origins with the URL of your Weights & Biases instance.
>
>          > [!NOTE]
>          >
>          > If data in your bucket expires because of an [object lifecycle management policy](https://cloud.google.com/storage/docs/lifecycle), you may lose the ability to read the history of some runs.
>
>       3. Replace `<bucket_name>` with the correct bucket name and run `gsutil`.
>
>          ```bash theme={"system"}
>          gsutil cors set cors-policy.json gs://<bucket_name>
>          ```
>
>       4. Verify the bucket's policy. Replace `<bucket_name>` with the correct bucket name.
>
>          ```bash theme={"system"}
>          gsutil cors get gs://<bucket_name>
>          ```
> 2. If you use [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) or [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), grant the `storage.admin` role to the Google Cloud service account linked to the Weights & Biases platform. Weights & Biases requires this role to check the bucket's CORS configuration and attributes, such as whether object versioning is enabled. If the service account doesn't have the `storage.admin` role, these checks result in an HTTP 403 error.
>
>    * For [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), the account is: `wandb-integration@wandb-production.iam.gserviceaccount.com`
>    * For [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), the account is: `deploy@wandb-production.iam.gserviceaccount.com`
>
>    Keep a record of the bucket name. Next, [configure Weights & Biases for BYOB](#configure-weights-&-biases).

> [tab] Azure
>
> For details, see [Create a blob storage container](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal) in the Azure documentation.
>
> **Instance level BYOB**:
>
> 1. Provision the Azure Blob Storage container.
>
>    For Self-Managed deployments, and for Dedicated Cloud deployments that don't use [this Terraform module](https://github.com/wandb/terraform-azurerm-wandb/tree/main/examples/byob), follow these steps to provision an Azure Blob Storage container in your Azure subscription:
>
>    1. Create a container with a name of your choice. Optionally, create a folder that you can configure as a sub-path to store all Weights & Biases files.
>    2. Configure the CORS policy on the container.
>
>       To set the CORS policy through the UI, go to the blob storage, scroll down to `Settings/Resource Sharing (CORS)`, and then set the following:
>
>       | Parameter | Value |
>       | - | - |
>       | Allowed Origins | The URL of your Weights & Biases instance |
>       | Allowed Methods | `GET`, `HEAD`, `PUT` |
>       | Allowed Headers | `*` |
>       | Exposed Headers | `*` |
>       | Max Age | `3000` |
>
>       > [!NOTE]
>       >
>       > If data in your bucket expires because of an [object lifecycle management policy](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-configure?tabs=azure-portal), you may lose the ability to read the history of some runs.
> 2. Choose an authentication method:
>
>    * **Storage account key**: Generate a storage account access key and record the key and storage account name. For organizations on Dedicated Cloud, share these values with your Weights & Biases account team using a secure sharing mechanism.
>    * **Workload identity**: Grant an Azure managed identity access to your storage account and configure Weights & Biases to use it. You don't need to share a storage account key. Follow the [workload identity instructions for your deployment type](#set-up-azure-workload-identity).
>
> **Team level BYOB**:
>
> For Dedicated Cloud deployments, Weights & Biases recommends that you use [Terraform](https://github.com/wandb/terraform-azurerm-wandb/tree/main/examples/secure-storage-connector) to provision the Azure Blob Storage container with the necessary access mechanism and permissions. For Dedicated Cloud deployments that don't use Terraform, or for Self-Managed deployments, provision the bucket by following the steps for provisioning instance-level storage. Provide the OIDC issuer URL for your instance. Make a note of the following details:
>
> * Storage account name
> * Storage container name
> * Managed identity client ID
> * Azure tenant ID

> [tab] S3-compatible
>
> Create your S3-compatible bucket. Make a note of:
>
> * Access key
> * Secret access key
> * URL endpoint
> * Bucket name
> * Folder path, if applicable
> * Region

Next, [determine the storage address](#determine-the-storage-address).

## Determine the storage address

After you provision the bucket, you need a storage address that Weights & Biases uses to locate and authenticate to it. The following sections describe the syntax to use to connect a Weights & Biases team to a BYOB storage bucket. In the examples, replace placeholder values between angle brackets (`<>`) with your bucket's details. Select a tab for detailed instructions.

> [tab] CoreWeave
>
> This section is relevant only for team level BYOB on **Dedicated Cloud** or **Self-Managed**. For instance level BYOB or for Multi-tenant Cloud, you're ready to [Configure Weights & Biases](#configure-weights-&-biases).
>
> Determine the full bucket path using the following format. Replace placeholders between angle brackets (`<>`) with the bucket's values.
>
> **Bucket format**:
>
> ```text theme={"system"}
> cw://<accessKey>:<secretAccessKey>@cwobject.com/<bucketName>?tls=true
> ```
>
> Weights & Biases supports the `cwobject.com` HTTPS endpoint. TLS 1.3 is required. Contact [support](mailto:forge-support@coreweave.com) to express interest in other CoreWeave endpoints.

> [tab] AWS
>
> **Bucket format**:
>
> ```text theme={"system"}
> s3://<accessKey>:<secretAccessKey>@<s3_regional_url_endpoint>/<bucketName>?region=<region>
> ```
>
> In the address, the `region` parameter is mandatory unless both your Weights & Biases instance and your storage bucket are deployed on AWS, and the Weights & Biases instance's `AWS_REGION` matches the bucket's AWS S3 region.

> [tab] Google Cloud
>
> **Bucket format**:
>
> ```text theme={"system"}
> gs://<serviceAccountEmail>:<urlEncodedPrivateKey>@<bucketName>
> ```

> [tab] Azure
>
> **Bucket format**:
>
> ```text theme={"system"}
> az://:<urlEncodedAccessKey>@<storageAccountName>/<containerName>
> ```

> [tab] S3-compatible
>
> **Bucket format**:
>
> ```text theme={"system"}
> s3://<accessKey>:<secretAccessKey>@<url_endpoint>/<bucketName>?region=<region>&tls=true
> ```
>
> In the address, the `region` parameter is mandatory.
>
> > [!NOTE]
> >
> > This section is for S3-compatible storage buckets that aren't hosted in S3, such as [MinIO Enterprise (AIStor)](https://www.min.io/product/aistor) or other enterprise-grade S3-compatible solutions hosted on your premises. For storage buckets hosted in AWS S3, see the **AWS** tab instead.
> >
> > MinIO Open Source is in [maintenance mode](https://github.com/minio/minio) with no active development or pre-compiled binaries. For production deployments, use enterprise-grade S3-compatible solutions.
> >
> > For cloud-native storage buckets with an optional S3-compatible mode, use the cloud-native protocol specifier when possible. For example, use `cw://` for a CoreWeave bucket, rather than `s3://`.

After you determine the storage address, you're ready to [configure team level BYOB](#team-level-byob).

## Configure Weights & Biases

After you [provision your bucket](#provision-your-bucket) and [determine its address](#determine-the-storage-address), you're ready to configure BYOB at the [instance level](#instance-level-byob) or [team level](#team-level-byob). This final step tells Weights & Biases to route storage of artifacts, run files, and other large objects to your bucket.

> [!WARNING]
>
> Plan your storage bucket layout carefully. After you configure a storage bucket for Weights & Biases, migrating its data to another bucket is complex and requires assistance from Weights & Biases. This applies to storage for Dedicated Cloud and Self-Managed, as well as team-level storage for Multi-tenant Cloud. For questions, contact [support](mailto:forge-support@coreweave.com).

### Instance level BYOB

> [!NOTE]
>
> For CoreWeave AI Object Storage at the instance level, contact [Support](mailto:forge-support@coreweave.com) instead of following these instructions. Self-service configuration isn't yet supported.

For **Dedicated Cloud**: Share the bucket details with your Weights & Biases team, who configures your instance. For Azure workload identity, [grant access to your storage account](#set-up-azure-workload-identity) and provide the storage account name, container name, and optional path.

For **Self-Managed**, configure instance level BYOB in the W\&B System Console. For Azure workload identity, first complete the [identity setup](#set-up-azure-workload-identity).

1. Log in to Forge as a user with the `admin` role.
2. Click the user icon at the top, then click **System Console**.
3. Navigate to **Settings** > **System Connections**.
4. In **Bucket Storage**, select the **Provider** and enter the bucket details. For Azure, select **Azure Blob Storage (az)**, enter the **Storage account**, and enter the **Blob container** separately.
5. Optional: Enter the **Path** to use in the new bucket.
6. Ensure that the identity or credentials for the selected provider have access to the bucket. For Azure, select an **Authentication** method:
   * **Storage account key**: Enter the **Storage account key**.
   * **Workload identity (user-delegation SAS)**: Use the identity configured by your deployment administrator. If this option is unavailable, complete the [identity setup](#set-up-azure-workload-identity).
7. Click **Save**.

After you save, Weights & Biases uses the configured bucket as the default storage destination for new artifacts and run files at the instance level.

If a setting isn't editable, contact your deployment administrator.

#### Set up Azure workload identity

Workload identity lets Weights & Biases access your Azure bucket without a storage account key. Select your deployment type for the setup instructions.

> [tab] Dedicated Cloud
>
> Weights & Biases configures the deployment. You configure access to your Azure storage account:
>
> 1. Contact your Weights & Biases team with your storage account's tenant ID to confirm which managed identity to use.
> 2. If the identity is in your Azure tenant, use its principal ID for the role assignments below. Otherwise, create or select a managed identity in your tenant and configure its federated credentials using the issuer, subject, and audience values provided by Weights & Biases. A managed identity [can't directly access storage in another tenant](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identities-faq#can-i-use-a-managed-identity-to-access-a-resource-in-a-different-directorytenant).
> 3. Grant the identity's principal **Reader** and **Storage Blob Data Contributor** at storage-account scope on your BYOB storage account.
> 4. Share the storage account name, container name, optional path, and the identity's tenant ID and client ID with your Weights & Biases team.
>
> After Weights & Biases configures the connection, verify access by uploading and downloading a run file or artifact.

> [tab] Self-Managed
>
> As the deployment administrator, configure workload identity in Azure and Kubernetes, then select it in System Console.
>
> Use the following versions for this workflow:
>
> | Component | Required version |
> | - | - |
> | W\&B Server | v0.84.0 or later, including every component that accesses storage |
> | Operator Helm chart | [v0.44.13](https://github.com/wandb/helm-charts/releases/tag/operator-wandb-0.44.13) or later |
> | W\&B System Console | v2.20.0 or later for the authentication selector |
>
> 1. Enable OpenID Connect (OIDC) token federation and Azure workload identity for the Kubernetes cluster. For Azure Kubernetes Service (AKS), follow [Configure Microsoft Entra Workload ID](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster).
> 2. Create or select an Azure managed identity and record its tenant ID, client ID, and principal ID. Grant its principal **Reader** and **Storage Blob Data Contributor** at storage-account scope on your BYOB storage account.
> 3. Configure `global.azureStorageIdentity` in your Helm values with the identity's tenant ID, client ID, and principal ID. Set up federation and the `azure.workload.identity/client-id` annotation for the Kubernetes service accounts that access storage. For Helm configuration details, see [Azure workload identity configuration](https://github.com/wandb/helm-charts/blob/operator-wandb-0.44.13/charts/operator-wandb/README.md#azure-managed-storage-workload-identity).
> 4. Follow the [Console procedure](#instance-level-byob) to select workload identity and save your bucket settings. Verify access by uploading and downloading a run file or artifact.

### Team level BYOB

You can configure team level BYOB when you create a team in the W\&B App or using the [SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#create-team) (POST Groups with optional `storageBucket`). You have two options:

* **Use an existing bucket**: You must [determine the storage location](#determine-the-storage-address) for your bucket first.
* **Create a new bucket** (Multi-tenant Cloud only): Weights & Biases can automatically create a bucket in your cloud provider when you create the team. Weights & Biases supports this for CoreWeave, AWS, and Google Cloud.

> [!NOTE]
>
> * After you create a team, you can't change its storage.
> * For instance level BYOB, see [Instance level BYOB](#instance-level-byob) instead.
> * If you plan to configure CoreWeave storage for the team, review the [CoreWeave requirements](#coreweave-requirements) and contact [support](mailto:forge-support@coreweave.com) to verify that your bucket is configured correctly in CoreWeave and to validate your team's configuration, since you can't change the storage details after you create the team.

Select your deployment type to continue.

> [tab] Multi-tenant Cloud
>
> 1. Switch to the browser window where you previously began to create the new team to find the Weights & Biases organization ID. Otherwise, log in to Forge as a user with the `admin` role, click the icon at the top left to open the left navigation, then click **Create a team to collaborate**.
>
> 2. Provide a name for the team.
>
> 3. Set **Storage Type** to **External storage**.
>
> 4. Click **Bucket location**.
>
> 5. To use an existing bucket, select it from the list.
>
> 6. To create a new bucket, click **Add bucket** at the bottom, then:
>
>    1. Click **Cloud provider** and select **CoreWeave**, **AWS**, or **Google Cloud**.
>    2. Enter the bucket details:
>       * **Name**: Enter the bucket name.
>       * **Path** (optional): Enter a sub-path to use within the bucket.
>    3. Provide additional connection settings for the chosen cloud provider:
>       * CoreWeave: No additional settings required.
>
>       * AWS: Optionally provide a **KMS key ARN** for encryption.
>
>       * Google Cloud: No additional settings required.
>
>    > [!NOTE]
>    >
>    > When you click **Create team**, Weights & Biases automatically creates the bucket in your cloud provider with the specified configuration.
>
> 7. Invite members to the team. In **Invite team members**, specify a comma-separated list of email addresses. Otherwise, you can invite members to the team after you create it.
>
> 8. Click **Create team**.
>
> If Weights & Biases encounters errors accessing the bucket or detects invalid settings, an error or warning displays at the bottom of the page. Otherwise, Weights & Biases creates the team.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. **Dedicated Cloud**: You **must** provide the bucket path to your account team so that they can add it to your instance's supported file stores before you follow the rest of these steps to use the storage bucket for a team.
>
> 2. **Self-Managed**: You **must** add the bucket path to the `GORILLA_SUPPORTED_FILE_STORES` environment variable and then restart Weights & Biases before you follow the rest of these steps to use the storage bucket for a team.
>
> 3. Log in to Forge as a user with the `admin` role, click the icon at the top left to open the left navigation, then click **Create a team to collaborate**.
>
> 4. Provide a name for the team.
>
> 5. Set **Storage Type** to **External storage**.
>
>    > [!NOTE]
>    >
>    > To use the instance level storage for team storage (regardless of whether it's internal or external), leave **Storage Type** set to **Internal**, even if the instance level bucket is configured for BYOB. To use separate external storage for the team, set **Storage Type** for the team to **External** and configure the bucket details in the next step.
>
> 6. Click **Bucket location**.
>
> 7. To use an existing bucket, select it from the list. To add a new bucket, click **Add bucket** at the bottom, then provide the bucket's details.
>
>    Click **Cloud provider** and select **CoreWeave**, **AWS**, **Google Cloud**, or **Azure**.
>
>    If the cloud provider isn't listed, ensure that you've followed the instructions in [Provision your bucket](#set-environment-variable) to add the bucket path to the supported file stores for your instance. If the storage provider is still not listed, [contact support](mailto:forge-support@coreweave.com) for assistance.
>
> 8. Specify the bucket details.
>    * For **CoreWeave**, provide only the bucket name.
>    * For Amazon S3, Google Cloud, or S3-compatible storage, provide the full bucket path you [determined earlier](#determine-the-storage-address).
>    * For Azure on W\&B Dedicated or Self-Managed, set **Account name** to the Azure account and **Container name** to the Azure Blob Storage container.
>    * Optionally, provide additional connection settings:
>      * If applicable, set **Path** to the bucket sub-path.
>      * **CoreWeave**: No additional connection settings required.
>      * **AWS**: Set **KMS key ARN** to the ARN of your KMS encryption key.
>      * **Google Cloud**: No additional connection settings required.
>      * **Azure**: Specify values for **Tenant ID** and **Managed Identity Client ID**. These fields are mandatory unless you configured the connection string with `GORILLA_SUPPORTED_FILE_STORES`.
>
> 9. Click **Create team**.
>
> If Weights & Biases encounters errors accessing the bucket or detects invalid settings, an error or warning displays at the bottom of the page. Otherwise, Weights & Biases creates the team.

## Troubleshooting

If W\&B reports errors when validating or connecting to your bucket, use the following sections to diagnose the most common causes by storage provider.

### CoreWeave

This section helps troubleshoot problems connecting to CoreWeave AI Object Storage.

* **Connection errors**
  * Verify that your Weights & Biases instance can connect to CoreWeave network endpoints.
  * CoreWeave uses virtual-hosted style paths, where the bucket name is a subdomain at the beginning of the path. For example, `cw://bucket-name.cwobject.com` is correct, while `cw://cwobject.com/bucket-name/` isn't.
  * Bucket names must not contain underscores (`_`) or other characters incompatible with DNS rules.
  * Bucket names must be globally unique among CoreWeave locations.
  * Bucket names must not begin with `cw-` or `vip-`, which are reserved prefixes.
* **CORS validation failures**
  * A CORS policy is required. CoreWeave is S3-compatible. For details about CORS, see [Configuring cross-origin resource sharing (CORS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html) in the AWS documentation.
  * `AllowedMethods` must include methods `GET`, `PUT`, and `HEAD`.
  * `ExposeHeaders` must include `ETag`.
  * The CORS policy's `AllowedOrigins` must include the domain that serves the web UI. For Multi-tenant Cloud, include `https://forge.coreweave.com` and `https://wandb.ai`. For Dedicated Cloud or Self-Managed, include the URL of your Weights & Biases instance. If only `https://wandb.ai` is allowed, uploads still succeed, but the UI can't display files from the bucket.
* **LOTA endpoint issues**
  * Weights & Biases doesn't yet support connections to LOTA endpoints. To express interest, [contact support](mailto:forge-support@coreweave.com).
* **Access key and permission errors**
  * Verify that your CoreWeave API access key isn't expired.
  * Verify that your CoreWeave API access key and secret key have sufficient permissions `GetObject`, `PutObject`, `DeleteObject`, `ListBucket`. The examples on this page meet this requirement. See [Create and Manage Access Keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md) in the CoreWeave documentation.

### Google Cloud

This section helps troubleshoot problems connecting to Google Cloud Storage.

* `Bucket does not have soft deletion enabled`
  Ensure that soft deletion is turned on for your Google Cloud Storage bucket. See [Edit a bucket's soft delete policy](https://docs.cloud.google.com/storage/docs/use-soft-delete).
