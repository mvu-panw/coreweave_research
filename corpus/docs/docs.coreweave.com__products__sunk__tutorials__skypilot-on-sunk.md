# Run SkyPilot on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/skypilot-on-sunk

# Run SkyPilot on SUNK

> Use SkyPilot to run containerized GPU workloads and interactive development sessions on SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SkyPilot is an open source framework that provides a unified interface to run AI workloads across any infrastructure, including Slurm and SUNK. When you use SkyPilot on SUNK, you define your workload in a YAML file, and SkyPilot handles the `sbatch` submission, container lifecycle management through [Pyxis and Enroot](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster.md#install-software-as-containers-using-pyxis-and-enroot), and multi-node coordination.

This guide is for SUNK users who want a simpler workflow to submit and manage GPU workloads than to write `sbatch` scripts by hand. It covers how to install SkyPilot, run containerized GPU workloads, use SkyPilot for interactive development as an alternative to `salloc`, and manage jobs on your SUNK cluster.

Consider using SkyPilot on SUNK if any of the following apply:

* You want a simpler interface to submit GPU workloads without writing `sbatch` scripts directly.

* You need to run containerized workloads across multiple nodes and want SkyPilot to handle the distributed setup.

* You want an `salloc`-like interactive development workflow with persistent sessions you can SSH into.

## Prerequisites

Before you complete the steps in this guide, be sure you have the following:

* A SUNK cluster running SUNK v7.x or later with Enroot 4.0.1 or later and Pyxis v0.21.0 or later.
* SSH access to your Slurm login node.
* Familiarity with Slurm commands, such as `srun`, `sbatch`, and `squeue`.
* Python 3.8 or later installed locally.

> [!WARNING]
>
> Container support through SkyPilot requires SUNK v7.x or later. Earlier versions with Enroot 3.5.0 have a known bug that prevents SkyPilot's container lifecycle management from working correctly.

## Install SkyPilot

Install SkyPilot locally so you can submit jobs to your SUNK cluster from your workstation. The Slurm plugin lets SkyPilot translate your YAML workload definitions into `sbatch` submissions.

```bash theme={"system"}
pip install "skypilot-nightly[slurm]"
```

### Configure SkyPilot for your SUNK cluster

To point SkyPilot at your SUNK cluster, complete the following steps:

1. Create the SkyPilot Slurm SSH configuration file:

   ```bash theme={"system"}
   mkdir -p ~/.slurm
   touch ~/.slurm/config
   ```

2. Add your SUNK login node to `~/.slurm/config`:

   ```text theme={"system"}
   Host [CLUSTER-NAME]
       HostName [LOGIN-NODE-IP]
       User [USERNAME]
       IdentityFile ~/.ssh/id_ed25519
   ```

   Replace the placeholders with the following values:

   * `[CLUSTER-NAME]`: A name for your cluster, for example `my-sunk-cluster`.
   * `[LOGIN-NODE-IP]`: Your login node's external IP address. To find it, run `kubectl get svc slurm-login -n tenant-slurm`.
   * `[USERNAME]`: Your Slurm username.

3. Start the SkyPilot API server and verify your configuration:

   ```bash theme={"system"}
   sky api start
   sky check
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   Enabled infra
     Slurm [compute]
       Allowed clusters:
       └── my-sunk-cluster
   ```

With SkyPilot installed and your cluster configured, you're ready to submit workloads.

## Containerized workloads

SkyPilot uses the `image_id` field in your YAML to specify a container image. Internally, this translates to Pyxis `--container-image` and `--container-name` flags on the `sbatch` and `srun` commands. You don't interact with Pyxis or Enroot directly.

### Run a single-node GPU task

Create a YAML file named `task.yaml` that specifies your resources and container image:

```yaml theme={"system"}
name: pytorch-gpu-test

resources:
  cloud: slurm
  accelerators: [GPU-TYPE]:[GPU-COUNT]
  image_id: docker:nvcr.io/nvidia/pytorch:24.12-py3

run: |
  python -c "
  import torch
  print(f'PyTorch {torch.__version__}')
  print(f'CUDA available: {torch.cuda.is_available()}')
  print(f'GPU count: {torch.cuda.device_count()}')
  if torch.cuda.is_available():
      print(f'GPU: {torch.cuda.get_device_name(0)}')
  "
```

Replace the placeholders with the following values:

* `[GPU-TYPE]`: The GPU type available on your cluster, for example `H100` or `B200`.
* `[GPU-COUNT]`: The number of GPUs to request.

The following table describes the key fields:

| Field | Description |
| - | - |
| `cloud: slurm` | Targets your SUNK cluster. |
| `accelerators` | GPU type and count. Must match a GPU type available on your cluster. Use `sinfo` on the login node to check available partitions. |
| `image_id` | The container image. Prefix with `docker:` for registry images. Supports Docker Hub, NGC, and GHCR. |
| `run` | Commands to execute inside the container. |

Launch the task, replacing `[TASK-YAML]` with the path to your YAML file:

```bash theme={"system"}
sky launch [TASK-YAML] -y
```

SkyPilot submits an `sbatch` job to your SUNK cluster, pulls and initializes the container image on the allocated node, runs the `run` commands inside the container, and streams logs back to your terminal.

> [!NOTE]
>
> The first launch with a given container image takes several minutes while SkyPilot pulls and caches the image. Subsequent launches reuse the cached image and start faster.

### Use a setup block for dependencies

If your workload needs additional packages, use the `setup` field. Setup runs once when the cluster is first provisioned, before `run`:

```yaml theme={"system"}
name: training-job

resources:
  cloud: slurm
  accelerators: [GPU-TYPE]:8
  image_id: docker:nvcr.io/nvidia/pytorch:24.12-py3

setup: |
  pip install wandb transformers datasets

run: |
  torchrun --nproc_per_node=$SKYPILOT_NUM_GPUS_PER_NODE train.py
```

## Interactive development

SkyPilot can work as an alternative to `salloc` for interactive GPU development. Instead of holding a terminal session open, SkyPilot provisions a persistent Slurm allocation that you can connect to over SSH and submit commands to on demand.

Internally, SkyPilot submits an `sbatch` job with `sleep infinity` as the main process, which keeps the allocation alive indefinitely. SSH and `sky exec` then attach to that running job through `srun --overlap`. The allocation stays up until you explicitly tear it down with `sky down`.

### Create a resource YAML

Create a YAML file that specifies resources but no `run` command:

```yaml theme={"system"}
name: dev-session

resources:
  cloud: slurm
  accelerators: [GPU-TYPE]:[GPU-COUNT]
  image_id: docker:nvcr.io/nvidia/pytorch:24.12-py3
```

> [!NOTE]
>
> The `image_id` field is optional. Without it, you get a bare-metal session on the compute node. With it, you get an interactive container that has your chosen ML framework pre-installed.

### Launch the cluster and connect

To launch your interactive session and attach to it, complete the following steps:

1. Launch the cluster:

   ```bash theme={"system"}
   sky launch -c [CLUSTER-NAME] interactive.yaml -y
   ```

   Replace `[CLUSTER-NAME]` with a name for your interactive session, for example `dev`.

2. Use SSH to log in to the running allocation:

   ```bash theme={"system"}
   ssh [CLUSTER-NAME]
   ```

   This connects through the Slurm compute node and opens a shell in the container if you specified `image_id`. You can then run commands interactively, as you would inside an `salloc` session:

   ```bash theme={"system"}
   nvidia-smi -L
   python -c "import torch; print(torch.__version__)"
   ```

3. Optional: Submit batch tasks to the running allocation with `sky exec`, similar to running `srun` within an existing `salloc`:

   ```bash theme={"system"}
   sky exec [CLUSTER-NAME] task.yaml
   ```

4. When you're done, release the Slurm allocation:

   ```bash theme={"system"}
   sky down [CLUSTER-NAME]
   ```

The following table maps common Slurm interactive commands to their SkyPilot equivalents:

| Slurm built-in | SkyPilot equivalent |
| - | - |
| `salloc --gres=gpu:1` | `sky launch -c dev interactive.yaml` |
| `srun nvidia-smi` | `ssh dev` and run commands, or `sky exec dev task.yaml` |
| `exit` or `scancel` | `sky down dev` |
| `squeue` | `sky queue dev` |

## Manage jobs

After you have one or more SkyPilot clusters running on SUNK, use the following commands to inspect their state, stream logs, and release resources when you're finished.

In SkyPilot, a "cluster" refers to the named Slurm allocation that SkyPilot manages on your behalf. Use the cluster name you defined with `sky launch -c [CLUSTER-NAME]` in the following commands:

| Command | Description |
| - | - |
| `sky status` | List all active clusters and their current status. |
| `sky queue [CLUSTER-NAME]` | Show all jobs on the specified cluster. |
| `sky logs [CLUSTER-NAME]` | Stream logs from the latest job on the specified cluster. |
| `sky cancel [CLUSTER-NAME] [JOB-ID]` | Cancel a specific job without releasing the allocation. |
| `sky down [CLUSTER-NAME]` | Tear down the cluster and release its Slurm allocation. |

## Known limitations

SkyPilot on SUNK has the following known limitations:

* **Managed jobs require consolidation mode.** `sky jobs launch` doesn't work with the default local API server because it requires a separate long-running controller process to monitor managed jobs. To enable managed jobs, turn on [consolidation mode](https://docs.skypilot.ai/en/stable/examples/managed-jobs.html#jobs-consolidation-mode), which runs the jobs controller within the API server. Consolidation mode is enabled by default on remote API servers deployed with `--deploy`. For a local API server, you must enable it manually in `~/.sky/config.yaml`:

  ```yaml theme={"system"}
  jobs:
    controller:
      consolidation_mode: true
  ```

  After you update the configuration, restart the API server for the change to take effect.

* **Autostop isn't supported.** Clusters remain active until you explicitly tear them down with `sky down`. Remember to release allocations when they're no longer needed to avoid wasting resources.

* **`sky exec` requires explicit GPU requests for GPU visibility.** When you run tasks with `sky exec` on container-based clusters, GPUs may not be visible unless you specify the `--gpus` flag. For example, `sky exec -c [CLUSTER-NAME] --gpus [GPU-TYPE]:[GPU-COUNT] -- nvidia-smi -L`. For interactive GPU work, you can also use `ssh [CLUSTER-NAME]` to connect directly to the running allocation.

* **SSH requires SUNK v7.x or later.** On SUNK v6.x, SSH to running jobs doesn't work due to Dropbear and Enroot compatibility issues.

* **Container support requires SUNK v7.x or later.** Earlier versions that use Enroot 3.5.0 have a bug that prevents Pyxis from finding running containers. This is fixed in Enroot 4.0.1 (shipped with SUNK v7.x).
