# wrapAnthropic

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/integrations/wrapanthropic

# wrapAnthropic

> Wrap an Anthropic client explicitly.

```typescript theme={"system"}
wrapAnthropic<T extends AnthropicAPI>(anthropic: T): T
```

Call as `integrations.wrapAnthropic()` after importing `integrations` from `@coreweave/forge-sdk/agentlens`.

Wrap an Anthropic client explicitly. Automatic ESM instrumentation is
available through `node --import=@coreweave/forge-sdk/instrument`.

## Type parameters

**T** `extends AnthropicAPI`

## Parameters

**anthropic** `T` *required*

## Returns

`T`
