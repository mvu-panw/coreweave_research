# CoreWeave Sandboxes for Agentic AI | CoreWeave Blog

Source: https://www.coreweave.com/blog/run-agentic-workloads-safely-at-scale-with-coreweave-sandboxes

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Until recently, models learned about the world by reading. They consumed text, predicted the next token, and produced more text. They didn't touch anything.
Today's most capable models act. They generate code, call tools, navigate browsers, and take actions on behalf of users. The training loop for agentic AI now requires execution. Agents explore action spaces and run the code they generate, and that code can be powerful, but it can also do damage.

 When an agent runs
 
 rm -rf /
 
 because it thinks that's what it's supposed to do, the deletion should stay contained. The agent should learn what its actions actually do. The cluster around it should stay intact. That's containment at the sandbox level. Running thousands of sandboxes reliably, in parallel, without one failure reaching the next. 

The teams pushing this hardest are running Reinforcement Learning (RL) at scale, building agentic workflows, and evaluating continuously. Today, they have three imperfect choices: build their own sandbox infrastructure, buy capacity from a separate vendor, or restrict what their agents are allowed to try. Each choice compounds operational debt as research scales. Engineering hours are spent on plumbing, compute capacity is underutilized, and governance gaps increase operational and security risks.
There’s a fourth option available today in public preview. CoreWeave Sandboxes is an execution layer for RL, agent tool use, and model evaluation at scale. You can run sandboxes on your own capacity across multiple CoreWeave Kubernetes Service (CKS) clusters, or as a serverless runtime on CoreWeave-managed compute.

### Built for how you actually train
Frontier research means letting agents explore action spaces and execute the code they generate. That work happens in an execution layer.
On CKS, your platform team configures sandboxes to match how you train. CoreWeave Sandboxes runs every sandbox inside its own Kubernetes pod, governed by a profile that defines network policies, resource limits, and namespace boundaries. Administrators set the boundaries once, and every sandbox a profile produces inherits them. 
On the serverless runtime, you start with code, not configuration. CoreWeave manages the cluster with strong security boundaries and runs every CPU sandbox inside a Kata Container by default, giving each sandbox its own hardware-virtualized kernel, filesystem, and network. It is one of the strongest isolation models available for these workloads, and it comes out of the box. Researchers authenticate with an existing W&B API key, install the Python client, and start running sandboxes in minutes. No clusters to provision. No infrastructure decisions to make. Your ML engineers stay focused on running sandboxes in a secure, enterprise-grade environment.
One failure stays in one sandbox. Memory spikes, infinite loops, and OOM errors are confined to the pod that produced them. Researchers scale rollouts to the thousands without one rollout's failure reaching the next.

CoreWeave Sandboxes solves a real gap in our AI research stack: secure, isolated code execution at scale directly in our existing compute. Our reinforcement learning workflows spin up thousands of sandboxes in parallel per training step, each with its own container image and resource boundaries. Adoption is frictionless—researchers run sandboxes within minutes of a 
 pip install cwsandbox
 no infrastructure knowledge required.
Brian Belgodere, Senior Technical Staff Member: AI/ML Systems, IBM Research

### Iterate while you run
When agent rollouts fail at scale, the information needed to find the failure mode usually lives across disconnected systems: sandbox lifecycle events in one, training metrics in another, LLM traces in a third. When 37 of 1,000 evals fail, finding which 37 means correlating timestamps across systems that don't share context. Debugging costs compound with run size.
Every sandbox is part of the training run. Sandbox lifecycle events land in the same W&B run timeline as your metrics, indexed alongside the rollouts they belong to. W&B Weave traces connect to per-sandbox execution, so every model call, tool call, and return value is correlated with the sandbox that produced it. The agent's code, inputs, and outputs are captured per sandbox and stored alongside the run, queryable later.

You don't switch systems or reconstruct context from infrastructure logs. You stay in the run.

### Get more from the compute you already have
Capacity is tight, and RL training pushes sandbox counts into the thousands per step. When routing to a separate sandbox vendor, sandboxes add inter-cluster latency, a second billing model, and another capacity ceiling on top of the one you're already pushing against.
On CKS, CoreWeave Sandboxes schedule across the clusters you already operate, picking up capacity wherever it opens up, including idle CPUs on your GPU nodes when you run them alongside SUNK. Profiles define the compute footprint each sandbox can access: instance type, CPU and memory, storage.
Managing separate clusters and scheduling sandboxes across different node types lacked a unified solution, costing us time and resources. CoreWeave Sandboxes eliminated that issue. We now run hundreds of concurrent sandboxes on CPU nodes and alongside Slurm training jobs on GPU nodes, all through a single setup. The Python SDK let our researchers get started immediately, and the CoreWeave team worked closely with us to adapt the open-source SDK to fit seamlessly into our codebase.
Roman Soletskyi, AI Scientist, Mistral

### Start running sandboxes
CoreWeave Sandboxes is available today through two consumption paths, both built on the same Python client and the same CoreWeave-managed control plane.

 For platform teams running training on CoreWeave, sandboxes are enabled in your existing CKS cluster with one CLI command. CoreWeave manages the control plane that handles authentication and request routing, and deploys a Runner inside your cluster that schedules and manages each sandbox. Your team doesn't deploy or operate either. Researchers install the Python client ( 
 
 pip install cwsandbox
 
 ) and run sandboxes immediately with no Kubernetes interaction.

1from cwsandbox import Sandbox
2
3with Sandbox.run() as sandbox:
4 result = sandbox.exec(["echo", "Hello Sandboxes!"]).result()
5 print(result.stdout)
6

 For researchers and applied AI teams who don't have a CKS cluster, or who want to extend their existing compute, CoreWeave serverless sandboxes are available through Weights & Biases. Install the SDK (
 
 pip install wandb[sandbox]
 
 ), authenticate with an existing W&B API key, and start running sandboxes in minutes. No clusters to provision, no profiles to configure, no infrastructure decisions to make. Your ML engineers stay focused on running sandboxes in a secure, enterprise-grade environment.

Because serverless sandboxes run through Weights & Biases, the platform features come built in. Every sandbox is pre-authenticated to your Weights & Biases identity, so calls to W&B Models and W&B Weave from inside the sandbox already know who you are. No API keys to pass, no credentials to mount. Secrets your agents need are injected securely from your W&B Team secrets store. Sandbox lifecycle events land in your W&B run timeline, and W&B Weave traces connect every model call and tool call back to the sandbox that produced it. Usage is tracked per org and included in your W&B plan, so there's no separate billing relationship to manage.
1from wandb.sandbox import Sandbox
2
3with Sandbox.run() as sandbox:
4 result = sandbox.exec(["echo", "Hello Sandboxes!"]).result()
5 print(result.stdout)
6

### The right execution layer for AI development
Models don't get trained once anymore. They get improved continuously through RL, agent tool use, and large-scale evaluation. The teams doing that work need an execution layer that runs at their pace, on their compute, without adding operational weight.
CoreWeave Sandboxes is that execution layer, on your own clusters or as a serverless runtime.

#### Get started
Existing CoreWeave customers can enable sandboxes directly in the Cloud Console.
Teams looking for self-service access can get started through Weights & Biases: Docs
 pip install wandb[sandbox]

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

Sandboxes,

Copy code

Copied!

Sandboxes,
