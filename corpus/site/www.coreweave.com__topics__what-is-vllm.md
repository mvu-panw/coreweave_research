# What Is vLLM? | vLLM Explained for AI Inference

Source: https://www.coreweave.com/topics/what-is-vllm

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

- 
URL

- 
Publish Date
July 2, 2026
- 
Print Time

Home

Topics

AI Infrastructure and Compute

What Is vLLM?

What Is vLLM?

- What Is vLLM?

7
min read

Copied

vLLM is an open-source LLM inference engine, originally developed at UC Berkeley's Sky Computing Lab and now maintained under the PyTorch Foundation. It sits between an application and GPU infrastructure, turning trained model weights into a high-throughput, low-latency service capable of handling real, concurrent traffic.
Before purpose-built inference engines like vLLM, serving a large language model at scale was inefficient by default: GPU memory was overallocated and largely wasted, requests queued while GPUs sat idle, and costs scaled faster than usage. vLLM addresses these constraints at the engine level, primarily by solving the KV cache memory management problem, allowing teams to serve more requests from the same hardware at a lower cost per token.
This page covers how vLLM works at a technical level, where it fits in the inference stack, and how its core innovations translate to real performance gains. It also covers how vLLM compares to other inference runtimes and how CoreWeave uses it in production.

## The problem vLLM was built to solve
Running LLMs in production at scale is computationally expensive and operationally complex. A trained model alone is not user-ready or ready for real traffic out of the box. It contains weights and learned behavior, but still needs a runtime to load those weights onto GPU hardware, manage execution, handle incoming requests, and return generated tokens to an application. 
Without purpose-built serving infrastructure, GPU resources are underutilized, costs grow faster than usage, and latency degrades under load. vLLM was designed to address these challenges directly:
- More efficient GPU utilization, keeping hardware busy rather than idle between requests
- Lowering cost per token, serving more requests from the same hardware
- Stabilizing latency at scale, maintaining consistent response times as concurrent load increases
- Enabling an open-source-friendly, portable deployment approach: Apache 2.0 licensed, hardware-agnostic, and compatible with standard tooling
Once these problems are addressed, several workloads that were previously impractical or prohibitively expensive become production-viable on the same hardware. In the project’s published benchmarks, vLLM achieved up to 24x higher throughput compared to naive HuggingFace Transformers serving, on the same hardware. vLLM is Apache 2.0 licensed, free to use, and actively maintained with contributions from NVIDIA, Red Hat, UC Berkeley, and a community of over 2,800 contributors to date.
This unlocked several use-cases for vLLM:
- Self-hosted open-weight model serving: teams replace expensive frontier API calls with self-hosted open-weight models (such as Llama, Qwen, DeepSeek, Mistral) served through a vLLM endpoint, which can help reduce costs by 5-20x on bulk inference workloads
- RAG (Retrieval-Augmented Generation) pipelines: RAG workloads send the same document or retrieved context to the model across many requests; vLLM's prefix caching reuses cached computation for shared context, delivering 30-50% throughput improvements automatically
- Agentic and multi-turn workflows: vLLM's low latency and high concurrency make it well-suited for agentic workloads, where throughput directly affects how quickly an agent can complete a task, many of which involve sequential inference calls per task.
- Multi-tenant SaaS: with multi-LoRA serving, a single vLLM instance running one base model can serve many customers with individual fine-tuned adapters, without separate GPU infrastructure per customer

## How vLLM works
To understand how vLLM works, you have to understand PagedAttention, continuous batching, and prefix caching. These three capabilities supported vLLM achieving the throughput numbers cited in benchmarks; all have since been adopted, in various forms, by SGLang, TensorRT-LLM, and others.
Other key technical capabilities include OpenAI-compatible API, speculative decoding, multi-LoRA serving, quantization, and multi-GPU serving.

### PagedAttention
PagedAttention is vLLM's core memory management algorithm, introduced in the original UC Berkeley research paper. Before vLLM, serving systems reserved a large, fixed block of GPU memory for each request's KV cache upfront, sized for the maximum possible response length, wasting 60-80% of GPU memory across concurrent requests.
PagedAttention solves this by treating GPU memory the way an operating system treats RAM: breaking the KV cache into small, fixed-size pages allocated on demand and freed when a request completes. When multiple requests share the same opening tokens (a common system prompt or document), their pages are shared across requests with no redundant memory use. The result is under 4% memory waste, compared to 60-80% in naive systems.
PagedAttention, a core technology of vLLM, reduces memory waste by breaking the KV cache into small, fixed-size pages and allocating them based on demand.

### Continuous batching
Continuous batching solves the GPU idle-time problem. Traditional static batching waited for every request in a batch to finish before starting the next, leaving GPUs idle on slots whose users had already completed. vLLM removes a finished request immediately and slots in a new one, keeping the batch full at all times. GPU utilization on production traffic rises from the 30-40% range to 80% or higher on the same hardware.
Continuous batching, another vLLM capability, helps reduce idle GPU time between requests, improving overall GPU utilization.

### Prefix caching
Prefix caching solves redundant GPU work across similar requests. Traditional serving recomputed the full KV cache from scratch for every request. Even when hundreds of requests shared the same system prompt or retrieved the same document, that identical work was repeated each time. 
vLLM detects shared prefixes automatically and reuses their cached KV computation; only the unique portion of each request is processed. On RAG workloads, this typically yields a 30-50% throughput improvement with no application changes required.
With prefix caching, vLLM computes the KV cache for a shared prefix once and reuses it across every request that shares it; only the unique query portion requires new computation.

## Where vLLM sits in the stack
A useful way to understand vLLM is by separating the stack into layers.
Where vLLM sits in the serving stack: Application layer > Traffic and API layer > vLLM runtime layer > Model execution and KV cache state > Infrastructure layer (GPU nodes, networking, storage)
At the top, the application layer contains the product experience: a chat UI, an AI agent, a copilot, or a workflow tool. Below that, a traffic and API layer handles routing, authentication, and TLS termination. vLLM operates at the runtime layer, receiving requests, managing GPU-based model execution, handling the KV cache, and returning generated tokens. Below vLLM, the infrastructure layer contains GPU nodes, storage, and networking.
Applications don't interact with the GPU or the model directly; they call an API endpoint, and vLLM handles everything in between.

### Building the production stack around vLLM
vLLM is the inference engine, not the full serving platform. A production deployment typically wraps it with:
- Ingress and routing: an ingress controller (such as Traefik or Nginx) for external traffic and load balancing
- TLS termination: certificate management (such as cert-manager) to secure the external endpoint
- Observability: vLLM exposes Prometheus metrics natively at /metrics, covering request throughput, latency, GPU utilization, KV cache utilization, and queue length. Grafana sits on top for dashboards.
- Autoscaling: an event-driven autoscaler (such as Kubernetes-based Event-driven Autoscaler, KEDA) scales replicas based on request queue depth or GPU utilization
- Model caching: persistent volume or remote cache (such as LMCache) to reduce cold-start time and enable KV cache reuse across replicas
- Rate limiting: vLLM accepts all requests until KV cache is exhausted; rate limiting belongs at the gateway, not the engine

## vLLM and other inference engines
vLLM sits in a broader category of LLM inference runtimes. The right choice depends on workload, hardware, and operational requirements. For most production teams in 2026, the decision comes down to vLLM or SGLang, with the choice driven by whether structured generation and agentic workloads are the primary concern.

### vLLM vs. SGLang
SGLang is the closest active open-source competitor to vLLM. It was built with strong support for structured generation and performs well on agentic workloads, tool-calling, and pipelines with shared prefixes. On some benchmarks at high concurrency with structured output requirements, SGLang shows comparable or better throughput. For general-purpose production serving, vLLM's broader model catalog, hardware support, and community size make it the more common default.

### vLLM vs. TensorRT-LLM
TensorRT-LLM is NVIDIA's own inference stack, optimized for NVIDIA GPU hardware. It can deliver strong raw throughput on NVIDIA infrastructure, but requires compiling a model-specific engine for each combination of model and hardware before serving — a process that takes 20–30 minutes per model. This makes it a reasonable option for stable, NVIDIA-only deployments, but less practical for teams iterating quickly or supporting multiple hardware types or model versions.

### vLLM vs. TGI
Text Generation Inference (TGI) from Hugging Face was a major vLLM alternative through 2024. As of late 2025, the TGI repository entered maintenance mode: it accepts bug fixes only, with no new features in development. Teams previously running TGI are largely migrating to vLLM or SGLang for new production deployments.

## How CoreWeave uses vLLM
CoreWeave uses vLLM as a supported inference runtime within its broader inference portfolio, and as the main engine in its documented deployment path for serving open-source LLMs on CoreWeave Kubernetes Service (CKS).
The production stack CoreWeave builds around vLLM follows the serving stack pattern described above: Traefik handles ingress and routing, cert-manager manages TLS certificates, Prometheus and Grafana provide observability, and KEDA handles event-driven autoscaling. For large-scale deployments, vLLM is configured with tensor parallelism across multiple H100 or H200 GPUs, with parallelism settings matched to the model and traffic pattern.
CoreWeave also integrates vLLM with LMCache for remote KV-cache reuse, allowing KV cache state to persist beyond a single replica and be shared across instances, reducing redundant computation on workloads with shared context.
Internally, CoreWeave treats vLLM as a maintained production component with structured versioning, upgrade playbooks, and staged promotion environments; it is maintained as a production-grade serving engine, not a tutorial dependency.

## Frequently asked questions

### What does vLLM stand for?

vLLM stands for virtual large language model. The "virtual" refers to the way it manages GPU memory using virtual memory principles (as in PagedAttention), not because the model itself is virtual.

### Is vLLM free and open source?

Yes. vLLM is Apache 2.0 licensed and hosted at github.com/vllm-project. The full engine, OpenAI-compatible server, distributed serving primitives, and all optimization features are open source.

### What models does vLLM support?

Most major open-weight model families: Llama 3 and 4, Qwen 2.5 and 3, DeepSeek R1 and V3, Mistral, Gemma, Phi, Mixtral, Granite, and many others, including vision-language and audio models. The supported models list expands with each release.

### Can vLLM run on multiple GPUs?

Yes. vLLM supports tensor parallelism, pipeline parallelism, expert parallelism, and disaggregated prefill across multiple GPUs and nodes.

## Related products & solutions

### Agentic AI
Build and run agentic AI systems with scalable, high-performance infrastructure

### AI inference
Deploy AI inference with low latency and optimized performance at scale

### Slurm on Kubernetes
Run Slurm on Kubernetes for scalable, managed AI training clusters

## Read more

See all resources

Blog
Unlocking AI Inference at Scale: CoreWeave Joins Red Hat Open Source Project llm-d as Founding Member

We're proud to announce we've joined Red Hat's new llm-d OSS project as a founding contributor. Learn more about how it's transforming AI inference.

Blog
CoreWeave Partners with Run:ai to Power AI Inference and Training at Scale

CoreWeave and Run:ai have partnered to integrate Run:ai’s orchestration platform with CoreWeave’s high-performance AI infrastructure.

Blog
Engineering Confidence: 4 Ways to Validate and Strengthen Your AI Infrastructure Resilience

Learn four practical strategies to validate and strengthen AI infrastructure resilience, from observability and automation to stress testing at GPU scale.

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
