# Flex Reservations and Spot Explained | CoreWeave Blog

Source: https://www.coreweave.com/blog/how-coreweave-spot-and-flex-reservations-work-and-when-to-use-each

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

AI demand isn’t flat, even when workloads run continuously. Some work needs always-on capacity, some needs guaranteed headroom, and some can trade interruptions for cost. That mix requires more than a single capacity model.
To support these diverse workloads, CoreWeave Capacity Plans now include four models—Reservations, On-Demand, Spot (GA), and Flex Reservations (preview). Each model is designed for a different workload pattern. 
Designed to match AI workloads that aren’t always steady, Spot and Flex Reservations expand how you balance guarantees, cost, and utilization. This post explains how each works in practice and when to use them.
‍
Capacity Plans Mix

## Flex Reservations: Guaranteed capacity without overbuying
Traditional reservation models offer guaranteed access but introduce the challenge of overprovisioning. When you reserve GPUs for 24/7 access, you pay for them whether they’re fully utilized or not. For AI teams with fluctuating workloads, that often means paying for idle capacity and underutilized infrastructure.

 21% budget loss | An estimated 21% of enterprise cloud infrastructure spend is wasted on underutilized resources.
(Harness Press Release, February 2025)(Harness Press Release, February 2025)

Flex Reservations are designed to change that, separating guaranteed access from full 24/7 run-rate pricing. Flex Reservations provide:
- Guaranteed access up to your Flex Reservations ceiling
- A lower holding fee to keep that capacity reserved (idle or running)
- A complementary usage rate that applies only when GPUs nodes  are in use 
Most clouds force a binary choice. Commit and pay continuously or stay flexible and give up capacity guarantees. With this new offering, CoreWeave sets a new standard by reserving capacity without overprovisioning. 
No more overbuying full-time reservations just to innovate. You secure the capacity you need for the long term, but your cost structure better aligns with actual utilization.

### How Flex works
From an operational perspective, nothing changes in how you deploy workloads. The change is in the commercial structure beneath it.
- You reserve a peak ceiling
- You pay a 24/7 holding fee
- You pay usage charges only when instances are in use
With Flex, you commit to a defined peak capacity (for example, 200 GPUs). That capacity is reserved for you up to that ceiling throughout the term, just like a traditional Reservation.
The reservation is continuous, but the cost is not.
Instead of paying full run rates around the clock, you pay a lower holding fee to keep that capacity reserved. That holding fee keeps the GPUs set aside for you so they’re available when you need them. The key change is simple. You are paying to hold the capacity, not paying full run rates when you are not using it.
When you actually spin up and use those GPUs, you pay a usage rate. When you scale down below your peak, you stop paying the usage rate on idle capacity and only pay the lower holding fee. That means your total cost flexes with real utilization, while your access does not.
The end goal is a cost model that reflects true AI usage—without forcing teams to plan down to the minute, or predict exactly the amount of capacity they will need.

### Spot: Lower-cost compute for interruptible workloads
Not every workload needs guaranteed uptime. Some jobs are inherently fault-tolerant while others are experimental, batch-based, or opportunistic. For these use cases, paying a premium for guaranteed capacity doesn’t always make sense.
Spot instances offer lower-cost access to GPUs with no long-term commitment, designed for workloads that can tolerate interruption.

## How CoreWeave Spot handles preemption differently
Like other Spot-style offerings in the market, these instances can be preempted, but for the right workloads the savings can be significant.
CoreWeave Spot surfaces preemption as a clear signal with advance notice, giving workloads time to checkpoint and shift work before a node is terminated.
If a Spot node is going to be preempted, you will receive:
- Explicit termination signaling: you receive explicit preemption signals and a defined notice window to checkpoint before termination, so interruption is manageable, not chaotic
- Defined preemption notice window: CoreWeave provides a defined advance notice window before termination, giving workloads time to checkpoint and drain cleanly
Other clouds typically offer shorter or variable notice periods, depending on the product tier and instance type. CoreWeave gives you more time to pause, pivot, and plan for when a spot reservation will be interrupted.

### Take Spot for a spin
We’ve said we designed Capacity Plans for real-world AI. Now you can test it on real-world infrastructure, with real benchmarks and real insights.
For Spot instances, CoreWeave ARENA provides a way to test them before you scale. You get a controlled environment to run end-to-end workloads under production-like conditions. Test performance, understand cost behavior, and evaluate scaling dynamics before committing to Spot or long-term capacity.
If your focus is production inference workflows, Weights and Biases Inference is another path built on CoreWeave infrastructure. It lets teams deploy and iterate within existing ML workflows while keeping visibility into performance and cost as demand evolves, including explicit GPU type selection.

### Is your workload a good fit for Spot?
For teams that build with resilience in mind, Spot can dramatically reduce the cost of experimentation and large-scale processing. At a high level, Spot works best when workloads are:
- Checkpointable: training jobs that regularly save model state, so progress isn’t lost
- Retry-safe: jobs that can automatically restart from the last saved step
- Distributed or fault-tolerant: systems where losing a node doesn’t collapse the entire job
- Non-urgent or batch-based: backfills, experiments, evaluation runs, and overflow workloads
Interruption ahead? Make sure you’ve designed for it. The most successful Spot users treat interruption as a design constraint, not an exception. At a high level:
- Checkpoint frequently enough to limit lost progress
- Separate control and worker nodes, so control logic survives instance termination
- Use orchestration frameworks that automatically reschedule terminated nodes
- Blend capacity types, running critical components on guaranteed capacity and elastic components on Spot
Many teams combine Flex or Reservations for baseline and peak guarantees, while shifting less critical work to On-Demand or Spot when fault-tolerant to reduce total cost.
The result is a portfolio approach: guaranteed where it must be, interruptible where it can be.

## Capacity planning that works for the realities of AI workloads
The cloud shouldn’t force you into tradeoffs that slow AI innovation or inflate cost. It should be built to support how AI works in the real world, including unpredictable spikes and undulating demand. Spot and Flex Reservations give teams more ways to match cost and certainty to how workloads actually behave, so you can spend less time guessing and more time building. 
A simple way to think about the mix:
- Use Spot for interruptible work where savings matter and your system can tolerate preemption. If you want to validate behavior first, test it with your own workload in CoreWeave ARENA.
- Use On-Demand for unpredictable work that can wait for available capacity, but cannot handle interruptions

- Use Flex Reservations when you need guaranteed access for peaks without paying full 24/7 run rates when you are not running at peak.

- Use Reservations for steady baseline workloads that need predictable, always-on capacity.
Whether you’re experimenting or scaling, there’s now a clearer way to choose the right capacity model.
- Learn more about CoreWeave’s flexible capacity plans.
- Test out GPU instances easily with low-cost Spot instances. See how it works in CoreWeave ARENA before committing to a contract.
- Learn more about the CoreWeave Cloud platform is fully integrated and purpose-built to power pioneers’ most complex AI workloads.
Ready to commit to smarter economics? Contact our team to learn more about Flex Reservations.

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
