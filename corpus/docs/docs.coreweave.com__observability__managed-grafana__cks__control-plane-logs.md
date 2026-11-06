# Control plane logs

Source: https://docs.coreweave.com/observability/managed-grafana/cks/control-plane-logs

# Control plane logs

> Grafana dashboard for viewing Kubernetes control plane component logs in CKS clusters

To view the dashboard, go to the [Control Plane Logs dashboard](https://cks-grafana.coreweave.com/d/cluster-health-logs/control-plane-logs).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Control Plane Logs dashboard shows logs from control plane components, including the API server, etcd, controller manager, and scheduler, to help you monitor their health and status.

The Control Plane Logs dashboard contains the following panels:

| Panel | Description |
| - | - |
| **API Server Error Logs** | Shows error logs from the API server. |
| **etcd Logs** | Shows logs from etcd. |
| **Controller Manager Logs** | Shows logs from the controller manager. |
| **Scheduler Logs** | Shows logs from the scheduler. |
| **Konnectivity Server Logs** | Shows logs from the Konnectivity server. |
