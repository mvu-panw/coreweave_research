# SlurmCluster

Source: https://docs.coreweave.com/products/sunk/discover_sunk/slurmcluster

# SlurmCluster

> The SlurmCluster CRD that configures cluster-wide Slurm information and generates topology files

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The SlurmCluster CRD configures and synchronizes Slurm's cluster-wide information. It creates the topology files Slurm uses when network topology is enabled.

This page describes how the SlurmCluster controller generates topology configuration so that cluster administrators can understand which Node labels drive topology output and how to select the appropriate topology plugin for their hardware.

## Topology ConfigMap generation

Slurm supports a topology plugin, which helps the Slurm Scheduler run related jobs on nearby Nodes to improve performance.

The topology is defined in [topology.conf](https://slurm.schedmd.com/topology.conf.html). The controller generates this file automatically based on Node labels. The file is saved into a ConfigMap and mounted into containers so you can update it without restarting the Pods. Only `scontrol reload` is required to apply the changes to the Slurm cluster.

Because the topology file is cluster-wide, duplicate entries aren't possible. Therefore, the topology can't be generated on a per-NodeSet basis. The SlurmCluster Controller generates the topology based on Node labels that describe the network topology.

SUNK supports two topology plugins: tree and block. The following sections describe how to switch between plugins and what Node labels each plugin uses.

### Change the topology plugin

The `topology.conf` can contain both topology definitions at the same time if labels for both are present on Nodes, but only one topology plugin can be active at a time.

The default is tree topology. To use block topology, set `TopologyPlugin: topology/block` under [`slurmConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) in the `slurm` chart values in SUNK Standard, or under `spec.slurmConfig` in the `SunkCluster` in SUNK Self-Service.

### Tree topology

The tree topology implementation expects an InfiniBand-style network structure. The Node labels are as follows:

* `ib.coreweave.cloud/fabric` - Indicates the top-level IB fabric the Node belongs to, to support multiple fabrics.
* `ib.coreweave.cloud/superpod` - The superpod within an IB fabric the Node belongs to.
* `ib.coreweave.cloud/leafgroup` - The leafgroup within the IB superpod the Node belongs to.
* `node.coreweave.cloud/datahall` - The datahall the Node is located in, used to make the leafgroup value unique. This label is optional.

The fabric and superpod labels must be unique within the cluster. If datahall isn't used, the leafgroup value must also be unique within the cluster. If datahall is used, the combined datahall + leafgroup value must be unique within the cluster.

For example, this is appropriate:

* F1 -> SP1 -> LG1, LG2
* F1 -> SP2 -> LG3, LG4
* F1 -> SP3 -> DH1-LG3, DH2-LG3

While this is not:

* F1 -> SP1 -> LG1, LG2
* F1 -> SP2 -> LG1, DH1-LG2
* F1 -> SP3 -> DH1-LG2, DH2-LG3

Only Nodes that have all the required labels can be pulled in correctly. If a Node is missing the required topology labels, the generated topology omits it.

### Block topology

The [block topology](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md) implementation is designed for NVlink systems, with one block per NVlink domain.

One block is generated for each unique `ds.coreweave.com/nvlink.domain` label value on the Nodes.

The block size is set to the size of the largest block. If a block has fewer than two Nodes, the controller emits no block topology configuration.
