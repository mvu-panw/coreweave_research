# Agentic workflows in production: Mechanisms, costs and trade-offs

Source: https://www.coreweave.com/blog/agentic-workflows-in-production-mechanisms-trade-offs-costs-and-design-patterns

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on July 22, 2026.
Most teams can get an agent to complete a task once. Getting the same agent to complete that task on the 100th identical request, at a cost you can forecast, with a trace you can read when it fails, is a different engineering problem. That gap between a working demo and an operable system is what this article is about.
The path runs through mechanisms, trade-offs, design patterns, and economics, with optimization treated as a thread through all of them rather than a footnote. We will start with where agentic workflows came from, because the current design consensus is largely a set of corrections to specific failures from 2023, and knowing which failure each pattern answers makes the patterns much easier to apply. From there: the execution loop, context engineering as the central optimization discipline, what agentic workflows actually cost in production with published numbers, how architecture choice changes those costs by an order of magnitude, how to evaluate trajectories rather than answers, and when to not build an agent at all.
Wherever a claim depends on a specific benchmark, product, or platform, it links to a primary source. This part of the stack has moved fast enough that a year-old article is actively misleading in places.

## Where agentic workflows came from
The idea of a language model calling external tools predates ChatGPT. In May 2022, AI21 Labs published MRKL Systems, a modular neuro-symbolic architecture in which a language model acts as a router delegating to external expert modules: a calculator, a currency converter, an API. The model did not execute anything. It produced the arguments, and the surrounding program made the call and fed the result back. That division of labor, where the model decides and the harness executes, is still the correct mental model for a production agent.
Two 2023 papers turned the idea into a usable pattern. Toolformer showed a model could learn in a largely self-supervised way when to call a tool, which one, and how to fold the result back in. ReAct interleaved explicit reasoning with concrete actions and environment observations, producing the thought, act, observe cycle still underneath most production agents. Reflexion added self-critique, where a failing agent wrote a verbal lesson into memory and conditioned its next attempt on it, achieving something like learning from failure without touching weights.
Then came the autonomous agent wave, and it is worth being precise about what went wrong, because the industry still designs against it. AutoGPT arrived in March 2023 and BabyAGI in April, both wrapping a strong model in an open-ended loop and pointing it at a goal. They were spectacularly popular and did not work. The failures were specific: agents looped forever because termination criteria were vague and the model always found one more improvement; they lost track of completed work because memory was too thin to prevent replanning in circles; they burned unbounded API budget because nothing capped spend; and they never asked clarifying questions, instead assuming capabilities they lacked and proceeding on bad premises.
Compare that list to the current production consensus. Explicit termination conditions. Hard step and budget limits. Structured state that survives turns. Escalation to a human as a designed outcome. Typed tool contracts so an agent cannot invent a capability. None of this is aesthetic preference. Each item is a scar.
The years since split into 2 more phases. Through 2024 the answer was structure - graph-based frameworks, explicit state machines, orchestration libraries that made control flow inspectable rather than emergent. Since roughly 2025, 2 forces changed the picture again. Models became strong enough at tool use and multistep reasoning that scaffolding which once required chained prompts now happens inside fewer, more capable turns; METR's measurements found that the length of tasks agents can complete autonomously at 50 percent reliability has been doubling roughly every seven months. At the same time the orchestration layer built for coding agents generalized into a standard application abstraction. Weights & Biases describes this as the arrival of the harness era, where the harness itself is commoditized and business-specific value moves into skills, prompts, and tools, with a shared data model of sessions made of turns, and turns made of steps.
From tool-calling models to production agent systems
The history matters for a practical reason. The hard part was never getting a model to decide what to do next. The hard part is bounding, observing, and paying for what happens after it decides.

## What agentic workflows are
A workflow is a sequence of steps toward a goal. An agentic workflow is a workflow where one or more agents decide some of those steps at runtime instead of following a fully prewritten path. That is the entire distinction. The agent chooses the next action based on what it just observed, rather than executing a fixed script.
Agentic does not mean unconstrained. A production agentic workflow is bounded by explicit goals, policies, tool contracts, state, budgets, and success criteria, and the agent selects among allowed actions as conditions change. It helps to separate two ideas that often get merged. An AI agent is the actor: a model plus its instructions, tools, and decision logic. An agentic workflow is the larger system composing agents with tools, memory, orchestration, and feedback into something that reaches a goal and reports what it did.
Take support triage. A ticket arrives, the agent reads it, decides whether it needs the billing system or the account system, pulls the record, checks whether the issue matches a known pattern, and either drafts a resolution or routes to a human. No two tickets follow an identical path, but every path is assembled from the same bounded set of tools and rules.

### How agentic workflows differ from RPA, traditional AI workflows, chatbots, and AI agents
These categories blur at the edges, and the blurring causes real architectural mistakes. Robotic process automation runs known steps in a fixed order and breaks when the interface or data shifts. Traditional AI workflows call models inside a predefined pipeline, so a model might classify or extract, but the path is fixed in advance. Chatbots manage dialogue and answer from a model or retrieval index without taking consequential actions. Agentic workflows add runtime planning and tool use, so the path changes based on observations, errors, retrieved evidence, or a constraint learned midway.

The last row is the one teams underestimate, and the rest of this article keeps returning to it. RPA and fixed pipelines have a cost per unit of work you can put in a spreadsheet. An agentic workflow has a cost distribution with a long tail, and the tail is where budgets die.

## The execution loop: plan, act, observe, reflect
The central mechanism is a bounded control loop. The agent forms a plan, chooses an action, calls a tool or model, observes the result, updates state, reflects on progress, and continues or stops. Production systems make this loop explicit, because autonomy hidden inside a framework cannot be tested, debugged, or budgeted.

Several things must be explicit for the loop to be operable. A state object carries the plan, observations, and remaining budget. Typed tool schemas define what each action accepts and returns. A retry policy, loop limit, per-step timeout, cost budget, and termination conditions decide when the agent stops, and whether it stopped because it succeeded, gave up, or escalated.

## Framework-independent, the loop looks like this
state = init_state(task, budget)

while not state.done and state.budget_ok():
 plan = agent.plan(state) # decide the next action
 action = plan.next_action

 if action.needs_approval: # gate irreversible actions
 await human_approval(action, state)

 result = tools.call(action) # typed call, validated I/O
 state.observe(result) # append observation to state
 state.spend(result.cost, result.latency)

 if agent.should_reflect(state): # bounded self-check
 state = agent.reflect(state) # revise plan or drop hypothesis

 state.check_termination() # success, give up, or escalate

return state.summary()

Writing the loop this way matters because every stage maps to something observable. Each plan is an inspectable decision, each tools.call a typed action with cost and latency, each observe the evidence the next decision rested on. When an agent misbehaves you want to see which observation produced which plan, not read a stack trace. 
This is the gap agent observability tools exist to close, and it is worth a short brief if you have not used one. Weave is the toolkit from Weights & Biases for developing, debugging, and monitoring AI applications. The core idea is that you instrument the functions you care about and it records what happened inside them. In Python that means calling weave.init("your-project") once and adding a @weave.op decorator to the functions you want tracked, after which Weave captures the inputs, outputs, code, token counts, and costs of each call, and nests child calls under their parents so a multistep run reads as a tree rather than a flat log. Calls to common model providers and frameworks are picked up automatically, and anything else can be wrapped with the same decorator.
import weave

weave.init("incident-response-agent")

@weave.op # each decorated function becomes a step
def query_logs(service: str, window: str) -> dict:
 ...

@weave.op
def run_agent(alert: dict) -> dict: # parent call, children nest underneath
 plan = agent.plan(alert)
 logs = query_logs(alert["service"], "15m")
 ...

What you get back is the trajectory, for the incident agent above, the alert that came in, the hypothesis it formed, the log query it ran, what came back, and why it moved to the next hypothesis, each with its own latency and token cost. That is the view you need at 3am when the agent restarted the wrong worker, and it is the reason agent-native tracing models runs as sessions, turns, and steps rather than as request logs.
Weave Trace2
The graph view shows hierarchical relationships between ops. This is helpful for understanding parent/child relationships.
There is also a cost structure hiding in this loop that shapes everything below. Every iteration resends the accumulated context: system prompt, tool schemas, conversation history, and every prior tool result. A ten-step agent does not make ten small calls. It makes ten increasingly large ones.
💡 Read more about Weave Trace here - https://docs.wandb.ai/weave/guides/tracking/trace-tree
‍

### How agentic workflows handle complex, multistep, and adaptive tasks
Consider an on-call agent responding to a production alert - elevated error rate on a service, cause unknown. Rather than guessing at a fix, the agent pulls recent logs and metrics, forms a hypothesis, and checks a second signal to confirm or rule it out. If the evidence does not fit, it drops that hypothesis and checks the next most likely cause. The agent narrows uncertainty one step at a time instead of asking a single prompt to diagnose everything at once.

Decomposition earns its keep because the agent cannot know up front whether it is a deploy regression, resource exhaustion, or an upstream failure. Each has a different fix and guessing wrong is expensive. Each step maps to a concrete tool call - query a metrics and logs backend, search a runbook or vector index of past incidents, check a dependency's health endpoint, open or update a ticket, page a human.
What separates this from a fixed runbook script is what happens when a check fails. If the 2nd signal contradicts the hypothesis, the agent abandons it rather than forcing the theory. If the alert lacks context, for example no affected service is tagged, the agent requests it or checks a fallback source rather than assuming. That single behavior, asking instead of assuming, is a direct lesson from the AutoGPT era. Escalation is a first-class outcome, not a failure: when hypotheses or budget run out, the agent escalates with a summary of what it checked and ruled out.

## Core components of production agentic workflows
A production agentic workflow is more than a prompt in a loop. It needs an agent policy, a model, typed tool interfaces, prompts, state management, short-term memory, long-term memory, feedback mechanisms, orchestration, integrations with the systems where actions land, and evaluation. Each has a distinct failure mode, which is the argument for keeping them separable rather than fused into one opaque call.

Prompt engineering here is interface design. System instructions, tool descriptions, response schemas, refusal rules, and worked examples constrain what the agent can do and how it reports what it did. A vague tool description produces malformed tool calls the same way a vague API doc produces bad client code.
A useful test for frameworks, they help only when they expose state, tool calls, retries, and traces. If a framework hides those behind convenience, the convenience is a production liability.

### Memory design: short-term state, long-term knowledge, and retrieval
Memory makes an agentic workflow adaptive only when scoped deliberately. Short-term memory is task-local: conversation history, scratchpad, current plan, tool observations, budget state. Long-term memory is persisted knowledge outliving a run: user preferences, prior resolutions, embeddings, structured facts, summaries, and outcomes.
Long-term memory enables adaptivity and personalization, and it is where quiet failures accumulate. Uncurated memory preserves errors and leaks sensitive data into future runs. A wrong resolution written after a failed task becomes tomorrow's confidently retrieved context. So the memory needs a write policy as explicit as any other contract. What may be stored, who may read it, retention period, summarization rules, retrieval strategy, and a deletion path. Adopt one rule early, do not write to long-term memory on failed or escalated tasks by default, since those trajectories are the most likely to encode a mistake.
Managed platforms have converged on this shape. Some platforms managed memory strategy handling extraction and consolidation automatically alongside a self-managed strategy for teams needing pipeline control, with episodic memory so agents accumulate experience across sessions. Whatever the backend, treat memory changes like schema migrations: evaluate with replay tests, ablations, and trace review before enabling writes in production.

## Context engineering: the attention budget and how to spend it
If one discipline separates teams shipping reliable agents from teams fighting them, it is context engineering. Prompt engineering asks how to word an instruction. Context engineering asks what tokens should occupy the window at every moment of a multistep run, and what should be evicted, compressed, or delegated elsewhere.
The reason is empirical. Anthropic's guidance on effective context engineering frames context as a finite resource with diminishing marginal returns, drawing on context rot: as token count grows, a model's ability to accurately recall information from that window degrades. The effect appears across models and follows from the architecture, since every token attends to every other token and relationships grow quadratically. The practical framing is an attention budget, and every token spends some of it.
This reframes a lot of design. Longer context windows are not a solution to context pressure, they are more rope.

The techniques that work are about curation:
- Tool scoping: Every tool definition costs tokens and adds distraction. Expose the smallest set of well-described tools the task needs. Bloated tool lists pull attention from the work and raise error rates, and most agent builds ship with far fewer tools than the first draft proposed.g
- Just-in-time retrieval: Rather than preloading everything the agent might need, keep lightweight identifiers in context and load details at runtime when a step requires them.
- Compaction: When the window fills, summarize older turns into compressed state and replace the raw history. Anthropic reports internal evaluations where context editing alone delivered a substantial performance lift, with a larger gain combined with a memory tool, and large token reductions on long multi-turn evaluations that would otherwise fail from context exhaustion.
- Structured note-taking: Let the agent write durable notes to a scratchpad or file and read them back, so key decisions survive compaction.
- Sub-agent isolation: Give a specialist a clean context window and return only a condensed summary to the lead agent. In Anthropic's multi-agent research system, subagents operate with isolated windows and hand back summaries on the order of one to two thousand tokens.
For the incident-response agent this is quite fixed. Raw log output is the single largest threat to that agent's context. A naive implementation dumps thousands of log lines into the window on the first tool call and reasons badly for the rest of the run. A context-engineered version has the log tool return a bounded structured summary with an identifier for the full result, writes its hypothesis to a scratchpad, and pulls the full payload only when a step requires it.

## What agentic workflows actually cost in production
Cost is where most agentic projects actually fail, and it is usually treated as an afterthought. Gartner predicted in June 2025 that over 40% of agentic AI projects would be canceled by the end of 2027, naming escalating costs, unclear business value, and inadequate risk controls. Model capability is not on that list. The failures are economic and managerial.

### Why agents cost what they do
The cost driver is the loop resending accumulated context. Anthropic's reported figures give the shape - agent interactions use roughly 4x times the tokens of a chat interaction, and multi-agent systems roughly 15x. Agent workloads routinely run input-to-output token ratios of 100:1 or worse, which means agentic cost is an input-token problem, not an output-token problem, and most intuitions built on chatbot pricing are wrong by an order of magnitude.
Let us work through a concrete support triage agent to see the mechanics. Assume a 6,000-token system prompt with tool schemas, 8 steps, roughly 1,500 tokens of tool result and reasoning added per step, and 300 output tokens per step. Input per turn is 6,000 plus 1,500 for each prior step, so the run totals about 90,000 input tokens and 2,400 output tokens. At representative frontier pricing of $3 per million input and $15 per million output, that is about $0.27 of input and $0.04 of output, roughly $0.31 per task.
Compare that to a single classification call using the same system prompt, about $0.02. The agent costs roughly 14x for a single call for the same nominal job, and the entire difference is context resent across turns.

Cache the stable system prompt at a typical cache-read rate of one tenth of base input and the same run drops to roughly $0.18, about a 42 percent reduction, which lands squarely inside the measured range discussed below. At 100,000 tasks per month that single change is worth about $13,000.

### Cost per successful task is the only honest metric
Cost per call flatters agents. If the triage agent succeeds 70 percent of the time and failures are retried once, the effective cost per successful task is materially higher than the per-run figure, and failed runs consume full token budgets before failing. A benchmark or dashboard ignoring failed runs will always make agents look cheaper than they are.
This is why the pass^k results matter economically and not just technically. An agent at 60% single-attempt success and 25 percent consistency across repeated attempts has a cost per reliably-completed task several times its headline number.
The same effect appears in published benchmark data. On a SWE-bench verified subset in the Holistic Agent Leaderboard, several configurations reached identical accuracy of 54.0% at wildly different costs, from about $259 to about $1,790 for the same task set. Identical accuracy, roughly seven times the spend. Without a cost axis, a leaderboard cannot tell you which of those to deploy, and most leaderboards still do not have one.

### Published cost frontiers
A few reference points, all with cost reported alongside accuracy:

Two patterns here are worth noting
- First, the accuracy-to-cost curve flattens hard at the top. In the deep research numbers, moving from low to high effort on the same frontier model bought under two accuracy points for more than double the cost.
- Second, the spread between workhorse and frontier models on coding tasks was roughly sixty times the cost for three or four index points. Whether that trade is worth it depends entirely on what a wrong answer costs you, which is a business question rather than an engineering one.
There is also a documented cliff when budgets get tight. In TestEvo-Bench, capping per-task spend at $1 dropped one agent's success rate on test generation from 70.6% to 44.2%, and another from 59.5% to 18.8%. Budget caps are a real control, and they are not free. Agents differ substantially in how gracefully they degrade under them, which is worth measuring before you set caps in production.

### The costs that are not tokens
Token spend is the visible part. Production budgets also carry tool and API call costs, which for search-heavy or data-heavy agents can rival inference; retrieval and vector database infrastructure; trace storage and observability, which scales with trajectory volume and verbosity; evaluation costs, since LLM-as-judge scoring is itself inference; human escalation handling, which is often the largest true unit cost when an agent routes to a person; and the engineering time to maintain tool contracts as underlying systems change.
A useful discipline, instrument cost per task in the trace from day one, tagged by outcome, so you can compute cost per successful task, cost per escalation, and the cost distribution rather than the mean. The tail matters more than the average. Agents that recursively spawn subagents or hit retry storms produce runs that cost orders of magnitude more than the median, and without per-run caps those runs are unbounded.

## Matching architecture to use case: how design choices move cost and performance
The choice of agentic architecture changes cost and performance far more than the choice of model, and the correct architecture is a function of task shape. The single most useful question is does the task decompose into independent branches, or does it form a dependency chain where each decision constrains the next?

### Model-tier orchestration is the best-documented cost win
The strongest published evidence for architecture-driven savings is model-tier orchestration, an expensive model plans and delegates, cheap models execute. Anthropic reported in its multi-agent documentation that on BrowseComp, an orchestrator model delegating to cheaper worker sub-agents reached 96% of the all-frontier configuration's performance at 46% of the cost, specifically 86.8% accuracy at $18.53 per problem against 90.8% at $40.56. The inverse pattern, where a cheaper executor consults an expensive advisor, landed around 92% of performance at roughly 63 percent of cost on a coding benchmark.
That first result is worth thinking. It is 4 accuracy points for less than half the bill, published by the vendor whose commercial incentive runs the other direction. The mechanism is simple: the orchestrator only sees plans and summaries, while workers absorb the bulk of the token-heavy reading and writing at the lower rate. Independent estimates of similar fleets, such as one strong orchestrator with several cheaper workers versus a uniform frontier fleet, land in the same neighborhood of roughly 40 percent savings.
2 conditions govern whether the saving holds. Workers must not genuinely need frontier reasoning for their subtasks, or you pay twice through retries. And repeat calls should land on the same worker so each keeps its own warm cache instead of re-paying full price for shared context.

### Cost and performance profiles by use case

The pattern across the table: agentic flexibility should be applied to the minority of traffic that needs it. Most production systems that hit their cost targets do so by classifying first and sending the routine majority down a cheap deterministic path, reserving the full loop for genuinely variable cases. Routing is usually a bigger lever than any per-call optimization, because it changes how many tasks enter the expensive path at all.

## Patterns that work in production
The most reliable agentic patterns are boring in a useful way. Plan explicitly, call tools through schemas, verify outputs, stop on clear criteria. The common set is planning, tool use, reflection, routing, retrieval, verification, retry, and human approval.
Planning decomposes a goal into steps and helps most when the environment is stable enough for a plan to stay valid for several steps. Overplanning is a genuine failure mode in fast-changing environments, because the agent commits to a stale plan and defends it. Tool use is what makes an agent useful beyond text, and it should always come with typed schemas, input validation, authentication, and narrow permissions. Reflection catches real mistakes, but unbounded reflection burns budget and can talk an agent out of a correct answer, so cap it and prefer an external evaluator or deterministic check where one exists.
2 patterns deserve more emphasis than they get. Routing is the cheapest reliability and cost win available. Verification through a deterministic check, schema validation, unit test, or second cheap model is worth more than an extra round of self-reflection, because it introduces information from outside the model's own reasoning.

### Multiagent collaboration without coordination collapse
Multiagent workflows scale only when collaboration runs through interfaces rather than open-ended conversation. With explicit roles, inputs, outputs, shared state, budgets, and escalation rules, adding agents adds capacity. Without them, it adds hidden dependencies, nondeterministic loops, duplicated tool calls, and failures that are hard to attribute.
The field has a useful disagreement here worth understanding rather than picking sides on. Anthropic reported that a multi-agent research system with a lead agent and subagents outperformed a single-agent configuration by 90.2 percent on its internal research evaluation, while also reporting the roughly 15x token multiplier and noting that token usage explained most of the performance variance. Cognition argued close to the opposite in "Don't Build Multi-Agents", agents acting on partial context make conflicting decisions a later step must reconcile, so a single continuous thread produces more coherent results.
Both are right about different task shapes. Anthropic's task was breadth-first research where subtasks are genuinely independent and the answer's value justifies the token bill. Cognition's was writing code, where each decision constrains the next and a parallel agent is a second author who never read the first author's reasoning.
Two cautions follow. So before attributing a quality gain to coordination, rule out that you simply spent more tokens; a fair comparison controls for budget. And reliability compounds badly across hops which is a ten-step chain at 95% per-step reliability is only about 60% reliable end to end, and every additional agent adds hops.

‍
Treat agents like services. A role, a contract, a versioned prompt, a permission scope, and its own evaluation. For shared state, blackboard or graph-state designs work when several agents truly need a common view, but prefer message passing over a global mutable context.
💡

## Optimizing agentic workflows layer by layer
Optimization is not one activity. It is four layers with different iteration speeds, costs, and risks, and the highest-leverage work is usually in the middle two.

The context layer is covered above and usually returns the most per hour spent, because agent workloads are dominated by input tokens.
The caching layer is where measured savings are largest and most underexploited. Prompt caching reuses computed key-value tensors behind a repeated prefix so providers skip prefill for content already processed. A systematic evaluation across three major providers on a multi-turn research benchmark found prompt caching reduced API costs by 41 to 80% and improved time to first token by 13 to 31%, with savings scaling by prompt size to nearly 90 percent at 50,000-token prompts.
The counterintuitive finding in that work directly shapes how you should structure an agent. Naive full-context caching is not the best strategy. Caching only the stable system prompt was most consistent across both cost and latency, because full-context caching triggers cache writes for dynamic tool calls and results that will never be reused, adding overhead without corresponding reads. On one model, full-context caching produced a latency regression of roughly 9% while system-prompt-only caching improved latency by about 31%. Cost savings were similar across strategies since the system prompt drives most of the benefit; latency is where strategy choice shows up.

The practical rules are specific. Keep the cacheable prefix stable, so no timestamps, session identifiers, or user-specific strings near the front of a system prompt, since one differing token at the beginning invalidates the whole prefix. Put unavoidable dynamic values at the end of the system prompt. Be careful with dynamic tool discovery, since changing the available tool set between requests invalidates the cached prefix containing tool definitions; a fixed set of general-purpose tools caches far better than a dynamically assembled one. And note that caching discounts input tokens only, so any savings model applying the discount to output spend is wrong.
One real tension deserves naming, because two recommended optimizations fight each other. Compaction and pruning of old tool calls improve context quality, and they break cached prefixes. The resolution most teams reach: keep the system prompt stable and heavily cached, and treat conversation history and tool results as dynamic content managed for context quality rather than cache hits.
The routing layer spends model capability where it changes outcomes, as covered in the architecture section above.
The training layer is slowest and most powerful. When an agent must be reliable at a specific repeated task, post-training beats prompt iteration. ART, the Agent Reinforcement Trainer, wraps Group Relative Policy Optimization behind a developer-facing API with multi-turn rollout support, and W&B Training runs it on a serverless backend so teams can post-train without provisioning GPUs, reporting cost reductions up to 40 percent and roughly 1.4 times faster training by packing jobs to maximize GPU utilization. The usual blocker is reward design; RULER addresses it with an LLM judge ranking multiple trajectories relative to each other, requiring no labeled data or handcrafted reward function, and reported matching or exceeding handcrafted rewards on three of four benchmarks. The strategic point: a smaller fine-tuned model on a narrow, high-volume task can beat a larger prompted one on cost, latency, and reliability at once, which is the rare optimization that does not trade one axis against another.
💡 A sensible order of operations: fix context, then caching, then routing, then consider training, measuring after each. Teams that jump to a bigger model usually find they paid more for a problem that lived in their context.
‍

## Evaluating and debugging agentic workflows
Agentic evaluation has to score trajectories, not just final text. A useful test records the prompt, plan, tool calls, observations, memory reads, cost, latency, and outcome, so a regression can be explained rather than guessed at. Traces become test data.
The most important measurement shift is from single-attempt success to consistency. τ-bench introduced pass^k, the fraction of k independent attempts at the same task that all succeed, and the results are sobering: an agent resolving over 60 percent of retail tasks on a single attempt dropped to roughly 25 percent when required to succeed across eight attempts. A system that looks like a 60 percent performer is closer to one in four measured honestly. If your agent faces real users, the hundredth identical request matters more than the first.
Offline evaluation still matters and has a ceiling: it scores failure modes you already thought of, and the space of valid agent behavior is too wide to anticipate. This is why online evaluation has become central. Weights & Biases made this argument when it rebuilt Weave around production agents, noting that heuristics like latency, token counts, tool-call counts, and error rates catch known problems while online signals cast a wider net by analyzing what agents actually do against real traffic, with newly discovered failure modes then extracted into offline evaluation sets.

Concretely, each piece of Weave maps to a specific problem you hit in this loop.
The first problem is that you cannot debug what you cannot see. A failed agent run leaves you with a final answer and no account of how it got there. Weave Traces solve that by rendering the trajectory as sessions, turns, and steps, so you can walk the run and find the step where it went wrong. Because tracing is built on the OpenTelemetry GenAI semantic conventions, a harness already emitting OpenTelemetry is understood without custom instrumentation.
The second problem is that you cannot tell whether a change helped. Someone edits a prompt, the outputs look different, and nobody can say whether quality moved or which cases regressed. W&B Weave Evaluations address this by pairing a dataset with scorers and aggregating results, so two prompt or model versions can be compared side by side on accuracy, latency, and cost rather than on impressions.
Inside Weave Evaluations - Evaluations compare versions on the same dataset, so a prompt change can be judged on accuracy, latency, and cost instead of impressions.
The third problem is that testing a fix usually means shipping it. You have a failing production trace and a hypothesis, and the only way to check it is to deploy. The Playground closes that loop by replaying a captured trace against a different model or prompt, so you see whether the change fixes that exact case before it reaches users.
Inside Playground - The Playground replays a real failing trace against a different model or prompt, which tests a fix against the exact case that broke.
‍
The fourth problem is that production failures are silent. An agent that is subtly unhelpful, looping, or unsafe does not throw an exception, and nobody files a ticket for an answer that was merely bad. Monitors and Signals watch live traffic and surface those behavioral issues, which is what turns unknown failure modes into dataset rows.

The fifth problem is that some outputs must never reach a user at all. Guardrails apply scorers inline so an unsafe or off-policy output can be flagged or blocked before it becomes an action.
Track trajectory-level metrics: Task success, pass^k consistency, step count, tool-call accuracy, invalid action rate, escalation rate, token cost per task, p50 and p95 latency, policy violations, and user correction rate. A cost per successful task is more honest than cost per call, since a cheap model failing twice before succeeding is not cheap.

## Orchestration tooling and platform selection
Three broad choices solve different problems. Agent frameworks encode control flow. Durable workflow engines handle reliability: retries, checkpoints, long-running state surviving a crash. Managed agent platforms reduce integration work by bundling runtime, memory, tools, and observability, at some cost in flexibility. Choose on failure semantics before framework aesthetics.
On frameworks, LangGraph gives fine control over stateful execution graphs, LlamaIndex leans toward retrieval-heavy agents, and CrewAI is the fastest path to a working multiagent prototype. Two changes are worth flagging because older articles get them wrong. Microsoft merged Semantic Kernel and AutoGen into the Microsoft Agent Framework, which reached 1.0 for Python and .NET in April 2026 with both predecessors in maintenance mode. AWS has open-sourced Strands Agents, and Google's Agent Development Kit is the common way to define agents on its stack. Interoperability runs through the Model Context Protocol for tool access and the Agent2Agent protocol for agent-to-agent communication.
For durability, Temporal, Ray, Airflow, Prefect, and Dagster provide retries, checkpointing, and long-running state a plain agent loop lacks. On managed platforms: OpenAI's Agents SDK and Responses API are the supported path, and the older Assistants API is deprecated with a sunset date of August 26, 2026, so it should not be a target for new work. AWS splits between Bedrock AgentCore, a model-agnostic runtime hosting agents built on any framework, and Bedrock Managed Agents. Google offers Vertex AI Agent Builder and Agent Engine alongside the Agent Development Kit, Microsoft offers the Azure AI Foundry Agent Service, and Anthropic offers the Claude Agent SDK and Claude Managed Agents.‍
💡 The recommendation cutting across all of it: choose the least autonomous architecture that satisfies the task, then add agentic flexibility only where the workflow genuinely needs a runtime decision.
‍

### Infrastructure characteristics for production inference
Agentic workflows stress inference infrastructure differently, for the reason described earlier. A ReAct-style agent making ten tool calls might generate only a few hundred output tokens while consuming hundreds of thousands of input tokens. At input-to-output ratios around 100:1, prefill dominates: the great majority of GPU time per request goes to processing input, not generating output. Generation is not the bottleneck. Context is.
That reorders the infrastructure priority list. KV cache hit rate becomes a first-class operational metric rather than a tuning detail, since a high hit rate directly removes the dominant cost. Paged attention is table stakes in any current serving stack, and prefix caching through vLLM's automatic prefix cache or SGLang's RadixAttention is the strongest server-side lever for self-hosted agents. Beyond caching: autoscaling, request batching, streaming, model routing, GPU memory planning, queue backpressure, timeout handling, rate-limit management, and multi-region reliability.
Self-hosting on vLLM, Text Generation Inference, Triton, or Kubernetes buys operational control, direct cache management, and lower unit cost at scale, at the price of staffing and capacity planning. API providers remove that burden and hand you their caching semantics instead, which means designing prompts around someone else's cache boundaries. Credible options with integrated GPU or managed inference include AWS, Google Cloud, Azure, CoreWeave, Anyscale, and Databricks.
Observability closes the loop. Weights & Biases is now part of CoreWeave, and W&B Inference serves hosted open models that trace into Weave, making the principle concrete. Every inference call should be traceable to cost, latency, model version, prompt version, cache hit status, and final task outcome.

## Trade-offs: accuracy vs latency, cost vs throughput, flexibility vs determinism
Agentic workflows trade determinism for adaptive problem solving, and the right operating point depends on task risk and variability.
Accuracy versus latency comes first: retrieval, planning, reflection, verification, and larger models can raise success rates, and each adds a sequential call. Cost versus throughput follows: agent loops multiply token and GPU usage, so caching, batching, routing, small verifier models, and hard budgets keep load bounded. Flexibility versus determinism is third: free-form planning handles variable tasks, while graphs, schemas, approval gates, and finite-state transitions improve repeatability. Autonomy versus control determines how much sits behind approval gates, and personalization versus privacy is the memory trade-off.
A fifth axis deserves its own line because it is routinely missed: capability versus consistency. The pass^k results show these are different properties. Adding capability does not automatically buy consistency, and consistency is what production requires.

## Failure modes, guardrails, and governance
The hardest failures are valid-looking actions taken in the wrong context. This is now studied rather than folklore. MAST, the Multi-Agent System Failure Taxonomy, was built from more than 1,600 annotated execution traces across seven frameworks with strong inter-annotator agreement, identifying 14 distinct failure modes in three categories: specification and system design issues, inter-agent misalignment, and task verification failures. Roughly 40% of observed failures fall in the first category, around a third in the second, and the remainder in verification.
The distribution is the actionable part. Most failures are not the model being insufficiently smart. They are design failures - ambiguous specification, poor decomposition, unclear roles, missing termination conditions, step repetition, context lost at handoffs, inadequate output checking. The authors note explicitly that improvements in base model capability will be insufficient to address the full taxonomy. If you are waiting for the next model release to fix your agent's reliability, the evidence suggests a long wait, because the bugs are in the system design.
Alongside these, design against prompt injection, tool misuse, stale or poisoned memory, infinite loops, schema drift when a tool contract changes underneath the agent, partial outages, hallucinated tool results, and inconsistent handoffs.
Guardrails belong around actions, not only final text: tool allowlists, authentication scopes, sandboxing, policy checks, budget limits, circuit breakers that trip on retry storms, output validation, and human approval for high-risk or irreversible actions. Policy as code, evaluated outside the agent's reasoning loop before an action reaches a tool, is stronger than asking a model to police itself.
Governance makes this auditable: audit logs of every action, versioned prompts, versioned model configs and tool schemas, artifact lineage, retention rules, access control, and incident review. The edge cases are easy to miss. Nondeterministic evaluations that pass and fail on identical input. Hidden retry storms that quietly multiply cost. Memory writes after a failed task. Agents taking irreversible actions during a partial outage when verification tools are unavailable. Subagents recursively spawning subagents with no per-run cap, which can multiply a task's cost by another order of magnitude.

## When not to use agentic workflows
An agentic workflow is the wrong tool when a deterministic rule, SQL query, classifier, search index, or RPA script solves the task reliably. Agents add latency, cost, nondeterminism, and operational surface area, so they need a real uncertainty or adaptation problem to justify them. Gartner's observation that many use cases positioned as agentic do not require agentic implementations is the same point from the buyer's side.
Several signals should stop you:
- Strict latency or cost environments rarely tolerate multiple model calls, reflection loops, and retries. 
- High-risk workflows without approvals, auditability, rollback paths, policy enforcement, and assigned responsibility should not be handed to an agent. The approach fits poorly when success is ambiguous, when there is no evaluation data, when integrations are too brittle to trust, or when the team cannot monitor and debug traces. 
- The pass^k evidence adds one more - if your task requires near-deterministic consistency and you have no plan to measure it across repeated trials, an agent will disappoint you in production in a way it never did in testing.
The alternatives are a rules engine, a conventional ML service, retrieval-only RAG without autonomous actions, a batch pipeline, a human-in-the-loop queue, or a deterministic workflow engine. Choosing one is not a step down. It is matching the tool to the problem.

## Conclusion
The production question is not whether an agent can complete a task once. It is whether the workflow fails safely, improves under evaluation, and stays inside its latency and cost budgets. Everything in the current design consensus, from explicit termination conditions to typed tools to trajectory evaluation, exists because someone learned the cost of the alternative.
The practical path follows ->
- Start with a narrow, high-variance task where a fixed pipeline genuinely struggles. 
- Implement the minimal loop with plan, tool calls, observations, and budget made explicit, and trace every step with cost attached. 
- Build trajectory evaluations from real cases and measure consistency across repeated runs, not single-attempt success. 
- Optimize in order - context, caching, routing, then post-training. 
- Choose architecture from task shape rather than ambition, and remember that the best-documented cost win available is letting an expensive model plan while cheap models execute. 
- Compare against a deterministic baseline before scaling. If the agent cannot beat that baseline on something you can measure, that is a useful result too, and a much cheaper one to learn now than after launch.
‍

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
min read

### CoreWeave Builds the First Global Backbone Network Purpose-Built for AI

5
min read

### Post-Training at the Frontier

7
min read

### CoreWeave Powers Agentic AI, HPC, and Data Analytics Workloads with NVIDIA HGX Rubin NVL8

5
min read

### Introducing CoreWeave Physical AI Launchables: Run Workloads With One Command

min read

### CoreWeave Zero Trust AI Framework: Your Model. Your Data. Your Trust. 

8
min read

### From Training to Serving: Reflection’s Beam on CoreWeave

min read

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

- Contact us
- Login

### Products
- GPU Compute
- CPU Compute
- Storage Services
- Networking Services
- Managed Services
- Bare Metal Servers
- 
Platform
- Fleet LifeCycle Controller

- Node LifeCycle Controller
- Tensorizer
- Observability

### Solutions
- AI Model Training
- AI Inference
- VFX & Rendering
- Mission Control

### AI Infrastructure

### Why CoreWeave

### Resources
- Customer Stories
- Documentation
- Status
- Pricing
- Resource Center
- Events & Webinars

### About
- About Us
- Careers
- Life at CoreWeave
- 
- Newsroom
- Investors
- Supplier Code of Conduct
- GHG Emissions Statement
- Privacy Policy
- Terms of Service
- 
Do Not Sell or Share My Personal Information

© CoreWeave.
290 W Mt Pleasant Ave
Suite 4100
Livingston, NJ 07039 

- 

- 

CoreWeave Forge,

Copy code

Copied!

CoreWeave Forge,
