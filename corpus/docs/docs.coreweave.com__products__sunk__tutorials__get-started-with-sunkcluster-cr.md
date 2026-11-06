# Get started with SUNK Self-Service using the SunkCluster CR

Source: https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr

# Get started with SUNK Self-Service using the SunkCluster CR

> Stand up a SUNK Self-Service cluster end to end by applying a SunkCluster custom resource to a CKS cluster

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This tutorial shows how to stand up a SUNK Self-Service cluster end to end by applying a `SunkCluster` custom resource (CR) to a CoreWeave Kubernetes Service (CKS) cluster. You start from a CKS cluster that has the `SunkCluster` CRD, which CoreWeave installs when it enables SUNK Self-Service for the cluster. From there, provision the user access that Slurm requires and apply a single manifest. Finish by connecting to a login Pod over SSH and running a Slurm command.

The `SunkCluster` CR path is the declarative alternative to the Cloud Console form. It gives you direct control over the manifest and fits GitOps workflows, though it requires a few extra setup steps that the Console otherwise performs for you. For a side-by-side comparison of the two paths, see [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md). For a full description of every field you can set, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference).

By the end of this tutorial, you have a running SUNK cluster that your users can connect to over SSH and submit Slurm jobs against.

## In this tutorial

This tutorial covers the following steps:

1. Confirm the `SunkCluster` CRD is present and create the `tenant-slurm` namespace.
2. Create the user groups that have access to the cluster.
3. Enable the SCIM API and SUNK User Provisioning, and create a SCIM token.
4. Store the SCIM token as a Kubernetes secret.
5. Author and apply the `SunkCluster` manifest.
6. Verify the cluster is ready.
7. Connect to a login Pod over SSH.

## Prerequisites

Before you begin, make sure you have the following:

* A new or existing CKS cluster that you can apply manifests against. See [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md). In an existing CKS cluster, SUNK Self-Service creates new Node Pools for SUNK. SUNK Self-Service doesn't support existing Node Pools. To check that your requirements fit SUNK Self-Service, see [Supported configurations](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md#supported-configurations).
* `kubectl` access to that cluster, with a kubeconfig downloaded from the Cloud Console. See [Manage API access tokens and kubeconfig files](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
* The `SunkCluster` CRD. CKS clusters don't include it by default; CoreWeave installs it when it enables SUNK Self-Service for your cluster. You confirm this in the first step. If it's missing, contact your CoreWeave Solutions Architect.
* Sufficient compute and CPU [quota](https://docs.coreweave.com/products/cks/clusters/quotas.md) for the compute nodes and the Slurm control plane.
* Sufficient [Distributed File Storage (DFS) quota](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-quotas.md) for the home directory in the manifest, plus about 550 GiB for the volumes the Slurm control plane creates for itself, most of it for its database. Each CKS cluster has a 10 TiB DFS quota by default.
* Administrator access to [CoreWeave IAM](https://console.coreweave.com/organization/iam/scim) so you can enable the SCIM API, create a token, and manage groups.
* An SSH public key on your CoreWeave profile. Without a key attached to your profile, a user added to a Slurm group can't connect to the login Pod over SSH. Add one on your [Profile page](https://console.coreweave.com/account/settings) under **Update Slurm attributes**.

## Step 1: Confirm the CRD and create the namespace

When you apply a `SunkCluster` resource, the [out-of-band operator](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md) reconciles it into the underlying `NodePools`, `NodeSets`, and `SlurmCluster` resources that make up a running cluster. It watches all namespaces. This tutorial uses `tenant-slurm` by convention, which keeps Slurm resources together and matches the rest of the SUNK documentation.

First, confirm the `SunkCluster` CRD is present:

```bash theme={"system"}
kubectl get crd sunkclusters.sunk.coreweave.com
```

If the command returns the CRD, you're ready to continue. If it returns `Error from server (NotFound)`, the CRD isn't present on your cluster. Contact your CoreWeave Solutions Architect before continuing.

Next, create the `tenant-slurm` namespace:

```bash theme={"system"}
kubectl create namespace tenant-slurm
```

This tutorial creates both the `SunkCluster` resource you apply later and the SCIM secret you create in Step 4 in `tenant-slurm`, so they live together.

## Step 2: Create the user groups

SUNK provisions cluster access to groups of users, not individual users. CoreWeave creates two groups for you in the Cloud Console, which this tutorial uses:

* `slurm-users` for standard access.
* `sudo-users` for users who can run privileged commands.

Confirm these groups exist on the [**Groups**](https://console.coreweave.com/organization/groups) page in the [CoreWeave Cloud Console](https://console.coreweave.com).

To grant access to additional groups, create them and reference their names in the `SunkCluster` manifest in Step 5. If you federate users from an identity provider (IdP) with Automated User Provisioning (AUP), create the groups there and let AUP sync them into CoreWeave IAM. Otherwise, create them directly in the Console:

1. On the [**Groups**](https://console.coreweave.com/organization/groups) page, select **Create Group**, enter the group name, and select **Create**.
2. Repeat for each additional group.

Any group name you reference in the manifest must match a group that exists in CoreWeave IAM. For more detail on user and group provisioning, see [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#create-sunk-user-groups).

> [!NOTE]
>
> When you add a user to a group, SUNK provisions their Slurm account, but the login Pod only permits SSH from a key attached to the user's CoreWeave profile. Each user must add their own SSH public key on their [Profile page](https://console.coreweave.com/account/settings) under **Update Slurm attributes**.

## Step 3: Enable the SCIM API and create a token

SUNK User Provisioning (SUP) uses a SCIM token to read user and group data from CoreWeave IAM and provision matching POSIX and Slurm identities on the cluster. Enable the API and create a token:

1. In the Cloud Console, go to the [**SCIM Configuration**](https://console.coreweave.com/organization/iam/scim) page.
2. Enable **Enable SCIM API** and **Enable SUNK User Provisioning**. If you federate users from an IdP with AUP, also enable **Enable Automated User Provisioning**.
3. Create a SCIM token with a name of your choice, and copy the token value. You use it in the next step.

> [!WARNING]
>
> Treat the SCIM token like a password. Copy it into the Kubernetes secret in the next step and don't commit it to source control. The Console doesn't display the token again after you leave the page.

For more detail on enabling SUP and the difference between AUP and SUP, see [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md).

> [!TIP]
>
> You can also set up SCIM after you apply the manifest. A `SunkCluster` you create with `kubectl` still appears in the Cloud Console. If its SCIM token is missing, the Console detects this and presents a link to enable it. Because the SCIM secret is optional at creation time (see Step 4), you can apply the cluster first. Then complete SCIM setup from the UI when the Console prompts you.

## Step 4: Store the SCIM token as a Kubernetes secret

The out-of-band operator finds the SCIM token by looking for a secret in the `SunkCluster` resource's namespace, `tenant-slurm` in this tutorial, whose name follows a convention. As a result, you don't reference the secret from the `SunkCluster` manifest. Name the secret `[CLUSTER-NAME]-nsscache-scim-secret`, where `[CLUSTER-NAME]` is the name you give the `SunkCluster` in Step 5. Decide that name now so you can reuse it in both steps. Inside the secret, store the token under the key `nsscache-scim-auth-token`.

Create the secret, replacing `[CLUSTER-NAME]` with your cluster name and `[SCIM-TOKEN]` with the token value you copied in the previous step:

```bash theme={"system"}
kubectl create secret generic [CLUSTER-NAME]-nsscache-scim-secret \
  --namespace tenant-slurm \
  --from-literal=nsscache-scim-auth-token=[SCIM-TOKEN]
```

`kubectl create secret generic` base64-encodes the value for you, so paste the token in plain text. Confirm the secret exists:

```bash theme={"system"}
kubectl get secret [CLUSTER-NAME]-nsscache-scim-secret -n tenant-slurm
```

```text theme={"system"}
NAME                              TYPE     DATA   AGE
my-cluster-nsscache-scim-secret   Opaque   1      5s
```

> [!NOTE]
>
> The SCIM secret is optional at creation time, and the out-of-band operator brings the cluster up without it. User provisioning over SCIM works once the secret is present, so create it before users need to connect. You can create it after you apply the manifest in Step 5, and the out-of-band operator picks it up.

## Step 5: Author and apply the SunkCluster manifest

With access provisioned, declare the cluster. Save the following manifest as `sunkcluster.yaml`, replacing `[CLUSTER-NAME]` with a name for your cluster and `[ORG-ID]` with your [organization ID](https://docs.coreweave.com/security/authn-authz/orgs-users.md#organization-ids). The manifest leaves out `sunkVersion` and `slurmVersion`, so the cluster gets the latest SUNK release available on SUNK Self-Service and the Slurm build that ships with it. The cluster stays on those versions until you change them. For instance types, see the [available instances](https://docs.coreweave.com/platform/instances/about-instances.md) page.

> [!NOTE]
>
> SUNK supports one `SunkCluster` per CKS cluster. If more than one exists, the operator reconciles only a single active cluster.

```yaml theme={"system"}
apiVersion: sunk.coreweave.com/v1alpha1
kind: SunkCluster
metadata:
  name: [CLUSTER-NAME]
  namespace: tenant-slurm
spec:
  ubuntuVersion: "24.04"

  nodes:
    - name: control-plane
      instanceType: cd-gp-a192-genoa
      count: 2
      controlPlane: true
    - name: gpu
      instanceType: gd-8xh100ib-i128
      count: 4
      controlPlane: false

  storage:
    homeDir:
      path: /mnt/home
      size: 2Ti

  login:
    groups:
      - name: slurm-users
        # userPods and groupPod default to true
      - name: sudo-users
        userPods: false
        groupPod: true
    sudoGroups:
      - sudo-users
    userPods:
      access:
        annotations:
          # external-hostname is optional
          service.beta.kubernetes.io/external-hostname: sunk.[ORG-ID]-[CLUSTER-NAME].coreweave.app
          service.beta.kubernetes.io/coreweave-load-balancer-ip-families: ipv4
          service.beta.kubernetes.io/coreweave-load-balancer-type: public
    groupPods:
      access:
        annotations:
          # external-hostname is optional
          service.beta.kubernetes.io/external-hostname: sunk.[ORG-ID]-[CLUSTER-NAME].coreweave.app
          service.beta.kubernetes.io/coreweave-load-balancer-ip-families: ipv4
          service.beta.kubernetes.io/coreweave-load-balancer-type: public
```

This manifest declares:

* **`nodes`**: Each entry becomes one managed `NodePool`, and each entry without `controlPlane: true` also becomes one `NodeSet`. The `name` and `instanceType` fields are immutable after creation. `count` is mutable and scales the underlying `NodePool`. The entry with `controlPlane: true` hosts the Slurm control plane.
* **`storage.homeDir`**: The shared home directory mount, sized at the `2Ti` default here. Shared storage is pooled across all users in the cluster.
* **`login.groups`**: The groups whose members can access the cluster, matching the groups from Step 2. `userPods` gives each member their own login Pod, and `groupPod` creates one Pod shared by the group. The `sudo-users` entry creates only a shared group Pod for that group. Members of the groups listed under `sudoGroups` get sudo on the login Pods.
* **`login.userPods.access` and `login.groupPods.access`**: The load balancer annotations that expose login Pods on a public address for SSH. `coreweave-load-balancer-type: public` requests an external IP, `coreweave-load-balancer-ip-families: ipv4` selects the address family, and the optional `external-hostname` annotation assigns a stable hostname. The two classes are configured separately so you can expose them independently.

> [!NOTE]
>
> External IPs are billable and are off by default. Because a cluster typically has many more user Pods than group Pods, you can expose only the group Pods to limit external-IP cost. This approach still gives every user a way to connect. Omit the `access` annotations entirely to keep login Pods internal, then reach them with `kubectl port-forward` as described in [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

Apply the manifest:

```bash theme={"system"}
kubectl apply -f sunkcluster.yaml
```

```text theme={"system"}
sunkcluster.sunk.coreweave.com/[CLUSTER-NAME] created
```

After you apply the resource, the out-of-band operator begins reconciling it into the `NodePools`, `NodeSets`, and `SlurmCluster` that make up a running cluster. For GitOps, commit the manifest and point your continuous-delivery tool at the `tenant-slurm` namespace. See [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md).

## Step 6: Verify the cluster is ready

The operators provision the cluster asynchronously. A new SUNK cluster can take up to around 40 minutes to come up, with node provisioning accounting for most of that time.

Check the `SunkCluster` resource to track progress:

```bash theme={"system"}
kubectl get sunkcluster -n tenant-slurm
```

The summary output gives a brief overview of overall readiness. For the full set of status conditions and their `reason` and `message` details, add `-o yaml`:

```bash theme={"system"}
kubectl get sunkcluster -n tenant-slurm -o yaml
```

The cluster is ready when the aggregate `Ready` condition is `True`. That condition is only `True` when each of its dependent conditions is `True`. While the cluster comes up for the first time, the `Ready` condition reports `reason: Bootstrapping` and a `message` that lists the dependent conditions still pending. For example, the message might read `Waiting for conditions: NodePoolsAvailable, NodeSetsAvailable, SlurmClusterAvailable`. Each dependent condition reports `reason: InProgress` while it works, `reason: Ready` when satisfied, or `reason: Error` when it fails.

You can also inspect the underlying resources directly:

```bash theme={"system"}
kubectl get slurmcluster -n tenant-slurm
kubectl get nodepools
kubectl get nodesets -n tenant-slurm
```

For full descriptions of each condition and its `reason` values, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#status-conditions). If the cluster is stuck with `Ready: False`, the most common cause is insufficient quota. Insufficient Node Pool quota holds `NodePoolsAvailable` in `reason: InProgress`, and insufficient DFS quota usually sets `VolumesAvailable` or `SlurmClusterAvailable` to `reason: Error`. A rejected database volume instead leaves `SlurmClusterAvailable` in `reason: InProgress`; see [Storage volume creation fails](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md#storage-volume-creation-fails). If the cluster stays in `Bootstrapping` with no error, check the `DatabaseAvailable` condition on the `SlurmCluster`, and check for Pods that can't pull their images. For more, see [Troubleshoot](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md#troubleshoot).

## Step 7: Connect to a login Pod over SSH

Once the cluster is ready, find the login service's external address and connect over SSH. This address exists because the `login` access annotations in Step 5 requested a public load balancer. Look up the address:

```bash theme={"system"}
kubectl get svc slurm-login
```

The `EXTERNAL-IP` field in the output is the target address for SSH access:

```text theme={"system"}
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)   AGE
slurm-login   LoadBalancer   192.0.2.100      203.0.113.100    22/TCP    2d21h
```

Connect with SSH, replacing `[USERNAME]` with your Slurm username and `[EXTERNAL-IP]` with the address from the previous command:

```bash theme={"system"}
ssh [USERNAME]@[EXTERNAL-IP]
```

On a successful login, the cluster presents a welcome message and a prompt. To confirm the cluster is working, run a small job that prints the hostname on a few nodes:

```bash theme={"system"}
srun -N 2 hostname
```

```text theme={"system"}
slurm-gpu-0
slurm-gpu-1
```

If you see an error such as "Invalid partition name specified" or "Invalid account or account/partition combination specified," you likely haven't been added as a Slurm user yet. If the cluster has no public IP, or for more connection options such as port forwarding, see [Connect to a Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

You now have a running SUNK cluster created from a `SunkCluster` manifest, with user access provisioned and a verified SSH login.

## Next steps

Continue with the following resources:

* [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference) for every supported field.
* [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) to add more users and groups.
* [Connect to a Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) for more ways to reach the cluster and run jobs.
* [Train on SUNK](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk.md) to run an end-to-end training workload on your new cluster.
