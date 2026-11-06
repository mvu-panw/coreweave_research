# Upgrade Kubernetes

Source: https://docs.coreweave.com/products/cks/clusters/upgrade-kubernetes

# Upgrade Kubernetes

> Upgrade CKS clusters to the latest Kubernetes version

Upgrading your CKS cluster ensures access to the latest features, performance improvements, and critical security updates. This guide provides step-by-step instructions for upgrading your CKS cluster to the next available Kubernetes version.

## Version sequence

* Clusters can only be upgraded to the next Kubernetes minor version (for example, from 1.32 to 1.33).
* All upgrades must be sequential. If newer versions exist, you must upgrade one version at a time. You can't skip versions.
* Downgrades aren't supported after an upgrade.

## Eligibility

A cluster isn't eligible for upgrade in the following cases:

* **Unsupported configuration**: Some clusters don't support self-service upgrades when internal components are out of date or not enabled.
* **Deprecated Kubernetes APIs**: If a cluster uses Kubernetes APIs that are deprecated in the target version, the upgrade can't proceed.
  * **Note**: CoreWeave checks for deprecated APIs in your cluster, but can't guarantee that it detects all deprecated APIs in use. Before you upgrade, review the [Kubernetes Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/) for your target version and ensure that your workloads are compatible.
* **Cluster health issues**: Upgrades require the cluster to be in a healthy state.
* **Node version skew**: If any Nodes are more than two versions behind the Control Plane, the upgrade can't proceed until you [reboot those Nodes](#step-2-reboot-the-nodes), which upgrades them to the latest kubelet version.

## Upgrade process

Upgrading a cluster involves two main steps:

1. **[Upgrade the Control Plane](#step-1-upgrade-the-control-plane)**: Use the Cloud Console, the CKS API, or the [Terraform](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs) provider.
2. **[Reboot the Nodes](#step-2-reboot-the-nodes)**: Reboot the Nodes in each Node Pool to upgrade the kubelets to match the Control Plane version.

Each step can be completed using the Cloud Console or the CKS API.

### Step 1: Upgrade the Control Plane

Use the Cloud Console or the CKS API to upgrade the Control Plane of your cluster. The Control Plane upgrade is a prerequisite for rebooting Nodes to complete the Kubernetes upgrade.

> [tab] Cloud Console
>
> 1. Navigate to the [Clusters page](https://console.coreweave.com/clusters) in Cloud Console.
>
> 2. Review the **Kubernetes Version** tags. Clusters eligible for upgrade display an alert tag next to the version.
>
>    ![CKS Cluster versions](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/cluster-upgrade-version.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=f81e48a9369e2aa73e25a555489bcb0b)
>
> 3. Click the alert tag, which opens an upgrade dialog for the next available version.
>
> 4. Click **Upgrade to \[version]** to start the process.

> [tab] CKS API
>
> 1. Inspect the `isUpgradable` field on the cluster resource. The value must be `true` for the cluster to be upgradable.
>
> 2. Create `data.json` with a JSON object for the `PATCH` request with [all required fields](https://docs.coreweave.com/products/cks/reference/cks-api.md#patch-/v1beta1/cks/clusters/id).
>
>    ```json theme={"system"}
>    {
>      "id": "your_cluster_id",
>      "oidc": {
>        "issuerUrl": "your_issuerUrl",
>        "clientId": "your_clientId"
>      },
>      "authzWebhook": {
>        "server": "your_server"
>      },
>      "authnWebhook": {
>        "server": "your_server"
>      },
>      "version": "1.33"
>    }
>    ```
>
>    Replace the required fields with your cluster's specific values. Set `version` to the next Kubernetes minor version. See the [versions supported by CKS](https://docs.coreweave.com/products/cks/reference/cluster-components.md#kubernetes-versions).
>
> 3. Submit [the request](https://docs.coreweave.com/products/cks/reference/cks-api.md#patch-/v1beta1/cks/clusters/id) with `data.json` in the request body. Replace `[CLUSTER-ID]` in the endpoint URL with the cluster ID, and replace `[API-ACCESS-TOKEN]` with an [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md) for your cluster.
>
>    ```bash theme={"system"}
>    curl -X PATCH https://api.coreweave.com/v1beta1/cks/clusters/[CLUSTER-ID] \
>           -H "Content-Type: application/json" \
>           -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
>           -d @data.json
>    ```
>
> 4. Fetch the [cluster's `status`](https://docs.coreweave.com/products/cks/reference/cks-api#get-/v1beta1/cks/clusters/id). When the upgrade is complete, `status` reflects the new version.

If a cluster fails to upgrade, or is not upgradable when you believe it should be, [contact support for assistance](https://docs.coreweave.com/support.md).

### Step 2: Reboot the Nodes

Upgrading the Control Plane doesn't automatically update the Nodes. They continue to run their current Kubernetes version until rebooted, which lets workloads run without interruption. After you upgrade the Control Plane, reboot all Nodes in your Node Pools as soon as possible. This completes the Kubernetes upgrade and ensures consistent performance and feature compatibility.

See [Reboot Nodes on CKS](https://docs.coreweave.com/products/cks/nodes/reboot.md) for detailed instructions.
