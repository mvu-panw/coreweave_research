# Custom schedulers and third-party integrations

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/custom-schedulers

# Custom schedulers and third-party integrations

> Run Volcano, Run:ai, SkyPilot, and other schedulers on CKS

CoreWeave Kubernetes Service (CKS) is standard Kubernetes, so it runs the broad ecosystem of Kubernetes schedulers and orchestration frameworks. This page explains what you own when you install a third-party scheduler and how to keep it compatible with CKS.

For CKS built-in scheduling, see [Workload scheduling on CKS](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md) and [Scheduling profiles](https://docs.coreweave.com/products/cks/clusters/scheduling/scheduling-profiles.md). For CoreWeave's first-party Kueue distribution, see [Kueue](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue.md).

> [!WARNING]
>
> Third-party schedulers conflict with [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) by default. Before you run a third-party scheduler on a production cluster, contact [CoreWeave Support](https://docs.coreweave.com/support/contact.md) so CoreWeave can make verification Pods preemptible by it. See [Third-party schedulers and HPC Verification](#third-party-schedulers-and-hpc-verification).

## Responsibilities for third-party schedulers

CoreWeave manages platform components in the `cw-*` and other Control Plane namespaces, including the GPU device plugin, the Container Network Interface (CNI), Node lifecycle automation, and HPC Verification. CoreWeave also manages [SUNK](https://docs.coreweave.com/products/sunk.md) and the [`cks-kueue` chart](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue). See [What CoreWeave manages](https://docs.coreweave.com/support/what-coreweave-manages.md).

You own each third-party scheduler integration. That mean you install, configure, operate, and monitor it. When you use a third-party scheduler, you must:

* Deploy and maintain the scheduler.
* Pin scheduler container images to a specific tag or digest. Don't use `latest`.
* Configure multi-node GPU workloads for InfiniBand. See [Use GPUDirect RDMA](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md).
* Use instance-type and CoreWeave topology labels for GPU and topology-aware placement. See [Node type selection labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#node-type-selection-labels).
* Install and operate the observability stack that the scheduler requires in your namespaces.

Note that the Kubernetes `default-scheduler` continues to run because CoreWeave platform components depend on it.

## Third-party schedulers and HPC Verification

CoreWeave runs [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) tests on idle Nodes at the top of each hour. Verification Pods use a CoreWeave PriorityClass with a negative value (`cw-hpc-verification` at `-1`, or `cw-hpc-validation` at `-50` where CoreWeave has rolled out the new class), so the Kubernetes `default-scheduler` preempts them as soon as one of your workloads schedules onto the Node.

That preemption works only when the scheduler that placed the verification Pods is the same scheduler that places your workloads. Because verification Pods are submitted through the `default-scheduler`, a third-party scheduler doesn't treat them as candidates for preemption. This affects Volcano and the KAI Scheduler (including Run:ai).

This conflict produces the following symptoms:

* Verification Pods that linger on Nodes you expect to use.
* Workloads that stay Pending with insufficient-GPU messages during the hourly verification window.
* Topology fit failures, because verification Pods appear to consume capacity your scheduler can't reclaim.

### Make HPC Verification Pods preemptible

Scheduler-side configuration alone doesn't resolve this. CoreWeave applies a per-cluster change to how verification Pods are submitted and labeled, so that your scheduler can preempt them. The change depends on which scheduler you run and on how you configured it, so CoreWeave builds it for your cluster rather than applying a standard patch. To run a third-party scheduler on a production cluster, do the following:

1. Install and configure your scheduler, including any preemption settings it requires. See the following scheduler-specific sections.
2. To have verification Pods made preemptible by your scheduler, contact [CoreWeave Support](https://docs.coreweave.com/support/contact.md) with your cluster ID, the scheduler name and version, and its configuration.
3. After CoreWeave confirms the change, verify that one of your workloads preempts a running `hpc-verification-*` Pod on an otherwise idle Node.

## Avoid `.spec.nodeName`

Setting `.spec.nodeName` bypasses the scheduler entirely, including any custom scheduler you install. The Pod is then invisible to Kueue and to topology-aware scheduling. Use a `nodeSelector` or `nodeAffinity` to target Nodes instead. See [Workload scheduling](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#avoid-spec-nodename-for-node-targeting) for more information about avoiding `.spec.nodeName`.

## Volcano on CKS

Volcano's `preempt` action lets it preempt lower-priority Pods, and it isn't enabled by default. To turn it on, edit the existing `volcano-scheduler-configmap` ConfigMap in the namespace where you installed Volcano. Add `preempt` to the `actions` list in the `volcano-scheduler.conf` key:

```yaml theme={"system"}
data:
  volcano-scheduler.conf: |
    actions: "enqueue, allocate, backfill, preempt"
```

This configuration is necessary but not sufficient. Volcano preempts only the Pods it scheduled, so it doesn't act on verification Pods placed by the `default-scheduler`. After you update the ConfigMap, contact [CoreWeave Support](https://docs.coreweave.com/support/contact.md) to have verification Pods made preemptible by Volcano, then verify that one of your workloads preempts a running `hpc-verification-*` Pod on an otherwise idle Node.

## Run:ai and the KAI Scheduler on CKS

The KAI Scheduler is NVIDIA's open source scheduler derived from Run:ai. Like Volcano, it doesn't preempt Pods placed by the `default-scheduler`, so your workloads can't reclaim Nodes from verification Pods. Workloads submitted during the verification window report that the Node has insufficient GPU resources.

No scheduler-side configuration resolves this. As with Volcano, CoreWeave applies the per-cluster change described in [Third-party schedulers and HPC Verification](#third-party-schedulers-and-hpc-verification). For the KAI Scheduler, that change references the queue and the PriorityClass that your installation uses, so CoreWeave builds it from your configuration instead of applying a standard remedy. Contact [CoreWeave Support](https://docs.coreweave.com/support/contact.md) before you run the KAI Scheduler on a production cluster, and include your cluster ID, the scheduler version, and your queue configuration.

## SkyPilot on CKS

SkyPilot orchestrates jobs but doesn't provide its own Kubernetes scheduler. On CKS, `default-scheduler` places the Pods that SkyPilot submits. When you use Kueue, Kueue controls admission before those Pods reach the scheduler. For setup and worked examples, see [Run SkyPilot on CKS](https://docs.coreweave.com/products/cks/tutorials/skypilot.md).

A common SkyPilot misdiagnosis is reporting that Nodes disappeared when SkyPilot redeployed the cluster. Before you suspect a hardware or capacity fault, determine whether SkyPilot tore down and recreated the resources, and check the Node Pool status to confirm capacity is intact. See [Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md).

For multi-node jobs, configure InfiniBand as described in [Run SkyPilot on CKS](https://docs.coreweave.com/products/cks/tutorials/skypilot.md). Without it, multi-node jobs can fall back to Ethernet and run slowly.

## Anyscale on CKS

To run Ray and Anyscale workloads on CKS, see [Anyscale](https://docs.coreweave.com/products/cks/clusters/frameworks/anyscale.md) and [Run Ray with Kueue](https://docs.coreweave.com/products/cks/clusters/frameworks/ray-with-kueue.md).

## When to open a support ticket

Open a ticket with [CoreWeave Support](https://docs.coreweave.com/support/contact.md) in the following situations:

* You plan to run a third-party scheduler on a production cluster.
* Your workloads don't preempt verification Pods after CoreWeave applies the per-cluster change.
* A third-party scheduler interacts with CoreWeave platform automation in a way you can't resolve from your configuration.

Include your cluster ID, the scheduler name and version, its configuration, the workload manifest, and the observed behavior. See [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md).

## Related pages

* [Workload scheduling on CKS](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md): labels, taints, and the default scheduler.
* [Scheduling profiles](https://docs.coreweave.com/products/cks/clusters/scheduling/scheduling-profiles.md): the CKS scheduling profiles.
* [Kueue](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue.md): CoreWeave's supported Kueue distribution.
* [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md): how HPC Verification tests interact with your scheduler.
