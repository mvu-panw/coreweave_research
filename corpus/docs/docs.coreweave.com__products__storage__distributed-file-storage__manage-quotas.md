# Manage quotas

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas

# Manage quotas

> Manage Distributed File Storage quotas per CKS cluster, including limits, monitoring, and increase requests.

Distributed File Storage (DFS) enforces a storage quota per CoreWeave Kubernetes Service (CKS) cluster, which sets an upper limit on the total provisioned size of DFS-backed PersistentVolumeClaims (PVCs) in that cluster. This page explains how DFS quotas work, how to monitor your usage, and how to request a quota increase. Use this information to plan capacity and avoid blocked PVC creation.

## Default quota

By default, each CKS cluster has a maximum DFS quota of 10 TiB. This is the total provisioned capacity across all DFS PVCs in that cluster.

| Quota | Default value |
| - | - |
| Maximum capacity (per CKS cluster) | 10 TiB |

You can monitor your DFS storage usage and quotas per cluster in the [DFS Usage dashboard](https://cks-grafana.coreweave.com/d/dfs-usage-dashboard/dfs-usage) in Grafana.

## How quotas affect PVCs

You can create and resize DFS-backed PVCs as long as the sum of provisioned DFS capacity in a cluster remains within that cluster's quota. If a request to create or resize a PVC would exceed the quota, the request fails with an error instead of over-provisioning the cluster.

## Request a quota increase

If your workloads require more storage than your current quota allows, contact CoreWeave support to request an increase before DFS blocks PVC creation.

To request a quota increase, [contact CoreWeave support](https://coreweave.freshdesk.com/support/login) and include:

* Your organization name and Org ID, found in the [Settings page](https://console.coreweave.com/account/settings).
* The region and zone.
* The affected CKS cluster names.
* The requested DFS quota (TiB) for each cluster.
* Optional: a brief description of the workloads and expected storage growth (for example, new clusters or changes over the next 30 to 90 days).

## Storage capacity alerts

DFS sends alerts when the provisioned storage in a cluster approaches that cluster's quota, giving you time to act before DFS blocks PVC creation. A separate set of alerts covers individual volumes running out of free space.

For the full list of alerts, their trigger conditions, and the PromQL behind them, see [Distributed File Storage alerts](https://docs.coreweave.com/products/storage/distributed-file-storage/monitoring/alerts.md).
