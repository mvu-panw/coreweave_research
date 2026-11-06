# Introduction to Mission Control Agent

Source: https://docs.coreweave.com/observability/mission-control-agent

# Introduction to Mission Control Agent

> Understand how Mission Control Agent investigates your environment and performs supported changes.

> [!NOTE]
>
> CoreWeave Mission Control Agent is in public preview. Availability, behavior, and tool coverage
> might change during the preview. Responses are AI-generated and can be incomplete or inaccurate,
> so verify them before you act.

Mission Control Agent is a conversational interface in the CoreWeave Cloud Console. Ask a question
in plain language, and the agent gathers evidence from your metrics, logs, dashboards, resource
state, and CoreWeave documentation. In organizations where CoreWeave has enabled write tools, the
agent can also perform a limited set of supported resource changes with your permissions.

The agent returns an answer with supporting evidence, such as charts, tables, log excerpts, and
resource details. This evidence helps you verify the answer and continue an investigation without
manually correlating several observability views.

## When to use Mission Control Agent

Use Mission Control Agent when you are working in the Cloud Console and want to investigate an
operational question or request a supported write action without configuring a separate client. For
example, you can ask about the following areas:

* Cluster, Node, and GPU health.
* Workload scheduling and utilization.
* CoreWeave SUNK clusters and Slurm jobs.
* CoreWeave AI Object Storage buckets.
* Usage and CoreWeave product documentation.
* Supported resource changes, when write tools are enabled for your organization. For details, see
  [Request a supported change](https://docs.coreweave.com/observability/mission-control-agent/use.md#request-a-supported-change).

## How Mission Control Agent works

Mission Control Agent runs as the signed-in user. Every request uses your identity and permissions,
so the agent can access only the resources available to you in your organization. It doesn't use a
separate service account or grant itself additional permissions.

The agent uses Mission Control tools to connect questions to CoreWeave observability data, resource
state, and documentation. The Cloud Console also provides the current page and any resources that
you reference as context for the conversation.

## Capabilities and limits

Mission Control Agent can gather evidence and explain what it finds. In organizations where
CoreWeave has enabled write tools, you can also request supported resource changes, such as applying
a Kubernetes manifest or updating selected Inference deployment fields. Write tools use the
signed-in user's permissions and aren't self-serve. For instructions and safety considerations, see
[Request a supported change](https://docs.coreweave.com/observability/mission-control-agent/use.md#request-a-supported-change).

The agent can access only data exposed through its supported tools and any context that you provide
in the conversation.

## Mission Control Agent and Mission Control MCP

Mission Control Agent and Mission Control MCP provide access to CoreWeave operational capabilities
through different interfaces. Choose the interface that matches your workflow:

* **Mission Control Agent** runs in the Cloud Console and uses your signed-in identity. Use it when
  you want to investigate while working in the Cloud Console without additional setup.
* **Mission Control MCP** is a hosted Model Context Protocol (MCP) server that you connect to an
  MCP-compatible client with a CoreWeave API token. Use it to bring CoreWeave data into tools such
  as Claude Code, Cursor, or the ChatGPT desktop app.

For an overview, see [Introduction to Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md). For
MCP setup instructions, see
[Configure Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp/configure.md).

## Next steps

Use the following resources to continue with Mission Control:

* [Use Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent/use.md): Open the agent, ask a
  question, provide resource context, and verify the answer.
* [Manage Mission Control Agent settings](https://docs.coreweave.com/observability/mission-control-agent/manage-settings.md):
  Control organization access and available data-sharing preferences.
* [Introduction to Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md): Connect an MCP client
  when you want CoreWeave tools outside the Cloud Console.
* [Mission Control MCP tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md): Review
  the operational tools and their inputs.
