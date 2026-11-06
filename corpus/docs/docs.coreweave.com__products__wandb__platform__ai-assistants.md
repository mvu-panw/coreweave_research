# Use Weights & Biases with AI Assistants

Source: https://docs.coreweave.com/products/wandb/platform/ai-assistants

# Use Weights & Biases with AI Assistants

> Use W&B Skills and the Weights & Biases MCP Server to automate workflows, query data, and search documentation.

Weights & Biases integrates with AI assistants in two complementary ways:

* **W\&B Skills** teach coding agents how to use Weights & Biases effectively in your code and analysis workflows.
* **The Weights & Biases MCP Server** connects AI assistants to your Weights & Biases data and documentation so they can answer natural-language questions about your runs, traces, evaluations, and artifacts.

Use Skills when you want your coding agent to write or modify Weights & Biases-aware code. Use the MCP server when you want an AI assistant to query live Weights & Biases data or search Weights & Biases documentation. The two work well together: Skills provide workflow patterns, and MCP provides data access.

Depending on the integration, Weights & Biases works with several major coding agents, IDEs, and chat assistants, including:

* Claude Code
* Codex
* Cursor
* Gemini CLI
* Visual Studio Code (VS Code)
* Mistral LeChat
* Claude Desktop

For a full list of agents supported by W\&B Skills, see the [W\&B Skills CLI documentation](https://github.com/vercel-labs/skills#supported-agents).

## W\&B Skills

W\&B Skills are reusable instruction sets that teach coding agents how to use Weights & Biases effectively. Instead of manually guiding your agent through W\&B APIs and best practices, install Skills so that the agent can work with experiment tracking, tracing, evaluations, and monitoring on its own.

### Capabilities

Skills cover both the [W\&B Python SDK](https://docs.coreweave.com/products/wandb/ref.md) (training runs, metrics, artifacts, sweeps) and the [Weave SDK](https://docs.coreweave.com/products/wandb/weave/reference/python-sdk.md) (traces, evaluations, scorers). They include helper libraries, reference docs, and data analysis patterns so your agent can handle the following workflows.

| Workflow | Capabilities |
| - | - |
| **Model training** | <ul><li>Log metrics and rich media during training and fine-tuning.</li><li>Track and compare experiments.</li><li>Analyze runs and results, such as loss curves and accuracy scores.</li><li>Tune hyperparameters.</li></ul> |
| **Agent building** | <ul><li>Trace agentic AI applications.</li><li>Analyze traces and classify failure modes.</li><li>Evaluate models and agents with labeled datasets.</li><li>Run online evaluations for production monitoring.</li></ul> |

### Prerequisites

W\&B Skills require the following:

* [Node.js](https://nodejs.org/) for the `npx` command.

* A Forge API Key. Create one at [forge.coreweave.com/settings#apikeys](https://forge.coreweave.com/settings#apikeys) and then set it as an environment variable. Replace `[YOUR-API-KEY]` with your API key:

  ```bash theme={"system"}
  export WANDB_API_KEY="[YOUR-API-KEY]"
  ```

* Optional: Set your Weights & Biases project name as a `WANDB_PROJECT` environment variable. This lets your agent target the correct Weights & Biases project without you specifying it each time.

### Install W\&B Skills

Choose a global installation to make Skills available to all your projects, or a project-specific installation to scope Skills to a single project.

To install W\&B Skills globally for all your projects, use the `--global` flag:

```bash theme={"system"}
npx skills add wandb/skills --skill '*' --yes --global
```

To install Skills only for the current project, run the install command from your project directory without the `--global` flag:

```bash theme={"system"}
npx skills add wandb/skills --skill '*' --yes
```

Install Skills for specific agents using the `--agent` flag:

```bash theme={"system"}
npx skills add wandb/skills \
  --agent claude-code \
  --skill '*' \
  --yes \
  --global
```

For a list of `--agent` and `--skill` options, see the [Vercel Labs skills CLI documentation](https://github.com/vercel-labs/skills#supported-agents).

After installation completes, your agent has access to W\&B Skills and is ready to handle Weights & Biases-related tasks.

### Use W\&B Skills

Ask your agent to perform Weights & Biases-related tasks for your project. The following example prompts demonstrate some of the tasks your agent can do with W\&B Skills:

* "Log training metrics for my PyTorch model to Weights & Biases."
* "Analyze the loss curves for my last 10 runs and identify the best performing configuration."
* "Trace my LangChain agent and log the results to Weave."
* "Run an evaluation on my agent using the test dataset and summarize the results."
* "Find the failure modes in my last evaluation and classify them."
* "Compare the configs of run A and run B and show me the differences."

### W\&B Skills usage tips

Skills performs better with specific queries than with broad, open-ended questions. The following table compares recommended prompts with prompts that are too vague.

| Recommended | Not recommended |
| - | - |
| "What is the final validation loss for my last 5 runs?" | "How is my model doing?" |
| "Summarize the token usage across my last 10 traces." | "Show me all my traces." |
| "Compare the configs of run A and run B." | "What are my best runs?" |
| "What eval had the highest F1 score?" | "How are my evaluations going?" |

## Weights & Biases MCP Server

Model Context Protocol (MCP) is an open standard that lets AI agents call external tools. The Weights & Biases MCP Server gives your IDE, coding assistant, or chat agent direct access to your Weights & Biases data and documentation. With this access, your agent can answer questions about your runs, traces, evaluations, and artifacts without copy-paste. For details of what you can do with the server, see the [Weights & Biases MCP Server capabilities](#weights-&-biases-mcp-server-capabilities) section.

## Deployment types

The Weights & Biases MCP Server is available in two deployment options. Use the hosted server for the fastest setup, or set up a local version if you need more isolation and flexibility. The local version requires your client to use a different URL to access the server.

> [card] Hosted server (recommended)
>
> A Weights & Biases-managed MCP server that your client connects to over HTTP with your API Key. No installation, no local process to maintain.
>
> [Use the hosted server](#use-the-hosted-server)

> [card] Local install
>
> Run the MCP server on your own machine over STDIO or HTTP. Use when you need air-gapped operation, pinning to a specific release, custom server behavior, active server development, or support for a client that only speaks STDIO.
>
> [Run the MCP server locally](#run-the-mcp-server-locally)

## Prerequisites

Before you configure any client, make sure you have the following in place:

* Create an API Key at [forge.coreweave.com/settings#apikeys](https://forge.coreweave.com/settings#apikeys).
* Set the key as the `WANDB_API_KEY` environment variable, or pass it to your client as a bearer token.
* For Dedicated Cloud, Self-Managed, and local installs against a non-default instance, set the `WANDB_BASE_URL` environment variable to your instance URL.
* Weights & Biases pins the `mcp` SDK to [1.14.0](https://pypi.org/project/mcp/1.14.0/), release `2024-11-05`. Clients must connect using `mcp` SDK 1.14.x. For streamable HTTP support in W\&B Dedicated Cloud, `mcp` SDK 1.14.x release `2025-03-26` or newer is required.

## Use the hosted server

Weights & Biases runs a managed MCP server for every deployment type. You don't need to install anything. Configure your client to connect over HTTP with an API Key in the `Authorization` header.

### Connection URL

The URL depends on your type of Weights & Biases deployment:

| Deployment | Server URL |
| - | - |
| Multi-tenant Cloud | `https://mcp.withwandb.com/mcp` |
| Dedicated Cloud | `https://[YOUR-INSTANCE]/mcp` |
| Self-Managed | `https://[YOUR-INSTANCE]/mcp` |

For Dedicated Cloud or Self-Managed, replace `https://mcp.withwandb.com/mcp` with `https://[YOUR-INSTANCE]/mcp` and keep everything else the same. The following client configurations use the Multi-tenant URL.

> [tab] Claude Code
>
> Register the Weights & Biases MCP server with Claude Code, replacing the bearer token with your API Key:
>
> ```bash theme={"system"}
> claude mcp add --transport http wandb https://mcp.withwandb.com/mcp \
>   --header "Authorization: Bearer [YOUR-WANDB-API-KEY]"
> ```
>
> Add `--scope user` to configure Claude Code globally. Omit it to configure only the current project.
>
> Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams. If the connection fails, see [Troubleshooting](#troubleshooting). For more information, see [Claude Code's MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp).

> [tab] Claude Desktop
>
> Claude Desktop's built-in custom connectors interface doesn't support API key authentication for remote MCP servers. To work around this, use the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) npm proxy to connect Claude Desktop to the Weights & Biases remote MCP server. The proxy runs locally and forwards requests to `https://mcp.withwandb.com/mcp` with your bearer token.
>
> You need [Node.js](https://nodejs.org/) installed on your system.
>
> Open your Claude Desktop config file in a text editor. You can find the config file at the following location for your OS:
>
> * **macOS**: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
> * **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
>
> Add the following to the JSON object in your config file, replacing `[YOUR-WANDB-API-KEY]` with your API Key:
>
> ```json theme={"system"}
> {
>   "mcpServers": {
>     "wandb": {
>       "command": "npx",
>       "args": [
>         "-y",
>         "mcp-remote",
>         "https://mcp.withwandb.com/mcp",
>         "--header",
>         "Authorization:${AUTH_HEADER}"
>       ],
>       "env": {
>         "AUTH_HEADER": "Bearer [YOUR-WANDB-API-KEY]"
>       }
>     }
>   }
> }
> ```
>
> The full header value is set through the `env` field rather than directly in `args` to work around a space-escaping issue in some Claude Desktop versions.
>
> Restart Claude Desktop to activate the new configuration. Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams. If the connection fails, see [Troubleshooting](#troubleshooting).

> [tab] Codex
>
> Export your API Key as an environment variable, then register the server with Codex:
>
> ```bash theme={"system"}
> export WANDB_API_KEY=[YOUR-WANDB-API-KEY]
> codex mcp add wandb \
>   --url https://mcp.withwandb.com/mcp \
>   --bearer-token-env-var WANDB_API_KEY
> ```
>
> Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams. If the connection fails, see [Troubleshooting](#troubleshooting).

> [tab] Cursor
>
> Install the server in Cursor automatically with the [one-click installation link](https://cursor.com/en/install-mcp?name=wandb\&config=eyJ0cmFuc3BvcnQiOiJodHRwIiwidXJsIjoiaHR0cHM6Ly9tY3Aud2l0aHdhbmRiLmNvbS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIge3tXQU5EQl9BUElfS0VZfX0iLCJBY2NlcHQiOiJhcHBsaWNhdGlvbi9qc29uLCB0ZXh0L2V2ZW50LXN0cmVhbSJ9fQ%3D%3D), then replace the placeholder with your API Key in the `Authorization` field.
>
> To configure Cursor manually:
>
> 1. On macOS, open **Cursor** > **Settings** > **Cursor Settings**. On Windows or Linux, open **Preferences** > **Settings** > **Cursor Settings**.
>
> 2. Select **Tools and MCP**.
>
> 3. In **Installed MCP Servers**, select **Add Custom MCP**. Cursor opens the `mcp.json` configuration file.
>
> 4. Add the following to the `mcpServers` object:
>
>    ```json theme={"system"}
>    {
>      "mcpServers": {
>        "wandb": {
>          "transport": "http",
>          "url": "https://mcp.withwandb.com/mcp",
>          "headers": {
>            "Authorization": "Bearer [YOUR-WANDB-API-KEY]",
>            "Accept": "application/json, text/event-stream"
>          }
>        }
>      }
>    }
>    ```
>
> 5. Restart Cursor.
>
> 6. Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams.
>
> If the connection fails, see [Troubleshooting](#troubleshooting). For more information, see [Cursor's MCP documentation](https://cursor.com/docs/context/mcp).

> [tab] Gemini CLI
>
> Install the Weights & Biases MCP extension:
>
> ```bash theme={"system"}
> gemini extensions install https://github.com/wandb/wandb-mcp-server
> ```
>
> Restart Gemini CLI. Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams.
>
> If the connection fails, see [Troubleshooting](#troubleshooting). For more information, see [Gemini CLI's MCP documentation](https://geminicli.com/docs/tools/mcp-server/).

> [tab] Mistral LeChat
>
> 1. In LeChat, open the **Intelligence** menu and select **Add Connector**.
> 2. Select **Custom MCP Connector**.
> 3. Configure the following fields:
>    * **Connector Server**: `https://mcp.withwandb.com/mcp`
>    * **Description**: (Optional) A short description.
>    * **Authentication Method**: Select **API Token Authentication**.
>    * **Header name**: Leave as `Authorization`.
>    * **Header type**: Select **Bearer**.
>    * **Header value**: Your API Key.
> 4. Select **Create**.
> 5. Verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams.
>
> If the connection fails, see [Troubleshooting](#troubleshooting). For more information, see [LeChat's MCP documentation](https://mistral.ai/news/le-chat-mcp-connectors-memories).

> [tab] OpenAI Responses API
>
> Add the server to the `tools` field of your OpenAI Responses API call:
>
> ```python theme={"system"}
> import os
> from openai import OpenAI
>
> client = OpenAI()
>
> resp = client.responses.create(
>     model="gpt-4o",
>     tools=[{
>         "type": "mcp",
>         "server_label": "wandb",
>         "server_description": "Query W&B data",
>         "server_url": "https://mcp.withwandb.com/mcp",
>         "authorization": os.getenv("WANDB_API_KEY"),
>         "require_approval": "never",
>     }],
>     input="List my W&B entities.",
> )
>
> print(resp.output_text)
> ```
>
> Pass the raw API Key as the `authorization` value. OpenAI prepends `Bearer ` when it calls the server, so don't include it yourself. The OpenAI MCP integration runs server-side, so it can't reach a local MCP server. For local development, see [Run the MCP server locally](#run-the-mcp-server-locally).

> [tab] VS Code
>
> Open your global or workspace `mcp.json` (for example, `~/.vscode/mcp.json` or `.vscode/mcp.json`) and add the following:
>
> ```json theme={"system"}
> {
>   "servers": {
>     "wandb": {
>       "type": "http",
>       "url": "https://mcp.withwandb.com/mcp",
>       "headers": {
>         "Authorization": "Bearer [YOUR-WANDB-API-KEY]"
>       }
>     }
>   }
> }
> ```
>
> Restart VS Code, confirm the server appears in the MCP panel, and verify the connection by asking `List my W&B entities.` The agent should call `list_entities_tool` and return your username and any teams.
>
> If the connection fails, see [Troubleshooting](#troubleshooting).

## Run the MCP server locally

A local install is an alternative to the hosted server, not the default for any deployment type. Use it when the hosted server doesn't fit your setup.

Common reasons to run locally:

* **Air-gapped or offline environments** where your client can't reach a hosted Weights & Biases endpoint.
* **Pinned version**. The hosted server follows the main branch. A local install can pin to a specific release tag.
* **Custom server behavior** such as changing tool descriptions, adding tools, or setting a non-default response token budget.
* **Active development** on the server itself.
* **STDIO-only clients** or clients that require a local process.

For Dedicated Cloud or Self-Managed users, prefer the hosted path. Only use a local install from [wandb/wandb-mcp-server](https://github.com/wandb/wandb-mcp-server) if the hosted server isn't yet enabled on your instance or one of the preceding reasons applies. Set a `WANDB_BASE_URL` environment variable to your instance URL.

### Local prerequisites

To run the server locally, make sure you have the following:

* Python 3.11 or higher.
* [`uv`](https://docs.astral.sh/uv/) or `pip`.
* An API Key, set as `WANDB_API_KEY`.
* `WANDB_BASE_URL` set to your instance URL if you use Dedicated Cloud or Self-Managed.

### Install the server

Choose an install method and run the following command to install the MCP server:

> [tab] uvx (no permanent install)
>
> ```bash theme={"system"}
> uvx --from git+https://github.com/wandb/wandb-mcp-server wandb_mcp_server
> ```

> [tab] uv
>
> ```bash theme={"system"}
> uv pip install wandb-mcp-server
> ```

> [tab] pip
>
> ```bash theme={"system"}
> pip install wandb-mcp-server
> ```

> [tab] Install from GitHub
>
> ```bash theme={"system"}
> pip install git+https://github.com/wandb/wandb-mcp-server
> ```

### Configure your client

After installing the server, configure your client to launch it. Select your MCP client and then run the following configuration, replacing `[YOUR-WANDB-API-KEY]` with your API Key as necessary:

> [tab] Claude Code
>
> Register the local server with Claude Code. Add `--scope user` for a global configuration.
>
> ```bash theme={"system"}
> claude mcp add wandb \
>   -e WANDB_API_KEY=[YOUR-WANDB-API-KEY] \
>   -e WANDB_BASE_URL=https://your-wandb-instance.example.com \
>   -- uvx --from git+https://github.com/wandb/wandb-mcp-server wandb_mcp_server
> ```

> [tab] Claude Desktop
>
> Open your Claude Desktop config file:
>
> * **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
> * **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
>
> Add the following JSON. Use the full path to `uvx` because Claude Desktop may not find it on your `PATH` otherwise.
>
> ```json theme={"system"}
> {
>   "mcpServers": {
>     "wandb": {
>       "command": "/full/path/to/uvx",
>       "args": [
>         "--from",
>         "git+https://github.com/wandb/wandb-mcp-server",
>         "wandb_mcp_server"
>       ],
>       "env": {
>         "WANDB_API_KEY": "[YOUR-WANDB-API-KEY]",
>         "WANDB_BASE_URL": "https://your-wandb-instance.example.com"
>       }
>     }
>   }
> }
> ```
>
> Restart Claude Desktop to apply the configuration.

> [tab] Codex
>
> ```bash theme={"system"}
> codex mcp add wandb \
>   --env WANDB_API_KEY=[YOUR-WANDB-API-KEY] \
>   --env WANDB_BASE_URL=https://your-wandb-instance.example.com \
>   -- uvx --from git+https://github.com/wandb/wandb-mcp-server wandb_mcp_server
> ```

> [tab] Cursor
>
> Add the following to your `mcp.json` configuration:
>
> ```json theme={"system"}
> {
>   "mcpServers": {
>     "wandb": {
>       "command": "uvx",
>       "args": [
>         "--from",
>         "git+https://github.com/wandb/wandb-mcp-server",
>         "wandb_mcp_server"
>       ],
>       "env": {
>         "WANDB_API_KEY": "[YOUR-WANDB-API-KEY]",
>         "WANDB_BASE_URL": "https://your-wandb-instance.example.com"
>       }
>     }
>   }
> }
> ```
>
> Omit `WANDB_BASE_URL` to use the default W\&B API endpoint.

> [tab] VS Code
>
> Add the following to your `.vscode/mcp.json` or global MCP configuration:
>
> ```json theme={"system"}
> {
>   "servers": {
>     "wandb": {
>       "command": "uvx",
>       "args": [
>         "--from",
>         "git+https://github.com/wandb/wandb-mcp-server",
>         "wandb_mcp_server"
>       ],
>       "env": {
>         "WANDB_API_KEY": "[YOUR-WANDB-API-KEY]",
>         "WANDB_BASE_URL": "https://your-wandb-instance.example.com"
>       }
>     }
>   }
> }
> ```

### Run the server with HTTP transport

For web-based clients and for testing, run the server with HTTP transport:

```bash theme={"system"}
uvx wandb_mcp_server --transport http --host 0.0.0.0 --port 8080
```

To expose a local server to external clients, such as the OpenAI Responses API, use a tunnel:

```bash theme={"system"}
uvx wandb_mcp_server --transport http --port 8080

# In another terminal
ngrok http 8080
```

Update your MCP client configuration to use the tunnel URL.

### Environment variables

The following environment variables control authentication, instance routing, and server behavior for local installs. Set them in your client's `env` block or export them in your shell.

| Variable | Description |
| - | - |
| `WANDB_API_KEY` | API Key for authentication. Required. |
| `WANDB_BASE_URL` | Custom Weights & Biases instance URL for Dedicated Cloud or Self-Managed. Defaults to `https://api.wandb.ai`. |
| `WANDB_MCP_PROXY_DOCS` | Enable the `search_wandb_docs_tool` documentation search proxy. Default: `true`. |
| `WANDBOT_BASE_URL` | Custom endpoint for the docs search proxy. |
| `MAX_RESPONSE_TOKENS` | Token budget for tool-response truncation. Default: `30000`. |
| `MCP_SERVER_LOG_LEVEL` | Logging verbosity. One of `DEBUG`, `INFO`, `WARNING`, `ERROR`. |

For the complete command-line reference and advanced options, see the [wandb-mcp-server README](https://github.com/wandb/wandb-mcp-server#readme).

## Weights & Biases MCP Server capabilities

Use the MCP server to analyze experiments, debug traces, create reports, manage registry and artifacts, and answer questions from the Weights & Biases docs. The following example prompts demonstrate some of the tasks you can ask your agent to perform when it's connected to the Weights & Biases MCP Server:

* "Show me the top 5 runs by `eval/accuracy` in `your-team/your-project`."
* "How did the latency of my hiring agent's predict traces evolve over the last month?"
* "Generate a W\&B report comparing decisions made by the hiring agent last week."
* "What versions of the `production-model` artifact exist, and what changed between `v2` and `v3`?"
* "How do I create a leaderboard in Weave?"

### Available tools

The server offers several tools grouped by purpose. The following table lists each tool's name, when the agent should use it, and a concrete prompt you can use to invoke that tool.

> [tab] Discovery
>
> Tools that help you discover project and entity names, and inspect schemas.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `list_entities_tool` | No entity is specified, or to enumerate the teams and accounts the API key can reach. | "What Weights & Biases teams do I have access to?" |
> | `query_wandb_entity_projects` | The entity is known but the project name is not, or an earlier query failed with "project not found". | "List all projects under `your-team`." |
> | `probe_project_tool` | To discover available metrics, config keys, and tags in an unfamiliar run-based project. | "Probe `your-team/your-project` and tell me what metrics are logged." |
> | `infer_trace_schema_tool` | To discover field names, types, and sample values in an unfamiliar Weave traces project before querying. | "What fields are on the Weave traces in `your-team/your-project`?" |

> [tab] Experiments and runs
>
> Tools that query, compare, and diagnose W\&B runs.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `query_wandb_tool` | The question is about runs, sweeps, configs, summaries, or artifacts in Weights & Biases. Runs a GraphQL query. | "Show me the top 5 runs by `eval/accuracy` in `your-team/your-project`." |
> | `get_run_history_tool` | The question is about training curves, metric trends over time, or any time-series logged to a run. | "Plot the loss curve for run `abc123` in `your-team/your-project`." |
> | `compare_runs_tool` | The question is what changed between two runs, or which of two runs is better. Returns config diff, metric delta, and optional aligned history. | "Compare runs `abc123` and `def456` in `your-team/your-project`." |
> | `diagnose_run_tool` | The question is whether a run converged, is overfitting, or hit NaN values. Returns specific recommendations. | "Is run `abc123` in `your-team/your-project` overfitting?" |

> [tab] Weave traces
>
> Tools that query and aggregate LLM traces and evaluations.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `query_weave_traces_tool` | Trace data is required (LLM calls, evaluations, agent runs). Start with `detail_level="summary"` and escalate to `"full"` only for specific traces. | "Show me failed traces in `your-team/your-project` from the last 24 hours." |
> | `count_weave_traces_tool` | The question is how many traces or how many errors, and the trace data itself isn't needed. | "How many traces failed in `your-team/your-project` this week?" |
> | `resolve_trace_roots_tool` | After `query_weave_traces_tool` finds child traces, to map each back to its root session or workflow in one batched call. | "Find LLM calls that contain `rate limit` and tell me which sessions they belong to." |
> | `summarize_evaluation_tool` | The question is how an eval went, what the pass rate is, or which tasks fail most. Aggregates `Evaluation.evaluate` hierarchies. | "Summarize the most recent eval in `your-team/your-project`." |

> [tab] Reports
>
> Tools that persist analysis back to Weights & Biases.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `create_wandb_report_tool` | An explicit request to create a report or save findings. Accepts Markdown plus a `panels` array for line plots, bar plots, and run comparisons. | "Create a W\&B report comparing runs `abc123` and `def456`." |
> | `log_analysis_to_wandb` | Values computed in the MCP session (latency distributions, error breakdowns) need to be persisted as a run before being referenced in a report. | "Log these latency percentiles to Weights & Biases as an analysis run." |

> [tab] Artifacts and registry
>
> Tools that enable you to inspect and diff models, datasets, and other versioned artifacts.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `list_registries_tool` | The question is about model registries, registered models, or registered datasets in an organization. | "What registries exist in `your-org`?" |
> | `list_registry_collections_tool` | To see what models or datasets live inside a specific registry. | "What collections are in the `model` registry of `your-org`?" |
> | `list_artifact_versions_tool` | To list available versions of a model, dataset, or other artifact collection. | "List versions of `production-model` in `your-team/your-project`." |
> | `get_artifact_details_tool` | To inspect one specific artifact version, including lineage and files. | "What is in `production-model:v3`?" |
> | `compare_artifact_versions_tool` | The question is what changed between two artifact versions. | "Diff `production-model:v2` and `production-model:v3`." |

> [tab] Docs
>
> Tools that answer product questions from the official Weights & Biases documentation.
>
> | Tool | Use when | Example prompt |
> | - | - | - |
> | `search_wandb_docs_tool` | The question is how to use a Weights & Biases or Weave feature or API. Proxies [docs.wandb.ai](https://docs.coreweave.com/forge-home.md). | "How do I create a leaderboard in Weave?" |

### Schema-first trace queries

For Weave trace queries, call `infer_trace_schema_tool` first to discover available fields, then call `query_weave_traces_tool` with a precise column list and `detail_level`:

| `detail_level` | Returns | Use when |
| - | - | - |
| `schema` | Structural fields only. Fastest. | Browsing or counting. |
| `summary` | Truncated inputs and outputs. The default. | Most analysis tasks. |
| `full` | Everything untruncated. | Drilling into a small number of specific traces. |

This pattern keeps token usage low for broad questions and lets the agent escalate to `full` only for the traces that matter.

## Usage tips

The following sections describe practices and workflows that help you get better results from the Weights & Biases MCP Server. Start with the general practices, then read the section that matches your workload for more specific advice and multi-step tool chains.

### General best practices

Follow these practices regardless of your use case:

* **Specify the entity and project.** MCP tools need an explicit entity (your team or personal account) and project name. Include both in every question, for example "in `your-team/your-project`".
* **Ask focused questions.** Prefer "Which eval had the highest F1 score?" to "What is my best evaluation?". Specific metrics and time ranges produce better tool calls.
* **Verify full retrieval.** For broad questions such as "What are my best performing runs?", ask the agent to confirm it retrieved all available runs rather than only the most recent ones.
* **Combine with W\&B Skills.** [W\&B Skills](#w\&b-skills) teach coding agents how to structure Weights & Biases workflows. Skills provide patterns and MCP provides data access, and the two work well together.

### For trace-heavy workflows

Follow these practices when working with Weave traces:

* **Start with the schema.** Call `infer_trace_schema_tool` before `query_weave_traces_tool` to provide the agent with the valid fields and filter values.
* **Pick the right `detail_level`.** Use `schema` to browse, `summary` (the default) for analysis, and `full` only when drilling into a small number of specific traces.
* **Chain `resolve_trace_roots_tool`.** After a child-trace query, pass the resulting `trace_id` list to `resolve_trace_roots_tool` to map each trace to its root session in one batched call.
* **Prefer `summarize_evaluation_tool` for evals.** It aggregates the `Evaluation.evaluate` and `predict_and_score` hierarchy automatically. Only fall back to `query_weave_traces_tool` for raw trace data.

For an end-to-end workflow, see [Triage failing LLM calls](#triage-failing-llm-calls).

### For run-heavy workflows

Follow these practices when working with W\&B runs:

* **Probe before you query.** Call `probe_project_tool` on an unfamiliar run-based project to discover metric keys, config keys, and tags before constructing GraphQL.
* **Use `get_run_history_tool` for time series.** GraphQL doesn't sample, so for loss curves and other time-series data `get_run_history_tool` is both faster and cheaper.
* **Let `compare_runs_tool` do the diff.** It returns config and metric deltas with aligned history in a single call, avoiding manual comparison.
* **Run a health check first.** When a training run looks wrong, call `diagnose_run_tool` before digging into history manually.

For end-to-end workflows, see [Diagnose a bad training run](#diagnose-a-bad-training-run) and [Summarize evals and compare model versions](#summarize-evals-and-compare-model-versions).

### For Dedicated Cloud and Self-Managed

Follow these practices for non-multi-tenant deployments:

* Prefer the hosted server on your instance at `https://[YOUR-INSTANCE]/mcp`. It exposes the same tools as the Multi-tenant server with no client-side `WANDB_BASE_URL` needed. Only fall back to a local install if the hosted server isn't yet enabled.
* When you do run locally against your instance, set `WANDB_BASE_URL` to your instance URL in the client's `env` block. Without it, the server targets `api.wandb.ai` and the server returns no data.
* Rate limits on Dedicated Cloud are separate from Multi-tenant. See [Dedicated Cloud rate limits](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud/rate-limits.md) for defaults and how to request changes.

### For local installs

Follow these practices when running the server on your own machine:

* Prefer STDIO transport for desktop clients (Cursor, VS Code, Claude Code, Claude Desktop). Only switch to HTTP transport when a client explicitly requires it (for example, the OpenAI Responses API).
* When tool calls fail silently, set `MCP_SERVER_LOG_LEVEL=DEBUG` in the client's `env` block and recheck the client's MCP logs.
* If you install from GitHub (`uvx --from git+https://github.com/wandb/wandb-mcp-server wandb_mcp_server`), `uvx` pins to the default branch. Pin an explicit tag by appending `@v0.3.2` to the Git URL when you need a stable version.

## Recommended workflows

Most real questions need more than one tool. The following workflows show common multi-step tool chains you can ask your agent to perform.

### Explore an unfamiliar project

To explore what has been logged to a project, chain these tools:

1. `list_entities_tool` to find an entity or team.
2. `query_wandb_entity_projects` to find the project.
3. `probe_project_tool` for run-based projects, or `infer_trace_schema_tool` for Weave trace projects.
4. A targeted `query_wandb_tool` or `query_weave_traces_tool` call using the discovered keys.

### Triage failing LLM calls

To find bad traces and the sessions that produced them, chain these tools:

1. `query_weave_traces_tool` with a filter on error or exception fields, and `detail_level="summary"`.
2. `resolve_trace_roots_tool` on the resulting `trace_id` list to map each failure to its root session.
3. `query_weave_traces_tool` with `detail_level="full"` on a small number of specific roots to drill in.
4. `create_wandb_report_tool` to document the findings.

### Diagnose a bad training run

To run a health check on a suspicious training run, chain these tools:

1. `get_run_history_tool` to pull the loss and validation curves.
2. `diagnose_run_tool` for automated convergence, overfitting, and NaN checks.
3. `compare_runs_tool` against a known-good baseline run.
4. `create_wandb_report_tool` with line-plot panels to share the diagnosis.

### Summarize evals and compare model versions

To find which model version performed best on an evaluation, chain these tools:

1. `summarize_evaluation_tool` for per-scorer pass rates and error counts.
2. `list_artifact_versions_tool` on the relevant model collection.
3. `compare_artifact_versions_tool` between the candidate and current production version.
4. `log_analysis_to_wandb` and `create_wandb_report_tool` to publish the comparison.

## Troubleshooting

Use the following table to help you diagnose and resolve issues using the Weights & Biases MCP Server:

| Symptom | Cause and fix |
| - | - |
| `401 Unauthorized` or `Invalid API key` | Your API Key is missing, malformed, or not authorized for the target entity or team. Regenerate a key at [forge.coreweave.com/settings#apikeys](https://forge.coreweave.com/settings#apikeys) and confirm it is passed as a bearer token or set in `WANDB_API_KEY`. |
| Empty results for queries you expect to succeed | The team, entity, or project name is incorrect, or the API key doesn't have access. Confirm both with the agent and retry. |
| `404 Not Found` or `connection refused` on `https://[YOUR-INSTANCE]/mcp` | The hosted MCP server isn't yet enabled on your Dedicated Cloud or Self-Managed instance, or the client is pointed at the wrong URL. Contact [Weights & Biases support](mailto:forge-support@coreweave.com) to request enablement, then confirm the URL in [Connection URL](#connection-url). |
| `429 Too Many Requests` on Dedicated Cloud | You have hit your instance's rate limits. See [Dedicated Cloud rate limits](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud/rate-limits.md) for how to request higher limits. |
| Local server can't find `uvx` in Claude Desktop | Use the full path to `uvx` in the `command` field of `claude_desktop_config.json`. |
