# NVSHMEM and GDRCopy for GPU-to-GPU communication

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/nvshmem-gdrcopy

# NVSHMEM and GDRCopy for GPU-to-GPU communication

> Enable NVSHMEM and GDRCopy for high-performance GPU-to-GPU communication on CoreWeave

This guide explains how to run multi-Node GPU workloads that rely on NVSHMEM and GDRCopy on either CoreWeave Kubernetes Service (CKS) or SUNK.

NVSHMEM (NVIDIA SHMEM) is a communication library that implements one-sided put and get operations across GPUs over NVLink and InfiniBand. GDRCopy (GPUDirect RDMA Copy) provides low-latency copies to and from GPU memory using NVIDIA GPUDirect RDMA. Both build on the same GPUDirect RDMA capability described in [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md).

## Support for NVSHMEM and GDRCopy

NVSHMEM and GDRCopy follow a shared responsibility model, the same pattern as other GPU communication libraries such as NCCL and cuDNN:

* **CoreWeave provides the host prerequisites** in the ncore Node image at the Node level. These include the GDRCopy kernel driver (`gdrdrv`), the `nvidia-peermem` kernel module that enables GPUDirect RDMA, and NVIDIA GPU drivers with peer memory support. The image also sets the following NVIDIA driver options through the kernel command line, so you don't need to request them or change your workloads:

  * `nvidia.NVreg_EnableStreamMemOPs=1`
  * `nvidia.NVreg_RegistryDwords="PeerMappingOverride=1;"`

* **You provide the userspace library** by installing NVSHMEM or GDRCopy in your own container image. CoreWeave does not install these libraries system-wide.

## Prerequisites

To use NVSHMEM and GDRCopy, you must meet the following requirements:

* Your Nodes run ncore image version 2.10.1 or later, which includes the GDRCopy kernel driver, `nvidia-peermem`, and the required kernel parameters. Recent ncore images include these components by default. If your Nodes run an older image, [contact CoreWeave Support](https://docs.coreweave.com/support.md) to request an update.
* For NVSHMEM IBGDA over InfiniBand, select an InfiniBand-capable Node Pool. See the prerequisites in [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md). CoreWeave recommends NVIDIA driver version 570 or later for IBGDA workloads.
* The NVSHMEM or GDRCopy userspace library is installed in your container image.

## Verify the Node prerequisites

Confirm that your Nodes run a supported ncore image and driver version. Replace `[NODE-NAME]` with the name of a Node in your cluster:

```bash theme={"system"}
kubectl get node [NODE-NAME] -o custom-columns='NCORE:.metadata.labels.node\.coreweave\.cloud/ncore-image-tag,DRIVER:.metadata.labels.gpu\.coreweave\.cloud/driver-version'
```

The output shows the ncore image tag and NVIDIA driver version for the Node:

```text title="Example output" theme={"system"}
NCORE          DRIVER
2.16.0         570.148.08
```

If the ncore image tag is earlier than 2.10.1, [contact CoreWeave Support](https://docs.coreweave.com/support.md) to update the image before you continue.

## Enable GDRCopy in your container

Set the `NVIDIA_GDRCOPY` environment variable in the container so that it can access the `gdrdrv` driver on the host:

```yaml theme={"system"}
env:
  - name: NVIDIA_GDRCOPY
    value: enabled
```

> [!NOTE]
>
> If you use SUNK, this environment variable is already set.

## Configure NVSHMEM for CoreWeave InfiniBand devices

CoreWeave presents InfiniBand host channel adapters (HCAs) with device names that begin with `ibp` (for example, `ibp0`), rather than the `mlx5` naming that NVSHMEM's IBGDA transport expected in earlier versions. The configuration required depends on your NVSHMEM version:

* **NVSHMEM 3.5 or later**: No configuration is needed. NVSHMEM accepts `ibp` device names by default.

* **NVSHMEM 3.4.5**: Set the `NVSHMEM_HCA_PREFIX` environment variable in your container. In this version, the default HCA prefix is `mlx5`, so NVSHMEM skips `ibp` devices unless you set the variable explicitly:

  ```yaml theme={"system"}
  env:
    - name: NVSHMEM_HCA_PREFIX
      value: ibp
  ```

* **NVSHMEM earlier than 3.4.5**: These versions recognize only `mlx5` device names and don't include the `NVSHMEM_HCA_PREFIX` environment variable. Patch the NVSHMEM source as described in [Patch NVSHMEM versions earlier than 3.4.5](#patch-nvshmem-versions-earlier-than-3-4-5).

If your workload also uses NCCL, set `NCCL_IB_HCA` to `ibp` for all NVSHMEM versions, as described in [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md#configure-the-pods).

### Patch NVSHMEM versions earlier than 3.4.5

> [!NOTE]
>
> These instructions apply only to NVSHMEM versions earlier than 3.4.5. Later versions don't require a source patch. See [Configure NVSHMEM for CoreWeave InfiniBand devices](#configure-nvshmem-for-coreweave-infiniband-devices).

To recognize the InfiniBand devices presented on CoreWeave Nodes, patch `ibgda` in your container. The following example applies to NVSHMEM version 3.2.5. Download NVSHMEM version 3.2.5.

In `src/modules/transport/ibgda/ibgda.cpp`, change the device-name check from `mlx5` to `ibp`.

**Original code:**

```cpp highlight={1} theme={"system"}
if (!strstr(name, "mlx5")) {
    ftable.close_device(device->context);
    device->context = NULL;
    NVSHMEMI_WARN_PRINT("device %s is not enumerated as an mlx5 device. Skipping...\n",
                        name);
    continue;
}
```

**Modified code:**

```cpp highlight={1} theme={"system"}
if (!strstr(name, "ibp")) {
    ftable.close_device(device->context);
    device->context = NULL;
    NVSHMEMI_WARN_PRINT("device %s is not enumerated as an mlx5 device. Skipping...\n",
                        name);
    continue;
}
```

## Additional resources

* [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md)
* [About HPC interconnect](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md)
* [Configure compute Nodes](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md)
* [Slurm images reference](https://docs.coreweave.com/products/sunk/reference/slurm-images.md)
