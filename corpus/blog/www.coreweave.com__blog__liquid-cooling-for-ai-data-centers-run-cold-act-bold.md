# Liquid Cooling for AI Data Centers | CoreWeave Blog

Source: https://www.coreweave.com/blog/liquid-cooling-for-ai-data-centers-run-cold-act-bold

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Data center operators have been  through multiple cycles of how to use liquid to cool equipment. These cycles have included full immersion liquid cooling, back of the rack liquid cooling, and liquid cooling of ambient air temperature. Notably, there has been a long period of air cooling that is now transitioning to new liquid cooling techniques. Direct-to-chip liquid cooling increases effectiveness of GPU performance, and closed-loop reduces environmental impact.
“Cooling” at the equipment level is a bit of a misnomer. Heat fluctuations from chips cause ambient temperature rises that threaten the performance of chips, and can lead to permanent damage. The goal of equipment “cooling” systems is not to chill the equipment per se, but to transfer away as fast as possible the heat that equipment generates.  
Air cooling passes air over hot materials, in an effort to transfer heat to the molecules in the air, and then away from the equipment. However, there is a limit to the amount of heat that can be transferred due to the density of molecules in air. Liquids have much greater molecular density than air, and therefore they can absorb much more heat. 
There are two important aspects to this process: how to efficiently transfer heat away from the chip, and how to keep liquid at a temperature that it continues to absorb heat from a hotter material (heat flows from hotter materials to cooler materials). Direct-to-chip approaches are highly efficient, dramatically reducing the increase in surrounding air temperature because they have direct contact with chips, and therefore conduct heat. Closed-loop approaches are more environmentally friendly because they recycle non-toxic coolant instead of constantly drawing in liquid from the surrounding area.
At the end of 2024, to stay ahead of the increasing power density and heat requirements of the latest generations of AI equipment, CoreWeave decided to invest heavily in liquid cooling when feasible. 

The early adoption of direct-to-chip liquid cooling was a significant reason why CoreWeave has been an industry leader in delivering production scale offerings of recent generations of AI equipment and large-scale clusters. CoreWeave’s decision and action has directly supported customers in their bold aspirations, including 9 of the 10 leading foundation model providers, as well as e-commerce, science, media and entertainment, and enterprise productivity organizations.
Figure 1: Direct to chip liquid cooling in a CoreWeave data center

## Every GPU is critical
The general purpose cloud’s architectural paradigm of multiple redundant services that transactions were load-balanced across, meant the degradation in performance or failure of a single server was a relatively minor event compared to the impact of such degradation in AI workloads.
AI workloads, on the other hand, require optimized performance. To maximize the value and lifespan of AI servers, silicon fatigue needs to be reduced. Secondly, the effective performance of a single workload executing over 100, 1,000, 10,000 or 100,000 GPUs can be impacted by an under-performing GPU. CoreWeave takes multiple hardware and software approaches to reliability, recovery, and performance. Liquid cooling is part of this holistic approach by reducing hardware-level errors arising from silicon fatigue and heat-damaged components.
There are two critical aspects to liquid cooling: the interface to the AI equipment and how the liquid is cooled.

### Direct-to-chip: AI equipment interface
New generations of AI chips have plates that are affixed directly to chip packages. These plates circulate liquid that transfers heat away from chips.  By taking this approach to heat transfer, CoreWeave is able to build infrastructure that is measurably more power efficient than previous generations of cooling.
Figure 2: Liquid-cooled NVIDIA Blackwell compute tray

### Closed-loop: Continuous liquid recycling
Previous generations of liquid cooling required that water continuously be drawn from the surrounding environment. Once coolant is installed in a closed loop liquid cooling system, it continuously recycles through cooling equipment (including both chillers and dry cooling). Coolant loss is minimal, requiring attention only once every few years. Aside from these periodic top-offs, the system operates without the need for supplemental water.
Figure 3: Liquid cooling for compute units

### Cool AI through AI agents
We don’t just use AI to help our clients; we also use it to manage the very hardware those clients rely on. CoreWeave leverages proactive AI agents that transform liquid cooling from a reactive drain on the environment into a strategic, more sustainable performance advantage.

### Thermal management at scale
By monitoring systems in real-time, CoreWeave’s AI agents help manage thermal increases to enable peak GPU performance while minimizing disruptions.

## More sustainable tech, stronger communities
From data center site selection to investing in cutting-edge cooling technology, CoreWeave works closely with local communities to improve sustainability and add economic value. We don’t just operate in communities; we operate as members of them. Closed-loop liquid cooling systems and other features of our AI data centers align with that commitment.
‍The sustainability edge: By putting liquid to work in a perpetual recycling loop, we eliminate the need to continuously draw water from local water supplies. This protects local resources while providing a more efficient way to transfer heat away from sensitive components. Many CoreWeave data centers use closed loop liquid cooling.

 | Feature
 | Impact on Performance
 | Community Benefit

 | Direct-to-chip
 | Higher density and zero throttling
 | Power efficiency

 | Closed-loop system
 | Reliable thermal stability
 | Recycled water

 | AI agents
 | Proactive heat management
 | Efficient power consumption

 | CoreWeave Mission Control
 | Real-time cluster optimization
 | Reduced operational footprint

## Cool AI: Rapid deployment, high performance
CoreWeave has consistently been the first to achieve production scale availability and deployment of new generations of AI systems. An important contributor to that achievement was early recognition and adoption of liquid cooling. This achievement is the result of supply chain partnerships and CoreWeave engineering’s  focus on meeting the unique demands of each new generation of AI and the communities we serve. 
Operationalizing liquid cooling at scale has rapidly transitioned to a critical architectural pillar that helps to determine how fast a company can stand up capacity, how reliably that capacity performs, how continuously capacity can be enabled to run at top-speed, and how many years the equipment will perform and be reliable.

## The data center, reimagined
The next era of AI requires more than just silicon; it requires a reimagining of the data center fundamentals. CoreWeave designs the facilities that make high-density AI a game-changing reality, ensuring that our platforms remain practical, more sustainable, and powerful at scale. 
Learn more about CoreWeave AI data centers 
Attend our webinar on Real Cloud Infrastructure for Real AI Workloads with Chen Goldberg.
Learn more about the CoreWeave Cloud platform and why it’s the Essential Cloud for AITM.
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

No items found.

Copy code

Copied!

No items found.
