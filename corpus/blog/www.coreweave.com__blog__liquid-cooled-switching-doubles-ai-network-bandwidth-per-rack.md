# CoreWeave Brings Liquid Cooled Switching to AI Networking | CoreWeave Blog

Source: https://www.coreweave.com/blog/liquid-cooled-switching-doubles-ai-network-bandwidth-per-rack

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In modern AI cloud infrastructure, networking has become a strategic component, one that determines how effectively GPU compute translates into goodput for training and inference performance. That's a fundamental shift from traditional cloud infrastructure, where networking was often treated as plumbing, simply moving bits from one point to another. As liquid cooling enables rack-scale systems like NVIDIA Vera Rubin NVL72 to deliver exaflops of compute, the network must evolve alongside them. Just as compute has adopted liquid cooling, networking is following the same technique, with liquid cooling enabling new switch chipsets that deliver massive performance in a compact form factor.
With liquid cooled switches, the network is no longer the limiting factor for what these accelerators can achieve. Trillion-parameter models, agentic systems running multi-step reasoning and parallel actions, and RL pipelines with their tight inference-training loops all depend on fast, low-latency communication between GPUs. Liquid-cooled switches let you push more bandwidth through denser rack configurations, so you can architect a network fabric that fully utilizes GPU and CPU resources within and across multiple racks.
At CoreWeave, we design networking as a foundational layer of the AI cloud to ensure the fabric is never a bottleneck. With the deployment of Vera Rubin NVL72, we became one of the first cloud providers to deploy NVIDIA Spectrum-X Ethernet SN6600-LD, the industry's first fully liquid cooled 102.4 Tb/s Ethernet switch.

## Ultra high performance with liquid-cooled switching 
CoreWeave deployed the NVIDIA Spectrum-X SN6600-LD as the switching fabric for Vera Rubin NVL72. Built on the NVIDIA Spectrum-6 ASIC and fully liquid-cooled, the SN6600-LD delivers 102.4 Tb/s of switching capacity across 64 × 1.6 Tb/s ports using 200G SerDes, doubling the per-lane bandwidth of the previous generation while fitting into a compact 2U form factor. This combination of density and performance, made possible by liquid cooling, enables an unprecedented 1.64 Pb/s of switching capacity per rack.
To put 1.64 Pb/s of switching capacity into perspective, the network could transfer the entire text collection of the Library of Congress approximately 160 times every second, sustained at full load and without congestion. Delivering the full networking bidirectional GPU-to-GPU bandwidth is needed when you are continuously improving your agents or training models.
With the density and capacity of the SN6600-LD, CoreWeave provides a fully non-blocking, multi-plane, multi-rail spine and leaf fabric connecting Vera Rubin NVL72 GPUs without oversubscription. For customers running large scale training, this translates directly into higher model FLOPS utilization (MFU) by cutting network latency, giving every GPU full bandwidth, and keeping GPU idle time near zero For inference workloads, it delivers consistently low latency, which means faster response times, higher throughput, and better accelerator utilization.
NVIDIA Spectrum-X SN6600-LD deployed in CoreWeave Data Center

## Unified and programmable management for liquid cooling  
In “A Deep Dive on CoreWeave Innovations for NVIDIA Vera Rubin NVL72,” we introduced Valvey and Racky, part of CoreWeave Mission Control, that manages Vera Rubin environmentals. Valvey and Racky’s management domain also includes the NVIDIA Spectrum-6 SPX rack, bringing the same unified monitoring and control to both Vera Rubin NVL72 and SN6600-LD Ethernet switches. 
Valvey is our patent-pending programmable per-rack liquid cooling valve assembly that monitors and controls flow rate, temperature, pressure, and leak detection. Extended now to the Spectrum-6 SPX switch rack, Valvey brings the network into the same thermal management loop as Vera Rubin NVL72.  
Racky, our rack control manager, aggregates power, cooling, and environmental sensors into a single interface. It monitors rack health, controls valves and power functions, and surfaces telemetry such as leak detection, flow rates, and temperature. Rather than monitoring each rack's subsystems independently, Racky presents everything through a unified management layer that connects directly to CoreWeave's broader infrastructure stack.
In addition to Valvey and Racky, the Rack Lifecycle Controller (RLCC) automates the deployment, operation, and lifecycle management of AI infrastructure at the rack level. Rather than managing individual devices, RLCC treats an entire rack including GPUs, networking, power, and cooling systems as a single programmable resource. RLCC orchestrates firmware, configuration, health monitoring, and recovery across every component. That's what makes high-density AI infrastructure repeatable to deploy, without the operational complexity that usually comes with it.
For customers, the operational result is simplicity through a unified rack management domain that is software-defined and programmable with one control surface, one observability layer, and one capacity model covering both compute and network fabric. Unlike air-cooled systems, the management overhead required for separate power monitoring, separate thermal management, and separate incident response workflows has been made obsolete with CoreWeave Mission Control. 
Once compute and network fabric run under a single observability and capacity model, the signal feeding the rest of the stack gets more reliable too. That's what lets a research and iteration agent like CoreWeave ARIA, built into Weights & Biases, give researchers cleaner answers when they're iterating on a model. The telemetry it's reasoning over comes from infrastructure that's already unified, making our entire stack a competitive advantage for AI researchers to work smarter and faster. 

## Denser, faster, cooler: New efficiency gains
Liquid-cooling allows the SN6600-LD to sustain line-rate switching performance at full density without thermal constraints. In a standard 48U rack, 16 SN6600-LD switches can be deployed, delivering 1.64 Pb/s of total switching capacity. At that scale, the choice between air-cooled and liquid-cooled switching stops being a component-level decision and becomes an infrastructure architecture decision, one with compounding consequences across space, power, and operational complexity. Replacing the air-cooled Spectrum-4 based SN5600/SN5610 with the liquid-cooled Spectrum-6 based SN6600-LD across this topology produces three measurable gains:
100% increase in total switching performance per rack. The SN5600/SN5610 delivers 51.2 Tb/s of switching performance across 64 ports of 800Gb/s on 100Gb SerDes. The SN6600-LD delivers 102.4 Tb/s across 64 ports of 1.6Tb/s on 200Gb SerDes, doubling performance capacity, port speed, and per-lane bandwidth in the same form factor.  
62.5% reduction in rack footprint and floor space. With the higher density and capacity, the SN6600-LD switching infrastructure consolidates rack footprint and floor space by 62.5% for 16,000 Vera Rubin GPUs. Higher switching capacity in a smaller footprint means more GPU density per square foot and more room for cluster expansion within a fixed data center space, reducing the total cost per square foot.
30% improvement in power efficiency. Liquid cooling is substantially more efficient than air cooling, and that efficiency shows up directly at the switching layer: the SN6600-LD improves power efficiency by 30% compared to the SN5600/SN5610 for 16,000 Vera Rubin GPUs. The megawatts saved reduce costs, simplify operations, and free up power for higher GPU density.
Per-rack efficiencies of liquid cooled NVIDIA Spectrum-6 SN6600-LD vs air cooled SN5600 when connecting 16,000 NVIDIA Vera Rubin GPUs 
Together, these efficiencies mean CoreWeave reduces the carbon footprint per unit of AI compute delivered by consuming less power, space, and material per unit of compute, while delivering twice the switching performance per rack. As GPU clusters scale into the hundreds of thousands, that efficiency multiplies, making liquid-cooled switching both a performance and a sustainability advantage.

## CoreWeave delivers converged compute and network cooling with significant efficiency gains  
For the first time in modern data center design, compute, networking, and cooling are converging into a single, software-defined infrastructure layer, purpose-built for the scale of AI. The efficiency gains are unprecedented and will enable higher density with lower power and space requirements.
At CoreWeave, that convergence is already a reality. From NVIDIA GB200 NVL72 and GB300 NVL72 systems to Vera Rubin NVL72 and the liquid-cooled SN6600-LD, we have built an AI cloud where compute, networking, and thermal infrastructure operate seamlessly as one. Managed end-to-end by Valvey, Racky, and the Rack Lifecycle Controller, every component is orchestrated through a common operational model that automates deployment, lifecycle management, and thermal optimization across the entire rack.
This integrated approach enables us to deploy denser infrastructure, operate more efficiently, and deliver the non-blocking, high-performance fabric that next-generation AI workloads demand. Rather than treating cooling, networking, and compute as separate systems, we engineer them as a unified platform, allowing customers to focus on training and serving models, not managing infrastructure.
Most AI clouds still treat compute, networking, and cooling as three separate problems, solved by three separate teams. We built ours as one system, because at rack scale, that's the only way the math works. This is the AI cloud CoreWeave is building today.
Want the deeper technical walkthrough of what's covered here? Register for Inside the Rack Scale Revolution: How CoreWeave and NVIDIA Are Building the Foundation for AI's Next Leap.
See Vera Rubin NVL72 and liquid cooling in action. Watch Scaling the Agentic Era with CoreWeave.
See how NVIDIA frames the shift to gigascale, liquid-cooled networking. Read Built for Vera Rubin, NVIDIA Spectrum-6 Arrives in Gigascale AI Factories.
Get the full picture on where rack-scale AI infrastructure is headed. Join us at Fully Connected 26, September 29 to October 1, 2026.

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

CoreWeave Interconnect,

Copy code

Copied!

CoreWeave Interconnect,
