# Batch logging

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/batch-logging

# Batch logging

> Emit complete turns and conversations after the fact with log_turn and log_conversation.

Access these through the `tracing` module:

```python theme={"system"}
from coreweave.forge.agentlens import tracing
```

## log\_turn

```python theme={"system"}
def log_turn(
    *,
    conversation_id: str,
    agent_name: str = '',
    conversation_name: str = '',
    model: str = '',
    agent_id: str = '',
    agent_description: str = '',
    agent_version: str = '',
    messages: Union[list[Message], None] = None,
    output_messages: Union[list[Message], None] = None,
    system_instructions: Union[list[str], None] = None,
    spans: Union[list[Union[LLM, Tool, SubAgent]], None] = None,
    started_at: Union[datetime, None] = None,
    ended_at: Union[datetime, None] = None,
    include_content: bool = True,
    continue_parent_trace: bool = False,
    attributes: Attributes = None,
) -> LogResult: ...
```

Imperatively emit one turn and its child spans to OTel.

Use when context managers aren't viable (stateless containers, callbacks,
queue workers). Each child span passed in should have `started_at` /
`ended_at` set; the emitted OTel span timestamps come from those fields.
Falls back to the earliest/latest child timestamp, then `now()`, when
the turn doesn't supply its own. `agent_id` / `agent_description` /
`agent_version` mirror the streaming path.

`attributes` are stamped on every emitted span; the streaming path reads
these from the active conversation instead. Use custom, non-semconv keys: a
key that collides with a span's own `gen_ai.*` / `weave.*` attribute
is unsupported (which value wins is path-dependent).

`messages` records the turn input and `output_messages` records the
terminal agent response on the same `invoke_agent` span.

## log\_conversation

```python theme={"system"}
def log_conversation(
    *,
    turns: list[Turn],
    conversation_id: str = '',
    conversation_name: str = '',
    agent_name: str = '',
    model: str = '',
    agent_id: str = '',
    agent_description: str = '',
    agent_version: str = '',
    include_content: bool = True,
    continue_parent_trace: bool = False,
    attributes: Attributes = None,
) -> LogResult: ...
```

Imperatively emit a complete conversation.

Each Turn's `.spans` attribute provides its children. Auto-generates
`conversation_id` if empty. By default each turn gets its own OTel trace.
`agent_name` / `model` / `agent_id` / `agent_description` /
`agent_version` are conversation-level defaults. A Turn's own value wins;
the conversation value only fills in when the Turn leaves it empty. The
conversation's `continue_parent_trace` applies to every turn and
supersedes the per-Turn value.

`attributes` are stamped on every emitted span. Use custom, non-semconv
keys: a key that collides with a span's own `gen_ai.*` / `weave.*`
attribute is unsupported (which value wins is path-dependent).

## LogResult

```python theme={"system"}
class LogResult(BaseModel): ...
```

Result of a batch log\_\* call.

`LogResult` is a Pydantic model. Set any field below as a keyword argument when you construct it.

**Fields**

| Field | Type | Default |
| - | - | - |
| `conversation_id` | `str` | `''` |
| `trace_ids` | `list[str]` | `[]` |
| `root_span_ids` | `list[str]` | `[]` |
| `span_count` | `int` | `0` |
