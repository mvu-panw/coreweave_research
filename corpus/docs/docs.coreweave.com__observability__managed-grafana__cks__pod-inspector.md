# Pod Inspector

Source: https://docs.coreweave.com/observability/managed-grafana/cks/pod-inspector

# Pod Inspector

> Grafana dashboard for viewing combined Pod metrics, events, logs, and resource usage in CKS

The Pod Inspector dashboard provides a combined view of common Pod metrics, Kubernetes events, and Pod logs, filtered to a specific Pod or container in any namespace. Use it to investigate the runtime behavior of a single Pod or container when troubleshooting issues such as restarts, resource pressure, or scheduling problems.

To view the dashboard, go to the [Pod Inspector dashboard](https://cks-grafana.coreweave.com/d/G8-j827Mk/pod-inspector).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The following table describes each panel available in the dashboard.

| Panel title | Description |
| - | - |
| **Node History** | Shows the history of the Node's status or events. |
| **Type** | Displays the type of the monitored resource. |
| **Node** | Shows Node information. |
| **Network Throughput** | Shows the network throughput of the Node. |
| **Container Waiting History** | Shows the history of containers in a `Waiting` state. |
| **CPU Percentage Usage** | Shows the CPU utilization as a percentage of the total available. |
| **CGNAT Traffic Classification** | Shows the Carrier-Grade NAT (CGNAT) traffic. |
| **CPU Usage (Cores)** | Displays CPU usage as the number of cores in use. |
| **Memory Percentage Usage** | Shows the memory utilization as a percentage of the total available. |
| **CPU Throttle Rate** | Shows the rate at which the CPU is being throttled. |
| **Memory Usage (RSS)** | Displays the resident set size (RSS) memory usage. |
| **OOM History** | Shows the history of out-of-memory (OOM) events. |
| **InfiniBand Bandwidth on Node (Active)** | Shows the active bandwidth on the Node's InfiniBand network interface. |
| **Container Restarts** | Shows the number of container restarts over time. |
| **GPU Usage** | Shows the utilization of the Node's GPU. |
| **GPU Memory Usage** | Shows the memory usage of the Node's GPU. |
| **Logs** | Displays log entries from the Node or its containers. |
| **Kubernetes Events** | Displays the Kubernetes events related to the monitored resource. |
