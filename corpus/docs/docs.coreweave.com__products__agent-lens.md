# Agent Lens

Source: https://docs.coreweave.com/products/agent-lens

# Agent Lens

> Overview of Agent Lens on CoreWeave

CoreWeave Agent Lens is an agent observability platform that helps you gain insights into your agent's or harness's performance and behaviors. The platform lets you instrument and trace your agent's and harness's conversations, performance metrics, tool calls, reasoning, and errors. This can help you:

* Surface trends about what customers ask your agents
* Debug tool calls regularly failed
* Evaluate the quality of your agent's output
* Track costs

## Get started

> [card] [Integrate Agent Lens](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md)
>
> Pick a built-in integration for your agent SDK or harness and start tracing sessions, turns, LLM calls, and tool calls in the Agents Lens UI.

> [card] [Send OpenTelemetry spans to Agent Lens](https://docs.coreweave.com/products/agent-lens/get-started/opentelemetry.md)
>
> Quickly configure your OTel-instrumented agent to send traces to Agent Lens's OTLP endpoint. No Agent Lens SDK installation required.

> [card] [View agent metrics in the Agent Lens UI](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md)
>
> Review your agent's conversations, metrics, and trends in the Agent Lens UI.

## Automatically instrument your agent

Start by installing the Agent Lens instrumentation skill using `npx`:

```bash theme={"system"}
npx skills add wandb/skills
```

When the installer asks which skills to install, select `agentlens-tracing-instrument`. You don't need the repository's other skills to instrument your agent.

After installing the skill, open your coding agent of choice and run the skill to instrument your code:

```text theme={"system"}
/agentlens-tracing-instrument
```

After the agent has instrumented the code, review it, and then set your [Forge API key](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md#create-a-new-api-key) as the following environment variable:

```bash theme={"system"}
export WANDB_API_KEY=[YOUR-API-KEY]
```

After you instrument your agent and run it, it sends tracing data to Agent Lens and you can [view its activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md) in the UI.
