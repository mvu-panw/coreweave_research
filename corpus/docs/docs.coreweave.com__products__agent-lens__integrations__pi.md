# Pi extension

Source: https://docs.coreweave.com/products/agent-lens/integrations/pi

# Pi extension

> Trace Pi agentic sessions, LLM calls, and tool executions in Agent Lens.

[Pi](https://pi.dev/) is a terminal-based coding agent. CoreWeave Agent Lens traces Pi sessions, LLM calls, and tool executions automatically using the `createOtelExtension` integration from the Weights & Biases Weave SDK (`weave`), which conforms to the [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md). This page shows you how to enable Agent Lens tracing in a Pi application so you can observe agent behavior, debug runs, and analyze token usage and cost.

> [!NOTE]
>
> The CoreWeave Forge SDK doesn't have a Pi integration yet, so this page uses the Weave SDK. Traces you send with Weave appear in Agent Lens, because both products share the same trace data.

> [!WARNING]
>
> This integration sends Pi session data to Agent Lens. That data can include user prompts, model responses, tool inputs and outputs, file contents read by Pi tools, shell commands and output, and fetched URLs and page content.
>
> The integration doesn't implement PII scrubbing or sensitive-data redaction. If you can't send this data to Agent Lens under your security or compliance requirements, don't enable Agent Lens tracing in your Pi application.

## Prerequisites

* [Node.js](https://nodejs.org/) (v22.19 or later). On Node 20, `npm` installs an older Pi release that still supports it.
* A CoreWeave Forge account and [API key](https://forge.coreweave.com/settings#apikeys) set as a `WANDB_API_KEY` environment variable.

> [!NOTE]
>
> Pi is a TypeScript and Node.js framework with no Python equivalent. Pi requires the ESM module system. Your project must use `"type": "module"` in `package.json`, or compile TypeScript to ESM output. CommonJS projects error. For more information about setting up an ESM project, see [TypeScript SDK integration](https://docs.coreweave.com/products/wandb/weave/guides/integrations/js.md#set-up-an-esm-project).

## Install packages

Install Agent Lens, Pi, and Node type definitions as local project dependencies:

```bash lines theme={"system"}
npm install weave @earendil-works/pi-coding-agent
npm install --save-dev @types/node tsx typescript
```

## Trace a Pi prompt and response

The following example shows the minimum setup needed to trace a single Pi prompt and response. Call `init()` from the `weave` package before you create your agent session, then pass `createOtelExtension()` as an extension factory. Agent Lens traces the full agent lifecycle: the conversation, each prompt-and-response cycle (`invoke_agent`), individual LLM calls (`chat`), and tool executions (`execute_tool`). `SessionManager.inMemory()` generates the session ID automatically.

```typescript lines twoslash theme={"system"}
// @noErrors
import {init, createOtelExtension} from 'weave';

import {
  createAgentSession,
  DefaultResourceLoader,
  SessionManager,
  getAgentDir,
} from '@earendil-works/pi-coding-agent';

async function main() {
  // 1. Initialize Weave. Sets up the OTEL TracerProvider that points at your
  //    Weave project. All spans created by createOtelExtension() are
  //    automatically exported here.
  await init('[YOUR-TEAM]/[YOUR-PROJECT]');

  // 2. Create a resource loader and inject the Weave OTEL extension.
  //    The resource loader provides the Pi runtime environment and
  //    extension lifecycle used for tracing agent activity.
  const resourceLoader = new DefaultResourceLoader({
    cwd: process.cwd(),
    agentDir: getAgentDir(),
    extensionFactories: [createOtelExtension({})],
  });

  await resourceLoader.reload();

  // 3. Start the agent session
  const {session} = await createAgentSession({
    resourceLoader,
    sessionManager: SessionManager.inMemory(),
  });

  // 4. Bind extensions. Triggers session_start event so the OTEL adapter
  //    creates the root conversation span and captures the conversation ID.
  await session.bindExtensions({});

  // 5. Stream assistant output to stdout
  session.subscribe(event => {
    if (
      event.type === 'message_update' &&
      event.assistantMessageEvent.type === 'text_delta'
    ) {
      process.stdout.write(event.assistantMessageEvent.delta);
    }
  });

  // 6. Send a prompt and wait for the full response
  await session.prompt('What files are in the current directory?');
  console.log();
}

main();
```

Compile and execute the script with `tsx`, replacing `[FILENAME]` with the name of your TypeScript file:

```bash theme={"system"}
npx tsx [FILENAME].ts
```

When you run your code, your traces appear in the **Conversations** tab of your Agent Lens project at `https://forge.coreweave.com/agent-lens/[YOUR-TEAM]/[YOUR-PROJECT]`. Agent Lens captures Pi sessions, LLM calls, and tool executions for every run of your application.

### Next steps

To turn this example into a multi-turn conversation, add more prompts. Agent Lens traces each call to `session.prompt()` as a separate `invoke_agent` span, all nested under a single root span. The agent retains context across prompts automatically.

After running the code, the **Conversations** tab shows the full multi-turn timeline with nested LLM calls, tool executions, token usage, and cost.
