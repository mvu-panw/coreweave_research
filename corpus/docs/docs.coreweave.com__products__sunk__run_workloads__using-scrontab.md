# Use scrontab to schedule recurring batch jobs

Source: https://docs.coreweave.com/products/sunk/run_workloads/using-scrontab

# Use scrontab to schedule recurring batch jobs

> Schedule recurring batch jobs in SUNK using scrontab, a cron-like Slurm utility for automated job submission

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page shows SUNK cluster administrators and users how to schedule recurring Slurm batch jobs with `scrontab`. Use `scrontab` when you need cron-style automation that integrates with Slurm's scheduler, resource allocation, and accounting.

`scrontab` is a utility for scheduling recurring Slurm batch jobs in a High-Performance Computing (HPC) Slurm cluster. It uses similar syntax to `cron`, but has additional functionality specific to Slurm, making it a suitable option for scheduling complex and resource-intensive jobs.

`scrontab` uses the `sbatch` mechanism to submit Slurm jobs at specified intervals, where they are then managed and executed by the Slurm workload manager. The Slurm workload manager dynamically allocates resources, queues jobs, and distributes jobs across the cluster.

## Preliminary steps

Before you can use `scrontab`, you must complete the following setup steps:

* Enable `scrontab` in the cluster by setting `ScronParameters: enable` under [`slurmConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) in the `slurm` chart values in SUNK Standard, or under `spec.slurmConfig` in the `SunkCluster` in SUNK Self-Service. See the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for a list of available parameters.
* Enable the ability to run additional syscalls required by `scrontab` by adding the "SYS\_ADMIN" security context capability. See the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).
* Connect to the login node. For detailed instructions, see [Connect to the Slurm Login Node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).
* Ensure that scripts intended to be used with `scrontab` are executable by running `chmod +x [SCRIPT]`.
* Ensure that scripts intended to be used with `scrontab` are in a shared location so that all compute nodes can access them.

## Edit the `scrontab` file

To edit the `scrontab` file, execute the following command:

```bash theme={"system"}
scrontab -e
```

If the `scrontab` file doesn't already exist, `scrontab -e` provides a default, unconfigured example for you to edit. You can then add `#SCRON` directives and scheduled job entries as described in the following sections.

## `scrontab` behavior and considerations

In the examples on this page, replace `[JOB-ID]` with the value from the `JOBID` column in `squeue` output for your scheduled job.

`scrontab` behaves differently than `cron` and `#SBATCH` directives in several ways. To ensure a smooth scheduling experience, remember the following concepts:

* Options set using `#SCRON` are reset after each `scrontab` entry.
* The entered times specify when a job **becomes eligible** to run. The actual execution time depends on Slurm's scheduler and resource availability.
* `#SCRON` directives configure the Slurm job when it is submitted. Thus, Slurm is likely to **ignore `#SBATCH` directives within the script itself**.
* When `scrontab` jobs are canceled, their **future executions are also canceled**. When you delete an entire `scrontab` file using `scrontab -r`, running jobs defined in that file complete but aren't rescheduled afterward.
* `scrontab` jobs retain their `JobID` across executions. If a job is still running when its next scheduled time arrives, **new instances aren't created**.
* Jobs can be rescheduled based on the times specified in the `scrontab` entries using `scontrol requeue [JOB-ID]`.
* The time specified in `scrontab` is relative to the **Slurm controller's timezone**, not your local time.

## Apply `#SCRON` directives

To apply `#SCRON` options to an entry, add a line beginning with `#SCRON` before the given entry. Options set with `#SCRON` apply only to the single following `crontab` entry.

```text title="Example scrontab directive" theme={"system"}
#SCRON --your-options
```

Most `#SBATCH` directives are also available to use as `#SCRON` directives. For a complete list of options, see [SchedMD's `sbatch` documentation](https://slurm.schedmd.com/sbatch.html).

> [!WARNING]
>
> Options set using `#SCRON` are reset after each `scrontab` entry.

These are some example options that are frequently useful:

* `#SCRON --chdir=[DIR]` sets the directory where the job runs.
* `#SCRON --time=[TIME]` sets the time limit for the job.
* `#SCRON --output=[FILE]` sets the file location for capturing `stdout` and `stderr` outputs. The default location for these is `/root/slurm-[JOB-ID].out`.

> [!WARNING]
>
> `#SCRON` directives configure the Slurm job when it is submitted. Because of this, Slurm treats the `#SBATCH` directives defined within the running script as user environment variables and ignores them.

## Scheduling

> [!NOTE]
>
> The entered time specifies when a job becomes eligible to run. The actual execution time depends on Slurm's scheduler and resource availability.

The format for defining the time and date is the same as in `cron`. Times are defined in one line, using five fields to define the minute, hour, day of month, month, and day of week respectively.

The format is as follows:

```text title="Example scrontab directive" theme={"system"}
#SCRON --optional-sbatch-directives
[MINUTE] [HOUR] [DAY-OF-MONTH] [MONTH] [DAY-OF-WEEK] /path/to/script.sh
```

> [!WARNING]
>
> The time specified in `scrontab` is relative to the Slurm controller's timezone.

Set the values for each field according to the following tables:

| Field | Values |
| - | - |
| `[MINUTE]` | `(0-59)` |
| `[HOUR]` | `(0-23)` |
| `[DAY-OF-MONTH]` | `(1-31)` |
| `[MONTH]` | `1-12` or `Jan-Dec` |
| `[DAY-OF-WEEK]` | `(0-7)` where `0` and `7` are Sunday |

Also, you may use special characters to control scheduling behavior:

| Special character | Name | Behavior |
| - | - | - |
| `*` | Wildcard | Matches all values for that field |
| `,` | Comma | Specifies a list of values |
| `-` | Hyphen | Specifies a range of values |
| `/` | Slash | Specifies step values |

The [Examples](#examples) section demonstrates the syntax for some common scheduling patterns.

`scrontab` also includes aliases for common settings. For example, the `@hourly` alias schedules a job to become eligible at the first minute of each hour. For more examples, see [SchedMD's `scrontab` documentation](https://slurm.schedmd.com/scrontab.html#SECTION_SCRONTAB-OPTIONS).

### Rescheduling

To skip the next run of a `cron` job and reschedule it for the next available time, use `scontrol requeue`, as shown in the following example:

```bash theme={"system"}
scontrol requeue [JOB-ID]
```

> [!WARNING]
>
> `scrontab` assigns a single job ID to all occurrences of a given job. Thus, canceling one run of a job also cancels all future runs of the job, and the definition of the canceled job is commented out in the user's `scrontab` file.

## Examples

The following sections describe examples of `scrontab` scheduling options and demonstrate how they fit with `#SCRON` directives.

### Record timestamped job statistics

The following code block records data for selected jobs every other hour, and saves the log files to a specified location:

```text title="Example scrontab directive" theme={"system"}
# Save data on specific jobs every other hour.
#SCRON --job-name "log_jobs"
0 */2 * * * sacct --jobs=[JOB-ID-LIST] --format=JobID,AllocCPUS,ConsumedEnergy,NTasks > /logs/jobs/$(date +\%Y\%m\%d-\%H\%M).log
```

The following sections examine each element of this code block in detail.

#### `#SCRON` directives

This command begins with a `#SCRON` directive:

```text title="Example #SCRON directive" theme={"system"}
#SCRON --job-name "log_jobs"
```

`--job-name` specifies the name for the Slurm job. In this example, the job is named `"log_jobs"`. This name appears in Slurm's account systems, including `sacct` and `squeue`, making it easier to track and identify.

#### Scheduling

Next, the command specifies the scheduling behavior of this job:

```text title="Example scheduling syntax" theme={"system"}
0 */2 * * *
```

A value of `0` in the `[MINUTE]` field specifies that the job should run exactly on the hour.

A value of `*/2` in the `[HOUR]` field specifies that this executes every other hour. `*` indicates "every hour", but adding `/2` indicates "every 2nd occurrence". Thus, every other hour.

The `*` in the `[DAY-OF-MONTH]`, `[MONTH]`, and `[DAY-OF-WEEK]` fields specify that this job runs every day of every month.

#### Slurm command

After the scheduling specifications comes the actual command to run as a Slurm job. This example uses `sacct`. The `sacct` command is a Slurm CLI utility that provides detailed information about past jobs, including resource usage, status, and more.

```bash title="Example Slurm command with options" theme={"system"}
sacct --jobs=[JOB-ID-LIST] --format=JobID,AllocCPUS,ConsumedEnergy,NTasks
```

The `--jobs=[JOB-ID-LIST]` option for `sacct` specifies the job to retrieve information about. Replace `[JOB-ID-LIST]` with the job IDs you want to query. You can either list specific job IDs or provide a range of job IDs.

> [!TIP]
>
> To list specific jobs, use a comma-separated list, such as `--jobs=123,456,789`.
>
> To target a range of jobs, specify the beginning and end of the range and place a `-` between them, such as `--jobs=123-789`.

The `--format=` option specifies what fields of information you want `sacct` to provide for each job. The names of these fields correspond with column names.

This example uses `--format=` to direct `sacct` to return the following information:

| Field | Content |
| - | - |
| `JobID` | The unique identifier for the job. |
| `AllocCPUS` | The number of CPUs allocated to the specified job. |
| `ConsumedEnergy` | The amount of energy consumed by the job, in Joules. To see this metric, you must have energy accounting enabled in your Slurm configuration. |
| `NTasks` | The number of tasks, or processes, within the job. |

#### Save the logs to a specified location

To save the requested logs to a specified location, use `>` to redirect the output of `sacct` to a specified directory and use the `date` command to create a logfile with the current date and time.

```bash title="Example logfile" theme={"system"}
sacct --jobs=[JOB-ID-LIST] --format=JobID,AllocCPUS,ConsumedEnergy,NTasks > /logs/jobs/$(date +\%Y\%m\%d-\%H\%M).log
```

The following table defines the options used to generate the filename:

| Option | Format |
| - | - |
| `%Y` | Displays the full year. |
| `%m` | Displays the month, `(01-12)` |
| `%d` | Day of the month, `(01-31)` |
| `%H` | Hour, `(00-23)` |
| `%M` | Minute, `(00-59)` |
| `\` | An escape character, used before the `%`, to prevent `scrontab` from reading `%` as a newline character. |
| `.log` | The file extension. |

If this job ran at 16:00 (4:00 PM) on June 26, 2025, the filename is `/logs/jobs/20250626-1600.log`.

### Use time shortcuts and additional `sbatch` options

```text theme={"system"}
# Run a 30-minute job daily at 4:00 PM with a minimum of two nodes, and save the stdout and stderr
# outputs to a specific location.
#SCRON --chdir /project-location
#SCRON --time 0:30:00
#SCRON --nodes 2
#SCRON --output /output-location/output.log
@teatime ./script.sh
```

`@teatime` is [an alias](https://slurm.schedmd.com/scrontab.html#SECTION_SCRONTAB-OPTIONS) provided by `scrontab`. It specifies that the job becomes eligible at 16:00 (4:00 PM) each day.

### Automate node management

```text theme={"system"}
# Every Saturday at 6:00 AM, put nodes in drain state for maintenance.
0 6 * * 6 scontrol update nodename=slurm-node-[000-009] state=drain reason="maintenance"
```
