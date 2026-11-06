# Set attributes on agent spans

Source: https://docs.coreweave.com/products/agent-lens/tracing/attributes

# Set attributes on agent spans

> Attach custom attributes to agent spans to filter and analyze activity in Agent Lens.

When you instrument an agent with the CoreWeave Forge SDK, each span object (`Turn`, `LLM`, `Tool`, and `SubAgent`) lets you attach custom metadata as attributes. Attributes are key-value properties of a span. Use them to stamp contextual information such as user IDs, tenants, experiment names, or environment labels onto agent spans, and then filter and group agent activity by that metadata in the CoreWeave Agent Lens UI.

You can set attributes on a single span with `set_attributes()` (Python) or `setAttributes()` (TypeScript), or set conversation-wide attributes that apply to every span a conversation emits. `set_attributes` mirrors the [OpenTelemetry (OTel) span API](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes) method `Span.set_attributes`. The Agent Lens SDK emits OTel spans and stores all attributes, so they remain queryable in Agent Lens.

The examples on this page assume you have installed the SDK and initialized it as described in [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md#before-you-begin).

## Set attributes on a span

Use `set_attributes()` (Python) or `setAttributes()` (TypeScript) to stamp arbitrary attributes on a single span. Pass a dictionary or object whether you have one key or many. The method returns the span, so you can chain calls.

> [tab] Python
>
> ```python lines theme={"system"}
> from coreweave.forge.agentlens import tracing
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> with tracing.start_conversation(agent_name="my-agent"):
>     with tracing.start_turn(user_message="What is the weather in Tokyo?") as turn:
>         # Stamp attributes on this turn span
>         turn.set_attributes({"user_id": "12345", "tenant": "acme", "env": "production"})
> ```

> [tab] TypeScript
>
> ```typescript lines theme={"system"}
> import { tracing } from '@coreweave/forge-sdk/agentlens';
>
> await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
>
> await tracing.runIsolated(async () => {
>   const conversation = tracing.startConversation({ agentName: 'my-agent' });
>   const turn = tracing.startTurn({ userMessage: 'What is the weather in Tokyo?' });
>
>   // Stamp attributes on this turn span
>   turn.setAttributes({ user_id: '12345', tenant: 'acme', env: 'production' });
>
>   turn.end();
>   conversation.end();
> });
> ```

The same methods are available on every span class. For example, you can tag an individual tool call or LLM call:

> [tab] Python
>
> ```python lines theme={"system"}
> with tracing.start_turn(user_message="What is the weather in Tokyo?") as turn:
>     with turn.start_tool(name="get_weather") as tool:
>         tool.set_attributes({"weave.display_name": "Weather lookup"})
> ```

> [tab] TypeScript
>
> ```typescript lines theme={"system"}
> const turn = tracing.startTurn({ userMessage: 'What is the weather in Tokyo?' });
> const tool = turn.startTool({ name: 'get_weather' });
>
> tool.setAttributes({ 'weave.display_name': 'Weather lookup' });
>
> tool.end();
> turn.end();
> ```

Most attribute keys are arbitrary custom metadata, but Agent Lens reserves two prefixes for special handling. Keys under `weave.*` map to built-in Agent Lens fields, and keys under `gen_ai.*` map to OpenTelemetry GenAI semantic-convention fields. In the preceding example, `weave.display_name` is a reserved key that sets the span's display name in the Agent Lens UI. For arbitrary metadata that you want to filter and group by, use your own keys such as `user_id` or `tenant`, which Agent Lens stores as filterable custom attributes.

## Record what happens during a span

Attributes can also record something that happens while a span is running, such as a permission prompt or its outcome. Set the attributes when the moment occurs, while the span is still recording:

> [tab] Python
>
> ```python lines theme={"system"}
> with tracing.start_turn(user_message="Delete the old backups.") as turn:
>     turn.set_attributes({"permission.scope": "filesystem.delete"})
>     # ... ask the user and wait for their answer ...
>     turn.set_attributes({"permission.granted": True})
> ```

> [tab] TypeScript
>
> ```typescript lines theme={"system"}
> const turn = tracing.startTurn({ userMessage: 'Delete the old backups.' });
> turn.setAttributes({ 'permission.scope': 'filesystem.delete' });
> // ... ask the user and wait for their answer ...
> turn.setAttributes({ 'permission.granted': true });
> turn.end();
> ```

An attribute records a value, not the time it was set. If you need to know when something happened within a span, record the time as its own attribute, for example `permission.granted_at`.

> [!NOTE]
>
> The SDK's `add_event()` (Python) and `addEvent()` (TypeScript) methods are deprecated, because OpenTelemetry is [deprecating the Span Event API](https://opentelemetry.io/blog/2026/deprecating-span-events/). Record this data with attributes instead.

## Set attributes on every span in a conversation

Stamping attributes one span at a time works well for span-specific metadata, but some metadata applies to an entire conversation. To apply the same attributes to every span a conversation emits, pass `attributes` when you start the conversation. This is useful for propagating conversation-wide metadata such as a deployment name or environment.

> [tab] Python
>
> ```python lines theme={"system"}
> from coreweave.forge.agentlens import tracing
>
> tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")
>
> conversation = tracing.start_conversation(
>     agent_name="my-agent",
>     attributes={"deployment": "canary", "env": "production"},
> )
> # Every turn, LLM, tool, and sub-agent span in this conversation carries these attributes.
> ```

> [tab] TypeScript
>
> ```typescript lines theme={"system"}
> import { tracing } from '@coreweave/forge-sdk/agentlens';
>
> await tracing.init('[YOUR-TEAM]/[YOUR-PROJECT]');
>
> await tracing.runIsolated(async () => {
>   const conversation = tracing.startConversation({
>     agentName: 'my-agent',
>     attributes: { deployment: 'canary', env: 'production' },
>   });
>   // Every turn, LLM, tool, and sub-agent span in this conversation carries these attributes.
> });
> ```

> [!NOTE]
>
> As with per-span attributes, use your own custom keys for conversation attributes. Set semantic-convention fields, such as the agent name, conversation name, or model, through their typed parameters (`agent_name`, `conversation_name`, `model`) rather than through `attributes`. Avoid keys under the reserved `gen_ai.*` and `weave.*` prefixes. Agent Lens extracts those into typed fields during ingestion, so a custom value under a reserved key is unsupported.

## When you can set attributes

Set attributes while the span is recording, that is, after the span starts and before it ends. In Python, this is inside the `with` block. In TypeScript, this is after `start*()` and before `end()`.

If you call `set_attributes()`, or its TypeScript equivalent, on a span that hasn't started yet or has already ended, the call is a no-op and logs a warning that names the fix.

The call is silent (no warning) only when tracing hasn't been initialized.

> [!TIP]
>
> To attach attributes when logging completed agent activity in a single batch rather than during live execution, populate the span object's declared fields directly and pass the object to `log_turn` or `log_conversation`. See [Log agent activity in batches](https://docs.coreweave.com/products/agent-lens/tracing/batch-logging.md).

## View and filter attributes in the UI

Adding attributes is only the first step. Their value comes from using them to analyze agent activity. After you stamp attributes on agent spans, you can filter and group agent conversations by those attributes in the **Conversations** tab of your Agent Lens project. For details, see [View agent activity](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md).
