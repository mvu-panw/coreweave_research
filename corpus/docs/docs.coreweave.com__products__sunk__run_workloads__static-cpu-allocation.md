# Static CPU allocation and the SUNK Pod Scheduler

Source: https://docs.coreweave.com/products/sunk/run_workloads/static-cpu-allocation

# Static CPU allocation and the SUNK Pod Scheduler

> Why Kubernetes static CPU allocation is incompatible with the SUNK Pod Scheduler and how to prevent node drains.

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page is for cluster operators and workload owners who run SUNK on CoreWeave CKS. It explains how to identify Pods that trigger static CPU allocation, why the issue causes SUNK nodes to drain, and how to configure Pod resources to prevent it. Follow this guidance to avoid silent Slurm job failures and unexpected node drains caused by CPU pinning.

For a related allocation issue where oversized per-task CPU or memory requests leave a GPU unusable, see [Avoid stranding GPUs with CPU and memory requests](https://docs.coreweave.com/products/sunk/run_workloads/avoid-stranded-gpus.md).

Kubernetes can pin specific CPU cores to a Pod so that no other process on the Node shares those cores. This feature is called **static CPU allocation**, and the CPU Manager static policy in the `kubelet` controls it. CoreWeave CKS Nodes enable this policy by default.

Static CPU allocation is useful for latency-sensitive workloads that benefit from dedicated cores. However, it's **incompatible with the SUNK Pod Scheduler** because Slurm can't account for CPU cores that the `kubelet` has pinned to other Pods.

> [!WARNING]
>
> Do not schedule Pods that have Guaranteed QoS and a whole-number CPU request on Kubernetes Nodes used for SUNK. These Pods trigger static CPU allocation, which causes resource contention in Slurm. As a result, Slurm nodes drain with misleading error messages such as `batch job complete failure`.

## Static CPU allocation

A Pod triggers static CPU allocation when both of these conditions are true:

* The Pod has **Guaranteed QoS** class, meaning every container, including init containers, sets CPU and memory requests equal to its limits.
* The CPU request is a **whole integer** (for example, `cpu: 4`), not a fractional value (for example, `cpu: 3.5` or `cpu: 750m`).

For example, this resource specification triggers static CPU allocation because requests and limits are equal and the CPU value is an integer:

```yaml theme={"system"}
resources:
  requests:
    cpu: "4"
    memory: 8Gi
  limits:
    cpu: "4"
    memory: 8Gi
```

### CPU allocation with SUNK

Slurm is configured with a fixed CPU count for each node. It doesn't account for CPUs that the `kubelet` has pinned to Guaranteed QoS Pods. When static CPU allocation removes cores from the shared pool, the CPUs available to Slurm shrink to the configured total minus whatever the `kubelet` has pinned. Slurm continues to schedule jobs against the original count, which leads to resource contention.

The following sequence shows how the issue occurs:

1. Kubernetes schedules a Pod with Guaranteed QoS and integer CPU requests onto a SUNK node.
2. The CPU Manager in the `kubelet` pins specific CPU cores to the Pod using `cpuset` cgroups.
3. Slurm schedules a job to the node with pinned resources.
4. The job encounters resource contention and fails.
5. Slurm drains the node because of the job failure.

### Common drain reasons

Static CPU allocation drains a node with one of the following reasons. These messages can be misleading because none of them point to the underlying CPU pinning by the `kubelet`.

| Reason | Cause | Safe to undrain? |
| - | - | - |
| `batch job complete failure` | A job fails from resource contention on the pinned cores. | Only after you fix the Pod. Otherwise, the node drains again the next time a contended job lands on it. |
| `Low socket*core*thread count`, `Low CPUs` | `slurmd` detects fewer CPUs than configured, such as 127 instead of 128, because the `kubelet` removed the pinned CPUs from the shared pool. | No, until the CPU count is restored. Fix the Pod and restart `slurmd` first. See [CPU topology mismatch from a statically pinned Pod](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#cpu-topology-mismatch-from-a-statically-pinned-pod). |

## Prevent node drains from static CPU allocation

A Pod triggers static CPU allocation only when it has Guaranteed QoS *and* a whole-number CPU request, so breaking either condition prevents the drain. Choose one of the following fixes for every Pod that runs on SUNK nodes:

* Switch the Pod to Burstable QoS by setting its CPU request lower than its limit, or by omitting the CPU limit.
* Keep Guaranteed QoS, but request a fractional CPU value such as `3500m`.

Either change excludes the Pod from the `kubelet`'s static CPU manager, so it no longer pins cores. For the rules the `kubelet` applies, see [CPU management policies](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/#static-policy) in the Kubernetes documentation. The following sections describe each fix and how to verify the configuration.

### Switch Pods to Burstable QoS

Set CPU requests lower than CPU limits to change the Pod's QoS class from Guaranteed to Burstable:

```yaml theme={"system"}
resources:
  requests:
    cpu: "3"
    memory: 8Gi
  limits:
    cpu: "4"
    memory: 8Gi
```

You can also omit the CPU `limits` field altogether to produce Burstable QoS. With Burstable QoS in place, the `kubelet` no longer pins CPU cores, and Slurm can account for the full CPU capacity of the node.

### Keep Guaranteed QoS with a fractional CPU request

If the workload needs Guaranteed QoS, for example so that the `kubelet` evicts it last under memory pressure, keep requests equal to limits but use a fractional CPU value:

```yaml theme={"system"}
resources:
  requests:
    cpu: "3500m"
    memory: 8Gi
  limits:
    cpu: "3500m"
    memory: 8Gi
```

The Pod keeps its Guaranteed QoS class. Because its CPU request isn't a whole number, the `kubelet` runs it from the shared CPU pool instead of pinning cores to it.

### Verify a Pod's QoS class

To check whether a Pod has Guaranteed or Burstable QoS, query its status. Replace `[POD-NAME]` and `[NAMESPACE]` with your Pod's name and namespace:

```bash theme={"system"}
kubectl get pod [POD-NAME] -n [NAMESPACE] -o jsonpath='{.status.qosClass}'
```

A result of `Burstable` means the Pod can't trigger static CPU allocation. A result of `Guaranteed` is a problem only if the Pod also requests a whole number of CPUs, so check its CPU request as well.

To check all Pods on a specific Node, replace `[NODE-NAME]` with the Node's name:

```bash theme={"system"}
kubectl get pods -A --field-selector spec.nodeName=[NODE-NAME] -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.qosClass}{"\n"}{end}'
```

For any Pod with the `Guaranteed` QoS class, check whether its CPU request is a whole number. If it is, update its resource specification as described in [Prevent node drains from static CPU allocation](#prevent-node-drains-from-static-cpu-allocation).

## Recover drained nodes

If this issue has already drained nodes, address the underlying CPU pinning before the nodes can return to service. Update the Pod resource specification so that CPU requests don't equal CPU limits, or so that the CPU request is a fractional value. The Pod reschedules without pinned cores. Then restart `slurmd` on each affected node so that it re-reads the CPU count, and undrain the node. For the `slurmd` log lines to expect before and after the fix, see [CPU topology mismatch from a statically pinned Pod](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#cpu-topology-mismatch-from-a-statically-pinned-pod). For instructions on undraining nodes, see [Drain and undrain Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md).

To identify nodes drained by this issue, look for the drain reasons listed in [Common drain reasons](#common-drain-reasons):

```bash theme={"system"}
sinfo -t drain -NO "NodeList:45,Reason:130" | grep -F -e "batch job complete failure" -e "Low socket*core*thread count" -e "Low CPUs"
```
