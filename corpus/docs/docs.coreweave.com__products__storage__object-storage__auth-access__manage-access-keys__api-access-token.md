# Direct access token exchange

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token

# Direct access token exchange

> Exchange a CoreWeave API access token directly for temporary AI Object Storage credentials

You can exchange a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md) directly for temporary AI Object Storage credentials, without creating a separate static Access Key.

If you already authenticate with a CoreWeave API access token, CoreWeave recommends this method over creating a static Access Key in Cloud Console, because it removes the extra key-creation step and carries the principal's SCIM group memberships in the `iam:[ORG-ID]:groups` condition key for [group-based and attribute-based access control](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#attribute-based-access-control).

Your client requests credentials from the AI Object Storage API access token endpoint, passing your API access token as a bearer token.

> [!NOTE]
>
> Exchanging an API access token for temporary credentials requires the `Object Storage Admin` role or an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) that grants `cwobject:CreateAccessKey`.

## Configure your environment

You can set up the exchange in two ways. CoreWeave recommends the CoreWeave Intelligent CLI, because it caches the exchanged credentials and reuses them across commands and processes.

### Use the CoreWeave Intelligent CLI (recommended)

The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) provides `cwic auth accesskey api-token`, a [credential process](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html) that performs the exchange and caches the result on disk. Every command and every process that uses the profile shares one set of credentials until they approach expiry, instead of exchanging its own.

> [!NOTE]
>
> This command requires CoreWeave Intelligent CLI version 1.37.0 or later. Install `cwic` by following the [installation instructions](https://github.com/coreweave/cwic#installation).

1. Authenticate once. On a workstation, pass `--storage keyring` to keep the API access token in your operating system credential store instead of a file on disk:

   ```bash title="Authenticate and store the token in the keyring" theme={"system"}
   cwic auth login --storage keyring
   ```

   This also records the keyring as the backend for that organization, so the Access Keys that `cwic auth accesskey` exchanges later are cached there too, and you don't need to repeat the flag.

   > [!NOTE]
   >
   > A keyring is only reachable from a desktop session, so omit `--storage keyring` on a server, in a container, or in a Pod, where `cwic` uses its on-disk cache instead. For the platform details and the macOS re-authorization prompt after an upgrade, see [Store the cache in your system keyring](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/share-credentials-across-processes.md#store-the-cache-in-your-system-keyring).

2. Add a profile that names the command. Replace `[AVAILABILITY-ZONE]` with the CoreWeave Availability Zone you're using:

   ```ini title="~/.aws/config" theme={"system"}
   [profile coreweave]
   region = [AVAILABILITY-ZONE]
   endpoint_url = https://cwobject.com
   credential_process = cwic auth accesskey api-token
   s3 =
       addressing_style = virtual
   ```

3. Test your configuration by listing your buckets:

   ```bash title="List your buckets" theme={"system"}
   AWS_PROFILE=coreweave aws s3 ls
   ```

`cwic` reads the API access token from the `COREWEAVE_API_TOKEN` environment variable, or, if that's unset, from the token stored by `cwic auth login` for the active organization.

### Set container credential environment variables

Use this method when you can't add the `cwic` binary to the environment, such as a third-party container image. It configures the [AWS container credentials feature](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html) directly, with no extra software.

1. Ensure you're using a supported S3 client. The minimum supported versions are `awscli >= 2.33.2` and `boto3 >= 1.42.5`.

2. Set the following environment variables. Replace `[API-ACCESS-TOKEN]` with your API access token and `[AVAILABILITY-ZONE]` with the CoreWeave Availability Zone you're using:

   ```bash title="Set the environment variables" theme={"system"}
   export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/api-token
   export AWS_CONTAINER_AUTHORIZATION_TOKEN="Bearer [API-ACCESS-TOKEN]"

   aws configure set s3.addressing_style virtual

   export AWS_REGION="[AVAILABILITY-ZONE]"
   export AWS_ENDPOINT_URL_S3="https://cwobject.com"
   ```

3. Test your configuration by listing your buckets:

   ```bash title="List your buckets" theme={"system"}
   aws s3 ls
   ```

With this method the SDK holds the credentials in memory for the life of the process, and nothing is shared between processes. Every new process performs its own exchange, including every `aws` command you run. A workload that starts many processes in parallel produces a matching burst of credential requests. For ways to avoid that, see [Share credentials across processes](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/share-credentials-across-processes.md).

## Results

On success, CoreWeave validates the API access token and returns temporary credentials with the identity format `coreweave/[UID]`. The returned credentials inherit permissions from your [organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) and any applicable [bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md).

## Group-based access control

Because the temporary credentials carry the principal's SCIM group memberships in the `iam:[ORG-ID]:groups` condition key, you can write access policies that grant or deny access based on group membership instead of naming individual principals. To use this:

* [Attribute-based access control](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#attribute-based-access-control): how principal attributes such as group memberships are referenced in policy conditions.
* [Group-based access](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#group-based-access): an example bucket policy that grants access to members of a specific group.
