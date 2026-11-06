# Open Models Can Win on Cost and Control | CoreWeave Blog

Source: https://www.coreweave.com/blog/why-open-models-can-win-on-enterprise-cost-and-control

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

If you're running inference at scale, your model choice is now a line item, not a capability bet. That shifts the open model vs. closed model debate away from one that most industry pundits are having today. 
Rather than asking, “Which model is best?” enterprises are asking the question that actually determines success: “Which model will efficiently run at scale?”

## The gap between open and closed models has condensed
Kimi K3 shipped on July 16 with a 1 million-token context window, native vision, and a sparse mixture-of-experts architecture. In independent testing, it scored a 60 for intelligence, behind only three closed frontier models at release. Moonshot published the open weights on July 27, as committed. 
Since then, DeepSeek published their V4 Flash and Pro 0813 models, Alibaba published the Qwen 3.8 series, and Z.ai published GLM-5.3-Flash. All these models vie for the frontier across a number of different applications, not just writing code.
That changes the enterprise conversation. A model you can download now performs within a few points of the best closed systems money can rent. For most production workloads, "is it good enough" stopped being the question.

## Inference is where the savings live
Training a model has a large, fixed up-front cost. Inference is both a perpetual enabler and an ongoing cost: every user request, every agent step, every retrieval call, every token. That is why serving economics, even more than benchmark scores, decides what enterprises actually run at scale.
The current math is hard to ignore. On the high end, typical latest-generation frontier models cost approximately $50 per million tokens. Moonshot hosts Kimi K3 at $15 per million tokens, while serving a right-sized open model on your own GPUs typically runs closer to $1 per million tokens. Cost analyses this year put the break-even for self-hosting near 5 to 10 million tokens a day. 
Kimi K3 derived from published API procing of $3 per million input tokens and $15 per million output tokens. Frontier and self-hosted figures are illustrative and subject to model, hardware, and utilization assumptions.
Per Stanford's 2026 AI Index, the best open model now scores within about 3.4% of the best closed model, and according to MIT, open-weight access averages roughly one-sixth the price. Managed inference providers, CoreWeave included, enable the scaling advantages of a closed model provider without any ongoing fixed costs.
Open weights also hand you the levers that move cost-per-token: quantization, batching, right-sized hardware, and distillation into smaller task models. Kimi K3's own API launched at $3 per million input tokens and $15 per million output, matching a leading closed model. The difference is that with published weights, the API price is a ceiling, not a floor.

## Control is the deeper advantage
Once you’ve hosted your first model, you can fine-tune it. With open weights, tuning happens on your infrastructure, on your data, with nothing shipped to a third party. Closed vendors offer fine-tuning at their discretion, and that discretion moves over time.
Distillation follows the same logic. A growing production pattern in 2026 is a large teacher model distilled into small, cheap, task-specific students. Most closed providers can update their terms of service to prohibit patterns like distillation at any time. Open licenses generally do not prohibit it, and a frontier-class open teacher makes the pattern more valuable, not less.
Then there are guardrails. A vendor's moderation layer is tuned to the vendor's risk profile, not yours. Enterprises in regulated industries need guardrails tuned to their own policies, deterministic filters where regulators demand them, and the ability to inspect, version, and freeze the exact model that passed validation. Open weights make all of that possible. And no deprecation notice can retire a model sitting in your own storage.

## And, not or
There is a place in the world for both models. Closed, frontier models have embedded guardrails and can be a great way for enterprises to start adopting AI in the workplace. As enterprises scale their AI usage, iterating on open models enables cost optimization and greater control in high-volume paths where unit economics decide whether a feature ships.
Between cost optimization, iterative training loops, sovereignty, and more nuanced guardrails and controls, open models empower enterprises in ways that may be difficult for closed models to generalize across all industries.

## Open weights need serious infrastructure
The savings above are not automatic. They assume serving done well: high GPU utilization, interconnects that keep large models fed, autoscaling that absorbs traffic spikes without breaking the latency SLA. Weak infrastructure quietly gives back everything the open weights saved.
That is the work CoreWeave was built for. If your team is weighing a move from closed-source API access to add open-model serving, we can help you model the unit economics before you commit a single GPU.
‍Want to run Kimi K3 on CoreWeave? You can deploy the open weights today with Dedicated Inference—bring your own model weights and serve them on dedicated GPU infrastructure through an OpenAI-compatible endpoint—or run them entirely under your own control on CoreWeave Kubernetes Service.
For other open weights models:
- ‍Deploy DeepSeek V4 Pro (0813) on Serverless Inference: deploy a leading model for coding tasks and agents
- Deploy on Serverless Inference: pay-per-token serving, no cluster to stand up
- See CoreWeave Mission Control: GPU, network, and storage behavior in real time
- Try CoreWeave ARIA in preview: put an agent to work as a researcher, to fine-tune and improve your models
‍Kimi K3 is not yet part of the Serverless Inference model catalog; currently available pay-per-token models are listed here. Benchmark results, rankings, and third-party pricing referenced in this post are as of July 2026 and subject to change. Use of third-party models is subject to the applicable model license.

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

Inference,

Copy code

Copied!

Inference,
