# Google Antigravity plugin

Source: https://docs.coreweave.com/products/agent-lens/integrations/google-antigravity

# Google Antigravity plugin

> Track Google Antigravity agent turns in Agent Lens for observability and debugging.

The [CoreWeave Forge plugin for Google Antigravity](https://github.com/coreweave/forge-agent-lens-for-google-antigravity) traces agent turns, model calls, tool calls, and subagents. When a turn finishes, the plugin's [Stop hook](https://antigravity.google/docs/hooks) reads the conversation transcript and sends the turn to Agent Lens as one trace. Turns from the same Antigravity conversation share a conversation ID, so Agent Lens shows them as one conversation.

This guide walks you through how to install the plugin, configure it, view the resulting traces, and troubleshoot common issues.

> [!WARNING]
>
> This plugin sends Antigravity session data to Agent Lens. That data can include your prompts, the model's responses and reasoning, and tool arguments and results, including anything a tool prints.
>
> PII scrubbing and sensitive-data redaction aren't implemented. The plugin doesn't remove secrets or personal data from captured content. To omit prompts, responses, reasoning, and tool arguments and results, set `FORGE_ANTIGRAVITY_INCLUDE_CONTENT=false`. Spans still include names, timing, and workspace paths. See [Content capture](#content-capture). If you can't send this data to Agent Lens under your security or compliance requirements, don't install this plugin.

## Prerequisites

Before you install the plugin, you need the following:

* [Antigravity CLI](https://github.com/google-antigravity/antigravity-cli) (`agy`) `1.1.10` or later
* [uv](https://docs.astral.sh/uv/getting-started/installation/), whose `uvx` command runs the hook
* Python 3.10 or later
* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys)
* An Agent Lens project (`[YOUR-TEAM]/[YOUR-PROJECT]`) to receive traces

## Install the plugin

Complete the following steps to install the plugin and send your first trace to Agent Lens.

**1. Set your project and API key**

Replace `[YOUR-TEAM]/[YOUR-PROJECT]` with your Agent Lens project and `[YOUR-API-KEY]` with your API key, and then export them:

```bash lines theme={"system"}
export FORGE_TRACE_PROJECT="[YOUR-TEAM]/[YOUR-PROJECT]"
export WANDB_API_KEY="[YOUR-API-KEY]"
```

The hook runs with the environment that `agy` was started in. Set `FORGE_TRACE_PROJECT` and the API key in your shell profile, or wherever you start `agy`, and make sure `uvx` is on that `PATH`. Instead of `WANDB_API_KEY`, the hook can read the key from the Weights & Biases host's entry in `~/.netrc`.

**2. Run the installer**

```bash lines theme={"system"}
uvx forge-agent-lens-for-google-antigravity@latest install
```

The installer registers the plugin with `agy plugin install`, checks the settings the hook needs, and prints where traces will appear:

```text theme={"system"}
Installed the Antigravity plugin (forge-agent-lens-for-google-antigravity X.Y.Z).
✓ Hook command         uvx forge-agent-lens-for-google-antigravity@X.Y.Z
✓ FORGE_TRACE_PROJECT  my-team/antigravity-traces
✓ W&B API key          WANDB_API_KEY
View traces: https://forge.coreweave.com/agent-lens/my-team/antigravity-traces
```

If the installer shows `✗ Hook command`, see [Troubleshooting](#troubleshooting).

**3. Start a new session**

Start a new `agy` session. Each finished turn appears in Agent Lens.

## View Antigravity traces in Agent Lens

The installer prints a link to your project's traces. You can also open your project in the Agent Lens UI:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, and then select your project in the project selector at the top of the side menu.
2. In the side menu, select **Conversations**.
3. Select the **Conversations** tab to view all agent conversations saved for your project.
4. Select a conversation to inspect the full conversation tree.

For more information about the Conversations tab, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).

The plugin names each conversation after the first workspace folder of the session. If the session has no workspace folder, the conversation is named `Antigravity`.

## What gets traced

Each turn becomes one trace:

```text theme={"system"}
invoke_agent Antigravity     the turn, from your request until the agent stops
├─ chat <model>              each model response
├─ execute_tool <tool>       each tool call and its result
└─ invoke_agent <subagent>   each subagent started by invoke_subagent
```

Spans use the [OpenTelemetry (OTel) GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md) (`gen_ai.*` attributes), and are timed from the step timestamps in the Antigravity transcript.

### Limitations

The plugin has the following limitations:

* Antigravity's transcript doesn't record token usage, model request settings, or response IDs, so traces have no token counts or costs.
* A subagent's `invoke_agent` span has its prompt and result but no child spans, because the transcript doesn't record the subagent's own model and tool calls.

## Configuration reference

Configure the plugin with environment variables that you set in the environment where you start `agy`.

| Variable | Default | Description |
| - | - | - |
| `FORGE_TRACE_PROJECT` | Required | Agent Lens project, as `[YOUR-TEAM]/[YOUR-PROJECT]`. |
| `WANDB_API_KEY` | `~/.netrc` entry | Forge API key. |
| `FORGE_ANTIGRAVITY_INCLUDE_CONTENT` | `true` | Set to `false` to omit prompts, responses, reasoning, and tool arguments and results. |

### Content capture

With `FORGE_ANTIGRAVITY_INCLUDE_CONTENT=false`, spans still include the following:

* Model, tool, and subagent names, and subagent roles
* Timing
* Workspace paths
* The Stop hook's execution number and termination reason

The Forge SDK also adds your operating system and Python versions to every span.

## Troubleshooting

If traces aren't reaching Agent Lens, first find the plugin's messages with the `grep` command. Antigravity doesn't show hook output in its terminal UI or in `agy -p` output. It writes the hook's messages, including links to where to view traces and any export errors, to its CLI logs:

```bash lines theme={"system"}
grep -h "forge-agent-lens-for-google-antigravity:" ~/.gemini/antigravity-cli/log/cli-*.log | tail
```

Then match what you find against the following table.

| Symptom | What to check |
| - | - |
| `install` shows `✗ Hook command` | Install [uv](https://docs.astral.sh/uv/getting-started/installation/) so that `uvx` is on `PATH`. |
| The log says `FORGE_TRACE_PROJECT is not set` | Set it in the environment where you start `agy`, and then start a new session. |
| The log says `trace export failed` | The rest of the line names the error. Check that your API key is valid and that you have access to the project. |
| No log lines from the plugin | Run `agy plugin list` to confirm the plugin is installed, and confirm that `uvx` is on the `PATH` that `agy` starts with. |

## Manage the plugin

To upgrade, rerun the install command. It replaces the installed plugin. To pin a version, or switch to one, install from that version:

```bash lines theme={"system"}
uvx forge-agent-lens-for-google-antigravity@[VERSION] install
```

Disable, re-enable, or remove the plugin with [`agy plugin`](https://antigravity.google/docs/plugins?tab=cli):

```bash lines theme={"system"}
agy plugin disable forge-agent-lens-for-google-antigravity
agy plugin enable forge-agent-lens-for-google-antigravity
agy plugin uninstall forge-agent-lens-for-google-antigravity
```

If you set up version `0.1.0` or `0.1.1` with `uv tool install`, upgrading leaves that executable unused. Remove it with:

```bash lines theme={"system"}
uv tool uninstall forge-agent-lens-for-google-antigravity
```
