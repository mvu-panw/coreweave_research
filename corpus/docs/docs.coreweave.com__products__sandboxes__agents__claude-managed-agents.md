# Use Sandboxes with Claude Managed Agents

Source: https://docs.coreweave.com/products/sandboxes/agents/claude-managed-agents

# Use Sandboxes with Claude Managed Agents

> Connect a self-hosted sandbox worker to Claude Managed Agents and verify tool execution on CoreWeave.

Connect [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) to a worker running in a CoreWeave sandbox. Anthropic manages the agent loop and conversation. The worker executes tools and returns their results to Anthropic. This integration uses a self-hosted environment and is separate from the Claude Code CLI and Remote Control.

Claude Managed Agents is also in beta. Its API requires the `managed-agents-2026-04-01` beta header. The Anthropic software development kit (SDK) used in this guide adds it automatically. See [Anthropic beta access](https://platform.claude.com/docs/en/managed-agents/overview#beta-access).

## Prerequisites

Before you begin, you need the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* Claude Managed Agents access in your Anthropic workspace and a Console API key for the client that creates sessions.
* An existing agent configured with `agent_toolset_20260401`. Follow Anthropic's [Managed Agents quick start](https://platform.claude.com/docs/en/managed-agents/quickstart) to create one and record its ID.
* For the SDK examples, either Python 3.11 or later with [`uv`](https://docs.astral.sh/uv/), or Node.js 22 or later.

## Choose sandbox credentials

These examples use serverless capacity. The Sandboxes SDK examples require a Forge API key to resolve secret references. For `cws-agent`, choose either credential. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

For the SDK path, create your local project before you save the configuration file. Save the file for your language beside the scripts you run from this guide. Use the same file for creation, reconnection, and cleanup. It stores your authentication choice, not the key itself.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and `[WANDB-ENTITY]` with the Forge team that holds your worker secret:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> export WANDB_ENTITY="[WANDB-ENTITY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset. The SDK configuration in this tab selects it explicitly.
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > import os
> >
> > from cwsandbox import AuthHeaders
> >
> > AUTH = AuthHeaders(
> >     headers={
> >         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
> >         "x-entity-id": os.environ["WANDB_ENTITY"],
> >     },
> >     strategy="wandb_api_key",
> > )
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClient({
> >   apiKey: process.env.WANDB_API_KEY,
> >   entity: process.env.WANDB_ENTITY,
> > });
> > ```

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> Use this credential for the `cws-agent` path. The SDK worker examples require Forge secret injection.

## Create an environment

In the [Claude Console](https://platform.claude.com/environments), create a **Self-hosted** environment. Open it and generate an environment key. Record the environment ID and store the key securely. See Anthropic's [environment setup](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#create-a-self-hosted-environment).

The environment key authenticates workers to this environment. The Console API key creates sessions from your client. Keep the two credentials separate.

For the verification task, use an environment with only the worker created in this guide. That prevents another worker from claiming the test session.

With the environment ready, choose either `cws-agent` or the Sandboxes SDK to start its worker, then run the verification task.

## Quick start with cws-agent

Follow the [`cws-agent` installation instructions](https://github.com/coreweave/cws-agent#install). The tool configures a snapshot mount to save and restore your workspace with [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md#start-a-sandbox-with-a-snapshot-mount).

Replace `[ENVIRONMENT-KEY]`, `[ENVIRONMENT-ID]`, and `[SANDBOX-NAME]` with your environment key, environment ID, and a `cws-agent` workspace name for the sandbox. For the workspace name, use 1 to 40 lowercase letters, digits, or hyphens, starting with a letter or digit:

```bash theme={"system"}
export ANTHROPIC_ENVIRONMENT_KEY="[ENVIRONMENT-KEY]"
cws-agent launch [SANDBOX-NAME] --claude-env [ENVIRONMENT-ID]
```

Launch starts one worker in `/workspace/claude/0` and returns to your shell. The tool passes the environment key into the sandbox.

To view the worker's terminal, run:

```bash theme={"system"}
cws-agent connect [SANDBOX-NAME] --cmd 'tmux attach -t claude-0'
```

Detach with **Ctrl-b**, then **d**. Continue to [Run and verify a task](#run-and-verify-a-task). Send tasks through the Managed Agents API. The `cws-agent run` command doesn't drive Managed Agents conversations.

## Set up with the Sandboxes SDK

This alternative starts Anthropic's `ant` worker as the sandbox's main process. It doesn't require `cws-agent` or configure snapshots.

Run Python snippets in the virtual environment created in this guide. Save TypeScript snippets as `.mts` files in the project where you install the client, then run them with `npx tsx [FILENAME].mts`.

### Configure credentials and install the client

Use the **Forge API key** configuration from [Choose sandbox credentials](#choose-sandbox-credentials), including `WANDB_ENTITY` for the team that holds the secret. This SDK flow uses [Forge secret injection](https://docs.coreweave.com/products/sandboxes/secrets.md) on serverless capacity. It doesn't support a CoreWeave API access token or CoreWeave Kubernetes Service (CKS) placement.

Ask a Forge administrator to [add a team secret](https://docs.coreweave.com/products/wandb/platform/secrets.md#add-a-secret) named `ANTHROPIC_ENVIRONMENT_KEY` with your environment key as its value. Use a Forge API key with access to that team. Keep the value in Secret Manager. The SDK script sends only the secret's name.

Export the non-sensitive environment ID from the Claude Console in the terminal where you run the script:

```bash theme={"system"}
export ANTHROPIC_ENVIRONMENT_ID="[ENVIRONMENT-ID]"
```

Choose a client and install it locally:

> [tab] Python
>
> Use Python 3.11 or later and `uv`:
>
> ```bash theme={"system"}
> uv venv --python 3.11
> source .venv/bin/activate
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> ```

> [tab] TypeScript
>
> Use Node.js 22 or later. Install the client and TypeScript runner in your project:
>
> ```bash theme={"system"}
> npm install @coreweave/cwsandbox@1.0.0 tsx
> ```

### Start the worker

Save the script for your language using the filename shown. The script installs the `ant` CLI in a Linux image with Bash, starts one worker, and prints the sandbox ID. The platform resolves the Forge secret and injects it as `ANTHROPIC_ENVIRONMENT_KEY` for the worker. You don't need to export the environment key locally for this SDK flow.

> [tab] Python
>
> ```python title="start_claude_worker.py" theme={"system"}
> from sandbox_auth import AUTH
> import os
>
> from cwsandbox import Sandbox, Secret
>
> worker = """
> set -o pipefail
> case "$(uname -m)" in
>     x86_64) arch=amd64 ;;
>     aarch64) arch=arm64 ;;
>     *) echo "Unsupported architecture" >&2; exit 1 ;;
> esac
> version=1.33.0
> curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${version}/ant_${version}_linux_${arch}.tar.gz" \
>     | tar -xz -C /usr/local/bin ant
> mkdir -p /workspace
> exec ant beta:worker poll --workdir /workspace
> """
>
> sandbox = Sandbox.run(
>     "bash", "-ec", worker,
>     container_image="python:3.12-bookworm",
>     placement_mode="serverless",
>     secrets=[Secret(store="wandb", name="ANTHROPIC_ENVIRONMENT_KEY")],
>     environment_variables={
>         "ANTHROPIC_ENVIRONMENT_ID": os.environ["ANTHROPIC_ENVIRONMENT_ID"],
>     },
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=8 * 3600,
>     tags=["claude-managed-agents-worker"],
>     auth=AUTH,
> )
> try:
>     sandbox.wait()
> except BaseException:
>     sandbox.stop().result()
>     raise
>
> print(f"Worker sandbox ID: {sandbox.sandbox_id}")
> ```

> [tab] TypeScript
>
> ```typescript title="start_claude_worker.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID;
> if (!environmentId) throw new Error("Set ANTHROPIC_ENVIRONMENT_ID.");
>
> const worker = `
> set -o pipefail
> case "$(uname -m)" in
>     x86_64) arch=amd64 ;;
>     aarch64) arch=arm64 ;;
>     *) echo "Unsupported architecture" >&2; exit 1 ;;
> esac
> version=1.33.0
> curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v\${version}/ant_\${version}_linux_\${arch}.tar.gz" \\
>     | tar -xz -C /usr/local/bin ant
> mkdir -p /workspace
> exec ant beta:worker poll --workdir /workspace
> `;
>
> const sandbox = await client.run(["bash", "-ec", worker], {
>   containerImage: "python:3.12-bookworm",
>   secrets: [{ store: "wandb", name: "ANTHROPIC_ENVIRONMENT_KEY" }],
>   environmentVariables: {
>     ANTHROPIC_ENVIRONMENT_ID: environmentId,
>   },
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 8 * 3600,
>   waitUntilRunning: false,
>   tags: ["claude-managed-agents-worker"],
> });
> try {
>   await sandbox.wait();
> } catch (error) {
>   await sandbox.stop();
>   throw error;
> }
> console.log(`Worker sandbox ID: ${sandbox.sandboxId}`);
> ```

Run the script:

> [tab] Python
>
> ```bash theme={"system"}
> python start_claude_worker.py
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx start_claude_worker.mts
> ```

The script waits for startup. In Python, `wait()` can also return if the main process has already completed. A printed sandbox ID doesn't confirm that the worker is authenticated or polling. Before starting a task, inspect its status and recent logs. Replace `[SANDBOX-ID]` with the printed ID:

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> print("Sandbox status:", sandbox.get_status())
> for container in sandbox.container_statuses:
>     print(container.name, container.state, container.exit_code, container.restart_count)
> for line in sandbox.stream_logs(tail_lines=100):
>     print(line, end="")
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.fromId("[SANDBOX-ID]");
> console.log("Sandbox status:", sandbox.status, "Exit code:", sandbox.exitCode);
> for (const line of await sandbox.logs.read({ tailLines: 100 })) {
>   process.stdout.write(line);
> }
> ```

The Python client also reports per-container state, exit codes, and restart counts. The TypeScript client doesn't expose those details yet. Rerun this check to fetch newer logs.

This worker polls over outbound HTTPS. It doesn't require an inbound service. Each session uses the same sandbox filesystem, so this example doesn't provide a fresh sandbox per session. For that architecture, see Anthropic's [self-hosted sandbox integration guide](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes).

## Run and verify a task

Run the session client on your own machine for either setup path. Install the Anthropic SDK for your language:

> [tab] Python
>
> ```bash theme={"system"}
> uv venv --python 3.11 .claude-client
> source .claude-client/bin/activate
> uv pip install 'anthropic>=1.6.0'
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npm install @anthropic-ai/sdk@0.126.0 tsx
> ```

Replace `[ANTHROPIC-API-KEY]` with your Console API key, `[AGENT-ID]` with your existing agent ID, and `[ENVIRONMENT-ID]` with the environment connected to your worker:

```bash theme={"system"}
export ANTHROPIC_API_KEY="[ANTHROPIC-API-KEY]"
export ANTHROPIC_AGENT_ID="[AGENT-ID]"
export ANTHROPIC_ENVIRONMENT_ID="[ENVIRONMENT-ID]"
```

Save the verification script for your language using the filename shown. It asks the agent to write a unique, non-secret value in its working directory. Self-hosted tool execution produces temporary idle events while the worker handles allowed calls. The script waits through those events and stops when the turn ends or another action is required. Inspect the printed stop reason before retrieving the file.

> [tab] Python
>
> ```python title="verify_claude_worker.py" theme={"system"}
> import os
> import uuid
>
> from anthropic import Anthropic
>
> client = Anthropic()
> proof = uuid.uuid4().hex
> session = client.beta.sessions.create(
>     agent=os.environ["ANTHROPIC_AGENT_ID"],
>     environment_id=os.environ["ANTHROPIC_ENVIRONMENT_ID"],
>     title="CoreWeave worker verification",
> )
> print(f"Session ID: {session.id}")
> print(f"Expected file contents: {proof}")
> events_by_id = {}
>
> with client.beta.sessions.events.stream(session.id) as events:
>     client.beta.sessions.events.send(
>         session.id,
>         events=[{
>             "type": "user.message",
>             "content": [{
>                 "type": "text",
>                 "text": f"Write exactly {proof} to managed-agent-proof.txt in your working directory and read it back.",
>             }],
>         }],
>     )
>     for event in events:
>         print(event.model_dump_json())
>         events_by_id[event.id] = event
>         if event.type == "session.status_idle":
>             reason = event.stop_reason
>             if reason and reason.type == "requires_action":
>                 pending = [events_by_id.get(event_id) for event_id in reason.event_ids]
>                 if pending and all(
>                     getattr(tool, "evaluated_permission", None) == "allow"
>                     for tool in pending
>                 ):
>                     continue
>             break
> ```

> [tab] TypeScript
>
> ```typescript title="verify_claude_worker.mts" theme={"system"}
> import { randomUUID } from "node:crypto";
> import Anthropic from "@anthropic-ai/sdk";
>
> const agent = process.env.ANTHROPIC_AGENT_ID;
> const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID;
> if (!agent || !environmentId) {
>   throw new Error("Set ANTHROPIC_AGENT_ID and ANTHROPIC_ENVIRONMENT_ID.");
> }
> const client = new Anthropic();
> const proof = randomUUID().replaceAll("-", "");
> const session = await client.beta.sessions.create({
>   agent,
>   environment_id: environmentId,
>   title: "CoreWeave worker verification",
> });
> console.log(`Session ID: ${session.id}`);
> console.log(`Expected file contents: ${proof}`);
> const allowedEvents = new Map<string, boolean>();
>
> await client.beta.sessions.events.send(session.id, {
>   events: [{
>     type: "user.message",
>     content: [{
>       type: "text",
>       text: `Write exactly ${proof} to managed-agent-proof.txt in your working directory and read it back.`,
>     }],
>   }],
> });
>
> const events = await client.beta.sessions.events.stream(session.id);
> try {
>   for await (const event of events) {
>     console.log(JSON.stringify(event));
>     if ("id" in event) {
>       allowedEvents.set(event.id,
>         "evaluated_permission" in event && event.evaluated_permission === "allow");
>     }
>     if (event.type === "session.status_idle") {
>       const reason = event.stop_reason;
>       if (reason?.type === "requires_action" && reason.event_ids.length > 0 &&
>           reason.event_ids.every((id) => allowedEvents.get(id) === true)) {
>         continue;
>       }
>       break;
>     }
>   }
> } finally {
>   events.controller.abort();
> }
> ```

Run it and inspect the events:

> [tab] Python
>
> ```bash theme={"system"}
> python verify_claude_worker.py
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx verify_claude_worker.mts
> ```

If the script stops with `requires_action`, inspect the referenced tool events. Calls with `evaluated_permission: "ask"` need Anthropic's [tool-confirmation workflow](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#tool-confirmation). The worker handles allowed calls. If they stall, inspect its logs. Keep the session ID to continue that session rather than creating another one.

After the task completes, read the file from the sandbox with the command for your setup. Replace `[SANDBOX-NAME]` or `[SANDBOX-ID]` with the workspace name or printed sandbox ID:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent exec [SANDBOX-NAME] 'cat /workspace/claude/0/managed-agent-proof.txt'
> ```

> [tab] Sandboxes SDK
>
> > [tab] Python
> >
> > ```python theme={"system"}
> > from sandbox_auth import AUTH
> > from cwsandbox import Sandbox
> >
> > sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> > result = sandbox.exec(["cat", "/workspace/managed-agent-proof.txt"], check=True).result()
> > print(result.stdout, end="")
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript theme={"system"}
> > import { client } from "./sandbox-client.mts";
> >
> > const sandbox = await client.fromId("[SANDBOX-ID]");
> > const result = await sandbox.commands.run(["cat", "/workspace/managed-agent-proof.txt"], { check: true });
> > process.stdout.write(result.stdout);
> > ```

For Python, reactivate the virtual environment where you installed `cwsandbox` if needed. For TypeScript, save the SDK snippet as an `.mts` file and run it with `npx tsx`.

The file must match the value printed by the client. This ties the agent's tool execution to the specific CoreWeave sandbox.

## Keep results and stop

Wait for active tasks to finish and copy any results you need out of the sandbox. Then stop it using the command for your setup:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent down [SANDBOX-NAME]
> ```
>
> `down` snapshots the workspace before stopping. If capture fails, check `cws-agent status [SANDBOX-NAME]` and resolve the failure before retrying. If you can discard unsaved changes, use `down --no-snapshot`.

> [tab] Sandboxes SDK
>
> > [tab] Python
> >
> > ```python theme={"system"}
> > from sandbox_auth import AUTH
> > from cwsandbox import Sandbox
> >
> > sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> > sandbox.stop().result()
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript theme={"system"}
> > import { client } from "./sandbox-client.mts";
> >
> > const sandbox = await client.fromId("[SANDBOX-ID]");
> > await sandbox.stop();
> > ```
>
> This example doesn't configure persistent storage. Copy files out before stopping.

The sandbox's lifetime can terminate a task in progress. Ending a Managed Agents session doesn't stop this always-on worker. Stopping or restoring the sandbox also doesn't delete or restore Anthropic's conversation history.

## Troubleshoot

Use these checks to resolve common issues:

* If the session waits for a worker, check the environment ID, the worker logs, and whether another task already occupies the worker.
* If the worker can't authenticate, check its environment key. The Console API key used by the session client is a different credential.
* If a tool is missing, build an image with the required dependencies. The example uses a Python image and doesn't install a project-specific toolchain.

Tool inputs and outputs flow to Anthropic even though execution happens on CoreWeave. Managed Agents isn't eligible for Zero Data Retention or HIPAA Business Associate Agreement coverage. See [Anthropic's data-retention eligibility](https://platform.claude.com/docs/en/managed-agents/overview#beta-access). Review the [self-hosted environment security model](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security) for data handling and worker permissions.
