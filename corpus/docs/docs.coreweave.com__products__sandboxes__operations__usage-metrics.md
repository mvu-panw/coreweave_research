# View sandbox usage

Source: https://docs.coreweave.com/products/sandboxes/operations/usage-metrics

# View sandbox usage

> Track sandbox billing, client activity, and fleet resource metrics.

Serverless sandbox usage appears in the Forge console with your organization's other billable products. Organization admins see usage across all teams. Team admins see the same charts, limited to the teams they administer.

## View usage over time

> [!NOTE]
>
> This feature isn't enabled for every organization yet. If you don't see it, contact [Support](mailto:forge-support@coreweave.com) or your AISE.

Select your deployment type:

> [tab] Multi-tenant Cloud
>
> 1. Click the account selector in the upper-right corner. If your organization isn't the current account, select it under **Other accounts**, then open the menu again.
> 2. In the **Account** section, click **Billing**.
> 3. Click the **Usage & Alerts** tab.
> 4. From the sidebar, select **Sandboxes** to display its **Usage over time** chart.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. Click the account selector in the upper-right corner.
> 2. Click **Organization dashboard**.
> 3. Click **Usage & Alerts**.
> 4. From the sidebar, select **Sandboxes** to display its **Usage over time** chart.

For the chart controls and the other usage categories, see [Manage billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md#view-usage-over-time).

Forge sandbox billing doesn't support usage or spend alerts on any plan.

## Log sandbox metrics to a Weights & Biases run

A `Session` can log client-side sandbox metrics, such as sandboxes created, executions, success rates, and startup times, to your active Weights & Biases run. These metrics describe how your code uses sandboxes. They don't report CPU or memory use. To turn them on and see the full list, see the Weights & Biases metrics integration section of [RL training](https://docs.coreweave.com/products/sandboxes/client/guides/rl-training.md).

## Monitor CoreWeave organization metrics

CoreWeave Sandboxes publish per-organization metrics that describe every active sandbox: how many are running, what resources they requested, and how much CPU and memory they're consuming. Use these metrics to track fleet activity, attribute usage, and build your own dashboards and alerts. To compare reserved capacity against consumption, see [Size sandbox CPU and memory](https://docs.coreweave.com/products/sandboxes/resource-sizing.md).

### Prerequisites

The metrics are available in the [Explore section](https://docs.coreweave.com/observability/managed-grafana.md) of CoreWeave Grafana. To access Grafana, sign in to the [CoreWeave Cloud Console](https://console.coreweave.com/).

To query metrics, you need the [Observability Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry) role in an [Identity and Access Management (IAM) access policy](https://docs.coreweave.com/security/iam/access-policies.md). In the legacy CoreWeave permissions model, membership in the [`metrics` group](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions) grants equivalent access. For details, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md#prerequisites).

You can also query the same metrics programmatically through the [metrics API](https://docs.coreweave.com/observability/logs-metrics/introduction.md) at `observe.coreweave.com` with an API access token.

> [!NOTE]
>
> Queries are automatically scoped to your organization. Selectors on `cluster` or `cluster_org` are rewritten to your organization, so a query that references another organization returns your own data rather than an empty result.

### Common labels

All `cwsandbox_*` metrics carry the following labels:

| Label | Description | Example | Notes |
| - | - | - | - |
| `org_id` | Your Organization ID | `abc123` | Always your own organization. |
| `cluster` | Constant, equal to `org_id` | `abc123` | Sandbox metrics always live under this pseudo-cluster, regardless of where sandboxes are placed. |
| `cluster_org` | The Organization ID | `abc123` | Queries are automatically scoped to the organization. |
| `region` | The Region serving the sandbox fleet | `US-EAST-02` | See [the list of Regions](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). |
| `zone` | The Zone serving the sandbox fleet | `US-EAST-02A` | See [the list of Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). |

The label contract is identical whether your sandboxes run on CoreWeave-managed shared capacity or on your own CoreWeave Kubernetes Service (CKS) clusters with a [managed runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md). To break usage down by placement, group by the `runner_id` label on `cwsandbox_sandbox_info`.

### Lifecycle metrics

These metrics come from the sandbox control plane and update about every 30 seconds. Per-sandbox series exist while the sandbox is active and disappear shortly after it stops.

#### Metric `cwsandbox_sandboxes`

The number of active sandboxes in each lifecycle state. Units are in sandboxes.

The following labels are available for filtering and grouping:

| Label | Description | Example | Notes |
| - | - | - | - |
| `state` | The lifecycle state | `RUNNING` | Values are `PLACING`, `CREATING`, `RUNNING`, and `TERMINATING`. Stopped and completed sandboxes are excluded. |

#### Metric `cwsandbox_sandbox_info`

A constant `1` series that carries the identity of each active sandbox. Use it to join identity labels onto the usage metrics.

The following labels are available for filtering and grouping:

| Label | Description | Example | Notes |
| - | - | - | - |
| `sandbox_id` | The sandbox ID | `0e0394fc-877b-4971-8e97-b99ea4f6bcd5` | Matches the ID returned when the sandbox started. |
| `profile_id` | The legacy profile ID, if any | `""` or `default` | Empty for policy-based `v1` placements. See [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md#what-changed-from-profiles). |
| `runner_id` | The runner serving the sandbox | `prod-east-14-managed` | Identifies placement, including your own [managed runners](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md). |
| `image` | The sandbox container image | `python:3.11-slim` | The image the sandbox was started with. |

For legacy `v1beta2` placements, the `profile_id` label contains the profile the runner resolves, including an automatically selected or default profile. For policy-based `v1` placements, you don't select a profile or policy, and the `profile_id` label is empty. Prometheus treats an empty label as absent.

#### Metric `cwsandbox_sandbox_age_seconds`

The age of each active sandbox since creation. Units are in seconds. Labeled by `sandbox_id`.

#### Metric `cwsandbox_sandbox_requested_cpu_millicores`

The CPU each sandbox requested at admission, not measured usage. Units are in millicores. Labeled by `sandbox_id`.

#### Metric `cwsandbox_sandbox_requested_memory_bytes`

The memory each sandbox requested at admission, not measured usage. Units are in bytes. Labeled by `sandbox_id`.

#### Metric `cwsandbox_sandbox_requested_gpus`

The GPUs each sandbox requested at admission. Units are in GPUs. Labeled by `sandbox_id` and `gpu_type`.

### Usage metrics

These metrics are measured on the node running each sandbox and update about every 30 seconds.

#### Metric `cwsandbox_sandbox_cpu_usage_seconds_total`

A counter of the CPU time each sandbox has consumed. Units are in CPU seconds. Labeled by `sandbox_id`. Use `rate()` or `increase()` to compute consumption over a window.

#### Metric `cwsandbox_sandbox_memory_working_set_bytes`

The current working-set memory of each sandbox. Units are in bytes. Labeled by `sandbox_id`.

> [!NOTE]
>
> Usage values reflect the sandbox workload container. For sandboxes running on microVM isolation, the values come from inside the guest and exclude virtualization overhead and platform sidecar processes. The CPU counter resets if the workload container restarts, which `rate()` and `increase()` handle automatically. A short gap in a series means collection was briefly interrupted. Stale values are never reported.

### PromQL examples

#### Running sandboxes over time

```promql theme={"system"}
sum(cwsandbox_sandboxes{state="RUNNING"})
```

#### CPU cores in use per sandbox

```promql theme={"system"}
rate(cwsandbox_sandbox_cpu_usage_seconds_total[5m])
```

#### CPU usage enriched with sandbox identity

Join the usage counter with `cwsandbox_sandbox_info` on `sandbox_id` to attach the runner, image, and legacy profile labels. The join also works for policy-based `v1` sandboxes, where the `profile_id` label is empty:

```promql theme={"system"}
rate(cwsandbox_sandbox_cpu_usage_seconds_total[5m])
* on (sandbox_id) group_left (profile_id, runner_id, image)
cwsandbox_sandbox_info
```

#### Total memory in use across the fleet

```promql theme={"system"}
sum(cwsandbox_sandbox_memory_working_set_bytes)
```

#### CPU efficiency, used versus requested

```promql theme={"system"}
sum(rate(cwsandbox_sandbox_cpu_usage_seconds_total[5m]))
/
(sum(cwsandbox_sandbox_requested_cpu_millicores) / 1000)
```

#### Requested GPUs by type

```promql theme={"system"}
sum by (gpu_type) (cwsandbox_sandbox_requested_gpus)
```

#### Longest-running sandboxes

```promql theme={"system"}
topk(10, cwsandbox_sandbox_age_seconds)
```
