# Distributed File Storage Usage

Source: https://docs.coreweave.com/observability/managed-grafana/storage/distributed-storage

# Distributed File Storage Usage

> Grafana dashboard for monitoring Distributed File Storage usage, capacity, and Persistent Volume Claims

To view the dashboard, go to the [Distributed File Storage Usage dashboard](https://cks-grafana.coreweave.com/d/felwdhehb6ewwa/distributed-file-storage-usage).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Distributed File Storage Usage dashboard provides metrics about storage usage and capacity.

![Distributed file storage dashboard.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/dfs-dashboard.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=13ad7108e7c491c18448572362514999)

The dashboard contains the following panels:

| Panel | Description |
| - | - |
| **Storage Volume Usage** | Displays the total storage volume in use. |
| **Storage Volume Capacity** | Displays the total available storage volume capacity. |
| **Storage Volume Usage vs Capacity (Last 7 days)** | Shows the storage volume usage over the last 7 days. |
| **Number of PVCs by Storage Class** | Shows a breakdown of Persistent Volume Claims (PVCs) by their assigned Storage Class. |
| **Persistent Volume Claims** | Shows Persistent Volume Claims with their size, used space, percentage used, and current status. |
