# Handle Slurm signals for graceful shutdown

Source: https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals

# Handle Slurm signals for graceful shutdown

> Trap Slurm termination signals to checkpoint training jobs and report an accurate run status instead of a crash

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

A signal handler in your training code lets a job save a checkpoint and report an accurate status before Slurm forcibly stops it. By default, most training scripts ignore Slurm's termination signals, so when a job is canceled, hits its time limit, or is preempted, the process is killed mid-step. Two things go wrong: you lose the progress made since the last checkpoint, and your experiment tracker records the run as `crashed`, which is indistinguishable from a real failure.

This guide shows you how Slurm terminates a job, how to trap the termination signal in your training code to checkpoint and exit cleanly, and how to report a deliberate cancellation or preemption so it doesn't look like a crash.

## How Slurm terminates a job

When Slurm stops a running job, it doesn't kill the process immediately. It sends a sequence of signals with a grace period in between, which is the window your code uses to shut down cleanly.

When you cancel a job with [`scancel`](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job) (without the `--signal` option), Slurm does the following:

1. Sends `SIGCONT` to all job steps to ensure they're running.
2. Sends `SIGTERM` to request a graceful shutdown.
3. Waits for the number of seconds set by `KillWait` in `slurm.conf`.
4. Sends `SIGKILL`, which the process can't catch, to force termination.

The same `SIGCONT`-`SIGTERM`-`SIGKILL` signal sequence also applies when a job reaches its time limit, with the same `KillWait` interval between `SIGTERM` and `SIGKILL`. Preemption uses the same signals, but the grace window is set by the partition's or QOS's `GraceTime` (which defaults to `0`) and then by `KillWait` after that window closes. On SUNK, [`KillWait`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) defaults to 30 seconds, so on cancellation or a time limit your handler has roughly 30 seconds to save a checkpoint and exit before `SIGKILL` arrives. Confirm the value for your cluster, because a large checkpoint may need a longer window.

> [!NOTE]
>
> `SIGKILL` can't be trapped, ignored, or delayed. Any checkpointing or cleanup must finish within the `KillWait` window after `SIGTERM`.

### Request an earlier warning with `--signal`

If `KillWait` is too short to write your checkpoint, request an advance signal with the [`--signal`](https://slurm.schedmd.com/sbatch.html#OPT_signal) directive. Slurm sends the signal a set number of seconds before the job's time limit, giving you more time than `KillWait` alone:

```bash theme={"system"}
#SBATCH --signal=B:SIGTERM@120
```

* `B:` sends the signal to the batch script's shell only. Omit `B:` to signal the job steps (the processes started by `srun`) instead.
* `@120` requests the signal 120 seconds before the time limit. Because of Slurm's event-handling resolution, the signal can arrive up to 60 seconds earlier than requested, so treat the interval as a minimum.

`--signal` fires relative to the job's time limit. A `scancel` still follows the `KillWait` window described earlier.

## Prerequisites

Before you start, you must have the following:

* A training script that supports checkpointing, so it can resume from a saved state.
* A writable, shared checkpoint location that every node in the job can reach, such as [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) or a shared filesystem. To set up a shared filesystem, see [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md) or [Configure storage mounts on SUNK Self-Service](https://docs.coreweave.com/products/sunk/manage_sunk/configure-storage-mounts.md).
* A working SUNK cluster where you can [submit training jobs](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md).

## Add a signal handler to your training code

Register a handler for `SIGTERM` in your training process. The handler sets a flag that the training loop checks between steps, so the process checkpoints at a safe point rather than in the middle of an operation.

The following example shows the pattern for a PyTorch training loop. Replace `[CHECKPOINT-PATH]` with your checkpoint location.

```python title="train.py" theme={"system"}
import signal
import sys
import torch

# Flag set by the signal handler and checked by the training loop.
stop_requested = False

def handle_sigterm(signum, frame):
    global stop_requested
    print("Received SIGTERM. Will checkpoint and exit at the next safe point.", flush=True)
    stop_requested = True

signal.signal(signal.SIGTERM, handle_sigterm)

def save_checkpoint(model, optimizer, step):
    torch.save(
        {
            "step": step,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        "[CHECKPOINT-PATH]",
    )
    print(f"Checkpoint saved at step {step}.", flush=True)

def train(model, optimizer, dataloader):
    for step, batch in enumerate(dataloader):
        # ... run one training step ...

        if stop_requested:
            save_checkpoint(model, optimizer, step)
            sys.exit(0)
```

With this handler registered, your process saves a checkpoint and exits cleanly when Slurm sends `SIGTERM`, instead of being killed mid-step. Checkpointing between steps keeps the saved state consistent. Checkpoint frequently enough during normal training that a forced `SIGKILL` never costs more work than you're willing to lose.

> [!WARNING]
>
> Handle only `SIGTERM` for graceful shutdown. `SIGKILL` can't be caught, and trapping signals such as `SIGINT` can interfere with interactive debugging.

## Report the run status to your experiment tracker

Catching `SIGTERM` prevents lost progress, but it doesn't by itself fix how the run appears in your experiment tracker. This section uses [Weights & Biases](https://docs.coreweave.com/forge-home.md) as the example, because it's a common cause of the "canceled job looks crashed" scenario.

W\&B marks a run's final state from the process exit:

| Situation | What your code does | Resulting run state |
| - | - | - |
| No signal handling | Process is killed. `run.finish()` is never called | `crashed` |
| Deliberate cancellation | `run.finish(exit_code=0)` | `finished` |
| Preemption (resumable) | `run.mark_preempting()` then `run.finish(exit_code=1)` | `preempted` |

If the process is killed before it calls `run.finish()`, W\&B only detects that the run stopped sending heartbeats and marks it `crashed`. That's why an unhandled `scancel` looks identical to a real failure.

Extend the signal handler to finish the run cleanly. No arbitrary custom state such as `canceled` exists, so add a tag if you want to distinguish a user cancellation from a normal completion in the UI. Replace `[PROJECT-NAME]` with your W\&B project name.

```python title="train.py (Weights & Biases)" theme={"system"}
import signal
import sys
import wandb

run = wandb.init(project="[PROJECT-NAME]")
stop_requested = False

def handle_sigterm(signum, frame):
    global stop_requested
    stop_requested = True

signal.signal(signal.SIGTERM, handle_sigterm)

def shutdown(model, optimizer, step, preempted=False):
    save_checkpoint(model, optimizer, step)  # your checkpoint function
    if preempted:
        # Report a resumable preemption. Weights & Biases records the run as "preempted".
        run.mark_preempting()
        run.finish(exit_code=1)
        sys.exit(1)
    else:
        # Report a deliberate cancellation. Weights & Biases records the run as "finished".
        run.tags = tuple(set((run.tags or ()) + ("canceled",)))
        run.finish(exit_code=0)
        sys.exit(0)
```

Choose the branch that matches your workflow:

* Use the cancellation branch when a user stops a job that is not meant to resume. The run shows as `finished` with your `canceled` tag rather than `crashed`.
* Use the preemption branch for resumable or preemptible jobs. The run shows as `preempted`, which keeps preemption distinct from both crashes and successful completions.

> [!WARNING]
>
> Even with a handler, the run can still end up `crashed` if the shutdown is too abrupt for `run.finish()` to complete and sync. Keep the `KillWait` window (or your `--signal` lead time) large enough for both the checkpoint write and the final sync.

## Forward the signal from the batch script

When your training process is the job step, as in `srun python train.py`, let Slurm signal the step directly by requesting the advance warning without `B:`:

```bash theme={"system"}
#SBATCH --signal=SIGTERM@120
```

`slurmstepd` then sends a catchable `SIGTERM` straight to your Python process, and the handler from the previous section runs. No forwarding is needed.

You only need to forward the signal yourself when the training process is not the direct job step, for example when a launcher wraps it and doesn't propagate signals. In that case, don't forward `SIGTERM` through `srun`: `srun` forwards `SIGTERM` (along with `SIGQUIT` and `SIGHUP`) to its tasks as `SIGKILL`, which your code can't catch. Forward a user-defined signal instead, which `srun` passes through unchanged, and trap that same signal in your training code:

```bash title="train.sbatch" theme={"system"}
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --signal=B:SIGUSR1@120

# srun escalates SIGTERM to SIGKILL, so forward SIGUSR1, which srun passes through unchanged.
_forward_signal() {
    echo "Forwarding SIGUSR1 to the training step."
    kill -USR1 "${SRUN_PID}"
    wait "${SRUN_PID}"
}
trap _forward_signal SIGUSR1

srun python train.py &
SRUN_PID=$!
wait "${SRUN_PID}"
```

In this case, register the handler in your training code for the signal you forward (`signal.SIGUSR1`) rather than `SIGTERM`. The `wait` calls are important. Without them, the batch script exits as soon as it receives the signal, and Slurm kills the training step before it can checkpoint.

## Result

With signal handling in place, compare how the same interruption looks:

* **Without handling:** the process dies at `SIGKILL`, the last steps of progress are lost, and the run is recorded as `crashed`, indistinguishable from a genuine failure.
* **With handling:** the process saves a checkpoint within the grace window, exits cleanly, and the run is recorded as `finished` (with a `canceled` tag) or `preempted`, accurately reflecting what happened.

## Related

* [Checkpoint and restart Slurm jobs after a node failure](https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart.md): resume from checkpoint after a hardware-triggered restart, instead of a graceful shutdown.
* [Submit a training job with PyTorch or TensorFlow](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md): submit the jobs you're instrumenting here.
* [Slurm parameters reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md#slurmConfig): the `KillWait` setting that defines the grace window.
* [scancel documentation](https://slurm.schedmd.com/scancel.html): the signal sequence Slurm uses to cancel a job.
* [Python signal module](https://docs.python.org/3/library/signal.html): reference and examples for handling signals in Python.
* [Weights and Biases signal handling for sweeps](https://docs.coreweave.com/products/wandb/sweeps/signal-handling-sweep-runs.md): how W\&B maps exit codes and preemption signals to run states, including automatic requeue for sweep agents.
