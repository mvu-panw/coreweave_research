# Get started with CoreWeave

Source: https://docs.coreweave.com/get-started

# Get started with CoreWeave

> Find your setup path and the right documentation for your CoreWeave workload.

CoreWeave is a cloud platform purpose-built for AI and high-performance compute. CoreWeave Kubernetes Service (CKS) runs bare-metal clusters on our GPU and CPU fleet, enabling model training and inference at scale. SUNK is CoreWeave's solution for running Slurm on Kubernetes, providing Slurm-based job scheduling on top of CKS for distributed training workloads.

This page orients you to the key concepts, tools, and setup paths, with links to full instructions for each.

## Start here

Here's how to get started with CoreWeave. Each step jumps to the details further down this page.

1. **Set up your account and team.** Activate your account, invite users, and grant access with IAM Access Policies. See [Account setup](#account-setup).
2. **Set up your tools.** Install `kubectl` and Helm for CKS, or Git and SSH for SUNK. See [Environment setup](#environment-setup).
3. **Run a workload.** Deploy a model for inference on CKS, or run distributed training on SUNK. See [Run workloads](#run-workloads).
4. **Secure and connect.** Add VPCs, network policies, and private connectivity as you scale. See [Security and networking](#security-and-networking).
5. **Automate it.** Manage your infrastructure with the REST APIs, the Terraform provider, and CoreWeave Skills. See [Automate your solution](#automate-your-solution).

## Where common tasks live in the Console

Use this table as a quick lookup for the most common tasks. Each row links to the page with full instructions. The [Cloud Console](https://console.coreweave.com) navigation evolves over time, so follow the linked pages rather than memorize menu positions.

| Task | Where it lives | Reference |
| :- | :- | :- |
| Invite a teammate | Console: Organization, Users | [Invite users](#invite-users-and-manage-your-org) |
| Grant or restrict access | IAM Access Policies | [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md) |
| Create an API token and kubeconfig | Console: Tokens | [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) |
| Create your first cluster | Console: Compute | [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) |
| View resource quotas | Console: Organization, Quotas | [Quota self-service](https://docs.coreweave.com/products/cks/clusters/quotas.md) |
| Request more capacity | Account Executive or support | [About capacity plans](https://docs.coreweave.com/platform/capacity-plans.md) |
| View invoices and usage | Console: Billing | [Billing insights](https://docs.coreweave.com/billing/billing-insights.md) |
| Monitor workloads | CoreWeave Grafana | [CoreWeave Observe](https://docs.coreweave.com/observability.md) |
| Subscribe to platform incidents | `status.coreweave.com` | [Status page and incidents](https://docs.coreweave.com/support/status-and-incidents.md) |
| Open a support ticket | Console: Help | [Contact support](https://docs.coreweave.com/support/contact.md) |

## Account setup

Account activation and user invitation apply to all CoreWeave users. If your team uses SUNK, admins must also complete a separate [user provisioning step](#provision-users-for-sunk) before you can connect to Slurm login nodes over SSH.

### Activate your account

When CoreWeave approves your organization, the CoreWeave Sales team sends an invitation email. Click **Activate** to access the [Cloud Console](https://console.coreweave.com).

> [!NOTE]
>
> The first user invited becomes an administrator by default and can invite others.

For more details, see [Activate and sign in to your CoreWeave organization](https://docs.coreweave.com/security/authn-authz/activate-org.md).

### Invite users and manage your org

Admins invite users from the [Users](https://console.coreweave.com/organization/users) page. New users click the invitation link and sign in with the same email used for the invite.

To sync users and groups from your IdP (Okta, Microsoft Entra, and others) instead of inviting manually, use [Automated User Provisioning (AUP)](https://docs.coreweave.com/security/automated-user-provisioning.md) with SCIM. This keeps your organization in sync with your identity provider.

See the following guides for setup instructions:

* [Configure AUP with Okta](https://docs.coreweave.com/security/automated-user-provisioning/configure-okta.md)
* [Configure AUP with Microsoft Entra](https://docs.coreweave.com/security/automated-user-provisioning/configure-microsoft-entra.md)

### IAM and access policies

Identity and Access Management (IAM) Access Policies define which users and groups can perform actions on platform services, such as creating and managing CKS clusters, managing IAM users and groups, and viewing billing. Admins create policies in the Cloud Console and assign roles to principals.

The following services use their own separate authorization systems rather than IAM Access Policies:

* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md), which uses organization and bucket access policies.
* [CKS clusters](https://docs.coreweave.com/products/cks.md), which use Kubernetes RBAC.
* [SUNK clusters](https://docs.coreweave.com/products/sunk.md), which use [SUNK User Provisioning (SUP)](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) rather than IAM Access Policies directly.

See [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md) for the full reference.

### Provision users for SUNK

Users who need access to SUNK require additional provisioning beyond the standard Cloud Console invite:

* An admin must enable SCIM API and SUNK User Provisioning in the Cloud Console.
* Each user must add an SSH public key before they can connect to Slurm login nodes.

See [Provision users in SUNK](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) for the full setup, including IdP-based provisioning with AUP and `nsscache` configuration.

## Environment setup

The tools you need depend on your path:

* CKS users need `kubectl` and Helm.
* SUNK end users need Git and SSH.
* AI Object Storage is optional and works with both CKS and SUNK workloads.

### Kubernetes and kubectl (CKS)

`kubectl` is the command-line tool for interacting with CKS clusters. To use it, you first need a cluster (see [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md)). Once a cluster exists, install [kubectl](https://kubernetes.io/docs/tasks/tools/), then create an API access token and download the kubeconfig file from the [Tokens](https://console.coreweave.com/tokens) page in the Cloud Console.

See [Manage API access tokens and kubeconfig files](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) for setup instructions.

### Helm (CKS)

Helm is an admin and infrastructure tool that deploys CoreWeave-provided charts, including Traefik, cert-manager, and container registries. If you're an admin, [install Helm](https://helm.sh/docs/intro/install/) (3.8+). End users running workloads on CKS don't need Helm installed locally.

See [CoreWeave Charts](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction.md) for the available charts and how to add the repository to Helm.

### AI Object Storage

AI Object Storage has an [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) that you can use with any S3-compatible client, such as the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [s3cmd](https://s3tools.org/download), or [Boto3](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html#installation).

[LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) is an intelligent caching proxy installed on every Node that improves data transfer rates for training and inference workloads. When running workloads inside a CoreWeave cluster, use the LOTA endpoint (`http://cwlota.com`) instead of the primary endpoint (`https://cwobject.com`).

Before creating buckets and objects, admins must configure access policies and authentication:

* Create at least one organization access policy before any S3-compatible request can succeed. See [About policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md) for more information.
* Choose how workloads authenticate: static access keys for simplicity and quick testing, or [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for production workloads that shouldn't rely on long-lived credentials.

See [Get started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) for authentication, policies, and full setup instructions.

### Git and SSH (SUNK)

Use Git to clone training code and job scripts onto the login node or shared storage.

SUNK end users connect to Slurm login nodes over SSH. SSH is typically pre-installed on macOS and Linux. On Windows, use [OpenSSH](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse) or enable it in **Settings**.

See [Connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) for setup instructions.

### Documentation MCP server

The CoreWeave documentation site exposes a Model Context Protocol (MCP) server endpoint that lets AI coding assistants query the docs directly in your development environment. (This is a separate control from the **Ask AI** button at the top of the page.)

To connect your assistant, do the following:

1. Expand the **Copy MCP Server** menu at the top of any documentation page, to the right of the page title:

   ![Documentation MCP server menu](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/get-started/_media/docs-mcp-menu.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=571e09121103723fe20fca7cbca5e391)
2. Copy the MCP server URL to configure tools manually. Alternatively, you can install the MCP server on an IDE or install it locally. You can also copy or view the page content as Markdown, and launch the AI assistant chat window in your browser.

## Run workloads

Choose your path based on your use case.

### Inference

Deploy a model for inference on CKS. See [Deploy an open source LLM on CKS](https://docs.coreweave.com/products/cks/deploy-model.md) for a complete walkthrough covering cluster setup and Open WebUI.

### Training

Run multi-node, multi-GPU distributed training with Slurm on SUNK. See [Train on SUNK](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk.md) for a complete walkthrough covering cluster setup, job submission, and monitoring.

## Security and networking

Explore the following recommended functionality as you scale:

* **VPCs**: [Virtual Private Clouds](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md) isolate clusters and control traffic. Use custom VPCs for multi-cluster communication, peering, or on-premises connectivity.
* **Network policies**: [Deploy network policies](https://docs.coreweave.com/security/tutorials/deploying-network-policies.md) to enforce Layer 4 and Layer 7 traffic rules at the DPU level.
* **Direct Connect**: [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md) provides private, dedicated links to CoreWeave from Equinix or Megaport.
* **HPC interconnect**: [GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) enables low-latency, high-throughput multi-node training.

See [Security](https://docs.coreweave.com/security.md) and [Networking](https://docs.coreweave.com/products/networking.md) for the full picture.

## Automate your solution

CoreWeave exposes REST APIs, infrastructure-as-code options, and agent-driven workflows for managing resources programmatically.

### REST APIs

CoreWeave provides the following REST APIs:

* **CKS API**: Create, list, update, and delete clusters programmatically. See [CKS API Reference](https://docs.coreweave.com/products/cks/reference/cks-api.md).
* **VPC API**: Manage VPCs through REST. See [VPC API](https://docs.coreweave.com/products/networking/vpc/vpc-api.md).
* **Object Storage API**: Manage access keys, policies, and organization settings programmatically. See [AI Object Storage API Reference](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md).

### Infrastructure-as-code

The [CoreWeave Terraform Provider](https://docs.coreweave.com/platform/terraform.md) lets you manage your CoreWeave infrastructure as code, including CKS clusters, VPCs, Object Storage buckets, and Object Storage access policies. Declare your infrastructure in configuration files and apply changes consistently across environments.

See [Terraform reference architecture](https://docs.coreweave.com/platform/reference-architecture.md) for a complete example.

### Agent-driven workflows

[CoreWeave Skills](https://docs.coreweave.com/platform/coreweave-skills.md) are Agent Skills that let Claude Code and other compatible agents carry out CoreWeave workflows for you, such as creating a cluster and Node Pool or loading a model into a bucket. Install them from the official `coreweave/skills` repository.

## For more information

Explore these resources to plan and scale your CoreWeave deployment:

* **Instances**: [GPU and CPU specifications](https://docs.coreweave.com/platform/instances/about-instances.md) help you [choose the right instance](https://docs.coreweave.com/platform/instances/selecting-an-instance.md) for your workload.
* **Node lifecycle**: See [how CKS Nodes are validated and maintained](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md), from [Day 1](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day1.md) setup through [Day 2+](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md) operations.
* **Observability**: [CoreWeave Observe](https://docs.coreweave.com/observability.md) covers Grafana dashboards, logs, metrics, telemetry, and alerts.
* **Regions**: [Regions and availability zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) covers global infrastructure and how CoreWeave delivers reliability and connectivity.
* **Pricing**: [Instance pricing](https://www.coreweave.com/pricing) provides guidance on costs and how to optimize them for your workload.
