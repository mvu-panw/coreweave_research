# Access BYOB using pre-signed URLs

Source: https://docs.coreweave.com/products/wandb/platform/hosting/data-security/presigned-urls

# Access BYOB using pre-signed URLs

> Learn how Weights & Biases uses pre-signed URLs for blob storage, team-level access control, and audit logging.

Weights & Biases uses pre-signed URLs to simplify access to blob storage from your AI workloads or user browsers. This page explains how pre-signed URLs work in Weights & Biases. It also outlines the access controls, network restrictions, and audit logging that administrators should configure to secure blob storage access.

For background on pre-signed URLs, refer to the cloud provider's documentation:

* [Pre-signed URLs for AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html), which also applies to S3-compatible storage like [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md).
* [Signed URLs for Google Cloud Storage](https://cloud.google.com/storage/docs/access-control/signed-urls).
* [Shared Access Signature for Azure Blob Storage](https://learn.microsoft.com/azure/storage/common/storage-sas-overview).

Pre-signed URLs work as follows:

1. When needed, AI workloads or user browser clients within your network request pre-signed URLs from Weights & Biases.
2. Weights & Biases responds to the request by accessing the blob storage to generate the pre-signed URL with the required permissions.
3. Weights & Biases returns the pre-signed URL to the client.
4. The client uses the pre-signed URL to read from or write to the blob storage.

A pre-signed URL expires after the following durations:

* **Read operations**: 1 hour.
* **Write operations**: 24 hours, to allow more time to upload large objects in chunks.

## Team-level access control

Each pre-signed URL is restricted to specific buckets based on [team-level access control](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-teams) in the Weights & Biases platform. Consider a user who belongs to only one team, and that team is mapped to a storage bucket using the [secure storage connector](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md). In this case, the pre-signed URLs generated for their requests can't access storage buckets mapped to other teams.

> [!NOTE]
>
> Weights & Biases recommends adding users only to the teams they need to belong to.

## Network restriction

Weights & Biases recommends using IAM policies to restrict the networks that can use pre-signed URLs to access external storage. This helps ensure that only networks running your AI workloads, or gateway IP addresses that map to your user machines, can access your Weights & Biases-specific buckets.

Consult your cloud provider's documentation for guidance on configuring these IAM policies:

* For CoreWeave AI Object Storage, refer to [Bucket policy reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#condition) in the CoreWeave documentation.
* For AWS S3 or S3-compatible storage like MinIO hosted on your premises, refer to the [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html#PresignedUrlUploadObject-LimitCapabilities), the [MinIO documentation](https://github.com/minio/minio), or the documentation for your S3-compatible storage provider.

## Audit logs

Weights & Biases recommends using [Weights & Biases audit logs](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/audit-logging.md) together with blob-storage-specific audit logs. For blob storage audit logs, refer to the documentation for each cloud provider:

* [CoreWeave audit logs](https://docs.coreweave.com/products/storage/object-storage/auth-access/audit-logging.md#audit-logging-policies).
* [AWS S3 access logs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html).
* [Google Cloud Storage audit logs](https://cloud.google.com/storage/docs/audit-logging).
* [Monitor Azure Blob Storage](https://learn.microsoft.com/azure/storage/blobs/monitor-blob-storage).

Admin and security teams can use audit logs to track what each user does in Weights & Biases and take action if they need to limit certain operations for specific users.

> [!NOTE]
>
> Pre-signed URLs are the only supported blob storage access mechanism in Weights & Biases. Weights & Biases recommends configuring some or all of the preceding security controls to fit your organization's needs.

## Determine the user that requested a pre-signed URL

To correlate pre-signed URL activity with specific Weights & Biases users when reviewing audit logs, inspect the provider-specific query parameter that Weights & Biases appends to each URL:

| Storage provider | Query parameter | Value |
| - | - | - |
| CoreWeave AI Object Storage | `X-User` | username |
| AWS S3 | `X-User` | username |
| Google Cloud Storage | `X-User` | username |
| Azure Blob Storage | `scid` | Deterministic UUID derived from the username |

### Correlate Azure Blob Storage activity with a user

Azure requires `scid` to be a GUID, so Weights & Biases derives a stable UUID from the username instead of including the username directly. The UUID doesn't contain the username and you can't decode it. To correlate Azure storage activity with a user, compute or maintain a mapping between usernames and their corresponding `scid` values.

Azure includes `scid` only on user-delegation SAS URLs, which Weights & Biases generates when the storage bucket is configured with a managed identity. Shared-key SAS URLs don't include `scid`.

> [!NOTE]
>
> Weights & Biases appends attribution parameters to pre-signed URLs by default. To turn off attribution for all storage providers, set the `GORILLA_BUCKET_ATTRIBUTION_DISABLED` environment variable to `true`.  When attribution is off, Weights & Biases omits `scid` and `X-User`, and you can't correlate pre-signed URL activity with individual users.
