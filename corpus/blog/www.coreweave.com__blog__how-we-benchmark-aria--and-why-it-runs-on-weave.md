# How We Benchmark ARIA—and Why It Runs on Weave

Source: https://www.coreweave.com/blog/how-we-benchmark-aria--and-why-it-runs-on-weave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on August 24, 2026.
When ARIA gave a bad answer, our first move was often to change the prompt or tool guidance and run the task again. Sometimes the second attempt worked. It was tempting to call the problem fixed.
But a successful rerun only showed that ARIA completed that task once. The change may have helped. The tool may have recovered, the project data may have changed, or the fix may have solved this example while breaking another. The original failure told us what to investigate, not how ARIA had to actually improve.
To answer that broader question, we compare the current ARIA configuration with the proposed version across a reviewed set of tasks. We use Weave because it keeps production observability and evaluation in the same evidence model. The original failure, the offline attempts, their scores, and the underlying model and tool operations stay connected so we could better capture when a candidate ARIA regressed.

## The production failure has to survive the trip
ARIA works inside W&B, where a question already has a project, selected Runs, metrics, artifacts, and page state behind it. A prompt copied into a benchmark file cannot reproduce that job by itself.
Production ARIA runs through the ARIA service. The service stores each user request and the agent work that follows as a durable Turn: the prompt, reconstructable history, configured agent and environment, and the state needed to continue. Production and offline evaluations use the same driver to run a Turn. That keeps the behavior we test aligned with the behavior we can actually ship.
W&B Agent Factory, or WBAF, imports production-aligned ARIA configurations and runs the ARIA-specific tasks, environments, and scorers. The complete path is simple: the ARIA service records the Turn, Weave holds the evidence, WBAF compares the current and proposed configurations, and an accepted change returns to production review before it ships. WBAF does not ship a separate ARIA.
That ownership rule solved a practical problem. ARIA moves quickly, and a benchmark copy can become stale without anybody intending it. We now bind the comparison to the production configuration or exact ARIA change we mean to test. Otherwise we may spend money proving that a candidate beats yesterday's ARIA and learn nothing about the version users have.
The ARIA service can preserve the Turn and sandbox state, but it does not freeze the whole W&B project at that historical moment. New Runs arrive, artifacts change, and services may answer differently later. Exact replay needs immutable references or prepared fixtures for the external data that matters.
Figure 1. WBAF runs the same resolved suite separately for current and proposed ARIA. Weave keeps both evidence records visible, the task and trial rows still have to align, and people retain release authority.
﻿
Even an imperfectly replayable Turn is better than a prompt reconstructed from memory. It gives us the real starting state and makes the remaining drift visible. The next challenge is resisting the urge to simplify that job until the benchmark becomes easy to run and irrelevant to the product.

## The task has to resemble the job
An ARIA evaluation task contains more than a question. Some failures depend on the page the user was viewing. Some need several conversational turns. Some require state before the run and a check afterward. Others are about stopping: an answer that arrives after exhausting the budget may be correct and still miss the product requirement.
The current task inventory roughly falls into four kinds of work:

 Kinds of tasks in the ARIA benchmark
 
 | Kind of task | Examples | What the task has to preserve

 | Find the right evidence | Locate the relevant Runs, artifacts, documentation, or evaluation results; use the page the researcher was already viewing. | Which context ARIA received, which sources it opened, and whether it found the evidence the question required.
 
 | Analyze or debug research | Compare experiments, explain a regression, diagnose a training issue, or propose the next hypothesis. | The connection between the evidence and the conclusion, not only whether the answer sounds plausible.
 
 | Create something in W&B | Build a report or visualization, edit an existing view, or configure a sweep. | Whether the object or action actually exists and whether ARIA avoided forbidden side effects.
 
 | Complete a longer investigation | Work across a large project or carry an analysis through several turns. | State between turns, bounded resource use, and whether ARIA stopped when the job was done.

WBAF tasks can include structured page context, resources, a sandboxed environment, scripted multi-turn interactions, step and time limits, setup, teardown, and must-pass behavior. WBAF can also run supported Codex and Claude Code configurations as baselines, which helps us tell an ARIA-specific regression from a task any capable coding agent can solve under the same conditions.
The checks need the same specificity. If ARIA is asked to create a report, a polished final answer is not proof that the report exists. We use different scorers because they answer different questions:

 Scorer types used to evaluate ARIA
 
 | Scorer | What it checks | When and why we use it

 | Deterministic | Did the report actually exist? Did ARIA trigger a forbidden side effect? | When the result can be inspected directly and does not need a judge.
 
 | Rubric | Was the answer useful, well-supported, or appropriately calibrated? | When quality requires judgment—but only after we compare the judge with human decisions.
 
 | Trajectory | Which evidence and tools did ARIA use along the way? | When a good-looking answer reached by the wrong path is not good enough.
 
 | Reference | Did the result match truth prepared before the run? | When we have a stable answer or artifact to compare against. The reference stays away from the agent.

Those scores can contribute to an overall result, but we still show them separately. A good explanation cannot cancel a deterministic safety failure. Missing cost is not zero cost. A sandbox that dies before the task begins is an infrastructure failure, not a wrong answer. We need to know which failure we saw before we can decide what to change.
As those checks became more specific, the benchmark became more than a list of questions. Each task carried a claim about the behavior we wanted to protect, along with the environment and scoring needed to test it. Adding tasks was easy. Keeping all of them useful was harder.

## The benchmark cannot only grow
There is a satisfying policy where every change runs against every task ever collected. We do not work that way. We run the suite relevant to the capability that changed and use WBAF's wba-all suite when broader regression coverage is appropriate.
We arrived there through accumulation. Our first tasks were easy to explain: find a Run, inspect an Evaluation, explain a regression, create a report. The next tasks came from messier trace patterns. In one kind of case, ARIA found the right Run but never opened the artifact that explained why its metrics changed. In another, it wrote a convincing description of a report without actually creating the report. A third repeated the same broad history query until the Turn ran out of time, even though a narrower read would have answered the question.
Those examples are sanitized composites. To make a production pattern safe for evaluation, we had to reduce it to the behavior we want to test and leave the original conversation and project data out. Related tasks became suites, and soon every unusual trace looked like a candidate for permanent coverage. The benchmark grew faster than our ability to say what each row still protected.
The scope of the benchmark should match the scope of the change. If we change how ARIA uses the page in front of it, we run tasks where that page state affects the answer. If we change how ARIA launches or approves work, we check what it actually did, not only what it said afterward. And when a change touches several parts of the context or tool flow, we widen the run rather than treating it like a documentation edit.
Production failures are one source of new tasks, but they do not enter automatically. A trace may contain private data, describe a transient infrastructure problem, or repeat behavior we already cover. A person decides whether it is safe and useful to study and what correct behavior should mean.
We remove tasks too. Product behavior changes, two tasks turn out to measure the same thing, or a once-difficult task becomes saturated. Keeping everything forever teaches the agent to satisfy a museum of old arguments and makes the result harder to interpret.
The suite can evolve between studies. Once a comparison starts, its candidates, tasks, attempts, runtime, and scoring rules stay fixed. Changing them after seeing the result creates a new experiment.
In practice, that leaves us with a few kinds of suite, each used for a different decision:

 ARIA evaluation suites
 
 | Suite | Why it exists | When we use it

 | aria-pr | A small, hand-authored gate for stable behavior we are not willing to lose. | On ARIA pull requests and in the nightly run, before treating a candidate as ready to ship.
 
 | wba-all and wbax-all | Broad regression coverage across established ARIA behavior and complete research work. | Nightly, and when a change could affect several capabilities rather than one narrow feature.
 
 | Focused capability suites | Isolate behavior such as MCP use, documentation and grounding, report generation, hypotheses, sweeps, or large-project research. | When a change targets one of those capabilities, so we can run the relevant evidence instead of the entire archive.
 
 | guardrails-all | Keep safety and correct action separate from answer quality. | When a change touches actions, data access, privacy, credentials, or another safety boundary.
 
 | Harness and lifecycle smoke suites | Check the runner, stopping limits, setup, teardown, and multi-turn plumbing. | When the harness, sandbox, timeout, or lifecycle code changes. A pass shows that the machinery worked; it does not show that ARIA improved.
 
 | Experimental, quarantine, and demo suites | Develop new tasks, investigate unstable cases, and validate development paths without mixing them into the release signal. | Before a task is stable, while a flaky or sensitive case is under review, or when we are testing the evaluation setup itself. They do not support release claims.

## From one failure to a candidate
When a Turn fails, we first look for the smallest change that might address it. The improvement workflow reads the Weave trace alongside the relevant code and the context used for that Turn. It can suggest one bounded change to the system prompt, a script, or a Skill a package of instructions, references, and scripts for a specific job, then rerun the task as a sanity check. If the evidence points to the service or infrastructure, that becomes engineering work rather than another prompt instruction.
Recurring failures need a wider view. WBAF's nightly triage workflow turns a bounded set of recent production sessions into a versioned Weave dataset, then checks for infrastructure problems, user frustration, security risk, and deterministic policy signals. Explicit user feedback stays separate from the judge-derived rates. The resulting issue registry and dashboard help people see whether one bad Turn is isolated or part of a pattern.
That registry does not automatically become the benchmark. When a pattern is worth protecting against, a person turns it into a safe, representative task: preserve the behavior, leave the original conversation and project data out, define what success means, and add variations when one example would be brittle. We then run that task against the production-aligned configuration and the proposed candidate in Weave. If the task reveals a broader risk, it joins the relevant capability suite or regression gate after review.
We also explored a diagnostic system called BehaviorTrace. It reconstructed execution paths, grouped similar failures, and drafted possible coverage gaps. That work helped us think about trace diagnosis, but it is not the production-to-evaluation workflow we use today. The current loop keeps the important decisions with people: which pattern matters, whether existing coverage is enough, what the task should test, and whether the result supports shipping a change.
Once we have a reviewed diagnosis, we define the candidate precisely: which prompt, Skill, script, model route, tool behavior, configuration, or code changed. Baseline and candidate receive the same tasks, context, attempts, stopping rules, runtime class, and scorers. Failed attempts remain in the denominator.
That comparison is two evaluation runs, not one magic command:
1suite = resolve(eval_yaml)
2
3baseline = run_eval(suite, production_agent)
4candidate = run_eval(suite, proposed_agent)
5
6verify_same_task_and_trial_rows(baseline, candidate)
Conceptual pseudocode. WBAF runs one agent per evaluation; task and trial alignment must be checked before interpreting the delta.
The examples used to diagnose the problem are discovery. A separate confirmation set is fixed before we choose the candidate and opened afterward to see whether the change transfers. Editing that set after seeing the answer is not repairing the experiment. It is changing the test.
Figure 2. The tasks used to choose a change and the tasks used to check it are different. The held-back set stays untouched until the candidate is fixed.

## The evidence has to reconcile
A Weave Evaluation connects the task dataset, the agent prediction, the scorers, and their child Calls. A reviewer can open one failed row, follow it to the agent's root Call, and inspect the tool path behind the answer. If we correct a scorer, WBAF can rescore stored predictions under a new evaluation identity instead of paying to regenerate the agent output or rewriting the old result.
That last part has been more important than it sounds. Evaluators are software and product policy at the same time; we get them wrong too. Keeping the prediction separate from the scoring revision lets us repair the evaluator without pretending the original judgment never happened.
We still reconcile what we planned with what ran. A task that never started remains missing. A prediction without its expected trace or score is incomplete. A polished chart does not rescue missing evidence.
This is the practical dogfooding claim. Weave tracing is how we inspect ARIA in production; Weave Evaluations is how WBAF connects offline tasks, predictions, and scores. Using one evidence model does not make the evaluation correct. It makes errors in the tracing, scoring, and reconciliation visible to the team building the agent.
People still select the failure, review the diagnosis, decide what good behavior means, and review the production change. I do not see those handoffs as unfinished autonomy. They stop the same system from writing the question, supplying the answer, grading itself, and approving the release.
Figure 3. ARIA can help inspect and test a proposed change. People decide what becomes a task and what returns to production; only a change shipped through normal review closes the loop.

### What became Fugue
ARIA's tasks and diagnostics belong in WBAF. Production ARIA runs through the ARIA service. But some controls kept recurring: lock the exact candidates and tasks, align attempts, keep private truth away from the agent, show the plan and cost before execution, require approval, isolate the runtime, and reconcile the result with its evidence.
Those controls became Fugue, a separate experiment-governance project for agents beyond ARIA. It does not run production ARIA or replace WBAF. Its job is to make a proposed comparison inspectable and to prevent an agent from approving its own budget or silently launching the next study.
We wanted ARIA to help improve ARIA. What we trust today is narrower: it can inspect a failure, propose a change, and help test it while people retain control of the expected behavior and the decision to ship.
When the evidence says no, somebody still has to be willing to listen.

### Further reading
- CoreWeave ARIA describes the current public product.
- The AI Loop: Launch Day Is Day One describes how production evidence feeds evaluation and improvement.
- W&B Weave introduces the shared tracing and evaluation system.
- Understand Ops, Calls, and Traces documents Weave's trace model.
- Evaluations overview documents the Dataset, prediction, and scorer relationship.
- Why I Built Fugue: Controlled Experiments for Agent Systems explains how those controls grew out of the evaluation work.
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

ARIA,

Copy code

Copied!

ARIA,
