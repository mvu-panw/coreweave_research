# Get started with CoreWeave AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/get-started-caios

# Get started with CoreWeave AI Object Storage

> Set up Object Storage authentication, policies, and storage access for enterprise workloads

This guide walks administrators through granting access to Object Storage and authorized users through creating a bucket and uploading an object.

## Before you begin

Determine which parts of this guide apply to you:

* Object Storage administrators must have the [Object Storage Admin IAM role](https://docs.coreweave.com/security/iam/access-policies/roles.md#object-storage) or the `cwobject:EnsureAccessPolicy` permission to create and update organization access policies. These control plane actions use the [AI Object Storage API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md). Start at [Create an organization access policy](#create-an-organization-access-policy).
* Object Storage users following this guide need the `cwobject:CreateAccessKey` permission and the `s3:` permissions required for their storage operations. You also need a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md). The resulting access key authenticates your requests to the [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md). If you're not an administrator, start at [Get access keys](#get-access-keys).

## Get access to Object Storage

Accessing Object Storage requires authorization through an organization access policy and credentials through an access key. An Object Storage administrator configures the policy, and the authorized user obtains credentials. The access key authenticates requests to the S3-compatible API, while the organization access policy determines which `s3:` operations the user can perform.

### Create an organization access policy

This section applies to Object Storage administrators. For a new CoreWeave organization, create at least one [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md). You must create the policy before anyone in the organization can access the Object Storage S3-compatible API. The policy must authorize both credential creation and the storage operations that other users in your organization need.

If your organization already has an organization access policy, you can create a new policy to grant additional permissions to users, or edit the existing policy to grant additional permissions. You can grant the `cwobject:EnsureAccessPolicy` permission to allow other administrators to create organization access policies.

For quick testing and validation, the following policy grants one CoreWeave user full access to all S3 buckets and objects in your organization. On the [**Settings**](https://console.coreweave.com/account/settings) page, find the user's identifier (UID), then create the policy using the Cloud Console:

1. In the Cloud Console, navigate to the [**Object storage access policies**](https://console.coreweave.com/object-storage/access-policies) page.
2. In the **Object storage access** tab, click **Create policy**.
3. In the **Create object storage access policy** page, enter the **Policy name**. For example, "admin-test-policy".
4. Within the policy, add one statement. In the **Statement** section, enter a descriptive **Name** for the statement. For example, "full-admin-access".
5. For **Access**, select **Allow access**.
6. For **Principals**, enter `coreweave/[USER-UID]`. Replace `[USER-UID]` with your user UID.
7. For both **Actions** and **Resources**, enter `*`. This allows the user to perform all actions on all resources in the organization.
8. To create the policy, click **Submit**.

Alternatively, you can [create a policy programmatically](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) using the AI Object Storage API or the CoreWeave Terraform provider. See [examples of organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/examples.md).

To allow other users in your organization to create access keys, grant them the `cwobject:CreateAccessKey` permission. Also grant them the `s3:` permissions required for their storage operations. The [Cloud Console permissions reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/console-permissions.md) provides a complete table that maps Object Storage permissions to actions available in the Cloud Console.

After you create the organization access policy, other users in your organization can obtain access keys and perform the `s3:` operations that the policy allows. They can see the corresponding actions in the Cloud Console.

### Get access keys

[Access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md) authenticate users and workloads to the Object Storage S3-compatible API. This section shows how to create static access keys for testing and validation. If you already have a CoreWeave API access token, [exchange it for temporary access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md) instead of creating static access keys.

To create access keys, you need either the Object Storage Admin IAM role or an organization access policy that grants your identity `cwobject:CreateAccessKey`. You also need a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md).

1. In the Cloud Console, navigate to the [Object storage access keys](https://console.coreweave.com/object-storage/access-keys) page.
2. In the upper right corner, click **Create key**.
3. In the **Create access key** modal:
   1. Enter a **Name** for the access key.
   2. For **Duration**, select the desired duration for the access key.
4. Click **Create key**.
5. Save the **Access Key ID** and **Secret Key** for later use.

After you save both values, you have the credentials required to authenticate to the S3-compatible API.

For production workloads, use [OpenID Connect (OIDC) Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md).

## Set CoreWeave-specific configurations

The following sections describe how to set CoreWeave-specific configurations in your development environment. If you're using the Cloud Console, skip these sections and proceed to [Create a bucket](#create-a-bucket).

### Select an endpoint for improved performance

Object Storage works with [LOTA (Local Object Transport Accelerator)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), a local proxy for Object Storage. To improve performance, always use the LOTA endpoint when running inside a CoreWeave cluster. For tuning guidance, see [Performance best practices](https://docs.coreweave.com/products/storage/object-storage/improving-performance/best-practices.md).

| Endpoint | URL | Notes |
| - | - | - |
| Primary endpoint | `https://cwobject.com` | Uses HTTPS and requires TLS v1.3. Ensure your S3-compatible tools and OpenSSL use TLS v1.3. Use this endpoint when running outside of a CoreWeave cluster. |
| LOTA endpoint | `http://cwlota.com` | Uses HTTP protocol, not HTTPS. To improve performance, the LOTA endpoint routes to the LOTA cache. Always use this endpoint when running inside a CoreWeave cluster. |

### Create a CoreWeave configuration profile

Before you create your first bucket in Object Storage, apply the following settings in your AWS configuration file or environment variables. This one-time configuration adds CoreWeave-specific settings to your development environment.

In this section, you'll create a configuration profile for your Object Storage access keys. You'll also set your default endpoint URL and virtual addressing style. We recommend using a separate profile for Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services.

1. Create a new profile and name it `cw`:

   ```bash title="Create a new profile" theme={"system"}
   aws configure --profile cw
   ```

2. When prompted for information, provide the following values:

   | Field | Value |
   | - | - |
   | AWS Access Key ID | The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your Object Storage Access Key. |
   | AWS Secret Access Key | The Secret Key of your Object Storage Access Key. |
   | Default region name | Optional. To set a default region, see the [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones). |
   | Default output format | Use `json` for JSON output. |

3. Set the default endpoint URL to the appropriate endpoint for your use case:

   * The primary endpoint, `https://cwobject.com`, for use when running outside of a CoreWeave cluster.
   * The LOTA endpoint, `http://cwlota.com`, for use when running inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path to improve performance.

   ```bash title="Set the primary endpoint for local development" theme={"system"}
   aws configure set endpoint_url https://cwobject.com --profile cw
   ```

4. Set the S3 `addressing_style` to `virtual`:

   ```bash title="Set virtual addressing style" theme={"system"}
   aws configure set s3.addressing_style virtual --profile cw
   ```

   This setting is required because Object Storage doesn't support the `path` addressing style.

Your `cw` profile is now configured to use the selected Object Storage endpoint and virtual addressing style.

For full configuration examples, including `boto3`, see [Set endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md).

## Create a bucket

After you have access to Object Storage, you can [create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md) to store data. Object Storage uses buckets as the primary organizational unit for object data.

To create a bucket with the CoreWeave Cloud Console, follow these steps:

1. In the Cloud Console, select **Data and storage** > [**Object storage**](https://console.coreweave.com/object-storage/buckets).
2. In the **Object storage** tab, click **Create bucket**.
3. In the **Create bucket** modal, enter a valid **Bucket name**.

   > [accordion] Bucket naming rules
   >
   > Bucket names must be globally unique and adhere to the following rules:
   >
   > * **Length:** 3 to 63 characters.
   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
   > * **Prohibited patterns:** Cannot start with `xn--`.
   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.
4. Select the [**Super Region**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#geographical-hierarchy) (for example, **Europe** or **US-Central**) for the bucket.
5. In the **Zone** dropdown menu, select the desired Availability Zone for the bucket.
6. Click **Create**.

The bucket is now ready to store objects.

Alternatively, you can create buckets programmatically using [S3-compatible tools](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md#create-a-bucket-with-cli-clients) or the [CoreWeave Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs/resources/object_storage_bucket).

## Upload data to a bucket

To upload and manage objects with the Cloud Console, follow these steps:

1. In the Cloud Console, navigate to the [**Object storage**](https://console.coreweave.com/object-storage/buckets) page.
2. Click the name of the bucket you want to upload data to. The bucket view opens.
3. Use the bucket view to upload, download, browse, and delete objects. See [Manage objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) for the full set of Cloud Console operations.

For a desktop alternative, [use Cyberduck](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/cyberduck.md) as a graphical storage browser.

Object Storage is S3-compatible, so you can use any S3-compatible tool to manage your data. To learn how to use Object Storage with the Cloud Console, `s3cmd`, `boto3`, or the AWS CLI, see [Manage objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md). For high-performance and bulk transfers, use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd). For instructions, see [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).

For example, use the AWS CLI to copy a file into a bucket addressed using the `s3://` scheme:

Replace `[LOCAL-FILE-PATH]` with the path to the file to upload and `[BUCKET-NAME]` with the name of your bucket.

```bash title="Example command" theme={"system"}
aws s3 cp [LOCAL-FILE-PATH] s3://[BUCKET-NAME] --profile cw
```

```text title="Example output" theme={"system"}
upload: ./my-important-file.txt to s3://my-bucket-name/my-important-file.txt
```

If you prefer to work with objects through a Portable Operating System Interface (POSIX) filesystem, you can mount a bucket with a Filesystem in Userspace (FUSE) tool. This workflow has community support and isn't a managed feature. For read-heavy training workloads, a native S3 software development kit (SDK) with LOTA usually performs better. For guidance, see [Can I mount an Object Storage bucket as a filesystem?](https://docs.coreweave.com/support/storage/articles/can-i-mount-an-object-storage-bucket-as-a-filesystem).

Object Storage has default quota limits. See [Manage quota limits](https://docs.coreweave.com/products/storage/object-storage/manage-quotas.md) for more information.

## Next steps

Now that you've created a bucket and uploaded data, you can set up authentication for production workloads and configure bucket access policies and versioned buckets.

### Set a bucket access policy

You can set a [bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) to control a specific bucket and its objects. Both the requesting principal's organization access policy and the bucket access policy, when one exists, must allow the request. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation). To control the resource, including access from other organizations, use a bucket access policy. Those principals must also have an organization access policy in their own organization that allows the action.

You can set bucket access policies programmatically with S3-compatible tools such as the AWS CLI, `s3cmd`, or `boto3`. You can also use the CoreWeave Terraform provider. You can't create bucket access policies with the Cloud Console. For instructions, see [how to manage bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md).

### Manage versioned buckets

Versioned buckets let you keep multiple variants of an object in the same bucket. When you enable versioning, Object Storage assigns a unique version ID to each object. You can then retrieve, restore, or delete specific versions of an object. Versioning is disabled by default.

You can use `rclone` and the AWS CLI to manage versioned buckets with Object Storage. For more information, see [Versioned buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md).

### Set up authentication for production workloads

You can use OIDC Workload Identity Federation to implement secure, automated credential management for production workloads. OIDC Workload Identity Federation generates time-limited access keys and is the default Workload Identity Federation protocol for Object Storage production workloads.

Before you can generate access keys using OIDC Workload Identity Federation, you must configure it for your organization.

1. [Configure OIDC Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for your organization.
2. [Configure your environment](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md#step-5-configure-your-environment) to generate temporary access keys for your production workloads.

### API reference and compatibility information

Use the following references:

* For the AI Object Storage API reference, see the [AI Object Storage API documentation](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md).
* For S3-compatible API reference, see the [S3-compatible API documentation](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md).
* For the mapping of Object Storage actions to permissions, see the [Cloud Console permissions reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/console-permissions.md).
