# Drain and undrain Slurm nodes

Source: https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes

# Drain and undrain Slurm nodes

> Identify the reason a node was drained, manually drain and undrain nodes

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page shows Slurm administrators how to identify why a node was drained, manually drain a node for maintenance, and return drained nodes to service. Use these procedures when you need to temporarily remove a node from scheduling, investigate an automatic drain, or restore nodes after resolving an underlying issue.

Draining a Slurm node prevents it from accepting new jobs while letting any running jobs complete. After a node is drained, it enters a `drained` state and remains unavailable for scheduling until it's undrained (resumed). Unlike Kubernetes Node draining, which evicts running Pods, Slurm draining doesn't terminate running workloads. It only stops new jobs from being assigned to the node.

SUNK login nodes include built-in aliases for draining, undraining, and monitoring node states. See [Aliases for node monitoring](#aliases-for-node-monitoring).

## When nodes are drained automatically

Before you manually drain or undrain a node, it helps to understand the cases where SUNK drains nodes on its own and resolves them without user intervention.

Two systems are involved. SUNK's [Node Health Check (NHC)](#node-health-check-nhc-drains) runs in the Epilog after a job, and only when no other job is still running on the node. A failed check drains the node. Separately, CoreWeave's [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) framework tests idle Nodes every hour, and a passing test is what returns an NHC-drained node whose drain reason carries `sunk:verify-undrain` to service. In some cases, CoreWeave's services automatically drain, restart, recheck, and undrain the node with no action required from you.

Nodes can also be drained in response to an underlying error or event, such as a failing [Prolog or Epilog script](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md). These cases can require troubleshooting to determine the underlying cause.

### Automatic undrain with HPC Verification

When a drain reason includes `sunk:verify-undrain`, SUNK automatically undrains the node after it passes the next hourly [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test, which runs only while the node is idle. No user action is required. If the node fails the test, or never goes idle, it stays drained and you must investigate the underlying issue. To read the test output, use the `sn` alias or the [Node Details](https://docs.coreweave.com/observability/managed-grafana/fleet/node-details.md) Grafana dashboard.

The same mechanism applies to a node you drain yourself. Include `sunk:verify-undrain` in the reason, and SUNK returns the node to service after the next passing test. Use this to take a healthy node out of service temporarily. See [Manually drain a Slurm node](#manually-drain-a-slurm-node).

If you have a compute node in a `drained` state, you can [identify the drain reason](#identify-the-drain-reason) to determine whether you need to take action. Outside the automated HPC Verification cycle, you can [manually drain a node](#manually-drain-a-slurm-node) if you need to temporarily prevent it from accepting new jobs, such as during maintenance, and [manually undrain the node](#manually-undrain-a-slurm-node) to return it to service.

CoreWeave's documentation also includes an overview of [Slurm node states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md), and further information about [nodes in the `INVAL` state](https://docs.coreweave.com/products/sunk/manage_sunk/inval-node-state).

## Connect to the Slurm login node

To drain and undrain nodes, first [connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md#connect-through-ssh).

After connecting to the Slurm login node, you can use the built-in aliases and `scontrol` commands in the following sections to examine and manage drained nodes.

> [!TIP]
>
> Run all Slurm commands, including `scontrol`, from within the Slurm login node shell.

## Identify the drain reason

Before deciding whether to undrain a node, check the drain reason so you know whether the node is recovering automatically or requires manual intervention.

To find out why a node is in a drain state, use the `scontrol show node` command:

```bash theme={"system"}
scontrol show node [NODE-NAME]
```

Replace `[NODE-NAME]` with the actual name of the node you want to check, or remove the `[NODE-NAME]` entirely to list all nodes.

The output of these commands shows a `reason` for the node's drain state. Based on the reason listed, you can determine whether the `drained` state is due to a Kubernetes event or a Slurm issue and proceed accordingly.

> [!NOTE]
>
> An asterisk `*` alongside a node state indicates that the node isn't responding. Nodes in a `drain*` or `down*` state have been removed from the cluster and can be ignored. You can see this suffix if you check the state while the pod isn't yet fully connected.

### Aliases for node monitoring

The SUNK login node image includes the following aliases and shell functions. They are available in every login node shell session by default.

| Alias | Description |
| - | - |
| `drain [NODE-NAME] [REASON]` | Drains a node with a reason, automatically prefixed with your username. |
| `undrain [NODE-NAME]` | Undrains (resumes) a single node. |
| `sn` | Shows detailed node information. Runs `scontrol show node`. |
| `dl` | Lists all nodes in the `drain` and `idle` states, with reasons. |
| `dld` | Lists all nodes in the `drain` state, with reasons, including nodes that are actively draining with running jobs. |
| `downl` | Lists all nodes in the `down` state, with reasons. |

The `dl` alias is equivalent to the following command:

```bash theme={"system"}
sinfo -t "drain&idle" -NO "NodeList:45,Comment:10,Timestamp:25,Reason:130" | uniq
```

The plain Slurm command `sinfo -R` isn't an alias, but it works on any Slurm cluster. It lists every node in the `down`, `drained`, `draining`, `fail`, or `failing` state with its reason:

```bash theme={"system"}
sinfo -R
```

## Manually drain a Slurm node

Generally, SUNK automatically drains Slurm nodes when it finds an issue. If you plan to perform maintenance on a node or want to temporarily remove it from service, you can drain it manually.

The simplest way to drain a node is with the built-in `drain` alias:

```bash theme={"system"}
drain [NODE-NAME] "the reason for draining"
```

The `drain` alias automatically prefixes the reason with your username, resulting in a drain reason in the following format. Replace `[USERNAME]` with your username and `[REASON]` with the reason you provide.

```text theme={"system"}
[USERNAME]: [REASON]
```

To drain a node and have SUNK automatically undrain it after it passes the next [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test, include `sunk:verify-undrain` in the reason:

```bash theme={"system"}
drain [NODE-NAME] "investigating issue (sunk:verify-undrain)"
```

Alternatively, you can use `scontrol update` directly:

```bash theme={"system"}
scontrol update nodename=[NODE-NAME] state=drain reason="the reason for draining"
```

Replace `[NODE-NAME]` with the name of the node you're draining.

## Manually undrain a Slurm node

SUNK undrains nodes whose drain reason contains `sunk:verify-undrain` without any action from you. See [Automatic undrain with HPC Verification](#automatic-undrain-with-hpc-verification). You can undrain these nodes manually if you don't want to wait.

If you manually drained the node and have already corrected any underlying issues, you can manually undrain the node at your discretion.

### Undrain a single node

The simplest way to undrain a node is with the built-in `undrain` alias:

```bash theme={"system"}
undrain [NODE-NAME]
```

Alternatively, use `scontrol update` directly to change the node `state` to `resume`:

```bash theme={"system"}
scontrol update nodename=[NODE-NAME] state=resume
```

Replace `[NODE-NAME]` with the name of the node you're undraining.

Monitor the node after undraining it. If the issue that caused the automatic drain persists, SUNK can automatically drain the node again the next time it attempts to run a job.

### Undrain all drained nodes

To undrain all nodes currently in both a `drain` and an `idle` state, use the following command:

```bash theme={"system"}
for node in $(dl | cut -d " " -f 1); do
    echo "undraining $node";
    scontrol update nodename=$node state=resume;
done
```

This command uses the [`dl` alias](#aliases-for-node-monitoring).

### Undrain nodes by reason

Use `grep` to undrain nodes that have been drained for a specific reason. Before you undrain nodes in this manner, confirm which nodes the script processes:

```bash theme={"system"}
dl | grep [REASON]
```

After you confirm that the listed nodes match those you intend to undrain, undrain them with the following command.

The following example undrains only nodes with `scheduler: k8s pod deletion timeout for job` listed in the drain reason:

```bash theme={"system"}
for node in $(dl | grep "scheduler: k8s pod deletion timeout for job" | cut -d " " -f 1); do
    echo "undraining $node";
    scontrol update nodename=$node state=resume;
done
```

This command uses the [`dl` alias](#aliases-for-node-monitoring).

## Common drain reasons

Drain reasons fall into a few groups by source: Kubernetes events (`k8s:`), Node Health Check failures (`NHC:`), Prolog and Epilog failures, and system conditions. Two quick rules cover most cases:

* A reason starting with `k8s:` comes from a Kubernetes-related event, such as a node update. These are often temporary and resolve automatically.
* A reason containing `sunk:verify-undrain` means SUNK returns the node to service automatically after the next passing HPC Verification test. See [Automatic undrain with HPC Verification](#automatic-undrain-with-hpc-verification).

> [!NOTE]
>
> A drain reason of `k8s: pod scheduled for deletion: rolling update` indicates that the node is waiting to update and doesn't accept new jobs to avoid disrupting active work. This often appears on Slurm nodes when the Kubernetes NodeSet is updated. After the `slurmd` Pod restarts, the Syncer undrains the node without any action needed from you.

A reason that includes neither `k8s` nor `sunk:verify-undrain` usually means no automation returns the node to service. The reason alone doesn't tell you where the fault is, because Kubernetes drains cover hardware failures too, and Slurm drains can come from a transient scheduler problem. Identify the reason in the sections below, fix the underlying problem, then [undrain the node](#manually-undrain-a-slurm-node) yourself.

Drains performed using the `drain` alias or `scontrol` have a manually-entered reason.

For drain reasons that come from a Prolog or Epilog script, see [Troubleshoot Prolog and Epilog failures](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md#troubleshoot-prolog-and-epilog-failures).

The following sections describe the reasons you're most likely to see and how to tell a node-local problem from a cluster-wide one.

### Kubernetes drain reasons

Kubernetes drains fall into two groups: routine node reorganization and failures that start an automated repair.

#### Routine Kubernetes actions

These reasons appear when a node leaves the NodeSet's feasible pool or when the NodeSet is scaled down or updated.

| Reason | What it indicates | Safe to undrain? |
| - | - | - |
| `k8s: pod scheduled for deletion: rolling update` | The node is waiting to update and doesn't accept new jobs so that it doesn't disrupt active work. | No. Undraining cancels the pending update. The Syncer undrains the node after the `slurmd` Pod restarts. |
| `k8s: pod scheduled for deletion: node removal` | SUNK is removing the node from the NodeSet, for example after a scale-down, and its `slurmd` Pod is scheduled for deletion. | No. The node leaves Slurm when the pod is deleted. |
| `k8s: pod terminated` | The `slurmd` Pod on the Kubernetes Node was deleted, which ends Slurm's connection to the node. The node is likely no longer in the cluster, or no longer in production. | Don't undrain manually. Return the node to service through the Kubernetes controls that allocate it, such as the NodeSet replica count in SUNK Standard, or the matching `nodes[].count` in the `SunkCluster` in SUNK Self-Service. |

Any of these reasons can appear with or without further detail. If the reason also contains `cordon`, the Kubernetes Node was cordoned, either by automated repair or by hand. See [Kubernetes failure cases](#kubernetes-failure-cases).

#### Kubernetes failure cases

Kubernetes failure cases are mostly hardware failures. When a Node condition fires, CoreWeave automation [cordons](https://docs.coreweave.com/glossary.md#cordon) the Kubernetes Node. Depending on the condition, the Node stays cordoned until the condition clears, or the [CoreWeave Node lifecycle controller](https://docs.coreweave.com/glossary.md#coreweave-node-lifecycle-controller) coordinates a reboot or a move to triage. The SUNK [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) mirrors the cordon into Slurm as a drain, so the reason takes the form `k8s: cordon: [CORDON-REASON]` while the `slurmd` Pod is running, and `k8s: pod terminated: cordon: [CORDON-REASON]` after the pod is gone.

Don't undrain these nodes manually. Most return to production on their own once the repair succeeds. The exceptions are the administrator-initiated reasons. `AdminMaintenanceMode` and `AdminPermanentFailure` stay in place until someone clears them. `AdminTemporaryFailure` stays until someone clears it or the Node reboots. If a node stays drained for any other reason, the repair didn't succeed and the underlying fault needs investigation.

The cordon reason names the fault. For the most common reasons, what each indicates, and whether CoreWeave's automation keeps the Node cordoned, reboots it, or moves it to triage, see [Health and lifecycle cordon reasons](https://docs.coreweave.com/products/cks/nodes/cordon.md#health-and-lifecycle-cordon-reasons). One reason is specific to SUNK:

| Cordon reason | What it indicates |
| - | - |
| `unknown` | The Kubernetes Node is cordoned but has no `node.coreweave.cloud/cordonReason` annotation, so CoreWeave automation didn't cordon it. A plain `kubectl cordon` causes this, as does a third-party operator running in your cluster, such as a storage operator during a filesystem update. Check who ran the cordon. An operator might record it in the Node's events, which you can read with `kubectl describe node`, but a plain `kubectl cordon` leaves no event. The drain clears when the Node is uncordoned. |

#### How long to wait for a Kubernetes repair

A repair has two phases, and only the second has a predictable duration. First, most transitions wait for the Kubernetes Node to become idle, and that wait has no timeout. It lasts as long as your jobs keep running on the Node. Second, once the Node is idle, CoreWeave either reboots it or moves it to triage.

To tell which, read the Node's lifecycle state. Replace `[KUBERNETES-NODE-NAME]` with the name of the Kubernetes Node that hosts the Slurm node's `slurmd` Pod:

```bash theme={"system"}
kubectl get node [KUBERNETES-NODE-NAME] -o custom-columns='NAME:.metadata.name,STATE:.status.conditions[?(@.type=="PhaseState")].reason,PENDING:.status.conditions[?(@.type=="PendingPhaseState")].reason'
```

If you don't have `kubectl` access to the cluster, look the Node up in the [Node Details](https://docs.coreweave.com/observability/managed-grafana/fleet/node-details.md) Grafana dashboard instead. Its **Logs** panel group merges the Node's Kubernetes events, including the lifecycle transition events described in [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md), and the **Summary** group shows the Node's active alerts and HPC Verification status.

* **A reboot state**, such as `production-reboot`, `production-powerreset`, or `production-powercycle`: The Node reboots and returns to `production`, and the drain clears. An HPC Verification test runs after the reboot, not before the Node returns. As a rule of thumb, allow about an hour after the Node goes idle. If the Node hasn't returned after about three hours, CoreWeave moves it to triage.
* **`triage`**: The Node leaves your cluster for repair, and CKS delivers a replacement. The Slurm node doesn't come back. Its reason becomes `k8s: pod terminated`, and `scontrol show node` shows `BootTime=None` and `SlurmdStartTime=None`. The replacement joins Slurm as a new node.

For what each state means, see [Node states in a CKS cluster](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md#node-states-in-a-cks-cluster). If the Node has been idle for longer than these windows and its state hasn't changed, or the Slurm node stays drained after the Node returns to `production`, [contact support](https://docs.coreweave.com/support.md) with the node name and the full drain reason.

### Slurm drain reasons

Slurm drains come primarily from problems that occur while jobs are running. Most carry `sunk:verify-undrain` and clear on their own after the next passing HPC Verification test. If a node stays drained, find out why it failed and couldn't recover.

| Reason | What it indicates | Safe to undrain? |
| - | - | - |
| `NHC: [CHECK-NAME]` | A Node Health Check failed during the job's Epilog task. See [Node Health Check (NHC) drains](#node-health-check-nhc-drains). | Yes, after the underlying problem is resolved. |
| `prolog pre-hook failed` | A pre-hook task failed before the job started. This is often transient, such as heavy traffic or a Kubernetes API server failure that makes in-flight [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) pre-hook calls fail. An API server failure can drain many nodes at once for this reason. | Yes. Check the pre-hook logs on the draining pods first. |
| `Duplicate jobid` | This is when a job restarts on the same node with the same id in a short period of time. Slurm automatically drains the node. | Yes. On SUNK v7.3.0 and later, SUNK undrains the node automatically after a passing HPC Verification test. |
| `scheduler: k8s pod deletion timeout for job [JOB-ID]` | The scheduler Epilog task timed out while verifying that the job's Kubernetes resources were deleted. Other connection errors, such as 5xx replies or a failure to connect, don't trigger this drain. | Yes, once the Kubernetes resources are released. |
| `batch job complete failure` | An intermittent failure at job completion. CPU contention in the SUNK scheduler is a common cause, and the node itself is usually healthy. The node drains again the next time a contended job lands on it. A Pod with [Guaranteed QoS](https://docs.coreweave.com/support/cks/articles/how-do-kubernetes-qos-classes-work) pinning CPU cores produces the same reason: see [Static CPU allocation and the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/static-cpu-allocation.md). | Yes, if the node is otherwise healthy. |
| `RuntimeError: CUDA error: uncorrectable NVLink error detected during the execution` | A GPU fault on the node, reported through an [XID error](https://docs.coreweave.com/support/cks/articles/what-do-gpu-xid-error-codes-mean) from the NVIDIA driver. | Yes, if the node is healthy and a recent HPC Verification test passed. Otherwise, investigate the GPU fault first. |
| `Low RealMemory` | The memory that `slurmd` reports doesn't match the memory configured in Slurm. The reason includes the comparison, such as `Low RealMemory (reported:2062607 < 100.00% of configured:2063456)`. Affected nodes are usually also in the `INVAL` state. | No. Undraining doesn't reconcile the configuration. See [Memory and CPU configuration mismatches](#memory-and-cpu-configuration-mismatches). |
| `Low socket*core*thread count`, `Low CPUs` | The hardware CPU count no longer matches the configured Slurm topology, which is the product of sockets, cores per socket, and threads per core. | No, until the CPU count is restored. See [Memory and CPU configuration mismatches](#memory-and-cpu-configuration-mismatches). |

### Node Health Check (NHC) drains

SUNK runs [Node Health Check (NHC)](https://github.com/mej/nhc) as one of the scripts in the Epilog chain after a job, and only when no other job is still running on the node. A failed check drains the node with a reason that begins with `NHC:`.

That timing is why these drains appear after a job finishes. The text after `NHC:` names the failed check. Most NHC drains carry `sunk:verify-undrain`, so they clear on their own once the node passes the next HPC Verification test. See [Automatic undrain with HPC Verification](#automatic-undrain-with-hpc-verification). If a node fails the same check repeatedly, the hardware needs attention. To read the failed check's output, use the `sn` alias or the [Node Details](https://docs.coreweave.com/observability/managed-grafana/fleet/node-details.md) Grafana dashboard. For how the Syncer decides that a node can be undrained, see [NHC drain and HPC Verification](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md#nhc-drain-and-hpc-verification).

These checks cover node hardware that CoreWeave maintains, so most NHC drains resolve without you doing anything. One NHC failure instead leaves the node cycling between drained and undrained, because verification passes while the fault remains. For that case and its fix, see [Why does my node keep draining for a missing InfiniBand device?](https://docs.coreweave.com/support/sunk/articles/why-does-my-node-keep-draining-for-a-missing-infiniband-device). If a node stays drained after repeated checks, [contact CoreWeave support](https://docs.coreweave.com/support.md) with the node name and the full drain reason.

### Memory and CPU configuration mismatches

`Low RealMemory`, `Low socket*core*thread count`, and `Low CPUs` all mean that the resources `slurmd` reports no longer match what Slurm has configured for the node. Undraining doesn't help, because the node re-drains as soon as `slurmd` reports the mismatched count again.

Slurm saves a node's configuration when the node first registers, so a node whose resources change afterward usually also lands in the `INVAL` state. See [Address nodes in the `INVAL` state](https://docs.coreweave.com/products/sunk/manage_sunk/inval-node-state) for how to compare `slurmd -C` output against `slurm.conf` and restart the daemons.

For a `Low RealMemory` drain where the configuration can't be reconciled, delete the node from Slurm so that it re-registers with its current configuration:

```bash theme={"system"}
scontrol delete node=[NODE-NAME]
```

If the node has an active workload, wait for the job to finish first. If the node stays in the `COMPLETING` state, SUNK v6.8.0 and later marks it `DOWN` automatically through the `cleanup-completing` automation. You can then delete it. On earlier versions, mark the node down yourself before deleting it:

```bash theme={"system"}
scontrol update nodename=[NODE-NAME] state=DOWN reason="cleanup completing"
```

The following section describes the most common cause of a CPU count mismatch and how to correct it.

#### CPU topology mismatch from a statically pinned Pod

For the full explanation of which Pods pin CPU cores and how to configure them, see [Static CPU allocation and the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/static-cpu-allocation.md).

`slurmd` drains a node when the CPU count the kernel reports is no longer divisible by the configured Slurm topology. The usual cause is a Pod with [Guaranteed QoS](https://docs.coreweave.com/support/cks/articles/how-do-kubernetes-qos-classes-work) and a whole-number CPU request landing on the node. Under the kubelet's [static CPU manager policy](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/#static-policy), which CKS Nodes enable by default, the kubelet pins that whole CPU exclusively to the Pod and removes it from the shared pool. As a result, `slurmd` detects one fewer CPU than configured, such as 127 instead of 128.

The `slurmd` logs on the affected node show the mismatch directly:

```text theme={"system"}
slurmd: error: Thread count (127) not multiple of core count (64)
slurmd: error: NodeNames=[NODE-NAME] CPUs=127 match no Sockets, Sockets*CoresPerSocket or Sockets*CoresPerSocket*ThreadsPerCore. Resetting CPUs.
slurmd: debug: CPUs:127 Boards:1 Sockets:2 CoresPerSocket:32 ThreadsPerCore:1
slurmd: error: Node configuration differs from hardware: CPUs=64:127(hw) Boards=1:1(hw) SocketsPerBoard=2:2(hw) CoresPerSocket=32:32(hw) ThreadsPerCore=1:1(hw)
```

A hardware count of `127(hw)` on a node with 128 CPUs confirms that a statically pinned Pod claimed one CPU.

The rest of the log follows from that one missing CPU. `slurmd` divides the 127 CPUs it detects by the 64 cores and rounds down to one thread per core. It then resets the configured CPU count to 64, which is 2 sockets times 32 cores per socket times 1 thread per core. That's why this log reports `ThreadsPerCore=1` and `CPUs=64`, while the healthy startup line later in this section reports `Threads=2` and `CPUs=128` for the same hardware.

To resolve the mismatch, follow these steps:

1. Describe the underlying Kubernetes Node and look under **Non-terminated Pods** for a Pod whose CPU requests and limits are equal integers, such as `1/1`.
2. Change that workload to a non-integer CPU request, such as `900m`, or to Burstable QoS by making its requests and limits differ. Either change excludes the Pod from kubelet's static CPU manager.
3. [Restart `slurmd`](https://docs.coreweave.com/products/sunk/manage_sunk/interact-with-kubernetes#restart-the-slurm-daemon) on each drained node so that it re-reads the corrected CPU count.
4. Confirm the topology in the `slurmd` logs, then [undrain the node](#manually-undrain-a-slurm-node).

On a healthy restart, the `slurmd` startup line reports the full hardware count, and the `match no Sockets` and `Resetting CPUs` errors no longer appear:

```text theme={"system"}
slurmd: CPUs=128 Boards=1 Sockets=2 Cores=32 Threads=2 Memory=2063457 TmpDisk=14649107 Uptime=80672 CPUSpecList=(null) FeaturesAvail=(null) FeaturesActive=(null)
```

The `CPUs=` value matches the node's hardware again, and `Sockets`, `Cores`, and `Threads` multiply to it, so the configured topology divides evenly.

If you undrain the node before you fix the offending Pod, it re-drains within seconds.

### Mass drain versus isolated drain

Whether one node drained or many drained at once is a strong signal of where the problem originates. Use `dl` or `sinfo -R` to count how many nodes share a drain reason and roughly when they drained. The following rules of thumb are how CoreWeave support triages drains. They hold in most cases, but they aren't guarantees:

* **One node, with an `NHC:` GPU, InfiniBand, or filesystem check**: Treat it as a node-local issue and wait for the `sunk:verify-undrain` cycle.
* **Many nodes drained close together with the same InfiniBand or NCCL (NVIDIA Collective Communications Library) check**: Suspect a shared fabric event, such as a leaf or spine switch, rather than many simultaneous independent hardware failures. Don't mass-undrain to "fix" it, because that can mask an ongoing event. Open a support ticket. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include the shared reason and the affected node list.
* **Many nodes drained with `prolog pre-hook failed`**: A Kubernetes API server or [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) failure can fail every in-flight pre-hook call at once. These nodes are healthy and safe to undrain in bulk once the API server and Syncer are healthy again. See [Undrain nodes by reason](#undrain-nodes-by-reason).
* **All or most nodes drained at the same time, whatever the reason**: Check for a Slurm controller restart or a control-plane event before you investigate individual nodes. These drains are safe to undrain once the controller and Syncer are healthy.
