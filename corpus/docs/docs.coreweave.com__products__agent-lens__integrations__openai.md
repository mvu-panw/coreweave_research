# OpenAI

Source: https://docs.coreweave.com/products/agent-lens/integrations/openai

# OpenAI

> Trace OpenAI SDK calls in Agent Lens with the CoreWeave Forge SDK.

The CoreWeave Forge SDK automatically traces calls you make with the OpenAI SDK for Python and Node.js. After you initialize tracing, each call you make inside a conversation is recorded in Agent Lens as an LLM span with its messages, tool calls, request settings, and token usage, including cached and reasoning tokens. You don't change how you call the OpenAI SDK.

The integration traces Chat Completions (including streaming), structured-output parsing, the Responses API (including streaming), and image generation.

## Prerequisites

* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an `OPENAI_API_KEY` environment variable.
* For Python: Python 3.10 or later and `openai` 1.99.9 or later.
* For TypeScript: Node.js 18.19 or later (or 20.6 or later) and `openai` 4.0.0 or later.

## Install packages

```bash Python theme={"system"}
pip install "coreweave[openai]"
```

```bash TypeScript theme={"system"}
npm install @coreweave/forge-sdk openai
```

## Trace OpenAI conversations

Call `tracing.init()` with your Forge team and project names. In Python, `tracing.init()` patches the OpenAI SDK, whether you import it before or after the call. In TypeScript, start Node with the instrumentation flag shown in the TypeScript tab.

Agent Lens shows only calls that run inside a conversation. A call made outside a conversation has no conversation ID, so it doesn't appear in Agent Lens. Create one conversation for each agent session, and start a turn for each user message. Every turn shares the conversation's ID, so Agent Lens groups the turns into one conversation, and each call becomes an LLM span of the turn it runs in.

> [tab] Python
>
> ```python lines theme={"system"}
> from openai import OpenAI
> from coreweave.forge.agentlens import tracing
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
> client = OpenAI()
>
> questions = [
>     "What is inference latency?",
>     "How does batching affect it?",
>     "Summarize what we discussed in one sentence.",
> ]
>
> history = []
> with tracing.Conversation(agent_name="support-agent") as conversation:
>     for question in questions:
>         with conversation.start_turn(user_message=question):
>             history.append({"role": "user", "content": question})
>             response = client.responses.create(model="gpt-5-mini", input=history)
>             history.append({"role": "assistant", "content": response.output_text})
>             print(response.output_text)
>
> tracing.shutdown()
> ```

> [tab] TypeScript
>
> Wrap each agent run in `tracing.runIsolated()`, so that its conversation and turns stay separate from other concurrent runs.
>
> ```typescript lines title="app.mjs" theme={"system"}
> import OpenAI from 'openai';
> import {tracing} from '@coreweave/forge-sdk/agentlens';
>
> await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
> const openai = new OpenAI();
>
> const questions = [
>   'What is inference latency?',
>   'How does batching affect it?',
>   'Summarize what we discussed in one sentence.',
> ];
>
> await tracing.runIsolated(async () => {
>   const conversation = tracing.startConversation({agentName: 'support-agent'});
>   const history = [];
>   try {
>     for (const question of questions) {
>       const turn = conversation.startTurn({userMessage: question});
>       try {
>         history.push({role: 'user', content: question});
>         const response = await openai.responses.create({model: 'gpt-5-mini', input: history});
>         history.push({role: 'assistant', content: response.output_text});
>         console.log(response.output_text);
>       } finally {
>         turn.end();
>       }
>     }
>   } finally {
>     conversation.end();
>   }
> });
>
> await tracing.shutdown();
> ```
>
> Run the script with the instrumentation flag, which loads the Forge instrumentation before your code so that the OpenAI SDK is patched when your code imports it:
>
> ```bash theme={"system"}
> node --import=@coreweave/forge-sdk/instrument app.mjs
> ```
>
> If you can't use the flag, for example because a bundler combines your dependencies into one file, wrap the client instead:
>
> ```typescript theme={"system"}
> import {integrations} from '@coreweave/forge-sdk/agentlens';
>
> const openai = integrations.wrapOpenAI(new OpenAI());
> ```
>
> When you run without the flag, `tracing.init()` prints a one-time warning about it. You can ignore the warning if you wrap your clients.

To add turns to an existing conversation later, such as in a web app that handles one turn per request, pass the same `conversation_id` (Python) or `conversationId` (TypeScript) each time you create the conversation.

For more about conversations, turns, and the other span types, see [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md).

## Turn off automatic patching

In Python, pass `autopatch_integrations=False` to `tracing.init()`. You can then patch and unpatch the OpenAI SDK yourself with `tracing.integrations.patch_openai()` and `tracing.integrations.unpatch_openai()`.

In TypeScript, run without the `--import=@coreweave/forge-sdk/instrument` flag, and wrap only the clients you want to trace with `integrations.wrapOpenAI()`.

## View your traces

In [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, select your project in the project selector at the top of the side menu, and then select **Conversations**. For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
