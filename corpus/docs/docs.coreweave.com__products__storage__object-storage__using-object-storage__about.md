# Connect to Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/about

# Connect to Object Storage

> Authentication methods and client setup for CoreWeave AI Object Storage

This page helps you connect to CoreWeave AI Object Storage by selecting an authentication method, configuring an S3-compatible client, and starting to work with objects in your buckets. It's for developers and operators who prepare applications or tools to interact with Object Storage.

## Authentication methods

Object Storage supports several authentication methods. Choose the method that best fits your use case, then continue to [Configure your client](#configure-your-client).

### OIDC Workload Identity Federation (recommended)

For production workloads, [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) provides a secure authentication method. Your applications obtain tokens from your identity provider and exchange them for temporary CoreWeave access credentials that automatically expire.

In Kubernetes environments, the [Container Credentials API](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html) enables automatic credential rotation without application changes. For setup details, see [Configure AWS CLI and boto3](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md).

### Direct access token exchange

If you already authenticate with a CoreWeave API access token, you can exchange it directly for temporary credentials using the Container Credentials API, without creating a separate static Access Key. The temporary credentials also carry the principal's SCIM group memberships for [group-based and attribute-based access control](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#attribute-based-access-control). For setup details, see [Direct access token exchange](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md).

### Credential process

The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) provides ready-made [credential process](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html) commands, so you don't need to write and maintain your own script. AWS SDKs run the command named in your AWS config to fetch and refresh credentials. The CLI commands cache the exchanged keys, so parallel processes that use the same profile share one credential instead of each performing their own exchange. This works for interactive sign-in and for machine workloads. See [Share credentials across processes](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/share-credentials-across-processes.md).

If those commands don't cover your token exchange, you can still point `credential_process` at a custom script. For that pattern, see [Configure AWS CLI and boto3](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md#workload-identity-federation-with-a-credential-process).

### Static credentials

For initial testing and development, you can use static Access Keys created through the [Cloud Console](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md). Static credentials are long-lived and require manual rotation, so they aren't recommended for production use.

> [!WARNING]
>
> Static Access Keys are a security risk in production environments because they are long-lived and can be leaked. Use [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) instead.

## Configure your client

After choosing an authentication method, configure your S3-compatible client:

* Cloud Console: no additional client configuration required. Sign in to the [Cloud Console](https://console.coreweave.com/object-storage/buckets) and [browse objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) directly.
* [AWS CLI and boto3](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws.md)
* [rclone](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/rclone.md)
* [Cyberduck](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/cyberduck.md)
* [s3cmd](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/s3cmd.md)

## Work with objects

With authentication set up and your client configured, you're ready to interact with your data. You can [manage objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) in your buckets, including uploads, listings, deletions, and renames.

For endpoint configuration details, including virtual-hosted addressing and LOTA endpoints, see [Set endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md).
