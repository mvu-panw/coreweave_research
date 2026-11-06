# Bring your own bucket for file system snapshots

Source: https://docs.coreweave.com/products/sandboxes/file-system-snapshots/bring-your-own-bucket

# Bring your own bucket for file system snapshots

> Store sandbox file system snapshots in an object storage bucket you own instead of the CoreWeave-managed default.

This guide shows you how to store [File System Snapshots (FSS)](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) in an object storage bucket you own, instead of the CoreWeave-managed default.

By default, CoreWeave provisions and manages an FSS bucket for your organization automatically. You don't have to do anything. Follow this guide only if you want your sandbox snapshots to land in a bucket you own and control.

You set up three things, in order:

1. **An OIDC provider (Workload Identity Federation config)** in your CoreWeave organization, so the per-sandbox tokens CoreWeave mints can be exchanged for temporary credentials in your organization.
2. **A bucket policy** on your bucket that grants that federated identity the scoped access FSS needs.
3. **The bucket registration** with CoreWeave, through a single API call.

> [!NOTE]
>
> Before you start, create the bucket you want to use. This guide does not cover bucket creation. See [Create buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md).

## How FSS uses your bucket

You never hand CoreWeave a static access key. Instead, every time a sandbox takes or restores a snapshot:

1. CoreWeave mints a short-lived OIDC JWT for that sandbox. The token is issued by `https://oidc.cwsandbox.com`, has the audience `cw-credential-vendor`, and carries claims that identify the organization, the user, the bucket, and the exact object the sandbox is allowed to touch.
2. Inside the sandbox, the AWS SDK exchanges that token through Workload Identity Federation for temporary S3 credentials scoped to your bucket, and auto-rotates them.
3. Your bucket policy authorizes that federated identity. It pins access down to a per-user prefix and to your organization only.

The Workload Identity Federation config (Step 1) is what makes your organization trust the CoreWeave token issuer. The bucket policy (Step 2) is what those exchanged credentials are evaluated against. Both are required.

## Values you need

Collect these before you begin. The values marked **fixed** are the same for every customer. The rest are specific to you.

| Value | Description | Where it comes from |
| - | - | - |
| OIDC issuer | The CoreWeave token issuer URL. | **Fixed:** `https://oidc.cwsandbox.com` |
| Audience (`aud`) | The audience CoreWeave stamps on FSS tokens. | **Fixed:** `cw-credential-vendor` |
| `[BUCKET-NAME]` | The bucket you created for FSS. | You chose it. See [Bucket name rules](#bucket-name-rules). |
| `[REGION]` | The CoreWeave Availability Zone your bucket lives in, used as the S3 region. | [All Availability Zones](https://docs.coreweave.com/platform/regions/all-availability-zones.md), for example `US-EAST-01A`. |
| `[ORG-ID]` | Your CoreWeave organization ID, the 6-character ID for the organization that owns the bucket and runs your sandboxes. | Cloud console. |
| `[CW-TOKEN]` | A CoreWeave API access token for an organization admin. Needs the `sandbox_admin` IAM action for Step 3. | [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md). |

> [!NOTE]
>
> Your organization ID is the same value everywhere it appears in the policy below: in the principal ARN, in each `oidc:[ORG-ID]:...` condition key, and as the value the `org_id` condition is matched against.

## Step 1: Register the OIDC provider

In the CoreWeave Cloud Console, go to the Workload Identity Federation OIDC page:

```text theme={"system"}
https://console.coreweave.com/organization/iam/workload-federation/oidc
```

Add a new OIDC provider with the following values:

| Field | Value |
| - | - |
| Issuer | `https://oidc.cwsandbox.com` |
| Audience | `cw-credential-vendor` |

This tells your organization to trust the tokens CoreWeave mints for your sandboxes. Without it, the credential exchange described in [How FSS uses your bucket](#how-fss-uses-your-bucket) fails before any bucket policy is evaluated.

For background on how OIDC Workload Identity Federation and the Cloud Console configuration work, see [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md).

## Step 2: Attach the bucket policy

Attach the following policy to your bucket. It is the same policy CoreWeave applies to managed FSS buckets, parameterized with your organization ID.

Replace the placeholders:

* `[BUCKET-NAME]` with your bucket name.
* `[ORG-ID]` with your 6-character organization ID, everywhere it appears.

```json theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "OIDCFederatedScopedAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::[ORG-ID]:role/https://oidc.cwsandbox.com:*"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts",
        "s3:CreateMultipartUpload",
        "s3:UploadPart",
        "s3:CompleteMultipartUpload"
      ],
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/${oidc:[ORG-ID]:user_hash}/*",
      "Condition": {
        "StringEquals": {
          "oidc:[ORG-ID]:org_id": "[ORG-ID]",
          "oidc:[ORG-ID]:bucket_name": "[BUCKET-NAME]"
        }
      }
    },
    {
      "Sid": "OIDCFederatedRestoreObjectScope",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::[ORG-ID]:role/https://oidc.cwsandbox.com:*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/${oidc:[ORG-ID]:restore_object_key}",
      "Condition": {
        "StringEquals": {
          "oidc:[ORG-ID]:org_id": "[ORG-ID]",
          "oidc:[ORG-ID]:bucket_name": "[BUCKET-NAME]"
        }
      }
    },
    {
      "Sid": "DenyCrossOrg",
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::[ORG-ID]:role/https://oidc.cwsandbox.com:*"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "oidc:[ORG-ID]:org_id": "[ORG-ID]"
        }
      }
    }
  ]
}
```

### What each statement does

* **`OIDCFederatedScopedAccess`** is the read and write grant for snapshot work. It is scoped to a per-user prefix, `${oidc:[ORG-ID]:user_hash}/*`. A given user's token only resolves to keys under their own hashed prefix, so users in your organization cannot write over each other's snapshots. The `bucket_name` condition prevents a token minted for a different bucket from being used here.
* **`OIDCFederatedRestoreObjectScope`** is a narrow `GetObject` grant for the exact object a restore is reading, `${oidc:[ORG-ID]:restore_object_key}`. This lets one sandbox restore a snapshot another user in your organization created, while the per-user write scoping still holds.
* **`DenyCrossOrg`** is defense in depth. It denies everything if the token's `org_id` claim is not your organization, so even a leaked or misrouted token cannot touch your bucket.

> [!NOTE]
>
> The condition keys use the `oidc:[ORG-ID]:[CLAIM]` form that CoreWeave AI Object Storage evaluates. CoreWeave fills in the `${oidc:[ORG-ID]:user_hash}` and `${oidc:[ORG-ID]:restore_object_key}` variables from the sandbox's token at request time. Do not substitute those. Leave them as written. Only the `[ORG-ID]` inside them is yours to fill in.

## Step 3: Register the bucket with CoreWeave

Tell CoreWeave to use your bucket by setting your organization's FSS bucket config. This is a single `PUT` that fully replaces the organization's config.

```bash theme={"system"}
curl -X PUT https://api.cwsandbox.com/v1beta2/file-system-snapshots/bucket-config \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [CW-TOKEN]" \
  -d '{
    "bucketName": "[BUCKET-NAME]",
    "region": "[REGION]"
  }'
```

* `api.cwsandbox.com` is the standard sandbox API host, the same one the data plane uses for other calls such as starting a sandbox.
* This call requires the `sandbox_admin` IAM action. On the [Access Policies](https://docs.coreweave.com/security/iam/access-policies/manage.md) page, assign the **Sandbox Admin** role, which grants this action. It's admin-gated because it sets the snapshot bucket for new sandboxes. See [Change or revert your bucket](#change-or-revert-your-bucket).
* Both `bucketName` and `region` are required together. Sending one without the other is rejected with `CWSANDBOX_INVALID_REQUEST`.

A successful response confirms that bring-your-own-bucket mode is in effect:

```json title="Example output" theme={"system"}
{
  "bucketName": "my-fss-bucket",
  "region": "US-EAST-01A",
  "mode": "FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_BRING_YOUR_OWN",
  "effectiveBucketName": "my-fss-bucket"
}
```

You can read the config back at any time. Any organization member can read it, with no admin role required:

```bash theme={"system"}
curl https://api.cwsandbox.com/v1beta2/file-system-snapshots/bucket-config \
  -H "Authorization: Bearer [CW-TOKEN]"
```

## Step 4: Verify

Run a snapshot and restore round trip against a real sandbox:

1. Start a sandbox with a fresh filesystem:

   ```bash theme={"system"}
   curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes \
     -H "Authorization: Bearer [CW-TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{
       "containerImage": "ubuntu:22.04",
       "command": "sleep",
       "args": ["3600"],
       "fileSystem": { "mountPath": "/work", "size": "10Gi" }
     }'
   ```

2. Write a file under `/work`, then stop the sandbox and snapshot on stop. Replace `[SANDBOX-ID]` with the ID of the sandbox you started. A successful response includes `success: true` and a `fileSystemSnapshotId`:

   ```bash theme={"system"}
   curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes/[SANDBOX-ID]/stop \
     -H "Authorization: Bearer [CW-TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{
       "sandboxId": "[SANDBOX-ID]",
       "fileSystemSnapshotOnStop": true,
       "waitForReady": true,
       "maxTimeoutSeconds": 600
     }'
   ```

   With `waitForReady: true`, a response with `success: true` confirms that the snapshot is `READY`. You can continue to the restore step. A snapshot ID alone doesn't confirm readiness. If the call returns `success: false`, reports an error, or times out, follow [Snapshot status and failures](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md#snapshot-status-and-failures) to check any available snapshot ID and recover before restoring.

3. After the snapshot is `READY`, restore it into a new sandbox. Replace `[SNAPSHOT-ID]` with the `fileSystemSnapshotId` from the successful capture or the snapshot whose status you checked:

   ```bash theme={"system"}
   curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes \
     -H "Authorization: Bearer [CW-TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{
       "containerImage": "ubuntu:22.04",
       "command": "sleep",
       "args": ["3600"],
       "fileSystem": {
         "mountPath": "/work",
         "size": "10Gi",
         "fileSystemSnapshot": { "fileSystemSnapshotId": "[SNAPSHOT-ID]" }
       }
     }'
   ```

If the file you wrote is present in the restored sandbox, your bucket is working. You can also confirm the snapshot landed in your bucket directly: each `FileSystemSnapshot` returned by `GetFileSystemSnapshot` and `ListFileSystemSnapshots` includes an `objectBucket` field showing which bucket the snapshot was stored in.

## Change or revert your bucket

The `PUT` in Step 3 is a full replace, so it is also how you change or undo your config:

* **Switch back to CoreWeave-managed**: `PUT` an empty body (`{}`). CoreWeave resumes managing a bucket for you automatically.
* **Move to a different bucket**: `PUT` the new `bucketName` and `region`.

> [!WARNING]
>
> Read this before you change a bucket. Changing or clearing your FSS bucket abandons access to snapshots stored in the previous bucket. CoreWeave does not copy data between buckets.
>
> * Restoring a snapshot whose stored bucket is not your current bucket returns `CWSANDBOX_FSS_BUCKET_MISMATCH`, which reports the snapshot's bucket and the current one. The stranded snapshots still appear in list and get calls. They are just not restorable while a different bucket is active.
> * This is reversible. Point the config back at the old bucket and those snapshots become restorable again.
> * New sandboxes use the updated config. Existing sandboxes that were bound to a bucket when they started keep snapshotting to that bucket. Legacy sandboxes without a stored bucket binding use the organization's current config when they take a snapshot.

## Troubleshooting

| Symptom | Likely cause | Fix |
| - | - | - |
| `AccessDenied` on snapshot or restore | The bucket policy principal, `org_id` value, or `bucket_name` condition doesn't match, or the Workload Identity Federation config (Step 1) is missing or has the wrong audience. | Verify the OIDC provider has issuer `https://oidc.cwsandbox.com` and audience `cw-credential-vendor`. Verify `[ORG-ID]` and `[BUCKET-NAME]` in the policy are correct. |
| `CWSANDBOX_FSS_BUCKET_MISMATCH` on restore | You changed the FSS bucket. The snapshot lives in a different bucket than the current one. | Revert the config to the bucket that holds the snapshot. |
| `CWSANDBOX_INVALID_REQUEST` on the `PUT` | Partial config (bucket without region or the reverse), or an invalid bucket name. | Send `bucketName` and `region` together. Check the [Bucket name rules](#bucket-name-rules). |
| `PermissionDenied` on the `PUT` | The token's user lacks the `sandbox_admin` IAM action. | On the [Access Policies](https://docs.coreweave.com/security/iam/access-policies/manage.md) page, assign the **Sandbox Admin** role, which grants `sandbox_admin`. |
| `PathStyleRequestNotAllowed` | Path-style S3 addressing was used. | CoreWeave AI Object Storage requires virtual-hosted-style addressing. |
| `CWSANDBOX_FSS_AUTH_FAILED` on snapshot | Credential exchange or bucket authorization failed. | Re-check Step 1 (OIDC provider) and Step 2 (bucket policy). If it persists, contact CoreWeave Support. |

If a sandbox is governed by a policy with allowlist-only egress, make sure it can reach the CoreWeave credential endpoint (`https://api.coreweave.com`). Otherwise the credential fetch times out and the first S3 operation fails.

## Reference

The following sections describe the bucket name rules, the S3 actions the policy grants, and the token claims the policy references.

### Bucket name rules

When you register a bucket in Step 3, CoreWeave validates the name against the standard object storage rules.

> [accordion] Bucket naming rules
>
> Bucket names must be globally unique and adhere to the following rules:
>
> * **Length:** 3 to 63 characters.
> * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> * **Prohibited patterns:** Cannot start with `xn--`.
> * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

The `region` is a CoreWeave Availability Zone, for example `US-EAST-01A`, and must match the zone your bucket lives in. For the full list of zones, see [All Availability Zones](https://docs.coreweave.com/platform/regions/all-availability-zones.md).

### S3 actions granted

The policy grants exactly the actions FSS needs and nothing more: `s3:GetObject`, `s3:PutObject`, `s3:CreateMultipartUpload`, `s3:UploadPart`, `s3:CompleteMultipartUpload`, `s3:AbortMultipartUpload`, and `s3:ListMultipartUploadParts`. Writes use multipart upload, and restore uses `GetObject`.

### Token claims used by the policy

CoreWeave stamps these claims onto each per-sandbox token. The bucket policy conditions reference them as `oidc:[ORG-ID]:[CLAIM]`.

| Claim | Used for |
| - | - |
| `org_id` | Matched against your organization in every `Allow` and in the `DenyCrossOrg` guard. |
| `user_hash` | The per-user write prefix (`[USER-HASH]/...`). |
| `bucket_name` | Ties the token to this bucket. |
| `restore_object_key` | The exact object a restore may read. |

## Related resources

* [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md): how snapshots, restore, and forking work.
* [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md): how OIDC federation and the Cloud Console configuration work.
* [Create buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md): create the bucket this guide assumes you already have.
* [All Availability Zones](https://docs.coreweave.com/platform/regions/all-availability-zones.md): the zones to use as your bucket's region.
* [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md): create the token used in Step 3.
* [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies/manage.md): grant the `sandbox_admin` action required for Step 3.
