# Run Prolog and Epilog scripts on SUNK

Source: https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog

# Run Prolog and Epilog scripts on SUNK

> Overview of Slurm Prolog and Epilog scripts in SUNK, including how they work and failure handling behavior

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page explains how SUNK runs Slurm Prolog and Epilog scripts, the best practices to follow when authoring them, and how SUNK behaves when these scripts fail. Use this information to customize job setup and teardown on SUNK clusters while keeping nodes healthy and workloads consistent.

In Slurm, [Prolog and Epilog scripts](https://slurm.schedmd.com/slurm.conf.html#SECTION_PROLOG-AND-EPILOG-SCRIPTS) run before and after each job, respectively. They're commonly used in HPC environments to perform setup and teardown tasks. These scripts are essential for customizing job behavior and maintaining consistency across workloads.

* **Prolog scripts** run on each compute node allocated to the job, when Slurm allocates it and before the job starts. They ensure pre-job tasks are done, such as setting environment variables, loading software modules, or mounting file systems. They can also collect job metadata for debugging or optimization.

* **Epilog scripts** run after the job finishes, regardless of success or failure. They handle post-job tasks, such as logging metrics, notifying users, archiving outputs, transferring data to external systems, or cleaning up files.

In SUNK, these scripts are deployed and managed as Kubernetes ConfigMaps, providing a centralized way to manage them. This approach ensures that script changes propagate consistently across all Slurm nodes in the cluster.

Slurm also supports `PrologSlurmctld` and `EpilogSlurmctld` scripts that run on the control node for system-wide policy enforcement.

For more information, see the [Slurm Prolog and Epilog Guide](https://slurm.schedmd.com/prolog_epilog.html).

## How SUNK handles Prolog and Epilog

While Slurm typically uses a single script for Prolog and Epilog, SUNK extends this with entrypoint scripts, `prolog.sh` and `epilog.sh`, that set up the environment and call `run-parts.sh` to run all scripts in the `/etc/slurm/prolog.d/` and `/etc/slurm/epilog.d/` directories. This modular approach helps you manage workflows by breaking them into smaller, reusable scripts.

## Best practices

When using Prolog and Epilog scripts in SUNK, follow these best practices for efficiency, reliability, and security:

**Minimize resource usage**: Keep scripts lightweight to avoid exceeding Kubernetes pod limits. Scripts should use minimal CPU and memory to prevent interference with user jobs. Keep scripts as short and fast as possible to avoid delays in job start or cleanup. Avoid Slurm commands such as `squeue`, `scontrol`, or `sacctmgr` in the script, because they can cause performance issues.

**Test thoroughly**: Validate scripts in a test environment before deployment to prevent disruptions in production.

**Ensure idempotency**: Scripts must run multiple times without causing unintended effects, especially during retries and restarts. Implement error handling and log errors for debugging.

**Handle environment dependencies**: Be aware of environment dependencies and ensure they're met. Because scripts don't have a search path set, use fully qualified paths or set a `PATH` environment variable to run programs.

**Log script execution**: Include logging to track script execution, identify issues, and capture relevant job details such as job ID and node assignments. Don't hardcode credentials in logs. Use secure methods for secrets.

**Review and update regularly**: Update scripts regularly to reflect changes in the environment, job requirements, or security policies. Keep scripts version-controlled and document changes to ensure team awareness.

## Failure handling

Understanding how SUNK reacts when a Prolog or Epilog script fails helps you predict job and node behavior and design scripts that recover safely.

Failure handling in Prolog and Epilog scripts depends on the type of script and the context in which it runs. The following rules apply to Prolog and Epilog scripts in Slurm when the job fails with a non-zero exit code:

* If `Prolog` fails, the node is set to a `DRAIN` state, and the job is requeued. The job is placed in a held state unless `nohold_on_prolog_fail` is configured in `SchedulerParameters`. SUNK sets `nohold_on_prolog_fail` by default, so the requeued job isn't held.
* If a `PrologSlurmctld` batch job fails, the job is requeued.
* If a `PrologSlurmctld` interactive job fails, such as `salloc` or `srun`, the job is canceled.
* If `Epilog` fails, the node is set to a `DRAIN` state.
* If `EpilogSlurmctld` fails, the failure is only logged, and the job isn't requeued.

## Troubleshoot Prolog and Epilog failures

When a Prolog or Epilog script fails, the node is drained and the drain reason records what happened. Use the following steps to diagnose and recover.

SUNK runs [Node Health Check (NHC)](https://github.com/mej/nhc) as one of the scripts in the Epilog chain after a job, and only when no other job is still running on the node. A failed check drains the node with a reason that begins with `NHC:`.

An `NHC:` drain is therefore an Epilog failure with a hardware or system cause rather than a script bug. For those, see [Node Health Check (NHC) drains](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#node-health-check-nhc-drains).

### Find the drain reason

A failed Prolog or Epilog drains the node with a reason you can read from Slurm. These commands are safe to run anytime and are read-only:

```bash theme={"system"}
# Show a node's state and Reason field, including a Prolog or Epilog failure.
scontrol show node [NODE-NAME]
```

```bash theme={"system"}
# List all drained nodes with their reasons.
sinfo -R
```

Drain reasons related to Prolog and Epilog include strings such as `Prolog error`, `Epilog error`, `prolog pre-hook failed`, and reasons indicating the Epilog runtime exceeded its timeout. For the full catalog of drain reasons and which are safe to undrain, see [Drain and undrain Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md).

### Recover the node

If the drain reason includes `sunk:verify-undrain`, SUNK automatically returns the node to service after it passes the next [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) test. No action is required unless it keeps failing.

For a Prolog or Epilog failure that doesn't auto-undrain, fix and test the script first, then undrain the node:

```bash theme={"system"}
# Undrain a single node using the built-in login node alias.
undrain [NODE-NAME]
```

```bash theme={"system"}
# Or undrain with scontrol directly.
scontrol update nodename=[NODE-NAME] state=resume
```

Monitor the node after undraining it. If you don't fix the underlying cause, SUNK drains the node again the next time a job triggers the failing script.

### Common causes you can fix

Most Prolog and Epilog drains trace to the script itself:

* **Non-zero exit code**: A command in the script failed. Fix the logic and test it before redeploying.
* **Unset `PATH`**: Scripts run without a search path. Use fully qualified paths or set `PATH` explicitly. See [Best practices](#best-practices).
* **Missing paths or devices**: A check for a path or device that isn't present exits non-zero and drains the node. Harden these checks so they fail gracefully.
* **Long-running scripts**: A script that exceeds the Prolog or Epilog timeout drains the node. Keep scripts short and fast.
* **Slurm commands in scripts**: Avoid `squeue`, `scontrol`, and `sacctmgr` in scripts, because they add load and latency.

Because `slurmd` doesn't reliably log Prolog standard output unless the script fails, redirect output to a file inside the script while you debug:

```bash theme={"system"}
# Add near the top of the script to capture output for debugging.
exec >> /tmp/prolog_debug.log 2>&1
```

> [!WARNING]
>
> **`PrologFlags=Serial` slows array jobs**
>
> Setting `PrologFlags=Serial` in your Slurm configuration forces per-node serialization of Prolog and Epilog execution: Each task's Prolog or Epilog must wait for all preceding ones on that node to finish. Epilog runs the same serialized path, which doubles the effect.
>
> For array jobs with high per-node concurrency (for example, 100 or more tasks on one node), this creates queueing that scales with the number of tasks. The wait can turn a near-instant script into delays of several minutes. The symptoms are tasks reporting `NODE_FAIL` or `Prolog hung on node`, and Prolog or Epilog runtimes far longer than the scripts themselves. Because `Serial` serializes the entire chain of scripts in `prolog.d` and `epilog.d`, a heavier chain amplifies the delay.
>
> SUNK sets `PrologFlags=Alloc,Serial` by default, so if you run high-concurrency array jobs and see this pattern, consider removing `Serial`. Check the current value with `scontrol show config | grep PrologFlags`, and set the new value through `slurmConfig` in the Slurm chart values on SUNK Standard, or `spec.slurmConfig` on the `SunkCluster` resource on SUNK Self-Service, rather than editing the ConfigMap in place.
