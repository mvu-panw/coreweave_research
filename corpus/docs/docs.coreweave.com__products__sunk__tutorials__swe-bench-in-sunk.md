# Run SWE-bench in SUNK with Docker

Source: https://docs.coreweave.com/products/sunk/tutorials/swe-bench-in-sunk

# Run SWE-bench in SUNK with Docker

> Run the SWE-bench LLM benchmark on SUNK using Docker-in-Docker with GPU resources

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SWE-bench is a benchmark for evaluating large language models on software issues collected from GitHub. SWE-bench uses Docker to create reproducible artifacts that can be ported to different platforms.

This guide is for SUNK users who want to evaluate large language models against the SWE-bench suite on GPU-backed nodes. By the end of the guide, you have SWE-bench installed in a Python virtual environment on a SUNK node and a successful benchmark run that produces a JSON report.

This guide explains how to run [SWE-bench](https://www.swebench.com/original.html) on SUNK with the following steps:

1. [Enable support for Docker in SUNK](https://docs.coreweave.com/products/sunk/run_workloads/docker-in-docker.md)
2. [Select a node to run the benchmark on](#acquire-gpu-resources)
3. [Install SWE-bench in a Python environment on the selected node](#clone-swe-bench-and-set-up-python)

## Tested versions

This guide is tested and verified on the following configurations:

* SUNK `cgroup/v1` and `cgroup/v2`
  * v6.9.1
  * v7.1.0
* NVIDIA L40 and H100 GPUs

## Prerequisites

To run SWE-bench on SUNK, you first need to enable Docker support. For instructions, see the [guide on using Docker in SUNK](https://docs.coreweave.com/products/sunk/run_workloads/docker-in-docker.md).

> [!WARNING]
>
> Using Docker in SUNK requires enabling privileged Pods and disabling the recommended AppArmor profile. This process grants elevated kernel capabilities and weakens isolation guarantees. See the [known security risks](https://docs.coreweave.com/products/sunk/run_workloads/docker-in-docker.md#known-security-risks) section for more details.
>
> **It is your responsibility to verify that third-party code is safe to execute alongside your other workloads**.

To run SWE-bench in SUNK, select a node to run the benchmark on, set up a Python environment on that node, and then install SWE-bench in the Python environment.

## Acquire GPU resources

SWE-bench needs an interactive shell on a GPU node so the benchmark harness can build Docker images and run evaluations against the GPU. First, identify a node or partition on which to run the benchmark. The following examples use an H100 node in the `h100` partition.

Choose **one** of the following methods:

### Option 1: `exec` into an existing GPU pod

List the Pods in your namespace, replacing `[NAMESPACE]` with your Kubernetes namespace:

```bash theme={"system"}
kubectl get pods -n [NAMESPACE]
```

In this example, the target Pod is named `h100-123-123`. Open an interactive terminal session inside the Pod with `kubectl exec`:

```bash theme={"system"}
kubectl exec -it -n [NAMESPACE] h100-123-123 -- bash
```

### Option 2: Start an interactive job within a Slurm login Pod

Use this option when you don't already have a GPU Pod running and want Slurm to allocate one for the session. In this example, the Slurm login Pod is `tenant-slurm-login-0`:

```bash theme={"system"}
kubectl exec -it -n [NAMESPACE] tenant-slurm-login-0 -- bash
```

Use `srun` to start an interactive session on your chosen partition. In this example, the partition is `h100`:

```bash theme={"system"}
srun --nodes=1 --gres=gpu:1 --partition=h100 --pty bash
```

## Clone SWE-bench and set up Python

With an interactive shell on a GPU node ready, you can install SWE-bench and run the benchmark. Clone SWE-bench and set up the Python environment. The following examples use [`uv`](https://docs.astral.sh/uv/) to create a Python virtual environment. For `venv` and `pip` versions of this process, see the [Python documentation](https://python.land/virtual-environments/virtualenv).

1. Install `uv` with `curl`:

   ```bash theme={"system"}
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

   Follow the instructions in the provided output about sourcing to add `uv` to your `PATH`.

2. Clone the `SWE-bench` repository:

   ```bash theme={"system"}
   git clone https://github.com/SWE-bench/SWE-bench.git
   cd SWE-bench
   ```

3. Create a Python virtual environment:

   ```bash theme={"system"}
   uv venv
   ```

4. Install the current directory, `SWE-bench`, as a Python package in the virtual environment:

   ```bash theme={"system"}
   uv pip install .
   ```

5. Execute the benchmark inside the Pod:

   ```bash theme={"system"}
   uv run python -m swebench.harness.run_evaluation \
       --predictions_path gold \
       --max_workers 1 \
       --instance_ids sympy__sympy-20590 \
       --namespace '' \
       --run_id validate-gold
   ```

   The expected output is as follows:

   ```text theme={"system"}
   Built swebench @ file:///opt/nccl-tests/SWE-bench
   Uninstalled 2 packages in 4ms
   Installed 2 packages in 4ms
   <frozen runpy>:128: RuntimeWarning: 'swebench.harness.run_evaluation' found in sys.modules after import of package 'swebench.harness', but prior to execution of 'swebench.harness.run_evaluation'; this may result in unpredictable behaviour
   Using gold predictions
   README.md: 3.67kB [00:00, 25.5MB/s]
   data/dev-00000-of-00001.parquet: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 107k/107k [00:00<00:00, 488kB/s]
   data/test-00000-of-00001.parquet: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.11M/1.11M [00:00<00:00, 13.0MB/s]
   Generating dev split: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 23/23 [00:00<00:00, 5326.84 examples/s]
   Generating test split: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:00<00:00, 25575.54 examples/s]
   Building base image (sweb.base.py.x86_64:latest)
   Base images built successfully.
   Total environment images to build: 1
   All environment images built successfully.
   Running 1 instances...
   Evaluation: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:56<00:00, 56.05s/it, ✓=1, ✖=0, error=0]All instances run.
   Evaluation: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:56<00:00, 56.05s/it, ✓=1, ✖=0, error=0]
   Cleaning cached images...
   Removed 0 images.
   Total instances: 1
   Instances submitted: 1
   Instances completed: 1
   Instances incomplete: 0
   Instances resolved: 1
   Instances unresolved: 0
   Instances with empty patches: 0
   Instances with errors: 0
   Unstopped containers: 0
   Unremoved images: 0
   Report written to gold.validate-gold.json
   ```

   A successful run creates a report file named `gold.validate-gold.json` in the working directory.

## Known limitations

### H200 GPU compile error

SWE-bench does not compile on an H200 GPU. The benchmark terminates with the following error:

```text wrap theme={"system"}
ebench.harness.docker_build.BuildImageError: Error building image sweb.base.py.x86_64:latest: The command '/bin/sh -c apt update && apt install -y wget git build-essential libffi-dev libtiff-dev python3 python3-pip python-is-python3 jq curl locales locales-all tzdata && rm -rf /var/lib/apt/lists/*' returned a non-zero code: 255
Check (logs/build_images/base/sweb.base.py.x86_64__latest/build_image.log) for more information.
```

### Non-InfiniBand node behavior

Enabling privileged Pods on non-InfiniBand nodes may result in NCCL failing to use `eth0` correctly. Privileged Pods expose InfiniBand devices that aren't enabled on these nodes, and NCCL tries to use them. The HPC-X network plugin also loads by default when HPC-X is on the library path. For more information about plugin loading, see the [NCCL configuration reference](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md). To force NCCL to use `eth0`, set the following environment variables:

```bash theme={"system"}
# Non-InfiniBand nodes only: pin NCCL and UCX to eth0 and disable CollNet.
export NCCL_SOCKET_IFNAME=eth0
export UCX_NET_DEVICES=eth0
export NCCL_COLLNET_ENABLE=0
export NCCL_IB_HCA=eth0
```
