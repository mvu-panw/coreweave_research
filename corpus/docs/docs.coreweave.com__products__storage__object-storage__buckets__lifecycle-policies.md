# Configure bucket lifecycle policies

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies

# Configure bucket lifecycle policies

> Use lifecycle policies to expire objects, clean up old versions, and abort incomplete multipart uploads.

A **bucket lifecycle policy** is a set of rules that tells CoreWeave AI Object Storage to automatically delete objects, expire old object versions, or abort incomplete multipart uploads on a schedule you define. Lifecycle policies are the most reliable way to keep storage costs predictable, prevent unbounded growth from forgotten data, and unblock bucket deletion when incomplete multipart uploads accumulate.

A lifecycle configuration is a JSON document with one or more rules. Each rule has a filter that selects which objects it applies to and one or more actions that run when an object matches the filter and reaches the rule's age threshold.

## Supported actions

AI Object Storage supports the following lifecycle actions:

* **`Expiration`**: Delete current object versions when they reach a given age, on a specific date, or after they become an expired delete marker.
* **`NoncurrentVersionExpiration`**: For versioned buckets, delete noncurrent object versions when they reach a given age. Optionally retain a fixed number of newer noncurrent versions.
* **`AbortIncompleteMultipartUpload`**: Permanently abort multipart uploads that have not completed within a given number of days after initiation, removing all uploaded parts.

`Transition` actions, which move objects between storage classes, are not supported. Within the `STANDARD` storage class, AI Object Storage classifies objects as Hot, Warm, or Cold for billing automatically, based on access patterns. See [Cost management](https://docs.coreweave.com/products/storage/object-storage/about.md#cost-management) for details.

To move objects into the Archive storage class (`STANDARD_IA`), write or copy them with the storage class set explicitly, or enable Automated Archive on the bucket. Automated Archive is a control-plane setting rather than a lifecycle transition. See [Use the Archive storage class](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md).

## Access control for lifecycle configurations

Bucket access policies control who can manage a lifecycle configuration. They don't contain the lifecycle rules themselves.

### Control configuration access

Grant the following permissions in a bucket access policy to authorize the corresponding S3-compatible lifecycle configuration API calls:

* `s3:GetLifecycleConfiguration` authorizes [`s3:GetBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3getbucketlifecycleconfiguration).
* `s3:PutLifecycleConfiguration` authorizes [`s3:PutBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3putbucketlifecycleconfiguration).
* `s3:DeleteLifecycleConfiguration` authorizes [`s3:DeleteBucketLifeCycle`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3deletebucketlifecycle).

### Understand automated deletion

> [!WARNING]
>
> Lifecycle rule execution is separate from organization and bucket access policy evaluation. A `Deny` on `s3:DeleteObject` doesn't stop lifecycle deletions.

Lifecycle deletions run as a privileged service action. To control automated deletion, restrict who can create or replace lifecycle configurations through [`s3:PutBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3putbucketlifecycleconfiguration).

## Lifecycle rule behavior

The following behaviors affect how lifecycle rules select objects and run actions:

* **Object age is measured from creation time, not last access time.** A `Days: 7` rule deletes an object 7 days after it was uploaded, regardless of how recently it was read. To target objects by access pattern, use the [tier-based pricing model](https://docs.coreweave.com/products/storage/object-storage/about.md#cost-management) instead. To delete objects based on when they were last accessed, see [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md).
* **Eligibility is evaluated at UTC midnight day boundaries.** Eligibility is calculated by adding `Days` to the object's creation time and rounding the result up to the next midnight UTC. A `Days: 7` rule on an object uploaded at 14:00 UTC on day 1 makes it eligible at midnight UTC on day 9. Storage fees continue to accrue until the physical deletion completes.
* **Applying or editing a policy restarts lifecycle scanning.** Objects that are already eligible are processed according to the matching rule as the new scan reaches them. Objects that become eligible later are processed after the UTC midnight on which they become eligible. Processing is asynchronous, and the first visible deletions can be delayed, especially for large buckets.
* **Large buckets clear progressively.** Scanning resumes where each batch stopped, and a prefix with tens of millions of objects can take many hours to clear. Different prefixes can show progress at different times. Monitor total bucket usage alongside object or version listings; activity in one prefix might not represent progress across the bucket.
* **Versioning interacts with `Expiration`.** On a versioning-enabled bucket, an `Expiration` rule does not permanently delete objects -- it writes a delete marker, making the current version noncurrent. On a versioning-suspended bucket, expiration creates a delete marker with a null version ID; if the current version already has a null version ID, it is permanently replaced. To permanently remove data in either case, also configure `NoncurrentVersionExpiration`.
* **Putting a configuration replaces the existing one.** [`s3:PutBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3putbucketlifecycleconfiguration) overwrites the entire lifecycle configuration for a bucket. Always send the full set of rules you want enforced.
* **Each bucket can have up to 1,000 lifecycle rules.** See [Manage quotas and limits](https://docs.coreweave.com/products/storage/object-storage/manage-quotas.md) for the full limits table.
* **Disabling or deleting a rule unschedules pending expirations.** If a rule is disabled or removed, objects that were already queued for expiration are unscheduled and are not deleted.
* **When multiple rules match the same object on the same day, the most aggressive action wins.** Permanent deletion takes precedence over creating a delete marker. If two expiration rules overlap, the shorter expiration period is applied. When a broad rule (empty prefix) and a narrower rule (specific prefix) both match, both run independently.

## Rule filters

A rule's `Filter` selects which objects the rule applies to. A rule with an empty filter applies to every object in the bucket.

### Prefix filter

A prefix filter applies the rule to objects whose keys start with the given prefix. Use prefix filters to scope rules to a folder-like portion of a bucket.

```json title="Apply only to objects under the logs/ prefix" theme={"system"}
{
  "Rules": [
    {
      "ID": "ExpireLogsAfter30Days",
      "Filter": {
        "Prefix": "logs/"
      },
      "Status": "Enabled",
      "Expiration": {
        "Days": 30
      }
    }
  ]
}
```

### Tag filter

A tag filter applies the rule to objects that carry a specific object tag. Use tag filters when objects you want to expire are not grouped by key prefix.

```json title="Apply only to objects tagged temp=true" theme={"system"}
{
  "Rules": [
    {
      "ID": "ExpireTaggedTemporaryObjects",
      "Filter": {
        "Tag": {
          "Key": "temp",
          "Value": "true"
        }
      },
      "Status": "Enabled",
      "Expiration": {
        "Days": 7
      }
    }
  ]
}
```

To match objects that have **all** of multiple tags, wrap the tags in `And`. Objects with additional tags beyond those listed still match.

```json title="Apply only to objects tagged environment=dev AND team=ml-training" theme={"system"}
{
  "Filter": {
    "And": {
      "Tags": [
        { "Key": "environment", "Value": "dev" },
        { "Key": "team", "Value": "ml-training" }
      ]
    }
  }
}
```

### Size filter

A size filter matches objects whose size falls within a specified range. Both boundaries are **exclusive** -- objects exactly at the boundary value are not matched. Values are in bytes.

```json title="Apply only to objects larger than 1 MB and smaller than 100 MB" theme={"system"}
{
  "Filter": {
    "ObjectSizeGreaterThan": 1048576,
    "ObjectSizeLessThan": 104857600
  }
}
```

Size constraints can be combined with a prefix and tags using `And`. See [Combined filter](#combined-filter) below.

### Combined filter

A rule can combine a prefix, multiple tags, and object size constraints by wrapping them in `And`.

```json title="Apply to large objects under archive/ tagged class=cold" theme={"system"}
{
  "Rules": [
    {
      "ID": "ExpireLargeColdArchives",
      "Filter": {
        "And": {
          "Prefix": "archive/",
          "Tags": [
            { "Key": "class", "Value": "cold" }
          ],
          "ObjectSizeGreaterThan": 1048576
        }
      },
      "Status": "Enabled",
      "Expiration": {
        "Days": 90
      }
    }
  ]
}
```

## Common configurations

The following configurations cover the most common use cases. Each configuration is a complete, valid lifecycle document you can apply to a bucket as is.

> [tab] Expire objects after 7 days
>
> This configuration expires every object in the bucket 7 days after it is uploaded.
>
> ```json title="Expire all objects 7 days after creation" theme={"system"}
> {
>   "Rules": [
>     {
>       "ID": "ExpireObjectsAfter7Days",
>       "Filter": {},
>       "Status": "Enabled",
>       "Expiration": {
>         "Days": 7
>       }
>     }
>   ]
> }
> ```

> [tab] Expire noncurrent versions
>
> On versioned buckets, this configuration expires noncurrent object versions 7 days after they become noncurrent and retains the 10 most recent noncurrent versions of each object.
>
> ```json title="Expire noncurrent versions after 7 days, keep 10 newest noncurrent" theme={"system"}
> {
>   "Rules": [
>     {
>       "ID": "ExpireNoncurrentAfter7DaysKeep10",
>       "Filter": {},
>       "Status": "Enabled",
>       "NoncurrentVersionExpiration": {
>         "NoncurrentDays": 7,
>         "NewerNoncurrentVersions": 10
>       }
>     }
>   ]
> }
> ```

> [tab] Abort incomplete multipart uploads
>
> This configuration aborts multipart uploads that have not completed 7 days after they were initiated, removing all uploaded parts. This is the recommended baseline for every bucket. Without it, abandoned uploads accumulate as orphaned parts that consume storage and prevent bucket deletion.
>
> ```json title="Abort incomplete multipart uploads after 7 days" theme={"system"}
> {
>   "Rules": [
>     {
>       "ID": "AbortIncompleteMpuAfter7Days",
>       "Filter": {},
>       "Status": "Enabled",
>       "AbortIncompleteMultipartUpload": {
>         "DaysAfterInitiation": 7
>       }
>     }
>   ]
> }
> ```

> [tab] Expire objects on a fixed date
>
> Date-based expiration removes matching objects on and after a specific UTC date. Unlike day-count expiration, this is **not a one-time event** -- newly created objects that match the filter continue to be expired as long as the rule is enabled. Disable or remove the rule to stop the action.
>
> ```json title="Expire all objects after December 31, 2025" theme={"system"}
> {
>   "Rules": [
>     {
>       "ID": "ExpireAfterDate",
>       "Filter": {},
>       "Status": "Enabled",
>       "Expiration": {
>         "Date": "2025-12-31T00:00:00Z"
>       }
>     }
>   ]
> }
> ```

> [tab] ML training retention policy
>
> This configuration applies three retention rules suited to AI training workloads: short retention for inference outputs, medium retention for training checkpoints, and automatic MPU cleanup across the entire bucket.
>
> ```json title="Retention policy for training and inference data" theme={"system"}
> {
>   "Rules": [
>     {
>       "ID": "ExpireInferenceOutputs",
>       "Filter": { "Prefix": "inference-outputs/" },
>       "Status": "Enabled",
>       "Expiration": { "Days": 7 }
>     },
>     {
>       "ID": "ExpireTrainingCheckpoints",
>       "Filter": { "Prefix": "checkpoints/" },
>       "Status": "Enabled",
>       "Expiration": { "Days": 14 }
>     },
>     {
>       "ID": "AbortIncompleteMpuAfter7Days",
>       "Filter": {},
>       "Status": "Enabled",
>       "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
>     }
>   ]
> }
> ```

You can combine multiple rules in one configuration. A single configuration that applies all three of the preceding patterns at once would include three entries in the `Rules` array.

## Apply a lifecycle configuration

Save the lifecycle configuration to a file, then apply it to your bucket using one of the following clients.

> [tab] AWS CLI
>
> 1. Save the configuration to a local file, for example `lifecycle.json`.
>
> 2. Apply the configuration. Replace `[BUCKET-NAME]` with the name of your bucket.
>
>    ```bash title="Apply a lifecycle configuration with AWS CLI" theme={"system"}
>    aws s3api put-bucket-lifecycle-configuration \
>        --bucket [BUCKET-NAME] \
>        --lifecycle-configuration file://lifecycle.json
>    ```

> [tab] s3cmd
>
> s3cmd accepts the lifecycle configuration as an XML document.
>
> 1. Save the configuration to a local file, for example `lifecycle.xml`. The XML form of the abort-incomplete-multipart-upload example shown earlier is:
>
>    ```xml title="lifecycle.xml" theme={"system"}
>    <LifecycleConfiguration>
>      <Rule>
>        <ID>AbortIncompleteMpuAfter7Days</ID>
>        <Filter />
>        <Status>Enabled</Status>
>        <AbortIncompleteMultipartUpload>
>          <DaysAfterInitiation>7</DaysAfterInitiation>
>        </AbortIncompleteMultipartUpload>
>      </Rule>
>    </LifecycleConfiguration>
>    ```
>
> 2. Apply the configuration. Replace `[BUCKET-NAME]` with the name of your bucket.
>
>    ```bash title="Apply a lifecycle configuration with s3cmd" theme={"system"}
>    s3cmd setlifecycle lifecycle.xml s3://[BUCKET-NAME]
>    ```

> [tab] Boto3
>
> 1. Set environment variables for your CoreWeave credentials:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
>    Alternatively, configure your CoreWeave credentials to work with the AWS CLI.
>
>    We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.
>
>    > [!TIP]
>    >
>    > For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.
>
>    > [accordion] Configure CoreWeave credentials with static access keys
>    >
>    > 1. Create a `cw` profile:
>    >
>    >    ```bash title="Create a new profile" theme={"system"}
>    >    aws configure --profile cw
>    >    ```
>    >
>    > 2. When prompted, provide the following values:
>    >
>    >    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    >    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    >    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    >    * **Default output format**: Use `json` for JSON output.
>    >
>    > 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>    >
>    >    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    >    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>    >
>    >    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    >    aws configure set endpoint_url https://cwobject.com --profile cw
>    >    ```
>    >
>    > 4. Set the S3 `addressing_style` to `virtual`:
>    >
>    >    ```bash title="Set virtual addressing style" theme={"system"}
>    >    aws configure set s3.addressing_style virtual --profile cw
>    >    ```
>    >
>    > To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>    >
>    > If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.
>
>    > [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>    >
>    > If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>    >
>    > Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>    >
>    > ```bash title="Configure WIF OIDC credentials" theme={"system"}
>    > export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
>    > export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>    >
>    > aws configure set s3.addressing_style virtual
>    >
>    > export AWS_REGION="[AVAILABILITY-ZONE]"
>    > export AWS_ENDPOINT_URL_S3="https://cwobject.com"
>    > ```
>    >
>    > With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>    >
>    > Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.
>
> 2. Apply the lifecycle configuration. Replace `[BUCKET-NAME]` with the name of your bucket.
>
>    ```python title="Apply a lifecycle configuration with Boto3" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>
>    boto_config = Config(
>        region_name='US-EAST-04A',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    response = s3.put_bucket_lifecycle_configuration(
>        Bucket='[BUCKET-NAME]',
>        LifecycleConfiguration={
>            'Rules': [
>                {
>                    'ID': 'AbortIncompleteMpuAfter7Days',
>                    'Filter': {},
>                    'Status': 'Enabled',
>                    'AbortIncompleteMultipartUpload': {
>                        'DaysAfterInitiation': 7
>                    }
>                }
>            ]
>        }
>    )
>
>    print(response)
>    ```

## Verify a lifecycle configuration

Confirm the active configuration on a bucket. For a current object that matches an `Expiration.Date` or `Expiration.Days` rule, use the `HeadObject` (AWS CLI: `head-object`) or `GetObject` API to read the `x-amz-expiration` header. It reports the calculated expiration date and rule ID before deletion occurs; it does not confirm processor progress. This header does not report the schedule for `NoncurrentVersionExpiration` rules. For incomplete multipart uploads that match an `AbortIncompleteMultipartUpload` rule, `ListParts` returns the `x-amz-abort-date` and `x-amz-abort-rule-id` headers instead.

> [tab] AWS CLI
>
> ```bash title="Get the active lifecycle configuration with AWS CLI" theme={"system"}
> aws s3api get-bucket-lifecycle-configuration --bucket [BUCKET-NAME]
> ```

> [tab] s3cmd
>
> ```bash title="Get the active lifecycle configuration with s3cmd" theme={"system"}
> s3cmd getlifecycle s3://[BUCKET-NAME]
> ```

> [tab] Boto3
>
> ```python title="Get the active lifecycle configuration with Boto3" theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3 = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> response = s3.get_bucket_lifecycle_configuration(Bucket='[BUCKET-NAME]')
> for rule in response.get('Rules', []):
>     print(rule)
> ```

## Delete a lifecycle configuration

Removing the lifecycle configuration stops all automated lifecycle actions on the bucket. Objects that were already queued for expiration are unscheduled and are not deleted.

> [tab] AWS CLI
>
> ```bash title="Delete the lifecycle configuration with AWS CLI" theme={"system"}
> aws s3api delete-bucket-lifecycle --bucket [BUCKET-NAME]
> ```

> [tab] s3cmd
>
> ```bash title="Delete the lifecycle configuration with s3cmd" theme={"system"}
> s3cmd dellifecycle s3://[BUCKET-NAME]
> ```

> [tab] Boto3
>
> ```python title="Delete the lifecycle configuration with Boto3" theme={"system"}
> import os
> import boto3
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3 = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> s3.delete_bucket_lifecycle(Bucket='[BUCKET-NAME]')
> ```

## Rule field reference

The following fields are available in a lifecycle rule:

| Field | Description |
| - | - |
| `ID` | Identifier for the rule. Up to 255 characters. |
| `Filter` | Selects which objects the rule applies to. Contains a `Prefix`, `Tag`, or `And` clause. An empty filter matches every object in the bucket. |
| `Filter.Prefix` | Object key prefix to match. For example, `foo/` matches both `foo/bar` and `foo/baz`. |
| `Filter.Tag` | A single tag key/value pair to match. |
| `Filter.And` | Combines a prefix, multiple tags, and object size constraints in one filter. |
| `Filter.ObjectSizeGreaterThan` | Minimum object size, in bytes. |
| `Filter.ObjectSizeLessThan` | Maximum object size, in bytes. |
| `Status` | `Enabled` or `Disabled`. Disabled rules do not run. |
| `Expiration` | Deletes the current version of matching objects when they reach a given age (`Days`), on a specific UTC date in ISO 8601 format (`Date`), or when an expired delete marker is present (`ExpiredObjectDeleteMarker`). |
| `Expiration.ExpiredObjectDeleteMarker` | If `true`, removes a delete marker that has no remaining noncurrent versions. Cannot be combined with `Days` or `Date`. |
| `NoncurrentVersionExpiration` | On versioned buckets, deletes noncurrent versions after `NoncurrentDays`. Optionally retains `NewerNoncurrentVersions` of the most recent noncurrent versions. |
| `AbortIncompleteMultipartUpload` | Aborts multipart uploads that have not completed `DaysAfterInitiation` days after they were started. |

## Common questions

**Can I recover objects that were deleted by a lifecycle rule?**

In a non-versioned bucket, no -- expired objects are permanently deleted. In a versioning-enabled bucket, an `Expiration` rule creates a delete marker rather than permanently deleting the object, so you can restore a previous version by copying it back as the current version. Enable versioning before configuring expiration rules if you need recoverability.

**Can I use multiple prefixes in a single rule?**

No. A single lifecycle rule supports only one prefix. To apply the same action to objects under multiple prefixes, either create a separate rule for each prefix, or use object tags to group objects under a tag-based filter.

**Can I exclude a prefix from a lifecycle rule?**

Lifecycle rules do not support exclusion filters. Use object tags to mark the objects you want to include, then create a tag-based rule that targets them rather than trying to exclude objects by prefix.

**Do lifecycle rules apply to objects that already exist in the bucket?**

Yes. When you add or update a lifecycle configuration, rules apply to both existing and newly created objects. Existing objects that already meet the expiration criteria are queued for removal immediately.

**What happens when I update a lifecycle configuration?**

[`PutBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3putbucketlifecycleconfiguration) replaces the entire existing configuration. To add or modify a single rule, retrieve the current configuration first, make your changes, and then put the updated configuration back.

## Related

* [Empty and delete a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/empty-and-delete-bucket.md): Use a lifecycle policy to keep buckets ready for deletion.
* [Abort incomplete multipart uploads](https://docs.coreweave.com/products/storage/object-storage/buckets/abort-multipart-uploads.md): Locate and clean up incomplete multipart uploads before applying a recurring rule.
* [Versioned buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md): Manage versioned buckets and noncurrent versions.
* [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md): Identify and delete objects by last access time, instead of by creation time.
* [Manage AI Object Storage with Terraform](https://docs.coreweave.com/products/storage/object-storage/use-terraform-aws-provider.md): Apply lifecycle configurations as code, including a known issue with `NoncurrentVersionTransitions` in version 0.7.0 of the CoreWeave provider.
* [S3 API compatibility](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#s3-api-compatibility-notes): Reference notes for `PutBucketLifecycleConfiguration`, `GetBucketLifecycleConfiguration`, and `DeleteBucketLifecycle`.
