# Introduction to CoreWeave Charts

Source: https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction

# Introduction to CoreWeave Charts

> Finding and consuming Helm charts vetted for use in CKS

CoreWeave Charts is a CoreWeave-hosted collection of [Helm](https://helm.sh/) charts that we've tested and validated for use within [CKS](https://docs.coreweave.com/products/cks.md). This collection primarily contains two types of Helm charts: those that CoreWeave has developed, and some third-party charts for third-party applications.

This page is for CKS users who want to discover, inspect, and install Helm charts from the CoreWeave repository. It covers how to add the repository to Helm, search for charts, view chart details, and install applications. With these steps, you can deploy vetted workloads to your cluster.

> [!NOTE]
>
> While all examples here use `coreweave` as the local repository name, you can substitute any pertinent name.

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.

## Add and search the repository

To add the CoreWeave Charts repository to Helm, add `https://charts.core-services.ingress.coreweave.com` with [`helm repo add`](https://helm.sh/docs/helm/helm_repo_add/):

```bash theme={"system"}
helm repo add coreweave https://charts.core-services.ingress.coreweave.com
```

Refresh the local repository indexes before searching:

```bash theme={"system"}
helm repo update
```

To see all available charts within the repository, use [`helm search repo`](https://helm.sh/docs/helm/helm_search_repo/).

To list the entire contents of the CoreWeave repository, run `helm search repo coreweave`:

```bash theme={"system"}
helm search repo coreweave
```

To list all available stable versions of a specific chart, add the `--versions` (`-l`) flag. For example, to list the versions of `cert-manager`:

```bash theme={"system"}
helm search repo coreweave/cert-manager --versions
```

Add `--devel` to include prerelease versions.

## View charts

To view information about a given chart, use [`helm show chart`](https://helm.sh/docs/helm/helm_show_chart/):

```bash theme={"system"}
helm show chart coreweave/cert-manager
```

The output includes the chart's version, dependencies, keywords, and maintainers. Check for `deprecated: true` before choosing a chart for a new deployment.

To inspect the chart's default configuration, use [`helm show values`](https://helm.sh/docs/helm/helm_show_values/):

```bash theme={"system"}
helm show values coreweave/cert-manager
```

## Keywords

Chart keywords describe a chart's origin and the applications it deploys:

* `coreweave` - identifies CoreWeave-developed charts or applications.
* `vendored` - identifies charts that deploy upstream third-party applications.

A chart can contain both keywords, as `coreweave/cert-manager` does. Check the `maintainers` fields of the chart and its dependencies to identify who maintains each component.

## Chart support

If you're experiencing issues with a specific chart, see the `keywords` and `maintainers` sections of the application's [Chart.yaml file](https://helm.sh/docs/topics/charts/#the-chartyaml-file), or its dependency charts.

If you need further assistance, [create a ticket with support](https://coreweave.freshdesk.com/support/login).

> [!NOTE]
>
> CoreWeave can't provide support for third-party applications. Our support team handles queries on the infrastructure on which your applications run, not the apps themselves.

## Install applications with CoreWeave Charts

After you've identified the chart you want, review its configuration and confirm that you have [access to the target CKS cluster](https://docs.coreweave.com/products/cks/auth-access/introduction.md). Use [`helm install`](https://helm.sh/docs/helm/helm_install/) to deploy it.

The following example installs [cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) with the bundled `cert-issuers` subchart disabled. The subchart must remain disabled until cert-manager and its Custom Resource Definitions (CRDs) are running.

Run either of the following installation commands. They install the same release with equivalent configuration.

To set the value on the command line:

```bash theme={"system"}
helm install cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set cert-issuers.enabled=false
```

Alternatively, save the same configuration in `values.yaml`:

```yaml title="values.yaml" theme={"system"}
cert-issuers:
  enabled: false
```

Then install the chart using the values file:

```bash theme={"system"}
helm install cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --values values.yaml
```

The `cert-issuers.enabled` value defaults to `false`. These examples set it explicitly to demonstrate command-line and file-based configuration. See [cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) for issuer configuration.

To deploy a container registry, follow [Deploy a container registry on CKS](https://docs.coreweave.com/products/cks/tutorials/deploy-zot-registry.md).

See [Using Helm: Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing) for more examples of customizing a chart during installation.
