# Configure Telemetry Relay

Source: https://docs.coreweave.com/observability/telemetry-forwarding/configure

# Configure Telemetry Relay

> Forward CoreWeave audit logs to HTTPS endpoints or AWS S3 destinations

You can configure CoreWeave Telemetry Relay through the CoreWeave Cloud Console or the [Telemetry Relay API](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api.md). This guide shows you how to use the Cloud Console to forward supported audit logs to HTTPS endpoints or AWS S3 destinations. It also shows you how to view the resulting Telemetry Relay resources.

> [!NOTE]
>
> With self-service, you can forward only supported audit logs to HTTPS endpoints or AWS S3 destinations. [Contact Support](https://docs.coreweave.com/support.md) if you want to forward other telemetry or use a different destination type.

To configure Telemetry Relay, you define the following:

* **Destinations**: Where Telemetry Relay forwards telemetry, such as an HTTPS endpoint.
* **Streams**: Predefined telemetry categories, such as audit logs.
* **Pipelines**: A configuration that links a stream to a destination.

![Telemetry streams connect to endpoints through pipelines, with secrets for endpoint access.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/telemetry-relay.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=b8dfa553ab7c642bc3c76009c4d406c7)

For more information, see [Introduction to Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/relay.md).

## Prerequisites

To configure Telemetry Relay or view destinations and pipelines, you need one of the following [CoreWeave roles](https://docs.coreweave.com/security/iam/access-policies/roles.md):

| Role | Permissions |
| :- | :- |
| Telemetry Relay Admin | Create, read, update, and delete Telemetry Relay components. |
| Telemetry Relay Reader | Read Telemetry Relay components. |

## Create a destination

Use the Cloud Console to create a destination:

1. In the Cloud Console, navigate to [Telemetry Relay](https://console.coreweave.com/telemetry-relay/pipelines) > **Destinations** > **Create destination**.

2. On the **Create destination** page, enter a **Display name** for the destination. The display name appears in the **Destinations** table and in the **Destination** dropdown when you create a pipeline.

3. For **Endpoint type**, select **HTTPS** or **AWS S3**.

   The following image shows **AWS S3** selected as the endpoint type:

   ![Create destination page with AWS S3 selected as the endpoint type.](https://mintcdn.com/coreweave-dbfa0e8d/YEjb_m5CbDiBlhjX/observability/_media/create-aws-s3-destination.png?fit=max\&auto=format\&n=YEjb_m5CbDiBlhjX\&q=85\&s=1b30fd7e59c9fd925a5441424a11a722)

4. Configure the fields for the selected endpoint type:

   * **HTTPS**:
     * For **Endpoint URL**, enter the URL where Telemetry Relay sends telemetry.
     * For **Authentication type**, select the credential scheme Telemetry Relay uses when it connects to the endpoint.
   * **AWS S3**:
     * For **S3 URI**, enter the AWS S3 bucket and optional prefix where Telemetry Relay writes logs. The `[BUCKET-NAME]` placeholder is the bucket name, and `[PREFIX]` is the optional prefix, as in `s3://[BUCKET-NAME]/[PREFIX]/`. You can also enter the Amazon Resource Name (ARN) for an AWS S3 bucket. The Cloud Console converts it to an S3 URI.
     * For **Region**, enter the bucket's AWS region.
     * Enter an **Access key ID** and **Secret access key**.
     * Optional: For temporary credentials, enter a **Session token (optional)**.

5. Click **Submit**.

The new destination appears in the **Destinations** table.

## Create a pipeline

Use the Cloud Console to create a pipeline:

1. In the Cloud Console, navigate to **Telemetry Relay** > **Create pipeline**.
2. On the **Create pipeline** page, fill in the following fields:

   * **Source**: The telemetry stream to forward, such as **CoreWeave API Audit Logs** or **Kubernetes Events**.
   * **Destination**: An existing HTTPS endpoint or AWS S3 destination to receive the stream. The dropdown lists compatible destinations that you created in the **Destinations** tab.

   After you fill in both fields, the read-only **Generated Pipeline Name** field shows the resulting slug. The slug combines the source and destination names (for example, `logs-audit-console-my-endpoint`). You don't enter a name yourself.
3. Click **Submit**.

The new pipeline appears in the **Pipelines** table.

To leave the **Create pipeline** page without saving, click **Back to Pipelines**.

## List destinations

To view destinations:

* In the Cloud Console, navigate to **Telemetry Relay** > **Destinations**. The table lists the **Name**, **Type**, **Region**, and **Endpoint** for each destination.

## List streams

To view available telemetry streams:

* In the Cloud Console, navigate to **Telemetry Relay** > **Create pipeline** > **Source**.

The following image shows the supported streams in the **Source** dropdown:

![List of available telemetry streams in the Create pipeline source dropdown.](https://mintcdn.com/coreweave-dbfa0e8d/YEjb_m5CbDiBlhjX/observability/_media/list-streams.png?fit=max\&auto=format\&n=YEjb_m5CbDiBlhjX\&q=85\&s=c762980e5bb76d7d033bf8cd7abe47ec)

Self-service supports the following streams:

| Display name | API slug |
| :- | :- |
| Console Audit Logs | `logs-audit-console` |
| CoreWeave API Audit Logs | `logs-audit-cw-api` |
| Kubernetes API Audit Logs | `logs-audit-kube-api` |
| Kubernetes Events | `logs-events` |

The Telemetry Relay API exposes the same streams through slug identifiers.

To leave the **Create pipeline** page without creating a pipeline, click **Back to Pipelines**.

## List pipelines

To view pipelines:

* In the Cloud Console, navigate to **Telemetry Relay**. The **Pipelines** tab opens by default. Each row shows the autogenerated pipeline name, source stream, and destination.

## Advanced configuration

For destination types and telemetry streams that self-service doesn't support, contact Support.

Support can enable the following configurations:

* Prometheus Remote Write v1-compatible endpoints for metrics.
* Forwarding for streams outside the self-service scope, such as system journal logs, customer cluster metrics, and platform metrics.
