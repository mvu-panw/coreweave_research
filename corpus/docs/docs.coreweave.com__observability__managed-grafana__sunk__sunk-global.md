# SUNK Global

Source: https://docs.coreweave.com/observability/managed-grafana/sunk/sunk-global

# SUNK Global

> Monitor SUNK infrastructure and resources across all regions and clusters

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The **SUNK Global** dashboard provides a high-level overview of SUNK infrastructure across all regions, cluster organizations, and clusters. It shows alerts, job distribution, software version information, and control plane health metrics.

To open the dashboard, go to the [SUNK Global dashboard](https://cks-grafana.coreweave.com/d/sunk-global/sunk-global).

The following sections describe the filters available at the top of the dashboard and the panels grouped under each section.

## Filters and parameters

Use these filters at the top of the page to choose the data you want to view:

| Field | Value |
| - | - |
| **Data Source** | The Prometheus data source selector. |
| **Region** | The regions to view. Supports multi-select. |
| **Org** | The cluster organizations to view. Supports multi-select. |
| **Cluster** | The specific Kubernetes clusters to view. Supports multi-select. |

Set the time range and refresh rate parameters at the top-right of the page. The default time range is 1 hour.

## Panel descriptions

### SUNK alerts

The **SUNK Alerts** section displays active alerts across all monitored SUNK infrastructure.

| Panel | Description |
| - | - |
| **SUNK Alerts Timeline** | A time-series graph showing when alerts fired. Each line represents an alert grouped by `alertname`, `region`, `cluster_org`, and `cluster`. |
| **SUNK Alerts Table (Instant)** | A table showing all firing SUNK alerts. Includes `alertname`, severity, team, `region`, `cluster_org`, `cluster`, `namespace`, `node`, `nodeset`, and `pod` information. Namespace, node, and pod values link to detailed dashboards. |

![SUNK Alerts section showing timeline and table of firing alerts](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/sunk_alerts.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=f5b6c550337075c2bc874cad5b3db351)

The **SUNK Alerts Table** provides clickable links to drill down into the Slurm Cluster Dashboard view for each alert so you can investigate the context around firing alerts. You can also click node values to view Node Details or pod values to access the Pod Inspector for detailed troubleshooting.

### Slurm jobs

The **Slurm Jobs** section displays running Slurm job distribution.

| Panel | Description |
| - | - |
| **Largest Job by Nodes** | A donut chart showing the top 10 largest running jobs by node count. Click a slice to navigate to the Slurm Job Metrics dashboard. |

### Software versions

The **Software Versions** section displays version distribution across the SUNK infrastructure.

| Panel | Description |
| - | - |
| **SUNK Versions Piechart** | A donut chart showing SUNK version distribution across Syncer containers. |
| **SUNK Versions Table** | A table listing SUNK versions by `region`, `cluster_org`, `cluster`, and `namespace` with node counts. |
| **SUNK Operator Versions** | A donut chart showing SUNK Operator (controller-manager) version distribution. |
| **SUNK Operator Versions Table** | A table listing SUNK Operator (controller-manager) versions by `region`, `cluster_org`, and `cluster` with node counts. |
| **CUDA Versions Piechart** | A donut chart showing CUDA version distribution across `slurmd` containers. |
| **CUDA Versions Table** | A table listing CUDA versions by `region`, `cluster_org`, `cluster`, and `namespace` with node counts. |
| **OS Versions Piechart** | A donut chart showing Ubuntu OS version distribution across SUNK daemon containers. |
| **OS Versions Table** | A table listing OS versions by `region`, `cluster_org`, `cluster`, and `namespace` with node counts. |

![SUNK Versions showing piechart and table of versions across infrastructure](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/sunk_versions.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=b59e1aa443e0aad259ae5227cd518f3a)

The **SUNK Versions** panels show which version each cluster uses across your infrastructure. The piechart shows the distribution at a glance, and the table shows exactly which clusters run each version. Use this to plan and coordinate upgrades.

![CUDA Versions showing distribution across infrastructure](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/cuda_versions.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=606a0c0167f32c0a773e6dbb29097d43)

The **CUDA Versions** panels show CUDA version distribution across all `slurmd` containers. Use these panels to track which CUDA versions your clusters run and to plan upgrades across your infrastructure.

### Control plane health

The **Control Plane Health** section displays SUNK control plane component status.

| Panel | Description |
| - | - |
| **Control Plane Restart Counters** | A time-series graph showing restart count increases for control plane containers (`scheduler`, `slurmctld`, `slurmdbd`, `slurmrestd`, `syncer`, `mysql`) over time. |
| **Control Plane Readiness Status (Instant)** | A table showing the current ready state of control plane pods. Includes Container, Pod, Status (Ready or Not Ready), `region`, `cluster_org`, `cluster`, `namespace`, and a link to view pod logs in Loki. |

![Control Plane Readiness Status table showing pod status across infrastructure](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/control_plane_readiness.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=d3c3f150bdd5c2f14a91353c5cd0d027)

The **Control Plane Readiness Status** table displays the current ready state of all control plane components. You can drill down into individual pods through the Pod Inspector or open Loki logs directly from the table to troubleshoot any control plane components.
