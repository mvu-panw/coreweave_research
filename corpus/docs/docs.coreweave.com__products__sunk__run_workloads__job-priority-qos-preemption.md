# Job priority, QoS, and preemption

Source: https://docs.coreweave.com/products/sunk/run_workloads/job-priority-qos-preemption

# Job priority, QoS, and preemption

> On SUNK, priority weights and preemption start unset; understand the model before you tune it

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

On CoreWeave SUNK, priority and preemption work exactly as they do in upstream Slurm. SUNK's default Slurm configuration sets no `PriorityWeight*` values and no `PreemptType`, so a new cluster has flat priority and no preemption until an administrator configures them.

If you submit jobs, you can inspect priority, request a QoS your account is authorized for, and set a time limit. Changing priority weights, preemption settings, or QoS definitions requires cluster-admin access, and each section that describes one says so.

If your job sits `PENDING`, start with [Why is my Slurm job stuck in PENDING?](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending), which maps every `REASON` code to a next step. Return here when you need to understand why ordering is flat, how preemption is scoped, or why backfill never evaluates your job.

## Symptoms

A job sits `PENDING` with `Reason=Priority` or `Reason=Resources` while other jobs run, or a running job gets preempted and seems to vacate slowly. This page explains the scheduling model behind those outcomes.

## How Slurm priority works on SUNK

Slurm uses a multifactor priority formula to order `PENDING` jobs:

```text theme={"system"}
Priority = sum over factors of (Weight_factor * Factor_value)
```

The factors include job age (how long the job has waited), fairshare (your account's historical resource use), QoS, partition tier, and job size. Each factor has a configurable weight (`PriorityWeightAge`, `PriorityWeightFairshare`, `PriorityWeightQOS`, `PriorityWeightPartition`, `PriorityWeightJobSize`).

Every `PriorityWeight*` factor defaults to `0` in Slurm, and SUNK's default Slurm configuration doesn't set any of them. The multifactor plugin is still running, because `PriorityType` defaults to `priority/multifactor`. Every job scores the same, so Slurm falls through to its remaining tie-breaks: jobs that can preempt, jobs with an advanced reservation, partition `PriorityTier`, job priority, submit time, then job ID. In practice that means submission order.

The weights are `slurm.conf` settings, so changing them requires cluster-admin access. If an administrator sets only `PriorityWeightQOS` to a non-zero value, QoS becomes the only factor that changes the order.

QoS priority and preemption are separate concerns. `PriorityWeightQOS` affects which `PENDING` jobs get resources first. It doesn't control which running jobs get preempted. The `Preempt` field on each QoS controls preemption, as described in [Preemption on SUNK](#preemption-on-sunk).

For accounting setup that feeds fairshare and priority, see [How do I set up Slurm accounting for priority scheduling?](https://docs.coreweave.com/support/sunk/articles/how-do-i-set-up-slurm-accounting-for-priority-scheduling).

## Inspect priorities

Use these read-only commands from a login Pod to see why a job has the priority it does. Replace `[JOB-ID]` with the value from the `JOBID` column in `squeue` output for the job you want to inspect.

```bash theme={"system"}
# Show the priority breakdown for queued jobs. Read the factor columns to see
# which factor dominates. Safe to run anytime; read-only.
sprio -l
```

```bash theme={"system"}
# Show a single job's Priority, Reason, StartTime, and Scheduler. Safe; read-only.
scontrol show job [JOB-ID]
```

```bash theme={"system"}
# Show queued jobs with priority and QoS columns. Safe; read-only.
squeue -o '%i %j %u %P %Q %q %T %M %l %D %R'
```

In the `squeue` output, the `%Q` (priority) and `%q` (QoS) columns tell you how a job ranks and which QoS it uses.

```bash theme={"system"}
# Show configured QoS levels, their priority, and their preempt relationships.
# Safe to run anytime; read-only.
sacctmgr show qos format=Name,Priority,Preempt,PreemptMode,MaxTRESPerUser
```

```bash theme={"system"}
# Show your fairshare values. A FairShare near 0 means low priority when
# fairshare is a weighted factor. Safe; read-only.
sshare -u [USERNAME]
```

## Preemption on SUNK

Preemption lets a higher-priority job reclaim resources from a lower-priority job. Changing `PreemptType`, `PreemptMode`, or QoS `Preempt` fields requires cluster-admin access.

`PreemptType` selects the plugin that decides what can preempt what. Slurm leaves it unset by default and SUNK's default Slurm configuration doesn't set it either, so preemption is off until an administrator picks a plugin:

* `preempt/qos`: QoS definitions control which QoS can preempt which others. A QoS can preempt another only if the other QoS appears in its `Preempt` field.
* `preempt/partition_prio`: partition `PriorityTier` controls preemption. Jobs in a higher `PriorityTier` partition may preempt jobs in a lower one. This is independent of `PriorityWeightPartition`, so preemption can work even when scheduling priority weights are zero.

`PreemptMode` selects what happens to the preempted job:

* `OFF`: no preemption. This is the default, and it's compatible only with preemption disabled cluster-wide.
* `CANCEL`: Slurm cancels the preempted job.
* `REQUEUE`: Slurm returns the preempted job to the queue to run again later. The job must be eligible for requeue. `JobRequeue` defaults to `1`, and SUNK doesn't change it, so a batch job is eligible unless it was submitted with `--no-requeue` or the cluster sets `JobRequeue=0`. Design the job to be safe to re-run from a checkpoint.
* `SUSPEND`: Slurm suspends the preempted job in place.

Slurm honors a per-partition `PreemptMode` only under `PreemptType=preempt/partition_prio`. Under `PreemptType=preempt/qos` it reads `PreemptMode` from the QoS instead, so `PreemptMode=OFF` on a partition does nothing to stop QoS-driven preemption there. See [`PreemptMode`](https://slurm.schedmd.com/slurm.conf.html#OPT_PreemptMode) in the `slurm.conf` reference. That mismatch is the usual reason a partition you believe is preemption-free still loses jobs. Check the plugin first, then the partition and QoS settings:

```bash theme={"system"}
# Check which preemption plugin is active. Safe; read-only.
scontrol show config | grep -E 'PreemptType|PreemptMode'

# Check a partition's effective PreemptMode. Safe; read-only.
scontrol show partition [PARTITION] | grep PreemptMode

# Check PreemptMode per QoS, which governs under preempt/qos. Safe; read-only.
sacctmgr show qos format=Name,Priority,Preempt,PreemptMode
```

Setting `PreemptMode=OFF` on a QoS doesn't protect it either. For a QoS, `OFF` doesn't disable preemption. It clears the QoS-specific setting, so the QoS falls back to the cluster-wide `PreemptMode`, the same as the default value `CLUSTER`. Jobs in a QoS are only safe from preemption when no other QoS lists that QoS in its `Preempt` field, so an administrator has to remove it from all of them. To check, run `sacctmgr show qos` and make sure no other QoS lists it in the `Preempt` column. For details, see [`PreemptMode`](https://slurm.schedmd.com/sacctmgr.html#OPT_PreemptMode) in the `sacctmgr` reference.

For background on `GANG` preemption and other modes, see the [Slurm preemption documentation](https://slurm.schedmd.com/preempt.html). SUNK doesn't add product-specific behavior to those modes.

## Why a preempted job vacates slowly

Two settings govern the gap between "Slurm selected this job for preemption" and "its nodes are free." Both are cluster-admin settings.

`GraceTime` is the preemption grace window. Slurm moves the job's end time to now plus `GraceTime` and sends `SIGCONT` and `SIGTERM` right away as notice. Partitions and QoS levels each carry their own value, both default to `0`, and each has a condition: a partition's `GraceTime` applies only under `PreemptType=preempt/partition_prio`, and a QoS `GraceTime` applies only to `PreemptMode=CANCEL` and `PreemptMode=REQUEUE`.

`KillWait` governs the kill that follows. At the job's new end time Slurm sends `SIGCONT` and `SIGTERM`, waits `KillWait` seconds, then sends `SIGKILL`. On SUNK, [`KillWait`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) defaults to 30 seconds. A large `KillWait` makes working preemption look broken: the preempting job starts, and the preempted job sits in `COMPLETING` until the window closes.

```bash theme={"system"}
# Read the cluster's KillWait value. Safe; read-only.
scontrol show config | grep KillWait

# Read a partition's GraceTime. Safe; read-only.
scontrol show partition [PARTITION] | grep GraceTime
```

To vacate quickly under preemption, trap `SIGTERM` in your job and checkpoint and exit promptly. For the full signal sequence and a worked handler, see [Handle Slurm signals](https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals.md).

## Request a higher QoS

To request a higher-priority QoS at submission, if your account is authorized for it:

```bash theme={"system"}
sbatch --qos=[QOS-NAME] job_script.sh
```

If your job's priority is too low to ever schedule and you can't change weights, contact your cluster administrator. Raising priority weights, adjusting QoS priority values, or moving a job to an unpreemptible partition are administrator actions. For the upstream reference, see the [Slurm priority documentation](https://slurm.schedmd.com/priority_multifactor.html).

## Backfill starvation from a job with no time limit

The backfill scheduler fits lower-priority jobs into gaps before higher-priority jobs are ready. To do that, it predicts when running jobs finish, based on each job's `TimeLimit`. A job with an unlimited time limit has no predictable end time, so backfill can't plan around it. Lower-priority jobs behind it are never backfilled.

The signature of this problem is a job that stays `PENDING` even though nodes are idle:

```bash theme={"system"}
# Look for Reason=Priority with StartTime=Unknown and Scheduler=Main.
# That combination means backfill never evaluated the job. Safe; read-only.
scontrol show job [JOB-ID] | grep -E 'Reason|StartTime|Scheduler'
```

`StartTime=Unknown` with `Scheduler=Main` means only the main scheduler considers the job, and the main scheduler enforces strict priority order. The fix is to set an accurate `TimeLimit` on every job so backfill can plan:

```bash theme={"system"}
#SBATCH --time=04:00:00
```

This matters most for many same-priority single-node jobs, which rely on backfill to pack onto idle nodes.

## Common scenarios

The following scenarios show how priority and preemption interact in practice.

**Scavenger workloads.** A scavenger job uses a low-priority QoS that higher-priority QoS levels can preempt. It runs on otherwise idle resources and yields when higher-priority work arrives. This requires the higher-priority QoS levels to list the scavenger QoS in their `Preempt` field, which a cluster administrator sets with `sacctmgr`.

**Development versus production tiers.** Administrators commonly define a tier of QoS levels (for example, a production QoS that can't be preempted and a lower QoS for development jobs). The exact layout is cluster-specific. Use `sacctmgr show qos` to see what your cluster defines.

**Over-weighting QoS causes starvation.** When `PriorityWeightQOS` is the only non-zero weight and is set high, small differences in QoS priority values become large effective gaps. Lower-priority jobs can then sit `PENDING` with `Reason=Resources` even when nodes are idle. The fix is for a cluster administrator to balance the weights: reduce `PriorityWeightQOS`, adjust the relative spacing of QoS priority values, or enable other factors such as age and fairshare.

## When to file a support ticket

Open a ticket when scheduling behavior still doesn't match your configuration after you have confirmed the priority weights, QoS definitions, `PreemptType`, `PreemptMode`, `GraceTime`, and `KillWait`. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include the output of `scontrol show job [JOB-ID]`, `sprio -l`, `sacctmgr show qos`, and `scontrol show config | grep -E 'Priority|Preempt|KillWait'`, along with the partition's `GraceTime`.

## Related pages

* [Why is my Slurm job stuck in PENDING?](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending): each `REASON` code and the action it calls for.
* [Monitor Slurm job states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states.md): job state codes and `PENDING` reasons.
* [Handle Slurm signals](https://docs.coreweave.com/products/sunk/run_workloads/handle-slurm-signals.md): the `SIGCONT`-`SIGTERM`-`SIGKILL` sequence, `GraceTime`, and `KillWait`.
* [Set up Slurm accounting for priority scheduling](https://docs.coreweave.com/support/sunk/articles/how-do-i-set-up-slurm-accounting-for-priority-scheduling): accounting that feeds fairshare.
* [SUNK support articles](https://docs.coreweave.com/support/sunk.md): help for job, node, and training problems.
