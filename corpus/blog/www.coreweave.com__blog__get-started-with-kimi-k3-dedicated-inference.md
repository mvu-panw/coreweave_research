# Deploy Kimi K3 Dedicated Inference on CoreWeave

Source: https://www.coreweave.com/blog/get-started-with-kimi-k3-dedicated-inference

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

CoreWeave customers can deploy Moonshot AI's newest flagship release Kimi K3 on Dedicated Inference, bringing their own weights to CoreWeave. CoreWeave handles the deployment on NVIDIA GB300 NVL72 systems, with optimized support to serve Kimi K3's architecture efficiently.

## Get started with Kimi K3 on Dedicated Inference
Getting Kimi K3 running on Dedicated Inference works the same way as any other custom deployment: upload the weights to CoreWeave AI Object Storage, then create a gateway and a deployment pointing to them, choosing GPU class and the runtime. CoreWeave provisions a tenant-isolated gateway that handles authentication, load balancing, and routing, and schedules the deployment across the GPUs you selected. From there, your endpoint is live, with min/max replica autoscaling and the routing work described above running underneath it. Billing is per GPU-hour against the GPU class you chose, with no egress or ingress fees on top. The step-by-step guide in our technical documentation will walk you through the following steps:
- Stage the Kimi K3 weights and the DSpark draft model in a CoreWeave AI Object Storage bucket.
- Grant Dedicated Inference access to that bucket.
- Create a gateway to expose the model.
- Create the deployment with the validated Kimi K3 engine configuration.
- Wait for the deployment to load the weights and start the engine.
- Send an inference request to verify the endpoint.
- Clean up the gateway and deployment when you're done.
Get Started with Kimi K3 on Dedicated Inference
CoreWeave doesn't provide Kimi K3 weights or a license. You must bring your own valid license. Review Moonshot AI's license terms before deploying Kimi K3.

## A 2.8 trillion-parameter open-source model built for frontier-level performance
Kimi K3 is the largest open-source model currently available. It's a 2.8 trillion-parameter mixture-of-experts architecture, with benchmarks that land close to the top proprietary systems from other frontier labs. As of August, Kimi K3 has a score of 60 on Artificial Analysis's Intelligence Index, an independent benchmark spanning reasoning, coding, and knowledge tasks. It also ranks #2 on LMArena's Frontend Code Arena, topping all models except Claude Opus 5 Max in blind developer comparisons.
The model ships with a one-million-token context window, native visual understanding, and an always-on reasoning mode called "thinking mode," built on two architectural techniques Moonshot developed internally: Kimi Delta Attention (KDA), a hybrid linear attention mechanism, and Attention Residuals (AttnRes), a replacement for standard residual connections that delivers consistent scaling gains.

## How CoreWeave serves Kimi K3 at production scale
Serving Kimi K3 is not simply a matter of fitting its weights onto GPUs. At production scale, the challenge is increasing concurrent request volume while preserving time to first token and per-user decode throughput, particularly for agentic and multi-turn workloads that repeatedly reuse long contexts.
CoreWeave benchmarked Kimi K3 on NVIDIA GB200 and GB300 NVL72 across concurrency levels ranging from 1 to 32 users, using 16 GPUs on each platform. These benchmarks reflect agentic workloads — multi-turn, tool-calling interactions that place sustained pressure on throughput and latency in ways single-turn benchmarks don't capture, with a 95% cache hit rate sustained throughout testing. We evaluated performance across three dimensions: output token throughput per GPU, mean request latency, and p50 decode throughput per user. The resulting Pareto frontiers show the relationship between infrastructure efficiency and user interactivity at each concurrency level.
On GB300, Kimi K3 continued scaling through concurrency 32, reaching 198,000 TPM per GPU. From concurrency 4 through 32, GB300 delivered lower p50 TTFT than GB200, with reductions of 23% at concurrency 4, 32% at concurrency 8, 18% at concurrency 16, and 97% at concurrency 32. At concurrency 32, GB300 delivered 198,000 TPM per GPU compared with 64,000 TPM per GPU on GB200, which is 209% higher. Its p50 decode throughput was also 133% higher. GB200 peaked at 149,000 TPM per GPU at concurrency 16. Performance dropped sharply beyond that point, making concurrency 32 unusable for GB200 for latency-sensitive interactive workloads.
For this workload, GB300's larger HBM capacity and additional AI compute provide enough headroom to sustain twice the practical concurrency of GB200. GB300 also delivered 18% to 32% lower p50 TTFT, while supporting more simultaneous long-context requests without the sharp throughput degradation observed on GB200.

## Inside the stack: NVIDIA Dynamo and vLLM support for Kimi K3
Hardware alone isn't enough. Extracting the full performance of Kimi K3 requires coordinated optimizations across the serving stack, from cluster-level scheduling to model-specific runtime kernels. At the infrastructure layer, CoreWeave serves Kimi K3 on NVIDIA Dynamo. At the runtime layer, CoreWeave serves Kimi K3 through vLLM, incorporating optimizations developed by the vLLM team, Moonshot AI, and NVIDIA.
When a user submits a Kimi K3 deployment through the CoreWeave inference API, the inference stack built on NVIDIA Dynamo renders the Dynamo Frontend and Worker components across CoreWeave-managed infrastructure. Each Kimi K3 deployment spans at least 2 GB300 NVL72 nodes (8 GPUs) so a single NVL72 rack hosts up to 9 replicas. Production-grade deployments scale across multiple racks, with each replica pinned to a single NVLink domain so tensor and expert-parallel traffic stays on the NVLink switch instead of falling back to IB across racks.
The same stack supports KV-cache aware routing to ensure repeat queries are sent to replicas with warm prefixes. This is especially critical for reducing token cost and optimizing for high throughputs for multi-turn agentic, coding, and long-context workloads. It also supports speculative decoding (MTP or bring your own speculators such as Inferact/Kimi-K3-DSpark or RadixArk/Kimi-K3-DSpark) improves per-user decode TPS and prefill/decode disaggregation lets each component scale independently for higher throughput and lower TTFT.
Dedicated Inference is built for models like this: — ones that need real infrastructure work to run well, not just space to fit their weights. Bring your own Kimi K3 license and weights, and CoreWeave handles the rest, so you get a production-ready endpoint without owning the serving stack yourself.
Get Started with Kimi K3 on CoreWeave Dedicated Inference

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

Inference,

Copy code

Copied!

Inference,
