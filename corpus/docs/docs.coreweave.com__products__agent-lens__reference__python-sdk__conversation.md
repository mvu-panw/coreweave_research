# Conversation

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/conversation

# Conversation

> The Conversation class groups turns under one conversation ID.

```python theme={"system"}
class Conversation(BaseModel): ...
```

A conversation. Groups turns by conversation\_id (no span).

`continue_parent_trace` controls trace isolation for the turns this
conversation creates. Default `False` means each turn starts its own OTel
trace (the right choice for the standalone Conversations tab view). Set `True`
when the application has an outer trace (for example a fastapi-instrumented
request) that should contain the agent invocation.

`Conversation` is a Pydantic model. Set any field below as a keyword argument when you construct it.

`Conversation` is a context manager and can be used in a `with` statement.

## Fields

| Field | Type | Default | Description |
| - | - | - | - |
| `conversation_id` | `str` | `''` | |
| `conversation_name` | `str` | `''` | |
| `agent_name` | `str` | `''` | Conversation-level defaults each turn inherits (its own value wins). system\_instructions is excluded; it varies per turn. |
| `model` | `str` | `''` | |
| `agent_id` | `str` | `''` | |
| `agent_description` | `str` | `''` | |
| `agent_version` | `str` | `''` | |
| `include_content` | `bool` | `True` | |
| `continue_parent_trace` | `bool` | `False` | |
| `attributes` | `dict[str, Any]` | `{}` | Attributes stamped on every span this conversation emits. |

## Methods

### start\_turn

```python theme={"system"}
def start_turn(
    *,
    user_message: str = '',
    model: str = '',
    agent_name: str = '',
    agent_id: str = '',
    agent_description: str = '',
    agent_version: str = '',
    system_instructions: Union[list[str], None] = None,
) -> Turn: ...
```

Create and start a turn. Auto-ends the previous turn if still open.

Sets the `_current_turn` contextvar so the turn is visible via
`get_current_turn()` regardless of whether a context manager is used.
Each of `agent_name` / `model` / `agent_id` / `agent_description`
/ `agent_version` falls back to the conversation's default when left
empty; `continue_parent_trace` is inherited. Override any of them later
via `turn.record(...)`.

`system_instructions` (the agent's system prompt) is carried on the
turn's invoke\_agent span; it can also be set later via attribute
assignment on the returned `Turn`, mirroring `start_llm`.

### end

```python theme={"system"}
def end() -> None: ...
```
