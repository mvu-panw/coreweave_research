# LLM

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm

# LLM

> An LLM call.

An LLM call. Emits a `chat` span with `gen_ai.*` attributes.

Created by `tracing.startLLM()` (or `turn.startLLM()`, or
`subagent.startLLM()`) and terminated with `end()`. The most recently started
LLM is the current one (`getCurrentLLM`, `tracing.startTool`). An LLM started
under a SubAgent while another LLM is active nests LIFO: it is current until
it ends, then the enclosing LLM is current again. Nest tool/subagent calls
under an LLM via `startTool` / `startSubagent`.

Populate `inputMessages` / `outputMessages` / `usage` / `reasoning` directly,
or via the helper functions (`output`, `think`, `attachMedia`, `record`).

All recorded data is flushed to the span at `end()`.

## Examples

```typescript theme={"system"}
const llm = tracing.startLLM({model: 'gpt-4o-mini', providerName: 'openai'});

try {
  llm.inputMessages = [{role: 'user', content: prompt}];
  const resp = await openai.chat.completions.create({...});
  llm.output(resp.choices[0].message.content ?? '');
  llm.record({usage: {inputTokens: resp.usage?.prompt_tokens}});
} finally {
  llm.end();
}
```

```typescript theme={"system"}
const llm = tracing.startLLM({
  model: 'gpt-4o-mini',
  providerName: 'openai',
  systemInstructions: ['You are a helpful weather bot.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});

try {
  // ... call the LLM, populate llm.outputMessages / usage ...
} finally {
  llm.end();
}
```

## Properties

**inputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

Input messages sent to the model. Flushed to `gen_ai.input.messages` on
`end()`.

**model** `string`

Read-only.

**outputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

Assistant messages returned by the model. Flushed to
`gen_ai.output.messages` on `end()`.

**providerName** `string`

Read-only.

**reasoning** `Reasoning`

Type: [`Reasoning`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/reasoning)

Chain-of-thought content. Folded into the last assistant message as a
ReasoningPart at serialization time.

**usage** `Usage`

Type: [`Usage`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/usage)

Token counts and cache stats. Flushed to `gen_ai.usage.*` on `end()`.

## Methods

### `attachMedia()`

```typescript theme={"system"}
attachMedia(opts: AttachMediaOpts): this
```

Stage a media attachment for the LLM call. Pick exactly one of
`content` (inline base64 bytes), `uri` (URI reference), or `fileId`
(pre-uploaded file id). The attachment is glued onto the last user
message in `inputMessages` on `end()`.

#### Parameters

**opts** `AttachMediaOpts` *required*

#### Returns

`this`

### `attachMediaUrl()`

```typescript theme={"system"}
attachMediaUrl(url: string, opts: {modality: Modality}): this
```

Convenience for `attachMedia({uri, modality})`.

#### Parameters

**url** `string` *required*

**opts** `object` *required*

**properties**

**modality** `Modality` *required*

Type: [`Modality`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/modality)

#### Returns

`this`

### `end()`

```typescript theme={"system"}
end(opts?: SpanEndOptions): void
```

Flush accumulated state and close the span. Idempotent. Pass `error` to mark failed; pass `endTime` to backdate the close.

#### Parameters

**opts** `SpanEndOptions`

### `output()`

```typescript theme={"system"}
output(content: string): this
```

Append an assistant message to the response.

#### Parameters

**content** `string` *required*

#### Returns

`this`

### `record()`

```typescript theme={"system"}
record(
  opts: {
    inputMessages?: Message[];
    outputMessages?: Message[];
    usage?: Usage;
    reasoning?: Reasoning;
    responseId?: string;
    responseModel?: string;
    finishReasons?: string[];
    outputType?: string;
    mediaAttachments?: AttachMediaOpts[];
  },
): this
```

Bulk-set any subset of the mutable fields. Replaces (does not merge).
Useful for assigning everything at once after a provider call returns.

#### Parameters

**opts** `object` *required*

**properties**

**inputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**outputMessages** `Message[]`

Type: [`Message`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message)`[]`

**usage** `Usage`

Type: [`Usage`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/usage)

**reasoning** `Reasoning`

Type: [`Reasoning`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/reasoning)

**responseId** `string`

**responseModel** `string`

**finishReasons** `string[]`

**outputType** `string`

**mediaAttachments** `AttachMediaOpts[]`

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

### `startSubagent()`

```typescript theme={"system"}
startSubagent(opts: SubAgentInit): SubAgent
```

Start a child SubAgent span nested under this LLM.

#### Parameters

**opts** `SubAgentInit` *required*

Type: [`SubAgentInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/subagentinit)

#### Returns

[`SubAgent`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent)

### `startTool()`

```typescript theme={"system"}
startTool(opts: ToolInit): Tool
```

Start a child Tool span nested under this LLM.

#### Parameters

**opts** `ToolInit` *required*

Type: [`ToolInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolinit)

#### Returns

[`Tool`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool)

### `think()`

```typescript theme={"system"}
think(content: string): this
```

Set or extend the model's reasoning/chain-of-thought content. Accumulates
into `this.reasoning.content`. Folded into the last assistant message as
a `ReasoningPart` at serialization time, matching the Python SDK's
on-the-wire shape.

#### Parameters

**content** `string` *required*

#### Returns

`this`
