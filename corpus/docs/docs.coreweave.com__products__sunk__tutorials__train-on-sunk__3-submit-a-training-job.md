# 3. Submit a training job with PyTorch or TensorFlow

Source: https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job

# 3. Submit a training job with PyTorch or TensorFlow

> Submit multi-node, multi-GPU distributed training jobs using PyTorch torchrun on Slurm

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

In this section, you submit a training job to Slurm using the PyTorch `torchrun` utility. This step builds on [the previous section](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job.md) by introducing a multi-node, multi-GPU job that more closely exemplifies a real-world distributed training scenario. By the end, you've submitted a PyTorch training job across multiple nodes and GPUs, and you understand how the equivalent workflow differs for TensorFlow.

This section helps you understand how to use Slurm with PyTorch or TensorFlow.

## Submit a training job using PyTorch

Use the [`torchrun` launcher](https://docs.pytorch.org/docs/stable/elastic/run.html#launcher-api) to schedule a multi-node, multi-GPU [PyTorch](https://pytorch.org) job on Slurm. The `torchrun` launcher is a superset of the launch utility from the [`torch.distributed`](https://docs.pytorch.org/docs/stable/distributed.html#) package, which provides PyTorch support and communication primitives for multi-process parallelism across multiple GPUs running on one or more nodes.

> [!NOTE]
>
> The directives for Slurm and the parameters for `torchrun` can be confused with one another. To keep them straight, remember this distinction:
>
> * Slurm **allocates the nodes** to be used for PyTorch.
> * `torchrun` **spawns the jobs** within a single node.

## Example using PyTorch

The following annotated example script shows a multi-node distributed training job using PyTorch. The goal is to define the allocation and ensure that the `srun` command runs once on each node. Replace `[USERNAME]` with your username.

```bash theme={"system"}
#!/bin/bash

#SBATCH --job-name=pytorch_test
#SBATCH --nodes=2
#SBATCH --gres=gpu:8
#SBATCH --ntasks-per-node=1
#SBATCH --time=20:00
#SBATCH --exclusive

# Activate the Python virtual environment
source /mnt/home/[USERNAME]/test_env/bin/activate

# Set NCCL debugging and the network interface
export NCCL_DEBUG=INFO
export OMP_NUM_THREADS=1

# Set the RDZV_HOST variable to the hostname
export RDZV_HOST=$(hostname)

# Generate a reasonably unique number for the communication port.
export RDZV_PORT=$(expr 10000 + $(echo -n $SLURM_JOB_ID | tail -c 4))

echo "running on host $RDZV_HOST using port $RDZV_PORT"

echo "Starting job"
date
hostname

# Start the PyTorch Process
srun python3 \
    -m torch.distributed.run \
    --rdzv-id=$SLURM_JOB_ID \
    --rdzv-backend=c10d \
    --rdzv-endpoint="$RDZV_HOST:$RDZV_PORT" \
    --nnodes=2 \
    --nproc-per-node=8 \
    /mnt/home/[USERNAME]/tnet2/tnet2/train_c3_cw.py

echo "Calculation complete"

echo "Ending job"
date
```

The following annotated version of the script shows the same code:

```bash title="Example script with annotations" theme={"system"}
#!/bin/bash

#SBATCH --job-name=pytorch_test
#SBATCH --nodes=2
#SBATCH --gres=gpu:8
#SBATCH --ntasks-per-node=1 # Critical configuration. Sets 1 torchrun call per node.
#SBATCH --time=20:00
#SBATCH --exclusive

# Activate the Python virtual environment
source /mnt/home/[USERNAME]/test_env/bin/activate

# Set NCCL debugging and the network interface
export NCCL_DEBUG=INFO
# Environment variables used by PyTorch.
# These `export` commands are executed by the shell on the primary compute node
# before the `srun` command is executed, so the variables are only set once.
export OMP_NUM_THREADS=1

# Set the RDZV_HOST variable to the hostname
export RDZV_HOST=$(hostname) # RDZV_HOST is the hostname of the primary compute node.

# Generate a reasonably unique number for the communication port.
# RDZV_PORT is created to be a unique port name for PyTorch to use.
# Using the Slurm job ID (`$SLURM_JOB_ID`) as part of the port number reduces the chance
# of a job clash, should more than one job be running on the same node.
export RDZV_PORT=$(expr 10000 + $(echo -n $SLURM_JOB_ID | tail -c 4))

echo "running on host $RDZV_HOST using port $RDZV_PORT"

echo "Starting job"
date
hostname

# Start the PyTorch Process
srun python3 \
# Invoking `python -m torch.distributed.run` is equivalent to invoking `torchrun`.
# Torchrun should be invoked using the same arguments on each node that is
# participating in the training run. This srun command is run once on each
# node in the allocation by Slurm. In this example, it is run twice, using
# the same parameters. The host that is named in `--rdzv-endpoint` opens a
# port to listen from the other host.
    -m torch.distributed.run \
    --rdzv-id=$SLURM_JOB_ID \
    --rdzv-backend=c10d \
    # The Rendezvous Backend in PyTorch (parameters beginning with `--rdzv-`)
    # coordinates how distributed workers find one another before beginning a
    # distributed training job.
    --rdzv-endpoint="$RDZV_HOST:$RDZV_PORT" \
    --nnodes=2 \
    --nproc-per-node=8 \
    /mnt/home/[USERNAME]/tnet2/tnet2/train_c3_cw.py

echo "Calculation complete"

echo "Ending job"
date
```

Most of these parameters are similar to those used in [the previous section](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job.md), with a few notable exceptions:

* `#SBATCH --ntasks-per-node=1`: This `sbatch` parameter is **important** when running multi-GPU PyTorch jobs with Slurm.
  * Slurm manages nodes, and `torchrun` manages what runs on them. If you omit this line, the default number of tasks per node is `1`.
  * However, setting this number higher might cause problems. As a best practice in this configuration, explicitly set the number of tasks to `1`, as shown here.
  * For most other applications, set this number to the total number of desired tasks per node.
* `export OMP_NUM_THREADS=1`: An environment variable that sets the number of threads that run within an OpenMP job.
  * Here, it's set to `1` explicitly.
  * If you don't set it, PyTorch relies on OpenMP's default behavior, which may use as many threads as there are physical cores.
  * Explicitly setting this parameter avoids accidentally launching more threads than there are processors on a node.

> [!NOTE]
>
> Invoking `python -m torch.distributed.run`, as the preceding script does, is equivalent to invoking `torchrun`. Invoke `torchrun` using the same arguments on each node that participates in the training run, which the preceding script ensures.

### Rendezvous backend

The [Rendezvous Backend in PyTorch](https://docs.pytorch.org/docs/stable/elastic/run.html#launcher-api) coordinates how distributed workers find one another before beginning a distributed training job.

As specified in [the Rendezvous Backend documentation](https://docs.pytorch.org/docs/stable/elastic/run.html#note-on-rendezvous-backend), multi-node training requires the following parameters:

* `--rdzv-id`: A unique job ID, shared by all nodes participating in the job.
* `--rdzv-backend`: An implementation of the [`torch.distributed.elastic.rendezvous.RendezvousHandler`](https://docs.pytorch.org/docs/stable/elastic/rendezvous.html#torch.distributed.elastic.rendezvous.RendezvousHandler) interface.
* `--rdzv-endpoint`: The endpoint where the rendezvous backend runs, usually in `host:port` format.

The preceding script implements these parameters as follows:

```text title="Rendezvous parameters" theme={"system"}
    --rdzv-id=$SLURM_JOB_ID \
    --rdzv-backend=c10d \
    --rdzv-endpoint="$RDZV_HOST:$RDZV_PORT" \
```

In this case, the `--rdzv-backend` is the `c10d` backend, the `--rdzv-endpoint` is set to the `$RDZV_HOST:$RDZV_PORT` combination generated earlier in the script, and the `--rdzv-id` is set to `$SLURM_JOB_ID`, which is a single unique identifier for the entire job and is the same on both nodes.

The following backends are supported without additional setup:

* `c10d` (recommended)
* `etcd-v2` and `etcd` (legacy)

> [!NOTE]
>
> To use `etcd-v2` or `etcd`, set up an etcd server with the `v2` API enabled using the `--enable-v2` parameter.

### Launch the job in a container

To launch the same job inside a container, use a similar script with a few key differences:

* Don't use a virtual environment.
* A container already has the right components installed and configured, so the script doesn't need to handle these installations.
* The `srun` command specifies the container by targeting its squash file.

Replace `[USERNAME]` with your username.

```bash title="Example srun using a container" theme={"system"}
srun --container-image=/mnt/home/[USERNAME]/nightly-torch.sqsh \
    --container-mounts=/mnt/home:/mnt/home \
    --no-container-remap-root
```

You can load this container image from a shared filesystem or pull it from a registry.

> [!NOTE]
>
> Inside an Enroot or Pyxis container, `/tmp` is backed by `tmpfs` (RAM), not the Node's local NVMe. Writing large amounts of temporary data to `/tmp` can fill memory and cause `ENOSPC` errors even when disk metrics look clean. To keep temporary files on NVMe, set `TMPDIR` to an NVMe-backed path. For details, see [Node-local storage and `/tmp` on Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/node-local-storage-and-tmp).
>
> The `--no-container-remap-root` flag makes file ownership match the submitting user. It doesn't grant real root. For details, see [Why do sudo, chown, and chmod fail inside a Pyxis container?](https://docs.coreweave.com/support/sunk/articles/why-do-permission-errors-occur-in-pyxis-enroot-containers).

> [!NOTE]
>
> For more information about developing containers, see [Pull and modify a container using Slurm](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster.md#pull-and-modify-a-container-using-slurm) in the previous section.

## TensorFlow launch utilities with Slurm

If you use TensorFlow instead of PyTorch, the launch workflow differs. With TensorFlow, some of the logic from the Slurm script moves into the Python code.

> [!WARNING]
>
> The following examples aren't full Python code for TensorFlow and don't run as presented. They are for example purposes only.

```python theme={"system"}
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

tf.keras.backend.clear_session()
slurm_resolver = tf.distribute.cluster_resolver.SlurmClusterResolver(port_base=15000)
communication = tf.distribute.experimental.CommunicationImplementation.NCCL
mirrored_strategy = tf.distribute.MultiWorkerMirroredStrategy( \
    cluster_resolver=slurm_resolver, communication_options=communication)
with mirrored_strategy.scope():
    inputs = keras.Input(shape=(392,), name='img')
    x = layers.Dense(32, activation='relu')(inputs)
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(6)(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name='name')
    model.compile(.......) # model options here

# x_test and y_test hold test data
# Load x_train and y_train

history = model.fit(x_train, y_train,
                    batch_size=32,
                    epochs=5,
                    validation_split=0.2)
test_scores = model.evaluate(x_test, y_test, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])
```

To launch this job, use the following Slurm script. Replace `[USERNAME]` with your username.

```bash theme={"system"}
#!/bin/bash
#SBATCH --job-name=name     # job name
#SBATCH --nodes=2           # number of nodes
#SBATCH --ntasks-per-node=1 # number of MPI task per node
#SBATCH --gres=gpu:8        # number of GPUs per node
#SBATCH --cpus-per-task=32  # experiment to get the best value
#SBATCH --time=00:20:00     # job length
#SBATCH --output=%x_%j.out  # std out filename
#SBATCH --error=%x_%j.out   # std err filename
#SBATCH --exclusive         # use entire machine

# Activate the python virtual environment
source /mnt/home/[USERNAME]/test_env/bin/activate

# Set NCCL debugging and network interface

export NCCL_DEBUG=INFO
export OMP_NUM_THREADS=1

echo "Starting job"
date
hostname

# Start Python Process
srun python example.py

echo "Calculation complete"

echo "Ending job"
date
```

After you submit a job to Slurm, it's visible [through Grafana](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/4-monitor-jobs.md) and from the command line. In the next section, you monitor running jobs using these methods.
