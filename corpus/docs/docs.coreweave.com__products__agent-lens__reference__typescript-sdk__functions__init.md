# init

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/init

# init

> Reference for the init function in the Agent Lens TypeScript SDK.

```typescript theme={"system"}
init(projectName: string, options?: TracingInitOptions): Promise<void>
```

Call as `tracing.init()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

## Parameters

**projectName** `string` *required*

**options** `TracingInitOptions` (default: \{})

Type: [`TracingInitOptions`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/tracinginitoptions)

## Returns

`Promise<void>`
