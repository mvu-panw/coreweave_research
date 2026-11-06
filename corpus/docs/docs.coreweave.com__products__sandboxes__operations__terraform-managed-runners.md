# Manage runners with Terraform

Source: https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners

# Manage runners with Terraform

> Deploy, configure, and import CoreWeave Sandbox managed runners with the CoreWeave Terraform provider.

Use the `coreweave_sandbox_managed_runner` resource to manage a runner and its sandbox policy on a CoreWeave Kubernetes Service (CKS) cluster. Terraform records the desired configuration, detects drift, and applies configuration changes through the managed-runner API.

For the full attribute schema, see the [managed runner resource reference](https://docs.coreweave.com/platform/terraform/resources/sandbox_managed_runner.md). For the corresponding CLI and REST workflows, see [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).

## Before you begin

You need the following resources and tools:

* Terraform and the [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md). The examples use provider version `0.26.0` or later in the `0.x` series.
* An existing CKS cluster, its universally unique identifier (UUID), and its Availability Zone. Find these values on the [Clusters](https://console.coreweave.com/clusters) page in the cloud console.
* A CoreWeave API access token with `sandbox_admin` permission. See [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) and [Manage Access Policies](https://docs.coreweave.com/security/iam/access-policies/manage.md).
* A Terraform state backend with access controls. Terraform can store runner environment overrides and policy values in state, even when it marks them sensitive.

Each CKS cluster can host at most one managed runner. If your cluster already has one, [import it](#import-an-existing-runner) before applying the configuration.

## Configure authentication

The provider reads `COREWEAVE_API_TOKEN`. If you already exported your token as `CW_API_KEY`, set the provider's environment variable:

```bash theme={"system"}
export COREWEAVE_API_TOKEN="$CW_API_KEY"
```

The provider defaults to `https://api.coreweave.com`. Authentication is independent of the CoreWeave Intelligent CLI login. Keep the token out of Terraform configuration files.

## Define the runner

Save the following configuration in a `main.tf` file. It creates a runner with the stable release channel, a weekly maintenance window, and a policy that sets sandbox resource defaults and a default lifetime.

```terraform title="main.tf" theme={"system"}
terraform {
  required_providers {
    coreweave = {
      source  = "coreweave/coreweave"
      version = "~> 0.26"
    }
  }
}

provider "coreweave" {}

variable "runner_id" {
  type        = string
  description = "Runner identifier, unique within your organization."
}

variable "cluster_id" {
  type        = string
  description = "UUID of the existing CKS cluster."
}

variable "zone" {
  type        = string
  description = "Availability Zone of the existing CKS cluster."
}

resource "coreweave_sandbox_managed_runner" "runner" {
  runner_id  = var.runner_id
  cluster_id = var.cluster_id
  zone       = lower(var.zone)

  spec = {
    release_channel = "RELEASE_CHANNEL_STABLE"
    maintenance_policy = {
      windows = [{ cron = "0 2 * * SAT", duration_seconds = 3600 }]
    }
    overrides = {
      resources = {
        cpu_request    = "1"
        memory_request = "2Gi"
        cpu_limit      = "4"
        memory_limit   = "8Gi"
      }
    }
  }

  policy = {
    display_name = "Sandbox constraints"
    constraints = {
      resources = {
        default_cpu    = "1"
        default_memory = "2Gi"
        max_cpu        = "8"
        max_memory     = "32Gi"
        max_gpu_count  = 0
      }
      lifecycle = { default_lifetime_seconds = 3600 }
    }
  }
}

output "runner_status" {
  value = {
    runner_id           = coreweave_sandbox_managed_runner.runner.runner_id
    install_status      = coreweave_sandbox_managed_runner.runner.install_status
    connection_status   = coreweave_sandbox_managed_runner.runner.connection_status
    active_revision     = coreweave_sandbox_managed_runner.runner.active_revision
    target_revision     = coreweave_sandbox_managed_runner.runner.target_revision
    rollout_in_progress = coreweave_sandbox_managed_runner.runner.rollout_in_progress
  }
}
```

The two resource sections serve different purposes:

* `spec` configures the runner. In this example, `spec.overrides.resources` sizes the runner's own Pods, and the maintenance window starts at 2 AM UTC on Saturdays.
* `policy` configures the sandboxes that the runner serves. This example caps CPU and memory for each sandbox container, forbids GPUs with `max_gpu_count = 0`, and sets a default lifetime of 1 hour. The default lifetime isn't a maximum lifetime. To adapt the constraints to your workloads, see [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md).

The `policy` object is required. Use an explicit empty object only when you intend an empty policy. The `zone` value must be lowercase, which `lower(var.zone)` ensures.

Replace `[RUNNER-ID]`, `[CLUSTER-ID]`, and `[ZONE]` with your runner identifier, CKS cluster UUID, and Availability Zone, then save the values in a `terraform.tfvars` file:

```terraform title="terraform.tfvars" theme={"system"}
runner_id  = "[RUNNER-ID]"
cluster_id = "[CLUSTER-ID]"
zone       = "[ZONE]"
```

## Apply and verify the rollout

To apply the configuration and verify the runner rollout, complete the following steps:

1. Initialize the provider and validate the configuration:

   ```bash theme={"system"}
   terraform init
   terraform validate
   ```

2. Review and apply the plan:

   ```bash theme={"system"}
   terraform plan -out=runner.tfplan
   terraform apply runner.tfplan
   ```

   A successful apply means the API accepted the configuration. Runner installation and rollout continue asynchronously.

3. Refresh the observed status and inspect the output:

   ```bash theme={"system"}
   terraform plan -refresh-only -out=runner-status.tfplan
   terraform apply runner-status.tfplan
   terraform output runner_status
   ```

   The runner is ready when `install_status` is `RUNNER_INSTALL_STATUS_READY`, `connection_status` is `RUNNER_CONNECTION_STATUS_CONNECTED`, and `active_revision` equals `target_revision`. While it's still provisioning, refresh again after the rollout progresses. If installation fails, the computed `install_error` attribute contains details.

## Update the configuration

Edit the resource in the `main.tf` file, review a new plan, and apply it. Keep the complete desired policy and override settings in Terraform so later applies preserve your intent. Changes made through the CLI or API can appear as drift. A subsequent Terraform apply can revert them.

Removing an optional setting inside `spec` resets that setting through an explicit API update mask. Changing the overrides replaces the `spec.overrides` object, so retain any other overrides you want to keep. The resolved `deployment_spec` is read-only.

A concurrent policy edit can cause an apply to fail because the provider uses a policy revision token (`etag`). Refresh and review a new plan before retrying. Changing `runner_id`, `cluster_id`, or `zone` replaces the runner rather than updating it in place.

### Configure runner affinity

Affinity requires a provider release that includes `spec.overrides.affinity`. Provider `0.26.0` doesn't include this attribute. Until a supporting version is available, use the [REST affinity example](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-configure-runner-affinity). Coordinate REST changes with Terraform configuration to avoid overwriting them in later applies.

With a supporting provider installed, merge the following attribute into the existing `spec.overrides` object. Replace the illustrative label with a label used by your cluster's Nodes:

```terraform title="Affinity attribute inside spec.overrides" theme={"system"}
affinity = jsonencode({
  nodeAffinity = {
    preferredDuringSchedulingIgnoredDuringExecution = [{
      weight = 100
      preference = {
        matchExpressions = [{
          key      = "example.com/capacity-class"
          operator = "In"
          values   = ["on-demand"]
        }]
      }
    }]
  }
})
```

The attribute accepts Kubernetes `Affinity` JSON, including node affinity, Pod affinity, and Pod anti-affinity. Keys inside `jsonencode()` use Kubernetes camel case. This preferred rule leaves other eligible Nodes available and doesn't guarantee on-demand-first placement. Existing node selectors and tolerations still apply.

Affinity controls runner Pods only. It doesn't configure sandbox Pod placement or [node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md).

Affinity is replaced as a whole. Set `affinity = jsonencode({})` to clear all rules, including inherited affinity. Remove the attribute to restore platform defaults. In both cases, keep the other attributes in `spec.overrides` that you still need.

## Import an existing runner

Define the resource and variables from the runner configuration example, adapting its policy and spec to the existing runner before applying. Replace `[RUNNER-ID]` with the runner identifier in the organization associated with your API token:

```bash theme={"system"}
terraform init
terraform import coreweave_sandbox_managed_runner.runner '[RUNNER-ID]'
terraform plan
```

Import records the existing runner in state without creating another runner. Review the plan and reconcile the configuration with the imported values before applying. Terraform uses the runner identifier as the import ID, not the cluster UUID.

## Remove a runner

Remove the resource and any references to it, including the `runner_status` output, from your configuration. Then review and apply the resulting plan. Deleting the resource decommissions the managed runner. The provider waits up to 30 minutes for deletion to complete before removing it from state.

## See also

For related workflows and reference information, see the following pages:

* [Managed runner resource reference](https://docs.coreweave.com/platform/terraform/resources/sandbox_managed_runner.md).
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md).
