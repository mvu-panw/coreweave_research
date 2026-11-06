# Run notebooks on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/notebooks-on-sunk

# Run notebooks on SUNK

> Run interactive marimo and Jupyter notebooks on SUNK clusters with GPU resources

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Interactive notebooks provide an environment for data exploration, model development, and visualization on SUNK. This guide covers running notebooks on SUNK's Slurm-managed clusters for both interactive development and batch job execution.

Consider using notebooks on SUNK if:

* You need an interactive environment for data exploration or model prototyping.
* You want to iterate quickly on code while using GPU resources.
* You need to visualize results during development before running full batch jobs.

This guide uses [marimo](https://github.com/marimo-team/marimo) as the primary example. marimo notebooks are pure Python scripts that run both interactively and as batch jobs. The same port forwarding and container techniques also work for [Jupyter notebooks](https://jupyter-notebook.readthedocs.io/en/stable/).

## Prerequisites

Before completing the steps in this guide, be sure you have the following:

* Access to a SUNK cluster with permissions to submit jobs.
* Familiarity with Slurm commands, such as `srun`, `sbatch`, and `squeue`.
* A shared directory for storing notebooks, such as `/mnt/data` or your home directory.

## Install marimo

You can install marimo within a container or conda environment. The recommended approach uses containers for reproducibility.

### Use containers

To create a container with marimo installed, pull a base Python container and save it as a squash file.

1. From the login node, pull a Python container and install marimo:

   ```bash theme={"system"}
   srun --container-image=python:3.11-slim \
          --container-remap-root --container-mounts=/mnt/home:/mnt/home \
          --container-save ${HOME}/marimo.sqsh --pty bash -i
   ```

2. Within the container, install marimo:

   ```bash theme={"system"}
   pip install marimo # and other packages like torch, jax, and others
   ```

3. Exit the container to save it. The container is available at `${HOME}/marimo.sqsh`.

For more information about working with containers on SUNK, see the [SUNK Training guide](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster.md#install-software-as-containers-using-pyxis-and-enroot).

### Use conda

Alternatively, you can create a conda environment with marimo:

```bash theme={"system"}
conda create --name marimo-env python=3.11 pip
conda activate marimo-env
pip install marimo
```

## Interactive development

The following sections describe how to run marimo as an interactive session on a compute node so you can develop notebooks in your browser while the workload runs on Slurm-managed GPU resources.

For interactive notebook development, you can run marimo in headless mode and connect through port forwarding.

### Submit an interactive job

Create a script named `run_marimo.sh`:

```bash theme={"system"}
#!/bin/bash
#SBATCH --job-name=marimo
#SBATCH --output=marimo-%j.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16GB
#SBATCH --time=4:00:00

# Activate your environment (choose one)
# Option 1: Using conda
# eval "$(conda shell.bash hook)"
# conda activate marimo-env

# Option 2: Using container (add --container flags to srun below)

# Start marimo in headless mode
python -m marimo edit /mnt/home/${USER}/notebook.py --headless --host 0.0.0.0 --port 3000
```

Submit the job:

```bash theme={"system"}
sbatch run_marimo.sh
```

### Connect through port forwarding

1. Find your compute node using `squeue`:

   ```bash theme={"system"}
   squeue -u $USER
   ```

   You should see output similar to:

   ```text theme={"system"}
   JOBID  PARTITION  NAME    USER       ST  TIME   NODES  NODELIST(REASON)
   1234   h100       marimo  user_name  R   0:30   1      slurm-h100-231-147
   ```

2. Establish an SSH tunnel from your local machine to the compute node through the login node:

   ```bash theme={"system"}
   ssh -L 3000:slurm-h100-231-147:3000 username@login-node
   ```

   Replace `slurm-h100-231-147` with your actual compute node name.

3. Access the marimo interface at `http://localhost:3000` in your web browser.

### Use containers for interactive sessions

To run marimo interactively within a container:

```bash theme={"system"}
srun -p h100 --exclusive \
       --container-image=${HOME}/marimo.sqsh \
       --container-mounts=/mnt/home:/mnt/home \
       --pty bash -c "python -m marimo edit /mnt/home/${USER}/notebook.py --headless --host 0.0.0.0 --port 3000"
```

## Batch job execution

Once a notebook works interactively, you can run it unattended as a batch job. This is useful for longer training runs or for parameter sweeps that don't require a live UI.

marimo notebooks can run as batch jobs using command-line arguments through `mo.cli_args()`.

### Create a notebook for batch execution

Create a marimo notebook that accepts command-line arguments:

```python theme={"system"}
import marimo
...
app = marimo.App()

with app.setup:
    import marimo as mo

def _():
    # Access command-line arguments
    args = mo.cli_args()
    learning_rate = float(args.get("learning-rate", 0.01))
    epochs = int(args.get("epochs", 100))
    print(f"Training with learning_rate={learning_rate}, epochs={epochs}")

# Your training code here
...

if __name__ == "__main__":
    app.run()

```

### Submit as a batch job

Create a batch script `batch_notebook.sh`:

```bash theme={"system"}
#!/bin/bash
#SBATCH --job-name=marimo-batch
#SBATCH --output=marimo-batch-%j.out
#SBATCH --cpus-per-task=8
#SBATCH --mem=32GB
#SBATCH --time=2:00:00

eval "$(conda shell.bash hook)"
conda activate marimo-env

python /mnt/home/${USER}/notebook.py -- --learning-rate 0.01 --epochs 100
```

Submit the job:

```bash theme={"system"}
sbatch batch_notebook.sh
```

## GPU configuration

The preceding examples request only CPU and memory. To accelerate notebook workloads with GPUs, request them through Slurm by adding GPU resources to your SBATCH directives:

```bash theme={"system"}
#!/bin/bash
#SBATCH --job-name=marimo-gpu
#SBATCH --output=marimo-gpu-%j.out
#SBATCH --partition=h100
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64GB
#SBATCH --time=4:00:00

eval "$(conda shell.bash hook)"
conda activate marimo-env

python -m marimo edit /mnt/home/${USER}/gpu_notebook.py --headless --host 0.0.0.0 --port 3000
```

For multi-GPU workloads:

```bash theme={"system"}
#SBATCH --gpus-per-task=8
#SBATCH --exclusive
```

## VS Code integration

You can use notebooks with [VS Code tunnels on SUNK](https://docs.coreweave.com/products/sunk/access_sunk/vs-code-with-slurm.md) for a more integrated development experience.
After setting up a VS Code tunnel to your compute node, install the marimo [VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) or use Jupyter notebooks directly within VS Code.
