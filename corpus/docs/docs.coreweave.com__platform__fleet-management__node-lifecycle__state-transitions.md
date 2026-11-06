# Node state transitions in CKS

Source: https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions

# Node state transitions in CKS

> How CoreWeave automation cordons, reboots, and replaces Nodes inside a CKS cluster

When CoreWeave's Node lifecycle automation detects an issue on a production Node during [Day 2+ operations](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md), it remediates the Node by moving it through a lifecycle state transition. That transition might be a reboot inside your cluster or a move to triage for investigation. This page explains how those transitions behave in a CoreWeave Kubernetes Service (CKS) cluster: the difference between pending and immediate transitions, the labels and conditions that mark them, the states you can observe, and how your workloads affect transition timing.

For the full lifecycle from initialization through production, see [Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md).

## Remediation categories

CoreWeave's health signals fall into two categories:

* **Solved by reboot**: The Node reboots inside your cluster and returns to service. Examples include GPU reset requests and kernel deadlocks.
* **Needs triage**: The Node leaves your cluster for investigation, repair, preventative maintenance, or vendor return. CKS delivers a replacement Node automatically.

For either category, CoreWeave matches the type of transition, pending or immediate, to the known severity of the issue.

## Pending state transitions

CoreWeave uses a pending transition when the issue's severity is uncertain and interrupting a running workload would be worse than waiting. A pending transition works as follows:

1. CKS sets the `node.coreweave.cloud/pending-state` label on the Node to the target state, such as `production-reboot`, and updates the `PendingPhaseState` Node condition. The condition's `reason` names the target state, and its `message` describes what triggered the transition.
2. CKS cordons the Node so no new workloads schedule onto it, and records the reason, `NLCCPendingExitProduction`, in the `node.coreweave.cloud/cordonReason` annotation. See [Node cordoning](https://docs.coreweave.com/products/cks/nodes/cordon.md).
3. The transition waits for [non-interruptible workloads to finish](#active-nodes-and-stalled-transitions). While these workloads are still running, the Node emits `CWNCPhasePendingTenantWorkloadRunning` events that name the Pods preventing the transition.
4. CKS drains the remaining Pods. Gracefully interruptible Pods delay the maintenance action until they terminate or their termination grace period expires; interruptible Pods don't. The state transition then proceeds and the action takes place.

Non-interruptible workloads keep running while the transition is pending. Once they finish, CKS can drain the remaining Pods. The transition can proceed even while `CWActive` is `True`, subject to the gracefully interruptible wait described above.

## Immediate state transitions

CoreWeave uses an immediate transition when the issue is known to be fatal or to severely degrade performance, such as a confirmed hardware fault or thermal throttling. In these cases, waiting doesn't protect your workload, because the workload is already failing or running on broken hardware.

An immediate transition doesn't wait for the Node to become idle. The Node leaves the `production` state and CKS begins evicting Pods right away. Pods labeled [`qos.coreweave.com/graceful-interruptible`](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling#gracefully-interruptible) block the action until they terminate or their `terminationGracePeriodSeconds` expires; all other Pods are evicted without a waiting period, even if a pending transition would normally wait for them.

## Active Nodes and stalled transitions

A pending transition waits for non-interruptible workloads to finish before CKS starts draining the Node. This maintenance check differs from the `CWActive` condition used for Node Pool scale-down. For the maintenance check:

* `DaemonSet` Pods never count as active.
* Pods labeled `qos.coreweave.cloud/interruptable: "true"` don't count as active.
* Pods labeled `qos.coreweave.com/graceful-interruptible: "true"` don't prevent CKS from starting the drain once non-interruptible workloads finish. They do delay the maintenance action until they terminate or their `terminationGracePeriodSeconds` expires after the deletion request. See [Pod interruption and eviction policies](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#pod-interruption-and-eviction-policies).
* Control plane Pods can block a pending transition. The maintenance check does not exclude Pods in namespaces labeled `ns.coreweave.cloud/org=control-plane`.
* Any other Pod in the `Running` phase counts as active.

The separate [`CWActive` idle rules](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools#idle-nodes) mean a Node can show `CWActive = True` while a pending transition proceeds. A Node can also show `CWActive = False` while a running control plane Pod blocks the transition.

> [!WARNING]
>
> **Crash-looping Pods stall pending transitions.**
>
> A Pod in `CrashLoopBackOff` keeps its `.status.phase` set to `Running`, even though `kubectl` reports its status as `CrashLoopBackOff`. Because the phase stays `Running`, CKS still counts the Pod as active. If a Deployment keeps restarting a crashed Pod on a Node with a pending transition, the Node stays cordoned indefinitely: the hardware issue prevents the Pod from running, and the restarting Pod prevents the remediation. SUNK avoids this for its `slurmd` Pods: the SUNK Syncer sets the [`qos.coreweave.cloud/interruptable`](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling#interruptible) label to `true` whenever no Slurm job is running on the Pod, so an idle `slurmd` Pod doesn't count as active. While a Slurm job runs on the Pod, the label is `false` and the Pod counts as active, so the transition waits for the job.
>
> If a Node in your cluster is stuck with a pending state and a crash-looping Pod, delete the Pod or apply an [interruptible label](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#pod-interruption-and-eviction-policies) so the transition can proceed.

## Node states in a CKS cluster

Every Node carries a `node.coreweave.cloud/state` label with its current lifecycle state and, during a pending transition, a `node.coreweave.cloud/pending-state` label with the target state. The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) shows both in the `STATE` and `PENDING STATE` columns of `cwic node get`. See [View Node details](https://docs.coreweave.com/products/cks/nodes/manage.md#view-node-details).

The states you are most likely to observe on Nodes in your cluster are:

| State | Description |
| - | - |
| `production` | The Node is in service and accepts workloads. Healthy Nodes show this state with no pending state. |
| `production-reboot` | The Node reboots inside your cluster, then returns to `production` and accepts workloads. An [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test runs after the reboot, but the Node doesn't wait for it. If the reboot doesn't complete, the Node moves to `production-reboot-fail`. |
| `production-collect-reboot` | The same as `production-reboot`, but CoreWeave collects diagnostic data from the Node before rebooting it. |
| `production-powercycle` | A variant of the reboot flow that fully power cycles the Node, including its Data Processing Unit (DPU), instead of rebooting it. |
| `production-powerreset` | A variant of the reboot flow that power resets the Node's server while its DPU stays powered on. |
| `triage` | CoreWeave has sidelined the Node for investigation or repair. For a pending move to triage, CKS waits for non-interruptible workloads to finish, then drains the remaining Pods before the Node leaves your cluster. An immediate move, such as for `GPUFallenOffBus`, ends running workloads right away. CKS delivers a replacement. |
| `production-triage` | CoreWeave investigates the Node while it remains in your Node Pool, without first returning it to CoreWeave's fleet. |

Bare Metal Service customers can also request `production-triage` through the Bare Metal triage API. In CKS, CoreWeave manages this transition. Use only documented Node procedures.

Nodes also pass through [Day 1 states](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day1.md) such as Zap and Test before they reach production, but those states occur before a Node joins your cluster.

Use only documented procedures to change [CoreWeave-managed Node metadata](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#coreweave-managed-node-metadata).

## Example: a pending reboot

The following sequence shows a typical pending reboot, using a GPU reset request as the trigger:

1. The NVIDIA driver reports that a GPU needs a reset, for example because of a pending memory row remap. CoreWeave monitoring sets the `GPUWantsReset` condition on the Node.
2. The Node moves to the `production-reboot` pending state. The Node emits a `CWNCPhaseNccPendingChange` event that names the condition that triggered the transition, sets the `node.coreweave.cloud/pending-state` label, and updates the `PendingPhaseState` condition.
3. CKS cordons the Node. Your existing workloads keep running, and the Node emits `CWNCPhasePendingTenantWorkloadRunning` events while they do.
4. Once non-interruptible workloads finish, CKS drains the remaining Pods and reboots the Node inside your cluster, waiting for gracefully interruptible Pods to terminate or reach their termination grace period.
5. After the reboot, the Node returns to `production` and CKS uncordons it. An HPC Verification test runs after that, but the Node doesn't wait for it. The test needs the Node's GPUs free, so a workload scheduled right away can stop it or prevent it from starting. If the reboot doesn't complete in time, the Node moves to `production-reboot-fail`.

To inspect a transition in progress, describe the Node and review its conditions and events:

```bash theme={"system"}
kubectl describe node [NODE-NAME]
```

Replace `[NODE-NAME]` with the name of your Node.

To follow only the Node's events as a transition progresses, watch them instead of repeatedly describing the Node:

```bash theme={"system"}
kubectl events --for=node/[NODE-NAME] --watch
```

## Triage transitions

When CoreWeave determines that a Node needs investigation rather than a reboot, the Node moves toward the `triage` state:

1. CoreWeave's Node lifecycle automation sets a condition such as `NeedsTriage` on the Node. The Node receives a `NoSchedule` taint and is cordoned, so no new workloads schedule onto it.
2. For a pending triage transition, CKS ordinarily waits for non-interruptible workloads to finish before draining the remaining Pods. If the Node is in the [prefill flow](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#how-prefill-works), CKS can start draining it when the prefill timeout expires, even if workloads are still running.
3. CKS removes the Node from your cluster and returns it to CoreWeave's fleet for remediation. CoreWeave re-validates the Node before it can return to any production fleet; a Node that needs the full onboarding test suite takes roughly 48 hours to return.
4. CKS delivers a replacement Node to your Node Pool automatically. Prefill can deliver the replacement before the old Node leaves.

[Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) provisions the replacement before the old Node drains, so the Node Pool stays at its target capacity throughout. Without prefill, the replacement arrives after the old Node is removed, which can leave a capacity gap of 20 to 40 minutes.

## Prepare your workloads for transitions

How quickly a transition completes depends on how your workloads signal their tolerance for interruption:

* **Stateless workloads**: Apply the `qos.coreweave.cloud/interruptable` label so CKS excludes the Pods from the Node's active status. Pending transitions proceed without waiting for these Pods. See [Interruptible](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#interruptible).
* **Stateful workloads that need cleanup time**: Apply the `qos.coreweave.com/graceful-interruptible` label so reboots and deferred maintenance wait until the Pod terminates or its `terminationGracePeriodSeconds` expires. This period defaults to 30 seconds; set it longer than your workload's expected cleanup time. Node Pool removal has a separate drain deadline. See [Gracefully interruptible](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#gracefully-interruptible) and [Pod termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) in the Kubernetes documentation.
* **Critical jobs**: Leave both labels off. CKS ordinarily defers pending transitions until the job completes. For Nodes in the prefill flow, timeout expiry can still start a drain while the job is running; see [Triage transitions](#triage-transitions). Deferring a transition also defers remediation, as described in [Long-running GPU Pods](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#long-running-gpu-pods).
* **Capacity-sensitive Node Pools**: Enable [Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) so replacements arrive before triaged Nodes drain.

## See also

* [Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md): The full lifecycle from Day 0 through Day 2+.
* [Node cordoning](https://docs.coreweave.com/products/cks/nodes/cordon.md): Common cordon reasons and how to respond.
* [Workload scheduling on CKS](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md): Eviction strategies, labels, and taints.
* [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md): Request safe or immediate reboots manually.
* [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md): Node conditions and events set by CKS.
