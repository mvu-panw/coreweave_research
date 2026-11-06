# wrapOpenAI

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapopenai

# wrapOpenAI

> Wrap an OpenAI client explicitly.

```typescript theme={"system"}
wrapOpenAI<T extends OpenAIAPI>(openai: T): T
```

Call as `integrations.wrapOpenAI()` after importing `integrations` from `@coreweave/forge-sdk/agentlens`.

Wrap an OpenAI client explicitly. Automatic ESM instrumentation is
available through `node --import=@coreweave/forge-sdk/instrument`.

## Type parameters

**T** `extends OpenAIAPI`

## Parameters

**openai** `T` *required*

## Returns

`T`
