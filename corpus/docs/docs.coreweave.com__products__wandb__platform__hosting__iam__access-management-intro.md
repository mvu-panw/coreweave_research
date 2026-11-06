# Access management

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management-intro

# Access management

> Manage users, teams, roles, and project visibility as an organization or team admin in Weights & Biases.

This page introduces how access management works in Weights & Biases, including how to administer users and teams, maintain admin access to your organization, and control who can view individual projects. It's intended for organization admins, team admins, and project owners.

> [!NOTE]
>
> In multi-tenant Forge, access management is separate from CoreWeave IAM. Forge roles don't grant access to CoreWeave Infrastructure, and CoreWeave IAM roles don't grant Forge access. See [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md).

## Manage users and teams within an organization

This section explains how admin roles are assigned and what each role can do to manage users and teams.

Weights & Biases assigns the *instance admin role* to the first user who signs up to Weights & Biases with a unique organization domain. The organization admin assigns specific users team admin roles.

> [!NOTE]
>
> Weights & Biases recommends that you have more than one instance admin in an organization. This best practice ensures that admin operations can continue when the primary admin isn't available.

A *team admin* is a user in an organization who has administrative permissions within a team.

Organization admins can access and use an organization's account settings at `https://forge.coreweave.com/account-settings/` to invite users, assign or update a user's role, create teams, remove users from your organization, and assign the billing admin. See [Add and manage users](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-users) for more information.

After an organization admin creates a team, the instance admin or a team admin can:

* Invite users to the team or remove users from the team. By default, only an admin can perform this action. To change this behavior, see [Team settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md#privacy).
* Assign or update a team member's role.
* Automatically add new users to a team when they join your organization.

Both the organization admin and the team admin use team dashboards at `https://wandb.ai/[YOUR-TEAM-NAME]` to manage teams. For more information, and to configure a team's default privacy settings, see [Add and manage teams](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-teams).

## Maintain admin access

This section describes why you must always preserve admin access and how automated user deprovisioning can put that access at risk.

You must ensure that at least one admin user always exists in your instance or organization. Otherwise, no user can configure or maintain your organization's Weights & Biases account.

If you manage users interactively, deleting a user requires admin access, including when deleting another admin user. This helps reduce the risk of removing the sole admin user.

However, if an organization uses automated processes to deprovision users from Weights & Biases, a deprovisioning operation could inadvertently remove the last remaining admin from the instance or organization.

For assistance with developing operational procedures, or to restore admin access, contact [support](mailto:forge-support@coreweave.com).

## Limit visibility to specific projects

Define the scope of a Weights & Biases project to limit who can view, edit, and submit W\&B runs to it. Limiting who can view a project is particularly useful if a team works with sensitive or confidential data.

A team admin or the owner of a project can set and edit a project's visibility.

For more information, see [Project visibility](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects.md).
