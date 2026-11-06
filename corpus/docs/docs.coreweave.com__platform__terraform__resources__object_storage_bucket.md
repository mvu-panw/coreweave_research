# coreweave_object_storage_bucket (Resource)

Source: https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket

# coreweave_object_storage_bucket (Resource)

> Terraform resource for creating CoreWeave Object Storage buckets with availability zone and tag configuration

Buckets are the primary organizational containers for your data in CoreWeave AI Object Storage. Bucket names must be globally-unique and not begin with `cw-` or `vip-`, which are reserved for internal use. Before creation, the provider verifies the complete list of buckets owned by the organization and fails without sending a create request if that inventory cannot be completed; an existing bucket with the requested name must be imported. Learn more about [creating buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md).

## Example usage

```terraform theme={"system"}
resource "coreweave_object_storage_bucket" "default" {
  name = "my-tf-test-bucket"
  zone = "US-EAST-04A"
  tags = {
    foo = "bar"
  }
}
```

## Schema

### Required

* `name` (String) The bucket name. Must be globally unique and must not begin with `cw-` or `vip-`.
* `zone` (String) The Availability Zone in which the bucket is located.

### Optional

* `tags` (Map of String) Map of tags to assign to the bucket.

## Import

Import is supported using the following syntax:

```bash theme={"system"}
terraform import coreweave_object_storage_bucket.default {{name}}
```

```terraform theme={"system"}
import {
  to = coreweave_object_storage_bucket.default
  id = "{{name}}"
}
```
