# MessagePart

Source: https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/messagepart

# MessagePart

> A message part in the GenAI semconv parts model.

```typescript theme={"system"}
type MessagePart =
  | {type: 'text'; content: string}
  | {type: 'reasoning'; content: string}
  | {type: 'tool_call'; id: string; name: string; arguments?: string}
  | {type: 'tool_call_response'; id: string; response?: string}
  | {type: 'file'; file_id: string; mime_type?: string; modality: Modality}
  | {type: 'blob'; content: string; mime_type: string; modality: Modality}
  | {type: 'uri'; uri: string; mime_type?: string; modality: Modality};
```

A message part in the GenAI semconv parts model. Parts are serialized as-is
into `gen_ai.input.messages` / `gen_ai.output.messages`, so the keys are the
semconv wire keys (snake\_case), matching the Python SDK and the Agent Lens UI.

Related types: [`Modality`](https://docs.coreweave.com/products/agent-lens/reference/typescript-sdk/type-aliases/modality)
