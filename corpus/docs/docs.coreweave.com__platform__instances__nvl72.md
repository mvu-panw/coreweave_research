# About NVL72-powered instances

Source: https://docs.coreweave.com/platform/instances/nvl72

# About NVL72-powered instances

> Learn how NVL72-powered instances deliver efficient, high-performance, energy-conscious AI compute power

AI models with trillions of parameters are increasingly common, and the demand for computational power is surging. Traditional GPU solutions struggle to meet these demands, which leads to development bottlenecks, high energy consumption, and escalating costs.

CoreWeave's NVL72-powered instances address these challenges by harnessing the architecture of NVIDIA's Vera Rubin and Grace Blackwell superchips and the NVLink Switch System. Liquid cooling improves efficiency by consuming less energy than traditional air-cooled systems. Choose these instances when you need high performance for large-scale AI training and inference, large memory capacity for massive datasets, and fast GPU-to-GPU communication for distributed computing.

## Vera Rubin instances

CoreWeave's [Vera Rubin instances](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) pair NVIDIA Rubin GPUs with NVIDIA Vera Arm CPUs and connect over sixth-generation NVLink. They use NVIDIA Spectrum-X RoCE (RDMA over Converged Ethernet) with BlueField-4 and ConnectX-9 SuperNICs for large-scale AI in Ethernet-based cloud environments. For detailed specifications, see the [Vera Rubin NVL72 instance page](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md).

## GB300 instances

CoreWeave's GB300 instances are offered in two specialized networking configurations that deliver 800 Gbps of bandwidth:

* [GB300 instances with Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) are optimized for low latency in traditional HPC and large-scale AI training.
* [GB300 instances with Spectrum-X RoCE (RDMA over Converged Ethernet)](https://docs.coreweave.com/platform/instances/gpu/gb300-4x-e.md) use BlueField-3 and ConnectX-8 SuperNICs for large-scale AI in Ethernet-based cloud environments.

## GB200 instances

CoreWeave's [GB200 instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) are powered by 4x NVIDIA GB200 GPUs and connected with 400 Gb/s NDR InfiniBand, built on the NVIDIA Quantum-2 InfiniBand fabric.

## Deploy NVL72-powered instances as full racks

NVL72-powered instances must be deployed as **full racks of 18 Nodes** to ensure optimal performance. CKS enforces full-rack deployment and won't allow requesting partial racks.

When deploying Node Pools for rack-based instances, use `targetRacks` to request Nodes at the rack level. You can still use `targetNodes`, but the value must be a multiple of 18, such as 36 or 54.

Use `targetRacks` to specify the number of racks directly, where each rack contains 18 Nodes:

```yaml title="NodePool using targetRacks" {8} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gb200-4x
  targetRacks: 1
```

Alternatively, use `targetNodes` set to a multiple of **18**, such as **18**, **36**, or **54**:

```yaml title="NodePool using targetNodes" {8} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gb200-4x
  targetNodes: 18
```

> [!NOTE]
>
> Autoscaling is not supported for rack-based instance types. Setting `autoscaling: true` on a Node Pool with a GB200, GB300, or Vera Rubin instance type is rejected by CKS.

Because NVL72-powered instances must be deployed as full racks, [CoreWeave's Day 2+ automation](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md) can't automatically replace a malfunctioning Node with one from a different rack. Instead, NVL72-powered Nodes must be physically exchanged within the same rack. As a best practice, workloads should tolerate up to two unavailable Nodes per rack for maintenance purposes. If a rack has more than two unavailable Nodes, the entire rack is cordoned and drained for service.

## Manage Pod affinity

To take full advantage of the NVL72 architecture's shared NVLink fabric, all Nodes from the same job must be scheduled onto the same rack with the same NVLink domain for optimal performance. This is especially important for large-scale distributed computing tasks, where efficient communication between GPUs reduces processing times.

> [!NOTE]
>
> Slurm users should use the [Topology/Block Plugin for Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md) to control job placement.

The following sections describe how to control Pod placement using NVLink domain labels and, when needed, InfiniBand or RoCE network labels.

### Control placement with NVLink domain

Kubernetes controls Pod placement with affinity rules that steer Pods toward Nodes with specific labels. In CKS, all Nodes are labeled with their NVLink domain, allowing precise control over Pod placement. To ensure multiple Pods are scheduled onto the same NVL72 rack, set their affinity toward Nodes within the same NVLink domain.

In the NVL72 architecture, all Nodes within the same rack share the same unique `ds.coreweave.com/nvlink.domain` label. If a Node Pool spans multiple racks, Pods can reference multiple NVLink domains in `matchExpressions.values`.

For example, this Pod affinity rule targets a single NVLink domain. Replace `[NVLINK-DOMAIN]` with the value of the `ds.coreweave.com/nvlink.domain` label for your target rack. To find it, run `kubectl get nodes -L ds.coreweave.com/nvlink.domain`:

```yaml theme={"system"}
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: ds.coreweave.com/nvlink.domain
          operator: In
          values:
          - [NVLINK-DOMAIN]
```

### Control placement with InfiniBand labels

In some cases, it's useful to deploy Pods on Nodes in different NVLink domains while controlling the InfiniBand or RoCE network location. See [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md) for more information.

## More resources

To learn more about our platform, see the following resources:

* [Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md)
* [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md)
* [CPU instances](https://docs.coreweave.com/platform/instances/cpu-instances.md)
* [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md)
* [Pricing information](https://www.coreweave.com/pricing)
