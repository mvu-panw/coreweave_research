# Create a SUNK Self-Service cluster

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster

# Create a SUNK Self-Service cluster

> Create a SUNK Self-Service cluster on CKS using the Cloud Console or a SunkCluster custom resource

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SUNK Self-Service is the operation mode in which CoreWeave runs SUNK for you. You declare a cluster once, and CoreWeave provisions the compute, the Slurm control plane, login Pods, shared storage, and user access. By the end of this guide, you have a running SUNK cluster that your users can connect to over SSH and submit Slurm jobs against.

You can create a SUNK Self-Service cluster in two ways:

* **Cloud Console**: a guided form with a live YAML preview. The Cloud Console performs additional setup for you, including creating a CKS cluster if you don't already have one, creating a SCIM API token for user provisioning, and creating an IAM group.
* **`SunkCluster` custom resource (CR)**: apply a YAML manifest directly to your CKS cluster. This path requires extra, manual setup steps to provision user access.

Both paths submit the same `SunkCluster` resource. The out-of-band operator reconciles it into the underlying `NodePools`, `NodeSets`, and `SlurmCluster` resource that make up a running cluster.

> [!NOTE]
>
> Before you create a cluster, check that your requirements fit SUNK Self-Service. See [Supported configurations](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md#supported-configurations). For a requirement outside them, such as custom images, LDAP, custom Slurm plugin files, or existing Node Pools, use [SUNK Standard](https://docs.coreweave.com/products/sunk/choose-operation-mode.md). For detailed guidance, [contact CoreWeave Support](https://docs.coreweave.com/support.md).

## Choose Cloud Console or `SunkCluster` CR

Before you begin, decide which path fits your workflow. The Cloud Console is the fastest way to a working cluster. The `SunkCluster` CR path gives you direct control over the manifest and fits GitOps workflows. For a complete, step-by-step walkthrough of the CR path, from provisioning access to connecting over SSH, see [Get started with SUNK Self-Service using the SunkCluster CR](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md).

When you create a new SUNK cluster in the Cloud Console, it automatically performs additional setup steps for you.

If you choose the `SunkCluster` CR path, you must perform the SCIM API enablement, SCIM API token, and IAM group steps yourself. See [SUNK user provisioning](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) and [nsscache reference](https://docs.coreweave.com/products/sunk/reference/nsscache_reference.md) for the user-provisioning building blocks.

Creating a new SUNK cluster requires the following steps:

| Setup step | Cloud Console | `SunkCluster` CR |
| - | - | - |
| Create a CKS cluster (when you don't already have one) | Automatic | Manual |
| Create `NodePools` for compute and control plane | Automatic | Automatic (operator) |
| Enable the SCIM API and SUNK user provisioning for your organization | Manual (the form prompts an admin) | Manual |
| Create a SCIM API token and Kubernetes secret for user provisioning | Automatic | Manual |
| Create the IAM group and assign membership | Automatic | Manual |
| Apply the `SunkCluster` resource | Automatic | Manual |

## Prerequisites

Before you create a SUNK cluster, verify that you have:

* Sufficient compute and CPU [quota](https://docs.coreweave.com/products/cks/clusters/quotas.md) for the nodes and the Slurm control plane.
* Sufficient [Distributed File Storage (DFS) quota](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md) for the home directory and any additional mounts, plus about 550 GiB for the volumes the Slurm control plane creates for itself, most of it for its database. Each CKS cluster has a 10 TiB DFS quota by default.
* An SSH public key on each user's CoreWeave profile. Without an SSH public key, a user added to a Slurm group can't connect to the login Pod over SSH, and receives a generic "permission denied" error when they attempt the connection. See [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

For the `SunkCluster` CR path only, you also need:

* A new or existing CKS cluster that you can apply manifests against. See [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md). In an existing CKS cluster, the out-of-band operator creates new Node Pools for SUNK from `spec.nodes`. SUNK Self-Service doesn't support existing Node Pools, so Slurm doesn't run on the Node Pools already in the cluster. To use them, choose [SUNK Standard](https://docs.coreweave.com/products/sunk/choose-operation-mode.md). Give each `spec.nodes` entry a name that no existing Node Pool uses. The operator skips an entry whose name matches a Node Pool it doesn't manage.
* A namespace in that cluster to apply the `SunkCluster` to. The out-of-band operator does not require a particular name, and it creates the NodeSets, the `SlurmCluster`, and the shared storage volumes in the same namespace as the `SunkCluster`. The examples on this page use `tenant-slurm`, which is the namespace the Cloud Console uses. Only one `SunkCluster` can be active in a cluster at a time.
* The SCIM API and SUNK User Provisioning enabled, and a SCIM API token stored as a Kubernetes secret in the same namespace as the `SunkCluster`. Unlike the Cloud Console path, you create the token and secret yourself. Name the secret `[CLUSTER-NAME]-nsscache-scim-secret`, where `[CLUSTER-NAME]` is the name of the `SunkCluster`, and store the token under the key `nsscache-scim-auth-token`. The cluster comes up without the secret, but user provisioning over SCIM works only once the secret exists. See [Store the SCIM token as a Kubernetes secret](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md#step-4-store-the-scim-token-as-a-kubernetes-secret), [SUNK user provisioning](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) and the [nsscache reference](https://docs.coreweave.com/products/sunk/reference/nsscache_reference.md).

## Create the cluster

Select the appropriate tab to view the steps for your chosen method.

> [tab] Cloud Console
>
> **1. Open the SUNK page**
>
> Sign in to the [CoreWeave Cloud Console](https://console.coreweave.com/sunk) and go to the **SUNK** page. Select **Create cluster**.
>
> The form is on the left and a live YAML preview is on the right. Anything you change in the form updates the YAML, and any field you add directly to the YAML is included when you submit.
>
> **2. Choose a CKS cluster**
>
> Select **Create new** to provision a new CKS cluster for SUNK. To create a SUNK Self-Service cluster in an existing CKS cluster, use the `SunkCluster` CR path, which creates new Node Pools for SUNK. SUNK Self-Service doesn't support existing Node Pools. See [Get started with SUNK Self-Service using the SunkCluster CR](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md).
>
> **3. Set compute capacity**
>
> Each entry in the compute capacity list becomes one managed `NodePool` and one `NodeSet` in your cluster. The out-of-band operator keeps the `NodeSet` count in sync with the `NodePool` count, so changing **Nodes** later scales the cluster automatically. Counts are measured in Nodes, not GPUs.
>
> By default, the form populates with all of your available quota. Reduce the count for any node type you don't want to use, or remove the row entirely. Removed types remain available for future use, up to your quota.
>
> **4. Provision access**
>
> Confirm that your SSH public key is attached to your profile. The Cloud Console reads the key from your [Profile page](https://console.coreweave.com/account/settings) under **Update Slurm attributes**.
>
> Choose the groups that should have access to the cluster:
>
> * **Slurm users** receive standard access.
> * **Sudo users** can run privileged commands.
>
> Select **Default** to have the Cloud Console create groups named `slurm-users` and `sudo-users` for you. To grant a person access after the cluster is up, add them to one of the selected groups in **Administration** > **Groups**.
>
> > [!NOTE]
> >
> > A user must add their own SSH public key to their CoreWeave profile before they can connect to the login Pod over SSH. Adding them to a group provisions the user account inside Slurm, but doesn't place a key on the login node.
>
> **5. Size the control plane and login Pods**
>
> Choose CPU resources for the control plane. The control plane runs the Slurm control plane workloads and the login Pods.
>
> SUNK provides two kinds of login Pod: **per-user Pods** (the `userPods` field) give each user in a group their own login Pod, while a **shared group Pod** (the `groupPod` field) is shared by all users in a group. You configure both on the `SunkCluster` resource under `spec.login`, and can enable either or both per group and size them independently. For the full list of user and group settings, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#logingroup).
>
> If the form reports that your CPU quota is insufficient, you can:
>
> * Disable `userPods` for select group(s).
> * Disable `groupPod` for select group(s).
> * Reduce the number of users with login Pods.
> * Reduce the per-Pod login resources.
> * Request a quota increase.
>
> **6. Choose group login access**
>
> Under **Group login access**, choose how users reach the shared group login Pods:
>
> * **Public access**: group login Pods get an external IP address, so users can connect directly over SSH.
> * **Private access**: group login Pods get an internal `ClusterIP` address, and users reach them through `kubectl port-forward`.
>
> Per-user login Pods take the same two options, set independently, so you can expose group login Pods, per-user login Pods, both, or neither. To make per-user login Pods public, set [`login.userPods.access`](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#accessconfig) in the YAML preview.
>
> To reach login Pods through Tailscale instead, run Tailscale outside the login Pods (a sidecar isn't supported) and [contact CoreWeave Support](https://docs.coreweave.com/support.md) for guidance before you set it up.
>
> **7. Configure shared storage**
>
> Set the size of the home directory mount and add additional mounts as needed. Shared storage is pooled across all users in the cluster, not per group. Users typically create their own subpaths under each mount.
>
> **8. Submit**
>
> The form requires the SCIM API and SUNK user provisioning to be enabled for your organization. If they aren't, an organization admin turns on **Enable SCIM API** and **Enable SUNK user provisioning** in the form's **SCIM user provisioning** section.
>
> Review the YAML preview, optionally copy it for source control, and select **Submit**. The Cloud Console sets up the resources the cluster needs, such as the SCIM API token and the IAM group, and submits the `SunkCluster` resource to the `tenant-slurm` namespace. For the full list, see [Choose Cloud Console or `SunkCluster` CR](#choose-cloud-console-or-sunkcluster-cr). The SCIM API token expires after 364 days. To replace it, see [Replace a SCIM API token before it expires](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#replace-a-scim-api-token-before-it-expires).
>
> After submitting, the out-of-band operator begins reconciling the cluster. See [Verify the cluster is ready](#verify-the-cluster-is-ready) to track progress.

> [tab] SunkCluster CR
>
> **1. Confirm the SunkCluster CRD is installed**
>
> Check that the `SunkCluster` CRD is installed in your CKS cluster:
>
> ```bash theme={"system"}
> kubectl get crd sunkclusters.sunk.coreweave.com
> ```
>
> If the CRD is missing, CoreWeave hasn't set up the out-of-band operator for your cluster yet. Contact your CoreWeave Solutions Architect.
>
> **2. Create the namespace**
>
> ```bash theme={"system"}
> kubectl create namespace tenant-slurm
> ```
>
> The examples on this page use this namespace.
>
> **3. Author the SunkCluster manifest**
>
> Save the following manifest, replacing `[CLUSTER-NAME]` with a name for your cluster. The manifest leaves out `sunkVersion` and `slurmVersion`, so the cluster gets the latest SUNK release available on SUNK Self-Service and the Slurm build that ships with it. The cluster stays on those versions until you change them. See [Upgrade a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/upgrade-sunk-cluster.md).
>
> ```yaml theme={"system"}
> apiVersion: sunk.coreweave.com/v1alpha1
> kind: SunkCluster
> metadata:
>   name: [CLUSTER-NAME]
>   namespace: tenant-slurm
> spec:
>   ubuntuVersion: "24.04"
>
>   nodes:
>     - name: control-plane
>       instanceType: cd-gp-a192-genoa
>       count: 2
>       controlPlane: true
>     - name: gpu
>       instanceType: gd-8xh100ib-i128
>       count: 4
>       controlPlane: false
>
>   storage:
>     homeDir:
>       path: /mnt/home
>       size: 1Ti
>     additionalMounts:
>       - path: /mnt/data
>         size: 1Ti
>
>   login:
>     groups:
>       - name: slurm-users
>         # userPods and groupPod default to true
>       - name: sudo-users
>         userPods: false
>         groupPod: true
>     sudoGroups:
>       - sudo-users
>     groupPods:
>       access:
>         annotations:
>           example.com/annotation: "value"
>       resources:
>         memory: 8Gi
>         cpu: 4
>     userPods:
>       resources:
>         memory: 8Gi
>         cpu: 4
> ```
>
> Each entry in `spec.nodes` becomes one managed Node Pool, and each entry without `controlPlane: true` also becomes one NodeSet. The `name` and `instanceType` fields are immutable after creation. To replace a node type, add a new entry and remove the old one. The `count` field is mutable and scales the underlying Node Pool. Set `controlPlane: true` on entries that should host the Slurm control plane.
>
> The `login` block controls login Pods: `userPods` gives each user in a group their own login Pod, and `groupPod` creates a Pod shared by the group. List sudo-enabled groups under `sudoGroups`. Login Pods are defined entirely on the `SunkCluster` resource; there is no separate login chart to deploy. See the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#logingroup) for defaults and all login fields.
>
> For the full list of fields, see [SunkCluster reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference.md).
>
> **4. Apply the manifest**
>
> ```bash theme={"system"}
> kubectl apply -f sunkcluster.yaml
> ```
>
> For GitOps, commit the manifest and point your continuous-delivery tool at the `tenant-slurm` namespace. See [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md).
>
> After applying, the out-of-band operator begins reconciling the `SunkCluster` resource into a running cluster. See [Verify the cluster is ready](#verify-the-cluster-is-ready) to track progress.

## Verify the cluster is ready

After you submit, the operators work asynchronously to provision the cluster. Use the following steps to confirm that the cluster has finished reconciling and is ready for users.

A new SUNK cluster can take up to around 40 minutes to come up. Node provisioning accounts for most of that time.

To check progress, inspect the `SunkCluster` resource and its status conditions:

```bash theme={"system"}
kubectl get sunkcluster -n tenant-slurm -o yaml
```

The cluster is ready when the `Ready` condition is `True`. The aggregate `Ready` condition is only `True` when each of its dependent conditions is `True`.

While the cluster is coming up for the first time, the `Ready` condition reports `reason: Bootstrapping` and a `message` that lists the dependent conditions still pending (for example, `Waiting for conditions: NodePoolsAvailable, NodeSetsAvailable, SlurmClusterAvailable`). Each dependent condition reports `reason: InProgress` while it is in progress, `reason: Ready` when satisfied, or `reason: Error` when it fails.

For full descriptions of each condition, the `reason` values, and the underlying `SlurmCluster` conditions that `SlurmClusterAvailable` aggregates, see the [SunkCluster reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference.md#status-conditions).

You can also inspect the underlying resources directly:

```bash theme={"system"}
kubectl get slurmcluster -n tenant-slurm
kubectl get nodepools
kubectl get nodesets -n tenant-slurm
```

Once the cluster is ready, see [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) to log in and submit jobs.

## Troubleshoot

The following sections describe common errors you may encounter while creating or verifying a SUNK cluster.

### `kubectl` returns `Error from server (NotFound)` for `SunkCluster`

CoreWeave hasn't set up the out-of-band operator for the CKS cluster, so the `SunkCluster` CRD is missing. Verify with:

```bash theme={"system"}
kubectl get crd sunkclusters.sunk.coreweave.com
```

If the CRD doesn't exist, contact your CoreWeave Solutions Architect to enable SUNK Self-Service on your cluster.

### A user with group access gets `Permission denied` when they connect over SSH

The user might be in a group that hasn't been given access to the cluster. See [SUNK user provisioning](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) for details about user and group permissions.

If the user has been assigned to a group with cluster access and still can't connect to the login Pod over SSH, verify that the user has added an SSH public key to their CoreWeave profile. Slurm provisions the user account from group membership, but the login node only permits SSH from a key that is attached to the user's profile. Ask the user to add a key on their [Profile page](https://console.coreweave.com/account/settings) under **Update Slurm attributes**, then retry the SSH connection.

### A new `SunkCluster` stays in `Bootstrapping` after you set `slurmVersion`

Check that the `slurmVersion` value starts with a `v`. The [version mapping table](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md) lists versions without the `v`, but `slurmVersion` needs it. The out-of-band operator builds the Slurm image tag from `slurmVersion`, so a value without the `v` names an image that doesn't exist. The cluster's Slurm Pods can't pull it, and on a new cluster the `Ready` condition keeps reporting `reason: Bootstrapping`.

To confirm, look for Pods in the `ErrImagePull` or `ImagePullBackOff` state. If you applied the `SunkCluster` to a namespace other than `tenant-slurm`, use that namespace in the following command:

```bash theme={"system"}
kubectl get pods -n tenant-slurm
```

Correct the value on the `SunkCluster`, for example with `kubectl edit sunkcluster [CLUSTER-NAME] -n tenant-slurm`, or by updating and reapplying your manifest.

### The `SunkCluster` is stuck with `Ready: False`

Check the [conditions](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference.md#status-conditions) on the resource for the first dependent condition that isn't `True`. The `reason` and `message` on each condition identify the underlying problem. A common cause is insufficient quota holding `NodePoolsAvailable` in `reason: InProgress`. For storage quota, see [Storage volume creation fails](#storage-volume-creation-fails).

If `SlurmClusterAvailable` is the blocker, inspect the `SlurmCluster` directly to see which subcomponent is pending:

```bash theme={"system"}
kubectl get slurmcluster -n tenant-slurm -o yaml
```

### Storage volume creation fails

When a volume would exceed the cluster's [DFS quota](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md), the PVC is rejected. Which condition reports the rejection depends on the volume:

* **The home directory or an additional mount:** `VolumesAvailable` reports `reason: Error`, with a `message` that starts with `Failed to reconcile PVCs:`.
* **The Slurm controller's state volume:** `SlurmClusterAvailable` reports `reason: Error`. The `SlurmctldAvailable` condition on the `SlurmCluster` carries the rejection text.
* **The Slurm database volume:** no condition reports `reason: Error`. `SlurmClusterAvailable` stays in `reason: InProgress` and `Ready` stays in `reason: Bootstrapping`. Check the `message` of the `DatabaseAvailable` condition on the `SlurmCluster`, which reports why the database isn't healthy yet. With the default settings, the database volume is the largest volume the control plane creates, so it's the one most likely to be rejected.

To see the `SlurmCluster` conditions, run:

```bash theme={"system"}
kubectl get slurmcluster -n tenant-slurm -o yaml
```

To fix the problem, [request a DFS quota increase](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md#request-a-quota-increase). If the rejected PVC belongs to a home directory or mount that doesn't exist yet, you can instead lower its size in `spec.storage` and reapply the `SunkCluster`. You can't shrink a PVC that already exists, and removing a mount from `spec.storage` doesn't delete its PVC, so neither frees quota.

A home directory and mounts that split the full 10 TiB default quota between them always fail, because the control plane's volumes count against the same quota as `spec.storage`. With the default settings, those volumes take about 550 GiB, most of it for the database, so leave at least that much of the quota free when you size the home directory and mounts.

A PVC that was created but hasn't bound yet doesn't count as a failure: `VolumesAvailable` stays `reason: Ready` and lists the claim in its `message` as `not yet bound`. If the cluster stays in `Bootstrapping` and the `message` keeps listing the same claims, check the PVCs and their events:

```bash theme={"system"}
kubectl get pvc -n tenant-slurm
kubectl describe pvc [PVC-NAME] -n tenant-slurm
```

### The cluster stays in `Bootstrapping` and Pods can't pull their images

The `SunkCluster` status doesn't report image-pull failures. While a Pod can't pull its image, the condition for that Pod stays in `reason: InProgress` with no mention of the image: `ControllerManagerAvailable` for the in-cluster operator, `NodeSetsAvailable` for the `slurmd` Pods, or `SlurmClusterAvailable` for the Slurm control plane and login Pods. The `Ready` condition stays in `reason: Bootstrapping`.

If the cluster stays in `Bootstrapping` longer than expected, check the Pods in the `SunkCluster` namespace and in `cw-sunk`, the namespace that holds the in-cluster operator:

```bash theme={"system"}
kubectl get pods -n tenant-slurm
kubectl get pods -n cw-sunk
```

A Pod with the status `ErrImagePull` or `ImagePullBackOff` can't pull its image. To see which image and why, check the Pod's events, replacing `[NAMESPACE]` with the namespace the Pod is in:

```bash theme={"system"}
kubectl describe pod [POD-NAME] -n [NAMESPACE]
```

The operator builds the Slurm image tag from `slurmVersion` and `ubuntuVersion`, and the SUNK operator image tag from `sunkVersion`. If the tag in the events doesn't exist, set `slurmVersion` and `sunkVersion` to a supported combination from [SUNK and Slurm versions](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md), check that `ubuntuVersion` is `22.04` or `24.04`, and reapply the `SunkCluster`.

## Next steps

After your cluster is running, use the following resources to configure and manage it:

* [SunkCluster reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference.md) for every supported field.
* [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md) for supported version combinations.
* [Connect to t Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) to start running jobs.
* [`SunkCluster` reference: login settings](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#logingroup) to tune login Pods and resources.
* [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md) for long training runs.
