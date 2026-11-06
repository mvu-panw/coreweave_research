# wrapGoogleGenAI

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapgooglegenai

# wrapGoogleGenAI

> Wrap a Google Gen AI client explicitly.

```typescript theme={"system"}
wrapGoogleGenAI<T>(client: T): T
```

Call as `integrations.wrapGoogleGenAI()` after importing `integrations` from `@coreweave/forge-sdk/agentlens`.

Wrap a Google Gen AI client explicitly. Automatic ESM instrumentation is
available through `node --import=@coreweave/forge-sdk/instrument`.

## Type parameters

**T**

## Parameters

**client** `T` *required*

## Returns

`T`
