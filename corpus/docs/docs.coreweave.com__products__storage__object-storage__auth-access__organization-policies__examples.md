# Organization access policies examples

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/examples

# Organization access policies examples

> View examples of AI Object Storage organization access policies

This page lists examples of organization access policies for common use cases. You can use these examples as templates to create your own organization access policies, whether you need to grant broad administrative access, limit users to read-only operations, or combine multiple access patterns in a single policy.

Learn about [the structure of organization access policies and how to set them](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md).

## Full control

The following examples grant broad access to S3 resources. Use them when you need to give administrators, specific users, or all organization members full control over buckets and objects.

### Full control of all resources for admins

This policy contains one statement that grants full S3 API access (`s3:*`) to all SAML admins for all resources in the organization. The `resources` field is set to `"*"` to allow access to all S3 buckets and objects, and the `principals` field is set to `["role/Admin"]` to allow access to all users in the SAML Admin group.

```json title="Full control of all buckets for admins" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "full-s3-api-access",
    "statements": [
      {
        "name": "allow-full-s3-api-access-to-all",
        "effect": "Allow",
        "actions": [
          "s3:*"
        ],
        "resources": ["*"],
        "principals": ["role/Admin"]
      }
    ]
  }
}
```

### Full control of one specific bucket for all users

This policy contains one statement that grants full S3 API access (`s3:*`) to all users for a specific bucket. Replace `[BUCKET-NAME]` with the name of the bucket.

The `resources` field includes both the bucket itself and all objects within that bucket, which allows both bucket-level operations (like listing the bucket) and object-level operations (like getting or putting objects within that bucket). The `principals` field is set to `"*"` to allow access to all users.

```json title="Full control of one specific bucket for all users" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "full-access-specific-bucket",
    "statements": [
      {
        "name": "full-s3-access-for-all-users",
        "effect": "Allow",
        "actions": ["s3:*"],
        "resources": [
          "[BUCKET-NAME]",
          "[BUCKET-NAME]/*"
        ],
        "principals": ["*"]
      }
    ]
  }
}
```

### Full S3 API access to all users

This policy contains one statement that grants full S3 API access (`s3:*`) to all principals and resources in the organization. The `resources` field is set to `"*"` to allow access to all S3 buckets and objects, and the `principals` field is also set to `"*"` to allow access to all users.

Use this approach when you want to grant full access by default, then restrict specific buckets with bucket access policies.

```json title="Full S3 API access to all users" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "full-s3-api-access",
    "statements": [
      {
        "name": "allow-full-s3-api-access-to-all",
        "effect": "Allow",
        "actions": [
          "s3:*"
        ],
        "resources": ["*"],
        "principals": ["*"]
      }
    ]
  }
}
```

### Full control of all buckets for a specific user

This policy grants full S3 access (`s3:*`) to a specific Cloud Console user, identified by their UID. Replace `[USER-UID]` with the user's UID, which you can find in the user's settings within the Cloud Console.

The `resources` field uses the wildcard `"*"` to grant access across all buckets, but you can also narrow it to a specific bucket with the short-form resource names, as shown in [Full control of one specific bucket for all users](#full-control-of-one-specific-bucket-for-all-users).

```json title="Full control of all buckets for a specific user" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "s3-full-control-specific-user",
    "statements": [
      {
        "name": "full-s3-access-for-user",
        "effect": "Allow",
        "actions": ["s3:*"],
        "resources": ["*"],
        "principals": ["coreweave/[USER-UID]"]
      }
    ]
  }
}
```

## Read-only access

The following examples restrict access to read-only operations. Use them when you want users to view or download data without the ability to modify or delete it.

### Read-only access to all buckets

This policy provides read-only access to all S3 buckets for all principals. The actions `s3:List*`, `s3:Get*`, and `s3:Head*` commonly define read-only permissions.

```json title="Read-only access to all buckets" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "s3-read-only-all-buckets",
    "statements": [
      {
        "name": "read-only-access",
        "effect": "Allow",
        "actions": [
          "s3:List*",
          "s3:Get*",
          "s3:Head*"
        ],
        "resources": ["*"],
        "principals": ["*"]
      }
    ]
  }
}
```

### Read-only access to a specific bucket

This policy restricts everyone in the organization to read-only access for a specific bucket. Note the short-form bucket name used in the resources array, which is required in organization access policies.

Two resources are listed:

* The bucket itself (for example, `"[BUCKET-NAME]"`).
* All objects within that bucket (for example, `"[BUCKET-NAME]/*"`).

This allows both bucket-level operations (like listing the bucket) and object-level operations (like getting or listing objects within that bucket). The `principals` field is set to `"*"` to allow access to all users.

Replace `[BUCKET-NAME]` in the policy with the name of the bucket you want to restrict to read-only access.

```json title="Read-only access to a specific bucket" highlight={14-17} theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "specific-bucket-access",
    "statements": [
      {
        "name": "read-only-my-specific-bucket",
        "effect": "Allow",
        "actions": [
          "s3:List*",
          "s3:Get*",
          "s3:Head*"
        ],
        "resources": [
          "[BUCKET-NAME]",
          "[BUCKET-NAME]/*"
        ],
        "principals": ["*"]
      }
    ]
  }
}
```

### Allow non-admins limited AI Object Storage API access

This policy contains one statement for AI Object Storage API actions (`cwobject:`). It grants all non-admins the ability to create access keys and list access policies, but doesn't grant any other `cwobject:` access. Remember that `cwobject:` actions are global and require `"resources": ["*"]`.

Admins (as defined in Cloud Console) already have full `cwobject:` access, so this policy limits non-admin users to only these specified actions.

```json title="Allow non-admins limited AI Object Storage API access" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "limited-cwobject-access",
    "statements": [
      {
        "name": "allow-token-creation",
        "effect": "Allow",
        "actions": [
          "cwobject:CreateAccessKey",
          "cwobject:CreateAccessKeySAML",
          "cwobject:ListAccessPolicy",
          "cwobject:ListAccessKeyInfo"
        ],
        "resources": ["*"],
        "principals": ["*"]
      }
    ]
  }
}
```

### AI Object Storage API and S3 API access for a SAML group

This policy contains two statements that, when combined, grant all S3 API and AI Object Storage API actions to a specific SAML group, `role/Admin`.

* The first statement (`cwobject-access-for-saml-group`) grants all AI Object Storage API actions (`cwobject:*`).
* The second statement (`s3-access-for-saml-group`) grants all S3-compatible actions (`s3:*`).

This grants broad administrative access at the organization level, while you control membership through your Identity Provider (IdP) group.

```json title="AI Object Storage API and S3 API access for a SAML group" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "full-access-saml-admin-group",
    "statements": [
      {
        "name": "cwobject-access-for-saml-group",
        "effect": "Allow",
        "actions": [
          "cwobject:*"
        ],
        "resources": ["*"],
        "principals": ["role/Admin"]
      },
      {
        "name": "s3-access-for-saml-group",
        "effect": "Allow",
        "actions": [
          "s3:*"
        ],
        "resources": ["*"],
        "principals": ["role/Admin"]
      }
    ]
  }
}
```

## Advanced example

The following example shows how multiple statements can work together in a single policy to model a realistic access pattern.

This example combines three statements similar to the earlier examples into a single policy.

* The first statement, `s3-access`, grants full S3 API access to all principals and buckets.
* The second statement, `cwobject-access`, grants limited AI Object Storage API access to all non-admins.
  * Admin users don't need to be listed here, because they [have a special internal policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md#key-considerations) that grants full access.
* The third statement, `read-only`, makes a specific bucket read-only for a specific SAML group.

This resembles a real-world scenario that allows all users to manage S3 buckets, restricts AI Object Storage API access for non-admins, and limits a specific SAML group to read-only access on a specific bucket.

Replace `[BUCKET-NAME]` in the policy with the name of the bucket you want to restrict to read-only access.

```json title="Advanced example" theme={"system"}
{
  "policy": {
    "version": "v1alpha1",
    "name": "complex-access-policy",
    "statements": [
      {
        "name": "s3-access",
        "effect": "Allow",
        "actions": ["s3:*"],
        "resources": ["*"],
        "principals": ["*"]
      },
      {
        "name": "cwobject-access",
        "effect": "Allow",
        "actions": [
          "cwobject:CreateAccessKey",
          "cwobject:CreateAccessKeySAML",
          "cwobject:ListAccessPolicy",
          "cwobject:ListAccessKeyInfo"
        ],
        "resources": ["*"],
        "principals": ["*"]
      },
      {
        "name": "read-only",
        "effect": "Allow",
        "actions": [
          "s3:List*",
          "s3:Get*",
          "s3:Head*"
        ],
        "resources": [
          "[BUCKET-NAME]",
          "[BUCKET-NAME]/*"
        ],
        "principals": ["role/SAMLGroup"]
      }
    ]
  }
}
```
