# Conversation

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/conversation

# Conversation

> A Conversation groups Turns under a single gen_ai.conversation.id.

A Conversation groups Turns under a single `gen_ai.conversation.id`. It is
not itself an OTel span; children stamp the conversation id onto theirs.

## Properties

**agentName** `string`

Read-only.

**attributes** `Attributes`

Read-only.

**conversationId** `string`

Read-only.

**model** `string`

Read-only.

## Methods

### `end()`

```typescript theme={"system"}
end(opts?: SpanEndOptions): void
```

#### Parameters

**opts** `SpanEndOptions`

### `startTurn()`

```typescript theme={"system"}
startTurn(opts?: TurnInit): Turn
```

Start a new `Turn` under this `Conversation`. The turn inherits the
conversation's `conversationId`; `agentName`, `agentId`, `agentDescription`,
`agentVersion` and `model` fall back to the conversation's values when not
provided on `opts`.

#### Parameters

**opts** `TurnInit` (default: \{})

Type: [`TurnInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/turninit)

#### Returns

[`Turn`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/turn)

#### Examples

```typescript theme={"system"}
const turn = conversation.startTurn();
```

```typescript theme={"system"}
const turn = conversation.startTurn({
  model: 'gpt-4o',
  agentName: 'research-bot',
  agentId: 'research-bot-prod',
  agentDescription: 'Looks up facts on Wikipedia.',
  agentVersion: '1.4.2',
  userMessage: 'What is the weather in Tokyo?',
  systemInstructions: ['You are a helpful weather bot.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});
```
