# Choose a SUNK operation mode

Source: https://docs.coreweave.com/products/sunk/choose-operation-mode

# Choose a SUNK operation mode

> Pick SUNK Standard or SUNK Self-Service based on who operates the control plane and what you need to configure

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SUNK runs in two operation modes. In SUNK Standard, you deploy and operate the SUNK Helm charts yourself. In SUNK Self-Service, CoreWeave operates the cluster for you from a single `SunkCluster` resource. In both modes, Slurm nodes run as Kubernetes Pods, and your users connect to a login node and submit jobs with the same Slurm commands.

This page helps you pick a mode for a new cluster. For what SUNK is and how it works, see [About SUNK](https://docs.coreweave.com/products/sunk.md). For the Self-Service product in depth, see [About SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md).

## SUNK Self-Service

CoreWeave provisions and operates the cluster from one `SunkCluster` resource: the compute nodes, the Slurm control plane, login Pods, shared storage, and user access. You declare the cluster you want, and CoreWeave's managed control plane keeps the running cluster reconciled to it, including when you change node counts or upgrade the SUNK version.

You can create and manage a Self-Service cluster in two ways. The Cloud Console is a guided form that can also create the CoreWeave Kubernetes Service (CKS) cluster, enable the SCIM API for user provisioning, and create the Identity and Access Management (IAM) group that grants cluster access. The `SunkCluster` custom resource (CR) path applies the same resource with `kubectl`, which fits a GitOps workflow. Both paths submit the same resource.

SUNK Self-Service runs SUNK 8.0 and later. It's the recommended mode for a new cluster on CKS. For the full list of what it supports, see [Supported configurations](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md#supported-configurations).

## SUNK Standard

You deploy and operate the `sunk` and `slurm` Helm charts, usually through ArgoCD or another GitOps pipeline. Every chart value is yours to set, and you own each upgrade between SUNK releases.

SUNK Standard runs SUNK 7.x and SUNK 8.0 and later. It's also the only mode that runs outside CoreWeave. [SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md) is SUNK Standard on a Kubernetes cluster that CoreWeave doesn't operate.

## Compare the modes at a glance

| | SUNK Standard | SUNK Self-Service |
| - | - | - |
| Ideal for | Teams with an existing Helm or ArgoCD pipeline, or that need chart-level control of the cluster | New clusters on CKS, and teams that want CoreWeave to operate the Slurm control plane |
| Who operates the Slurm control plane | You, through the Helm charts | CoreWeave, through its managed control plane |
| How you configure the cluster | Values files for the `sunk` and `slurm` charts | One `SunkCluster` resource |
| Interfaces | Helm, ArgoCD or another GitOps tool, and `kubectl` | Cloud Console, and `kubectl` with the `SunkCluster` CR |
| SUNK versions | 7.x and earlier, and 8.0 and later | 8.0 and later |
| Runs outside CoreWeave | Yes, as [SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md) | No |

## Choose based on what you need

Start from what your cluster has to do. Either mode meets most requirements, so the following lists name only the ones that decide it. Migration between modes isn't supported, so if you expect to need a Standard-only capability later, start on SUNK Standard.

### When to pick SUNK Standard

Pick SUNK Standard if you need any of the following:

* **Custom controller, login, or `slurmd` images.** A Self-Service cluster runs the images CoreWeave publishes. You choose the SUNK, Slurm, CUDA, and Ubuntu versions, not the image. See [Create custom images for SUNK Standard](https://docs.coreweave.com/products/sunk/optimize_workloads/custom-images.md).
* **An LDAP directory for user identity.** Self-Service provisions users through SCIM only. See [Manage users with nsscache on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache.md), which covers LDAP. On SUNK 7.x and earlier, the [directory service guide](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/directory-services.md) also applies.
* **Custom Slurm plugin files**, such as a `job_submit.lua` or `cli_filter.lua` script, or any other file you have to mount into `/etc/slurm` yourself. Slurm configuration keys aren't a reason to pick Standard, because `spec.slurmConfig` carries them in Self-Service. A file you have to place on disk is. See [Customize cluster behavior with Lua plugins on SUNK Standard](https://docs.coreweave.com/products/sunk/optimize_workloads/lua-plugins.md).
* **Node affinity and tolerations on each compute node group**, for example, to bind a NodeSet to a specific Node Pool. In Self-Service, each entry in `spec.nodes` sets a name, an instance type, a node count, and whether the group hosts the control plane. See [Bind NodeSets to Node Pools for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md) and [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md).
* **Node Pools that already exist in your cluster.** SUNK Self-Service doesn't support existing Node Pools. It creates its own Node Pools from `spec.nodes`.
* **An existing Helm or ArgoCD pipeline** that you want to keep as the source of truth for the cluster. See [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md).
* **SUNK 7.x.** Self-Service starts at SUNK 8.0.
* **A Kubernetes cluster outside CoreWeave.** SUNK Anywhere is SUNK Standard. See [About SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md).

### When to pick SUNK Self-Service

Pick SUNK Self-Service if you want any of the following:

* **CoreWeave to operate the Slurm control plane**, login Pods, shared storage, and user provisioning, and to keep component versions aligned when you upgrade.
* **A guided path to a first cluster.** If you're new to SUNK, or to running Slurm on Kubernetes, start with Self-Service.
* **The Cloud Console** to create the cluster, including the CKS cluster, SCIM setup, and the IAM group.
* **A GitOps flow that applies one resource** instead of two charts and their values files.

> [!NOTE]
>
> The following are available in both modes, so they aren't a reason to pick SUNK Standard: the SUNK Pod Scheduler, Pyxis and Enroot containers, Docker and privileged containers, custom s6 scripts, custom Prolog and Epilog scripts, the Slurm REST API, GPU Straggler Detection, and Slurm configuration keys.

## SUNK versions by mode

| SUNK version | SUNK Standard | SUNK Self-Service |
| - | - | - |
| 8.0 and later | Yes | Yes |
| 7.x and earlier | Yes | No |

Each SUNK release pairs with one Slurm version. See [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md).

## Next steps

* To create a SUNK Self-Service cluster, see [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md). For an end-to-end walkthrough of the CR path, see [Get started with SUNK Self-Service using the SunkCluster CR](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md).
* To deploy SUNK Standard, see [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md) for the ArgoCD app-of-apps pattern, then [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md). Both pages predate SUNK 8.0, so check their key names against the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md).
* For every configurable field in either mode, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference) or the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).
