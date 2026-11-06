# Claude Agent SDK

Source: https://docs.coreweave.com/products/agent-lens/integrations/claude-agents-sdk

# Claude Agent SDK

> Trace an agent built with the Claude Agent SDK using Agent Lens.

The Claude Agent SDK enables you to quickly build agent applications powered by Claude. You can integrate CoreWeave Agent Lens into your Claude agents to automatically trace their calls, including agent queries, model responses, tool use, and multi-turn conversations.

> [!NOTE]
>
> This integration uses the Weights & Biases Weave SDK (`weave`), because the CoreWeave Forge SDK doesn't support this framework yet. Traces you send with Weave appear in Agent Lens, because both products share the same trace data.

## Trace Claude Agent SDK agents with Agent Lens

> [tab] Python
>
> The Weave SDK autopatches the [Claude Agent SDK for Python](https://github.com/anthropics/claude-agent-sdk-python), letting you capture traces from your Claude agents with minimal setup.
>
> This guide shows how to initialize Weave and run a multi-turn Claude agent with MCP tools through `query()`. Agent Lens automatically traces the conversation, model calls, and tool calls end-to-end.
>
> ### Prerequisites
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * An Anthropic API key set as an `ANTHROPIC_API_KEY` environment variable.
> * Python 3.10+.

> [tab] TypeScript
>
> The Weave SDK integrates with the [`@anthropic-ai/claude-agent-sdk`](https://github.com/anthropics/claude-agent-sdk) to automatically trace `query()` calls, including agent spans, model responses, and tool calls.
>
> ### Prerequisites
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * An Anthropic API key set as an `ANTHROPIC_API_KEY` environment variable.
> * Node.js 18+.
> * `@anthropic-ai/claude-agent-sdk` version `0.3.178` or later.

### Install packages

Install the following packages in your developer environment. The `weave` package captures traces, `claude-agent-sdk` provides the agent runtime, and the remaining packages support the example tool.

```bash Python theme={"system"}
pip install weave claude-agent-sdk requests
```

```bash TypeScript theme={"system"}
npm install weave @anthropic-ai/claude-agent-sdk zod
```

### Initialize Agent Lens in your code

> [tab] Python
>
> Add `weave.init` to the project, update your Forge team and project names, and then build an agent the way you normally would. `weave.init` enables the autopatching that captures traces from the Claude Agent SDK.
>
> This example defines a `wikipedia_search` MCP tool and runs a three-turn conversation. Each turn is a separate `query()` call, but later turns pass `resume` with the first turn's session ID so that all turns group as one conversation in the Agent Lens **Conversations** tab. The first two turns trigger Wikipedia lookups, and the third uses the previous conversation context to produce a summary without a tool call.
>
> ```python lines highlight="13,49,55" theme={"system"}
> import anyio
> import requests
> import weave
>
> from claude_agent_sdk import (
>     ClaudeAgentOptions,
>     ResultMessage,
>     create_sdk_mcp_server,
>     query,
>     tool,
> )
>
> weave.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> @tool(
>     "wikipedia_search",
>     "Search Wikipedia for a topic and return its title and intro paragraph.",
>     {"query": str},
> )
> async def wikipedia_search(args: dict) -> dict:
>     r = requests.get(
>         "https://en.wikipedia.org/w/api.php",
>         params={
>             "action": "query", "generator": "search", "gsrsearch": args["query"], "gsrlimit": 1,
>             "prop": "extracts", "exintro": True, "explaintext": True, "format": "json",
>         },
>         headers={"User-Agent": "weave-demo"},
>     ).json()
>     page = next(iter(r["query"]["pages"].values()))
>     return {"content": [{"type": "text", "text": f"{page['title']}: {page['extract']}"}]}
>
> wiki_server = create_sdk_mcp_server(
>     name="wiki",
>     version="1.0.0",
>     tools=[wikipedia_search],
> )
>
> async def main():
>     session_id = None
>
>     for question in [
>         "Who founded Anthropic?",
>         "What is Claude (the AI assistant)?",
>         "Summarize what we discussed in one sentence.",
>     ]:
>         options = ClaudeAgentOptions(
>             mcp_servers={"wiki": wiki_server},
>             allowed_tools=["mcp__wiki__wikipedia_search"],
>             resume=session_id,
>         )
>         print(f"USER: {question}")
>
>         async for message in query(prompt=question, options=options):
>             if isinstance(message, ResultMessage):
>                 session_id = message.session_id
>                 print(f"AGENT: {message.result}\n")
>
>
> anyio.run(main)
> ```
>
> Each `query()` call produces an `invoke_agent` root span. Because the follow-up turns resume the same session, Weave stamps the same `gen_ai.conversation.id` on all spans, and Agent Lens groups them as one conversation. `ResultMessage.session_id` carries the ID to reuse, and `resume` accepts `None` on the first turn, which starts a new session.
>
> Without `resume`, each turn starts its own session and appears as a separate conversation. `ClaudeSDKClient` is the exception: it holds one session open for the lifetime of the `async with` block, so turns you send through the same client are already grouped. Weave patches both paths.

> [tab] TypeScript
>
> Weave automatically instruments `query()` via module loader hooks. The required setup differs slightly between module systems. For more information on CommonJS versus ESM and how Weave's loader hooks work, see the [TypeScript SDK third-party integration guide](https://docs.coreweave.com/products/wandb/weave/guides/integrations/js.md).
>
> * **CommonJS projects**: No extra configuration needed. Require `weave` before `@anthropic-ai/claude-agent-sdk` so auto-instrumentation runs first.
> * **ESM projects**: Start Node with the `--import=weave/instrument` flag so the instrumentation loads before any other modules.
>
> This example defines a `wikipedia_search` MCP tool and runs a three-turn conversation. Each turn is a separate `query()` call, but later turns pass `resume` with the first turn's `session_id` so that all turns group as one session in the Agent Lens Conversations. The first two turns trigger Wikipedia lookups, and the third uses the previous conversation context to produce a summary without a tool call.
>
> ```typescript lines highlight="36" title="main.mjs" theme={"system"}
> import * as weave from "weave";
> import { createSdkMcpServer, query, tool, type Options } from "@anthropic-ai/claude-agent-sdk";
> import { z } from "zod";
>
> const wikipediaSearch = tool(
>     "wikipedia_search",
>     "Search Wikipedia for a topic and return its title and intro paragraph.",
>     { query: z.string().describe("The topic to search for") },
>     async ({ query }) => {
>     const url = new URL("https://en.wikipedia.org/w/api.php");
>     url.search = new URLSearchParams({
>         action: "query",
>         generator: "search",
>         gsrsearch: query,
>         gsrlimit: "1",
>         prop: "extracts",
>         exintro: "true",
>         explaintext: "true",
>         format: "json",
>     }).toString();
>
>     const response = await fetch(url, { headers: { "User-Agent": "weave-demo" } });
>     const data = await response.json();
>     const page = Object.values(data.query.pages)[0] as { title: string; extract: string };
>     return { content: [{ type: "text" as const, text: `${page.title}: ${page.extract}` }] };
>     },
> );
>
> const wikiServer = createSdkMcpServer({
>     name: "wiki",
>     version: "1.0.0",
>     tools: [wikipediaSearch],
> });
>
> async function main() {
>     await weave.init("[YOUR-TEAM]/[YOUR-PROJECT]");
>
>     const baseOptions: Options = {
>     model: "claude-sonnet-4-5",
>     maxTurns: 4,
>     mcpServers: { wiki: wikiServer },
>     allowedTools: ["mcp__wiki__wikipedia_search"],
>     };
>
>     const questions = [
>     "Who founded Anthropic?",
>     "What is Claude (the AI assistant)?",
>     "Summarize what we discussed in one sentence.",
>     ];
>
>     let sessionId: string | undefined;
>
>     for (const prompt of questions) {
>     const options: Options = sessionId
>         ? { ...baseOptions, resume: sessionId }
>         : baseOptions;
>
>     console.log(`USER: ${prompt}`);
>     for await (const message of query({ prompt, options })) {
>         if (message.type === "system" && message.subtype === "init") {
>         sessionId ??= message.session_id;
>         }
>         if (message.type === "result" && message.subtype === "success") {
>         console.log(`AGENT: ${message.result}\n`);
>         }
>     }
>     }
> }
>
> main().catch(console.error);
> ```
>
> Each `query()` call produces an `invoke_agent` root span. Because the follow-up turns resume the same `session_id`, Agent Lens stamps the same `gen_ai.conversation.id` on all spans and groups them as one session in the Conversations view.
>
> Save the example as `main.mjs` and run it with the `--import=weave/instrument` flag so the loader hook runs before any other module:
>
> ```bash theme={"system"}
> node --import=weave/instrument main.mjs
> ```

### View your traces in Agent Lens

After the script runs, `weave.init()` prints a link to your project in Weave. The same traces appear in Agent Lens, because both products share the same trace data. To view them in Agent Lens:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com) and select **Agent Lens** from the product menu.
2. Select your project.
3. In the Agent Lens side menu, select **Conversations**, and then select your conversation.

Each turn renders as an `invoke_agent` span with nested `chat` and `execute_tool` spans. Each span shows its input, model, output, token usage, and tool results.

For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
