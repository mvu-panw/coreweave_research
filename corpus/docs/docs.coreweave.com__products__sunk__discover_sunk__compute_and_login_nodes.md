# Compute and login nodes

Source: https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes

# Compute and login nodes

> Understand the roles of SUNK compute nodes and login nodes as Kubernetes Pods running Slurm

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

## Compute nodes

SUNK **compute nodes** are Kubernetes Pods running `slurmd`. They're mapped to physical Nodes in the cluster. Jobs run within Slurm cgroups on these Nodes, which are typically large, feature high memory and fast networking, and have either GPUs or significant CPU resources. Compute nodes are the "workhorses" of the Slurm cluster. They define and manage the specific hardware used to run Slurm jobs, and they handle the resources used to run jobs submitted to Slurm.

> [!NOTE]
>
> In SUNK, Slurm nodes run in Kubernetes Pods. Slurm nodes are **not the same** as Kubernetes Nodes, the worker machines that run Kubernetes Pods. To maintain a distinction between the two in this documentation, Kubernetes **Nodes** are capitalized while Slurm **nodes** are not.

## Login nodes

SUNK **login nodes** let you access your Slurm cluster. They're Kubernetes Pods with exposed IP addresses that enable connections, so you can prepare data, submit jobs, and check job statuses. They aren't intended for heavy computation, so they don't typically have a GPU. Submit your work to compute nodes with `srun` or `sbatch` instead of running it on the login node.

> [!WARNING]
>
> Don't run compute-heavy work directly on a Slurm login node. Login nodes are shared and meant for job submission, file management, and monitoring. Running workloads directly consumes shared resources and can make the login node unresponsive for everyone. This includes high-concurrency data transfers, such as s5cmd or Rclone writing to NFS-backed volumes like CoreWeave Distributed File Storage. Submit work, including large parallel transfers, to compute nodes with `srun` or `sbatch`.

> [!TIP]
>
> With SUNK, you can create flexible [Compute node definitions](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md) to meet the specific resource requirements of your workloads.
