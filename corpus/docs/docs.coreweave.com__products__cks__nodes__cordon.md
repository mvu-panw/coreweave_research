# Node cordoning

Source: https://docs.coreweave.com/products/cks/nodes/cordon

# Node cordoning

> Cordon CKS Nodes yourself and understand why CoreWeave cordons Nodes

This guide explains what Node cordoning is, how to cordon a Node yourself, why CoreWeave cordons Nodes, and how to respond when a Node is cordoned.

## What is Node cordoning?

In Kubernetes, a cordoned Node prevents new workloads from scheduling onto it. Existing workloads on the Node continue to run until you explicitly drain them or they complete. Cordoning typically indicates maintenance, troubleshooting, or reliability actions.

Both you and CoreWeave can cordon Nodes. You can cordon a Node to isolate it while you troubleshoot or perform your own maintenance. CoreWeave cordons Nodes proactively to ensure reliability, maintain cluster health, and manage maintenance activities with minimal impact on workloads.

## Cordon a Node yourself

Choose the cordon method that matches how long the isolation needs to last:

* Use [`cwic node cordon`](#cordon-with-the-coreweave-intelligent-cli) when you want the cordon integrated with CoreWeave tooling and recorded in the cordon reason annotation. This is the preferred method.
* Use [`kubectl cordon`](#cordon-with-kubectl) for quick, short-lived cordons.
* Use a [custom taint](#isolate-a-node-long-term-with-a-custom-taint) when isolation must survive Node reboots. A taint applied directly to a Node doesn't carry over to a replacement Node.

> [!WARNING]
>
> Don't set the `node.coreweave.cloud/cordonReason` annotation yourself. The annotation is informational output that CoreWeave automation writes when it cordons a Node. Setting it manually doesn't cordon the Node, and it can cause automation to uncordon the Node when it reconciles the annotation. For a manual cordon, use one of the methods in this section and follow the [CoreWeave-managed Node metadata guidance](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#coreweave-managed-node-metadata).

### Cordon with the CoreWeave Intelligent CLI

The preferred way to cordon a Node is the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) `node cordon` command. To install and authenticate the CLI, see [Manage Node Pools](https://docs.coreweave.com/products/cks/nodes/manage.md#use-coreweave-intelligent-cli).

```bash theme={"system"}
cwic node cordon [NODE-NAME]
```

Replace `[NODE-NAME]` with the name of your Node. You can pass multiple Node names separated by spaces. To record why you cordoned the Node, add a reason and a message:

```bash theme={"system"}
cwic node cordon -r "[REASON]" -m "[MESSAGE]" [NODE-NAME]
```

Replace `[REASON]` with a brief reason and `[MESSAGE]` with a longer description. Both are recorded on the Node's `AdminTemporaryFailure` condition. If you can't use the CLI, you can [set the condition with `kubectl patch`](#set-admintemporaryfailure-on-a-node) instead.

`cwic node cordon` sets the `AdminTemporaryFailure` Node condition, which CoreWeave automation recognizes as an intentional manual cordon and leaves in place. The Node's `node.coreweave.cloud/cordonReason` annotation reports `AdminTemporaryFailure`, so anyone who inspects the Node can see that it was cordoned manually.

To clear your manual cordon, run:

```bash theme={"system"}
cwic node uncordon [NODE-NAME]
```

Other active cordon reasons can keep the Node cordoned. Check the [cordon reason](#check-why-a-node-is-cordoned) before returning workloads to it.

> [!NOTE]
>
> The `AdminTemporaryFailure` condition clears when the Node reboots. The Node can remain cordoned for other reasons. If your scheduling restriction must survive reboots, use a [custom taint](#isolate-a-node-long-term-with-a-custom-taint).

### Cordon with `kubectl`

You can also use a standard Kubernetes cordon:

```bash theme={"system"}
kubectl cordon [NODE-NAME]
```

A plain `kubectl cordon` sets only the Node's `unschedulable` flag, with no CoreWeave-recognized reason behind it. CoreWeave automation manages this flag during Node lifecycle operations, so it can clear your cordon. For example, automation uncordons a Node when its CoreWeave-recognized cordon conditions clear, and a plain cordon doesn't survive a Node reboot because the Node uncordons itself when it boots. When the cordon matters for more than a brief period, prefer `cwic node cordon` or a custom taint.

To remove the cordon, run:

```bash theme={"system"}
kubectl uncordon [NODE-NAME]
```

### Isolate a Node long-term with a custom taint

For long-term isolation, apply a custom taint with the `NoSchedule` effect instead of a cordon:

```bash theme={"system"}
kubectl taint nodes [NODE-NAME] [TAINT-KEY]=true:NoSchedule
```

Replace `[TAINT-KEY]` with a key you own, such as `example.com/maintenance-hold`. Keep your custom key outside the `*.coreweave.cloud` and `*.coreweave.com` domains to avoid conflicting with CoreWeave-managed taints.

CoreWeave automation preserves a custom taint that you apply directly to the Node if its key and effect aren't managed through the Node Pool. Use a dedicated key that isn't also configured in the Node Pool's `spec.nodeTaints`. The taint persists across reboots while the same Kubernetes Node object exists. If CoreWeave replaces the Node or deletes and recreates its Node object during remediation, the taint doesn't carry over. Apply the taint to the replacement Node if it also needs isolation.

To remove the taint from the current Node, run:

```bash theme={"system"}
kubectl taint nodes [NODE-NAME] [TAINT-KEY]=true:NoSchedule-
```

Like a cordon, a `NoSchedule` taint prevents new Pods from scheduling onto the Node without evicting the Pods already running there. Pods that tolerate the taint can still schedule onto the Node. A taint by itself doesn't cause `SchedulingDisabled` to appear in `kubectl get nodes` output the way a cordon does. Check a Node's taints with `kubectl describe node`.

> [!WARNING]
>
> Use `NoSchedule` to prevent new scheduling while keeping existing Pods running. A `NoExecute` taint also evicts running Pods that don't tolerate it, which can interrupt your workloads, and it can block HPC Verification after a reboot. See [Taints](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#taints).

## Reasons CoreWeave cordons Nodes

The following sections describe the reasons CoreWeave might cordon Nodes.

### Maintenance and updates

CoreWeave cordons Nodes that require hardware maintenance, kernel updates, or hardware replacements to avoid scheduling new workloads. This practice allows maintenance activities without disrupting running workloads.

### Health monitoring

CoreWeave monitors Node health and performance. If a Node exhibits issues that could affect workload reliability, CoreWeave may cordon it to prevent new workloads from being scheduled. These issues can include:

* **Hardware issues:** GPU hardware errors trigger automatic Node cordoning and rebooting, or an immediate move to triage for faults such as a GPU falling off the PCI bus.
* **Kernel deadlocks:** Severe kernel issues may also cause Nodes to reboot and remain cordoned until resolved.
* **InfiniBand or Ethernet link flaps:** CoreWeave cordons Nodes with unstable network connections (intermittent connectivity) so workloads aren't placed on unreliable Nodes. This detection looks for instability, so a link that fails cleanly and stays down doesn't cordon the Node. If a Node keeps running but delivers less network bandwidth than you expect, [contact support](https://docs.coreweave.com/support.md) with the Node name.
* **Connectivity failures:** If Kubernetes detects critical network issues, CoreWeave cordons the affected Nodes until stability is restored.

### Time synchronization

CKS Nodes synchronize time to CoreWeave's internal time infrastructure. CoreWeave monitors time on all Nodes, and a Node whose clock drifts beyond acceptable bounds may be cordoned for triage. Running any competing time daemon (including `chrony`, `ntpd`, `systemd-timesyncd`) directly on a Node or in containers may cause clock drift and trigger this behaviour. Overriding the time servers on CKS Nodes is not supported. Containers with time daemons must be configured to disable the daemon and/or prevent the daemon from altering the kernel clock.

### Temporary issues

Temporary issues detected through Kubernetes health checks can lead to short-term Node cordoning. These usually resolve automatically, and Nodes become schedulable again without intervention.

### Scheduled maintenance

CoreWeave intentionally cordons Nodes during scheduled maintenance.

### Lifecycle management

CoreWeave manages [Node lifecycle events](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md), such as provisioning, decommissioning, reboots, and upgrades. Temporary cordoning may occur when Nodes transition between different operational states to maintain cluster stability and reliability during lifecycle transitions. To understand how these transitions behave inside your cluster, see [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md).

Before removing a Node from the cluster, CKS cordons it and drains its workloads so they can be rescheduled onto healthy Nodes.

## Check why a Node is cordoned

When CoreWeave cordons a Node, it records the reason in the `node.coreweave.cloud/cordonReason` annotation. Check this annotation to understand whether the cordon is an expected maintenance action or a possible sign of poor Node health.

Read the cordon reason for a Node:

```bash theme={"system"}
kubectl get node [NODE-NAME] -o jsonpath='{.metadata.annotations.node\.coreweave\.cloud/cordonReason}'
```

Replace `[NODE-NAME]` with the name of your Node.

For the Node's full status, including whether it is unschedulable and its current conditions, use `describe`:

```bash theme={"system"}
kubectl describe node [NODE-NAME]
```

For lifecycle reasons such as `NLCCPendingExitProduction`, the matching Node condition message names the state the Node is moving to and what initiated the transition. A username identifies a CoreWeave engineer who started it by hand, while a message such as `Reboot from Slurm` identifies automation:

```text title="Example condition" theme={"system"}
NLCCPendingExitProduction   True   Reason: triage
Message: PendingPhaseState transition out of production to triage by user <username>
```

## Common cordon and drain reasons

The following table lists the cordon reasons you are most likely to see on a CKS Node, what each one means, and whether it represents an expected maintenance action or a possible health issue.

| Cordon reason | What it means | Maintenance or health signal | What to do |
| - | - | - | - |
| `NLCCPendingExitProduction` | The [CoreWeave Node lifecycle controller](https://docs.coreweave.com/glossary.md#coreweave-node-lifecycle-controller) is removing the Node from production for a planned reason, such as maintenance, firmware testing, hardware investigation, a reboot, or a move to triage. The Node is cordoned while non-interruptible workloads finish, then CKS drains the remaining Pods. | Lifecycle transition. Read the condition message to identify what triggered it. | No action is required. Let your workloads finish, or move them when you are ready. Don't uncordon the Node, because CoreWeave automation reapplies the cordon. After the maintenance drain, CoreWeave completes the transition named in the condition message: for a reboot or a rolling update, the Node returns to service; for a move to triage, it leaves the cluster and CoreWeave delivers a replacement. |
| `NeedsTriage` | CoreWeave's Node lifecycle automation detected a possible hardware or health issue and flagged the Node for investigation. The Node is cordoned and receives a `NoSchedule` taint so that new workloads aren't scheduled onto it. | Health signal. CoreWeave investigates the Node and, if needed, remediates or replaces it. | Plan to move affected workloads off the Node. CKS removes the Node and delivers a replacement according to the [triage transition and prefill policies](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#triage-transitions). If a workload is failing on the Node, [contact support](https://docs.coreweave.com/support.md) with the Node name. |
| `AdminTemporaryFailure` | A manual cordon. A CoreWeave engineer might set it to isolate a Node for a short-term reason, or you can set it yourself with [`cwic node cordon`](#cordon-with-the-coreweave-intelligent-cli) or [`kubectl patch`](#set-admintemporaryfailure-on-a-node). It prevents new scheduling but doesn't, on its own, start a CoreWeave investigation. | Depends on who set it. It marks a manual action rather than an automatic health verdict. | If you didn't set it and you are unsure why it's present, [contact support](https://docs.coreweave.com/support.md) with the Node name. If you set it to flag a problem, also notify CoreWeave so the Node is investigated. |
| Plain `kubectl cordon` (`SchedulingDisabled` with no CoreWeave cordon reason) | Someone ran `kubectl cordon` on the Node. The Node has no `node.coreweave.cloud/cordonReason` annotation. | Your own action, not a CoreWeave maintenance event. | Uncordon the Node with `kubectl uncordon [NODE-NAME]` when you are ready. CoreWeave automation can clear a plain `kubectl cordon`, so use a [custom taint](#isolate-a-node-long-term-with-a-custom-taint) for long-term isolation. |

### Health and lifecycle cordon reasons

CoreWeave's Node lifecycle automation sets the following cordon reasons from Node conditions. Each reason names the fault, and the last column describes what CoreWeave's automation does next: keep the Node cordoned until the condition clears, reboot it, or move it to `triage`. Unless the row says it's immediate, a reboot waits for non-interruptible workloads to finish before draining the remaining Pods. Gracefully interruptible Pods can delay the reboot until they terminate or their termination grace period expires; `CWActive` can still be `True` while this maintenance proceeds. For what each lifecycle state means, see [Node states in a CKS cluster](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#node-states-in-a-cks-cluster).

On a SUNK cluster, these reasons also appear as Slurm drain reasons in the form `k8s: cordon: [CORDON-REASON]`. See [Kubernetes failure cases](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#kubernetes-failure-cases).

| Cordon reason | What it indicates | What CoreWeave automation does |
| - | - | - |
| `AdminImmediateReboot` | An administrator asked to reboot the Node as soon as possible. This condition is deprecated in favor of `AdminImmediatePowerCycle`, but CoreWeave automation still acts on it. To request a reboot yourself, follow [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md) instead of setting either condition. | Reboots the Node immediately, without waiting for it to become idle. |
| `AdminMaintenanceMode` | The Node is scheduled for maintenance while remaining in production. | Keeps the Node cordoned until an administrator clears the condition. |
| `AdminPermanentFailure` | An administrator removed the Node from production use. | Keeps the Node cordoned until an administrator clears the condition. |
| `ConnectivityFailure` | The Node can't connect to its controller. After 10 minutes, this becomes `ConnectivityUpdateTime`. | Keeps the Node cordoned until the condition clears. |
| `ConnectivityUpdateTime` | No heartbeat from the Node for at least 10 minutes. Failing cluster networking Pods, such as Calico, can cause this. | Keeps the Node cordoned until the condition clears. |
| `DNSFailure` | A DNS lookup from the Node failed. | Keeps the Node cordoned until the condition clears. |
| `GPUECCUncorrectableError` | A GPU reported an uncorrectable ECC memory error. | Reboots the Node immediately. |
| `GPUFallenOffBus` | A GPU can no longer communicate on the PCI bus. | Moves the Node to `triage` immediately, which ends running workloads. CKS delivers a replacement. |
| `GPUFault` | A generic GPU [XID error](https://docs.coreweave.com/support/cks/articles/what-do-gpu-xid-error-codes-mean). | Waits for non-interruptible workloads to finish, then drains and reboots the Node. |
| `GPUPCIFault` | The Node can't communicate with its GPUs over PCI. | Moves the Node to `triage` immediately. CKS delivers a replacement. |
| `GPUWantsReset` | The NVIDIA driver reports that a GPU needs a reset, for example because of a pending memory row remap. | Waits for non-interruptible workloads to finish, then drains and reboots the Node. |
| `InfiniBandLinkFault` | An InfiniBand link fault, such as a flapping switch port or cable. When many Nodes report it at once, the cause is usually the fabric rather than the Nodes. | Keeps the Node cordoned while the link fault is active. Separate repeated-flap alerts can also set `NeedsTriage` or `NeedsDrainTriage` and request pending triage. `NeedsDrainTriage` issues a separate drain request, so workloads can be evicted before the pending transition proceeds. |
| `KernelDeadlock` | The operating system kernel deadlocked. | Waits for non-interruptible workloads to finish, then drains and reboots the Node. |
| `NetworkAlertFault` | A network monitoring alert fired for the Node. | Keeps the Node cordoned until the condition clears. |
| `NLCCImmediateReboot` | The CoreWeave Node lifecycle controller requested an immediate reboot. | Reboots the Node immediately. |

### What a cordon affects

A cordon by itself prevents new workloads from scheduling onto a Node. It does not evict the workloads already running there. For a pending maintenance transition, CoreWeave ordinarily waits for non-interruptible workloads to finish before draining the remaining Pods. This maintenance check differs from `CWActive` idleness; see [Active Nodes and stalled transitions](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#active-nodes-and-stalled-transitions).

A cordoned Node still counts toward its Node Pool's `CURRENT`, so a Node Pool can sit at target while its schedulable capacity is reduced. If Pods stay `Pending` while the Node Pool looks healthy, see [At target but Pods won't schedule](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md#at-target-but-pods-will-not-schedule).

## Patch Node conditions safely

For documented procedures that update Node conditions, use a strategic merge patch. Specify `--type=strategic` with `kubectl`, or `Content-Type: application/strategic-merge-patch+json` with the Kubernetes API. This preserves conditions not included in the patch.

> [!WARNING]
>
> A JSON merge patch that includes `status.conditions` replaces the entire array. It removes any omitted conditions, including `Ready`. CoreWeave automation can then misread the Node's state, and your Pods can be terminated.

### Set AdminTemporaryFailure on a Node

Use the following command to set `AdminTemporaryFailure` on a Node:

```bash title="Set AdminTemporaryFailure on a Node" theme={"system"}
kubectl patch node [NODE-NAME] --type=strategic --subresource=status \
  -p '{"status":{"conditions":[{"type":"AdminTemporaryFailure","status":"True","reason":"Node issue","message":"[WHAT-YOU-OBSERVED]"}]}}'
```

## Interpret current Node conditions

Standard Kubernetes Node conditions are visible to you and safe to act on. View them in the `Conditions` section of `kubectl describe node`, or list them directly:

```bash theme={"system"}
kubectl get node [NODE-NAME] -o jsonpath='{range .status.conditions[*]}{.type}={.status}{"\n"}{end}'
```

The following conditions are the ones you can act on.

| Condition | Healthy value | What an unhealthy value means | What to do |
| - | - | - | - |
| `Ready` | `True` | The kubelet isn't reporting healthy. New Pods won't schedule, and running Pods can be evicted through the `node.kubernetes.io/not-ready` taint. | Check the [cordon reason](#common-cordon-and-drain-reasons). For `NLCCPendingExitProduction` or `NeedsTriage`, let recovery proceed. Otherwise, [contact support](https://docs.coreweave.com/support.md). |
| `MemoryPressure` | `False` | The Node is low on memory and the kubelet may evict Pods. | Reduce workload memory or adjust Pod memory limits. |
| `DiskPressure` | `False` | The Node is low on disk and the kubelet may evict Pods. | Free space in ephemeral storage, remove unused container images, or reduce log and checkpoint volume. |
| `PIDPressure` | `False` | The Node is running out of process IDs. | Reduce the number of processes your workloads create per Node. |
| `NetworkUnavailable` | `False` | The condition is missing, so no network provider has reported the Node network as ready. On clusters that use Cilium, it sets `False` once it's running and never sets `True`. | If it persists, [contact support](https://docs.coreweave.com/support.md). |

For conditions defined by CoreWeave, follow the [CoreWeave-managed Node metadata guidance](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#coreweave-managed-node-metadata).

## What to do when a Node is cordoned

If you notice that one of your Nodes is cordoned, the following actions can help you assess the situation and decide whether to intervene.

### Check Node status

Confirm the Node state with `kubectl describe node [NODE-NAME]` to verify the reason for cordoning. If workloads remain running and stable, you don't need to take immediate action.

### Monitor workloads

Ensure your workloads have redundancy or are configured for high availability to tolerate temporary Node unavailability. If workloads become impacted, evaluate whether manual intervention is necessary, such as deleting affected Pods to trigger rescheduling.

### Persistent issues

If a Node remains cordoned for an extended period or your workload is severely impacted, open a support ticket to inform CoreWeave about the issue. Clearly document your observations, such as the Node status and workload behavior, in your support request.

## Important considerations

Keep the following considerations in mind when working with cordoned Nodes:

* Use only documented procedures to change [CoreWeave-managed Node metadata](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#coreweave-managed-node-metadata).
* **Cordoning does not always indicate a serious or permanent Node issue:** Nodes often recover automatically after temporary issues. If the issue is severe or persistent, CoreWeave proactively moves affected Nodes out of production into triage.

## Support

If you need assistance or have questions regarding Node cordoning, [contact CoreWeave support](https://docs.coreweave.com/support.md).
