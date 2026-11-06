# How nTop Hit NASA’s 2030 CFD Goal Early on CoreWeave | CoreWeave Blog

Source: https://www.coreweave.com/blog/10000-les-simulations-in-32-hours-ntop-and-coreweave-hit-nasas-cfd-2030-target

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

It makes no sense to get on an airplane that hasn’t been physically tested before boarding. But the reality is that while (many) thousands of designs are investigated by engineering teams,  only a handful can actually be physically tested. The role of simulation in engineering is vital and irreplaceable.
Whether it’s the flight for your last business trip, the car you drove to pick up your kids, or the appliances in your home, physics-based simulation is essential to how engineering enterprises design their products to be safe and predictable. 

## How physics-based simulation powers modern engineering
Engineering simulation is best understood as a set of computational methods that let engineers test physics in software before committing to hardware, materials, prototypes, or field trials. At the highest level, the taxonomy is aligned with the kind of physics being modeled. Many of these simulations are non-linear, which complicates the efforts and methodologies required to get accurate approximations of design performance.
“The world is non-linear, it’s true. But fear not, for here is a clue: When signals are small, and stabl’ overall, x˙ = Ax will do.”  

### From fluid dynamics to structural deformation: The many forms of engineering simulation
Computational Fluid Dynamics (CFD) predicts fluid flow and heat transfer in applications ranging from aerospace and transportation to energy systems and climate modeling. Since most practical flows are turbulent, turbulence modeling remains a fundamental challenge in CFD. Its importance extends beyond predictive accuracy: turbulence is a major source of viscous drag, and approximately 30% of global energy consumption is spent overcoming drag in transportation systems 1.
Structural simulation, often called Finite Element Analysis (FEA), predicts how parts deform, vibrate, fatigue, crack, or fail under load, which is central to safer buildings, lighter vehicles, stronger machines, and more reliable infrastructure. 
Electromagnetic simulation models fields, antennas, motors, chips, sensors, and power systems. 
Molecular and materials simulation looks at behavior at atomic or microscopic scales to help discover better batteries, polymers, semiconductors, drugs, and advanced materials. 
Multiphysics simulation couples several of these domains together, because real products rarely experience just one kind of physics in isolation.

### 10,000 drone simulations in 32 hours
nTop is a computational design and simulation platform used by leading aerospace, defense, and advanced manufacturing teams to build the kind of complex geometry that traditional CAD can't handle reliably. Its solver, nTop Fluids, runs CFD natively on GPUs.
nTop and CoreWeave's physical AI team partnered on a joint proof of concept to test the limits of what a single simulation engineer can accomplish in roughly one day, using nTop Fluids on CoreWeave's GPU cloud infrastructure.
The present work is a joint Industrial Test Case which simulates aerodynamics for different drone designs, leveraging nTop Fluids software on CoreWeave Cloud. The goal was to test the boundary of what’s possible for engineers today—how many designs could be evaluated (i.e. simulations ran) in about 1 day as an aerodynamicist/simulation practitioner? 

### What Is Large-Eddy Simulation (LES), and why is it so expensive to run?
We chose Large-Eddy Simulation (LES) deliberately, primarily because it’s a higher-fidelity approach than the Reynolds-Averaged Navier-Stokes (RANS) methods most engineering teams rely on. RANS averages turbulence into statistical approximations, which is fast but loses important physical detail. 
LES directly resolves the large turbulent structures in the flow and only models the smallest scales, which makes it significantly more accurate and orders of magnitude more compute-intensive. That cost is the reason LES has historically been reserved for one-off "capability" calculations rather than large-scale design studies.

### What it takes to run 10,000 CFD simulations without human intervention
Demonstrations like this show what becomes feasible when scalable software and purpose-built infrastructure come together: higher volumes of simulations, shorter time intervals, at higher levels of fidelity. The full study ran headless with no manual intervention required to fix software or infrastructure issues, and scaled reliably end-to-end. The two key ingredients were nTop Fluids' ability to robustly generate and simulate geometries, and CoreWeave Cloud,  purpose-built for AI workloads and accelerated by the latest NVIDIA GPUs.

### Designing the experiment: 2,400 drone variants across 5 angles of attack
A Design of Experiments (DoE) methodology was used to systematically explore the design space and identify high-performing configurations. Each design was represented by a set of parametric variables—such as airfoil thickness—that were varied across predefined ranges. Sampling combinations of these parameters generated a diverse population of drone geometries, as shown in Figure 1, enabling broad coverage of the feasible design space.
In total, 2,400 drone planform geometry variants were considered across five angles of attack, for a total of 10,000 simulations. Angle of attack refers to the orientation of the wing relative to the oncoming airflow, which changes as a drone climbs, descends, or maneuvers. Testing across multiple angles captures how each design performs across a range of flight conditions. The base geometry used for this study was a fully parametric Group 3 long-endurance fixed-wing UAS, which was built in nTop.

### Hitting NASA's CFD Vision 2030 target four years early
By executing a massive ensemble of 10,000 Large-Eddy Simulations (LES) within a 32-hour window, this work marks a paradigm-shifting milestone that directly realizes the ultimate operational goals outlined in NASA's CFD Vision 2030 Study 2. 
A foundational pillar of the 2030 vision dictates that engineers must be able to "conceive, create, analyze, and interpret a large ensemble of related simulations in a time-critical period (e.g., 24 hours)" to routinely impact critical engineering decisions [2]. Historically, high-fidelity, turbulence-resolving methods like LES have been restricted to isolated, slow "capability" calculations due to their severe computational expense. Transitioning LES into a high-throughput framework capable of running ten thousand iterations in near-day turnaround effectively bridges the gap between high-fidelity physics and massive capacity computing. This achievement demonstrates the automated workflows, extreme parallelism, and next-generation numerical scaling that NASA identified as a 2030 target.

### Explore the full dataset: A live results dashboard
As visualized in the video above in Figure 2, each simulation provides a field of aerodynamic values both on the surface of the drone as well as in the field around it. The computational workload of the simulation in general is to execute a numerical method that strives to estimate the solution to the physical equations which govern aerodynamics. 
These values, like pressure and velocity, are often post-processed on the fly in the same simulation software to also provide additional metrics that help judge if a design is ‘good’ or ‘bad’, like the drag coefficient for example. Designers therefore have a wealth of information for each design, which they can use however they like to ascertain performance. For this case study, we have created a live dashboard in Figure 3 to iteratively explore the full test matrix of simulations ran as a part of this study. 

## Why CoreWeave for Engineering Simulation and CFD

### What engineering HPC workloads need from a cloud
We find ourselves at an interesting nexus between the rapid and sustained growth of cloud compute, which support a large diversity of workloads, and the unrelenting need for High Performance Computing (HPC), which is a necessity for the majority of Original Equipment Manufacturers (OEMs) and the engineering community that make the things indispensable to our daily lives. OEMs and engineering teams increasingly expect automation, autoscaling, and resilience from their cloud providers. For these simulations and computational methods to run in containerized applications, Kubernetes has become the de facto orchestrator for containerized workloads, and studies have shown it can run HPC applications with no measurable performance penalty versus bare metal3 .

### How CoreWeave delivers credible cloud HPC
The PoC on CoreWeave’s GPU Cloud Powered by NVIDIA is compelling because it demonstrates exactly the kind of converged cloud HPC environment that engineering simulation teams increasingly need: one that preserves the performance expectations of legacy HPC workflows while adding the portability, automation, and operational flexibility of cloud-native infrastructure. 
Many simulation workloads cannot be cleanly split into independent parallel tasks; they depend on tightly coupled GPU and CPU communication, predictable interconnect behavior, fast storage, containerized software stacks, and scheduler patterns that HPC users already understand. 
CoreWeave brings those pieces together through purpose-built accelerated compute, high-performance networking, Kubernetes-native orchestration, and Slurm-compatible workflows. This approach makes CoreWeave Cloud an ideal platform for modernizing CFD and adjacent simulation workloads—without forcing teams to abandon the operating models their solvers were built around.
That matters because the engineering simulation community is not simply looking for “cloud GPUs”; it is looking for infrastructure that behaves like credible HPC. A CoreWeave demonstration can therefore move the conversation from theoretical cloud migration to concrete engineering value: faster time-to-solution, repeatable containerized runs, access to modern GPU acceleration, and a path for legacy simulation codes to run in a cloud environment designed for the realities of HPC rather than retrofitted around them.

### What this unlocks: CFD in physical AI
The value of running 10,000 high-fidelity simulations in 32 hours is not just to find the specific best design for this design campaign; it is the dataset itself. A campaign of this scale and geometric diversity, produced at LES resolution, is large enough to serve as the training foundation for machine learning surrogate models—models that predict aerodynamic performance directly from geometry parameters, orders of magnitude faster than running a new simulation per query.
This is exactly the bridge from classical CFD into physical AI that CoreWeave's Cloud platform is built to support. 
Moving compute-heavy physics simulation off legacy CPU clusters and onto modern GPU clusters is only the first step. The second step closes the loop: using simulation outputs to train ML models that compress optimization cycles, power digital twins, and predict real-world performance with the speed engineering teams actually need to make decisions. CoreWeave's physical AI platform—bare-metal NVIDIA GPU clusters, integrated experiment tracking through Weights & Biases, and forward-deployed engineering expertise—brings those pieces together for teams working across aerospace, automotive, semiconductors, materials, and energy.

## Run your simulations on CoreWeave
Whether you're modernizing CFD pipelines, exploring larger design spaces, or training the next generation of engineering surrogate models, CoreWeave Cloud provides a purpose-built platform for simulation workloads that can scale beyond on-premise infrastructure. Fixed workstation and CPU cluster capacity rarely allows the kind of campaign-scale runs that high-volume DoEs and design space exploration demand. Our physical AI team partners directly with engineering and scientific organizations to make studies like this routine, not the exception.
Explore Physical AI on CoreWeave >
Read the engineering perspective from nTop >
‍
1 Beneitez, Miguel, et al. “Improving turbulence control through explainable deep learning.” arXiv preprint arXiv:2504.02354 (2025).
2 Slotnick, Jeffrey P., et al. CFD vision 2030 study: a path to revolutionary computational aerosciences. No. NF1676L-18332. 2014.
3 Sochat, Vanessa, et al. "Usability evaluation of cloud for HPC applications." Proceedings of the SC'25 Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis. 2025.‍
All images and videos courtesy of nTop.

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

CoreWeave for Physical AI,

Copy code

Copied!

CoreWeave for Physical AI,
