# startTool

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/starttool

# startTool

> Start a Tool span.

```typescript theme={"system"}
startTool(opts: ToolInit): Tool
```

Call as `tracing.startTool()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Start a Tool span. Parent resolution (matches the design's "flat by
default, hierarchical if you nest"):

* If an LLM is active, the Tool nests under it.
* Otherwise, the Tool is a sibling under the current Turn.

Throws if neither a Turn nor an LLM is active.

## Parameters

**opts** `ToolInit` *required*

Type: [`ToolInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolinit)

## Returns

[`Tool`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool)

## Examples

```typescript theme={"system"}
tracing.startTool({
  name: 'get_weather',
  args: {city: 'Tokyo'},
  toolCallId: 'call_t1',
});
```

```typescript theme={"system"}
tracing.startTool({
  name: 'get_weather',
  args: {city: 'Tokyo'},
  toolCallId: 'call_t1',
  startTime: new Date('2026-05-29T10:00:00.800Z'),
});
```
