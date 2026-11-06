# About organization access policies

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about

# About organization access policies

> Learn about AI Object Storage organization access policies

Organization access policies authorize the principals in your organization to take CoreWeave AI Object Storage actions. They aren't a blanket control over every bucket. A policy in your organization applies to principals from your organization. It doesn't apply to principals from another organization, and it can't grant or block unauthenticated access.

This page is for administrators who need to grant Object Storage actions to principals in their organization. Written in JSON with the same syntax as bucket access policies, organization access policies apply to both the S3-compatible API and the AI Object Storage API. For an authenticated request to succeed, the requesting principal's organization access policy must allow it. When the target bucket has a bucket access policy, that policy must also allow it.

> [!NOTE]
>
> Unauthenticated requests skip organization access policies. Access from another organization requires a bucket access policy, and that principal's own organization access policy must also allow the action. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

Set your organization access policies after you create access tokens and keys, and before bucket operations.

## Key considerations

AI Object Storage organization access policies have specific aspects and considerations to understand:

| Policy aspect | Description |
| - | - |
| Admin access | Principals with the `Object Storage Admin` IAM role (assigned through CoreWeave [IAM access policies](https://docs.coreweave.com/security/iam/access-policies.md)) have unrestricted access to all `cwobject:` API actions (control plane), but that role does not grant S3-compatible API access. S3-compatible access must still be granted through Object Storage [organization and bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md). |
| Group usage | Organization access policies don't allow CoreWeave IAM *groups* (created in the Cloud Console). Use individual user UIDs (from Cloud Console) or SAML users and groups instead. |
| `s3:PutBucketPolicy` | The `s3:PutBucketPolicy` action is a **global** operation that only evaluates **organization** policies (it ignores bucket-level policies) and requires org policies to explicitly allow `s3:PutBucketPolicy` or `s3:*` with `"resources": ["*"]` or specific bucket names. This behavior prevents users from accidentally locking themselves out of a bucket with a misconfigured bucket access policy. |
| Global operations | All `cwobject:` API actions and the `s3:ListAllMyBuckets` operation are global operations that must specify `"resources": ["*"]` in organization access policies. |
| Policy evaluation | Both the requesting principal's organization access policy and, when one exists, the target bucket's bucket access policy must allow the request. The organization access policy is evaluated first. If it doesn't allow the request, the API rejects the request without consulting the bucket policy. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation). |
| Policy limit | Each organization can have up to 100 active organization access policies. The API rejects a request to create an additional policy at the limit. If your organization reaches the limit, consolidate or remove policies before you add more. |
| Policy management | Use organization access policies to grant actions to principals in your organization. Use [bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) to control a specific resource, including access from other organizations. |

Learn [how to set an organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) or [view examples of organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/examples.md).
