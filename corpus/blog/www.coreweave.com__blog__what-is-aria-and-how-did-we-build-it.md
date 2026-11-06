# What Is ARIA, and How Did We Build It?

Source: https://www.coreweave.com/blog/what-is-aria-and-how-did-we-build-it

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on September 25, 2026.
When we released ARIA in public preview on June 29, 2026, the obvious thing to show was the agent chat experience: ask a question about your experiments, watch it inspect the evidence, and get an answer. Chat is where ARIA lives, but it is not the part that really shows off what ARIA does.
We began with a fairly normal idea: put a capable, tool-using agent inside W&B, where the Runs, metrics, artifacts, and production traces already live. We thought the main advantage would be context. A researcher should not have to copy half a project into a prompt before an agent can help.
Context did matter. But once ARIA started doing useful research, the harder questions changed. Could the work survive after the chat closed? Could another person inspect the evidence? Could a long investigation recover from failure? Could the agent take an action without quietly taking authority from the researcher? And when ARIA got something wrong, could we turn that failure into a better version of the product?
The product grew around those questions. What we built is still an agent inside W&B, but it is better understood as a research process that begins in a conversation.

## We started with context
Imagine opening a W&B project because a training run has become slower. You already have a filtered workspace, a few suspicious Runs selected, and a metric that changed after the last configuration update. You ask what happened.
A general assistant sees the sentence. Before it can help, you need to describe the project, paste in the relevant metrics, explain the filters, and decide which artifacts fit in the prompt. You are halfway through the investigation before the investigation starts.
ARIA starts from the W&B context around the question. It can inspect experiment data and production traces, follow evidence across Runs, and create a workspace or report that keeps the finding beside the data that supports it. If the next useful step is another experiment, ARIA can prepare that work and ask the researcher to approve the launch.
Figure 1. ARIA created and verified a pinned workspace section while the researcher could inspect the resulting charts beside the conversation. Image from the official ARIA launch report.
The persistent output changed our idea of a good answer. A polished paragraph that disappears with the conversation is difficult to review and almost useless to a teammate who was not there. A report can be shared. A workspace can keep updating as new Runs arrive. Another researcher can open either one, disagree with the conclusion, and continue from the same evidence instead of reconstructing the work from screenshots.
I had initially thought of those artifacts as a nicer way to present the answer. In practice, they became part of the answer. The conversation is where the researcher asks for help; the durable artifact is where the research becomes useful to the rest of the team.
Working inside W&B also forced us to be clearer about authority. Reading selected Runs is part of an investigation. Creating a report changes a shared project. Launching an experiment spends real compute. ARIA can do the tedious work around those decisions, but the model sounding confident cannot be the thing that grants it more permission. Researchers still approve consequential actions.
Figure 2. ARIA shortens the work between observing a result and starting the next experiment. The loop closes only when a researcher approves the action. Adapted from CoreWeave's AI Loop.

## The research outgrew the chat
The first version of the agent loop was easy to picture. ARIA received a request, chose a tool, inspected the result, and continued until it had an answer. A harness assembled the prompt and project context, exposed the allowed tools, kept the conversation history, and enforced limits.
Real investigations made that loop much less tidy. A question such as “why did these runs get slower?” may depend on the page the researcher was viewing, the filters applied to it, a particular metric, and an artifact produced by an earlier experiment. We turned that page state into structured context so ARIA could tell where it came from and what the researcher had selected. We also kept the limitation explicit: a filtered page is a useful starting point, not proof that the agent has seen the whole project.
Then the jobs became longer. ARIA might inspect hundreds of Runs, generate a visualization, wait for remote work, recover from a failed tool call, or continue after the researcher closes the browser. Once an investigation could outlive the browser session, we needed somewhere durable to store the work and a worker that could resume it.
The production ARIA service stores one user request and the agent work that follows as a durable Turn. A Turn includes the prompt, reconstructable history, the configured agent and environment, and the state needed to continue. Turns form a tree, which lets a researcher return to an earlier point and take the work in another direction. A worker claims a Turn and records its progress. The active work runs in an isolated sandbox whose files and state can be snapshotted and restored.
None of this is the glamorous part of an agent demo. It is the part that determines whether the demo can become a product. Conversation history helped ARIA pick up the thread, but the service still had to persist the work and recover it when something failed. The browser could show progress, but it could not be responsible for scheduling the job or keeping it alive after the tab closed.
As those responsibilities accumulated, we split them deliberately. The ARIA service owns authorization, persistence, dispatch, and progress. The agent decides what to do next. The environment exposes state and tools. The sandbox isolates execution. A shared driver coordinates one Turn across those pieces.
Figure 3. The same investigation gains structured page context, a durable Turn, resumable execution, and restorable files. Closing the browser removes the viewer, not the work.
That separation was not architecture for its own sake. It gave failures a more useful address. If the agent chose the wrong tool, we could investigate agent behavior. If the worker lost state, we could repair recovery. If the sandbox failed before the task began, we did not have to pretend the agent had answered incorrectly. It also let us change the agent without rebuilding the entire service, and change the infrastructure without claiming that ARIA had become smarter.

## Production failures became useful evidence
Once ARIA was doing real work, we needed a better way to learn from the cases where it failed. Our first instinct was familiar: read the trace, remember the important parts, and write a cleaner evaluation task that reproduced the headline problem.
The trouble was that the rewrite often removed the reason the failure happened. The prompt survived, but the page context did not. The expected outcome survived, but the earlier turns or environment state did not. We ended up testing a simplified story about the failure rather than the thing users had actually experienced.
The durable Turn gave us a better starting point. It already contains the request, reconstructable history, configured agent and environment, and a reference to restorable state. The same driver used by the production worker can run a controlled task offline. That keeps the evaluated candidate close to the version of ARIA we could actually ship instead of creating a benchmark-only cousin that behaves almost—but not quite—like the product.
Weave makes that bridge useful rather than merely possible. Weave is W&B's observability and evaluation system for agents and LLM applications. It records agent operations as Calls and connects them into traces, so we can inspect a production failure and an offline comparison through the same evidence model. We can follow an evaluation result down to the model and tool calls that produced it, compare attempts, add scoring, and keep the evidence attached to the change being considered.
W&B Agent Factory, or WBAF, provides the ARIA-specific research environment on top of that evidence. It imports a production-aligned ARIA configuration and runs the tasks, environments, and scorers needed to test a proposed change. The ownership is intentionally boring: the ARIA service remains the production source of truth, Weave records production and evaluation evidence, WBAF runs the comparison, and a change that looks good still returns to normal production review before it ships. WBAF does not ship a second ARIA.
There is an important limit to this story. We can preserve the conversation and sandbox state, but the surrounding W&B project may continue changing. New Runs arrive, artifacts move, and services return different data. Reproducing an old Turn exactly therefore requires immutable references or prepared fixtures for the external evidence that mattered. Preserving the agent's state is not the same as freezing the world it could observe.
That caveat sounds obvious after you say it. It was less obvious when the Turn and sandbox restored successfully and the whole job looked replayable. Building ARIA has included a healthy amount of discovering that the precise version of an exciting claim is usually more useful than the exciting version.

## Could ARIA help us improve ARIA?
Connecting production work to evaluation made a more ambitious idea plausible: give ARIA one of its own failures and let it help with the repair.
We are not claiming that ARIA autonomously rewrites itself today. The current workflow is narrower: we inspect the failed Turn, the context it received, and the relevant code or instructions, then use an agent to help suggest one focused change. The editable surface might be a system instruction, a script, a tool contract, or a Skill: a package of instructions, references, and scripts for one bounded job.
Looking at the code as well as the conversation matters. Suppose a trace shows the agent requesting too much data, timing out, and then repeating the same plan. If we read only the transcript, the tempting fix is another sentence telling it to be more selective. The actual cause may be a Skill that teaches the wrong query pattern, a tool that does not expose a bounded read, or retry behavior that restores the same bad state. We wrote extra prompt rules more often than I would like to admit. They worked just often enough to turn into prompt whack-a-mole.
An agent can propose the edit, and we can rerun the motivating case. If the next attempt uses the right evidence and finishes cleanly, that is useful. It tells us the change is worth investigating.
It does not tell us that ARIA improved overall. The project may have changed. A service may have recovered. The edit may solve that conversation while breaking three related tasks. The failed Turn helps us locate a problem; a controlled comparison tells us whether the proposed fix deserves to ship.
This is the version of self-improvement we trust. ARIA can help inspect a failure, propose a change, and gather evidence about it. People still decide what correct behavior means, whether the comparison was fair, and whether the result is strong enough to release. ARIA does not grade its own homework and merge the answer.
Post 0, “How We Benchmark ARIA—and Why It Runs on Weave,” explains how we build those comparisons, what the benchmark contains, and where human review remains in the loop.

## Where the series goes next
This series follows the four parts of ARIA that became interesting once the initial agent loop met real use:
- the product thesis behind putting a research agent inside the research platform;
- the interface for dense, parallel, and long-running work;
- the workers, environments, and sandboxes that keep that work alive;
- the evaluation process that turns production failures into reviewed changes.
Some posts will explain systems that exist today. Others will describe directions we are still exploring, and we will label them that way. The goal is to show how the pieces were built and where their boundaries are, not to make the roadmap sound finished early.
The evaluation work also left us with a more general problem. Other agents needed the same controls we wanted around ARIA experiments: lock the candidates and tasks, show a person the plan before execution, isolate the run, and reconcile the result with the evidence afterward. We extracted those controls into Fugue, a separate experiment-governance project. Fugue is not part of ARIA's runtime, and it does not replace WBAF's ARIA-specific tasks or diagnostics. The Fugue series will cover that branch of the work.
We started by putting a tool-using agent inside W&B. The work since then has been about making its research survive the conversation, remain inspectable by other people, and improve without quietly granting the agent authority over what “better” means.

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
