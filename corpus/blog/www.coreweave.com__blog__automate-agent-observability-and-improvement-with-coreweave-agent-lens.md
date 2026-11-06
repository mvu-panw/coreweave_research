# CoreWeave Agent Lens: Automate Agent Observability and Improvement

Source: https://www.coreweave.com/blog/automate-agent-observability-and-improvement-with-coreweave-agent-lens

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Product development has entered a new era. AI agents are now the default engine powering all new applications across all industries, from customer support and enterprise logistics to scientific research and physical AI.
Applications based on agents offer an ever-widening range of new capabilities, but also lead to countless new failure modes, frustrating experiences for end-users, and operational hazards such as runaway costs and concerns around safety and compliance.
Detecting and addressing these failure modes early is instrumental to rolling out safe, powerful, and high-quality AI functionalities at scale.
This new era demands a new generation of observability tools. Ones that can process vast amounts of user-agent transactions, and automatically identify failures, capability gaps, and runaway trends.
That’s why we’re introducing CoreWeave Agent Lens.
Agent Lens is built to automate agent observability and let builders focus on two core questions: what are users asking of their agent and how does it fail to carry out those tasks?

## Turn production traffic into prioritized insights

Leaning on CoreWeave’s world-leading AI infrastructure, Agent Lens is capable of ingesting and analyzing the entirety of your agents’ OpenTelemetry tracing data and extracting insights at an unprecedented scale. Agent Lens automatically surfaces semantic clusters of user intents and agent failures, with no configuration necessary, greatly accelerating time to detection and remediation.
A dashboard can show that a metric moved; Agent Lens explains which behaviors are driving the change. It analyzes production conversations, detects semantically related events, and organizes them into clusters that teams can review and act on.

### Detect recurring failures automatically
Failure detection begins with the full production corpus, not a small, manually sampled set. Agent Lens identifies conversations that share the same underlying failures even when the wording, tool sequence, or surface error differs. It groups those cases into failure clusters, links each cluster to the specific evidence in its source traces, and provides representative examples for review.
Teams can rank issues using signals such as frequency, change over time, and affected workflows. Instead of reading traces one by one, they can start with the failures that matter most, inspect the supporting evidence, and move directly into root-cause analysis. As new traces arrive, clusters continue to update, making regressions and emerging patterns easier to spot before they spread.

### Understand customer intent and capability gaps
Insights also cluster conversations by user intent. These clusters show what customers are asking the agent to do, how demand changes over time, and where requests exceed the agent’s current capabilities. Product managers can use that evidence to distinguish an isolated request from an emerging need, while engineers can connect high-demand intents to the failures that block successful completion.
Intent and failure views are more useful together. A frequently requested task may deserve investment even when its failure rate is modest. A less common intent may require immediate attention when failures create safety, compliance, or customer-impact risk. Agent Lens gives teams the production evidence to make those tradeoffs explicitly.

### Turn conversations into customer insights
Agent Lens turns large volumes of customer conversations into prioritized themes. Automatic intent clustering provides a current view of what customers are trying to accomplish, while failure clustering highlights where the agent struggles to complete those tasks. Product and engineering teams can review the same evidence, identify emerging needs, and focus improvement work without manually labeling every conversation.

## Align every evaluation with your quality standards
Generic checks can’t capture every business-specific expectation. A support agent may need to follow an escalation policy, a research agent may need to cite the correct source, and a financial services agent may need to meet additional accuracy and compliance requirements. Agent Lens lets teams create custom LLM judges from the failures they discover in production.
Domain experts define the expected behavior and score a set of representative examples. Agent Lens compares human labels with judge outputs, surfaces disagreements, and supports iterative refinement of the judge criteria. Teams can review false positives and false negatives, clarify the rubric, and improve alignment before applying the judge broadly.
Once aligned, the judge can score new production traces automatically. This turns expert knowledge into a scalable quality signal and makes previously hidden failure modes measurable over time. Preconfigured signals run on CoreWeave inference and are optimized out of the box, helping teams begin automated evaluation within minutes of connecting traces.

### Test each candidate fix against real failures
Detecting a failure is only useful if the team can determine whether a change fixes it. Agent Lens converts production failures into test cases that preserve the input, relevant context, expected behavior, and evaluation criteria.
From a failure, make a test call with a candidate prompt, model, tool configuration, or code change. Review the response and judge the results beside the original production case to see whether the proposed fix addresses the specific problem. Then run the candidate against the full evaluation set to measure the aggregate effect and identify regressions in other behaviors.
This creates a practical release gate. Teams can compare the current agent with one or more candidates, inspect example-level differences, and promote a change only after the new agent performs better on real production cases. A fix ships because it has been tested, not because it merely looks reasonable in a single replay.

### Turn production evidence into continuous improvement
Agent Lens keeps the improvement loop connected. A failure cluster can become an evaluation set. An aligned judge can score the current agent, and each candidate changes. Validated results can guide the next prompt update, tool change, model choice, or training run without copying context between disconnected systems.
Connect coding agents, such as Claude Code, through Skills and MCP so they can work directly with production evidence. With the appropriate permissions, an agent can retrieve a prioritized failure cluster, inspect representative traces, propose a change, make test calls, run the evaluation set, and summarize the result for review. Teams remain in control of what is approved and promoted while automating the repetitive work between insight and verification.
Over time, every production failure strengthens the evaluation system. The test set grows with real-world behavior, judges become better aligned with domain expectations, and teams gain a repeatable path from detection to diagnosis, fix, and validation.

## Start improving production agents
Agent Lens, part of CoreWeave Forge, aims to power your agents’ full auto-improving loop, converting discovered failures into test cases to enable regression testing before shipping updates to production. Agent Lens is built for enterprise workloads, providing the scale, flexibility, and control that pioneers demand. It is available in public preview today on CoreWeave’s hosted cloud (dedicated and on-prem coming soon). Insights and online LLM judges are free until the end of 2026. Log your agent traces and start improving your agents in Forge today.

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

Agent Lens,

Copy code

Copied!

Agent Lens,
