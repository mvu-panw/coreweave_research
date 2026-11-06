# Cabinet Wrangler

Source: https://docs.coreweave.com/observability/managed-grafana/fleet/cabinet-wrangler

# Cabinet Wrangler

> Grafana dashboard for monitoring cabinet details, GPU data, and Node information across racks

To view the dashboard, go to the [Cabinet Wrangler dashboard](https://cks-grafana.coreweave.com/d/ceif6c5udzytca/cabinet-wrangler).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Cabinet Wrangler dashboard provides an overview of cabinet details and status, including GPU data and Node information across racks.

![Cabinet Wrangler dashboard](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/cabinet-wrangler.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=a518e98cdd00229f095536a4e24999b2)

The dashboard contains the following panels.

| Panel | Description |
| - | - |
| **Any Production GPUs** | Total count of nodes in racks with any number of healthy nodes. |
| **NVL64 Production GPUs** | Baseline count of nodes based on the number of racks with at least 16 healthy nodes (Rack Count \* Threshold (16)). |
| **NVL64+ Production GPUs** | Total count of nodes in racks with at least 16 healthy nodes. |
| **NVL72 Production GPUs** | Total count of nodes in racks with 18 healthy nodes. |
| **NVL64+ Active Production Percentage** | Percentage of active production GPUs of type NVL64 or higher. |
| **Production GPUs** | Distribution of the classes of Production GPUs. |
| **Number of Racks with Production Schedulable Nodes** | Number of racks with schedulable Nodes for production workloads. |
| **Number of Racks with Production Nodes (stacked)** | Stacked chart of the data in the **Number of Racks with Production Nodes** panel. |
| **GPU Utilization (max by `rack_name`)** | Time-series graph of maximum GPU utilization aggregated by rack name. |
| **Cabinet Details** | Detailed table with **Summary** and **NLCC State Counts** tabs. Shows metrics such as rack name, Active status, Health rollup, and Kubernetes schedulable status. |
| **Node Messages** | Messages or logs related to the system's Nodes. |
