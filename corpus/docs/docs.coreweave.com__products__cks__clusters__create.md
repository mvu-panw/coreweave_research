# Create a CKS cluster

Source: https://docs.coreweave.com/products/cks/clusters/create

# Create a CKS cluster

> Create and configure a CKS cluster using the Cloud Console or Terraform, from naming through deployment

This guide walks you through creating a CoreWeave Kubernetes Service (CKS) cluster. It covers the end-to-end path to your first cluster: provisioning the cluster, configuring its network and authentication settings, and verifying that it deploys successfully. You can create a cluster with the [Cloud Console](#create-a-cluster-using-the-cloud-console) or with [Terraform](#create-a-cluster-with-terraform).

After your cluster reaches the `STATUS_RUNNING` state, shown as **Running** in the Cloud Console, add a Node Pool to give it compute capacity. For a complete worked example that creates a cluster, adds a GPU Node Pool, and deploys a model, see [Deploy an open source LLM on CKS](https://docs.coreweave.com/products/cks/deploy-model.md).

## Before you begin

Before you create your first cluster, confirm the following:

* Your CoreWeave organization and team are set up, and your user has permission to create clusters. See [Organizations and users](https://docs.coreweave.com/security/authn-authz/orgs-users.md).
* Your organization has cluster and GPU quota available in the Zone where you plan to deploy. See [Resource quotas](https://docs.coreweave.com/products/cks/clusters/quotas.md).
* You have chosen a Region and Zone for the cluster. See [About Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

## Create a cluster using the Cloud Console

To create a new CKS cluster using the Cloud Console, open the [Clusters](https://console.coreweave.com/clusters) page, under **Compute** in the sidebar. From here, you can create new CKS clusters, or view and manage deployed ones.

If you don't yet have any clusters, this page is empty:

![A screenshot of the Cloud Console cluster dashboard, with no current clusters](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=f12e3a571dae1274ca3d8a17bafb0b09)

To begin creating a cluster, click the **Create Cluster** button.

### 1. Setup

Give your cluster a name. Reflect the location in the name so clusters stay organized at scale. Here are some guidelines:

* Keep names short and put the location first so that they group together naturally in reports.
* Use only lowercase letters, numbers, and hyphens to keep names compatible with URLs and automation.
* Avoid mutable details like Kubernetes version, Node Pool sizes, or temporary attributes that may change.

Here are some example names to use as a starting point, where `[short_name]` is a concise descriptor of an environment, lifecycle, or workload:

* `use04a-[short_name]`, such as `use04a-prod` or `use04a-staging`
* `us-east-04a-[short_name]`, such as `us-east-04a-prod` or `us-east-04a-staging`

Select a Kubernetes version from the dropdown list of supported versions. CKS supports the latest three versions of Kubernetes. See [Cluster Components](https://docs.coreweave.com/products/cks/reference/cluster-components.md) for more information about supported versions.

![A screenshot of the first step to creating a cluster, labeled "Setup"](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-setup.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=376d7425b9c06eb96bc9e0d11ae90ef7)

Select whether you want your cluster to access the Kubernetes API through the internet.

> [!WARNING]
>
> CKS only supports public clusters as a self-service option. To set up a private cluster, [contact CoreWeave Support](https://docs.coreweave.com/support.md).

If you need a private cluster, see [Private cluster access](https://docs.coreweave.com/products/cks/auth-access/introduction.md#private-cluster-access) for how to reach the Kubernetes API after CoreWeave provisions it.

To configure a custom [Audit Policy](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/#audit-policy) for the cluster, select the **Custom Audit Policy** checkbox to open the Audit Policy YAML editor.

> [!NOTE]
>
> To learn more about cluster Audit Policies, see the [official Kubernetes documentation](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/).

![A screenshot of the Audit Policy editing window](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/cluster-audit-policy.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=428253f9855158d33965c3c1f2b8d1d3)

Use this window to edit the Audit Policy configuration file directly. Click the **Save** button in the bottom right corner to save the Audit Policy and resume the cluster creation process.

The Audit Policy uses the following default settings, which you can change as needed.

> [accordion] Default cluster audit policy
>
> ```yaml title="audit-policy.yaml" lines theme={"system"}
> apiVersion: audit.k8s.io/v1 # This is required.
> kind: Policy
> # Don't generate audit events for all requests in RequestReceived stage.
> omitStages:
>   - "RequestReceived"
> rules:
>   # Log pod changes at RequestResponse level
>   - level: RequestResponse
>     resources:
>       - group: ""
>         # Resource "pods" doesn't match requests to any subresource of pods,
>         # which is consistent with the RBAC policy.
>         resources: ["pods"]
>   # Log "pods/log", "pods/status" at Metadata level
>   - level: Metadata
>     resources:
>       - group: ""
>         resources: ["pods/log", "pods/status"]
>
>   # Don't log requests to a configmap called "controller-leader"
>   - level: None
>     resources:
>       - group: ""
>         resources: ["configmaps"]
>         resourceNames: ["controller-leader"]
>
>   # Don't log watch requests by the "system:kube-proxy" on endpoints or services
>   - level: None
>     users: ["system:kube-proxy"]
>     verbs: ["watch"]
>     resources:
>       - group: "" # core API group
>         resources: ["endpoints", "services"]
>
>   # Don't log authenticated requests to certain non-resource URL paths.
>   - level: None
>     userGroups: ["system:authenticated"]
>     nonResourceURLs:
>       - "/api*" # Wildcard matching.
>       - "/version"
>
>   # Log the request body of configmap changes in kube-system.
>   - level: Request
>     resources:
>       - group: "" # core API group
>         resources: ["configmaps"]
>     # This rule only applies to resources in the "kube-system" namespace.
>     # The empty string "" can be used to select non-namespaced resources.
>     namespaces: ["kube-system"]
>
>   # Log configmap and secret changes in all other namespaces at the Metadata level.
>   - level: Metadata
>     resources:
>       - group: "" # core API group
>         resources: ["secrets", "configmaps"]
>
>   # Log all other resources in core and extensions at the Request level.
>   - level: Request
>     resources:
>       - group: "" # core API group
>       - group: "extensions" # Version of group should NOT be included.
>
>   # A catch-all rule to log all other requests at the Metadata level.
>   - level: Metadata
>     # Long-running requests like watches that fall under this rule will not
>     # generate an audit event in RequestReceived.
>     omitStages:
>       - "RequestReceived"
> ```

### 2. Network

Configure the network settings for the cluster. On the **Network** configuration page, first select the [Super Region](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) where you want to deploy the cluster. Then, select the [Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

> [!NOTE]
>
> Zone availability is subject to capacity.

![A screenshot of the second step to creating a cluster, labeled "Network"](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-network.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=e2747af24c902c0fcc67cae498fc54ad)

#### Select a VPC

If you already [created a VPC](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md) to use with this cluster, select the same Zone where you deployed that VPC. Otherwise, you can either use a default VPC that CoreWeave creates for you during this process, or create a new custom VPC.

You can still customize default VPCs from this page by clicking the **Customize** option beside the **Create a default VPC** radio button.

![A screenshot of the default VPC customization window](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-network-customize.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=2dc928dfdbfdf9eb3644c69792793909)

This opens a configuration screen, where you can adjust the available VPC prefixes and Host Prefixes as needed. This screen also shows the default Host Prefix assigned to the default VPC.

![A screenshot of the default VPC customization window](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-vpc.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=be94aba765507e192d898c04ac32f196)

> [!NOTE]
>
> Each Zone has its own default prefixes, which populate default VPCs. You can change these. Refer to [Regions](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) to see each Zone's default prefixes.

### 3. Auth

The **Auth** screen is where you configure how the cluster handles authentication and authorization. All settings on this screen are optional: you can add an authentication webhook, an authorization webhook, and OIDC, or skip them all and click the **Next** button to continue without changes. When you select any of these options, additional configuration fields appear.

![A screenshot of Step 3 of cluster configuration, auth settings](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-auth.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=ec84df75f72b4e769c023155941504a5)

#### Add an authentication webhook

When you select the **Add an authentication webhook** checkbox, the **Server** and **Certificate Authority** fields appear. To configure the webhook, you must provide a URL in the **Server** input field, and can optionally include a Certificate Authority.

> [!NOTE]
>
> To learn more about Webhook authentication in Kubernetes, see the [official Kubernetes documentation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#webhook-token-authentication).

#### Add an authorization webhook

When you select the **Add an authorization webhook** checkbox, the **Server** and **Certificate Authority** fields appear. To configure the webhook, you must provide a URL in the **Server** input field.

> [!NOTE]
>
> To learn more about Webhook authorization in Kubernetes, see the [official Kubernetes documentation](https://kubernetes.io/docs/reference/access-authn-authz/webhook/).

#### Enable OIDC

To enable OIDC, the **Issuer URL** and **Client ID** fields are required. All other fields are optional.

> [!NOTE]
>
> To learn more about OIDC for Kubernetes, see the [official Kubernetes documentation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens).

#### Certificate Authority

Each of the authentication and authorization options provides an optional **Certificate Authority** checkbox. Selecting this checkbox opens a YAML editor where you can enter a Certificate Authority X.509 certificate.

### 4. Deploy

The final step of cluster creation provides an overview of all options selected during the creation process. After reviewing and confirming the cluster's configuration, click the **Submit** button to deploy the new cluster.

![A screenshot of the final step to creating a cluster, labeled "Deploy"](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-cluster-deploy.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=fe7485664c0565e85ed238d51b93dace)

Your cluster appears on the cluster dashboard with the status **Creating**. When the Control Plane is ready, the cluster's status changes to **Running**. If cluster creation fails, its status changes to **Failed**. For an explanation of what happens between **Creating** and **Running**, see [Provisioning sequence and timing](#provisioning-sequence-and-timing).

## Create a cluster with Terraform

You can also create a cluster with the [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md). A CKS cluster requires a VPC, so the example below creates a `coreweave_networking_vpc` resource and references it from the `coreweave_cks_cluster` resource.

This example covers the minimum needed to create a cluster. For the full list of fields, accepted values, and nested attributes, see the reference pages for [`coreweave_cks_cluster`](https://docs.coreweave.com/platform/terraform/resources/cks_cluster) and [`coreweave_networking_vpc`](https://docs.coreweave.com/platform/terraform/resources/networking_vpc).

### 1. Configure the provider

Add the CoreWeave provider and supply your API token. Replace `[API-ACCESS-TOKEN]` with your CoreWeave API token, which starts with `CW-SECRET-`. For all provider options, see the [CoreWeave Provider](https://docs.coreweave.com/platform/terraform.md) reference.

```terraform title="provider.tf" theme={"system"}
terraform {
  required_providers {
    coreweave = {
      source = "coreweave/coreweave"
    }
  }
}

provider "coreweave" {
  # Reads the token from the COREWEAVE_API_TOKEN environment variable.
}
```

```bash theme={"system"}
export COREWEAVE_API_TOKEN="[API-ACCESS-TOKEN]"
```

### 2. Define the VPC and cluster

Define a VPC and a cluster in the same Availability Zone. The cluster references the VPC by `id`, and its `pod_cidr_name`, `service_cidr_name`, and `internal_lb_cidr_names` values must match `vpc_prefixes` names defined on the VPC.

```terraform title="main.tf" theme={"system"}
resource "coreweave_networking_vpc" "default" {
  name = "default"
  zone = "US-EAST-04A"

  host_prefixes = [
    {
      name     = "primary"
      type     = "PRIMARY"
      prefixes = ["10.16.192.0/18"]
    },
  ]

  vpc_prefixes = [
    {
      name  = "pod cidr"
      value = "10.0.0.0/13"
    },
    {
      name  = "service cidr"
      value = "10.16.0.0/22"
    },
    {
      name  = "internal lb cidr"
      value = "10.32.4.0/22"
    },
  ]
}

resource "coreweave_cks_cluster" "default" {
  name                   = "default"
  version                = "v1.35"
  zone                   = "US-EAST-04A"
  vpc_id                 = coreweave_networking_vpc.default.id
  public                 = false
  pod_cidr_name          = "pod cidr"
  service_cidr_name      = "service cidr"
  internal_lb_cidr_names = ["internal lb cidr"]
}
```

Each field in this example corresponds to an option in the Cloud Console creation flow. The following table shows where you set each one in the Console.

| Terraform field | Console step | Where you set it |
| - | - | - |
| `name` (cluster) | Setup | Cluster name |
| `version` | Setup | Kubernetes version dropdown |
| `public` | Setup | Kubernetes API internet-access selection |
| `zone` | Network | Zone |
| `vpc_id` | Network | Select a VPC |
| `pod_cidr_name`, `service_cidr_name`, `internal_lb_cidr_names` | Network | VPC prefixes in the VPC customization screen |
| `name`, `host_prefixes`, `vpc_prefixes` (VPC) | Network | VPC name, Host Prefix, and VPC prefixes in the VPC customization screen |

The Console **Network** step also has a **Super Region** selector. Terraform has no equivalent field, because the `zone` value determines the Region.

The `coreweave_cks_cluster` resource also supports optional settings that mirror the Cloud Console flow: an `audit_policy` block like the **Setup** step, and `oidc`, `authn_webhook`, and `authz_webhook` blocks like the **Auth** step. For their fields and an example that includes them, see the [`coreweave_cks_cluster`](https://docs.coreweave.com/platform/terraform/resources/cks_cluster) reference.

### 3. Apply the configuration

From the directory that contains your `.tf` files, initialize the working directory, preview the changes, and apply them:

```bash theme={"system"}
terraform init
terraform plan
terraform apply
```

`terraform init` downloads the CoreWeave provider, `terraform plan` shows the resources Terraform will create, and `terraform apply` creates the VPC and cluster after you confirm. After Terraform applies the plan, the cluster appears on the [Clusters](https://console.coreweave.com/clusters) page with the status `Creating`, the same as a Console-created cluster. See [Provisioning sequence and timing](#provisioning-sequence-and-timing) for what happens next.

If `terraform apply` fails with `unavailable` after repeated attempts to create the cluster, see [Why does Terraform report unavailable when creating a CKS cluster?](https://docs.coreweave.com/support/cks/articles/why-does-terraform-report-unavailable-when-creating-a-cks-cluster).

## Provisioning sequence and timing

After you submit a cluster, CKS provisions it in stages. Knowing the sequence helps you understand what each status means and when the cluster is ready for workloads.

1. **Control Plane provisioning.** The cluster appears on the dashboard with the status `Creating`. During this stage, CKS provisions the Managed Control Plane and its associated network configuration.
2. **Control Plane ready.** When the Control Plane is ready, the cluster status changes to **Running**. At this point you can generate an access token and connect with `kubectl`.
3. **In-cluster resource provisioning.** The `STATUS_RUNNING` state reflects the Control Plane only. The cluster can still be provisioning required in-cluster resources, including required Control Plane Node Pools and required applications such as CNI and DNS. For the components that make up a cluster and where each one runs, see [Cluster components](https://docs.coreweave.com/products/cks/reference/cluster-components.md).
4. **Add Node Pools.** A new cluster has no compute capacity until you add a Node Pool. After you create a Node Pool, its Nodes provision separately from the cluster. Node Pool provisioning can be delayed while the cluster is still being created, and provisioning can take up to 15 minutes. When the Node Pool status is `Healthy`, the cluster has capacity to run workloads. See [Deploy an open source LLM on CKS](https://docs.coreweave.com/products/cks/deploy-model.md) for a worked example.

> [!NOTE]
>
> Provisioning time varies with Zone capacity, the resources you request, and current demand. Use the status shown on the [Clusters](https://console.coreweave.com/clusters) page and the Node Pool status as the source of truth rather than a fixed schedule.

## View details of deployed clusters

To view more information about a deployed cluster, click the vertical ellipses menu beside the cluster name and select **View Details**. This opens the cluster's current configuration in JSON, along with information about the cluster's age, location, name, associated API endpoint, and current state. To return to the dashboard, close this panel.

## Cluster statuses

The cards at the top of the cluster dashboard provide information about the status of your current clusters.

> [!WARNING]
>
> The cluster's status refers to the status of the cluster's Control Plane. A CKS cluster in the `STATUS_RUNNING` state can still be provisioning in-cluster resources. These resources include required Control Plane Node Pools and required applications such as CNI and DNS configurations. See [Cluster Components](https://docs.coreweave.com/products/cks/reference/cluster-components.md) for more information.

| Name | Description |
| - | - |
| **Running** | Displays the number of clusters in the `STATUS_RUNNING` state. |
| **Unhealthy** | Displays the number of clusters in the `STATUS_ERROR` state. |
| **Failed** | Displays the number of clusters in the `STATUS_FAILED`, `STATUS_UPGRADE_FAILED`, or `STATUS_PREEMPTED` state. This card appears only when at least one cluster is in one of these states. |

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.
