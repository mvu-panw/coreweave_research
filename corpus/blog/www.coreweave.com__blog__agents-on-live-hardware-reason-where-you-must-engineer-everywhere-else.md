# Data center anomaly detection with AI agents

Source: https://www.coreweave.com/blog/agents-on-live-hardware-reason-where-you-must-engineer-everywhere-else

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

An AI data center is a physical system. Power draw, inlet temperature, coolant flow, fan speed, all sampled continuously. Somewhere in that stream is the node that might interrupt a training run.
We wanted agents to find it first. The question was never whether to use them. It was where. Point an agent at every part of a problem and you get a system that is slow, and capable of giving you a different answer on Tuesday than it gave on Monday.
So we gave them two different jobs: offline, building a deterministic anomaly detector, and live, reasoning only about what it flags. That split turned out to be the most useful thing we learned.

## An agent can build the tool, or be the tool 
The familiar version is a coding assistant: describe a problem, and the agent writes something that solves it. When it finishes, the agent is done and the code is what you keep. That is one of two ways to use an agent, and the difference that matters is whether the agent is still there when the system runs.
You can use an agent to build the tool. The agent works offline, explores the data, interprets the requirements, and assembles a pipeline from conventional machine learning and data processing components. What ships to production is that pipeline. The agent is not there when it runs.
Or you can use an agent as the tool. The agent sits inside the running system. It is called on live data, reasons about what it sees, and produces an answer. Take the agent away and the system stops working.
Neither is the lesser choice, and the interesting problems need both. Ours did.

 | 
 | Agents to build the tool
 | Agents as the tool

 | What the agent does
 | Works offline: explores the data, assembles and tunes the pipeline
 | Runs inside the live system, reasoning over each case

 | What runs in production
 | Conventional ML and data processing code
 | The agent: model, tools, and context

 | Best suited for
 | Repetitive, well-defined, constantly running
 | Open-ended, varied, each case genuinely new

 | Same input, same output?
 | Always
 | Not guaranteed

 | Cost profile
 | Expensive to build once, then cheap on every data point
 | Cheap to set up, then a real cost on every call

 | How you explain a result
 | Inspect the code and the model
 | Read the reasoning the agent produced

Figure 1: The two agent modes, side by side. 

‍
Detecting anomalies in data center telemetry needs both. It breaks into two questions, and they are not the same kind of question. Find anomalous events. Then explain them, and guide the resolution. The first repeats millions of times a day and should give the same answer every time. The second needs judgment, because no procedure written in advance covers every case.
Figure 2: Workflow schematic. Agents building the detection pipeline on the left, agents reviewing and analyzing flagged anomalies on the right.
‍

## Part 1: Agents to build anomaly detection tools
Anomaly detection runs continuously, across every channel, forever: five million signals a day. No operations team can watch that. The failures that matter are also subtle: a node degrades slowly, across several channels at once, in a pattern that looks unremarkable on any one of them.
Putting an agent in the live path would mean asking it to judge every one of those signals. The problem is that the same input should always produce the same output, and language models work the other way: they sample from a distribution, and even at low temperature the same prompt can return a different answer on a different run. Useful when you want a fresh perspective, disqualifying when you are deciding whether a node is failing. An operations team needs a detector that behaves the same way every time.
So we used agents to build the detector instead. What the agent gets is a harness rather than a prompt: a working environment with tools to profile the telemetry, engineer features, train candidate models, and score its own results against a held-out set of labeled incidents.
The harness is where the design lives. It fixes what the detector has to achieve, hands the agent the means to get there, and checks every candidate against the same held-out incidents. The agent can rewrite the code. It cannot move the goalposts. It repeats that cycle until the metrics stop improving, and we review what comes out before anything reaches production.
Setting that up is where the engineering goes. The features that matter have to come from somewhere, so we sat with the engineers who run the fleet and worked out which signals actually carry a failure and how to represent them. The definition of a real incident is ours too, and that is what the agent scores itself against. Point an agent at a complex system with no requirements and you get something that detects plenty and means nothing.
Given that kind of environment, AI agents are genuinely good at this work. One placed first out of 685 submissions on a materials-science benchmark, reasoning about the underlying physics rather than brute-forcing the search. The full write-up is in Tabular ML didn't die. It was just waiting for agents.
The interesting part is that a non-deterministic process produces a deterministic artifact. The agent varies. What it hands over does not: feature definitions, model weights, thresholds, post-processing. Ordinary code and a fixed model, versioned, diffable, and reviewed by a person before it goes near production. Run it twice on the same signal and you get the same answer, forever, on every one of the five million that arrive each day.
This is not a one-off step, and that is the shift worth noticing. A deterministic tool used to be expensive enough to build that you shipped it and left it alone for a year. When an agent does the building, the same tool gets rebuilt whenever the data moves. New telemetry arrives, or a failure mode presents differently, and the agents revisit the pipeline and refine it. It stops being frozen.
An engineer stays involved throughout. They decide what the tool has to do, check that what comes back measures the right thing, and send it round again when it misses. The agent makes each round fast. The judgment is still theirs.

## Part 2: Agents to reason about anomalies and to recommend actions
Explaining an anomaly and guiding the resolution is a different kind of problem. When an anomaly is flagged, the questions are open-ended. Is this real? What caused it? What should be done about it?
Answering those means combining things that are hard to codify. A training job slows down but nothing fails outright. The cause could be the GPU, the network, or storage, and an experienced operator would know which to check first. There is no pipeline to build in advance, because the useful procedure is the one you write after you have seen the case.
Here the agent is the tool, assisting the reasoning and the debugging. Each flagged event arrives with a signal window, related signals, and the node's position in the cluster. The agent can query historical telemetry, pull additional information about the node, and search prior incidents and runbooks. It returns a judgment on whether the anomaly is real, a recommended action, and the reasoning that got it there.
The harness matters here too, for a different reason. Asked to explain an anomaly from memory, an agent will produce something plausible, and sometimes something invented. This one cannot answer from memory: every claim it makes has to come from a tool call it ran. That does not guarantee the answer is right. It does mean an engineer can check where it came from.
What it does not do is act. An agent can be confidently wrong about a root cause, and on a live cluster that mistake costs far more than the convenience of automating it. Every recommendation goes to a human with the evidence attached, and the decision stays theirs. Any system that can affect physical infrastructure needs explicit safety rules covering what it may do, when it may act, and when a person has to approve.
What makes this affordable is scope. The agent only ever sees the events the detector has already surfaced, not every data point. That filtering does more than keep the reasoning practical: a detector that flags a thousand things a day is worse than useless, because operators stop reading it and the real event lands in a queue nobody trusts. Precision is a design requirement.
Figure 3: How the two modes work hand in hand to funnel five million signals down to five daily alerts.
‍

## What early anomaly detection buys us
Threshold-based alerting often fires only after an issue has started. For some types of issues, it does not fire at all and the outage is the first signal.
The detector can surface issues minutes, hours, or even days before they affect a customer. That lead time gives the data center operations team, and the reasoning agent, an opportunity to investigate the signal, identify the underlying problem, and resolve it before it becomes a customer-facing failure.
The value is not in automating one particular remediation. It is in creating a window to understand what is happening and choose the right response.

## The physical AI loop, applied to our own data centers
What we have described is the physical AI loop, applied to our own data centers. We observe the telemetry coming off the machines, curate it down to the few events worth attention, improve the pipeline as we learn, and evaluate each candidate against known incidents before it merges. Then it runs, and the next turn starts.
What makes it interesting is what moves between the two modes as the loop turns. Over time, new patterns arise that can be codified in the deterministic system. An agent reviewing anomalies sees the same situation twice, recognizes that a class of anomaly is regular enough for a simple deterministic rule, and proposes one. That proposal goes to the engineer who owns that hardware. That is where the decision belongs: they are the ones who can judge whether the rule describes a failure mode worth alerting on.
This is not hypothetical. The reasoning side has already proposed a rule that now sits with that engineer. An agent used as a tool ended up building a tool.
Work starts expensive and flexible. What proves repeatable gets codified and moves to the cheap, predictable side. Most agent deployments get more expensive as they scale. This one is built to get cheaper.

## What it took to build
Three things had to be in the room for this to work, and most projects are short at least one of them.
The first is data with history. A detector is only as good as the incidents you can train it against, and that archive takes years to accumulate. Mission Control has been collecting and acting on fleet telemetry at this scale for longer than the detector has existed.
The second is people who have seen failures. Finding patterns is the easy half. Knowing which patterns are worth an alert, and which are noise that looks like signal is a judgment that accumulates over years of operating the hardware.
The third is the engineering to join them. Hand an agent a dataset and you get a model. Hand it a harness, a set of requirements, and an engineer who will send it back when the answer is wrong, and you get something an operations team will run.
Each of those exists somewhere. Getting all three pointed at the same problem is the harder part.

## None of this is specific to data centers
A data center is a physical system with sensors on it. So is a battery pack on a test rig, a robotic arm, or a race car. The parallels are close: continuous sensor data, rare events that matter, and the same three ingredients in short supply.
Supplying that combination inside customer engineering teams is what CoreWeave's Physical AI Field Engineers do. They scope the problem, stand up the infrastructure, and turn scattered test and sensor data into a model whose findings change something physical: a setup gets adjusted, a part gets replaced. A fault caught and corrected before it becomes a failure is the work described above, on someone else's hardware.
The same split applies: a tool gets built from the team's own data, it runs predictably, and the engineers keep every decision that matters. What is changing is who builds the tool.
‍
See how Physical AI Field Engineering applies this to engineering data 
Hear the engineering version of the same question: what makes a model trustworthy enough for a domain expert to act on
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

CoreWeave for Physical AI,

Copy code

Copied!

CoreWeave for Physical AI,
