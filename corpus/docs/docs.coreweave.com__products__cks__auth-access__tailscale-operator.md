# Deploy the Tailscale Kubernetes Operator

Source: https://docs.coreweave.com/products/cks/auth-access/tailscale-operator

# Deploy the Tailscale Kubernetes Operator

> Deploy Tailscale's Kubernetes Operator on CKS using workload identity federation and the required tailnet policy

Deploy the [Tailscale Kubernetes Operator](https://tailscale.com/docs/kubernetes-operator/install-operator) on CoreWeave Kubernetes Service (CKS) with Tailscale's Helm chart and OpenID Connect (OIDC) workload identity federation. This guide is for cluster administrators who want private access to in-cluster Services through their tailnet. For Kubernetes API access, use the [CoreWeave-managed Tailscale control plane integration](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md).

Before you install the operator, configure both `disable-linux-cgnat-drop-rule` and `ipPool: ["100.64.0.0/13"]` in your tailnet policy as shown in [Configure the required CKS networking attributes](#configure-the-required-cks-networking-attributes). The IP pool alone isn't sufficient: The drop-rule attribute is required for Tailscale's standard images to communicate with CKS internal services.

## Prerequisites

Before you begin, confirm that you meet these prerequisites:

* A CKS cluster and `kubectl` credentials authorized to install the chart's resources, including ClusterRoles and ClusterRoleBindings. See the [operator RBAC definitions](https://github.com/tailscale/tailscale/blob/main/cmd/k8s-operator/deploy/chart/templates/operator-rbac.yaml).
* [Helm](https://helm.sh/docs/intro/install/) installed locally.
* Permission to edit the tailnet policy and create federated identities in the Tailscale admin console. Editing the policy requires the Owner, Admin, or Network admin role. See [Tailscale user roles](https://tailscale.com/docs/reference/user-roles) for permissions to manage credentials.
* Your CKS cluster's OIDC issuer URL. See [Your CKS cluster as a trusted OIDC IdP](https://docs.coreweave.com/products/cks/auth-access/workload-identity/introduction.md#your-cks-cluster-as-a-trusted-oidc-idp).

The following sections describe how to configure the policy and federated identity in the Tailscale admin console, then install the operator with Helm. To manage the policy and identity with Terraform instead, go to [Configure Tailscale with Terraform](#optional-configure-tailscale-with-terraform).

## Configure the tailnet policy

Configure the CKS networking attributes and operator tag ownership before you install the chart.

### Configure the required CKS networking attributes

Tailscale assigns device addresses from `100.64.0.0/10` by default. CKS uses `100.124.0.0/18` within that range for internal services. Two policy settings are required:

* `ipPool: ["100.64.0.0/13"]` allocates tailnet addresses from a pool that doesn't overlap CKS internal services.
* `disable-linux-cgnat-drop-rule` disables Tailscale's Linux carrier-grade network address translation (CGNAT) drop rule. This rule can otherwise block traffic from CKS internal services even when the tailnet uses a non-overlapping IP pool.

Changing the IP pool affects new address assignments. It doesn't automatically renumber existing devices. Disabling the CGNAT drop rule also removes its protection against spoofed CGNAT traffic.

Merge the following `nodeAttrs` entry into your [tailnet policy](https://tailscale.com/docs/features/tailnet-policy-file/manage-tailnet-policies). This entry applies both settings only to devices tagged `tag:k8s` or `tag:k8s-operator`, as defined in [Configure operator tags](#configure-operator-tags). Preserve any existing policy entries.

```json title="Required CKS networking policy" theme={"system"}
{
  "nodeAttrs": [
    {
      "target": ["tag:k8s", "tag:k8s-operator"],
      "attr": ["disable-linux-cgnat-drop-rule"],
      "ipPool": ["100.64.0.0/13"]
    }
  ]
}
```

For more information about address allocation, see [Tailscale IP pools](https://tailscale.com/docs/reference/ip-pool).

### Configure operator tags

Merge these tags into the `tagOwners` section of your tailnet policy. The operator uses `tag:k8s-operator` to manage devices tagged `tag:k8s`.

```json title="Operator tag ownership" theme={"system"}
{
  "tagOwners": {
    "tag:k8s-operator": [],
    "tag:k8s": ["tag:k8s-operator"]
  }
}
```

After merging the required networking attributes and operator tags, save your policy on the **Access controls** page. Resolve any validation errors before continuing. Tailscale validates the policy syntax when you save it. See [Troubleshooting grants](https://tailscale.com/docs/reference/troubleshooting/grants) if validation fails.

### Combined policy example

The following example extends Tailscale's default `grants` and SSH rules with the required CKS networking attributes, operator tags, and the policy settings from the [CoreWeave-managed Tailscale control plane integration](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md#configure-access-controls). It supports both the self-managed operator and the CoreWeave-managed VPN proxy in one tailnet. The network grant allows all tailnet traffic, matching the default policy. Adapt it to your organization's access requirements and preserve existing policy entries.

The `tag:coreweave` entry and `autoApprovers.services` rule support the managed VPN proxy. Service auto-approval allows that proxy to advertise its Tailscale service without manual approval. If you only use the operator, these entries are unnecessary.

The optional relay configuration uses only CoreWeave relays because `OmitDefaultRegions` is `true`. See [Configure CoreWeave relays](#optional-configure-coreweave-relays) and the [CoreWeave relay map](https://raw.githubusercontent.com/coreweave/tailscale-derp/main/derpmap/derpmap.json) before choosing relay regions.

```json title="tailnet-policy.json" theme={"system"}
{
  "grants": [
    {"src": ["*"], "dst": ["*"], "ip": ["*"]}
  ],
  "ssh": [
    {
      "action": "check",
      "src": ["autogroup:member"],
      "dst": ["autogroup:self"],
      "users": ["autogroup:nonroot", "root"]
    }
  ],
  "nodeAttrs": [
    {
      "target": ["tag:k8s", "tag:k8s-operator"],
      "attr": ["disable-linux-cgnat-drop-rule"],
      "ipPool": ["100.64.0.0/13"]
    }
  ],
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "907": {
        "RegionID": 907,
        "RegionCode": "us-east-04",
        "RegionName": "us-east-04",
        "Nodes": [
          {
            "Name": "907a",
            "RegionID": 907,
            "HostName": "derp.us-east-04.coreweave.com"
          }
        ]
      }
    }
  },
  "autoApprovers": {
    "services": {
      "tag:coreweave": ["tag:coreweave"]
    }
  },
  "tagOwners": {
    "tag:coreweave": [],
    "tag:k8s-operator": [],
    "tag:k8s": ["tag:k8s-operator"]
  }
}
```

### Optional: Add managed VPN Kubernetes permissions

If you use the VPN guide's [Tailscale Managed Auth mode](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md#configure-grants), you can also add a Kubernetes impersonation grant. Merge the following entries into the existing `tagOwners` and `grants` sections in the combined policy. Keep the existing network grant and other entries.

This lets devices tagged `tag:admin` impersonate the Kubernetes groups `admin` and `view` through the managed proxy.
These are group names, not automatic assignments of the similarly named ClusterRoles.
Each matching device receives both groups. The tag ownership rule lets tailnet administrators assign `tag:admin`.
These entries aren't required for operator installation or the other VPN authentication modes.

```json title="Optional additions for Tailscale Managed Auth" theme={"system"}
{
  "tagOwners": {
    "tag:admin": ["autogroup:admin"]
  },
  "grants": [
    {
      "src": ["tag:admin"],
      "dst": ["tag:coreweave"],
      "app": {
        "tailscale.com/cap/kubernetes": [
          {
            "impersonate": {
              "groups": ["admin", "view"]
            }
          }
        ]
      }
    }
  ]
}
```

## Configure workload identity federation

The operator authenticates using a Kubernetes ServiceAccount token issued by your CKS cluster. Follow [Tailscale's federated identity setup](https://tailscale.com/docs/features/workload-identity-federation#set-up-a-federated-identity) with these settings:

1. In the Tailscale admin console, select **Trust credentials > Credential > OpenID Connect**.
2. Select **Custom issuer**. Enter your cluster's issuer URL in the format `https://oidc.cks.coreweave.com/id/[CLUSTER-ID]`, replacing `[CLUSTER-ID]` with your CKS cluster ID. Use the issuer value described in [Your CKS cluster as a trusted OIDC IdP](https://docs.coreweave.com/products/cks/auth-access/workload-identity/introduction.md#your-cks-cluster-as-a-trusted-oidc-idp).
3. Set **Subject** to `system:serviceaccount:tailscale:operator`. This identifies the `operator` ServiceAccount in the `tailscale` Namespace used by the Helm installation. If you change either name, update the subject to match.
4. Leave **Audience** blank when you create the credential so Tailscale generates the default audience.
5. Grant **Write** access for **General/Services**, **Devices/Core**, and **Keys/Auth Keys**, with `tag:k8s-operator` for each scope.
6. Generate the credential and copy its **Client ID** and **Audience**. The default audience is `api.tailscale.com/[CLIENT-ID]`. These values aren't secrets.

CKS publishes the OIDC discovery document and signing keys publicly, including for private clusters. No additional ClusterRoleBinding is required. Skip the discovery ClusterRoleBinding step in Tailscale's generic Kubernetes federation guide.

## Install the Tailscale Helm chart

Install the operator with Tailscale's Helm chart:

1. Add [Tailscale's Helm repository](https://tailscale.com/docs/kubernetes-operator/install-operator#install-using-helm):

   ```bash theme={"system"}
   helm repo add tailscale https://pkgs.tailscale.com/helmcharts
   helm repo update
   ```

2. Install the chart. Replace both occurrences of `[CLIENT-ID]` with the federated identity's client ID. The audience must match the value generated by Tailscale. Leave `oauth.clientSecret` unset.

   ```bash theme={"system"}
   helm upgrade \
     --install \
     tailscale-operator \
     tailscale/tailscale-operator \
     --namespace=tailscale \
     --create-namespace \
     --set-string oauth.clientId="[CLIENT-ID]" \
     --set-string oauth.audience="api.tailscale.com/[CLIENT-ID]" \
     --wait
   ```

The chart projects a ServiceAccount token with this audience into the operator Pod. The operator exchanges that token with Tailscale to obtain short-lived credentials. You don't need an OAuth client secret or a pre-created `operator-oauth` Secret. See [Tailscale's operator workload identity federation guide](https://tailscale.com/docs/kubernetes-operator/manage-and-configure/workload-identity-federation).

Continue with [Verify the installation](#verify-the-installation).

## Optional: Configure Tailscale with Terraform

To configure the policy and federated identity with Terraform, use the [Tailscale Terraform provider](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs). This example manages the tailnet policy, creates the operator's federated identity, and produces Helm values for the same Tailscale chart used in [Install the Tailscale Helm chart](#install-the-tailscale-helm-chart).

This path requires the [Terraform CLI](https://developer.hashicorp.com/terraform/install) on your runner and Tailscale provider version 0.25.0 or later. Version 0.25.0 [introduced the federated identity resource](https://github.com/tailscale/terraform-provider-tailscale/releases/tag/v0.25.0).

### Prepare the policy and provider authentication

Save your complete tailnet policy in the `tailnet-policy.json` file beside the `main.tf` file. Use the [combined policy example](#combined-policy-example) as a reference. Preserve your existing access rules and include both required CKS networking attributes and the operator tags. If you use the managed VPN, include its entries too. The `tailscale_acl` resource in the following configuration reads this same file, including any optional Kubernetes impersonation grant you add.

> [!WARNING]
>
> The [`tailscale_acl` resource](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs/resources/acl) manages the entire tailnet policy, not just the CKS entries. Import your existing policy before applying, and review the plan for unintended changes. If Terraform already manages your policy, update that resource instead of creating a second policy resource.

Authenticate the Terraform runner using an existing administrative credential as described in [Tailscale provider authentication](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs#authentication). For federation, supply `TAILSCALE_OAUTH_CLIENT_ID` and `TAILSCALE_IDENTITY_TOKEN` through your runner's environment. This identity must be authorized to manage the tailnet policy and create the operator's federated identity with its requested scopes and tags. It's separate from the operator identity created in [Create the policy and operator identity](#create-the-policy-and-operator-identity) and must exist before Terraform runs.

### Create the policy and operator identity

Save the following configuration in the `main.tf` file. Replace `[CLUSTER-ID]` with your CKS cluster ID in the `terraform.tfvars` example that follows.

```terraform title="main.tf" theme={"system"}
terraform {
  required_providers {
    tailscale = {
      source  = "tailscale/tailscale"
      version = ">= 0.25.0"
    }
  }
}

provider "tailscale" {}

variable "cks_cluster_id" {
  description = "CKS cluster ID used in the public OIDC issuer URL."
  type        = string
}

resource "tailscale_acl" "tailnet" {
  acl = file("${path.module}/tailnet-policy.json")
}

resource "tailscale_federated_identity" "operator" {
  description = "CKS Tailscale Operator"
  issuer      = "https://oidc.cks.coreweave.com/id/${var.cks_cluster_id}"
  subject     = "system:serviceaccount:tailscale:operator"
  scopes      = ["devices:core", "auth_keys", "services"]
  tags        = ["tag:k8s-operator"]

  depends_on = [tailscale_acl.tailnet]
}

output "operator_helm_values" {
  description = "Helm values containing the operator client ID and generated audience."
  value = yamlencode({
    oauth = {
      clientId = tailscale_federated_identity.operator.id
      audience = tailscale_federated_identity.operator.audience
    }
  })
}
```

```hcl title="terraform.tfvars" theme={"system"}
cks_cluster_id = "[CLUSTER-ID]"
```

The [`tailscale_federated_identity` resource](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs/resources/federated_identity) returns the client ID in `id`. Omitting `audience` lets Tailscale generate it, and the output uses that returned value directly. The `devices:core`, `auth_keys`, and `services` scopes grant the write access required by the operator. The dependency ensures that the operator tags exist before Terraform creates the identity.

Initialize Terraform, import the existing tailnet policy, and review the plan before applying:

```bash theme={"system"}
terraform init
terraform import tailscale_acl.tailnet acl
terraform plan -out=tfplan
terraform apply tfplan
```

Run the import only when first bringing an existing policy under this resource's management. If you already created the operator identity in the admin console, [import that identity](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs/resources/federated_identity#import) instead of creating another one.

### Install the chart using Terraform outputs

Write the generated client ID and audience to a Helm values file, then install the upstream chart:

```bash theme={"system"}
terraform output -raw operator_helm_values > tailscale-operator-values.yaml
helm repo add tailscale https://pkgs.tailscale.com/helmcharts
helm repo update
helm upgrade --install tailscale-operator tailscale/tailscale-operator \
  --namespace=tailscale \
  --create-namespace \
  --values tailscale-operator-values.yaml \
  --wait
```

The generated values file contains only the client ID and audience. The operator obtains its short-lived token from Kubernetes at runtime. Continue with [Verify the installation](#verify-the-installation).

## Verify the installation

After installation, verify the operator and its connection to your tailnet:

1. Verify that the `tailscale-operator` is running in the `tailscale` Namespace.

   ```bash theme={"system"}
   kubectl get pods -n tailscale
   ```

   Output:

   ```text theme={"system"}
   NAME                        READY   STATUS    RESTARTS        AGE
   operator-54f98f5c6f-jwjmr   1/1     Running   0               9m18s
   ```

2. In the Tailscale admin console, open **Machines**. Confirm that `tailscale-operator` appears with the `tag:k8s-operator` tag, as described in [Tailscale's installation validation](https://tailscale.com/docs/kubernetes-operator/install-operator#validation).

At this point, the operator runs in the cluster and is registered with your tailnet. You can now expose in-cluster services to your tailnet so they are reachable from other Tailscale devices.

## Expose services

To expose a Kubernetes Service to your tailnet, add the `tailscale.com/expose` annotation. For declarative management, include the annotation in the Service manifest managed by your deployment workflow.

### Annotate a Kubernetes Service

This example uses the existing `kubernetes` Service in the `default` Namespace to demonstrate the annotation. For the recommended way to access your cluster's Kubernetes API, use the [CoreWeave-managed Tailscale control plane integration](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md).

Expose the Service and verify that its proxy Pod is created:

1. To expose a Service to your tailnet, annotate the Service with the `tailscale.com/expose: true` annotation.

   ```bash theme={"system"}
   kubectl annotate service kubernetes tailscale.com/expose="true" -n default
   ```

2. After the Service is exposed, verify that a new Pod is created in the `tailscale` Namespace.

   ```bash theme={"system"}
   kubectl get pods -n tailscale
   ```

   Output, with the newly created Pod highlighted:

   ```text highlight={3} theme={"system"}
   NAME                        READY   STATUS    RESTARTS      AGE
   operator-54f98f5c6f-jwjmr   1/1     Running   0             59m
   ts-kubernetes-6f9dq-0       1/1     Running   0             8m7s
   ```

You can access the Service through the Tailscale IP address or MagicDNS hostname. By default, MagicDNS names are formatted as `[NAMESPACE]-[SERVICE-NAME].[MAGICDNS-HOSTNAME]`.

To connect in the other direction, from a sandbox on your cluster to a device on your tailnet, see [Reach a tailnet service from a sandbox](https://docs.coreweave.com/products/sandboxes/tailscale-egress.md).

## Optional: Configure CoreWeave relays

Tailscale runs relay servers worldwide to help [establish direct connections](https://tailscale.com/blog/how-nat-traversal-works) to endpoints on your tailnet. When direct connections aren't possible, the relays forward traffic to your endpoints.

To complement the Tailscale-hosted [relays](https://login.tailscale.com/derpmap/default), CoreWeave hosts [its own relays](https://raw.githubusercontent.com/coreweave/tailscale-derp/main/derpmap/derpmap.json) in select regions to relay traffic to your CKS workloads.

To use CoreWeave-hosted relays, you must [add them to your tailnet configuration](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#step-2-adding-derp-servers-to-your-tailnet).

> [!NOTE]
>
> Each Tailscale client selects a home relay based on latency, so it might not select a CoreWeave-hosted relay. To use only CoreWeave relays, enable `OmitDefaultRegions` in your tailnet configuration. This configuration may not be optimal when connecting to endpoints outside a CoreWeave Region.

For additional operator configuration, see [Tailscale's Kubernetes Operator documentation](https://tailscale.com/docs/kubernetes-operator).

## Troubleshooting

If Tailscale proxy Pods repeatedly restart, see [Why are my Tailscale proxy Pods in CrashLoopBackOff?](https://docs.coreweave.com/support/cks/articles/why-are-my-tailscale-proxy-pods-in-crashloopbackoff).
