# CoreWeave's Stack for Physical AI | CoreWeave Blog

Source: https://www.coreweave.com/blog/wayve-decart-neura-robotics-nissan-all-running-physical-ai-on-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

A robot learns to fold laundry by training on thousands of simulated attempts before it ever touches real fabric. A self-driving car learns to react to a pedestrian stepping into the road, trained on millions of simulated miles before it ever drives on the road. A drone wing gets tested ten thousand times in simulation before a single prototype is built. A global car manufacturer turns historical test data into a faster vehicle development cycle. Companies like Wayve, Decart, NEURA Robotics, nTop, and Nissan don't share an industry, and they don't sit at the same point in the physical AI loop: some run the loop from simulation through deployment, others lean on a single step. What they share is the stack underneath. None of this work runs on a general-purpose cloud stitched together after the fact.
This covers that stack: compute, orchestration, tooling, and engineering expertise, and how teams draw on different parts depending on where their workload sits in the loop.

## What makes physical AI different
Physical AI closes the gap between perception and action: sensors gather real-world input, vision and 3D models interpret it, other models decide what to do, and actuators carry it out in real time. This dynamic introduces constraints conventional AI never has to deal with: millisecond latency requirements, safety-critical reliability standards, models that reason over three-dimensional space and visual input instead of flat text, and training data that often has to be generated through physics simulation rather than scraped from the Internet.
Large language models were trained on the text data already sitting on the Internet. There is no equivalent library of footage for a robot learning to fold laundry or a vehicle learning to react to a pedestrian stepping into the road, so physical AI teams have to generate that training data themselves, through simulation or synthetic alterations of the limited real-world data they do have, rather than entirely relying on collection of real-world data.

### What physical AI infrastructure has to do
Those real-world constraints translate into five requirements for the infrastructure physical AI actually needs:
- Simulation-generated training data. The compute burden starts before training even begins: infrastructure has to process massive volumes of real footage, curating it and generating synthetic versions, as well as rendering and simulating the environments and object interactions models learn from.
- Multi-modal sensor fusion. Vision, depth, force, and proprioceptive data all arrive simultaneously and need to be processed together, which demands more memory bandwidth than single-modality workloads.
- Millisecond inference. A two-second response is fine for a chatbot. It's not fine for a robot arm or a vehicle braking for an obstacle.
- Continuous retraining loops. Edge cases accumulate fast once a system is deployed, so checkpointing and fast data pipelines become operational requirements, not nice-to-haves.
- Fault tolerance with real consequences. A model failure in software produces a bad output. In a physical system, it can produce a dangerous one. That's why, for physical AI, most of that work runs in simulation and staged validation before a model earns the right to run in the real world, not in live production the way the AI loop describes for most software AI.
For a deeper walkthrough of the category, see CoreWeave's explainer: What Is physical AI?

### The physical AI loop: observe, curate, improve, evaluate, run
Meeting those requirements takes a flywheel: observing both real sensor data and simulated environments, curating and generating synthetic versions of it, improving models by training various forms with it, calling for predictions from those models in evaluation before deploying them to run in the real world. With CoreWeave's scale and performance, the flywheel runs until fidelity is reached, without infrastructure-based limitations.
The flywheel isn't theoretical. CoreWeave has built and deployed reference pipelines across physical AI workloads, so teams can see the same generate, train, evaluate, repeat running on a real problem instead of starting from a blank cluster. The examples below aren't tuned for maximum throughput, they are simple demonstrations to show what's achievable:

#### Robotic Manipulation in MuJoCo
A simulated robot arm performs a number of pick-and-place tasks in a household kitchen. We ran 4,800 simulations in 85 minutes using MuJoCo on one node, executing simulation, rendering, and data generation for each task.

#### Robotic Synthetic Data Generation in NVIDIA Isaac Sim
We used Isaac Sim as a synthetic data factory to create 10,000 randomized warehouse scene samples in just 21 minutes.  Each sample was observed by three virtual cameras and saved with labels that a perception model can learn from. It was a large, parallel generation run for labeled visual training data. 

#### Robotic Simulation in NVIDIA Isaac Sim
With NVIDIA Isaac Sim’s Franka pick-and-place example, we ran 113,000 simulations in just under 8 hours. Every episode moves a simulated robot arm, closes the gripper on a cube, transfers the cube, and measures whether placement succeeded.

#### Autonomous Vehicle Simulation in CARLA
1.25M autonomous vehicles simulations were run in approximately 12 hours in CARLA. These simulations varied weather, traffic density, map, intersection, and seed across independent one-GPU shards.

#### Autonomous Vehicle Simulation-Based Policy Evaluation in NVIDIA AlpaSim
AlpaSim renders camera observations, the model plans a trajectory and is fed back into the world environment, a closed loop that exposes compounding errors. We ran over 1,600 rollouts in under four hours. This speeds up model comparison over a variety of important scenarios to triage failure before road testing; it isn't a safety certification on its own.

#### Reinforcement Learning in NVIDIA Isaac Lab
The project trained an AI controller to reorient a cube with a simulated Shadow Hand using NVIDIA Isaac Lab and the RL-Games PPO learning method, while each GPU ran 8,192 independent hand-and-cube physics simulations in parallel. These simulations were separate attempts at the same task, not 8,192 different AI models, allowing the controller to learn from many experiences at once.
These blueprints are available today on CoreWeave. A team evaluating this stack doesn't have to take the loop on faith, they can run one directly and watch it close on their own data.

 ×

## Where physical AI is already being deployed
Three categories account for most of the demand CoreWeave sees today, and each stresses the infrastructure differently:
Robotics. Humanoids, industrial robots, and autonomous machines rely on long-running GPU jobs for policy training, model fine-tuning, synthetic data generation, and sim-to-real validation—the bottleneck is usually iteration speed, not raw model size.
Autonomous vehicles. Self-driving cars, trucks, drones, and shuttles need world model training, Vision Language Action (VLA) models fine-tuning, sensor simulation, and closed-loop evaluation, generating terabytes of sensor data per vehicle per day that has to move, store, and train efficiently.
Industrial. High-fidelity physics simulation and digital twins are moving off legacy CPU clusters and onto GPUs with a strong cloud adoption rate, letting engineering teams predict how a part or system will perform before it's physically built or tested.

## The CoreWeave physical AI stack
CoreWeave's promise to physical AI teams is that they shouldn't have to spend months stitching together simulation, training, storage, and experiment tracking before they can start building VLAs, world models, and RL policies. The platform is designed to cover the physical AI loop end to end, so a checkpoint that fails in the field traces back to the exact run and dataset that produced it, without switching tools to find out.
CoreWeave physical AI stack

### Foundational infrastructure
Everything sits on top of bare-metal NVIDIA GPU clusters (RTX, Blackwell, Hopper, and Ada Lovelace generations), delivering 96% useful compute and up to 47% lower three-year TCO than general-purpose clouds, independently verified by Signal65. NVIDIA RTX PRO 6000 Blackwell GPUs handle the ray-traced rendering and neural graphics behind high-fidelity synthetic environments and digital twins, on the same platform used to train the models learning from them. CPU compute handles the unglamorous but essential work of sensor and simulation data pre-processing.
None of that holds up without the layers underneath it. CoreWeave’s AI infrastructure features high-speed interconnects, InfiniBand and RoCE (RDMA over Converged Ethernet), move data directly between GPUs across different servers, bypassing the CPU and the overhead of standard networking. That matters because physical AI training runs often span hundreds of GPUs exchanging sensor data, simulation state, and gradients continuously throughout a job. Without that kind of interconnect, GPUs sit idle waiting for data to arrive between batches instead of computing. Distributed and object storage hold petabyte-scale sensor and simulation data without a separate pipeline bolted on. CoreWeave Kubernetes Service (CKS) orchestrates the training and simulation jobs running on top of all of it.
That orchestration doesn't lock a team in, either. CKS is standard Kubernetes, so workloads are defined in open manifests instead of a proprietary scheduler. If a physical AI team is going to spend years on one infrastructure decision, portability matters as much as performance does.
CoreWeave was the first AI cloud provider to stand up a fully validated NVIDIA Vera Rubin NVL72 system, and is the first cloud named an NVIDIA Exemplar Cloud for both training and inference and delivered leading MLPerf v6.0 results. That means when you partner with CoreWeave, you’re partnering with a cloud that gets you early access to the latest GPU generations.

### Scheduling and orchestration for long-running jobs
Physical AI workloads don't look like typical inference traffic: RL training runs, sim-to-real validation, and world model jobs are long-running and bursty in a different way. SUNK (Slurm on Kubernetes) schedules these jobs across GPU fleets, and CoreWeave Sandboxes provide secure, isolated code execution for agentic and experimental workflows.
Cost visibility runs at the same granularity as the scheduling itself. SUNK and CKS expose GPU utilization down to the job and namespace level in Grafana, so a platform team can trace spend back to the specific training run, team, or workload that generated it. Paired with CoreWeave's zero-egress pricing, the cost story a platform leader has to defend to finance is attributable by design.
For teams building distributed VLA pipelines, PyTorch Foundation's Ray now deploys directly into a customer's own CoreWeave account via CKS, giving full control over data in CoreWeave AI Object Storage while scaling training and fine-tuning workloads across accelerated compute.

### NVIDIA OSMO: orchestration for physical AI
On the simulation side, NVIDIA's OSMO, an open-source orchestrator purpose-built for physical AI, connects data generation, training, simulation, and hardware-in-the-loop testing across heterogeneous compute. In practice, the GPUs, CPUs, and specialized simulation or robotics hardware in a pipeline rarely look the same at each stage, and OSMO coordinates the handoff between them. 
A single physical AI pipeline might generate synthetic data on one type of machine, train a model on GPU clusters, then validate it directly against real sensor hardware, and OSMO is what keeps that pipeline moving as one workflow instead of three disconnected steps.

### AI development and experimentation
CoreWeave gives physical AI teams a full development and experimentation stack, backed by its acquisition of Weights & Biases: Models for experiment tracking, Registry for versioned lineage from checkpoint back to the exact data and training run that produced it, Weave for traces, evaluations, and monitoring, and ARIA (AI Research and Iteration Agent) for automating parts of the research process. The goal is that every VLA checkpoint, world model version, or RL policy stays traceable, so debugging a regression takes hours instead of weeks. This is the AI loop, tuned for VLAs, world models, and RL policies instead of chat agents.
For prototyping and exploration, CoreWeave offers open-source reactive notebooks, backed by its integration of marimo following its acquisition in 2025, giving engineering teams (many of whom are roboticists and physicists first, not AI engineers) a lighter-weight environment than a full ML pipeline for early iteration.

### Operations and observability
CoreWeave Mission Control® brings observability, fleet and node lifecycle management, and secure audit visibility together to keep large GPU fleets reliable. That matters for physical AI teams, where infrastructure failures during a training run can cost days, not minutes.
Fleet and Node Lifecycle Controllers continuously monitor for health regressions and replace nodes automatically when thresholds are met, before a degrading node silently drags down a run. In long, distributed jobs like physical AI training and sim-to-real validation, GPU Straggler Detection uses NCCL-level signals to identify the exact rank, GPU, and node causing a slowdown, and CoreWeave's internal benchmarks show that automated path runs about 3x faster than a traditional manual investigation. When something does need a human, requests route directly to the engineers who operate the platform, not a support queue reading from a runbook.

## Engineering expertise: Physical AI Field Engineering
CoreWeave puts engineering expertise, not just infrastructure, in front of physical AI customers, backed by its integration of Monolith following its acquisition in October 2025.
Physical AI Field Engineering starts with a scoping workshop, on-site with a customer's team: mapping their engineering workflows, digging into their biggest pain points, and aligning on priorities and a realistic timeline before any model gets built. From there, we don't hand over a report and step back, our engineers prototype the solution end to end, alongside the customer's team, and stay involved until it's running in production, not just running in a demo.
- Strategy. Helping identify which problems are actually worth solving with AI, and which data is worth building on.
- Simulation infrastructure. Helping customers stand up the GPU, storage, and simulation stack their workload actually needs, and connecting into CoreWeave's broader physical AI infrastructure when that need scales.
- Real-world data. Turning scattered test, sensor, and production data into a model that predicts an outcome, catches an anomaly, or explains a failure, instead of leaving that signal buried and unused.
- Agentic learning. Turning what a model finds into something that changes the physical world: a robot that executes a trained skill, a fault that gets caught and corrected before it becomes a failure, a system that gets recalibrated to run better.
What customers get isn't a report. It's a model validated against the physics of their own systems, and increasingly an agent built on top of it, run directly by the customer's own.
‍
Image supplied courtesy of nTop

## Who's building on CoreWeave
- NEURA Robotics runs a daily physical AI loop at its NEURA Gym facilities: a robot attempts a task, the team evaluates the result, collects new data, retrains, validates in simulation, and tests again on the real robot, tracked end to end with W&B Models across base training, simulation, and real-world stages. (Read the story)
- Decart trained Oasis 3, the first API-accessible world model, on CoreWeave, generating real-time, controllable simulation environments where robots learn across multi-view autonomous driving and robotics scenarios. (Read the story)
- Woven by Toyota built AutoTriage, a video AI agent that automates bug classification in autonomous driving development, using Weights & Biases to track experiments and evaluate video inputs and outputs, a 10× increase in triage speed and scale. (Read the story)
- PhysicsX trains Large Physics Models, physics-informed models that compress simulation and optimization cycles across aerospace, automotive, semiconductors, materials, and energy, on CoreWeave's cloud, and lets enterprise customers train private, domain-specific versions on proprietary data. (Partnership announcement)
- nTop ran 10,000 Large-Eddy Simulations for a drone wing on CoreWeave infrastructure in just 32 hours, achieving a NASA CFD Vision 2030 stretch goal four years early. (Read the story)‍
- Nissan paired over 90 years of historical test data with machine-learning predictions across the vehicle development cycle; a pilot on chassis bolt-joint testing cut physical prototype tests by 17%, with a rollout across Nissan's European range projected to halve total testing time. (Read the story)

## Why teams choose CoreWeave
Physical AI teams are roboticists, simulation engineers, and physicists, not cloud infrastructure specialists. On a general-purpose cloud, that gap becomes their problem to solve before they can do any actual work. CoreWeave already has that plumbing in place, purpose-built for physical AI's sustained, compute-heavy jobs, and backed by engineers who've closed the sim-to-real gap before.
Three things tend to matter most when a physical AI team evaluates infrastructure:
- Throughput on long-running jobs. RL training, VLA fine-tuning, and world model runs can take days or weeks, and bare-metal access with 96% useful compute means less of that time is lost to virtualization overhead.
- Lineage from data to deployed model. When a policy fails in the field, teams need to trace it back to the exact checkpoint, training run, and dataset that produced it, the job Registry and Weave are built for.
- Domain expertise, not just GPUs. Closing the sim-to-real gap is a physics and engineering problem as much as an infrastructure one, which is why field engineering is part of the pitch rather than an add-on.

### See it on your own workloads
Run a robotics, autonomous vehicle, or industrial AI workload on CoreWeave and see the difference bare-metal GPUs, orchestration, and field engineering make. Talk to CoreWeave about a specific project, explore the physical AI page for the latest products and customer stories, learn from our webinars, or see how the AI loop applies the same observe, curate, improve, evaluate, run cycle across every model CoreWeave runs.
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

CoreWeave for Physical AI,

Copy code

Copied!

CoreWeave for Physical AI,
