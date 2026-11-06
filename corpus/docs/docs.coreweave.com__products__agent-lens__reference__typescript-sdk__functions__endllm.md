# endLLM

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endllm

# endLLM

> End the current LLM.

```typescript theme={"system"}
endLLM(opts?: SpanEndOptions): void
```

Call as `tracing.endLLM()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

End the current LLM. No-op if no LLM is active.

## Parameters

**opts** `SpanEndOptions`

## Examples

```typescript theme={"system"}
tracing.endLLM();
```

```typescript theme={"system"}
tracing.endLLM({endTime: new Date('2026-05-29T10:00:00.800Z')});
```

```typescript theme={"system"}
tracing.endLLM({error: new Error('llm call failed')});
```
