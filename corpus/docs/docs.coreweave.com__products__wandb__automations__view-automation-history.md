# View an automation's history

Source: https://docs.coreweave.com/products/wandb/automations/view-automation-history

# View an automation's history

> View the execution history of your W&B Automations to check status, triggering events, and action results.

> [!NOTE]
>
> Automation execution history is available on W\&B Multi-tenant Cloud, W\&B Dedicated Cloud, and W\&B Self-Managed v0.75.0 and later.

This page describes how to view and understand the execution history of your W\&B [automations](https://docs.coreweave.com/products/wandb/automations.md). Execution history shows what triggered an automation, what actions ran, and whether they succeeded or failed. Reviewing automation history helps you confirm that automations run as expected, troubleshoot failures, and audit which events triggered downstream actions.

Each executed automation generates a record that includes:

* **Execution timestamp**: When the automation triggered.
* **Triggering event**: The specific event that triggered the automation.
* **Status**: The execution's status. See [Execution status](#execution-status).
* **Action details**: Information about which action ran, such as notifying a Slack channel, running a webhook, or sending a prompt to ARIA.
* **Result details**: Additional information, if any, about the final outcome of the automation, including the error for a failed execution.

Automation history is available for automations at any scope. On any deployment type, you can view history from a registry's or project's **Automations** tab. Select the **Registry** or **Project** tab for detailed instructions.

On W\&B Multi-tenant Cloud and W\&B Dedicated Cloud (Server v0.83.0 and later), you can also view history from the global **Automations** hub in the left navigation: click an automation's name to view its execution history alongside its configuration, including for Team-scoped and Organization-scoped automations. See [Automations hub](https://docs.coreweave.com/products/wandb/automations.md#automations-hub).

> [tab] Registry
>
> 1. Click **Registry** in the project sidebar.
>
> 2. Select your registry from the list.
>
> 3. Navigate to the **Automations** tab, which lists the registry's automations. Click the **Last execution** timestamp to view the execution history details. Use the search bar to filter by automation name, and sort by the last triggered date to find recently executed automations.
>
> 4. View the registry's automation executions in reverse chronological order in the **Automations history** tab, including the event, action, and status. Click an execution timestamp to view details about a particular execution.
>
> > [!TIP]
> >
> > If a collection has associated automation executions, the icon ![Collection automation execution symbol, a circle with a right-pointing arrow](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/collection-automation-execution-icon.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8717ec3676b4e239b79972ce1b5215f0) displays, along with the number of associated executions.

> [tab] Project
>
> 1. Navigate to your project.
> 2. Click the **Automations** tab in the project sidebar, which lists the project's automations. Click the **Last execution** timestamp to view the execution history details. Use the search bar to filter by automation name, and sort by the last triggered date to find recently executed automations.
> 3. In the **History** tab, view all executions of the project's automations in reverse chronological order. Each execution's metadata displays, including the event, action, and status. Click an execution timestamp to view details about a particular execution.

## Execution details

After locating an execution in the history, use the following information to interpret its status and outcome.

### Execution status

Each automation execution has one of the following statuses:

* **Finished**: The automation completed all actions successfully.
* **Failed**: The automation encountered an error and didn't complete.
* **Pending**: The automation is queued for execution.
* **Skipped**: The automation matched the event but didn't run its action. An [ARIA automation](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md) is skipped when it exceeds its limit of three conversations per minute.

### Execution metadata

Click any execution in the history to view the following details:

* **Event details**: The specific event that triggered the automation, including:
  * Event type (for example, "New artifact version", "Run completed").
  * Entity information, such as run ID or artifact name.
  * User who triggered the event (if applicable).
* **Action details**: Information about what the automation attempted:
  * Action type (Slack notification, webhook, or ARIA).
  * Target (Slack channel or webhook URL).
  * Payload sent (for webhooks) or prompt sent (for ARIA).
* **Result information**:
  * Response status (for webhooks).
  * Any error messages or stack traces (for failed executions).

## Next steps

* [Create an automation](https://docs.coreweave.com/products/wandb/automations/create-automations.md)
* [Automation events and scopes](https://docs.coreweave.com/products/wandb/automations/automation-events.md)
* [Create a secret](https://docs.coreweave.com/products/wandb/platform/secrets.md)
