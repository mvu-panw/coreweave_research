# Autoscale Node Pools

Source: https://docs.coreweave.com/products/cks/nodes/autoscaling

# Autoscale Node Pools

> Scale Node Pools based on workload resource utilization

CKS supports scaling Node Pools by using the [Kubernetes Cluster Autoscaler](https://github.com/kubernetes/autoscaler), letting you scale CKS Node Pools in response to workload demands for GPU, CPU, or memory resources. This page explains how to configure Node Pool autoscaling, describes the underlying scale-up and scale-down behavior, and covers monitoring and troubleshooting so you can match capacity to your workload demand.

Cluster Autoscaler is available in all CKS clusters running Kubernetes 1.32 or later. To upgrade your clusters to the latest version, see [Upgrade Kubernetes](https://docs.coreweave.com/products/cks/clusters/upgrade-kubernetes.md).

## Autoscaling limitations

Review these limitations before enabling autoscaling:

| Feature | Limitation |
| - | - |
| SUNK | SUNK doesn't support Node Pool autoscaling. A NodeSet creates `slurmd` Pods only for Nodes that already exist, so it never triggers a scale-up. See [Node Pool autoscaling](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md#node-pool-autoscaling). |
| Rack-based instances | CKS rejects `autoscaling: true` for rack-based instance types, such as GB200 and GB300. |
| [Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) | CKS doesn't start new prefill operations on Node Pools with autoscaling enabled. Prefill operations already in progress continue. |
| `CWActive` condition | The autoscaler uses its own utilization checks, so it can mark an underutilized Node for removal while the Node is still active. See [Node utilization](#node-utilization). |

If you have questions about autoscaling, or need help making adjustments to an autoscaler's settings, [contact Support](https://docs.coreweave.com/support.md).

## Autoscaling behavior

The following table summarizes the scale-up and scale-down behavior and its billing implications:

| Behavior | Scale up | Scale down |
| - | - | - |
| **Time** | 5 to 15 minutes depending on the instance type. Scale-up time is generally independent of the number of Nodes added in a single operation. Time can vary, however, based on resource availability and the size of the increase. | Scale-down follows the autoscaler's utilization and eviction rules and can remove a Node that still runs workloads. See [Node utilization](#node-utilization). |
| **Job scheduling** | Pods schedule onto the new Nodes once they join the cluster. | |
| **Billing** | You are not charged for Nodes while they scale up. | You are not charged for Nodes after you remove all jobs and CoreWeave reclaims the Node. |

## Node Pool autoscaling compared to Pod autoscaling

This page covers **Node Pool autoscaling**, which adjusts the number of Nodes in a CKS Node Pool. It does not configure Pod-level autoscaling. The two scale at different layers and are commonly used together:

| Scaler | What it scales | Where it runs | How to configure |
| - | - | - | - |
| **Cluster Autoscaler** (Node Pool autoscaling) | Number of Nodes in a Node Pool | Managed by CoreWeave on the CKS control plane | Set `autoscaling: true`, `minNodes`, and `maxNodes` on the [Node Pool](https://docs.coreweave.com/products/cks/reference/node-pool.md) manifest (see below) |
| **Horizontal Pod Autoscaler (HPA)** | Number of Pod replicas in a Deployment, StatefulSet, or ReplicaSet | Standard Kubernetes controller in your CKS cluster | Apply a standard [`HorizontalPodAutoscaler`](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) resource that targets your workload |
| **Vertical Pod Autoscaler (VPA)** | CPU and memory requests on existing Pods | User-installed in your CKS cluster | Install and configure upstream [VPA](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) yourself |

A typical pattern is to combine HPA and Cluster Autoscaler: HPA adds Pod replicas in response to load, and once Pods are unschedulable due to insufficient capacity, Cluster Autoscaler adds Nodes to the Node Pool. Note that Node Pool scale-up takes 5 to 15 minutes on bare metal, so size HPA targets and Node Pool `minNodes` to absorb fast traffic spikes without waiting for new Nodes.

For Dedicated Inference deployments, replica-level autoscaling is managed by the Inference service rather than HPA. See [Scaling and capacity claims](https://docs.coreweave.com/products/inference/scaling.md).

## Configure autoscaling

The autoscaler adjusts the Node Pool's `targetNodes` value within the min and max range that you define in the Node Pool manifest.

To enable autoscaling, set the following values:

* `autoscaling`: Set autoscaling to `true`.
* `maxNodes`: Set the number of maximum Nodes you want to scale up to.
* `minNodes`: Set the number of minimum Nodes you want to scale down to.

The following example Node Pool manifest sets these values:

* `autoscaling`: Set autoscaling to `true`.
* `maxNodes`: Set to `4`.
* `minNodes`: Set to `2`.

```yaml theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  autoscaling: true # Set autoscaling to true
  instanceType: gd-8xh100ib-i128  # Select your desired instance type
  maxNodes: 4 # Set desired maximum nodes.
  minNodes: 2 # Set desired minimum nodes
  targetNodes: 2
  nodeLabels:
    my-label/node: "true"
  nodeAnnotations:
    my-annotation/node: "true"
  nodeTaints:
    - key: node-taint
      value: "true"
      effect: NoSchedule
```

## Autoscaling behavior

Autoscaling increases or decreases the number of Nodes in a Node Pool when the following occurs:

* **Scale up**: When CKS cannot schedule Pods due to insufficient resources, like CPU or memory, CKS scales up the Node Pools. For more information, see [How does up-scale work?](https://github.com/kubernetes/autoscaler/blob/2289138bd92dd56a686109994217e8cee4180142/cluster-autoscaler/FAQ.md#how-does-scale-up-work) in the Kubernetes documentation.
* **Scale down**: When CKS determines that Nodes are underutilized for a configured period, CKS scales down the Node Pools. For more information, see [How does scale-down work?](https://github.com/kubernetes/autoscaler/blob/2289138bd92dd56a686109994217e8cee4180142/cluster-autoscaler/FAQ.md#how-does-scale-down-work) in the Kubernetes documentation.

### Provisioning requests

ProvisioningRequest lets you request capacity for groups of Pods through the Cluster Autoscaler. ProvisioningRequest support is enabled by default on all CKS clusters. CoreWeave installs the `provisioningrequests.autoscaling.x-k8s.io` custom resource definition (CRD). You don't need to install the CRD or enable request processing yourself.

To let the Cluster Autoscaler adjust a Node Pool's size, [configure autoscaling](#configure-autoscaling) on that Node Pool with `autoscaling: true`, `minNodes`, and `maxNodes`. Scaling remains subject to [available quota and capacity](#autoscaling-considerations).

### Node utilization

The autoscaler marks a Node as *unneeded* when the Pods running on it request less than 50% (the default threshold) of the Node's allocatable CPU or GPU or memory. The autoscaler calculates Node utilization using `max(cpu_or_gpu_requests, memory_requests)`. The Node must stay below the threshold for the entire duration of the scale-down window (10 minutes by default) before the autoscaler marks it for removal.

#### Prevent Pod eviction or Node removal

The autoscaler doesn't currently support monitoring the `CWActive` condition on Nodes. As a result, the autoscaler can determine a Node is underutilized and mark for removal even while it's still active. To prevent this, use one of the following annotations:

* **To prevent Pod eviction**: Annotate the Pod with `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`.
* **To prevent Node removal**: Annotate the Node with `cluster-autoscaler.kubernetes.io/scale-down-disabled: "true"`.

## Node selectors and autoscaling

Cluster Autoscaler can scale the appropriate Node Pool when a Pod cannot be scheduled due to resource limits. CKS decides which Node Pool to scale based on the placement requirements defined in the Pod specification, for example, in the `nodeSelector` or `affinity` fields. These fields help the autoscaler choose a Node Pool that matches the Pod's requirements. If you don't specify Pod placement requirements, the autoscaler may scale any available Node Pool.

## Autoscaling considerations

For autoscaling to work, the following criteria must be met:

* **Available quota**: You must have the available quota amount that meets or exceeds the number specified in the `maxNodes` field. For example, if you have `maxNodes` set to 10, you must have that quota available in your organization. To check your organization's quota, see the [`quota` reference documentation](https://docs.coreweave.com/products/cks/reference/node-pool#condition-quota).

* **Available capacity**: The region where your cluster exists must have the capacity to provision the Nodes. For example, if the region your cluster is in doesn't have the capacity to provision Nodes, CKS can't scale your Node Pools. To determine your organization's capacity, see the [`capacity` reference documentation](https://docs.coreweave.com/products/cks/reference/node-pool#condition-capacity).

## Scale-to-zero

The scale-to-zero feature is useful when you want to minimize resource costs by letting a Node Pool drop to zero Nodes when there's no demand.

To scale a Node Pool to zero, set `minNodes` to `0` and `maxNodes` to a value greater than `0` on that Node Pool. This setting lets the Node Pool scale down to zero Nodes when there's no demand.

## Cluster autoscaler monitoring

To monitor autoscaling without querying metrics or logs directly, use the [NodePools and Cluster Autoscaler dashboard](https://docs.coreweave.com/observability/managed-grafana/cks/nodepools-and-cluster-autoscaler.md) in CoreWeave Grafana. The dashboard provides prebuilt panels for Node Pool capacity and conditions, Node Pool events, and Cluster Autoscaler scaling activity, errors, and logs. Filter the panels by region, zone, organization, cluster, and Node Pool to focus on the resources you care about.

If you want to query the underlying logs and metrics yourself, use the **Explore** view in CoreWeave Grafana as described in the following sections.

### Query autoscaler logs and metrics directly

To view logs in [CoreWeave Grafana](https://cks-grafana.coreweave.com/), navigate to **Explore** and use **CoreWeave Logs** for logs:

![Left sidebar showing the Explore menu](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/explore.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=b03ce70854997b56d73a69d97d270c63)

![Left sidebar showing the Loki menu](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/loki.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=ca70c0ec5a2a3132cc62ce8a5f01a025)

You can search for the string `app="cluster-autoscaler"`:

![Grafana Explorer search for autoscaling logs](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/products/cks/_media/auto-scale.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=7d8da3681c4ef31cd0c5aeafe3f8b7c9)

To view metrics in [CoreWeave Grafana](https://cks-grafana.coreweave.com/), navigate to **Explore** and use **CoreWeave Metrics**.

All the metrics are prefixed with `cluster_autoscaler_`. For more information, see the [Kubernetes Cluster Autoscaler Monitoring documentation](https://github.com/kubernetes/autoscaler/blob/a9cb59fdd2dd888529af74929313f3f55c73e7c9/cluster-autoscaler/proposals/metrics.md). To find autoscaling metrics, navigate to **CoreWeave Metrics** and search `cluster_autoscaler`:

![Grafana Explorer for searching autoscaling metrics](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/products/cks/_media/autoscale-metrics.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=0006aa191f3889c892fb3ba02192ec58)

## Test autoscaling

You can test your autoscaling configuration using the following workload. The workload requires all eight GPUs on four Nodes, so if you run it on a Node Pool with fewer than four Nodes available, Cluster Autoscaler adds the correct number of instances to accommodate the workload.

The workload uses the `nodeSelector` field to specify the required instance to schedule. When a cluster has multiple Node Pools, the `nodeSelector` field lets the cluster know which Node Pool to scale.

```yaml theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: nvidia-l40-gpu-job
spec:
  parallelism: 4
  completions: 4
  template:
    metadata:
      labels:
        app: nvidia-l40-gpu
        gpu.nvidia.com/class: L40
        gpu.nvidia.com/model: L40
        gpu.nvidia.com/vram: "46"
    spec:
      restartPolicy: Never
      containers:
        - name: gpu-app
          image: nvidia/cuda:12.3.0-devel-ubuntu22.04
          command: ["/bin/bash", "-c"]
          args:
            - |
              apt-get update && apt-get install -y build-essential cmake make git && \
              git clone https://github.com/NVIDIA/cuda-samples.git && \
              cd cuda-samples && mkdir build && cd build && \
              cmake .. -DCMAKE_CUDA_ARCHITECTURES=89 && \
              echo "start here" make && ls -la  && \
              cd Samples/1_Utilities/deviceQuery && \
              make && ./deviceQuery && sleep 6000
          resources:
            limits:
              nvidia.com/gpu: 8
      nodeSelector:
        gpu.nvidia.com/class: L40
        gpu.nvidia.com/model: L40
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
```

### Troubleshoot autoscaling behavior

To diagnose a Node Pool that doesn't reach the autoscaler's target, start with the pool's status fields, conditions, and events. See [Diagnose a Node Pool that isn't at target](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md#diagnose-a-node-pool-that-is-not-at-target). The following table covers problems specific to the autoscaler itself.

| Problem | Potential issue | Suggested fix |
| - | - | - |
| Nodes don't scale up. | **Node Pool created with `minNodes:0`**. When you create a Node Pool with `minNodes: 0`, the pool initially has no Nodes. The autoscaler requires at least one Node (`targetNodes: 1`) so it can cache the "shape" (resource characteristics) of the Node. This cache is necessary for the autoscaler to determine if it can schedule Pods onto the Node Pool in the future. **CKS removes a Node, causing the autoscaler to attempt to schedule a new Node with the wrong "shape"**. Occasionally, the autoscaler may cache a Node that CoreWeave automation has "tainted" (marked unschedulable). The cached taint can cause the autoscaler to incorrectly determine that it can't scale up the pool, even if new scheduling requests exist. | Manually set `targetNodes` to `1`. This triggers CKS to add a Node, updating the cache (or clearing a bad cache entry) and causing it to schedule a new Node. |
