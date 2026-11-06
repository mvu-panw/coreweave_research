# 1. Set up a Slurm cluster

Source: https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster

# 1. Set up a Slurm cluster

> Connect to a Slurm login node through SSH and verify cluster access to begin training on SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This is the first part of the **Train on SUNK** tutorial series. In this part, you connect to your Slurm cluster's login node, verify that the cluster is operational, confirm that shared storage is available for training data, and prepare the cluster to run software using containers. Completing these steps confirms that you can reach the cluster, submit jobs, move data into persistent storage, and install software, all of which are prerequisites for the training workflow in the parts that follow.

This tutorial is for users who have access to an existing SUNK cluster and want to prepare it for running training workloads.

## Prerequisites

Before you begin, make sure you have the following:

* Access to a SUNK cluster running on CoreWeave Kubernetes Service (CKS).
* A user account on the Slurm cluster, with your SSH public key registered through your organization's identity provider. If you don't have access, contact CoreWeave support.
* `kubectl` access to the CKS cluster hosting Slurm, so you can look up the login node's external address.
* An SSH client on your local machine, along with the matching private key.

## Connect to the Slurm login node with SSH

In this section, you locate the address of the Slurm login node and open an SSH session to it. The login node is the entry point for submitting Slurm jobs and managing data on the cluster.

> [!NOTE]
>
> Customer identity providers (IdPs) manage user access to Slurm clusters, federated into a cluster-side directory service. CoreWeave grants access based on allowed users' public SSH keys. For assistance, contact CoreWeave support.

### Acquire the IP address or DNS record of the login node

The `slurm-login` Service on your CKS cluster provides information about how to connect to the login node, including the external IP address or DNS record, if there is one.

To get the login service's IP address or DNS record, use `kubectl get svc slurm-login`.

```bash title="Obtain the external IP address" theme={"system"}
kubectl get svc slurm-login
```

The `EXTERNAL-IP` field in the output is the target IP address for SSH access.

```text title="Example output" theme={"system"}
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)   AGE
slurm-login   LoadBalancer   192.0.2.100      203.0.113.100    22/TCP    2d21h
```

Use SSH to log in to the login node with either this IP address, or the DNS record created for the login node if there is one.

```bash title="Log in with SSH" theme={"system"}
ssh -i /path/to/ed25519_private_key [USERNAME]@[EXTERNAL-IP]
```

> [accordion] See an example: SSH
>
> In this example, the username is `exampleuser`, and the target IP address is `203.0.113.100`.
>
> ```bash title="Example: Log in with SSH" theme={"system"}
> ssh -i ~/.ssh/ed25519-key exampleuser@203.0.113.100
> ```

On successful login, the cluster presents a welcome message, along with a command prompt:

```text theme={"system"}
Welcome to a CoreWeave Slurm HPC Cluster

[USERNAME]@slurm-login-0:~$
```

You're now logged in to the Slurm login node, and from here you can start to run Slurm commands.

## Verify the Slurm cluster

With an SSH session open on the login node, the next step is to confirm that Slurm itself is healthy and that compute nodes are reachable. To verify that your Slurm cluster is working as expected, run a basic Slurm job.

### Check for available nodes

First, check how many nodes you have available with `sinfo`:

```bash title="List nodes in idle or mix states" theme={"system"}
sinfo -N --states=idle,mix
```

The `-N` flag instructs `sinfo` to list each node individually. You can add criteria to this query with the `--states=` flag.

`--states=idle,mix` limits the output to nodes in the `idle` and `mix` states. Nodes in these states are [available to run workloads](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md).

`sinfo` returns a list of nodes that match your criteria:

```text title="Example sinfo output" theme={"system"}
NODELIST       NODES  PARTITION      STATE
slurm-h100-10      1  h100           idle
slurm-h100-11      1  all*           idle
slurm-h100-12      1  h100           mix
slurm-h100-13      1  all*           mix
slurm-h100-14      1  h100           idle
slurm-h100-15      1  all*           mix
```

In this example, `sinfo` lists six available nodes.

### Submit an interactive job

`srun` is the Slurm command that submits an interactive job to the Slurm cluster. Use it to discover the hostname of each available node.

In the following command, replace `[AVAILABLE-NODES]` with the number of available nodes in your Slurm cluster:

```bash title="Example: Find the hostname on a specified number of nodes" theme={"system"}
srun -N [AVAILABLE-NODES] hostname
```

The `-N` flag, when used with `srun`, requests the specified number of Slurm nodes. For example, `-N 6` requests six nodes to run a job.

If you request more nodes than are currently available, `srun` remains in a `Pending` state until all of the requested nodes become available.

The `hostname` command runs on each requested node, and prints the name of the machine for each node:

```text title="Example output" theme={"system"}
slurm-h100-10
slurm-h100-11
slurm-h100-12
slurm-h100-13
slurm-h100-14
slurm-h100-15
```

If you run into any errors such as "Invalid partition name specified", or "Invalid account or account/partition combination specified", you likely haven't been added as a Slurm user. To add yourself, follow these steps, replacing `[USERNAME]` with your username:

```bash title="Add yourself as a Slurm user" theme={"system"}
sudo su
sacctmgr create user -i account=root adminlevel=admin name=[USERNAME]
exit
```

If your Slurm cluster uses accounts other than `root`, run the preceding command for each account you need to be added to.

After completing this section, you have confirmed that the Slurm controller can see available compute nodes and that you can submit interactive jobs to them.

## Verify data access

Now that the cluster is reachable and jobs can run, the next prerequisite for training is making sure your data lives in persistent storage that every node can read. Before you can run a training job, you'll need to transfer your data into the cluster's persistent storage. POSIX-compliant shared storage on your cluster is persistent Distributed File Storage (DFS). Anything stored in DFS is available across all the nodes of your Slurm cluster, and remains even when nodes are replaced.

> [!WARNING]
>
> Any data placed on a node *outside* DFS doesn't persist through node restarts or replaced nodes.

Shared DFS storage is mounted on login and compute nodes. Data is usually mounted in `/mnt`, in directories such as `/mnt/home` and `/mnt/data`.

### Check available DFS space

See how much space is available with `df -H`.

> [accordion] See an example: `df -H`
>
> In this example, the mount directories are `/mnt/data` and `/mnt/home`.
>
> ```bash title="Example: Check available space" theme={"system"}
> df -H /mnt/data /mnt/home
> ```
>
> ```text title="Example output" theme={"system"}
> Filesystem                                                   Size  Used Avail Use% Mounted on
> 100.121.2.187:/k8s/pvc-7236f9d2-d948-42b1-b909-ff634723fcc2   11T     0   11T   0% /mnt/data
> 100.121.2.182:/k8s/pvc-f1ada11a-11f3-4b73-84f0-8b01e8c4bfae  1.1T  4.2M  1.1T   1% /mnt/home
> ```

### Copy files from the local machine to the Slurm cluster

Recommended tools for transferring data are `scp` or `rsync`.

`rsync` is faster for large directories. If interrupted, pick up where you left off by reissuing the command.

> [accordion] See an example: `rsync` and `scp`
>
> To copy data from the local machine to the remote machine, use these commands, replacing `[USERNAME]` with your username and `[IP-ADDRESS]` with the remote machine's IP address:
>
> Using `rsync`:
>
> ```bash theme={"system"}
> rsync -avz -e "ssh -i ~/.ssh/id_ed25519" ./data/ [USERNAME]@[IP-ADDRESS]:/remote/path/
> ```
>
> Using `scp`:
>
> ```bash theme={"system"}
> scp -i /path/to/ed_25519-private-key /path/to/local-file-to-copy [USERNAME]@[IP-ADDRESS]:/remote/path
> ```
>
> To copy data from the remote machine to the local machine, reverse the commands:
>
> Using `rsync`:
>
> ```bash theme={"system"}
> rsync -avz -e "ssh -i ~/.ssh/id_ed25519" [USERNAME]@[IP-ADDRESS]:/remote/path/ local-path
> ```
>
> Using `scp`:
>
> ```bash theme={"system"}
> scp -i /path/to/ed_25519-private-key [USERNAME]@[IP-ADDRESS]:remote-file-to-copy local-path
> ```

## Install software on the Slurm cluster

With data in place, the final preparation step is making sure the software your training job needs is available on compute nodes in a way that survives reboots and node replacements. This section explains the recommended approaches and why they exist.

> [!WARNING]
>
> Installing software directly onto Slurm compute nodes isn't considered best practice. Instead, use Pyxis with Enroot, a container-based solution that manages and isolates software environments.

Slurm runs on top of CoreWeave Kubernetes Service (CKS), where the operating system runs in an ephemeral container. Because of this, system software installed on the operating system disk of login and `slurmd` Pods doesn't persist on the operating system disk through reboots.

Several methods can install software permanently on the cluster, each suited to different use cases.

| Pyxis and Enroot | s6-overlay | Distributed File System (DFS) |
| - | - | - |
| Recommended for cases where compute nodes require a lot of software. | Installs software on Slurm login and compute nodes as part of the SUNK deployment. Recommended for installing development tools, such as text editors and `git`. | Recommended for persistent storage. |

> [!TIP]
>
> CoreWeave AI Object Storage is an S3-compatible solution for object storage, recommended for storing and loading model data and checkpoints. It provides Node-local caching on GPUs and cross-Zone support.

### Install software as containers using Pyxis and Enroot

Running high-performance code on GPUs presents its own challenges. CoreWeave uses [Pyxis](https://github.com/NVIDIA/pyxis), a container environment developed by NVIDIA as a plugin for use with Slurm in GPU-accelerated environments.

Pyxis uses `enroot` to run containers, which lets unprivileged cluster users run tasks in containers with `srun`. This provides a safer way to manage software on Slurm nodes by encapsulating software environments, and makes them reproducible.

Pyxis with Slurm enables interactive development in your container environment. The following sections describe how to do this with an interactive shell on a compute node using `enroot` and Pyxis with Slurm.

#### Set credentials to pull Pyxis containers

To pull containers from protected repositories, set the appropriate credentials. First, create an `enroot` directory, then create a `.credentials` file within that directory:

```bash title="Create the credentials directory" theme={"system"}
mkdir -p ~/.config/enroot
touch ~/.config/enroot/.credentials
```

Add repository credentials to this file using [`netrc` file format](https://github.com/NVIDIA/enroot/blob/1cebc0c8de1295e11a95c15d37029f759790a11a/doc/cmd/import.md).

> [accordion] See an example: Credential formats
>
> **NVIDIA NGC:** Generate an NGC API key if you don't already have one. Then, open `~/.config/enroot/.credentials` and enter the following in the file, replacing `[API-KEY]` with your NGC key:
>
> ```text title="NGC example" theme={"system"}
> machine nvcr.io login $oauthtoken password [API-KEY]
> ```
>
> **Docker Hub:** Add the following information into your `~/.config/enroot/.credentials` file, replacing `[LOGIN]` with your Docker Hub login and `[PASSWORD]` with your password.
>
> ```text title="Docker Hub example" theme={"system"}
> machine auth.docker.io login [LOGIN] password [PASSWORD]
> ```

If `enroot` can't find your credentials, export the `ENROOT_CONFIG_PATH` variable to point to the directory where your credentials are stored, ideally in your `.bashrc` file, so that it's set persistently:

```bash theme={"system"}
export ENROOT_CONFIG_PATH=${HOME}/.config/enroot/
```

#### Pull and modify a container using Enroot

Pulling and modifying containers on compute nodes can be useful for debugging or for creating a container image for the first time.

First, create an interactive session on a compute node. In this case, you request an interactive session on an exclusive H100 node in the H100 partition.

```bash theme={"system"}
srun -p h100 --exclusive --cpus-per-task=16 --mem=64G --pty bash -i
```

Next, use `enroot` to import and run an image from Docker Hub.

```bash theme={"system"}
enroot import docker://ubuntu
```

Use the `create` command to save the Docker image as a squash file (`.sqsh`).

```bash theme={"system"}
enroot create ubuntu.sqsh
```

Finally, run `enroot` with the `start` command using the `--rw` flag. This makes the container root system readable and writable, so any filesystem changes made after you start the container persist.

```bash theme={"system"}
enroot start --rw ubuntu
```

You can also mount local files on the container with the `-m` flag.

> [!NOTE]
>
> For more information, see [the official Enroot documentation](https://github.com/NVIDIA/enroot/blob/master/doc/usage.md).

#### Pull and modify a container using Slurm

> [!TIP]
>
> Using Slurm to pull and modify containers is recommended when containers run as expected. If you experience difficulties running containers with Slurm, try using `enroot` directly instead, as described in the preceding section.

To pull and modify a container using Slurm, first create an interactive bash session with Slurm.

From the login node, pull your container, and save it as a squash file. In this example, you pull the latest PyTorch container from CoreWeave and save it as a squash file.

```bash theme={"system"}
srun \
  --cpus-per-task=8 --mem=32G \
  --container-image=ghcr.io#coreweave/ml-containers/nightly-torch:es-actions-8e29075-base-25011003-cuda12.6.3-ubuntu22.04-torch2.7.0a0-vision0.22.0a0-audio2.6.0a0 \
  --container-save=/mnt/home/username/nightly-torch.sqsh \
  echo "hello world"
```

Use the flag `--container-save` to specify where to save the container, and execute an `echo` command to specify a command for `srun`.

#### Mount the container

With [container-mounts](https://github.com/NVIDIA/pyxis/wiki/Usage), you can mount a local filesystem into the container. In the following example, `/mnt/home` is mounted from the local cluster to `/mnt/home` on the container, and an interactive job launches on a GPU node.

```bash theme={"system"}
srun -C gpu --cpus-per-task=16 --mem=64G \
  --container-image=/mnt/home/username/nightly-torch.sqsh \
  --container-mounts=/mnt/home:/mnt/home \
  --pty bash -i
```

Running this command launches an interactive development shell on a GPU node. In this example, a test script (`test_script.py`) runs from `/mnt` and tests the CUDA installation.

> [!NOTE]
>
> Inside a Pyxis or Enroot container, `/tmp` is backed by `tmpfs` (RAM), not the Node's NVMe storage. If your code or libraries write large temporary files to `/tmp`, set `TMPDIR` to an NVMe-backed path instead. For details, see [Node-local storage and `/tmp` on Slurm nodes](https://docs.coreweave.com/products/sunk/manage_sunk/node-local-storage-and-tmp). If `sudo`, `chown`, or Slurm CLI commands fail inside the container, see [How do I run containers with Pyxis and Enroot in Slurm?](https://docs.coreweave.com/support/sunk/articles/how-do-i-run-containers-with-pyxis-and-enroot-in-slurm).

```python title="CUDA installation test" theme={"system"}
import torch
print(torch.version.cuda)
print(torch.cuda.device_count())
print(torch.cuda.get_device_name())
```

Test this interactively by running:

```bash title="Run the CUDA installation test" theme={"system"}
python /mnt/home/username/test_script.py
```

Exiting the interactive shell doesn't delete the container or the squash file, and the test file `test_script.py` persists in `/mnt/home/username`. However, no changes to the root filesystem of the container files themselves are saved.

In the following example command, you launch an interactive session with the `nightly-torch` container and specify that it saves (using `--container-save`) as `new-nightly-torch.sqsh`. Now, you can make changes to the container itself, and they persist in the new squash filesystem, `new-nightly-torch.sqsh`, after you exit the container.

```bash theme={"system"}
srun -C gpu \
  --container-image=/mnt/home/username/nightly-torch.sqsh \
  --container-mounts=/mnt/home:/mnt/home \
  --container-save /mnt/home/username/new-nightly-torch.sqsh \
  --pty bash -i
```

### Install software at deployment time using s6-overlay

> [!TIP]
>
> As a best practice, install the same packages on compute and login nodes to avoid user confusion. Limit installed packages to usability applications such as `git`, text editors, and basic command-line tools. Configure this where you configure Slurm application values, usually in a GitOps repository maintained by a Slurm administrator.

Use s6-overlay to install software on the Slurm login and compute nodes at cluster initialization time, or to create long-running jobs, such as services.

For compute nodes, define script details in the `compute.s6` section of the Slurm `values.yaml` file. For login nodes, define script details in the `login.s6` section of the Slurm `values.yaml` file.

Each script needs a name, a type, and the script itself in `bash`.

> [accordion] See an example: Installing `rclone` using s6-overlay
>
> ```yaml title="Example compute.s6 stanza" theme={"system"}
> compute:
>   s6:
>     packages:
>       type: oneshot
>       script: |
>         #!/usr/bin/env bash
>         apt-get update
>         apt -y install rclone screen git
> ```

### Install software in a persistent DFS mounted directory

Software installed in mounted DFS directories, such as your home directory or `/mnt/data`, persists on nodes through reboots or replacements.

> [!WARNING]
>
> In general, only follow instructions for installing software that doesn't require root access or administrative privileges.

> [accordion] See an example: Conda
>
> You can often install Python environments without root privileges.
>
> In this example, you create a [conda](https://docs.conda.io/en/latest/) environment called `myenv` using Python version 3.11 in a persistent DFS mounted directory at `/mnt/data`.
>
> First, initialize conda to use `bash` with [`conda init`](https://docs.conda.io/projects/conda/en/stable/commands/init.html#conda-init). Then, source your `.bashrc` file.
>
> ```bash theme={"system"}
> /opt/conda/bin/conda init bash
> source ~/.bashrc
> ```
>
> Next, create the conda environment with the desired specifications, where `--prefix` targets the location in which to store the environment.
>
> ```bash theme={"system"}
> conda create --prefix /mnt/data/myenv python=3.11
> ```
>
> Finally, activate the environment.
>
> ```bash theme={"system"}
> conda activate /mnt/data/myenv
> ```

You have now connected to your Slurm cluster, confirmed that nodes are available, verified shared storage, and reviewed the options for installing software. The cluster is ready for the training workflow covered in the next part of this tutorial series.
