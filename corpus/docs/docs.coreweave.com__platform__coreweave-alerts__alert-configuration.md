# Configure alerts

Source: https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration

# Configure alerts

> Choose which alerts your organization receives and where each one is delivered

Organization administrators use the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page to choose which CoreWeave Alerts their organization receives and which destinations each one uses. Subscribe or unsubscribe alerts per destination so your team gets the right signals in the right places. This page is separate from the [Integrations](https://console.coreweave.com/organization/integrations) page, where you connect destinations.

In-app delivery is on by default for every organization, so alerts appear on the Cloud Console [Alert history](https://console.coreweave.com/account/alerts) page. To extend delivery to Slack or a webhook, connect the destination on the Integrations page and then opt alerts in to it. Enabling an additional destination doesn't disable in-app.

## Prerequisites

To view and configure alerts, you need the following:

* The **Alerts Viewer** IAM role to view the Alert configuration page.
* The **Alerts Admin** IAM role to subscribe or unsubscribe alerts.
* The **Integrations Viewer** IAM role to see the list of connected destinations on this page.
* At least one connected destination (in-app is always available, and Slack or webhook are optional). See [CoreWeave Alerts](https://docs.coreweave.com/platform/coreweave-alerts.md) for the full destination list and setup instructions.

Roles are assigned through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies/manage.md).

## Open the alert configuration page

1. Log in to the [CoreWeave Cloud Console](https://console.coreweave.com).
2. From the left navigation menu, select **Alerts** > **Alert configuration**, or go directly to the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page.

The page lists every alert your organization can receive, grouped by category. Each category shows how many alerts in it are enabled.

## Understand the layout

Each alert row shows:

* The alert name and a short description.
* A severity badge: **Critical**, **Warning**, or **Info**.
* The current delivery state. If enabled, the row lists the channels that deliver it (for example, `Enabled: In-app, Slack OAuth`). If you turn off all destination toggles for an alert, the row shows `Disabled`. The alert isn't delivered anywhere until you re-enable at least one destination.

Categories include Storage, AI Object Storage, GPU (hardware health and runtime errors), and SUNK.

## Configure a single alert

Use this flow when you want to tune delivery for one specific alert.

1. On the Alert configuration page, locate the alert you want to change.
2. Click the alert row. A drawer opens with the alert name, severity, description, and a list of every connected destination.
3. Toggle each destination on or off. In-app is on by default and appears alongside any connected Slack or webhook destinations. You can toggle all destinations independently.
4. Click **Save**. The drawer closes and the row updates to show the new delivery state.

## Configure an entire category

Use this flow when you want every alert in a category to behave the same way (for example, send all SUNK alerts to Slack).

1. On the Alert configuration page, locate the category you want to change.
2. In the upper right corner of the category, click **Configure all**. A drawer opens with the connected destinations grouped by channel.
3. Select the channels that should receive every alert in the category. Clear a channel to unsubscribe every alert in the category from that channel.
4. Click **Save**. Every alert in the category now matches your selection.

> [!NOTE]
>
> **Configure all** sets the same subscription state for every alert in the category. If you want a mix (for example, most alerts in Slack but a couple of noisy ones only in-app), configure the category first and then tune individual alerts with the per-alert flow.

## Add or change destinations

The Alert configuration page reads from the list of destinations connected on the Integrations page. To add Slack or a webhook, or to swap one out:

1. Click **Go to integrations** in the callout at the top of the Alert configuration page, or go directly to the [Integrations](https://console.coreweave.com/organization/integrations) page.
2. Follow the [Slack OAuth](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md) or [webhook](https://docs.coreweave.com/platform/coreweave-alerts/webhooks.md) setup instructions.
3. Return to the Alert configuration page. The new destination appears in the per-alert and per-category drawers, ready for you to subscribe alerts to it.

Your organization can have at most one Slack destination and one generic webhook destination at a time. You must delete the existing destination before creating a new one of the same type.

## Verify delivery

After you save subscription changes, confirm that alerts reach the destinations you expect. The [Alert history](https://console.coreweave.com/account/alerts) page shows delivery status for every destination an alert was sent to. Click an alert entry to see each destination, its integration type, delivery status, and timestamp.

* **In-app:** Confirm the alert appears on the Alert history page with a **Delivered** status and a timestamp.
* **Slack and webhook:** Click the alert on the Alert history page to see the delivery status for each destination, then verify the message or payload appeared on the destination itself. Send a test from the [Integrations](https://console.coreweave.com/organization/integrations) page to confirm the destination is reachable. For details, see [Webhook integrations](https://docs.coreweave.com/platform/coreweave-alerts/webhooks.md) and [Slack OAuth integration](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md).
