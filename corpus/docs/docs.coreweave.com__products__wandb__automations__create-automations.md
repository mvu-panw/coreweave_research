# Overview

Source: https://docs.coreweave.com/products/wandb/automations/create-automations

# Overview

> Create and manage W&B automations to streamline your ML workflows

This page shows how to create and manage [automations](https://docs.coreweave.com/products/wandb/automations.md), which start in response to specific events in Weights & Biases. When a specific event occurs within an organization, team, project, registry, or collection, the automation notifies a Slack channel, runs a webhook, or sends a prompt to ARIA. Use this overview to understand the prerequisites and high-level workflow, then follow the detailed instructions in [Create a Slack automation](https://docs.coreweave.com/products/wandb/automations/create-automations/slack.md), [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md), or [Create an ARIA automation](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md).

> [!NOTE]
>
> Looking for companion tutorials for automations?
>
> * [Learn to automatically trigger a GitHub Action for model evaluation and deployment](https://forge.coreweave.com/wandb/wandb/wandb-model-cicd/reports/Model-CI-CD-with-W-B--Vmlldzo0OTcwNDQw).
> * [Watch a video demonstrating automatically deploying a model to a SageMaker endpoint](https://www.youtube.com/watch?v=s5CMj_w3DaQ).
> * [Watch a video series introducing automations](https://youtube.com/playlist?list=PLD80i8An1OEGECFPgY-HPCNjXgGu-qGO6\&feature=shared).

## Requirements

When creating automations:

* A team admin can create and manage automations for the team's projects, as well as components of their automations, such as webhooks, secrets, and Slack integrations. Refer to [Team settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md).
* To create a registry automation, you must have access to the registry. Refer to [Configure Registry access](https://docs.coreweave.com/products/registry/configure_registry.md#registry-roles).
* To create a Slack automation, you must have permission to post to the Slack instance and channel you select.

## Create an automation

You can create an automation from the global **Automations** hub in the left navigation, from a project or registry's **Automations** tab, or directly from a line plot panel in the workspace. When you create an automation from the hub, you choose its scope (Organization, Team, Registry, Registry collection, or project). See [Automations hub](https://docs.coreweave.com/products/wandb/automations.md#automations-hub).

### Create from the Automations tab

At a high level, to create an automation from the **Automations** tab, follow these steps:

1. If necessary, [create a Forge secret](https://docs.coreweave.com/products/wandb/platform/secrets.md) for each sensitive string required by the automation, such as an access token, password, or SSH key. Secrets let you reuse sensitive strings safely and keep them out of automation configurations. Define secrets in your **Team Settings**. Webhook automations most commonly use secrets.
2. Configure team-level webhook or Slack integrations to authorize Weights & Biases to post to Slack or run the webhook on your behalf. Multiple automations can use a single webhook or Slack integration. Define these actions in your **Team Settings**.
3. In the project or registry, create the automation, which specifies the event to watch for and the action to take (such as posting to Slack or running a webhook). When you create a webhook automation, you configure the payload it sends.

After you complete these steps, the automation runs whenever the specified event occurs in the project or registry.

### Create a run metric automation from a workspace panel

From a line plot in the workspace, you can also create a [run metric automation](https://docs.coreweave.com/products/wandb/automations/automation-events.md#run-events) for the metric it shows:

1. Hover over the panel, then click the bell icon at the top of the panel.

   ![Automation bell icon location](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/run_metric_automation_from_panel.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=122de71b7adaba2a371fb0697b4662a0)
2. Configure the automation using the basic or advanced configuration controls. For example, apply a run filter to limit the scope of the automation, or configure an absolute threshold.

For details, refer to:

* [Create a Slack automation](https://docs.coreweave.com/products/wandb/automations/create-automations/slack.md)
* [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md)
* [Create an ARIA automation](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md)

## View and manage automations

View and manage automations from a project or registry's **Automations** tab:

* To view an automation's details, click its name.
* To view an automation's execution history (which actions ran and whether they succeeded), click its name and select the **History** tab. For more information, see [View an automation's history](https://docs.coreweave.com/products/wandb/automations/view-automation-history.md).
* To edit an automation, click its **action ()** menu, then click **Edit automation**.
* To delete an automation, click its **action ()** menu, then click **Delete automation**.

## Go further

For more information, see the following resources:

* [Automations tutorials](https://docs.coreweave.com/products/wandb/automations/tutorial.md): Build a [project run failure alert](https://docs.coreweave.com/products/wandb/automations/project-automation-tutorial.md) or a [registry alias-to-webhook automation](https://docs.coreweave.com/products/wandb/automations/registry-automation-tutorial.md) in the W\&B App.
* [Automation events and scopes](https://docs.coreweave.com/products/wandb/automations/automation-events.md).
* [Create a Slack automation](https://docs.coreweave.com/products/wandb/automations/create-automations/slack.md).
* [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md).
* [Create an ARIA automation](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md).
* [Create a secret](https://docs.coreweave.com/products/wandb/platform/secrets.md).
