# CoreWeave Observe™

Source: https://docs.coreweave.com/observability

# CoreWeave Observe™

> Learn about observability solutions from CoreWeave Observe™

Observability is critical to monitoring and maintaining the health and performance of a CoreWeave Cloud environment. The collection and visualization of metrics, logs, and events can help to identify potential issues and optimize future workloads. CoreWeave provides a corpus of telemetry data, collecting and indexing over 200 million metrics samples per second across all customer environments.

You can select the observability solutions that best fit your needs.

## Observability solutions

CoreWeave Observe™ offers the following solutions for investigating and operating your CoreWeave environment and for collecting, monitoring, and visualizing logs and metrics:

* **CoreWeave Grafana**: CoreWeave's fully managed Grafana instance provides an immediate observability solution at no cost to customers. Explore performance metrics and preconfigured dashboards optimized to visualize complex workloads. This option requires no setup or maintenance, but doesn't allow for customization of the provided dashboards. See [Introduction to CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md) for more information.

* **Weights & Biases**: Weights & Biases (W\&B) enables AI developers to build AI agents, applications, and models with confidence. When you build models on CoreWeave Kubernetes Service (CKS), you can integrate CoreWeave infrastructure alerts such as GPU failures, thermal violations, and more into your W\&B dashboards. See the [Weights & Biases documentation](https://docs.coreweave.com/products/wandb/runs/infrastructure-alerts.md) for more information.

* **CoreWeave Metrics**: Query metrics with PromQL, the Prometheus Query Language. PromQL is the flexible, expressive language built for querying metrics stored in Prometheus-compatible backends. See [Introduction to CoreWeave Logs and Metrics](https://docs.coreweave.com/observability/logs-metrics/introduction.md) for more information.

* **CoreWeave Logs**: Query logs with LogQL, the Grafana Loki querying language. See [Introduction to CoreWeave Logs and Metrics](https://docs.coreweave.com/observability/logs-metrics/introduction.md) for more information.

* **CoreWeave Telemetry Relay and telemetry forwarding**: Forward telemetry data to endpoints outside of CoreWeave. See [CoreWeave Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/relay.md) for more information.

* **CoreWeave Mission Control Agent**: Investigate your CoreWeave environment through a conversational interface in the Cloud Console. The agent uses the current page and referenced resources as context and returns answers with supporting evidence. Mission Control Agent is in public preview. In organizations where CoreWeave has enabled write tools, it can also perform supported resource changes. For more information, see [Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent.md).

* **CoreWeave Mission Control MCP**: Connect a Model Context Protocol (MCP)-compatible AI client to CoreWeave APIs and observability data through a hosted server. Available tools inherit your existing CoreWeave permissions, and organization-gated write tools can modify supported resources. For more information, see [Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md).

* **Self-hosted Grafana**: Self-host a Grafana instance to create and customize dashboards, including those provided with CoreWeave Grafana, without limitation. This option requires more setup and configuration than the managed option, but grants the freedom to create fully customized dashboards that can be tuned to display unique workloads. See [Self-hosted Grafana](https://docs.coreweave.com/observability/self-hosted-grafana.md) for more information.

* **Resource Usage**: Monitor compute, storage, and networking usage in Grafana to manage costs and optimize performance. See [Cost and Usage Monitoring](https://docs.coreweave.com/observability/usage-monitoring.md) for more information.

* **CoreWeave Alerts**: Real-time notifications about your clusters, deployments, and operations, delivered through Slack or a webhook. See [CoreWeave Alerts](https://docs.coreweave.com/platform/coreweave-alerts.md) for more information.
