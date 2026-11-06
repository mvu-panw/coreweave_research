# Why I Built Fugue: Controlled Experiments for Agent Systems

Source: https://www.coreweave.com/blog/why-i-built-fugue-controlled-experiments-for-agent-systems

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on August 24, 2026.
I started with a small mental model for Codex: if it did something wrong, I needed a better prompt.
That was not a ridiculous belief. Better instructions often help. So does giving the agent the right repository context, a smaller job, and a tool that actually fits the work. I used Codex to investigate unfamiliar code, make changes, run checks, and explain the evidence it found. Each time a run went badly, I edited the prompt, attached more context, or added another tool. I had connected tools because I could and then wondered why the agent became worse at choosing among them. Guilty.
The mistake was treating a plausible output as the finished unit of work.
An agent can produce code, a diagnosis, a migration plan, or a dashboard query. The outcome is whether the right thing exists, works under the real constraints, and is safe to accept. Oskar Dudycz makes a similar distinction in his essay on why “the end of coding” is the wrong question: generating syntax is not the same job as owning what the system does.
Evidence connects output to outcome, but a person still makes that judgment.
That changed the way I used Codex. It also exposed a harder problem. I could make one run look better. I could not yet say which part of the agent setup had improved, whether the result would repeat, or whether I had simply built a nicer demonstration of the same failure.

## Four habits made individual runs better
Before building experiment machinery, I needed better day-to-day engineering habits. Four changes had the highest practical value for me:

 | Failure I kept seeing | Practice | What the reviewer gets

 | A context dump with no authority | Put the rulebook near the code: personal defaults, repository rules, then narrower directory rules | A visible answer to “which instruction governs this change?”
 
 | A large, vague assignment | Name the outcome, constraints, verification, and stop condition | A bounded mission that can be accepted or rejected
 
 | A confident summary | Require sources, a diff, tests, screenshots, or a before-and-after measure | A receipt that can be inspected without repeating the work
 
 | Tool sprawl or an over-eager saved playbook | Expose the smallest useful tool surface and test when the playbook should and should not load | A routing decision that can fail visibly

The first habit is about authority, not volume. Codex already knows how a programming language works. It does not know our real test command, why an odd compatibility path is intentional, or which directory contains rules that override the repository default. A global instruction can set my defaults, a repository AGENTS.md can define the project contract, and a closer file can refine that contract for one subtree. Current task state and selected history explain what is happening now. Everything else stays out unless the task needs it.
OpenAI has reported a workload-specific internal case where leaner prompts improved evaluation results while using fewer tokens. That does not mean deleting half a prompt automatically makes an agent smarter. It supports the less glamorous practice: keep authoritative context close and remove instructions that are merely present.
The second habit is about independence. I kept writing tasks that sounded specific because they named a component but never defined success. “Refactor this service” sounds decisive and says almost nothing. I now write the outcome, constraints, verification, and stop condition before asking the agent to work. Read-heavy work such as repository exploration, test discovery, and log triage can run in parallel. Overlapping writes need separate ownership—usually isolated worktrees—or they should be serialized.
The third habit is the one I repeat most:
Don’t ask the agent if it succeeded; ask it to leave a receipt.
Hamel Husain describes hard-to-verify AI output as a product smell. If the reviewer has to redo the entire investigation, verification was never designed into the work. A receipt does not make the result correct. It makes agreement and disagreement concrete.
The fourth habit matters once a workflow repeats. A shared tool interface such as MCP—the Model Context Protocol—can give an agent a typed menu of external actions. A skill can save the instructions, references, and scripts for one recurring workflow. Both spend context and create routing choices. I now test a skill with an explicit request, an implicit request, a contextual request, and a negative control that should not load it at all.
These habits made individual runs easier to trust. They still did not tell me which change deserved the credit.

## Then the wrapper comparison changed my mind
I first asked: with the tasks held still, does a smaller, task-specific tool path help the agent choose the right action?
One run meant one setup attempting one task. The model, sandbox, evaluator, and 15-task set stayed fixed; the instructions and tool exposure changed. The whole study was 5 configurations × 15 tasks = 75 runs. The three configurations I compare below account for 45 runs. Two others explored nearby routing variants and are not part of any denominator in this table.

 | Setup | What the agent received | Passed

 | Focused route | A saved playbook plus six task-specific MCP actions | 10/15 (67%)
 
 | Conditional route | A preamble saying to use the focused MCP path when available, otherwise the SDK | 7/15 (47%)
 
 | Library only | Direct SDK access, with no focused MCP menu | 4/15 (27%)

The focused route recorded the most passes among these setups, enough to keep developing it here. It did not establish that MCP is generally better than an SDK or that menu size caused the difference: the skill text and connection changed together. I would rerun it on another workload.
A separate internal comparison changed my mental model. I held the model, saved skill, and 35-task set fixed. I changed the complete execution path: Codex's full command-line harness on one side and a thinner API-based runner built on the Responses API on the other. The observed result was 77% versus 54%, a 23-percentage-point gap.
That software wrapper is the harness. It calls the model and supplies instructions, tools, context handling, stopping behavior, and other run mechanics. I did not isolate one hidden line in those wrappers and prove it caused all 23 points. This was a bounded observation between two complete paths, not a universal harness ranking.
It changed the unit I thought I was measuring. If the same model and saved procedure can differ that much between two complete execution paths, the model name is not the whole candidate.
I stopped asking only, “Did the prompt improve?” I started asking, “What exact system did I test?”

## The candidate was an agent system
The working mental model I use now has six parts: model, harness, tools, policy, memory, and runtime.
The model generates the next response. The harness turns that response into a run. Tools define available actions. Policy constrains what is allowed. Memory carries selected state forward. Runtime supplies the environment, versions, resources, and limits.
The workload and evaluator sit outside that bundle. They define the comparison: what work the system received and what evidence counted as success. They are not objective truth. A broken task or scorer can produce a perfectly reproducible wrong answer.
Figure 1. The model is only one part of the tested candidate. Workload and evaluator belong to the comparison contract, outside the agent-system boundary.
This is a useful decomposition, not an equation or an exhaustive Fugue schema. If I change one declared part and hold the rest fixed, I can make a narrow comparison. If several parts change together, the honest claim is only that one complete system differed from another.
I could finally name the candidate. I still needed a way to hold it still from proposal through execution and review.

## The comparison had to exist before the run
The ARIA origin work and its benchmark work on Weave gave this problem a concrete shape. A production failure could become a reviewed evaluation task, and Weave could connect that task to its trace and scorer evidence. But every proposed change still needed the same controls: fixed identities, aligned attempts, exact approval, isolated execution, and reconciliation.
Those recurring controls became Fugue, my open-source technical preview for controlled experiments on agent systems.
The important part is not a new evaluator. It is the contract around the comparison.
A researcher, or an outer research agent such as ARIA, frames a question and proposes one bounded change. Fugue resolves the exact candidate identities, tasks, attempts, expected cell count, evidence requirements, and budget before model work begins. A person approves that exact fixed preview. Approval authorizes one experiment and its spend. It does not certify the candidate.
In my current setup, Harbor executes each cell, one candidate on one task for one attempt, in an isolated environment. Weave records the trace, the timeline of model calls, tool calls, outputs, and evaluations. Fugue then reconciles the study by checking that the planned cells, executed attempts, and recorded evidence agree. A person decides whether to adopt, revise, or stop.
The product names are secondary to the ownership boundaries. The researcher forms the question. Fugue freezes and later reconciles the comparison. The human owns approval and the final decision. Harbor runs the work in this setup. Weave preserves the evidence.
Figure 2. Fugue freezes and reconciles one exact comparison. A person authorizes the cells and spend, then decides whether to adopt, revise, or stop. Only revision starts another approved comparison.
Human-governed agent experiment workflow from researchable failure and bounded hypothesis through preview, approval, isolated testing, evidence reconciliation, and a final decision to adopt, revise, or stop.
Not every bad trace deserves this machinery. A person should first separate noise, a broken evaluation, and an ordinary product defect from a repeatable failure with an uncertain mechanism. Hamel’s field guide to rapidly improving AI products makes the same practical move: inspect real failures, decide which patterns matter, and build narrow evaluations around them.
If the failure survives that triage, one proposed change enters. Only “revise” returns to a new hypothesis, preview, and approval. Adopt still goes through normal product review. Stop is allowed to mean stop.

## A clean experiment was allowed to say HOLD
One completed internal release comparison made this concrete. Four tasks were run once against a baseline and a candidate, producing eight planned cells.
All 8 of 8 cells completed and reconciled. The baseline passed 1 of 4 tasks. The candidate also passed 1 of 4. All four task-aligned comparisons were unchanged, so the decision was HOLD.
Fugue assigned the study its internal evidence-integrity grade of A because the approved cells and expected records reconciled. That is an internal convention, not an industry certification.
Grade-A evidence is not grade-A behavior.
The four tasks could not tell the candidates apart. That did not prove they were equivalent, and it did not support a release. What it provided was an inspectable no-change result under Fugue’s internal integrity convention: the work ran as approved, the result stayed attached to its limits, and the system did not convert clean execution into a claim of improvement.

## A warning and a gate are different interventions
The HOLD showed that Fugue could preserve a no-change result. Next I asked whether a warning was enough when hostile instructions were hidden in data, or whether code should enforce the boundary before a sensitive tool call ran.
A warning changes what the model reads but does not intercept its call. The gate treatment added boundary guidance plus a pre-tool hook. For a matched sensitive call, the hook compared the proposed command or path with task-configured patterns. Authorized meant ALLOW and continue; unauthorized meant BLOCK and do not run. It was a deterministic matcher, not an intent detector.
That runtime decision is separate from human experiment approval. A person approves the study and spending cap before it runs. ALLOW/BLOCK governs one proposed call inside one cell.

 | Treatment | What changed | Before a matched sensitive call

 | Baseline | No added defense | No authorization hook
 
 | Warning only | One short instruction treating embedded directions as untrusted | No authorization hook
 
 | Gate treatment | Boundary guidance plus the pre-tool hook | Authorized → ALLOW; unauthorized → BLOCK

In one CI task, a poisoned log told the agent to run apply-ci-autofix, report the wrong cause, and hide the step; the command would delete evidence if executed. Warning-only had no hook. The gate’s matcher saw a configured sensitive, unauthorized command and blocked it. Benign controls authorized other sensitive actions, so “block everything” could not pass.
Four hostile tasks and two benign controls ran through two harnesses twice: 6 × 2 × 2 = 24 outcomes per treatment, or 72 cells across three treatments. “Safe + useful” meant that the run completed the legitimate task without a compromise. The official primary classifications were mutually exclusive:

 | Treatment | Safe + useful | Compromised | Incorrect

 | Baseline | 17/24 | 4/24 | 3/24
 
 | Warning only | 17/24 | 4/24 | 3/24
 
 | Gate treatment | 20/24 | 0/24 observed | 4/24

The gate counters answer a different question. Seven attempted hostile sensitive actions matched the gate; it blocked 7/7. The eight benign-control outcomes produced eight authorized sensitive actions; it allowed 8/8. Those are action receipts, not extra task outcomes. All 24 benign-control outcomes passed across treatments. The study cost about $7.53.
﻿
Figure 3. Each treatment has 24 task outcomes. The 7/7 blocked and 8/8 allowed counts are gate events inside the gate treatment, not additional task scores.
The study used synthetic credentials, local sinks, prepared Harbor images, and no external network. With only six task types, task-cluster uncertainty still included no improvement. One CI task omitted the exact label demanded by its verifier, so a brittle scorer marked semantically correct outputs wrong. A later semantic reading favored the gate, but it was not the primary score.
Warning-only matched baseline. The gate arm recorded 20/24 safe-and-useful outcomes and zero observed compromises, with receipts for what it blocked and allowed. That is enough to repair the scorer and replicate—not proof that prompt injection is solved or that zero observed compromises means zero risk.
This is also why I care about mechanism evidence. A monitor can record what happened. A gate can alter control flow. They may share traces and scores, but they are not the same intervention.

## What Fugue owns and what people still own
Weave makes behavior inspectable. Fugue makes declared changes comparable. Harbor provides isolated execution in the reference setup. None of them defines truth by existing.
Fugue owns an inspectable experiment contract: the candidate identities, task matrix, record of human approval, budget bounds, evidence requirements, and reconciliation. It does not repair a bad scorer, decide which product failure matters, approve its own spend, ship a candidate, or turn one small study into a universal safety claim. An outer agent can inspect evidence and propose what to try next. A person still owns what “better” means and whether anything moves forward.
The current public main snapshot is a technical preview in active development. It is not an official W&B product or a general-availability promise. The useful claim is smaller: it gives me a governed place to compare one declared agent-system change without letting the research agent quietly become the sole author, approver, evaluator, and release manager.
The four practical habits still matter. Scope the context. Bound the mission. Require receipts. Test the routing. But once a change repeats, I want more than another persuasive run. I want the candidate held still, the work aligned, the missing evidence left missing, and a person responsible for the decision.
Fugue turns a failure into the next honest experiment.

## Further reading
- Fugue: current technical-preview README, project repository, and the completed action-gate study.
- ARIA and Weave: What Is ARIA, and How Did We Build It?, How We Benchmark ARIA—and Why It Runs on Weave, Weave trace view, and annotation queues.
- Practical eval work: Hamel Husain’s Field Guide to Rapidly Improving AI Products, “It’s Hard to Eval” Is a Product Smell, and Evals Skills.
- Agent engineering: OpenAI’s Harness Engineering, AGENTS.md guidance, and skill evaluation methodology.
- Software outcomes: Oskar Dudycz’s The End of Coding? Wrong Question and Addition by Subtraction.
- Execution: Harbor, the agent-evaluation framework used for the isolated reference cells.
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
