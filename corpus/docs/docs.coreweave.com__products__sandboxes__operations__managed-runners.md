# Deploy and manage a runner

Source: https://docs.coreweave.com/products/sandboxes/operations/managed-runners

# Deploy and manage a runner

> Deploy and manage a runner on CoreWeave Kubernetes Service (CKS) with CoreWeave Intelligent CLI, REST API, or Terraform.

A managed runner is the CoreWeave-managed component that runs sandboxes inside your CKS cluster. This page covers the full lifecycle: deployment, health checks, configuration changes as your needs change, and removal when you no longer need the runner.

For a walkthrough from enabling a runner to running your first sandbox, see [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md).

To manage a runner as infrastructure as code, see [Manage runners with Terraform](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md) for provider setup and the full Terraform lifecycle.

## Before you begin

The CLI, `curl`, and Terraform examples on this page authenticate with a CoreWeave API access token. Generate one from the [Tokens](https://console.coreweave.com/tokens) page in the cloud console and copy the **Token Secret** value. For more on tokens, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

CLI: install the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`), then run `cwic auth login` and paste the token when prompted. The CLI stores the token locally using its configured credential storage backend. Subsequent commands read it automatically. You don't need to set an environment variable.

```bash theme={"system"}
cwic auth login
```

`curl`: export the token in your shell so the examples on this page can pick it up. Replace `API_ACCESS_TOKEN` with your CoreWeave API access token:

```bash theme={"system"}
export TOKEN="API_ACCESS_TOKEN"
```

Terraform: install Terraform and the [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md), and use a token with `sandbox_admin` permission. The deployment example uses provider `0.26.0` or later in the `0.x` series. Set the provider's authentication variable from the token exported in the previous shell command:

```bash theme={"system"}
export COREWEAVE_API_TOKEN="$TOKEN"
```

If your cluster already has a runner, [import it into Terraform state](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#import-an-existing-runner) before applying.

## Runner commands

The `cwic sandbox runner` group manages runners. The following table maps each lifecycle task to the command that performs it. Later sections walk through these commands in context.

| Goal | Command |
| - | - |
| Deploy a runner (wizard) | `cwic sandbox runner create RUNNER_ID` |
| Deploy a runner from a file | `cwic sandbox runner create RUNNER_ID -f runner.yaml` |
| List runners | `cwic sandbox runner get` (alias `ls`) |
| Inspect one runner | `cwic sandbox runner get RUNNER_ID` |
| Detailed view | `cwic sandbox runner describe RUNNER_ID` |
| Edit a runner | `cwic sandbox runner edit RUNNER_ID` |
| Apply an available update | `cwic sandbox runner upgrade RUNNER_ID` |
| Delete a runner | `cwic sandbox runner delete RUNNER_ID` |
| Read the runner's policy | `cwic sandbox runner policy get RUNNER_ID` |
| Edit the runner's policy | `cwic sandbox runner policy edit RUNNER_ID` |

All input accepts YAML or JSON.

## Deploy a runner

Within your organization, each CKS cluster hosts at most one managed runner. To deploy a runner, supply the following details:

* Runner ID: a client-assigned human-readable ID, unique within your organization.
* Zone: the geographic zone the cluster belongs to.
* Cluster ID: which CKS cluster the runner runs on. Find the ID on the [Clusters](https://console.coreweave.com/clusters) page in the cloud console.
* Policy: the rules the runner enforces for sandboxes on its cluster. A stored policy is required for v1 sandbox placement. The v1 create API requires an explicit `policy` in the request.

  For runners registered without a policy through a legacy path, the gateway can save a [deployment-configured default](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#set-a-default-policy-for-new-runners) on connection or first v1 placement. Existing policies are preserved. The policy can supply a default sandbox lifetime. The platform enforces the 30-day maximum. See [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md).

> [tab] CLI
>
> The wizard collects cluster, release channel, and maintenance windows interactively, then opens your editor with a pre-filled spec before submitting:
>
> ```bash theme={"system"}
> cwic sandbox runner create prod-us-east-1
> ```
>
> File mode accepts YAML or JSON, which makes it the preferred path for repeatable setups. It also suits agents like Claude Code or Codex that generate runner specs on your behalf. The CLI also reads from stdin with `-f -`. Replace `CLUSTER_ID` with the ID of the CKS cluster to deploy the runner on:
>
> ```yaml title="runner.yaml" theme={"system"}
> identity:
>   zone: us-east-1
>   cluster_id: "CLUSTER_ID"
> spec:
>   release_channel: RELEASE_CHANNEL_STABLE
>   maintenance_policy:
>     windows:
>       - cron: "0 9 * * SAT"
>         duration_seconds: 14400
> policy:
>   display_name: default
>   constraints:
>     resources:
>       default_cpu: "1"
>       default_memory: "2Gi"
>       max_cpu: "4"
>       max_memory: "8Gi"
>       require_limits: true
>     lifecycle:
>       default_lifetime_seconds: 3600
> ```
>
> Submit the spec:
>
> ```bash theme={"system"}
> cwic sandbox runner create prod-us-east-1 -f runner.yaml
> ```

> [tab] curl
>
> Replace `CLUSTER_ID` with the ID of the CKS cluster to deploy the runner on:
>
> ```bash title="Deploy a managed runner" theme={"system"}
> curl -X POST https://api.coreweave.com/v1/sandbox/managedRunners \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "displayName": "Production runner (US East)",
>     "identity": {
>       "runnerId": "prod-us-east-1",
>       "zone": "us-east-1",
>       "clusterId": "CLUSTER_ID"
>     },
>     "spec": {
>       "releaseChannel": "RELEASE_CHANNEL_STABLE",
>       "maintenancePolicy": {
>         "windows": [
>           { "cron": "0 9 * * SAT", "durationSeconds": 14400 }
>         ]
>       }
>     },
>     "policy": {
>       "displayName": "default",
>       "constraints": {
>         "resources": {
>           "defaultCpu": "1",
>           "defaultMemory": "2Gi",
>           "maxCpu": "4",
>           "maxMemory": "8Gi",
>           "requireLimits": true
>         },
>         "lifecycle": { "defaultLifetimeSeconds": 3600 }
>       }
>     }
>   }'
> ```

> [tab] Terraform
>
> Follow [Define the runner](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#define-the-runner) for the complete resource configuration, then apply and verify the rollout.

Note the following behaviors:

* `maintenance_policy.windows` is optional. When set, automatic updates apply only during the specified cron windows.
* `runner_group_id` is optional. Use it for scheduling affinity when you have multiple runners in the same zone.

### Common validation errors

| Error | Fix |
| - | - |
| `runner.identity.zone is required` | Supply a zone. Find zones where you have a CKS cluster (and therefore quota for a runner) on the Clusters page in the cloud console, or by running `cwic cluster get`. |
| Missing `identity.cluster_id` | Supply the cluster ID. Find it on the Clusters page in the cloud console, or by running `cwic cluster get`. |
| `policy exceeds 256 KiB limit` | Trim the policy document. The encoded document is capped at 256 KiB. |
| `a managed runner already exists for this cluster` | A cluster hosts at most one managed runner. [Update the existing one](#update-a-runner), or [delete it](#delete-a-runner) first. |

## Check runner status

After creation, check the runner's status to confirm it rolled out successfully and to diagnose problems if it didn't.

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner describe prod-us-east-1
> ```
>
> For a quick summary in tabular form, use the alias `get`:
>
> ```bash theme={"system"}
> cwic sandbox runner get prod-us-east-1
> ```
>
> Both commands use the runner ID you supplied on create (`prod-us-east-1`).

> [tab] curl
>
> ```bash title="Fetch a runner" theme={"system"}
> curl -H "Authorization: Bearer $TOKEN" \
>   https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1
> ```
>
> Use the runner ID you supplied on create.

> [tab] Terraform
>
> Follow [Apply and verify the rollout](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#apply-and-verify-the-rollout) to refresh the observed runner status and check readiness.

The API response carries two status fields to track:

* `installStatus`: progress of the runner deployment into your cluster. Values include `RUNNER_INSTALL_STATUS_PENDING`, `RUNNER_INSTALL_STATUS_PROVISIONING`, `RUNNER_INSTALL_STATUS_READY`, and `RUNNER_INSTALL_STATUS_FAILED`.
* `connectionStatus`: reported connectivity (`RUNNER_CONNECTION_STATUS_CONNECTED` or `RUNNER_CONNECTION_STATUS_DISCONNECTED`). Read it together with `installStatus` and `lastHeartbeatTime`. See [Heartbeats](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md#heartbeats) for the health fields.

The CoreWeave Intelligent CLI's table and `describe` output use short display labels, such as `READY` and `CONNECTED`, for these API enum values.

For installation failures, structured error details can be absent if stored error data is unavailable or can't be decoded. When `installStatus` is `RUNNER_INSTALL_STATUS_FAILED`, the response can include a structured `installError`:

```text title="Example output" theme={"system"}
{
  "installError": {
    "reason": "...",
    "message": "...",
    "remediationHints": ["Add toleration for taint 'workload=gpu:NoSchedule'"],
    "occurredTime": "2026-04-24T12:03:11Z"
  }
}
```

Follow the available `remediationHints` to address the failure. Internal diagnostic details are redacted from the API response. The `diagnosticDetail` field doesn't provide logs you can attach to a support ticket.

If structured error details are absent or you need more help, [contact support](https://docs.coreweave.com/support/contact.md#contact-forge-support). Include the runner ID and any error details returned in the response.

## Update a runner

For a runner managed with Terraform, edit its resource configuration, review `terraform plan`, and apply the plan. Keep the complete desired policy and overrides in the configuration. Later applies can revert changes made through the CLI or API. For drift and replacement behavior, see [Update the Terraform configuration](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#update-the-configuration).

The runner edit command supports both an interactive wizard and a file-driven patch. Internally, updates use a field mask: only the fields you change are applied. Everything else is read-only, including `installStatus`, `connectionStatus`, timestamps, and the resolved deployment spec.

For mutable field paths, see [Field masks on updates](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md#field-masks-on-updates).

In the `v1` REST API, the `PATCH` body is the managed runner itself, with no request wrapper. The field mask travels as the `updateMask` query parameter. An omitted or empty mask replaces the whole mutable resource.

`v1` managed-runner writes reject `profile_bindings` (configure `policy` instead) and `spec.allow_privileged_profile_annotations`. These settings remain available on legacy `v1beta2`, where the privileged-profile flag's Protobuf or YAML path is `managed_spec.allow_privileged_profile_annotations`. In REST JSON and the `updateMask` query parameter, use `managedSpec.allowPrivilegedProfileAnnotations`.

### Common runner updates

The following examples show how to edit a runner: switching release channels, replacing the policy it carries, tuning where the runner Pod lands in your cluster, and allowing legacy profile templates to carry a privileged posture.

#### Example: switch release channel

> [tab] CLI
>
> Apply a one-line patch from stdin:
>
> ```bash theme={"system"}
> echo 'spec: {release_channel: RELEASE_CHANNEL_RAPID}' \
>   | cwic sandbox runner edit prod-us-east-1 -f -
> ```
>
> Or write the patch to a file and submit it:
>
> ```yaml title="patch.yaml" theme={"system"}
> spec:
>   release_channel: RELEASE_CHANNEL_RAPID
> ```
>
> ```bash theme={"system"}
> cwic sandbox runner edit prod-us-east-1 -f patch.yaml
> ```

> [tab] curl
>
> ```bash title="Move a runner to the RAPID channel" theme={"system"}
> curl -X PATCH "https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1?updateMask=spec.releaseChannel" \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "identity": { "runnerId": "prod-us-east-1" },
>     "spec": { "releaseChannel": "RELEASE_CHANNEL_RAPID" }
>   }'
> ```

#### Example: replace the policy

The examples in this guide select the root `policy` update mask, which replaces the whole document. Read the current policy, change what you need, and send the complete document back with its current `etag`. A root-policy replacement clears groups you leave out.

Follow [Update a policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy) for the CLI and REST procedures. Capture the policy and its `etag` from the same read, then submit the edited document with that `etag` to detect concurrent changes.

#### Example: pin Node placement through deployment overrides

Use the Node selector, tolerations, scheduler settings, and affinity in `spec.overrides` to control where the runner's own Pods run. Other overrides have a different scope: `cpu_runtime_class` and `gpu_runtime_class` configure the runtimes used for sandbox Pods.

A common case is routing the runner Pod through the SUNK Pod Scheduler so it can run in your SUNK cluster alongside Slurm jobs. Set the scheduler name and the SUNK annotations on the runner overrides. See [SUNK Pod Scheduler integration](https://docs.coreweave.com/products/sandboxes/profiles/sunk-integration.md) for the available annotations and required setup.

> [tab] CLI
>
> ```yaml title="overrides.yaml" theme={"system"}
> spec:
>   overrides:
>     node_selector:
>       node-pool: system
>     tolerations:
>       - key: dedicated
>         operator: Equal
>         value: system
>         effect: NoSchedule
> ```
>
> ```bash theme={"system"}
> cwic sandbox runner edit prod-us-east-1 -f overrides.yaml
> ```

> [tab] curl
>
> ```bash title="Pin the runner to a specific node pool" theme={"system"}
> curl -X PATCH "https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1?updateMask=spec.overrides" \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "identity": { "runnerId": "prod-us-east-1" },
>     "spec": {
>       "overrides": {
>         "nodeSelector": { "node-pool": "system" },
>         "tolerations":  [ { "key": "dedicated", "operator": "Equal", "value": "system", "effect": "NoSchedule" } ]
>       }
>     }
>   }'
> ```

#### Example: configure runner affinity

Use `spec.overrides.affinity` to set Kubernetes Node affinity, Pod affinity, or Pod anti-affinity for the runner's own Pods. The value is a Kubernetes `Affinity` object, with Kubernetes camel case keys inside it. Runner affinity doesn't configure sandbox Pod placement or change Node budgets.

The following example prefers Nodes labeled `example.com/capacity-class: on-demand` while leaving other eligible Nodes available. Replace this illustrative label with one used by your cluster.

> [tab] CLI
>
> Use a version of the CoreWeave Intelligent CLI that supports runner affinity. If the command reports an unknown `affinity` field, upgrade the CLI or use the REST example.
>
> 1. Save the affinity patch:
>
>    ```yaml title="affinity.yaml" theme={"system"}
>    spec:
>      overrides:
>        affinity:
>          nodeAffinity:
>            preferredDuringSchedulingIgnoredDuringExecution:
>              - weight: 100
>                preference:
>                  matchExpressions:
>                    - key: example.com/capacity-class
>                      operator: In
>                      values: [on-demand]
>    ```
>
> 2. Apply it to your runner:
>
>    ```bash theme={"system"}
>    cwic sandbox runner edit prod-us-east-1 -f affinity.yaml
>    ```
>
> An affinity-only patch targets `spec.overrides.affinity`, preserving other overrides. If the same patch includes other override fields, the CLI replaces the whole `spec.overrides` object. Include every sibling override you want to keep.

> [tab] REST
>
> This request replaces affinity while preserving other overrides:
>
> ```bash title="Set runner affinity" theme={"system"}
> curl --fail-with-body -X PATCH \
>   'https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1?updateMask=spec.overrides.affinity' \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "spec": {
>       "overrides": {
>         "affinity": {
>           "nodeAffinity": {
>             "preferredDuringSchedulingIgnoredDuringExecution": [
>               {
>                 "weight": 100,
>                 "preference": {
>                   "matchExpressions": [
>                     {
>                       "key": "example.com/capacity-class",
>                       "operator": "In",
>                       "values": ["on-demand"]
>                     }
>                   ]
>                 }
>               }
>             ]
>           }
>         }
>       }
>     }
>   }'
> ```

> [tab] Terraform
>
> See [Configure runner affinity with Terraform](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#configure-runner-affinity) for provider support, the affinity attribute, and how to clear rules or restore defaults.

Kubernetes combines preferred affinity with other scheduling scores. This preference doesn't guarantee on-demand-first placement or move an already running Pod when preferred capacity becomes available. Existing `node_selector` restrictions still apply. Nodes with `NoSchedule` or `NoExecute` taints require matching tolerations. To allow spot fallback, don't use a Node selector that excludes spot Nodes.

For a hard placement restriction, use `requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms`. Required Node affinity and `node_selector` must both match. Terms are combined with logical OR. Expressions within a term are combined with logical AND. Required Node affinity participates in runner preflight checks. Kubernetes evaluates preferred affinity and Pod affinity or anti-affinity during scheduling.

After an update, use `cwic sandbox runner describe prod-us-east-1` to check rollout progress. In the API response, verify that `activeRevision` matches `targetRevision`, `installStatus` is `RUNNER_INSTALL_STATUS_READY`, and `connectionStatus` is `RUNNER_CONNECTION_STATUS_CONNECTED`. The resolved configuration appears in the output-only `deploymentSpec.affinity` field.

Affinity is replaced as a whole, rather than merged rule by rule. To remove all affinity rules, including inherited rules, apply an explicit empty object:

```bash theme={"system"}
printf '%s\n' 'spec: {overrides: {affinity: {}}}' \
  | cwic sandbox runner edit prod-us-east-1 -f -
```

To remove the override and restore platform defaults, use `affinity: null` in an affinity-only CLI patch. For REST, keep `updateMask=spec.overrides.affinity` and send `{"spec":{"overrides":{}}}`. Clearing affinity leaves Node selectors and tolerations unchanged.

The legacy `v1beta2` field is `managed_spec.overrides.affinity`. New integrations use the `v1` field `spec.overrides.affinity` shown here.

#### Example: allow a privileged profile posture

`allow_privileged_profile_annotations` controls whether the legacy profile templates bound to a runner may carry a privileged posture. It applies to runners that still use profile bindings rather than a policy, so the request goes to the `v1beta2` surface. It defaults to `false`, and a template that carries one is rejected on a runner where the flag isn't set.

Despite the name, the flag governs two kinds of content:

* Privileged Pod annotations, meaning the runtime and scheduler prefixes.
* Privileged structured Pod-spec fields, such as `serviceAccountName`, host namespaces, `hostPath` volumes, and privileged or escalating containers.

A template that a runner rejects returns `permission_denied` and names the offending fields. For example, a template that sets `securityContext.appArmorProfile` and `securityContext.seccompProfile` fails with the following:

```text title="Example output" theme={"system"}
Error: updating runner: permission_denied: profile_bindings[7]: template
"[TEMPLATE-ID]" contains privileged pod-spec fields
[securityContext.appArmorProfile securityContext.seccompProfile];
runner does not have allow_privileged_profile_annotations=true
```

Set the flag on the runner that rejected the template. The flag is scoped to one runner, so repeat this for each runner that needs the privileged posture.

Use the `v1beta2` REST API to set the flag. In CoreWeave Intelligent CLI 1.49.0, `cwic sandbox runner edit` uses `v1` and rejects this legacy setting.

```bash title="Allow a privileged profile posture on one runner" theme={"system"}
curl -X PATCH "https://api.coreweave.com/v1beta2/sandbox/managed-runners/prod-us-east-1?updateMask=managedSpec.allowPrivilegedProfileAnnotations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "prod-us-east-1",
    "managedSpec": { "allowPrivilegedProfileAnnotations": true }
  }'
```

After the update succeeds, reapply the profile template that was rejected.

> [!WARNING]
>
> Setting this flag widens what sandboxes on the runner can do, including reaching host resources. Set it only on runners where the privileged posture is required. Any user with the [Sandbox Admin](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox) role can set this flag. Setting it can give sandboxes Node access comparable to that of a cluster administrator.

## Trigger an on-demand runner update

When `updateAvailable` is `true` on the runner, you can apply the update immediately rather than wait for the next maintenance window:

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner upgrade prod-us-east-1
> ```

> [tab] curl
>
> ```bash title="Apply an available update immediately" theme={"system"}
> curl -X POST https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1:applyAvailableUpdate \
>   -H "Authorization: Bearer $TOKEN"
> ```

The control plane resolves the latest version on the runner's release channel and bumps `target_revision`. The in-cluster controller rolls it out.

## List runners

To see every runner in your organization, or to narrow the view to a specific zone, cluster, or connection state, use the following list commands.

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner get
> ```
>
> Filter by zone, cluster, or connection status. The `--connection-status` flag accepts the short values `CONNECTED` and `DISCONNECTED`:
>
> ```bash theme={"system"}
> cwic sandbox runner get --zone us-east-1
> cwic sandbox runner get --connection-status CONNECTED
> ```

> [tab] curl
>
> ```bash title="List managed runners" theme={"system"}
> curl -H "Authorization: Bearer $TOKEN" \
>   'https://api.coreweave.com/v1/sandbox/managedRunners?pageSize=50&zone=us-east-1'
> ```
>
> The following query parameters are supported:
>
> * `zone`
> * `clusterId`
> * `connectionStatus`
> * `installStatus`
> * `runnerId`
> * `runnerGroupId`
> * `pageSize` (default 50, max 100).
> * `pageToken`
>
> Pagination is cursor-based.

## Delete a runner

Remove a runner when you no longer need sandbox capacity on its cluster, or before you redeploy a fresh runner on the same cluster.

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner delete prod-us-east-1
> ```
>
> The CLI prompts for confirmation. Pass `--yes` to skip the prompt for scripted use:
>
> ```bash theme={"system"}
> cwic sandbox runner delete prod-us-east-1 --yes
> ```

> [tab] curl
>
> ```bash title="Decommission a runner" theme={"system"}
> curl -X DELETE https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1 \
>   -H "Authorization: Bearer $TOKEN"
> ```

> [tab] Terraform
>
> Follow [Remove a runner](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md#remove-a-runner) to review and apply the Terraform deletion plan.

Deleting a runner removes the runner deployment in your cluster. Any sandboxes running on that runner stop. The policy is part of the runner, so it's deleted with it. If you intend to redeploy the cluster, keep the policy document in version control.

> [!WARNING]
>
> Deletion is permanent. If you only want to pause traffic, move sandboxes to another runner before you delete this one.

## See also

For related guidance, see the following pages:

* [Configure Node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md): limit sandbox CPU and memory requests by Node Pool or group of Nodes.
* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): the resource model, how the gateway brokers requests, control plane compared to data plane, and multi-cluster topology.
* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how a sandbox resolves against a policy.
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): every constraint group, with worked examples.
* [Control plane API overview](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md): authentication, field masks, and the request and response shapes for every endpoint.
* [Policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile.md): every field you can set in a policy.
