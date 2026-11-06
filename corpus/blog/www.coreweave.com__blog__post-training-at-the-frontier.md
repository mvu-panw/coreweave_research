# RL Post-Training Nemotron 3.5 Lightning | CoreWeave Blog

Source: https://www.coreweave.com/blog/post-training-at-the-frontier

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In early September, CoreWeave, NVIDIA, and You.com ran a three-week sprint to post-train an open-weight model for agentic web search, using web-grounded search data, supervised fine-tuning (SFT), reinforcement learning (RL), and managed  RL Rollouts. The final workflow reached 45.45% accuracy on BrowseComp, compared with 36.97% for the original baseline—a 22.94% relative improvement—with 31.55% fewer tool calls per task. For teams building search agents, that means more questions answered correctly with fewer tool calls.
For teams running RL post-training, better training data is only part of the challenge. Inference must generate rollouts, training must update the policy, and the updated weights must reach serving replicas before the next cycle. Conventional redeployments can interrupt rollout generation and leave accelerators waiting. CoreWeave RL Rollouts, using NVIDIA Dynamo and related serving technologies, is designed to reduce that synchronization overhead.
This technical deep dive examines You.com’s data and training strategy, CoreWeave’s managed RL Rollouts infrastructure, NVIDIA’s model and serving technologies, and the results and practical lessons from the collaboration.

## The bottleneck in RL post-training: Inference cadence
Open-weight models have improved rapidly, but foundation models alone are not enough. Teams post-training models for specific tasks—search, reasoning, code generation—now have one constraint: keeping their RL loop productive.
In a typical RL loop, the cycle is: generate rollouts → score them → update the policy → repeat. Efficiency during RL Rollouts can be a big bottleneck in the post-training stack. Most infrastructure treats these as separate problems. RL infrastructure requires treating them as one.
The three companies addressed complementary parts of the problem: You.com supplied search and web-grounded training data; NVIDIA contributed the Nemotron model, post-training, and serving technologies; and CoreWeave provided the managed training and rollout  infrastructure that connects these stages.

## The work: Web-grounded data, difficulty filtering, and GRPO
You.com started with a problem statement: open datasets age fast and lean heavily on Wikipedia. Real questions live on the real web. So they built training data from the web graph itself.
Instead of open-source benchmarks, You.com generated multi-turn QA pairs grounded in objective facts on real web pages. They sampled from the middle popularity band—skipping the spam-heavy tail and boilerplate-heavy head—then followed 1-hop links to pull page content from their index. The result: questions whose answers lived on the web, not in archived datasets.
Then came difficulty filtering. You.com ran each question eight times through Nemotron 3.5 Lightning using their own search APIs, scoring each attempt with an LLM judge. They bucketed questions by pass rate: too easy (8/8), easy, medium, hard, too hard (0/8). The hypothesis was simple: if the model sometimes solves it, it's trainable. If it never does, it's not worth the compute budget yet.
The team used 4,932 SFT traces generated with You.com Search and  NeMo Automodel, followed by 1,480 RL tasks trained with group relative policy optimization (GRPO) and a binary reward signal. The source draft reports ~1 hour for SFT on four NVIDIA HGX B200  GPUs and  ~8 hours for the RL run. The results showed that the infrastructure made the timeline possible, but the data strategy made it count.

## The infrastructure: RL Rollouts and checkpoint synchronization
CoreWeave and NVIDIA focused on the rollout side of the training loop: reducing the time it takes to get each new policy onto inference replicas. In a conventional rolling redeploy, each replica restarts, downloads the full checkpoint from object storage, and waits for the engine to initialize while other replicas keep serving. The restarting replica is unavailable during that time, and its unfinished requests can be lost. Repeated across a training run, those interruptions add up.
Illustration of the collective RL training loop between You.com and CoreWeave
RL Rollouts replaces these restarts with in-place weight updates, which we call Hot-Load. The trainer publishes a checkpoint and calls the Hot-Load API while earlier rollouts are still running. CoreWeave's control plane coordinates the update across replicas and tracks the checkpoint version each one serves. 
NVIDIA Dynamo, NVIDIA ModelExpress, and vLLM handle the update within each replica.  Before loading the new weights, the replica pauses serving but keeps its in-flight requests and cache in memory. Once the weights are loaded into the existing engine, serving resumes and those requests continue on the new weights. New requests queue during the pause. As with a rolling redeploy, other replicas keep serving; the difference is that the updating replica resumes serving much faster and preserves its state.
This lets trainers overlap weight updates with rollout generation and allow a request to span multiple policies. For strictly on-policy training, the trainer can request a prompt-cache reset and wait for every replica to finish updating before sending the next batch.
Delta weight sync reduces both the amount of data the trainer uploads and the time replicas need to load weights compared with full weight sync. Rather than publishing the full model each time, the trainer publishes a compressed delta against a baseline checkpoint.
 In our Nemotron 3.5 Lightning tests, these deltas were roughly 0.14%–0.95% of the full BF16 checkpoint size. The weight-distribution design also avoids having every replica download from object storage: one replica reconstructs the checkpoint locally, and the others receive the weights via GPU-to-GPU transfers over CoreWeave’s InfiniBand network or NVIDIA NVLink interconnect. In a benchmark using Nemotron 3.5 Lightning with four replicas on CoreWeave’s NVIDIA GB300 NVL72 systems, the fastest delta Hot-Load was roughly 15× faster than the average cold-start redeploy.
For training workflows that repeatedly refresh inference weights, faster updates can reduce waiting between rounds and keep GPUs doing useful work for more of the cycle. Reducing that overhead can also leave more room for experiments within a fixed development budget; the impact depends on how much of the workflow is spent loading weights.

Rollout responses also return the data needed for training. Trainers can request token IDs and per-token logprobs, along with expert-routing data for supported mixture-of-experts (MoE) deployments where it is enabled. Logprobs use the standard OpenAI-compatible response fields, while routing data is available through an NVIDIA Dynamo extension.  

## The result: higher accuracy with fewer tool calls
The base model hit 36.97% accuracy on BrowseComp with baseline tooling. It made 168 tool calls per task on average, many of them wasted. Three failure patterns dominated: death loops (searching repeatedly for the same information), weak tool use (not extracting value from search results), and second-guessing (finding the right answer, doubting it, then answering incorrectly).
With You.com Search and the combined optimization workflow, BrowseComp accuracy reached 45.45% versus 36.97% for the original baseline. Average tool calls dropped from approximately 168 to 115 per task—a 31.55% reduction. The model learned to reason more, search more strategically, and trust its findings.
One illustrative BrowseComp trace asked the agent to identify a car model through a chain of clues about a CEO: acquisition year, degree, spouse's MBA, endowment, and a 2019-2023 interview. In the reported comparison, the base model made 313 tool calls (149 search, 118 web fetches, 46 bash) and consumed 1.3M characters of useless search results. It never figured out who the CEO was. The optimized agent completed the task in 7 tool calls. It found the CEO on the second call, then used five more to verify each clue. Same search tool, same task—just a model that learned to reason.

## The blueprint: What it takes to replicate this
This wasn't a bespoke, one-time effort. The team built toward a repeatable pattern.
Start with strong search. It sets the ceiling for everything built on it. You.com tuning their search endpoints for post-training consistency improved performance by ~4% before any training happened.
Build questions from the real web. Web-graph QA plus open datasets, decontaminated against your eval. One-time effort, but it pays dividends. Open datasets age; the web refreshes daily.
Filter by difficulty before you train. Pass@8 with production search; keep what the model sometimes solves. Skip the too-easy and too-hard tails. This alone cuts training cost and improves convergence.
SFT on your own traces, then GRPO. Binary judge reward; a small, targeted dataset is enough. You.com used 4,932 SFT traces and 1,480 RL tasks. CoreWeave's infrastructure ran that in ~9 hours total.
Leverage the Hot-Load API to sync weights efficiently. Use delta weight sync to reduce inference stalls and avoid costly cold-start redeploys.
Measure accuracy and efficiency together. Not just accuracy—also tool calls, tokens consumed, time, and cost. The post-trained model improved on all axes.

## What's next for RL Rollouts
The work doesn't stop. You.com plans to scale toward ~100K rows of training data, salvaging failed trajectories for SFT and pulling more web-graph QA. The agent side will add confidence-gated budgets and early stopping. RL will shift toward efficiency-aware rewards—using cheaper search for early RL iterations, then switching to more expensive search for inference polish.
On the infrastructure side, CoreWeave and NVIDIA are documenting the deployment patterns and roadmap for running RL Rollouts at scale. The team is also upstreaming the You.com search provider integration to NVIDIA NeMo Gym, making it available to other teams building agentic post-training workloads.

## Partnership with You.com and NVIDIA
Three companies worked in parallel for three weeks to prove the pattern works. You.com engineered the data pipeline and search integration. CoreWeave ran the RL trainer and deployed the serving infrastructure. NVIDIA built the checkpoint mechanics and training metadata support in Dynamo and vLLM, and contributed to the  supervised fine-tuning work.
EVP of Product and Engineering Chen Goldberg shared the result in her keynote at Fully Connected 2026 on September 30th, three weeks after the buildathon began. That timeline only happens when the infrastructure is right and the teams share a clear commitment to making it work.
If you're running your own RL training loop, the blueprint is available. The infrastructure exists. The work is portable—not just to other models, but to other problem domains where RL training cadence has been a bottleneck.
Want to get started with RL Rollouts?
- Explore the documentation, including the inference cookbook, an open source repository of RL recipes that train against a hot-load-enabled deployment
- Register for the webinar on post-training Nemotron, featuring experts from NVIDIA and You.com
- Watch the Fully Connected 2026 Breakout Session Recording “Post-Training at the Frontier: How You.com, NVIDIA, and CoreWeave Improved Nemotron’s Agentic Search”
- Talk to us​​

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
min read

### CoreWeave Builds the First Global Backbone Network Purpose-Built for AI

5
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

### Closing the Loop Between Inference and Post-Training

7
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

Inference,

Training,

Copy code

Copied!

Inference,

Training,
