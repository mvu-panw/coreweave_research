# Turn

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/turn

# Turn

> The Turn class records one user-agent exchange as an invoke_agent span.

```python theme={"system"}
class Turn(BaseModel): ...
```

One user-agent exchange. Maps to an invoke\_agent OTel span.

By default each turn starts its own OTel trace (`continue_parent_trace=False`)
so the Conversations tab shows one trace per turn. Set `continue_parent_trace=True`
on the Conversation (or directly on the Turn) when an outer trace is already
active and you want the agent invocation to nest inside it; for example inside
a fastapi-instrumented request.

`Turn` is a Pydantic model. Set any field below as a keyword argument when you construct it.

`Turn` is a context manager and can be used in a `with` statement.

## Fields

| Field | Type | Default |
| - | - | - |
| `agent_name` | `str` | `''` |
| `model` | `str` | `''` |
| `agent_id` | `str` | `''` |
| `agent_description` | `str` | `''` |
| `agent_version` | `str` | `''` |
| `system_instructions` | `list[str]` | `[]` |
| `messages` | `list[Message]` | `[]` |
| `output_messages` | `list[Message]` | `[]` |
| `spans` | `list[Union[LLM, Tool, SubAgent]]` | `[]` |
| `continue_parent_trace` | `bool` | `False` |
| `started_at` | `Union[datetime, None]` | `None` |
| `ended_at` | `Union[datetime, None]` | `None` |

## Methods

### user

```python theme={"system"}
def user(content: str) -> Turn: ...
```

Append a user message mid-turn.

### start\_llm

```python theme={"system"}
def start_llm(
    *,
    model: str = '',
    provider_name: str = '',
    system_instructions: Union[list[str], None] = None,
) -> LLM: ...
```

Start an LLM call (chat span, child of this turn).

Sets the `_current_llm` contextvar so the LLM is visible via
`get_current_llm()` regardless of whether a context manager is used.

### start\_tool

```python theme={"system"}
def start_tool(*, name: str, arguments: str = '', tool_call_id: str = '') -> Tool: ...
```

Start a tool execution (execute\_tool span, child of this turn).

### start\_subagent

```python theme={"system"}
def start_subagent(
    *,
    name: str,
    model: str = '',
    system_instructions: Union[list[str], None] = None,
    set_current: bool = True,
) -> SubAgent: ...
```

Start a sub-agent invocation (nested invoke\_agent span, same trace).

### record

```python theme={"system"}
def record(
    *,
    messages: Union[list[Message], None] = None,
    output_messages: Union[list[Message], None] = None,
    system_instructions: Union[list[str], None] = None,
    agent_name: Union[str, None] = None,
    model: Union[str, None] = None,
    agent_id: Union[str, None] = None,
    agent_description: Union[str, None] = None,
    agent_version: Union[str, None] = None,
) -> Turn: ...
```

Set multiple turn fields in one call.

Collapses the per-field assignments a manually-instrumented agent
otherwise makes on a turn (`system_instructions`, `agent_id`,
...) into a single keyword call. Only fields explicitly passed
(non-`None`) are applied; existing values are preserved.
`messages` and `output_messages` independently replace the turn's
existing input and output messages. This differs from
`Turn.user(...)`, which appends a single input message. Returns
`self` for chaining. Mirrors `LLM.record`.

Note: on the streaming (`with`) path the turn span is named from
`agent_name` at `__enter__`, so set `agent_name` via
`start_turn` rather than `record` if you need the span name to
reflect it; `record` still updates the `gen_ai.agent.name`
attribute.

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
