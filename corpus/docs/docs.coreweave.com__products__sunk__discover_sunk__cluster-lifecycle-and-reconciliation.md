# SUNK Self-Service cluster lifecycle and reconciliation

Source: https://docs.coreweave.com/products/sunk/discover_sunk/cluster-lifecycle-and-reconciliation

# SUNK Self-Service cluster lifecycle and reconciliation

> How a SUNK Self-Service cluster is created and reconciled, and how to read its status conditions to track progress

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

A SUNK Self-Service cluster is reconciled, not scripted. You declare the cluster you want in a `SunkCluster` resource, and the operators continuously work to make the running cluster match that declaration. This page explains the reconciliation model, the order in which a cluster comes up, and how to read the status conditions that report progress.

## The reconciliation model

Reconciliation is the continuous loop that drives a cluster's actual state toward the desired state you declare. The `SunkCluster` resource is the desired state. Two operators reconcile it: the out-of-band operator turns your `SunkCluster` into managed `NodePools` and a generated `SlurmCluster` resource, and the in-cluster operator turns that `SlurmCluster` into the running Slurm control plane. For where each operator runs and what else it manages, see [SUNK Self-Service architecture](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md).

Because the loop is continuous, reconciliation governs the whole lifecycle, not just creation. When you change a mutable field, such as scaling a node count, the operators reconcile the difference. When a component fails, the operators work to restore it. The status conditions described later report the result of each loop.

## Creation ordering

A cluster comes up in dependency order: each stage depends on the one before it. The first stage is a prerequisite you provide; the rest are reconciled for you after you apply the `SunkCluster`.

| Stage | What it produces | Provided by |
| - | - | - |
| CKS cluster | The Kubernetes cluster that hosts SUNK. After you apply the `SunkCluster`, the out-of-band operator installs the SUNK operator in it. | You, as a prerequisite |
| `SunkCluster` resource | The declared cluster specification, applied to a namespace of your choice. | You (Console or CR) |
| `NodePools` | The managed pools that provision the physical Nodes for compute and the control plane. | Out-of-band operator |
| `NodeSets` | The Slurm compute node definitions backed by the Nodes from the compute `NodePools`. | Out-of-band operator |
| `SlurmCluster` | The Slurm control plane (`slurmctld`, accounting, the Syncer, and the scheduler if you enable it) and the login Pods your users connect to over SSH. | Out-of-band operator generates the resource, and the in-cluster operator runs the control plane from it |

Until a stage's dependency is satisfied, the stage can't complete. For example, `NodeSets` can't report ready Pods until their `NodePools` have provisioned Nodes, and the `SlurmCluster` can't bring up `slurmctld` until the control-plane Nodes exist. This dependency chain is why the status conditions described next become ready in roughly the same order.

> [!NOTE]
>
> Node provisioning is usually the longest stage. A new cluster can take up to around 40 minutes to become ready, and most of that time is the `NodePools` reaching their target Node count. Once Nodes are available, the Slurm control plane and login Pods come up quickly.

## Track progress with status conditions

The `SunkCluster` reports its progress through `status.conditions`. Inspect them at any time. Replace `[NAMESPACE]` with the namespace you applied the `SunkCluster` to:

```bash theme={"system"}
kubectl get sunkcluster -n [NAMESPACE] -o yaml
```

The aggregate `Ready` condition is the single signal for whether the cluster is fully reconciled. It's `True` only when every dependent condition is `True`. While the cluster is coming up for the first time, `Ready` reports `reason: Bootstrapping` and a `message` that lists the dependent conditions still pending, such as `Waiting for conditions: NodePoolsAvailable, NodeSetsAvailable, SlurmClusterAvailable`.

Three of the dependent conditions track the stages of the creation ordering, so the one that is not yet `Ready` tells you where the cluster is:

* `NodePoolsAvailable` covers the `NodePools` stage.
* `NodeSetsAvailable` covers the `NodeSets` stage.
* `SlurmClusterAvailable` aggregates the `SlurmCluster`, including `slurmctld`, accounting, login Pods, the Syncer, and the scheduler.

The other dependent conditions track supporting components, such as the SUNK operator Deployment and the NVIDIA device plugin.

Each condition carries a `reason`, one of `Ready` (satisfied), `InProgress` (working), `Bootstrapping` (set on the aggregate `Ready` during first creation), or `Error` (failed). The `message` adds detail and usually names the specific resources still pending, such as `NodePools not at target: [a192, gb200]` or `NodeSets not ready: [a192 (0/36 ready)]`.

When `SlurmClusterAvailable` is not `True`, inspect the underlying `SlurmCluster` to find which subcomponent is pending or failing. Use the same namespace as the `SunkCluster`:

```bash theme={"system"}
kubectl get slurmcluster -n [NAMESPACE] -o yaml
```

For the complete set of conditions, including the `SlurmCluster` subcomponent conditions and the `lastReadyTime` field, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#status-conditions).

### Bootstrapping compared to a regression

The status distinguishes a cluster that has never been ready from one that was ready and then regressed. The `lastReadyTime` field records the most recent time `Ready` became `True`:

* If `lastReadyTime` is unset and `Ready` reports `reason: Bootstrapping`, the cluster is still coming up for the first time.
* If `lastReadyTime` is set but `Ready` is now `False`, the cluster was previously healthy and a component has regressed. The dependent condition in `reason: Error` or `reason: InProgress` indicates which one.

## Ongoing reconciliation

After a cluster is ready, the operators keep reconciling it against the `SunkCluster` resource. Editing a mutable field, such as a node `count`, prompts the operators to reconcile the change: scaling a count up or down adjusts the underlying `NodePool` and `NodeSet`. Immutable fields, such as a node entry's `name` and `instanceType`, are fixed after creation. For which fields are mutable and the effect of changing version fields, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference).

If a cluster is stuck with `Ready: False`, the most common cause is insufficient quota. Insufficient Node Pool quota holds `NodePoolsAvailable` in `reason: InProgress`, and insufficient DFS quota usually sets `VolumesAvailable` or `SlurmClusterAvailable` to `reason: Error`. A rejected database volume instead leaves `SlurmClusterAvailable` in `reason: InProgress`. See [Storage volume creation fails](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md#storage-volume-creation-fails) for that case, and [Troubleshoot](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md#troubleshoot) for common failure modes and fixes.
