# ConversationInit

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/conversationinit

# ConversationInit

> Reference for the ConversationInit interface in the Agent Lens TypeScript SDK.

Used by: [`tracing.startConversation()`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startconversation)

## Properties

**agentDescription** `string`

Human-readable agent description. Propagated as the default
`agentDescription` to every `Turn` created via `startTurn()` unless
the turn sets its own; emitted on each turn's `invoke_agent` span as
`gen_ai.agent.description`.

**agentId** `string`

Stable agent identifier. Propagated as the default `agentId` to every
`Turn` created via `startTurn()` unless the turn sets its own; emitted
on each turn's `invoke_agent` span as `gen_ai.agent.id`.

**agentName** `string`

Agent name. Propagated as the default `agentName` to every `Turn`
created via `startTurn()` unless the turn sets its own; emitted on
each turn's `invoke_agent` span as `gen_ai.agent.name`.

**agentVersion** `string`

Agent version string. Propagated as the default `agentVersion` to
every `Turn` created via `startTurn()` unless the turn sets its own;
emitted on each turn's `invoke_agent` span as `gen_ai.agent.version`.

**attributes** `Attributes`

Custom attributes propagated to every span the conversation emits.

A key here that collides with a span's own `gen_ai.*` / `weave.*`
attribute is unsupported; the span's value wins.

**conversationId** `string`

Conversation ID propagated to every span under this conversation as
`gen_ai.conversation.id`. Auto-generated if omitted.

**model** `string`
