# Manage quotas and limits

Source: https://docs.coreweave.com/products/storage/object-storage/manage-quotas

# Manage quotas and limits

> Manage quotas and limits for CoreWeave AI Object Storage

CoreWeave AI Object Storage has the following quotas and limits by default.

## Quotas

Object Storage tracks capacity quotas separately for each storage class. The quota for `STANDARD` applies to the Hot, Warm, and Cold tiers combined. The quota for `STANDARD_IA` applies to the Archive tier, if your organization uses this tier.

| Quota | Default value |
| - | - |
| Default `STANDARD` capacity (per Availability Zone, per organization) | 20 TiB |
| Default `STANDARD_IA` capacity (per Availability Zone, per organization) | 0 TiB |
| Default number of buckets per organization | 1,000 |
| Default LOTA cache capacity per Node | 3 TiB |

When usage in a storage class reaches that class's quota, write operations to that storage class are blocked. Enforcement lags actual usage, so writes can continue past the quota (see [Capacity overshoot](#capacity-overshoot)). To reclaim capacity by removing data your workloads no longer access, see [Delete cold objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/delete-cold-objects.md).

To request a quota increase, [contact CoreWeave support](https://coreweave.freshdesk.com/support/login) and include:

* Your organization name and Org ID, found on the [Settings page](https://console.coreweave.com/account/settings).
* The region and zone.
* The storage class (`STANDARD` or `STANDARD_IA`) the request applies to.
* The requested object storage quota (TiB).
* A brief description of the workloads and expected storage growth (Optional). For example, new clusters or changes over the next 30 to 90 days.

## Per-bucket capacity caps

Each bucket's `STANDARD` usage counts toward the organization's shared `STANDARD` quota in its Availability Zone. A per-bucket capacity cap adds a bucket-specific limit. Reaching the bucket cap blocks writes only to that bucket, while reaching the shared quota blocks `STANDARD` writes to all buckets in the zone.

A cap helps prevent one bucket from exhausting the shared quota. It doesn't reserve capacity, increase the shared quota, or require moving or rewriting existing data.

Per-bucket capacity caps have the following prerequisites:

* Changing a cap requires the `cwobject:ConfigureBucketCapacityCap` permission.
* Per-bucket capacity caps are entitlement-gated. Your organization must be entitled before you can configure a cap, and the API rejects requests without the entitlement. To request the entitlement, [contact CoreWeave support](https://coreweave.freshdesk.com/support/login).

### Cap enforcement

The following rules apply while a cap is in place:

* The cap counts `STANDARD` usage and applies only to writes that add `STANDARD` data. It excludes `STANDARD_IA` usage and Archive transitions.
* Writes that would push bucket usage past the cap are rejected once enforcement sees the updated usage. Reads and deletes remain available at the cap, so you can reclaim space.
* Each part of a multipart upload is checked separately, so an upload can fail partway through when the bucket reaches its cap.
* Enforcement uses periodically aggregated and cached usage, so a bucket can overshoot its cap before writes are rejected. See [Capacity overshoot](#capacity-overshoot).
* Lowering a cap below current usage deletes nothing. Further growth is blocked until usage falls, you raise the cap, or you clear it.
* Buckets without a cap are unaffected.

A rejected write returns HTTP `405 Method Not Allowed` with a message similar to the following:

```text title="Example error" theme={"system"}
Bucket capacity cap exceeded for bucket "training-checkpoints" (org a1b2c3d4). Delete objects, increase the bucket capacity cap, or clear it before retrying.
```

### Set or change a cap

Manage caps through the `SetBucketSettings` control-plane API, not the S3-compatible API. Each request needs an [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

1. Save the following as `bucket-settings.json`, replacing `[BUCKET-NAME]` with your bucket and `capacityCapBytes` with the cap in bytes. Zero is a valid cap, which blocks every `STANDARD` write that adds bytes. The maximum accepted value is `9223372036854775807` bytes, just under 8 EiB.

   ```json title="bucket-settings.json" theme={"system"}
   {
     "bucketName": "[BUCKET-NAME]",
     "settings": {
       "capacityCapBytes": "1099511627776"
     }
   }
   ```

2. Submit the request:

   ```bash title="Example request" theme={"system"}
   curl -X PUT https://api.coreweave.com/v1/cwobject/bucket/settings \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
     -d @bucket-settings.json
   ```

   A successful response reports the stored cap in the read-only `configuredCapacityCapBytes` field:

   ```json title="Response status code 200" theme={"system"}
   {
     "settings": {
       "configuredCapacityCapBytes": "1099511627776"
     }
   }
   ```

A new value replaces the existing cap. If you omit `capacityCapBytes` from a settings update, the cap stays unchanged, so you can change other bucket settings without the cap entitlement.

To set a cap with Terraform, use `capacity_cap_bytes` on the [`coreweave_object_storage_bucket_settings`](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs/resources/object_storage_bucket_settings) resource. This attribute requires the CoreWeave Terraform provider v0.25.0 or later.

### View the current cap

Read the cap and the bucket's current usage with `GetBucketInfo`:

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1/cwobject/bucket-info/[BUCKET-NAME] \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```

```json title="Response status code 200" theme={"system"}
{
  "info": {
    "name": "training-checkpoints",
    "settings": {
      "configuredCapacityCapBytes": "1099511627776"
    },
    "usage": [
      {
        "measurementType": "MEASUREMENT_TYPE_USAGE_BYTES",
        "value": "824633720832",
        "valueHumanReadable": "768 GiB"
      }
    ]
  }
}
```

When no cap is configured, the response omits `configuredCapacityCapBytes`. The same field appears in `ListBucketInfo` responses.

### Clear a cap

To remove the bucket-specific limit, send `clearCapacityCap` instead of `capacityCapBytes`. The bucket's `STANDARD` usage still counts toward the organization's shared quota. The two fields are mutually exclusive.

```json title="bucket-settings.json" theme={"system"}
{
  "bucketName": "[BUCKET-NAME]",
  "settings": {
    "clearCapacityCap": {}
  }
}
```

Deleting the bucket also removes its cap.

## Capacity overshoot

Storage-class quotas and per-bucket capacity caps are soft limits. Object Storage enforces them against periodically aggregated usage, not a real-time byte count, so writes can continue after actual usage exceeds the quota or cap. Don't rely on a quota or cap to reject a particular write at an exact capacity boundary.

Usage is aggregated every 5 minutes, so overshoot depends primarily on write throughput during a window of roughly 5 to 10 minutes.

S3 servers also cache each bucket's usage, so per-bucket cap enforcement can lag the usage that `GetBucketInfo` reports. After a period without S3 requests, a new request can be checked against an older cached value while the cache refreshes in the background. S3 requests such as `HeadBucket`, `ListObjectsV2`, and `PutObject` trigger this refresh when the server's cache entry has expired. Polling `GetBucketInfo` doesn't refresh the cache, so updated usage in its response doesn't guarantee that the next upload is checked against that value.

Potential overshoot is approximately the sustained write throughput multiplied by the usage-update delay:

* **Per-bucket cap:** The bucket's sustained write throughput during the roughly 5-to-10-minute aggregation window.
* **Storage-class quota:** The combined write throughput across all buckets in the affected Availability Zone and storage class.

When you choose a bucket cap, leave headroom for potential overshoot based on the bucket's sustained write throughput during that window.

## Limits

The following limits are technical constraints on individual objects and multipart uploads.

| Limit | Default value |
| - | - |
| Maximum part size | 5 GiB |
| Minimum part size<sup>1</sup> | 5 MiB |
| Maximum object size | 48.828125 TiB |
| Maximum parts per multipart upload | 10,000 |
| Lifecycle rules per configuration | 1,000 |

<sup>1</sup> The last object part of a multipart upload can be less than 5 MiB in size.

### Request rate

CoreWeave AI Object Storage does not publish a per-account requests-per-second (RPS) quota. The service is designed to scale with normal S3-style workloads, including parallel reads and writes across many objects. If you plan a workload that will sustain very high request rates (for example, large-scale dataset shuffling, fan-out across thousands of clients, or high-QPS prefix-scale rename or list operations), [contact CoreWeave support](https://coreweave.freshdesk.com/support/login) before you run it so that capacity planning and any applicable rate shaping can be reviewed. For rename-specific guidance at scale, see [Rename objects](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md).

## Storage capacity alerts

Object Storage sends alerts when your usage approaches or is projected to exceed a quota, giving you time to act before write operations are blocked. Alerts fire independently for each storage class quota in each Availability Zone.

For the full list of alerts, their trigger conditions, and the PromQL behind them, see [Object storage alerts](https://docs.coreweave.com/products/storage/object-storage/monitoring/alerts.md).
