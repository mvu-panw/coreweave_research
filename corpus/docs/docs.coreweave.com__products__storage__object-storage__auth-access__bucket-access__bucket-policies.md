# About bucket access policies

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies

# About bucket access policies

> Learn to control user actions on specific resources

This page explains how bucket access policies work in CoreWeave AI Object Storage, how to apply one to a bucket, and how to structure the JSON document so you can write your own. Use this page when you need precise, S3-specific access control for an individual bucket, such as sharing a bucket with users from another organization or restricting access to a single prefix.

Bucket access policies are JSON objects that define allowed or denied actions on a single bucket and its contents. Only the bucket owner can attach or update this policy.

Object Storage authorizes each request against two policies, both of which must allow the request:

* The requesting principal's organization access policy. You configure these in the [Cloud Console](https://console.coreweave.com/object-storage/access-policies) or through the [AI Object Storage API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/apply-or-update-access-policy.md) (for example, with `curl`).
* The target bucket's bucket access policy, when one exists. Bucket access policies apply only to one bucket and its objects. Use them to control the resource, including access from other organizations. Those principals must also have an organization access policy in their own organization that allows the action on the bucket's resource ARN.

For the full evaluation rules, including unauthenticated requests, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

## Set a bucket access policy

To set a bucket access policy, use the [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) with standard S3 tools like `aws s3api` or `s3cmd`, or use the [CoreWeave Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs/resources/object_storage_bucket_policy). The policy is a JSON object that defines the access rules for the bucket and its objects.

For example, the following command applies a JSON policy file to a bucket. Replace `[BUCKET-NAME]` with the name of your bucket and `[POLICY-FILE]` with the path to the JSON file that contains the policy.

```bash theme={"system"}
aws s3api put-bucket-policy --bucket [BUCKET-NAME] --policy file://[POLICY-FILE]
```

The policy file must be a valid JSON object that adheres to the structure and rules defined in this guide. After the command succeeds, the bucket enforces the new policy in addition to your organization access policies. The sections that follow describe the constraints to keep in mind and the JSON fields you use to author the policy.

## Key considerations

Keep the following aspects of bucket access policies in mind:

| Policy aspect | Details |
| - | - |
| **Policy scope** | Bucket access policies can only grant S3-compatible API permissions. Actions under the `cwobject:` API (for example, managing access keys or audit logging) must be allowed through an organization access policy that uses `"Resource": ["*"]`. |
| **Lifecycle configuration** | Bucket access policies uniquely govern [bucket lifecycle configuration](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md), including: - Expiration actions (delete by date, age, or expired-marker) - Noncurrent version expiration - Abort incomplete multipart uploads |
| **Access policies versus lifecycle policies** | Bucket access policies are not the same as [lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md). Lifecycle policies manage object lifecycles, while bucket access policies control access to the bucket and its objects. - Set access policies with `s3:PutBucketPolicy`. - Set lifecycle policies with `s3:PutBucketLifecycleConfiguration`. |
| **Global operations** | Certain actions are global and only evaluate organization policies: - `s3:ListAllMyBuckets` must specify `"Resources": ["*"]`. - `s3:PutBucketPolicy` is global and only checks organization access policies to avoid lock-out. |
| **Principal specification** | CoreWeave IAM groups can't be named as a `Principal` in bucket access policies. Specify principals by UID (from Cloud Console) or through SAML users and groups. To grant access based on group membership, use condition keys instead. See [Attribute-based access control](#attribute-based-access-control). |
| **Explicit S3-compatible API access** | The `Object Storage Admin` IAM role (or membership in the legacy `admin` group) does not grant S3-compatible API access. You must explicitly allow it through organization or bucket access policies. |

Make sure that your policy fits within the maximum policy size of 20 KB.

### Avoid lockout

Bucket policy management can create lockout scenarios. To prevent accidental lockout, grant `s3:PutBucketPolicy` permissions carefully. Since `s3:PutBucketPolicy` is evaluated only against organization policies (not bucket policies), any user with org-level permissions can overwrite a bucket policy.

Restrict org-level `s3:PutBucketPolicy` access to administrators, and use bucket policies to grant read and delete permissions (`s3:GetBucketPolicy`, `s3:DeleteBucketPolicy`) to bucket owners and operators.

### Avoid public buckets

Don't make a bucket that holds model weights or customer data public. A bucket access policy that allows unauthenticated requests, such as an `Allow` statement with `"Principal": "*"` and no `Condition`, lets anyone on the internet access the bucket. Model licenses and terms of use often restrict who can download the weights. Unauthenticated requests carry no principal, so audit logs show only the request's source IP, not which consumer made it, and you can't cut off one consumer by revoking their access keys.

To share data instead, use [presigned URLs](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#presigned-urls) for temporary access to individual objects, or name each consumer as a principal in a bucket access policy that allows only the actions they need. Each consumer then authenticates with their own [access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md). A consumer in another organization also needs an organization access policy in their own organization that allows those actions.

## Structure of bucket access policies

Bucket access policies use JSON objects with two top-level fields: `Version`, `Statement`. The `Statement` field is an array of objects, each defining the access rules for a specific bucket or object. Each statement can include the following:

| Field | Description |
| - | - |
| `Sid` | Optional identifier for the policy statement. |
| `Effect` | Indicates whether the policy allows or denies access. |
| `Principal` | The user, role, or group to which the policy applies. |
| `Action` | The specific actions that the policy allows or denies. |
| `Resource` | The resources to which the policy applies, specified in ARN format. |
| `Condition` | Optional element that specifies additional constraints for when the policy applies. |

### Version

`Version` is required. It defines the version of the policy language. Use `2012-10-17` for all policies. Some old policies use `2008-10-17`. Any other value is invalid.

```json highlight={2} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": { ... }
    }
  ]
}
```

### Statement

`Statement` is required. It's the main policy element that defines the access rules for buckets and objects. It can contain a single policy or an array. Enclose each policy in curly braces, and enclose arrays of policies in square brackets.

```json highlight={3-14} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": { ... }
    },
    { ... },
    { ... }
  ]
}
```

### Sid

`Sid` (Statement ID) is optional. It's a short, human-readable identifier for the policy statement, which is useful for tracking and managing policies. Each `Statement` in an array of statements can have an assigned `Sid`. Each `Sid` must be unique within the JSON policy, and may only consist of ASCII uppercase letters, lowercase letters, or numbers.

```json highlight={5} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": { ... }
    }
  ]
}
```

### Effect

`Effect` is required. It specifies whether the statement allows or denies the action. The valid options are `Allow` or `Deny`, and these are case-sensitive. By default, CoreWeave denies access to resources. To allow access to a resource, set the `Effect` element to `Allow`. To override an allow that is otherwise in force, set the `Effect` element to `Deny`.

```json highlight={6} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": { ... }
    }
  ]
}
```

### Principal / NotPrincipal

This field defines who gets access to the resources specified in the policy. Either `Principal` or `NotPrincipal` is required. You can't use them together.

* Use `Principal` to specify the user, role, or group allowed for this policy.
* Use `NotPrincipal` to deny access to all except the principal specified. `NotPrincipal` is only supported with `"Effect": "Deny"`. You can't use it with `"Effect": "Allow"`.

Troubleshooting the side effects of `NotPrincipal` can be difficult. We recommend using options such as `Condition` instead.

The key in the `Principal` object specifies the identity type:

* Use `CW` for users from the CoreWeave Cloud Console.
* Use `AWS` for identities from a federated SAML provider.

The value in the Principal object must be an ARN (Amazon Resource Name). In the path, indicate the source of the `Principal`:

* For Console users: `arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]`
* For SAML users: `arn:aws:iam::[ORG-ID]:saml/[USER-ID]`

You can find your organization ID and user UID on the [Settings page](https://console.coreweave.com/account/settings) of your Cloud Console account.

For OIDC users who set up Workload Identity Federation:

* Use `arn:aws:iam::[ORG-ID]:role/[JWT-ISSUER-URL]:[JWT-SUBJECT-USER-ID]`, where `[JWT-ISSUER-URL]` is the issuer of the JWT token and `[JWT-SUBJECT-USER-ID]` is the subject of the JWT token.

Do not use `user/` in the ARN path. It isn't a valid prefix for CoreWeave or SAML identities.

To specify multiple principals in a single policy statement, include multiple entries in the `Principal` object:

```json highlight={7-12} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": { ... }
    }
  ]
}
```

### Action / NotAction

Either `Action` or `NotAction` is required. You can't use them together.

* Use `Action` to describe the specific actions that are allowed or denied.
* Use `NotAction` to match everything except the specified actions.

Wildcards such as `s3:*` are allowed to match multiple actions. Be careful when you combine `NotAction` and `"Effect": "Allow"` in the same policy because it could grant users more permissions than intended. See the list of [API calls and required actions](#required-policies-and-actions) to determine what actions must be allowed for each API call.

```json highlight={8-11} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [ ... ],
      "Condition": { ... }
    }
  ]
}
```

### Resource / NotResource

Either `Resource` or `NotResource` is required. You can't use them together.

* Use `Resource` to apply the policy to the listed resources.
* Use `NotResource` to apply the policy to all resources except the ones listed.

Use ARN format to specify resources. Wildcards `*` and `?` are allowed within each colon-separated ARN segment. Wildcards don't extend past colon boundaries.

Don't use `NotResource` in tandem with `"Effect": "Allow"` and `"Action": "*"` because this allows all actions on all resources except those listed.

In the following example, replace `[BUCKET-NAME]` with your bucket name and `[OBJECT-KEY]` with the object key the policy applies to:

```json highlight={9-12} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]/[OBJECT-KEY]",
        "arn:aws:s3:::???-bucket/*/test"
      ],
      "Condition": { ... }
    }
  ]
}
```

### Condition

`Condition` is optional. A `Condition` consists of an operator, and a key with a value. CoreWeave evaluates the condition to grant or deny access based on the request context.

#### Condition operators

The supported condition operators are:

| Field | Description |
| - | - |
| `IpAddress` | The specified IP address or range, such as `203.0.113.0/24` |
| `IpAddressIfExists` | Same as `IpAddress`, but also matches when the source IP is absent |
| `NotIpAddress` | All IP addresses except the specified address |
| `NotIpAddressIfExists` | Same as `NotIpAddress`; an absent source IP still matches |
| `StringEquals` | Exact, case-sensitive match |
| `StringNotEquals` | Match all except specified string, case-sensitive |
| `StringLike` | Case-sensitive match allowing wildcards |
| `StringNotLike` | Negated case-sensitive match allowing wildcards |
| `StringEqualsIgnoreCase` | Exact match, ignores case |
| `StringNotEqualsIgnoreCase` | Negated exact match, ignores case |
| `Bool` | Match a boolean key against `true` or `false` |
| `BoolIfExists` | Same as `Bool`, but also matches when the key is absent |
| `Null` | Check for absent condition key |

#### Condition keys

The supported condition keys are:

| Field | Description |
| - | - |
| `cw:PrincipalArn` | The principal, formatted as `arn:partition:service:region:[ACCOUNT-ID]:[RESOURCE-TYPE/][RESOURCE-ID]`. |
| `cw:ResourceArn` | The resource ARN of the request. |
| `cw:ResourceOrgID` | The organization ID from the owner of a resource. |
| `cw:PrincipalOrgID` | The organization ID from the principal. |
| `cw:SourceIP` | The source IP address of the request. |
| `cw:Bucket` | The bucket name of the request. |
| `s3:prefix` | The prefix of the request, used to list objects. |
| `s3:ObjectCreationOperation` | `true` on `PutObject`, `CompleteMultipartUpload`, `CopyObject`, and `RenameObject`; `false` on `CreateMultipartUpload`, `UploadPart`, and `UploadPartCopy`. Absent on internal writes that have no request context. See [Require conditional writes](#require-conditional-writes). |
| `s3:if-none-match` | The `If-None-Match` precondition on the destination object. Set only when an object-creation request carries the header. On a copy, the copy-source precondition header doesn't set this key. The header accepts only the value `*`. |
| `s3:if-match` | The `If-Match` precondition on the destination object. Set only when an object-creation request carries the header. On a copy, the copy-source precondition header doesn't set this key. |
| `iam:[ORG-ID]:groups` | The CoreWeave IAM group memberships of the principal, sourced from SCIM. This key can contain multiple values, which you match using [set operators](#multi-valued-condition-keys-and-set-operators). Populated when the principal authenticates with a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md). Replace `[ORG-ID]` with your organization ID. |
| `oidc:[ORG-ID]:groups` | The group memberships carried in the `groups` claim of an OIDC token. This key can contain multiple values, which you match using [set operators](#multi-valued-condition-keys-and-set-operators). Populated when the principal authenticates through [OIDC Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md). Replace `[ORG-ID]` with your organization ID. |

```json highlight={10-16} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UniquePolicyName",
      "Effect": "Allow",
      "Principal": { ... },
      "Action": [ ... ],
      "Resource": [ ... ],
      "Condition": {
        // Operator
        "IpAddress": {
          // Key with value
          "cw:SourceIP": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

#### Internal CoreWeave service principals and IP conditions

The inventory reporting service does not provide a source IP address when it writes reports to your destination bucket.

An `IpAddress` condition does not match a request without a source IP address. A `NotIpAddress` condition does match one. That leads to two common problems:

* An `Allow` statement that includes an `IpAddress` condition does not grant access to a request that has no source IP.
* A `Deny` statement that uses `NotIpAddress` and applies to all principals can block a request that has no source IP, even if another statement allows that principal to access the bucket.

For blanket allow-by-IP statements, prefer `IpAddressIfExists`. That condition matches when the source IP is in the allowed range, or when the request has no source IP, so it does not block inventory reporting. You can also keep the inventory service `Allow` statement free of IP conditions, or place it before an `Allow` that uses `IpAddress`.

For a `NotIpAddress` `Deny` statement that would otherwise apply to all principals, exclude the inventory reporting service with `NotPrincipal`. Do not rely on `NotIpAddressIfExists` for this case. An absent source IP still matches that condition, so the `Deny` still applies.

In the following example, replace `[ALLOWED-IP-RANGE]` with the CIDR range or ranges you want to allow, such as `203.0.113.0/24`.

```json theme={"system"}
{
  "Sid": "DenyRequestsOutsideAllowedIPRanges",
  "Effect": "Deny",
  "NotPrincipal": {
    "CW": "arn:aws:iam::static:role/static/inventory"
  },
  "Action": "s3:*",
  "Resource": [
    "arn:aws:s3:::[BUCKET-NAME]",
    "arn:aws:s3:::[BUCKET-NAME]/*"
  ],
  "Condition": {
    "NotIpAddress": {
      "cw:SourceIP": ["[ALLOWED-IP-RANGE]"]
    }
  }
}
```

This statement does not grant the inventory reporting service access. Add a separate `Allow` statement with the permissions that the service requires. For inventory reporting, see [Set bucket access policies](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure.md#set-bucket-access-policies).

#### Multi-valued condition keys and set operators

Some condition keys, such as `iam:[ORG-ID]:groups` and `oidc:[ORG-ID]:groups`, carry more than one value. To compare a value in your policy against a multi-valued key, prefix a string operator with a set qualifier:

| Set qualifier | Description |
| - | - |
| `ForAnyValue:` | The condition matches if *at least one value* in the key matches a value in your policy. |
| `ForAllValues:` | The condition matches only if *every value* in the key matches a value in your policy. |

For example, `ForAnyValue:StringEqualsIgnoreCase` matches when any one of the principal's groups equals one of the listed values, ignoring case. Use these qualifiers whenever you write conditions against group memberships or other multi-valued attributes.

## Example use cases

The following examples show bucket access policies for common scenarios. Use them as templates and adapt the principals, resources, and conditions to your own buckets.

### Full access to a specific bucket for one user

This policy grants full access to a specific bucket for one user. It has two statements:

* The first statement allows the specified user to perform all S3 actions on the bucket and its contents.
* The second statement denies all other users access to the bucket and its contents.

Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[USER-ID]` with the ID of the user you want to grant full access to.
* `[BUCKET-NAME]` with the name of the bucket you want to grant full access to.

```json title="Full access to a specific bucket for one user" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowOnlyOneUser",
      "Effect": "Allow",
      "Principal": {
        "CW": "arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ]
    },
    {
      "Sid": "DenyAllOthers",
      "Effect": "Deny",
      "NotPrincipal": {
        "CW": "arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ]
    }
  ]
}
```

### Read-only for a specific bucket for a user and group

This policy grants read-only access to a specific bucket for one console user and one SAML group. It has two statements:

* The first statement allows the specified principals to list the bucket and get its location.
* The second statement allows the specified principals to get objects from the bucket.

Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[USER-ID]` with the console user's ID.
* `[SAML-GROUP-ID]` with the SAML group ID.
* `[BUCKET-NAME]` with the name of the bucket.

```json title="Read-only for a specific bucket for a user and group" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListBucket",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::[BUCKET-NAME]",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    },
    {
      "Sid": "AllowGetObjects",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    }
  ]
}
```

### Read-only for a specific bucket for a specific user

This policy grants read-only access to a specific bucket for a specific user. It has two statements:

* The first statement allows the specified user to list the bucket and get its location.
* The second statement allows the specified user to get objects from the bucket.

Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[USER-ID]` with the ID of the user you want to grant read-only access to.
* `[BUCKET-NAME]` with the name of the bucket you want to grant read-only access to.

```json title="Read-only for a specific bucket for a specific user" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UserReadBucket",
      "Effect": "Allow",
      "Principal": {
        "CW": "arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::[BUCKET-NAME]"
    },
    {
      "Sid": "UserGetObjects",
      "Effect": "Allow",
      "Principal": {
        "CW": "arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/*"
    }
  ]
}
```

### Read-only for all buckets for a user and group

This policy grants read-only access to all buckets for one console user and one SAML group. It has three statements:

* The first statement allows the specified principals to list all buckets.
* The second statement allows the specified principals to list and describe all buckets.
* The third statement allows the specified principals to get objects from all buckets.

Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[USER-ID]` with the console user's ID.
* `[SAML-GROUP-ID]` with the SAML group ID.

```json title="Read-only for all buckets for a user and group" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListAllBuckets",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": "s3:ListAllMyBuckets",
      "Resource": "arn:aws:s3:::*",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    },
    {
      "Sid": "ListAndDescribeBuckets",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::*",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    },
    {
      "Sid": "GetAllObjects",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::*/*",
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    }
  ]
}
```

### Limit to a specific prefix

This policy restricts the `ListBucket` action to a specific prefix within a bucket. It has two statements:

* The first statement allows the user to list objects in the bucket only if the prefix matches `projects`.
* The second statement denies the user from listing objects in the bucket if the prefix doesn't match `projects`.

The Condition statement allows the user to list only object keys that start with the `projects` prefix. An explicit `Deny` statement blocks the user from listing any other keys, even if other policies grant broader permissions. For instance, the user might later receive permissions to list all keys through an updated user policy or bucket policy. But because `Deny` takes precedence over `Allow`, CoreWeave denies any request to list keys outside the `projects` prefix.

Replace `[BUCKET-NAME]` with the name of the bucket, `[ORG-ID]` with your organization's ID, `[USER-ID]` with the console user's ID, and `[SAML-GROUP-ID]` with the SAML group ID.

```json title="Limit to a specific prefix" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowIfPrefixEquals",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]",
      "Condition": {
        "StringEquals": {
          "s3:prefix": "projects",
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    },
    {
      "Sid": "DenyIfPrefixNotEquals",
      "Effect": "Deny",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]",
      "Condition": {
        "StringNotEquals": {
          "s3:prefix": "projects"
        }
      }
    }
  ]
}
```

### Require conditional writes

This policy lets a principal add objects but not overwrite them. Use it when several writers share one identity, such as workloads that authenticate through [OIDC Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md). It has two statements:

* The first statement allows the user to create objects in the bucket.
* The second statement denies object creation unless the request carries an `If-None-Match` precondition, which makes the write succeed only when no object already exists at the key.

The `Deny` statement combines two conditions. The `Null` operator matches when `s3:if-none-match` is absent, and the `Bool` operator limits the statement to requests where `s3:ObjectCreationOperation` is `true`.

Object Storage sets `s3:ObjectCreationOperation` to `true` on `PutObject`, `CompleteMultipartUpload`, `CopyObject`, and `RenameObject`, and authorizes all four against `s3:PutObject`, so one pair of statements covers every creation path. A write that the `Deny` statement matches fails with `AccessDenied`. For the client side of these preconditions, see [Use conditional requests](https://docs.coreweave.com/products/storage/object-storage/buckets/conditional-requests.md).

Both statements are required. If a bucket policy exists but neither allows nor denies the request, [evaluation implicitly rejects it](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation), so a document that contains only the `Deny` statement also blocks the creates you intend to permit.

Use `Bool` rather than `BoolIfExists`. Internal CoreWeave services such as inventory reporting write without a request context, so `s3:ObjectCreationOperation` is absent on those writes. `BoolIfExists` matches an absent key, so the `Deny` statement blocks those writes.

Replace `[BUCKET-NAME]` with the name of the bucket, `[ORG-ID]` with your organization's ID, and `[USER-ID]` with the console user's ID.

```json title="Require conditional writes" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowObjectCreation",
      "Effect": "Allow",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"]
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/*"
    },
    {
      "Sid": "DenyOverwrites",
      "Effect": "Deny",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"]
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
      "Condition": {
        "Null": {
          "s3:if-none-match": "true"
        },
        "Bool": {
          "s3:ObjectCreationOperation": "true"
        }
      }
    }
  ]
}
```

## Attribute-based access control

Attribute-based access control (ABAC) grants access based on attributes carried by the principal rather than by naming each principal individually. When a principal authenticates, the credential carries a set of attributes, and you reference those attributes in a policy `Condition` to decide whether to allow or deny the request.

The most common attribute is the principal's group memberships:

* When a principal authenticates with a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md), the resulting credentials carry the principal's SCIM group memberships in the multi-valued `iam:[ORG-ID]:groups` condition key.
* When a principal authenticates through [OIDC Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the groups from the token's `groups` claim are carried in the multi-valued `oidc:[ORG-ID]:groups` condition key.

ABAC keeps policies stable as your organization changes. Instead of editing bucket policies every time someone joins or leaves a team, you manage membership in your identity provider, and the policy continues to grant access based on the group. Because the attributes come from the credential, you don't list individual principals to enforce these rules.

> [!NOTE]
>
> ABAC is different from specifying a group as a `Principal`. As described in [Key considerations](#key-considerations), you can't name a CoreWeave IAM group as a `Principal` in a bucket access policy. You can, however, match group memberships in a `Condition` using the `iam:[ORG-ID]:groups` and `oidc:[ORG-ID]:groups` keys, which is the basis for the [group-based access](#group-based-access) examples.

## Group-based access

This policy grants read access to a bucket only to principals who belong to the `admin` group. It uses the multi-valued `iam:[ORG-ID]:groups` condition key with the `ForAnyValue:StringEqualsIgnoreCase` set operator, so the request is allowed when any one of the principal's groups is `admin`.

Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[BUCKET-NAME]` with the name of the bucket you want to grant access to.

> [!CAUTION]
>
> Always include a `Condition` with `cw:PrincipalOrgID` when using `"Principal": "*"`. Without it, the bucket is accessible to anyone on the internet, not just principals in your organization.

```json title="Grant read access to members of the admin group" highlight={17-19} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAdminGroupRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ],
      "Condition": {
        "ForAnyValue:StringEqualsIgnoreCase": {
          "iam:[ORG-ID]:groups": ["admin"]
        }
      }
    }
  ]
}
```

To match groups from an OIDC token instead of an API access token, use the `oidc:[ORG-ID]:groups` key. Fill in the following parameters:

* `[ORG-ID]` with your organization's ID.
* `[BUCKET-NAME]` with the name of the bucket you want to grant access to.
* `[GROUP-NAME]` with the name of the group in your OIDC token's `groups` claim.

> [!CAUTION]
>
> Always include a `Condition` with `cw:PrincipalOrgID` when using `"Principal": "*"`. Without it, the bucket is accessible to anyone on the internet, not just principals in your organization.

```json title="Grant read access to members of an OIDC group" highlight={17-19} theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowOIDCGroupRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ],
      "Condition": {
        "ForAnyValue:StringEqualsIgnoreCase": {
          "oidc:[ORG-ID]:groups": ["[GROUP-NAME]"]
        }
      }
    }
  ]
}
```

To require membership in more than one group, list multiple values in the array, or add a separate condition with `ForAllValues:` to require all of them.

## Required policies and actions

Each API call requires permission to perform one or more related actions, and those action names don't always match the API calls. Some API calls perform multiple actions that require permission to separate actions. For example, copying an object requires permission to perform both `s3:PutObject` and `s3:GetObject` actions.

Use the following permission mapping when you plan bucket access policies. See [Object Storage API features](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#api-calls) for a complementary list of API calls mapped to their associated actions.

| Required action permission | API call |
| - | - |
| `s3:AbortMultipartUpload` | `s3:AbortMultiPartUpLoad` |
| `s3:CreateBucket` | `s3:CreateBucket` |
| `s3:DeleteBucket` | `s3:DeleteBucket` |
| `s3:DeleteObject` | `s3:DeleteObject` `s3:DeleteObjects` `s3:RenameObject` |
| `s3:DeleteObjectTagging` | `s3:DeleteObjectTagging` |
| `s3:DeleteObjectVersion` | `s3:DeleteObject` `s3:DeleteObjects` |
| `s3:DeleteLifecycleConfiguration` | `s3:DeleteBucketLifeCycle` |
| `s3:DeleteBucketPolicy` | `s3:DeleteBucketPolicy` |
| `s3:DeleteBucketTagging` | `s3:DeleteBucketTagging` |
| `s3:GetLifecycleConfiguration` | `s3:GetBucketLifecycleConfiguration` |
| `s3:GetBucketLocation` | `s3:GetBucketLocation` |
| `s3:GetBucketPolicy` | `s3:GetBucketPolicy` |
| `s3:GetBucketTagging` | `s3:GetBucketTagging` |
| `s3:GetBucketVersioning` | `s3:GetBucketVersioning` |
| `s3:GetObject` | `s3:CopyObject` `s3:GetObject` `s3:GetObjectAcl` `s3:GetObjectAttributes` `s3:HeadObject` `s3:UploadPartCopy` |
| `s3:GetObjectTagging` | `s3:GetObjectTagging` |
| `s3:ListAllMyBuckets` | `s3:ListBuckets` |
| `s3:ListBucket` | `s3:GetBucketACL` `s3:HeadBucket` `s3:ListObjectsV2` `s3:ListObjectVersions` |
| `s3:ListMultipartUploadParts` | `s3:ListParts` |
| `s3:ListBucketMultipartUploads` | `s3:ListMultiPartUploads` |
| `s3:PutLifecycleConfiguration` | `s3:PutBucketLifecycleConfiguration` |
| `s3:PutBucketPolicy` | `s3:PutBucketPolicy` If no policy exists, CoreWeave grants access to create a new policy if the user's organization ID matches the bucket's organization. |
| `s3:PutBucketTagging` | `s3:PutBucketTagging` |
| `s3:PutBucketVersioning` | `s3:PutBucketVersioning` |
| `s3:PutObject` | `s3:CompleteMultiPartUpLoad` `s3:CopyObject` `s3:CreateMultiPartUpLoad` `s3:PutObject` `s3:RenameObject` `s3:UploadPart` `s3:UploadPartCopy` `PutObject`, `CompleteMultiPartUpLoad`, `CopyObject`, and `RenameObject` support [conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes). |
| `s3:PutObjectTagging` | `s3:PutObjectTagging` |

## Bucket lifecycle policy

Bucket access policies and bucket lifecycle policies are configured separately and serve different purposes. Lifecycle policies automate object expiration, noncurrent version cleanup, and aborting incomplete multipart uploads, but they are not part of the bucket access policy. See [Bucket lifecycle policies](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md) for the full reference, examples, and apply procedures.

Permission to apply a lifecycle configuration is governed by the bucket access policy:

* [`s3:PutBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3putbucketlifecycleconfiguration) creates or replaces the lifecycle configuration on a bucket.
* [`s3:GetBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3getbucketlifecycleconfiguration) reads the lifecycle configuration on a bucket.
* [`s3:DeleteBucketLifeCycle`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3deletebucketlifecycle) removes the lifecycle configuration from a bucket.

> [!WARNING]
>
> Lifecycle deletions run as a privileged service action and are not evaluated against the bucket access policy or organization access policy. A `Deny` statement on `s3:DeleteObject` does not prevent a lifecycle rule from deleting matching objects. Control retention by restricting who can call `s3:PutBucketLifecycleConfiguration`. For more information, see [Understand automated deletion](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md#understand-automated-deletion).
