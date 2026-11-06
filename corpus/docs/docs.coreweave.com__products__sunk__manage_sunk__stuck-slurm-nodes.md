# Address nodes stuck during cleanup operations

Source: https://docs.coreweave.com/products/sunk/manage_sunk/stuck-slurm-nodes

# Address nodes stuck during cleanup operations

> Troubleshooting steps for Slurm nodes stuck in the Completing state

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

In Slurm, `COMPLETING` is an interim state that occurs while the job [Epilog script](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md) and cleanup operations are running. If these cleanup operations fail, Slurm jobs may remain in the `COMPLETING` state indefinitely.

In SUNK v6.8.0 and later, a built-in automation handles cleanup of jobs and nodes stuck in the `COMPLETING` state. For SUNK versions earlier than v6.8.0, follow the manual remediation steps in this guide to address a Slurm node stuck in `COMPLETING`.

## Match CG duration to a cause

`COMPLETING` (`CG`) is a normal, brief interim state while Slurm tears down a finished job. Before remediating, compare how long the job has been completing against the cluster's teardown timeouts:

```bash theme={"system"}
# Print the timeouts that govern teardown. Safe; read-only.
scontrol show config | grep -E "KillWait|UnkillableStepTimeout"
```

SUNK sets `KillWait` to 30 seconds and `UnkillableStepTimeout` to 900 seconds by default. Read the live values rather than assuming the defaults.

On SUNK v6.8.0 through v6.9.0, the `cleanup-completing` automation uses twice `KillWait`, which is 60 seconds at the default. [SUNK v6.9.1](https://docs.coreweave.com/release-notes/sunk-v-6-9-1.md) changes the default calculation to twice `UnkillableStepTimeout` plus 10 minutes, which is 40 minutes at the defaults. This calculation applies to later 6.x releases and 7.x releases unless you configure a cleanup timeout override.

On SUNK v8.0.0 and later, [`cleanupCompleting.timeoutSeconds`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#cleanupCompleting--timeoutSeconds) defaults to 2,400 seconds, or 40 minutes. Changing `UnkillableStepTimeout` alone doesn't change this timeout. On earlier versions, setting `cleanupCompleting.timeoutSeconds` overrides the calculated timeout.

The following table provides approximate timing guidance. Cleanup depends on the automation being enabled and its schedule or check interval. It skips nodes with running jobs. The table matches how long a job has been in `CG` to the timeout that is most likely holding it there:

| CG duration is roughly | Likely cause | What it implies |
| - | - | - |
| Briefly, below the cleanup threshold for your SUNK version | Normal teardown. The Epilog chain, including the Node Health Check, is running. | No action. |
| Around `KillWait` | Job processes didn't exit before the `SIGKILL` deadline, or the Epilog is blocked waiting for the job's Kubernetes resources to be deleted, often because the node is unreachable. | The node can drain with `Kill task failed` or `scheduler: k8s pod deletion timeout for job [JOB-ID]`, even if the Epilog finishes cleanly moments later. Both are safe to undrain once the node is healthy. |
| Around `UnkillableStepTimeout` | A job step is still unkillable after `SIGKILL`. | SUNK's unkillable-step handler requests a reboot of the node. Wait for the reboot to finish. See [How long to wait for a Kubernetes repair](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#how-long-to-wait-for-a-kubernetes-repair). |
| Around twice `KillWait`, or 60 seconds at the default | On SUNK v6.8.0 through v6.9.0, the job has reached the default cleanup threshold. | The `cleanup-completing` automation can mark the node `DOWN`. These versions use a shorter timeout than v6.9.1 and later. |
| Around twice `UnkillableStepTimeout` plus 10 minutes, or 40 minutes at the defaults | On SUNK v6.9.1 and later 6.x releases, and on 7.x releases, the job has reached the default cleanup threshold. The node may be unreachable or the Epilog unable to complete. | The `cleanup-completing` automation can mark the node `DOWN`. A configured `cleanupCompleting.timeoutSeconds` overrides this calculation. |
| Around `cleanupCompleting.timeoutSeconds`, or 40 minutes at the default | On SUNK v8.0.0 and later, the job has reached the configured cleanup threshold. The node may be unreachable or the Epilog unable to complete. | The `cleanup-completing` automation can mark the node `DOWN`. |

Depending on the SUNK version, the cleanup reason begins with `cleanup completing: reached timeout` or `Node marked DOWN by SUNK due to stuck in COMPLETING state`. For versions earlier than v6.8.0, follow the manual remediation steps in this guide.

> [!WARNING]
>
> Do not perform a sync with Argo during this process. Syncing with Argo overwrites the in-cluster changes prematurely.

**1. List the stuck nodes**

Use the `squeue` command to identify the job stuck in `COMPLETING` and fetch its associated node list:

```bash theme={"system"}
squeue -t CG -o "%.18i %.9P %.8j %.8u %.2t %.10M %.10L %R"
```

For more information about this and other Slurm commands, see the documentation for monitoring [Slurm node states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md) and [Slurm job states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states.md).

**2. Set nodes to the DOWN state**

For each node, use `scontrol` to set the node state to `DOWN` with the reason `"cleanup completing"`. Replace `[NODE-NAME]` with the name of the stuck node:

```bash theme={"system"}
scontrol update node=[NODE-NAME] state=DOWN reason="cleanup completing"
```

This step is necessary because Slurm's default `cleanup_completing` logic only addresses nodes in the `DOWN` state.

**3. Optional: Re-register nodes in INVAL**

Complete this step only if the nodes are also in the [`INVAL` state](https://docs.coreweave.com/products/sunk/manage_sunk/inval-node-state). `sinfo` shows this state as `inval`, and `scontrol show node` shows it as the `INVALID_REG` flag in the `State` field. If the nodes are in `INVAL`, set them to `DOWN` as shown in the previous step.

Then delete the node from Slurm for a clean re-registration:

```bash theme={"system"}
scontrol delete node=[NODE-NAME]
```

If `scontrol delete` returns `Requested nodes are busy`, the node is part of an active reservation. Remove the node from the reservation before deleting it, then add it back after the node re-registers. Replace `[RESERVATION-NAME]` with the name of the reservation:

1. Identify the reservation the node belongs to:

   ```bash theme={"system"}
   scontrol show node [NODE-NAME] | grep -i reserv
   ```

2. Remove the node from the reservation:

   ```bash theme={"system"}
   scontrol update ReservationName=[RESERVATION-NAME] Nodes-=[NODE-NAME]
   ```

3. Delete the node:

   ```bash theme={"system"}
   scontrol delete node=[NODE-NAME]
   ```

4. After the node re-registers, add it back to the reservation:

   ```bash theme={"system"}
   scontrol update ReservationName=[RESERVATION-NAME] Nodes=+[NODE-NAME]
   ```

After completing these steps, the impacted nodes should be in the `DOWN` state. The Slurm job then transitions from the `COMPLETING` state to the `COMPLETED` state, and after a short time, the nodes transition back to `IDLE`.

If the node is `DOWN` and the Slurm job remains in the `COMPLETING` state, cancel the job. If the Slurm job is still stuck in the `COMPLETING` state, reconfigure.
