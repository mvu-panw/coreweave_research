# 2. Submit a simple job to the cluster

Source: https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job

# 2. Submit a simple job to the cluster

> Prepare and submit a basic Slurm batch job script with SBATCH directives and environment variables

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This part of the SUNK training tutorial walks you through preparing a basic Slurm batch job script, submitting it to the cluster, monitoring its progress, and inspecting its output. By the end, you'll be familiar with the core Slurm commands (`sbatch`, `squeue`, `scancel`, `sacct`, and `sinfo`) that you'll use throughout the rest of the tutorial series to run real training workloads on SUNK.

## Prepare the job script

The most common approach to running jobs on Slurm is to submit job scripts to Slurm. Scripts typically consist of three sections:

1. **Directives:** Slurm directives begin with `#SBATCH`. These directives specify which resources and settings Slurm uses to run the script.
2. **Environment variables:** Environment variables are the variables your application requires to run. In this section, load modules and set up environment variables such as `$PATH` and `$LD_LIBRARY_PATH`.
3. **Code:** The actual code that runs your application.

The following example shows a basic Slurm job script, which sets Slurm directives using [sbatch](https://slurm.schedmd.com/sbatch.html), then calls a Python program:

```bash theme={"system"}
#!/bin/bash

# SBATCH directives
#SBATCH --job-name=my_job # The name of your job
#SBATCH --output=my_job.out # The output file location of your job
#SBATCH --error=my_job.err # The error file location of your job
#SBATCH --time=01:00:00 # The maximum time your job can run. In this case, 1 hour
#SBATCH --nodes=1 # The number of nodes to use
#SBATCH --ntasks-per-node=1 # The number of tasks to run per node
#SBATCH --gres=gpu:1 # The number of GPUs to use

# Export environment variables
export VARIABLE1="variable_1"

echo "Starting job"
date
hostname

echo "Running calculation..."

# In this section, your application is called.
# For example, to run a Python script called `myprog.py`:
python3 /home/username/myprog.py

echo "Calculation complete"

echo "Ending job"
date
```

### Sbatch directives

Use `#SBATCH` directives to configure the job submission. Each directive specifies a different aspect of the job, such as its name, output files, time limits, and resource requirements. The following table summarizes some common directives:

| Directive | Description |
| - | - |
| `#SBATCH --job-name=` | Sets the name of the job. Useful for locating it in status reports later |
| `#SBATCH --output=` | Specifies the output file for standard output. You can use a full path, or one relative to the submission directory |
| `#SBATCH --error=` | Specifies the output file for standard error |
| `#SBATCH --time=` | Sets the time limit for the job. In the preceding example, 1 hour. If the job is still running after the specified duration, the job is stopped |
| `#SBATCH --nodes=` | How many nodes the job should request. In the preceding example, 1 node |
| `#SBATCH --ntasks-per-node=` | How many tasks per node this job should request. In the preceding example, 1 task per node |
| `#SBATCH --gres=gpu:` | How many GPUs this task should request. In the preceding example, 1 GPU |

## Submit the job

With the job script prepared, you're ready to hand it off to the Slurm scheduler so it can be queued and run on the cluster.

Submit your job to the Slurm queue by running the script using `sbatch`. This command submits the `my_job_script.sh` script to the Slurm scheduler, and Slurm allocates resources to run your job based on the sbatch directives in the script. If resources matching these directives are available, the job may start immediately. Otherwise, it waits in a queue until other jobs finish.

```bash title="Example command" theme={"system"}
sbatch my_job_script.sh
```

After job submission, Slurm returns a job ID. In this example, the job ID is `371`. Keep this job ID. You'll use it to check status, cancel the job, or look up results later.

```text title="Example output" theme={"system"}
Submitted batch job 371
```

## Check the job status

Once a job is submitted, you'll want to know whether it's still queued, running, or already finished. Slurm exposes that information through the `squeue` command.

To check the status of your job, use the `squeue` command. The `squeue` command shows the status of all jobs in the cluster. To see a specific job, target the job ID from the submission command. In this example, where the job ID is `371`, locate the job by running `squeue 371`.

You can also target jobs by the person who submitted them, identified by username, by running `squeue -u myname`.

Running `squeue` without any arguments shows all jobs in the queue, including their status, time running, and the nodes they are running on.

```bash theme={"system"}
squeue
```

You should see output similar to the following:

```text theme={"system"}
JOBID PARTITION     NAME     USER   ST      TIME  NODES   NODELIST(REASON)
371        h100     my_job   user1  R       2:01      1   h100-208-101
372        h100     calc     user2  R       1:38      1   h100-208-153
363        h100     calc2    user3  R       1:25      1   h100-208-153
```

| Job state | Explanation |
| - | - |
| `PD` | Job is pending. The Nodelist(reason) column details why. |
| `R` | Job is running. The Nodelist(reason) column shows which nodes the job uses. |
| `CG/CD` | Job has completed or is completing. |
| `F` | The job has failed. |
| `TO` | Because of a time out, Slurm terminated the job. The time limit is usually specified in the job script or partition configuration. |

> [!NOTE]
>
> For more detailed metrics on your job, view your job in the [Slurm Job Metrics Grafana dashboard](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md).

## Cancel the job

If you submit a job in error or no longer need its results, you can stop it from running (or remove it from the queue) so it doesn't consume cluster resources.

To cancel your job, use the `scancel` command.

```bash theme={"system"}
scancel 371
```

If your job is pending, Slurm removes it from the queue. If your job is running, Slurm stops it.

## View job output

After your job finishes, you'll typically want to inspect what it produced and check for any errors.

Slurm collects standard output and error output in the files specified by the sbatch directives in the job script. After your job completes, you can view the output in these files.

> [!TIP]
>
> Use a text editor to view these files, since their contents may be lengthy.

> [!NOTE]
>
> An empty output file doesn't always mean a stalled job. When standard output is redirected to a file instead of a terminal, Python and most other language runtimes buffer it in blocks rather than lines, and write to the file only when a buffer fills or the program exits. A healthy, still-running job can show a 0-byte or stale `.out` file for a long time.
>
> To see output in near real time, set `export PYTHONUNBUFFERED=1` in your job script, run your program with `python3 -u`, or add `flush=True` to individual `print()` calls. To confirm whether a running job is making progress, check its GPU and filesystem activity in Grafana, as described in [Monitor jobs with Grafana](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/4-monitor-jobs.md), rather than relying on the size of the output file.

## View cluster information

Before submitting more jobs, it's often useful to understand what nodes and partitions are available, and which are already busy.

To view more details about your cluster, use the `sinfo` command.

```bash title="Example command" theme={"system"}
sinfo
```

This example output displays information on a small cluster that consists of 3 nodes. The output includes the partition name, availability, time limit, number of nodes, state, and node list.

```text title="Example output" theme={"system"}
PARTITION      AVAIL  TIMELIMIT  NODES  STATE NODELIST
h100              up   infinite      1    mix h100-208-101
h100              up   infinite      1   idle h100-208-[101,103,125]
h100              up   infinite      1  alloc h100-208-153
```

### Node states

| Status | Description |
| - | - |
| `idle` | Nodes are idle |
| `alloc` | Nodes are fully allocated to jobs |
| `mix` | Nodes are running jobs, but still have some available space |

## View completed job history

Because `squeue` only shows recent jobs, you'll need a different command to look up history for jobs that have already completed or failed.

The `squeue` command only shows job status while jobs are in a pending or running state, and for a few hours after completion. To see the status of a completed or failed job, use the `sacct` command instead.

```bash title="Example command" theme={"system"}
sacct
```

In this example output, the selected job completed successfully. The output shows the states of this simple job in three parts:

```text title="Example output" theme={"system"}
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode
------------ ---------- ---------- ---------- ---------- ---------- --------
371              my_job       h100       root          1  COMPLETED      0:0
371.batch         batch                  root          1  COMPLETED      0:0
371.0        all_reduc+                  root          1  COMPLETED      0:0
```

1. The line with a `JobID` of `371` and a `JobName` of `my_job` displays the state of the entire job.
2. The line prefaced with a `JobID` of `371.batch` and a `JobName` of `batch` displays the state of the submitted script.
3. The final line, with a `JobID` of `371.0` and a `JobName` of `all_reduc+`, displays the status of one of the tests CoreWeave runs after each job to confirm the cluster performs correctly. The test typically takes a few seconds to run.

> [!TIP]
>
> Busy clusters may contain thousands of jobs. It can be helpful to restrict the output to a specific time range or user, for example:
>
> To see jobs only from a specific user:
>
> ```bash title="Example command" theme={"system"}
> sacct --user=user1
> ```
>
> To see jobs from a specific time range:
>
> ```bash title="Example command" theme={"system"}
> sacct --starttime=2025-03-24T06:10 --endtime=2025-03-24T07:20
> ```
>
> The `--starttime` option displays only jobs that have begun *after* the given start time. The `--endtime` option displays only jobs that have ended *before* the given end time. Specify all times in ISO format.
