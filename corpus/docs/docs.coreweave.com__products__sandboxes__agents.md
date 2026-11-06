# Run agents on Sandboxes

Source: https://docs.coreweave.com/products/sandboxes/agents

# Run agents on Sandboxes

> Run interactive and autonomous agents with longer sessions, parallel work, and tools on CoreWeave.

Give your agent a workspace where it can edit code, run tests, and save results on CoreWeave. This overview helps you choose an integration and configure the environment for longer sessions, subagents, and tool execution.

For agents that operate a graphical desktop through screenshots, mouse input, and keyboard input, see [Run a computer-use agent in a sandbox](https://docs.coreweave.com/products/sandboxes/tutorials/computer-use.md).

For benchmark-based agent evaluation, see [Run evaluations on CoreWeave sandboxes](https://docs.coreweave.com/products/sandboxes/evals.md).

The [Claude Code cloud sessions](https://docs.coreweave.com/products/sandboxes/agents/claude-code-cloud.md) example provisions a worker sandbox on demand through a sandbox-hosted orchestrator for each session you start at claude.ai/code. The worker stops after release.

## Interactive coding agents and autonomous agents

With an interactive coding agent, you work alongside the agent: ask questions, review edits, and approve actions through a terminal, browser, or mobile app. For example, use Claude Code to investigate a failing test while you guide the changes.

With an autonomous agent, you delegate a task and collect results later. For example, assign a repository migration, let the agent run tests and revise its changes, then review the result. Configure its permissions, credentials, and stopping conditions before starting work. It can still pause for your input when needed.

These are ways of working, not separate sandbox types. A coding harness can support both. The harness manages the agent loop, model context, tool selection, and delegation. CoreWeave supplies the compute and filesystem where tools run. A longer sandbox lifetime gives the agent more execution time, but conversation compaction and task recovery depend on the harness.

## Choose an integration

The following integrations execute commands in a CoreWeave sandbox. The location of the agent loop and the interface you use differ:

| Guide | Agent loop runs in | You interact through | Use it to |
| - | - | - | - |
| [Claude Code](https://docs.coreweave.com/products/sandboxes/agents/claude-code.md) | The sandbox | An attached terminal, Claude's mobile or Desktop app, or claude.ai/code | Work on a repository from your terminal or use Remote Control from another device. |
| [Cursor](https://docs.coreweave.com/products/sandboxes/agents/cursor.md) | The sandbox | An attached terminal or a script | Edit a repository interactively or run unattended coding tasks. |
| [OpenCode CLI](https://docs.coreweave.com/products/sandboxes/agents/opencode.md) | The sandbox | An attached terminal or a command | Run coding tasks with Serverless Inference or another model provider. |
| [Muse Code](https://docs.coreweave.com/products/sandboxes/agents/muse-code.md) | The sandbox | The Sandboxes SDK | Run a CLI task on a repository and retrieve the result. |
| [Pi](https://docs.coreweave.com/products/sandboxes/agents/pi.md) | The sandbox | An attached terminal | Work on a repository with your choice of model provider, including Serverless Inference. |
| [Claude Managed Agents](https://docs.coreweave.com/products/sandboxes/agents/claude-managed-agents.md) | Anthropic's managed service | The Managed Agents API | Connect a self-hosted worker to a managed agent session. |
| [Codex](https://docs.coreweave.com/products/sandboxes/agents/codex.md) | The sandbox | Codex CLI in the sandbox, a local CLI connected to Codex App Server, or desktop and paired mobile apps | Work on a remote repository with Codex. |
| [Devin Outposts](https://docs.coreweave.com/products/sandboxes/agents/devin-outposts.md) | Devin Cloud | Devin Cloud | Run Devin's commands in a sandbox through an outpost worker. |
| [OpenAI Agents API](https://docs.coreweave.com/products/sandboxes/agents/openai-agents-api.md) | OpenAI's managed service | Your application through the Agents API | Run agent tools and subagent analyses in a self-hosted sandbox. |

The Claude Code and Pi examples start an interactive agent in a workspace you manage. The Cursor examples support interactive work and unattended tasks. The Muse Code example runs a task without an interactive terminal. The Managed Agents and Devin Outposts examples start workers that reuse a sandbox across queued sessions. Ending one provider session doesn't stop that worker sandbox.

Model inference remains with the provider configured for your agent. Running tools in a sandbox doesn't prevent the agent from sending prompts, file contents, or tool output to that provider. Review its data-handling requirements before connecting your workspace.

## Build your own integration

Use the [Sandboxes SDK](https://docs.coreweave.com/products/sandboxes/client.md) to create an environment, execute tool calls, collect results, and stop compute from your own harness. Start with [command execution](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md), [file operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md), and [cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md).

## Get started with cws-agent

[`cws-agent`](https://github.com/coreweave/cws-agent) automates sandbox creation, agent installation, and workspace management. Most integration guides include a quick-start path that uses it. Other guides set up the sandbox directly with the Sandboxes SDK. Where a guide documents both, you can use either path independently.

Follow the [installation instructions](https://github.com/coreweave/cws-agent#install), then choose an integration guide and configure your sandbox credential in [Choose sandbox credentials](#choose-sandbox-credentials). Authenticate to the agent provider separately.

For configuration imports, parallel sessions, and saving or restoring workspaces, see the [`cws-agent` documentation](https://github.com/coreweave/cws-agent#more). You don't need `cws-agent` to integrate a harness directly.

## Choose sandbox credentials

These examples use serverless capacity. Both credentials support serverless sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

For the SDK path, create your local project before you save the configuration file. Save the file for your language beside the scripts you run from this guide. Use the same file for creation, reconnection, and cleanup. It stores your authentication choice, not the key itself.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and export it in your local terminal:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset. The SDK configuration in this tab selects it explicitly.
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.WANDB
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.COREWEAVE_API_KEY
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

## Choose where sandboxes run

[Serverless placement](https://docs.coreweave.com/products/sandboxes/get-started.md#run-a-sandbox-on-serverless-capacity) uses capacity CoreWeave operates. It's the starting point in these guides.

Use [CoreWeave Kubernetes Service (CKS) placement](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) when you need your own cluster placement and sandbox policy. Your administrator deploys the runner and configures the network and resource constraints. Agents require outbound access to their provider and any package or source hosts they use.

## Run longer sessions

The lifetime is a wall-clock limit, including startup, and can't be extended after creation. It doesn't guarantee that the agent finishes or recovers from interruptions.

Serverless sandboxes default to a 10-minute lifetime when you omit `max_lifetime_seconds`. A CKS runner can supply a different policy default. Set the lifetime explicitly at creation, allowing time for setup and the task.

### Set a serverless sandbox lifetime

After completing [SDK installation](https://docs.coreweave.com/products/sandboxes/get-started.md#run-your-first-sandbox) and saving your credential configuration, use this creation request for a sandbox with a 24-hour lifetime:

> [tab] Python
>
> ```python theme={"system"}
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> sandbox = Sandbox.run(
>     auth=AUTH,
>     placement_mode="serverless",
>     container_image="python:3.12-slim",
>     resources={"cpu": "4", "memory": "8Gi"},
>     max_lifetime_seconds=24 * 60 * 60,
> )
> print(f"Sandbox ID: {sandbox.sandbox_id}")
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
> const sandbox = await client.create({
>   containerImage: "python:3.12-slim",
>   resources: { cpu: "4", memory: "8Gi" },
>   maxLifetimeSeconds: 24 * 60 * 60,
>   waitUntilRunning: false,
> });
> console.log(`Sandbox ID: ${sandbox.sandboxId}`);
> ```

Save the printed ID to [reconnect with the SDK](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#reconnection). The ID confirms that creation was accepted, not that startup has finished. Follow an integration guide to wait for readiness, install, and start your agent, or supply an image with your tools already installed.

Both standalone creation calls leave the sandbox running after the script exits. TypeScript's `withSandbox()` stops it when its callback finishes. A `with Sandbox.run(...)` block stops it when the block exits. Sandboxes created through an SDK `Session` stop when that session closes, including during process-exit cleanup.

With `cws-agent` installed and authenticated, set the same lifetime when launching Claude Code. Replace `[SANDBOX-NAME]` with a `cws-agent` session name for your workspace. Use 1 to 40 lowercase letters, digits, or hyphens, starting with a letter or digit:

```bash theme={"system"}
cws-agent launch [SANDBOX-NAME] --lifetime 24h --cpu 4 --memory 8Gi --permission-mode native
```

To keep an interactive agent running when you close your terminal, run it inside a terminal multiplexer. See the [`tmux` guide](https://github.com/tmux/tmux/wiki/Getting-Started) for detach and reconnect instructions. A detached session can still wait for an approval or login.

### Configure CKS placement and policy

CKS placement requires a CoreWeave API access token with the `sandbox_user` IAM action. Follow [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md). In Python, set `auth=AuthStrategy.COREWEAVE_API_KEY`, keep `max_lifetime_seconds`, and set `placement_mode="cks"` and `runner_ids=["[RUNNER-ID]"]`. Replace `[RUNNER-ID]` with your cluster's runner ID. In TypeScript, use the `@coreweave/cwsandbox/node` entry point, keep `maxLifetimeSeconds`, and set `runnerIds: ["[RUNNER-ID]"]` to select CKS.

The runner must have a configured policy. The resource ceilings must accommodate the creation request. Retain other constraints and any higher ceilings needed by existing workloads. Policy writes replace the entire document, and changes apply to newly created sandboxes.

To make 24 hours the default for requests that omit a lifetime, have the administrator edit the existing policy with the [CoreWeave Intelligent CLI](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy):

```bash theme={"system"}
cwic sandbox runner policy edit [RUNNER-ID]
```

Merge these fields into the existing `constraints` object. This is a policy fragment, not a complete replacement document:

```json theme={"system"}
{
  "constraints": {
    "lifecycle": {
      "defaultLifetimeSeconds": 86400
    },
    "resources": {
      "maxCpu": "4",
      "maxMemory": "8Gi"
    }
  }
}
```

An explicit request lifetime takes precedence over `defaultLifetimeSeconds`. The platform maximum is 30 days. The policy has no `maxLifetimeSeconds` field to raise.

To permit provider connections, also configure [network egress](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-network-access): `allowedEgress` permits requested destinations, while `defaultEgress` supplies access when the request omits egress rules. An allowance alone doesn't grant access.

### Keep execution time and conversation state separate

A tool command's `timeout_seconds` is separate from the sandbox lifetime. Give long builds and tests an appropriate command timeout. For unattended tasks, use the harness's supported background execution and recovery features, and save intermediate results. See [command timeouts](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md#set-a-timeout) and [sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md).

## Delegate work to subagents

Configure subagents in your harness. No sandbox creation flag enables subagents. For example, Claude Code includes built-in subagents. In an interactive session, ask it to split independent investigations:

```text theme={"system"}
Use separate subagents to inspect the API and its tests in parallel.
Have each report relevant files and findings without editing anything.
Combine their findings into an implementation plan.
```

To define a reusable specialist, create this file in the sandbox's project before starting Claude Code:

```markdown title=".claude/agents/test-reader.md" theme={"system"}
---
name: test-reader
description: Inspect tests and report coverage gaps without editing files.
tools: Read, Grep, Glob
---
Find tests relevant to the requested change. Summarize coverage gaps and
cite the test files. Do not modify files.
```

Ask Claude to use `test-reader` for a specific task. Delegation is available by default. A `permissions.deny` rule for the parent agent's `Agent` tool blocks delegation. For tool permissions and other options, see [Claude Code subagent configuration](https://code.claude.com/docs/en/sub-agents).

Subagents using one sandbox share its compute and filesystem. Size CPU and memory for concurrent tools, and avoid simultaneous edits to the same files. When workers need independent credentials or isolation, use separate sandboxes.

For separate coding tasks, [`cws-agent` parallel sessions](https://github.com/coreweave/cws-agent/blob/main/docs/sessions.md) provide separate Git worktrees within one sandbox. These are independent sessions, not harness-managed subagents or separate security boundaries.

## Use tools efficiently

Prepare the environment so agents can spend time on the task:

* **Install recurring dependencies in the image.** Pass a prepared `container_image` at creation to avoid installing the same test tools and runtimes for every session. See [sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md).
* **Select the tools the task needs.** Configure skills and Model Context Protocol (MCP) servers in the harness. For a CLI session managed by `cws-agent`, preview local configuration and import selected items into its sandbox:

  ```bash theme={"system"}
  cws-agent config preview [SANDBOX-NAME] --verbose
  cws-agent config sync [SANDBOX-NAME]
  ```

  Configuration import isn't available for Claude Managed Agents workers. The `sync` command prompts for selections and confirmation. Restart the agent to load the changes. Install required executables in the sandbox and replace laptop-only paths. See [skills and MCP imports](https://github.com/coreweave/cws-agent/blob/main/docs/config-import.md).
* **Return focused results.** Have tools filter or summarize data in the sandbox before returning it to the model. For example, save full test output to a file and return failed test names and a short failure summary. Keep the file available for follow-up inspection.
* **Parallelize independent operations.** When resources allow, run independent checks concurrently. Wait for prerequisites before dependent steps. The [SDK execution guide](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md#sequential-compared-with-parallel-execution) shows how to start commands and collect results.

Tool discovery, context compaction, and decisions about which tools to call remain harness features. CoreWeave runs the commands and stores their files.

## Keep results and stop compute

Exiting an agent or ending a provider session doesn't necessarily stop its sandbox. Follow the cleanup steps in the integration guide, and set a lifetime when you create compute.

Copy results out before stopping, push changes to your repository, or configure a snapshot mount to use [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md). Snapshots preserve files, not running processes. Provider conversation history has its own lifecycle.
