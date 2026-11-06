# Run OpenCode in a sandbox

Source: https://docs.coreweave.com/products/sandboxes/agents/opencode

# Run OpenCode in a sandbox

> Run OpenCode in a sandbox with Serverless Inference or another model provider.

Run OpenCode against a repository in a CoreWeave sandbox. Send a task from your
terminal, check the resulting files, and save the workspace for later. The agent
process, workspace, and commands run in the sandbox. Model requests go to your
configured provider.

## Prerequisites

Before you begin, you need the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* Access to a model through Serverless Inference or another
  OpenCode provider. Provider access and
  billing are separate from sandbox access.
* A public repository URL. Private repositories require Git credentials inside
  the sandbox.
* `cws-agent` installed by following its
  [installation instructions](https://github.com/coreweave/cws-agent#install).

## Choose sandbox credentials

These examples use serverless capacity. Both credentials support serverless sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and export it in your local terminal:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset.

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```

## Launch OpenCode with cws-agent

Use `cws-agent` to install OpenCode in a sandbox, clone your repository into
the `/workspace/project` directory, and configure a snapshot mount for
[file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md).

Choose one of the following provider options. Replace `[SANDBOX-NAME]` with a
session name containing 1 to 40 lowercase letters, digits, or hyphens. Start the
name with a letter or digit. Replace `[REPOSITORY-URL]` with your public repository URL.

### Use Serverless Inference (recommended)

Serverless Inference is the preferred provider for this guide. You can use
it to access hosted open models. You can use any model and provider supported by
OpenCode instead. Follow
[Use another model provider](#use-another-model-provider).

Complete the [Serverless Inference prerequisites](https://docs.coreweave.com/products/inference/serverless/api-reference.md#prerequisites),
including a Forge project, and check your available
[inference credits](https://docs.coreweave.com/products/inference/serverless/usage-limits.md).
Set a Forge API key for inference. This example selects GLM 5.2 explicitly:

```bash theme={"system"}
export WANDB_API_KEY="[WANDB-API-KEY]"
cws-agent launch [SANDBOX-NAME] --agent opencode \
  --repo-url [REPOSITORY-URL] --lifetime 2h \
  --wandb --wandb-model zai-org/GLM-5.2 \
  --permission-mode native --detach
```

The `--wandb` preset configures Forge's inference endpoint and limits OpenCode to that provider. This CLI preset reads `WANDB_API_KEY` and forwards it into the sandbox for inference. Sandbox access uses the credential selected in [Choose sandbox credentials](#choose-sandbox-credentials). To choose a different
Forge model, replace `zai-org/GLM-5.2` with an ID from the
[available models](https://docs.coreweave.com/products/inference/serverless/models.md) list.

### Use another model provider

To use another provider, omit `--wandb` and `--wandb-model` when you create the
sandbox. Export that provider's API key locally. For example, choose one of
these alternatives and replace the key placeholder:

> [tab] Anthropic
>
> ```bash theme={"system"}
> export ANTHROPIC_API_KEY="[ANTHROPIC-API-KEY]"
> ```

> [tab] OpenAI
>
> ```bash theme={"system"}
> export OPENAI_API_KEY="[OPENAI-API-KEY]"
> ```

Replace `[PROVIDER-ID]/[MODEL-ID]` in both fields with your OpenCode model
identifier, using the `anthropic/` or `openai/` provider prefix as appropriate.
The `small_model` field selects the model for lightweight tasks such as title
generation. See [OpenCode models](https://opencode.ai/docs/models/).

```bash theme={"system"}
export OPENCODE_CONFIG_CONTENT='{"model":"[PROVIDER-ID]/[MODEL-ID]","small_model":"[PROVIDER-ID]/[MODEL-ID]"}'
cws-agent launch [SANDBOX-NAME] --agent opencode \
  --repo-url [REPOSITORY-URL] --lifetime 2h \
  --env-passthrough OPENCODE_CONFIG_CONTENT \
  --permission-mode native --detach
```

If they're set, `cws-agent` forwards `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`.
For providers whose keys aren't forwarded automatically, follow their
[OpenCode provider configuration](https://opencode.ai/docs/providers/) and use
`--env-passthrough [VARIABLE-NAME]` for additional environment variables.

Both launch options print `session ready.` after setup. `--detach` leaves the
sandbox running without opening the terminal interface or importing local
skills and Model Context Protocol (MCP) configuration. The 2-hour lifetime is a
wall-clock limit, including setup. Stop compute when you finish.

## Run a task and check the result

From your local terminal, ask OpenCode to write and read a file:

```bash theme={"system"}
cws-agent run [SANDBOX-NAME] \
  'Create sandbox-proof.txt in the current directory containing exactly Hello from CoreWeave followed by a newline, then read it back. Do not commit or push anything.' \
  --permission-mode native
```

This runs OpenCode without an interactive terminal. `--permission-mode native`
keeps OpenCode's configured permissions. Without it, `cws-agent` defaults to
accepting approval requests. If your OpenCode policy requires approval for the
task, use an interactive session to approve it. See
[OpenCode permissions](https://opencode.ai/docs/permissions/).

Check the actual file independently of the agent's response:

```bash theme={"system"}
cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt'
```

The output should be `Hello from CoreWeave`. Before you stop compute, retrieve
a local copy:

```bash theme={"system"}
cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt' > sandbox-proof.txt
```

### Optional: Work interactively

From an interactive terminal on macOS or Linux, open OpenCode in the
same workspace:

```bash theme={"system"}
cws-agent connect [SANDBOX-NAME] --permission-mode native --no-config-sync
```

The `--no-config-sync` flag skips local skills and MCP imports. Send prompts and
approve actions in OpenCode, then use `/exit` to return to your local terminal.
When you exit OpenCode, the sandbox continues to run. Repeat the connection
command to open OpenCode again. It doesn't automatically select a previous conversation.
For conversation history and resume commands, see
[`cws-agent` sessions](https://github.com/coreweave/cws-agent/blob/main/docs/sessions.md).

## Save, stop, and restore

After the agent finishes, snapshot the workspace and stop compute:

```bash theme={"system"}
cws-agent down [SANDBOX-NAME]
```

`down` saves the `/workspace` directory before stopping the sandbox. If the snapshot fails,
the sandbox remains running. Inspect the error and retry after resolving it.
To stop without waiting for an explicit snapshot, run:

```bash theme={"system"}
cws-agent down [SANDBOX-NAME] --no-snapshot
```

Don't rely on this command to save changes. Copy results elsewhere or confirm
a completed snapshot before stopping. Restore requires a completed snapshot.

To return to a workspace saved with Forge inference, make sure `WANDB_API_KEY` is
still exported in your local terminal, then run:

```bash theme={"system"}
cws-agent restore [SANDBOX-NAME] --wandb --wandb-model zai-org/GLM-5.2 --lifetime 2h --no-config-sync
```

Use the same `--wandb-model` value you launched with. If you omit it while using
`--wandb`, restore selects the preset's default model.

For another provider, re-export its key and `OPENCODE_CONFIG_CONTENT`, then run:

```bash theme={"system"}
cws-agent restore [SANDBOX-NAME] --env-passthrough OPENCODE_CONFIG_CONTENT --lifetime 2h --no-config-sync
```

Restore creates a new sandbox from the saved workspace. Supply environment-only
credentials again. Snapshots can contain saved OpenCode logins
and conversation data, but they don't preserve running processes.

Run the file check again to confirm the `sandbox-proof.txt` file survived. Continue with
`cws-agent run` or the interactive connection command. Stop the restored sandbox
with `cws-agent down` when you finish.

## Troubleshoot

If setup or a task fails, use the following checks:

* Sandbox authentication fails: Check the selected sandbox credential and account access.
* Forge model requests fail: Check inference access, credits, and the model
  ID. Sandbox access alone doesn't establish inference access.
* Another provider isn't available: Start a new session without `--wandb`.
  The Forge preset is saved in the workspace, so omitting `--wandb` on restore
  doesn't remove it. For an existing workspace, see
  [Forge preset configuration](https://github.com/coreweave/cws-agent/blob/main/docs/opencode.md#resume-and-restore).
* A headless task needs approval: Connect interactively and use OpenCode's
  approval prompts before continuing.

## Next steps

For more information, see these guides:

* [Run agents on CoreWeave sandboxes](https://docs.coreweave.com/products/sandboxes/agents.md) explains agent
  execution models and workspace lifetimes.
* [OpenCode configuration](https://opencode.ai/docs/config/) covers model,
  provider, and project settings.
* [Use the Sandboxes SDK](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md) explains how
  to manage command execution directly from your application.
