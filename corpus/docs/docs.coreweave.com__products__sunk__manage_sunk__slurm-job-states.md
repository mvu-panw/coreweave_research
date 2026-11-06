# Monitor Slurm job states

Source: https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states

# Monitor Slurm job states

> View real-time and historic information about Slurm jobs

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Slurm job states track the lifecycle of a specific workload initiated by a user in the cluster. This page explains how to monitor those job states so that you can confirm a workload is progressing as expected, diagnose why a job is waiting, or review the resource usage of a job that's already finished.

Slurm job states are distinct from [Slurm node states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md), which describe the availability and health of the hardware used to support the Slurm cluster.

[CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md#sunk) includes dashboards for tracking metrics related to job performance and resource usage within your SUNK cluster.

Slurm also provides commands for tracking job states and steps. The following sections describe when to use each one:

| Command | Data type | Purpose |
| - | - | - |
| `squeue` | Real-time | Overview of jobs in queue or currently running |
| `scontrol` | Real-time | Detailed, live metadata about a specific job |
| `sacct` | Historic | Accounting and history; resource usage of completed jobs |

> [!TIP]
>
> Run all Slurm commands, including `squeue`, `scontrol`, and `sacct`, from within the Slurm login Pod shell.

## View a summary of current jobs with `squeue`

Use the `squeue` command to view real-time status information about Slurm jobs and job steps. `squeue` provides an overview of jobs currently running or in queue. For more detailed real-time information about a particular job, use `scontrol`.

Run the `squeue` command by itself to display the status of every active job in the system:

```bash theme={"system"}
squeue
```

To filter for specific information, add flags to the `squeue` command. The following examples show common filters.

To display details about a specific job, use the `-j` flag. Replace `[JOB-ID]` with the value from the `JOBID` column for that job:

```bash theme={"system"}
squeue -j [JOB-ID]
```

To view information about jobs in a specific state, use `squeue` with the `-t` flag. Enter [Slurm job state codes](#slurm-job-state-codes) as a comma-separated list.

```bash theme={"system"}
squeue -t [STATE]
```

To view jobs started by a specific user, use the `-u` flag:

```bash theme={"system"}
squeue -u [USERNAME]
```

By default, `squeue` may omit job steps to keep the output concise. To display job steps with `squeue`, use the `-s` flag:

```bash theme={"system"}
squeue -s
```

### Determine the reason a job is `PENDING`

Running a Slurm job is a request for resource allocation, not an instantaneous execution. Until the requested resources are available, the job remains in a `PENDING` state. This is expected behavior and is part of the Slurm job lifecycle.

The `squeue` command includes a `REASON` column that provides insight into why a job is in a given state.

The following table lists common `PENDING` reasons. For a full decision tree that walks each reason from symptom to action, see [Troubleshoot a `PENDING` job](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending).

| Listed reason | Meaning |
| - | - |
| `Resources` | The cluster doesn't currently have the resources available to execute the job. The job runs when resources free up. |
| `Priority` | Higher-priority jobs are ahead of this job in the queue. When they complete or free resources, this job runs. |
| `ReqNodeNotAvail` | A node the job requires (by name, feature, or reservation) is currently unavailable, for example, drained or down. Run `sinfo -R` to list unavailable nodes. |
| `BeginTime` | The job has a future start time set with `--begin`. It runs at that time. |
| `Reservation` | The job targets a Slurm reservation that hasn't started yet, or is excluded from one. Check `scontrol show reservation`. |
| `AssocGrpGRES` | The job's accounting association has reached its group limit on a generic resource, most often GPUs. Wait for other jobs to release GPUs, or request fewer. |
| `AssocGrpCpuLimit` | The job's association has reached its group CPU limit. Wait, or request fewer CPUs. |
| `QOSMaxJobsPerUserLimit` | The job's QoS limits how many jobs one user can run at once, and you're at the limit. |
| `BadConstraints` | No node can satisfy the `--constraint` expression. List features with `sinfo -o "%P %f"` and fix the constraint. |
| `PartitionConfig` | The request exceeds a static partition limit, such as node count or memory per node. Compare against `scontrol show partition`. |
| `Dependency` | The `--dependency` flag is in use, and the job it waits on hasn't yet reached the required state. |
| `JobHeldUser` | You placed the job on hold with `scontrol hold`. Release it with `scontrol release [JOB-ID]`. |
| `JobHeldAdmin` | An administrator placed the job on hold. Contact them before releasing. |
| `JobArrayTaskLimit` | You have reached the maximum number of simultaneously running tasks allowed for a single job array. |

See [Troubleshoot a `PENDING` job](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending) for these situations:

* Idle nodes that won't run the job.
* Partition or feature mismatches.
* The `Requested node configuration is not available` message.

> [!NOTE]
>
> Running `squeue` sends a remote procedure call to `slurmctld`. To avoid overloading the Slurm Controller and impacting performance, limit `squeue` calls to the minimum necessary.

## View detailed information about a specific Slurm job with `scontrol`

The `scontrol` command provides a more detailed view about a particular job, compared to the summary offered by `squeue`. Like `squeue`, `scontrol` displays live, real-time data, and you can configure it to display job steps.

To view detailed information about a specific job, use `scontrol show job` with the relevant `[JOB-ID]`:

```bash theme={"system"}
scontrol show job [JOB-ID]
```

To view granular details about a specific job step, use `scontrol show step` with the relevant `[JOB-ID]` and `[STEP-ID]`:

```bash theme={"system"}
scontrol show step [JOB-ID].[STEP-ID]
```

## View information about completed Slurm jobs with `sacct`

To view information about completed jobs, including job steps and resource usage, use the `sacct` command. Unlike `squeue` and `scontrol`, `sacct` displays data about jobs that aren't currently running or in queue. The output of `sacct` displays job steps by default.

For a comprehensive view of job steps for a given job, use the `sacct` command with the `-j` flag. Replace `[JOB-ID]` with the job ID returned at submission or the value in the `sacct` job row's `JobID` column:

```bash theme={"system"}
sacct -j [JOB-ID]
```

Add the `--showsteps` flag to the preceding command to explicitly list individual steps in the output:

```bash theme={"system"}
sacct -j [JOB-ID] --showsteps
```

Use the `--format` flag with `sacct` to format the output in a more readable manner:

```bash theme={"system"}
sacct --format=JobID,JobName,State,ExitCode
```

## Slurm job state codes

Use this reference to interpret the state codes that appear in the output of the preceding commands. Slurm job states are designated by codes, which appear in the `STATE` or `ST` columns of the `squeue` or `sacct` command output.

| Job state | Shorthand | Meaning |
| - | - | - |
| `PENDING` | `PD` | The job is waiting for resource allocation. Use `squeue` to [view the reason the job is in this state](#determine-the-reason-a-job-is-pending), or see [Troubleshoot a `PENDING` job](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending). |
| `RUNNING` | `R` | The job has an allocation of nodes and is currently executing job steps. |
| `CONFIGURING` | `CF` | Resources have been allocated, but the nodes are still being configured. |
| `COMPLETING` | `CG` | The job is finishing. Cleanup scripts are executing and nodes are returning to the nodepool. |
| `COMPLETED` | `CD` | The job finished successfully with an exit code of `0`. |
| `FAILED` | `F` | The job terminated with a failure condition, or non-zero exit code. |
| `TIMEOUT` | `TO` | The job terminated after reaching its requested time limit. |
| `NODE_FAIL` | `NF` | The job terminated after one or more of the nodes running it crashed or became unresponsive. Slurm requeues the job automatically; to make it resume from checkpoint instead of restarting from scratch, see [Checkpoint and restart Slurm jobs after a node failure](https://docs.coreweave.com/products/sunk/run_workloads/checkpoint-and-restart.md). |
| `PREEMPTED` | `PR` | The job was removed from its allocated nodes to make room for a higher-priority job. |
