# Claude Code plugin

Source: https://docs.coreweave.com/products/agent-lens/integrations/claude-code

# Claude Code plugin

> Track Claude Code sessions in Agent Lens for observability and debugging.

The [CoreWeave Forge plugin for Claude Code](https://github.com/coreweave/forge-agent-lens-for-claude-code) automatically traces every Claude Code session and sends the structured data to Agent Lens. The plugin logs every turn, tool call, and subagent with no code changes required. Use these traces to debug sessions, audit tool usage, and monitor cost and latency across runs.

This guide walks you through installing the plugin, viewing your Claude Code traces in Agent Lens, configuring the plugin, and managing its lifecycle.

> [!WARNING]
>
> This plugin sends Claude Code session data to Agent Lens. That data can include user prompts, Claude responses, tool inputs and outputs, file contents read by Claude Code tools, shell commands and output, and fetched URLs and page content.
>
> PII scrubbing and sensitive-data redaction aren't implemented. If you can't send this data to Agent Lens under your security or compliance requirements, don't install this plugin.

## Prerequisites

* [Node.js](https://nodejs.org/) v18.19 or later, or v20.6 or later (includes `npm`).
* [Claude Code](https://claude.ai/code) installed and authenticated.
* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
* An Agent Lens project (`[YOUR-TEAM]/[YOUR-PROJECT]`) to receive traces.

## Install the plugin

Install the CLI, run the installer to register the plugin with Claude Code, then start a Claude Code session to begin tracing.

**1. Install the CLI**

> [!NOTE]
>
> This plugin is separate from the `weave-claude-code` plugin documented in the [Weave guide](https://docs.coreweave.com/products/wandb/weave/guides/integrations/agents/claude-code-harness.md). Its CLI is `forge-agent-lens-for-claude-code`, and its skills use the `forge` name. If you installed `weave-claude-code` or the earlier `@coreweave/forge-claude-code` package, uninstall it before you install this plugin, so the two don't send duplicate traces:
>
> ```bash lines theme={"system"}
> # If you installed weave-claude-code:
> weave-claude-code uninstall
> npm uninstall -g weave-claude-code
>
> # If you installed @coreweave/forge-claude-code:
> forge-claude-code uninstall
> npm uninstall -g @coreweave/forge-claude-code
> ```
>
> Settings don't carry over from either package. Set your project and API key again when the installer prompts for them. If you set the plugin's environment variables, rename `WEAVE_PROJECT` to `FORGE_TRACE_PROJECT` and `WEAVE_AGENT_NAME` to `FORGE_CLAUDE_CODE_AGENT_NAME`.

```bash lines theme={"system"}
npm install -g @coreweave/forge-agent-lens-for-claude-code
```

**2. Run the installer**

```bash lines theme={"system"}
forge-agent-lens-for-claude-code install
```

The installer does the following:

* Creates `~/.forge-agent-lens-for-claude-code/settings.json`.
* Registers the plugin in Claude Code.
* Prompts for your Agent Lens project (`[YOUR-TEAM]/[YOUR-PROJECT]`) and Forge API key if they aren't already set.

To skip prompts in CI, bootstrap scripts, or other automated systems, set environment variables before running:

```bash lines theme={"system"}
FORGE_TRACE_PROJECT=[YOUR-TEAM]/[YOUR-PROJECT] \
WANDB_API_KEY=[YOUR-API-KEY] \
forge-agent-lens-for-claude-code install --non-interactive
```

In non-interactive mode, the installer still creates the config file and registers the plugin. It uses `FORGE_TRACE_PROJECT` and `WANDB_API_KEY` from the environment and warns if either is missing. It doesn't write these values to `settings.json`.

By default, the installer registers the plugin from GitHub. If your CI system or container can't reach GitHub, pass `--source=local` to register the plugin from the npm package you installed in the previous step:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code install --non-interactive --source=local
```

**3. Start Claude Code**

```bash lines theme={"system"}
claude
```

If Claude Code is already running, run `/reload-plugins` in the session instead.

The plugin traces sessions automatically from this point. It traces every Claude Code session on this machine, not only the sessions in one project.

## View Claude Code traces in Agent Lens

After running at least one Claude Code session, open your project in the Agent Lens UI:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, and then select your project in the project selector at the top of the side menu.
2. In the side menu, select **Conversations**.
3. Select the **Conversations** tab to view all agent conversations saved for your project.
4. Select a conversation to inspect the full conversation tree.

For more information about the Conversation tab, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).

Each user prompt produces one OTEL trace that follows the [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md). The trace shows a full turn hierarchy:

```text theme={"system"}
invoke_agent claude-code               (Root, one trace per user prompt.)
├─ chat <model>                        (Each LLM call within the turn.)
├─ execute_tool <tool_name>            (Each tool call such as Read, Bash, Grep.)
└─ invoke_agent <subagent_type>        (Subagent dispatched through the Agent tool.)
   ├─ chat <model>
   └─ execute_tool <tool_name>
```

The root `invoke_agent claude-code` span uses the top-level agent name, which defaults to `claude-code`. You can change it with the `agent_name` setting or the `FORGE_CLAUDE_CODE_AGENT_NAME` environment variable (see [Configure the plugin](#configure-the-plugin)). Subagents keep their own type names.

Multi-turn conversations are linked server-side by conversation ID, so you can follow a conversation across multiple traces. Each span includes token usage, model name, tool inputs and outputs, timing, and the textual content of prompts and responses. For more information about traced data, see [What Gets Traced](https://github.com/coreweave/forge-agent-lens-for-claude-code/blob/main/README.md#what-gets-traced) in GitHub.

## Configure the plugin

Use the `forge-agent-lens-for-claude-code config` commands to view or update plugin settings after installation:

```bash lines theme={"system"}
# Show all current settings.
forge-agent-lens-for-claude-code config show

# Show one setting, including any environment variable override.
forge-agent-lens-for-claude-code config get project

# Set your Agent Lens project.
forge-agent-lens-for-claude-code config set project [YOUR-TEAM]/[YOUR-PROJECT]

# Set your Forge API key.
forge-agent-lens-for-claude-code config set wandb_api_key [YOUR-API-KEY]

# (Optional) Customize the agent name shown in the Conversations tab.
forge-agent-lens-for-claude-code config set agent_name [YOUR-AGENT-NAME]
```

By default, conversations appear under the agent name `claude-code` in the Conversations tab. Set `agent_name` to use a different name, for example to distinguish teams or projects. The name can't be empty, and surrounding whitespace is trimmed.

The plugin's background daemon reads its settings when it starts. To apply a changed setting to a running daemon, restart it:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code restart
```

Environment variables take precedence over the settings file:

```bash lines theme={"system"}
export FORGE_TRACE_PROJECT=[YOUR-TEAM]/[YOUR-PROJECT]
export WANDB_API_KEY=[YOUR-API-KEY]
export FORGE_CLAUDE_CODE_AGENT_NAME=[YOUR-AGENT-NAME]
```

## Agent Lens skills

After installation, three Agent Lens-specific skills are available directly inside any Claude Code session.

| Skill | Command | Description |
| - | - | - |
| Install | `/forge:forge-install` | Walks through the installation and configuration flow interactively. Use this on a fresh machine or to diagnose a broken setup. |
| Status | `/forge:forge-status` | Checks the current plugin status and explains any issues. Equivalent to running `forge-agent-lens-for-claude-code status`, but Claude interprets the output and tells you what to fix. |
| Config | `/forge:forge-config` | Read or update plugin configuration without leaving Claude Code. |

You can use the `forge:forge-config` skill to set Agent Lens values from within Claude Code:

```text theme={"system"}
/forge:forge-config set project [YOUR-TEAM]/[YOUR-PROJECT]
/forge:forge-config set wandb_api_key [YOUR-API-KEY]
/forge:forge-config set agent_name [YOUR-AGENT-NAME]
```

## Check plugin status

You can use these CLI commands to check plugin status or troubleshoot issues:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code status
```

Each line shows `✓` (OK), `✗` (action needed), or `-` (not yet active but not an error).

If conversations aren't appearing in Agent Lens, run the following command to print the last 50 lines of the daemon log:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code logs
```

To print more lines, pass `--tail` with a line count:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code logs --tail 200
```

To tail the log in real time:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code logs --follow
```

The log file is also at `~/.forge-agent-lens-for-claude-code/logs/daemon.log`.

For more detailed daemon output while you diagnose an issue, turn on debug mode:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code config set debug true
```

To turn on debug mode for the current shell session only, set `FORGE_CLAUDE_CODE_DEBUG=1` instead.

## Uninstall

To remove the plugin from Claude Code and stop tracing, run:

```bash lines theme={"system"}
forge-agent-lens-for-claude-code uninstall
```

Pass `--keep-logs` to preserve the log directory.
