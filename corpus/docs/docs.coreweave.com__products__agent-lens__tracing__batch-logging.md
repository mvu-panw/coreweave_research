# Batch logging for your agent

Source: https://docs.coreweave.com/products/agent-lens/tracing/batch-logging

# Batch logging for your agent

> Manually log agent traces for frameworks that have already completed the LLM call and need to record it.

For frameworks that have already completed the LLM call and only need to record it, use `tracing.log_turn` and `tracing.log_conversation` from the CoreWeave Forge SDK. All spans are created and ended immediately without keeping any context managers open.

Data logged this way can be historical. No live conversation is needed. Set `conversation_id` to any stable string that uniquely identifies the conversation. Turns that share the same `conversation_id` are grouped as a single conversation in the **Conversations** tab.

If you're building your own agent loop, use the real-time instrumentation APIs described in [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md) instead.

## Log a turn

To record a single completed turn after it happens, use `tracing.log_turn`. It accepts a fully-formed turn, including all LLM and tool spans. Construct the `LLM` and `Tool` objects directly rather than through a `start_*` factory. A directly constructed span doesn't emit anything until you pass it to `log_turn`, so these objects work as plain data.

> [tab] Python
>
> ```python lines highlight="1,2,4,29" theme={"system"}
> from coreweave.forge.agentlens import tracing
> from coreweave.forge.agentlens.tracing import LLM, Message, Tool, Usage
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> llm_span = LLM(
>     model="gpt-4o",
>     provider_name="openai",
>     input_messages=[Message(role="user", content="What is the weather?")],
>     output_messages=[Message(role="assistant", content="Let me check.")],
>     usage=Usage(input_tokens=100, output_tokens=20),
> )
>
> tool_span = Tool(
>     name="get_weather",
>     arguments='{"city": "Tokyo"}',
>     result='"24°C, sunny"',
> )
>
> llm_span2 = LLM(
>     model="gpt-4o",
>     provider_name="openai",
>     input_messages=[Message(role="user", content="What is the weather?")],
>     output_messages=[Message(role="assistant", content="It is 24°C and sunny.")],
>     usage=Usage(input_tokens=150, output_tokens=30),
> )
>
> # Log a turn with all its spans.
> tracing.log_turn(
>     conversation_id="my-conversation-abc",
>     agent_name="weather-bot",
>     messages=[
>         Message(role="user", content="What is the weather in Tokyo?"),
>         Message(role="assistant", content="It is 24°C and sunny in Tokyo."),
>     ],
>     spans=[llm_span, tool_span, llm_span2],
> )
> ```

> [tab] TypeScript
>
> ```plaintext theme={"system"}
> This feature is not available in the TypeScript SDK yet.
> ```

`log_turn` returns a `LogResult` containing the trace IDs of the emitted spans.

An optional `model` parameter on `log_turn` sets the model on the turn's own span, not on the child LLM spans. Each `LLM` span carries its own `model` independently. If a turn uses multiple models, set `model` on `log_turn` to whichever you consider the primary model for that turn.

To record when the turn actually happened rather than when you logged it, pass `started_at` and `ended_at` as timezone-aware `datetime` values.

## Log a conversation

To bulk-import a complete, multi-turn conversation at once, use `tracing.log_conversation`. The `turns` parameter accepts a list of `Turn` objects, each constructed the same way as the spans in the previous `log_turn` example.

> [tab] Python
>
> ```python lines theme={"system"}
> tracing.log_conversation(
>     conversation_id="my-conversation-abc",
>     agent_name="weather-bot",
>     turns=[turn_1, turn_2],
> )
> ```

> [tab] TypeScript
>
> ```plaintext theme={"system"}
> This feature is not available in the TypeScript SDK yet.
> ```
