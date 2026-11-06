# SubAgent

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/subagent

# SubAgent

> The SubAgent class records a delegated agent invocation as a nested invoke_agent span.

```python theme={"system"}
class SubAgent(BaseModel): ...
```

A delegated agent invocation within a turn.

Maps to a nested invoke\_agent OTel span in the same trace.

`SubAgent` is a Pydantic model. Set any field below as a keyword argument when you construct it.

`SubAgent` is a context manager and can be used in a `with` statement.

## Fields

| Field | Type | Default |
| - | - | - |
| `name` | `str` | `''` |
| `model` | `str` | `''` |
| `agent_id` | `str` | `''` |
| `agent_description` | `str` | `''` |
| `agent_version` | `str` | `''` |
| `system_instructions` | `list[str]` | `[]` |
| `input_messages` | `list[Message]` | `[]` |
| `output_messages` | `list[Message]` | `[]` |
| `tool_name` | `str` | `''` |
| `tool_call_id` | `str` | `''` |
| `tool_call_arguments` | `JSONString` | `''` |
| `tool_call_result` | `JSONString` | `''` |
| `started_at` | `Union[datetime, None]` | `None` |
| `ended_at` | `Union[datetime, None]` | `None` |

## Methods

### start\_llm

```python theme={"system"}
def start_llm(
    *,
    model: str = '',
    provider_name: str = '',
    system_instructions: Union[list[str], None] = None,
) -> LLM: ...
```

Start an LLM call within this sub-agent.

Sets the `_current_llm` contextvar so the LLM is visible via
`get_current_llm()` regardless of whether a context manager is used.
Pins the LLM's OTel parent to this SubAgent's span when the SubAgent
has been entered.

### start\_tool

```python theme={"system"}
def start_tool(*, name: str, arguments: str = '', tool_call_id: str = '') -> Tool: ...
```

Start a tool execution within this sub-agent.

Pins the Tool's OTel parent to this SubAgent's span when the SubAgent
has been entered.

### start\_subagent

```python theme={"system"}
def start_subagent(
    *,
    name: str,
    model: str = '',
    set_current: bool = True,
) -> SubAgent: ...
```

Start a nested sub-agent under this one.

Pins the nested SubAgent's OTel parent to this SubAgent's span when
this SubAgent has been entered.

### record

```python theme={"system"}
def record(
    *,
    name: Union[str, None] = None,
    model: Union[str, None] = None,
    system_instructions: Union[list[str], None] = None,
    input_messages: Union[list[Message], None] = None,
    output_messages: Union[list[Message], None] = None,
    tool_name: Union[str, None] = None,
    tool_call_id: Union[str, None] = None,
    tool_call_arguments: Union[str, None] = None,
    tool_call_result: Union[str, None] = None,
    agent_id: Union[str, None] = None,
    agent_description: Union[str, None] = None,
    agent_version: Union[str, None] = None,
) -> SubAgent: ...
```

Set multiple sub-agent fields in one call.

Collapses the per-field assignments a manually-instrumented agent
otherwise makes on a sub-agent (`system_instructions`, `agent_id`,
...) into a single keyword call. Only fields explicitly passed
(non-`None`) are applied; existing values are preserved. Returns
`self` for chaining. Mirrors `Turn.record` / `LLM.record`.

Note: on the streaming (`with`) path the sub-agent span is named
from `name` at `__enter__`, so set `name` via `start_subagent`
/ `turn.subagent` rather than `record` if you need the span name
to reflect it; `record` still updates the `gen_ai.agent.name`
attribute.

### end

```python theme={"system"}
def end() -> None: ...
```

### start

```python theme={"system"}
def start(*, set_current: bool = True) -> Self: ...
```

Start this sub-agent's span. `__enter__` without the `with`.

Pass `set_current=False` to `start_subagent` when sub-agents can be in flight
concurrently. `end()` detaches via `ContextVar.reset`, which
silently corrupts the ambient context stack when overlapping spans
end out of LIFO order; the surviving sibling stops being current,
and the last detach restores an already-ended span. Children created
through `start_llm` / `start_tool` / `start_subagent` nest under
this span either way, because those factories thread an explicit
parent context.

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
