# Automation tutorial overview

Source: https://docs.coreweave.com/products/wandb/automations/tutorial

# Automation tutorial overview

> Learn to build a project run-failure alert or a registry alias automation.

W\&B Automations follow this pattern: when an **event** occurs and optional **conditions** are met, an **action** runs automatically. For example:

* When a run fails (event), notify a Slack channel (action).
* When the `production` alias is added to an artifact (event), call a webhook to trigger deployment (action).
* When a new model version is linked (event), send a prompt to ARIA to compare it against production (action).

Events and available conditions differ for automations scoped to a [project](https://docs.coreweave.com/products/wandb/automations/automation-events.md#project) or a [registry](https://docs.coreweave.com/products/wandb/automations/automation-events.md#registry). See [Automation events and scopes](https://docs.coreweave.com/products/wandb/automations/automation-events.md).

This page links to two end-to-end tutorials that show you how to create an automation in Weights & Biases. Each tutorial walks through a different scenario, so you can follow the one that matches what you want to build. For detailed guidance, select a tutorial.

* **[Project automation tutorial](https://docs.coreweave.com/products/wandb/automations/project-automation-tutorial.md)**: Alert when a run fails (Slack notification).
* **[Registry automation tutorial](https://docs.coreweave.com/products/wandb/automations/registry-automation-tutorial.md)**: Trigger a webhook when an alias (for example, `production`) is added to an artifact.
