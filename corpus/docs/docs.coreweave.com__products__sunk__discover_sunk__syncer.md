# Syncer

Source: https://docs.coreweave.com/products/sunk/discover_sunk/syncer

# Syncer

> How the SUNK Syncer bidirectionally synchronizes state between Slurm nodes and Kubernetes Pods

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The Syncer bidirectionally synchronizes the state between Slurm nodes and the respective Kubernetes Pods. It translates [state information](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md) into formats understood by each side, such as `Ready`, `Running`, or `Drain`, and lets operations made on either side update the state of the other. The Syncer is deployed along with each Slurm cluster.

## Information flow and reconcile operations

The Syncer supports several flows of information and operations. The following sections describe each flow and the conditions that trigger it.

### Slurm drains from Kubernetes

When certain conditions happen on the Kubernetes side that make the respective Slurm node either inoperable or undesired for continued Slurm job scheduling, the Syncer propagates these conditions as [a drain on the Slurm node](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md). When the condition clears, the Syncer then removes the drain.

A drain from Kubernetes uses the `k8s:` prefix to indicate within Slurm that the drain originated on the Kubernetes side.

> [!NOTE]
>
> The Syncer only removes or updates drain reasons that are prefixed with `k8s:`. A non-prefixed drain is left as is, with one exception: the Syncer resumes a drain whose reason contains `sunk:verify-undrain` after the node passes an HPC Verification test. See [NHC drain and HPC Verification](#nhc-drain-and-hpc-verification).

Some of the possible conditions that apply a drain are:

* The Kubernetes Pod associated with this Slurm node is not ready.
* The Kubernetes Pod associated with this Slurm node has been deleted.
* The Kubernetes Pod associated with this Slurm node is pending deletion. See [NodeSet Controller](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#safe-deletion).
* The Kubernetes Pod associated with this Slurm node is Cordoned. See [Pod Controller](https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller.md#node-cordon).

Many Kubernetes-side drains are removed automatically when the originating condition is resolved on the Kubernetes side. When the drain is removed in Slurm before the originating condition is resolved, the Syncer reapplies the drain.

### Slurm downed nodes

Nodes in Slurm can be set `down` by three routes:

* Automatically by the Slurm Controller.
* Manually by the user from within Slurm.
* Upon Pod deletion in Kubernetes.

When a node is downed, the Syncer doesn't automatically resume or drain the node. This allows for more flexibility when managing nodes in Slurm. The Slurm controller transitions nodes out of down per the [ReturnToService](https://slurm.schedmd.com/slurm.conf.html#OPT_ReturnToService) configuration value.

> [!NOTE]
>
> The default (and recommended) configuration of the Slurm chart uses `ReturnToService=2`, which automatically resumes any down node that starts communicating with the Slurm controller. To change this behavior, adjust this value. A non-default value requires the user to take action within Slurm after a Pod is updated in Kubernetes, before the node is usable in Slurm.

### Slurm node deletion

The Syncer updates the state within Slurm following NodeSlice changes. For example, when nodes are removed from [NodeSets](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md), these changes are reflected in the underlying NodeSlice(s). After detecting removed NodeSlice entries, the Syncer requests deletion of the corresponding Slurm nodes.

Enable this functionality using the Slurm chart option [.syncer.config.syncer.slurmNodeCleanUp](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).

### Slurm node status

The Syncer converts the current running, responding, and drain Slurm states into conditions and labels on the Pod. The conditions `SlurmDrain`, `SlurmRunning`, and `SlurmNotResponding` mirror the state within Slurm. The Syncer propagates the reason for the drain into the Message for the `SlurmDrain` condition.

The labels `sunk.coreweave.com/running`, `sunk.coreweave.com/drain`, and `sunk.coreweave.com/not_responding` aid dashboards that use metrics from kube-state-metrics, and aren't used for any logic within the Operator or Syncer. When a Slurm node is drained from within Slurm, that drain propagates up to the Node as well. For more information, see [NodeController](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md).

### NHC drain and HPC Verification

> [!NOTE]
>
> Although this feature was implemented for CoreWeave's particular environment, it can be used for similar workflows in other environments.

SUNK runs [Node Health Check (NHC)](https://github.com/mej/nhc) as one of the scripts in the Epilog chain after a job, and only when no other job is still running on the node. A failed check drains the node with a reason that begins with `NHC:`.

CoreWeave's [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) tests run similar checks and trigger the undrain of older NHC failures. For the Epilog chain itself, see [Run Prolog and Epilog scripts](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md).

The Syncer identifies drains that can be undrained through the presence of `sunk:verify-undrain` anywhere in the node's drain reason. When this string is present, the Syncer checks the `HPCVerification` condition of the Pod to see if a newer verification pass has happened since the drain.

### Extra field

Nodes in Slurm have an `Extra` field that can be used to store user-specified information. SUNK uses this to store information that provides visibility within Slurm to conditions on the Kubernetes side. The Syncer manages updates to the `Extra` field to reflect the information. The information is stored as JSON in the `Extra` field to allow for parsing and manipulation.

> [!NOTE]
>
> Users can add more information into the `Extra` field in Slurm. The `Extra` field must contain valid JSON, or the contents are cleared and replaced at the next synchronization. When there are conflicts, JSON fields set by the Syncer overwrite those set by the user.

## Hook API

The hook API provided by the Syncer lets events in Slurm directly trigger operations within Kubernetes. Some of these hooks facilitate blocking synchronization or immediate actions. The Syncer provides several hooks for node objects, described in the following sections.

### Pre-hook

The pre-hook endpoint ensures that other jobs running outside Slurm on the Node are removed before the Slurm jobs start. It also begins the state propagation that triggers the [Pod Controller](https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller.md#node-lock) and [Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md#node-lock) to perform further actions.

### Reboot

> [!NOTE]
>
> This endpoint is only available when the Syncer has permissions to perform operations on the Nodes. The Syncer node permissions are set with the Slurm chart option [.syncer.nodePermissions.enabled](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).

The reboot endpoint reboots the Kubernetes Node associated with a Slurm node. By default, this endpoint sets the `PhaseState` condition on the Node along with the associated reason `production-powerreset`, which then triggers other Node management tooling to reboot the Node. To modify the condition type and associated reason, use [.syncer.hooksAPI.nodeRebootCondition](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) and [.syncer.hooksAPI.nodeRebootReason](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).

## Metrics

The Syncer provides a scrapeable metrics endpoint, which exposes metrics for the nodes, jobs, and the overall Slurm cluster. The PodMonitor deployed with the SUNK chart labels all metrics with their associated Slurm cluster using the `slurm_cluster` label. The Syncer also exports additional metrics for the standard Go runtime and controller runtime.

> [!NOTE]
>
> Use these metrics, not Kubernetes Pod metrics, to track what Slurm has allocated on a compute node. Kubernetes Pod metrics report almost no CPU or memory usage for a `slurmd` Pod, because Slurm runs job processes in cgroups it manages outside the container's cgroup. See [Why do slurmd Pod metrics show almost no CPU or memory usage?](https://docs.coreweave.com/support/sunk/articles/why-do-slurmd-pod-metrics-show-almost-no-cpu-or-memory-usage).

Labels added by the code are shown in the following list. More labels can be added by the scrape configuration.

The Syncer applies the following labels:

* **account**: Slurm account name
* **id**: Slurm job ID
* **name**: Slurm job name
* **node**: Slurm node name
* **partition**: Slurm partition
* **state**: Slurm job current state
* **user**: Slurm user name
* **message\_type**: Slurm RPC message type

| Metric | Unit | Labels | Description |
| - | - | - | - |
| slurm\_controller\_rpc\_count | count | message\_type | RPC count per message type. |
| slurm\_controller\_rpc\_mean\_duration\_seconds | seconds | message\_type | RPC mean duration per message type. |
| slurm\_job\_state | -- | partition, account, user, id, name, state | Current state of the job represented in the `state` label. |
| slurm\_job\_cpus\_allocated | count | partition, account, user, id, node | The number of CPUs allocated to a job by Slurm node. Only present for running jobs. |
| slurm\_job\_gpus\_allocated | count | partition, account, user, id, node | The number of GPUs allocated to a job by Slurm node. Only present for running jobs. |
| slurm\_job\_uptime\_seconds | seconds | partition, account, user, id, node | The number of seconds a job has been running. Only present for running jobs. |
| slurm\_jobs\_pending | count | partition, account, user | The number of pending jobs in the Slurm cluster. |
| slurm\_jobs\_running | count | partition, account, user | The number of running jobs in the Slurm cluster. |
| slurm\_jobs\_suspended | count | partition, account, user | The number of suspended jobs in the Slurm cluster. |
| slurm\_node\_state | -- | node ,partition ,state | Current state of the node represented in the `state` label. |
| slurm\_node\_cpu\_alloc | count | node | The number of CPUs allocated per node. |
| slurm\_node\_cpu\_idle | count | node | The number of CPUs idle per node. |
| slurm\_node\_cpu\_total | count | node | The total number of CPUs per node. |
| slurm\_node\_mem\_alloc | MB | node | The amount of allocated memory per node. |
| slurm\_node\_mem\_total | MB | node | The total amount of memory per node. |
| slurm\_node\_gpu\_alloc | count | node | The number of GPUs allocated per node. |
| slurm\_node\_gpu\_idle | count | node | The number of GPUs idle per node. |
| slurm\_node\_gpu\_total | count | node | The total number of GPUs per node. |
| slurm\_nodes\_alloc | count | -- | The number of nodes with state allocated. |
| slurm\_nodes\_comp | count | -- | The number of nodes with state completing. |
| slurm\_nodes\_down | count | -- | The number of nodes with state down. |
| slurm\_nodes\_drain | count | -- | The number of nodes with state drain. |
| slurm\_nodes\_err | count | -- | The number of nodes with state error. |
| slurm\_nodes\_fail | count | -- | The number of nodes with state fail. |
| slurm\_nodes\_idle | count | -- | The number of nodes with state idle. |
| slurm\_nodes\_maint | count | -- | The number of nodes with state maintenance. |
| slurm\_nodes\_mix | count | -- | The number of nodes with state mix. |
| slurm\_nodes\_resv | count | -- | The number of nodes with state reserved. |
| slurm\_nodes\_total | count | -- | The total number of nodes. |
| slurm\_nodes\_not\_responding | count | -- | The number of nodes with state not\_responding. |
| slurm\_partition\_cpu\_alloc | count | partition | The number of CPUs allocated in a partition. |
| slurm\_partition\_cpu\_idle | count | partition | The number of CPUs idle in a partition. |
| slurm\_partition\_cpu\_total | count | partition | The total number of CPUs in a partition. |
| slurm\_partition\_mem\_alloc | MB | partition | The amount of allocated memory in a partition. |
| slurm\_partition\_mem\_total | MB | partition | The total memory in a partition. |
| slurm\_partition\_gpu\_alloc | count | partition | The number of GPUs allocated in a partition. |
| slurm\_partition\_gpu\_idle | count | partition | The number of GPUs idle in a partition. |
| slurm\_partition\_gpu\_total | count | partition | The total number of GPUs in a partition. |
| slurm\_queue\_canceled | count | -- | The number of canceled jobs in the Slurm cluster (only those still tracked by slurmctld). |
| slurm\_queue\_completed | count | -- | The number of completed jobs in the Slurm cluster (only those still tracked by slurmctld). |
| slurm\_queue\_completing | count | -- | The number of completing jobs in the Slurm cluster. |
| slurm\_queue\_configuring | count | -- | The number of configuring jobs in the Slurm cluster. |
| slurm\_queue\_failed | count | -- | The number of failed jobs in the Slurm cluster (only those still tracked by slurmctld). |
| slurm\_queue\_node\_fail | count | -- | The number of jobs stopped due to node failure in the cluster (only those still tracked by slurmctld). |
| slurm\_queue\_pending | count | -- | The number of pending jobs in the Slurm scheduler queue. |
| slurm\_queue\_pending\_dependency | count | -- | The number of pending jobs in the Slurm scheduler queue with unsatisfied dependencies. |
| slurm\_queue\_preempted | count | -- | The number of preempted jobs in the Slurm cluster (only those still tracked by slurmctld). |
| slurm\_queue\_running | count | -- | The number of running jobs in the Slurm cluster. |
| slurm\_queue\_suspended | count | -- | The number of suspended jobs in the Slurm cluster. |
| slurm\_queue\_timeout | count | -- | The number of timed out jobs in the Slurm cluster (only those still tracked by slurmctld). |
| slurm\_scheduler\_backfill\_cycle\_last\_seconds | seconds | -- | The duration of the last scheduler backfill cycle. |
| slurm\_scheduler\_backfill\_cycle\_mean\_seconds | seconds | -- | The mean duration of the scheduler backfill cycles. |
| slurm\_scheduler\_backfill\_depth\_mean | count | -- | The mean depth of the scheduler backfill. |
| slurm\_scheduler\_backfilled\_jobs\_total | count | -- | The number of jobs started due to backfilling since last Slurm start. |
| slurm\_scheduler\_backfilled\_jobs\_cycle\_total | count | -- | The number of jobs started due to backfilling since last time stats were reset. |
| slurm\_scheduler\_backfilled\_jobs\_heterogeneous\_total | count | -- | The number of heterogeneous jobs started due to backfilling since last Slurm start. |
| slurm\_scheduler\_cycle\_last\_seconds | seconds | -- | The duration of the last scheduler cycle. |
| slurm\_scheduler\_cycle\_mean\_seconds | seconds | -- | The mean duration of the scheduler cycles. |
| slurm\_scheduler\_cycles\_per\_minute | opm | -- | The number of scheduler cycles per minute. |
| slurm\_scheduler\_dbd\_queue | count | -- | The number of items in the scheduler dbd agent queue. |
| slurm\_scheduler\_jobs\_submitted | count | -- | The number of submitted jobs reported by the scheduler. |
| slurm\_scheduler\_jobs\_started | count | -- | The number of jobs started by the scheduler. |
| slurm\_scheduler\_jobs\_completed | count | -- | The number of jobs completed by the scheduler. |
| slurm\_scheduler\_jobs\_failed | count | -- | The number of jobs failed by the scheduler. |
| slurm\_scheduler\_jobs\_cancelled | count | -- | The number of jobs canceled by the scheduler. |
| slurm\_scheduler\_jobs\_pending | count | -- | The number of jobs pending in the scheduler queue. |
| slurm\_scheduler\_jobs\_running | count | -- | The number of jobs currently running in the scheduler. |
| slurm\_scheduler\_queue | count | -- | The number of items in the scheduler queue. |
| slurm\_scheduler\_threads | count | -- | The number of scheduler threads. |
| slurm\_scheduler\_cycle\_mean\_depth | count | -- | The mean depth of the scheduler cycles. |
