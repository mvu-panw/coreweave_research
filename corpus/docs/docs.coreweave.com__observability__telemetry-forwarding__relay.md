# Introduction to Telemetry Relay

Source: https://docs.coreweave.com/observability/telemetry-forwarding/relay

# Introduction to Telemetry Relay

> Use Telemetry Relay to forward telemetry to destinations outside of CoreWeave

CoreWeave Telemetry Relay is a managed solution that forwards telemetry to destinations outside CoreWeave's observability platform. Use it to centralize CoreWeave telemetry with data from other systems in your observability stack or security information and event management (SIEM) tools. Telemetry Relay provides the following features:

* **Comprehensive data aggregation**: Imports telemetry data from multiple sources.
* **Flexible routing**: Fine-grained data routed to customer-specified endpoints.
* **Reliable delivery**: Prioritizes data completeness with low latency.
* **Fully managed with easy configuration**: Zero operational overhead for configuring data filters and endpoint routing.

Telemetry Relay supports multiple data streams and endpoints.

![Telemetry streams connect to endpoints through pipelines, with secrets for endpoint access.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/telemetry-relay.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=b8dfa553ab7c642bc3c76009c4d406c7)

Telemetry Relay is built from the following components:

* **Streams**: Predefined telemetry categories, for example, audit logs.
* **Pipelines**: A configuration that links a stream to an endpoint.
* **Endpoints**: Destinations, such as HTTPS endpoints or AWS S3 destinations.

## Configure Telemetry Relay

Configure Telemetry Relay through the [CoreWeave Cloud Console](https://docs.coreweave.com/observability/telemetry-forwarding/configure.md) or the [Telemetry Relay API](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api.md). You can forward the following audit logs to HTTPS endpoints or AWS S3 destinations:

* Console Audit Logs
* CoreWeave API Audit Logs
* Kubernetes API Audit Logs
* Kubernetes Events

Audit log data can also include [Support Access Management](https://docs.coreweave.com/security/support-access-management.md) logs for customers who enable Support Access Management. For other telemetry, destination types, or configuration help, contact [Support](https://docs.coreweave.com/support.md).

> [!NOTE]
>
> Telemetry Relay can't forward application metrics. To forward application metrics, see [Forward application metrics](https://docs.coreweave.com/observability/logs-metrics/forward-metrics.md).

Support can also help you assess feasibility and timelines for the following advanced configurations:

* Data streams, including platform logs and platform metrics beyond the self-service log streams
* Forwarding and filtering, including routing and filtering rules for what gets sent
* Destination types beyond HTTPS endpoints and AWS S3 destinations, including Prometheus Remote Write v1
* Advanced networking requirements

> [!WARNING]
>
> When Telemetry Relay forwards metrics to a default Prometheus deployment, Prometheus may receive a sample twice. Prometheus accepts the first sample and logs errors about rejected time samples for the duplicates. To avoid this, use a horizontally scalable, multi-tenant Prometheus deployment that handles duplicate samples.
