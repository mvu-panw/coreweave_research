# IMEX overview

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/imex-overview

# IMEX overview

> What Internode Memory Exchange is and how CoreWeave Kubernetes Service exposes IMEX on rack-scale GPU instances

[Internode Memory Exchange (IMEX)](https://docs.nvidia.com/multi-node-nvlink-systems/imex-guide/overview.html) is NVIDIA's service for mapping GPU memory across compute Nodes that belong to the same NVLink domain. IMEX works at the driver level so that CUDA applications and communication libraries such as NCCL can transparently import and export memory over NVLink, rather than treating each Node as an isolated GPU pool.

On CoreWeave, IMEX matters most for [rack-scale, NVLink-connected systems](https://docs.coreweave.com/platform/instances/nvl72.md) where a single distributed job must treat GPUs across Nodes as one large memory fabric. If your workload doesn't rely on cross-Node NVLink memory access, you don't need to think about IMEX.

## NVLink domains and placement

An **NVLink domain** (sometimes called an NVLink cluster) is the set of Nodes that can reach each other over NVLink. Your Pods must land on Nodes that are part of the same domain, or cross-Node NVLink memory access won't work as expected.

In practice, that means you must align scheduling with physical connectivity. On [NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md), all Nodes in a single rack share the same NVLink domain. The `nvidia.com/gpu.clique` label identifies the **NVLink partition** within that domain. Workloads must use this label as a Pod affinity `topologyKey` so that all related Pods land on Nodes in the same partition. On CKS full-rack deployments, the default partition spans the entire domain, so partition and domain boundaries align. For the mechanics of setting this up, see [IMEX with Dynamic Resource Allocation](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling.md).

## VPC primary prefix requirement

IMEX address mapping depends on Nodes receiving physical-location-based IP addresses from the VPC underlay. This mapping only works when the VPC primary host prefix is no smaller than your zone's default host prefix.

> [!WARNING]
>
> For [NVL72 rack-level instances](https://docs.coreweave.com/platform/instances/nvl72.md), provision the VPC with a primary host prefix no smaller than the zone default. For example if your region has a /18 prefix, use a subnet mask of at least that size or larger. A smaller prefix forces dynamic address allocation, which will break standard IMEX. Note that IMEX DRA does not have that limitation. For your zone's default host prefix, see [Create and manage VPCs](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md#host-prefixes).

## IMEX on CoreWeave Kubernetes Service

CoreWeave delivers IMEX **channel** access to workloads through Kubernetes [Dynamic Resource Allocation](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) and the NVIDIA DRA driver. You declare a `ComputeDomain` and attach `ResourceClaims` to Pods that need IMEX. The platform provisions the supporting IMEX-related components on the Node. You don't manually configure low-level IMEX services inside your containers.

IMEX with DRA is in **Limited Availability** on supported instance types and continues to evolve. For prerequisites, enablement, and full YAML examples, read [IMEX with Dynamic Resource Allocation](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling.md).

> [!NOTE]
>
> Earlier clusters used a transparent `nvidia-imex` DaemonSet model for IMEX channels. New work should use DRA and `ComputeDomain` resources. See [Cluster Components](https://docs.coreweave.com/products/cks/reference/cluster-components.md) for how these pieces fit together.

## Where to go next

The following resources provide more context and configuration guidance:

* [IMEX with Dynamic Resource Allocation](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling.md): create `ComputeDomain` objects, claim IMEX channels, and verify `ResourceClaim` state.
* [NVIDIA IMEX guide](https://docs.nvidia.com/multi-node-nvlink-systems/imex-guide/overview.html): background on NVLink multi-Node architecture, IMEX behavior, and terminology such as Fabric Manager roles (for administrators who need NVIDIA's full reference).
