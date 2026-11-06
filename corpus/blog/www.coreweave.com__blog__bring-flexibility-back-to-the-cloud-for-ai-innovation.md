# Bring Back AI Cloud Elasticity with CoreWeave Flex | CoreWeave Blog

Source: https://www.coreweave.com/blog/bring-flexibility-back-to-the-cloud-for-ai-innovation

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

For a long time the cloud sold a simple idea. You could start small, scale infinitely, and pay only for what you used. That promise created space for new ideas to flourish because the “what if this works” moment didn’t come with a capacity cliff.
Once you’re scaling with GPUs, AI teams have learned they can’t rely on that behavior. Just like all applications, AI demand runs in waves. Training and evaluation come in iterative cycles. Inference rises and falls through the day, across regions, and across product moments you can’t always predict. The variability isn’t the problem. The problem is that you can’t count on capacity showing up when demand rises unless you pay for it all the time, and “on-demand” doesn’t always feel on-demand when it matters most.
That has a real cost that doesn’t show up on a bill. It changes how teams innovate. When capacity can’t be trusted, teams stop building toward the upside. They over-protect early ideas with always-on commitments, or they keep projects small because scaling feels like a risk. Either way, the cloud stops being the place where new ideas can grow.

## CoreWeave Flexible Capacity Plans bring innovation back to the cloud
We’re fixing that with CoreWeave Flexible Capacity Plans. Most clouds still force a blunt tradeoff. You either overbuy always-on capacity to protect availability, or you rely on best-effort scaling when demand spikes, risking interruptions when it matters most. The goal isn’t more pricing complexity or buzzwords. It’s a simple controllable way to match cost and certainty to how AI actually runs, so innovation isn’t gated by capacity tradeoffs that don’t fit the workload.

## Where predictability meets agility in the cloud
Customers already use two familiar modes on CoreWeave. Reservations cover the steady baseline when you know you need capacity continuously. On-Demand covers incremental best-effort top-up. The gap has been everything in between: workloads that are variable, still growing and often fluctuate day to day where paying full 24×7 economics is wasteful, but best-effort availability is not an acceptable risk. Flexible Capacity Plans add two run options that close that gap.

Flex Reservations, launching in preview, are guaranteed capacity for workloads that rise and fall. You choose a ceiling and CoreWeave guarantees access up to that level. The difference is you’re not paying full 24×7 economics just to keep the guarantee. Flex introduces a holding fee that maintains the guarantee and usage charges when instances are actually running. It’s a better fit where utilization is uneven, adoption curves are uncertain, and the “this worked” moment needs to be met with capacity, not best-effort availability. This is also where we think the differentiation is clear: CoreWeave is setting a new standard by guaranteeing capacity without requiring customers to pre-schedule exact windows or overbuy full-time reservations just to innovate.
Spot is now generally available as a lower-cost option for work that can tolerate interruption. The important part is that interruption is explicit and comes with several minutes of notice and clear signals, so teams can shift work off the node before it’s terminated. This will allow customers to plan for the interruption. Spot is delivered as a node pool type in CoreWeave Kubernetes Service (CKS) with clear preemption signaling and operational guardrails, so teams can design reliable checkpoint-and-recover workflow. For experiments, backfills, batch work, and overflow, Spot gives teams a straightforward way to trade interruption tolerance for lower cost.

### A portfolio approach to AI capacity—from proof to production
Most teams will run a mix of these plans because most AI environments are a portfolio. A steady baseline is real. Peaks are real. Best effort, batch work is real. The right model does not force all of those needs into one shape. It gives teams a simple framework: reserve what is steady, use Flex when peaks must be protected, and use Spot or On-Demand when work can move or when best-effort is acceptable.
In practice, this portfolio shows up as teams move from early testing to real operation. They prove a workload, start to ramp it, and suddenly the question shifts from performance tuning to whether capacity will be there when demand rises. CoreWeave ARENA supports the proof step by letting teams run real workloads end to end under real conditions. Flexible Capacity Plans are built for the ramp and scale step that comes next. And for many teams, what comes next is operating that workload in production. One of the clearest places that shift shows up is inference.

## Production inference needs clarity, not hidden tradeoffs
‍That predictability matters even more in inference because inference isn’t a deployment milestone anymore. In production, it’s something you operate day-to-day, under constantly changing demand. Traffic shifts. Latency targets tighten. Models evolve. Cost becomes an everyday discipline. It’s tempting to reduce operational burden by abstracting away infrastructure details, but the tradeoff will almost certainly show up later. Teams lose clarity into chosen GPU classes, runtime behavior, time-to-serve expectations, and the real drivers of cost and performance at exactly the moment they need to manage them most. And when pricing is disconnected from those underlying drivers, unit economics can become harder to forecast, explain, and optimize as usage scales

‍
CoreWeave AI Inference is built to support the full lifecycle, from model experimentation to deploying with production clarity. 

### Serverless Inference
Developers should be able to run the best open-source models on-demand, pay in simple tokens, and build their application without managing infrastructure directly. This is possible with Serverless Inference in Weights & Biases, built on CoreWeave infrastructure. And when teams need light customization, they can bring LoRA-style adapters to their base models without standing up and operating dedicated inference infrastructure.
Serverless Inference in Weights & Biases
‍

### Dedicated Inference (Preview) 
When it’s time to deploy and scale, platform teams should be able to run inference on chosen GPU classes, on open runtimes, with infrastructure-aligned economics and operational visibility that stays useful under real demand. This is possible on our newly announced Dedicated Inference offering. It’s designed for teams that want lifecycle support without giving up the knobs and visibility they’ll need once inference becomes business-critical. This foundation also pairs naturally with Flexible Capacity Plans because inference is one of the clearest examples of wave-shaped demand. Many teams will reserve a baseline, protect peaks with Flex, and use Spot for tolerant background work like batch scoring, evals, backfills, or overflow. That’s a common operating pattern in production. 

### Inference on CKS 
If customers want even further control of the infrastructure, and want to run additional services or application components next to their models, they can leverage our industry leading Kubernetes offering to deploy directly on to the hardware. CoreWeave Kubernetes Services offers an accelerated and inference-focused platform for the most control of application deployment. 
Customers such as Cline are rapidly moving inference workloads to CoreWeave to take advantage of high-throughput, low-latency inference.
“Cline is the leading open-source, agentic coding platform for large global enterprises. As adoption grows, so does the need for scalable inference capacity, especially for companies seeking to remain model agnostic. We use the Serverless Inference in Weights & Biases to support enterprise-ready environments for our most security-sensitive customers. ”  
Saoud Rizwan, Founder, Cline
Across all three entry points, the principles stay the same: keep execution clear, keep the economics continuous, and keep visibility into how performance and cost behave under real demand.
So whether teams run inference directly on CKS, adopt lifecycle-supported execution through Dedicated Inference, or use Serverless Inference, the principles stay the same: clear execution, infrastructure-aligned economics, and visibility into how performance and cost behave under real demand.

### Innovation should not be gated by 24x7 pricing
AI demand will keep moving in waves. Teams shouldn’t have to fight that reality with one-size commitments or best-effort risk. Flexible Capacity Plans restore the practical elasticity pioneers need so new ideas can grow, successful workloads can scale, and production systems can be operated with control instead of guesswork. And as more of those systems become production inference, the mandate is simple: match each workload to the right capacity model, keep the economics consistent, and make scaling predictable.
>> Learn more about CoreWeave’s Flexible Capacity Plans

>> Learn more about CoreWeave Dedicated Inference

>> Find out more about W&B Inference

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
