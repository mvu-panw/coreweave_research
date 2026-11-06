# Codex plugin

Source: https://docs.coreweave.com/products/agent-lens/integrations/codex

# Codex plugin

> Trace Codex agentic sessions, LLM calls, and tool executions in Agent Lens.

The [CoreWeave Forge plugin for Codex](https://github.com/coreweave/forge-agent-lens-for-codex) automatically traces Codex turns and sends the structured data to Agent Lens. Every model call and tool execution is logged with no changes to your Codex workflow. Use these traces to debug sessions, audit tool usage, and monitor token usage and latency across runs.

The plugin reads Codex's own rollout session files (`~/.codex/sessions/**/rollout-*.jsonl`) to reconstruct spans. When a turn finishes, a Stop hook starts a detached collector, so Codex never waits on the network. Turns from the same Codex session share a conversation ID, so Agent Lens shows them as one conversation.

> [!WARNING]
>
> By default, this plugin captures span content: your prompts, the model's responses and reasoning, tool-call arguments, tool results, and the working directory. Tool results include shell commands, command output, and file contents. This data is sent to your Agent Lens instance.
>
> Personally identifiable information (PII) scrubbing and sensitive-data redaction aren't implemented. To send structure, token usage, model, and timing only (with no prompts, code, or output), set `FORGE_CODEX_INCLUDE_CONTENT=false`. See [Turn off content capture](#turn-off-content-capture). If you can't send this data to Agent Lens under your security or compliance requirements, don't install this plugin.

## Prerequisites

* macOS or Linux. Windows isn't supported.
* [Node.js](https://nodejs.org/) v20.6 or later.
* [OpenAI Codex CLI](https://github.com/openai/codex) with hooks and rollout logging enabled. `codex --ephemeral` isn't supported because it doesn't write a rollout file.
* A CoreWeave Forge account and [Forge API key](https://forge.coreweave.com/settings#apikeys).
* An Agent Lens project (`[YOUR-TEAM]/[YOUR-PROJECT]`) to receive traces.

## Install the plugin

**1. Install the package**

> [!NOTE]
>
> This plugin is separate from the `weave-codex` plugin documented in the [Weave guide](https://docs.coreweave.com/products/wandb/weave/guides/integrations/agents/codex-harness.md). Its package is `@coreweave/forge-agent-lens-for-codex`, and its command, environment variables, and settings directory use the `forge-agent-lens-for-codex` and `FORGE_` names. If you installed `weave-codex`, run `weave-codex uninstall` and `npm uninstall -g weave-codex` before you install this plugin, so the two don't send duplicate traces. Set `FORGE_TRACE_PROJECT` to the value you used for `WEAVE_PROJECT`. The plugin doesn't read the `weave-codex` settings.

```bash lines theme={"system"}
npm install --global @coreweave/forge-agent-lens-for-codex
```

**2. Set your project and API key**

Replace `[YOUR-TEAM]/[YOUR-PROJECT]` with your Agent Lens project and `[YOUR-API-KEY]` with your API key, and then export them:

```bash lines theme={"system"}
export FORGE_TRACE_PROJECT="[YOUR-TEAM]/[YOUR-PROJECT]"
export WANDB_API_KEY="[YOUR-API-KEY]"
```

You can also run `wandb login` instead of setting `WANDB_API_KEY`. For how the plugin resolves each setting, see [Configuration reference](#configuration-reference).

**3. Install the Stop hook**

```bash lines theme={"system"}
forge-agent-lens-for-codex install
```

This merges a Stop hook into `~/.codex/hooks.json`, backing up the original file once to `hooks.json.bak`. The command also skips your existing Codex sessions, so only turns you run after installation are sent to Agent Lens. To send that history deliberately, see [Collect past sessions](#collect-past-sessions).

**4. Approve the hook in Codex**

Codex doesn't run newly added hooks until you approve them:

1. Open a terminal and run:

   ```bash lines theme={"system"}
   codex
   ```

2. Inside the interactive Codex screen, not your shell, type:

   ```text theme={"system"}
   /hooks
   ```

3. Under **Stop** Events, select the Forge Agent Lens hook, and then enable or trust it.

For a one-off automation run, Codex also supports the `--dangerously-bypass-hook-trust` flag.

Run `forge-agent-lens-for-codex status` to confirm that the hook is installed and the plugin is `ready`.

Now you can run Codex normally, and each completed turn is sent to Agent Lens.

## View Codex traces in Agent Lens

After running at least one Codex session, open your project in the Agent Lens UI:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, and then select your project in the project selector at the top of the side menu.
2. In the side menu, select **Conversations**.
3. Select a conversation to inspect the full turn hierarchy.

For more on the Conversations tab, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).

The plugin emits one OTEL trace per Codex turn, following the [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md):

| Span | Emitted on | Key attributes |
| - | - | - |
| `invoke_agent codex` | Per turn (root span) | Agent name and version, `codex.session.id`, `codex.turn.id`, model, user prompt and final answer (when content capture is on), and `codex.cwd` (when content capture is on) |
| `chat <model>` | Per model call | Provider name, `gen_ai.usage.*` (input, output, cached, and reasoning tokens), finish reason, assistant output (when content capture is on) |
| `execute_tool <name>` | Per tool execution | `gen_ai.tool.name`, `gen_ai.tool.call.id`, arguments and result (when content capture is on), and MCP calls also carry `mcp.server.name` |

Span timestamps come from the rollout file, so durations reflect actual execution time. A turn is sent once. If an export fails, the plugin retries that turn the next time the Stop hook fires.

### Known limitations

* The `codex` (interactive TUI) and `codex exec` commands are supported. `codex mcp`, direct app-server or API sessions, and aborted turns that fire no Stop event aren't covered.
* A spawned subagent appears as a tool span only. Its separate rollout file isn't reconstructed as a nested trace, so its own model calls and tool executions aren't captured.
* Some `codex exec` environments don't run the Stop hook. See [Headless runs and explicit collection](https://github.com/coreweave/forge-agent-lens-for-codex#headless-runs-and-explicit-collection) in the plugin README.

## Configuration reference

This section lists the settings you can use to customize plugin behavior. State, settings, and the log file live in `~/.forge-agent-lens-for-codex/`, including `settings.json` and `logs/collector.log`. Set `FORGE_CODEX_HOME` only for isolated development or test environments.

| Setting | Environment variable | `settings.json` key | Default |
| - | - | - | - |
| Agent Lens project | `FORGE_TRACE_PROJECT` | `project` | None (required, `entity/project`) |
| Forge API key | `WANDB_API_KEY` | Not stored | Matching `~/.netrc` entry (through `wandb login`) |
| Provider name | `FORGE_CODEX_PROVIDER_NAME` | `provider_name` | `openai` |
| Include content | `FORGE_CODEX_INCLUDE_CONTENT` | `include_content` | `true` |
| Debug logging | `FORGE_CODEX_DEBUG` | `debug` | `false` (errors always log) |

Set `FORGE_CODEX_PROVIDER_NAME` if Codex sends requests through a proxy or bridge to a different model provider. The plugin records the value on model spans.

### Credential resolution order

The plugin never writes your API key to `settings.json`. It looks for a key in this order:

1. The `WANDB_API_KEY` environment variable.
2. The `~/.netrc` entry for `api.wandb.ai`, or for the host in `WANDB_BASE_URL` if you set it.

For the project and the other settings, an environment variable takes precedence over `settings.json`, which takes precedence over the default.

The Forge SDK resolves the trace server and transport. For a custom deployment, set `WANDB_BASE_URL`, or set `WF_TRACE_SERVER_URL` to override the trace server explicitly.

### Turn off content capture

Set `FORGE_CODEX_INCLUDE_CONTENT=false` to omit prompts, assistant output, reasoning, tool arguments and results, and the working directory. Spans keep model names, token usage, timing, tool names, call IDs, and MCP server names.

For interactive Stop-hook collection, set `include_content` to `false` in `~/.forge-agent-lens-for-codex/settings.json` instead. A variable set only on the `codex` command may not reach hooks run by an already-running Codex app server, so the setting in the file is the reliable one. The environment of the hook process takes precedence over the settings file, so make sure that environment doesn't set `FORGE_CODEX_INCLUDE_CONTENT=true`. If it's unset, the plugin uses the value in `settings.json`. The environment variable is reliable for explicit `forge-agent-lens-for-codex collect` runs.

## Collect past sessions

`collect --all` is an explicit backfill. It sends turns that haven't been exported yet from every rollout session. A rollout without a cursor is read from the beginning, so this command can send history created before you installed the plugin:

```bash lines theme={"system"}
forge-agent-lens-for-codex collect --all
```

Add `--json` to send JSON results.

## Check plugin status

You can use this command to check plugin status or troubleshoot issues:

```bash lines theme={"system"}
forge-agent-lens-for-codex status
```

The output shows the plugin version, whether the hook is installed, the resolved project, whether an API key resolved, the provider, the content and debug settings, the log file path, how many rollout files were found, and the status. The command never prints your API key. Add `--json` for the same report as JSON.

If turns don't appear in Agent Lens, check the collector log:

```bash lines theme={"system"}
cat ~/.forge-agent-lens-for-codex/logs/collector.log
```

## Troubleshooting

The following sections describe common issues and how to resolve them. The collector log at `~/.forge-agent-lens-for-codex/logs/collector.log` is the primary diagnostic source. The plugin always logs errors regardless of the `debug` setting.

### No traces appear after running Codex

1. Run `forge-agent-lens-for-codex status`. If the last line reads `not ready`, fix the reason it prints.
2. Confirm that the hook is installed and enabled. If you skipped the approval, run `codex`, run `/hooks`, and enable the hook.
3. Confirm that `FORGE_TRACE_PROJECT` is set to a valid `entity/project` slug, with exactly one `/`. `status` prints the resolved project.
4. Confirm that an API key resolved. `status` reports whether one resolved, but not where it came from. If the plugin reads the wrong key, check `WANDB_API_KEY` and `~/.netrc`.
5. Confirm that Codex isn't running with `--ephemeral`. That flag suppresses the rollout file the plugin reads.
6. If you upgraded the package or switched Node.js versions, run `forge-agent-lens-for-codex install` again. The hook records the Node.js and package paths it was installed with.

### Turns appear but input and output text is empty

Content capture may be disabled. Check that `FORGE_CODEX_INCLUDE_CONTENT` isn't set to `false` and that `include_content` isn't set to `false` in `~/.forge-agent-lens-for-codex/settings.json`. `status` prints the resolved `include content` value.

### Errors sending traces to Agent Lens

If the plugin is active and generates spans that don't appear in Agent Lens, check the collector log for an export error and match it against this table.

| Symptom | Most likely cause | Fix |
| - | - | - |
| `401` or `403` | Invalid API key, or a key without access to the project | Verify the key is current and has access to the entity and project. `WANDB_API_KEY` takes precedence over `~/.netrc`, so update or unset it if it holds an old key. |
| Connection refused or DNS error | DNS, proxy, or firewall | Confirm the host can reach `trace.wandb.ai` over HTTPS (port `443`). If you set `WF_TRACE_SERVER_URL` or `WANDB_BASE_URL`, confirm it can reach that host instead. |

## Upgrade the plugin

The hook records the Node.js and package paths it was installed with. To upgrade, or after switching Node.js versions, reinstall the package and run `install` again:

```bash lines theme={"system"}
npm install --global @coreweave/forge-agent-lens-for-codex@latest
forge-agent-lens-for-codex install
```

## Uninstall

To stop automatic tracing and remove the Codex Stop-hook handler:

```bash lines theme={"system"}
forge-agent-lens-for-codex uninstall
```

Then, to remove the package, run:

```bash lines theme={"system"}
npm uninstall --global @coreweave/forge-agent-lens-for-codex
```
