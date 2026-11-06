# startConversation

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startconversation

# startConversation

> Start a new Conversation and install it as the current conversation.

```typescript theme={"system"}
startConversation(opts?: ConversationInit): Conversation
```

Call as `tracing.startConversation()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Start a new Conversation and install it as the current conversation.
Subsequent calls to `startTurn` will pick it up automatically.
Call inside `tracing.runIsolated`, with one scope per request or agent run.

Pass `attributes` to propagate custom (non-semconv) attributes to every
span the conversation emits.

## Parameters

**opts** `ConversationInit` (default: \{})

Type: [`ConversationInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/conversationinit)

## Returns

[`Conversation`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/conversation)

## Examples

```typescript theme={"system"}
tracing.startConversation({agentName: 'research-bot'});
```

```typescript theme={"system"}
tracing.startConversation({
  agentName: 'research-bot',
  conversationId: '019efa53-8a65-711c-b4c1-7c1cb72c0bb7',
  attributes: {'myagent.version': '1.23'},
});
```
