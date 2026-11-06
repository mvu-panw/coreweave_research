# Run SGLang

Source: https://docs.coreweave.com/products/cks/clusters/frameworks/sglang

# Run SGLang

> Run the SGLang serving framework with SkyPilot on CKS for LLM inference workloads

Using [SGLang](https://github.com/sgl-project/sglang?tab=readme-ov-file) on CKS is easiest with [SkyPilot](https://github.com/skypilot-org/skypilot), which provides a way to launch and manage distributed applications on Kubernetes clusters. SGLang is a serving framework for large language models (LLMs), and pairing it with SkyPilot lets you launch LLM inference workloads on CKS without managing Kubernetes manifests directly.

This guide is for CKS users who want to serve an LLM for inference on their cluster. It shows you how to set up SGLang with SkyPilot on CKS by covering the following:

* Install and run SkyPilot
* Run SGLang

By the end of this guide, you have a working SGLang inference server running on your CKS cluster.

## Prerequisites

Before you complete the steps in this guide, be sure your development environment meets the following requirements:

* You have your `kubeconfig` file properly set and can interact with clusters and Pods using `kubectl`.

* An environment variable set to `HF_TOKEN` with your Hugging Face token. For more information, see the Hugging Face instructions at [User access tokens](https://huggingface.co/docs/hub/en/security-tokens).

* Authentication to use the `meta-llama/Llama-3.1-8B-Instruct` model. For more information, go to [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B) and request access. Approval for restricted models can take a few hours or longer.

* The `socat` and `netcat` networking utilities.

## Install SkyPilot

SkyPilot is the launcher you use to deploy SGLang to CKS, so install it before continuing. You can install SkyPilot using [Anaconda](https://www.anaconda.com/) or [uv](https://github.com/astral-sh/uv). The following instructions cover both techniques. Choose whichever matches your existing Python toolchain.

### Install SkyPilot with Anaconda

Python development environment with [Anaconda](https://anaconda.org/anaconda/conda) installed.

The following commands create a Conda environment named `sky` with Python 3.10 and install SkyPilot with Kubernetes support:

```bash theme={"system"}
conda create -y -n sky python=3.10
conda activate sky
pip install "skypilot[kubernetes]"
```

> [!NOTE]
>
> * CKS requires SkyPilot version 0.10.1 or later.
> * SkyPilot requires Python 3.7 to 3.13.

Once you see output stating that Kubernetes is enabled infra, you've successfully installed SkyPilot. For example, you might see output similar to the following:

```text theme={"system"}
Enabled infra
  Kubernetes [compute]
```

**Debugging steps**: Follow any instructions for installing missing dependencies.

### Install SkyPilot with `uv`

To install SkyPilot with `uv`, you might need to download and install `uv` first. Follow the instructions on the [uv GitHub repository](https://github.com/astral-sh/uv).

After you install `uv`, the following commands create a virtual environment with Python 3.10 and install SkyPilot with Kubernetes support:

```bash theme={"system"}
uv venv --seed --python 3.10
uv pip install "skypilot[kubernetes]"
```

You should see output similar to the following:

```text theme={"system"}
Enabled infra
  Kubernetes [compute]
```

## Run SkyPilot

With SkyPilot installed, verify that it can reach your CKS cluster before launching workloads. The `sky check` command verifies SkyPilot's connectivity to your Kubernetes infrastructure:

```bash theme={"system"}
sky check
```

### Optional: Run a `nccl` test on Nodes with InfiniBand enabled

If you have Nodes with InfiniBand enabled, you can confirm that GPU-to-GPU networking is healthy across Nodes before running SGLang. Run a `nccl` test by completing the following steps:

1. Copy the following file and name it `nccl-network-tier.yaml`. Replace `accelerators` with your Node type (which corresponds to the `gpu.nvidia.com/class` property):

   ```yaml theme={"system"}
   name: nccl-network-tier
   resources:
     infra: k8s
     # Replace accelerators with your Node type that has InfiniBand enabled.
     accelerators: H100_NVLINK_80GB:8
     image_id: ghcr.io/coreweave/nccl-tests:12.8.1-devel-ubuntu22.04-nccl2.26.2-1-0708d2e
     network_tier: best  # Automatically requests rdma/ib: 1 resource and sets env vars

   num_nodes: 2

   run: |
     if [ "${SKYPILOT_NODE_RANK}" == "0" ]; then
       echo "Head node"

       # Total number of processes, NP should be the total number of GPUs in the cluster
       NP=$(($SKYPILOT_NUM_GPUS_PER_NODE * $SKYPILOT_NUM_NODES))

       # Append :${SKYPILOT_NUM_GPUS_PER_NODE} to each IP as slots
       nodes=""
       for ip in $SKYPILOT_NODE_IPS; do
         nodes="${nodes}${ip}:${SKYPILOT_NUM_GPUS_PER_NODE},"
       done
       nodes=${nodes::-1}
       echo "All nodes: ${nodes}"

       mpirun \
         --allow-run-as-root \
         --tag-output \
         -H $nodes \
         -np $NP \
         -N $SKYPILOT_NUM_GPUS_PER_NODE \
         --bind-to none \
         -x PATH \
         -x LD_LIBRARY_PATH \
         -x NCCL_DEBUG=INFO \
         -x NCCL_SOCKET_IFNAME=eth0 \
         -x NCCL_IB_HCA \
         -x UCX_NET_DEVICES \
         -x SHARP_COLL_ENABLE_PCI_RELAXED_ORDERING=1 \
         -x NCCL_COLLNET_ENABLE=0 \
         -x NCCL_NET_PLUGIN=none \
         /opt/nccl-tests/build/all_reduce_perf \
         -b 512M \
         -e 8G \
         -f 2 \
         -g 1 \
         -c 1 \
         -w 5 \
         -n 10
     else
       echo "Worker nodes"
     fi
   ```

   The `mpirun` command sets `NCCL_NET_PLUGIN=none` so the test runs on NCCL's built-in InfiniBand transport instead of the HPC-X plugin, and `NCCL_COLLNET_ENABLE=0` keeps the CollNet (SHARP) path disabled. These settings match the H100 non-SHARP reference job in the [`nccl-tests` repository](https://github.com/coreweave/nccl-tests/blob/master/mpi-operator/nccl-test-distributed-h100-64-mpijob.yaml). For more information, see the [NCCL configuration reference](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md).

2. Launch the `nccl` test cluster with SkyPilot:

   ```bash theme={"system"}
   sky launch -c nccl-test-sky nccl-network-tier.yaml
   ```

## Run SGLang

With SkyPilot installed and verified, you can now launch SGLang on your cluster to serve an LLM. To run [SGLang](https://github.com/sgl-project/sglang?tab=readme-ov-file) on CKS, you can use the following example script.

You need to complete the steps to install and run SkyPilot as described in the preceding sections.

The following example launches the `meta-llama/Llama-3.1-8B-Instruct` model behind an SGLang server on port 30000. To run SGLang, complete the following steps:

1. Copy the following YAML file and name it `sglang.yaml`. Be sure to replace the `accelerators` field with your GPU type:

   ```yaml theme={"system"}
   envs:
     HF_TOKEN: null

   resources:
     image_id: docker:lmsysorg/sglang:latest
     # Replace with your GPU type.
     accelerators: H100_NVLINK_80GB
     ports: 30000

   run: |
     conda deactivate
     python3 -m sglang.launch_server \
       --model-path meta-llama/Llama-3.1-8B-Instruct \
       --host 0.0.0.0 \
       --port 30000
   ```

2. Launch the SGLang server with SkyPilot, replacing `[HUGGING-FACE-TOKEN]` with your Hugging Face token:

   ```bash theme={"system"}
   HF_TOKEN=[HUGGING-FACE-TOKEN] sky launch -c sglang sglang.yaml --env HF_TOKEN
   ```
