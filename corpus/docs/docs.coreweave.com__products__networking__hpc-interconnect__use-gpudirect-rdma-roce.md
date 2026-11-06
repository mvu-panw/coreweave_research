# Use GPUDirect RDMA with RoCE

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce

# Use GPUDirect RDMA with RoCE

> Configure and use GPUDirect RDMA over RoCE on CoreWeave, including Pod configuration and NCCL setup

In this guide, learn how to use GPUDirect RDMA with RoCE-based backend fabrics at CoreWeave, and how to test it with NCCL. GPUDirect RDMA over RoCE lets multi-Node GPU workloads move data directly between GPU memory and the network fabric, which is essential for high-throughput, low-latency collective operations in distributed training and HPC jobs. This guide targets platform engineers and ML practitioners who deploy Pods on RoCE-enabled CoreWeave clusters.

## Prerequisites

CoreWeave supports GPUDirect RDMA over RoCE (RDMA over Converged Ethernet) for some [GPU instance types](https://docs.coreweave.com/platform/instances/gpu-instances.md) built on Spectrum-X Ethernet fabrics.

To use this feature, you must:

* Select a Node Pool with RoCE support.
* Install NCCL, and UCX or OFED userspace as needed, in the Pod image.
* For the GB300 RoCE examples, use an image with HPC-X 2.50 or newer and the Spectrum-X NCCL plugin at `/opt/hpcx/nccl_spectrum-x_plugin/lib`.
* Configure the Pods to use GPUDirect RDMA over RoCE.

For background on CoreWeave's high-performance fabrics, see [About CoreWeave HPC interconnects](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md).

## Select a Node Pool with RoCE support

To use GPUDirect RDMA over RoCE, make sure the [Node Pool](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md) has Nodes connected to a RoCE-capable fabric, as shown in the GPU instance types list and your contract.

All Nodes on these clusters have the required RoCE kernel drivers and firmware pre-installed. CKS manages the RoCE driver, NIC configuration, and fabric integration. To avoid Node instability, don't install additional low-level driver management tools inside your Pods.

If you're unsure whether a given cluster or Node Pool has RoCE enabled, contact your CoreWeave representative.

## Configure the Pods

Configure the Pods to use GPUDirect RDMA over RoCE. The following sections describe the three required configuration tasks, with an optional fourth task for debug logging:

1. Request the RoCE RDMA resource so Pods land on Nodes with RoCE.
2. Attach RoCE interfaces into the Pod using Multus.
3. Configure NCCL (and optionally UCX) to use those interfaces.

On some platforms (for example, SUNK NodeSets such as `gb300-4x-e`), the NodeSet handles steps 1 and 2. For direct Kubernetes workloads, you configure them explicitly in the Pod spec.

After you complete these steps, your Pods run on RoCE-capable Nodes, have the RoCE backend interfaces attached, and use NCCL configured for GPUDirect RDMA traffic.

### Request the RoCE RDMA resource

Set the value of `spec.containers.resources.requests.rdma/ib` to `1`.

This value doesn't indicate the number of RoCE devices requested. Kubernetes uses it as a boolean to schedule Pods onto servers that expose RoCE RDMA resources.

Kubernetes schedules resources through `requests` and `limits`. When you specify only `limits`, Kubernetes sets `requests` to the same amount as the limit. For more information, see the Kubernetes documentation on [container resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

For a Pod configuration example showing how to set the `rdma/ib` value for both `requests` and `limits`, see [Kubernetes example](#kubernetes-example).

### Attach RoCE interfaces with Multus

CoreWeave exposes RoCE backend interfaces into Pods using [Multus CNI](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#multus-cni) and NetworkAttachmentDefinition (NAD) objects.

On RoCE-enabled clusters, CoreWeave defines NADs that map host RoCE devices (for example, Spectrum-X `ibs#p#` ports) into Pod network interfaces through MACVLAN and VRF configuration.

On some clusters, CoreWeave provides a set of per-port NADs (for example, `ibs0p0-macvlan` and `ibs0p1-macvlan`). In that case, the `k8s.v1.cni.cncf.io/networks` annotation contains one entry per backend interface, for example:

```yaml theme={"system"}
metadata:
  annotations:
    k8s.v1.cni.cncf.io/networks: |-
      [{
        "name": "ibs0p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p3-macvlan",
        "namespace": "cw-multus"
      }]
```

Key points:

* `name` and `namespace` must match the RoCE NADs configured in your cluster.
* The attached interfaces appear inside the Pod as additional Linux network interfaces, such as `net1` and `net2`. These names are distinct from the RDMA verbs-device names used for selection with `NCCL_IB_HCA`.
* Some clusters also provide a single "backend" NAD name. Your CoreWeave representative can provide the correct annotation for your cluster.

#### GB300 multi-rail Pod requirements

On GB300 RoCE, a direct Kubernetes Pod that needs RoCE access must include all of the following. Without the Multus annotations, only `eth0` is available in the Pod and no `ibp` devices are exposed.

* All 16 Multus annotations, one per backend interface, as shown in the preceding example (`ibs0p0-macvlan` through `ibs3p3-macvlan` in the `cw-multus` namespace).
* The RDMA resource request `rdma/ib: 1` in `resources`.
* The `IPC_LOCK` capability:

  ```yaml theme={"system"}
  securityContext:
    capabilities:
      add: ["IPC_LOCK"]
  ```

On SUNK NodeSets such as `gb300-4x-e`, the NodeSet handles the Multus attachment, so you don't add these annotations to the Slurm job yourself.

### Configure NCCL and UCX for RoCE

To configure the Pod to use GPUDirect RDMA over RoCE, set these environment variables:

* `NCCL_SOCKET_IFNAME`: The front-end interface name for NCCL's TCP-based control and out-of-band communication. Commonly set to the primary Pod interface, for example `eth0`.
* `NCCL_IB_HCA`: The RDMA verbs devices that NCCL uses for GPUDirect RDMA collectives. The GB300 examples use the device-name prefix `ibp`. Confirm the names inside the workload container with `ibv_devices`, as described in the [RoCE cluster recipe](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#roce-spectrum-x-cluster-recipe). Don't substitute a Multus network-interface name such as `net1` unless it is also the actual RDMA device name.

If your stack also needs UCX over RDMA, configure its devices and transports separately. For GB300, follow [UCX and GPUDirect RDMA on GB300 RoCE](#ucx-and-gpudirect-rdma-on-gb300-roce), including the container-library prerequisites. The NCCL examples on this page don't set `UCX_NET_DEVICES` or `UCX_TLS`.

#### Environment variables that differ from InfiniBand

RoCE on CoreWeave uses an IPv6 address family and an Ethernet traffic class, so a few NCCL variables differ from the [InfiniBand recipe](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md). On RoCE clusters such as GB300, set these in addition to the preceding variables:

* `NCCL_IB_ADDR_FAMILY`: Set to `AF_INET6`. RoCE addressing on CoreWeave is IPv6, unlike InfiniBand.
* `NCCL_IB_TC`: The RoCE traffic class, for example `96` on GB300.
* `NCCL_NET_PLUGIN`: Leave unset so NCCL loads the Spectrum-X network plugin, and prepend the plugin's library directory, `/opt/hpcx/nccl_spectrum-x_plugin/lib`, to `LD_LIBRARY_PATH`. The plugin requires HPC-X 2.50 or newer. For details, see [NCCL network plugin guidance](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#nccl-network-plugin-guidance).

For the full side-by-side comparison of InfiniBand and RoCE variables, see [NCCL configuration reference for CoreWeave fabrics](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md).

The following Kubernetes and Slurm configuration fragments show the GB300 RoCE settings to add to your workload.

### UCX and GPUDirect RDMA on GB300 RoCE

NCCL and UCX use different RDMA data paths, so a node where NCCL tests pass doesn't guarantee that UCX-based workloads work. This matters for stacks that use UCX as their RDMA backend, including NIXL (used by vLLM for disaggregated prefill and decode) and MPI applications. NIXL can't use NCCL as a backend, so it depends entirely on a correctly built UCX.

UCX-based GPUDirect RDMA on GB300 RoCE requires `rdma-core` version 54 or later, with UCX built against it. A container whose UCX is built against an older `rdma-core` initializes successfully, including detecting `nvidia-peermem` and DMA-BUF, but fails during actual data transfer. CoreWeave's `nccl-tests` images, published at [`ghcr.io/coreweave/nccl-tests`](https://github.com/coreweave/nccl-tests), include a compatible UCX.

Symptoms of an `rdma-core` mismatch:

* UCX initialization succeeds, but data transfer fails with a remote operation error reporting `vendor_err 0x89`, or with `Unexpected UCX error: Input/output error`.
* NCCL tests pass on the same nodes, because NCCL's built-in verbs path handles GPU memory differently than UCX's path.

Set these UCX variables for GB300 RoCE. Use the `mlx5` transports, not `rc_verbs` or `ud_verbs`:

```bash theme={"system"}
# Use mlx5 transports for GB300 RoCE GPUDirect RDMA.
export UCX_TLS=rc_mlx5,ud_mlx5,cuda_copy

# GID index for the IPv6 global address (not link-local).
export UCX_IB_GID_INDEX=11

# Use multiple RDMA rails for bandwidth.
export UCX_MAX_RMA_RAILS=4

# Enumerate the active RoCE ports after Multus annotations are applied.
export UCX_NET_DEVICES=ibp0p0:1,ibp0p1:1,ibp0p2:1,ibp0p3:1
```

If a UCX workload that previously worked suddenly fails across multiple Pods at once with `Destination is unreachable`, that points to a fabric-level event rather than a container or configuration problem. Check whether other jobs on the same fabric are affected before changing your job, and see [Read IB and RoCE node labels for placement](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md) to check backend link health.

### Optional: Enable extended NCCL logging

To increase the verbosity of NCCL's logging, set the `NCCL_DEBUG` environment variable to `INFO` for extra debug information. This can help diagnose issues with RDMA support, but it increases the log file size, so disable it when testing is complete. For more logging options, see [`NCCL_DEBUG` in the NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html?#nccl-debug).

## Kubernetes example

For a GB300 RoCE workload, add the following configuration to your Pod spec. It shows how to:

* Attach RoCE backend interfaces through the `k8s.v1.cni.cncf.io/networks` annotation.
* Set the `rdma/ib` value in the Pod spec for both `requests` and `limits`.
* Add the `IPC_LOCK` capability described in [Attach RoCE interfaces with Multus](#attach-roce-interfaces-with-multus).
* Set the required environment variables.

Use the NAD names and namespace configured for your cluster. Replace `[IMAGE-LD-LIBRARY-PATH]` with your image's existing `LD_LIBRARY_PATH` value to preserve its other library directories. If the image has no existing value, use only `/opt/hpcx/nccl_spectrum-x_plugin/lib`. Supply the literal path in the YAML, not a shell expression such as `$LD_LIBRARY_PATH`.

Leave `NCCL_NET_PLUGIN` unset in both the image and the Pod environment so NCCL can load the Spectrum-X plugin. If your image sets it, remove that setting from the image or unset it in your workload's startup script before launching NCCL.

```yaml title="GB300 RoCE Pod configuration fragment" theme={"system"}
# [...]
metadata:
  annotations:
    k8s.v1.cni.cncf.io/networks: |-
      [{
        "name": "ibs0p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs0p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs1p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs2p3-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p0-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p1-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p2-macvlan",
        "namespace": "cw-multus"
      },{
        "name": "ibs3p3-macvlan",
        "namespace": "cw-multus"
      }]
spec:
  containers:
  - name: example
    securityContext:
      capabilities:
        add: ["IPC_LOCK"]
    resources:
      requests:
        cpu: 10
        memory: 10Gi
        rdma/ib: 1
        nvidia.com/gpu: 4
      limits:
        cpu: 10
        memory: 10Gi
        rdma/ib: 1
        nvidia.com/gpu: 4
    env:
      # Control / OOB traffic over primary Pod interface
      - name: NCCL_SOCKET_IFNAME
        value: eth0

      # RDMA device-name prefix. Confirm it with ibv_devices in the container.
      - name: NCCL_IB_HCA
        value: ibp

      - name: NCCL_IB_ADDR_FAMILY
        value: AF_INET6
      - name: NCCL_IB_TC
        value: "96"

      # Preserve the image's other library directories when replacing the placeholder.
      - name: LD_LIBRARY_PATH
        value: "/opt/hpcx/nccl_spectrum-x_plugin/lib:[IMAGE-LD-LIBRARY-PATH]"

      # Optional: extended NCCL logging for debugging
      - name: NCCL_DEBUG
        value: INFO
# [...]
```

Setting `NCCL_DEBUG` to `INFO` enables extended logging. Remove this variable when you don't need extended logging.

## Slurm example

For a SUNK GB300 RoCE job, add the following settings to your batch script. On NodeSets such as `gb300-4x-e`, the NodeSet handles the Multus attachment. Use your cluster's partition name and job resource counts. Run the exports and `unset NCCL_NET_PLUGIN` inside the workload container before launching NCCL so they apply to its environment and preserve its library path. Remove `NCCL_DEBUG` when you don't need extended logging.

```bash title="GB300 RoCE Slurm configuration fragment" theme={"system"}
#!/bin/bash

#SBATCH --partition gb300
#SBATCH --nodes 16
#SBATCH --ntasks-per-node 4
#SBATCH --gpus-per-node 4
# [...] other SBATCH options, as needed

# Control / OOB traffic over front-end Ethernet
export NCCL_SOCKET_IFNAME=eth0

# RDMA device-name prefix. Confirm it with ibv_devices in the container.
export NCCL_IB_HCA=ibp

# GB300 RoCE address family and traffic class.
export NCCL_IB_ADDR_FAMILY=AF_INET6
export NCCL_IB_TC=96

# Load the Spectrum-X plugin from HPC-X 2.50 or newer.
unset NCCL_NET_PLUGIN
export LD_LIBRARY_PATH="/opt/hpcx/nccl_spectrum-x_plugin/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

# Optional: extended NCCL logging while validating RoCE behavior
export NCCL_DEBUG=INFO  # Remove NCCL_DEBUG when you don't need debug logging
```

## Test with NCCL

CoreWeave provides several sample NCCL test jobs for use with MPI Operator or Slurm. These jobs live in the [`nccl-tests` repository](https://github.com/coreweave/nccl-tests/blob/master/README.md#running-nccl-tests), and you can use them to test GPUDirect RDMA support with RoCE.

These NCCL test jobs validate NCCL, but they don't validate UCX-based workloads such as NIXL, because UCX uses a different RDMA path. To validate UCX, use a UCX-based test such as `ucx_perftest` from a container with a compatible `rdma-core`.

## Related pages

* [NCCL configuration reference for CoreWeave fabrics](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md): full NCCL and UCX variable reference.
* [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md): the InfiniBand equivalent of this guide.
* [Read IB and RoCE node labels for placement](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md): topology-aware placement and link-health checks.
