# startTurn

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/functions/startturn

# startTurn

> Start a new Turn.

```typescript theme={"system"}
startTurn(opts?: TurnInit): Turn
```

Call as `tracing.startTurn()` after importing `tracing` from `@coreweave/forge-sdk/agentlens`.

Start a new Turn. If a Conversation is active, the turn inherits its
`conversationId`; otherwise the turn has no conversation id.

## Parameters

**opts** `TurnInit` (default: \{})

Type: [`TurnInit`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/interfaces/turninit)

## Returns

[`Turn`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/classes/turn)

## Examples

```typescript theme={"system"}
tracing.startTurn();
```

```typescript theme={"system"}
tracing.startTurn({
  agentId: 'research-bot-prod',
  agentName: 'research-bot',
  agentDescription: 'Looks up facts on Wikipedia.',
  agentVersion: '1.4.2',
  model: 'gpt-4o',
  userMessage: 'What is the weather in Tokyo?',
  systemInstructions: ['You are a helpful weather bot.'],
  startTime: new Date('2026-05-29T10:00:00.000Z'),
});
```
