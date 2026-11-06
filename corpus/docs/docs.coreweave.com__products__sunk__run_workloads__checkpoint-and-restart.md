# Checkpoint and restart Slurm jobs after a node failure

Source: https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart

# Checkpoint and restart Slurm jobs after a node failure

> Configure a Slurm job on SUNK to automatically requeue and resume from checkpoint after a node failure

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

When the node running a Slurm job on SUNK fails, for example from a hardware fault, Slurm requeues the job and restarts the batch script from the beginning. Without a checkpoint to resume from, this means losing all progress made before the failure. This guide shows you how to make a Slurm job checkpoint-aware. It becomes explicit about being requeued, able to detect that it was restarted, and able to resume from its last saved state instead of starting over.

This guide covers hardware-triggered restarts: a job that requeues because the node running it failed. For user-initiated or scheduler-initiated stops, such as `scancel`, a job hitting its time limit, or preemption, see [Handle Slurm signals for graceful shutdown](https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals.md).

## How SUNK handles a node failure

When a node running a Slurm job stops responding, Slurm marks that node [`DOWN`](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states#slurm-node-states) and terminates the job with a [`NODE_FAIL`](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states#slurm-job-state-codes) state.

SUNK doesn't override Slurm's cluster-wide `JobRequeue` setting, which defaults to `1`. This means jobs are eligible for requeue after a node failure without any special configuration. Slurm returns the job to the queue and, once resources are available, restarts the batch script from the beginning using the same job ID. The job's output and error files, and its accounting record, continue under that same ID.

This automatic requeue is [documented Slurm behavior](https://slurm.schedmd.com/sbatch.html), not a CoreWeave customization. A cluster administrator can require jobs to opt in explicitly by setting `JobRequeue=0`. If requeue behavior on your cluster doesn't match what's described here, check that setting with your cluster administrator.

## Prerequisites

Before you start, you must have the following:

* A training script that already checkpoints its own state, for example by periodically calling `torch.save()`. This guide assumes your framework can save and load a checkpoint. It doesn't cover how to implement checkpointing itself.
* A writable, shared checkpoint location that every node in the job can reach, such as [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) or a shared filesystem. To set up a shared filesystem, see [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md) or [Configure storage mounts on SUNK Self-Service](https://docs.coreweave.com/products/sunk/manage_sunk/configure-storage-mounts.md).
* A working SUNK cluster where you can [submit training jobs](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md).

## Make your job explicitly requeueable

Add `--requeue` to your `sbatch` script to make the job's requeue eligibility explicit, regardless of the cluster's `JobRequeue` default:

```bash theme={"system"}
#SBATCH --requeue
```

Pair it with `--open-mode=append` so a requeued run appends to the existing output and error files instead of truncating them. Slurm's default open mode is `truncate`, so without this flag a node failure erases your job's logs from before the failure:

```bash theme={"system"}
#SBATCH --open-mode=append
```

This flag governs the output and error files only. Any training progress made since the last checkpoint is lost to the failure itself, which is what the checkpoint interval controls.

> [!WARNING]
>
> `--no-requeue` disables all automatic recovery for a job, including recovery from a node failure. Don't set it on a long-running training job unless you want a node failure to end the job permanently.

## Detect a requeue and resume from checkpoint

Slurm sets `SLURM_RESTART_COUNT` in the batch script's environment whenever it restarts a job, whether from a node failure or an explicit requeue. The variable is unset on the job's first run. After a requeue, it holds the number of times the job has restarted.

Check this variable at the start of your job script to decide whether to resume from a checkpoint or start fresh:

```bash title="train.sbatch" theme={"system"}
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --requeue
#SBATCH --open-mode=append
#SBATCH --nodes=2
#SBATCH --gres=gpu:8

if [ "${SLURM_RESTART_COUNT:-0}" -gt 0 ]; then
    echo "Restart number ${SLURM_RESTART_COUNT}. Resuming from checkpoint."
    RESUME_ARGS="--resume-from-checkpoint"
else
    echo "First run. Starting from scratch."
    RESUME_ARGS=""
fi

srun python3 train.py $RESUME_ARGS
```

Your training code then determines which checkpoint to load. Point it at a stable identifier, such as the job ID (`$SLURM_JOB_ID`) or a fixed "latest" path, rather than a value derived from wall-clock time. A checkpoint path built from the current date, for example, silently points at a new location after midnight. A job that restarts across a day boundary then can't find the checkpoint it wrote before the restart.

When more than one process in a job restores from the same checkpoint, have a single process, conventionally rank 0, read it and broadcast the result to the other ranks. Letting every rank read the same object at once collapses read throughput. Rank-0-read-then-broadcast is the standard pattern for distributed training at scale, not a workaround.

## Choose a checkpoint interval

Balance checkpoint frequency against two costs: the time and I/O each checkpoint write costs the job, and the training progress you lose if a node fails between checkpoints. Time a single checkpoint write for your job, decide how much recomputation you can tolerate after a failure, and set the interval so the write cost stays a small fraction of the work it protects. Large multi-node jobs, such as those running on [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md), write bigger checkpoints, so the write cost weighs more heavily.

Design long-running jobs to treat a node failure as a normal, recoverable event rather than an exception. On NVL72 racks specifically, if more than two nodes become unavailable, CoreWeave cordons and drains the entire rack. See [Deploy NVL72-powered instances as full racks](https://docs.coreweave.com/platform/instances/nvl72.md#deploy-nvl72-powered-instances-as-full-racks) for that policy.

## Store checkpoints in CoreWeave AI Object Storage

[Object Storage](https://docs.coreweave.com/products/storage/object-storage.md), accessed through [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md), is the recommended location to store checkpoints. A requeued job can land on a different set of nodes than the original run, so checkpoints need to be reachable from every node in the job:

* **Object Storage** is durable and reachable from any node in the cluster. This means a checkpoint written by one set of nodes is available to a different set of nodes after a requeue.
* **LOTA** caches recently accessed objects on local node disks. Re-reading a large checkpoint after a restart doesn't require a full round trip to the storage backend every time.

Avoid [node-local storage](https://docs.coreweave.com/products/sunk/manage_sunk/node-local-storage-and-tmp.md), such as `/tmp` or NVMe scratch space, for checkpoints. A failed node's local storage isn't recoverable, and a requeued job isn't guaranteed to return to the same node. A [shared filesystem PVC](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md) also works, but sizing it to hold checkpoints for large models adds an operational cost that Object Storage avoids.

## Example: `sbatch` script with checkpoint and resume

The following example combines the patterns from this guide into a complete template. Replace `[BUCKET-NAME]` with your Object Storage bucket name and `[INTERVAL-MINUTES]` with the checkpoint interval you chose, then adapt the `train.py` flags to match your own training script.

```bash title="train.sbatch" theme={"system"}
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --requeue
#SBATCH --open-mode=append
#SBATCH --nodes=2
#SBATCH --gres=gpu:8
#SBATCH --ntasks-per-node=1
#SBATCH --time=8:00:00

CHECKPOINT_URI="s3://[BUCKET-NAME]/checkpoints/${SLURM_JOB_ID}"

if [ "${SLURM_RESTART_COUNT:-0}" -gt 0 ]; then
    echo "Restart number ${SLURM_RESTART_COUNT}. Resuming from ${CHECKPOINT_URI}."
    RESUME_ARGS="--resume-from ${CHECKPOINT_URI}"
else
    echo "First run. Starting from scratch."
    RESUME_ARGS=""
fi

srun python3 train.py \
    --checkpoint-uri "${CHECKPOINT_URI}" \
    --checkpoint-interval-minutes [INTERVAL-MINUTES] \
    $RESUME_ARGS
```

This example assumes `train.py` accepts `--checkpoint-uri`, `--checkpoint-interval-minutes`, and `--resume-from`, and implements the matching save and load logic.

Submit this script the same way you'd submit any other job. If a node failure interrupts the run, Slurm requeues it automatically. The restart check at the top of the script then resumes training from the last checkpoint in Object Storage instead of starting over.

## Related

* [Fault tolerance in SUNK](https://docs.coreweave.com/products/sunk/discover_sunk/fault-tolerance.md): how CoreWeave takes failing Nodes out of production, and how to requeue a job on application exit codes.
* [Handle Slurm signals for graceful shutdown](https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals.md): checkpoint and exit cleanly on `scancel`, a time limit, or preemption, instead of a node failure.
* [Monitor Slurm job states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states.md#slurm-job-state-codes): the `NODE_FAIL` state a job enters when its node fails.
* [About NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md): the rack-level node-failure tolerance policy for NVL72 systems.
* [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md): segment sizing for NVL72 racks, including the recommended `--segment` maximum.
* [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md): how LOTA accelerates repeated reads of the same object.
* [`sbatch` documentation](https://slurm.schedmd.com/sbatch.html): the canonical reference for `--requeue`, `--open-mode`, and `SLURM_RESTART_COUNT`.
