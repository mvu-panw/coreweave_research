# Red Hat AI Inference on CKS | CoreWeave Blog

Source: https://www.coreweave.com/blog/red-hat-ai-inference-on-cks-for-hybrid-inference

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Running inference workloads in a hybrid environment—on-premises and in the cloud—remains a challenge for many enterprise teams. Security requirements, data residency policies, and regulatory constraints mean running inference across on-premises and cloud environments simultaneously—not because it’s convenient, but because it’s required. With inference workloads in both places, the operational burden compounds: maintaining separate stacks, tooling, and expertise for each environment, all while keeping pace with rapidly evolving models and optimization techniques. 
Today, we're announcing a new approach that meets this pressing need—a deployment blueprint for running Red Hat AI Inference on CoreWeave Kubernetes Service (CKS). Developed by CoreWeave and Red Hat, this tested, documented reference architecture gives enterprise teams a supported path to production inference in hybrid environments. With it, teams can run the same open-source inference stack on-premises and on CoreWeave—without sacrificing Kubernetes-native control, open runtimes, or infrastructure transparency.
The new  blueprint  is a supported deployment path for customers who choose to self-manage inference on CKS using Red Hat's open-source stack. It complements CoreWeave's existing inference portfolio by giving customers the option to run the same solution they already use on other clouds and on-premises. 
This collaboration builds on our role as a founding contributor to the llm-d open-source project along with Red Hat, IBM Research, Google Cloud, and NVIDIA. It deepens a shared commitment to making high-performance inference infrastructure accessible, open, and Kubernetes-native.

### Why hybrid inference matters now
Enterprise inference is no longer a deployment event. It’s a continuously operated production service where latency, availability, and cost behavior must remain predictable under live demand.
The operational requirement is clear: run the same inference stack both on-prem and in the cloud. When the stack is consistent across environments, operational knowledge transfers cleanly, deployment patterns are reusable, and troubleshooting doesn't require context-switching between platforms. That consistency is also harder to achieve than it sounds. A typical production deployment involves model serving gateways, distributed serving frameworks, inference servers, model optimizations, and support for multiple accelerators—each layer individually configured, tested, and maintained. Teams building this from scratch face a significant operational burden that only grows as models evolve and new optimization techniques emerge.

### What Red Hat AI Inference brings to the table
Red Hat AI Inference is an open-source, end-to-end inference solution built for production inference. It includes model serving gateways with standard OpenAI-compatible interfaces, distributed LLM serving through llm-d with efficient inference scheduling and routing, KV cache management, and prefill/decode disaggregation. It supports inference servers such as vLLM for single-node and multi-node serving, model optimizations including quantization and speculative decoding, and works across accelerators.
The llm-d project at the heart of this innovative stack has since been donated to the CNCF as a Sandbox project, reflecting the industry's commitment to making distributed inference a first-class Kubernetes workload. CoreWeave contributed Tensorizer to vLLM, enabling faster model loading when scaling from zero.

### Why CKS is the right foundation for this blueprint
CKS is purpose-built for AI. It exposes deep observability at every layer of the stack, from bare-metal GPU allocation to inference-level diagnostics, and provides automated node lifecycle management — including health checks, remediation, and node draining — for high cluster reliability under production demand. For teams running large models that require multi-node inference, high-throughput interconnects, and low-latency scheduling, CKS provides first-to-market access to NVIDIA’s most powerful GPU generations and InfiniBand networking. This  infrastructure allows Red Hat AI Inference and llm-d to deliver maximum performance. 
CKS also preserves the Kubernetes-native operational model teams already use on-premises. Teams bring their existing Kubernetes expertise and workflows, and they work the same way on CoreWeave as they do in their own data centers. With CKS, there’s no  new abstraction,  proprietary orchestration layer, or  separate set of operational tooling.
Red Hat brings deep enterprise expertise in hybrid deployments, broad adoption across regulated industries, and recognized leadership in open-source Kubernetes and Linux platforms. Together, CoreWeave and Red Hat are making it easier for enterprise teams to deploy production inference with confidence—whether that workload lives on-premises, on CoreWeave, or across both.

### Looking ahead
Production inference is evolving quickly, and open, Kubernetes-native approaches should evolve with it. As the llm-d project and Red Hat AI Inference continue to mature, we expect this reference architecture to grow with them—supporting the latest models, accelerators, and deployment patterns that bridge on-premises and cloud environments. To get started, review the deployment blueprint documentation or read the Red Hat perspective on this partnership. For a deeper dive on the inference stack, explore the llm-d project on GitHub.

#### Hear more from CoreWeave and Red Hat—live on YouTube, May 27 at 1:15 PM ET
 
Find out what RedHat AI Inference's distributed inference capabilities bring to platform teams. And what these new capabilities mean for organizations building a Model-as-a-Service infrastructure and scaling agentic AI workloads in production.

 Join the conversation

Explore Red Hat AI Inference on CoreWeave CKS
- ‍Review the CoreWeave documentation
- ‍Learn more about Inference on CKS
Explore Red Hat AI Inference 
- Read the Red Hat announcement

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
