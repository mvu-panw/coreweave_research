# SUNK Self-Service architecture

Source: https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture

# SUNK Self-Service architecture

> The two operators behind SUNK Self-Service: where each runs, what it watches, and what it creates

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Two operators run a SUNK Self-Service cluster. The out-of-band operator runs in a CoreWeave-managed control plane and turns your `SunkCluster` resource into the resources that make up a cluster. The in-cluster operator runs inside your CoreWeave Kubernetes Service (CKS) cluster and turns those resources into a running Slurm cluster. This page explains what each operator does, where it runs, and how the two divide the work.

For what SUNK Self-Service provisions and the two ways to create a cluster, see [About SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md). For the order in which a cluster comes up and how to read its status conditions, see [SUNK Self-Service cluster lifecycle and reconciliation](https://docs.coreweave.com/products/sunk/discover_sunk/cluster-lifecycle-and-reconciliation.md).

## Two operators

The following table summarizes where each operator runs and what it manages. The sections after the table describe each operator in more detail.

| Operator | Where it runs | Watches | Creates or manages |
| - | - | - | - |
| Out-of-band operator | A CoreWeave-managed control plane, outside your CKS cluster | `SunkCluster` | The SUNK custom resource definitions (CRDs), the in-cluster operator, the Node Pools, the NodeSets, the shared storage volumes, and the generated `SlurmCluster` resource |
| In-cluster operator | Your CKS cluster, as the `sunk-controller-manager` Deployment in the `cw-sunk` namespace | `SlurmCluster`, NodeSets | `slurmctld`, the accounting database, the login Pods, the [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md), the [scheduler](https://docs.coreweave.com/products/sunk/discover_sunk/scheduler.md) when it's enabled, and the `slurmd` Pods |

### Out-of-band operator

The out-of-band operator reconciles `SunkCluster` resources. It runs outside your CKS cluster, and CoreWeave deploys, operates, and upgrades it. You don't install or maintain the out-of-band operator yourself.

When you apply a `SunkCluster`, the out-of-band operator does two kinds of work in your cluster:

* **Installs SUNK.** It applies the SUNK CRDs, including `NodeSet` and `SlurmCluster`, creates the `cw-sunk` namespace with the permissions SUNK needs, and deploys the in-cluster operator there.
* **Builds your cluster's resources.** It creates one Node Pool for each entry in the `SunkCluster` resource's `nodes` list, and one NodeSet for each compute entry. A control-plane entry, one with `controlPlane: true`, gets a Node Pool but no NodeSet. It also creates the shared storage volumes, deploys supporting components such as GPU device scheduling, and generates a `SlurmCluster` resource from your `SunkCluster`. It creates the NodeSets and the `SlurmCluster` in the same namespace as the `SunkCluster`, and the `SunkCluster` owns them.

It keeps reconciling after the cluster is running. When you change a node count, for example, it scales the matching Node Pool and NodeSet.

### In-cluster operator

The in-cluster operator runs inside your CKS cluster as the `sunk-controller-manager` Deployment in the `cw-sunk` namespace. It reconciles the `SlurmCluster` resource into the login Pods your users connect to and the Slurm control plane: `slurmctld`, the accounting database, and the Syncer that keeps Slurm node state aligned with Kubernetes. It runs the scheduler only when `spec.scheduler.enabled` is `true` in your `SunkCluster`, and that field defaults to `false`. It also reconciles each [NodeSet](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md) into the `slurmd` Pods, one per Kubernetes Node.

The [Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md) and the [Pod Controller](https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller.md) are part of the same Deployment. The `sunkVersion` field in your `SunkCluster` sets which version of the in-cluster operator runs. See [Upgrade a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/upgrade-sunk-cluster.md).

> [!NOTE]
>
> The in-cluster operator is the SUNK operator, the same operator that the `sunk` Helm chart installs in SUNK Standard. The out-of-band operator is the part that SUNK Self-Service adds to it.

## The `SlurmCluster` is an internal interface

You configure a SUNK Self-Service cluster through the `SunkCluster` resource. The out-of-band operator translates it into the `SlurmCluster` resource that the in-cluster operator consumes, and reapplies the fields it manages every time it reconciles. A direct edit to one of those fields in the generated `SlurmCluster` doesn't last, so make the change in the `SunkCluster` instead. For the fields you can set, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference).

The `SlurmCluster` is still useful for troubleshooting. Both resources report status conditions. When the `SunkCluster` condition `SlurmClusterAvailable` isn't `True`, the `SlurmCluster` conditions show which part of the Slurm control plane is pending. See [Track progress with status conditions](https://docs.coreweave.com/products/sunk/discover_sunk/cluster-lifecycle-and-reconciliation.md#track-progress-with-status-conditions).

## Where each component runs

The CoreWeave-managed control plane holds only the out-of-band operator. Everything else runs in your CKS cluster:

* **In the `cw-sunk` namespace:** the in-cluster operator, and supporting components that the out-of-band operator deploys, such as the NVIDIA device plugin.
* **In your `SunkCluster` resource's namespace:** the NodeSets, the `SlurmCluster`, and the Slurm control plane and login Pods the in-cluster operator creates from it.
* **On your CKS Nodes:** the Slurm compute nodes, each a `slurmd` Pod on one Kubernetes Node. See [Compute and login nodes](https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes.md).

Your users connect to the login Pods over SSH, and user provisioning keeps their POSIX and Slurm identities in sync with the groups you authorize. See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md).

## Related topics

* [About SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md): what SUNK Self-Service provisions and what stays your responsibility.
* [SUNK Self-Service cluster lifecycle and reconciliation](https://docs.coreweave.com/products/sunk/discover_sunk/cluster-lifecycle-and-reconciliation.md): creation order, status conditions, and ongoing reconciliation.
* [Get started with SUNK Self-Service using the SunkCluster CR](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md): create a cluster from a manifest, end to end.
* [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference): every field and status condition.
* [SlurmCluster](https://docs.coreweave.com/products/sunk/discover_sunk/slurmcluster.md): the `SlurmCluster` CRD and the topology files it generates.
