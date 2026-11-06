# Quickstart: Set up custom agent observability

Source: https://docs.coreweave.com/products/agent-lens/get-started/custom-agents

# Quickstart: Set up custom agent observability

> Instrument a custom agent with Agent Lens to capture existing OTel spans.

The CoreWeave Forge SDK lets you trace agents built with popular SDKs or custom harnesses. This quickstart shows you how to manually integrate CoreWeave Agent Lens into a custom-built multi-turn agent to emit and capture OpenTelemetry spans. For conceptual understanding about Agent Lens for agents, see [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md).

If you're looking to integrate Agent Lens with SDKs or harnesses such as the Claude Agent SDK or Codex, see [Choose an agent integration](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md) instead. Agent Lens autopatches into several agent-building SDKs and agent harnesses for quick integration.

## What you'll learn

By the end of this quickstart, you'll have a working multi-turn agent that emits Agent Lens-compatible OTel spans. You'll also understand how Agent Lens maps conversations, turns, LLM calls, and tool calls onto your agent code so you can apply the same pattern to your own custom agents.

The code in this guide sets up a small Python or TypeScript research agent that can look things up on Wikipedia. It asks three questions (three turns) and uses the LLM to choose when to search Wikipedia for an answer. Agent Lens records every step (the conversation, each question, each AI response, and each Wikipedia lookup) so you can see what happened in the Agent Lens Conversations tab.

This guide shows you how to:

* Initialize Agent Lens for agent tracing with `tracing.init()`.
* Open a conversation and a turn with `start_conversation` / `startConversation` and `start_turn` / `startTurn`.
* Wrap LLM calls with `start_llm` / `startLLM` and record usage.
* Wrap tool executions with `start_tool` / `startTool` and record results.
* Record complete token usage and a priceable model so token counts and cost render.
* View the resulting conversation, turns, and tool calls in the Conversations tab.

## How the Agent Lens SDK works with agents

The Agent Lens SDK includes a generic OTel ingest system for agents, meaning that Agent Lens can capture information from any OTel span in your agent's code. However, Agent Lens requires special handling of the following spans to render your agent's traces in the Conversations tab of the Agent Lens UI.

| Concept | Python | TypeScript | OTel span |
| - | - | - | - |
| A conversation | `tracing.start_conversation(...)` | `tracing.startConversation(...)` | (no span, groups turns) |
| One user or agent exchange | `tracing.start_turn(...)` | `tracing.startTurn(...)` | `invoke_agent` |
| One LLM API call | `tracing.start_llm(...)` | `tracing.startLLM(...)` | `chat` |
| One tool execution | `tracing.start_tool(...)` | `tracing.startTool(...)` | `execute_tool` |

In Python, all four functions work as context managers (`with tracing.start_*(...) as obj:`). On exit, they end the span and flush attributes, including on exceptions. In TypeScript, call `.end()` on each returned object. Use `try { ... } finally { obj.end(); }` to guarantee cleanup on exceptions, and wrap each agent run in `tracing.runIsolated()` so that concurrent runs don't share a conversation.

Other [GenAI semantic-convention attributes](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md), such as `gen_ai.usage.*` and `gen_ai.agent.name`, enable additional rendering, but they're optional.

## Prerequisites

* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys).
* An OpenAI API key.
* Python 3.9+ (for the Python examples).
* Node.js 18+ and a TypeScript runner such as `tsx` (the TypeScript examples require built-in `fetch` and aren't plain JavaScript).

## Install packages

Install the following packages into your developer environment:

```bash Python theme={"system"}
pip install coreweave openai requests
```

```bash TypeScript theme={"system"}
npm install @coreweave/forge-sdk openai
npm install --save-dev tsx
```

Save the TypeScript examples as `.mts` files and run them with `npx tsx [FILENAME].mts`.

## Initialize Agent Lens

`tracing.init()` authenticates with your API key and configures the OTel exporter that sends agent spans to Agent Lens. The project name must include your team. The SDK reads the API key from the `WANDB_API_KEY` environment variable, or you can pass it as the `api_key` / `apiKey` argument.

```python lines Python theme={"system"}
import getpass
import os

os.environ["WANDB_API_KEY"] = getpass.getpass("Enter your API key: ")
os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

TEAM = input("Enter your team name: ")
PROJECT = input("Enter your project name: ")

from coreweave.forge.agentlens import tracing
tracing.init(f"{TEAM}/{PROJECT}", autopatch_integrations=False)
```

```typescript lines highlight="" TypeScript theme={"system"}
// Set WANDB_API_KEY and OPENAI_API_KEY in your environment before running this project
import { tracing } from '@coreweave/forge-sdk/agentlens';

await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
```

## Define a tool

The following code defines the agent's Wikipedia search tool along with an OpenAI tool schema that specifies when and how to use the tool.

```python lines Python theme={"system"}
import json
import requests

def wikipedia_search(query: str) -> str:
    r = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 1,
            "prop": "extracts", "exintro": True, "explaintext": True, "format": "json",
        },
        headers={"User-Agent": "agent-lens-demo"},
    ).json()
    return next(iter(r["query"]["pages"].values()))["extract"]

wikipedia_tool_schema = {
    "type": "function",
    "function": {
        "name": "wikipedia_search",
        "description": "Search Wikipedia for a topic and return its intro paragraph.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}
```

```typescript lines TypeScript theme={"system"}
async function wikipediaSearch(query: string): Promise<string> {
  const url = new URL('https://en.wikipedia.org/w/api.php');
  url.search = new URLSearchParams({
    action: 'query',
    generator: 'search',
    gsrsearch: query,
    gsrlimit: '1',
    prop: 'extracts',
    exintro: 'true',
    explaintext: 'true',
    format: 'json',
  }).toString();
  const res = await fetch(url, { headers: { 'User-Agent': 'agent-lens-demo' } });
  const data = (await res.json()) as {
    query: { pages: Record<string, { extract: string }> };
  };
  return Object.values(data.query.pages)[0].extract;
}

const wikipediaToolSchema = {
  type: 'function' as const,
  function: {
    name: 'wikipedia_search',
    description: 'Search Wikipedia for a topic and return its intro paragraph.',
    parameters: {
      type: 'object',
      properties: { query: { type: 'string' } },
      required: ['query'],
    },
  },
};
```

## Run a traced multi-turn agent

With the tool and Agent Lens initialization in place, the next step combines them into a complete agent loop. This loop shows how conversations, turns, LLM calls, and tool calls nest together.

The following example runs three turns in a single conversation. Each turn:

1. Opens a `chat` span and lets the LLM choose whether to call the tool.
2. If the LLM requests a tool, opens an `execute_tool` span around the call and feeds the result back to the LLM.
3. Opens a second `chat` span to produce the final answer.

> [!NOTE]
>
> The Agent Lens SDK automatically traces calls made with the OpenAI, Anthropic, and Google Gen AI client libraries. This quickstart records each LLM call by hand with `start_llm()` to show how the spans fit together, so it passes `autopatch_integrations=False` to `init()`. Without it, each call is recorded twice: once by your `start_llm()` span and once by the automatic integration. Pass the argument on your first `init()` call, because a later call with `autopatch_integrations=False` doesn't remove patches that an earlier call applied. In your own code, either let autopatching record your LLM calls, or turn it off and record them yourself.

```python lines Python theme={"system"}
from coreweave.forge.agentlens import tracing
from openai import OpenAI

openai_client = OpenAI()
MODEL = "gpt-4o-mini"

def run_turn(history, user_message):
    history.append({"role": "user", "content": user_message})

    with tracing.start_turn(user_message=user_message, model=MODEL):
        # LLM call 1: the model might decide to use a tool.
        with tracing.start_llm(model=MODEL, provider_name="openai") as llm:
            resp = openai_client.chat.completions.create(
                model=MODEL, messages=history, tools=[wikipedia_tool_schema],
            )
            msg = resp.choices[0].message
            llm.output(msg.content or "")
            # record() sets usage, the priced model, and response id in one call.
            llm.record(
                usage=tracing.Usage(
                    input_tokens=resp.usage.prompt_tokens,
                    output_tokens=resp.usage.completion_tokens,
                    cache_read_input_tokens=getattr(
                        resp.usage.prompt_tokens_details, "cached_tokens", 0
                    ),
                ),
                response_id=resp.id,
                response_model=resp.model,
            )
            history.append(msg.model_dump(exclude_none=True))

        # If no tool was requested, the first LLM response is the answer.
        if not msg.tool_calls:
            return msg.content

        # Execute each requested tool call.
        for tc in msg.tool_calls:
            with tracing.start_tool(
                name=tc.function.name,
                arguments=tc.function.arguments,
                tool_call_id=tc.id,
            ) as tool:
                tool.result = wikipedia_search(**json.loads(tc.function.arguments))
                history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": tool.result,
                })

        # LLM call 2: synthesize the final answer.
        with tracing.start_llm(model=MODEL, provider_name="openai") as llm:
            resp = openai_client.chat.completions.create(model=MODEL, messages=history)
            msg = resp.choices[0].message
            llm.output(msg.content)
            llm.record(
                usage=tracing.Usage(
                    input_tokens=resp.usage.prompt_tokens,
                    output_tokens=resp.usage.completion_tokens,
                    cache_read_input_tokens=getattr(
                        resp.usage.prompt_tokens_details, "cached_tokens", 0
                    ),
                ),
                response_id=resp.id,
                response_model=resp.model,
            )
            history.append({"role": "assistant", "content": msg.content})
            return msg.content

tracing.init(f"{TEAM}/{PROJECT}", autopatch_integrations=False)

with tracing.start_conversation(agent_name="research-bot") as conversation:
    history = []
    for question in [
        "Who founded Anthropic?",
        "What is Claude (the AI assistant)?",
        "Summarize what we discussed in one sentence.",
    ]:
        print(f"USER: {question}")
        print(f"AGENT: {run_turn(history, question)}\n")

tracing.shutdown()
```

```typescript lines TypeScript theme={"system"}
import { tracing } from '@coreweave/forge-sdk/agentlens';
import OpenAI from 'openai';

const openaiClient = new OpenAI();
const MODEL = 'gpt-4o-mini';

// history is a list of OpenAI chat messages; typed loosely for brevity.
async function runTurn(history: any[], userMessage: string): Promise<string | null> {
  history.push({ role: 'user', content: userMessage });

  const turn = tracing.startTurn({ userMessage, model: MODEL });
  try {
    // LLM call 1: the model might decide to use a tool.
    const llm1 = tracing.startLLM({ model: MODEL, providerName: 'openai' });
    let msg;
    try {
      const resp = await openaiClient.chat.completions.create({
        model: MODEL,
        messages: history,
        tools: [wikipediaToolSchema],
      });
      msg = resp.choices[0].message;
      llm1.output(msg.content ?? '');
      // record() sets usage, the priced model, and response id in one call.
      llm1.record({
        usage: {
          inputTokens: resp.usage?.prompt_tokens,
          outputTokens: resp.usage?.completion_tokens,
          cacheReadInputTokens: resp.usage?.prompt_tokens_details?.cached_tokens,
        },
        responseId: resp.id,
        responseModel: resp.model,
      });
      history.push(msg);
    } finally {
      llm1.end();
    }

    // If no tool was requested, the first LLM response is the answer.
    if (!msg.tool_calls?.length) {
      return msg.content ?? null;
    }

    // Execute each requested tool call.
    for (const tc of msg.tool_calls) {
      if (tc.type !== 'function') continue;
      const tool = tracing.startTool({
        name: tc.function.name,
        args: tc.function.arguments,
        toolCallId: tc.id,
      });
      try {
        const { query } = JSON.parse(tc.function.arguments);
        tool.result = await wikipediaSearch(query);
        history.push({ role: 'tool', tool_call_id: tc.id, content: tool.result });
      } finally {
        tool.end();
      }
    }

    // LLM call 2: synthesize the final answer.
    const llm2 = tracing.startLLM({ model: MODEL, providerName: 'openai' });
    try {
      const resp = await openaiClient.chat.completions.create({
        model: MODEL,
        messages: history,
      });
      const msg2 = resp.choices[0].message;
      llm2.output(msg2.content ?? '');
      llm2.record({
        usage: {
          inputTokens: resp.usage?.prompt_tokens,
          outputTokens: resp.usage?.completion_tokens,
          cacheReadInputTokens: resp.usage?.prompt_tokens_details?.cached_tokens,
        },
        responseId: resp.id,
        responseModel: resp.model,
      });
      history.push({ role: 'assistant', content: msg2.content });
      return msg2.content ?? null;
    } finally {
      llm2.end();
    }
  } finally {
    turn.end();
  }
}

await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');

await tracing.runIsolated(async () => {
  const conversation = tracing.startConversation({ agentName: 'research-bot' });
  try {
    const history: any[] = [];
    for (const question of [
      'Who founded Anthropic?',
      'What is Claude (the AI assistant)?',
      'Summarize what we discussed in one sentence.',
    ]) {
      console.log(`USER: ${question}`);
      console.log(`AGENT: ${await runTurn(history, question)}\n`);
    }
  } finally {
    conversation.end();
  }
});

await tracing.shutdown();
```

## Record token usage and cost

Each `chat` span carries token usage and a model ID. Agent Lens renders token counts from usage and derives cost from usage plus the model ID, so an incomplete or unpriceable value shows `0 in / 0 out` tokens or `Cost -` even when the rest of the trace looks correct. `record(...)` sets these fields (along with `output_messages`, `response_id`, `reasoning`, and more) in one call. Only the fields you pass are applied.

Two things must be right for cost to appear:

* **Complete usage.** `input_tokens` is the *total* input, including any cached tokens. Agent Lens prices cache reads and cache writes at their own rates and subtracts them from the input total, so `cache_read_input_tokens` and `cache_creation_input_tokens` must be reported *in addition to* a total `input_tokens` that includes them. For providers with prompt caching (for example, Anthropic), cached tokens routinely dominate the input, so omitting them makes usage and cost render as roughly zero.
* **A priceable model ID.** Pass the concrete ID the response returns (`resp.model`) as `response_model`. Cost is a lookup on the model. Agent Lens prefers `response_model` (the exact model the provider served) and falls back to the `model` you passed to `start_llm`. An alias such as `opus` or `sonnet` is not priceable and renders `Cost -`.

OpenAI counts cached tokens inside `prompt_tokens`, so the example above maps directly. Anthropic reports cached tokens *separately* from `input_tokens`, so add them back into the total Agent Lens prices against:

```python lines Python theme={"system"}
with tracing.start_llm(model=MODEL, provider_name="anthropic") as llm:
    resp = anthropic_client.messages.create(
        model=MODEL, max_tokens=1024, messages=history,
    )
    u = resp.usage
    llm.output(resp.content[0].text)
    llm.record(
        usage=tracing.Usage(
            input_tokens=u.input_tokens
            + u.cache_read_input_tokens
            + u.cache_creation_input_tokens,
            output_tokens=u.output_tokens,
            cache_read_input_tokens=u.cache_read_input_tokens,
            cache_creation_input_tokens=u.cache_creation_input_tokens,
        ),
        response_id=resp.id,
        response_model=resp.model,
    )
```

```typescript lines TypeScript theme={"system"}
const u = resp.usage;
llm.record({
  usage: {
    inputTokens:
      u.input_tokens + u.cache_read_input_tokens + u.cache_creation_input_tokens,
    outputTokens: u.output_tokens,
    cacheReadInputTokens: u.cache_read_input_tokens,
    cacheCreationInputTokens: u.cache_creation_input_tokens,
  },
  responseId: resp.id,
  responseModel: resp.model,
});
```

## See your agent traces in the Conversations tab

Open your project in Agent Lens and select **Conversations**. You'll see:

* One conversation for `research-bot` containing three turns.
* Each turn (`invoke_agent`) with two `chat` spans and an `execute_tool` span nested inside.
* Token counts, latency, model, and the full message exchange on each `chat`.

Select the conversation to inspect the inputs, outputs, tool arguments, and tool results on the **Thread** and **Spans** tabs.

## Link to a conversation from your app

To deep-link from your own UI to a conversation in Agent Lens, you need the conversation's ID. `start_conversation` / `startConversation` exposes it as `conversation_id` / `conversationId`, so you can log it or store it alongside your own request ID and open the conversation later from the **Conversations** tab.

```python lines Python theme={"system"}
with tracing.start_conversation(agent_name="research-bot") as conversation:
    # ... run turns ...
    print(f"Agent Lens conversation ID: {conversation.conversation_id}")
```

```typescript lines TypeScript theme={"system"}
await tracing.runIsolated(async () => {
  const conversation = tracing.startConversation({ agentName: 'research-bot' });
  try {
    // ... run turns ...
    console.log(`Agent Lens conversation ID: ${conversation.conversationId}`);
  } finally {
    conversation.end();
  }
});
```

## Next steps

* Learn how to [trace agents with Agent Lens](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md) and what features and options are available in the Agent Lens SDK.
* See [Choose an agent integration](https://docs.coreweave.com/products/agent-lens/get-started/integrations.md) for more options about how to integrate Agent Lens with your agents.
