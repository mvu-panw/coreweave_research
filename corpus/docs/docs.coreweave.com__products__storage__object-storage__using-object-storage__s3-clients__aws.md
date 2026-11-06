# Configure AWS CLI and boto3 for AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/s3-clients/aws

# Configure AWS CLI and boto3 for AI Object Storage

> How to configure AWS CLI and boto3 to use CoreWeave AI Object Storage

This page shows how to configure the AWS CLI and boto3 to interact with CoreWeave AI Object Storage, so you can use AWS tooling against CoreWeave endpoints. We recommend using a separate [AWS profile](https://docs.aws.amazon.com/sdkref/latest/guide/file-format.html#file-format-profile) for Object Storage to avoid conflicts with other AWS profiles and S3-compatible services. Both static credentials and [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) are supported, but we recommend Workload Identity Federation.

> [!NOTE]
>
> If you use [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) with boto3, use `boto3 >= 1.42.5`, which incorporates a required fix for CoreWeave APIs.

## Static credentials

Static credentials are the simplest way to get started when you have an access key and secret key on hand. The same Access Key and Secret Key work with most S3-compatible clients. To set up the AWS shared configuration for Object Storage, create a `cw` profile.

1. Create a new profile and name it `cw`:

   ```bash theme={"system"}
   aws configure --profile cw
   ```

2. When prompted for information, provide the following values:

   | Field | Value |
   | - | - |
   | AWS Access Key ID | The Object Storage [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md). |
   | AWS Secret Key | The Object Storage Secret Key. |
   | Default region name | Optional. To set a default region, use a [CoreWeave Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). |
   | Default output format | Use `json` for JSON output. |

3. Set the endpoint URL to the appropriate endpoint for your use case:

   | Endpoint URL | Description |
   | - | - |
   | `https://cwobject.com` | The primary endpoint for Object Storage. Use this when running outside of a CoreWeave cluster. |
   | `http://cwlota.com` | The [LOTA endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), which routes to the LOTA cache for best performance. Always use the LOTA endpoint when running inside a CoreWeave cluster. |

   ```bash theme={"system"}
   aws configure set endpoint_url http://cwlota.com --profile cw
   ```

4. Set the default addressing style to `virtual`. This is required for Object Storage.

   ```bash theme={"system"}
   aws configure set s3.addressing_style virtual --profile cw
   ```

With your profile in place, the AWS CLI is ready to issue commands against Object Storage using static credentials.

## Workload Identity Federation in Kubernetes

This approach is best for workloads running inside CKS, where short-lived tokens are preferred over long-lived static credentials. When an OIDC token is available in a file and automatically rotated (as in Kubernetes and CKS), use the [Container Credentials API](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html). These configurations work with the AWS CLI, boto3, and other S3 clients that use the AWS credential providers.

Start with a basic config file for the endpoints:

```bash theme={"system"}
aws configure set region US-EAST-04A --profile cw
aws configure set endpoint_url https://cwobject.com --profile cw
aws configure set s3.addressing_style virtual --profile cw
```

This produces a configuration like:

```ini theme={"system"}
[profile cw]
region = US-EAST-04A
endpoint_url = https://cwobject.com
s3 =
    addressing_style = virtual
```

Then set the Container Credentials environment variables. These are often injected automatically by the [Pod Identity Webhook](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/pod-identity-webhook.md).

Replace `[ORG-ID]` with your CoreWeave organization ID.

Your **Org ID** is a short hexadecimal string (for example, `ab1cd2`). Find it on the [Settings page](https://console.coreweave.com/account/settings) of your Cloud Console account.

```bash theme={"system"}
export AWS_PROFILE=cw
export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=/path/to/token

aws s3 ls
```

The SDK reads the token from the file path and exchanges it for temporary credentials at the specified endpoint, then refreshes them automatically before expiry.

## Workload Identity Federation with a credential process

When you want federated credentials outside of CKS, such as on developer workstations or in CI environments, you can use a credential process. Without an auto-rotated token file, AWS SDKs support a [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html) that invokes a custom command to fetch credentials. This works for both human and machine workloads.

The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) provides a ready-made credential process that implements this pattern, including an on-disk cache that lets parallel processes share one credential.

For example, to exchange a CoreWeave API access token, add a line to your AWS config file (`~/.aws/config`) that invokes `cwic auth accesskey api-token`. The `cwic` command reads `COREWEAVE_API_TOKEN`, or the token stored by `cwic auth login`. Credentials are cached per token.

```ini title="Configuration for a CoreWeave API access token" highlight="4" theme={"system"}
[profile cw]
region = US-EAST-04A
endpoint_url = https://cwobject.com
credential_process = cwic auth accesskey api-token
s3 =
    addressing_style = virtual
```

For OIDC token exchange and further examples, see [Share credentials across processes](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/share-credentials-across-processes.md).

### Custom script for credential process

If you want to use a custom script instead of the `cwic auth accesskey` commands, you can set the `credential_process` configuration to the path of your script. For example, if your script is in `/bin/cw-auth.sh`, you can set the `credential_process` configuration to:

```ini title="Configuration with custom script for credential process" highlight="4" theme={"system"}
[profile cw]
region = US-EAST-04A
endpoint_url = https://cwobject.com
credential_process = /bin/cw-auth.sh
s3 =
    addressing_style = virtual
```

When an S3 client invokes a command using this profile, it runs the specified script and expects output in this format:

```json title="Standard JSON output format for credentials" theme={"system"}
{
    "Version": 1,
    "AccessKeyId": "[ACCESS-KEY-ID]",
    "SecretAccessKey": "[SECRET-ACCESS-KEY]",
    "SessionToken": "[SESSION-TOKEN]",
    "Expiration": "[RFC3339-TIMESTAMP]"
}
```

The script implementation depends on your platform. It might perform an interactive browser sign-in, fetch a GitHub Actions ID token, or use another identity provider. The general pattern is:

1. Check for cached credentials.
2. Obtain a new OIDC token from your identity provider if the cached credentials are missing or expired.
3. Exchange the token with the CoreWeave API for temporary credentials.
4. Cache and return the response.
