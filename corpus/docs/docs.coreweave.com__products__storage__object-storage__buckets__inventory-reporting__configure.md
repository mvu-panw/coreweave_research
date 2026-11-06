# Configure inventory reporting for CoreWeave AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure

# Configure inventory reporting for CoreWeave AI Object Storage

> How to configure inventory reports for CoreWeave AI Object Storage buckets and objects

This guide explains how to configure and enable inventory reports for CoreWeave AI Object Storage buckets and objects. Inventory reports provide a scheduled, machine-readable list of the objects in a bucket, which you can use to audit object counts, track storage growth, and feed downstream analytics or compliance workflows.

## Prerequisites

This guide assumes you've already met the following prerequisites:

* You've already created a source bucket that you want to inventory.
* You have permissions to create a destination bucket for the output.
* You have permissions to set [bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) on the destination bucket.

To revisit any of these prerequisites, follow the links to the relevant guides:

* [Set up an access key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md)
* [Set up an organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md), which is required before you can create a bucket.
* [Create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md) to inventory.

## Choose a destination bucket

The destination bucket is where inventory reports are written. You can create a separate destination bucket for your inventory output, or use the same bucket as the source bucket. The rest of this guide refers to both options as the "destination bucket".

To use a separate destination bucket for your inventory reports, create a new bucket. When you create the bucket, choose a name that follows the bucket naming rules.

> [accordion] Bucket naming rules
>
> Bucket names must be globally unique and adhere to the following rules:
>
> * **Length:** 3 to 63 characters.
> * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> * **Prohibited patterns:** Cannot start with `xn--`.
> * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

Replace `[DESTINATION-BUCKET]` with the name for your destination bucket and `[AVAILABILITY-ZONE]` with the [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) to create it in.

```bash theme={"system"}
aws s3api create-bucket \
  --bucket [DESTINATION-BUCKET] \
  --create-bucket-configuration LocationConstraint=[AVAILABILITY-ZONE]
```

Inventory reporting is available in all [AI Object Storage regions](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

## Set bucket access policies

To enable inventory reporting, you must grant the CoreWeave inventory service permission to write reports to your destination bucket. This requires setting a [bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) on the destination bucket. This policy is required whether you use a separate destination bucket or write reports to the same bucket as your source data.

> [!WARNING]
>
> Inventory reporting requests do not include a source IP address. Do not put an `IpAddress` condition on the inventory service `Allow` statement, or that `Allow` does not match. For blanket allow-by-IP statements that must still permit inventory, use `IpAddressIfExists`. If you also use a `NotIpAddress` `Deny`, exclude the inventory service account from that `Deny`. See [Internal CoreWeave service principals and IP conditions](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#internal-coreweave-service-principals-and-ip-conditions).

The following permissions are required:

* Allow the CoreWeave inventory service account to write to the destination bucket. This is a CoreWeave-managed service account that generates and writes inventory reports to your destination bucket. On a bucket access policy for the destination bucket, grant write permission (`s3:PutObject`) and permission to clean up incomplete uploads (`s3:AbortMultipartUpload`) to the service account with the ARN `arn:aws:iam::static:role/static/inventory`. The service account uses `s3:AbortMultipartUpload` to clean up multipart uploads left behind by failed inventory report generation.
* Allow the user or entity that manages the bucket and accesses the reports to list the destination bucket and read, write, and delete report objects. The user configuring the inventory report needs the following permissions on the *source* bucket to apply the inventory configuration:

  * `s3:PutInventoryConfiguration`: Required to create, update, or delete an inventory configuration.
  * `s3:GetInventoryConfiguration`: Required to get or list inventory configurations.

Depending on your use case, you might need to grant additional permissions to the user or entity.

### Create source bucket policy

The following example bucket policy allows the entity requesting the inventory configuration to apply and manage the inventory configuration on the source bucket.

1. Create a source bucket policy file.

   Replace `[SOURCE-BUCKET]` with the name of the bucket you want to inventory, `[ORG-ID]` with your organization ID, and `[USER-UID]` with the UID of the user managing the inventory configuration.

   ```json title="source-bucket-policy.json" theme={"system"}
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "AllowInventoryConfigurationAccess",
         "Effect": "Allow",
         "Action": [
           "s3:PutInventoryConfiguration",
           "s3:GetInventoryConfiguration"
         ],
         "Resource": [
           "arn:aws:s3:::[SOURCE-BUCKET]"
         ],
         "Principal": {
           "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-UID]"]
         }
       }
     ]
   }
   ```

2. Apply the source bucket policy:

   ```bash theme={"system"}
   aws s3api put-bucket-policy \
     --bucket [SOURCE-BUCKET] \
     --policy file://source-bucket-policy.json
   ```

### Create destination bucket policy

The following example bucket policy allows the CoreWeave inventory service account to write inventory reports to the destination bucket, and the user or entity that issues the inventory list request to access the destination bucket.

Create a destination bucket policy file. Replace `[DESTINATION-BUCKET]` with the name of your destination bucket, `[ORG-ID]` with your organization ID, and `[USER-UID]` with the UID of the user managing the reports.

```json title="destination-bucket-policy.json" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowServiceAccountWriteReportsToDestination",
      "Effect": "Allow",
      "Principal": {
        "CW": "arn:aws:iam::static:role/static/inventory"
      },
      "Action": [
        "s3:PutObject",
        "s3:AbortMultipartUpload"
      ],
      "Resource": [
        "arn:aws:s3:::[DESTINATION-BUCKET]/*"
      ]
    },
    {
      "Sid": "AllowOwnerListDestination",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::[DESTINATION-BUCKET]"
      ],
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-UID]"]
      }
    },
    {
      "Sid": "AllowOwnerManageDestinationObjects",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::[DESTINATION-BUCKET]/*"
      ],
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-UID]"]
      }
    }
  ]
}
```

The destination bucket policy contains the following statements:

* The first statement, `AllowServiceAccountWriteReportsToDestination`, allows the CoreWeave inventory service account to write reports to the destination bucket. It also allows the service account to cancel incomplete multipart uploads from failed report generation. The `Principal` field identifies `arn:aws:iam::static:role/static/inventory`, the CoreWeave-managed service account that generates and writes inventory reports.
* The second statement, `AllowOwnerListDestination`, allows the entity to list objects in the destination bucket.
* The third statement, `AllowOwnerManageDestinationObjects`, allows the entity to read, write, and delete inventory report objects. The `Principal` fields in the second and third statements identify the user who reads and manages the inventory reports.

### Apply source and destination bucket policies

With both policy files prepared, apply them to their respective buckets so the inventory service and the user managing the configuration have the access they need:

```bash theme={"system"}
aws s3api put-bucket-policy \
  --bucket [SOURCE-BUCKET] \
  --policy file://source-bucket-policy.json

aws s3api put-bucket-policy \
  --bucket [DESTINATION-BUCKET] \
  --policy file://destination-bucket-policy.json
```

After you apply both policies, the inventory service can write reports to the destination bucket, and the user managing the configuration can access the required buckets.

### Use the same bucket for source and destination

Alternatively, to write inventory reports to the same bucket as the source bucket, grant access to the service account to write to the source bucket. You still need the [inventory configuration permissions](#set-bucket-access-policies). If you created the bucket, you likely already have these permissions.

1. Create the following bucket policy file:

   ```json title="same-bucket-policy.json" theme={"system"}
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "AllowServiceAccountWriteReports",
         "Effect": "Allow",
         "Principal": {
           "CW": "arn:aws:iam::static:role/static/inventory"
         },
         "Action": [
           "s3:PutObject",
           "s3:AbortMultipartUpload"
         ],
         "Resource": [
           "arn:aws:s3:::[SOURCE-BUCKET]/*"
         ]
       }
     ]
   }
   ```

   Replace `[SOURCE-BUCKET]` with the name of your source bucket. The `s3:AbortMultipartUpload` permission lets the service account clean up multipart uploads left behind by failed inventory report generation.

2. Apply this policy to the source bucket:

   ```bash theme={"system"}
   aws s3api put-bucket-policy \
     --bucket [SOURCE-BUCKET] \
     --policy file://same-bucket-policy.json
   ```

## Configure the inventory report

With the destination bucket and access policies in place, you can now configure the inventory report itself. To configure inventory reporting, you specify:

* A **source bucket** to inventory. You can inventory all the objects in the bucket or only prefixes that you specify. If you don't specify a prefix, all objects are inventoried.
* A **destination bucket** where reports are written. You can use a separate destination bucket or the same bucket as the source bucket.
* An optional prefix (subdirectory) within the destination bucket for organizing reports. If you don't specify a prefix, the reports are written to the root of the destination bucket. Use a prefix (like `inventory-reports/`) in your inventory configuration to separate reports from your source data.

You can configure your inventory report using the [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) with standard S3 tools like `aws s3api`. The configuration is a JSON object that defines the inventory configuration for the bucket.

The following fields are available:

| Field | Description | Note |
| - | - | - |
| `Destination.S3BucketDestination` | Configures destination bucket for inventory report | |
| `Destination.S3BucketDestination.Bucket` | Destination bucket name, can be same as source bucket | Example: `[DESTINATION-BUCKET]` |
| `Destination.S3BucketDestination.Format` | Report object format | Accepts: `CSV`, `TSV`, `JSON`, `ORC`, `Parquet` |
| `Destination.S3BucketDestination.Prefix` | Prefix for report objects | Example: `inventory/`  Inventory report objects are created with `inventory/` prefix in the object key. |
| `IsEnabled` | Controls enablement of the inventory configuration | Accepts: `true` or `false` |
| `Filter` | Filters source objects to include in inventory report | |
| `Filter.Prefix` | Source objects' prefix | Example: `documents/`  Only objects with prefix `documents/` are included in the report. |
| `Id` | Inventory configuration ID | Example: `my-inventory-config` |
| `IncludedObjectVersions` | Controls which object versions are included in the inventory report | Accepts: `All` or `Current` - `All`: Include all versions - `Current`: Only current versions |
| `OptionalFields` | Controls additional information to include in the report | Example: `["Size", "LastAccessedDate"]`  Inventory report then has fields: - `Bucket` - `Key` - `Size` - `LastAccessedDate` |
| `Schedule` | Controls the schedule of inventory reporting | |
| `Schedule.Frequency` | Sets schedule frequency | Accepts: `Daily` or `Weekly` |

1. Create a bucket inventory configuration file. The following is an example bucket inventory configuration:

   Replace `[DESTINATION-BUCKET]` with the name of the bucket where inventory reports are written.

   ```json title="bucket-inventory-config.json" theme={"system"}
       {
       "Destination": {
           "S3BucketDestination": {
               "Bucket": "arn:aws:s3:::[DESTINATION-BUCKET]",
               "Format": "ORC",
               "Prefix": "inventory/"
           }
       },
       "IsEnabled": true,
       "Filter": {
           "Prefix": "documents/"
       },
       "Id": "my-inventory-config",
       "IncludedObjectVersions": "All",
       "OptionalFields": [
           "LastAccessedDate"
       ],
       "Schedule": {
           "Frequency": "Daily"
       }
   }
   ```

2. Apply the bucket inventory configuration:

   Replace `[SOURCE-BUCKET]` with the name of the bucket you want to inventory.

   ```bash theme={"system"}
   aws s3api put-bucket-inventory-configuration \
     --bucket [SOURCE-BUCKET] \
     --id my-inventory-config \
     --inventory-configuration file://bucket-inventory-config.json
   ```

You now have an inventory configuration for the source bucket.

## Manage inventory report configurations

After an inventory configuration is in place, you can update, inspect, or remove it as your needs change. You can manage your inventory report configurations using the [S3 API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) with standard S3 tools.

The following is an example of how to create, update, get, and delete inventory report configurations using the AWS CLI:

Replace `[SOURCE-BUCKET]` with the name of the bucket you're inventorying.

```bash theme={"system"}
# Create or update bucket inventory configuration by ID
aws s3api put-bucket-inventory-configuration \
  --bucket [SOURCE-BUCKET] \
  --id my-inventory-config \
  --inventory-configuration file://bucket-inventory-config.json

# List bucket inventory configurations
aws s3api list-bucket-inventory-configurations --bucket [SOURCE-BUCKET]

# Get bucket inventory configuration by ID
aws s3api get-bucket-inventory-configuration \
  --bucket [SOURCE-BUCKET] \
  --id my-inventory-config

# Delete bucket inventory configuration by ID
aws s3api delete-bucket-inventory-configuration \
  --bucket [SOURCE-BUCKET] \
  --id my-inventory-config
```

If you check your inventory configuration with the `get` command, you might see output like this:

```json title="bucket-inventory-config.json" theme={"system"}
{
    "InventoryConfiguration": {
        "Destination": {
            "S3BucketDestination": {
                "Bucket": "arn:aws:s3:::my-destination-bucket",
                "Format": "ORC",
                "Prefix": "inventory/"
            }
        },
        "IsEnabled": true,
        "Filter": {
            "Prefix": "documents/"
        },
        "Id": "my-inventory-config",
        "IncludedObjectVersions": "All",
        "OptionalFields": [
            "LastAccessedDate"
        ],
        "Schedule": {
            "Frequency": "Daily"
        }
    }
}
```

## Use Terraform

Use the [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md) version 0.22.0 or later to manage inventory report configurations with native CoreWeave resources. Authenticate with a CoreWeave API token using `COREWEAVE_API_TOKEN`. The provider obtains temporary S3 credentials itself, so no separately managed access-key resource is required.

The following example creates source and destination buckets and a daily ORC report for objects under `documents/`, including `LastAccessedDate`. The destination policy grants the inventory service only `s3:PutObject` and `s3:AbortMultipartUpload` on the `inventory/` prefix. The owner statements let the Terraform caller list the destination bucket and read, write, and delete reports under that prefix. They also grant the bucket reads and cleanup permissions Terraform uses to manage these resources. The identity running Terraform still needs the [bucket and inventory configuration permissions](#set-bucket-access-policies) described earlier, along with permission to create buckets and manage their policies.

Replace `[SOURCE-BUCKET]` and `[DESTINATION-BUCKET]` with bucket names, and `[AVAILABILITY-ZONE]` with an [AI Object Storage Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). If the buckets already exist, import them into Terraform before applying this configuration.

> [accordion] Bucket naming rules
>
> Bucket names must be globally unique and adhere to the following rules:
>
> * **Length:** 3 to 63 characters.
> * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> * **Prohibited patterns:** Cannot start with `xn--`.
> * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

```hcl title="main.tf" theme={"system"}
terraform {
  required_providers {
    coreweave = {
      source  = "coreweave/coreweave"
      version = ">= 0.22.0"
    }
  }
}

provider "coreweave" {}

data "coreweave_caller_identity" "current" {}

resource "coreweave_object_storage_bucket" "source" {
  name = "[SOURCE-BUCKET]"
  zone = "[AVAILABILITY-ZONE]"
}

resource "coreweave_object_storage_bucket" "destination" {
  name = "[DESTINATION-BUCKET]"
  zone = "[AVAILABILITY-ZONE]"
}

resource "coreweave_object_storage_bucket_policy" "destination" {
  bucket = coreweave_object_storage_bucket.destination.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowServiceAccountWriteReportsToDestination"
        Effect = "Allow"
        Principal = {
          CW = "arn:aws:iam::static:role/static/inventory"
        }
        Action = [
          "s3:PutObject",
          "s3:AbortMultipartUpload",
        ]
        Resource = ["arn:aws:s3:::${coreweave_object_storage_bucket.destination.name}/inventory/*"]
      },
      {
        Sid    = "AllowOwnerManageDestination"
        Effect = "Allow"
        Principal = {
          CW = "arn:aws:iam::${data.coreweave_caller_identity.current.organization_id}:coreweave/${data.coreweave_caller_identity.current.principal_id}"
        }
        Action = [
          "s3:ListBucket",
          "s3:GetBucketPolicy",
          "s3:DeleteBucketPolicy",
          "s3:GetBucketLocation",
          "s3:GetBucketTagging",
          "s3:DeleteBucket",
        ]
        Resource = ["arn:aws:s3:::${coreweave_object_storage_bucket.destination.name}"]
      },
      {
        Sid    = "AllowOwnerManageDestinationObjects"
        Effect = "Allow"
        Principal = {
          CW = "arn:aws:iam::${data.coreweave_caller_identity.current.organization_id}:coreweave/${data.coreweave_caller_identity.current.principal_id}"
        }
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = ["arn:aws:s3:::${coreweave_object_storage_bucket.destination.name}/inventory/*"]
      },
    ]
  })
}

resource "coreweave_object_storage_bucket_inventory" "report" {
  bucket                   = coreweave_object_storage_bucket.source.name
  name                     = "my-inventory-config"
  enabled                  = true
  included_object_versions = "All"
  optional_fields          = ["Size", "LastAccessedDate"]

  schedule {
    frequency = "Daily"
  }

  filter {
    prefix = "documents/"
  }

  destination {
    bucket {
      bucket_arn = "arn:aws:s3:::${coreweave_object_storage_bucket.destination.name}"
      format     = "ORC"
      prefix     = "inventory/"
    }
  }

  depends_on = [coreweave_object_storage_bucket_policy.destination]
}
```

The `depends_on` entry ensures Terraform applies the destination policy before creating the inventory configuration. If you change the destination prefix, update the policy's `Resource` path to match. The policy resource replaces the entire destination policy. For an existing bucket, include any statements you need to retain in this configuration before applying it.

Once a bucket policy exists, requests it does not explicitly allow are implicitly denied, even when an organization access policy allows them. The owner statements use `coreweave_caller_identity` to grant the authenticated caller access. Add explicit bucket policy grants for any other report readers. See [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

The inventory resource supports the following options:

| Argument | Supported values |
| - | - |
| `included_object_versions` | `All` includes all versions. `Current` includes only current versions. |
| `optional_fields` | `Size`, `LastModifiedDate`, `LastAccessedDate`, `StorageClass`, `ETag`, `IsMultipartUploaded`, `EncryptionStatus`, `ChecksumAlgorithm`. Omit the argument if you don't need extra fields. An empty set is invalid. |
| `destination.bucket.format` | `CSV`, `TSV`, `JSON`, `ORC`, `Parquet`. |
| `schedule.frequency` | `Daily` or `Weekly`. |

To import an existing inventory configuration, use the ID format `bucket:inventory_name`. Replace `[SOURCE-BUCKET]` with the source bucket name and `[INVENTORY-NAME]` with the existing inventory configuration name:

```bash theme={"system"}
terraform import coreweave_object_storage_bucket_inventory.report '[SOURCE-BUCKET]:[INVENTORY-NAME]'
```

## Check your inventory report

After you apply your inventory configuration, allow some time for the inventory report to be generated and written to the destination bucket, then check the path where you configured the inventory report to be written. No notification is sent when the inventory report completes, so you must check the destination bucket to confirm the report is ready.

When the inventory report completes, you should see a `manifest.json` file written to the root of the subdirectory specified in the inventory configuration, and one or more inventory data files. You can use the manifest file to understand the structure of the inventory report. See [Manifest file](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting.md#manifest-file).

## Disable inventory reporting

If you no longer need inventory reports for a bucket, you can stop generating new reports without losing the configuration's history. To disable inventory reporting, either modify the inventory configuration to set `IsEnabled` to `false`, or delete the inventory configuration.

The following example shows a modified inventory configuration file that disables inventory reporting:

```json title="modified-inventory-config.json" highlight={9} theme={"system"}
{
  "Destination": {
    "S3BucketDestination": {
      "Bucket": "arn:aws:s3:::[DESTINATION-BUCKET]",
      "Format": "ORC",
      "Prefix": "inventory/"
    }
  },
  "IsEnabled": false,
  "Filter": {
    "Prefix": "documents/"
  },
  "Id": "my-inventory-config",
  "IncludedObjectVersions": "All",
  "OptionalFields": [
    "LastAccessedDate"
  ],
  "Schedule": {
    "Frequency": "Daily"
  }
}
```

Use these commands to apply the modified inventory configuration or delete the inventory configuration:

```bash theme={"system"}
# Modify bucket inventory configuration
aws s3api put-bucket-inventory-configuration \
  --bucket [SOURCE-BUCKET] \
  --id my-inventory-config \
  --inventory-configuration file://modified-inventory-config.json

# Delete bucket inventory configuration
aws s3api delete-bucket-inventory-configuration \
  --bucket [SOURCE-BUCKET] \
  --id my-inventory-config
```
