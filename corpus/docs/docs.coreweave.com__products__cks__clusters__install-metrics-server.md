# Install metrics-server

Source: https://docs.coreweave.com/products/cks/clusters/install-metrics-server

# Install metrics-server

> Install metrics-server for kubectl top and Horizontal Pod Autoscaler on CKS

> [!NOTE]
>
> **CKS and the metrics-server**
>
> * CKS clusters created after July 7, 2025 do not include [metrics-server](https://github.com/kubernetes-sigs/metrics-server); if your workloads need it, install it yourself as described on this page.
> * Clusters created before July 7, 2025 include a CoreWeave-managed metrics-server in the `kube-system` namespace, so you don't need to install your own. See the [July 7, 2025 release notes](https://docs.coreweave.com/release-notes/control-plane-node-pools.md) for details about this change.

Metrics-server is not required for core cluster functionality. It serves the Kubernetes Metrics API, which powers `kubectl top node` and `kubectl top pod` and provides real-time metrics to the [Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

Metrics-server only affects `kubectl top` and HPA. Metrics shown in CoreWeave Grafana are collected through a separate pipeline and don't depend on metrics-server. To collect custom application metrics, see [Forward application metrics](https://docs.coreweave.com/observability/logs-metrics/forward-metrics.md).

## Prerequisites

Before you begin, make sure you have:

* At least one [CPU Node](https://docs.coreweave.com/platform/instances/cpu-instances.md) in your cluster to run the metrics-server Pods.
* `kubectl` access to your CKS cluster with permission to create resources in the `kube-system` namespace. See [Obtain access with a kubeconfig file](https://docs.coreweave.com/products/cks/auth-access/managed-auth/kubeconfig.md).
* [Helm](https://helm.sh/docs/intro/install/) version 3 or later installed on your workstation.

## Install metrics-server

**1. Install the chart**

Install the upstream metrics-server Helm chart into the `kube-system` namespace:

```bash theme={"system"}
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update
helm upgrade --install metrics-server metrics-server/metrics-server \
  --namespace kube-system
```

Confirm the Deployment is ready:

```bash theme={"system"}
kubectl get deployment metrics-server --namespace kube-system
```

You should see `1/1` in the `READY` column:

```text title="Example output" theme={"system"}
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
metrics-server   1/1     1            1           60s
```

**2. Verify the Metrics API**

Query Node metrics:

```bash theme={"system"}
kubectl top nodes
```

If metrics-server is working correctly, the command returns CPU and memory usage for each Node:

```text title="Example output" theme={"system"}
NAME      CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
g123ab4   512m         1%       12480Mi         9%
g567cd8   4210m        3%       98304Mi         14%
```

Metrics can take a minute or two to appear after installation.
