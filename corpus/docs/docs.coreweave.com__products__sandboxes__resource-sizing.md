# Size sandbox CPU and memory

Source: https://docs.coreweave.com/products/sandboxes/resource-sizing

# Size sandbox CPU and memory

> Choose CPU and memory requests, compare them with usage, and constrain allocations with a runner policy

A sandbox reserves the CPU and memory it requests for as long as it runs. Choose each value for the work the sandbox needs to do. The ratio between them affects which Nodes have capacity for the request; actual consumption depends on the workload.

This guide shows how to choose a ratio, measure whether it matches your workload, and cap what other users of a runner can request.

## Why the ratio matters

For serverless placement, CoreWeave meters CPU and memory independently, on the capacity you reserve rather than the capacity you consume. A sandbox that requests 1 CPU and 64 GiB of memory is metered for all 64 GiB for its entire running window, even if it never allocates more than 1 GiB.

The ratio also affects placement. A Node has a fixed amount of each resource, so repeated requests skewed toward one resource can fill it while leaving the other available. In a simplified example, consider a Node with 32 allocatable CPUs and 128 GiB of allocatable memory. Two sandboxes requesting 1 CPU and 64 GiB each would reserve all 128 GiB but only 2 of the 32 CPUs. This example counts only workload requests; actual placement also accounts for runtime overhead, other workloads, and any [Node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md).

## Start from the host shape

For CoreWeave Kubernetes Service (CKS) placement, compare your request with the eligible Nodes' allocatable CPU and memory and any Node allocation budgets. Use allocatable resources rather than a Node's nominal installed RAM. For serverless placement, CoreWeave manages the capacity and policy; don't assume that every request uses a particular Node SKU.

A `cpu` request of `1` reserves one vCPU. Divide requested memory in GiB by requested CPU to calculate GiB per CPU. Requests with more memory per CPU than an eligible Node's allocatable ratio can become memory-bound. Requests with less memory per CPU can become CPU-bound. Available capacity and other workloads also affect placement.

Choose CPU and memory from measurements of a representative workload, then adjust each resource based on its usage. The following allocations illustrate the ratio calculation. They aren't workload-specific recommendations:

| Request | Calculation | Ratio |
| - | - | - |
| 2 CPU, 4 GiB | 4 / 2 | 2 GiB per CPU |
| 8 CPU, 16 GiB | 16 / 8 | 2 GiB per CPU |
| 4 CPU, 24 GiB | 24 / 4 | 6 GiB per CPU |

A request must also satisfy the policy that governs its placement, which can set a lower maximum than the host shape allows. See [Limits and quotas](https://docs.coreweave.com/products/sandboxes/reference/limits-and-quotas.md).

GPU sandboxes must size CPU and memory separately: a GPU request reserves GPUs only. See [GPU sandboxes](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md).

## Set requests and limits

For serverless placement, the default, set equal CPU and memory requests and limits. The value you request is the value you reserve and are metered for. Equal values leave no burst headroom, so size the request for the workload's peak.

The following sandbox reserves 2 CPU and 4 GiB for as long as it runs:

```python theme={"system"}
from cwsandbox import Sandbox

sandbox = Sandbox.run(
    resources={"cpu": "2", "memory": "4Gi"},
)
```

To request less than the limit, use CKS placement on a runner whose policy permits unequal values. See [Burstable QoS](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md#burstable-qos).

## Measure what your sandboxes use

Before you change a request, compare reserved capacity against consumption. The following queries require access to CoreWeave organization metrics through Grafana or the metrics API; see the [metrics prerequisites](https://docs.coreweave.com/products/sandboxes/operations/usage-metrics.md#prerequisites). If you use Forge credentials, see [View sandbox usage](https://docs.coreweave.com/products/sandboxes/operations/usage-metrics.md) for the available usage charts.

The following query returns fleet-wide memory consumed as a fraction of memory reserved:

```promql theme={"system"}
sum(cwsandbox_sandbox_memory_working_set_bytes)
/
sum(cwsandbox_sandbox_requested_memory_bytes)
```

The following query makes the same comparison for CPU:

```promql theme={"system"}
sum(rate(cwsandbox_sandbox_cpu_usage_seconds_total[5m]))
/
(sum(cwsandbox_sandbox_requested_cpu_millicores) / 1000)
```

A result well below 1 means the fleet reserves more than the measured usage. A fleet-wide average can hide individual sandboxes with high usage, so inspect workload-level peaks before reducing either resource. Treat measured usage as a lower bound: on microVM isolation these values come from inside the guest and exclude virtualization overhead and sidecar processes. Reduce requests gradually rather than to the measured figure.

The following query returns aggregate reserved memory per requested CPU, in GiB per CPU:

```promql theme={"system"}
sum(cwsandbox_sandbox_requested_memory_bytes) / 1024^3
/
(sum(cwsandbox_sandbox_requested_cpu_millicores) / 1000)
```

## Cap requests on a runner

A runner policy bounds what any container on that runner may request, and, through the ceilings, what a whole sandbox may resolve to. Set CPU and memory bounds together so that a sandbox cannot request one resource in isolation:

```json theme={"system"}
{
  "constraints": {
    "resources": {
      "minCpu": "500m",
      "maxCpu": "8",
      "minMemory": "1Gi",
      "maxMemory": "32Gi",
      "cpuCeiling": "8",
      "memoryCeiling": "32Gi",
      "requireLimits": true
    }
  }
}
```

Your administrators configure this policy for CKS placement. CoreWeave manages the policy for serverless placement.

A request above a maximum fails with `CWSANDBOX_RESOURCE_CEILING_EXCEEDED`. See [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-compute) and the [`ResourceConstraints` reference](https://docs.coreweave.com/products/sandboxes/reference/profile#resourceconstraints).

These bounds apply to each resource independently: a policy that permits 8 CPU and 32 GiB also permits 1 CPU with 32 GiB. To limit how much of a Node the sandboxes on a runner can hold in aggregate, see [Configure Node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md).
