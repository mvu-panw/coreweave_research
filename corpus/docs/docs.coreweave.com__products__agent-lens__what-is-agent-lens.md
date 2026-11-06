# What is Agent Lens?

Source: https://docs.coreweave.com/products/agent-lens/what-is-agent-lens

# What is Agent Lens?

> Learn about CoreWeave Agent Lens and how it helps you trace, monitor, and improve LLM agents

CoreWeave Agent Lens is an observability platform that lets you observe and track your agent's behavior and metrics. It captures conversations, tool calls, and performance metrics, and surfaces the specific behaviors that you're interested in tracking.

Agent Lens is in public preview in Forge.

## Core capabilities

Agent Lens provides the following core functionality:

* **[Visibility](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md)** into agent sessions and multi-turn conversations.
* **[Trace sub-agents](https://docs.coreweave.com/products/agent-lens/tracing/sub-agents.md)** to gain visibility into work that your agents delegate to sub-agents.
* **[Aggregated insights](https://docs.coreweave.com/products/agent-lens/insights.md)** into your agent's behaviors, errors, and trends.
* **[Custom behavior tracking](https://docs.coreweave.com/products/agent-lens/tags/create-tag.md)** using tags that describe the agent or user behavior you want to analyze.
* **[Dashboard metrics](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md)** that display usage, error rates, and token cost.
* **[Feedback collection](https://docs.coreweave.com/products/agent-lens/conversations/annotate-turns.md)** to capture human judgments and annotations.

## How Agent Lens works

Agent Lens is built on [OpenTelemetry (OTel)](https://opentelemetry.io/docs/concepts/) and the [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md). Agent Lens accepts any OTel span and stores its attributes so you can query them. Spans that follow the GenAI agent conventions, such as `invoke_agent` and `execute_tool`, render as conversations, turns, and tool calls in Agent Lens.

## Integration options

You can integrate Agent Lens using the following guides, depending on your needs:

* If your agent is already instrumented with OTel, you can send its existing spans to Agent Lens without re-instrumenting your code.  See how to [send your existing spans to Agent Lens without any SDK integration](https://docs.coreweave.com/products/agent-lens/get-started/opentelemetry.md).
* If you want to trace an existing harness, such as Codex or Claude Code, [install its plugin](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md#agent-harnesses). The plugin sends your harness's spans to your project, where they appear in Agent Lens.
* If your agent calls a model with the OpenAI, Anthropic, or Google Gen AI SDK, see the [LLM provider SDK integrations](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md#llm-provider-sdks).
* If you're building an agent with a popular agent SDK, see the [supported agent SDK integrations](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md#agent-sdks).
* If you're building a custom agent and need help instrumenting it, see the [custom agents quickstart](https://docs.coreweave.com/products/agent-lens/get-started/custom-agents.md).

## Agent Lens and Weights & Biases Weave

Agent Lens is a new agent observability product from the team that builds [Weights & Biases Weave](https://docs.coreweave.com/products/wandb/weave.md). Both products are part of CoreWeave Forge and can be used together. They share the same trace data, so any agent traces you send to one appear in the other, and there is no data to copy or migrate.

Agent Lens is the recommended experience for tracing, monitoring, and analyzing agents. It adds capabilities that Weave doesn't have, such as [insights](https://docs.coreweave.com/products/agent-lens/insights.md) into agent failures and user intents, and a simplified view of conversations, turns, and spans. If you already use Weave to trace agents, open the same project in Agent Lens to see your existing conversations there.

Weave continues to cover workflows that Agent Lens doesn't support yet, such as:

* Evaluations
* Function-specific traces using Ops and Calls
* Guardrails

Many of these workflows are coming to Agent Lens. If you need them now, use Weave alongside Agent Lens to cover these gaps.

The two products use different SDKs and applications under Forge:

| | Agent Lens | Weights & Biases Weave |
| - | - | - |
| SDK | [CoreWeave Forge SDK](https://docs.coreweave.com/products/agent-lens/get-started/custom-agents.md) | [Weights & Biases Weave SDK](https://docs.coreweave.com/products/wandb/weave/guides/integrations.md) |
| UI | [Agent Lens application](https://forge.coreweave.com/agent-lens) | [Weights & Biases application](https://forge.coreweave.com/wandb/home) |

Use the App Launcher in the upper-left corner of the CoreWeave Forge console to select **Agent Lens** or **Weights & Biases**.

Agent Lens and Weave share the same backend, so some configuration names keep the Weights & Biases naming:

* `WANDB_API_KEY`: the environment variable the Forge SDK reads for your CoreWeave Forge API key.
* `trace.wandb.ai`: the endpoint that receives traces.
* `wandb.entity` and `wandb.project`: the OpenTelemetry resource attributes that route spans to your project.

The Claude Code, Codex, Google Antigravity, and OpenClaw harness integrations are Forge plugins: `@coreweave/forge-agent-lens-for-claude-code`, `@coreweave/forge-agent-lens-for-codex`, `forge-agent-lens-for-google-antigravity`, and `@coreweave/forge-agent-lens-for-openclaw`.
