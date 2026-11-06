# Announcing distributed AI on CoreWeave with fully managed Ray on Anyscale

Source: https://www.coreweave.com/blog/distributed-ai-on-coreweave-with-ray-anyscale

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

We’re excited to announce that Anyscale, powered by Ray, can now be deployed directly in CoreWeave customer accounts via BYOC on CoreWeave Kubernetes Service (CKS).

Ray is an open-source distributed framework for parallelizing Python and AI applications. As a python-native framework that supports unstructured data formats and orchestration over heterogeneous clusters, those with CPUs and GPUs, Ray abstracts the complexity of any distributed AI workloads such as training, fine-tuning, inference, or multimodal data processing. 
Better workload balancing can help unlock the full potential of your AI ambitions. Learn in our blog how CoreWeave and Ray can maximize utilization, reduce idle time, and accelerate time to market.
Developed by the original creators of Ray, Anyscale eliminates the complexity of developing, operating, and scaling distributed data and AI workloads with Ray. Anyscale helps teams build and scale AI fast and efficiently with extensive developer tooling, resilient clusters, proprietary performance improvements (RayTurbo), and built-in governance controls—all purpose-built for Ray. 
‍
Anyscale on CoreWeave CKS
‍
With today’s announcement, CoreWeave now offers first-party support of Anyscale for CKS, making it easier than ever to run distributed AI workloads with Ray directly within your CoreWeave environment. By deploying fully managed Ray clusters in their own account, CoreWeave customers maintain full control of their data in CoreWeave AI Object Storage while being able to efficiently use a wide range of accelerated compute options. Together with the Weights & Biases integration with Anyscale via Ray, CoreWeave customers can further streamline the path to production for their AI workloads with scalable experiment tracking and artifact management.

We built CoreWeave AI Object Storage to specifically meet the needs and conquer the usual storage challenges of working with AI workloads. See how CoreWeave AI Object Storage supports the performance, speed, and scale AI ambitions need to succeed.
‍
 
Seamless Ray Workload Experiment Tracking and Observability with Weights & Biases
‍
OOTB Integration Between Experiment Tracking in W&B and Anyscale Logs
‍
Enhanced performance and reliability with distributed AI on CoreWeave

Anyscale offers many clear advantages over open-source Ray. By running Anyscale on  CoreWeave’s purpose-built AI Cloud platform, customers can make full use of AI infrastructure highly optimized for machine learning at scale.
By running Anyscale workloads on CoreWeave clusters, customers gain significant benefits that result in clear competitive advantage:
- Highly efficient cluster validation: A best-in-class validation suite performs comprehensive checks to ensure cluster readiness. This continuously evaluates infrastructure components, including GPUs, CPUs, memory, storage, and networking. It also verifies functional health to confirm the cluster is fully prepared to support large-scale, production-grade workloads at the time of delivery.

- Proactive health checking and monitoring: Automated, proactive health checks continuously monitor Ray nodes, detecting early signs of potential issues and remediating the source of anomalous behavior before it impacts workloads.

- World-class observability: Users benefit directly from a vast and ultra-granular array of metrics as detailed as GPU temperatures or real-time ingress and egress traffic right at their fingertips. Utilize powerful, intuitive dashboards with a comprehensive view of entire fleets, allowing customers to identify under-optimized workloads and correlate job interruptions to underlying issues.

- Industry-leading performance: All of these reliability and observability features combined allow customers to get the most out of their AI workloads, unlocking an industry-leading standard of up to 96% goodput. 
‍
Want to learn how CoreWeave provides up to 96% goodput across AI workloads? Learn in this blog how our AI Cloud platform optimizes every layer of the stack.
Finally, Anyscale is a fully managed platform, with access control, single sign-on with SAML, and quota management. These features are critical to scaling Ray beyond just a few clusters.
‍
Why Anyscale vs. Self-Managed Ray on CKS?

While the Ray compute framework is built for distributed execution, and KubeRay—the open-source Kubernetes (K8s) operator—can help teams get started with managing their first Ray workload, together they are just great starting foundations. To reliably scale Ray to a production-ready platform and get the most out of CoreWeave’s cutting-edge GPU infrastructure, teams still need to build out many other components that include developer tooling, comprehensive observability, cost controls, job queues, user management, and more. Anyscale shortcuts the path to production and eliminates the operational burden of building out developer tooling and managing Ray by providing: 
- Anyscale Workspaces: Use an interactive dev console with advanced workload observability to help you debug quickly, build faster, and seamlessly transition from dev to prod. This interface also makes it easy for devs to self-serve infrastructure needed for development without any K8s expertise required. 
‍
- Fully Managed Ray Clusters: Offload operational complexity with proactive unhealthy node draining and replacement, fast autoscaling, and integrated monitoring using managed Prometheus and Grafana dashboard. 
‍
- RayTurbo: Boost performance with workload-specific optimizations not available in the open-source distribution. This includes the ability to run 5x faster data preprocessing with RayTurbo Data alongside other optimizations available as part of the RayTurbo Train and RayTurbo Serve libraries. 
‍
- Budget and Cost Dashboards: Set and track budgets at the organization or project-level and receive alerts when spending limits are exceeded.
‍
- SLA-Backed Support. Get guaranteed response times from Ray experts to ensure your production AI workloads stay up and running with paid support plans.  
These are just a few of the platform components that, when combined with the CoreWeave AI Cloud platform, enable users to accelerate their production AI initiatives, take a Reinforcement Learning (RL) workload, for example:
- Using the RayTurbo distribution of RLlib, developers can use familiar Python syntax and Notebook-like IDE to set up and run jobs that can scale up to 64 GPUs and 1000’s of simulations. This can be on a wider range of RL frameworks not natively supported on the OSS distribution, such as BC-IRL and infinite (proprietary enhancements to scale out) APPO.
- With W&B, RL researchers can visualize learning curves, hyperparameter sweeps, and simulator behaviors at scale. Combined with RayTurbo’s robustness to node preemption and simulator failures
‍

### Getting Started
To get started, whether it is to scale out a multimodal data pipeline, train a model, or run large-scale inference, talk to your CoreWeave account manager or reach out to [email protected] to arrange a demo or proof-of-concept engagement.

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

CoreWeave Kubernetes Service (CKS),

Copy code

Copied!

CoreWeave Kubernetes Service (CKS),
