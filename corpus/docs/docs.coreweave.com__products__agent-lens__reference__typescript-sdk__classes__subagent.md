# SubAgent

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent

# SubAgent

> Reference for the SubAgent class in the Agent Lens TypeScript SDK.

## Properties

**model** `string`

Read-only.

**name** `string`

Read-only.

## Methods

### `end()`

```typescript theme={"system"}
end(opts?: SpanEndOptions): void
```

Read current field values (to reflect mutations made via `record()`
since `start`) and close the span. Idempotent. Pass `error` to mark
it as failed; pass `endTime` to backdate the close.

#### Parameters

**opts** `SpanEndOptions`

### `record()`

```typescript theme={"system"}
record(
  opts: {
    messages?: Message[];
    outputMessages?: Message[];
    name?: string;
    model?: string;
    systemInstructions?: string[];
    agentId?: string;
    agentDescription?: string;
    agentVersion?: string;
  },
): this
```

Bulk-set any subset of the mutable fields. Replaces (does not merge).
Input and output messages are serialized when the span ends.

The span is named from `name` when it starts, so pass `name` to
`startSubagent` if the name has to carry it. `record` still updates the
field that `end()` writes to `gen_ai.agent.name`; it does not rename the
span.

#### Parameters

**opts** `object` *required*

**properties**

**messages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**outputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**name** `string`

**model** `string`

**systemInstructions** `string[]`

**agentId** `string`

**agentDescription** `string`

**agentVersion** `string`

#### Returns

`this`

### `setAttributes()`

```typescript theme={"system"}
setAttributes(attributes: Attributes): this
```

Set multiple attributes on the span at once. Warns and no-ops after
`end()`. Mirrors OTel `Span.setAttributes` (and the Python SDK's
`set_attributes`).

#### Parameters

**attributes** `Attributes` *required*

#### Returns

`this`

#### Examples

```typescript theme={"system"}
span.setAttributes({'weave.tag': 'prod', 'gen_ai.response.id': id});
```

### `startLLM()`

```typescript theme={"system"}
startLLM(opts: LLMInit): LLM
```

Start a child LLM span nested under this SubAgent.

#### Parameters

**opts** `LLMInit` *required*

Type: [`LLMInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/llminit)

#### Returns

[`LLM`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm)

### `startSubagent()`

```typescript theme={"system"}
startSubagent(opts: SubAgentInit): SubAgent
```

Start a nested SubAgent span under this SubAgent.

#### Parameters

**opts** `SubAgentInit` *required*

Type: [`SubAgentInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/subagentinit)

#### Returns

[`SubAgent`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent)

### `startTool()`

```typescript theme={"system"}
startTool(opts: ToolInit): Tool
```

Start a child Tool span nested under this SubAgent.

#### Parameters

**opts** `ToolInit` *required*

Type: [`ToolInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolinit)

#### Returns

[`Tool`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool)
