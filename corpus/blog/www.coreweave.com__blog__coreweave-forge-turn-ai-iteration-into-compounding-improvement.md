# Introducing CoreWeave Forge | CoreWeave Blog

Source: https://www.coreweave.com/blog/coreweave-forge-turn-ai-iteration-into-compounding-improvement

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

At Fully Connected 2026, we announced CoreWeave Forge, which connects and accelerates each stage of the AI improvement lifecycle. It’s a single development environment for serving models in production, observing in-production conversations, curating data, building the next version and evaluating the final product before deploying it into production. Keeping models accurate and agents reliable means repeating that cycle after every deployment. Some organizations already run this cycle across a patchwork of disconnected systems and manual workflows, stitching stages together by hand. Others are only beginning to formalize it. Either way, today's AI teams often stall between the diverse tools of their AI loop or get lost in the handoffs.
CoreWeave Forge changes all that. It creates a fully connected improvement loop that reduces manual handoffs between stages and stays open to whichever model, framework, or cloud you already run. With a tightly connected, streamlined loop, your time from production issues to validated fixes shortens with every cycle, accelerating progress and reducing your time from first agent to best agent.

The more you ship, the faster you improve. That’s the virtuous cycle fueling CoreWeave Forge. 

## CoreWeave Forge cures production exhaustion
We designed CoreWeave Forge to address the ever-increasing operational complexity of AI production. A few years ago, just getting a model into production was a major milestone that teams celebrated. Today, a first deployment is still a milestone, but it’s only the beginning. Once a team ships its first agent, the hard questions begin. How do we keep the outputs accurate and our customers happy? And what will it cost us to keep it that way?
After a few iterations, the excitement fades and it becomes harder to see the impact of improvements, or even know which improvements to try. The AI engineers who trained the model and understand what “good” looks like hand it off to an application or SRE team that owns production, and from that point on the two groups are looking at different systems. Application traces land in an observability dashboard built for uptime, which tells the on-call engineer that the service is healthy but tells the research team nothing about answer quality or user sentiment. The evaluation suite that was previously accurate drifts because no one on the production side owns updating it against shifting user behavior and traffic. And no one on the research side even sees the traffic. Researchers, AI engineers, and business leads go back to their separate dashboards as they prepare another release. And every system requires ongoing maintenance as the technology landscape shifts beneath it. 
Over time, these gaps make it increasingly difficult to turn production feedback into higher-quality, more cost-effective, and more performant AI applications. Teams spend significant time maintaining tools and coordinating handoffs, leaving less time to improve the applications themselves.
The problem isn’t a lack of talent or infrastructure. It’s a disconnected AI improvement loop.

## Disconnected tools make it hard to loop
We designed CoreWeave Forge to connect the systems that run, observe, curate, improve, and evaluate AI workloads—and make them easy to use. These stages follow a familiar cycle for most teams. Run a model or agent in production, watch what it does, turn that signal into data, improve the system, prove the new version is better, then ship it. That’s the general template of AI development today.  

‍
We designed CoreWeave Forge to not only connect the AI loop but also address the specific challenges of each critical stage:
- Run: Deploy models and agents in production and generate real-world signals. Opportunity: Running the right models, the right harness, and capturing the right signals.

- Observe: Capture traces, metrics, tool usage, and behavioral feedback from metal to agent to understand performance.Opportunity: Knowing what to monitor and what to examine so your team can identify what actually went wrong and what to improve.

- Curate: Transform production signals into high-value datasets and continuously refreshed evaluation suites.
Opportunity: Enabling AI-supported and human-in-the-loop curation of data and insights, keeping improvement data refreshed against current workload patterns and opportunities.

- Improve: Use curated data to optimize agents, shift models, improve the harness, refine models with various techniques from reinforcement learning to supervised fine-tuning to model distillation, and deliver better quality, faster performance, and lower cost.
Opportunity: Using the right improvement solution to deliver the expected outcome and ensure curated examples arrive with the lineage that explains them. .

- Evaluate: Measure new models and agents against repeatable quality standards before, during, and after deployment.
Opportunity: Defining and clearly understanding improvements against clear standards versus shipping changes strictly on the basis of subjective judgment. 
The challenges along the AI loop can be daunting and time-consuming, but they’re not intractable. Starting today, there’s a solution. One that ensures that these stages are connected,  open, and easy to understand. Customers like MasterClass and Canva are starting to use Forge already to complete their AI loop. 

## CoreWeave Forge connects the entire AI lifecycle
CoreWeave Forge connects all the stages of the AI loop on the cloud purpose-built for AI, creating one connected environment that enables teams to move from production insights to production improvements, faster:

### What’s new: 
- CoreWeave Agent Lens (New Service) turns production agent observability into continuous improvement and understandable insights. Every step, decision, and tool call traced end to end, readable as a conversation or in full technical detail. Monitors score live traffic with human oversight and curation, so prioritized failures surface early with recommendations on how to address them. Agent Lens improves failure detection by 20% and fixes issues at half of the cost.
- CoreWeave ARIA (now Generally Available) helps you learn, research, code, and iterate across the AI loop, analyzing runs, proposing experiments, recommending code changes (and storing them in GitHub), and bringing back actionable evidence. ARIA becomes a key component to making the entire loop more accessible and easy to understand for expert AI and non-expert AI users. 
- CoreWeave Sandboxes (now Generally Available) lets you run agents, tool calls, RL, and evals in isolated CPU or GPU execution environments, on serverless infrastructure or on the infrastructure you already train on.
- Model Distillation (New Service) trains a smaller, open-weights model on your larger model’s outputs for a task you’ve already proven in production, scores it head-to-head against the model you run today, and gives you the evidence to move traffic safely. 
- CoreWeave Notebooks (New Service) lets you experiment and collaborate with your team with fast and capable managed Python notebooks. Share evals and custom analytics per-model and per-agent.

### What’s also included is the best place to run inference and a system of record that connects all the components: 
- CoreWeave Inference lets you access leading open-weights models via Serverless Inference or run Dedicated Inference for larger workloads on dedicated and fully isolated infrastructure.
- Weights & Biases Models accelerates model development whether training or post-training with experiment tracking, scalable hyperparameter sweeps, interactive analysis, and automated workflows. Integrated with CoreWeave ARIA to support autoresearch, autonomously improving a model based upon detected signals. 
- Post-Training improves model quality and cuts latency and cost using your own production signal, with no training cluster required. Serverless SFT (supervised fine-tuning) and Serverless RL (reinforcement learning) let you experiment with your own training recipes.
- CoreWeave Registry lets you manage, discover, and deploy your AI assets. It’s a single source of truth for models, agents, and datasets across the AI lifecycle.
CoreWeave Forge provides a durable system of record for efficient AI development from first agent to best agent. Every dataset, evaluation, model version, trace, and deployment stays connected. Now teams can understand what changed, why it changed, and whether the change actually improved results. 

### Run inference your way
Every stage of the cycle, from deployment to evals, depends on inference. But what you need from an inference solution depends on what you’re building and the demands of each workload. CoreWeave Inference gives you the flexibility to choose the right approach. 
With Serverless Inference you can start building with a catalog of open-source models while CoreWeave manages the infrastructure. With Dedicated Inference you run models on isolated compute, with control over model weights, deployment settings, and GPU resources. As your needs evolve, you can move between the two without replatforming. 
Teams use both approaches in production. Cline leverages open-source models in Serverless Inference to power their open-source, open-choice coding agent trusted by over 11 million developers.The AI writing assistant Grammarly uses Dedicated Inference to scale efficiently, with explicit GPU selection and fully managed operations.
Inference is more than just serving a static model. When you’re continuously improving a model through reinforcement learning, the lines between training and inference start to blur. Inference becomes part of the training loop itself: the policy generates rollouts, training produces updated weights, and those weights return to serving so the next round of rollouts uses the latest policy. Keeping that loop moving requires infrastructure that can quickly put updated weights into use.
Today, we’re expanding Dedicated Inference with RL rollouts (New Service), built on the same NVIDIA Dynamo foundation that powers CoreWeave Inference. RL Rollouts brings updated checkpoints into a live deployment with minimal downtime. If you're running your own RL training loop, CoreWeave hot-loads those checkpoints so you can generate rollouts with the latest policy and keep the next round of training moving. We have partnered with NVIDIA and you.com’s engineering team to post-train NVIDIA Nemotron 3.5 Lightning on CoreWeave using RL rollouts in NeMo gym with you.com’s web search API, improving the model reload latency 15x against baseline.

## Partners help close the loop
Forge connects the five stages of the AI loop. But your loop doesn't stop at our edge; it reaches into the observability platform, the data warehouse, and the security stack your team already depends on, tools we didn't build and aren't asking you to replace.
The CoreWeave Partner Network is designed to ensure you can operate your AI application on your terms. It includes partners across infrastructure, data services, ISVs, and models and inference. Each solution is tested and proven on CoreWeave under real production conditions before it reaches you.
That same principle extends past the tools you already run: an agent that can't search the live web is stuck reasoning over what it knew at training time. This is why the CoreWeave Partner Network is extending to the tools your agents call, starting with search. Exa, Parallel Web Systems, and You.com join as partners to give agents built on CoreWeave a search layer, reachable through one integration instead of a separate contract for each.

## CoreWeave Forge fits your infrastructure
Though CoreWeave Forge runs best on CoreWeave Cloud, we also recognize that you don’t run all your workloads in one place. You have workloads on other clouds, your own private data centers, and across a broad computing footprint.
With CoreWeave Forge, you’re free to build with any model, framework, or cloud. It runs where your workloads live. The improvement data you generate stays yours in portable form, with open interfaces at the seams. Curated datasets and evaluation suites become your competitive advantage. And you can use them wherever you choose: not just through open interfaces and standards, but also with our partners. Your data. Your stack. Your AI.

## Start building faster on CoreWeave Forge
We announced CoreWeave Forge at Fully Connected 2026 because we believe the future of AI belongs to fully connected systems, not disconnected workflows. The teams moving fastest today don’t just deploy models. They continuously improve them. CoreWeave Forge helps make compounding improvement possible by bringing running, observing, curating, improving, and evaluating closer, so your team can move faster. CoreWeave Forge works with the infrastructure and tools you already use. So there’s no migration tax, fragmented workflows, or manual stitching between systems. 
With CoreWeave Forge, every deployment feeds what you build next. From first agent to best agent. When the entire AI loop stays connected, each version starts ahead of the last, and those gains compound over time.
Everyone can start building with CoreWeave Forge today. Try CoreWeave Forge Pro free for 30 days. Real credits across every product line let you run the whole AI loop end to end, so every version compounds before you commit. Start your free trial.

That’s why we created CoreWeave Forge. Now it’s your turn to build what’s next.
 Start building on CoreWeave Forge
 Explore CoreWeave Forge
 Leverage our experts in CoreWeave ARENA‍

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
