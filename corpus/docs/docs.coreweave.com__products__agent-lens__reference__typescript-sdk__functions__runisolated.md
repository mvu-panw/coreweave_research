# runIsolated

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/runisolated

# runIsolated

> Give one request or agent run its own tracing state, including across awaits.

```typescript theme={"system"}
runIsolated<T>(fn: () => T): T
```

Call as `tracing.runIsolated()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Give one request or agent run its own tracing state, including across awaits.

## Type parameters

**T**

## Parameters

**fn** `() =\> T` *required*

## Returns

`T`
