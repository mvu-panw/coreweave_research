# OpenClaw plugin

Source: https://docs.coreweave.com/products/agent-lens/integrations/openclaw

# OpenClaw plugin

> Track OpenClaw agent sessions in Agent Lens for observability and debugging.

The [CoreWeave Forge plugin for OpenClaw](https://github.com/coreweave/forge-agent-lens-for-openclaw) automatically traces every agent session running through the OpenClaw gateway and sends the structured data to Agent Lens. The plugin logs every turn, model call, and tool execution without requiring any application code changes. Use these traces to debug sessions, audit tool usage, and monitor cost and latency across runs.

This guide is for OpenClaw gateway operators who want to enable Agent Lens tracing for the agents running behind the gateway. It walks you through how to install the plugin, configure it, view the resulting traces, and troubleshoot common issues.

> [!WARNING]
>
> This plugin sends OpenClaw session data to Agent Lens. That data can include user prompts, model responses, tool inputs and outputs, tool results, and conversation history.
>
> The plugin doesn't implement personally identifiable information (PII) scrubbing or sensitive-data redaction. If you need to suppress content capture, set `captureContent: false` in the plugin config. If you can't send this data to Agent Lens under your security or compliance requirements, don't install this plugin.

## Prerequisites

* [Node.js](https://nodejs.org/) v24.16 or later, or v26.1 or later. Node.js v25 isn't supported.
* [OpenClaw](https://openclaw.ai) `2026.9.8` or later.
* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys).
* An Agent Lens project (`[YOUR-TEAM]/[YOUR-PROJECT]`) to receive traces.

## Install the plugin

Complete the following steps to install the plugin, register it with the OpenClaw gateway, and confirm that traces reach your Agent Lens project.

**1. Install the package**

> [!NOTE]
>
> This plugin is separate from the `weave-openclaw` plugin documented in the [Weave guide](https://docs.coreweave.com/products/wandb/weave/guides/integrations/agents/openclaw-harness.md). Its plugin ID is `forge`, and its config entry and status command use that name. If you installed `weave-openclaw`, disable and uninstall it before you install this plugin, so the two don't send duplicate traces. Move your settings from `plugins.entries.weave` to `plugins.entries.forge` and replace `weave` with `forge` in `plugins.allow`. The configuration fields and credentials are unchanged.

```bash lines theme={"system"}
openclaw plugins install clawhub:@coreweave/forge-agent-lens-for-openclaw
```

The OpenClaw gateway loads the plugin through its config. You don't import it from application code.

**2. Set your API key**

Replace `[YOUR-API-KEY]` with your API key, and then export it:

```bash lines theme={"system"}
export WANDB_API_KEY="[YOUR-API-KEY]"
```

OpenClaw also loads `WANDB_API_KEY` from `~/.openclaw/.env`. See the [configuration reference](#configuration-reference) for other ways to supply the key.

**3. Add the plugin to your gateway config**

The default config location is `~/.openclaw/openclaw.json` (JSON5, which allows comments and trailing commas). Run `openclaw onboard` to scaffold one if you don't have it yet.
Update `[YOUR-TEAM]` and `[YOUR-PROJECT]` for your project.

```json lines theme={"system"}
{
  plugins: {
    allow: ["forge"],
    entries: {
      forge: {
        enabled: true,
        config: { entity: "YOUR-TEAM", project: "YOUR-PROJECT" },
        hooks: { allowConversationAccess: true },
      },
    },
  },
}
```

Set `hooks.allowConversationAccess` to `true` so OpenClaw runs the plugin's content-bearing hooks, `llm_input` and `agent_end`. Without it, model-call spans have no prompt text or system instructions. Trace structure, tool calls, and token and cost totals still come through diagnostic events.

OpenClaw's top-level `diagnostics.enabled` setting is `true` by default. Setting it to `false` turns off the diagnostic events the plugin relies on, so no traces are sent.

**4. Restart the gateway and verify**

Restart the OpenClaw gateway:

```bash lines theme={"system"}
openclaw gateway restart
```

Then run `/forge status` in any OpenClaw chat surface. When the plugin reports `running`, it's active. Traces appear in your Agent Lens project at `https://forge.coreweave.com/agent-lens/[YOUR-TEAM]/[YOUR-PROJECT]` within a few seconds of your first agent run. The `dashboard` line in the status output links to the same project in Weave, which shares the trace data.

## View OpenClaw traces in Agent Lens

Once the plugin is active, each agent session produces a trace you can inspect in the Agent Lens UI. After running at least one agent session, open your project in the Agent Lens UI:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, and then select your project in the project selector at the top of the side menu.
2. In the side menu, select **Conversations**.
3. Select the **Conversations** tab to view all agent conversations saved for your project.
4. Select a conversation to inspect the full conversation tree.

For more information about the Conversations tab, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).

The plugin emits spans per the [OpenTelemetry (OTel) GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md):

| Span | Emitted on | Key attributes |
| - | - | - |
| `invoke_agent <agent>` | Per agent run | `gen_ai.agent.name`, `gen_ai.conversation.id`, cumulative cost, token usage |
| `chat <model>` | Per model call | `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` |
| `execute_tool <tool>` | Per tool execution | `gen_ai.tool.name`, `gen_ai.tool.call.id` |

## Configuration reference

This section is the full configuration reference for the `forge` plugin entry in `openclaw.json`.

Only `entity` and `project` are required. The plugin looks for an API key in this order:

1. The `apiKey` field in the plugin config, as a `SecretRef` object or a literal string. For security purposes, we do not recommend using literal strings.
2. The `WANDB_API_KEY` environment variable, which OpenClaw also loads from `~/.openclaw/.env`.
3. A `~/.netrc` entry for `api.wandb.ai`, populated by `wandb login`.

An `env` `SecretRef` works without extra setup. A `file` or `exec` `SecretRef` requires a matching `secrets.providers` entry in your gateway config. See [OpenClaw secrets management](https://docs.openclaw.ai/gateway/secrets).

```json lines theme={"system"}
{
  plugins: {
    entries: {
      forge: {
        enabled: true,
        config: {
          entity: "YOUR-TEAM",
          project: "YOUR-PROJECT",
          // Reads WANDB_API_KEY from env if apiKey is omitted.
          // SecretRef supports source: "env", "file", or "exec". The "env"
          // source works with provider: "default". The "file" and "exec"
          // sources need a matching secrets.providers entry.
          // Plain string is supported but discouraged.
          apiKey: { source: "env", provider: "default", id: "WANDB_API_KEY" },
          serviceName: "openclaw-agent",
          // Optional, improves Conversations tab grouping.
          agentName: "my-agent",
          agentVersion: "v1.0",
          agentDescription: "What my agent does.",
          // ON by default. Set to false for a hard off (compliance or
          // retention policy). The plugin does not redact captured
          // strings; scrub upstream if needed.
          captureContent: true,
          // How often, in milliseconds, the plugin sends traces. Minimum 1000.
          flushIntervalMs: 1000,
        },
        hooks: { allowConversationAccess: true },
      },
    },
  },
}
```

`captureContent` is `true` by default. When `captureContent` is `true`, the plugin also emits input and output messages, tool arguments, and tool results following the `gen_ai.input.messages` and `gen_ai.output.messages` payload shape. The plugin stamps subagents, compaction events, loop detection, retry attempts, and context sizing as additional attributes and span events.

Set `captureContent` to `false` to turn off capture for compliance or retention policies.

## Troubleshooting

If traces aren't reaching Agent Lens or content fields are empty, use the following sections to diagnose the most common causes.

The gateway log is the terminal output from the process running `openclaw`, or your process manager's log stream if you daemonized it.

### Plugin loaded but no spans show up

1. Run `/forge status`. If lifecycle is `disabled`, `config-error`, or `not-started`, the plugin didn't activate. Check the gateway log for `forge: entity is required`, `forge: project is required`, or `forge: init failed`.
2. Check you haven't set `diagnostics.enabled: false` in the gateway config. This field should be `true`.
3. Confirm the entity and project match the Agent Lens project you're inspecting. `/forge status` should print `project=[YOUR-TEAM]/[YOUR-PROJECT]`.
4. Confirm the auth source. `/forge status` should print `auth=...`. If it says `WANDB_API_KEY env` but you set the key in a different environment variable, the plugin is reading the wrong key.

### Spans land but input text is empty

Look in the gateway log for:

```text theme={"system"}
[plugins] typed hook "llm_input"  blocked because non-bundled plugins must set
                                  plugins.entries.forge.hooks.allowConversationAccess=true
[plugins] typed hook "agent_end"  blocked ...
```

OpenClaw gates content-bearing hooks behind an operator opt-in. Set `plugins.entries.forge.hooks.allowConversationAccess: true` in your config and restart the gateway. Span structure and cost and usage data come through diagnostic events, not hooks, so those keep working even when `allowConversationAccess` is `false`.

### Errors sending spans to Agent Lens

If the plugin is active and generating spans but they don't appear in Agent Lens, check the gateway log for an export error and match it against the following table.

| Symptom | Most likely cause | Fix |
| - | - | - |
| `401` or `403` | Invalid or scope-limited API key | Verify the key is current and has access to the entity and project. `wandb login` refreshes `~/.netrc`. |
| Connection refused or DNS error | DNS, proxy, or firewall | Confirm the gateway host can reach Forge on port `443`. |

## Manage the plugin

Use the following commands to update, disable, enable, or remove the plugin:

```bash lines theme={"system"}
openclaw plugins update forge
openclaw plugins disable forge
openclaw plugins enable forge
openclaw plugins uninstall forge
```
