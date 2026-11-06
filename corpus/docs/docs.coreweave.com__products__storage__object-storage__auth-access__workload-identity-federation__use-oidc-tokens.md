# Use Workload Identity Federation with OIDC

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens

# Use Workload Identity Federation with OIDC

> Exchange OIDC tokens for temporary AI Object Storage credentials using Workload Identity Federation

With OIDC Workload Identity Federation, your workloads obtain an OIDC JWT from your Identity Provider (IdP) and exchange it for temporary AI Object Storage credentials. This eliminates the need to store long-lived secrets in your applications, which reduces the risk of credential leakage and simplifies key rotation.

This guide is for administrators and platform engineers who need to grant non-CoreWeave workloads access to AI Object Storage without provisioning static keys. It walks through the complete workflow: configuring your OIDC provider, creating a WIF configuration in the Cloud Console, setting up organization access policies, and exchanging tokens for credentials. By the end, your workloads can authenticate using short-lived credentials derived from their existing OIDC identity.

## How OIDC WIF works

Your workload obtains an OIDC token from your identity provider and sends it to the AI Object Storage WIF endpoint. CoreWeave validates the token against your WIF configuration, derives a role identity from the token's `iss` (issuer) and `sub` (subject) claims, and returns a temporary Access Key / Secret Key pair for AI Object Storage.

The role identity follows the format `role/<ISSUER_URL>:<SUBJECT_USER_ID>`. For example, if your IdP issues tokens with `iss: https://idp.example.com` and `sub: svc-data-ingest`, the derived role is `role/https://idp.example.com:svc-data-ingest`.

Your [organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) authorize the WIF role as a principal in your organization. Add a [bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) when you need to control a specific resource. These policies must reference this role as a principal.

> [!WARNING]
>
> Workload Identity Federation only generates temporary credentials. It doesn't manage AI Object Storage organization access policies, bucket access policies, or Terraform state. You must configure policies separately and ensure they reference the correct WIF role principal.

## Prerequisites

Before you begin, ensure you have:

* A CoreWeave organization with AI Object Storage enabled.
* Administrator privileges for your organization (the **IAM Admin** role and **Object Storage Admin** role, or equivalent legacy access).
* The CoreWeave organization ID (find this on the [Settings page](https://console.coreweave.com/account/settings) in Cloud Console).
* AWS CLI version `2.33.2` or later. If you use Python SDKs, make sure your SDK is at least `boto3 >= 1.42.5`.
* An OIDC Identity Provider that supports [OpenID Connect Discovery](#verify-your-provider-supports-openid-connect-discovery) and can issue JWTs with the required claims. See [Required OIDC claims](#required-oidc-claims).

## Step 1: Configure your OIDC provider

Configure your IdP to issue JWTs for the workloads that need AI Object Storage access. CoreWeave uses these tokens to verify the identity of your workload before issuing temporary credentials, so the claims they carry must match the values in your WIF configuration. The tokens must include the standard claims listed in [Required OIDC claims](#required-oidc-claims).

### Verify your provider supports OpenID Connect Discovery

CoreWeave validates each incoming token against your provider's public signing keys (JWKS), and it locates those keys through OpenID Connect Discovery. Your IdP must meet two requirements:

* It implements [OpenID Connect Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html). The provider serves a discovery document at `[ISSUER-URL]/.well-known/openid-configuration`, and that document points to the provider's JWKS endpoint.
* It exposes the discovery document and JWKS endpoint publicly so CoreWeave can reach them. The IdP itself doesn't need to be on the public internet, but these two endpoints must be reachable. Most managed and private Kubernetes clusters expose them publicly even when the cluster's API server is private.

To confirm your provider supports discovery, request its discovery document. Replace `[ISSUER-URL]` with your provider's issuer URL, such as `https://idp.example.com`:

```bash title="Check the discovery endpoint" theme={"system"}
curl [ISSUER-URL]/.well-known/openid-configuration
```

A compliant provider returns a JSON document that includes a `jwks_uri` field. Confirm that the key set is reachable too:

```bash title="Check the JWKS endpoint" theme={"system"}
curl [ISSUER-URL]/.well-known/openid-configuration | jq -r .jwks_uri
```

Most identity providers and Kubernetes distributions support OpenID Connect Discovery by default. Some providers require extra configuration to expose these endpoints publicly.

> [!WARNING]
>
> If either endpoint is unreachable or your provider doesn't expose a discovery endpoint, CoreWeave can't validate its tokens. Contact CoreWeave support before continuing.

### Required OIDC claims

The following standard OIDC claims are required. The `aud` claim varies most across OIDC providers (see [Configure the `aud` claim for your provider](#configure-the-aud-claim-for-your-provider)).

| Claim | Description |
| - | - |
| `iss` | Issuer URL of your OIDC provider. Must match the issuer configured in your WIF configuration. |
| `aud` | Audience for the token. Must match the audience configured in your WIF configuration. |
| `sub` | Stable subject identifier for the workload (for example, a service account, client ID, or application ID). |
| `exp` | Expiration time (Unix timestamp). The token must not be expired. |
| `iat` | Issued-at time (Unix timestamp). |

CoreWeave supports the optional `nbf` (not before) claim. If present, the token is invalid before that time.

### Example JWT payload

```json theme={"system"}
{
  "iss": "https://idp.example.com",
  "aud": "https://coreweave.com/iam",
  "sub": "svc-data-ingest",
  "exp": 1640995200,
  "iat": 1640991600
}
```

This token produces the role identity `role/https://idp.example.com:svc-data-ingest`.

### Configure the `aud` claim for your provider

The `iss`, `sub`, `exp`, and `iat` claims are standard, and every OIDC provider issues them the same way. The `aud` (audience) claim is the exception: each provider sets it differently, and you choose its value. Whatever value your tokens carry in `aud` must match the **Client ID (Audience)** in your WIF configuration (see [Step 2](#step-2-create-a-wif-configuration-in-cloud-console)).

Choose a single audience value for your CoreWeave integration and use it consistently. The CoreWeave integrations default to `https://coreweave.com/iam`, and the following examples use that value.

Select your provider to see how to set the `aud` claim:

> [tab] GitHub Actions
>
> GitHub Actions sets the `aud` claim when a workflow requests its OIDC token. The [`coreweave/actions-public/auth/caios-login`](https://github.com/coreweave/actions-public/tree/main/auth/caios-login) action requests the token for you and defaults the audience to `https://coreweave.com/iam`. Set the `audience` input to use a different value. Replace `[ORG-ID]` with your CoreWeave organization ID:
>
> ```yaml highlight={5} theme={"system"}
> - uses: coreweave/actions-public/auth/caios-login@v1.1.0
>   with:
>     region: US-EAST-04A
>     org-id: [ORG-ID]
>     audience: https://coreweave.com/iam
> ```
>
> If you request the token yourself instead of using the action, pass the audience when you call the GitHub OIDC token endpoint. For example, in a step that uses the GitHub Actions toolkit:
>
> ```javascript highlight={1} theme={"system"}
> const token = await core.getIDToken("https://coreweave.com/iam")
> ```
>
> For the end-to-end workflow, see the [GitHub Actions tutorial](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/github.md).

> [tab] Kubernetes
>
> On Kubernetes, you set the `aud` claim through the `audience` field of a projected service account token volume. Mount the token into your pod, then point `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` at the mounted file:
>
> ```yaml highlight={7} theme={"system"}
> volumes:
>   - name: caios-token
>     projected:
>       sources:
>         - serviceAccountToken:
>             path: caios-token
>             audience: https://coreweave.com/iam
>             expirationSeconds: 600
> ```
>
> Kubernetes sets the token's `aud` claim to the `audience` value and its `sub` claim to `system:serviceaccount:[NAMESPACE]:[SERVICE-ACCOUNT]`. Use that subject when you reference the role in your access policies.
>
> For non-CKS clusters, see [Other Kubernetes clusters](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/kubernetes.md) to find the OIDC issuer URL. For CKS clusters, see the [CKS Object Storage authentication tutorial](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md).
>
> Each WIF configuration pairs one issuer with one audience. You can create more than one configuration for the same issuer, but only register audiences that AI Object Storage must accept.
>
> If a workload needs tokens for multiple providers, such as both `sts.amazonaws.com` for AWS and `https://coreweave.com/iam` for CoreWeave, project a separate token for each provider and set each token's audience to that provider's expected value. The following partial Pod specification places both tokens in one projected volume at different paths:
>
> ```yaml theme={"system"}
> volumes:
>   - name: provider-tokens
>     projected:
>       sources:
>         - serviceAccountToken:
>             path: coreweave-token
>             audience: https://coreweave.com/iam
>             expirationSeconds: 600
>         - serviceAccountToken:
>             path: aws-token
>             audience: sts.amazonaws.com
>             expirationSeconds: 600
> ```
>
> Configure each provider to read the token from its corresponding mounted path. Don't register another provider's audience in a CoreWeave WIF configuration, because that allows tokens intended for the other provider to authenticate to CoreWeave.

For other providers, set the audience wherever the provider lets you specify the token's target application or API, then use the same value as the **Client ID (Audience)** in your WIF configuration.

## Step 2: Create a WIF configuration in Cloud Console

Next, register your IdP with CoreWeave. The WIF configuration specifies how CoreWeave validates tokens from your IdP, including which issuer URL to trust and which audience value to expect.

1. Log in to the Cloud Console and navigate to the [Workload Federation](https://console.coreweave.com/organization/iam/workload-federation/oidc) page.
2. Click **Create OIDC configuration**. The configuration form opens:

![Workload Identity Federation OIDC configuration creation page](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/wif-oidc-page.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=cea05851036b12be0a1d1a66bda8ebcd)

Provide the following values:

* **Name**: A unique name for the configuration.
* **Issuer URL**: Your OIDC provider's identifier URL, such as `https://your-domain.okta.com` or `https://accounts.google.com`. CoreWeave uses this to verify that your trusted identity provider issued the tokens and to fetch the provider's JWKS for signature validation.
* **Client ID (Audience)**: The client identifier that tokens must target. CoreWeave validates that incoming tokens contain this value in their `aud` claim.
* **Description**: A brief description of the configuration.

Click **Create** to save the configuration. After creation, CoreWeave generates a **Config ID**. You can view this ID on the Workload Federation page. At this point, CoreWeave can validate tokens from your IdP, but the WIF role doesn't yet have permission to do anything.

## Step 3: Create organization access policies

Organization access policies control what your WIF role can do. Before your workload can exchange OIDC tokens for credentials, you must grant the `cwobject:CreateAccessKeyOIDC` action to the WIF role.

The principal for your OIDC role follows the format `role/<ISSUER_URL>:<SUBJECT_USER_ID>`, matching the role identity derived from your token.

The following policy grants the WIF role permission to create temporary credentials through the OIDC endpoint. The `cwobject:` actions are global and must use `"resources": ["*"]`. Optionally, you can also grant other `cwobject:` actions to the WIF role.

```json highlight={9-11} theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "allow-oidc-key-creation",
    "statements": [
      {
        "name": "allow-create-access-key-from-oidc",
        "effect": "Allow",
        "actions": [
          "cwobject:CreateAccessKeyOIDC"
        ],
        "resources": ["*"],
        "principals": [
          "role/https://idp.example.com:svc-data-ingest"
        ]
      }
    ]
  }
}
```

See [Organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) for the full schema and additional examples.

### Grant S3 permissions

After your workload can create credentials, you need policies that grant those credentials permission to access buckets. This policy grants read and write access to a specific bucket:

```json highlight={19-21} theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "data-ingest-read-write-my-bucket",
    "statements": [
      {
        "name": "allow-data-ingest-rw-my-bucket",
        "effect": "Allow",
        "actions": [
          "s3:Get*",
          "s3:List*",
          "s3:Put*",
          "s3:DeleteObject"
        ],
        "resources": [
          "[BUCKET-NAME]",
          "[BUCKET-NAME]/*"
        ],
        "principals": [
          "role/https://idp.example.com:svc-data-ingest"
        ]
      }
    ]
  }
}
```

## Step 4: (Optional) Add bucket access policies

Use a bucket access policy to control access to a specific resource, including access for principals from other organizations. Your organization access policies don't control access from another organization. Those principals must also have an organization access policy in their own organization that allows the action. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

Organization access policies and bucket access policies have different syntax requirements:

| Aspect | Organization access policies | Bucket access policies |
| - | - | - |
| Principals | Simple strings (for example, `role/https://idp.example.com:svc-data-ingest`) | Full ARNs (for example, `arn:aws:iam::[ORG-ID]:role/https://idp.example.com:svc-data-ingest`) |
| Resources | Short bucket names (`[BUCKET-NAME]`, `[BUCKET-NAME]/*`) | Full S3 ARNs (`arn:aws:s3:::[BUCKET-NAME]`, `arn:aws:s3:::[BUCKET-NAME]/*`) |

See [Bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) for the full schema and examples.

## Step 5: Configure your environment

After your IdP, WIF configuration, and organization access policies are in place, your workload can request temporary credentials from CoreWeave. In this final step, you configure your environment to use the temporary credentials, after which you can use any S3-compatible client to interact with your buckets.

1. Ensure you're using the correct version of the AWS CLI. The minimum required version is `awscli >= 2.33.2`. If you use Python SDKs, the minimum required version is `boto3 >= 1.42.5`.

   ```bash title="Check the AWS CLI version" theme={"system"}
   aws --version
   ```

2. Set the following environment variables, filling in the values for your CoreWeave organization ID, the path to your JWT token file, and the CoreWeave region you're using. This uses the [AWS container credentials feature](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html), so although the environment variables reference AWS CLI environment variables, you must fill in your CoreWeave-specific values:

   ```bash title="Set the environment variables" theme={"system"}
   export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
   export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]

   aws configure set s3.addressing_style virtual

   export AWS_REGION="[AVAILABILITY-ZONE]"
   export AWS_ENDPOINT_URL_S3="https://cwobject.com"
   ```

3. Test your configuration by listing your buckets:

   ```bash title="List your buckets" theme={"system"}
   aws s3 ls
   ```

On success, CoreWeave validates the token, derives the role identity, and returns temporary credentials. The `Expiration` field indicates when the credentials expire. The credentials inherit permissions from your organization access policies and any applicable bucket policies.

If you receive an error message like the following, check that you're using the correct version of the AWS CLI (`awscli >= 2.33.2`) or Python SDK (`boto3 >= 1.42.5`):

```text theme={"system"}
Unsupported host 'api.coreweave.com'.  Can only retrieve metadata from a loopback address or one of these hosts: 169.254.170.2, 169.254.170.23, fd00:ec2::23, localhost
```

### Credentials request and response

This uses the [AWS container credentials feature](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html), which pulls from your configured credentials file and runs a GET request to the CoreWeave OIDC WIF endpoint as follows:

```http title="Request" theme={"system"}
GET https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
Authorization: [JWT-TOKEN]
```

The response is a JSON object with the following fields:

```json title="Response" theme={"system"}
{
  "AccessKeyId":"CW...",
  "SecretAccessKey":"cw...",
  "Token": "",
  "Expiration":"2026-01-23T19:03:47Z",
  "attributes": {
    "cw-role":"<iss>:<sub>"
  }
}
```

## Troubleshooting

If credential exchange or S3 operations fail, the following sections cover the most common causes and what to check.

### Token exchange returns "permission denied"

If the `/temporary-credentials/oidc` call returns an error like `{"code": 7, "message": "permission denied", "details": []}`, check:

* **Missing cwobject permission**: Ensure your organization access policy grants `cwobject:CreateAccessKeyOIDC` to the WIF role. This permission is required for the token exchange to succeed.
* **Token validity**: Ensure the `iss` and `aud` claims match your WIF configuration. Verify the token isn't expired (`exp`) and isn't being used before `nbf` (if set).
* **WIF configuration**: Confirm the Issuer URL and Client ID in your WIF configuration exactly match the values in your tokens.

### Token exchange succeeds but S3 operations return AccessDenied

If you receive credentials but S3 operations fail, the issue is in your access policies. Check that at least one organization access policy:

* Allows the needed `s3:*` actions (for example, `s3:Get*`, `s3:List*`, `s3:Put*`).
* Uses the correct short-form resources (`"my-bucket"`, `"my-bucket/*"`).
* Lists the correct WIF role in `principals` using the format `role/<ISSUER_URL>:<SUBJECT_USER_ID>`.

If you're also using bucket access policies alongside organization policies, confirm they allow the required actions for the relevant principal ARNs. Be aware that explicit `Deny` statements can override other `Allow` statements.

## Related tutorials

For a step-by-step guide to federating CKS workloads with AI Object Storage specifically, see [CKS Workload Federation for AI Object Storage](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md).

CoreWeave sandboxes carry a built-in OIDC token and don't need the IdP configuration in [Step 1](#step-1-configure-your-oidc-provider). To grant a sandbox access to AI Object Storage, see [Grant sandboxes access to AI Object Storage](https://docs.coreweave.com/products/sandboxes/operations/object-storage-access.md).
