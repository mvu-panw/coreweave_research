# Distributed File Storage alerts

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/monitoring/alerts

# Distributed File Storage alerts

> Reference for Distributed File Storage cluster quota and per-volume alerts, and how CoreWeave delivers them.

Distributed File Storage (DFS) alerts on two independent capacity problems: a CoreWeave Kubernetes Service (CKS) cluster running out of quota to provision new volumes, and an individual volume running out of free space. This page lists every DFS alert, the condition that triggers it, and how CoreWeave delivers it. Use it to decide which alerts to route to Slack or a webhook, and to interpret an alert you have already received.

The two alert families measure different things and aren't interchangeable:

* **Cluster quota alerts** measure *provisioned* capacity (the total size of the PVCs you have requested) against your cluster quota. A cluster can hit its quota while every volume in it is nearly empty.
* **Per-volume alerts** measure *used* space inside a single volume. A volume can fill up while the cluster has plenty of unprovisioned quota left.

## Cluster quota alerts

The following alerts fire when the provisioned DFS capacity in a CKS cluster approaches that cluster's quota. Provisioned capacity is the sum of bound and in-flight PVC requests. A cluster quota alert fires after its condition holds for 10 minutes, and evaluates per organization, per cluster, and per Availability Zone.

| Alert name | Condition | Severity |
| :- | :- | :- |
| `DFSQuotaProvisioningNearLimit` | Provisioned capacity is at or above 80% of the cluster quota | Warning |
| `DFSQuotaProvisioningLimit` | Provisioned capacity is at or above 95% of the cluster quota | Critical |

When `DFSQuotaProvisioningLimit` is firing for a cluster, it suppresses `DFSQuotaProvisioningNearLimit` for that same cluster and Availability Zone, so one cluster approaching its quota produces one notification rather than two. Multiple clusters approaching their quotas produce separate notifications.

Once provisioned capacity reaches the quota, requests to create or resize a DFS PVC fail instead of over-provisioning the cluster. To act on these alerts, either delete PVCs you no longer need or [request a quota increase](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md#request-a-quota-increase). Because the quota counts provisioned rather than used capacity, deleting data inside a volume doesn't reclaim quota, and you can't [shrink an existing PVC](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-volumes.md) to give capacity back.

## Per-volume alerts

The following alerts fire when an individual DFS volume runs low on free space. A per-volume alert fires after its condition holds for 10 minutes, and evaluates per PVC, identified by organization, cluster, Availability Zone, namespace, and PVC name.

| Alert name | Condition | Severity |
| :- | :- | :- |
| `DFSPVCUsageNearLimit` | The volume has 20% or less free space | Warning |
| `DFSPVCUsageLimit` | The volume has 5% or less free space | Critical |
| `DFSPVCUsageProjectedNearLimit` | The volume is projected to have 20% or less free space within 7 days | Warning |

`DFSPVCUsageProjectedNearLimit` extrapolates a linear growth trend from the previous 6 hours of free space, so a short burst of writes can trigger it even when longer-term growth is flat.

When a more urgent alert is firing for a volume, it suppresses the less urgent ones for that same volume, in this order: `DFSPVCUsageLimit`, then `DFSPVCUsageNearLimit`, then `DFSPVCUsageProjectedNearLimit`. Each volume is evaluated on its own, so several volumes filling up at once produce separate notifications.

To act on these alerts, delete data from the volume or [resize the PVC](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-volumes.md). For bulk deletion on large directories, see [Delete files with VAST trash](https://docs.coreweave.com/products/storage/distributed-file-storage/delete-files.md). Resizing a PVC consumes cluster quota, so confirm the cluster has headroom before you resize.

> [!NOTE]
>
> Per-volume alerts are internal to CoreWeave. They aren't available as notifications on the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page, and you can't route them to a destination of your own. CoreWeave monitors them and might contact you about a volume that's filling up. To get notified yourself, build an equivalent alert or dashboard panel from the expressions in [Build custom alerts and dashboards](#build-custom-alerts-and-dashboards).

## Alert delivery

Cluster quota alerts appear in the Cloud Console, and you can also route them to Slack or a webhook. In-app delivery is enabled by default. To add a destination or change which alerts reach it, see [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md). On the **Alert configuration** page, these alerts are grouped under the **Storage** category.

## Build custom alerts and dashboards

You can query these metrics yourself to monitor thresholds the built-in alerts don't cover.

### Provisioned capacity as a percentage of cluster quota

This is the expression behind the cluster quota alerts:

```promql theme={"system"}
sum by (cluster_org, cluster, zone) (
  pvmo_watcher_bound_pvc_bytes{provisioner=~"csi.vastdata.com|csi.coreweave.com"}
  + pvmo_watcher_inflight_pvc_bytes{provisioner=~"csi.vastdata.com|csi.coreweave.com"}
)
/ on(cluster_org, cluster, zone)
sum by (cluster_org, cluster, zone) (
  pvmo_quota_validation_quota_bytes{
    mode="enabled",
    provisioner=~"csi.vastdata.com|csi.coreweave.com"
  }
)
* 100
```

### Free space per volume

This expression reports the percentage of free space in each DFS volume, which is the value the per-volume alerts compare against their thresholds:

```promql theme={"system"}
max by (cluster_org, cluster, namespace, zone, persistentvolumeclaim) (
  kubelet_volume_stats_available_bytes
  / kubelet_volume_stats_capacity_bytes
)
* 100
```

To alert on a volume the way `DFSPVCUsageNearLimit` does, add `<= 20` to the end of the expression. For the critical threshold, use `<= 5`.

> [!NOTE]
>
> `kubelet_volume_stats_available_bytes` covers every PVC in the cluster, not only DFS volumes. To restrict the result to DFS, join against `kube_persistentvolumeclaim_info` on the DFS storage class your PVCs use, which is `shared-vast` for most clusters. See [Create Distributed File Storage volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md).

### Projected free space per volume

This is the projection behind `DFSPVCUsageProjectedNearLimit`, which extrapolates 7 days ahead from a 6-hour lookback:

```promql theme={"system"}
max by (cluster_org, cluster, namespace, zone, persistentvolumeclaim) (
  predict_linear(kubelet_volume_stats_available_bytes[6h], 7 * 24 * 3600)
  / kubelet_volume_stats_capacity_bytes
)
* 100
```

## Related topics

* [Manage quotas](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md): the cluster quota these alerts measure against, and how to request an increase.
* [Distributed File Storage Usage dashboard](https://docs.coreweave.com/observability/managed-grafana/storage/distributed-storage.md): the built-in Grafana dashboard for DFS usage, capacity, and PVCs.
* [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md): choose destinations for these alerts.
