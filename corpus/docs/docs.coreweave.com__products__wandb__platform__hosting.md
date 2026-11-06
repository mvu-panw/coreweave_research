# Deployment options overview

Source: https://docs.coreweave.com/products/wandb/platform/hosting

# Deployment options overview

> Compare Weights & Biases deployment options: Forge, Dedicated Cloud, and Self-Managed installations.

You can deploy Weights & Biases in various ways to meet your organization's infrastructure and security requirements. This page helps administrators and platform decision-makers compare the available deployment options, so you can choose the one that best fits your security, scale, and operational needs.

> [!TIP]
>
> To get started quickly, Weights & Biases recommends [Forge](https://forge.coreweave.com/wandb).
>
> Some features and functionality require an [Enterprise](https://coreweave.com/forge-pricing) license. To try these features, sign up for an [Enterprise trial](https://wandb.ai/site/enterprise-trial/) and choose your deployment type.

> [card] Forge
>
> A fully managed service deployed in Weights & Biases's cloud infrastructure, where you can access the Weights & Biases products at the desired scale, with cost-efficient pricing options, and with continuous updates for the latest features and functionality. Weights & Biases recommends Forge for your product trial, or to manage your production AI workflows if you don't need the security of a private deployment, self-service onboarding is important, and cost efficiency is critical.
>
> For more information, see [Forge](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md).

> [card] W\&B Dedicated Cloud
>
> A fully managed service with dedicated, isolated infrastructure in Weights & Biases's cloud. Choose this option if your organization requires conformance to strict governance controls including data residency, needs advanced security capabilities, and wants to optimize AI operating costs by not having to build and manage the required infrastructure with security, scale, and performance characteristics.
>
> For more information, see [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md).

> [card] W\&B Self-Managed
>
> Deploy and manage W\&B Server on your own managed infrastructure. W\&B Server is a self-contained packaged mechanism to run the W\&B Platform and its supported Weights & Biases products. Weights & Biases recommends this option if all your existing infrastructure is on-premises, or your organization has strict regulatory needs that W\&B Dedicated Cloud doesn't satisfy. With this option, you're fully responsible for managing the provisioning, and continuous maintenance and upgrades of the infrastructure required to support W\&B Server.
>
> For more information, see [W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md).

## Key differences

After reviewing the preceding deployment options, use the following table to compare how each option handles infrastructure, security, and operational responsibilities.

| | Forge | Dedicated Cloud | Self-Managed |
| - | - | - | - |
| MySQL / DB management | Fully hosted and managed by Weights & Biases | Fully hosted and managed by Weights & Biases on cloud or region of customer choice | Fully hosted and managed by customer |
| Object storage (S3/GCS/Blob storage) | **Option 1**: Fully hosted by Weights & Biases **Option 2**: Customer can configure their own bucket per team, using the [Secure Storage Connector](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) | **Option 1**: Fully hosted by Weights & Biases **Option 2**: Customer can configure their own bucket per instance or team, using the [Secure Storage Connector](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) | Fully hosted and managed by customer |
| SSO support | Weights & Biases managed via Auth0 | **Option 1**: Customer managed **Option 2**: Managed by Weights & Biases via Auth0 | Fully managed by customer |
| W\&B Service (App) | Fully managed by Weights & Biases | Fully managed by Weights & Biases | Fully managed by customer |
| App security | Fully managed by Weights & Biases | Shared responsibility of Weights & Biases and customer | Fully managed by customer |
| Maintenance (upgrades, backups, etc.) | Managed by Weights & Biases | Managed by Weights & Biases | Managed by customer |
| Support | Support SLA | Support SLA | Support SLA |
| Supported cloud infrastructure | Google Cloud | AWS, Google Cloud, Azure | AWS, Google Cloud, Azure, on-premises bare-metal |
