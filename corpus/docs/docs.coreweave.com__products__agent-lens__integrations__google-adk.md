# Google ADK

Source: https://docs.coreweave.com/products/agent-lens/integrations/google-adk

# Google ADK

> Trace an agent built with Google's Agent Development Kit (ADK) using Agent Lens.

Google's Agent Development Kit (ADK) is a flexible, model-agnostic framework for building and orchestrating agents. While optimized for Gemini, ADK supports any model and both simple tasks and complex multi-agent workflows. CoreWeave Agent Lens automatically traces agents built with ADK, including each agent invocation, sub-agent handoff, model call, and tool call. Agent Lens displays the captured data in the **Conversations** tab of your project.

> [!NOTE]
>
> This integration uses the Weights & Biases Weave SDK (`weave`), because the CoreWeave Forge SDK doesn't support this framework yet. Traces you send with Weave appear in Agent Lens, because both products share the same trace data.

## Trace Google ADK agents with Agent Lens

> [tab] Python
>
> The Weave SDK autopatches [Google ADK for Python](https://google.github.io/adk-docs/) so you can capture traces from your ADK agents with minimal setup. This guide shows how to initialize Weave and then run a multi-turn research agent built with Google ADK so that Agent Lens captures every agent invocation, model call, and tool call across the session.
>
> ### Prerequisites
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * A [Google API key](https://aistudio.google.com/apikey) for Gemini.
> * Python 3.10+.

> [tab] TypeScript
>
> The Weave SDK integrates with [Google ADK for Node.js](https://google.github.io/adk-docs/) (`@google/adk`) to automatically trace your agent runs.
>
> ### Prerequisites
>
> * A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
> * A [Google API key](https://aistudio.google.com/apikey) set as a `GEMINI_API_KEY` or `GOOGLE_GENAI_API_KEY` environment variable.
> * Node.js 18+.
> * `@google/adk` version `1.0.0` or later.

### Install packages

Install the following packages in your developer environment. These provide the Weave SDK, the Google ADK framework, and the HTTP client used by the example tool.

```bash Python theme={"system"}
pip install weave google-adk requests
```

```bash TypeScript theme={"system"}
npm install weave @google/adk zod
```

### Initialize Agent Lens in your code

> [tab] Python
>
> Add `weave.init` to the project, along with your Forge team and project names, and then build an agent the way you normally would. The following code creates a `research_assistant` agent that uses `gemini-3.6-flash` and a `wikipedia_search` tool, then runs three questions through a single ADK session while Agent Lens captures the trace.
>
> ```python lines highlight="8" theme={"system"}
> import asyncio
> import requests
> import weave
> from google.adk.agents import Agent
> from google.adk.runners import InMemoryRunner
> from google.genai import types
>
> weave.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> def wikipedia_search(query: str) -> dict:
>     """Search Wikipedia for a topic and return its title and intro paragraph.
>
>     Args:
>         query: The topic to search for.
>
>     Returns:
>         A dictionary with the article title and intro extract.
>     """
>     r = requests.get(
>         "https://en.wikipedia.org/w/api.php",
>         params={
>             "action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 1,
>             "prop": "extracts", "exintro": True, "explaintext": True, "format": "json",
>         },
>         headers={"User-Agent": "weave-demo"},
>     ).json()
>     page = next(iter(r["query"]["pages"].values()))
>     return {"title": page["title"], "extract": page["extract"]}
>
> agent = Agent(
>     name="research_assistant",
>     model="gemini-3.6-flash",
>     instruction=(
>         "You are a research assistant. Use the wikipedia_search tool to look up "
>         "topics when needed, and cite the article titles you used."
>     ),
>     tools=[wikipedia_search],
> )
>
> async def main():
>     runner = InMemoryRunner(agent=agent, app_name="research-app")
>     session = await runner.session_service.create_session(
>         app_name="research-app", user_id="user-1"
>     )
>
>     questions = [
>         "Who founded Anthropic?",
>         "What is Claude (the AI assistant)?",
>         "Summarize what we discussed in one sentence.",
>     ]
>
>     for question in questions:
>         print(f"USER: {question}")
>         async for event in runner.run_async(
>             user_id="user-1",
>             session_id=session.id,
>             new_message=types.Content(
>                 role="user",
>                 parts=[types.Part(text=question)],
>             ),
>         ):
>             if event.is_final_response() and event.content:
>                 print(f"AGENT: {event.content.parts[0].text}\n")
>
> asyncio.run(main())
> ```
>
> The example runs three turns in a single ADK session. The first two turns trigger Wikipedia lookups, and the third uses the previous conversation context to produce a summary without a tool call.
>
> Every turn passes the same `session_id`. ADK sets `gen_ai.conversation.id` from that session, so Agent Lens renders the three turns as one conversation in the **Conversations** tab. If you create a session per turn instead, each turn appears as a separate conversation.

> [tab] TypeScript
>
> Weave traces `@google/adk` runners through the `WeaveAdkPlugin`, which you register directly on the runner's `plugins` array. Registering the plugin explicitly works the same way in ESM and CommonJS projects, so no module loader hook setup is required.
>
> The following code creates a `research_assistant` agent with a `wikipedia_search` tool, then runs three questions through a single ADK session while Agent Lens captures the trace.
>
> ```typescript lines highlight="35" theme={"system"}
> import * as weave from "weave";
> import { FunctionTool, Gemini, InMemoryRunner, LlmAgent } from "@google/adk";
> import { WeaveAdkPlugin } from "weave";
> import { z } from "zod";
>
> const GEMINI_API_KEY = process.env.GEMINI_API_KEY
>
> const wikipediaSearchTool = new FunctionTool({
>   name: "wikipedia_search",
>   description: "Search Wikipedia for a topic and return its title and intro paragraph.",
>   parameters: z.object({
>     query: z.string().describe("The topic to search for"),
>   }),
>   execute: async ({ query }) => {
>     const url = new URL("https://en.wikipedia.org/w/api.php");
>     url.search = new URLSearchParams({
>       action: "query",
>       generator: "search",
>       gsrsearch: query,
>       gsrlimit: "1",
>       prop: "extracts",
>       exintro: "true",
>       explaintext: "true",
>       format: "json",
>     }).toString();
>
>     const response = await fetch(url, { headers: { "User-Agent": "weave-demo" } });
>     const data = await response.json();
>     const page = Object.values(data.query.pages)[0] as { title: string; extract: string };
>     return { title: page.title, extract: page.extract };
>   },
> });
>
> async function main() {
>   await weave.init("[YOUR-TEAM]/[YOUR-PROJECT]");
>
>   const agent = new LlmAgent({
>     name: "research_assistant",
>     description: "Answers research questions using Wikipedia.",
>     instruction:
>       "You are a research assistant. Use the wikipedia_search tool to look up " +
>       "topics when needed, and cite the article titles you used.",
>     model: new Gemini({ model: "gemini-3.6-flash", apiKey: GEMINI_API_KEY }),
>     tools: [wikipediaSearchTool],
>   });
>
>   const APP_NAME = "weave-adk-example";
>   const USER_ID = "example-user";
>
>   const runner = new InMemoryRunner({
>     agent,
>     appName: APP_NAME,
>     plugins: [new WeaveAdkPlugin()],
>   });
>   const session = await runner.sessionService.createSession({
>     appName: APP_NAME,
>     userId: USER_ID,
>   });
>
>   const questions = [
>     "Who founded Anthropic?",
>     "What is Claude (the AI assistant)?",
>     "Summarize what we discussed in one sentence.",
>   ];
>
>   for (const question of questions) {
>     console.log(`USER: ${question}`);
>     for await (const event of runner.runAsync({
>       userId: USER_ID,
>       sessionId: session.id,
>       newMessage: {
>         role: "user",
>         parts: [{ text: question }],
>       },
>     })) {
>       const text = event.content?.parts
>         ?.map(part => part.text)
>         .filter(Boolean)
>         .join("");
>       if (text) {
>         console.log(`AGENT: ${text}\n`);
>       }
>     }
>   }
>
>   await weave.flushOTel();
> }
>
> main().catch(console.error);
> ```
>
> The example runs three turns in a single ADK session. The first two turns trigger Wikipedia lookups, and the third uses the previous conversation context to produce a summary without a tool call.
>
> Every turn passes the same `sessionId`. ADK sets `gen_ai.conversation.id` from that session, so Agent Lens renders the three turns as one conversation in the **Conversations** tab. If you create a session per turn instead, each turn appears as a separate conversation.

### View your traces in Agent Lens

After the script runs, `weave.init()` prints a link to your project in Weave. The same traces appear in Agent Lens, because both products share the same trace data. To view them in Agent Lens:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com) and select **Agent Lens** from the product menu.
2. Select your project.
3. In the Agent Lens side menu, select **Conversations**, and then select your conversation.

Each turn renders as an `invoke_agent` span with nested `chat` and `execute_tool` spans. Each span shows its input, model, output, token usage, and tool results.

For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
