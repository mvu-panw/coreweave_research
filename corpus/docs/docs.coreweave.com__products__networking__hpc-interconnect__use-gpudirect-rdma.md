# Use GPUDirect RDMA with InfiniBand

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma

# Use GPUDirect RDMA with InfiniBand

> Configure GPUDirect RDMA over InfiniBand on CoreWeave, including Node Pool selection and NCCL settings

In this guide, learn how to use [GPUDirect Remote Direct Memory Access (RDMA) with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md#about-gpudirect-rdma) at CoreWeave, and how to test it with the NVIDIA Collective Communications Library (NCCL). GPUDirect RDMA enables direct memory access between GPUs across Nodes over InfiniBand, which reduces latency and frees CPU cycles for distributed training and other multi-Node GPU workloads. This guide is for users running multi-Node GPU workloads on CKS or Slurm who need high-bandwidth, low-latency communication between GPUs.

## Prerequisites

CoreWeave supports GPUDirect RDMA over InfiniBand for some [GPU instance types](https://docs.coreweave.com/platform/instances/gpu-instances.md).

To use this feature, you must:

* Select a Node Pool with InfiniBand support.
* Install NCCL and the OpenFabrics Enterprise Distribution (OFED) driver in the Pod image.
* Configure the Pods to use GPUDirect RDMA.

## Select a Node Pool with InfiniBand support

To use GPUDirect RDMA, make sure the [Node Pool](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md) has Nodes with InfiniBand, as shown in our [list of GPU instance types](https://docs.coreweave.com/platform/instances/gpu-instances.md).

All Nodes with InfiniBand have the required kernel drivers pre-installed. CKS manages all the required driver and operator dependencies. To avoid Node instability, you should not install other driver management tools.

Once you have a Node Pool that supports InfiniBand, the next section covers the Pod-level configuration that opts workloads into GPUDirect RDMA.

## Configure the Pods

Configure your Pods to use GPUDirect RDMA over InfiniBand by following these steps:

1. Set the value of `spec.containers.resources.requests.rdma/ib` to `1`.

   This value doesn't indicate the number of InfiniBand devices requested. It works as a boolean to schedule Pods onto servers with InfiniBand support.

   Kubernetes schedules resources through `requests` and `limits`. When you specify only `limits`, Kubernetes sets `requests` to the same amount as the limit. For more information, see [Resource management for Pods and containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) in the Kubernetes documentation.

   For a full YAML example showing how to set the `rdma/ib` value in the Pod spec for both `requests` and `limits`, see [Kubernetes example](#kubernetes-example).

2. Configure the Pods to use GPUDirect RDMA by setting these environment variables:

   * `NCCL_SOCKET_IFNAME`: The interface NCCL uses for control and bootstrap traffic. Set this to the primary Pod interface, which the examples on this page set to `eth0`. This isn't the RDMA data path.
   * `NCCL_IB_HCA`: The InfiniBand host channel adapters (HCAs) NCCL uses for RDMA collectives. Set this to `ibp` on CoreWeave InfiniBand clusters.
   * `NCCL_NET_PLUGIN`: Leave unset so NCCL loads the HPC-X network plugin from the container image. This is the recommended default on InfiniBand. Run every rank from the same container image, so every rank loads the same plugin build; a rank on a different build can fault during collectives. Set `NCCL_NET_PLUGIN=none` instead only if you have a measured reason to use NCCL's built-in transport. For more information, see [NCCL network plugin guidance](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#nccl-network-plugin-guidance).

   Unified Communication X (UCX) is controlled by the following variables. NCCL doesn't use UCX, so these variables don't affect NCCL collectives. Set them to stop UCX from initializing a transport your job doesn't need.

   * `UCX_NET_DEVICES`: The network devices UCX uses. The examples on this page set `eth0`, the front-end interface.
   * `UCX_TLS`: The set of transports UCX is allowed to use. The examples on this page set `tcp`. Together with `UCX_NET_DEVICES=eth0`, this keeps UCX off the InfiniBand devices.

   If your stack runs UCX alongside NCCL and needs UCX on the RDMA fabric, such as an MPI build that uses UCX for its own transfers, point `UCX_NET_DEVICES` at the InfiniBand devices instead of `eth0`, and set `UCX_TLS` to the RDMA transports your stack needs instead of `tcp`. RoCE clusters that run UCX over RDMA also use different values. For more information, see [UCX and GPUDirect RDMA on GB300 RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md#ucx-and-gpudirect-rdma-on-gb300-roce).

   For Kubernetes and Slurm examples, see [Kubernetes example](#kubernetes-example) and [Slurm example](#slurm-example). For the full NCCL and UCX variable reference, see [NCCL configuration reference for CoreWeave fabrics](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md).

3. Optional: Enable extended logging with the `NCCL_DEBUG` environment variable.

   To increase the verbosity of NCCL's logging, set the `NCCL_DEBUG` environment variable to `INFO` for extra debug information. This helps diagnose issues with RDMA support, but it increases the log file size, so disable it when testing is complete. See `NCCL_DEBUG` in the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html?#nccl-debug) for more logging options.

### Kubernetes example

When you deploy a Kubernetes Pod in the cluster, use the highlighted lines in this example to set the `rdma/ib` value in the Pod spec for both `requests` and `limits`, and to set the required environment variables.

```yaml title="Kubernetes example with debug logging" highlight={9,14,16-24} theme={"system"}
# [...]
spec:
  containers:
  - name: example
    resources:
      requests:
        cpu: 10
        memory: 10Gi
        rdma/ib: 1
        nvidia.com/gpu: 8
      limits:
        cpu: 10
        memory: 10Gi
        rdma/ib: 1
        nvidia.com/gpu: 8
    env:
      - name: NCCL_SOCKET_IFNAME
        value: eth0
      - name: NCCL_IB_HCA
        value: ibp
      - name: UCX_TLS
        value: tcp
      - name: UCX_NET_DEVICES
        value: eth0
      - name: NCCL_DEBUG
        value: INFO
# [...]
```

Setting `NCCL_DEBUG` to `INFO` enables extended logging. Remove it if you don't need extended logging.

### Slurm example

When you deploy a Slurm job, use the highlighted lines in this example to set the required environment variables. Remove `NCCL_DEBUG` unless you need extended logging.

```bash title="Example Slurm sbatch script" highlight={9-12} theme={"system"}
#!/bin/bash

#SBATCH --partition h100
#SBATCH --nodes 16
#SBATCH --ntasks-per-node 8
#SBATCH --gpus-per-node 8
# [...] other SBATCH options, as needed

export NCCL_SOCKET_IFNAME=eth0
export NCCL_IB_HCA=ibp
export UCX_TLS=tcp
export UCX_NET_DEVICES=eth0
export NCCL_DEBUG=INFO # Remove NCCL_DEBUG unless debug logging
```

Every rank must load the same network plugin, so run every rank from the same container image. For more information, see [NCCL network plugin guidance](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#nccl-network-plugin-guidance).

## Test with NCCL

After you configure your Pods or Slurm jobs, verify that GPUDirect RDMA works as expected by running NCCL tests across multiple Nodes.

CoreWeave provides several sample NCCL test jobs designed for use with Message Passing Interface (MPI) Operator or Slurm. To test GPUDirect RDMA support with InfiniBand, see the [`nccl-tests` repository](https://github.com/coreweave/nccl-tests/blob/master/README.md#running-nccl-tests) for the test jobs and instructions for running them.

## Troubleshoot RDMA scheduling and NCCL startup

This section covers the two most common problems when bringing up GPUDirect RDMA: a Node that doesn't advertise the `rdma/ib` resource, and a job that hangs during NCCL initialization.

### What rdma/ib: 0 means

`rdma/ib: 0` on a Node means the Node isn't advertising the RDMA resource, so the scheduler treats it as having no RDMA capacity. A Pod that requests `rdma/ib` doesn't schedule on that Node and stays `Pending` with a `FailedScheduling` event such as `Insufficient rdma/ib`. This isn't a problem with your Pod spec. The RDMA device plugin on that Node isn't advertising the resource, usually because the Node hasn't finished initializing its RDMA devices, the device plugin isn't registered with the kubelet, or the Node has no RDMA hardware.

### Detect rdma/ib: 0

Replace `[NODE-NAME]` with the name of the Node to inspect:

```bash theme={"system"}
# Show the rdma/ib resource reported by a specific Node.
# Safe to run anytime; read-only.
kubectl describe node [NODE-NAME] | grep -A2 "rdma/ib"
```

```bash theme={"system"}
# List allocatable rdma/ib across all Nodes to spot Nodes reporting 0 or none.
# Safe to run anytime; read-only.
kubectl get nodes -o custom-columns='NODE:.metadata.name,RDMA:.status.allocatable.rdma/ib'
```

A Node that should have RDMA but reports `0` isn't in a state you can fix from the workload side. Avoid scheduling on it and open a ticket. Restarting the device plugin requires platform access that customers don't have.

### First checks when NCCL hangs at init

When a multi-Node job hangs during NCCL initialization, the most common cause is that traffic silently fell back to TCP because RDMA wasn't in use. Check these in order:

1. Confirm every Pod requested `rdma/ib: 1` in both `requests` and `limits`. A Pod that omits the request schedules without RDMA and falls back to TCP.
2. Confirm the Nodes advertise `rdma/ib` using the preceding detection commands. If any Node reports `0`, the job may have landed partly on non-RDMA capacity.
3. Confirm the container image includes the OFED user-space libraries. A mismatch between the image's RDMA libraries and the Node kernel modules causes a fallback or failure.
4. Confirm interface selection. If `NCCL_SOCKET_IFNAME` or `NCCL_IB_HCA` point at the wrong interface, NCCL can't find the RDMA path. Set `NCCL_DEBUG=INFO` and look for `NET/IB` (RDMA in use) versus `NET/Socket` (TCP fallback) in the logs.

You can also [check InfiniBand port status](#check-infiniband-port-status) from inside the Pod.

If a multi-Node job runs but throughput is far below expectations rather than hanging, NCCL has usually fallen back to TCP for the same reasons. For a full diagnostic walkthrough, including baselining with nccl-tests and isolating a degraded Node, see [Why is my multi-node NCCL training slow?](https://docs.coreweave.com/support/platform/articles/why-is-my-multi-node-nccl-training-slow).

### Check InfiniBand port status

Check the status of the InfiniBand ports used by your job:

1. From inside the Pod, display the port states:

   ```bash theme={"system"}
   ibstat
   ```

2. For each port intended to carry the job's InfiniBand traffic, confirm that the output shows `State: Active`, `Physical state: LinkUp`, and `Link layer: InfiniBand`. A port that isn't active can't carry RDMA traffic.

These states confirm link status, but don't establish that NCCL selected the RDMA transport. Check the NCCL logs as described in [NCCL initialization checks](#first-checks-when-nccl-hangs-at-init).
