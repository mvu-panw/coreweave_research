# Manage resources with the SUNK Pod Scheduler

Source: https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources

# Manage resources with the SUNK Pod Scheduler

> Configure Node sharing, resource allocation, and GPU management for Kubernetes Pods scheduled through Slurm

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

When Kubernetes Pods and Slurm jobs run on the same Kubernetes Nodes, you need to configure how they share GPU, CPU, and memory resources. This page is for cluster administrators and workload operators who use the SUNK Pod Scheduler. It walks through the common scenarios and the configuration each one requires so that Pods and Slurm jobs can coexist without resource contention or scheduling failures.

## Resource sharing rules

Before choosing a configuration, understand what can and cannot be shared:

* **Slurm manages GPUs exclusively.** The SUNK Pod Scheduler converts Pod `nvidia.com/gpu` requests into Slurm generic resource (GRES) allocations (for example, `gres:gpu:h100:4`). Slurm assigns specific GPU indices to each job, so no two jobs receive the same physical GPU. Two SUNK-scheduled Pods from the same Slurm user can share a Node and use different GPUs with `exclusive: "user"`.
* **CPU and memory can be shared** between Kubernetes Pods and Slurm jobs, as long as the `slurmd` container resource requests are lowered. See [Lower slurmd resource requests](#lower-slurmd-resource-requests).
* **Avoid static CPU pinning.** A container in a Guaranteed QoS Pod triggers [static CPU allocation](https://docs.coreweave.com/products/sunk/run_workloads/static-cpu-allocation.md) when it requests a whole number of CPUs. With container-level resource settings, Guaranteed QoS requires every container to have positive CPU and memory requests equal to its corresponding limits. Use Burstable QoS or fractional CPU requests to avoid pinning, which can cause resource contention and node drains in Slurm.
* **A Node can host both GPU and CPU-only workloads.** For example, a Slurm job using all GPUs can coexist with a SUNK-scheduled CPU-only Pod, as long as CPU and memory are available.

> [!WARNING]
>
> Use `nvidia.com/gpu` for GPU requests in all Pod specs, including Pods scheduled by the SUNK Pod Scheduler. Don't request `sunk.coreweave.com/accelerator` directly. SUNK reserves this resource for its own internal Pods, such as `slurmd`, and converts `nvidia.com/gpu` requests into Slurm GRES allocations. A direct request for `sunk.coreweave.com/accelerator` bypasses this conversion and can cause incorrect GPU accounting or contention between Slurm jobs and Kubernetes Pods.

> [!WARNING]
>
> Slurm has no visibility into Pods scheduled through the standard Kubernetes scheduler. If you run non-DaemonSet Pods on Slurm Nodes without the SUNK Pod Scheduler, you cause GPU allocation conflicts and resource contention.

## Common scenarios

Choose the scenario that matches your workload. Each includes the annotations and resource configuration you need.

> [!NOTE]
>
> The specific CPU, memory, and GPU values in these examples depend on your Node type and `slurmd` configuration. To find the right values for your cluster, see [Check available resources](#check-available-resources).

### GPU Node scenarios

The following scenarios cover Pods that run on Nodes with GPUs.

#### Full-Node GPU Pod

**Use when:** A single Pod uses all GPUs on the Node, or you want full Node isolation.

Set `exclusive: "none"` to prevent any other Slurm job from sharing the Node:

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "none"
```

Set your Pod's resource **requests** low and use high **limits**, because the kubelet must fit both the Pod's requests and the `slurmd` container's requests within the Node's allocatable resources:

```yaml theme={"system"}
resources:
  limits:
    memory: 960Gi       # High limit so the container can use full Node memory
    nvidia.com/gpu: "8"
  requests:
    cpu: "10"           # Low request to fit alongside slurmd
    memory: 10Gi        # Low request to fit alongside slurmd
    nvidia.com/gpu: "8"
```

> [!WARNING]
>
> Even with full-Node exclusive mode, the kubelet enforces Kubernetes resource accounting. If the combined requests from `slurmd`, system Pods, and your Pod exceed the node's allocatable memory, the kubelet rejects the Pod and reports `OutOfmemory`. Check the actual `slurmd` requests, then keep Pod requests low or [lower `slurmd` resource requests](#lower-slurmd-resource-requests) as needed.

#### Multiple partial-GPU Pods sharing a Node

**Use when:** You want to run multiple Pods that each use a subset of a Node's GPUs (for example, two Pods each using 4 of 8 GPUs).

Create a dedicated Slurm user for Kubernetes Pods and set `exclusive: "user"`. This lets SUNK-scheduled Pods share Nodes with each other while keeping other Slurm users off those Nodes.

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "user"
  sunk.coreweave.com/user-id: "1001"  # Dedicated Slurm user for K8s Pods
```

```yaml theme={"system"}
resources:
  limits:
    memory: 480Gi
    nvidia.com/gpu: "4"
  requests:
    cpu: "10"           # Low request to fit alongside slurmd
    memory: 10Gi        # Low request to fit alongside slurmd
    nvidia.com/gpu: "4"
```

**Resource configuration required:** You must [lower `slurmd` resource requests](#lower-slurmd-resource-requests) and [enable memory tracking](#enable-memory-tracking-in-slurm) to prevent scheduling failures.

#### CPU-only Pod alongside GPU workloads

**Use when:** You need to run a CPU-only workload (monitoring agent, data preprocessing, sandbox environment) on a Node that also runs GPU workloads.

Set `exclusive: "ok"` and do not request GPUs:

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "ok"
```

```yaml theme={"system"}
resources:
  requests:
    cpu: "10"
    memory: 10Gi
  # No nvidia.com/gpu request
```

Because the Pod doesn't request GPUs, no conflict occurs with Slurm's GPU allocator.

**Resource configuration required:** You must [lower `slurmd` resource requests](#lower-slurmd-resource-requests) to make CPU and memory available for the Pod.

> [!WARNING]
>
> A CPU-only Pod with `exclusive: "ok"` can't land on a Node where a Slurm job runs with full exclusive mode (`--exclusive`). If you need CPU-only Pods to coexist with GPU jobs, use `exclusive: "user"` on the GPU workloads instead.

### CPU Node scenarios

The same `exclusive` annotation controls sharing on CPU-only Nodes. The difference is that GPU GRES allocation isn't a factor, so the main concern is CPU and memory sharing.

#### Full-Node CPU Pod

**Use when:** A Pod needs the entire CPU Node with no other workloads.

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "none"
```

```yaml theme={"system"}
resources:
  limits:
    memory: 256Gi       # Match your CPU Node's total memory
  requests:
    cpu: "10"
    memory: 10Gi
```

As with GPU Nodes, keep Pod requests low to fit alongside `slurmd` container requests.

#### Share a CPU Node between Pods and Slurm jobs

**Use when:** You want to run SUNK-scheduled Pods and Slurm jobs on the same CPU Node, sharing the CPU and memory pool.

Use `exclusive: "user"` with a dedicated Slurm user so that SUNK Pods and Slurm jobs from the same user can coexist:

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "user"
  sunk.coreweave.com/user-id: "1001"  # Dedicated Slurm user for K8s Pods
```

```yaml theme={"system"}
resources:
  requests:
    cpu: "10"
    memory: 10Gi
```

Alternatively, use `exclusive: "ok"` to allow sharing with any Slurm user:

```yaml theme={"system"}
annotations:
  sunk.coreweave.com/exclusive: "ok"
```

**Resource configuration required:** You must [lower `slurmd` resource requests](#lower-slurmd-resource-requests) and [enable memory tracking](#enable-memory-tracking-in-slurm) to prevent oversubscription on shared CPU Nodes.

## Configure shared resources

The preceding scenarios reference two settings that you must adjust before SUNK-scheduled Pods can share a Node with Slurm jobs. Adjusting these settings ensures the kubelet has enough allocatable resources for the additional Pods. The following sections describe each setting in detail.

### Check available resources

The resource values you use for Pod requests and `slurmd` configuration depend on your Node type. Different GPU and CPU Nodes have different amounts of allocatable CPU and memory. Before configuring resource sharing, check your Node's capacity, replacing `[NODE-NAME]` with the Node's name:

```bash theme={"system"}
kubectl get node [NODE-NAME] -o jsonpath='cpu: {.status.allocatable.cpu}, memory: {.status.allocatable.memory}'
```

Then check what `slurmd` currently requests, replacing `[SLURMD-POD-NAME]` with the name of the Pod running `slurmd` and `[NAMESPACE]` with its namespace:

```bash theme={"system"}
kubectl get pod [SLURMD-POD-NAME] -n [NAMESPACE] -o jsonpath='{.spec.containers[?(@.name=="slurmd")].resources.requests}'
```

The difference between the Node's allocatable resources and the total requests from `slurmd` and other containers (such as `sssd`, `munged`, and `user-lookup`) determines how much room is available for SUNK-scheduled Pods.

### Lower slurmd resource requests

Check the actual `slurmd` requests before you change them. In SUNK 8.x, enabling the Pod Scheduler selects a low-profile overlay even if `compute.lowProfileRequests` is `false`. The standard overlay sets requests to 10 CPU and `10Gi` and leaves limits unchanged. Development profiles can use smaller requests, and the overlay preserves existing requests if a CPU or memory limit is below the overlay's target value. For SUNK 7.x, inspect the resources configured in the NodeSet's `slurmd` container.

If `slurmd` requests already leave enough capacity for your Pods and system overhead, skip to [Enable memory tracking in Slurm](#enable-memory-tracking-in-slurm). If its requests consume most of the node's allocatable CPU or memory, lower them to avoid `OutOfcpu` or `OutOfmemory` kubelet rejections.

Lower the `slurmd` container's requests while keeping limits high so Slurm jobs can still use the full Node. The specific values depend on your Node type, but a common starting point is to set requests to a small fraction of the Node's total resources:

```yaml theme={"system"}
nodes:
  my-gpu-nodes:
    enabled: true
    definitions:
      - h100
    replicas: 4
    resources:
      requests:
        cpu: 10
        memory: 10Gi
      limits:
        memory: 1920Gi  # Set to your Node's total memory
```

This configuration reserves only 10 CPUs and `10Gi` of memory for `slurmd`, freeing the rest for SUNK-scheduled Pods. The high memory limit ensures Slurm jobs can still use the full Node memory. Adjust the `limits.memory` value to match your Node type's total memory.

> [!WARNING]
>
> If `slurmd` keeps requesting most of the Node's CPU and memory, Pod scheduling failures often follow when sharing Nodes. If the kubelet rejects your Pods with `OutOfmemory` or `OutOfcpu`, check the `slurmd` requests first.

For an example manifest that changes `slurmd` resources, see [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md#the-manifest).

### Enable memory tracking in Slurm

SUNK v7.3.0 and later set `SelectTypeParameters` to `CR_CPU_MEMORY` by default, which tracks memory as a consumable resource. Earlier SUNK versions defaulted to `CR_Core`, which doesn't track memory. That lets multiple jobs oversubscribe memory, leading to out-of-memory (OOM) errors. Check your cluster's current value with `scontrol show config | grep SelectTypeParameters`.

When sharing Nodes, make sure `SelectTypeParameters` is a memory-aware value:

```yaml theme={"system"}
slurmConfig:
  SelectTypeParameters: CR_CPU_MEMORY
```

With this setting, Slurm tracks both CPU and memory when it places jobs, which prevents oversubscription.

Lowering `slurmd` requests leaves room for other Pods in Kubernetes, while `CR_CPU_MEMORY` lets Slurm track memory allocated to its jobs. The two systems still account for resources separately. Size Pod requests for the capacity remaining after `slurmd`, DaemonSets, and other system Pods.

## Exclusive annotation values

The `sunk.coreweave.com/exclusive` annotation (SUNK v5.7.0 and later) maps directly to Slurm's [`--exclusive`](https://slurm.schedmd.com/sbatch.html#OPT_exclusive) option. It accepts the following string values:

| Value | Slurm behavior | When to use |
| - | - | - |
| `"none"` | The Node is allocated exclusively to this job. No other jobs can share the Node. | Full-Node GPU Pods, or when you want complete isolation. |
| `"ok"` | The job can share the Node with any other job, regardless of user or account. | CPU-only workloads sharing Nodes with GPU workloads. |
| `"user"` | The job can share the Node only with jobs from the same Slurm user. | Multiple SUNK Pods each using a subset of a Node's GPUs. This is the recommended approach for partial-GPU Pods. |
| `"mcs"` | The job can share the Node only with jobs that have the same MCS (Multi-Category Security) label. | When using Slurm MCS labels to group workloads by tenant or project. |
| `"topo"` | The job doesn't share its topology Block with any other job. This value has an effect only on clusters with the Topology/Block Plugin enabled. | Rarely. The job holds its entire Block, which can leave a whole rack idle. Consult CoreWeave support before using this value. See [Exclusive option](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md#exclusive-option). |

> [!NOTE]
>
> The `"none"` value name can be misread. In Slurm's `--exclusive` option, `none` means "exclusive mode is on, and the sharing override is none," meaning Slurm allows no sharing. It does **not** mean "no exclusivity."

## GPU allocation

Slurm manages GPU allocation exclusively through GRES. The SUNK Pod Scheduler converts Pod GPU requests into Slurm GRES allocations, and Slurm assigns specific GPU indices to each job. Don't schedule GPU Pods through the standard Kubernetes scheduler on Slurm Nodes, because this bypasses Slurm's GRES tracking and causes GPU conflicts.

When scheduling GPU Pods, choose one of these approaches:

* **Full-Node exclusive** with `exclusive: "none"` when the Pod uses all GPUs.
* **Per-user exclusive** with `exclusive: "user"` and a dedicated `user-id` when multiple Pods each use a subset of GPUs. This is the recommended approach for partial-GPU workloads.
* **Slurm reservation** with the `sunk.coreweave.com/reservation` annotation to dedicate specific Nodes for Kubernetes Pods.

When you submit GPU jobs directly through Slurm, oversized `--cpus-per-task` or `--mem-per-cpu` requests can leave a GPU unusable on a Node. For how to size these requests, see [Avoid stranding GPUs with CPU and memory requests](https://docs.coreweave.com/products/sunk/run_workloads/avoid-stranded-gpus.md).

## Reserve resources for system Pods

Slurm doesn't account for resources consumed by DaemonSets, the `slurmd` container itself, or other system Pods. As a result, Slurm may allocate resources that appear available from Slurm's perspective but are already consumed from Kubernetes' perspective, which causes kubelet rejections.

To account for this overhead:

* Ensure `slurmd` resource requests are set low enough to leave room for SUNK-scheduled Pods.
* Be conservative with resource requests when packing multiple workloads onto a single Node.
* Set `SelectTypeParameters` to a memory-aware value (such as `CR_CPU_MEMORY`) so that Slurm tracks memory as a consumable resource.

## Scale-up and scale-down behavior

If your cluster autoscales, the timing and Pod-placement behaviors described in the following sections affect how shared Nodes fill and drain. When you use the SUNK Pod Scheduler with autoscaling, be aware of the following behaviors:

### Scale-up

When new Nodes join the cluster, Slurm's configuration takes about a minute to include them. During this window, the new Nodes aren't available for scheduling.

Slurm doesn't bin-pack workloads. When Slurm schedules new Pods, it selects Nodes based on its internal bitmap ordering, which may spread Pods across multiple partially-used Nodes instead of filling one Node before moving to the next. This can lead to GPU fragmentation.

### Scale-down

When Nodes are removed, Kubernetes selects which Pods to terminate. Kubernetes doesn't coordinate this selection with Slurm, so Kubernetes may terminate Pods across multiple Nodes rather than fully drain a single Node. Combined with the lack of bin-packing, this can leave Nodes with partially-used GPU allocations that can't be reclaimed.

### Impact on exclusive mode

Fragmentation has a larger impact with `exclusive: "user"` or `exclusive: "none"`. In per-user exclusive mode, a Node with even one remaining Pod can't accept Slurm jobs from other users, which makes unused GPUs on that Node inaccessible. Plan your scaling strategy accordingly.
