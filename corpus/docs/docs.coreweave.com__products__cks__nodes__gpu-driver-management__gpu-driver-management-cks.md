# About GPU driver management in CKS

Source: https://docs.coreweave.com/products/cks/nodes/gpu-driver-management/gpu-driver-management-cks

# About GPU driver management in CKS

> Configure and manage GPU driver versions for your Node Pools

> [!WARNING]
>
> GPU driver management in CKS has the following limitations:
>
> * **Manifest configuration**: Set GPU driver versions in the Node Pool manifest using `kubectl`, GitOps, or the [Cloud Console manifest editor](https://docs.coreweave.com/products/cks/nodes/manage.md#cloud-console).
> * **Limited version updates**: You can only select major version updates. When minor updates are available, the `Manual` and default `OnSpecUpdate` strategies leave the configuration pending in [`status.pendingNodeConfiguration`](https://docs.coreweave.com/products/cks/reference/node-pool#pending-node-configuration). With `Always`, CKS stages it automatically. See [Manage Node Pool configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration).
> * **No release channel support**: Node Pools do not support the `latest` and `stable` release channels.
>
> [Contact CoreWeave support](https://docs.coreweave.com/support.md) if you have questions about GPU driver management.

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.

This page explains how GPU driver management works in CoreWeave Kubernetes Service (CKS) so you can pin your Node Pools to a supported driver version and route workloads to Nodes that match. Use this approach when your training, inference, or high-performance computing (HPC) workloads depend on a specific NVIDIA driver version for compatibility, performance, or reproducibility.

CKS lets you specify a GPU driver version for your Node Pools. You can specify driver versions in the Node Pool manifest when deploying a Node Pool. CKS workloads can target Nodes running specific driver versions using the `nodeSelector` field in the workload manifest.

> [!NOTE]
>
> Selecting a driver version using the `gpu` field is optional. If you don't specify a version, the Node Pool uses the latest available driver version.

## Upcoming deprecations

Effective **July 29, 2026**, CoreWeave is deprecating several Canonical distributions, kernel, and driver versions. These versions are deprecated upstream and no longer receive security fixes.

CoreWeave handles all updates and migrations to supported versions, so you don't need to take any action.

**Operating systems**

| Distribution | Status | Notes |
| - | - | - |
| Ubuntu 22.04 LTS (Jammy) | Deprecated | Deprecated on July 29, 2026 |
| Ubuntu 24.04 LTS (Noble) | Supported | |
| Ubuntu 26.04 LTS (Resolute) | Supported | Supported on July 29, 2026 |

On Noble, only kernels 6.8 LTS and 6.17 LTS remain supported. Resolute launches with kernel 7.0.

**NVIDIA GPU drivers**

| Driver | Status | Notes |
| - | - | - |
| 535 | Deprecated | Deprecated on July 29, 2026 |
| 580 | Supported | Default |
| 595 | Supported | Not recommended due to bugs and vulnerabilities |
| 615 | Supported | |
| 620 | [Vera Rubin NVL72 only](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) | |

**Networking stack**

| Component | Status | Deprecated on |
| - | - | - |
| Legacy Mellanox OFED | Deprecated | July 29, 2026 |
| DOCA 3.2 | Deprecated | July 29, 2026 |
| DOCA 3.3 | Supported | |

If you have questions, [contact CoreWeave support](https://docs.coreweave.com/support.md).

## Supported driver versions

Use the following table to confirm which driver version to pin when configuring a Node Pool. CoreWeave supports all tested release driver (TRD) versions from NVIDIA, listed in the following table as major versions.

> [!NOTE]
>
> Although you aren't required to upgrade from a major version, CoreWeave recommends that you upgrade frequently to ensure the best combination of testing coverage, security posture, stability, and performance.

| Name | Instance ID | Default GPU driver | Compatible GPU driver |
| - | - | - | - |
| [Vera Rubin NVL72 Spectrum-X RoCE](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) | `verarubin-4x-e` | `620` | `620` |
| [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) | `gb300-4x` | `580` | `580`, `595`, `615` |
| [GB300 NVL72 Spectrum-X RoCE](https://docs.coreweave.com/platform/instances/gpu/gb300-4x-e.md) | `gb300-4x-e` | `580` | `580`, `595`, `615` |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) | `gb200-4x` | `580` | `580`, `595`, `615` |
| [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) | `b300-8x` | `580` | `580`, `595`, `615` |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) | `b200-8x` | `580` | `580`, `595`, `615` |
| [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) | `gd-8xh200ib-i128` | `580` | `580`, `595`, `615` |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | `gd-8xh100ib-i128` | `580` | `580`, `595`, `615` |
| [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | `rtxp6000-8x` | `580` | `580`, `595`, `615` |
| [RTX PRO 6000 Blackwell Server Edition (Standard Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x-v2.md) | `rtxp6000-8x-v2` | `580` | `580`, `595`, `615` |
| [L40S](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40s-i128.md) | `gd-8xl40s-i128` | `580` | `580`, `595`, `615` |
| [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) | `gd-8xl40-i128` | `580` | `580`, `595`, `615` |
| [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) | `gd-1xgh200` | `580` | `580`, `595`, `615` |
| [A100](https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128.md) | `gd-8xa100-i128` | `580` | `580`, `595`, `615` |

## Additional resources

For step-by-step procedures and related reference material, see:

* [Update GPU driver versions in CKS Node Pools](https://docs.coreweave.com/products/cks/nodes/gpu-driver-management/update-gpu-driver.md)
* [Node Pool Reference](https://docs.coreweave.com/products/cks/reference/node-pool.md)
* [Manage Node Pools](https://docs.coreweave.com/products/cks/nodes/manage.md)
