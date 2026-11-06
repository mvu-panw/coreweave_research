# LLM

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/llm

# LLM

> The LLM class records one LLM API call as a chat span.

```python theme={"system"}
class LLM(BaseModel): ...
```

One LLM API call. Maps to a chat OTel span.

`LLM` is a Pydantic model. Set any field below as a keyword argument when you construct it.

`LLM` is a context manager and can be used in a `with` statement.

## Fields

| Field | Type | Default |
| - | - | - |
| `model` | `str` | `''` |
| `provider_name` | `str` | `''` |
| `response_id` | `str` | `''` |
| `response_model` | `str` | `''` |
| `output_type` | `str` | `''` |
| `system_instructions` | `list[str]` | `[]` |
| `usage` | `Usage` | `Usage()` |
| `reasoning` | `Reasoning` | `Reasoning()` |
| `finish_reasons` | `list[str]` | `[]` |
| `input_messages` | `list[Message]` | `[]` |
| `output_messages` | `list[Message]` | `[]` |
| `media_attachments` | `list[MediaAttachment]` | `[]` |
| `request_temperature` | `Union[float, None]` | `None` |
| `request_max_tokens` | `Union[int, None]` | `None` |
| `request_top_p` | `Union[float, None]` | `None` |
| `request_top_k` | `Union[float, None]` | `None` |
| `request_frequency_penalty` | `Union[float, None]` | `None` |
| `request_presence_penalty` | `Union[float, None]` | `None` |
| `request_seed` | `Union[int, None]` | `None` |
| `request_stop_sequences` | `list[str]` | `[]` |
| `request_choice_count` | `Union[int, None]` | `None` |
| `started_at` | `Union[datetime, None]` | `None` |
| `ended_at` | `Union[datetime, None]` | `None` |

## Methods

### output

```python theme={"system"}
def output(content: str) -> LLM: ...
```

Append an assistant message to output\_messages.

### think

```python theme={"system"}
def think(content: str) -> LLM: ...
```

Set reasoning/chain-of-thought content.

### attach\_media

```python theme={"system"}
def attach_media(
    *,
    content: Union[bytes, str] = '',
    uri: str = '',
    file_id: str = '',
    mime_type: str = '',
    modality: str = '',
) -> LLM: ...
```

Attach media to this LLM call.

Exactly one source is required. Bytes are base64-encoded as an inline
GenAI blob. String content must already be base64-encoded. URIs and
provider file IDs are emitted as GenAI URI and file parts.

### attach\_media\_url

```python theme={"system"}
def attach_media_url(url: str, *, modality: str = '') -> LLM: ...
```

Attach a data URL or ordinary media URI to this LLM call.

### record

```python theme={"system"}
def record(
    *,
    input_messages: Union[list[Message], None] = None,
    output_messages: Union[list[Message], None] = None,
    media_attachments: Union[list[MediaAttachment], None] = None,
    usage: Union[Usage, None] = None,
    reasoning: Union[Reasoning, str, None] = None,
    response_id: Union[str, None] = None,
    response_model: Union[str, None] = None,
    finish_reasons: Union[list[str], None] = None,
    output_type: Union[str, None] = None,
) -> LLM: ...
```

Set multiple LLM-call fields in one call.

Manually-instrumented agents typically build up a chat span by
assigning eight or more individual fields at the end of an LLM
call (`input_messages`, `output_messages`, `usage`,
`response_id`, and so on). `record(...)` collapses those into a
single keyword call so the recording site stays compact.

Only fields explicitly passed (non-`None`) are applied;
existing values are preserved. `reasoning` accepts either a
`Reasoning` instance or a plain string (wrapped automatically).
Returns `self` for chaining.

### end

```python theme={"system"}
def end() -> None: ...
```

### start

```python theme={"system"}
def start() -> Self: ...
```

Start this span once; context-manager entry uses the same path.

### record\_error

```python theme={"system"}
def record_error(error: BaseException) -> Self: ...
```

Record a failure without ending the span; call `end()` when ready.

### set\_attributes

```python theme={"system"}
def set_attributes(attributes: dict[str, Any]) -> Self: ...
```

Stamp arbitrary OTel attributes on this span.

Pass a dict whether you have one key or many; single-key callers
use `span.set_attributes({"weave.tag": "value"})`. Mirrors OTel's
`Span.set_attributes`.

Must be called after a `start_*` factory, `start()`, or `with`
starts the span, and before it ends. Outside that window the call is a
no-op and logs a warning. For batch ingest, populate the object's declared fields
directly and pass it to `log_turn` / `log_conversation`.
