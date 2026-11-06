# Anthropic

Source: https://docs.coreweave.com/products/agent-lens/integrations/anthropic

# Anthropic

> Trace Anthropic SDK calls in Agent Lens with the CoreWeave Forge SDK.

The CoreWeave Forge SDK automatically traces calls you make with the Anthropic SDK for Python and Node.js. After you initialize tracing, each call you make inside a conversation is recorded in Agent Lens as an LLM span with its messages, tool calls, media, request settings, token usage, and prompt-cache usage. You don't change how you call the Anthropic SDK.

The integration traces the Messages API, including streaming, the Messages stream helper, and structured-output parsing. In TypeScript, it also traces Message Batches API calls as tool operations.

## Prerequisites

* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
* An [Anthropic API key](https://console.anthropic.com/settings/keys) set as an `ANTHROPIC_API_KEY` environment variable.
* For Python: Python 3.10 or later and `anthropic` 0.18.0 or later.
* For TypeScript: Node.js 18.19 or later (or 20.6 or later) and `@anthropic-ai/sdk` 0.52.0 or later.

## Install packages

```bash Python theme={"system"}
pip install "coreweave[anthropic]"
```

```bash TypeScript theme={"system"}
npm install @coreweave/forge-sdk @anthropic-ai/sdk
```

## Trace Anthropic conversations

Call `tracing.init()` with your Forge team and project names. In Python, `tracing.init()` patches the Anthropic SDK, whether you import it before or after the call. In TypeScript, start Node with the instrumentation flag shown in the TypeScript tab.

Agent Lens shows only calls that run inside a conversation. A call made outside a conversation has no conversation ID, so it doesn't appear in Agent Lens. Create one conversation for each agent session, and start a turn for each user message. Every turn shares the conversation's ID, so Agent Lens groups the turns into one conversation, and each call becomes an LLM span of the turn it runs in.

> [tab] Python
>
> ```python lines theme={"system"}
> from anthropic import Anthropic
> from coreweave.forge.agentlens import tracing
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
> client = Anthropic()
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
>             response = client.messages.create(
>                 model="claude-sonnet-5",
>                 max_tokens=256,
>                 messages=history,
>             )
>             answer = response.content[0].text
>             history.append({"role": "assistant", "content": answer})
>             print(answer)
>
> tracing.shutdown()
> ```

> [tab] TypeScript
>
> Wrap each agent run in `tracing.runIsolated()`, so that its conversation and turns stay separate from other concurrent runs.
>
> ```typescript lines title="app.mjs" theme={"system"}
> import Anthropic from '@anthropic-ai/sdk';
> import {tracing} from '@coreweave/forge-sdk/agentlens';
>
> await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
> const anthropic = new Anthropic();
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
>         const response = await anthropic.messages.create({
>           model: 'claude-sonnet-5',
>           max_tokens: 256,
>           messages: history,
>         });
>         const answer = response.content[0].text;
>         history.push({role: 'assistant', content: answer});
>         console.log(answer);
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
> Run the script with the instrumentation flag, which loads the Forge instrumentation before your code so that the Anthropic SDK is patched when your code imports it:
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
> const anthropic = integrations.wrapAnthropic(new Anthropic());
> ```
>
> When you run without the flag, `tracing.init()` prints a one-time warning about it. You can ignore the warning if you wrap your clients.

To add turns to an existing conversation later, such as in a web app that handles one turn per request, pass the same `conversation_id` (Python) or `conversationId` (TypeScript) each time you create the conversation.

For more about conversations, turns, and the other span types, see [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md).

## Turn off automatic patching

In Python, pass `autopatch_integrations=False` to `tracing.init()`. You can then patch and unpatch the Anthropic SDK yourself with `tracing.integrations.patch_anthropic()` and `tracing.integrations.unpatch_anthropic()`.

In TypeScript, run without the `--import=@coreweave/forge-sdk/instrument` flag, and wrap only the clients you want to trace with `integrations.wrapAnthropic()`.

## View your traces

In [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, select your project in the project selector at the top of the side menu, and then select **Conversations**. For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
