# startLLM

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startllm

# startLLM

> Start an LLM span as a child of the current Turn.

```typescript theme={"system"}
startLLM(opts: LLMInit): LLM
```

Call as `tracing.startLLM()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Start an LLM span as a child of the current Turn. Throws if no Turn is
active.

## Parameters

**opts** `LLMInit` *required*

Type: [`LLMInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/llminit)

## Returns

[`LLM`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm)

## Examples

```typescript theme={"system"}
tracing.startLLM({model: 'gpt-4o-mini', providerName: 'openai'});
```

```typescript theme={"system"}
tracing.startLLM({
  model: 'gpt-4o-mini',
  providerName: 'openai',
  systemInstructions: ['You are a helpful weather bot.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});
```
