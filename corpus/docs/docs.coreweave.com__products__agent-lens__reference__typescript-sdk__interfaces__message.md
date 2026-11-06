# Message

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/message

# Message

> Reference for the Message interface in the Agent Lens TypeScript SDK.

Used by: [`LLM.record()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/llm), [`SubAgent.record()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/subagent), [`Turn.record()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/turn)

## Properties

**content** `string`

**parts** `MessagePart[]`

Type: [`MessagePart`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/messagepart)`[]`

**role** `Role` *required*

Type: [`Role`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/role)

**toolCallId** `string`

**toolName** `string`
