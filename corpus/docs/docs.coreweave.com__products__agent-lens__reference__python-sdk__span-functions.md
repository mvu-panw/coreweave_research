# Span functions

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/span-functions

# Span functions

> Module-level functions that start, end, and look up the current conversation, turn, and LLM call.

Access these through the `tracing` module:

```python theme={"system"}
from coreweave.forge.agentlens import tracing
```

## start\_conversation

```python theme={"system"}
def start_conversation(
    *,
    agent_name: str = '',
    model: str = '',
    conversation_id: str = '',
    conversation_name: str = '',
    include_content: bool = True,
    continue_parent_trace: bool = False,
    attributes: Attributes = None,
) -> Conversation: ...
```

Create and activate a conversation. Sets the contextvar for cross-module access.

`attributes` are stamped on every span this conversation emits (for example an
integration identity like `weave.integration.*`). Use custom,
non-semconv keys: set semantic-convention fields via the typed params
(`conversation_name`, `model`, ...). A key that collides with a span's
own `gen_ai.*` / `weave.*` attribute is unsupported; which value
wins is path-dependent (streaming vs `log_turn`).

## start\_turn

```python theme={"system"}
def start_turn(
    *,
    user_message: str = '',
    model: str = '',
    agent_name: str = '',
    system_instructions: Union[list[str], None] = None,
) -> Turn: ...
```

Create and activate a turn. Uses the current conversation if available.

Starts the span and makes it current. Without a conversation, the turn
has no conversation id. Finish with `end_turn()`, `end()`, or `with`.

## start\_llm

```python theme={"system"}
def start_llm(
    *,
    model: str = '',
    provider_name: str = '',
    system_instructions: Union[list[str], None] = None,
) -> LLM: ...
```

Create and activate an LLM call. Uses the current turn if available.

Starts the span and makes it current, even without an active turn.

Pass `provider_name` explicitly. The SDK does not infer it from the
model identifier: prefix-based guessing misattributes user fine-tunes
(for example a model named `text-...`) and bakes assumptions about future
model names into telemetry that's expensive to correct after the fact.

## start\_tool

```python theme={"system"}
def start_tool(*, name: str, arguments: str = '', tool_call_id: str = '') -> Tool: ...
```

Create and start a tool execution span.

The Tool's OTel span automatically becomes a child of whatever span is
current in OTel context; typically a Turn span if one is active. No
explicit turn delegation is needed: parent-child propagation happens
via OTel context, not via the Conversation SDK contextvars.

## start\_subagent

```python theme={"system"}
def start_subagent(
    *,
    name: str,
    model: str = '',
    system_instructions: Union[list[str], None] = None,
    set_current: bool = True,
) -> SubAgent: ...
```

Create and start a sub-agent invocation span.

The SubAgent's OTel span automatically becomes a child of whatever span
is current in OTel context; typically a Turn span if one is active.
Mirrors `start_tool` in shape; OTel context handles parent-child
propagation, no explicit delegation is needed.

## end\_conversation

```python theme={"system"}
def end_conversation() -> None: ...
```

End the current conversation (from contextvar).

## end\_turn

```python theme={"system"}
def end_turn() -> None: ...
```

End the current turn (from contextvar).

## end\_llm

```python theme={"system"}
def end_llm() -> None: ...
```

End the current LLM call (from contextvar).

## get\_current\_conversation

```python theme={"system"}
def get_current_conversation() -> Union[Conversation, None]: ...
```

Return the active conversation from contextvar, or None.

## get\_current\_turn

```python theme={"system"}
def get_current_turn() -> Union[Turn, None]: ...
```

Return the active turn from contextvar, or None.

## get\_current\_llm

```python theme={"system"}
def get_current_llm() -> Union[LLM, None]: ...
```

Return the active LLM call from contextvar, or None.
