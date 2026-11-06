# Control plane metrics

Source: https://docs.coreweave.com/observability/managed-grafana/cks/control-plane-metrics

# Control plane metrics

> Grafana dashboard for monitoring CKS control plane performance across API server, etcd, and scheduler

To view the dashboard, go to the [Control plane metrics dashboard](https://cks-grafana.coreweave.com/d/cluster-health/control-plane-metrics).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Control plane metrics dashboard provides insights into your CKS control planes, with panel groups for the API server, etcd, controller manager, scheduler, and Konnectivity. The following sections describe each panel group.

## API server

The API server panels provide real-time monitoring of your API server's performance and health. The panels show metrics related to request rates, latencies, CPU usage, and memory usage.

![First panels in the API server panel group](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/api-server-panel-group.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=abb2381e160360203d81870909e728d2)

## etcd

The etcd panels show the performance and health of the etcd cluster. The panels show metrics such as put rates, range rates, synchronization durations, CPU usage, and memory usage.

![Panels in the etcd panel group](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/etcd-panel-group.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=d95535ebb029ce905f65129667c8834c)

## Controller manager

The controller manager panels show the performance and resource utilization of the Kubernetes controller manager. The panels display metrics such as request rates and durations, CPU usage, and memory usage.

![Panels in the controller manager panel group](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/control-manager-panel-group.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=402355f2138349280541d1072234f493)

## Scheduler

The scheduler panels show metrics related to request rates, scheduling durations, and resource usage such as CPU and memory.

![Panels in the scheduler panel group](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/scheduler-panel-group.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=ccecafa81efd23b1a1d762a7f7303be5)

## Konnectivity

The Konnectivity panels show metrics related to network connectivity and communication within the cluster, such as the number of established connections, stream packets, dial durations, and CPU and memory usage for connectivity-related components.

![Panels in the Konnectivity panel group](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/konnectivity-panel-group.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=5abebdd74bb632ac73bd71c4034bb702)
