# endConversation

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endconversation

# endConversation

> End the current Conversation.

```typescript theme={"system"}
endConversation(opts?: SpanEndOptions): void
```

Call as `tracing.endConversation()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

End the current Conversation. No-op if no Conversation is active.

## Parameters

**opts** `SpanEndOptions`

## Examples

```typescript theme={"system"}
tracing.endConversation();
```

```typescript theme={"system"}
tracing.endConversation({endTime: new Date('2026-05-29T10:00:01.700Z')});
```
