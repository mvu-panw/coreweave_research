# TypeScript SDK

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk

# TypeScript SDK

> Reference for the Agent Lens tracing and provider integration APIs in @coreweave/forge-sdk.

The Agent Lens TypeScript SDK is part of the CoreWeave Forge SDK package, `@coreweave/forge-sdk`. It records conversations, turns, LLM calls, tool calls, and sub-agent calls from a Node.js agent and sends them to Agent Lens.

The package requires Node.js 18.19 or later in the 18.x line, or Node.js 20.6 or later.

## Install and import

```bash theme={"system"}
npm install @coreweave/forge-sdk
```

Import the `tracing` and `integrations` namespaces from `@coreweave/forge-sdk/agentlens`:

```typescript theme={"system"}
import {tracing, integrations} from '@coreweave/forge-sdk/agentlens';
```

The same APIs are also available from the `@coreweave/forge-sdk/agentlens/tracing` and `@coreweave/forge-sdk/agentlens/integrations` entry points.

## Before you trace

* [`tracing.init()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/init) takes an `entity/project` name and reads your API key from the `WANDB_API_KEY` environment variable unless you pass `apiKey`.
* Wrap every request or agent run in [`tracing.runIsolated()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/runisolated). Tracing state is scoped to that callback, including across `await`, and the `start*()` functions throw when no scope is active.
* To trace OpenAI, Anthropic, or Google Gen AI calls automatically, start Node.js with the SDK's preload, or wrap each client with a `wrap*()` function from [Integrations](#integrations):

  ```bash theme={"system"}
  node --import=@coreweave/forge-sdk/instrument app.mjs
  ```

```typescript theme={"system"}
import {tracing} from '@coreweave/forge-sdk/agentlens';

await tracing.init('[ENTITY]/[PROJECT]');

await tracing.runIsolated(async () => {
  const conversation = tracing.startConversation({agentName: 'research-agent'});
  const turn = conversation.startTurn({userMessage: 'What is the weather in Tokyo?'});
  try {
    // Call your model and tools here.
  } finally {
    turn.end();
    conversation.end();
  }
});

await tracing.shutdown();
```

## Functions

* [`endConversation()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endconversation): End the current Conversation.
* [`endLLM()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endllm): End the current LLM.
* [`endTurn()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endturn): End the current Turn.
* [`forceFlush()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/forceflush)
* [`getCurrentConversation()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/getcurrentconversation)
* [`getCurrentLLM()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/getcurrentllm)
* [`getCurrentTurn()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/getcurrentturn)
* [`init()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/init)
* [`runIsolated()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/runisolated): Give one request or agent run its own tracing state, including across awaits.
* [`shutdown()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/shutdown)
* [`startConversation()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startconversation): Start a new Conversation and install it as the current conversation.
* [`startLLM()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startllm): Start an LLM span as a child of the current Turn.
* [`startSubagent()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startsubagent): Start a SubAgent span.
* [`startTool()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/starttool): Start a Tool span.
* [`startTurn()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startturn): Start a new Turn.

## Classes

* [`Conversation`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/conversation): A Conversation groups Turns under a single gen\_ai.conversation.id.
* [`LLM`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm): An LLM call.
* [`SubAgent`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent)
* [`Tool`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool): A tool invocation.
* [`Turn`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/turn): An agent invocation.

## Interfaces

* [`ConversationInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/conversationinit)
* [`LLMInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/llminit)
* [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)
* [`Reasoning`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/reasoning)
* [`SubAgentInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/subagentinit)
* [`ToolEndOptions`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolendoptions)
* [`ToolInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolinit)
* [`TracingInitOptions`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/tracinginitoptions)
* [`TurnInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/turninit)
* [`Usage`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/usage)

## Type aliases

* [`JsonObject`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/jsonobject): An object whose properties are representable in JSON.
* [`JsonValue`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/jsonvalue): A value representable in JSON.
* [`MessagePart`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/messagepart): A message part in the GenAI semconv parts model.
* [`Modality`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/modality)
* [`Role`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/role)

## Integrations

* [`instrumentAnthropic()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/instrumentanthropic)
* [`instrumentGoogleGenAI()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/instrumentgooglegenai): Register automatic ESM and CommonJS instrumentation for @google/genai.
* [`instrumentOpenAI()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/instrumentopenai)
* [`patchAnthropicModule()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/patchanthropicmodule): Apply the Anthropic integration to an ESM module namespace.
* [`patchGoogleGenAIModule()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/patchgooglegenaimodule): Apply the Google Gen AI integration to an ESM or CommonJS namespace.
* [`patchOpenAIModule()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/patchopenaimodule): Apply the OpenAI integration to an ESM module namespace.
* [`wrapAnthropic()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapanthropic): Wrap an Anthropic client explicitly.
* [`wrapGoogleGenAI()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapgooglegenai): Wrap a Google Gen AI client explicitly.
* [`wrapOpenAI()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapopenai): Wrap an OpenAI client explicitly.
