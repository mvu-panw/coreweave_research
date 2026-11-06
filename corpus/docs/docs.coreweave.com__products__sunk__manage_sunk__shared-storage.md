# Share storage across Slurm nodes on SUNK Standard

Source: https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage

# Share storage across Slurm nodes on SUNK Standard

> Create and mount Persistent Volume Claims as shared storage across Slurm compute and login nodes on SUNK Standard

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

This page shows SUNK administrators how to provision shared storage for Slurm compute and login nodes by mounting Persistent Volume Claims (PVCs). Use shared storage when you need to share job inputs and outputs across nodes, host user home directories, or give multiple users access to a common dataset.

In Kubernetes, to ensure that data persists beyond the lifecycle of a given Pod, you can use Persistent Volume Claims (PVCs). A PVC is a request for storage by a user that you can provision from a Persistent Volume (PV). This mechanism lets you abstract the details of how the storage is provided and how it's consumed.

In SUNK, each Slurm node is deployed in a Kubernetes Pod, which can mount shared PVCs in the normal manner. SUNK provides a mechanism to map the Kubernetes Pod's PVC to a specified mount location within the Slurm node. Multiple Slurm nodes can mount the same PVC. This is particularly useful when managing jobs that require sharing access between developers or researchers, storing user home directories, and saving job output for further processing.

## Create shared storage

This section walks through provisioning the PVCs that the compute nodes mount. In this example, three PVCs are mounted to the Slurm compute nodes. To get started, create three PVCs in the cluster with a Container Storage Interface (CSI) driver that supports the `ReadWriteMany` access mode, which is required so multiple nodes can mount the same volume simultaneously. For more information about creating PVCs, see the Kubernetes documentation on [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

Use the following names so they match the references in the mount configuration that follows:

* `root-nvme`
* `data-nvme`
* `data-hdd`

## Mount PVCs

With the PVCs in place, configure the Slurm compute nodes to mount them. Mount the PVCs to the Slurm nodes by adding the `volumeMounts` and `volumes` keys in the `compute` section of `values.yaml`:

```yaml theme={"system"}
compute:
  volumeMounts:
    - name: root-nvme # root home dir, useful if not using LDAP and connecting with `kubectl exec`
      mountPath: /root
    - name: data-nvme # Mount for high-speed storage
      mountPath: /mnt/nvme
    - name: data-hdd # Mount for high-capacity bulk storage
      mountPath: /mnt/hdd
  volumes:
    - name: root-nvme # This is useful if not using ldap
      persistentVolumeClaim:
        claimName: root-nvme
    - name: data-nvme # The high-speed storage PVC
      persistentVolumeClaim:
        claimName: data-nvme
    - name: data-hdd # The high-capacity bulk storage PVC
      persistentVolumeClaim:
        claimName: data-hdd
```

See [`compute.volumeMounts`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) and [`compute.volumes`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) in the Slurm Parameter Reference for a link to a full `values.yaml` example.

After you apply this configuration, the three PVCs are available at the specified mount paths on every Slurm compute node.

## Login node

To mount the same PVCs on login nodes, add the `volumeMounts` and `volumes` entries from the compute example to `login.common.pod.volumeMounts` and `login.common.pod.volumes` in `values.yaml`. Use the same volume names, PVC claim names, and mount paths so that files are available at the same paths on login and compute nodes.

Login nodes don't inherit `compute.volumeMounts` or `compute.volumes`. Both login and compute nodes receive volumes and mounts derived from the top-level `storage` configuration. The additional entries under `compute` apply only to compute nodes. See [`login.common.pod.volumeMounts`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#login--common--pod--volumeMounts) and [`login.common.pod.volumes`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#login--common--pod--volumes) in the Slurm Parameter Reference.

## Use shared storage

The following examples illustrate common patterns for working with the mounted PVCs from a login node. After you mount the PVCs, you can use them as you would any other storage. For example, you can create a directory in the PVC and use it to store job output, as shown in the following example:

```bash theme={"system"}
# On the login node
mkdir /mnt/nvme/job-output
# Mount is accessible on all compute nodes
srun -N 1 -n 1 hostname > /mnt/nvme/job-output/$(hostname).txt
```

You can also use the PVCs to share data between users. For example, you can create a directory in the PVC and use it to store data that multiple users can access:

```bash theme={"system"}
# On the login node
mkdir /mnt/nvme/shared-data
# Mount is accessible on all compute nodes
srun -N 1 -n 1 hostname > /mnt/nvme/shared-data/$(hostname).txt
```

A file a user creates in a shared directory belongs to that user's primary group, not to a group their teammates share, and the default umask strips group write permissions. Teammates can read the file but can't change it. To set up a directory where a team's new files stay group-writable, combine group ownership, the setgid bit, and a group-writable umask. Most clusters have a `slurm-users` group that provisioned users belong to, though a cluster set up with custom groups uses whatever names you defined. Run `groups` to check which groups you're in. The first two commands need `sudo`, so an administrator or a member of the `sudo-users` group runs them:

```bash theme={"system"}
# Set the group and the setgid bit so new files inherit the directory's group.
sudo chgrp -R slurm-users /mnt/nvme/[SHARED-DIR]
sudo chmod 2770 /mnt/nvme/[SHARED-DIR]

# Each collaborator adds a group-writable umask so new files are group-writable.
echo 'umask 002' >> ~/.bashrc
```

To change the default umask for every shell on the cluster instead, set `compute.umask` in `values.yaml`. Leave it unset to keep the image default of `0022`. See [`compute.umask`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters).

Storing user home directories in a PVC is also useful. This lets users access their home directories from any compute node. In this example, the root home directory is mounted to the PVC named `root-nvme`. This is useful if you aren't using LDAP and you connect with `kubectl exec`, and you have helper scripts or other files in the root home directory.

## Keep home directories private

Because `/mnt/home` is shared, keep your own home directory and credentials private:

```bash theme={"system"}
# Restrict your home directory to yourself only.
chmod 700 /mnt/home/[USERNAME]

# Restrict SSH keys and credentials specifically.
chmod -R go-rwx ~/.ssh
```

To reach the login Pod from your workstation, prefer SSH agent forwarding (`ssh -A`) over copying private keys onto the shared filesystem. Don't use agent forwarding for the next hop from the login Pod to a compute node. See [Connect with ProxyJump](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md#connect-with-proxyjump) for why, and use `ProxyJump` instead.

> [!WARNING]
>
> Don't put `newgrp slurm-users` in `~/.bashrc` or `~/.profile`. It spawns a new shell that makes non-interactive SSH sessions unresponsive, which freezes SCP, SFTP, rsync, and git-over-SSH transfers. If you must change the active group at login, guard it so it runs only in interactive shells:
>
> ```bash theme={"system"}
> [[ $- != *i* ]] && return
> newgrp slurm-users
> ```
