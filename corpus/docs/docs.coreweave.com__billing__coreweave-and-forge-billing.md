# CoreWeave Infrastructure and Forge billing

Source: https://docs.coreweave.com/billing/coreweave-and-forge-billing

# CoreWeave Infrastructure and Forge billing

> How Infrastructure and Forge billing relate and where you manage each one

Use this page to understand the CoreWeave Infrastructure and CoreWeave Forge billing systems, what each covers, and where each billing task belongs. This page is for administrators who manage spend on either platform or both.

The two systems stay separate. Each has its own billing page, permissions, usage views, and invoices, so a Forge invoice doesn't include CoreWeave Infrastructure usage.

To understand which access system governs a given resource, see [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md).

## Where to manage billing

Use the following table to find where each billing task belongs:

| Task | Where |
| - | - |
| Review CoreWeave Infrastructure usage and costs | [Billing](https://docs.coreweave.com/billing.md) and [Billing insights](https://docs.coreweave.com/billing/billing-insights.md) |
| Export CoreWeave Infrastructure usage programmatically | [FOCUS usage export API](https://docs.coreweave.com/billing/focus-export-api.md) |
| Grant permission to view CoreWeave billing | [CoreWeave IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md) ([Billing Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#billing) role) |
| Review Forge plan, usage, and spending alerts | [Forge billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md) |
| Manage Forge payment methods, billing admin, and invoices | [Forge billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md) |
| Ask about CoreWeave Infrastructure billing | `support@coreweave.com` |
| Ask about Forge billing | `forge-support@coreweave.com` |

## What each billing system covers

The following list describes what each billing system covers:

* **CoreWeave Infrastructure** bills for Cloud Console resources: CKS compute, capacity plans, Object Storage, and network usage. Review those charges in the [Cloud Console](https://docs.coreweave.com/billing.md).
* **CoreWeave Forge** bills for the Forge organization plan and the Forge usage categories shown in billing settings. Those categories can include storage, Weights & Biases tracked hours, Weave, Serverless Inference, Training, ARIA, and Sandboxes when the usage is billed to the Forge organization.

Some products can bill through either system, depending on how you run them. The following sections cover those cases.

### Sandboxes

Serverless sandboxes accept two credentials. Which account the sandbox belongs to and bills to depends on the credential you present:

| Credential | Billed through |
| - | - |
| CoreWeave API access token | CoreWeave Infrastructure |
| Forge API key | Forge |

For details, see [Choose a credential](https://docs.coreweave.com/products/sandboxes/get-started.md#choose-a-credential).

### Inference

Inference billing depends on the deployment option:

| Deployment option | Billed through |
| - | - |
| Serverless Inference | Forge (pay-per-token) |
| Dedicated Inference | CoreWeave Infrastructure (GPU-hour or node-based, depending on your contract) |
| Inference on CKS | CoreWeave Infrastructure (standard CKS billing) |

For details, see [Inference pricing](https://docs.coreweave.com/products/inference.md#pricing) and [Dedicated Inference billing](https://docs.coreweave.com/products/inference/billing.md).

## Manage billing across both platforms

If your organization uses both platforms, review billing separately in each one. CoreWeave Infrastructure and Forge don't share invoices, payment methods, usage alerts, or billing permissions.

* **Permissions.** CoreWeave uses the [Billing Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#billing) IAM role and related legacy groups. Forge uses [organization admin](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-users) and [billing admin](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md#billing-admin) roles inside Forge. Holding one role doesn't grant the other.
* **Usage and alerts.** CoreWeave billing insights cover infrastructure usage. Forge usage and spending alerts cover Forge plan categories. Configure and review each set of alerts in its own system.
* **Payment methods.** Add and update payment methods in each platform's billing page. A payment method on file for Forge doesn't apply to CoreWeave Infrastructure, and vice versa.
* **Invoices.** A Forge invoice doesn't include CoreWeave Infrastructure usage, and a CoreWeave Infrastructure invoice doesn't include Forge plan charges. Reconcile spend by checking both billing pages when you use both platforms.

> [!NOTE]
>
> Invoice separation, payment methods, usage alerts, and billing permissions are subject to change.

### Multi-tenant Forge deployments

The guidance on this page applies to multi-tenant Forge. W\&B Dedicated Cloud and W\&B Self-Managed deployments keep their existing billing configuration. See [Deployment options](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options.md).

## Related resources

The following pages cover related billing and access topics:

* [Billing](https://docs.coreweave.com/billing.md): Manage CoreWeave Infrastructure usage and costs in the Cloud Console.
* [Forge billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md): Review the Forge plan, usage, alerts, payment methods, and invoices.
* [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md): Understand how the two identity systems relate and where each administrative task belongs.
* [Get started with CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes/get-started.md): Choose the credential that determines which account a serverless sandbox bills to.
* [What moved in CoreWeave Forge](https://docs.coreweave.com/forge-whats-moved.md): Find projects, settings, and account locations in Forge if you already use Weights & Biases.
