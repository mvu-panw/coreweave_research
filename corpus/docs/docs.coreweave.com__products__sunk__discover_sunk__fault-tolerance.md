# Fault tolerance in SUNK

Source: https://docs.coreweave.com/products/sunk/discover_sunk/fault-tolerance

# Fault tolerance in SUNK

> How CoreWeave removes failing Nodes and how Slurm requeue restarts your SUNK jobs after a failure

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Long training jobs on SUNK run across many GPUs for days, so hardware failures during a job are expected. Two layers handle them. CoreWeave automation detects failing hardware and takes the Node out of production. Slurm requeue returns a failed job to the queue, so it restarts on healthy nodes without anyone resubmitting it. This page explains what each layer does, which failures your job has to handle itself, and how to configure requeue for application errors.

For the step-by-step setup of a requeueable job that resumes from a checkpoint, see [Checkpoint and restart Slurm jobs after a node failure](https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart.md).

## How CoreWeave takes failing Nodes out of production

CoreWeave's Node lifecycle automation monitors the Nodes in your cluster during [Day 2+ operations](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md). When it detects a problem, it moves the Node through a lifecycle state transition, such as a reboot or a move to triage. The type of transition depends on how severe the problem is known to be. For the full model, see [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md).

In SUNK, each Slurm compute node runs as a `slurmd` Pod on one Kubernetes Node, so a transition on the Kubernetes Node reaches Slurm. When CoreWeave cordons the Node, the [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) drains the matching Slurm node, so Slurm schedules no new jobs on it. The drain reason starts with `k8s: cordon:` while the `slurmd` Pod is running, and with `k8s: pod terminated: cordon:` after the Pod is gone. See [Kubernetes drain reasons](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#kubernetes-drain-reasons).

CoreWeave uses two types of transition, immediate and pending, and each affects a running job differently. The following sections describe each type.

### Immediate transitions

CoreWeave uses an immediate transition when the problem is known to be fatal or to severely degrade performance, such as a confirmed hardware fault or thermal throttling. The Node leaves production immediately, and CoreWeave Kubernetes Service (CKS) evicts its Pods, including the `slurmd` Pod. The job running on that node fails, and Slurm requeue brings it back.

### Pending transitions

CoreWeave uses a pending transition when the severity is uncertain and stopping a running job would cost more than waiting. CKS cordons the Node, the Slurm node drains, and the job already running there keeps running. The transition waits until the Node is idle, however long the job takes, and then CoreWeave reboots the Node or moves it to triage. A Node that goes to triage leaves your cluster, and CKS delivers a replacement that joins Slurm as a new node.

This design assumes that a serious fault crashes the job on its own. When it does, the job fails, the Node goes idle, and the transition proceeds.

> [!NOTE]
>
> Don't undrain a node that carries a `k8s:` drain reason. Most of these nodes return to production on their own once the repair finishes. For how long a repair takes and which drain reasons you need to act on, see [Drain and undrain Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#how-long-to-wait-for-a-kubernetes-repair).

## What happens to the job after a node failure

When the node running a job fails, Slurm marks the node `DOWN` and ends the job in the `NODE_FAIL` state. SUNK doesn't change Slurm's `JobRequeue` default. Unless a cluster administrator sets `JobRequeue=0`, a batch job is eligible for requeue after a node failure without any extra configuration. Slurm returns the job to the queue and restarts the batch script from the beginning under the same job ID.

A restart from the beginning loses all progress unless your job saves checkpoints and resumes from the latest one. [Checkpoint and restart Slurm jobs after a node failure](https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart.md) covers `--requeue`, detecting a restart with `SLURM_RESTART_COUNT`, and where to store checkpoints.

## Requeue on application exit codes

Node-failure requeue doesn't cover a job that fails because your application exited with an error. Examples include an out-of-memory error or an NVIDIA Collective Communications Library (NCCL) timeout inside your program. Slurm treats a job that fails this way as a normal job failure and doesn't requeue it, even with `--requeue` set.

To requeue on application errors, set `RequeueExit` in the Slurm configuration. It lists the batch job exit codes that should send a job back to the queue. It takes a comma-separated list of single codes and hyphenated ranges, for example `1-9,18`. `RequeueExitHold` takes the same format, but it holds the requeued job until someone releases it with `scontrol release`. The hold gives you a chance to inspect the failure first. Both are cluster-wide settings, and they apply only to jobs that Slurm can requeue, so a job submitted with `--no-requeue` isn't requeued on these codes. See [`RequeueExit`](https://slurm.schedmd.com/slurm.conf.html#OPT_RequeueExit) in the Slurm documentation.

Replace `[EXIT-CODES]` with the exit codes your application uses for recoverable failures:

> [tab] SUNK Standard
>
> Add the key under `slurmConfig` in the `slurm` chart's values:
>
> ```yaml theme={"system"}
> slurmConfig:
>   RequeueExit: "[EXIT-CODES]"
> ```

> [tab] SUNK Self-Service
>
> Add the key under `spec.slurmConfig` in your `SunkCluster` manifest. For the field, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#top-level-spec-fields).
>
> ```yaml theme={"system"}
> spec:
>   slurmConfig:
>     RequeueExit: "[EXIT-CODES]"
> ```

Slurm matches the exit code of the batch script, not of each task. If `srun` is the last command in your script, the script exits with the `srun` exit code. Otherwise, save the code and end the script with `exit` and that code.

Choose codes that separate a recoverable failure from a bug. A job that exits with a listed code every time requeues every time. To stop this loop, check `SLURM_RESTART_COUNT` at the start of the script and, once it passes your limit, exit with a code that isn't in the list.

## End a step when one rank fails

In a distributed job, one rank can exit, for example from an out-of-memory error, while the other ranks keep waiting on a collective operation that never completes. The job then holds its GPUs without making progress until a timeout fires. The `srun` flag `--kill-on-bad-exit=1` ends every task in the step as soon as any task exits with a nonzero code. As a result, the job fails quickly and requeue can take over:

```bash theme={"system"}
srun --kill-on-bad-exit=1 python train.py
```

The flag has a cost if your job uses Pyxis containers. When it ends the step, Slurm stops the remaining tasks with `SIGTERM`, waits `KillWait` seconds, and then sends `SIGKILL`. That shutdown can interrupt Pyxis while it removes its container directory, and the next attempt can then fail with `pyxis: ERROR File already exists`. If you use the flag with Pyxis, give each attempt a unique container name or clean up in an Epilog. See [Why does Pyxis report File already exists after a job is preempted?](https://docs.coreweave.com/support/sunk/articles/why-does-pyxis-report-file-already-exists-after-preemption)

## Check the requeue history of a job

To see each run of a requeued job, including the run that failed, query the accounting database with `sacct --duplicates`. Replace `[JOB-ID]` with the job ID returned at submission or the value in the `sacct` job row's `JobID` column:

```bash theme={"system"}
sacct -j [JOB-ID] --duplicates --format=JobID,JobName,State,ExitCode,Start,End,NodeList
```

A job requeued after a node failure shows a run in the `NODE_FAIL` state followed by a later run. To see how many times Slurm has restarted a job, run `scontrol show job [JOB-ID]` and read the `Restarts` field.

Run these commands from a login node when you need them. Don't poll them from inside a batch script. Repeated `scontrol` calls add load to the Slurm controller, and repeated `sacct` calls add load to the accounting database.

## Related topics

* [Checkpoint and restart Slurm jobs after a node failure](https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart.md): make a job requeueable and resume it from a checkpoint.
* [Handle Slurm signals for graceful shutdown](https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals.md): save state and exit cleanly on `scancel`, a time limit, or preemption.
* [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md): pending and immediate transitions, and the Node states they move through.
* [Drain and undrain Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md): drain reasons and when a node returns to service.
* [Monitor Slurm node states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md): node states including `DOWN` and `DRAINED`.
* [Introduction to GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md): find GPUs that slow a job without crashing it.
