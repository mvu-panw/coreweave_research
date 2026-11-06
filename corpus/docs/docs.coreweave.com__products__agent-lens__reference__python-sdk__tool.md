# Tool

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/tool

# Tool

> The Tool class records one tool execution as an execute_tool span.

```python theme={"system"}
class Tool(BaseModel): ...
```

One tool execution. Maps to an execute\_tool OTel span.

`arguments` and `result` use the `JSONString` annotation:
callers can assign a dict / list / scalar and the SDK JSON-encodes
it at construction or assignment. The stored value is always a
string, matching the wire format per GenAI semconv.

`Tool` is a Pydantic model. Set any field below as a keyword argument when you construct it.

`Tool` is a context manager and can be used in a `with` statement.

## Fields

| Field | Type | Default |
| - | - | - |
| `name` | `str` | `''` |
| `arguments` | `JSONString` | `''` |
| `result` | `JSONString` | `''` |
| `tool_call_id` | `str` | `''` |
| `tool_type` | `str` | `''` |
| `tool_description` | `str` | `''` |
| `tool_definitions` | `str` | `''` |
| `duration_ms` | `int` | `0` |
| `started_at` | `Union[datetime, None]` | `None` |
| `ended_at` | `Union[datetime, None]` | `None` |

## Methods

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
