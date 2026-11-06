# ML container images

Source: https://docs.coreweave.com/products/sunk/discover_sunk/ml-containers

# ML container images

> Overview of CoreWeave's optimized PyTorch container images for distributed training on CKS and SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

CoreWeave maintains a set of optimized machine learning container images, tuned for the CoreWeave platform, that you can use as a starting point for distributed training and other GPU workloads. This page describes the available images, what each one contains, and how to use them on [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) and [SUNK](https://docs.coreweave.com/products/sunk.md).

The images are published to `ghcr.io/coreweave/ml-containers` and built from the public [`coreweave/ml-containers`][ml-containers-repo] repository, where you can inspect the Dockerfiles to see exactly what each image installs.

## Available images

The following PyTorch images are the recommended starting points for most customers.

| Image | Description | Recommended for |
| - | - | - |
| `torch` | A custom build of PyTorch, torchvision, and torchaudio tuned for the CoreWeave platform. | A smaller starting point with the core PyTorch stack. |
| `torch-extras` | The `torch` image plus a set of common PyTorch extensions. | Distributed training and LLM training. This is the recommended default. |
| `nightly-torch` | An experimental, daily release channel that tracks the latest development versions of PyTorch. | Testing the latest features, not production. |
| `nightly-torch-extras` | The PyTorch extensions built on top of `nightly-torch`. | Testing the latest features, not production. |

> [!TIP]
>
> For most training workloads, start with `torch-extras`. If you want a smaller image with only the core PyTorch stack, use `torch`. Use the nightly images only for testing.

To browse every published image and its tags, see the [packages list][packages].

## PyTorch base images (torch)

The [`ml-containers/torch`][torch-pkg] image contains custom builds of [PyTorch](https://github.com/pytorch/pytorch), [torchvision](https://github.com/pytorch/vision), and [torchaudio](https://github.com/pytorch/audio), each tuned for use on the CoreWeave platform.

Each image is built on an Ubuntu LTS release. The image tag indicates the Ubuntu version, which in turn determines the Python version.

### Image variants

CoreWeave builds two variants of the `torch` image. Both variants are also available for [`torch-extras`](#pytorch-extras-torch-extras).

* `base`: Includes only the essentials (CUDA, torch, torchvision, and torchaudio). This variant has a small image size, which makes it fast to launch. It isn't built on `nccl-tests`, so it lacks networking libraries such as HPC-X, and it omits the CUDA development libraries apart from `nvcc`.
* `nccl`: Built on `nccl-tests`, so it includes the networking libraries tuned for the CoreWeave platform. It also includes the development libraries and build tools, such as `nvcc`, that are required to compile other PyTorch extensions. This variant is larger than `base`.

> [!NOTE]
>
> The `nccl` variant is the recommended choice for most workloads. For more details on the networking stack it inherits, see [`coreweave/nccl-tests`](https://github.com/coreweave/nccl-tests). To pick between `torch`, `torch-extras`, and `nccl-tests` for your workload, see [Choose and troubleshoot a training container image](https://docs.coreweave.com/products/sunk/discover_sunk/choosing-training-images.md#image-guidance).

## PyTorch extras (torch-extras)

The [`ml-containers/torch-extras`][torch-extras-pkg] image extends the [`torch`][torch-pkg] image with a set of common PyTorch extensions, including [DeepSpeed](https://github.com/deepspeedai/DeepSpeed), [xformers](https://github.com/facebookresearch/xformers), and [NVIDIA Apex](https://github.com/NVIDIA/apex). ([FlashAttention](https://github.com/Dao-AILab/flash-attention) is already included in the base `torch` image.) Each extension is compiled against the custom PyTorch builds in the `torch` image.

For the complete, current list of included extensions, see the [`coreweave/ml-containers`][ml-containers-repo] repository.

Both the `base` and `nccl` [variants](#image-variants) are available for `torch-extras`, matching those provided for `torch`. The `base` variant stays small because it uses a multi-stage build that avoids including CUDA development libraries, even though those libraries are required to build the extensions.

Customers running supervised fine-tuning, reinforcement learning, pretraining, or any multi-node PyTorch training should start with `torch-extras`.

## Nightly images

The [`nightly-torch`](https://github.com/coreweave/ml-containers/pkgs/container/ml-containers%2Fnightly-torch) image is an experimental, nightly release channel of the PyTorch base images, in the style of PyTorch's own nightly preview builds. It features the latest development versions of torch, torchvision, and torchaudio, pulled daily and compiled from source. The `nightly-torch-extras` image builds the PyTorch extensions on top of `nightly-torch`.

> [!WARNING]
>
> The nightly images are based on unstable, experimental preview builds of PyTorch and can contain bugs and other issues. For production workloads, use the `torch` or `torch-extras` images instead.

## Read an image tag

Image tags encode the component versions that most often affect compatibility. For example:

```text theme={"system"}
8a60b2d-nccl-cuda12.9.1-ubuntu22.04-nccl2.28.3-1-torch2.8.0-vision0.23.0-audio2.8.0-abi1
```

The fields appear in the order shown in the preceding example:

| Field | Example | Description |
| - | - | - |
| Commit | `8a60b2d` | The [`ml-containers`][ml-containers-repo] commit the image was built from. |
| Variant | `nccl` | The [image variant](#image-variants), either `base` or `nccl`. |
| CUDA | `cuda12.9.1` | The CUDA toolkit version. |
| Ubuntu | `ubuntu22.04` | The Ubuntu release, which determines the Python version. |
| NCCL | `nccl2.28.3-1` | The NCCL version. |
| PyTorch stack | `torch2.8.0-vision0.23.0-audio2.8.0` | The PyTorch, torchvision, and torchaudio versions. |
| ABI | `abi1` | The C++ ABI the build uses. |

Not every tag carries every field. A `base` tag omits the NCCL version, because that variant doesn't bundle the NCCL build, and a nightly tag adds a build date after the variant. Current builds always use `abi1`, and CoreWeave plans to drop the ABI field from future tags.

The tag is a summary. Extension versions such as FlashAttention and DeepSpeed, and the HPC-X version, aren't in it. For the complete list of components in a build, check the [`coreweave/ml-containers`][ml-containers-repo] repository at the commit in the tag.

Because tags change as CoreWeave publishes new builds, always get the current tag from the [packages list][packages].

A tag that starts with a name prefix rather than a commit is a branch build rather than a production build. See [Use unprefixed tags in production](https://docs.coreweave.com/products/sunk/discover_sunk/choosing-training-images.md#use-unprefixed-tags-in-production).

### Match the CUDA version to your GPU driver

Choose an image whose CUDA version is compatible with the GPU driver on your nodes. Don't assume the newest image is the right one. A recently published image can use a CUDA version that's newer than your nodes' driver supports. When this happens, workloads fail to start with driver-compatibility errors.

You can check the driver version on a node by running `nvidia-smi`.

For the minimum driver each CUDA version requires, and for how to diagnose image-related failures, see [Choose and troubleshoot a training container image](https://docs.coreweave.com/products/sunk/discover_sunk/choosing-training-images.md).

SUNK nodes inject GPU drivers into the container. They don't provide the full CUDA toolkit. If a job can detect GPUs but fails to load libraries such as `libcusparseLt.so.0`, see [Why are CUDA toolkit libraries missing in a SUNK container?](https://docs.coreweave.com/support/sunk/articles/why-are-cuda-toolkit-libraries-missing-in-sunk-containers).

## Use an image

After you've chosen an image and a tag, you can use an ML container image as a base for your own custom image, or run it directly on CKS or SUNK. In the following examples, replace `[TAG]` with a tag from the [packages list][packages].

### Build a custom image

To add your own dependencies, use an ML container image as the base image in a Dockerfile:

```dockerfile theme={"system"}
FROM ghcr.io/coreweave/ml-containers/torch-extras:[TAG]

# Install your additional dependencies
RUN pip install --no-cache-dir my-package
```

### Run on CKS

Reference the image in the `image` field of a Pod specification:

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: pytorch-training
spec:
  restartPolicy: Never
  containers:
    - name: trainer
      image: ghcr.io/coreweave/ml-containers/torch-extras:[TAG]
      command: ["python", "train.py"]
      resources:
        limits:
          nvidia.com/gpu: "8"
```

### Run on SUNK

SUNK uses [Pyxis](https://github.com/NVIDIA/pyxis) and [Enroot](https://github.com/NVIDIA/enroot) to run containers. Pass the image to `srun` with the `--container-image` flag. In the container URI, a `#` separates the registry host from the image path:

```bash theme={"system"}
srun --container-image=ghcr.io#coreweave/ml-containers/torch-extras:[TAG] \
  --container-mounts=/mnt/home:/mnt/home \
  --pty bash -i
```

On CoreWeave-managed Nodes, running containers with Enroot requires the CoreWeave AppArmor profile. See [Set up AppArmor profile for Enroot](https://docs.coreweave.com/products/sunk/manage_sunk/enroot-apparmor.md) for setup.

For a complete walkthrough of running a distributed training job on SUNK, see [Submit a training job](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md).

## Additional resources

For more information, see the following resources:

* [`coreweave/ml-containers` repository][ml-containers-repo]: Dockerfiles and source for all images.
* [Packages list][packages]: every published image and its current tags.
* [Slurm images](https://docs.coreweave.com/products/sunk/reference/slurm-images.md): the SUNK-built `slurm-containers` images for the Slurm control plane and nodes.
* [Create custom images for SUNK Standard](https://docs.coreweave.com/products/sunk/optimize_workloads/custom-images.md): customize a published image for SUNK.
* [Introduction to third-party frameworks](https://docs.coreweave.com/products/cks/clusters/frameworks/introduction.md): frameworks supported on CKS and SUNK.

[ml-containers-repo]: https://github.com/coreweave/ml-containers

[packages]: https://github.com/orgs/coreweave/packages?repo_name=ml-containers

[torch-pkg]: https://github.com/coreweave/ml-containers/pkgs/container/ml-containers%2Ftorch

[torch-extras-pkg]: https://github.com/coreweave/ml-containers/pkgs/container/ml-containers%2Ftorch-extras
