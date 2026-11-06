# NodePools and Cluster Autoscaler

Source: https://docs.coreweave.com/observability/managed-grafana/cks/nodepools-and-cluster-autoscaler

# NodePools and Cluster Autoscaler

> Grafana dashboard for monitoring CKS Node Pools, scaling conditions, and Cluster Autoscaler metrics and logs

To view the dashboard, go to the [NodePools and Cluster Autoscaler dashboard](https://cks-grafana.coreweave.com/d/7d7027d7-5f6d-4687-b566-6f8bd001d994/nodepools-and-cluster-autoscaler).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The NodePools and Cluster Autoscaler dashboard gives you a single place to inspect the state of your CKS Node Pools and the [Kubernetes Cluster Autoscaler](https://github.com/kubernetes/autoscaler) that scales them. Use it to review Node Pool capacity and conditions, read Node Pool events, and track autoscaler scaling activity, errors, and logs without querying metrics or logs directly. For background on how autoscaling works and how to configure it, see [Autoscale Node Pools](https://docs.coreweave.com/products/cks/nodes/autoscaling.md).

## Node Pools overview

The **NodePools Overview** table provides a global view of all your Node Pools. It renders the spec fields, status fields, and conditions for each Node Pool in one place. For details about what each column represents, see the [Node Pool reference documentation](https://docs.coreweave.com/products/cks/reference/node-pool.md).

| Column | Description |
| - | - |
| **NodePool** | The name of the Node Pool. |
| **Org ID** | The organization that owns the Node Pool. |
| **Cluster** | The cluster the Node Pool belongs to. |
| **Zone** | The availability zone where the Node Pool runs. |
| **Instance Type** | The instance type provisioned by the Node Pool. |
| **Compute Class** | The compute class assigned to the Node Pool. |
| **Target Nodes** | The number of Nodes the Node Pool is requesting. |
| **Current Nodes** | The number of Nodes present in the cluster for the Node Pool. |
| **Progressing Nodes** | The number of Nodes that have been assigned but have not yet fully booted into the cluster. |
| **Queued Nodes** | The number of queued Nodes waiting to be assigned. |
| **Prefill Nodes** | The number of Nodes in the Node Pool [prefill](https://docs.coreweave.com/products/cks/reference/node-pool.md#node-conditions) flow. |
| **Autoscaling** | Whether autoscaling is enabled on the Node Pool. |
| **Validated** | The [`Validated`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-validated) condition, which reports whether the Node Pool spec passed validation. |
| **AtTarget** | The [`AtTarget`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-attarget) condition, which reports whether the Node Pool has reached its target Node count. |
| **Capacity** | The [`Capacity`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-capacity) condition, which reports whether the zone has capacity to provision the requested Nodes. |
| **Quota** | The [`Quota`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-quota) condition, which reports whether the request is within the organization's quota. |
| **ReconfigRequired** | The [`NodeReconfigurationRequired`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-nodereconfigurationrequired) condition, which reports whether Nodes need to be reconfigured to match the spec. |

## Node Pool events

The **NodePool Events** table renders the events recorded for your Node Pools, such as scaling decisions and quota warnings. Filter the table by [event type](#dashboard-variables) (`Normal` or `Warning`) and event reason to focus on specific activity.

Because events come from exported logs, set the **Log Source** variable to a source that matches the **Region** and **Zone** you have selected. Otherwise, the table cannot render events.

## Cluster autoscaler

The **Cluster Autoscaler** section reports the activity and health of the Cluster Autoscaler. To drill into a single cluster, set the **Org ID** and **Cluster** variables at the top of the dashboard.

### Cluster autoscaler metrics

These panels summarize how the autoscaler is scaling your cluster and how its main loop is performing. The metrics panels use the **Data Source**, **Region**, **Zone**, **Org ID**, and **Cluster** variables.

| Panel | Description |
| - | - |
| **Safe to Autoscale** | Whether the cluster is healthy enough for autoscaling. |
| **Autoscaled NodePools Count** | The number of Node Pools managed by the Cluster Autoscaler. |
| **Autoscale Max Nodes Count** | The maximum number of Nodes aggregated across all autoscaled Node Pools. |
| **Autoscaled Nodes Count** | The number of Nodes in the cluster managed by the autoscaler. |
| **Cluster Autoscaler Duration p95 By Function** | The time taken by various parts of the autoscaler main loop. |
| **Errors** | The number of autoscaler loops that failed due to an error. |
| **Failed Scale Ups** | The number of times a scale-up operation has failed. |
| **Unneeded Nodes** | The number of Nodes currently considered unneeded by the autoscaler. |
| **Scaled Down Nodes** | The number of Nodes removed by the autoscaler. |
| **Unschedulable Pods Count** | The number of unschedulable (`Pending`) Pods in the cluster. |
| **Scaled Up Nodes** | The number of Nodes added by the autoscaler. |

### Cluster autoscaler logs

The **Logs** panel shows exported logs from the Cluster Autoscaler. The logs panel uses the **Log Source**, **Region**, **Zone**, **Org ID**, and **Cluster** variables. As with Node Pool events, set the **Log Source** variable to a source that matches the **Region** and **Zone** you have selected so the logs render correctly.

## Dashboard variables

The variables at the top of the dashboard filter the panels below them. Not every panel uses every variable.

| Variable | Description |
| - | - |
| **Data Source** | The metrics data source for the metric panels. |
| **Log Source** | The log data source for the events and logs panels. Match this to your selected region and zone. |
| **Region** | Filter to a specific region. |
| **Zone** | Filter to a specific availability zone. |
| **Org ID** | Filter to a specific organization. |
| **Cluster** | Filter to a specific cluster. |
| **Instance Type** | Filter to Node Pools of a specific instance type. |
| **Compute Class** | Filter to Node Pools of a specific compute class. |
| **NodePool** | Filter to a specific Node Pool. |
| **Event Type** | Filter Node Pool events by type (`Normal` or `Warning`). |
| **Event Reason** | Filter Node Pool events by reason. |
