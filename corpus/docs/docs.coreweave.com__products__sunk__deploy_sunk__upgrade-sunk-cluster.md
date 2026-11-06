# Upgrade a SUNK Self-Service cluster

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/upgrade-sunk-cluster

# Upgrade a SUNK Self-Service cluster

> Upgrade or patch a SUNK Self-Service cluster by changing its version fields, and what to expect during the rollout

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

A SUNK Self-Service cluster runs a specific set of software versions, declared on the `SunkCluster` resource. Upgrading a cluster means moving those versions forward. This page covers the version fields that determine what a cluster runs, how an upgrade rolls out and affects running jobs, and the steps to upgrade or patch a cluster.

CoreWeave doesn't upgrade your cluster for you. A cluster stays on the versions set in its `SunkCluster` resource until you change them, including after a newer SUNK release or a patch release ships. You decide when to upgrade. CoreWeave does update the out-of-band operator separately, without changing the versions your cluster runs.

## Version fields

Four fields on `spec` determine the versions a cluster runs:

| Field | Controls | Notes |
| - | - | - |
| `sunkVersion` | The SUNK release version. | Optional. A new cluster that leaves it out gets the latest SUNK release available on SUNK Self-Service, and the value doesn't change when that default changes. See [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md). |
| `slurmVersion` | The Slurm version. | Optional. A new cluster that leaves it out gets the Slurm build that ships with the default SUNK release. Use a Slurm release that your SUNK major version supports, for example Slurm 25.11 on SUNK 8. |
| `cudaVersion` | The CUDA version installed on compute nodes. | Optional. Defaults to `13.0`. Allowed values: `13.0`, `13.1`. |
| `ubuntuVersion` | The Ubuntu base image version for nodes. | Optional. Defaults to `24.04`. Allowed values: `22.04`, `24.04`. |

You can upgrade `sunkVersion` and `slurmVersion` together or one at a time, for example to pick up a fix in only one of them. `slurmVersion` must be a Slurm release that your SUNK major version supports, for example Slurm 25.11 on SUNK 8. The [version mapping table](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md) lists the Slurm build that ships with each SUNK release. Add a leading `v` to `slurmVersion`. `sunkVersion` works with or without the `v`. For the full field definitions, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#top-level-spec-fields).

## What changes during an upgrade

The `slurmVersion`, `ubuntuVersion`, and `cudaVersion` fields determine the compute node image, and `sunkVersion` sets the version of the SUNK operator that manages the cluster. When a cluster moves to a new version, the out-of-band operator regenerates the underlying cluster configuration and the compute `NodeSets` roll to the new image. Because `NodeSets` use a rolling update strategy, nodes are replaced gradually rather than all at once.

Rolling a compute node does not interrupt the Slurm jobs already running on it. `NodeSets` roll using [safe deletion](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#safe-deletion): the Syncer drains the Slurm node first, and the Pod is only replaced after the node is both drained and idle. The rollout replaces not-ready and idle Pods first, then waits for the remaining Pods to finish their work. As a result, a long-running job can hold its node at the old version until the job completes.

Each `NodeSet` replaces one node at a time, and you can't change this through the `SunkCluster` resource. The nodes waiting their turn keep accepting new jobs, so on a busy cluster with long-running jobs, a rollout can take days. A draining node accepts no new jobs, so the cluster's schedulable capacity also shrinks while the rollout progresses.

To keep a rollout from waiting on long jobs, requeue the jobs on a draining node so they restart elsewhere:

```bash theme={"system"}
scontrol requeue [JOB-ID]
```

Only batch jobs can be requeued. A requeued job restarts from the beginning unless it resumes from a checkpoint.

Upgrading the Slurm control plane briefly restarts the control plane workloads. Submitted and queued jobs are preserved in `slurmctld`'s saved state, which lives on a dedicated persistent volume, so they survive the restart, but the cluster is momentarily unavailable for new scheduling decisions while the controller comes back up.

## Find out about new releases

CoreWeave announces new SUNK releases, including patch releases, in the [release notes](https://docs.coreweave.com/release-notes.md), and adds each release to the [version mapping table](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md). When a patch release fixes a security issue, CoreWeave Support can also notify affected customers directly.

A patch release contains bug fixes for the release it patches, and can keep the same Slurm build. The version mapping table shows the Slurm build for each release. You apply a patch release the same way you apply any other upgrade, by following the steps in [Upgrade the cluster](#upgrade-the-cluster).

## Upgrade the cluster

To upgrade or patch a cluster, change its version fields on the `SunkCluster` resource. The examples in this section use the `tenant-slurm` namespace, which is the namespace the Cloud Console uses. Replace it if your `SunkCluster` is in a different namespace.

**1. Choose the target versions**

SUNK Self-Service runs SUNK 8.0 and later. See [Supported configurations](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md#supported-configurations). If you have questions about an upgrade, [contact CoreWeave Support](https://docs.coreweave.com/support.md).

To upgrade SUNK, pick its release from the [version mapping table](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md). If you also want that release's default Slurm build, take `slurmVersion` from the same row. To upgrade only Slurm, pick a Slurm build from the table that your SUNK major version supports, for example any 25.11 build on SUNK 8.

Read the [release notes](https://docs.coreweave.com/release-notes.md) for the target release and any releases between it and your current version.

To see the versions the cluster runs now, read them from the `SunkCluster`:

```bash theme={"system"}
kubectl get sunkcluster [CLUSTER-NAME] -n tenant-slurm \
  -o jsonpath='{.spec.sunkVersion}{" "}{.spec.slurmVersion}{"\n"}'
```

**2. Plan for running jobs**

Each compute node waits for its running jobs to finish before it rolls, and each `NodeSet` rolls one node at a time, so a rollout on a busy cluster can take days. Decide whether to let long-running jobs finish or to requeue them with `scontrol requeue` so the rollout finishes sooner. See [What changes during an upgrade](#what-changes-during-an-upgrade).

Because a cluster can't be rolled back, confirm the target versions before you continue. See [Roll back an upgrade](#roll-back-an-upgrade).

**3. Change the version fields**

Set the version fields you're upgrading, adding a leading `v` to `slurmVersion`. The following command sets both. To upgrade one component, include only its field:

```bash theme={"system"}
kubectl patch sunkcluster [CLUSTER-NAME] -n tenant-slurm --type=merge \
  -p '{"spec":{"sunkVersion":"[SUNK-VERSION]","slurmVersion":"[SLURM-VERSION]"}}'
```

* `[SUNK-VERSION]`: the SUNK release from the version mapping table. The leading `v` is optional.
* `[SLURM-VERSION]`: the Slurm build from the version mapping table, with a leading `v`.

If you manage the `SunkCluster` manifest in source control, edit the fields in the manifest and apply it instead:

```bash theme={"system"}
kubectl apply -f sunkcluster.yaml
```

**4. Watch the rollout**

Watch the `SunkCluster` until the `READY` column shows `Ready`. The column shows the reason on the `Ready` condition, and the `NODESETS`, `SLURMCLUSTER`, and `CONTROLLERMANAGER` columns show the reasons on the dependent conditions:

```bash theme={"system"}
kubectl get sunkcluster [CLUSTER-NAME] -n tenant-slurm -w
```

While the rollout runs, `Ready` is `False` with `reason: Degraded`, and its `message` lists the dependent conditions that aren't ready yet, for example `Was ready, now failing conditions: NodeSetsAvailable`. `ControllerManagerAvailable` and `SlurmClusterAvailable` report `reason: InProgress` while the SUNK operator and the Slurm control plane restart, and `NodeSetsAvailable` reports `reason: InProgress` while compute Pods aren't ready. For the full list of conditions and reasons, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#status-conditions).

To see the conditions in detail, inspect the full resource:

```bash theme={"system"}
kubectl get sunkcluster [CLUSTER-NAME] -n tenant-slurm -o yaml
```

How long the rollout takes depends mostly on the number of compute nodes and on how long running jobs hold them.

`Ready` can return to `True` before every node has rolled. `NodeSetsAvailable` checks that the compute Pods are ready, not that they run the new version, and a node waiting on a running job keeps its ready Pod on the old version. To confirm that the rollout finished, list the `NodeSets`:

```bash theme={"system"}
kubectl get nodesets -n tenant-slurm
```

The upgrade is complete when `Ready` is `True` and `UP-TO-DATE` equals `DESIRED` for every `NodeSet`.

If the replaced Slurm Pods report `ErrImagePull` or `ImagePullBackOff`, check that `slurmVersion` has its leading `v` and names a Slurm build in the version mapping table, then correct the value.

If a condition reports `reason: Error`, or the rollout stops progressing while no jobs are holding nodes, open a support ticket. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include the cluster name, the versions you upgraded from and to, and the output of `kubectl get sunkcluster [CLUSTER-NAME] -n tenant-slurm -o yaml`.

## Roll back an upgrade

Rolling a cluster back to an earlier version isn't supported. Slurm doesn't support downgrades, because an upgrade can convert the controller state and the accounting database to the newer version's format. Don't set `sunkVersion` or `slurmVersion` to an earlier release: the out-of-band operator doesn't block the change, so it rolls out like an upgrade.

If an upgrade causes a problem, open a support ticket instead of changing the versions back. Include the details listed in [Upgrade the cluster](#upgrade-the-cluster).

## Related

For more information, see the following pages:

* [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md) for the Slurm build that ships with each SUNK release.
* [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#top-level-spec-fields) for the version field definitions.
* [NodeSet](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#rolling-upgrade) for how a rolling upgrade orders and drains Pods.
