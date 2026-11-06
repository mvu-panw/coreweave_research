# Connect to the Slurm login node

Source: https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node

# Connect to the Slurm login node

> Connect to an individual Slurm login node using SSH

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page shows administrators and Slurm users how to connect to a Slurm login node to submit jobs and run management tasks against the cluster. To run jobs or management tasks in the Slurm cluster, you must first connect to the Slurm login node.

You can access the login node through SSH or `kubectl exec`, depending on your directory service configuration. SSH requires a directory service pre-configured for SSH access, while `kubectl exec` doesn't. This page covers SSH (with and without port forwarding), running your first Slurm command to confirm access, using `kubectl exec` when SSH isn't available, and troubleshooting a login node that's slow or drops your session.

For information about initial setup of Slurm login nodes, see [Configure Slurm individual login nodes](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login.md).

## Before you connect

Before you can reach a login node, both an administrator and each user must finish provisioning. A missing step here is the most common reason a first connection fails:

* **Administrator**: enable the SCIM API and SUNK User Provisioning, then create the user groups your cluster uses for login and admin access. The Cloud Console creates `slurm-users` and `sudo-users` by default, but a cluster set up with custom groups uses whatever names you defined. See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) and [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache).
* **Each user**: add at least one SSH public key to the **Slurm Attributes** section of your [Cloud Console settings](https://console.coreweave.com/account/settings), then confirm with your administrator that you belong to the required groups. See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md).

## Connect through SSH

SSH is the preferred way to reach a Slurm login node when the cluster exposes the login service on a public IP address. Use this method when your directory service is already configured for SSH access.

> [!NOTE]
>
> Accessing the login node through SSH requires a directory service with users configured for SSH access.

First, use the `kubectl get svc slurm-login` command to identify the login service's IP address or DNS record so you know where to point your SSH client. The `EXTERNAL-IP` field in the command output contains the IP address.

In the following example, the target IP address is `203.0.113.100`:

```bash title="Obtain the External IP address" theme={"system"}
kubectl get svc slurm-login
```

You should see output similar to the following:

```text theme={"system"}
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)   AGE
slurm-login   LoadBalancer   192.0.2.100      203.0.113.100    22/TCP    2d21h
```

Then, use SSH to log in with either the IP address or the DNS record created for the node.

```bash title="Log in with SSH" theme={"system"}
ssh example-user@203.0.113.100
```

You should see output similar to the following:

```text theme={"system"}
Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.13.0-40-generic x86_64)

example-user@slurm-login-0:~$
```

You're now logged into the Slurm login node and can run Slurm commands.

> [!WARNING]
>
> SSH is the preferred method of access for Slurm login nodes. However, don't directly access [Slurm compute nodes](https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes.md) through SSH to run tasks. Bypassing Slurm can interfere with currently running jobs and may cause nodes to drain unintentionally, leading to temporary loss of resources. Only use SSH to Slurm compute nodes to debug or inspect a job you already hold an allocation for, including with SSH-dependent tooling such as `rsync` or a remote debugger. To reach a node in a job you already hold, see [Access Slurm compute nodes](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md).

## Connect through port forwarding

Use port forwarding when no public IP address is allocated for the login node, so you can still reach it through SSH from your local machine.

If no public IP address is allocated for the node, first port-forward the service with the `kubectl port-forward` command, then log in through SSH using the port-forwarded address. Each login Pod has an associated headless service, allowing users to refer to the pod by name without specifying a fully qualified domain name (FQDN).

To access an individual login Pod with port-forwarding, use the `kubectl port-forward` and `ssh` commands, as shown in the following example:

```bash title="Log in with port-forwarding" theme={"system"}
kubectl port-forward svc/slurm-login-slurmuser1 10022:22
ssh example-user@localhost -p 10022
```

The port-forwarding command in this example, `kubectl port-forward svc/slurm-login-slurmuser1 10022:22`, works as follows:

* The `kubectl port-forward` command creates a port-forward.
* `svc/` specifies that the targeted resource is a Service.
* `slurm-login-slurmuser1` is the exact name of the targeted Kubernetes Service. Replace this value with the name used within your namespace.
* `10022:22` defines the port mapping. In this case, it forwards traffic from local port `10022` to port `22` on the target Service.

The SSH command, `ssh example-user@localhost -p 10022`, then connects to the local port `10022`. Because of the port-forwarding performed in the preceding command, Kubernetes sends this traffic to port `22` of the specified Kubernetes Service.

You're now logged into the Slurm login node and can run Slurm commands.

## Run Slurm commands

Once you're connected to the login node, confirm that the cluster is reachable from your session and that your user has permission to submit work.

After you log in, you have access to all normal Slurm operations to submit jobs or manage the cluster. SchedMD provides extensive [documentation for Slurm commands](https://slurm.schedmd.com/documentation.html) and some [printable cheat-sheets](https://slurm.schedmd.com/pdfs/summary.pdf).

To verify that the cluster is working, run a small job. For example, discover the hostname on six nodes, as shown in the following example:

```bash theme={"system"}
root@slurm-login-0:~# srun -N 6 hostname
slurm-rtx4000-3
slurm-rtx4000-1
slurm-rtx4000-0
slurm-cpu-epyc-0
slurm-cpu-epyc-1
slurm-rtx4000-2
```

If you run into any errors such as "Invalid partition name specified" or "Invalid account or account/partition combination specified", you likely haven't been added as a Slurm user. Ask your administrator to add you to a provisioned group. [SUNK User Provisioning](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) creates your Slurm user from that group membership within minutes.

On a cluster that doesn't run SUNK User Provisioning, an administrator can create the Slurm user directly. Replace `[USERNAME]` with your Slurm username:

```bash title="Add a Slurm user on a cluster without SUNK User Provisioning" theme={"system"}
sudo su
sacctmgr create user -i account=root adminlevel=admin name=[USERNAME]
exit
```

If your Slurm cluster uses accounts other than `root`, run the preceding command for each account you need to be added to.

> [!WARNING]
>
> Don't use `sacctmgr` to add users on a cluster where SUNK User Provisioning manages Slurm users. Each sync run deletes any Slurm user that doesn't map to a POSIX user in a provisioned group, including users created by hand. See [Slurm user and account lifecycle](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#slurm-user-and-account-lifecycle).

## Troubleshooting

If SSH is unavailable or you need root access for debugging, you can fall back to `kubectl exec` to open a shell directly on the login Pod.

When SSH isn't possible, use `kubectl exec` to access the Slurm login node as root. This method is useful for debugging and maintenance tasks.

```bash title="Access the Slurm login node with kubectl exec" theme={"system"}
kubectl exec -it slurm-login-0 -c sshd -- bash
root@slurm-login-0:/tmp#
```

### Slow shell commands

Slow `cd`, `ls`, or `git` on a login Pod usually comes from memory pressure, shared-storage contention, or a heavy neighbor process on a shared login Pod. The login Pod isn't a compute node, and a common cause for delay is interactive tooling that quietly consumes the whole pod: security scanners, AI coding agents, package builds such as `uv sync` or `ninja`, JVM-based IDEs, `rclone` transfers, and IDE remote-server processes. Move that work to `srun` or `sbatch`. Isolate shared-storage contention by comparing a local path to a shared path:

```bash theme={"system"}
# Compare a local path to a shared path to isolate storage contention. Safe; read-only.
time ls /tmp
time ls /mnt/home/$USER
```

If `/tmp` is fast but the shared path is slow, the contention is in shared storage, not the pod.

### SSH disconnects mid-session

Start by asking whether you're the only one affected. That narrows the cause faster than any other check.

* **Resource pressure or OOM**, if only sessions on your pod dropped. If the login Pod is OOM-killed, every session on it drops. A non-zero `RESTARTS` value on `kubectl get pod [LOGIN-POD-NAME]` around the time of the disconnect indicates that the pod was killed, often for memory. For related guidance on compute-node memory pressure, see [Diagnose unexplained memory pressure on a SUNK node](https://docs.coreweave.com/products/sunk/optimize_workloads/memory-accounting.md).
* **Node-level CPU contention**, if your pod looks healthy but sessions still drop. Workloads from other namespaces scheduled onto the same node can starve `sshd` until keepalives time out. Per-pod CPU can look normal while the node is saturated, so check the node rather than the pod. This is a node-level condition you can't fix from inside the pod, so escalate.
* **Authentication backend trouble**, if many users lost their sessions at the same moment across different pods. The directory service that authenticates SSH can drop its backend connection and reject every authentication until it reconnects, usually within minutes. Simultaneous disconnects across pods on different nodes point here rather than at any one node.
* **A transient network drop**, if SSH was unreachable for a minute or two and then recovered on its own with no pod restart and no node alert. Escalate if it recurs on the same node.

To keep work from dying with the connection, run long interactive sessions inside a terminal multiplexer such as `tmux`, and set `ServerAliveInterval` in your local `~/.ssh/config`. If `tmux` reports `server exited unexpectedly` on a pod that has been running for weeks, clear its stale sockets with `rm -rf /tmp/tmux-$(id -u)/` and start a new session.
