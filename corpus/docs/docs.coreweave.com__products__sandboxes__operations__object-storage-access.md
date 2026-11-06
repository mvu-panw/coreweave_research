# Grant sandboxes access to AI Object Storage

Source: https://docs.coreweave.com/products/sandboxes/operations/object-storage-access

# Grant sandboxes access to AI Object Storage

> Let sandboxes exchange their built-in OpenID Connect (OIDC) token for temporary CoreWeave AI Object Storage credentials

Every CoreWeave sandbox can carry a built-in OIDC token that it exchanges through Workload Identity Federation (WIF) for temporary AI Object Storage credentials. CoreWeave mints the token, mounts it into the container, and sets environment variables. Amazon Web Services (AWS) software development kits (SDKs) read these variables. A sandbox can therefore read and write buckets without you injecting a long-lived access key.

This page is for administrators who set up the trust relationship once per organization, and for researchers who then request object storage access on individual sandboxes. By the end, a sandbox can run `aws s3` commands or Boto3 code against your buckets using credentials that expire on their own.

## How it works

The sandbox gateway issues each sandbox a JSON Web Token (JWT) from the fixed CoreWeave issuer `https://oidc.cwsandbox.com`. AI Object Storage validates that token against a workload federation configuration in your organization, derives a role identity from the token's `iss` and `sub` claims, and returns temporary credentials scoped by your access policies.

The following configuration must be consistent:

| Configuration | Where it lives | What it does |
| - | - | - |
| OIDC workload federation config | Cloud console, under **Organization** > **IAM** | Configures AI Object Storage to trust tokens from `https://oidc.cwsandbox.com`. Produces a **Config ID**. |
| Organization access policies | AI Object Storage | Grant the derived sandbox role permission to exchange tokens and to act on buckets. |
| Sandbox WIF configuration | Sandboxes organization settings | Points the sandbox gateway at the Config ID and caps which buckets and permission level sandboxes may request. |

The derived role identity follows the format `role/https://oidc.cwsandbox.com:user:USER_ID`, where `USER_ID` is the CoreWeave user ID of the caller whose API access token started the sandbox. Because the subject varies per user, access policies either list each user's role or match the whole issuer with a trailing wildcard. See [Grant permissions to the sandbox role](#step-2-grant-permissions-to-the-sandbox-role).

Inside the sandbox, no credential-fetching process of your own is needed. The AWS SDK's container credentials provider reads the mounted token, calls the CoreWeave credential endpoint, and refreshes the credentials before they expire. OIDC token renewal is a separate gateway operation, described in [Token lifetimes](#token-lifetimes).

The organization WIF configuration, sandbox request, and storage policies serve different purposes:

| Configuration | Purpose |
| - | - |
| Organization WIF configuration | Limits the buckets and permission level that the gateway accepts in sandbox requests. |
| Sandbox `spec.objectStorageAccess` | Requests buckets, a permission level, and an optional object-key prefix for one sandbox. The gateway records these in its signed token. |
| AI Object Storage policies | Authorize token exchange and S3 operations. Organization policies and any applicable bucket policy must allow the operation. |

The request fields and token claims don't replace storage policies. Configure those policies to enforce the S3 actions and resources you intend to allow.

## Before you begin

The administrator steps require the following:

* A CoreWeave organization with AI Object Storage enabled, and at least one bucket. To create one, see [Create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md).
* Administrator privileges for your organization: the **IAM Admin** and **Object Storage Admin** roles, or equivalent legacy access.
* The `sandbox_admin` action in Identity and Access Management (IAM), which lets you set the sandbox WIF configuration. Grant it on the [Access Policies](https://console.coreweave.com/organization/iam/access-policies) page in the cloud console.
* Your CoreWeave organization ID, shown on the [Settings](https://console.coreweave.com/account/settings) page in the cloud console.
* A CoreWeave API access token. Generate one on the [Tokens](https://console.coreweave.com/tokens) page and copy the **Token Secret** value. For more information, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

Export the token so the `curl` examples on this page can read it. Replace `API_ACCESS_TOKEN` with your CoreWeave API access token:

```bash theme={"system"}
export TOKEN="API_ACCESS_TOKEN"
```

For the researcher steps, you need a working sandbox setup. If you don't have one, follow [Get started](https://docs.coreweave.com/products/sandboxes/get-started.md) first.

## Step 1: Create an OIDC workload federation config

Register the sandbox issuer with your organization so that AI Object Storage accepts sandbox tokens.

1. In the cloud console, go to the [Workload Federation](https://console.coreweave.com/organization/iam/workload-federation/oidc) page.

2. Click **Create OIDC configuration**.

3. Provide the following values:

   * **Name**: a name that identifies this configuration, such as `coreweave-sandboxes`.
   * **Issuer URL**: `https://oidc.cwsandbox.com`.
   * **Client ID (Audience)**: `https://oidc.cwsandbox.com`.
   * **Description** (Optional): a description of this configuration.

4. Click **Create**.

> [!WARNING]
>
> The issuer host has no hyphen. Sandbox tokens carry the issuer claim `https://oidc.cwsandbox.com`, and token validation compares that value exactly, so a configuration created against `https://oidc.cw-sandbox.com` never matches.

After the configuration is created, the Workload Federation page shows its **Config ID**. Copy that value: Step 3 needs it.

At this point AI Object Storage can validate sandbox tokens, but the resulting role has no permissions yet.

## Step 2: Grant permissions to the sandbox role

Organization access policies determine what a sandbox can do with the credentials it receives. Two grants are required, and they must be separate statements because the token exchange action is global while the S3 actions are scoped to buckets.

The following policy grants the token exchange. The `cwobject:CreateAccessKeyOIDC` action operates on all resources, so its statement uses `"resources": ["*"]`. Replace `USER_ID` with the CoreWeave user ID whose API access token starts sandboxes:

```json highlight={9-14} theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "allow-sandbox-oidc-key-creation",
    "statements": [
      {
        "name": "allow-create-access-key-from-sandbox-oidc",
        "effect": "Allow",
        "actions": [
          "cwobject:CreateAccessKeyOIDC"
        ],
        "resources": ["*"],
        "principals": [
          "role/https://oidc.cwsandbox.com:user:USER_ID"
        ]
      }
    ]
  }
}
```

To cover every user in your organization without listing each subject, principals accept a trailing wildcard: `role/https://oidc.cwsandbox.com:*`. Because the issuer portion still has to match exactly, this grant applies only to sandbox tokens, not to other identity providers you federate.

Next, grant the credentials permission to act on buckets. Replace `BUCKET_NAME_VALUE` with the bucket your sandboxes use:

```json highlight={16-19} theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "sandbox-read-write-bucket",
    "statements": [
      {
        "name": "allow-sandbox-rw-bucket",
        "effect": "Allow",
        "actions": [
          "s3:Get*",
          "s3:List*",
          "s3:Put*",
          "s3:DeleteObject"
        ],
        "resources": [
          "BUCKET_NAME_VALUE",
          "BUCKET_NAME_VALUE/*"
        ],
        "principals": [
          "role/https://oidc.cwsandbox.com:*"
        ]
      }
    ]
  }
}
```

Without the second policy, the token exchange succeeds and every bucket operation is denied.

With both statements in place, the sandbox role can exchange its token for credentials and act on the buckets you listed.

The S3 policy in this section allows access throughout the named bucket. To restrict access to a sandbox's object prefix, retain the organization S3 permissions and add a prefix-aware bucket policy. Both the organization policy and the bucket policy must allow each S3 operation. A bucket policy doesn't replace the organization grant. See [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

In a bucket policy, the principal takes its full Amazon Resource Name (ARN) form, `arn:aws:iam::ORG_ID:role/https://oidc.cwsandbox.com:*`. Forwarded OIDC attributes use condition keys named `oidc:ORG_ID:CLAIM`. See [Token claims](#token-claims) for the distinction between JWT claims and policy attributes.

## Step 3: Configure WIF for your Sandboxes organization

Tell the sandbox gateway which workload federation configuration to mint tokens against, and set the ceiling on what any sandbox in your organization may request. Each organization has one configuration.

The gateway's `SettingsService` serves this organization configuration at api.cwsandbox.com. For the distinction from managed-runner administration, see [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md#how-sandboxes-launch). The following `v1` `PATCH` request creates or replaces the complete configuration because it omits `updateMask`.

Replace `WIF_CONFIG_ID` with the Config ID from [Step 1](#step-1-create-an-oidc-workload-federation-config) and `BUCKET_NAME_VALUE` with each bucket you want to allow:

```bash title="Set the sandbox WIF configuration" theme={"system"}
curl -X PATCH "https://api.cwsandbox.com/v1/settings/objectStorageWifConfig" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wifConfigId": "WIF_CONFIG_ID",
    "enabled": true,
    "allowedBuckets": ["BUCKET_NAME_VALUE"],
    "maxPermission": "OBJECT_STORAGE_PERMISSION_READ_WRITE"
  }'
```

The fields behave as follows:

| Field | Required | Description |
| - | - | - |
| `wifConfigId` | Yes | The Config ID from the cloud console workload federation configuration. |
| `maxPermission` | Yes | The highest access level any sandbox may request: `OBJECT_STORAGE_PERMISSION_READ` or `OBJECT_STORAGE_PERMISSION_READ_WRITE`. |
| `enabled` | No | Set to `true` to enable access. Omission or `false` turns off access in a full replacement. |
| `allowedBuckets` | No | Bucket names sandboxes may request. An empty list permits requests for any bucket. Use an explicit list to limit requests to the required buckets. |

The organization comes from the authenticated caller, so the request body has no organization field, and callers can only manage their own organization's configuration.

Confirm the configuration was stored:

```bash title="Get the sandbox WIF configuration" theme={"system"}
curl "https://api.cwsandbox.com/v1/settings/objectStorageWifConfig" \
  -H "Authorization: Bearer $TOKEN"
```

To reject new sandbox requests for object storage access, delete the configuration:

```bash title="Delete the sandbox WIF configuration" theme={"system"}
curl -X DELETE "https://api.cwsandbox.com/v1/settings/objectStorageWifConfig" \
  -H "Authorization: Bearer $TOKEN"
```

Deleting or disabling the configuration also prevents subsequent OIDC token renewal for existing grants. It doesn't revoke tokens or temporary credentials already issued. See [WIF configuration changes](#wif-configuration-changes).

For request fields, update masks, and responses, see [Update object storage WIF configuration](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/settingsservice/update-object-storage-wif-config.md).

## Step 4: Request object storage access when you start a sandbox

Steps 1 through 3 are one-time administrator setup for the organization. The remaining steps are what a researcher does for each sandbox that needs object storage.

Object storage access is opt-in per sandbox. Set `spec.objectStorageAccess` in the create request, naming the buckets the sandbox needs and the permission level it requires. This example uses serverless placement. For a runner in your own CoreWeave Kubernetes Service (CKS) cluster, use `SANDBOX_MODE_CKS` instead. Replace `CONTAINER_IMAGE` with the image to run in the sandbox:

```bash title="Start a sandbox with object storage access" highlight={14-17} theme={"system"}
curl -X POST "https://api.cwsandbox.com/v1/sandboxes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "spec": {
      "mode": "SANDBOX_MODE_SERVERLESS",
      "containers": [{
        "name": "main",
        "image": "CONTAINER_IMAGE",
        "command": "sleep",
        "args": ["3600"],
        "resources": { "cpu": "1", "memory": "2Gi" }
      }],
      "objectStorageAccess": {
        "buckets": ["BUCKET_NAME_VALUE"],
        "permission": "OBJECT_STORAGE_PERMISSION_READ_WRITE"
      }
    }
  }'
```

Configure the grant with the following fields under `spec.objectStorageAccess`:

| Field | Required | Description |
| - | - | - |
| `buckets` | Yes | One or more bucket names. When `allowedBuckets` is nonempty, every requested bucket must appear in that list. An empty `allowedBuckets` list permits any bucket request. |
| `permission` | Yes | `OBJECT_STORAGE_PERMISSION_READ` or `OBJECT_STORAGE_PERMISSION_READ_WRITE`. The request can't exceed the organization's `maxPermission`. |
| `objectPrefix` | No | An object-key prefix applied to every requested bucket and emitted as the `object_prefix` token claim. A bucket policy must use that claim to enforce prefix access. |

A request that exceeds the organization limits is rejected, as is a request made while the organization has no active WIF configuration. These checks govern token issuance. The storage policies determine which S3 operations the resulting credentials can perform.

A sandbox that only reads training data should ask for `OBJECT_STORAGE_PERMISSION_READ` even in an organization whose ceiling is read-write.

### Optional: Limit access to an object prefix

Prefix-scoped access requires both a prefix in the sandbox request and a bucket policy that enforces it.

Set `spec.objectStorageAccess.objectPrefix` to request a prefix in the sandbox's OIDC token. The following excerpt shows the `spec.objectStorageAccess` portion of a create request. Replace `BUCKET_NAME_VALUE` with the bucket name and `OBJECT_PREFIX_VALUE/` with the prefix, including its trailing slash:

```json theme={"system"}
{
  "spec": {
    "objectStorageAccess": {
      "buckets": ["BUCKET_NAME_VALUE"],
      "permission": "OBJECT_STORAGE_PERMISSION_READ",
      "objectPrefix": "OBJECT_PREFIX_VALUE/"
    }
  }
}
```

A nonempty prefix must meet the gateway's validation rules:

* Start with an ASCII letter or number.
* Contain only ASCII letters, numbers, periods, underscores, forward slashes, and hyphens.
* End with `/`.
* Contain no `..` or `//` sequences.
* Be no more than 512 bytes.

For credential exchange, keep the prefix to 128 bytes or fewer. AI Object Storage applies this stricter limit to the forwarded `object_prefix` attribute. A longer prefix can pass sandbox creation but fail credential exchange. An empty or omitted prefix produces no `object_prefix` claim.

The caller supplies the prefix, but format validation doesn't determine which prefix that caller is entitled to use. If your application assigns prefixes to users or tenants, derive the prefix from their authenticated identity before you create the sandbox. Don't let an untrusted user choose another tenant's prefix.

To enforce the prefix, keep the organization S3 permissions from Step 2. Add the following statements to the bucket's access policy. Replace `BUCKET_NAME_VALUE` and `ORG_ID` with the bucket name and the organization that owns the sandbox identity. Preserve existing statements needed by administrators and other workloads. For instructions, see [Set a bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#set-a-bucket-access-policy).

```json title="Prefix-scoped read access" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SandboxPrefixRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ORG_ID:role/https://oidc.cwsandbox.com:*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::BUCKET_NAME_VALUE/${oidc:ORG_ID:object_prefix}*",
      "Condition": {
        "StringEquals": {
          "oidc:ORG_ID:org_id": "ORG_ID"
        }
      }
    },
    {
      "Sid": "SandboxPrefixList",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ORG_ID:role/https://oidc.cwsandbox.com:*"
      },
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::BUCKET_NAME_VALUE",
      "Condition": {
        "StringEquals": {
          "oidc:ORG_ID:org_id": "ORG_ID"
        },
        "StringLike": {
          "s3:prefix": "${oidc:ORG_ID:object_prefix}*"
        }
      }
    }
  ]
}
```

The first statement allows reads only under the token's prefix. The second allows bucket listings only when the request's `prefix` starts with that prefix. Both statements require the expected `org_id`. Neither grants access when `object_prefix` is absent.

These statements don't grant write operations. For read-write workloads, request `OBJECT_STORAGE_PERMISSION_READ_WRITE` and grant the required object actions in both policy layers.

Don't add a broader `Allow` for the same sandbox role in the bucket policy: it can grant access outside the prefix. An explicit `Deny` overrides an `Allow`. The prefix claim alone doesn't narrow an unrelated policy statement.

When you use these statements, list within the prefix instead of listing the bucket root. For example, after configuring the client as shown in Step 5, use `aws s3 ls s3://BUCKET_NAME_VALUE/OBJECT_PREFIX_VALUE/`. With Boto3, supply `Prefix='OBJECT_PREFIX_VALUE/'` in the `list_objects_v2()` call. A root listing has no matching prefix and isn't allowed by these statements.

## Step 5: Use the credentials inside the sandbox

When a sandbox starts with `spec.objectStorageAccess`, CoreWeave mounts its OIDC token and sets the environment variables that AWS SDKs use for [container credentials](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html):

| Variable | Value |
| - | - |
| `AWS_CONTAINER_CREDENTIALS_FULL_URI` | `https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/ORG_ID` |
| `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` | `/var/run/secrets/sandbox/storage-token/osa-token` |
| `AWS_ENDPOINT_URL_S3` | The AI Object Storage endpoint, such as `https://cwobject.com` |

The token itself is a read-only file at `/var/run/secrets/sandbox/storage-token/osa-token`. You don't need to read it, and you shouldn't copy it out of the sandbox or pass it to another workload.

Your client library performs the exchange. Set the region for your buckets, then use any S3-compatible client. Replace `AVAILABILITY_ZONE` with the Availability Zone your buckets are in, such as `US-EAST-04A`:

```bash title="List objects from inside a sandbox" theme={"system"}
export AWS_REGION="AVAILABILITY_ZONE"

aws configure set s3.addressing_style virtual

aws s3 ls s3://BUCKET_NAME_VALUE/
```

AI Object Storage requires virtual-hosted addressing. Path-style requests fail with `PathStyleRequestNotAllowed`.

Boto3 reads the same environment variables, so no explicit credentials are needed. The following example lists objects in a bucket, reading the endpoint and region from the sandbox environment:

```python title="list_objects.py" theme={"system"}
import os

import boto3
from botocore.client import Config

boto_config = Config(
    region_name=os.environ['AWS_REGION'],
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url=os.environ['AWS_ENDPOINT_URL_S3'],
    config=boto_config
)

response = s3.list_objects_v2(Bucket=os.environ['BUCKET_NAME'])

for item in response.get('Contents', []):
    print(item['Key'], item['Size'])
```

Run it inside the sandbox, with `BUCKET_NAME` set to the bucket you granted:

```bash theme={"system"}
export BUCKET_NAME="BUCKET_NAME_VALUE"

python list_objects.py
```

Successful output lists each object key and its size in bytes:

```text title="Example output" theme={"system"}
datasets/train/shard-00000.tar 268435456
datasets/train/shard-00001.tar 268435456
datasets/val/shard-00000.tar 67108864
```

Credential exchange requires SDK support for container credentials against a non-loopback host. Use `awscli` 2.33.2 or later, or `boto3` 1.42.5 or later. Older versions fail with `Unsupported host 'api.coreweave.com'`. Build these versions into your sandbox container image.

## Token lifetimes

The sandbox lifetime, its object storage OIDC token, and the temporary credentials obtained from that token are separate:

* **Sandbox lifetime**: `maxLifetimeSeconds` sets the requested maximum runtime. Increasing it doesn't extend the object storage OIDC token's lifetime.
* **Sandbox object storage OIDC token**: the sandbox gateway mints it when the sandbox starts. CoreWeave configures its lifetime independently of the sandbox lifetime.
* **Temporary AI Object Storage credentials**: minted on demand from the OIDC token. The exchange response carries an `Expiration` timestamp, and the AWS SDK refreshes the credentials before that time without any action from your code.

The SDK uses the token in the mounted file to request temporary credentials. It doesn't renew the OIDC token.

The managed service enables automatic OIDC token renewal. The gateway reissues tokens for running sandboxes, and the runner updates the mounted token file. The SDK reads the updated file on its next credential request. Renewal depends on the deployment's refresh configuration and a runner version that supports token updates.

If renewal fails and the token in the file expires, new credential exchanges fail even if the sandbox is still running. Existing temporary credentials have their own expiration. Increasing `maxLifetimeSeconds` doesn't repair a failed renewal.

### WIF configuration changes

The gateway stores the original sandbox grant and checks it against the current organization WIF configuration when it renews the OIDC token:

| Configuration change | Effect at a subsequent token renewal |
| - | - |
| Replace `wifConfigId` | The new token carries the current Config ID. |
| Change `allowedBuckets` to a nonempty list | The new token retains only originally requested buckets that remain allowed. If none remain, the gateway issues no replacement OIDC token for that grant. An empty list removes the organization bucket restriction. |
| Lower `maxPermission` to read | The new token's `permission` claim is `READ`. |
| Disable or delete the WIF configuration | The gateway issues no replacement OIDC token for existing grants. New sandbox requests for object storage access are rejected. |

These changes affect token issuance and claims. They don't rewrite storage policies or immediately revoke an existing token or temporary credential.

In particular, lowering `maxPermission` doesn't replace a storage policy change that removes write actions. To change which S3 operations are authorized, update the applicable organization and bucket policies. Stopping a sandbox stops its workload, but doesn't itself revoke a token or credential copied elsewhere.

## Token claims

Sandbox object storage tokens carry the following claims. IAM forwards an allowlisted subset of OIDC claims to AI Object Storage as policy attributes. The prefix policy in this guide uses the supported `oidc:ORG_ID:org_id` and `oidc:ORG_ID:object_prefix` attributes. Don't assume every claim in the JWT is available as a bucket-policy condition key.

| Claim | Description |
| - | - |
| `iss` | Always `https://oidc.cwsandbox.com`. |
| `sub` | `user:USER_ID`, the CoreWeave user that started the sandbox. Combined with `iss` to derive the role identity. |
| `aud` | `https://oidc.cwsandbox.com`, which must match the audience in the workload federation configuration. |
| `org_id` | The CoreWeave organization that owns the sandbox. |
| `user_id` | The CoreWeave user ID of the caller that started the sandbox. |
| `sandbox_id` | The ID of the sandbox that received the token. |
| `wif_config_id` | The workload federation Config ID used when this token was minted. |
| `buckets` | The requested buckets, restricted to the current nonempty organization allowlist when the token is renewed. |
| `permission` | `READ` or `READ_WRITE`, limited by the organization's maximum when the token is minted or renewed. |
| `object_prefix` | The requested object-key prefix. Omitted when no prefix is set. |
| `exp` | Expiration time as a Unix timestamp. |

## Troubleshooting

The following sections describe the failures you are most likely to see when setting up or using sandbox object storage access, and what to check for each one.

### The start request is rejected

If a create request with `spec.objectStorageAccess` fails, check the following:

* The organization has a WIF configuration with `enabled` set to `true`. Retrieve it with the Get request in [Step 3](#step-3-configure-wif-for-your-sandboxes-organization).
* Every bucket in the request appears in `allowedBuckets`, or `allowedBuckets` is empty.
* The requested `permission` doesn't exceed `maxPermission`.
* The request includes at least one bucket and a supported permission value.
* Any `objectPrefix` follows the [prefix validation rules](#optional-limit-access-to-an-object-prefix). Invalid prefixes produce an `InvalidArgument` error for `spec.object_storage_access.object_prefix`.

### Credential exchange returns permission denied

If the request to the `/temporary-credentials/oidc` endpoint returns a permission error, credential exchange was refused. Check that:

* An organization access policy grants `cwobject:CreateAccessKeyOIDC` on `"resources": ["*"]` to the sandbox role, in its own statement.
* The policy principal matches the derived role exactly, including the `user:` prefix on the subject. The principal is `role/https://oidc.cwsandbox.com:user:USER_ID`, not `role/https://oidc.cwsandbox.com:USER_ID`.
* The workload federation configuration in the cloud console is active and its issuer URL is `https://oidc.cwsandbox.com`, with no hyphen.
* The sandbox OIDC token file exists and its token hasn't expired. If a running sandbox loses access despite an enabled WIF configuration and correct storage policies, restart it to obtain a new token. If the problem recurs, contact CoreWeave Support with the sandbox ID.

### Credential exchange rejects a long prefix

A prefix longer than 128 bytes can pass the gateway's 512-byte validation limit but fail AI Object Storage's attribute-length validation. Use a shorter `objectPrefix` and create a new sandbox.

### Credential exchange succeeds but S3 operations return AccessDenied

If the SDK obtains temporary credentials but an S3 request returns `AccessDenied`, check the bucket permissions for those credentials. Confirm that an organization access policy grants the needed `s3:` actions on the short-form bucket resources (`BUCKET_NAME_VALUE` and `BUCKET_NAME_VALUE/*`) to the sandbox role. If a bucket policy exists, it must also allow the operation. Check both policy layers for `Deny` statements, which override any `Allow`.

For the prefix policy in this guide, confirm that the object key or listing prefix is within `objectPrefix`. Listing the bucket root isn't allowed by that policy.

### The credential request times out

Sandboxes governed by a policy with allowlist-only egress must be able to reach `https://api.coreweave.com`. Without that route, the credential fetch times out and the first S3 operation fails. Declare an egress rule for that destination in the sandbox's network configuration, and permit it in the policy's `allowedEgress` envelope.

If the sandbox declares no egress and doesn't set `denyEgress`, a matching classless inter-domain routing (CIDR) rule in the policy's `defaultEgress` can provide the grant. Hostname rules (`httpsHostname`) belong in sandbox requests and `allowedEgress`, and aren't supported in `defaultEgress`. An `allowedEgress` entry alone doesn't grant connectivity. See [Constrain network access](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-network-access).

### The workload creates many access keys

Each exchange creates a short-lived access key. Let the SDK's credential provider cache and refresh the credentials for the lifetime of your process instead of constructing a new client per work item. Minting keys per request generates large volumes of keys for no benefit.

## Related pages

For related guidance, see the following pages:

* [Workload Identity Federation for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md): how WIF works across CoreWeave.
* [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md): the general OIDC federation guide, for identity providers other than sandboxes.
* [Organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md): the policy schema used in Step 2.
* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): where the gateway and runner sit in the sandbox request path.
