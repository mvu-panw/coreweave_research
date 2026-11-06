# Delete cold objects

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects

# Delete cold objects

> Safely identify and delete cold objects using inventory reports, a quarantine buffer, and versioning

This guide describes a pattern for identifying and deleting cold objects in CoreWeave AI Object Storage buckets when the source of truth for that data lives elsewhere, for example in another cloud, a database, or an upstream system. It uses [Inventory Reporting](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting.md), a quarantine buffer window, and [versioning](https://docs.coreweave.com/products/storage/object-storage/buckets/rclone-versioned-buckets.md) to provide layers of defense against accidentally deleting recently accessed objects.

The pattern runs safely against a shared bucket, one that holds a mix of objects still being read and objects that are no longer being read, and deletes only the latter. Every destructive action is scoped to the specific object versions the workflow confirms as cold, so the workflow never affects unrelated objects and their versions.

> [!NOTE]
>
> This guide walks through the workflow one stage at a time. For convenience, the complete, runnable script is available in the [`doc-examples` repository](https://github.com/coreweave/doc-examples/tree/main/storage/delete-cold-objects), which assembles every stage into a [single file](https://github.com/coreweave/doc-examples/blob/main/storage/delete-cold-objects/delete_cold_objects.py) with one subcommand per stage.

## Use case

Use this pattern in the following situations:

* The data is a replica and the source of truth lives elsewhere.
* You want to reduce storage cost or attack surface by removing data your workloads no longer access.
* A bucket contains a mix of active and inactive objects and you want to remove only the inactive ones, leaving active objects untouched.
* You are consolidating from one bucket to another, for example a regional migration, and want to confirm the old bucket is unused before decommissioning.
* A small probability of incorrectly identifying an accessed object as cold is acceptable.

Use a different approach in the following situations:

* You require a hard guarantee that an object hasn't been accessed.
* You have a hard regulatory obligation to delete data by a specific deadline. Use a [lifecycle policy](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md) with expiration rules instead.
* You need auditable proof of deletion timing for compliance, for example regulated right-to-erasure workflows with service-level agreements.
* AI Object Storage is the system of record for the data and reimporting it is impossible or prohibitively expensive.
* Objects must be retained for a fixed period regardless of access.
* You want to keep the data but lower its cost. Move it to the [Archive storage class](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/archive-storage-class.md) instead of deleting it.

## Prerequisites

Before running this workflow, confirm the following:

* **Inventory reports include `LastAccessedDate`.** This field isn't part of every inventory schema by default. You must select it when you [configure the inventory report](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting/configure.md), and it depends on access tracking being active for the bucket. If `LastAccessedDate` is absent, the identification filter silently skips every row and produces an empty candidates list. Verify the field appears in the report's `manifest.json` (`fileSchema`) before relying on the output.
* **The caller has the required permissions.** A bucket access policy grants the action an API call requires, and those names don't always match the call. This workflow requires:

  * `s3:PutBucketVersioning` to enable versioning before deleting.
  * `s3:GetObjectTagging` and `s3:PutObjectTagging` to read and write the quarantine tag.
  * `s3:ListBucket` to list object versions. The `ListObjectVersions` call used by the cleanup and recovery steps maps to this action.
  * `s3:DeleteObject` for the delete step, which writes delete markers without specifying a version ID.
  * `s3:DeleteObjectVersion`, additionally required by the cleanup and recovery steps, which delete specific versions by ID.
  * `s3:GetObject` and `s3:ListBucket` on the inventory destination bucket, to download the inventory report files.

  The bucket-wide lifecycle alternative additionally needs `s3:PutLifecycleConfiguration`.
* **Versioning can be enabled on the bucket.** The delete step enables it if it isn't already on. If your organization restricts versioning, confirm this is permitted before starting.

## Pattern overview

The pattern has four stages:

1. **Identify** candidates from an inventory report using `LastAccessedDate`.
2. **Quarantine** candidates for a buffer window during which any access updates `LastAccessedDate`.
3. **Delete** with versioning enabled, so deletes are recoverable if a mistake is caught after the fact.
4. **Clean up** by permanently removing the recoverable versions and the delete markers, once you're confident the deletions were correct.

The Boto3 examples use environment variables for credentials and the target bucket. Set them before you start:

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
export BUCKET="[BUCKET-NAME]"
```

Alternatively, configure your CoreWeave credentials to work with the AWS CLI.

We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.

> [!TIP]
>
> For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.

> [accordion] Configure CoreWeave credentials with static access keys
>
> 1. Create a `cw` profile:
>
>    ```bash title="Create a new profile" theme={"system"}
>    aws configure --profile cw
>    ```
>
> 2. When prompted, provide the following values:
>
>    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    * **Default output format**: Use `json` for JSON output.
>
> 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>
>    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>
>    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    aws configure set endpoint_url https://cwobject.com --profile cw
>    ```
>
> 4. Set the S3 `addressing_style` to `virtual`:
>
>    ```bash title="Set virtual addressing style" theme={"system"}
>    aws configure set s3.addressing_style virtual --profile cw
>    ```
>
> To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>
> If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.

> [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>
> If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>
> Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>
> ```bash title="Configure WIF OIDC credentials" theme={"system"}
> export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
> export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>
> aws configure set s3.addressing_style virtual
>
> export AWS_REGION="[AVAILABILITY-ZONE]"
> export AWS_ENDPOINT_URL_S3="https://cwobject.com"
> ```
>
> With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>
> Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.

Stages 1 and 2 run in the same process. Stages 3 and 4 typically run later, in separate processes, so each one recreates the client and reloads state from a file. The first code block in each stage sets up a complete, runnable client and reads the same environment variables, so set them again in each new shell before you run that stage. Later snippets within the same stage reuse that client.

## Stage 1: Identify candidates

Generate an [inventory report](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting.md) for the bucket. The report includes a `LastAccessedDate` field that records the most recent time an object was read, as an [RFC 3339](https://www.rfc-editor.org/info/rfc3339/) timestamp in UTC, for example `2026-05-19T22:08:11Z`.

Filter for objects where `LastAccessedDate` is older than your threshold, for example 90 days. Consider only current live objects: skip non-latest versions, delete markers, and any rows with an empty `LastAccessedDate`. The resulting candidates list is consumed by Stage 2.

The examples in this guide assume the inventory file is a plain, uncompressed CSV. AI Object Storage inventory CSVs are headerless. The column schema is set by your inventory configuration and is listed in the report's `manifest.json` (`fileSchema`). The `FIELDS` list in the snippets matches one common configuration. Adjust it to match your schema. If your inventory reports are GZIP-compressed or in another format such as Parquet, decompress or convert them first.

The following snippets open a single local file, `inventory.csv`. Producing that file is a step the examples assume you have already done: read the inventory `manifest.json`, download the one or more data files it references, and concatenate them into the local CSV. See the [Inventory Reporting](https://docs.coreweave.com/products/storage/object-storage/buckets/inventory-reporting.md) guide for the manifest layout and data-file locations.

Set your credentials and the target bucket before running this stage:

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
export BUCKET="[BUCKET-NAME]"
```

```python title="Stage 1: Identify cold candidates from an inventory report" theme={"system"}
import os
import boto3
import csv
import json
from botocore.client import Config
from datetime import datetime, timedelta, timezone

boto_config = Config(
    region_name='US-EAST-04A',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)

bucket_name = os.environ['BUCKET']

# Column order is set by your inventory configuration and listed in
# manifest.json (fileSchema). Adjust if your schema differs.
FIELDS = [
    'Bucket', 'Key', 'VersionId', 'IsLatest', 'IsDeleteMarker', 'Size',
    'LastModifiedDate', 'IsMultipartUploaded', 'EncryptionStatus',
    'StorageClass', 'ChecksumAlgorithm', 'LastAccessedDate', 'ETag',
]

threshold_days = 90
cutoff = datetime.now(timezone.utc) - timedelta(days=threshold_days)

candidates = []
with open('inventory.csv') as f:
    # Inventory CSVs are headerless; provide column names explicitly.
    reader = csv.DictReader(f, fieldnames=FIELDS)
    for row in reader:
        # Only consider current live objects.
        if row['IsLatest'] != 'true' or row['IsDeleteMarker'] == 'true':
            continue
        if not row['LastAccessedDate']:
            continue
        # The "Z" -> "+00:00" replacement makes fromisoformat() work on
        # Python versions before 3.11.
        last_access = datetime.fromisoformat(
            row['LastAccessedDate'].replace('Z', '+00:00')
        )
        if last_access < cutoff:
            candidates.append(row['Key'])
```

## Stage 2: Quarantine

Don't delete candidates immediately. Instead, mark them and hold for a buffer window. This guide uses a tag-based quarantine: apply a tag such as `quarantine_set=YYYY-MM-DD` to each candidate. The approach is lightweight and modifies objects in place. You can use other approaches as well.

The `quarantine_set` tag is advisory. It records that an object is in quarantine and when the buffer window started, which makes the quarantine state visible when you inspect the bucket and lets you reconstruct the candidate set if the persisted state file is lost. The persisted state file, described later in this stage, not the tag, is the source of truth that drives the Stage 3 re-check and cleanup.

`PutObjectTagging` replaces the full tag set on an object. The following example fetches existing tags with `GetObjectTagging` and merges in the quarantine tag before writing the set back, preserving any other tags already on the object. The merge also replaces any prior `quarantine_set` tag, so it's safe to re-run the workflow.

This snippet reuses the `s3` client and `candidates` list from Stage 1.

```python title="Stage 2: Tag candidates for quarantine" theme={"system"}
quarantine_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
quarantine_tag = {'Key': 'quarantine_set', 'Value': quarantine_date}

for key in candidates:
    # Fetch existing tags so you don't overwrite them.
    response = s3.get_object_tagging(Bucket=bucket_name, Key=key)
    existing_tags = response.get('TagSet', [])
    # Drop any prior quarantine_set tag, then append the current one.
    merged_tags = [t for t in existing_tags if t['Key'] != 'quarantine_set']
    merged_tags.append(quarantine_tag)
    s3.put_object_tagging(
        Bucket=bucket_name,
        Key=key,
        Tagging={'TagSet': merged_tags},
    )
```

If your objects don't carry tags, you can skip the `GetObjectTagging` call and write the quarantine tag directly. If you don't need the quarantine state to be visible on the objects themselves, you can skip tagging altogether and rely solely on the persisted state file.

> [!WARNING]
>
> AI Object Storage limits objects to 10 tags. If a candidate is already at the limit, the tagging call fails with a `400 Bad Request` (`Tags cannot be more than 10`). Either remove an existing tag first or use a different quarantine mechanism.

For large candidate lists, parallelize tagging with `concurrent.futures.ThreadPoolExecutor` and tune `max_pool_connections` in the Boto3 `Config`. See [Performance best practices](https://docs.coreweave.com/products/storage/object-storage/improving-performance/best-practices.md) for details.

Leave quarantined objects in place for the buffer window, for example 30 days. Any access during this window updates `LastAccessedDate` and is caught by the re-check at Stage 3.

Persist state between stages. Stage 3 runs after the buffer window has elapsed, typically days or weeks later, so the original Python process has long since exited. Before exiting Stage 2, save the candidate key list and the quarantine date, the value used for the `quarantine_set` tag, to a durable location such as a local JSON file, a database, or object metadata. Stage 3 reloads both values to perform the re-check.

```python title="Stage 2: Persist quarantine state" theme={"system"}
with open('quarantine_state.json', 'w') as f:
    json.dump({'quarantine_date': quarantine_date, 'candidates': candidates}, f)
```

Stages 1 and 2 are now complete. Each candidate object is tagged with the quarantine date and the candidate list is saved to `quarantine_state.json`. Wait for the buffer window to elapse before proceeding to Stage 3.

## Stage 3: Delete

Stage 3 typically runs in a new process after the buffer window has elapsed. Recreate the Boto3 client and re-import the modules used in the following snippets. Set your credentials and the target bucket again in the new shell:

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
export BUCKET="[BUCKET-NAME]"
```

```python title="Stage 3: Set up the client" theme={"system"}
import os
import boto3
import csv
import json
from botocore.client import Config
from datetime import datetime, timezone

boto_config = Config(
    region_name='US-EAST-04A',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)

bucket_name = os.environ['BUCKET']

# Same FIELDS list used in Stage 1. It must match your inventory schema.
FIELDS = [
    'Bucket', 'Key', 'VersionId', 'IsLatest', 'IsDeleteMarker', 'Size',
    'LastModifiedDate', 'IsMultipartUploaded', 'EncryptionStatus',
    'StorageClass', 'ChecksumAlgorithm', 'LastAccessedDate', 'ETag',
]
```

Before you delete, ensure versioning is enabled on the bucket. The call is idempotent, so it's safe to run whether versioning is already on. With versioning enabled, each delete writes a delete marker rather than permanently removing the object, giving you a recovery copy until Stage 4 cleanup runs.

```python title="Stage 3: Enable versioning" theme={"system"}
s3.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={'Status': 'Enabled'},
)
```

Pull a fresh inventory report and re-check `LastAccessedDate` for each quarantined object. Make sure this report was generated after the buffer window closed. Inventory is produced on a schedule and has delivery latency, so a report generated mid-window would re-check against stale access times and could confirm an object that was in fact accessed near the end of the window. Build a `confirmed_candidates` list of keys whose `LastAccessedDate` hasn't advanced past the quarantine start date.

```python title="Stage 3: Re-check access times after the buffer window" theme={"system"}
# Restore state persisted at the end of Stage 2.
with open('quarantine_state.json') as f:
    state = json.load(f)

quarantine_date = state['quarantine_date']  # the YYYY-MM-DD quarantine_set value
candidates = state['candidates']  # the key list from Stage 1

quarantine_start = datetime.strptime(quarantine_date, '%Y-%m-%d').replace(
    tzinfo=timezone.utc
)
quarantined_keys = set(candidates)

confirmed_candidates = []
with open('inventory_fresh.csv') as f:
    reader = csv.DictReader(f, fieldnames=FIELDS)
    for row in reader:
        if row['Key'] not in quarantined_keys:
            continue
        if row['IsLatest'] != 'true' or row['IsDeleteMarker'] == 'true':
            continue
        if not row['LastAccessedDate']:
            continue
        last_access = datetime.fromisoformat(
            row['LastAccessedDate'].replace('Z', '+00:00')
        )
        # If last_access advanced past quarantine_start, the object was
        # accessed during the buffer window, so skip it.
        if last_access < quarantine_start:
            confirmed_candidates.append(row['Key'])
```

The re-check intentionally excludes objects accessed during the buffer window from `confirmed_candidates`. They keep their `quarantine_set` tag, which is harmless, and are never deleted. If you prefer to clear the tag from spared objects, do so here, but it isn't required for correctness.

Now delete the confirmed candidates. With versioning enabled, each delete writes a delete marker on top of the object rather than removing it outright. The version that was current becomes noncurrent and serves as your recovery copy.

```python title="Stage 3: Delete confirmed candidates" theme={"system"}
# delete_objects accepts up to 1000 keys per call. It returns HTTP 200 even
# when individual keys fail, so inspect the Errors list in each response.
errors = []
for i in range(0, len(confirmed_candidates), 1000):
    batch = [{'Key': k} for k in confirmed_candidates[i:i + 1000]]
    resp = s3.delete_objects(Bucket=bucket_name, Delete={'Objects': batch})
    errors.extend(resp.get('Errors', []))

if errors:
    print(f'{len(errors)} delete(s) failed; first error: {errors[0]}')
```

If you later identify a deletion as a mistake, you can restore the object by removing its delete marker. See the [recovery snippet](#optional-recovery-before-cleanup) in Stage 4. Persist `confirmed_candidates` to a durable location before exiting, because Stage 4 needs it.

```python title="Stage 3: Persist the confirmed deletion list" theme={"system"}
with open('confirmed_candidates.json', 'w') as f:
    json.dump(confirmed_candidates, f)
```

## Stage 4: Clean up

After the deletes in Stage 3, each deleted key has two artifacts: the noncurrent version, which is the former live object and your recovery copy, and the delete marker, which is the current version that makes the object appear gone.

This guide removes both explicitly, by version ID, for only the keys this workflow deleted. Targeting specific version IDs of specific keys is the most strongly scoped option available. The cleanup can only ever touch versions of keys in `confirmed_candidates`, and it never relies on a lifecycle rule's filter matching a noncurrent version, a behavior that varies between S3 implementations and can silently do nothing. A simpler bucket-wide lifecycle alternative is described at the end of this section, but it's only safe on a bucket dedicated to this pattern.

The recovery window is operational. Because cleanup is a script you run rather than a timer, the recovery copy survives until you run cleanup. Wait at least your recovery window, for example 30 days, after the Stage 3 delete before running it. Until then, you can undo a mistaken deletion.

### Optional: Recovery before cleanup

To undo a mistaken deletion, remove the current delete marker for the key. The noncurrent recovery copy is promoted back to current. This snippet uses the same Boto3 client setup shown in Stage 3.

```python title="Stage 4: Restore a single mistakenly deleted key" theme={"system"}
# Restore a single mistakenly deleted key by removing its current delete marker.
key = 'path/to/object'

paginator = s3.get_paginator('list_object_versions')
for page in paginator.paginate(Bucket=bucket_name, Prefix=key):
    for marker in page.get('DeleteMarkers', []):
        if marker['Key'] == key and marker['IsLatest']:
            s3.delete_object(
                Bucket=bucket_name, Key=key, VersionId=marker['VersionId']
            )

# Also drop the recovered key from the persisted cleanup list so a later
# re-deletion can't make cleanup purge it again. Cleanup already skips keys
# whose current version is a live object, but removing it here makes the
# recovery permanent regardless of what happens to the key before cleanup runs.
with open('confirmed_candidates.json') as f:
    confirmed_candidates = json.load(f)

confirmed_candidates = [k for k in confirmed_candidates if k != key]

with open('confirmed_candidates.json', 'w') as f:
    json.dump(confirmed_candidates, f)
```

To recover several keys at once, don't run the single-key snippet in parallel processes. Each one rewrites `confirmed_candidates.json`, so concurrent runs would overwrite each other's changes (last write wins) and leave some recovered keys still in the list. Instead, recover the whole set in one pass: remove every delete marker, then filter the state file once.

```python title="Stage 4: Restore several mistakenly deleted keys" theme={"system"}
# Batch recovery: restore several mistakenly deleted keys at once.
keys_to_recover = {'path/to/object', 'another/object'}

paginator = s3.get_paginator('list_object_versions')
markers_to_remove = []
for page in paginator.paginate(Bucket=bucket_name):
    for marker in page.get('DeleteMarkers', []):
        if marker['Key'] in keys_to_recover and marker['IsLatest']:
            markers_to_remove.append(
                {'Key': marker['Key'], 'VersionId': marker['VersionId']}
            )

# delete_objects accepts up to 1000 versioned entries per call. Removing each
# current delete marker promotes that key's recovery copy back to current.
# A 200 response can still report per-entry failures, so inspect Errors.
errors = []
for i in range(0, len(markers_to_remove), 1000):
    resp = s3.delete_objects(
        Bucket=bucket_name, Delete={'Objects': markers_to_remove[i:i + 1000]}
    )
    errors.extend(resp.get('Errors', []))

failed_keys = {e['Key'] for e in errors}
if failed_keys:
    print(f'{len(failed_keys)} key(s) could not be recovered; first error: {errors[0]}')

# Drop only the successfully recovered keys from the persisted cleanup list, so
# a key whose marker removal failed stays in the list and is retried or cleaned up.
recovered = keys_to_recover - failed_keys
with open('confirmed_candidates.json') as f:
    confirmed_candidates = json.load(f)

confirmed_candidates = [k for k in confirmed_candidates if k not in recovered]

with open('confirmed_candidates.json', 'w') as f:
    json.dump(confirmed_candidates, f)
```

For a small recovery set relative to bucket size, list per key with `Prefix=key` instead of scanning the whole bucket, the same tradeoff noted for the cleanup step.

### Cleanup after the recovery window

Permanently delete the recovery copies and the delete markers for the confirmed keys. The code purges a key only if its current version is still a delete marker, that is, the object is still in the deleted state. If a key was restored with the recovery snippet shown earlier, or re-created by a workload after Stage 3, its current version is a live object, and the key is skipped so the live data is never touched.

Cleanup typically runs in a new process after the recovery window has elapsed. Set your credentials and the target bucket again in the new shell:

```bash theme={"system"}
export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
export BUCKET="[BUCKET-NAME]"
```

```python title="Stage 4: Permanently remove versions and delete markers" theme={"system"}
import os
import boto3
import json
from collections import defaultdict
from botocore.client import Config

boto_config = Config(
    region_name='US-EAST-04A',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client(
    's3',
    endpoint_url='https://cwobject.com',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
    config=boto_config
)

bucket_name = os.environ['BUCKET']

# Reload the keys this workflow deleted (persisted at the end of Stage 3).
with open('confirmed_candidates.json') as f:
    confirmed_candidates = set(json.load(f))

paginator = s3.get_paginator('list_object_versions')
versions_by_key = defaultdict(list)  # key -> [{"Key", "VersionId"}, ...]
current_is_delete_marker = {}  # key -> True if the current version is a marker

# A full-bucket listing is simplest. If confirmed_candidates is small relative
# to the bucket, listing per key with Prefix=key is cheaper. Loop the keys and
# paginate with Prefix set to each one instead of scanning the whole bucket.
for page in paginator.paginate(Bucket=bucket_name):
    for v in page.get('Versions', []):
        if v['Key'] in confirmed_candidates:
            versions_by_key[v['Key']].append(
                {'Key': v['Key'], 'VersionId': v['VersionId']}
            )
            if v['IsLatest']:
                current_is_delete_marker[v['Key']] = False
    for m in page.get('DeleteMarkers', []):
        if m['Key'] in confirmed_candidates:
            versions_by_key[m['Key']].append(
                {'Key': m['Key'], 'VersionId': m['VersionId']}
            )
            if m['IsLatest']:
                current_is_delete_marker[m['Key']] = True

# Purge only keys whose current version is still a delete marker.
to_delete = []
skipped = []
for key in confirmed_candidates:
    if current_is_delete_marker.get(key) is True:
        to_delete.extend(versions_by_key[key])  # noncurrent versions + the marker
    else:
        skipped.append(key)  # restored or re-created since Stage 3, leave it alone

# delete_objects accepts up to 1000 versioned entries per call. It returns
# HTTP 200 even when individual versions fail. Inspect Errors and re-run
# cleanup to retry, since it only purges keys still in a deleted state.
errors = []
for i in range(0, len(to_delete), 1000):
    resp = s3.delete_objects(Bucket=bucket_name, Delete={'Objects': to_delete[i:i + 1000]})
    errors.extend(resp.get('Errors', []))

if errors:
    print(f'{len(errors)} version(s) failed to delete; first error: {errors[0]}')
if skipped:
    print(f'Skipped {len(skipped)} key(s) no longer in a deleted state.')
```

Deleting by version ID removes only the listed versions, so no unrelated object is affected. Because the loop deletes every version of a still-deleted key in one pass, both the recovery copy and the delete marker, the key is fully removed with no expired delete marker left behind, and no ordering hazard arises from promoting a recovery copy back to current.

### Bucket-wide lifecycle policy

If the bucket is dedicated to this pattern, meaning it holds no versioned data from any other source, you can let a [lifecycle policy](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md) do the cleanup instead of running the explicit code shown earlier. Apply a policy with two rules: one to expire noncurrent versions after your recovery window, and one to remove the resulting expired delete markers.

```python title="Stage 4 alternative: bucket-wide lifecycle cleanup" theme={"system"}
s3.put_bucket_lifecycle_configuration(
    Bucket=bucket_name,
    LifecycleConfiguration={
        'Rules': [
            {
                'ID': 'CleanupNoncurrentVersions',
                'Status': 'Enabled',
                'Filter': {},
                'NoncurrentVersionExpiration': {'NoncurrentDays': 30},
            },
            {
                'ID': 'CleanupDeleteMarkers',
                'Status': 'Enabled',
                'Filter': {},
                'Expiration': {'ExpiredObjectDeleteMarker': True},
            },
        ]
    }
)
```

> [!WARNING]
>
> Both rules use an empty filter and therefore apply bucket-wide. `NoncurrentVersionExpiration` doesn't act on current live objects, so active objects are never deleted, but it expires noncurrent versions created by unrelated overwrites elsewhere in the bucket. `ExpiredObjectDeleteMarker` can't be combined with a tag filter, so it can't be scoped to the `quarantine_set` tag either. A prefix filter is allowed, but it doesn't limit the rule to the keys this workflow deleted. For a shared bucket with active writes, the case this guide targets, these rules are too broad and the explicit, key-scoped cleanup described earlier is the correct choice. Use the lifecycle policy only when the entire bucket is yours to clean up.

## Accuracy and caveats

The following section describes the limitations and safety properties of this pattern.

`LastAccessedDate` is approximate and without guarantees: it comes from access log delivery, which has a small probability of dropped events.

The buffer window, not the `LastAccessedDate` field itself, is what gives this pattern its safety margin. The longer the window, the lower the residual risk of deleting an object that was actually accessed. A 30-day buffer is a reasonable default. Workloads where re-access is rarer but more consequential should use longer windows.

Versioning provides a final safety net. Even if a deletion is incorrect, you can recover the object by removing its delete marker, but only until you run the cleanup step, which permanently removes the recovery copy. Because cleanup is a script you run rather than a lifecycle timer, you control the recovery window directly. Wait at least as long as your workload requires before running it.

Scoping in a shared bucket. Every destructive action in this workflow is scoped to the specific keys confirmed as cold. The Stage 3 delete operates on `confirmed_candidates`, and the cleanup deletes only specific version IDs belonging to those keys, and only when the key is still in a deleted state. Actively read objects, versions created by overwrites of unrelated objects, and objects restored or re-created after Stage 3 are never affected. The one exception is the optional bucket-wide lifecycle alternative, which is not key-scoped.
