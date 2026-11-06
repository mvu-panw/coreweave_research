# About SUNK Self-Service

Source: https://docs.coreweave.com/products/sunk/about-self-service-sunk

# About SUNK Self-Service

> The operation mode in which CoreWeave runs SUNK for you on CKS. Declare a Slurm cluster as one SunkCluster resource.

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

**SUNK Self-Service** is the operation mode in which CoreWeave deploys SUNK for you on CoreWeave Kubernetes Service (CKS). You declare a Slurm cluster as a single Kubernetes resource, and CoreWeave provisions and operates it for you, including compute nodes, the Slurm control plane, login Pods, shared storage, and user access.

SUNK Self-Service is for teams that want SUNK without taking on the operational burden of installing the SUNK Helm charts, wiring up Node Pools, and keeping component versions in sync. If you're evaluating SUNK, or are new to running Slurm on Kubernetes, SUNK Self-Service is the recommended entry point. For an introduction to the underlying technology, see [About SUNK](https://docs.coreweave.com/products/sunk.md). To decide between this mode and SUNK Standard, see [Choose a SUNK operation mode](https://docs.coreweave.com/products/sunk/choose-operation-mode.md).

## Supported configurations

Before you create a cluster, check that your requirements fit SUNK Self-Service. The following table lists what SUNK Self-Service supports, and where to go when you need something else:

| Area | SUNK Self-Service supports | When you need something else |
| - | - | - |
| CKS cluster | A new CKS cluster that the Cloud Console creates for you, or a new or existing CKS cluster that you apply the `SunkCluster` CR to. In an existing CKS cluster, SUNK Self-Service creates new Node Pools for SUNK and doesn't use the cluster's existing Node Pools. | For a CKS cluster where you deployed SUNK with the Helm charts, use SUNK Standard. |
| Node Pools | Only the Node Pools that SUNK Self-Service creates from the `nodes` list in your cluster definition. SUNK Self-Service doesn't support existing Node Pools. | To run Slurm on Node Pools that already exist in your cluster, use SUNK Standard. |
| SUNK version | SUNK 8.0 and later. A new cluster defaults to the latest SUNK release available on SUNK Self-Service, which can trail a new SUNK release by a few days. See [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md). | For SUNK 7.x and earlier, use SUNK Standard. |
| User identity | Users and groups that SCIM provisions from CoreWeave IAM, including users that you sync from an identity provider (IdP) such as Okta or Microsoft Entra. See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md). | For an LDAP directory, use SUNK Standard. |
| Container images | The controller, login, and `slurmd` images that CoreWeave publishes. You choose the SUNK, Slurm, CUDA, and Ubuntu versions. | For custom controller, login, or `slurmd` images, use SUNK Standard. |
| Slurm configuration | CoreWeave's default Slurm configuration, with [GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md) on by default, plus the Slurm configuration keys that you set in `spec.slurmConfig`. | For custom Slurm plugin files, such as `job_submit.lua` or `cli_filter.lua`, use SUNK Standard. |
| Login access | Public or private access, set separately for group login Pods and per-user login Pods, so you can expose either type, both, or neither. Public access gives a Pod type an external IP address for SSH. Private access keeps it on an internal address that users reach through `kubectl port-forward`. To make a type public, set [`login.groupPods.access`](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#accessconfig) or [`login.userPods.access`](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#accessconfig). A type without `access` stays private. | To reach login Pods through Tailscale, run Tailscale outside the login Pods (a sidecar isn't supported) and [contact CoreWeave Support](https://docs.coreweave.com/support.md) for guidance before you set it up. |
| Upgrades | Upgrades that you start by changing the version fields on your `SunkCluster`. See [Upgrade a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/upgrade-sunk-cluster.md). | Your cluster stays on its current version until you change those fields. Coordinate upgrade timing with your CoreWeave Solutions Architect. |

SUNK Self-Service is available for new SUNK clusters. Moving an existing SUNK Standard cluster to SUNK Self-Service isn't supported, and SUNK Standard clusters keep running as they are.

## What SUNK Self-Service provisions

When you create a SUNK Self-Service cluster, CoreWeave sets up the following:

* A CKS cluster, when you choose to provision a new one through the Cloud Console.
* One Node Pool for each entry in your cluster's `nodes` list, and one NodeSet for each compute entry, kept in sync automatically as you scale.
* The Slurm control plane, including its MySQL database, running as Kubernetes Pods.
* Login Pods that your users SSH into, sized per user or per group.
* Shared storage volumes for home directories and additional mounts.
* The supporting cluster components that Slurm needs, such as GPU device scheduling, deployed and managed for you. You don't assemble or maintain these yourself.
* User provisioning through SCIM and an Identity and Access Management (IAM) group for cluster access, when you use the Cloud Console path.

You configure all of this with a single `SunkCluster` Kubernetes resource. CoreWeave keeps the underlying components reconciled, scales the cluster when you change node counts, and reports overall progress with status conditions that you can inspect with `kubectl`.

### What stays on your side

SUNK Self-Service provisions and maintains the cluster. The following remain your responsibility:

* Submitting and managing Slurm jobs through `sbatch`, `srun`, and the rest of the Slurm CLI.
* Building or selecting the container images that your Slurm jobs run through Pyxis and Enroot, separate from the `slurmd`, login, and control plane images that CoreWeave provides.
* Designing your Slurm partition layout and quality-of-service policies beyond the defaults.
* Managing the data you store in the shared volumes and the lifecycle of that data.
* Adding users to the IAM groups that grant cluster access, and making sure each user has an SSH public key on their CoreWeave profile.
* Monitoring and acting on job-level observability data, even though cluster-level health is reported through `SunkCluster` status conditions.

## SUNK Self-Service compared to SUNK Standard

SUNK is CoreWeave's technology for running Slurm on Kubernetes. A Kubernetes operator and a set of CRDs run inside the cluster to schedule Slurm jobs alongside Kubernetes workloads, but the components you deploy and manage depend on the operation mode. In SUNK Standard, you deploy and operate the sunk and slurm Helm charts yourself.

SUNK Self-Service is the managed operation mode built on the same components. It adds:

* A single, higher-level resource (`SunkCluster`) that captures the full cluster definition. You don't manage the SUNK Helm charts, Node Pool configuration, or individual SUNK CRDs by hand.
* An out-of-band operator, running in a CoreWeave-managed control plane, that provisions and maintains those underlying components.
* Optional integration with the Cloud Console for guided cluster creation and user provisioning.

You can think of `SunkCluster` as the entry point and SUNK as the runtime. When you change a `SunkCluster`, CoreWeave reconciles the change into the SUNK components that actually run Slurm.

## Architecture at a glance

SUNK Self-Service is built around an out-of-band operator that runs in a CoreWeave-managed control plane, outside your CKS cluster:

* **Out-of-band operator.** It watches `SunkCluster` resources and reconciles them into the underlying SUNK components. CoreWeave operates and upgrades it. You don't install or maintain it yourself. See [SUNK Self-Service architecture](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md).
* **Your CKS cluster.** The Slurm control plane, login Pods, compute nodes, and SUNK CRDs all run inside your CKS cluster. This is where Slurm jobs execute and where your users connect.

When you submit a `SunkCluster` resource, the out-of-band operator creates and updates the Node Pools, NodeSets, the `SlurmCluster` resource, shared storage, and supporting components in your cluster. Your day-to-day workflow stays in `kubectl` against your CKS cluster. The out-of-band operator runs outside your cluster, so cluster upgrades and operator maintenance don't require any action on your side.

## Two ways to manage your cluster

You can create and manage SUNK Self-Service clusters in two ways:

* **Cloud Console**: a guided form with a live YAML preview. The Console can also create a new CKS cluster, enable the SCIM API for user provisioning, and create an IAM group during cluster creation.
* **`SunkCluster` resource**: apply YAML directly to your CKS cluster. This is the GitOps-friendly path. CKS cluster creation, SCIM setup, and IAM group creation are separate manual steps.

Both paths submit the same `SunkCluster` resource. The Console emits YAML that you can copy into source control, and a cluster created in the Console can be edited later with `kubectl`.

For step-by-step instructions and a full prerequisites list, see [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md).

## Next steps

* [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md). Walk through the Console form or the `SunkCluster` CR.
* [SunkCluster reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference.md). Every supported field, with examples.
* [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md). Supported version combinations.
* [About SUNK](https://docs.coreweave.com/products/sunk.md). The technology that SUNK Self-Service provisions, and the SUNK Standard operation mode.
