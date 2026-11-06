# About SUNK

Source: https://docs.coreweave.com/products/sunk

# About SUNK

> Run Slurm on Kubernetes with SUNK, in the SUNK Standard or SUNK Self-Service operation mode

# Training and inference on one cluster

CoreWeave SUNK runs Slurm on Kubernetes, letting both batch training jobs and Kubernetes inference workloads share the same GPU pool. You get Slurm scheduling with Kubernetes deployment and higher utilization without running two separate stacks.

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

![SUNK logo](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/SUNK-v4_1.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=bc5e20032bf26efb0b03a7f35027d656)

SUNK is CoreWeave's system for running [Slurm](https://slurm.schedmd.com/overview.html) on Kubernetes. Slurm nodes run as Kubernetes Pods on CoreWeave Kubernetes Service (CKS), so Slurm jobs and Kubernetes workloads share the same compute. The Slurm cluster also gains the Node lifecycle management, observability, and GitOps tooling that Kubernetes brings.

Without SUNK, a team picks Slurm or Kubernetes, or runs both and splits its GPUs between them. With SUNK, one pool of compute serves batch training jobs through Slurm and long-running or bursty services through Kubernetes. The [SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/discover_sunk/scheduler.md) arbitrates between them on the same Nodes.

> [!NOTE]
>
> In SUNK, Slurm **nodes** run in Kubernetes **Pods**. These aren't the same as Kubernetes Nodes, which are the worker machines that run the Pods. To distinguish between them, this page capitalizes **Kubernetes** Nodes.

## Operation modes

SUNK runs in two operation modes. They run the same Slurm, and your users connect to a login node and submit jobs the same way in either.

**SUNK Standard.** You deploy and operate the `sunk` and `slurm` Helm charts, usually through ArgoCD or another GitOps pipeline. You set every chart value and own each upgrade. SUNK Standard runs SUNK 7.x and SUNK 8.0 and later, and it's the mode that runs outside CoreWeave, as [SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md).

**SUNK Self-Service.** CoreWeave provisions and operates the cluster from a single `SunkCluster` resource that you manage through the Cloud Console or `kubectl`. SUNK Self-Service runs SUNK 8.0 and later and is the recommended mode for a new cluster on CKS.

> [card] [Choose a SUNK operation mode](https://docs.coreweave.com/products/sunk/choose-operation-mode.md)
>
> What each mode gives you, and which one to pick for what your cluster has to do.

> [card] [About SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)
>
> What CoreWeave provisions and operates for you, and what stays on your side.

## SUNK Standard in depth

Two Helm charts make up a SUNK Standard deployment. The `sunk` chart installs the SUNK operator and the cluster-wide components it depends on, such as the MOCO MySQL operator. It can also install the NVIDIA device plugin, which is off by default. The `slurm` chart describes one Slurm cluster: its control plane, login Pods, compute node definitions, Slurm configuration, and accounting database.

In SUNK 7.x, the `slurm` chart rendered every component of the cluster directly. In SUNK 8.0 and later, the chart renders a `SlurmCluster` resource for the control plane, login Pods, and accounting, plus the compute NodeSets. The SUNK operator builds the cluster from them. Most keys keep their names, but the defaults you don't set now come from the operator. Upgrading from 7.x to 8.0 isn't a routine `helm upgrade`, so read the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md) first.

Start with these pages:

* [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md) for the ArgoCD app-of-apps pattern and the `NodeSet` sync customization. Its examples predate SUNK 8.0, so check key names against the release note.
* [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md) for node definitions, partitions, and images.
* [Bind NodeSets to Node Pools for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md) to place Slurm nodes on specific CKS Node Pools.
* [SUNK parameter reference](https://docs.coreweave.com/products/sunk/reference/sunk-parameters.md) and [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for every chart value.

## How SUNK works

The following pieces make SUNK work:

* **Compute and login nodes are Pods.** Each Slurm compute node is a Pod running `slurmd`, placed one-to-one on a Kubernetes Node. Login nodes are Pods with exposed IP addresses that users connect to over SSH. See [Compute and login nodes](https://docs.coreweave.com/products/sunk/discover_sunk/compute_and_login_nodes.md).
* **NodeSets define compute.** A NodeSet declares a group of Slurm nodes: image, resource requests, affinity, and replica count. Its controller creates the Pods and scales the set. See [NodeSet](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md).
* **The Syncer keeps both sides in agreement.** It mirrors state between Slurm nodes and their Pods in both directions, so a Pod that isn't ready shows as a drained Slurm node. See [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md).
* **The SUNK Pod Scheduler shares Nodes.** Pods that name it as their scheduler are placed through Slurm's own scheduling logic, on the same Nodes as Slurm jobs and under Slurm's priority and preemption rules. See [SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/discover_sunk/scheduler.md).
* **SlurmCluster carries cluster-wide Slurm configuration** and generates `topology.conf` from Node labels. See [SlurmCluster](https://docs.coreweave.com/products/sunk/discover_sunk/slurmcluster.md).
* **Slurm runs from images CoreWeave publishes.** The `slurmd` images ship per CUDA version, built on NCCL test images. Controller and login images ship per Ubuntu version. See [Slurm images](https://docs.coreweave.com/products/sunk/reference/slurm-images.md).

## Key features

SUNK supports the following:

* Containerized jobs through Pyxis and Enroot, including Docker workflows. See [Use Docker in SUNK](https://docs.coreweave.com/products/sunk/run_workloads/docker-in-docker.md).
* Topology-aware scheduling with Slurm's tree and block plugins. See [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md).
* GPU Straggler Detection for multi-node training jobs. See [Introduction to GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md).
* Prolog and Epilog scripts that prepare a node before a job and clean up after it. See [Run Prolog and Epilog scripts on SUNK](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md).
* s6 scripts that install software and configure Slurm nodes at startup. See [Run custom scripts with s6](https://docs.coreweave.com/products/sunk/run_workloads/run-scripts-with-s6.md).
* Task plugins and cgroups for CPU, memory, and GPU binding. See [Manage resource binding with task plugins](https://docs.coreweave.com/products/sunk/optimize_workloads/task-plugins.md).
* User provisioning from CoreWeave Identity and Access Management (IAM) through SCIM, so POSIX identities, SSH keys, and Slurm accounts follow your identity provider. See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md).
* On SUNK Standard only: custom images, Lua plugin files, and LDAP directories. [Choose a SUNK operation mode](https://docs.coreweave.com/products/sunk/choose-operation-mode.md) has the full list.

## Next steps

* [Choose a SUNK operation mode](https://docs.coreweave.com/products/sunk/choose-operation-mode.md) if you haven't picked one yet.
* [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md) to start a SUNK Self-Service cluster from the Cloud Console or the `SunkCluster` CR.
* [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md) to deploy SUNK Standard with ArgoCD.
* [Train on SUNK](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk.md) to set up a cluster, submit a training job, and monitor it.
