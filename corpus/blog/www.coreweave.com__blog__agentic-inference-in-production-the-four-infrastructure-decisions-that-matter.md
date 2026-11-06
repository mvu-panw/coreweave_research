# Agentic Inference in Production: 4 Key Decisions | CoreWeave

Source: https://www.coreweave.com/blog/agentic-inference-in-production-the-four-infrastructure-decisions-that-matter

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

This is the third and final chapter of our agentic inference series, and it’s the one that gets practical. In the first blog, we explored the unique shape of an agentic inference workflow, in which an agent turns one request into a chain of inference calls. The second blog examined what those repeated requests actually contain and how infrastructure can reduce time-to-first-token (TTFT) through prefix-aware routing.
Both left the same question open: What does infrastructure built for all of this actually look like once an agent is live and serving real traffic? And which deployment model do you use for it?
The answer is different for each team and each agent, depending on what you choose to optimize for, route on, scale on, and measure. Those decisions lead to which deployment model best suits your agent.
What follows are four decisions that determine whether an agent holds up in production, six questions about your own traffic that answer them, and the three deployment models those answers point to.

## Four decisions that determine whether your agent holds up
Four decisions sit underneath every production agent’s inference stack, whether or not anyone made them deliberately: What you optimize for, what you route on, what you scale on, and what you measure.

### 1. What you optimize for
Your stack targets one of two clocks, and the choice sets your batching and scheduling policy. 
- Time-to-first-token (TTFT): the wait before output starts streaming. The default in most stacks, and the right service-level objective (SLO) when a person is reading along. 
- End-to-end completion: time-to-last-token per step, and time-to-task-completion across the chain. The right SLO when a tool executor is the consumer, because it can’t act on a partial output.
Agentic inference in production comes down to four decisions: what you optimize for, route on, scale on, and count. Here's how each shapes your deployment model.

### 2. What you route on
Three signals are available to your router, and the one you pick decides how often a request lands on a worker that can skip prefill. 
- Least-connections (aka round-robin): sends each request to the first available worker, blind to both the session and the cache. The default in most stacks, and a good choice if your prefix changes on every call. 
- Session identity: pins a conversation to one worker. Cheap to implement, but load-blind, and it captures none of the reuse across different sessions that share a system prompt and tool definitions. 
- Prefix overlap: sends each request to a worker already holding reusable KV state for its prefix, balanced against that worker’s load, so prefill covers only the new tokens. Pays in proportion to how long and how stable your prefixes are. 
Blog two calls the third one prefix-aware routing; serving-engine and product documentation often call the same mechanism KV cache-aware routing.

### 3. What you scale on
Two settings here, and they interact. The trigger is what your inference autoscaler watches: 
- Latency or throughput: symptoms. Scaling on them is always late, because by the time p95 moves, the queue that caused it has been building for a while. 
- Concurrent running and queued requests: the demand pressure underneath those symptoms, and the earlier signal. 
The floor is how little you keep warm between bursts: 
- Scale to zero: right for a workload that runs a few times a day, punishing for agentic inference traffic. A cold replica has a cold cache, so every resume pays twice: once for the cold start, once for a full prefill of context that was warm twenty minutes ago. 
- A warm replica floor: you pay for idle capacity through the troughs and skip both penalties on every resume. 
- Fixed capacity: nothing to tune, and you pay for your peak all day. 
How finely you can set any of this depends on your deployment model. Routing decides where your traffic goes; the floor decides whether there’s anywhere good to send it.
The idle capacity under the warm replica floor is what you pay to avoid a cold start, plus a full prefill on every burst resume.

### 4. What you measure
Two units, and they can move in opposite directions. 
- Cost per token: what you’re billed on, and what most dashboards show by default. In a market where per-token prices keep falling, it’s a flattering number that can improve while your bill grows. 
- Cost per task: the whole chain. Tokens per step × steps per task × reasoning overhead, with every cache miss repaying for context the system already processed once. 
These four decisions don’t have one universal answer. You answer them differently depending on how much of the serving stack you own, which is what the rest of this piece is about.

## What shape is your inference traffic?
Workload shape comes before configuration. Prefix-aware routing, cache affinity, speculative decoding, disaggregated prefill—none of these are universally required, and each pays off in a particular regime. Speculative decoding fades as batch sizes climb. Disaggregation degrades below a scale threshold. Caching, as we'll get to, has a ceiling that a single mutating token can put you under. 
Techniques pitched without their boundaries are the fastest way to spend engineering time on something your traffic was never going to reward. Know your traffic shape first; then decide which parts of the stack are worth configuring. 
Six questions get you most of the way there.

### 1. How stable is your prefix? 
Caching requires an identical prefix, not a similar one. A timestamp in the system prompt, a reordered tool definition, a session variable injected before the instructions: any of them is a full miss on every call. Stable prefixes earn high hit rates; mutating ones collapse to nearly none. That exact-match ceiling makes prompt construction an infrastructure decision as much as a prompt-engineering one.

### 2. How long do your chains run? 
The more steps per task, the more the whole-chain SLO from Section 1 governs, and the more each step's latency compounds into something the user actually feels. Two hundred milliseconds per step is invisible at three steps and conspicuous at thirty.

### 3. What's your peak-to-average burst ratio? 
The wider the gap between idle and spike, the more your scaling policy matters, and the less a fixed, unconfigurable endpoint will serve you. A narrow ratio is a provisioning problem you solve once; a wide one is a policy you'll keep tuning.

### 4. Is a human waiting? 
Interactive agent traffic and async or batch inference work have genuinely different latency budgets. Optimizing one for the other wastes money in both directions: you'll overpay for warm capacity a nightly job didn't need, and underprovision the workflow someone is watching.

### 5. Is your traffic shape settled, or still moving? 
This is the question that most often decides the answer. A workload still finding its shape wants cost that tracks consumption, because you can't right-size capacity for traffic you can't yet predict. A known workload wants cost that tracks capacity, because at steady volume, that's the cheaper instrument.

### 6. What does your team actually want to operate? 
A serving stack you control is only an advantage if someone will tune it. An honest answer here saves more money than any technique in this piece; a highly configurable stack left at its defaults is just a more expensive version of a managed one.
Your traffic profile is the input to a single decision: How much of the serving stack do you need to own? That’s your deployment model, and it’s a bigger lever on your configuration than any individual technique you might enable.

## Which deployment model fits your workload
Deployment models are easiest to compare and evaluate based on what you control.
A fully managed solution means an endpoint against a curated model catalog. You control the prompt and the model choice; you don't select the serving engine, the routing policy, or the scaling behavior. Cost tracks consumption directly, the right instrument while the workload's shape is still moving: you pay for the traffic you had, not the capacity you guessed at.
A managed-but-configurable solution puts your own weights on dedicated capacity with the operational burden still carried by the provider. You select the serving engine, the routing behavior, and the scaling parameters, which is what turns Section 1's routing and scaling decisions into things you tune against your traffic rather than inherit. Cost tracks capacity, which is the right instrument once the workload is known.
A self-managed model gives you full control of scheduling, orchestration, and inference engine configuration on your own cluster. Maximum tuning surface, maximum operational ownership. Everything is available to you, and everything is yours to run.
Not three rungs on a ladder. Three positions on one axis, and the shared interface is why you can move between them.
Not three rungs on a ladder. Fully managed, managed-but-configurable, and self-managed are three positions on one axis—and the shared OpenAI-compatible interface is why you can move between them.

### Which inference deployment model matches your workload shape and control needs?

 | 
 | Fully managed
 | Managed but configurable
 | Self-managed

 | What you control
 | Prompt and model choices
 | Model, serving software, routing, scaling
 | The entire serving stack

 | Models and weights
 | Curated catalog
 | Your own weights
 | Your own weights

 | Serving software
 | Provider’s choice
 | Yours
 | Yours

 | Routing policy
 | Provider’s default
 | Yours to configure
 | Yours to build

 | Scaling policy
 | Provider’s default
 | Yours to set
 | Yours to build

 | Warm capacity
 | Managed for you
 | Configurable
 | Yours to manage

 | Cost traces to
 | Consumption (per token)
 | Capacity (per GPU-hour)
 | Capacity (per GPU-hour)

 | Operational burden
 | None
 | Low; provider runs the cluster
 | Yours

 | Best fit
 | Traffic shape still moving; iterating
 | Known workload, latency-sensitive agent traffic
 | Teams who will actively tune against their own traffic

 | Interface
 | OpenAI-compatible
 | OpenAI-compatible
 | OpenAI-compatible

Read the table against your answers. If your prefix mutates on every call, the routing row matters less than you’d think, because you’re below the exact-match ceiling and no routing policy will lift you above it. If your burst ratio is wide, read the scaling policy row closely. And if your traffic shape is still moving, the cost row settles it before the others get a vote.
Your decision today is reversible, thanks to OpenAI-compatible endpoints across all three models. You can start at one position, learn what your traffic actually looks like under real load, and move without rewriting the application around it. Given how many teams answer question five with “still moving,” that matters more than getting it right the first time.

## Your stack, built for your agent
Prompt structure, routing, and production infrastructure aren't three topics. They're one continuous argument: agentic inference needs infrastructure built for how they actually behave, not adapted from what worked for chat.
Which means the success of your agent depends on whether the stack was built for your agent. Not for a general workload, and not for the chat traffic your serving defaults were tuned around. It’s a stack built on your four answers (what you optimize for, what you route on, what you scale on, what you count) and the deployment model that fits the traffic those answers describe.
CoreWeave Inference offers all three positions on that control surface:
- Fully managed → Serverless Inference
- Managed-but-configurable → Dedicated Inference
- Self-managed → Inference on CKS
These aren't three products a team graduates between. There are three positions on one control surface, and the shared OpenAI-compatible interface is what makes moving along it cheap.
Go deeper:
- [Webinar] Three AI Inference Execution Paths: How to Match Your Workload to a Solution
- [eBook] Production AI Inference Infrastructure: An Evaluation Guide‍

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

CoreWeave Cloud,

Copy code

Copied!

CoreWeave Cloud,
