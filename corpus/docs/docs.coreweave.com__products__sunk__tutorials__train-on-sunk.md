# Train on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk

# Train on SUNK

> Multi-part tutorial for training a model on SUNK using Slurm, from cluster setup to job monitoring

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This multi-part tutorial walks you through training a model on CoreWeave SUNK. You start by setting up your first Slurm cluster and finish by monitoring training jobs in Grafana. Along the way, you'll interact with Slurm, submit jobs, and observe their performance.

This tutorial is for users who are new to SUNK or to running Slurm jobs on Kubernetes, and who want a guided introduction before running production workloads.

Use this tutorial to learn the SUNK job lifecycle before you adapt the workflow to your own training workloads.

> [card] What you'll need
>
> Before you start, you must have:
>
> * A working SUNK cluster deployed on CoreWeave Kubernetes Service (CKS) with a GPU Node Pool. If you need a cluster, follow [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md).
> * `git`, `ssh`, and `scp` installed on a local machine.
> * An SSH public key registered for your account with your organization's identity provider (or through the Cloud Console), so you can reach the Slurm login node.
> * Basic familiarity with [Slurm](https://slurm.schedmd.com/overview.html)

## Tutorial steps

Complete these pages in order:

1. [Set up your first Slurm cluster](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/1-set-up-slurm-cluster.md)
2. [Submit your first training job](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job.md) to learn about SUNK, Slurm, and supporting utilities.
3. [Submit a more complex training job](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md) that more closely reflects a real-world scenario.
4. [Monitor training jobs using CoreWeave Grafana](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/4-monitor-jobs.md).

## Tutorial background

Before you start, review the key concepts, preinstalled software, and tips in the following sections.

### Key concepts

The following sections describe the key Slurm, SUNK, and high-performance computing (HPC) cluster concepts used throughout this tutorial.

#### Slurm and SUNK

The tutorial uses the following Slurm and SUNK concepts:

* **Job:** a compute workload submitted by a user. A job can be a small task that requires a single CPU for a few seconds. A large job can require thousands of CPUs and GPUs for days or even weeks.
* **Login nodes:** the entry points for users to access the Slurm cluster. In SUNK, they are Kubernetes Pods where users prepare data, submit jobs, and check job status. Login nodes are not intended for heavy computation and don't typically have a GPU.
* **Compute nodes:** the machines that execute the jobs submitted by users. In SUNK, they are Kubernetes Pods that run `slurmd` and map to physical Nodes in the cluster.
* **Syncer:** a Kubernetes Pod that synchronizes the Kubernetes state with the Slurm state.
* **Controller:** a Kubernetes Pod that runs the Slurm controller, `slurmctld`, and also schedules jobs.

#### High-performance computing cluster components

The tutorial uses the following high-performance computing cluster components:

* **Network:** interconnects nodes for communication and data transfer. A CoreWeave HPC cluster usually has two networks: Ethernet for normal communications, including user sessions and storage, and a high-performance RDMA fabric, either InfiniBand or RoCE (NVIDIA Spectrum-X) depending on instance type, for performance-critical traffic such as node-to-node communication in a large training job. See [HPC Interconnect](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) for details.
* **Observability:** metrics that describe the performance of Slurm jobs and nodes, collected and consolidated for monitoring job and cluster performance using tools such as [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md).
* **Storage:** provides space for data and applications. This can be either traditional file storage or object storage, such as [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md).

### Preinstalled software

The following tools are preinstalled on SUNK login nodes:

* [Miniconda](https://www.anaconda.com/docs/getting-started/installation): Initialize Miniconda in your shell using `/opt/conda/bin/conda init bash`.
* [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html): a fast, lightweight alternative to `conda`. Initialize it in your shell with `micromamba shell init; source ~/.bashrc`.
* Java OpenJDK
* `s3cmd` and the AWS CLI for interacting with AI Object Storage. For large object storage transfers, install and use `rclone` or `s5cmd` in a container or `conda` environment. When you use `s5cmd` with [AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md), use the [CoreWeave fork of `s5cmd`](https://github.com/coreweave/s5cmd). See [Migrate data to AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/migrate-data.md#migrate-data-with-s5cmd).

> [!TIP]
>
> To develop on Slurm compute nodes, create an interactive Slurm session and [tunnel through VS Code](https://docs.coreweave.com/products/sunk/access_sunk/vs-code-with-slurm.md).

### Command conventions

The following guidelines clarify where to run commands and how to use placeholders in the examples.

* Run all commands in this tutorial on the Slurm login node, except for `ssh` or `scp` commands. Commands run inside an interactive Slurm session (`srun --pty`) execute on the allocated compute node instead.
* Bracketed uppercase values in code examples, such as `[USERNAME]`, are placeholders. Replace them with your own values when you run commands in your environment.

> [!CAUTION]
>
> **Don't use SSH to access compute nodes**
>
> SSH is the preferred method to access Slurm login nodes. However, don't use SSH to access Slurm compute nodes directly to run tasks. Direct access bypasses Slurm. It can interfere with running jobs, cause nodes to drain unintentionally, or lead to a temporary loss of resources. For debugging purposes only, use SSH to access Slurm compute nodes.

## Third-party frameworks

This tutorial focuses on a single training workflow, but SUNK supports many machine learning (ML) frameworks. Frameworks that run on Slurm or in Linux containers work on SUNK. Examples include PyTorch, TensorFlow, JAX, DeepSpeed, Megatron-LM, and Ray.

> [card] [Run Ray on SUNK](https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk.md)
>
> Launch and use a Ray cluster through Slurm on SUNK.

> [card] [Third-party frameworks](https://docs.coreweave.com/products/cks/clusters/frameworks/introduction.md)
>
> See popular AI and ML frameworks with links to CKS and SUNK guides.

## Additional resources

The tutorial assumes basic familiarity with Slurm. To learn more about Slurm, see the following resources:

* [SchedMD's official documentation for Slurm commands](https://slurm.schedmd.com/documentation.html)
* [SchedMD's PDF command cheat sheets](https://slurm.schedmd.com/pdfs/summary.pdf)
