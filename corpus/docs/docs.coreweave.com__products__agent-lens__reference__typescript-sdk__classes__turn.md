# Turn

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/turn

# Turn

> An agent invocation.

An agent invocation. Typically wraps the work to respond to a single
user message. Emits an `invoke_agent` span and acts as the root of the
trace for that turn: it is always started under `ROOT_CONTEXT` so it
never accidentally inherits a parent from another OTel-instrumented
library.

Created by `tracing.startTurn()` (or `conversation.startTurn()`) and
terminated with `end()`. Only one Turn may be active in an async chain.
Children (LLM, Tool, SubAgent) attach via the `startLLM`, `startTool`,
`startSubagent` methods.

## Examples

```typescript theme={"system"}
const turn = tracing.startTurn();

try {
  const llm = turn.startLLM({model: 'gpt-4o', providerName: 'openai'});
  // ...
  llm.end();
} finally {
  turn.end();
}
```

```typescript theme={"system"}
const turn = tracing.startTurn({
  model: 'gpt-4o',
  agentName: 'research-bot',
  agentId: 'research-bot-prod',
  agentDescription: 'Looks up facts on Wikipedia.',
  agentVersion: '1.4.2',
  userMessage: 'What is the weather in Tokyo?',
  systemInstructions: ['You are a helpful weather bot.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});

try {
  const llm = turn.startLLM({model: 'gpt-4o', providerName: 'openai'});
  // ...
  llm.end();
} finally {
  turn.end();
}
```

## Properties

**agentName** `string`

Read-only.

**model** `string`

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
    model?: string;
    systemInstructions?: string[];
    agentId?: string;
    agentName?: string;
    agentDescription?: string;
    agentVersion?: string;
  },
): this
```

Bulk-set any subset of the mutable fields. Replaces (does not merge).
Useful for assigning everything at once after a provider call returns.

The span is named from `agentName` when it starts, so pass `agentName` to
`startTurn` if the name has to carry it. `record` still updates the field
that `end()` writes to `gen_ai.agent.name`; it does not rename the span.

#### Parameters

**opts** `object` *required*

**properties**

**messages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**outputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**model** `string`

**systemInstructions** `string[]`

**agentId** `string`

**agentName** `string`

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

Start a child LLM span under this Turn.

#### Parameters

**opts** `LLMInit` *required*

Type: [`LLMInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/llminit)

#### Returns

[`LLM`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm)

### `startSubagent()`

```typescript theme={"system"}
startSubagent(opts: SubAgentInit): SubAgent
```

Start a child SubAgent span under this Turn.

#### Parameters

**opts** `SubAgentInit` *required*

Type: [`SubAgentInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/subagentinit)

#### Returns

[`SubAgent`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent)

### `startTool()`

```typescript theme={"system"}
startTool(opts: ToolInit): Tool
```

Start a child Tool span under this Turn.

#### Parameters

**opts** `ToolInit` *required*

Type: [`ToolInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolinit)

#### Returns

[`Tool`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool)
