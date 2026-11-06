# Forge

Source: https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud

# Forge

> Learn about Forge, a fully managed deployment on Google Cloud with built-in compliance and data security.

This page describes Forge, including its architecture, compliance posture, data security options, and identity and access management capabilities, so you can decide whether it fits your organization's hosting requirements.

CoreWeave Forge is a fully managed platform deployed in CoreWeave's Google Cloud account in [Google Cloud's North America regions](https://cloud.google.com/compute/docs/regions-zones). Forge uses autoscaling in Google Cloud to scale the platform based on changes in traffic.

![Forge architecture diagram](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/multi_tenant_cloud_arch.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=915f746c8f7ea65cc6f4c6292063109c)

Forge scales to meet your organization's needs and supports logging up to 250,000 metrics per project with up to 1 million data points per metric. For larger deployments, contact [support](mailto:forge-support@coreweave.com).

## Compliance

Forge's hosting platform meets the requirements of the [Service and Organization Controls (SOC) 2 Type 2](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2), published by the [Auditing Standards Board of the American Institute of Certified Public Accountants (AICPA)](https://www.aicpa-cima.com/home). A SOC 2 report evaluates a service organization's controls for security, availability, processing integrity, confidentiality, and privacy. Forge is subject to periodic internal and external audits to verify continued compliance. Refer to the [Weights & Biases Security Portal](https://security.wandb.ai/) to request the SOC 2 report and other security and compliance documents.

> [!TIP]
>
> Forge doesn't meet the requirements of the [Health Insurance Portability and Accountability Act of 1996 (HIPAA)](https://www.hhs.gov/hipaa/for-professionals/index.html). If your organization is subject to HIPAA, consider [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) instead.

## Data security

For users on Free or Pro plans, Weights & Biases stores all data only in the shared cloud storage and processes it with shared cloud compute services. Depending on your pricing plan, you may be subject to storage limits.

Users on an Enterprise plan can [bring their own bucket (BYOB) using the secure storage connector](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) at the [team level](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md#configuration-options) to store their files such as models, datasets, and more. You can configure a single bucket for multiple teams or you can use separate buckets for different teams. If you don't configure BYOB for a team, Weights & Biases stores the team's data in the shared cloud storage.

You are responsible for ensuring that your deployment complies with your organization's policies and [Security Technical Implementation Guidelines (STIG)](https://en.wikipedia.org/wiki/Security_Technical_Implementation_Guide), if applicable.

## Data retention policy

Forge retains the following items for 7 days after deletion:

* Runs and history.
* Non-artifact run files, such as media, configuration files, and log files.
* Artifacts and artifact references.

Until this period elapses, Weights & Biases can restore these items. Contact [support](mailto:forge-support@coreweave.com) or your AISE for assistance.

## Identity and access management (IAM)

If you're on an Enterprise plan, identity and access management features support secure authentication and authorization for your Weights & Biases deployment:

* Authenticate users with SSO using OIDC or SAML. Contact your account team or support if you'd like to configure SSO for your organization.
* [Configure user roles](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#assign-or-update-a-users-role) at the scope of the organization and within a team.
* Define the scope of a Weights & Biases project to limit who can view, edit, and submit W\&B runs to it with [restricted projects](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects.md).

## Billing and usage

Organization admins can manage usage and billing for their account from the **Billing** tab in their account view. If using the shared cloud storage on Forge, an admin can optimize storage usage across different teams in their organization.

## Maintenance

Forge is a multi-tenant, fully managed platform. CoreWeave manages the infrastructure, so you don't incur the overhead and costs of provisioning and maintaining it.

## Next steps

Access [Forge directly](https://forge.coreweave.com/wandb) to get started with most features for free. To try data security and IAM features, [request an Enterprise trial](https://wandb.ai/site/for-enterprise/multi-tenant-saas-trial).
