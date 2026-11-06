# Reboot Nodes

Source: https://docs.coreweave.com/products/cks/nodes/reboot

# Reboot Nodes

> Request safe and immediate reboots of CKS Nodes with the CoreWeave Intelligent CLI, kubectl, or the Kubernetes API

This guide explains how to manually reboot CKS Nodes, including how to choose between safe and immediate reboots and how to cancel a reboot that hasn't started yet.

You can manually reboot Nodes in two ways:

* **Standard Node reboot**: A typical reboot to apply a system update or other change.
* **Reconfigure reboot**: A reboot to apply an updated [Node Pool configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration) to existing Nodes.

This guide covers standard Node reboots. To reboot Nodes to apply Node Pool configuration updates, see [Apply Node Pool Configuration Updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md).

Nodes are managed as part of CoreWeave's
[Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md).
The [CoreWeave Node lifecycle controller](https://docs.coreweave.com/glossary.md#coreweave-node-lifecycle-controller) coordinates *required* reboots. For most faults it waits for your workloads to finish, but critical faults reboot the Node immediately. To learn how CoreWeave-initiated reboots behave, see [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md).

## Reboot options

You can request a reboot in the following ways:

| Method | Use it when |
| - | - |
| [CoreWeave Intelligent CLI](#request-a-node-reboot) | You want the shortest command and built-in safety checks. This is the recommended method. |
| [`kubectl`](#request-a-node-reboot) | You manage the cluster with `kubectl` and don't want to install the CoreWeave Intelligent CLI. |
| [Kubernetes API](#request-a-node-reboot) | You don't have `kubectl` available, or you're automating reboots from a system that already uses the Kubernetes API. |

### Safe versus immediate reboots

Before you request a reboot, choose the right reboot option. You can reboot a Node whether it's active or idle.

* **Safe reboot**: A safe reboot marks the Node to reboot after non-interruptible workloads finish. CKS requests a cordon to prevent new workload scheduling, then drains the Node before rebooting it.
* **Immediate reboot**: An immediate reboot reboots the Node without waiting for active workloads to stop. It still waits for [gracefully interruptible](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#gracefully-interruptible) Pods to terminate or reach their `terminationGracePeriodSeconds`.

A safe reboot follows the [pending-transition workload rules](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#active-nodes-and-stalled-transitions), so it can proceed while the separate [`CWActive` condition](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools#idle-nodes) is `True`.

After the Node reboots and rejoins the cluster, it returns to the `production` state and accepts customer workloads. CoreWeave triggers an [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test after the reboot, but the Node doesn't wait for the result. The test needs the Node's GPUs free, so a workload scheduled right away either stops a running test or prevents it from starting.

## Prerequisites

Before you begin a Node reboot, ensure you have the following:

* An active CoreWeave account.
* An [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md).
* [`kubectl`](https://kubernetes.io/docs/tasks/tools/) installed locally, if you use the `kubectl` method.

Depending on the method you use to reboot Nodes, confirm the following:

> [tab] CoreWeave Intelligent CLI
>
> Install the latest version of the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic).

> [tab] kubectl and Kubernetes API
>
> You need permission to get Nodes and to patch the `status` subresource of Nodes. To cancel a pending reboot, you also need permission to patch Nodes. Verify your permissions:
>
> ```bash theme={"system"}
> kubectl auth can-i get nodes
> kubectl auth can-i patch nodes --subresource=status
> kubectl auth can-i patch nodes
> ```
>
> Each command must return `yes`. You only need the `patch nodes` permission to cancel a pending reboot.

## Check the Node before rebooting

Only reboot a Node that is in the `production` lifecycle state. Don't manually request a reboot while a Node is transitioning between lifecycle states, because the reboot request can conflict with the transition that CoreWeave already has in progress.

The examples in this guide use a `NODE` environment variable. Replace `[NODE-NAME]` with the name of the Node you want to reboot:

```bash theme={"system"}
export NODE="[NODE-NAME]"
```

**1. Check the Node lifecycle state**

Run the following:

```bash theme={"system"}
kubectl get node "${NODE}" \
  -o jsonpath='{.status.conditions[?(@.type=="PhaseState")].reason}{"\n"}'
```

Continue only if the command returns `production`:

```text title="Example output" theme={"system"}
production
```

**2. Check for active workloads**

Run the following:

```bash theme={"system"}
kubectl get node "${NODE}" \
  -o jsonpath='{.status.conditions[?(@.type=="CWActive")].status}{"\n"}'
```

Interpret `CWActive` using the [idle Node rules](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes). Before you request an immediate reboot, check the Node's Pods. An immediate reboot can interrupt running workloads. For the workload types a safe reboot waits on, see [Active Nodes and stalled transitions](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#active-nodes-and-stalled-transitions).

If you have the CoreWeave Intelligent CLI, you can also check a Node's active status with the `cwic node get` command. Read the `ACTIVE` column, which reflects `CWActive`. Don't use the `READY` column, which reflects the Kubernetes `Ready` condition and is `true` on idle Nodes as well.

**3. Check customer-applied taints**

Inspect the Node's taints:

```bash theme={"system"}
kubectl get node "${NODE}" -o jsonpath='{.spec.taints}{"\n"}'
```

If you find a customer-applied `NoExecute` taint, change its effect to `NoSchedule` before you reboot. Update the Node or Node Pool configuration that manages it. Leave CoreWeave-managed taints unchanged. Customer-applied `NoExecute` taints can block post-reboot health verification, which leaves the Node unverified after it returns to `production`. See [Customer taints and HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#taints).

## Request a Node reboot

Choose one of the following methods to request a reboot.

> [tab] CoreWeave Intelligent CLI
>
> To use the CoreWeave Intelligent CLI to reboot a Node, run the following command, choosing a flag from the following list and replacing `[NODE-NAMES]` with a space-separated list of Nodes you want to reboot:
>
> ```bash theme={"system"}
> cwic node reboot [--safe|--force|--unset] [NODE-NAMES]
> ```
>
> The `--safe` flag queues a safe reboot, and the `--unset` flag cancels a pending safe reboot. The `--force` flag, or its alias `--yes`, requests an immediate reboot without prompting.
>
> Without a flag, `cwic node reboot` requests an immediate reboot. If any of the Nodes are active, it prompts you with three options:
>
> ```text title="Example output" theme={"system"}
> The following 2 nodes are currently Active (running non-preemptible workloads):
>   - node-1
>   - node-2
>
> Options:
>   [Y]es - Proceed with immediate reboot (may disrupt workloads)
>   [S]afe - Switch to safe reboot (waits for workloads to terminate)
>   [N]o - Cancel reboot
>
> Choose an option [Y/s/n]:
> ```
>
> For a safe reboot, `CWActive` can remain `True` while the maintenance wait completes. Enter `S` to switch to a safe reboot, which waits for non-interruptible workloads to finish before draining the Node. Gracefully interruptible Pods can then delay the reboot until they terminate or their termination grace period expires. Pressing Enter accepts the default, `Y`, and requests an immediate reboot.
>
> The CoreWeave Intelligent CLI refuses to reboot a Node that isn't in the `production` state, so you don't need to check the lifecycle state yourself.
>
> For example, to request an immediate reboot for the Nodes `node-1` and `node-2` without a confirmation prompt, run:
>
> ```bash theme={"system"}
> cwic node reboot --force node-1 node-2
> ```
>
> Adding a reason for the reboot is optional, but recommended. To set a message for the reboot, use the `--message` flag. For example, run:
>
> ```bash theme={"system"}
> cwic node reboot --message "Reason for this reboot" node-1 node-2
> ```
>
> Run `cwic node reboot --help` for more information.

> [tab] kubectl
>
> You can request a reboot with `kubectl`. A reboot request is a patch to the Node's `status` subresource that sets a lifecycle condition. Before you patch a Node, [check the Node](#check-the-node-before-rebooting).
>
> > [!WARNING]
> >
> > Use a [strategic merge patch](https://docs.coreweave.com/products/cks/nodes/cordon.md#patch-node-conditions-safely) to preserve the Node's other conditions.
>
> ### Request a safe reboot
>
> A safe reboot sets the `PendingPhaseState` condition and waits for non-interruptible workloads to finish before draining and rebooting the Node:
>
> ```bash theme={"system"}
> kubectl patch node "${NODE}" \
>   --type=strategic \
>   --subresource=status \
>   -p '{
>     "status": {
>       "conditions": [
>         {
>           "type": "PendingPhaseState",
>           "status": "True",
>           "reason": "production-powerreset",
>           "message": "Customer-requested safe reboot"
>         }
>       ]
>     }
>   }'
> ```
>
> The reboot remains pending until CKS determines that the Node can be rebooted.
>
> ### Request an immediate reboot
>
> An immediate reboot sets the `PhaseState` condition and starts without waiting for active workloads to stop:
>
> ```bash theme={"system"}
> kubectl patch node "${NODE}" \
>   --type=strategic \
>   --subresource=status \
>   -p '{
>     "status": {
>       "conditions": [
>         {
>           "type": "PhaseState",
>           "status": "True",
>           "reason": "production-powerreset",
>           "message": "Customer-requested immediate reboot"
>         }
>       ]
>     }
>   }'
> ```
>
> > [!WARNING]
> >
> > An immediate reboot interrupts any workloads running on the Node. Only gracefully interruptible Pods delay it, until they terminate or their grace period expires.

> [tab] Kubernetes API
>
> If you don't have `kubectl` available, call the Node `status` endpoint directly. A reboot request is a patch to the Node's `status` subresource that sets a lifecycle condition. Before you patch a Node, [check the Node](#check-the-node-before-rebooting).
>
> > [!WARNING]
> >
> > Use a [strategic merge patch](https://docs.coreweave.com/products/cks/nodes/cordon.md#patch-node-conditions-safely) to preserve the Node's other conditions.
>
> Replace the following placeholders:
>
> * `[APISERVER-URL]`: The Kubernetes API server URL from your kubeconfig.
> * `[API-ACCESS-TOKEN]`: An [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md) authorized to patch `nodes/status`.
> * `[NODE-NAME]`: The name of the Node you want to reboot.
>
> ```bash theme={"system"}
> export APISERVER="[APISERVER-URL]"
> export API_ACCESS_TOKEN="[API-ACCESS-TOKEN]"
> export NODE="[NODE-NAME]"
> ```
>
> ### Request a safe reboot
>
> ```bash theme={"system"}
> curl --fail-with-body --request PATCH \
>   "${APISERVER}/api/v1/nodes/${NODE}/status" \
>   -H "Authorization: Bearer ${API_ACCESS_TOKEN}" \
>   -H "Content-Type: application/strategic-merge-patch+json" \
>   --data '{
>     "status": {
>       "conditions": [
>         {
>           "type": "PendingPhaseState",
>           "status": "True",
>           "reason": "production-powerreset",
>           "message": "Customer-requested safe reboot"
>         }
>       ]
>     }
>   }'
> ```
>
> ### Request an immediate reboot
>
> ```bash theme={"system"}
> curl --fail-with-body --request PATCH \
>   "${APISERVER}/api/v1/nodes/${NODE}/status" \
>   -H "Authorization: Bearer ${API_ACCESS_TOKEN}" \
>   -H "Content-Type: application/strategic-merge-patch+json" \
>   --data '{
>     "status": {
>       "conditions": [
>         {
>           "type": "PhaseState",
>           "status": "True",
>           "reason": "production-powerreset",
>           "message": "Customer-requested immediate reboot"
>         }
>       ]
>     }
>   }'
> ```

### Reboot request reference

Refer to the following table when rebooting with `kubectl` or the Kubernetes API:

| Condition type | Status | Reason | Behavior |
| - | - | - | - |
| `PendingPhaseState` | `True` | `production-powerreset` | Waits for non-interruptible workloads to finish, then drains and reboots the Node. |
| `PhaseState` | `True` | `production-powerreset` | Reboots the Node immediately. |

For reboot automation, we recommend using the CoreWeave Intelligent CLI. Follow the [CoreWeave-managed Node metadata guidance](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#coreweave-managed-node-metadata).

The condition `type`, `status`, and `reason` fields form the reboot request contract and must use the values shown in the preceding table. The `message` field is descriptive. Use it to record the source or purpose of the request.

## Monitor the reboot

To watch the Node's lifecycle and readiness conditions, run:

```bash theme={"system"}
watch "kubectl get node \"${NODE}\" -o custom-columns='NAME:.metadata.name,STATE:.status.conditions[?(@.type==\"PhaseState\")].reason,PENDING:.status.conditions[?(@.type==\"PendingPhaseState\")].reason,READY:.status.conditions[?(@.type==\"Ready\")].status'"
```

During the reboot, the Node becomes unavailable and its readiness state changes. The reboot is complete when:

* The `State` reason returns to `production`.
* The Kubernetes `Ready` condition is `True`.
* Your workloads can be scheduled or resumed as expected.

The Node returns to `production` as soon as the reboot completes. The post-reboot [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test runs after that, so let it finish before scheduling workloads onto the Node. The test needs the Node's GPUs free: a workload that lands first prevents it from starting, and one that lands mid-test stops it.

## Cancel a pending reboot

You can cancel a safe reboot while it's still pending. A pending reboot has no timeout: it waits indefinitely until no workloads block the transition, so a pending request can remain in place for a long time. Cancel the request if you no longer want the Node to reboot.

You can't cancel a reboot after the Node starts rebooting, and you can't cancel an immediate reboot, because an immediate reboot doesn't wait before it starts. If a Node has already begun rebooting, wait for it to return to the `production` state.

To confirm that the reboot is still pending, run:

```bash theme={"system"}
kubectl get node "${NODE}" \
  -o jsonpath='{.status.conditions[?(@.type=="PendingPhaseState")].reason}{"\n"}'
```

If the command returns `production-powerreset`, the reboot is still pending and you can cancel it.

> [tab] CoreWeave Intelligent CLI
>
> To cancel a pending safe reboot, run the following command, replacing `[NODE-NAMES]` with a space-separated list of Nodes:
>
> ```bash theme={"system"}
> cwic node reboot --unset [NODE-NAMES]
> ```
>
> The `--unset` flag clears both the pending reboot condition and the pending state label.

> [tab] kubectl
>
> Run the following commands to cancel a pending reboot with `kubectl`. You must complete both steps. If you clear the condition without clearing the label, the Node can retain a stale pending state.
>
> **1. Clear the pending reboot condition**
>
> ```bash theme={"system"}
> kubectl patch node "${NODE}" \
>   --type=strategic \
>   --subresource=status \
>   -p '{
>     "status": {
>       "conditions": [
>         {
>           "type": "PendingPhaseState",
>           "status": "False",
>           "reason": "none",
>           "message": "Customer canceled the pending reboot"
>         }
>       ]
>     }
>   }'
> ```
>
> **2. Clear the pending state label**
>
> ```bash theme={"system"}
> kubectl label node "${NODE}" \
>   node.coreweave.cloud/pending-state=none --overwrite
> ```
>
> **3. Verify that the cancellation applied**
>
> ```bash theme={"system"}
> kubectl get node "${NODE}" \
>   -o custom-columns='NAME:.metadata.name,PENDING:.status.conditions[?(@.type=="PendingPhaseState")].reason,PENDING_LABEL:.metadata.labels.node\.coreweave\.cloud/pending-state'
> ```
>
> Both `PENDING` and `PENDING_LABEL` must return `none`.

## Troubleshooting

### The API returns 403 Forbidden

Your Kubernetes identity doesn't have permission to patch the Node status. If you're canceling a pending reboot, you need permission to patch both the Node and its `status` subresource.

To verify your permissions, run:

```bash theme={"system"}
kubectl auth can-i patch nodes --subresource=status
kubectl auth can-i patch nodes
```

Ask your cluster administrator to grant the minimum required permission.

### The Node doesn't reboot

Check that:

* The Node was in the `production` state when you submitted the request.
* The patch was applied to the `status` subresource.
* The condition type and reason use the values in [Reboot request reference](#reboot-request-reference).
* A safe reboot isn't waiting for non-interruptible workloads to finish or for gracefully interruptible Pods to terminate or reach their deletion deadline.

To inspect the relevant conditions, run:

```bash theme={"system"}
kubectl get node "${NODE}" \
  -o jsonpath='{range .status.conditions[*]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```

### A canceled reboot still occurs

Check that both the condition and the label were cleared:

```bash theme={"system"}
kubectl get node "${NODE}" \
  -o custom-columns='PENDING:.status.conditions[?(@.type=="PendingPhaseState")].reason,PENDING_LABEL:.metadata.labels.node\.coreweave\.cloud/pending-state'
```

If either value isn't `none`, repeat the cancellation steps. A reboot that has already started can't be canceled. [Contact CoreWeave Support](https://docs.coreweave.com/support.md) if the Node reboots after both values return `none`.

### The Node stays in `production-powerreset`

Check for customer-applied `NoExecute` taints on the Node:

```bash theme={"system"}
kubectl get node "${NODE}" -o jsonpath='{.spec.taints}{"\n"}'
```

HPC Verification Pods don't tolerate `NoExecute` taints. These taints can prevent verification Pods from scheduling or evict them after they start, which leaves the Node unverified rather than holding it in a reboot state. CoreWeave might delete and replace a Node that remains in `production-powerreset` or `production-reboot` too long.

Change taints to `NoSchedule` in the Node or Node Pool configuration that manages them. Verification Pods tolerate `NoSchedule`, so checks can run while Pods without matching tolerations stay off the Node. Leave CoreWeave-managed taints unchanged.

If verification doesn't start, check whether its controller Pod remains `Pending` in the `cw-hpc-verification` namespace. The controller must schedule before test Pods can start. To inspect scheduling events and collect details for Support, see [The verification controller Pod stays Pending](https://docs.coreweave.com/support/platform/articles/troubleshoot-hpc-verification#the-verification-controller-pod-stays-pending).

To request verification on an idle Node that has returned to `production`, follow [Verify a Node on demand](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#verify-a-node-on-demand). Allow verification to finish before scheduling GPU workloads. If verification still can't run, contact CoreWeave Support.

### The Node doesn't return to Ready

To collect the Node conditions and recent events, run:

```bash theme={"system"}
kubectl describe node "${NODE}"
```

[Contact CoreWeave Support](https://docs.coreweave.com/support.md) if the `PhaseState` doesn't return to `production` or the Node remains unavailable after the expected reboot interval. Include the following information:

* The cluster name.
* The Node name.
* The time when you submitted the reboot request.
* Whether you requested a safe or immediate reboot.
* The output of `kubectl describe node`.
