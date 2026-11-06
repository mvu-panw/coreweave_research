# Get started with SUNK Anywhere

Source: https://docs.coreweave.com/products/sunk/sunk_anywhere/get-started

# Get started with SUNK Anywhere

> Pull the SUNK operator image and Helm charts with a CoreWeave API access token, then deploy SUNK on your own cluster

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

A SUNK Anywhere deployment starts with the SUNK artifacts: the SUNK operator image and the `sunk` and `slurm` Helm charts. You authenticate to CoreWeave with an API access token, pull them, and configure your cluster to pull the operator image too. The deployment track for your provider lives in the [`coreweave/sunk-anywhere`](https://github.com/coreweave/sunk-anywhere) repository.

This page covers the CoreWeave half: getting a token, pulling the artifacts, and configuring your cluster to pull images. For what SUNK Anywhere is and what you take on by running it, see [About SUNK Anywhere](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md).

## Prerequisites

* A SUNK Anywhere license. See [Get access](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md#get-access).
* A CoreWeave account with access to the Cloud Console.
* A Kubernetes cluster that meets the [prerequisites in the repository](https://github.com/coreweave/sunk-anywhere#prerequisites). For which providers are validated, see [Supported Kubernetes providers](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md#supported-kubernetes-providers).
* `kubectl`, `helm`, and `docker` installed locally, with `kubectl` pointed at the cluster.

## Step 1: Create an API access token

In the Cloud Console, create an API access token and copy the token secret. For the full procedure, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md#create-a-new-api-access-token).

The token secret is your registry password, and your username is the email address associated with the token.

## Step 2: Log in with Docker

Authenticate Docker with your email address and token. Replace `[EMAIL]` with the email address associated with the token, and `[API-ACCESS-TOKEN]` with the token secret.

```bash theme={"system"}
echo "[API-ACCESS-TOKEN]" | docker login sunk.cwcr.io --username [EMAIL] --password-stdin
```

To verify the login, pull the SUNK operator image:

```bash theme={"system"}
docker pull sunk.cwcr.io/operator:v8.1.1
```

Pull the version you intend to deploy. Each SUNK release pairs with one Slurm version. For the full mapping, see [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md).

## Step 3: Log in with Helm

Authenticate Helm against the same registry with the same credentials.

```bash theme={"system"}
echo "[API-ACCESS-TOKEN]" | helm registry login sunk.cwcr.io --username [EMAIL] --password-stdin
```

Pull both charts. The `sunk` chart installs the SUNK operator and its cluster-wide dependencies, and the `slurm` chart describes one Slurm cluster.

```bash theme={"system"}
helm pull oci://sunk.cwcr.io/charts/sunk --version 8.1.1
helm pull oci://sunk.cwcr.io/charts/slurm --version 8.1.1
```

## Step 4: Configure your cluster to pull images

Your Docker login authenticates you, not the cluster. Pods pull images with a Kubernetes secret, and a Pod can use only a secret in its own namespace. Create a `docker-registry` secret in each namespace that you install a chart into. In the repository's tracks, the SUNK operator runs in `sunk` and the Slurm cluster runs in `tenant-slurm`, so you need two. If both charts share one namespace, one secret covers both.

Replace `[NAMESPACE]`, `[EMAIL]`, and `[API-ACCESS-TOKEN]`, and run the command once for each namespace.

```bash theme={"system"}
kubectl create secret docker-registry sunk-registry \
  --namespace [NAMESPACE] \
  --docker-server=sunk.cwcr.io \
  --docker-username=[EMAIL] \
  --docker-password=[API-ACCESS-TOKEN]
```

By default, both charts pull the SUNK operator image from a CoreWeave-internal registry that clusters outside CoreWeave can't reach, and neither chart sets a pull secret. Without the following values, the operator, Syncer, and scheduler Pods fail with `ImagePullBackOff`.

In the `sunk` chart's values, point the operator at the registry and give its Pod the secret:

```yaml theme={"system"}
operator:
  image:
    repository: sunk.cwcr.io/operator
imagePullSecrets:
  - name: sunk-registry
```

In the `slurm` chart's values, `sunkImage` covers the Syncer and scheduler, which run the operator image. `imagePullSecrets` covers the control plane and compute NodeSet Pods, but not login Pods, which pull the public Slurm images:

```yaml theme={"system"}
slurmCluster:
  spec:
    sunkImage:
      repository: sunk.cwcr.io/operator
    imagePullSecrets:
      - name: sunk-registry
```

The Slurm images come from a public registry, so they need no override.

Both charts also schedule the SUNK operator and the Slurm control plane only onto Nodes labeled `node.coreweave.cloud/class=cpu`. If your Nodes don't carry that label, set `operator.affinity` in the `sunk` chart and `slurmCluster.spec.affinity` in the `slurm` chart, or those Pods stay `Pending`.

## Step 5: Deploy SUNK

Clone the repository and follow the track for your provider.

```bash theme={"system"}
git clone https://github.com/coreweave/sunk-anywhere.git
cd sunk-anywhere
```

The repository has a track for GKE, one for EKS, and a generic track for any other Kubernetes. Every track covers storage, monitoring, and user access, and the GKE and EKS tracks also cover your provider's node pools. You can work through a track yourself, or open the repository in an AI coding agent and ask it to deploy on your provider. See [Deploy with an agent](https://docs.coreweave.com/products/sunk/sunk_anywhere/about.md#deploy-with-an-agent) and the repository [README](https://github.com/coreweave/sunk-anywhere#quick-start).

> [!NOTE]
>
> The repository's tracks don't use Steps 1 to 4. They install the charts from a Helm repository URL that CoreWeave sends you, rather than from the registry you logged in to in Step 3. The guides show that URL as `<COREWEAVE_HELM_REPO_URL>`, and the EKS scripts read it from the `COREWEAVE_HELM_REPO` environment variable. The tracks' values files also target SUNK 7.x, not the charts you pulled in Step 3. If a track asks for that URL, or you want a track to deploy the charts from Step 3, contact CoreWeave at [sunk@coreweave.com](mailto:sunk@coreweave.com).

## Next steps

* To keep the deployment in Git and upgrade it from a pipeline, see [Manage a SUNK Standard deployment with CI and GitOps](https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci.md). Its examples predate SUNK 8.0, so check them against the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md).
* For every value the two charts take, see the [SUNK parameter reference](https://docs.coreweave.com/products/sunk/reference/sunk-parameters.md) and the [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md).
* After the cluster is running, see [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md). Its examples use SUNK 7.x login resource names, so check them against the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md).
