# Google Gen AI

Source: https://docs.coreweave.com/products/agent-lens/integrations/google-genai

# Google Gen AI

> Trace Google Gen AI SDK calls to Gemini in Agent Lens with the CoreWeave Forge SDK.

The CoreWeave Forge SDK automatically traces calls you make with the Google Gen AI SDK for Python (`google-genai`) and Node.js (`@google/genai`). After you initialize tracing, each call you make inside a conversation is recorded in Agent Lens as an LLM span with its messages, system instructions, tools, media, request settings, response metadata, and token usage, including cached input and thinking tokens. You don't change how you call the Google Gen AI SDK.

The integration traces content generation (including streaming), chat helpers, and Imagen image generation. Calls through a Vertex AI client are attributed to `vertex_ai`, and Gemini Developer API calls are attributed to `gemini`.

> [!NOTE]
>
> To trace agents built with Google's Agent Development Kit (ADK), see [Google ADK](https://docs.coreweave.com/products/agent-lens/integrations/google-adk.md).

## Prerequisites

* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.
* A [Gemini API key](https://aistudio.google.com/apikey) set as a `GEMINI_API_KEY` environment variable.
* For Python: Python 3.10 or later and `google-genai` 1.0.0 through 1.23.0.
* For TypeScript: Node.js 18.19 or later (or 20.6 or later) and `@google/genai` 0.2.0 or later.

## Install packages

```bash Python theme={"system"}
pip install "coreweave[google-genai]"
```

```bash TypeScript theme={"system"}
npm install @coreweave/forge-sdk @google/genai
```

## Trace Google Gen AI conversations

Call `tracing.init()` with your Forge team and project names. In Python, `tracing.init()` patches the Google Gen AI SDK, whether you import it before or after the call. In TypeScript, start Node with the instrumentation flag shown in the TypeScript tab.

Agent Lens shows only calls that run inside a conversation. A call made outside a conversation has no conversation ID, so it doesn't appear in Agent Lens. Create one conversation for each agent session, and start a turn for each user message. Every turn shares the conversation's ID, so Agent Lens groups the turns into one conversation, and each call becomes an LLM span of the turn it runs in.

> [tab] Python
>
> ```python lines theme={"system"}
> from google import genai
> from coreweave.forge.agentlens import tracing
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
> client = genai.Client()
>
> questions = [
>     "What is inference latency?",
>     "How does batching affect it?",
>     "Summarize what we discussed in one sentence.",
> ]
>
> chat = client.chats.create(model="gemini-flash-latest")
> with tracing.Conversation(agent_name="support-agent") as conversation:
>     for question in questions:
>         with conversation.start_turn(user_message=question):
>             response = chat.send_message(question)
>             print(response.text)
>
> tracing.shutdown()
> ```

> [tab] TypeScript
>
> Wrap each agent run in `tracing.runIsolated()`, so that its conversation and turns stay separate from other concurrent runs.
>
> ```typescript lines title="app.mjs" theme={"system"}
> import {GoogleGenAI} from '@google/genai';
> import {tracing} from '@coreweave/forge-sdk/agentlens';
>
> await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
> const google = new GoogleGenAI({apiKey: process.env.GEMINI_API_KEY});
>
> const questions = [
>   'What is inference latency?',
>   'How does batching affect it?',
>   'Summarize what we discussed in one sentence.',
> ];
>
> await tracing.runIsolated(async () => {
>   const conversation = tracing.startConversation({agentName: 'support-agent'});
>   const chat = google.chats.create({model: 'gemini-flash-latest'});
>   try {
>     for (const question of questions) {
>       const turn = conversation.startTurn({userMessage: question});
>       try {
>         const response = await chat.sendMessage({message: question});
>         console.log(response.text);
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
> Run the script with the instrumentation flag, which loads the Forge instrumentation before your code so that the Google Gen AI SDK is patched when your code imports it:
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
> const google = integrations.wrapGoogleGenAI(
>   new GoogleGenAI({apiKey: process.env.GEMINI_API_KEY})
> );
> ```
>
> When you run without the flag, `tracing.init()` prints a one-time warning about it. You can ignore the warning if you wrap your clients.

To add turns to an existing conversation later, such as in a web app that handles one turn per request, pass the same `conversation_id` (Python) or `conversationId` (TypeScript) each time you create the conversation.

For more about conversations, turns, and the other span types, see [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md).

## Turn off automatic patching

In Python, pass `autopatch_integrations=False` to `tracing.init()`. You can then patch and unpatch the Google Gen AI SDK yourself with `tracing.integrations.patch_google_genai()` and `tracing.integrations.unpatch_google_genai()`.

In TypeScript, run without the `--import=@coreweave/forge-sdk/instrument` flag, and wrap only the clients you want to trace with `integrations.wrapGoogleGenAI()`.

## View your traces

In [CoreWeave Forge](https://forge.coreweave.com), select Agent Lens from the product menu, select your project in the project selector at the top of the side menu, and then select **Conversations**. For more information, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
