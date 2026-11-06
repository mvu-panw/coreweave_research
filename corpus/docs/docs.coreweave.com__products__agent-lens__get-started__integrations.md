# Choose an agent integration

Source: https://docs.coreweave.com/products/agent-lens/get-started/integrations

# Choose an agent integration

> Pick a built-in Agent Lens integration for your LLM provider SDK, agent SDK, or harness.

CoreWeave Agent Lens traces agents built with popular LLM provider SDKs, agent SDKs, and harnesses, without hand-instrumenting each turn. Conversations, turns, LLM calls, and tool calls render in the **Conversations** tab of your project.

Choose from one of the following supported integrations.

## LLM provider SDKs

LLM provider SDKs are the client libraries you use to call a model API directly. Install the CoreWeave Forge SDK and call `tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")`, and the Forge SDK patches the provider SDK to record each call. Agent Lens shows only calls that run inside a conversation, so make your calls inside a `Conversation`, as each integration page shows:

* [OpenAI](https://docs.coreweave.com/products/agent-lens/integrations/openai.md)
* [Anthropic](https://docs.coreweave.com/products/agent-lens/integrations/anthropic.md)
* [Google Gen AI](https://docs.coreweave.com/products/agent-lens/integrations/google-genai.md)

## Agent SDKs

Agent SDKs are libraries for building agents and multi-agent workflows in your own application code. These integrations use the Weights & Biases Weave SDK, because the Forge SDK doesn't support these frameworks yet. Add `weave.init("[YOUR-TEAM]/[YOUR-PROJECT]")` to your script, and Weave patches the agent SDK. The traces appear in Agent Lens, because Agent Lens and Weave share the same trace data.

Agent SDKs run one turn per call, so `weave.init()` alone doesn't group turns into a conversation. Pass the SDK's own session or group identifier on every turn. Each integration page shows which identifier to use:

* [OpenAI Agents SDK](https://docs.coreweave.com/products/agent-lens/integrations/openai-agents-sdk.md)
* [Google Agent Development Kit (ADK)](https://docs.coreweave.com/products/agent-lens/integrations/google-adk.md)
* [Claude Agent SDK](https://docs.coreweave.com/products/agent-lens/integrations/claude-agents-sdk.md)

## Agent harnesses

Agent harnesses are end-user agent runtimes, such as coding agents and developer tools. Install the plugin or extension for your harness, and then start a session in the harness to begin tracing.

The Claude Code, Codex, Google Antigravity, and OpenClaw integrations are Forge plugins. The Pi integration uses the Weave SDK, because the Forge SDK doesn't support Pi yet. Traces from all of them appear in Agent Lens:

* [Claude Code plugin](https://docs.coreweave.com/products/agent-lens/integrations/claude-code.md)
* [Codex plugin](https://docs.coreweave.com/products/agent-lens/integrations/codex.md)
* [Google Antigravity plugin](https://docs.coreweave.com/products/agent-lens/integrations/google-antigravity.md)
* [OpenClaw plugin](https://docs.coreweave.com/products/agent-lens/integrations/openclaw.md)
* [Pi extension](https://docs.coreweave.com/products/agent-lens/integrations/pi.md)

## Custom agents and OpenTelemetry

If your agent isn't built with one of the SDKs above, or it already emits OpenTelemetry spans, use the Forge SDK directly or send your spans to Agent Lens. Agent Lens accepts any OTel span and gives special handling to [GenAI semantic-convention attributes](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) so spans render in the **Conversations** tab:

* [Quickstart: Manually instrument an agent](https://docs.coreweave.com/products/agent-lens/get-started/custom-agents.md): a walkthrough of a small multi-turn agent.
* [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md): the full reference of agent helpers and concepts.
* [Send OpenTelemetry spans to Agent Lens](https://docs.coreweave.com/products/agent-lens/get-started/opentelemetry.md): point an existing OTel pipeline at the Agent Lens endpoint, with no SDK required.

## Next steps

Once your first conversation reaches Agent Lens, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md) to explore conversations, turns, and tool calls.
