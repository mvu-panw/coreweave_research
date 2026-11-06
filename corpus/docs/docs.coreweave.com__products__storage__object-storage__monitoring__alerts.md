# Object storage alerts

Source: https://docs.coreweave.com/products/storage/object-storage/monitoring/alerts

# Object storage alerts

> Reference for CoreWeave AI Object Storage alerts, their trigger conditions, and how they're delivered.

CoreWeave AI Object Storage sends alerts when your stored capacity approaches or is projected to exceed a quota, so that you can act before write operations are blocked. This page lists every customer-facing Object Storage quota alert, the condition that triggers it, and how CoreWeave delivers it. Use it to decide which alerts to route to Slack or a webhook, and to interpret an alert you have already received.

Every alert on this page evaluates per organization, per Availability Zone, and per storage class. If your organization has both a `STANDARD` and a `STANDARD_IA` quota, each quota produces its own alerts, and each Availability Zone produces its own alerts. For the quota values these alerts measure against, see [Manage quotas and limits](https://docs.coreweave.com/products/storage/object-storage/manage-quotas.md).

## Quota alerts

The following alerts fire on capacity usage relative to your storage class quota. A quota alert fires after its condition holds for 5 minutes.

| Alert name | Condition | Severity |
| :- | :- | :- |
| `CAIOSQuotaNearLimit` | Current usage is at or above 90% of quota | Warning |
| `CAIOSQuotaProjectedNearLimit` | Usage is projected to reach 90% of quota within 7 days | Warning |
| `CAIOSQuotaProjectedNearLimit24h` | Usage is projected to reach 90% of quota within 24 hours | Warning |
| `CAIOSQuotaProjectedLimit` | Usage is projected to reach 100% of quota within 7 days | Critical |
| `CAIOSQuotaProjectedLimit24h` | Usage is projected to reach 100% of quota within 24 hours | Critical |

The projection alerts extrapolate a linear growth trend from the previous week of usage. A projection alert can therefore fire while your current usage is still well below the threshold, and it stops firing if your growth rate flattens.

### Overlapping alert suppression

A single growth trend can satisfy several conditions at once. To keep one capacity problem from producing five notifications, CoreWeave suppresses the less urgent alerts in the following order, from most to least urgent:

1. `CAIOSQuotaProjectedLimit24h`
2. `CAIOSQuotaProjectedLimit`
3. `CAIOSQuotaNearLimit`
4. `CAIOSQuotaProjectedNearLimit24h`
5. `CAIOSQuotaProjectedNearLimit`

When an alert in this list is firing, it suppresses every alert lower in the list for the same organization, Availability Zone, and storage class. This order isn't strictly by severity: `CAIOSQuotaNearLimit` is a warning, but because it reports a condition that's already true, it suppresses the two projected-near warnings that follow it.

Suppression applies only within a single organization, Availability Zone, and storage class. Two Availability Zones approaching their quotas at the same time produce two separate notifications.

## Alert delivery

Object Storage alerts appear in the Cloud Console, and you can also route them to Slack or a webhook. In-app delivery is enabled by default. To add a destination or change which alerts reach it, see [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md). On the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page, these alerts are grouped under the **AI Object Storage** category.

## Build custom alerts and dashboards

You can query these metrics yourself to monitor thresholds the built-in alerts don't cover. For example, you can track usage per bucket to find which buckets drive growth in a zone that's approaching its quota.

The following expressions query the `STANDARD` storage class. To query `STANDARD_IA` instead, replace `storage_class="STANDARD"` with `storage_class="STANDARD_IA"` in each expression.

### Current usage as a percentage of quota

This is the expression behind `CAIOSQuotaNearLimit`:

```promql theme={"system"}
label_replace(
  sum(cwobject_bucket_usage{
    measurement_type="MEASUREMENT_TYPE_USAGE_BYTES",
    storage_class="STANDARD"
  }) by (cluster_org, bucket_zone, storage_class),
  "zone", "$1", "bucket_zone", "(.*)"
)
/ on(cluster_org, zone, storage_class)
label_replace(
  cwobject_quota_info{
    active="true",
    measurement_type="MEASUREMENT_TYPE_USAGE_BYTES",
    storage_class="STANDARD"
  },
  "zone", "$1", "quota_zone", "(.*)"
)
* 100
```

### Projected usage as a percentage of quota

This is the expression behind `CAIOSQuotaProjectedNearLimit` and `CAIOSQuotaProjectedLimit`, which project 7 days ahead from a 1-week lookback. To reproduce the 24-hour variants, replace `7 * 24 * 3600` with `24 * 3600`:

```promql theme={"system"}
predict_linear(
  (
    label_replace(
      sum(cwobject_bucket_usage{
        measurement_type="MEASUREMENT_TYPE_USAGE_BYTES",
        storage_class="STANDARD"
      }) by (cluster_org, bucket_zone, storage_class),
      "zone", "$1", "bucket_zone", "(.*)"
    )
  )[1w:],
  7 * 24 * 3600
)
/ on(cluster_org, zone, storage_class)
label_replace(
  cwobject_quota_info{
    active="true",
    measurement_type="MEASUREMENT_TYPE_USAGE_BYTES",
    storage_class="STANDARD"
  },
  "zone", "$1", "quota_zone", "(.*)"
)
* 100
```

### Usage per bucket

Add `bucket_name` to the `by` clause to break usage down by bucket, which identifies the largest buckets in a zone and the buckets responsible for recent growth:

```promql theme={"system"}
sum by (cluster_org, bucket_zone, bucket_name, storage_class) (
  cwobject_bucket_usage{
    measurement_type="MEASUREMENT_TYPE_USAGE_BYTES",
    storage_class="STANDARD"
  }
)
```

> [!NOTE]
>
> Buckets don't have individual quotas. Per-bucket usage shows where capacity is consumed, but the quota these alerts measure against applies to the whole storage class in an Availability Zone.

For a billing-oriented view of the same data, including the `billing:object_storage_used_bytes:total` metric and its labels, see [Cost and usage monitoring](https://docs.coreweave.com/observability/usage-monitoring.md#storage-usage).

## Related topics

* [Manage quotas and limits](https://docs.coreweave.com/products/storage/object-storage/manage-quotas.md): the quota and limit values these alerts measure against, and how to request an increase.
* [CAIOS Usage dashboard](https://docs.coreweave.com/observability/managed-grafana/storage/caios-usage.md): the built-in Grafana dashboard for Object Storage usage and quotas.
* [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md): choose destinations for these alerts.
