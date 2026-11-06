# CoreWeave Zero Trust AI Framework | CoreWeave Blog

Source: https://www.coreweave.com/blog/coreweave-zero-trust-ai-framework-your-model-your-data-your-trust

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Agentic AI is changing what customers need from cloud security. Agents retrieve context, call tools, use memory, generate traces, and trigger actions across other systems. Reinforcement learning can bring inference into the training loop, where rollout generation, reward logic, updated checkpoints, and new model behavior become part of the same operating path. Sensitive data no longer sits behind one application boundary. It moves through prompts, embeddings, weights, traces, outputs, evaluation records, and runtime systems.
Using a cloud provider often requires you to trust them with access and visibility to your data and workloads. The provider may administer encryption keys, maintain privileged access to servers, manage the execution environment, or offer its own AI models that may learn from customer interactions. Customers are asked implicitly to trust the provider’s policies and processes. 
CoreWeave is taking a different approach.  
 Today,we are announcing the CoreWeave Zero Trust AI Framework™, a customer-controlled security model built to give customers control over access to their models, data, infrastructure and runtime environments. The Zero Trust AI Framework is built around a simple idea. Customers running sensitive AI workloads should keep more control over the parts of the stack that determine access to their data, their models, and their runtime environment. 
This means customers can bring the security systems they already trust to CoreWeave instead of rebuilding around a provider-defined security model. The CoreWeave Zero Trust AI Framework brings together six layers of protection that includes leveraging Remote Key Encryption (RKE), Support Access Management (SAM), confidential computing, remote attestation, model data protection, and protected data movement. Together, they give customers greater sovereignty over their AI environments. 
The result is an AI cloud built around customer control, where security can help customers move faster with sensitive AI workloads instead of slowing them down.

As enterprises move increasingly sensitive and regulated data into AI workflows, zero trust must extend beyond identity and network security to the entire AI infrastructure stack. CoreWeave’s Zero Trust AI Framework addresses this requirement by giving customers control over encryption keys and administrative access while introducing verifiable infrastructure, confidential execution, protected data movement, and customer data controls that do not rely on using customer data to train or improve the cloud provider’s own AI models. This shifts trust from provider promises to technical controls, a critical step for enterprises deploying proprietary AI at scale.
 Dave McCarthy, Group Vice President, Cloud and Datacenters, Enterprise Infrastructure, IDC

## 1. Zero Key Access: Your keys remain yours 
Encryption is only as strong as the protection surrounding its keys. When a cloud provider can access or administer a customer’s keys, that provider remains part of the security boundary even if the underlying data is encrypted.
CoreWeave’s Zero Key Access approach changes that relationship.
With RKE, customers use keys from the key infrastructure they already operate, whether that is a software key manager, a hardware security module, or a KMS in another cloud, while running AI workloads on CoreWeave. RKE is designed so customers retain control of the keys used to protect their data at rest without transferring key authority to CoreWeave. Customers can continue managing keys through their preferred processes, policies, and key-management systems without transferring control to CoreWeave.
This creates an important separation between the infrastructure provider and the information running on that infrastructure. It also dramatically speeds up how customers deploy sensitive data on RKE-protected workloads on CoreWeave. Customers don't need to create new key management automation, deploy on a new cloud KMS, rebuild key management workflows, policy controls, governance processes, and internal approvals before they can run sensitive training and inference workloads. RKE takes care of all of that automatically with existing encryption infrastructure: on-prem and in the cloud. CoreWeave supplies the high-performance AI cloud, while the customer maintains authority over access to protected data.
For organizations operating in regulated industries or managing especially sensitive intellectual property, this separation can be fundamental. RKE supports security models in which access is governed by the customer’s existing identity infrastructure: their existing users, groups, and identity provider (IdP)can be federated to RKE-protected resources and CoreWeave IAM, so customers control who can access protected data as well as who holds the keys. If CoreWeave does not have the key or does not have the permissions to access it, CoreWeave cannot decrypt the data.
Zero Key Access turns encryption from a provider-managed promise into a customer-controlled safeguard.

## 2. Zero Node Access: You decide when support enters your environment 
Infrastructure occasionally requires service, troubleshooting, or operational support. In some provider environments, the provider retains administrative access for troubleshooting. CoreWeave’s Support Access Management (SAM) gives customers control over that decision. 
With SAM, customers determine when CoreWeave is permitted to access infrastructure for support. Access is explicitly authorized for a defined operational need rather than treated as always available. When the authorized support activity ends, access ends with it. 
Zero Node Access makes support access an explicit customer decision, not an assumed privilege of the provider. 

## 3. Zero Trust Infrastructure: Attestation verifies the system beneath the workload 
Protecting access to a workload is essential, but customers also need confidence in the infrastructure beneath it. Before sensitive code or data is released into an environment, customers should be able to verify that the underlying system is in an expected, trusted state. CoreWeave is advancing attestation services designed to provide that assurance.
With CoreWeave attestation services, the infrastructure executing a workload is transparently verified using hardware roots of trust. Attestation can also support automated trust decisions. A workload, key-management system, or orchestration layer can require valid evidence before releasing secrets, decrypting data, or allowing execution to proceed.

## 4. Zero In-Use Access: Protecting data with confidential computing 
Much of the world’s most sensitive enterprise data remains on premises, governed by stringent requirements such as GDPR, the EU AI Act, and national data-sovereignty mandates. Yet the most capable AI models have traditionally been accessed through cloud APIs, requiring organizations to move valuable data beyond the environments they directly control. Enterprises need AI to operate where their data resides or on infrastructure they can independently verify and trust. Confidential computing makes this possible. 
CoreWeave intends to support confidential computing on NVIDIA Blackwell and Vera Rubin platforms to help protect sensitive models, data, and code while they’re in use. Blackwell provides hardware-based isolation, cryptographic attestation, and inline NVIDIA NVLink™ encryption to preserve confidentiality and integrity for models and data during execution.
NVIDIA Rubin builds on this foundation with systems such as NVIDIA HGX Rubin NVL8, and NVIDIA Vera Rubin NVL72 extends NVIDIA’s third-generation confidential computing across the CPUs, GPUs, and NVLink fabric of an entire rack. Combined with CoreWeave’s attestation services, these capabilities will allow customers to cryptographically verify the infrastructure before releasing sensitive data or keys and then protect workloads throughout execution, supporting secure training and inference at rack scale without requiring customers to place implicit trust in the cloud operator.  
Sensitive workloads can run within hardware-protected environments designed to prevent unauthorized access to data and code while they are in use. CoreWeave plans to support confidential computing for select bare metal environments and is working toward confidential computing support across additional deployment models, including Kubernetes-based AI workloads. 
Confidential computing and attestation work together, but serve different purposes. Attestation verifies that the infrastructure is in an expected state before it is trusted. Confidential computing helps isolate and protect the workload during execution.
Together, they establish a stronger foundation for sensitive AI workloads. Customers can verify the platform, determine whether it satisfies their security policies, and then protect their data and code while the system processes them.

## 5. Zero Model Data: CoreWeave does not train on your data
A framework for zero trust requires a clear separation between operating AI infrastructure and developing models. The infrastructure provider should not have a competing interest in using customer prompts, training data, model weights, or outputs to build or improve its own models. This separation removes a potential conflict of interest and keeps the value created from customer data with the customer.
CoreWeave is not a cloud with a foundation model business that competes with customers. There is no need for us to use customer data to train models or enhance any AI software. CoreWeave’s purpose-built infrastructure and software enable customers to run, tune, and scale the models they choose without turning their data into an input for the provider’s own AI development. 
This means customers can deploy open-source models through CoreWeave Inference or improve their own models with Serverless Reinforcement Learning, Serverless Supervised Fine-Tuning, and Model Distillation. In each case, the customer’s model and data remain the customer’s assets.
CoreWeave succeeds by helping customers run their AI faster, more efficiently, and more reliably, not by learning from the information those customers bring to our cloud. We do not need access to customer prompts, training data, model weights, or outputs to create a competing AI system.
Your data improves your model, not the infrastructure provider’s.

## 6. Zero Trust Network Encryption: Protecting data across the CoreWeave backbone 
AI workloads rarely remain inside a single server or rack. Datasets may be staged near available compute, checkpoints may move between locations, and model artifacts may need to reach training or inference environments across a global footprint.
Every transfer introduces another surface that must be protected.
CoreWeave uses IEEE 802.1AE MACsec to protect communications across its backbone. MACsec encrypts data moving over network links, helping defend against interception, tampering, and unauthorized observation as information travels between CoreWeave data centers.
By embedding hardware encryption into the backbone, CoreWeave makes secure transport part of the network architecture rather than an additional burden placed on every application team. Combined with customer-controlled keys and workload-level security, MACsec adds another layer of protection around sensitive AI assets.

## CoreWeave stays out of your trust chain by design 
Each layer of the Zero Trust AI Framework addresses a point at which an infrastructure provider might otherwise enter the customer’s security boundary:
- Zero Key Access keeps encryption keys under customer control.
- Zero Node Access lets customers authorize when infrastructure support can enter.
- Zero Trust Infrastructure  uses hardware-rooted attestation to verify the execution environment.
- Zero In-Use Access protects data and code during active execution.
- Zero Model Data aligns CoreWeave’s business with customer ownership of models and data.
- Zero Trust Network Encryption  protects information moving across the CoreWeave backbone.
Together, these capabilities are designed to minimize CoreWeave’s role in the customer trust chain. Customers do not have to depend exclusively on policy statements or operational assurances. They can rely on architectural controls that limit access, verify infrastructure, separate responsibilities, and preserve ownership.
That’s the deeper promise of the Zero Trust AI Framework. It’s not simply that CoreWeave will handle customer data responsibly. It’s that we’re building an AI cloud where CoreWeave stays out of your trust chain by design in the first place.
Your Model. Your Data. Your Trust.
Ready to take control of your sensitive AI workloads? Start here:
- Explore the CoreWeave Trust Center
- Learn more about CoreWeave Remote Key Encryption
- Contact CoreWeave to discuss confidential AI workloads

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

### From Training to Serving: Reflection’s Beam on CoreWeave

min read

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

### Closing the Loop Between Inference and Post-Training

7
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

Mission Control,

Copy code

Copied!

CoreWeave Cloud,

Mission Control,
