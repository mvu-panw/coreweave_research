# coreweave_object_storage_organization_access_policy (Resource)

Source: https://docs.coreweave.com/platform/terraform/resources/object_storage_organization_access_policy

# coreweave_object_storage_organization_access_policy (Resource)

> Terraform resource for creating organization-wide access policies for CoreWeave Object Storage

[Organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) enforce permissions for AI Object Storage across your entire CoreWeave organization, automatically covering every resource, bucket, and user in your account. At least one organization access policy must be in place before you can create a bucket.

## Example usage

```terraform theme={"system"}
resource "coreweave_object_storage_organization_access_policy" "test" {
  name = "full-s3-api-access"
  statements = [
    {
      name       = "allow-full-s3-api-access-to-all"
      effect     = "Allow"
      resources  = ["*"]
      principals = ["*"]
      actions = [
        "s3:*",
        "cwobject:*",
      ]
    }
  ]
}
```

## Schema

### Required

* `name` (String) The name of the organization access policy, must be unique.
* `statements` (Attributes Set) The list of access policy statements associated with this policy. At least one statement is required. (see [below for nested schema](#nestedatt--statements))

### Nested Schema for `statements`

Required:

* `actions` (Set of String) Defines which operations the policy allows or denies. Organization access policies can include actions from two APIs - S3 (s3:*) and AI Object Storage API (cwobject:*). You can use wildcards (like s3:\* or cwobject:\*) to cover multiple actions at once.
* `effect` (String) Must be either Allow or Deny (case-sensitive). Determines whether the statement grants or denies the specified actions on the listed resources for the designated principals. By default, all access is denied.
* `name` (String) A short, human-readable identifier for this specific policy statement, similar to Sid in bucket access policies.
* `principals` (Set of String) Defines which users, roles, or groups the policy applies to. Only short-form identifiers are supported. If you use a full ARN, the policy will fail with an error. See the [AI Object Storage documentation](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) for guidelines on defining principals.
* `resources` (Set of String) Defines which resources the policy applies to. See the [AI Object Storage documentation](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) for guidelines on defining resources.

## Import

Import is supported using the following syntax:

```bash theme={"system"}
terraform import coreweave_object_storage_organization_access_policy.default {{name}}
```

```terraform theme={"system"}
import {
  to = coreweave_object_storage_organization_access_policy.default
  id = "{{name}}"
}
```
