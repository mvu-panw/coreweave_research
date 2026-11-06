# Introducing CoreWeave ARIA: AI Research and Iteration Agent

Source: https://www.coreweave.com/blog/introducing-coreweave-aria-ai-research-and-iteration-agent

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on July 29, 2026.
CoreWeave ARIA is a coding agent built directly into Weights & Biases, with deep knowledge of the platform. ARIA reads your experiments, builds live visualizations to back up its analysis, and has your full project context from the moment you start a conversation. Together, these capabilities power a full autoresearch loop, from analyzing your results, to forming hypotheses, to launching the next experiment and evaluating what came back.

ARIA powers the autoresearch loop for continuous improvement, running the full research cycle, not just analyzing it. Describe what you want to learn (for example "Does adding dropout after the attention layers help with the overfitting I'm seeing?") and ARIA forms a hypothesis, writes the config, and launches the experiment through W&B Launch on your team's compute.
When the run finishes, ARIA evaluates the results against your baseline, updates the workspace with comparison panels, and drafts a W&B Report describing its findings. If the result is inconclusive, it proposes a follow-up: a different dropout rate, a longer schedule, a sweep across values. Every run is tracked, every decision is visible in the conversation, and the gap between "run finished" and "next run configured" shrinks from hours to minutes.
By continuously forming hypotheses, running experiments, evaluating results, and executing the best next actions, ARIA creates an autonomous research loop that helps models and agents improve while you focus on the problems that require human judgment. 
ARIA analyzes 674 runs, identifies the top-performing configuration, and proposes a concrete follow-up experiment with a ready-to-use config that it can launch for you through W&B Launch.

## Live, persisted dashboards to back up analyses
When you ask ARIA a question, it doesn’t reply with a wall of text or a series of numbers. It creates shareable W&B workspaces, panels, and reports to back up its findings, faster than you could configure them yourself. 
ARIA knows which panel type fits the question: a heat map for two-dimensional parameter sweeps, a parallel coordinates plot for exploring hyperparameter interactions, a bar chart for comparing discrete configs. It filters down to the most important runs, groups where aggregation is required, and builds a workspace view you can keep using after the conversation ends. And because these are live W&B dashboards, they update as new runs come in, they’re visible to everyone on your team, and they’re as configurable as anything you’d build yourself.
When ARIA recommends next steps, the supporting charts and panels let you validate the reasoning at a glance. You stay in the loop not by reading through pages of text, but by seeing the evidence laid out visually.
ARIA identifies activation outliers across runs, creates a pinned workspace section with 5 targeted line-plot panels, and sets a run filter to surface the key runs, all directly in the user's workspace.

## Your full experiment context is already loaded
When you open ARIA from a workspace page, it already knows your project, your visible runs, and your active filters. You don’t have to screenshot your workspace view and paste it into a chat window or explain which project you’re working in.
Context here means more than just the page you’re on: ARIA can access the training code you log to W&B, experiment logs, loss curves, metrics, artifacts, and checkpoints. It can also span projects and extend into your teammates’ experiments. Ask “My validation loss plateaued at epoch 12, but downstream eval scores are still climbing. What’s going on?” and ARIA pulls the training logs, checks the learning rate schedule, compares against similar runs in your other projects, and cross-references techniques from recent papers on arXiv.
For teams working across multiple projects with hundreds of thousands of logged metrics, from accuracy numbers down to per-layer gradient norms, ARIA can surface patterns that are hard to spot manually.
The user asks "what happened?" from a failed run's log page. ARIA already knows the run, sees the CUDA OOM error in the logs, and starts investigating. No need to name the run or describe the problem.

## Built with deep platform knowledge
Weights & Biases is the AI developer platform designed to scale research projects to hundreds of thousands of experiments and metrics. A general-purpose coding agent can query W&B via APIs, but it wasn’t built for it. It doesn’t know the difference between a run's display name and its ID, how to query the run history API optimally, or which visualizations are auto-generated in a sweep. It struggles at scale: scanning entire projects when only a few runs matter, pulling full training histories when summaries are enough, making redundant calls that leave you waiting minutes for a simple answer.
ARIA is continuously trained by the W&B team on the platform's nuances. It knows how to scope queries efficiently, navigate massive projects, and work across team boundaries. The result? Fast, reliable answers whether your project has 20 runs or 20,000.
Asked whether any teammate has tried sandwich norm, ARIA knows to search across run names, configs, output logs, code artifacts, and metadata across all 60 runs, and reports exactly where it looked and what it ruled out.
‍

## Available on mobile
ARIA is available in the Weights & Biases mobile app. Researchers can monitor runs, investigate results, and interact with ARIA on the go. Download here.

## Example use cases 
Below are some of our most popular use cases 
- Analysis: What patterns do you see in my results?
- Visualization: Create a view that highlights key runs and panels, including a section on outliers
- Debugging: Why did some of my runs have an OOM error? Look at the logs, code and system metrics
- Experiment guidance: What's the next hyperparam set to try? Launch the job for me
- Search: My teammate is trying the same architecture in another project. Find their best run, then import it to my workspace for comparison
- Product questions: How can I overlay multiple metrics on the same chart?

## Where is this heading
The public preview is just the beginning. The roadmap for ARIA introduces features designed to transform how teams approach machine learning research:
A shared research partner for your whole team. The current version of ARIA answers your questions and builds what you ask for. The next version brings your whole team into the loop. Imagine shared agent conversations where everyone can see which questions have been asked, which patterns have been found, and which experiments have been proposed. A shared board where your team and ARIA both contribute research ideas, with ARIA comparing runs across projects and teammates to surface connections no single researcher would catch.
ARIA picks up the highest-priority hypothesis, designs the experiment, launches it on your infrastructure through W&B Launch, monitors the results, and reports back what it learned. Over time, ARIA builds a persistent memory of your project, your team’s preferred workflows, and your collective research goals. 
Extensible and enterprise-ready. ARIA adapts to how your team works.
- Encode custom instructions and skills so it follows your conventions and runs your preferred analysis workflows.
- Connect your own data sources through custom MCP servers, so ARIA can reach beyond W&B into your internal tools, databases, or documentation.
- Bring your own API keys to use your preferred LLM provider.
- On the infrastructure side, ARIA will connect to CoreWeave Mission Control through MCP, letting you analyze compute and experiments in the same conversation.
- Enterprise admin controls are on the roadmap, so your team can adopt ARIA with the governance your organization requires.

## Get started
ARIA is available now in public preview.
- Open any project in W&B,
- Click the agent icon in the sidebar, and
- Start with a real question about your experiments.
Read the docs to get started.
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
