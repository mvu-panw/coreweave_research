# Enterprise AI Security on CoreWeave: IAM and Key Control

Source: https://www.coreweave.com/blog/bringing-enterprise-identity-and-key-control-to-ai-on-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

If you run either the security or platform team at a large enterprise, then you've probably lived some version of this: the AI team has a model ready, the business wants it in production, and the whole thing is parked in security review because nobody can answer two questions cleanly. Who can touch it? And who holds the keys?
Those questions are hard for a reason. Enterprise AI is only useful when it can leverage business-critical, often sensitive data, and the frameworks that govern that data (PCI DSS, GDPR, ISO 27001) without creating another disconnected set of controls. You're being asked to run new workloads inside rules that were never built to handle them.
Then there's the practical side. Most enterprises are multi-cloud, with identity and security automation built up over a decade or more across providers that don't agree with each other on much. Every new cloud platform you add is another place that automation has to reach. If it doesn't, someone ends up hand-provisioning accounts and copying keys around, and least privilege quietly erodes.
We've worked through this with some of the largest enterprises in the world. What we've found is that the fastest path through the loop to production isn't a new security model. It's making sure our security layer speaks fluently with the ones that already exist. Cross-cloud is a cornerstone of the CoreWeave strategy with previous capabilities like cross-cloud Local Object Transport Accelerator (LOTA), SUNK Anywhere, and our announced Interconnect with GCP. With Security and Identity, it is even more critical that secrets aren’t replicated and identities aren’t duplicated. Today, both with identity and encryption, we’re putting federation first.

## CoreWeave IAM: bring your own identity provider
You already have an identity provider (IdP), and you've probably spent years wiring automation around it. Asking you to adopt another one, or to write a parallel set of provisioning scripts for one more cloud, tends to slow you down and widen the gap where mistakes happen.
So CoreWeave IAM doesn't ask. It sits at the center of CoreWeave Cloud, handling authentication and authorization for everything you deploy, and it federates with your existing IdP over SAML and OIDC. Microsoft Entra, Okta, an IdP that lives in another hyperscaler: whatever you bring stays the source of truth.
Automated User Provisioning (AUP) is where that gets tangible. Users and groups sync continuously from your IdP into CoreWeave IAM. A new hire shows up with the right access. A role change updates their permissions. A termination revokes them. That propagates across CoreWeave Kubernetes Service (CKS), CoreWeave AI Object Storage (CAIOS), and the Console without anyone filing a ticket or maintaining an LDAP bridge.
Authorization works the same way. CoreWeave IAM policies will look familiar if you've written them for another hyperscaler, so your existing access model translates rather than getting rebuilt. RBAC and ABAC patterns apply least privilege to identities as they arrive from your IdP, which means entitlements are enforced by policy instead of assigned by hand.

### What this looks like for a research team
Take SUNK, our Slurm-on-Kubernetes offering for training clusters. Slurm, an open-source job scheduler, has its own idea of identity (POSIX users, groups, accounts), and keeping that in sync with a corporate directory has traditionally been someone's part-time job.
With SUNK User Provisioning (SUP), it isn't. The moment a federated user lands in CoreWeave IAM, SUP creates their POSIX user and groups, syncs their SSH keys, and provisions their Slurm user and account. It runs off a per-customer SCIM endpoint and distributes identity through NSSCache rather than a live daemon, so logins stay fast even on clusters that scale up and churn constantly.
The practical result: add a researcher to a group in Entra or Okta, and they can SSH into a login node less than a minute later with the right UID, GID, and permissions already in place. No YAML, no account manager, no ticket. They get their access right away, and you get an access trail that starts and ends in the system you already audit.

## Remote Key Encryption: your keys stay yours
Identity answers who can touch the data. Encryption and key custody answer who can read it, and for regulated data, that second question is where most enterprise AI deployments stall.
Training data, checkpoints, and model weights are among the most sensitive assets you own. Every major compliance framework assumes you can name exactly who is able to decrypt them. In most clouds, part of that answer is the cloud provider, and reconciling that with your obligations is what keeps deployments sitting in review.
Remote Key Encryption (RKE) is our newest security product, and it's built to take the provider out of that sentence. RKE encrypts your data at rest on CoreWeave using keys that are generated, stored, and rotated entirely inside your existing key store, whether that's a secrets manager, a cloud key management system (KMS), or a hardware security module (HSM) in the cloud or on-prem. Encryption happens client-side, inside your trusted compute boundary, using automation you control.
The distinction that matters: RKE doesn't import your keys into a CoreWeave-side KMS. Your keys stay in your key manager and trust boundary. CoreWeave never sees plaintext and only ever holds ciphertext. Access to your dedicated, single-tenant nodes stays gated behind Support Access Management, so even our own support engineers can't reach them without your express permission.
And because RKE works with the key infrastructure you already run, the lifecycle workflows you already have (rotation, expiration, revocation) carry over without new tooling. Your encryption infrastructure stays the same, and RKE automatically manages key lifecycle management (key rotation, deletion) with your existing KMS and HSM infrastructure. 
RKE’s approach to key lifecycle management is unique. While RKE uses proven encryption algorithms and methods, it uses a patent pending method to enable you to use your existing remote key management systems as the system of record for protecting your AI data on CoreWeave. Like IAM and all of our security products, RKE uses this unique approach to support you in deploying sensitive AI workloads on CoreWeave with fewer obstacles than any other cloud platform. 

### What this looks like for an inference team
Say you're deploying inference and need to guarantee that nobody outside your organization, CoreWeave included, can access your model weights.
With RKE, you encrypt those weights on your node using your existing secrets manager or KMS before they're written to CoreWeave AI Object Storage. The keys never leave your custody. CoreWeave never stores or touches them. Rotation and expiration run on your schedule, inside your boundary. If an auditor asks who can decrypt the weights, the answer is a short list, and it doesn't have CoreWeave on it.

## Coming soon
RKE will be available later this year, protecting data on CoreWeave AI Object Storage with keys held in HashiCorp Vault Enterprise and general-purpose KMS and HSM products that speak the Key Management Interoperability Protocol (KMIP). Security work on AI projects often feels like a tax on speed, but it really doesn't have to. When identity and key custody plug into the systems you already trust, the review gets shorter, the automation gets simpler, and your teams get straight to business: building and shipping.
- Learn How to Evaluate Your Cloud for AI Workload Security from CoreWeave CISO Jim Higgins
- See how CoreWeave secures AI workloads, node to data center
- Learn more about CoreWeave Compliance and Governance‍

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

CoreWeave AI Object Storage,

Copy code

Copied!

CoreWeave AI Object Storage,
