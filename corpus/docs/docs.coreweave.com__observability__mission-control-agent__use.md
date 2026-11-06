# Use Mission Control Agent

Source: https://docs.coreweave.com/observability/mission-control-agent/use

# Use Mission Control Agent

> Ask questions, verify evidence, and request supported resource changes in the Cloud Console.

Use CoreWeave Mission Control Agent to investigate and interact with your CoreWeave environment from
the Cloud Console. The agent uses the page and resources in your conversation as context, then
returns an answer with supporting evidence. In organizations where CoreWeave has enabled write
tools, you can also request supported resource changes.

## Prerequisites

You need the following:

* Access to a CoreWeave organization where Mission Control Agent is available.
* Cloud Console permissions for the agent activity that you want to perform, including permission to
  view or change the resources involved.

## Open Mission Control Agent

In the top navigation of the Cloud Console, select **Ask Mission Control**. The agent opens in a
panel next to the current page.

You can also start a conversation from the **Ask Mission Control** message box on the Cloud
Console home page. Sending a message from the home page starts a new conversation and opens
Mission Control as a full page.

If the panel shows **Mission Control is off**, your organization administrator has turned off
Mission Control Agent. For more information, see
[Turn Mission Control Agent on or off](https://docs.coreweave.com/observability/mission-control-agent/manage-settings.md#turn-mission-control-agent-on-or-off).

Use the panel controls as needed:

* To give the conversation more room, select **Expand panel**.
* To return to the side panel, select **Collapse to dock**.
* To clear the current conversation, select **New chat**.

The conversation remains open as you navigate between Cloud Console pages.

> [!WARNING]
>
> Mission Control Agent supports one active conversation at a time. Selecting **New chat**,
> sending a message from the home page message box, or reloading the Cloud Console clears the
> current conversation. The Cloud Console doesn't provide a way to save or restore a cleared
> conversation.

## Ask a question

In the message box, enter an operational question. When possible, provide a specific resource and
symptom. For example, ask one of the following questions:

* "Why is my job pending?"
* "Which Nodes in this cluster need attention?"
* "Which jobs have low GPU utilization?"
* "How much data is stored in this bucket?"

To add resource context, type `@` in the message box and select an available resource. The agent
can use the referenced resource and the current Cloud Console page to scope its investigation.

Review the evidence included with the response before you act. Evidence might include charts,
tables, log excerpts, resource details, or links to relevant CoreWeave documentation.

If the answer is incomplete or the evidence doesn't support it, refine the question with a
specific resource, symptom, and time range. Don't rely on an unverified response for an operational
decision.

## Request a supported change

> [!NOTE]
>
> Write tools are available only to organizations where CoreWeave has enabled them. They aren't
> controlled from **Privacy and data**.

Mission Control Agent can perform a limited set of changes with your permissions. Supported
changes include applying a Kubernetes manifest to a named CoreWeave Kubernetes Service (CKS)
cluster and updating selected fields on a CoreWeave Inference deployment.

> [!WARNING]
>
> Mission Control Agent doesn't ask for confirmation before it runs a write tool, and it can't
> automatically undo a completed change. The agent can use any write tool that your permissions
> allow. Request only the specific fields or manifest that you intend to apply.

Request a change explicitly only when you intend Mission Control Agent to perform it. A diagnostic
question isn't a request to change a resource.

For example, you might ask: "On Inference deployment `[DEPLOYMENT-ID]`, set `autoscaling.max` to
`4`."

To request a supported change, follow these steps:

1. Name the resource and request the exact change. For a manifest, provide the complete manifest
   that you intend to apply.
2. In the agent's response, confirm which resource it changed and which values it applied.
3. Open the affected resource in the Cloud Console and confirm that its state matches your request.

## Related resources

Use the following resources to learn more about Mission Control:

* [Introduction to Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent.md): Understand the
  agent's trust and capability boundaries.
* [Manage Mission Control Agent settings](https://docs.coreweave.com/observability/mission-control-agent/manage-settings.md):
  Control organization access and data-sharing preferences.
* [Introduction to Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md): Connect an MCP client
  when you want CoreWeave tools outside the Cloud Console.
* [Mission Control MCP tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md): Review
  available tool inputs and outputs.
