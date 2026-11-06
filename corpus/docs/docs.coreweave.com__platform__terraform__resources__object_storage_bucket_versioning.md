# coreweave_object_storage_bucket_versioning (Resource)

Source: https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_versioning

# coreweave_object_storage_bucket_versioning (Resource)

> Terraform resource for enabling or suspending versioning on CoreWeave Object Storage buckets

Versioning protects your data by preserving all versions of objects and preventing permanent deletion. When objects are deleted, they are "soft deleted" with delete markers, allowing you to restore previous versions and recover data. After creating a versioned bucket with Terraform, [use `rclone` to manage versioned objects and delete markers](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets).

## Example usage

```terraform theme={"system"}
resource "coreweave_object_storage_bucket" "default" {
  name = "bucket-versioning-example"
  zone = "US-EAST-04A"
}

resource "coreweave_object_storage_bucket_versioning" "default" {
  bucket = coreweave_object_storage_bucket.default.name
  versioning_configuration {
    status = "Enabled"
  }
}
```

## Schema

### Required

* `bucket` (String) The bucket on which to enable or suspend versioning.

### Optional

* `versioning_configuration` (Block, Optional) (see [below for nested schema](#nestedblock--versioning_configuration))

### Nested Schema for `versioning_configuration`

Required:

* `status` (String) Versioning state of the bucket. Valid values: Enabled, Suspended, or Disabled. Disabled should only be used when creating or importing resources that correspond to unversioned S3 buckets since the S3 API does not allow setting an Enabled/Suspended bucket to Disabled.

## Import

Import is supported using the following syntax:

```bash theme={"system"}
terraform import coreweave_object_storage_bucket_versioning.default {{bucket_name}}
```

```terraform theme={"system"}
import {
  to = coreweave_object_storage_bucket_versioning.default
  id = "{{bucket_name}}"
}
```
