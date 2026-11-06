# Automation events and scopes

Source: https://docs.coreweave.com/products/wandb/automations/automation-events

# Automation events and scopes

> Learn about events and scopes that trigger W&B Automations, including artifact changes, run status, and metric conditions.

An automation starts when a specific event occurs within a given scope: an organization, a team, a project, a registry, or a collection. This page describes the events that can trigger an automation within each scope, so you can choose the right trigger when you configure an automation. Learn more about automations in the [Automations overview](https://docs.coreweave.com/products/wandb/automations.md) or [Create an automation](https://docs.coreweave.com/products/wandb/automations/create-automations.md).

Scopes are hierarchical: an Organization contains Teams, which contain projects and registries. Both projects and registries contain collections: a project contains the artifact collections logged to it, and a registry contains the collections that artifact versions are linked to. An automation observes its event across everything in its scope, including projects, registries, and collections created later. A single event can match automations at more than one scope. Each matching automation triggers independently.

To protect against excessive triggering at broad scopes, Weights & Biases applies a rate limit and a cooldown per automation. These safeguards can delay or skip repeated triggers of the same automation.

> [!NOTE]
>
> The Team and Organization scopes are available on W\&B Multi-tenant Cloud and on W\&B Dedicated Cloud (Server v0.83.0 and later). The Registry and Project scopes are available on all deployment types.

## Scope reference

| Scope | What the automation watches | Events available in the W\&B App |
| - | - | - |
| [Organization](#organization) | Every Team, project, registry, and collection in the organization, including ones created in the future. | Artifact and collection events, such as when a new version is added or linked, or when an alias or tag is added. Run-based events aren't available. |
| [Team](#team) | Every project, registry, and collection the Team owns, including ones created in the future. | The same artifact and collection events as the Organization scope. Run-based events aren't available. |
| [Registry](#registry) | Every collection in one registry, including collections added in the future. | [Registry events](#registry-events): a new version is linked to a collection, or an artifact alias is added. |
| [Project](#project) | Every collection in one project. Some events let you narrow the scope further. | [Artifact events](#artifact-events), [run events](#run-events), and [sandbox events](#sandbox-events). |

The following sections describe each scope in more detail.

## Organization

Use the Organization scope to define a policy once and apply it everywhere. For example, notify a compliance Slack channel whenever the `production` alias is added to any artifact in the organization.

Run-based events (the [run status change](#run-status-change) and [run metric](#run-metrics-change) events) aren't available at the Organization scope in the W\&B App.

## Team

Use the Team scope to apply a policy to everything one Team owns. A Team-scoped automation watches for the same artifact and collection events as the Organization scope. Run-based events aren't available at the Team scope in the W\&B App.

## Registry

A [Registry](https://docs.coreweave.com/products/registry.md) automation watches for the event taking place on any collection within a specific registry, including collections added in the future.

### Events&#x20;

A Registry automation can watch for these events:

* **A new version is linked to a collection**: Test and validate new models or datasets when they're added to a registry.
* **An artifact alias is added**: Trigger a specific step of your workflow when a new artifact version has a specific alias applied. For example, deploy a model when it has the `production` alias applied.

When the automation calls a webhook, it can access the same team-level webhook configurations and [team secrets](https://docs.coreweave.com/products/wandb/platform/secrets.md) as project-scoped automations.

## Project

A project-level automation watches for the event taking place on any collection in the [project](https://docs.coreweave.com/products/wandb/track/project-page.md). Depending on the event you specify, you can further limit the scope of the automation.

### Artifact events

This section describes the events related to an artifact that can trigger an automation.

* **A new version is added to an artifact**: Apply recurring actions to each version of an artifact. For example, start a training job when a new dataset artifact version is created.
* **An artifact alias is added**: Trigger a specific step of your workflow when a new artifact version in a project has an alias applied that matches the **Alias regex** you specify. For example, run a series of downstream processing steps when an artifact has the `test-set-quality-check` alias applied, or run a workflow each time a new artifact version has the `latest` alias. Only one artifact version can have a given alias at a time.
* **An artifact tag is added**: Trigger a specific step of your workflow when an artifact version in a project has a tag applied that matches the **Tag regex** you specify. For example, specify `^europe.*` to trigger a geo-specific workflow when a tag beginning with the string `europe` is added to an artifact version. Use artifact tags for grouping and filtering. You can assign the same tag to multiple artifact versions.

### Run events

The following sections describe how to configure an automation that starts based on a change in a [run's status](https://docs.coreweave.com/products/wandb/runs/run-states.md) or a change in a [run's metric value](https://docs.coreweave.com/products/wandb/track/log.md#what-data-is-logged-with-specific-wb-api-calls).

#### Run status change

> [!NOTE]
>
> * Currently available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud) and [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-dedicated-cloud).
> * A run with **Killed** status can't trigger an automation. This status indicates that an admin forcibly stopped the run.

Trigger a workflow when a run changes its [status](https://docs.coreweave.com/products/wandb/runs/run-states.md) to **Running**, **Finished**, or **Failed**. Optionally, you can further limit the runs that can trigger an automation by specifying a user or run name filter.

![Screenshot showing a run status change automation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/run_status_change.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=be965be8dda7da6ced6be15729fc1399)

Because run status is a property of the entire run, you can create a run status automation only from the **Automations** page, not from a workspace.

#### Run metrics change

> [!NOTE]
>
> Currently available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud) and [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-dedicated-cloud).

Trigger a workflow based on a logged value for a metric, either a metric in a run's history or a [system metric](https://docs.coreweave.com/products/wandb/ref/python/experiments/system-metrics.md) such as `cpu`, which tracks the percentage of CPU utilization. Weights & Biases logs system metrics automatically every 15 seconds.

You can create a run metrics automation from the project's **Automations** tab or directly from a line plot panel in a workspace.

To set up a run metric automation, configure how to compare the metric's value with the threshold you specify. Your choices depend on the event type and on any filters you specify.

Optionally, you can further limit the runs that can trigger an automation by specifying a user or run name filter.

##### Threshold

Use a threshold event to start an automation when a metric crosses a fixed value. For **Run metrics threshold met** events, configure:

1. The window of most recently logged values to consider (defaults to 5).
2. Whether to evaluate the **Average**, **Min**, or **Max** value within the window.
3. The comparison to make:
   * Above
   * Above or equal to
   * Below
   * Below or equal to
   * Not equal to
   * Equal to

For example, trigger an automation when average `accuracy` is above `0.6`.

![Screenshot showing a run metrics threshold automation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/run_metrics_threshold_automation.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=88b9cebb9df9bf7efe974ca5d6440373)

##### Change threshold

Use a change threshold event to start an automation when a metric shifts between two recent windows of values. For **Run metrics change threshold met** events, the automation uses two "windows" of values to check whether to start:

* The *current window* of recently logged values to consider (defaults to 10).
* The *prior window* of recently logged values to consider (defaults to 50).

The current and prior windows are consecutive and don't overlap.

To create the automation, configure:

1. The current window of logged values (defaults to 10).
2. The prior window of logged values (defaults to 50).
3. Whether to evaluate the values as relative or absolute (defaults to **Relative**).
4. The comparison to make:
   * Increases by at least
   * Decreases by at least
   * Increases or decreases by at least

For example, trigger an automation when average `loss` decreases by at least `0.25`.

![Screenshot showing a run metrics change threshold automation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/run_metrics_change_threshold_automation.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=ca0a2d5ae20d634ea840edc8b1f126ad)

#### Run metrics z-score change

> [!NOTE]
>
> Currently available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud) and [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-dedicated-cloud).

Weights & Biases can trigger an automation when a metric's z-score (standard score) exceeds a specified threshold. A z-score measures how many standard deviations the value is from the mean for that metric across a configurable window of runs in the project (defaults to 30 runs).

To use a z-score as an event trigger, select the **Run metrics z-score threshold met** event.

Automations based on z-score keep your team informed about unusual performance without checking absolute thresholds, which may vary as your model or training process evolves.

You can create a run metrics z-score automation from the project's **Automations** tab or directly from a line plot panel in a workspace.

To create a z-score automation, configure:

1. The target z-score threshold, expressed as a positive float value (for example, 2.0).
2. The window of logged values that determine the mean value (defaults to 30).
3. The comparison to make:
   * Above (triggers when performance is unusually high).
   * Below (triggers when performance is unusually low).
   * Either above or below.

For example, trigger an automation when `accuracy` has a z-score above 2, which means the run is performing well above other runs in the project.

Z-score values have the following meanings:

* A z-score of 0 means the metric is at the average.
* A z-score of +2.0 means the metric is 2 standard deviations above average.
* A z-score of -2.0 means the metric is 2 standard deviations below average.
* Values beyond ±2 are often considered statistically significant outliers.

#### Run filters

This section describes how the automation selects runs to evaluate.

By default, any run in the project triggers the automation when the event occurs. You can limit which runs trigger an automation by configuring one of the following filters:

| Filter | Description |
| - | - |
| **Filter to one user's runs** | Include only runs created by the specified user. |
| **Filter on run name** | Include only runs whose names match the given regular expression. |

The automation evaluates each run as follows:

* Each run is considered individually and can potentially trigger the automation.
* Each run's values are put into a separate window and compared to the threshold separately.
* In a 24-hour period, a particular automation can fire at most once per run.

For details, see [Create automations](https://docs.coreweave.com/products/wandb/automations/create-automations.md).

### Sandbox events

> [!NOTE]
>
> * Available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud).
> * Sandbox events are available only to organizations with access to [CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes.md).

This section describes the [sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md) events that can trigger an automation.

#### Sandbox status change

Trigger a workflow when a sandbox in the project is created, completes, or fails. For example, post to a Slack channel when a sandbox fails, or call a webhook that collects a sandbox's results when it completes.

To configure the automation, select one or more of the following states:

| State | When the automation starts |
| - | - |
| **Created** | The sandbox is scheduled and its container starts provisioning. A sandbox that fails before it's scheduled never reaches this state, but it still reaches **Failed**. |
| **Completed** | The sandbox reaches the `COMPLETED` state. Its main process exits with code `0`, or the sandbox is stopped. You can stop it with `Sandbox.stop()` or by exiting a `with Sandbox.run()` block. |
| **Failed** | The sandbox reaches the `FAILED` state. It fails to start, reaches its restart limit, or reaches its maximum lifetime. |

You can create a sandbox status automation at the Project scope, from the project's **Automations** tab.

##### Sandboxes that trigger an automation

A sandbox starts a project's automation only when all of the following are true:

* **The sandbox belongs to the project**: A sandbox belongs to the entity and project in your Weights & Biases settings. Examples include the `WANDB_ENTITY` and `WANDB_PROJECT` environment variables. If you don't set a project, the sandbox belongs to a project named `sandbox` in your default entity.
* **The sandbox uses a Forge API key**: Pass `auth=AuthStrategy.WANDB` when you create the sandbox or session. A sandbox created with a CoreWeave API access token doesn't start automations. For details, see [Choose authentication](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#choose-authentication).
* **The sandbox's creator can access the project**: The automation runs as the user who created the sandbox. If that user can no longer access the project when the event occurs, the automation doesn't start.

Because the automation runs as the sandbox's creator, `${event_author}` is that user, even if another user stopped the sandbox.

##### Sandbox variables

Webhook payloads and ARIA prompts can include the following variables, in addition to the standard variables such as `${project_name}`, `${entity_name}`, and `${event_author}`:

| Variable | Description |
| - | - |
| `${sandbox_id}` | The ID of the sandbox that triggered the action. |
| `${sandbox_state}` | The state the sandbox reached: `created`, `completed`, or `failed`. |
| `${sandbox_status}` | The sandbox's status when the event occurred. |
| `${sandbox_reason}` | The reason the sandbox reached its state, if one was reported. For example, the reason for a failed sandbox can describe an image pull error or a non-zero exit code. |
| `${sandbox_tags}` | The sandbox's tags, separated by commas. |
| `${sandbox_creator}` | The username of the user who created the sandbox. |

The reason is free text, so its wording can change. Use it to explain an outcome in a message, not to make decisions in your workflow. Weights & Biases escapes `${sandbox_reason}` and `${sandbox_tags}` in webhook payloads, so their contents can't break the JSON.

For example, the following webhook payload reports a failed sandbox:

```json theme={"system"}
{
  "text": "Sandbox ${sandbox_id} ${sandbox_state} in ${entity_name}/${project_name}: ${sandbox_reason}",
  "creator": "${sandbox_creator}",
  "tags": "${sandbox_tags}"
}
```

A Slack notification for a sandbox event includes the following information:

* Sandbox ID
* State
* Status
* Creator
* Project

In the [automation's history](https://docs.coreweave.com/products/wandb/automations/view-automation-history.md), each execution shows the following information:

* Sandbox ID
* State
* Reason
* Project

## Next steps

* [Create a Slack automation](https://docs.coreweave.com/products/wandb/automations/create-automations/slack.md)
* [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md)
