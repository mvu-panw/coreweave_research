# Introduction to CoreWeave Alerts

Source: https://docs.coreweave.com/platform/coreweave-alerts

# Introduction to CoreWeave Alerts

> Configure which alerts your organization receives and where they're delivered

CoreWeave Alerts delivers real-time notifications about your clusters, deployments, and operations. This page introduces the two areas you manage in the Cloud Console to control which alerts your organization receives and where they're delivered:

* **Destinations** determine where CoreWeave delivers alerts. In-app delivery is on by default, so alerts appear on the Cloud Console [Alert history](https://console.coreweave.com/account/alerts) page without any setup. You can also connect Slack or a webhook to extend delivery outside the Cloud Console. Enabling an additional destination doesn't disable in-app. Manage destinations on the [Integrations](https://console.coreweave.com/organization/integrations) page.
* **Alert configuration** determines which alerts your organization receives and which destinations each one goes to. Manage subscriptions on the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page.

The [Alert history](https://console.coreweave.com/account/alerts) page shows delivery status for every destination that received the alert. Click an entry to see each destination, its integration type, delivery status, and timestamp.

For the IAM roles required to access these pages, see [Before you begin](#before-you-begin). To manage destinations and alert configuration programmatically, see the [CoreWeave Alerts API](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md).

## Destinations

CoreWeave Alerts supports four destination types. In-app delivery is on by default and doesn't need to be configured.

| Destination type | Description |
| :- | :- |
| In-app | Delivers alerts to the Cloud Console [Alert history](https://console.coreweave.com/account/alerts) page. On by default for every organization. |
| Slack OAuth | Connects through an authorization flow to your Enterprise Slack workspace. Supports alert threading and multiple channels from a single authorization. |
| Slack Webhook | Connects to a single Slack channel using an incoming webhook URL. |
| Generic Webhook | Sends alerts to any HTTPS endpoint, with optional signature verification. |

> [!NOTE]
>
> Your organization can have at most one Slack destination (either Slack OAuth or Slack webhook) and one generic webhook destination at a time. To switch types, you must delete the existing destination before creating a new one.

Each entry on the [Alert history](https://console.coreweave.com/account/alerts) page shows the subject, delivery status, and timestamp. Click an entry to see every destination that received the alert.

### Destination type comparison

| Aspect | Slack OAuth | Slack Webhook | Generic Webhook |
| :- | :- | :- | :- |
| **Setup** | Multi-step authorization flow | Paste a Slack incoming webhook URL | Paste an endpoint URL, optionally configure a signing secret |
| **Bot identity** | Messages appear from CoreWeave Mission Control | Messages appear from the webhook app | N/A |
| **Channel flexibility** | Connect multiple channels from a single authorization | One webhook URL per channel | Any HTTPS endpoint |
| **Alert threading** | Can edit, reply to, and create threads on existing alerts | New message per alert | N/A |

## Alert configuration

On the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page, each alert has an independent toggle per destination, including in-app. The page groups alerts by category (such as Storage, AI Object Storage, GPU (hardware health and runtime errors), and SUNK) and tags each one with a severity of **Critical**, **Warning**, or **Info**. For each alert, you can do the following:

* Toggle delivery per destination. Enabling Slack or a webhook is additive. In-app stays on unless you explicitly turn it off.
* Use **Configure all** on a category to apply the same destination settings to every alert in that category at once.

An alert row shows **Disabled** when you turn off all destination toggles for that alert. This is intentional. The alert isn't delivered until you re-enable at least one destination.

For a walkthrough, see [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md).

### Alert reference by product

The following pages list the individual alerts in a category, the condition that triggers each one, and the metrics behind them:

* [Object storage alerts](https://docs.coreweave.com/products/storage/object-storage/monitoring/alerts.md): the **AI Object Storage** category.
* [Distributed File Storage alerts](https://docs.coreweave.com/products/storage/distributed-file-storage/monitoring/alerts.md): the **Storage** category.

## Before you begin

CoreWeave splits access to alerts between two areas, each with its own IAM roles. Grant these through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies/manage.md).

| Task | Required role |
| :- | :- |
| View the Integrations page and the destinations list | **Integrations Viewer** (`READ_INTEGRATIONS`) |
| Create, update, or delete Slack and webhook destinations | **Integrations Admin** (`WRITE_INTEGRATIONS`) |
| View the Alert configuration and Alert history pages | **Alerts Viewer** (`READ_NOTIFICATIONS`) |
| Subscribe or unsubscribe alerts on the Alert configuration page | **Alerts Admin** (`WRITE_NOTIFICATIONS`) |

> [!NOTE]
>
> The [Administrator default policy](https://docs.coreweave.com/security/iam/access-policies.md#default-access-policies) includes all available roles, including the Notifications and Integrations roles. Principals assigned to it can use CoreWeave Alerts without additional setup. If your organization uses legacy permissions, the `admin` group doesn't automatically include the Notifications or Integrations roles. You must create an IAM Access Policy to grant them explicitly.

## Set up an integration

The following cards link to step-by-step setup guides for each integration type.

> [card] [Slack OAuth integration](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md)
>
> Connect CoreWeave Alerts to your Enterprise Slack workspace using the OAuth authorization flow

> [card] [Webhook integrations](https://docs.coreweave.com/platform/coreweave-alerts/webhooks.md)
>
> Connect CoreWeave Alerts to Slack or any HTTPS endpoint using a webhook URL

## Configure alerts

> [card] [Configure alerts](https://docs.coreweave.com/platform/coreweave-alerts/alert-configuration.md)
>
> Choose which alerts your organization receives and which destinations each one goes to
