# Deployment options

Source: https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options

# Deployment options

> Choose a Weights & Biases deployment type: Forge, Dedicated Cloud, or Self-Managed.

Choose the hosting option that fits your organization's security, compliance, and operational needs. CoreWeave manages the infrastructure for Forge and Dedicated Cloud; with Self-Managed, you manage it.

## Forge

[Forge](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) is fully managed by CoreWeave, including upgrades, maintenance, platform security, and capacity planning. Forge is deployed in CoreWeave's Google Cloud account in [Google Cloud's North America regions](https://cloud.google.com/compute/docs/regions-zones). [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) optionally lets you store W\&B Artifacts and other related sensitive data in your own cloud or on-premises infrastructure.

See [Forge](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) or [get started for free](https://id.coreweave.com/signup).

## W\&B Dedicated Cloud

[W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) is a fully managed platform with dedicated, isolated infrastructure, designed with enterprise organizations in mind. W\&B Dedicated Cloud is deployed in Weights & Biases's AWS, Google Cloud, or Azure account. Dedicated Cloud provides more flexibility than Forge, but less complexity than W\&B Self-Managed. Weights & Biases manages upgrades, maintenance, platform security, and capacity planning. Each Dedicated Cloud instance has its own isolated network, compute, and storage, separate from other W\&B Dedicated Cloud instances.

Your Weights & Biases-specific metadata and data is stored in an isolated cloud storage and is processed using isolated cloud compute services. [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) optionally lets you store artifacts and other related sensitive data in your own cloud or on-premises infrastructure.

W\&B Dedicated Cloud includes an [enterprise license](https://docs.coreweave.com/products/wandb/platform/hosting/enterprise-licenses.md) with support for security and other enterprise-friendly capabilities.

For organizations with advanced security or compliance requirements, features such as HIPAA compliance, single sign-on, or customer-managed encryption keys (CMEK) are available with Enterprise support. [Request more information](https://www.coreweave.com/contact-us).

See [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [get started for free](https://id.coreweave.com/signup).

## W\&B Self-Managed

[W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) is entirely managed by you, either on your premises or in cloud infrastructure that you manage. Your IT/DevOps/MLOps team is responsible for:

* Provisioning your deployment.
* Securing your infrastructure in accordance with your organization's policies and [Security Technical Implementation Guidelines (STIG)](https://en.wikipedia.org/wiki/Security_Technical_Implementation_Guide), if applicable.
* Managing upgrades and applying patches.
* Continuously maintaining your Self-Managed W\&B Server instance.

You can optionally obtain an [enterprise license](https://docs.coreweave.com/products/wandb/platform/hosting/enterprise-licenses.md) for W\&B Self-Managed. An enterprise license includes support for security and other enterprise-friendly capabilities.

See [W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) or review the [reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md) guidelines.
