# Configure Mission Control MCP

Source: https://docs.coreweave.com/observability/mission-control-mcp/configure

# Configure Mission Control MCP

> Connect an MCP client to the hosted Mission Control MCP server with a CoreWeave API token.

Configure your MCP-compatible client to connect to the hosted Mission Control MCP server and
authenticate with a CoreWeave API token. For an overview of the server and its use cases, see
[Introduction to Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md). For documented tool
inputs and outputs, see the [Mission Control MCP tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md).

## Before you begin

You need the following:

* A CoreWeave account and a CoreWeave API token. Creating a token requires the **Access Token User**
  role. See [API access tokens](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md).
* An MCP-compatible client, such as Claude Code, Cursor, or the ChatGPT desktop app.

## Connect a client

**1. Create an API token**

Open the [CoreWeave Cloud Console tokens page](https://console.coreweave.com/tokens) and create
a new API token. Copy the token value. Your MCP client sends it as a bearer token when it calls
Mission Control MCP.

Treat the token like a password. It grants the same access that your account has, including
any organization-gated write tools that CoreWeave has enabled.

**2. Add the server to your client**

Configure your MCP client to connect to the Mission Control MCP endpoint and send your token as
a bearer token. Replace `[YOUR-COREWEAVE-API-TOKEN]` with the token from the previous step.

> [tab] Claude Code
>
> Run the following command:
>
> ```bash theme={"system"}
> claude mcp add --transport http mission-control \
>   https://mc.coreweave.com/mcp \
>   --header "Authorization: Bearer [YOUR-COREWEAVE-API-TOKEN]"
> ```
>
> Start a new Claude Code session after adding the server.

> [tab] Cursor
>
> Add the following to `~/.cursor/mcp.json`. Create the file if it does not exist.
>
> ```json theme={"system"}
> {
>   "mcpServers": {
>     "mission-control": {
>       "url": "https://mc.coreweave.com/mcp",
>       "headers": {
>         "Authorization": "Bearer [YOUR-COREWEAVE-API-TOKEN]"
>       }
>     }
>   }
> }
> ```
>
> Restart Cursor after saving the file.

> [tab] ChatGPT desktop app
>
> The ChatGPT desktop app shares its MCP configuration with Codex CLI. Export your token to an
> environment variable, then add the server. Replace `[YOUR-COREWEAVE-API-TOKEN]` with the
> token from the previous step.
>
> ```bash theme={"system"}
> export CW_TOKEN="[YOUR-COREWEAVE-API-TOKEN]"
> codex mcp add mission-control --url https://mc.coreweave.com/mcp --bearer-token-env-var CW_TOKEN
> ```
>
> Confirm the server is registered:
>
> ```bash theme={"system"}
> codex mcp list
> ```
>
> The `mission-control` server appears in the list without errors.

> [tab] Other clients
>
> Any MCP-compatible client can connect using the streamable HTTP transport. Refer to your
> client's documentation for where to place the server configuration, then use these values:
>
> * **URL**: `https://mc.coreweave.com/mcp`
> * **Header**: `Authorization: Bearer [YOUR-COREWEAVE-API-TOKEN]`
>
> Restart or reload your client after saving the configuration.

**3. Verify the connection**

Ask your agent a question and confirm it calls a Mission Control MCP tool:

* "List my CoreWeave clusters."
* "Search the CoreWeave docs for object storage authentication."
* "Find dashboards related to my cluster."

Look for a Mission Control MCP tool call, such as `list_datasources` or `cw_cluster_get`, in
your client's tool-use display. Seeing the tool call confirms the connection works. If your
client shows a 401 error instead, your token is missing or incorrect. Return to the first step
and create a new token.

The server resolves your organization and identity from the bearer token and scopes the
response to what your token can access.

## Next steps

* [Introduction to Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md): Review capabilities and
  how Mission Control MCP relates to Mission Control Agent.
* [Mission Control MCP tool reference](https://docs.coreweave.com/observability/mission-control-mcp/reference/tools.md): See the
  documented tools, inputs, and outputs.
