# TurnInit

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/turninit

# TurnInit

> Reference for the TurnInit interface in the Agent Lens TypeScript SDK.

Used by: [`tracing.startTurn()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startturn), [`Conversation.startTurn()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/conversation)

## Properties

**agentDescription** `string`

**agentId** `string`

**agentName** `string`

**agentVersion** `string`

**attributes** `Attributes`

Custom attributes set on this turn and passed to every child span.
Normally seeded from the conversation via `startConversation({ attributes })`;
set here for a rootless `startTurn({ attributes })` with no conversation.

**model** `string`

**startTime** `TimeInput`

**systemInstructions** `string[]`

**userMessage** `string`
