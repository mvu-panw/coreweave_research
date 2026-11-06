# Console permissions reference

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/console-permissions

# Console permissions reference

> Permissions required to perform AI Object Storage actions in the Cloud Console

This table lists the permissions required to perform CoreWeave AI Object Storage actions in the Cloud Console. The **Object Storage Admin** role grants the `cwobject:` control plane permissions, but it doesn't grant the `s3:` permissions required for bucket and object operations. Use this reference to grant the required permissions through an organization access policy.

To grant these permissions to users, you need the `Object Storage Admin` role. Then, you can [create an organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) to grant the permissions to the users. When these permissions are granted to a user, they will be able to perform the corresponding actions in the Cloud Console. For more information about organization access policies, see [About organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md).

| Feature in Console | AI Object Storage Permission Requirement |
| - | - |
| List (view) buckets | `cwobject:ListBucketInfo` |
| Create buckets | `s3:CreateBucket`  `cwobject:CreateAccessKey` |
| Delete buckets | `s3:DeleteBucket`  *(policy can include ability to delete individual buckets or all buckets)* |
| Open a bucket and browse its contents (read-only) | `cwobject:ListBucketInfo`  `cwobject:CreateAccessKey`  `s3:ListBucket` |
| Download objects | `s3:GetObject` |
| Upload objects | `s3:PutObject`  `s3:ListMultipartUploadParts`  `s3:AbortMultipartUpload` |
| Create folders | `s3:PutObject` |
| Rename objects or folders | `s3:GetObject`  `s3:PutObject`  `s3:DeleteObject` |
| Delete objects or folders | `s3:DeleteObject` |
| Create access keys | `cwobject:CreateAccessKeySAML`  `cwobject:CreateAccessKey` |
| Revoke access keys | `cwobject:RevokeAccessKeyByAccessKey` |
| List access keys | `cwobject:ListAccessKeyInfo` |
| Create or edit organization policies | `cwobject:EnsureAccessPolicy` |
| Delete organization policies | `cwobject:DeleteAccessPolicy` |
| View organization policies | `cwobject:ListAccessPolicy` |

> [!NOTE]
>
> * All `cwobject:` permissions are global operations and must specify `"resources": ["*"]` in the policy statement.
> * Cloud Console groups aren't allowed in organization access policies. Use UIDs (from the Cloud Console) or SAML users and groups instead.

### Required bucket policy permissions

To browse a bucket in the Cloud Console, the bucket's [bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) must grant the read-only permissions listed in the table. If a bucket policy doesn't grant these permissions to a principal, that principal can't browse the bucket in the Cloud Console even when their organization access policy does.

## Next steps

* Navigate to the [Organization Access Policies](https://console.coreweave.com/object-storage/access-policies) page in the Cloud Console to create an organization access policy.
* Learn more about creating [organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md).
