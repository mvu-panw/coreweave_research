# Restrict compute node access with pam_slurm_adopt

Source: https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt

# Restrict compute node access with pam_slurm_adopt

> Configure the pam_slurm_adopt PAM module to restrict SSH access to Slurm compute nodes to users with active job allocations

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

`pam_slurm_adopt` is a Pluggable Authentication Module (PAM) that blocks SSH logins to compute nodes where the user has no running job, and also ensures that SSH-launched processes are placed under the job's `extern` step cgroup so resource limits apply and processes are cleaned up when the job ends.

This guide explains how to enable `pam_slurm_adopt` on SUNK compute nodes. When it's active, users can no longer SSH directly to a compute node outside of a job allocation to bypass Slurm resource management.

SUNK doesn't configure `pam_slurm_adopt` for you, and compute nodes accept SSH by default in SUNK 8.0 and later. Until you configure it, any user with a provisioned SSH key can log in to any compute node and start work outside Slurm, which escapes resource accounting and can drain the node. Configure it on any SUNK Standard cluster where users hold SSH keys.

> [!NOTE]
>
> `pam_slurm_adopt` enforces authorization (whether a user is allowed to access a specific node), not authentication. Users authenticate using SSH keys distributed through SUNK User Provisioning. Authentication and authorization must both succeed to establish an SSH connection to a compute node.

## Prerequisites

Before configuring `pam_slurm_adopt`, the following must be in place:

* SSH is enabled on compute nodes (`compute.ssh.enabled: true`), which is the default on CoreWeave clusters. See [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md#other-global-options).
* SUNK User Provisioning (SUP) is configured so that SSH keys are distributed to compute nodes. See [Manage users with nsscache on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache.md).

SUNK requires the following Slurm configuration values and sets them by default. Confirm they are present in your `values.yaml` before continuing:

| Parameter | Required value | Default in SUNK |
| - | - | - |
| `slurmConfig.TaskPlugin` | Must include `task/cgroup` | `task/cgroup,task/affinity` |
| `slurmConfig.ProctrackType` | `proctrack/cgroup` | `proctrack/cgroup` |

## Step 1: Add `Contain` to `PrologFlags`

`pam_slurm_adopt` requires `PrologFlags` to include `Contain`. With this flag set, Slurm creates a PAM container for each job on the node, which allows the module to verify whether an SSH login belongs to an active allocation.

Add `Contain` to the existing `PrologFlags` value in your `values.yaml` (the SUNK default is `Alloc,Serial`):

```yaml theme={"system"}
slurmConfig:
  PrologFlags: "Alloc,Serial,Contain"
```

With this value set, Slurm creates the PAM containers that `pam_slurm_adopt` uses to verify SSH logins. Proceed to Step 2 to inject the PAM rule.

## Step 2: Inject the PAM rule with an s6 script

SUNK compute nodes run inside containers. The PAM configuration file (`/etc/pam.d/sshd`) isn't persistent, so you must inject the `pam_slurm_adopt` rule each time the container starts. Use an [s6 oneshot script](https://docs.coreweave.com/products/sunk/run_workloads/run-scripts-with-s6.md) under `compute.s6` in your `values.yaml` to do this:

```yaml theme={"system"}
compute:
  s6:
    pam-auth:
      type: oneshot
      timeoutUp: 0
      timeoutDown: 0
      script: |
        #!/usr/bin/env bash
        sed -i '/@include common-account/a -account    required      /usr/lib/x86_64-linux-gnu/security/pam_slurm_adopt.so' /etc/pam.d/sshd
```

The script inserts a PAM `account` rule for `pam_slurm_adopt` after the `@include common-account` line in `/etc/pam.d/sshd`. The leading `-` means PAM skips the rule if the module file isn't found, rather than failing the login.

> [!WARNING]
>
> Deliver the rule through `compute.s6`, as shown, rather than mounting a ConfigMap over `/etc/pam.d/sshd`. In SUNK 7.x and earlier, login Pods inherit the compute volume mounts, so a PAM file mounted for compute also lands on the login Pods. That denies every user who holds no job, locking them out of the login node as well. `compute.s6` scripts run only on compute nodes in every SUNK version, so the rule reaches `slurmd` Pods only.

## Apply the changes

With both `values.yaml` changes in place, upgrade the Helm release to apply them to the cluster. Replace `[RELEASE-NAME]` with the name of your Slurm Helm release, and `[NAMESPACE]` with the Kubernetes namespace where SUNK is deployed (typically `tenant-slurm`):

```bash theme={"system"}
helm upgrade [RELEASE-NAME] coreweave/slurm -f values.yaml -n [NAMESPACE]
```

## Expected behavior

After the changes take effect, the following behavior applies when users SSH to a compute node:

* Users with an active Slurm job allocation on the target node can SSH in. Slurm adopts their SSH session as a job step and tracks it for resource accounting.
* Users without an active allocation on the target node are denied access, regardless of whether their SSH key is valid.
* Users can still SSH to the Slurm login node at any time. The allocation check applies only to compute nodes.

For the user-facing side of this, including how to reach a compute node through the login node with `ProxyJump`, see [Access Slurm compute nodes](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md).
