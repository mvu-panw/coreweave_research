# About SUNK Anywhere

Source: https://docs.coreweave.com/products/sunk/sunk_anywhere/about

# About SUNK Anywhere

> Run SUNK Standard under license on a Kubernetes cluster that CoreWeave doesn't operate, such as GKE or EKS

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

SUNK Anywhere is SUNK Standard, licensed to run on a Kubernetes cluster that CoreWeave doesn't operate. The same `sunk` and `slurm` Helm charts, the same SUNK operator, and the same Slurm images run on your GKE Standard, Amazon EKS, or bare metal cluster. Slurm nodes are Kubernetes Pods there too, and your users connect to a login node and submit jobs with the same Slurm commands.

SUNK Anywhere isn't a third operation mode. The [SUNK Standard](https://docs.coreweave.com/products/sunk.md) pages apply, except where a page describes something CoreWeave Kubernetes Service (CKS) provides. Some of those pages also predate SUNK 8.0, so check their examples against the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md). For what the two modes are and which one to pick, see [Choose a SUNK operation mode](https://docs.coreweave.com/products/sunk/choose-operation-mode.md).

## What CoreWeave provides

* **The licensed `sunk` and `slurm` Helm charts and the SUNK operator image.** With a license, you pull them from a CoreWeave registry with your own API access token. See [Get started with SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/get-started.md).
* **The public [`coreweave/sunk-anywhere`](https://github.com/coreweave/sunk-anywhere) repository**, which holds a deployment track for each provider, annotated values files, an architecture and troubleshooting guide, and validation scripts that exercise `srun`, `sbatch`, GPU compute, the SUNK Pod Scheduler, and metrics. The repository itself is Apache 2.0 and contains no charts or images.

## What you operate

On CKS, CoreWeave runs the Kubernetes layer under SUNK. On your own cluster, you do. You're responsible for the following:

* **The Kubernetes cluster.** That includes the CNI plugin, `kube-proxy`, a default StorageClass that supports `ReadWriteOnce`, a LoadBalancer controller, IAM or workload identity integration with your cloud provider, NVIDIA drivers on your GPU node images, and the NVIDIA device plugin. Managed GPU node pools usually ship the device plugin. The `sunk` chart can install one for clusters without it, and the repository's generic track enables it. The `ReadWriteMany` storage that Slurm nodes share comes from the NFS server that each track installs, not from the default StorageClass.
* **Admission policy.** SUNK requires privileged containers, `hostPath`, and `hostNetwork`, so nothing in the cluster may block them.
* **Shared storage.** Each track sets up an in-cluster NFS server for `/home`, and the EKS track also offers EFS. If you have your own storage, point SUNK at that instead. See [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md).
* **Identity.** By default, each track provisions one local POSIX user with your SSH key. The repository's opt-in multi-user path wires up authentik with SSSD. That path works only with SUNK 7.x charts, because SUNK 8.0 removed SSSD from the charts. For directory-backed accounts on SUNK 8.0 and later, see [Manage users with nsscache on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache.md). `nsscache` has been the default directory service since SUNK 7.0, and the older [directory service guide](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/directory-services.md) applies to SUNK 7.x and earlier.
* **Monitoring wiring.** Each track ships DCGM exporter and Syncer scrape configuration into your provider's monitoring backend.
* **Upgrades.** You pull each new chart version and run the upgrade yourself, as in any SUNK Standard deployment. See [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md). Its examples predate SUNK 8.0, so check them against the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md).

Two references carry the values you'll set: the [SUNK parameter reference](https://docs.coreweave.com/products/sunk/reference/sunk-parameters.md) and the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md). For what's inside the images, see [Slurm images](https://docs.coreweave.com/products/sunk/reference/slurm-images.md). That page predates SUNK 8.0, and its guidance for readers outside CKS doesn't apply to SUNK Anywhere. For the image values SUNK Anywhere needs, see [Step 4 of Get started with SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/get-started.md#step-4-configure-your-cluster-to-pull-images).

## Supported Kubernetes providers

| Provider | Status |
| - | - |
| GKE Standard | Validated end to end, including monitoring |
| Amazon EKS | Validated end to end on a live cluster |
| Any other Kubernetes, including bare metal and on-premises | Validation in progress, through the repository's generic track |

GKE Autopilot and EKS Fargate aren't supported. Both restrict privileged Pods, `hostNetwork`, and custom DaemonSets, which SUNK requires.

## Deploy with an agent

The `sunk-anywhere` repository is written to be read by an AI coding agent. Clone it, open it in an agent that reads project context files, and ask the agent to deploy SUNK on your provider. The agent picks the track for your provider, prompts you for your cloud project or account ID, and works through the deployment. Ask it for GKE Standard, Amazon EKS, or generic Kubernetes.

If you'd rather not use an agent, the repository's `docs` directory carries a deployment guide for each provider that you can follow by hand. The agent path is described in the repository [README](https://github.com/coreweave/sunk-anywhere#quick-start).

## Get access

The `sunk` and `slurm` Helm charts and the SUNK operator image are CoreWeave proprietary software and need a license. To get one, contact CoreWeave at [sunk@coreweave.com](mailto:sunk@coreweave.com) or ask your CoreWeave account team.

## Next steps

> [card] [Get started with SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/get-started.md)
>
> Pull the SUNK operator image and Helm charts with a CoreWeave API access token, then deploy.

> [card] [About SUNK](https://docs.coreweave.com/products/sunk.md)
>
> What SUNK is, how it works, and what each component does.
