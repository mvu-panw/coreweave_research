# Message types

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/message-types

# Message types

> Messages, message parts, token usage, reasoning, and media attachments recorded on spans.

Access these through the `tracing` module:

```python theme={"system"}
from coreweave.forge.agentlens import tracing
```

## Message

```python theme={"system"}
class Message(BaseModel): ...
```

A single message in a conversation.

Two construction styles are supported:

1. Flat (back-compat, ergonomic for plain text):
   `Message(role="assistant", content="Hi there")`

2. Explicit parts (richer; supports tool calls, mixed reasoning+text,
   inline media):
   `Message(role="assistant", parts=[TextPart(content="Let me check"), ToolCallPart(id="c1", name="get_weather", arguments='{...}')])`

When `parts` is non-empty it is the canonical representation. When
empty, the serializer synthesizes a single TextPart (or
ToolCallResponsePart for `role="tool"`) from the flat fields.

`Message` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `role` | `Literal['user', 'assistant', 'system', 'tool']` | Required |
| `content` | `str` | `''` |
| `tool_call_id` | `str` | `''` |
| `tool_name` | `str` | `''` |
| `parts` | `list[MessagePart]` | `[]` |

### Message.user

```python theme={"system"}
@classmethod
def user(text: str) -> Message: ...
```

Build a user message from plain text.

### Message.system

```python theme={"system"}
@classmethod
def system(text: str) -> Message: ...
```

Build a system message from plain text.

### Message.assistant

```python theme={"system"}
@classmethod
def assistant(
    text: str = '',
    *,
    tool_calls: Union[list[ToolCallPart], None] = None,
) -> Message: ...
```

Build an assistant message with optional text and tool calls.

Use plain text for simple replies; pass `tool_calls` when the
assistant requests one or more tools. When both are present the
text is emitted as a leading `TextPart` followed by each
`ToolCallPart` so the chat view renders them inline.

### Message.tool\_result

```python theme={"system"}
@classmethod
def tool_result(call_id: str, output: Any) -> Message: ...
```

Build a tool-result message for a previously-requested tool call.

`output` may be a string, dict, list, scalar, or `None`; the
underlying `ToolCallResponsePart` JSON-encodes non-strings.

## MessagePart

```python theme={"system"}
MessagePart = Annotated[Union[TextPart, ReasoningPart, ToolCallPart, ToolCallResponsePart, BlobPart, UriPart, FilePart], Field(discriminator='type')]
```

## TextPart

```python theme={"system"}
class TextPart(BaseModel): ...
```

Plain-text content part.

`TextPart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['text']` | `'text'` |
| `content` | `str` | `''` |

## ReasoningPart

```python theme={"system"}
class ReasoningPart(BaseModel): ...
```

Reasoning / chain-of-thought content part.

`ReasoningPart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['reasoning']` | `'reasoning'` |
| `content` | `str` | `''` |

## ToolCallPart

```python theme={"system"}
class ToolCallPart(BaseModel): ...
```

An assistant's request to invoke a tool.

`arguments` is a string on the wire (per GenAI semconv). The
`JSONString` annotation lets callers pass a dict / list / scalar
at construction or assignment and the SDK JSON-encodes it; an
already-encoded string passes through unchanged.

`ToolCallPart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['tool_call']` | `'tool_call'` |
| `id` | `str` | `''` |
| `name` | `str` | `''` |
| `arguments` | `JSONString` | `''` |

## ToolCallResponsePart

```python theme={"system"}
class ToolCallResponsePart(BaseModel): ...
```

The result of executing a previously-requested tool call.

`response` is a string on the wire. Same `JSONString` ergonomics
as `ToolCallPart.arguments`.

`ToolCallResponsePart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['tool_call_response']` | `'tool_call_response'` |
| `id` | `str` | `''` |
| `response` | `JSONString` | `''` |

## BlobPart

```python theme={"system"}
class BlobPart(BaseModel): ...
```

Inline binary content (for example base64-encoded image / audio).

`BlobPart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['blob']` | `'blob'` |
| `mime_type` | `str` | `''` |
| `modality` | `str` | `''` |
| `content` | `str` | `''` |

## UriPart

```python theme={"system"}
class UriPart(BaseModel): ...
```

Reference to media content by URI.

`UriPart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['uri']` | `'uri'` |
| `mime_type` | `str` | `''` |
| `modality` | `str` | `''` |
| `uri` | `str` | `''` |

## FilePart

```python theme={"system"}
class FilePart(BaseModel): ...
```

Reference to media content by provider-side file id.

`FilePart` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `type` | `Literal['file']` | `'file'` |
| `mime_type` | `str` | `''` |
| `modality` | `str` | `''` |
| `file_id` | `str` | `''` |

## Usage

```python theme={"system"}
class Usage(BaseModel): ...
```

Token usage for an LLM call.

`Usage` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `input_tokens` | `int` | `0` |
| `output_tokens` | `int` | `0` |
| `total_tokens` | `Union[int, None]` | `None` |
| `reasoning_tokens` | `int` | `0` |
| `cache_creation_input_tokens` | `int` | `0` |
| `cache_read_input_tokens` | `int` | `0` |

## Reasoning

```python theme={"system"}
class Reasoning(BaseModel): ...
```

Reasoning/chain-of-thought content from an LLM call.

`Reasoning` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `content` | `str` | `''` |

## MediaAttachment

```python theme={"system"}
class MediaAttachment(BaseModel): ...
```

Media emitted as an OTLP GenAI blob, URI, or provider file part.

`MediaAttachment` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `content` | `str` | `''` |
| `uri` | `str` | `''` |
| `file_id` | `str` | `''` |
| `modality` | `str` | `''` |
| `mime_type` | `str` | `''` |
