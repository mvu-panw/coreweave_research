# Run veRL on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/verl-on-sunk

# Run veRL on SUNK

> Run Group Relative Policy Optimization (GRPO) training with veRL on SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This guide shows you how to run Group Relative Policy Optimization (GRPO) training with [veRL](https://github.com/verl-project/verl) on SUNK using the [Qwen3 8B model](https://huggingface.co/Qwen/Qwen3-8B). GRPO is a reinforcement learning technique for fine-tuning large language models on reasoning tasks, and veRL provides a trainer that scales across multiple GPUs with Ray. By the end of this tutorial, you have a reproducible Slurm batch script that pulls the veRL container, preprocesses the GSM8K dataset, launches a Ray cluster on SUNK, and runs GRPO training end-to-end. This guide is intended for ML practitioners who already have access to a SUNK cluster and want to run GRPO experiments without assembling the toolchain themselves.

The provided Slurm script handles container setup, dataset preparation, and Ray orchestration. It also writes logs and checkpoints to a run directory, and automatically logs to [Weights & Biases](https://wandb.ai/site) if you provide a `WANDB_API_KEY`.

## Prerequisites

To use this guide, you need the following:

* Access to a SUNK cluster.
* One available GPU node, at minimum. We recommend using an H200 node. By default, the script requests 1 node with 8 GPUs. If you use a smaller node, you need to adjust the hyperparameters to reduce GPU memory consumption.
* An NFS-backed working directory visible to all nodes (for data, checkpoints, container cache).
* Optionally, a `WANDB_API_KEY` to log to W\&B.

> [!NOTE]
>
> **Tested version**
>
> This script uses the following defaults:
>
> * veRL container tag: `app-verl0.5-transformers4.55.4-vllm0.10.0-mcore0.13.0-te2.2`
> * veRL commit: `8fdc4d3f202f41461f4de9f42a637228e342668b` (v0.5.0)
>
> Override through `VERL_TAG` and `VERL_VERSION` if needed.

## Choose an NFS-backed working directory

Because the training job spans multiple processes that must read and write the same data, container image, and checkpoints, you must place these artifacts on storage that every node in the allocation can see. Select a directory mounted on all nodes. In many SUNK clusters, your home directory suffices.

Optionally, you can export overrides for data, checkpoints, and container cache locations. This guide uses the default values, with no overrides, when showing example commands. If you set custom paths, substitute them in the commands below where indicated.

```bash theme={"system"}
# Example in home directory
mkdir -p ~/verl-experiments/qwen3-8b-grpo
cd ~/verl-experiments/qwen3-8b-grpo

# Optional: override defaults
# export DATA_DIR=/mnt/data/verl-experiments/data
# export CHECKPOINT_DIR=/mnt/data/verl-experiments/checkpoints
# export CONTAINER_DIR=/mnt/data/verl-experiments/containers
```

## Optional: Export your W\&B API key

If you set a `WANDB_API_KEY`, the veRL job logs to W\&B automatically. To set your API key, run the following commands, replacing `[WANDB-API-KEY]` with your W\&B API key:

```bash theme={"system"}
export WANDB_API_KEY=[WANDB-API-KEY]
echo "export WANDB_API_KEY=$WANDB_API_KEY" >> ~/.bashrc
```

## Create the batch script

The batch script is the entry point for the entire training run. It declares the Slurm resource request, configures the container and Ray environment, prepares the dataset, and launches GRPO training.

The script's network settings are for InfiniBand clusters. They keep UCX on the front-end network. If your stack needs UCX on the RDMA fabric, follow the UCX exception in the [InfiniBand cluster recipe](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#infiniband-cluster-recipe). For RoCE clusters, use the [RoCE cluster recipe](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#roce-spectrum-x-cluster-recipe).

Create the `verl-grpo-qwen3-8B-gsm8k.sbatch` script in your working directory:

```bash theme={"system"}
cat << 'EOF' > verl-grpo-qwen3-8B-gsm8k.sbatch
#!/bin/bash
###
#SBATCH --job-name=verl-grpo-qwen3-8B-gsm8k
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=8
#SBATCH --cpus-per-task=128
#SBATCH --mem=512GB
#SBATCH --time=10:00:00
#SBATCH --output="logs/%x_%j.out" # Use %x for job name and %j for slurm job ID in output file name
#SBATCH --exclusive

# NCCL environment variables are documented at:
# https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
# Out Of Band is set to run over front-end Ethernet.
# Backend is restricted to use ibp* interfaces to ensure it doesn't try to use any RoCE interfaces from the frontend.

export NCCL_SOCKET_IFNAME=eth0
export NCCL_IB_HCA=ibp

# Keep UCX off the InfiniBand fabric. This doesn't disable UCX.
# If your stack needs UCX over RDMA, use the devices and transports it needs.
# See the NCCL configuration reference linked above.
export UCX_TLS=tcp
export UCX_NET_DEVICES=eth0
export OMPI_MCA_coll_hcoll_enable=0
export PMIX_MCA_gds='^ds12'

# Define veRL container version we will use
# See https://hub.docker.com/r/verlai/verl/tags for available tags.
verl_tag="${VERL_TAG:-app-verl0.5-transformers4.55.4-vllm0.10.0-mcore0.13.0-te2.2}"
verl_version="${VERL_VERSION:-8fdc4d3f202f41461f4de9f42a637228e342668b}" # v0.5.0

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

ensure_nfs_dir() {
  local dir="$1"
  local error_message="$2"
  mkdir -p "$dir"
  local fstype
  fstype="$(stat '-fc%T' "$dir")"
  if [ "$fstype" != "nfs" ] ; then
    log "${error_message:-You must specify a directory that is mounted on all cluster nodes.}" >&2
    exit 1
  fi
}

# Define all the NFS directories we will use
export DATA_DIR="${DATA_DIR:-$(realpath -s data)}"
export CHECKPOINT_DIR="${CHECKPOINT_DIR:-$(realpath -s checkpoints)}"
export CONTAINER_DIR="${CONTAINER_DIR:-$(realpath -s images)}"
export TMPDIR="/tmp"
run_suffix="${RUN_SUFFIX:-${SLURM_JOB_ID:-$(date '+%Y%m%d_%H%M%S')}}"
export RUN_DIR="${RUN_DIR:-$CHECKPOINT_DIR/run_$run_suffix}"
export WANDB_DIR="${WANDB_DIR:-$RUN_DIR}"

log "Run directory: $RUN_DIR"
ensure_nfs_dir "$DATA_DIR" 'You must specify a data directory that is mounted on all cluster nodes.'
ensure_nfs_dir "$CHECKPOINT_DIR" 'You must specify a checkpoint directory that is mounted on all cluster nodes.'
ensure_nfs_dir "$CONTAINER_DIR" 'You must specify a container directory that is mounted on all cluster nodes.'
ensure_nfs_dir "$RUN_DIR" 'You must specify a RUN_DIR that is mounted on all cluster nodes.'
ensure_nfs_dir "$WANDB_DIR" 'You must specify a WANDB_DIR that is mounted on all cluster nodes.'

# Pull the container image, if not already pulled. For large parallel jobs, this
# will save time by not hitting the repository from each task. This will
# be executed once on the head node of the allocation.
# Will also clone and install the veRL package itself as that is not included in the container image.
export CONTAINER_IMAGE="${CONTAINER_DIR}/${verl_tag}_${verl_version}.sqsh"
if [ -f "$CONTAINER_IMAGE" ]; then
    log "Container image for veRL version $verl_tag already exists, no need to pull."
else
    log "Pulling container image for veRL version: $verl_tag and saving to $CONTAINER_IMAGE"
    srun --job-name=verl-image-pull \
        --container-image="docker://verlai/verl:$verl_tag" \
        --container-save="$CONTAINER_IMAGE" \
        bash -c "
        git clone https://github.com/verl-project/verl.git &&
        cd verl &&
        git checkout $verl_version &&
        pip install --no-deps 'click==8.1.7' 'typing_extensions>=4.14,<5' &&
        pip install -e . --no-deps" || {
        log "Failed to clone and install veRL package" >&2
        exit 1
    }
fi

# Log the assigned nodes
log "Using nodes: $SLURM_JOB_NODELIST"

# Download and process the dataset if necessary
mkdir -p "$DATA_DIR/gsm8k"
if [ ! -f "$DATA_DIR/gsm8k/train.parquet" ] || [ ! -f "$DATA_DIR/gsm8k/test.parquet" ]; then
    log "Downloading and processing GSM8K dataset..."
    srun --job-name=gsm8k-preprocess --nodes=1 \
        --container-image="$CONTAINER_IMAGE" \
        --container-mounts="$DATA_DIR:$DATA_DIR" \
        python3 verl/examples/data_preprocess/gsm8k.py --local_dir "$DATA_DIR/gsm8k" || {
        log "Failed to download and process GSM8K dataset" >&2
        exit 1
    }
else
    log "Using existing GSM8K dataset in $DATA_DIR/gsm8k"
fi

# Initialize the Ray cluster that veRL will use
nodes=$(scontrol show hostnames "$SLURM_JOB_NODELIST")
nodes_array=($nodes)

head_node=${nodes_array[0]}
head_node_ip=$(srun --job-name=head-ip --nodes=1 --ntasks=1 -w "$head_node" hostname --ip-address)

# If we detect a space character in the head node IP, we'll
# convert it to an ipv4 address. This step is optional.
if [[ "$head_node_ip" == *" "* ]]; then
    IFS=' ' read -ra ADDR <<<"$head_node_ip"
    if [[ ${#ADDR[0]} -gt 16 ]]; then
        head_node_ip=${ADDR[1]}
    else
        head_node_ip=${ADDR[0]}
    fi
    log "IPV6 address detected. We split the IPV4 address as $head_node_ip"
fi

# veRL expects this `RAY_ADDRESS` env var to be set when initializing the task runner.
port=6379
export RAY_ADDRESS="$head_node_ip:$port"
log "Ray Address: $RAY_ADDRESS"

# Make sure NFS paths are available, but also the tmp DIR
# so that files created by the ray workers are available to the main
# task runner.
mounts="$DATA_DIR:$DATA_DIR,$CHECKPOINT_DIR:$CHECKPOINT_DIR,$TMPDIR:$TMPDIR"

log "Starting HEAD at $head_node"
srun --job-name=ray-head --nodes=1 --ntasks=1 -w "$head_node" \
    --container-image="$CONTAINER_IMAGE" \
    --container-mounts="$mounts" \
    ray start --head --node-ip-address="$head_node_ip" --port=$port \
    --include-dashboard=false \
    --num-cpus "${SLURM_CPUS_PER_TASK}" --num-gpus 8 --block &

# Ensure the head node is ready before starting the workers.
sleep 5

# Number of nodes other than the head node.
worker_num=$((SLURM_JOB_NUM_NODES - 1))

for ((i = 1; i <= worker_num; i++)); do
   node_i=${nodes_array[$i]}
   log "Starting WORKER $i at $node_i"
   srun --job-name="ray-worker-$i" --nodes=1 --ntasks=1 -w "$node_i" \
        --container-image="$CONTAINER_IMAGE" \
        --container-mounts="$mounts" \
        ray start --address "$RAY_ADDRESS" \
        --include-dashboard=false \
        --num-cpus "${SLURM_CPUS_PER_TASK}" --num-gpus 8 --block &
done

# Ensure the workers are ready before running the training script.
sleep 5

# Run the GRPO training script after the Ray cluster is initialized
epochs=1 # Reduce epochs for the tutorial
log "Running GRPO training script..."
PYTHONUNBUFFERED=1 srun --job-name=grpo-training --kill-on-bad-exit=1 --overlap --nodes=1 -w "$head_node" \
    --container-image="$CONTAINER_IMAGE" \
    --container-mounts="$mounts" \
    bash verl/examples/grpo_trainer/run_qwen3-8b.sh \
    data.train_files="$DATA_DIR/gsm8k/train.parquet" \
    data.val_files="$DATA_DIR/gsm8k/test.parquet" \
    trainer.total_epochs="$epochs" \
    trainer.default_local_dir="$RUN_DIR"

log "Stopping Ray cluster gracefully..."
srun --job-name=ray-stop-all \
    --overlap \
    --nodes="$SLURM_JOB_NUM_NODES" \
    --ntasks="$SLURM_JOB_NUM_NODES" \
    --ntasks-per-node=1 \
    --container-image="$CONTAINER_IMAGE" \
    --container-mounts="$mounts" \
    ray stop || log "Ray stop failed on one or more nodes" >&2

EOF
```

### How the script works

> [accordion] Detailed explanation of how the script works
>
> SUNK supports running Slurm jobs inside `enroot` containers through the Pyxis plugin. Rather than rebuild dependencies each time, the batch script saves a container image locally before launching the training job, or reuses one that already exists. The script uses `srun` with the `--container-image` flag pointing to a public veRL base image, already bundled with `vLLM`, `SGLang`, and `Megatron`. Since this container does not include veRL itself, the script clones the veRL repository at the pinned commit and installs the veRL package from source, including the [Qwen3-8B training launch script](https://github.com/verl-project/verl/blob/v0.5.0/examples/grpo_trainer/run_qwen3-8b.sh) used in this tutorial. The `--container-save` flag then saves the container image to a local NFS directory.
>
> To prepare the dataset, a follow-up `srun` executes `verl/examples/data_preprocess/gsm8k.py`, which downloads [the `GSM8K` dataset](https://huggingface.co/datasets/openai/gsm8k) from Hugging Face and writes `train.parquet` and `test.parquet` into `DATA_DIR/gsm8k` so future runs can reuse the results without re-downloading.
>
> The script then starts a Ray head on the first node and workers on the remaining nodes, and exports `RAY_ADDRESS` so veRL can attach. This pattern mirrors the guidance in the [Run Ray on SUNK](https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk.md) guide.
>
> With the container cached and the dataset ready, the tutorial launches the Qwen3-8B GRPO script with `srun` on rank 0. veRL's trainer then uses the previously created Ray cluster to orchestrate processes across the nodes. The script passes config overrides to the trainer as CLI arguments, including input and output paths and a reduced total number of epochs. After the training script completes, it launches a final `srun` to gracefully tear down the Ray cluster.

After saving the file, you have a self-contained batch script that encodes the full GRPO training workflow and is ready to submit to Slurm.

## Submit the job

With the batch script in place, the next step is to hand it to Slurm so the scheduler can allocate the requested nodes and run the workflow. After creating the script, submit the job to Slurm with `sbatch`, as follows:

```bash theme={"system"}
sbatch verl-grpo-qwen3-8B-gsm8k.sbatch
```

Once submitted, the job performs the following steps:

1. Pull and cache the veRL container.
2. Download and preprocess [the `GSM8K` dataset](https://huggingface.co/datasets/openai/gsm8k), if missing.
3. Start a Ray cluster inside the allocation.
4. Run GRPO training, with 1 epoch by default.
5. Write logs and checkpoints to your run directory.

## Monitor progress

After submission, the job runs asynchronously on the cluster. The following sections describe how to locate the job, inspect its progress, and find the artifacts it produces.

### Fetch the job ID

The job ID is the handle Slurm uses to identify your run. Capturing it in an environment variable makes the rest of the monitoring commands easier to copy and reuse. Fetch the Slurm job ID from `squeue`, as follows:

```bash theme={"system"}
export VERL_JOB_ID="$(squeue --user=$(whoami) --name=verl-grpo-qwen3-8B-gsm8k -h -o "%A" | head -n1)"
```

### View the job status

Once you have the job ID, you can inspect the status of each step using `sacct`, as follows:

```bash theme={"system"}
sacct -j ${VERL_JOB_ID}
```

This outputs the status of each `srun` step in the `sbatch` script. With `sacct`, each step appears in its own row, in the following order:

1. Container image creation
2. Dataset processing
3. Ray node startup
4. Training job execution
5. Ray cluster cleanup

### Stream runtime logs

To stream runtime logs, use `tail` as follows:

```bash theme={"system"}
tail -f "logs/verl-grpo-qwen3-8B-gsm8k_${VERL_JOB_ID}.out"
```

### View the dataset

The `GSM8K` dataset is saved at the following path:

```bash theme={"system"}
ls -lah ./data/gsm8k
```

### View the run directory artifacts

To view the run directory artifacts, use `ls` as follows:

```bash theme={"system"}
ls -lah ./checkpoints/run_${VERL_JOB_ID}
```

Before a checkpoint is written, `wandb` is likely the only directory you'll see listed.

### Find the W\&B link in logs

To find the W\&B link in logs, use `grep` as follows:

```bash theme={"system"}
grep -E "View run at|View project at:" "logs/verl-grpo-qwen3-8B-gsm8k_${VERL_JOB_ID}.out"
```

The job can take about 15 minutes to reach the W\&B initialization step. Once initialized, the W\&B project and run URLs print in the logs and resemble the following:

```text theme={"system"}
wandb: ⭐️ View project at https://wandb.ai/<user>/verl_grpo_example_gsm8k
wandb: 🚀 View run at https://wandb.ai/<user>/verl_grpo_example_gsm8k/runs/nli58bea
```

## Example outputs

The following examples show what a successful run produces on disk and in the logs, so you can confirm your own run matches the expected shape.

### Directories created

```text theme={"system"}
./images/
  app-verl0.5-transformers4.55.4-vllm0.10.0-mcore0.13.0-te2.2_8fdc4d3f202f41461f4de9f42a637228e342668b.sqsh

./data/
  gsm8k/
    train.parquet
    test.parquet

./logs/
  verl-grpo-qwen3-8B-gsm8k_${VERL_JOB_ID}.out

./checkpoints/
  run_${VERL_JOB_ID}/        <-- RUN_DIR (primary outputs)
    wandb/                   <-- Local W&B run files (if WANDB_API_KEY is set)
    global_step_7/           <-- Final step for this tutorial
      actor/
        model_world_size_8_rank_*.pt
        optim_world_size_8_rank_*.pt
        extra_state_world_size_8_rank_*.pt
        huggingface/         <-- Saved model config + tokenizer
```

### Sample log excerpt

```text theme={"system"}
[2025-11-14 21:06:47] Run directory: /mnt/home/<user>/verl-experiments/checkpoints/run_6237
[2025-11-14 21:06:47] Using nodes: h200-204-169
[2025-11-14 21:06:47] Using existing GSM8K dataset in /mnt/home/<user>/verl-experiments/data/gsm8k
[2025-11-14 21:06:47] Ray Address: 10.0.5.165:6379
[2025-11-14 21:06:48] Starting HEAD at h200-204-169
[2025-11-14 21:06:58] Running GRPO training script...
...
local_global_step_folder: /mnt/home/<user>/verl-experiments/checkpoints/run_6237/global_step_7
INFO:2025-11-14 21:36:55,017:[Rank 7] Saved model to /mnt/home/<user>/verl-experiments/checkpoints/run_6237/global_step_7/actor/model_world_size_8_rank_7.pt
INFO:2025-11-14 21:37:14,123:[Rank 1] Saved optim to /mnt/home/<user>/verl-experiments/checkpoints/run_6237/global_step_7/actor/optim_world_size_8_rank_1.pt
INFO:2025-11-14 21:37:14,159:[Rank 1] Saved extra_state to /mnt/home/<user>/verl-experiments/checkpoints/run_6237/global_step_7/actor/extra_state_world_size_8_rank_1.pt
INFO:2025-11-14 21:37:15,223:[Rank 0] Saved model config and tokenizer class to /mnt/home/<user>/verl-experiments/checkpoints/run_6237/global_step_7/actor/huggingface
("Final validation metrics: {'val-core/openai/gsm8k/reward/mean@1': " '0.6588324488248674}')
[2025-11-14 21:37:36] Stopping Ray cluster gracefully...
SUCC scripts.py:1395 -- Stopped all 6 Ray processes.
```
