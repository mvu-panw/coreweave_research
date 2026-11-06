# Trace sub-agents

Source: https://docs.coreweave.com/products/agent-lens/tracing/sub-agents

# Trace sub-agents

> Use Agent Lens's sub-agent span to trace sub-agent delegations and view nested agent invocations.

This guide shows you how to use CoreWeave Agent Lens to trace sub-agents so that delegated agent invocations appear as nested spans in the same trace as the parent turn. Tracing sub-agents lets you see the full hierarchy of an agent's reasoning, including which specialist agents the parent called, what they did, and how they contributed to the final answer. This guide is for developers instrumenting multi-agent systems with Agent Lens.

A sub-agent is a delegated agent invocation that runs inside a turn. Use sub-agents when one agent hands off to another, such as when a supervisor agent dispatches a specialist agent.

When you instrument them with Agent Lens, sub-agents emit a nested `invoke_agent` OpenTelemetry (OTel) span in the same trace as the parent turn. In the **Conversations** tab, this nesting renders as a sub-agent invocation under the turn that triggered it, with its own LLM calls and tool calls grouped beneath.

## Sub-agent data model

Before instrumenting your code, it helps to understand how Agent Lens represents sub-agents in a trace. The `tracing.start_subagent` span maps to the OTel `invoke_agent` span and emits the same operation name as the parent turn. Agent Lens distinguishes the two by their parent-child relationship in the trace:

```plaintext theme={"system"}
Turn (root invoke_agent span)
├── LLM call (chat)              ← parent agent's reasoning
│   └── SubAgent (invoke_agent)  ← delegation happens here
│       ├── LLM call (chat)      ← sub-agent's own LLM call
│       └── Tool call (execute_tool)
└── LLM call (chat)              ← parent agent synthesizes the final answer
```

Sub-agents inherit the active conversation's `conversation_id`, so they're grouped with the rest of the conversation in the **Conversations** tab.

```python lines theme={"system"}
sub = tracing.start_subagent(
    name="research-specialist",   # Required: identifies this sub-agent in the UI.
    model="gpt-4o",               # Optional: defaults to the parent conversation's model if empty.
)
```

`tracing.start_subagent` creates an `invoke_agent` span that automatically becomes a child of whatever span is currently active in OTel context, typically the parent turn or the LLM call that triggered the delegation. OTel context propagation handles the parent-child relationship, so you don't need explicit delegation.

## Trace a single sub-agent

The following example runs a supervisor agent that receives a request and delegates it to a research-specialist sub-agent that uses a Wikipedia search tool to find the answer.

Agent Lens captures the full hierarchy by wrapping the conversation in `tracing.start_conversation` and then a `conversation.start_turn`. Agent Lens then captures the sub-agent trace using the `tracing.start_subagent` block for the specialist, and records each LLM call and tool execution as child spans.

The routing logic is intentionally omitted from these examples to focus on the tracing between agents.

```python lines highlight="6,7,10,16,22,30" theme={"system"}
from coreweave.forge.agentlens import tracing
from coreweave.forge.agentlens.tracing import Message, Usage

tracing.init("[YOUR-TEAM]/[YOUR-PROJECT]")

with tracing.start_conversation(agent_name="supervisor") as conversation:
    with conversation.start_turn(user_message="Research the founders of Anthropic.") as turn:

        # Supervisor LLM call: decide which specialist to delegate to.
        with tracing.start_llm(model="gpt-4o", provider_name="openai") as llm:
            llm.input_messages = [Message(role="user", content="Research the founders of Anthropic.")]
            llm.output("Delegating to the research specialist.")
            llm.usage = Usage(input_tokens=80, output_tokens=10)

        # Delegate to the research specialist as a sub-agent.
        with tracing.start_subagent(name="research-specialist", model="gpt-4o") as sub:
            with sub.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                sub_llm.input_messages = [Message(role="user", content="Find founders of Anthropic.")]
                sub_llm.output("I should search for this.")
                sub_llm.usage = Usage(input_tokens=120, output_tokens=15)

                with tracing.start_tool(name="wikipedia_search", arguments='{"query":"Anthropic"}') as tool:
                    tool.result = "Anthropic was founded by Dario and Daniela Amodei in 2021."

            with sub.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                sub_llm.output("Anthropic was founded by Dario and Daniela Amodei in 2021.")
                sub_llm.usage = Usage(input_tokens=200, output_tokens=25)

        # Back in the supervisor turn: synthesize the final answer.
        with tracing.start_llm(model="gpt-4o", provider_name="openai") as llm:
            llm.output("Anthropic was founded by Dario and Daniela Amodei in 2021.")
            llm.usage = Usage(input_tokens=300, output_tokens=20)
```

In the **Conversations** tab, the sub-agent appears as a nested `invoke_agent` block inside the turn, with its own LLM calls and tool calls grouped beneath. The supervisor's direct LLM calls remain siblings of the sub-agent.

## Trace multiple sub-agents

The following example runs a content-pipeline agent that handles a single request by delegating to three sibling sub-agents in sequence: a `researcher` that gathers facts, a `writer` that drafts the post, and a `reviewer` that polishes the final output.

Agent Lens captures all three sub-agents as siblings under the same turn by opening a separate `tracing.start_subagent` block for each. Because each sub-agent inherits the active turn's OTel context, the sub-agents appear as peer `invoke_agent` spans nested under the turn rather than under each other.

```python lines highlight="1,2,5,11,15,22" theme={"system"}
with tracing.start_conversation(agent_name="content-pipeline") as conversation:
    with conversation.start_turn(user_message="Write a short blog post about Anthropic.") as turn:

        # Researcher sub-agent: gather facts.
        with tracing.start_subagent(name="researcher", model="gpt-4o") as researcher:
            with researcher.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                sub_llm.input_messages = [Message(role="user", content="Find key facts about Anthropic.")]
                sub_llm.output("I should search Wikipedia.")
                sub_llm.usage = Usage(input_tokens=80, output_tokens=15)

                with tracing.start_tool(name="wikipedia_search", arguments='{"query":"Anthropic"}') as tool:
                    tool.result = "Anthropic was founded by Dario and Daniela Amodei in 2021."

        # Writer sub-agent: draft the post.
        with tracing.start_subagent(name="writer", model="gpt-4o") as writer:
            with writer.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                sub_llm.input_messages = [Message(role="user", content="Draft a post using the research.")]
                sub_llm.output("Anthropic, founded in 2021 by Dario and Daniela Amodei, builds AI safety research...")
                sub_llm.usage = Usage(input_tokens=180, output_tokens=120)

        # Reviewer sub-agent: polish the draft.
        with tracing.start_subagent(name="reviewer", model="gpt-4o") as reviewer:
            with reviewer.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                sub_llm.input_messages = [Message(role="user", content="Review and tighten the draft.")]
                sub_llm.output("Final post: Anthropic, founded in 2021 by Dario and Daniela Amodei, builds AI safety research...")
                sub_llm.usage = Usage(input_tokens=200, output_tokens=140)
```

In the **Conversations** tab, the turn contains three sibling sub-agent invocations, each with its own LLM call nested beneath, and the `researcher` includes its tool call. None of the sub-agents are children of each other.

## Trace nested sub-agents

A sub-agent can itself delegate to another sub-agent. Each `start_subagent` call nests under whatever span is currently active in OTel context.

```python lines highlight="1,2,4,5,11,16" theme={"system"}
with tracing.start_conversation(agent_name="orchestrator") as conversation:
    with conversation.start_turn(user_message="Compare Anthropic and OpenAI.") as turn:

        with tracing.start_subagent(name="research-coordinator") as coordinator:
            with tracing.start_subagent(name="anthropic-researcher") as r1:
                with r1.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                    sub_llm.output("Anthropic facts...")
                    sub_llm.usage = Usage(input_tokens=120, output_tokens=30)

                # Nested: the researcher delegates to its own summarizer sub-agent.
                with tracing.start_subagent(name="anthropic-summarizer") as summarizer:
                    with summarizer.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                        sub_llm.output("Anthropic summary: ...")
                        sub_llm.usage = Usage(input_tokens=80, output_tokens=20)

            with tracing.start_subagent(name="openai-researcher") as r2:
                with r2.llm(model="gpt-4o", provider_name="openai") as sub_llm:
                    sub_llm.output("OpenAI facts...")
                    sub_llm.usage = Usage(input_tokens=120, output_tokens=30)
```

The example produces three levels of nesting under the turn:

```plaintext theme={"system"}
turn (invoke_agent)
└── research-coordinator (invoke_agent)
    ├── anthropic-researcher (invoke_agent)
    │   ├── chat
    │   └── anthropic-summarizer (invoke_agent)   ← nested inside anthropic-researcher
    │       └── chat
    └── openai-researcher (invoke_agent)          ← sibling of anthropic-researcher
        └── chat
```

In the **Conversations** tab, `research-coordinator` appears as a sub-agent of the turn, `anthropic-researcher` and `openai-researcher` appear as siblings under the coordinator, and `anthropic-summarizer` appears as a sub-agent of `anthropic-researcher`.
