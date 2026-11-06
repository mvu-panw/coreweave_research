# Run Ray on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk

# Run Ray on SUNK

> Integrate Ray's distributed computing framework with SUNK's Slurm-based scheduler for parallel workloads

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SUNK is CoreWeave's solution for running Slurm on Kubernetes. Using Ray on SUNK provides Ray's Python native parallelism with Slurm's enterprise-level scheduler. By using Ray on SUNK, you let Slurm manage when and where jobs run, while Ray manages how it runs distributed tasks.

This tutorial walks you through integrating Ray's distributed computing framework with SUNK's Slurm-based job scheduler. By the end, you have prepared a Ray container, launched a Ray cluster through Slurm, and learned how to connect to a running Ray environment for interactive development or debugging.

Consider running Ray on SUNK if one of the following applies:

* Most of your compute usage is through Slurm, and you need Ray to orchestrate workloads.

* You want to support Ray and Slurm users from a single environment, using the Slurm scheduler for efficient resource allocation.

## Prerequisites

Before completing the steps in the guide, make sure you have the following:

* Access to a SUNK cluster with permissions to submit jobs.
* Familiarity with Slurm commands, such as `srun`, `sbatch`, and `squeue`.

## Create a Ray cluster on Slurm

When working with containers on Slurm, you typically pull them as squash files to a shared directory in the Slurm login nodes. Within the shared directory, you can then run the containers using multiple nodes without making simultaneous repository pulls.

Two methods for pulling containers are available:

* **Pulling a Ray container and saving it as a squash file using `enroot`.** This is useful if you need to debug container errors.

* **Pulling a container as a `sqsh` file using `srun`.** This is useful when your containers are well-tested and you only want to run jobs.

### Pull a Ray container

This procedure uses the first method: pulling a Ray container and saving it as a squash file with `enroot`. Use this approach when you want a debuggable container that you can inspect and modify interactively. To pull a Ray container, complete the following steps.

1. From the login node, create an interactive session on a GPU by running the following command:

   You can also create a [VS Code tunnel](https://docs.coreweave.com/products/sunk/access_sunk/vs-code-with-slurm.md) to the GPU.

   ```bash theme={"system"}
   srun -p [NODE-TYPE] --exclusive --pty bash -i
   ```

   Change `[NODE-TYPE]` based on your available resources.

   The following example requests an `h100` node:

   ```bash title="Example with h100 node" theme={"system"}
   srun -p h100 --exclusive --pty bash -i
   ```

   You should now be in a session on a GPU node. Verify you are in a shared directory, such as your home directory or `/mnt/data`.

2. Import and start the container. This can be any container, but the following example uses a `rayproject` nightly container:

   ```bash theme={"system"}
   # Import the container
   enroot import docker://rayproject/ray:nightly-py39-gpu

   # Create the container
   enroot create rayproject+ray+nightly-py39-gpu.sqsh

   # Start the container
   enroot start --rw rayproject+ray+nightly-py39-gpu
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   ==========
   == CUDA ==
   ==========

   CUDA Version 12.1.1

   Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
   ```

You now have an interactive session running on a single node within the container. Because you used the `--rw` flag to start the container, changes you make are saved when you exit.

If you're using a container from `ghcr.io`, prefix it with `docker://`, for example, `docker://ghcr.io/`. If your container requires permissions, you need to configure your `enroot` credentials. For more information about `enroot`, see the [SUNK Training guide](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster.md#install-software-as-containers-using-pyxis-and-enroot).

### Create a conda environment

Instead of using containers, you can create a conda environment that includes your dependencies. However, **this is not recommended**. Ray requires the versions of Ray and Python used in the head and worker nodes to be identical to those used in the Ray script that runs.

Conda environments with many users can be difficult to manage, but conda may be easier for testing and debugging when running Ray on Slurm.

If you use conda, you need to initialize your conda environment (only once).

1. To initialize a conda environment, determine its PATH and initialize it:

   ```bash theme={"system"}
   which conda
   ```

   Use the conda PATH in the next command. For example, if the PATH is the following:

   ```text theme={"system"}
   /home/ray/anaconda3/bin/conda
   ```

   Enter the PATH in the following command:

   ```bash theme={"system"}
   /home/ray/anaconda3/bin/conda init bash
   source ~/.bashrc
   ```

2. Create an environment with the version of Ray that you want to use and any additional packages. In the following example, the environment is called `rayenv`:

   ```bash theme={"system"}
   # Create a conda environment with a specific Python version
   conda create --name rayenv python=3.12 pip

   # Activate the ray environment
   conda activate rayenv

   # Install ray with selected packages
   pip install -U "ray[data,train,tune,serve]"
   ```

You can now activate the same environment before you launch a Ray cluster or job.

### Generate `sbatch` files

With a Ray container or conda environment in place, the next step is to launch a Ray cluster through Slurm. You can write a script to generate `sbatch` files for creating Ray clusters of the size and specifications you want. This lets you generate the right `sbatch` commands programmatically. For examples of these kinds of scripts, refer to the [NERSC GitHub repository](https://github.com/NERSC/slurm-ray-cluster).

The following example script starts up a Ray cluster and also runs a job. If you want to start a Ray cluster and use it interactively, make sure the `sbatch` script doesn't exit by putting a `sleep inf` command in the script. This keeps the script running for a specified time as an interactive development cluster. You can exit it earlier if you don't need it.

The example script requests GPUs per task with the `#SBATCH --gpus-per-task` directive, hardcoded to `8` in the following examples. Adjust the number of GPUs per task as you need.

To see available capacity, use the `sinfo` command. The partitions of different SKUs are typically separated by name, for example, `h100`, `h200`.

```bash theme={"system"}
sinfo
```

The following is a sample `sbatch` script. In the final `srun` command, replace `[USERNAME]` with your username, `[RAY-CONTAINER-SQUASH-FILE]` with the path to your Ray container squash file, and `[PYTHON-SCRIPT]` with the Python script you want to run:

```bash theme={"system"}
#!/bin/bash
#SBATCH --job-name=raytest
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --tasks-per-node=1 # we will launch one worker task per node
#SBATCH --cpus-per-task=8  # each worker task gets 8 CPUs. Adjust as needed.
#SBATCH --mem-per-cpu=1GB  # each cpu gets 1 GB of memory. Adjust as needed.
#SBATCH --gpus-per-task=8  # each worker task will use 8 GPUs. Adjust as needed.
#SBATCH --time=1-00:00:00  # specify a time limit of one day

# Here we activate a conda environment named "rayenv" to load Ray
# and its dependencies. This assumes that you have already created a
# conda environment named "rayenv" with Ray installed.
eval "$(conda shell.bash hook)"
conda activate rayenv
# Getting the node names
nodes=$(scontrol show hostnames "$SLURM_JOB_NODELIST")
nodes_array=($nodes)

head_node=${nodes_array[0]}
head_node_ip=$(srun --nodes=1 --ntasks=1 -w "$head_node" hostname --ip-address)

# If we detect a space character in the head node IP, we'll
# convert it to an ipv4 address. This step is optional.
if [[ "$head_node_ip" == *" "* ]]; then
IFS=' ' read -ra ADDR <<<"$head_node_ip"
if [[ ${#ADDR[0]} -gt 16 ]]; then
 head_node_ip=${ADDR[1]}
else
 head_node_ip=${ADDR[0]}
fi
echo "IPV6 address detected. We split the IPV4 address as $head_node_ip"
fi

port=6379
ip_head=$head_node_ip:$port
export ip_head
echo "IP Head: $ip_head"

echo "Starting HEAD at $head_node"
srun --nodes=1 --ntasks=1 -w "$head_node" \
   ray start --head --node-ip-address="$head_node_ip" --port=$port \
   --num-cpus "${SLURM_CPUS_PER_TASK}" --num-gpus 1 --block &

# Optional, though may be useful in certain versions of Ray < 1.0.
sleep 10

# Number of nodes other than the head node.
worker_num=$((SLURM_JOB_NUM_NODES - 1))

for ((i = 1; i <= worker_num; i++)); do
   node_i=${nodes_array[$i]}
   echo "Starting WORKER $i at $node_i"
   srun --nodes=1 --ntasks=1 -w "$node_i" \
       ray start --address "$ip_head" \
       --num-cpus "${SLURM_CPUS_PER_TASK}" --num-gpus 1 --block &
   sleep 5
done

# Update --container-image and the Python script you want to run.
# For an example, see the srun command after this example.
srun -J "cont" --overlap --container-image=/mnt/home/[USERNAME]/[RAY-CONTAINER-SQUASH-FILE] --container-remap-root --container-mounts=/mnt/home:/mnt/home python3 -u /mnt/home/[USERNAME]/[PYTHON-SCRIPT] "$SLURM_CPUS_PER_TASK"
```

**Example `srun` command for the preceding `sbatch` script**:

```bash theme={"system"}
srun -J "cont" --overlap \
--container-image=/mnt/home/[USERNAME]/rayproject+ray+nightly-py39-gpu.sqsh \
--container-remap-root \
--container-mounts=/mnt/home:/mnt/home \
python3 -u /mnt/home/[USERNAME]/tune_basic_example.py "$SLURM_CPUS_PER_TASK"
```

* `[USERNAME]`: Replace with your username.
* `rayproject+ray+nightly-py39-gpu.sqsh`: This is the Ray container squash file you downloaded in the [Pull a Ray container](#pull-a-ray-container) section.
* `tune_basic_example.py`: Create this file under your username with the contents found in the [NERSC repository](https://github.com/NERSC/slurm-ray-cluster/blob/master/examples/tune_basic_example.py).

Ray requires each person to be able to create their own Ray environments. After you create a Ray environment, you can either interactively log in and launch jobs, or connect to a running container within that job to debug.

### Pull a container as a `sqsh` file using `srun`

This procedure covers the second method introduced earlier: pulling a container as a `sqsh` file directly with `srun`. Use this approach when your container is already well-tested and you only need to run jobs. To pull a container as a `sqsh` file using `srun`, complete the following steps.

1. On a login node, run a short command, such as `echo hello`, on the development container. As an example, the following uses a `nccl` test to pull and save the container.

   ```bash theme={"system"}
   srun --container-image=ghcr.io#coreweave/nccl-tests:12.8.1-devel-ubuntu22.04-nccl2.26.2-1-0708d2e \
          --container-remap-root --no-container-mount-home \
          --container-save ${HOME}/nccl-test.sqsh echo hello
   ```

   Update `${HOME}` and `nccl-test.sqsh` based on where you want to save the file and what name to give it.

   You should see output similar to the following:

   ```text theme={"system"}
   pyxis: imported docker image: ghcr.io#coreweave/nccl-tests:12.8.1-devel-ubuntu22.04-nccl2.26.2-1-0708d2e
   hello
   pyxis: exported container pyxis_228.0 to /mnt/home/username/nccl-test.sqsh
   ```

2. To pull the latest Ray container, run the following command:

   ```bash theme={"system"}
   srun --container-image=rayproject/ray:nightly-py39-gpu \
          --container-save ${HOME}/ray-nightly-py39-gpu echo hello
   ```

   Update `${HOME}` and `ray-nightly-py39-gpu` based on where you want to save the file and what name to give it.

   You should see output similar to the following:

   ```text theme={"system"}
   pyxis: importing docker image: rayproject/ray:nightly-py39-gpu
   pyxis: imported docker image: rayproject/ray:nightly-py39-gpu
   hello
   pyxis: exported container pyxis_229.0 to /mnt/home/username/ray-nightly-py39-gpu
   ```

#### Interactively modify a container using `srun`

You can interactively modify a container using `srun` by mounting the home directory explicitly and saving the container. You can then install Ray inside the container:

```bash theme={"system"}
srun --container-image=${HOME}/nccl-test.sqsh \
       --container-remap-root --container-mounts=/mnt/home:/mnt/home \
       --container-save ${HOME}/nccl-test-new.sqsh --pty bash -i
```

Update `${HOME}` and `nccl-test.sqsh` based on where you saved the container image from the previous steps.

When you exit the container, `nccl-test-new.sqsh` is saved.

## Work with Ray on Slurm

Now that you can launch a Ray cluster through Slurm, this section covers how to use it. After your Ray environment is running, you can either connect interactively to the running Ray cluster for development or attach to a containerized Ray job to debug or inspect it. See instructions for each option in the following sections.

### Interactively log in to a Ray environment

You can run the script by submitting the `sbatch` script. The script includes the command to sleep an environment.

1. Use the preceding example script and save it as `ray.devcluster.batch`, and then run the following command:

   ```bash theme={"system"}
   sbatch ray.devcluster.batch
   ```

2. Your Ray environment is a job. You can find out what job it is by running the following command:

   ```bash theme={"system"}
   squeue
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   JOBID  PARTITION     NAME     USER       ST     TIME   NODES NODELIST(REASON)
   1335   hpc-low       raytest  user_name  R      15:46  2     slurm-h100-231-[147,217]
   ```

3. In the preceding output, the `JOBID` is `1335`. This is a mini Ray environment with two `h100` nodes. To connect to it and begin running things interactively, run the following command:

   ```bash theme={"system"}
   srun --jobid=1335 --overlap --pty bash -i
   ```

   * `--jobid`: Replace `1335` with the job ID you want to run.
   * `--overlap`: Specifies that you attach to the head node of the specified job, here `--jobid=1335`.

You are now connected to the head node of your Ray cluster and can run Ray commands interactively.

### Attach to a Ray job using a container

If you launch a job using a container, you can start a container from the same image inside that job's allocation, instead of sleeping in the Ray environment for a launched job.

> [!NOTE]
>
> The steps in this section use `--container-image`, which starts a fresh container from the image on a node in the allocation. It does not enter the container the Ray job is already running. To attach to the running container itself and see the job's processes and files, name the container when the job creates it and attach with `--container-name=[NAME]:exec`. See [Access Slurm compute nodes](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md).

To attach to a Ray job using a container, complete the following steps.

1. Run the `squeue` command to figure out what job it is:

   ```bash theme={"system"}
   squeue
   ```

2. Use `sacct` to find the step that runs the container. Replace `[JOB-ID]` with the value from the `JOBID` column in the preceding `squeue` output for your Ray allocation.

   `sacct` is a Slurm command that gives more information about the "steps" of the job. Steps are tasks launched within the allocation that use some or all of the resources.

   ```bash theme={"system"}
   sacct -j [JOB-ID]
   ```

3. This starts the container in the same allocation, so you can debug the run interactively. You want to be able to connect with the same container to a specific step.

   ```bash theme={"system"}
   srun --overlap --container-image=/mnt/data/coreweave/ray/nccl-test-new.sqsh --jobid 1336.3 --pty bash -i
   ```

   * `--container-image`: Replace with the location of your container image.
   * `--jobid`: Replace with your job ID.

   The [example script](#generate-sbatch-files) gives the step a name using the `-J` flag in the `srun` command. This makes it easier to find. This takes a minute because it first launches all the Ray daemons.

   The allocation has multiple nodes, but each `srun` step lands on one of them. Without a node selection, Slurm places the step on the first node of the allocation, which is the Ray head node and where you can run `ray status`.

4. To connect to a specific node in your Ray environment, provide it on the command line with the `--nodelist` flag.

   ```bash theme={"system"}
   srun --overlap --nodelist=slurm-h100-227-211 \
        --container-image=/mnt/data/coreweave/ray/nccl-test-new.sqsh \
        --jobid 1336.3 --pty bash -i
   ```

   * `--nodelist`: Replace with your node.
   * `--container-image`: Replace with the location of your container image.
   * `--jobid`: Replace with your job ID.

### Stop a Ray environment

To delete a job, find the job ID using `squeue` and cancel it with `scancel`. Replace `[JOB-ID]` with the value from the `JOBID` column for the job you want to delete:

```bash theme={"system"}
scancel [JOB-ID]
```
