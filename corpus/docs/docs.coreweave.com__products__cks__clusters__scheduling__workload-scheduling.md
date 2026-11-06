# Workload scheduling on CKS

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling

# Workload scheduling on CKS

> Control where CKS deploys Pods through namespaces, labels, and taints

In CoreWeave Kubernetes Service (CKS) (CoreWeave Kubernetes Service (CKS) is CoreWeave's managed Kubernetes service.), namespaces, labels, taints, and eviction policies organize Nodes. These features control where CoreWeave schedules its core managed services and ensure that customer workloads always run on healthy production Nodes.

This page is a reference for cluster operators and workload owners who need to understand how CKS schedules Pods, which labels and taints CoreWeave reserves, how to target Nodes with a selector or affinity rule, and how to choose an eviction strategy that matches a workload's tolerance for interruption. For cluster-level scheduler configuration, see [Scheduling profiles](https://docs.coreweave.com/products/cks/clusters/scheduling/scheduling-profiles.md). For third-party schedulers, see [Custom schedulers and third-party integrations](https://docs.coreweave.com/products/cks/clusters/scheduling/custom-schedulers.md).

For runtime-specific Node selection and isolation requirements, see [Container runtimes on CKS](https://docs.coreweave.com/products/cks/container-runtimes.md).

## CKS namespaces

CKS has two types of namespaces:

* **User namespaces** carry your Org ID label. You have full control over user namespaces. You can create, change, and delete them.
* **Control Plane namespaces** host critical services that run within the cluster. CoreWeave creates these namespaces. Don't alter or delete them. CoreWeave automates workloads within these managed namespaces and doesn't bill customers for jobs that run in Control Plane namespaces.

CKS applies the label `ns.coreweave.cloud/org=control-plane` to `cw-*` prefix namespaces, which host the CKS control plane components. To view these namespaces in a CKS cluster:

```bash theme={"system"}
kubectl get namespaces --selector=ns.coreweave.cloud/org=control-plane
```

For the components that run in each namespace, see [Cluster components](https://docs.coreweave.com/products/cks/reference/cluster-components.md).

## Node type selection labels

All CoreWeave [GPU](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU](https://docs.coreweave.com/platform/instances/cpu-instances.md) Nodes feature Instance IDs. To ensure consistency, every Node within a Node Pool carries an Instance ID through the `instance-type` label. For example:

```yaml theme={"system"}
node.kubernetes.io/instance-type=instance-type-example
```

For a list of all Instance IDs, see the [GPU Instance](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU Instance](https://docs.coreweave.com/platform/instances/cpu-instances.md) details.

> [!NOTE]
>
> Some customers may use the `node.kubernetes.io/type` label. CoreWeave updated this label to reference the new Instance ID.

## Node lifecycle labels

CKS uses labels to identify a Node's state in [the Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md). These labels ensure that CKS always schedules customer workloads on healthy production Nodes.

* `node.coreweave.cloud/state`: Identifies the [Node's lifecycle state](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md), such as `production`, `zap`, or `triage`.
* `node.coreweave.cloud/reserved`: Identifies the workload type running on the Node:
  * If `/reserved` is a customer Org ID and `/state=production`, it's for user workloads.
  * If `/state` is not `production`, then `/reserved` matches `/state`.
* `node.coreweave.cloud/reserved-desired`: Overrides `/reserved`. If it doesn't match `/reserved`, the marked Node is pending and transitions Reservations automatically.

## User-provided labels

Create custom Node labels for scheduling or organization, but never in the `*.coreweave.cloud` or `*.coreweave.com` namespaces. CKS reserves those for its own labels. A Node Pool that sets one in `nodeLabels` is still accepted, but the label never reaches the Nodes. CKS drops it and fires a [`CWNodePoolMetadataSanitized`](https://docs.coreweave.com/products/cks/reference/node-pool#events) warning Event on the Node Pool.

```yaml theme={"system"}
metadata:
  labels:
    foo.coreweave.cloud/bar: "true"   # Not allowed
    foo.coreweave.com/bar: "true"     # Not allowed
```

## Target Nodes

To run a Pod on a specific instance type, rack, or Node, use `nodeSelector` or
`nodeAffinity`. Both keep the Kubernetes scheduler involved, so preemption,
priority, topology spread, and Kueue integration all work.

Note that a Pod whose
`schedulerName` is the [SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md)
has its placement decided by Slurm instead: Node affinity still applies, but Pod
affinity, Pod anti-affinity, and topology spread constraints have no effect. Pods
that use the default scheduler are unaffected.

A `nodeSelector` matches a single value for each label and covers most cases.
Replace the bracketed placeholder in each of the following examples with your
target value.

To target an instance type, match the `instance-type` label described in [Node
type selection labels](#node-type-selection-labels):

```yaml title="Target an instance type" theme={"system"}
spec:
  nodeSelector:
    node.kubernetes.io/instance-type: [INSTANCE-ID]
```

To keep a job on Nodes that share an NVLink domain, match the NVLink domain
label. On [NVL72-powered Nodes](https://docs.coreweave.com/platform/instances/nvl72.md), every Node in a rack
shares the same globally unique value:

```yaml title="Target an NVLink domain" theme={"system"}
spec:
  nodeSelector:
    ds.coreweave.com/nvlink.domain: [NVLINK-DOMAIN]
```

To place Pods in the same physical rack, match the rack number. Quote the value,
because Kubernetes label values are strings:

```yaml title="Target a rack" theme={"system"}
spec:
  nodeSelector:
    node.coreweave.cloud/rack: "[RACK-NUMBER]"
```

To reach one specific Node, match its hostname. This is the supported
alternative to `.spec.nodeName`:

```yaml title="Target a single Node" theme={"system"}
spec:
  nodeSelector:
    kubernetes.io/hostname: [NODE-NAME]
```

For more flexible matching, use `nodeAffinity` with operators such as `In`,
`NotIn`, and `Exists`. Affinity accepts multiple values for the same key, which
helps when a Node Pool spans more than one rack or NVLink domain:

```yaml title="Match multiple NVLink domains with nodeAffinity" theme={"system"}
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: ds.coreweave.com/nvlink.domain
            operator: In
            values:
            - [NVLINK-DOMAIN-A]
            - [NVLINK-DOMAIN-B]
```

To target a specific InfiniBand or RoCE fabric, superpod, or leafgroup, see
[InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md).

### Avoid `.spec.nodeName` for Node targeting

Never use `.spec.nodeName` to pin a Pod to a Node.
Setting `.spec.nodeName` bypasses the Kubernetes scheduler entirely. The Pod
already looks scheduled, so the kubelet on the named Node admits it directly.

As a result, the Pod gets no preemption, no priority ordering, no affinity or
topology spread, and no Kueue or Topology-Aware Scheduling. If the Node lacks
free resources, the kubelet rejects the Pod during admission instead of
triggering preemption. The Pod ends in `Failed` with a reason such as
`OutOfcpu`, `OutOfmemory`, or `OutOfnvidia.com/gpu`. Because the scheduler
never saw the Pod, `kubectl describe pod` reports no `FailedScheduling` event to
explain the outcome.

CoreWeave runs short [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md)
Pods on idle Nodes at a priority lower than customer workloads. The
`default-scheduler` preempts them automatically, so you usually don't notice them.
Third-party schedulers don't preempt them by default. A Pod pinned with `.spec.nodeName` can't trigger that preemption, so
it can fail to schedule on a Node that looks free. Use `nodeSelector` or
`nodeAffinity` instead. See [Why is my Pod stuck in pending on
CKS?](https://docs.coreweave.com/support/cks/articles/why-is-my-pod-stuck-in-pending).

## Pod interruption and eviction policies

CKS supports three eviction strategies for Pods: **non-interruptible**, **interruptible**, and **gracefully interruptible**. These strategies determine how CKS handles Pods during Node maintenance, reboots, or scale-down events.

### Summary of eviction strategies

| Strategy | Pod label | Description | Note |
| - | - | - | - |
| **Non-interruptible** | None (default) | CKS waits for these Pods to stop before deferred maintenance, safe reboots, and Node Pool scale-down with the default `IdleOnly` strategy. Use for critical training jobs and single-instance stateful apps. | Immediate actions, `PreferIdle` scale-down, the Cluster Autoscaler, and [prefill timeout expiry](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#how-prefill-works) can still interrupt these Pods. |
| **Interruptible** | `qos.coreweave.cloud/interruptable` | CKS terminates Pods and proceeds with the Node action without waiting for their full `terminationGracePeriodSeconds`. Use for stateless workloads that you can restart without data loss. | Misspelled as `interruptable` for historical reasons. In the `qos.coreweave.cloud` namespace. |
| **Gracefully interruptible** | `qos.coreweave.com/graceful-interruptible` | Reboots and deferred maintenance wait until the Pod terminates or its `terminationGracePeriodSeconds` expires. Node Pool removal has a [separate drain deadline](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-idle-status-and-maintenance). Use *only* for stateful applications that block rebooting until the application terminates, such as databases and local storage. For all other workloads, use interruptible. | Spelled correctly. In the `qos.coreweave.com` namespace. |

Choose one interruption strategy per Pod and follow the [idle Node rules and label precedence](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes) when interpreting `CWActive`.

The following sections describe each strategy in detail.

### Non-interruptible

Workloads that you don't want interrupted, such as critical training jobs and single-instance stateful apps, shouldn't set either of the two labels in the preceding table. If neither label is set, the Pod is considered non-interruptible.

CKS treats Nodes with non-interruptible Pods as active, which is the default behavior for Pods. CKS waits for these Pods to stop before proceeding with deferred Node maintenance or safe reboots. When you lower `targetNodes` on a Node Pool that uses the default `IdleOnly` [scale-down strategy](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#scaling-strategies), CKS also waits for these Pods before it removes a Node. The `PreferIdle` strategy and the [Cluster Autoscaler](https://docs.coreweave.com/products/cks/nodes/autoscaling.md#node-utilization) can remove a Node that still runs non-interruptible Pods. A Node in the [prefill flow](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#how-prefill-works) can also start draining when its idle timeout expires, even if these Pods are still running.

[Immediate state transitions](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#immediate-state-transitions), including administrator-requested [immediate reboots](https://docs.coreweave.com/products/cks/nodes/reboot.md#safe-versus-immediate-reboots), can still interrupt non-interruptible Pods. Extreme events such as complete Node failure or data center power loss can also interrupt these Pods. Leaving both interruption labels unset doesn't protect a Pod from an immediate reboot.

### Long-running GPU Pods

A Pod that holds GPU resources (`nvidia.com/gpu`) indefinitely without an interruptible label has two consequences:

* **Deferred maintenance can stall**: CKS ordinarily waits for non-interruptible workloads to finish before starting discretionary maintenance. A long-running Pod can keep a pending transition waiting. For a Node in the [prefill flow](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#how-prefill-works), CKS can start draining it after the prefill timeout expires, even if workloads are still running. Critical hardware failures can still trigger immediate action.
* **Prevents HPC Verification tests**: CoreWeave runs hourly [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) tests on Nodes where all GPUs are available. A long-running Pod that holds GPUs prevents these tests from scheduling on that Node for the duration of the Pod's lifetime.

For deferred maintenance, choose an [interruption strategy](#summary-of-eviction-strategies) that matches your workload's tolerance for the [drain behavior of pending transitions](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#active-nodes-and-stalled-transitions).

To allow HPC Verification tests to run on a Node alongside a long-running GPU Pod, the Pod must not hold any GPUs. SUNK addresses this by introducing a separate `sunk.coreweave.com/accelerator` resource for `slurmd` Pods, leaving the Node's GPUs available for HPC Verification. See [SUNK-specific scheduling](#sunk-specific-scheduling) for details.

### Interruptible

Workloads such as inference Pods or stateless applications that you can restart without data loss should use the interruptible strategy. CKS terminates these Pods and proceeds with the Node action (such as reboot or scale-down) without waiting for the Pod's full `terminationGracePeriodSeconds`.

> [!WARNING]
>
> Never apply this label to distributed training jobs, single-instance databases, stateful services, or any workload that can't tolerate sudden termination. Evicting these workloads may cause data loss or require costly restarts across multiple Nodes.

To choose this strategy, apply the label `qos.coreweave.cloud/interruptable: "true"` to your Pods. This label is in the `qos.coreweave.cloud` namespace.

```yaml theme={"system"}
metadata:
  labels:
    qos.coreweave.cloud/interruptable: "true"
```

Note that for historical reasons, the label is misspelled as `interruptable`.

### Gracefully interruptible

Use the gracefully interruptible strategy only for stateful applications that block a reboot until the application terminates, such as databases and local storage. These workloads need to finish writing data or hand off state before a Node reboots or drains. For all other applications, including stateless workloads that can be restarted without data loss, use the [interruptible](#interruptible) strategy instead.

Gracefully interruptible Pods delay reboots (including immediate reboots) and deferred maintenance until they terminate or their `terminationGracePeriodSeconds` expires. Node Pool removal has a separate drain deadline and can remove a Node before a longer Pod grace period expires; see [Node idle status and maintenance](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-idle-status-and-maintenance). A deletion request starts the termination grace period. For how these Pods affect `CWActive` and dashboard activity indicators, see [Idle Nodes](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes).

To choose this, apply the label `qos.coreweave.com/graceful-interruptible: "true"` to your Pods. This label is in the `qos.coreweave.com` namespace.

```yaml theme={"system"}
metadata:
  labels:
    qos.coreweave.com/graceful-interruptible: "true"
```

### Key behaviors and limitations

The following sections describe behaviors and limitations to consider when using `graceful-interruptible` Pods.

#### Node Pool scale-down

When choosing a new Node to drain for scale-down, the default `IdleOnly` strategy requires `CWActive = False`. A counted gracefully interruptible Pod can prevent selection even if the Node also hosts interruptible Pods or has unused GPUs. Adding interruptible Pods doesn't make a Node idle while counted Pods remain.

To make Nodes eligible, finish or move the workloads keeping them active, then confirm `CWActive = False`. If you need scale-down to interrupt active workloads, consider the [`PreferIdle` strategy](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools#scaling-strategies). The [Cluster Autoscaler](https://docs.coreweave.com/products/cks/nodes/autoscaling.md#node-utilization) uses its own removal rules. Nodes already marked for removal or already draining follow their existing removal workflow.

#### Tolerations that prevent graceful eviction

Pods that tolerate either `node.coreweave.cloud/evict=true:NoExecute` or `node.coreweave.cloud/reserved:NoExecute` don't go through the `graceful-interruptible` logic and may be evicted immediately. See [Eviction taints](#eviction-taints).

#### Drain time differences

* Reboots and deferred maintenance use a default drain timeout of 3 minutes, and honor `terminationGracePeriodSeconds` for `graceful-interruptible` Pods.
* Node Pool removal has a separate 5-minute drain timeout. A longer Pod termination grace period doesn't extend this deadline.
* CKS-initiated scale-down doesn't wait for DaemonSets unless they carry `qos.coreweave.com/graceful-interruptible: "true"` and don't tolerate eviction taints.
* For services that require long termination phases, explicitly set `terminationGracePeriodSeconds` and account for the deadline on each removal path.

#### Potential for scale-down stalls

If too few Nodes become idle, the Node Pool can remain above its target. Use the [Node Pool health check commands](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md#run-a-node-pool-health-check) to inspect `CWActive` and identify the Pods keeping each Node active. See [Current is above target](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md#current-is-above-target) for diagnosis steps.

#### Risk of stuck Nodes

`IdleOnly` can wait for an eligible Node without starting a drain. Maintenance instead drains gracefully interruptible Pods after non-interruptible workloads finish, then waits for Pod termination or expiry of the termination grace period. This maintenance wait can finish while `CWActive` is still `True`. If a maintenance action remains stalled, inspect the [Node conditions and events](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#example-a-pending-reboot) and [contact Support](https://docs.coreweave.com/support.md) with the Node name and the blocking messages.

## Taints and tolerations

CKS uses taints to guard control-plane Nodes and enforce GPU and CPU scheduling. The following sections describe the eviction taints CKS applies to Nodes and the user-facing taints that route Pods to the correct hardware.

### Eviction taints

CKS applies the following eviction taints to Nodes:

* `node.coreweave.cloud/evict=true:NoExecute`
* `node.coreweave.cloud/reserved:NoExecute`

Pods that tolerate these bypass graceful eviction and may be evicted immediately.

### User taints

For custom taints on GPU Nodes, use `NoSchedule` to prevent new Pods without matching tolerations from scheduling. Use `PreferNoSchedule` when a scheduling preference is sufficient. Neither effect evicts Pods that are already running.

Do not use `NoExecute` taints on GPU Nodes. [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#taints) Pods tolerate arbitrary `NoSchedule` and `PreferNoSchedule` taints, but not arbitrary `NoExecute` taints. A `NoExecute` taint can block automated verification on both idle Nodes and rebooted Nodes, which leaves them unverified. CoreWeave might replace Nodes that remain in a reboot state too long.

This guidance applies to customer-managed taints, including taints configured on a Node Pool. Leave CoreWeave-managed taints unchanged. To request a test, see [Verify a Node on demand](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#verify-a-node-on-demand).

The verification controller in CKS customer clusters also tolerates arbitrary `NoSchedule` taints. If no tests start and the controller remains `Pending`, see [The verification controller Pod stays Pending](https://docs.coreweave.com/support/platform/articles/troubleshoot-hpc-verification#the-verification-controller-pod-stays-pending).

Pods without GPU requests automatically tolerate the CPU taint (`is_cpu_compute:NoSchedule`).

```yaml title="CPU taint" theme={"system"}
  - effect: NoSchedule
    key: is_cpu_compute
```

The GPU taint (`is_gpu=true:PreferNoSchedule`) prevents CPU-only Pods from scheduling on GPU Nodes unless necessary. A CPU-only Pod can still schedule on a GPU Node if no CPU Nodes are available.

```yaml title="GPU taint" theme={"system"}
  - effect: PreferNoSchedule
    key: is_gpu
    value: "true"
```

> [!CAUTION]
>
> Use caution before adding tolerations to your Pods, so workloads continue to run on healthy Nodes.

## SUNK-specific scheduling

The following sections describe scheduling behaviors specific to SUNK workloads on CKS.

To reserve a Node Pool for a SUNK NodeSet, match the pool's `nodeLabels` and `nodeTaints` to the NodeSet's affinity and tolerations. See [Bind NodeSets to Node Pools for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md).

### The SUNK `/lock` taint

To prevent contention with other Pods that request GPU access while long-running `slurmd` Pods are active, SUNK adds a new GPU resource to Kubernetes, `sunk.coreweave.com/accelerator`, in addition to the `nvidia.com/gpu` resource provided by NVIDIA's plugin.

Because the GPU has two different resource names, Kubernetes tracks the consumption separately, which lets `slurmd` Pods request the same underlying GPU as other Kubernetes Pods. However, this requires SUNK to manage GPU contention instead of the Kubernetes scheduler.

> [!WARNING]
>
> Use `nvidia.com/gpu` for GPU requests in all Pod specs, including Pods scheduled by the SUNK Pod Scheduler. Don't request `sunk.coreweave.com/accelerator` directly. SUNK reserves this resource for its own internal Pods, such as `slurmd`, and converts `nvidia.com/gpu` requests into Slurm generic resource (GRES) allocations. A direct request for `sunk.coreweave.com/accelerator` bypasses this conversion and can cause incorrect GPU accounting or contention between Slurm jobs and Kubernetes Pods.

SUNK manages the contention with a taint called `sunk.coreweave.com/lock`. SUNK applies this taint to Nodes through a call to the [SUNK Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) during the Prolog phase.

```yaml title="SUNK's lock taint" theme={"system"}
  - effect: NoExecute
    key: sunk.coreweave.com/lock
    value: "true"
```

> [!WARNING]
>
> Prolog completion blocks until SUNK evicts every Pod that doesn't tolerate the taint.

### DaemonSets on SUNK Nodes

[Kubernetes DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) that run on SUNK Nodes must tolerate the `sunk.coreweave.com/lock` taint, as well as `is_cpu_compute`, `is_gpu`, and `node.coreweave.cloud/reserved`:

```yaml title="Example toleration" lines highlight={3-14} theme={"system"}
spec:
  tolerations:
  - key: sunk.coreweave.com/lock
    value: "true"
    operator: Equal

  - key: is_cpu_compute
    operator: Exists

  - key: is_gpu
    operator: Exists

  - key: node.coreweave.cloud/reserved
    operator: Exists
```

## Scale down workloads

To scale down Pods in a specific order, use the Cloud Console or CKS API to adjust the cluster specification. For more information, see the [Kubernetes guide about Pod deletion cost](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost).

## Troubleshoot Pod scheduling

If a GPU Pod stays `Pending`, see [Why are my Pods not scheduling on GPU Nodes?](https://docs.coreweave.com/support/cks/articles/why-are-my-pods-not-scheduling-on-gpu-nodes) for common causes and fixes.

### Resource requests for GPU Pods

Size CPU and memory `requests` to roughly the per-GPU share of the instance, leaving headroom for DaemonSets and system overhead. Specify GPUs under `limits` as `nvidia.com/gpu: [COUNT]`. Kubernetes mirrors the value to `requests` automatically. For a worked whole-Node example, see [Target specific GPUs or CPUs](https://docs.coreweave.com/products/cks/nodes/manage.md#target-specific-gpus-or-cpus).

For long-running training and inference, set CPU and memory `requests` equal to `limits` so the Pod gets the Guaranteed Quality-of-Service (QoS) class and is the last to be evicted under resource pressure. See [How do Kubernetes QoS classes work?](https://docs.coreweave.com/support/cks/articles/how-do-kubernetes-qos-classes-work).

For recommended ratios and how requests behave on GPU Pods, see [What are the recommended resource requests and limits for GPU Pods?](https://docs.coreweave.com/support/cks/articles/what-are-the-recommended-resource-requests-and-limits-for-gpu-pods) and [How do CPU and memory requests work with GPU Pods?](https://docs.coreweave.com/support/cks/articles/how-do-cpu-and-memory-requests-work-with-gpu-pods).
