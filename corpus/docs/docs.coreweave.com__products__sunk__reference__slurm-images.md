# Slurm images

Source: https://docs.coreweave.com/products/sunk/reference/slurm-images

# Slurm images

> Reference for SUNK-built Slurm container images, including base and extras variants with supported CUDA versions

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This reference describes the container images the SUNK team builds and publishes, so you can choose the right image for your control plane, login, CPU, and GPU nodes. Use this page to understand what each image contains, which CUDA versions SUNK supports, and where to pull images from when you run SUNK inside or outside CoreWeave Kubernetes Service (CKS).

> [!NOTE]
>
> These are the `slurm-containers` images that run the Slurm control plane and nodes. For CoreWeave's optimized PyTorch base images for training workloads, see [ML container images](https://docs.coreweave.com/products/sunk/discover_sunk/ml-containers.md).

The SUNK team builds several images: base images (`controller`, `slurmd-cw-*`) and extras images (`controller-extras`, `slurmd-cw-*-extras`) built on top of the base:

* `controller`: Primarily for the control plane components, but you can also use it for CPU nodes.
* `controller-extras`: Extras for use on login nodes or CPU nodes.
* `slurmd-cw-*`: Images for GPU nodes.
* `slurmd-cw-*-extras`: Extras images for GPU nodes.

The following table shows how each image relates to the others, including which base image each extras variant is built on.

| Image | Based on | Image type |
| - | - | - |
| `controller (22.04)` | `ubuntu:jammy-20240911.1` | Base |
| `controller-extras (22.04)` | `controller (22.04)` | Extra |
| `slurmd-cw-cu122 (22.04)` | [`nccl-tests:12.2.2-devel-ubuntu22.04-nccl2.27.5-1-d5a135d`][nccl-image-ref] | Base |
| `slurmd-cw-cu124 (22.04)` | [`nccl-tests:12.4.1-devel-ubuntu22.04-nccl2.27.5-1-d5a135d`][nccl-image-ref] | Base |
| `slurmd-cw-cu128 (22.04)` | [`nccl-tests:12.8.1-devel-ubuntu22.04-nccl2.28.3-1-528fb68`][nccl-image-ref] | Base |
| `slurmd-cw-cu129 (22.04)` | [`nccl-tests:12.9.1-devel-ubuntu22.04-nccl2.28.3-1-528fb68`][nccl-image-ref] | Base |
| `slurmd-cw-cu130 (22.04)` | [`nccl-tests:13.0.1-devel-ubuntu22.04-nccl2.28.3-1-528fb68`][nccl-image-ref] | Base |
| `slurmd-cw-cu122-extras (22.04)` | `slurmd-cw-cu122 (22.04)` | Extra |
| `slurmd-cw-cu124-extras (22.04)` | `slurmd-cw-cu124 (22.04)` | Extra |
| `slurmd-cw-cu128-extras (22.04)` | `slurmd-cw-cu128 (22.04)` | Extra |
| `slurmd-cw-cu129-extras (22.04)` | `slurmd-cw-cu129 (22.04)` | Extra |
| `slurmd-cw-cu130-extras (22.04)` | `slurmd-cw-cu130 (22.04)` | Extra |

> [!NOTE]
>
> The `slurmd-cw-cu122` and `slurmd-cw-cu124` images ship NCCL 2.27.5, which doesn't meet the [Straggler Detection NCCL prerequisite](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md#prerequisites). Jobs that run directly on these images, without a container, don't report NCCL metrics.

SUNK supports up to two Ubuntu LTS versions and several CUDA versions.

> [!NOTE]
>
> * `slurm-cw-122` (CUDA 12.2) is deprecated as of SUNK v6.5.0 and is scheduled for removal in the next major version release.
> * `slurm-cw-124` (CUDA 12.4) is deprecated as of SUNK v6.9.0 and is scheduled for removal in the next major version release.
>
> `ubuntu-20.04` variants are no longer built after September 3, 2025 (CUDA 12.x nccl2.27.5-1-d5a135d are the last available versions).

> [!NOTE]
>
> Other packages in the images that aren't listed in the following sections might be dependencies for the listed packages and might change.

## Select an image

This section explains where to pull SUNK images from and how the `image` field resolves a registry and name.

| Image registry | Availability |
| - | - |
| `ghcr.io/coreweave/slurm-containers` | Public |
| `images.coreweave.com/cluster-images/coreweave/slurm-containers` | Internal to CKS |

All `image` fields support a `name` field to specify the desired image name:

* If you don't specify a repository, SUNK uses the default registry plus the image `name`.
* If you specify a repository, it overrides the value used. SUNK uses neither the `name` nor the default registry.

For example, an image named `controller`, as shown in the following example, uses the `controller` image from the default registry, `ghcr.io/coreweave/slurm-containers/controller`.

```yaml theme={"system"}
  image:
    name: controller
    repository:
```

### External SUNK users

If you run SUNK outside CKS, you must point the Helm chart at the public registry instead of the internal CKS one. To do this, change the `global.cks` value in [the `slurm` Helm chart](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) as follows:

`global.cks.enabled=false`

The default value, `global.cks.enabled=true`, pulls images from the internal CKS registry, which isn't available externally.

## Base images

Base images provide the foundation for SUNK's control plane and node images. This section describes their purpose and the packages they include.

### Purpose of base images

Base images serve as the foundation for the Slurm control plane components as well as the login and CPU-only `slurmd` Pods.

### Main packages with pinned versions

* [Slurm](https://slurm.schedmd.com/documentation.html): Workload manager.
* [s6-overlay](https://github.com/just-containers/s6-overlay): Process supervisor and service
  manager.
* [Pyxis](https://github.com/NVIDIA/pyxis): Plugin for Slurm that enables containerized jobs.
* [Enroot](https://github.com/NVIDIA/enroot): Container runtime.
* [kubectl](https://kubernetes.io/docs/reference/kubectl/): Command-line tool for interacting
  with Kubernetes clusters.

> [!NOTE]
>
> **NVSHMEM and GDRCopy support**
>
> NVSHMEM and GDRCopy require ncore image version 2.10.1 or later, which recent ncore images include by default.
> In your container, enable GDRCopy and configure NVSHMEM to recognize CoreWeave's `ibp` InfiniBand device names.
> For implementation instructions, see [Use NVSHMEM and GDRCopy for GPU-to-GPU communication](https://docs.coreweave.com/products/networking/hpc-interconnect/nvshmem-gdrcopy.md).

### Main packages from repositories

* End-user utilities: [htop](https://htop.dev/), [ping](https://en.wikipedia.org/wiki/Ping_\(networking_utility\)), [traceroute](https://en.wikipedia.org/wiki/Traceroute), [net-tools](https://sourceforge.net/projects/net-tools/), [numactl](https://github.com/numactl/numactl), [sudo](https://www.sudo.ws/), [wget](https://www.gnu.org/software/wget/)
* [OpenSSH server](https://www.openssh.org/): Enables secure remote access to the login nodes.
* [SSSD](https://sssd.io/) (System Security Services Daemon): Provides integration with external
  authentication providers using LDAP.
* [Munge](https://slurm.schedmd.com/authentication.html): Authentication service for creating
  and validating credentials.
* [Environment modules](https://modules.readthedocs.io/en/latest/): Enables dynamic modification
  of the user's environment.
* [libnvidia-container](https://github.com/NVIDIA/libnvidia-container): NVIDIA Container Toolkit
  for GPU support.

## Extra images

Extra images extend the base images with additional user-facing tools and utilities. Use them when you want a broader set of end-user tools on login or CPU nodes without building your own image. This section lists the packages added on top of the base images.

### Additional packages with pinned versions

* [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html): Package, dependency, and environment management for multiple languages.
* [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html): Lightweight alternative to Conda.

### Additional packages from repositories

* End-user utilities: [bc](https://www.gnu.org/software/bc/), [emacs](https://www.gnu.org/software/emacs/), [git](https://git-scm.com/), [glances](https://nicolargo.github.io/glances/), [lua](https://lua.org/), [mosh](https://mosh.org/), [nano](https://www.nano-editor.org/), [JRE](https://openjdk.org/), [pdsh](https://github.com/chaos/pdsh), [rsync](https://rsync.samba.org/), [s3cmd](https://s3tools.org/s3cmd), [silversearcher-ag](https://geoff.greer.fm/ag/), [tmux](https://github.com/tmux/tmux/wiki), [vim](https://www.vim.org/), [wget](https://www.gnu.org/software/wget/)
* [NHC (Node Health Check)](https://github.com/mej/nhc): Tool for monitoring and managing node health.
* [AWS CLI](https://aws.amazon.com/cli/): Command-line tool for interacting with Amazon Web Services.

[nccl-image-ref]: https://github.com/coreweave/nccl-tests/commit/d5a135d4ad919650f324a2ce4972118bc318783f
