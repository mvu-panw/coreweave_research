# coreweave_object_storage_bucket_settings (Resource)

Source: https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_settings

# coreweave_object_storage_bucket_settings (Resource)

> Terraform resource for managing CoreWeave Object Storage bucket settings such as audit logging

Manage settings for a CoreWeave AI Object Storage bucket.

## Example usage

```terraform theme={"system"}
resource "coreweave_object_storage_bucket" "default" {
  name = "my-bucket-with-settings"
  zone = "US-EAST-04A"
}

resource "coreweave_object_storage_bucket_settings" "default" {
  bucket                = coreweave_object_storage_bucket.default.name
  audit_logging_enabled = true

  # Limit STANDARD storage to 1 TiB. Your organization must be entitled to
  # configure per-bucket capacity caps before setting this attribute.
  capacity_cap_bytes = 1099511627776

  # Archive idle STANDARD objects to STANDARD_IA. Your organization must be
  # entitled to configure archive settings before enabling this.
  archive_enabled                = true
  archive_after_last_access_days = 60
}
```

## Schema

### Required

* `bucket` (String) The name of the bucket to manage settings for.

### Optional

* `archive_after_last_access_days` (Number) Days since last access (or creation if never accessed) before a STANDARD object version is archived to STANDARD\_IA. The default minimum is 60; your organization's entitlement may permit a different minimum, so the effective floor is validated server-side. Required when `archive_enabled` is true, and rejected otherwise.
* `archive_enabled` (Boolean) When true, idle STANDARD objects are archived to STANDARD\_IA after `archive_after_last_access_days` without access. Your organization must be entitled to configure this setting.
* `audit_logging_enabled` (Boolean) Whether audit logging is enabled for the bucket. Contact support to enable audit logging for your organization before enabling this setting.
* `capacity_cap_bytes` (Number) Maximum number of STANDARD-class bytes the bucket may store. New STANDARD writes are rejected once bucket usage would exceed this cap; `0` is a valid cap that blocks all new STANDARD writes. Omit to leave the cap unchanged. Removing this resource leaves any cap in place; the cap is cleared when the bucket itself is deleted. Your organization must be entitled to configure this setting.

## Import

Import is supported using the following syntax:

```bash theme={"system"}
terraform import coreweave_object_storage_bucket_settings.default {{bucket_name}}
```

```terraform theme={"system"}
import {
  to = coreweave_object_storage_bucket_settings.default
  id = "{{bucket_name}}"
}
```
