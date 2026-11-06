# Introduction to Mission Control MCP

Source: https://docs.coreweave.com/observability/mission-control-mcp

# Introduction to Mission Control MCP

> Connect AI agents to CoreWeave observability data and supported write actions through MCP.

CoreWeave Mission Control MCP is a hosted [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP)
server for CoreWeave infrastructure. It connects MCP-compatible clients, such as Claude Code,
Cursor, and the ChatGPT desktop app, to tools for observing, triaging, optimizing, and performing
supported changes in CoreWeave environments.

With a CoreWeave API token, you can ask natural-language questions about your infrastructure and
let an agent gather current evidence from metrics, logs, dashboards, documentation,
cluster state, Node details, and object storage context. The agent works inside the same
visibility boundary as your token, so it can access only resources available to your token.

CoreWeave hosts the server, so you don't need to deploy or operate it. Point your client at the
endpoint and authenticate with a token. Most tools are read-only. CoreWeave can enable
limited write tools for an organization, and those tools can change supported resources.

## Mission Control MCP capabilities

Mission Control MCP combines tool families in one connection so an agent can perform a multi-step
investigation. It coordinates access to dashboards, command-line interfaces (CLIs), and
documentation. It doesn't replace them.

Mission Control MCP provides the following capabilities:

* **Observability**: query metrics, search logs, inspect dashboards and the queries behind their
  panels, and discover datasources, backed by Grafana-compatible systems.
* **CoreWeave documentation**: search and read CoreWeave public documentation so an agent answers
  product and API questions from documentation rather than model memory.
* **CoreWeave resources**: inspect clusters, Nodes, CoreWeave SUNK resources, and CoreWeave AI
  Object Storage buckets, then connect that state to observability data.
* **Write actions**: apply a Kubernetes manifest to a CoreWeave Kubernetes Service (CKS) cluster
  and update supported CoreWeave Inference deployment fields, where enabled for your organization.

For documented tool inputs and outputs, see the
[Mission Control MCP tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md).

## How teams use Mission Control MCP

Mission Control MCP supports the following roles:

* **AI researchers and ML engineers** can stay in their editor while they ask for GPU health
  signals, Node status, workload logs, or relevant dashboards, then follow up with further
  questions.
* **Platform and infrastructure teams** can assemble an evidence chain that shows what is affected,
  which metrics changed, which errors appear in the logs, and which dashboards are relevant.
* **Application teams and operators** can answer operational questions that cross product surfaces,
  such as combining workload logs, metrics, and object storage state to investigate performance
  issues in training jobs.
* **Domain experts** can frame an investigation while the agent coordinates tool calls and turns
  operational telemetry into tables, prototypes, and next steps.

## Set up Mission Control MCP

To connect a client and start calling the tools, see
[Configure Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp/configure.md). Setup requires a
CoreWeave API token and an MCP-compatible client, such as Claude Code, Cursor, or the ChatGPT
desktop app.

## Related resources

Use the following resources to learn more about Mission Control:

> [card] [Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent.md)
>
> Use CoreWeave's conversational interface in the Cloud Console.

> [card] [Configure Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp/configure.md)
>
> Connect Claude Code, Cursor, the ChatGPT desktop app, or another MCP client to the hosted
> server.

> [card] [Tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md)
>
> Mission Control MCP tools, grouped by family, with inputs and outputs.

> [card] [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md)
>
> Managed Grafana dashboards, metrics, and logs that Mission Control MCP tools observe.

> [card] [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md)
>
> S3-compatible object storage that the object storage tools inspect.

> [card] [CoreWeave Skills](https://docs.coreweave.com/platform/coreweave-skills.md)
>
> Agent Skills that let your coding agent carry out CoreWeave tasks.
