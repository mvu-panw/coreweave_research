# Introducing Automated User Provisioning and SUNK User Provisioning | CoreWeave Blog

Source: https://www.coreweave.com/blog/introducing-automated-user-provisioning-and-sunk-user-provisioning

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Managing user access to compute clusters is often slow, manual, and error-prone. Researchers wait for credentials. Administrators spend hours configuring users and fixing permissions instead of focusing on performance or security. In large AI environments, this friction delays research, wastes valuable GPU time, and turns lost hours into real cost. When training runs span thousands of GPUs and experiments run continuously, even small delays in access slow discovery.
With Automated User Provisioning (AUP) and SUNK User Provisioning (SUP), you can now automate that entire process. Identities sync directly from enterprise providers into CoreWeave IAM and Slurm on Kubernetes (SUNK) clusters, giving teams secure, ready-to-use access in minutes. It takes teams from Day 1 to Day Now, cutting setup time from days to instant access so researchers can get back to running jobs and moving work forward. This innovation is just part of CoreWeave’s end-to-end AI-first experience, where infrastructure, orchestration, and identity are designed together to serve large-scale training and inference. No other cloud combines this level of access control with Slurm-to-Kubernetes integration and bare-metal performance for AI workloads.

### AUP: Federation built for CoreWeave Cloud
On its own, AUP enables secure, scalable identity management across CoreWeave Cloud, including CoreWeave Kubernetes Service (CKS), CoreWeave AI Object Storage, and the CoreWeave Console. By connecting your organization’s identity provider (IdP) to CoreWeave Identity and Access Management (IAM) through System for Cross-domain Identity Management (SCIM), the modern standard for secure identity synchronization, AUP keeps users and groups continuously aligned across every CoreWeave service.
Identity federation has been a longstanding pain point for enterprise IT teams. Integrations built on legacy LDAP are brittle, slow, and difficult to maintain, especially at AI scale. Directory mismatches, manual field mapping, and delayed user deactivation create both operational drag and security risk.
AUP replaces that complexity with a direct, standards-based connection. Using SCIM, it continuously syncs users and groups between identity providers such as Okta or Microsoft Entra and CoreWeave IAM. Any changes made upstream from new users, role updates, or deletions propagate automatically, removing manual steps and preventing stale credentials. The result? Unified identity management that scales from a single project to multi-cluster deployments without additional tooling.

### SUP: Provisioning for Slurm
For cluster administrators, provisioning users for Slurm environments has traditionally been time-consuming and inconsistent. Researchers lose valuable time waiting for cluster access, while admins manually create POSIX users, update configurations, and chase permission errors. Every manual step slows research and adds risk when credentials linger or are stored in plain text.
SUP extends CoreWeave IAM automation into Slurm-on-Kubernetes clusters, automatically creating POSIX users and groups, SSH keys, and Slurm users and accounts as soon as a user is added to CoreWeave IAM or to an upstream identity provider. Access and permissions are correct on first login, no YAML, no tickets, no delays.
“Using SUNK User Provisioning has made adding new users to our Slurm cluster trivial and given us the ability to easily set up the right set of permissions for our different use cases. If only all my activities were this straightforward.” 
Tim McNerney, Member of Technical Staff, Inflection AI

## Under the hood of SUP
SUP uses a per-customer SCIM endpoint and NSSCache to distribute user and group data across nodes. Unlike SSSD, which depends on a running daemon and constant network connectivity, NSSCache generates local caches that make authentication faster and more resilient for large-scale or transient HPC environments.
This approach is purpose-built for AI workloads that span both training jobs and real-time inference. CoreWeave is the only platinum-certified platform for ClusterMax, underscoring the reliability of this foundation. This certification validates CoreWeave’s ability to support both dedicated and semi-clustered HPC configurations at scale. Together, AUP and SUP deliver the first fully automated, end-to-end user provisioning system for Slurm clusters, an AI-native capability that no other cloud provides.
“Onboarding to Slurm on CoreWeave has been smooth and reliable. New user registration just works, unlike with other providers, where we often ran into setup issues. CoreWeave offers the best infrastructure support we’ve had so far.”‍
Zhaoyang Lv, Member of Technical Staff, Impossible Inc.
This release raises the bar for what users can expect from the #1 AI Cloud, purpose-built for the next generation of intelligent workloads. By reducing operational friction and securing identity at scale, AUP and SUP help teams focus on what matters most: advancing research and training models faster. 

### AUP and SUP in practice
AUP connects your identity provider to CoreWeave IAM. SUP then provisions that IAM data into SUNK. Getting started is straightforward. Enable SCIM, create a token in CoreWeave IAM, and set up SCIM in your identity provider following its instructions. We recommend AUP for federating identities not only for SUNK but also for other CoreWeave services like Object Storage and CKS.
Once AUP is in place, set up SUP for managing users in your Slurm clusters. It doesn’t matter whether users and groups in IAM came from an identity provider or were created manually. Create a SCIM token for SUP for each Slurm cluster and configure NSSCache in each one as described in our documentation. For small teams without an IdP, create SUNK-specific groups such as slurm-users and slurm-sudo in IAM and point NSSCache to the SCIM endpoint to fetch that data. Researchers can paste their own SSH keys in the user settings page and view their POSIX UID and GID.
What it looks like in practice
Watch the demo below showing identity updates propagating to clusters in real time: a new researcher joins your organization, the admin creates the user in the identity provider and adds them to the slurm-users group, AUP syncs that record to CoreWeave IAM via SCIM, and SUP, through NSSCache, picks it up on the next poll, within about a minute. SUP then provisions the POSIX user and group memberships with the correct UID and GID, SSH key, and a Slurm user and account. The researcher can log in immediately. No YAML, no sacctmgr, no tickets. Access and permissions are correct on first login.

‍‍
“CoreWeave made the transition from our old user management system to SUNK User Provisioning absolutely seamless. It’s now effortless to add new users to our Slurm cluster, without juggling SSH keys over email or Slack and without touching tons of system files. New team members get secure, instant access and are up and running on the infrastructure in minutes. That’s exactly the kind of smooth experience we’ve come to expect from CoreWeave.”
‍Jean-Philippe Robichaud, Principal Speech Scientist AI Research, REV.COM
If you are migrating from Authentik to SUP, federated or not, there are only a few extra steps. Our team will guide you through them. The migration takes minutes and does not impact running jobs.

### From identity to innovation
By automating identity and access from CoreWeave IAM through Slurm-on-Kubernetes, AUP and SUP remove one of the last manual barriers in AI research. Teams can onboard new researchers securely in minutes, reclaim GPU hours once lost to setup, and focus entirely on experimentation and discovery. These efficiency gains are what from Day 1 to Day Now means for identity in the AI era, and they’re only possible on the Essential Cloud for AI.
Getting started with AUP and SUP
To learn more, visit the SUNK overview page, explore the AUP setup guide for federated identity providers, or start with the SUP quick-start guide. You can also review our migration notes and a short demo video showing how identity updates propagate to clusters in real time.
With AUP and SUP, CoreWeave makes identity management for compute clusters automatic, secure, and immediate so your teams can spend less time on access and more time on discovery.
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

SUNK,

Copy code

Copied!

SUNK,
