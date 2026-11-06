# Tool

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool

# Tool

> A tool invocation.

A tool invocation. Emits an `execute_tool` span carrying the tool name,
the arguments, the tool-call id, and the result. String arguments and
results are recorded as-is; other JSON values are serialized.

Created by `tracing.startTool()` (or `turn.startTool()`, or
`llm.startTool()`) and terminated with `end()`, which accepts the result and
optional error metadata.

## Examples

```typescript theme={"system"}
const tool = tracing.startTool({name: 'get_weather', args: {city: 'Tokyo'}});
try {
  const result = await getWeather('Tokyo');
  tool.end({result});
} catch (error) {
  tool.end({error: error as Error, errorType: 'weather_error'});
  throw error;
}
```

## Properties

**args** `string`

Read-only.

**name** `string`

Read-only.

**toolCallId** `string`

Read-only.

## Methods

### `end()`

```typescript theme={"system"}
end(opts?: ToolEndOptions): void
```

Record an optional result and error type, then close the span. Idempotent.
Pass `error` to mark the span as failed and `endTime` to backdate the close.

#### Parameters

**opts** `ToolEndOptions`

Type: [`ToolEndOptions`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolendoptions)

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
