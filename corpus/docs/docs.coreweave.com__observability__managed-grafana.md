# Introduction to CoreWeave Grafana

Source: https://docs.coreweave.com/observability/managed-grafana

# Introduction to CoreWeave Grafana

> Learn about CoreWeave Grafana's preconfigured dashboards and custom dashboards (preview)

CoreWeave Kubernetes Service (CKS) provides a managed Grafana instance with preconfigured dashboards that display the metrics, events, and logs most relevant to your workloads.

With dashboard editing access, you can also create and save [custom dashboards](#custom-dashboards), currently in preview, in your organization's root folder. CoreWeave-provided dashboards remain read-only. For custom alerting, see [Self-hosted Grafana](https://docs.coreweave.com/observability/self-hosted-grafana.md) and [Custom GPU utilization alerts](https://docs.coreweave.com/observability/self-hosted-grafana/custom-alerts.md).

## Where to start

If you're new to CoreWeave Grafana, the following table lists the first dashboards to check for common tasks. For the full catalog, see [Available dashboards](#available-dashboards). To open any dashboard, see [Access CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana/access.md).

| If you want to | Open this dashboard |
| - | - |
| Debug a single Pod or container, including GPU usage, events, and logs | [Pod Inspector](https://docs.coreweave.com/observability/managed-grafana/cks/pod-inspector.md) |
| Check Node and GPU hardware health | [Node Details](https://docs.coreweave.com/observability/managed-grafana/fleet/node-details.md) |
| Review Kubernetes training workload efficiency and active GPUs | [Kubernetes Training Workloads](https://docs.coreweave.com/observability/managed-grafana/kubernetes/training-jobs.md) |
| See Slurm job trends by partition, account, and user | [Slurm Cluster](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-cluster.md) |
| Debug a specific Slurm job | [Slurm Job Metrics](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) |
| Monitor AI Object Storage performance and cache | [CAIOS Usage](https://docs.coreweave.com/observability/managed-grafana/storage/caios-usage.md) and [CAIOS LOTA](https://docs.coreweave.com/observability/managed-grafana/storage/caios-lota.md) |
| Monitor request rate, latency, and scaling for a Dedicated Inference deployment | [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md) |
| Build and save your own view of Pod metrics | [Create a custom dashboard](https://docs.coreweave.com/observability/managed-grafana/custom-dashboards.md) (preview) |

## Available dashboards

CoreWeave provides a suite of preconfigured dashboards, available by default in CoreWeave Grafana. The following sections describe the available dashboard categories.

### CoreWeave

The CoreWeave home dashboard provides an overview of your CoreWeave environment, including announcements, environment-wide metrics, and live service status.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Home | Displays platform announcements, top-level GPU, Pod, and storage metrics, links to key dashboards, and CoreWeave service status. To learn more, read the [Grafana Home documentation](https://docs.coreweave.com/observability/managed-grafana/coreweave/home.md). | [Home dashboard in Grafana](https://cks-grafana.coreweave.com/d/a400d6f5-96a9-4454-9cc8-3b15a746e09e/home) |

### CoreWeave Kubernetes Service (CKS)

CKS dashboards provide insights into Control Plane, Kubernetes, and Pod-level logs and metrics.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Control Plane Logs | Displays logs for Control Plane components, including the API server, etcd, controller manager, and scheduler to monitor their health and status. To learn more, go to [Control Plane Logs](https://docs.coreweave.com/observability/managed-grafana/cks/control-plane-logs.md). | [Control Plane Logs](https://cks-grafana.coreweave.com/d/cluster-health-logs/control-plane-logs) |
| Control Plane Metrics | Provides a detailed view of your cluster's health. To learn more, go to [Control Plane Metrics](https://docs.coreweave.com/observability/managed-grafana/cks/control-plane-metrics.md). | [Control Plane Metrics](https://cks-grafana.coreweave.com/d/cluster-health/control-plane-metrics) |
| Kubernetes Audit Logs | Displays Kubernetes audit logs, showing details of user activities and requests made to the Kubernetes API. To learn more, go to [Kubernetes Audit Logs](https://docs.coreweave.com/observability/managed-grafana/cks/kubernetes-audit-logs.md). | [Kubernetes Audit Logs](https://cks-grafana.coreweave.com/d/k8s-audit-logs/kubernetes-audit-logs) |
| Pod Inspector | Provides a combined view of common Pod metrics, Kubernetes events, and Pod logs, filtered to a specific Pod or container in any namespace. To learn more, go to [Pod Inspector](https://docs.coreweave.com/observability/managed-grafana/cks/pod-inspector.md). | [Pod Inspector](https://cks-grafana.coreweave.com/d/G8-j827Mk/pod-inspector) |

### Dedicated Inference

The Inference Model Overview dashboard provides request, queueing, latency, and scaling metrics for your [Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md) deployments.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Inference Model Overview | Displays request rate and success rate, queueing and load balancing, inference runtime latency, autoscaling, and per-Pod metrics for a deployment. To learn more, go to [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md). | [Inference Model Overview](https://cks-grafana.coreweave.com/d/dep76910f3im8h/inference-model-overview) |

### Fleet management

Fleet management dashboards provide insight into trends in resource consumption, state, and events for the Nodes and Pods in your clusters.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Cabinet Visualizer | Provides statistics and historical information about each cabinet, its cooling system, and the rack it contains. From here you can monitor the overall health of the cabinet and see important details about each Node in the enclosed rack to identify issues and track historical trends. To learn more, go to [Cabinet Visualizer](https://docs.coreweave.com/observability/managed-grafana/fleet/cabinet-visualizer.md). | [Cabinet Visualizer](https://cks-grafana.coreweave.com/d/de3qwk31ucpvkf/cabinet-visualizer) |
| Cabinet Wrangler | Provides an overview of the available GPUs and racks with production-schedulable Nodes. To learn more, go to [Cabinet Wrangler](https://docs.coreweave.com/observability/managed-grafana/fleet/cabinet-wrangler.md). | [Cabinet Wrangler](https://cks-grafana.coreweave.com/d/ceif6c5udzytca/cabinet-wrangler) |
| Node Details | Provides a detailed breakdown of Node and GPU health, both at the physical hardware level and in Kubernetes. This dashboard contains additional log panels to allow simultaneous viewing of metrics along with the log and event types commonly needed to debug or analyze a Node. To learn more, go to [Node Details](https://docs.coreweave.com/observability/managed-grafana/fleet/node-details.md). | [Node Details](https://cks-grafana.coreweave.com/d/ddbdicm9sw7c5x/node-details) |
| Node Wrangler | Provides visibility into the overall health and state of all Nodes in your clusters, along with their specs and hardware architectures. To learn more, go to [Node Wrangler](https://docs.coreweave.com/observability/managed-grafana/fleet/node-wrangler.md). | [Node Wrangler](https://cks-grafana.coreweave.com/d/FWuqvUH4z/node-wrangler) |

### Kubernetes training

Kubernetes dashboards provide detailed information about Kubernetes training workloads and the Kueue scheduling that places them.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Kubernetes Training Workloads | Provides a combined view of a training workload's hardware metrics and placement topology, including Nodes, Pods, job efficiency, and active GPUs. To learn more, go to [Kubernetes Training Workloads](https://docs.coreweave.com/observability/managed-grafana/kubernetes/training-jobs.md). | [Kubernetes Training Workloads](https://cks-grafana.coreweave.com/d/0e4589d5-97fc-4d60-8c5c-301d43f57edd/kubernetes-training-workloads) |
| Kueue Scheduling Dashboard | Displays Kueue scheduling metrics, including admissions, queue status, preemptions, and GPU topology capacity. To learn more, go to [Kueue Scheduling Dashboard](https://docs.coreweave.com/observability/managed-grafana/kubernetes/kueue-metrics.md). | [Kueue Scheduling Dashboard](https://cks-grafana.coreweave.com/d/amwdvqq/kueue-scheduling-dashboard) |

### Network backbone

The network backbone dashboards provide insight into the state of your network, including traffic metrics, connection counts, and latency.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Internet Transit | Provides a near-real-time view into how much traffic flows through your backbone ingress and egress points, how that traffic is distributed across internal services, and how well the network is performing from an end-user perspective. To learn more, go to [Internet Transit](https://docs.coreweave.com/observability/managed-grafana/network-backbone/internet-transit.md). | [Internet Transit](https://cks-grafana.coreweave.com/d/ce3pbkpbkhn9cd/internet-transit) |

### Storage

The storage dashboards provide performance and operational metrics for CoreWeave AI Object Storage, distributed file, VAST, and WEKA storage systems.

| Dashboard | Description | Dashboard link |
| - | - | - |
| CAIOS LOTA | Displays metrics for the CAIOS LOTA storage system, focusing on requests, cache hit rates, and range requests. To learn more, go to [CAIOS LOTA](https://docs.coreweave.com/observability/managed-grafana/storage/caios-lota.md). | [CAIOS LOTA](https://cks-grafana.coreweave.com/d/eeff523hiaewwc/caios-lota) |
| CAIOS Usage | Displays metrics to assist with monitoring and troubleshooting Object Storage performance. To learn more, go to [CAIOS Usage](https://docs.coreweave.com/observability/managed-grafana/storage/caios-usage.md). | [CAIOS Usage](https://cks-grafana.coreweave.com/d/bebi5t788t6v4c/caios-usage) |
| Distributed File Storage Usage | Displays information about distributed file storage usage, including storage volume metrics and persistent volume claims status. To learn more, go to [Distributed File Storage Usage](https://docs.coreweave.com/observability/managed-grafana/storage/distributed-storage.md). | [Distributed File Storage Usage](https://cks-grafana.coreweave.com/d/felwdhehb6ewwa/distributed-file-storage-usage) |
| VAST Actors | Displays metrics related to VAST storage performance, including NFS bandwidth, requests per second, metadata IOPS response time, and Node response times. To learn more, go to [VAST Actors](https://docs.coreweave.com/observability/managed-grafana/storage/vast-actors.md). | [VAST Actors](https://cks-grafana.coreweave.com/d/ddq5gg6gi5lvke/vast-actors) |
| WEKA | Provides information about the WEKA storage system, including cluster-wide info, protection status, cluster capacities, and performance metrics. To learn more, go to [WEKA](https://docs.coreweave.com/observability/managed-grafana/storage/weka.md). | [WEKA](https://cks-grafana.coreweave.com/d/feg6mkz6mg934d/weka) |

### SUNK

The SUNK dashboards provide insight into the state of your Slurm cluster, including job metrics, Node health, and resource consumption.

| Dashboard | Description | Dashboard link |
| - | - | - |
| Slurm Block Topology | Provides an overview of the availability, allocation, and status of compute Nodes, specifically organized by a block topology. To learn more, go to [Slurm Block Topology](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-block-topology.md). | [Slurm Block Topology](https://cks-grafana.coreweave.com/d/6d5afc99-124d-4ab4-9914-fde3bf8c581e/slurm-block-topology) |
| Slurm Cluster | Provides an overview of the state of SUNK jobs within your clusters, with less focus on the specifics of a given job. It aggregates metrics by relevant properties, such as job state, resource type, and user, to illustrate trends in jobs. To learn more, go to [Slurm Cluster](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-cluster.md). | [Slurm Cluster](https://cks-grafana.coreweave.com/d/bX7jn6dZk/slurm-cluster) |
| Slurm Job Metrics | Displays metrics used for debugging and analyzing the performance of specific jobs within your cluster. It provides detailed information about the Nodes running a given job, including alerts and states. To learn more, go to [Slurm Job Metrics](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md). | [Slurm Job Metrics](https://cks-grafana.coreweave.com/d/slurm-job-metrics/slurm-job-metrics) |
| SUNK Global | Provides a high-level overview of SUNK infrastructure across all regions, cluster organizations, and clusters. To learn more, go to [SUNK Global](https://docs.coreweave.com/observability/managed-grafana/sunk/sunk-global.md). | [SUNK Global](https://cks-grafana.coreweave.com/d/sunk-global/sunk-global) |

> [!NOTE]
>
> To access these dashboards in a self-hosted Grafana instance, [install the Helm Chart in the CoreWeave Charts repository](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction.md).

## Custom dashboards

> [!NOTE]
>
> Custom dashboards in CoreWeave Grafana are in preview.

Custom dashboards let you save visualizations of queries against the data sources available in CoreWeave Grafana. Use them to organize the metrics and logs relevant to your workloads in dashboards that other authorized users in your organization can view.

For a step-by-step example, see [Create a custom dashboard](https://docs.coreweave.com/observability/managed-grafana/custom-dashboards.md).

### Organization folders

CoreWeave provides a root folder named after your organization's display name followed by **Dashboards**, for example **\[Example Corp] Dashboards**. All custom dashboards and subfolders belong inside this folder. Users with dashboard editing access can rename the root folder and use subfolders to organize dashboards. Content created by your organization is visible only to authorized users in your organization.

> [!WARNING]
>
> Deleting your organization's root folder deletes all dashboards and subfolders inside it. If this happens, [open a support ticket](https://docs.coreweave.com/support/contact.md) to restore access to custom dashboards.

### Dashboard access

You manage dashboard access through [Identity and Access Management (IAM) access policies](https://docs.coreweave.com/security/iam/access-policies.md) in the Cloud Console.

The **Administrator** and **User** [default access policies](https://docs.coreweave.com/security/iam/access-policies.md#default-access-policies) grant read and write access to your organization's custom dashboards. The **Viewer** default policy grants read access. All three default policies also include **Observability Viewer**.

For custom policies, use the following roles:

| Role | Access |
| - | - |
| Grafana Dashboard Viewer | Read custom dashboards in your organization. |
| Grafana Dashboard Editor | Edit custom dashboards in your organization. |
| Observability Viewer | Access metrics and logs used by dashboards. |

To edit custom dashboards, you need both **Grafana Dashboard Viewer** and **Grafana Dashboard Editor**.

Dashboard permissions and data access are separate. The Grafana Dashboard roles control access to your organization's custom dashboards, not to the metrics and logs that dashboards query. To see data in a dashboard, you also need **Observability Viewer**. The Grafana Dashboard roles don't control access to CoreWeave-provided dashboards.
