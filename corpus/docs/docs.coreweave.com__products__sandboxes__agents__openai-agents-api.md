# Run OpenAI Agents API on Sandboxes

Source: https://docs.coreweave.com/products/sandboxes/agents/openai-agents-api

# Run OpenAI Agents API on Sandboxes

> Connect OpenAI-managed agents to a CoreWeave sandbox for tool execution and shared-workspace analysis.

Use CoreWeave Sandboxes as the execution environment for an OpenAI-managed agent.
Your application creates an Agents API session and a CoreWeave sandbox. A Codex
executor inside that sandbox connects to OpenAI and runs the agent's commands.
This page explains the execution model, the credentials each component requires,
and the resource lifetimes you manage. With that context, you can run the
companion recipe and adapt the same pattern in your own application.

The companion recipe investigates a synthetic inference-service
incident. Three specialist subagents analyze latency, errors, and capacity. Their
coordinator combines the results into an incident report and answers a follow-up.
The application downloads the results, and a separate local verifier checks the
calculations and recorded agent activity.

## Execution model

OpenAI runs the agent loop, manages conversation context, and supplies delegation
tools. CoreWeave runs the executor and the programs the agents write. Your
application manages sandbox provisioning, file transfer, and cleanup.

The coordinator and its subagents share one sandbox and one filesystem.
Creating a subagent doesn't create a separate CoreWeave sandbox. Give each
specialist its own output files and let the coordinator own the final report.
These file assignments are conventions for avoiding write conflicts, not access
controls.
See OpenAI's [multi-agent guide](https://developers.openai.com/api/docs/guides/agents-api/multi-agent).

## Requirements

Before you run the example, meet these requirements:

* A [Forge API key](https://forge.coreweave.com/settings#apikeys), or a CoreWeave API access token with the `sandbox_user` action,
  and capacity for one CPU sandbox. Follow
  [Choose a credential](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* An OpenAI project with Agents API access and access to the selected model.
* Python and `uv`, using the versions and lockfile in the companion recipe.
* Outbound HTTPS to `api.openai.com` and secure WebSocket access to
  `codex-cloud-environments.chatgpt.com`. Image setup also requires the package
  registries used to install the executor and runtime dependencies.

This example uses CPU compute to analyze supplied telemetry. It doesn't launch
an inference server or request a GPU. OpenAI model usage and CoreWeave sandbox
compute have separate billing terms.

## Keep application and executor credentials separate

This example uses three credentials: one sandbox credential and two OpenAI keys.
Each credential belongs to a single component, which keeps application access out
of the sandbox:

| Credential | Used by | Purpose |
| - | - | - |
| `WANDB_API_KEY` | Your application | Provision and operate sandboxes with Forge authentication (`--sandbox-auth wandb`) |
| `CWSANDBOX_API_KEY` | Your application | Provision and operate sandboxes with CoreWeave authentication (the default) |
| `OPENAI_API_KEY` | Your application | Create sessions, submit input, and inspect results |
| `OPENAI_EXECUTOR_API_KEY` | Sandbox executor, as `CODEX_API_KEY` | Connect this execution environment to OpenAI |

The recipe defaults to CoreWeave authentication. To use the Forge API key, pass
`--sandbox-auth wandb`. The recipe reads `WANDB_API_KEY` for Forge authentication. Only the selected sandbox credential is required, but
either mode requires both OpenAI keys. The application records the selected
mode so cleanup uses the same provider credentials.

The OpenAI application key requires `api.agents.read`, `api.agents.write`, and
`api.responses.write`. Create the separate environment key in
[**Agents > Environments > Keys**](https://platform.openai.com/agents?tab=environments\&environment_view=keys).
It must have the same organization, project, and user or service-account ownership
as the session. Set unrelated permissions to **None**.

The recipe passes the restricted executor key through the `environment_variables`
argument in the SDK. It doesn't configure a secret store.

Upload only task inputs. Keep application credentials, local configuration, and
the verifier outside the sandbox. Follow the
[OpenAI authentication instructions](https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted#authentication).

> [!WARNING]
>
> Agent-generated code can read the executor key. Restrict its permissions to limit
> what that code can access through OpenAI.

## Connect an agent session

The runnable recipe implements these steps with the OpenAI and CoreWeave SDKs:

1. Create a self-hosted Agents API session and save its session ID and environment
   ID. Use the exact returned `remote_url` when starting the executor.
2. Create a CoreWeave sandbox with an explicit maximum lifetime and both Python
   and Node.
3. Start `codex exec-server` with the returned environment ID and unchanged
   remote URL. Inject only the restricted executor key as `CODEX_API_KEY`.
4. Upload the synthetic inputs and task instructions, then confirm the environment
   connection. Submit the task and observe its outcome.
5. Retrieve generated artifacts and API activity records before cleanup.

At the end of this sequence, the agent's output files and the session's activity
records are available locally for inspection.

The following configuration excerpt enables built-in delegation at session creation.
The recipe passes these dictionaries to `client.beta.agents.sessions.create()`:

```python theme={"system"}
agent = {
    "model": "gpt-6-astra",
    "instructions": "Follow TASK.md. Delegate the three independent analyses, then synthesize their findings.",
    "multi_agent": {"enabled": True, "max_concurrent_subagents": 3},
}
environment = {
    "type": "self_hosted",
    "workspace_directory": "/workspace/project",
}
```

This configuration permits up to three concurrent subagents, excluding the
coordinator. The instructions request delegation. Configuration alone doesn't
prove the model used it.

The recipe attributes API-completed script commands through turn and subagent IDs.
Commands with explicit nonzero exit codes don't count as successful execution
evidence. The verifier reports omitted exit codes as unknown.
The optional `--require-exit-codes` check requires numeric zero-exit evidence for
every specialist. Overlapping `started_at` and `completed_at` intervals show
concurrent subagent turns. These timestamps have whole-second precision, so they
don't prove simultaneous shell processes or a speedup over a sequential run.

## Run the example

Follow the [recipe setup and run steps](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/openai-agents-api).
The recipe includes original synthetic data, a task specification, the
application, and an independent verifier.
After completing the recipe's installation and OpenAI credential setup, choose your sandbox credential. These commands use serverless capacity. The sandbox credential stays in the local application.

> [tab] Forge API key
>
> Set `WANDB_API_KEY` in the recipe's `.env` file, then explicitly select Forge authentication:
>
> ```bash theme={"system"}
> uv run python run.py run --sandbox-auth wandb --env-file .env --output-dir runs/incident-wandb-001
> ```
>
> If the run is interrupted, clean up using the same output directory:
>
> ```bash theme={"system"}
> uv run python run.py cleanup --env-file .env --output-dir runs/incident-wandb-001
> ```

> [tab] CoreWeave API access token
>
> Set `CWSANDBOX_API_KEY` in the recipe's `.env` file, then select CoreWeave authentication:
>
> ```bash theme={"system"}
> uv run python run.py run --sandbox-auth coreweave --env-file .env --output-dir runs/incident-001
> ```
>
> If the run is interrupted, clean up using the same output directory:
>
> ```bash theme={"system"}
> uv run python run.py cleanup --env-file .env --output-dir runs/incident-001
> ```

Cleanup reads the authentication mode from the saved resource journal. Keep the matching credential available until cleanup finishes.

Inspect the downloaded report alongside the verifier's findings.

You can also inspect session turns and tool calls in
[**OpenAI Logs > Agents**](https://platform.openai.com/logs?api=agents) while the session
exists. Select the matching organization and project. This example doesn't
provide a chat UI or establish ChatGPT or Codex app continuity.

For an existing command-line interface (CLI) workflow, see
[OpenAI Agents API in cws-agent](https://github.com/coreweave/cws-agent/blob/main/docs/openai-agents.md).
The recipe uses the SDKs directly and doesn't require that CLI.

## Session, sandbox, and file lifetimes

Manage the conversation, compute, and workspace files separately when choosing
what to preserve.

| Resource | What preserves it | What ends it |
| - | - | - |
| API conversation | Reusing the same OpenAI session ID | Explicit API session deletion, subject to provider retention policies |
| Running sandbox | Keeping CoreWeave compute alive | Explicit stop, maximum lifetime, or infrastructure failure |
| Workspace files | Keeping the sandbox or saving files or snapshots | Losing compute without a preserved copy |

Choose the compute lifetime explicitly. The recipe sets a 20-minute maximum
lifetime. A maximum lifetime is a cap, not an inactivity timer that each prompt
refreshes.

Reconnecting an executor to the same running sandbox retains its workspace. Starting
replacement compute with the same environment ID doesn't restore its files.
Download artifacts or use CoreWeave persistence features before stopping compute.
The recipe downloads artifacts and deletes its resources. It doesn't
implement automatic recovery or snapshot and restore.

Stopping a sandbox doesn't delete its API conversation. Deleting the conversation
doesn't stop the sandbox. Attempt both cleanup operations and report each failure.

## Handle failures

To investigate failures, use the following guidance:

* **The executor never connects:** check environment-key ownership, outbound network
  access, executor compatibility, and the exact remote URL returned by OpenAI.
* **OpenAI reports a usage or billing limit:** check the OpenAI organization and
  project billing limits before retrying. An executor connection alone doesn't
  establish that a model turn can run.
* **The stream disconnects or the client times out:** inspect session state and saved
  events before retrying input. A timeout doesn't itself cancel cloud work.
* **Delegation or overlap isn't observed:** read the saved activity evidence.
  A correct report alone is insufficient evidence of a parallel multi-agent run.
* **The OpenAI environment expires:** inspect its state before retrying. The recipe
  may wait until its work deadline rather than fail immediately.
* **The sandbox expires:** recover saved artifacts if available. A replacement
  sandbox requires an explicit file-restoration policy.
* **The application is interrupted:** use the recipe's saved resource journal and
  cleanup command. The maximum sandbox lifetime is a fallback, not a substitute
  for deleting the API session.

For applications that retain sessions, coordinate shutdown with incoming work.
An idle event alone isn't a safe shutdown signal. Webhook-driven provisioning is
a separate deployment pattern. See OpenAI's
[sandbox lifecycle guide](https://developers.openai.com/api/docs/guides/agents-api/environments/lifecycle).
