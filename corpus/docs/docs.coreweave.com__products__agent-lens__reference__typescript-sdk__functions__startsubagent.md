# startSubagent

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startsubagent

# startSubagent

> Start a SubAgent span.

```typescript theme={"system"}
startSubagent(opts: SubAgentInit): SubAgent
```

Call as `tracing.startSubagent()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Start a SubAgent span. Same parent-resolution rules as `startTool`.

## Parameters

**opts** `SubAgentInit` *required*

Type: [`SubAgentInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/subagentinit)

## Returns

[`SubAgent`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent)

## Examples

```typescript theme={"system"}
tracing.startSubagent({name: 'critic'});
```

```typescript theme={"system"}
tracing.startSubagent({
  name: 'critic',
  model: 'gpt-4o',
  systemInstructions: ['Critique the proposed plan.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});
```
