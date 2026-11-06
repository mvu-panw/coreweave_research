# Webhook integrations

Source: https://docs.coreweave.com/platform/coreweave-alerts/webhooks

# Webhook integrations

> Connect CoreWeave Alerts to Slack or any HTTPS endpoint using a webhook URL

CoreWeave Alerts supports two webhook-based integration types: a Slack webhook integration that sends alerts directly to a Slack channel, and a generic webhook integration that sends alerts to any HTTPS endpoint. After you connect an integration, you can subscribe alerts to these destinations on the [Alert configuration](https://console.coreweave.com/account/alerts/configuration) page.

## Slack webhook integration

As an alternative to the [OAuth flow](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md), you can connect CoreWeave Alerts to Slack using an incoming webhook URL.

### Prerequisites

To complete this integration, you need the following:

* The **Integrations Admin** IAM role, assigned through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies/manage.md).
* A Slack incoming webhook URL. To create one, follow Slack's [Sending messages using incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/) guide.

### Create a Slack webhook integration

1. Log in to the [CoreWeave Cloud Console](https://console.coreweave.com).
2. From the left navigation menu, select **Administration** > **Integrations**, or go directly to the [Integrations](https://console.coreweave.com/organization/integrations) page.
3. In the **Slack** section, click **Create Slack**.
4. Select the **Slack webhook** button.
5. In the **Display name** field, enter a recognizable name (for example, `Cluster-Alerts-Webhook`).
6. In the **Slack Webhook URL** field, enter your Slack incoming webhook URL. The URL must begin with `https://hooks.slack.com/services/`.
7. Click **Create integration**.

### Test the Slack webhook integration

1. On the Cloud Console [Integrations](https://console.coreweave.com/organization/integrations) page, find the Slack webhook integration you created.
2. Locate the vertical ellipsis icon on the right side of the integration row. Expand the menu and click **Send test**. A success message appears in the lower right corner of the Cloud Console.
3. In Slack, verify that the test notification message appears in your channel.
4. Open the [Alert history](https://console.coreweave.com/account/alerts) page. Confirm that the test alert appears with the correct subject, a **Delivered** status, the **Slack webhook** integration type, and a timestamp.

## Generic webhook integration

You can send CoreWeave Alerts to any HTTPS endpoint using a generic webhook integration. Use this integration to connect to third-party tools, custom dashboards, or internal services.

### Prerequisites

To complete this integration, you need the following:

* The **Integrations Admin** IAM role, assigned through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies/manage.md).

### Create a generic webhook integration

1. Log in to the [CoreWeave Cloud Console](https://console.coreweave.com).
2. From the left navigation menu, select **Administration** > **Integrations**, or go directly to the [Integrations](https://console.coreweave.com/organization/integrations) page.
3. In the **Webhook** section, click **Create webhook**.
4. In the **Display name** field, enter a recognizable name.
5. In the **Webhook URL** field, enter your HTTPS endpoint URL.
6. Optional: To create a signing secret, click **Generate signing secret**. CoreWeave includes this secret in the `X-CoreWeave-Signature` header with each request so your endpoint can verify the payload authenticity. Click **Download** to save the secret, and store it securely. You can't view the secret again after you create the integration.
7. Click **Create integration**.

### Webhook payload format

Generic webhook destinations receive a `POST` request with `Content-Type: application/json`. The body has two fields:

| Field | Description |
| :- | :- |
| `subject` | The alert name. Use this to route or summarize alerts on the receiving end. |
| `body` | The rendered alert message, which includes status (Firing or Resolved), description, and affected resources (node, cluster, zone). |

Example payload:

```json theme={"system"}
{
  "body": "GPUWantsReset Status: Firing GPU Recovery Action Changed (Xid 154) indicates the GPU encountered an issue requiring a reset, the detailed reason can be found in related alerts. The node will be restarted when current workloads finish. Affected: node: MyNode01 · cluster: MyCluster09 · zone: ZONE-A1",
  "subject": "GPUWantsReset"
}
```

### Test the generic webhook integration

1. On the Cloud Console [Integrations](https://console.coreweave.com/organization/integrations) page, find the generic webhook integration you created.
2. Locate the vertical ellipsis icon on the right side of the integration row. Expand the menu and click **Send test**. A success message appears in the lower right corner of the Cloud Console.
3. Verify that your endpoint received the test payload.
4. Open the [Alert history](https://console.coreweave.com/account/alerts) page. Confirm that the test alert appears with the correct subject, a **Delivered** status, the **Webhook** integration type, and a timestamp.

### Verify webhook signatures

If you configured a signing secret, CoreWeave sends an `X-CoreWeave-Signature` header with each webhook request. Use this header to verify that incoming requests are authentic.
