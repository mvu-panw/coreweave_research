# Identity and access management (IAM)

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/org_team_struct

# Identity and access management (IAM)

> Learn how IAM scopes (organizations, teams, and projects) map to your company.

Identity and access management has three scopes: [Organizations](#organization), [Teams](#team), and [Projects](#project). Understanding how these scopes nest helps you plan how to structure access, group users, and organize AI work across your company.

The following sections describe each scope and how it maps to your company's structure, and link to detailed management guides.

> [!NOTE]
>
> In multi-tenant Forge, identity, roles, and access scopes are separate from CoreWeave IAM. See [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md) to determine where to manage each type of access.

## Organization

An *Organization* is the root scope in your account or instance. All actions in your account or instance take place within the context of that root scope, including managing users, managing teams, managing projects within teams, and tracking usage.

If you use [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), you may have more than one organization where each may correspond to a business unit, a personal user, or a joint partnership with another business.

If you use [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or a [Self-Managed instance](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md), it corresponds to one organization. Your company may have more than one Dedicated Cloud or Self-Managed instance to map to different business units or departments, though that's strictly an optional way to manage AI practitioners across your businesses or departments.

For more information, see [Manage organizations](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md).

## Team

A *Team* is a subscope within an organization that may map to a business unit, function, department, or project team in your company. You may have more than one team in your organization depending on your deployment type and pricing plan.

AI projects are organized within the context of a team. Team admins govern access control within a team, and they may or may not be admins at the parent organization level.

For more information, see [Add and manage teams](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-teams).

## Project

A *Project* is a subscope within a team that maps to an AI project with specific intended outcomes. You may have more than one project within a team. Each project has a visibility mode that determines who can access it.

Within each project, your team's work is organized into the following building blocks. Every project comprises [Workspaces](https://docs.coreweave.com/products/wandb/track/workspaces.md) and [Reports](https://docs.coreweave.com/products/wandb/reports.md), and links to relevant [Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md), [Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md), and [Automations](https://docs.coreweave.com/products/wandb/automations.md).
