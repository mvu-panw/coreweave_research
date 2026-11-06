# ToolEndOptions

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/toolendoptions

# ToolEndOptions

> Reference for the ToolEndOptions interface in the Agent Lens TypeScript SDK.

Used by: [`Tool.end()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/tool)

## Properties

**endTime** `TimeInput`

**error** `Error`

**errorType** `string`

Stable failure classification recorded on the `error.type` attribute.

**result** `JsonValue`

Type: [`JsonValue`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/jsonvalue)

A JSON value. Strings are recorded as-is; other values are serialized.
