# Access Slurm compute nodes

Source: https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes

# Access Slurm compute nodes

> Open a shell on a compute node, attach to a job's running container, or connect over SSH through the login node

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Slurm jobs run on compute nodes, but the shell you submit from lives on the login node. When a job goes wrong, you often need to get onto the node where it's running and inspect it: check GPU state, read a log the job never flushed, or run a command inside the container the job started.

This guide covers the three ways to do that on a SUNK cluster, and when each one applies:

* `srun --overlap` opens a shell on a node in an allocation you already hold.
* `srun --container-name=[NAME]:exec` attaches to the container a job is already running, rather than starting a new one.
* SSH through the login node with `ProxyJump` gives you a plain shell on the node, which is what tooling such as `rsync` and remote debuggers expect.

`srun --overlap` and the container-attach method are scoped to your own allocation. SSH isn't. Unless an administrator has configured [`pam_slurm_adopt`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt), which is available on SUNK Standard, a provisioned key opens any compute node, whether or not you hold a job on it. See [SSH access on compute nodes](#ssh-access-on-compute-nodes).

> [!WARNING]
>
> Use compute node access to inspect and debug jobs you already hold an allocation for. Don't use it to run work outside Slurm. Processes started outside a job escape Slurm's resource accounting, interfere with running jobs, and can drain the node, taking it out of service for everyone. See [Compute and login nodes](https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes.md).

## Prerequisites

* An active job allocation on the cluster. The `srun` methods require one. SSH doesn't enforce one unless an administrator has configured [`pam_slurm_adopt`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt), but use it only on nodes where you hold a job. See [SSH access on compute nodes](#ssh-access-on-compute-nodes).
* Access to a Slurm login node. See [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).
* For the container attach method, SUNK v7.x or later. Earlier versions carry a bug that can prevent Pyxis from finding a running container; SUNK v7.x includes a fix. See the [SUNK v7.0.0 release notes](https://docs.coreweave.com/release-notes/sunk-v-7-0-0.md). To find your cluster's version, read `spec.sunkVersion` on the `SunkCluster` resource of a SUNK Self-Service cluster, or the chart version that `helm list -n [NAMESPACE]` reports for a SUNK Standard cluster.
* For the SSH method, `sshd` running on the compute nodes. CoreWeave clusters run it by default, in both SUNK Standard and SUNK Self-Service, so this usually needs no action. See [SSH access on compute nodes](#ssh-access-on-compute-nodes).

## Choose an access method

The following table matches each task to the method that fits it, along with what that method requires.

| You want to | Use | Needs |
| - | - | - |
| Run a command or open a shell on a node in your job | `srun --overlap` | Nothing beyond an allocation |
| Run a command inside the container your job is already running | `srun --overlap --container-name=[NAME]:exec` | SUNK v7.x, a named container, the right node |
| Use SSH-based tooling such as `rsync`, `scp`, or a remote debugger | `ssh -J` through the login node | `sshd` on the compute nodes, which is the default |

`srun --overlap` is the default choice. Choose SSH only when a tool you're running requires an SSH endpoint and can't work through `srun`.

## Open a shell on a node in your allocation

`srun --overlap` starts a new job step inside an allocation you already hold. The `--overlap` flag lets that step share resources with the steps already running, instead of waiting for them to release the node.

1. Find the job you want to inspect and the nodes it holds.

   ```bash theme={"system"}
   squeue --me
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   JOBID  PARTITION  NAME     USER          ST  TIME   NODES  NODELIST(REASON)
   1335   h100       raytest  example-user  R   15:46  2      slurm-h100-231-[147,217]
   ```

2. Expand the compact node list into individual hostnames. Replace `[JOB-ID]` with the value from the `JOBID` column for your allocation.

   ```bash theme={"system"}
   scontrol show hostnames $(squeue -j [JOB-ID] -h -o %N)
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   slurm-h100-231-147
   slurm-h100-231-217
   ```

3. Open an interactive shell on the job. Replace `[JOB-ID]` with your job ID.

   ```bash theme={"system"}
   srun --overlap --jobid [JOB-ID] --pty bash -i
   ```

   Without a node selection, Slurm places the step on the first node of the allocation. For a multi-node job, that's usually the rank-zero node.

4. Optional: To target a specific node instead, pass `-w` with a hostname from step 2.

   ```bash theme={"system"}
   srun --overlap --jobid [JOB-ID] -w [NODE-NAME] --pty bash -i
   ```

You now have a shell on the compute node, inside the job's cgroup. Anything you run counts against the job's resources, and it stops when the job ends.

To run a single command instead of opening a shell, omit `--pty` and pass the command directly:

```bash theme={"system"}
srun --overlap --jobid [JOB-ID] -w [NODE-NAME] nvidia-smi
```

## Attach to a container running in your job

To get inside the running container, name it when the job creates it, then attach with the `:exec` suffix.

That extra naming step matters because a shell from `srun --overlap` lands on the compute node, not inside the container your job started. The two have different filesystems, different environment variables, and different installed packages, so a debugging session on the node shows little about the environment the job's process runs in.

> [!NOTE]
>
> This requires SUNK v7.x or later. On earlier versions the attach fails with `"exec" flag was passed to --container-name but the container is not running`, even when the container is running. See the [SUNK v7.0.0 release notes](https://docs.coreweave.com/release-notes/sunk-v-7-0-0.md).

### Name the container when the job starts it

Pyxis only tracks a container by name if you give it one. Add `--container-name` to the `srun` or `sbatch` step that starts the container:

```bash theme={"system"}
srun --container-image=/mnt/home/[USERNAME]/[IMAGE].sqsh \
     --container-name=[NAME]-${SLURM_JOB_ID} \
     --container-mounts=/mnt/home:/mnt/home \
     sleep infinity
```

Include `${SLURM_JOB_ID}` in the name. Pyxis reuses an existing container filesystem when a matching name already exists on a node, so a fixed name such as `interactive` reuses whatever an earlier job left on that node. On a multi-node job, that yields containers with different contents on different nodes, all from the same image file.

A job-scoped name also keeps two users off one cached filesystem. The cache directory belongs to the user who created it, so a second user who reuses the same name gets `Permission denied` reading the container's root filesystem.

### Attach to the named container

Attach from the login node with `--container-name=[NAME]:exec`. With the `:exec` suffix, Pyxis enters the running container and fails if it isn't running, rather than quietly creating a new one.

```bash theme={"system"}
srun --overlap --jobid [JOB-ID] -w [NODE-NAME] \
     --container-name=[NAME]-[JOB-ID]:exec --pty bash -i
```

Replace the placeholders with the following:

* `[JOB-ID]`: the value from the `JOBID` column in `squeue --me` for your allocation. Because the job expanded `${SLURM_JOB_ID}` into the container name, this is also the suffix on the name you attach to.
* `[NODE-NAME]`: a hostname from `scontrol show hostnames`. Pass this every time. Pyxis creates one container per node, so the attach only succeeds on the node where that container is running.
* `[NAME]`: the base container name you set when the job started the container.

To confirm you're inside the container rather than on the compute node, check the filesystem, not the process list. Enroot doesn't create a separate PID namespace, so `ps` shows the same processes inside and outside the container. Print the OS release instead. Inside the container, it comes from your image:

```bash theme={"system"}
cat /etc/os-release
```

If your image and the compute node run the same distribution, look for a path or package that only your image has, such as your project directory or a Python package the job depends on.

You're now inside the job's container, sharing its filesystem and running alongside the job's own processes.

### `--container-name:exec` compared to `--container-image`

Both flags give you a shell with your image's filesystem, but they aren't interchangeable:

* `--container-name=[NAME]:exec` enters the container the job is already running. You see the job's processes, its environment, and any files it has written since it started.
* `--container-image=[IMAGE].sqsh` starts a fresh container from the image on the same node. You get the same software, but a clean filesystem and none of the job's runtime state.

Use `:exec` when you're debugging what a job is doing right now. Use `--container-image` when you want a scratch environment that happens to match the job's, such as testing a fix before you resubmit.

## Connect over SSH through the login node

SSH is worth the extra setup when a tool on your workstation requires a real SSH endpoint on the compute node, such as `rsync`, `scp`, or a remote debugger. For interactive shells, `srun --overlap` is simpler, and it puts the session in the job's cgroup without depending on how the cluster's PAM stack is configured.

Compute nodes have no public IP address, so your workstation can't reach one directly. Route the connection through the login node with `ProxyJump`. This requires SSH access to the login node itself. If your cluster's directory service isn't configured for SSH and you use `kubectl exec` instead, `ProxyJump` isn't available. See [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) to check which access method applies to your cluster.

### SSH access on compute nodes

CoreWeave clusters run `sshd` on compute nodes by default, so the SSH method is available without a configuration change. The Slurm chart CoreWeave publishes ships `compute.ssh.enabled: true`, and where the chart leaves the field unset, the SUNK operator defaults it to enabled. Either way, only an administrator who sets it to `false` turns compute SSH off. Users authenticate with the SSH keys that [SUNK User Provisioning](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) distributes, the same keys that grant login node access.

To turn compute SSH off on SUNK Standard, set the following in your Slurm `values.yaml`:

```yaml theme={"system"}
compute:
  ssh:
    enabled: false
```

> [!NOTE]
>
> The [`SunkCluster` resource](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference) on a SUNK Self-Service cluster has no field for this, so there's no supported way to change it. Contact CoreWeave support if you need compute SSH turned off.

> [!WARNING]
>
> Because compute SSH is on by default in SUNK 8.0 and later, a user with a provisioned key can log in to any compute node, whether or not they hold a job on it. Work started that way escapes Slurm's accounting and has drained nodes on production clusters. It also doesn't preempt CoreWeave's [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#preemption-on-sunk-clusters) tests, so a test can run on the same GPUs, and `nvidia-smi` on the node can show GPU and GPU memory usage that no Slurm job accounts for. On SUNK Standard, administrators should configure [`pam_slurm_adopt`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt), which denies logins to nodes where the user holds no allocation and places the session under the job's `extern` step cgroup, subject to the job's resource limits and cleaned up when the job ends. SUNK doesn't configure it for you. The `SunkCluster` resource on a SUNK Self-Service cluster has no setting for `pam_slurm_adopt`, so contact CoreWeave support if you need to restrict compute SSH there.

### Connect with ProxyJump

`ssh -J` opens a connection to the login node and tunnels a second SSH connection through it to the compute node. Your key never leaves your workstation. The login node forwards encrypted bytes it can't read.

Replace `[USERNAME]` with your Slurm username, `[LOGIN-NODE]` with the same login node address you already use to reach the cluster, and `[NODE-NAME]` with a hostname from `scontrol show hostnames`. To find the login node address, see [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

```bash theme={"system"}
ssh -J [USERNAME]@[LOGIN-NODE] [USERNAME]@[NODE-NAME]
```

The login node resolves `[NODE-NAME]`, so use the Slurm node name exactly as `squeue` reports it. If the name doesn't resolve, use the node's address from `scontrol show node [NODE-NAME]` instead.

> [!WARNING]
>
> Don't use agent forwarding (`ssh -A`) to reach compute nodes. Agent forwarding exposes your SSH agent socket on the login node, and anyone with root there can use it to authenticate as you, to any host your key opens. `ProxyJump` solves the same problem without that exposure.

### Make ProxyJump automatic

Rather than typing `-J` each time, put the jump in `~/.ssh/config` on your workstation. Match your cluster's node naming pattern so every compute node routes through the login node automatically:

```text title="~/.ssh/config" theme={"system"}
Host slurm-login
    HostName [LOGIN-NODE]
    User [USERNAME]
    IdentityFile ~/.ssh/id_ed25519

Host slurm-*
    User [USERNAME]
    ProxyJump slurm-login
    IdentityFile ~/.ssh/id_ed25519
```

With this in place, `ssh slurm-h100-231-147` connects through the login node without further flags. Adjust the `Host slurm-*` pattern to match the node names in your cluster, and make sure it doesn't also match the login node entry.

## Troubleshooting

The following sections cover the failures you're most likely to encounter when attaching to a container or connecting over SSH.

### Attach fails when the container is not running

The attach fails with `"exec" flag was passed to --container-name but the container is not running`. The step landed on a node where that named container isn't running. Pyxis creates one container per node, so Slurm can schedule an attach without `-w` onto a different node in the allocation.

1. Confirm which node runs the container, then target it with `-w`:

   ```bash theme={"system"}
   srun --overlap --jobid [JOB-ID] -w [NODE-NAME] bash -c 'enroot list -f'
   ```

2. Look for a row named `pyxis_[NAME]` with a non-empty PID. If the PID column is blank, the container isn't running on that node, or the name maps to a leftover container from an earlier job.

If the name is stale, remove it on that node and resubmit the job with a job-scoped name:

```bash theme={"system"}
srun --overlap --jobid [JOB-ID] -w [NODE-NAME] enroot remove -f pyxis_[NAME]
```

### Container contents differ between nodes in the same job

The job uses a fixed `--container-name`, and Pyxis reused a leftover container filesystem on some nodes instead of importing the image again. Give the container a job-scoped name, as described in [Name the container when the job starts it](#name-the-container-when-the-job-starts-it), or omit `--container-name` entirely for steps you don't need to attach to. Without a name, Pyxis creates a job-scoped container and cleans it up when the job ends.

### `Permission denied` when connecting over SSH to a compute node

Check these in order:

1. **You hold an allocation on that specific node.** With `pam_slurm_adopt` configured, a valid key alone isn't enough. Confirm with `squeue --me` that the node appears in your job's node list.
2. **Your key is on the cluster.** Compute nodes use the same provisioned keys as the login node. If you can't reach the login node either, add a key under **Slurm Attributes** in your [Cloud Console settings](https://console.coreweave.com/account/settings).
3. **`sshd` is running on the node.** Compute SSH is on by default, but an administrator can disable it with `compute.ssh.enabled: false`. A refused connection, rather than `Permission denied`, points here. Ask your administrator.

## Related

* [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md)
* [Tunnel VS Code for development on Slurm](https://docs.coreweave.com/products/sunk/access_sunk/vs-code-with-slurm.md)
* [Restrict compute node access with `pam_slurm_adopt`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt)
* [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md)
* [Run Ray on SUNK](https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk.md)
