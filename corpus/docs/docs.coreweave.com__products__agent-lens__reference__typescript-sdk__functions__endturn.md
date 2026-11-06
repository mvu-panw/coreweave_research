# endTurn

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/endturn

# endTurn

> End the current Turn.

```typescript theme={"system"}
endTurn(opts?: SpanEndOptions): void
```

Call as `tracing.endTurn()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

End the current Turn. No-op if no Turn is active.

## Parameters

**opts** `SpanEndOptions`

## Examples

```typescript theme={"system"}
tracing.endTurn();
```

```typescript theme={"system"}
tracing.endTurn({endTime: new Date('2026-05-29T10:00:01.700Z')});
```

```typescript theme={"system"}
tracing.endTurn({error: new Error('agent loop diverged')});
```
