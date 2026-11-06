# WEKA

Source: https://docs.coreweave.com/observability/managed-grafana/storage/weka

# WEKA

> Grafana dashboard for monitoring WEKA storage cluster alerts, capacity, protection status, and IOPS

The **WEKA** dashboard provides metrics for WEKA storage clusters. Use this dashboard to monitor cluster health and alerts, capacity, data protection status, IOPS, and per-filesystem performance.

To view the dashboard, go to the [WEKA dashboard](https://cks-grafana.coreweave.com/d/feg6mkz6mg934d/weka).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The following sections describe each panel group on the dashboard.

## Cluster-wide info

These panels summarize the overall state of the cluster, including alerts, capacity, throughput, and IOPS.

| Panel | Description |
| - | - |
| **Alerts Counter** | Displays the total count of active alerts. |
| **Failure domain** | Displays information about the failure domain configuration or status. |
| **Protection (Stripe width + Redundancy level)** | Shows details about the data protection scheme, including stripe width and redundancy level. |
| **Status** | Shows the overall operational status. |
| **Protection Status** | Shows the current data protection status. |
| **Protection Status Over Time** | Shows data protection status. |
| **Containers** | Shows metrics related to running containers, such as their count or state. |
| **Cluster Capacities** | Displays the various capacity metrics of the cluster. |
| **Processes** | Displays metrics about running processes on the cluster Nodes. |
| **Cluster drives** | Displays information or status about the drives in the cluster. |
| **Max Cpu Utilization** | Tracks the maximum CPU utilization across the cluster. |
| **Iops** | Shows the total Input/Output Operations Per Second (IOPS) of the cluster. |
| **Throughput** | Shows the total data throughput of the cluster. |
| **Drive Read/Write Requests/Sec** | Shows the rate of read and write requests per second to the storage drives. |
| **NIC Data rate per container type** | Shows the Network Interface Card (NIC) data rate, categorized by the type of container. |
| **AVG Drive Read/Write Latency** | Shows the average latency for drive read and write operations. |
| **Drive Read/Write Throughput** | Shows the data throughput for drive read and write operations. |

## Per-filesystem info

These panels show read and write latency, request rates, and throughput broken down by filesystem.

| Panel | Description |
| - | - |
| **Average Read Latency by FS** | Shows the average latency of read operations, broken down by individual filesystem (FS). |
| **Average Write Latency by FS** | Shows the average latency of write operations, broken down by individual filesystem (FS). |
| **AVG Read Requests/Sec by FS** | Shows the average number of read requests per second, with data grouped by filesystem (FS). |
| **AVG Write Requests/Sec by FS** | Shows the average number of write requests per second, with data grouped by filesystem (FS). |
| **Read Throughput by FS** | Shows the data read throughput, broken down by filesystem (FS). |
| **Write Throughput by FS** | Shows the data write throughput, broken down by filesystem (FS). |

## Top drives info

These panels surface drive health metrics, including S.M.A.R.T. errors, critical warnings, temperature, and failed or inactive drives.

| Panel | Description |
| - | - |
| **Drive Smart Media Errors** | Shows the count of media-related errors (such as bad sectors) reported by the drive's S.M.A.R.T. (Self-Monitoring, Analysis, and Reporting Technology) system. |
| **Drive Smart Critical Warnings** | Shows any critical warnings issued by the drive's S.M.A.R.T. system, which can be indicators of impending drive failure. |
| **Drive Smart Composite Temp** | Shows the composite temperature of the drives, a key health metric reported by S.M.A.R.T. |
| **Failed / Inactive Drives** | Shows any drives that are currently in a failed state or are otherwise inactive in the system. |

## Top processes info

These panels show per-process network traffic and drive request rates.

| Panel | Description |
| - | - |
| **Network Received** | Displays the amount of incoming network traffic. |
| **Network Transmitted** | Displays the amount of outgoing network traffic. |
| **Drive Read Requests** | Displays the number or rate of read requests being made to the storage drives. |
| **Drive Write Requests** | Displays the number or rate of write requests being made to the storage drives. |
