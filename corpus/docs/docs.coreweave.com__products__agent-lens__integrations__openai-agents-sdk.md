# OpenAI Agents SDK

Source: https://docs.coreweave.com/products/agent-lens/integrations/openai-agents-sdk

# OpenAI Agents SDK

> Trace an agent built with the OpenAI Agents SDK using Agent Lens.

The OpenAI Agents SDK is a lightweight framework for building agents and multi-agent workflows on top of OpenAI's API. CoreWeave Agent Lens automatically traces agents built with the OpenAI Agents SDK, including each agent invocation, sub-agent handoff, model call, and tool call.

> [!NOTE]
>
> This integration uses the Weights & Biases Weave SDK (`weave`), because the CoreWeave Forge SDK doesn't support this framework yet. Traces you send with Weave appear in Agent Lens, because both products share the same trace data.

## Trace OpenAI Agents SDK agents with Agent Lens

> [tab] Python
>
> The Weave SDK autopatches the [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python) so you can capture traces from your agents with minimal setup. This guide explains how to initialize Weave and then run a multi-turn research agent built with the OpenAI Agents SDK so that Agent Lens captures every agent invocation, model call, and tool call across the session.
>
> ### Prerequisites
>
> Before you begin, make sure you have the following:
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * An [OpenAI API key](https://platform.openai.com/api-keys).
> * Python 3.10+.

> [tab] TypeScript
>
> The Weave SDK integrates with the [OpenAI Agents Node SDK](https://github.com/openai/openai-agents-js) (`@openai/agents`) to automatically trace your agent runs. Requires `@openai/agents` version `0.4.15` or later.
>
> ### Prerequisites
>
> Before you begin, make sure you have the following:
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * An [OpenAI API key](https://platform.openai.com/api-keys).
> * Node.js 18+.

### Install packages

Install the following packages in your developer environment so that Weave and the OpenAI Agents SDK are available to your script.

```bash Python theme={"system"}
pip install weave openai-agents requests
```

```bash TypeScript theme={"system"}
npm install weave @openai/agents zod
```

### Initialize Agent Lens in your code

> [tab] Python
>
> Add `weave.init` to the project, along with your Forge team and project names, and then build your agent as usual. The following code defines a `wikipedia_search` function tool and a `Research assistant` agent, then runs three questions through the OpenAI Agents SDK `Runner` while Agent Lens captures the trace. Each `Runner.run` call starts its own trace, so the example passes a `RunConfig` with a shared `group_id` on every call. Weave uses `group_id` to group traces from the same conversation, falling back to each trace's own ID when no `group_id` is set.
>
> ```python lines  highlight="7,33,42" theme={"system"}
> import asyncio
> import uuid
> import requests
> import weave
> from agents import Agent, RunConfig, Runner, function_tool
>
> weave.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> @function_tool
> def wikipedia_search(query: str) -> str:
>     """Search Wikipedia for a topic and return its title and intro paragraph."""
>     r = requests.get(
>         "https://en.wikipedia.org/w/api.php",
>         params={
>             "action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 1,
>             "prop": "extracts", "exintro": True, "explaintext": True, "format": "json",
>         },
>         headers={"User-Agent": "weave-demo"},
>     ).json()
>     page = next(iter(r["query"]["pages"].values()))
>     return f"{page['title']}: {page['extract']}"
>
> agent = Agent(
>     name="Research assistant",
>     instructions=(
>         "You are a research assistant. Use the wikipedia_search tool to look up "
>         "topics when needed, and cite the article titles you used."
>     ),
>     tools=[wikipedia_search],
> )
>
> async def main():
>     run_config = RunConfig(group_id=str(uuid.uuid4()))
>     history = []
>     for question in [
>         "Who founded Anthropic?",
>         "What is Claude (the AI assistant)?",
>         "Summarize what we discussed in one sentence.",
>     ]:
>         history.append({"role": "user", "content": question})
>         print(f"USER: {question}")
>         result = await Runner.run(agent, input=history, run_config=run_config)
>         print(f"AGENT: {result.final_output}\n")
>         history = result.to_input_list()
>
> asyncio.run(main())
> ```
>
> The example runs three turns in a single conversation. The first two turns trigger Wikipedia lookups, and the third uses the prior conversation context to produce a summary without a tool call. Each call to `Runner.run` continues the conversation by passing the previous result's input list back as the next request, and shares the same `group_id` so that Agent Lens groups all three turns into one conversation in the **Conversations** tab. Without a shared `group_id`, each turn falls back to its own trace ID and appears as a separate conversation.

> [tab] TypeScript
>
> Weave automatically instruments `@openai/agents` via module loader hooks when it is imported. The required setup differs slightly between module systems. For more background on CommonJS versus ESM and how Weave's loader hooks work, see the [TypeScript SDK third-party integration guide](https://docs.coreweave.com/products/wandb/weave/guides/integrations/js.md).
>
> * **CommonJS projects**: No extra configuration needed. Require `weave` before `@openai/agents` so auto-instrumentation runs first.
> * **ESM projects**: Start Node with the `--import=weave/instrument` flag so the instrumentation loads before any other modules.
>
> The following code defines a `wikipedia_search` tool and a `Research assistant` agent, then runs three questions through the SDK's `Runner` while Agent Lens captures the trace. Each `run()` call is traced as a separate top-level trace, so the example creates a `Runner` with a shared `groupId` and reuses it across all three calls. Agent Lens uses `groupId` to group traces from the same conversation, falling back to each trace's own ID when no `groupId` is set.
>
> ```typescript lines  highlight="33" title="main.mjs" theme={"system"}
> import { randomUUID } from "node:crypto";
> import * as weave from "weave";
> import { Agent, Runner, tool, type AgentInputItem } from "@openai/agents";
> import { z } from "zod";
>
> const wikipediaSearch = tool({
>     name: "wikipedia_search",
>     description: "Search Wikipedia for a topic and return its title and intro paragraph.",
>     parameters: z.object({
>     query: z.string().describe("The topic to search for"),
>     }),
>     async execute({ query }) {
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
>     return `${page.title}: ${page.extract}`;
>     },
> });
>
> async function main() {
>     await weave.init("[YOUR-TEAM]/[YOUR-PROJECT]");
>
>     const agent = new Agent({
>     name: "Research assistant",
>     instructions:
>         "You are a research assistant. Use the wikipedia_search tool to look up " +
>         "topics when needed, and cite the article titles you used.",
>     tools: [wikipediaSearch],
>     });
>
>     const runner = new Runner({ groupId: randomUUID() });
>
>     const questions = [
>     "Who founded Anthropic?",
>     "What is Claude (the AI assistant)?",
>     "Summarize what we discussed in one sentence.",
>     ];
>
>     let history: AgentInputItem[] = [];
>     for (const question of questions) {
>     history.push({ role: "user", content: question });
>     console.log(`USER: ${question}`);
>     const result = await runner.run(agent, history);
>     console.log(`AGENT: ${result.finalOutput}\n`);
>     history = result.history;
>     }
> }
>
> main();
> ```
>
> The example runs three turns in a single conversation. The first two turns trigger Wikipedia lookups, and the third uses the prior conversation context to produce a summary without a tool call. Each call to `runner.run` continues the conversation by passing the previous result's `history` back as the next input, and shares the same `groupId` so Agent Lens groups all three turns into one session in the Conversations tab.
>
> Save the example as `main.mjs` and run it with the `--import=weave/instrument` flag so the loader hook runs before any other module:
>
> ```bash theme={"system"}
> node --import=weave/instrument main.mjs
> ```
>
> ### Manual instrumentation
>
> Manual instrumentation is only needed when module loader hooks cannot run, such as when using a bundler that combines dependencies into a single file, in environments that don't support Node CLI flags, or with dynamic module loading patterns that bypass loader hooks.
>
> Use `instrumentOpenAIAgents()` to register instrumentation explicitly:
>
> ```typescript lines theme={"system"}
> import * as weave from "weave";
>
> await weave.init("[YOUR-TEAM]/[YOUR-PROJECT]");
> await weave.instrumentOpenAIAgents();
> ```
>
> If you need full control over the tracing processor, such as to configure a custom processor or register it conditionally, create and register it directly:
>
> ```typescript lines theme={"system"}
> import { addTraceProcessor } from "@openai/agents";
> import { createOpenAIAgentsTracingProcessor } from "weave";
>
> const processor = createOpenAIAgentsTracingProcessor();
> addTraceProcessor(processor);
> ```

### View your traces in Agent Lens

After the script runs, `weave.init()` prints a link to your project in Weave. The same traces appear in Agent Lens, because both products share the same trace data. To view them in Agent Lens:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com) and select **Agent Lens** from the product menu.
2. Select your project.
3. In the Agent Lens side menu, select **Conversations**, and then select your conversation.

Each turn renders as an `invoke_agent` span with nested `chat` and `execute_tool` spans. Each span shows its input, model, output, token usage, and tool results.

For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
