# NodeSet

Source: https://docs.coreweave.com/products/sunk/discover_sunk/nodeset

# NodeSet

> The NodeSet CRD that represents a set of Slurm nodes as Kubernetes Pods with 1:1 Node mapping

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The NodeSet CRD represents a set of Slurm nodes. It manages the Kubernetes Pods that contain the Slurm nodes and their associated Kubernetes Nodes. The NodeSet deploys like a DaemonSet, with a 1:1
mapping between Pods and Kubernetes Nodes.

The NodeSet controller is responsible for creating, updating, and deleting the Pods that belong to the NodeSet, and handling their Node assignment.

This reference explains how the NodeSet controller selects Nodes, names and creates Pods, handles deletion and upgrades, and reports status. Use it to understand the behavior of the NodeSet CRD when planning, configuring, or troubleshooting SUNK deployments.

## Pod creation and scaling

The following sections describe how the NodeSet controller decides which Nodes to use, how it names the Pods it creates, and how it places them on the cluster.

A NodeSet scales up to the desired number of replicas, if possible. The number of available Kubernetes Nodes in the cluster that match the NodeSet's affinity, tolerations, and resource requests may limit this. The status indicates the total number of feasible Nodes, which may be less than the requested amount.

### Node selection

When selecting a Slurm node to assign a Pod, the NodeSet evaluates the Kubernetes Nodes in the cluster against the affinity, tolerations, and resource requests. The NodeSet controller also ensures that only one NodeSet uses a Node at a time. The NodeSet controller continues to evaluate Nodes until it reaches the desired number of new Pods, or the list of Nodes is exhausted. The selected Nodes are then added to the NodeSet.

> [!NOTE]
>
> The NodeSet only evaluates the required portion of the Node affinity. It ignores all other affinity sections.

For more information, see [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md).

### Pod naming

The NodeSet names the Pods it creates deterministically by their Node assignment. This makes the Slurm node list consistent, and the association between Kubernetes Nodes and Slurm nodes straightforward to determine. When the NodeSet controller finds a suitable Kubernetes Node, it creates the Pod with the naming convention `<prefix>-<name>`.

* `<prefix>` is set to `.Spec.PodNamePrefix` if present, or the NodeSet name if not.
* `<name>` is generated from the last two octets of the Node's internal IPv4 address, each zero-padded to three digits. For example, a Node with IP `10.174.12.2` results in a `<name>` of `012-002`.

> [!NOTE]
>
> Zero-padded numbers make the Slurm range syntax easier to use. Because CoreWeave's environment doesn't require additional octets to create unique names, only the last two octets are used.

### Pod creation

When the NodeSet creates a Pod, it overrides the Pod's Node affinity to match the Node name that the Pod is named after, forcing the Pod to schedule for that specific Node. The NodeSet also adds a toleration for the `sunk.coreweave.com/lock` key to the Pods.

When a `slurmd` Pod is added to a Node, the Node is added to one of the NodeSlices associated with the NodeSet. Because a `slurmd` Pod is intended to occupy a full Node when running, only one NodeSet schedules a Pod to a given Node at a time.

## Safe deletion

Safe deletion lets the NodeSet remove Pods during scale-down or upgrade without interrupting running workloads. This section describes how the NodeSet controller coordinates with the Syncer to drain Slurm nodes before deleting their Pods.

When a NodeSet scales down, or when a rolling upgrade runs, a safe deletion mechanism removes the Pods without interrupting any running Slurm jobs. The deletion process exchanges information between the cluster-wide NodeSet controller and the individual Slurm cluster Syncers through the `SlurmDelete` condition on the Pod.

When the NodeSet deletes a Pod for scaling or rolling update purposes, it sets the deletion condition to `true` with the reason `ScalingDeleteScheduled` or `RollingDeleteScheduled`. The Syncer responsible for that NodeSet then drains the Node in the associated Slurm cluster and updates the Pod's state. After the Pod is both drained and idle, the NodeSet controller deletes the Pod. See [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) for more details about the Pod conditions visible to the Syncer.

> [!NOTE]
>
> When a Pod is being deleted due to scaling, if the NodeSet scales down and then back up before the actual Pod deletion happens, the NodeSet controller removes the label and halts the deletion process. This also removes the drain condition from the Slurm node.

## Forced deletion

Forced deletion overrides safe deletion when Pods need to be removed within a bounded time window, even at the cost of interrupting running workloads.

When using the NodeSet options `operator.config.operator.nodeSet.forceScalingDeleteKnownConditionTimeout` and `operator.config.operator.nodeSet.forceScalingDeleteUnknownConditionTimeout`, the NodeSet
forcibly deletes Pods after the specified timeout is reached. By default, both options are set to `0`, which disables the feature. When enabled, these options take effect during NodeSet scale-down events. Pods are deleted after the configured timeout, even if a Slurm job is still running on the Pod.

* `forceScalingDeleteKnownConditionTimeout` applies when the Slurm state is known for the Pod, which is typical in a healthy cluster. For example, if this option is set to 10 seconds and a scale-down event occurs, the Pod is forcibly removed from Slurm 10 seconds later, even if a job is still running.
* `forceScalingDeleteUnknownConditionTimeout` functions the same way but applies when the Slurm state is unknown. This can occur if the cluster has issues.

## Scaling down

When a NodeSet is scaled down, the controller chooses which Pods to delete first based on their state. This section describes the priority-based ordering used to make that selection.

NodeSet scaling down follows a priority-based ordering, which is enabled by default through the `operator.config.operator.nodeSet.scaleDownPriorityOrdering` option. Each Pod is ranked and assigned a deletion priority, which determines the order of deletion. A Pod with a lower priority value is deleted first. The Pod's readiness, Slurm running state, drained state, and pending delete status determine the priority. Pods that aren't ready are deleted first, followed by idle and drained Pods, and finally Pods that are running workloads.

The following ranking determines the priority value:

1. Not-ready Pods are the lowest priority and are the first to be deleted.
2. Idle Pods that are `drained` and have the `delete` condition.
3. Idle Pods that are `drained` but do NOT have the `delete` condition.
4. Idle Pods that are not `drained`.
5. Pods running workloads that are `drained` and have the `delete` condition.
6. Pods running workloads that are `drained` and do NOT have the `delete` condition.
7. Pods running workloads that are not `drained`.

When you disable the `operator.config.operator.nodeSet.scaleDownPriorityOrdering` option, the NodeSet scales down. Newer Pods are deleted first, following the [Safe deletion](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#safe-deletion) process.

Regardless of the option chosen, when a Pod is removed, the associated NodeSlices are updated to no longer contain that Node.

## Rolling upgrade

A rolling upgrade replaces outdated Pods in a controlled manner so that the NodeSet can adopt a new template without taking the entire workload offline.

You can upgrade a NodeSet either by deletion or through a rolling update. A rolling update is the preferred option because it automates the upgrade using safe deletion.

To limit the maximum number of Pods that can be unavailable during a rolling update, configure the `maxUnavailable` value to a percentage or a number. This value also includes any Pods with a pending deleting status.

The rolling update uses a hash of the `.spec.template.spec` value to determine if a Pod is up to date. The Pod's `controller-revision-hash` label stores the associated value used when the Pod was created. If the value doesn't match the current NodeSet value, the Pod is considered outdated.

The rolling update prioritizes Pods by:

1. Non-ready Pods
2. Idle Pods that are not running Slurm workloads
3. Remaining Pods

This order lets the cluster update as many Pods as possible before waiting for the remaining Pods to become drained and idle.

## Status

The NodeSet exposes status fields and matching metrics that report the current scheduling and readiness of its Pods. Use these to observe how many Nodes are scheduled, ready, running jobs, or drained.

The NodeSet contains status information about the NodeSet, including:

| Field | Metric | Definition |
| - | - | - |
| `currentNumberScheduled` | `kube_sunk_nodeset_current` | Number of Nodes that the NodeSet is scheduled on. |
| `numberMisscheduled` | `kube_sunk_nodeset_misscheduled` | Number of Nodes having the NodeSet's Pods that should no longer be scheduled on. |
| `desiredNumberScheduled` | `kube_sunk_nodeset_desired` | Desired number of Nodes to schedule on. If `.spec.replicas` is set, this matches that value. Otherwise, it matches `numberFeasible`. |
| `updatedNumberScheduled` | `kube_sunk_nodeset_up_to_date` | Number of Nodes having scheduled the latest version of the NodeSet's Pod. |
| `numberFeasible` | `kube_sunk_nodeset_feasible` | Number of Nodes the NodeSet could schedule on (inclusive of those already scheduled). |
| `numberReady` | `kube_sunk_nodeset_ready` | Number of Nodes having the NodeSet's Pod in a Ready state. |
| `numberUnavailable` | `kube_sunk_nodeset_unavailable` | Number of Nodes scheduled but do not have the NodeSet's Pod in a Ready state. |
| `numberRunning` | `kube_sunk_nodeset_running` | Number of Nodes actively running Slurm jobs. |
| `numberDrain` | `kube_sunk_nodeset_drained` | Number of Nodes that are drained in Slurm. |
