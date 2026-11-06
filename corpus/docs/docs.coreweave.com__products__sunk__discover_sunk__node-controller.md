# Node Controller

Source: https://docs.coreweave.com/products/sunk/discover_sunk/node-controller

# Node Controller

> How the SUNK Node Controller synchronizes data between Kubernetes Nodes and slurmd Pods

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page describes how the SUNK Node Controller keeps Kubernetes Nodes in sync with Slurm-managed workloads, and what labels, annotations, and conditions it manages. Read this page to understand which Node-level signals SUNK owns. With that context, you can predict how Slurm state changes appear on the underlying Kubernetes Nodes when you operate or troubleshoot a SUNK cluster.

The SUNK Node Controller is distinct from the [CoreWeave Node lifecycle controller](https://docs.coreweave.com/glossary.md#coreweave-node-lifecycle-controller), which coordinates Node lifecycle state transitions.

The Node Controller manages data synchronized between Kubernetes Nodes and the NodeSlices and `slurmd` Pods, which [NodeSets](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md) manage. The Node Controller is deployed cluster-wide as part of the `sunk-controller-manager`. The Node Controller performs all Node operations on behalf of the individual Slurm cluster instances, which removes the requirement to grant extra permissions to modify Kubernetes Nodes.

## Information flow and operations

The Node Controller handles the flow of information from the NodeSlices to the Node and from the `slurmd` Pods to the Node. The sections that follow describe the most common information flows the Node Controller manages, including Node locking, drain handling, Pod-to-Node condition synchronization, and NodeSet labeling.

### Node lock

Because a `slurmd` Pod is idle when the Slurm node is idle, other Kubernetes workloads might schedule on the Kubernetes Node. However, when the `slurmd` Pod becomes active, SUNK must evict these other workloads and prevent them from rescheduling. Node locking accomplishes this.

The Node Controller manages the lock status. The Pod Controller then [propagates the lock annotation](https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller.md#node-lock) back to the Pod, where the [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md#pre-hook) picks it up.

### Slurm drain annotation and cordon condition

When a Slurm node is [put into a drain state](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md), the Pod has a condition and annotation set as follows:

* The node annotation containing the drain reason is `sunk.coreweave.com/drain`.
* The node condition for Cordon is `SlurmCordon`.
* When the Pod state isn't known, the condition is `Unknown`.

This allows Kubernetes to react to drain events in Slurm. The annotation reflects the Slurm reason for the drain. The Node Controller only sets the `SlurmCordon` condition if the drain originated in Slurm, rather than from a Kubernetes state.

### Pod conditions

In addition to the special handling of the `SlurmCordon` condition, the Node Controller synchronizes the following conditions from the Pod to the Node:

* `SlurmDrain`
* `SlurmRunning`
* `SlurmNotResponding`

These conditions are present on the Node when it's part of the NodeSet, and removed when the Node is no longer in the NodeSet. If the respective Pod is missing any of these conditions, the condition's status is set to `Unknown`.

### NodeSet labels

To identify Nodes associated with a particular NodeSet, the Node Controller labels them with information obtained from the NodeSlice objects. When a Node is present in a NodeSlice, the Node Controller labels it. If a Node isn't present in any NodeSlice, the labels are removed. Relevant labels include:

* `sunk.coreweave.com/nodeset` - The name of the NodeSet the Node is associated with.
* `sunk.coreweave.com/namespace` - The namespace of the NodeSet.
* `sunk.coreweave.com/cluster` - The name of the cluster the NodeSet is associated with.
* `sunk.coreweave.com/pod` - The name of the associated Pod, if present.

Together, these labels let operators and other controllers identify which NodeSet, namespace, cluster, and Pod each Kubernetes Node currently belongs to.
