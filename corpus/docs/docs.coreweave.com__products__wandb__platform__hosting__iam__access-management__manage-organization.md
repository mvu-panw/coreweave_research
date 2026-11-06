# Manage your organization

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization

# Manage your organization

> Manage users, teams, roles, seats, and billing within a Forge organization as an organization admin.

This page describes how to administer a Forge organization, including how to invite users, manage teams, assign roles and seats, and configure billing. Use these procedures to keep your organization's membership, access, and team structure aligned with how your company uses Forge.

As an admin of an organization, you can [manage individual users](#add-and-manage-users) within your organization and [manage teams](#add-and-manage-teams).

As a team admin, you can [manage teams](#add-and-manage-teams).

> [!NOTE]
>
> The following workflow applies to users with instance admin roles. Contact an admin in your organization if you believe you should have instance admin permissions.

To simplify user management in your organization, see [Automate user and team management](https://docs.coreweave.com/products/wandb/platform/hosting/iam/automate_iam.md).

## Change the name of your organization

> [!NOTE]
>
> The following workflow only applies to W\&B Multi-tenant Cloud.

1. In the upper right corner of the header, open your account menu.
2. Select **Settings**.
3. Within the **Settings** tab, select **General**.
4. Select the **Change name** button.
5. Within the modal that appears, provide a new name for your organization and select the **Save name** button.

## Add and manage users

As an admin, use your organization's dashboard to:

* Invite or remove users.
* Assign or update a user's organization role.
* Create custom roles that team admins can assign to team members.
* Assign the billing admin.

An organization admin can add users to an organization in several ways:

* Member-by-invite
* Auto provisioning with SSO
* Domain capture

The following sections describe each method.

### Seats and pricing

The following table summarizes how seats work for Models and Weave:

| Product | Seats | Cost based on |
| - | - | - |
| Models | Pay per seat | The number of Models paid seats you have and the usage you’ve accrued determine your overall subscription cost. Each user can be assigned one of three available seat types: Full, Viewer (Enterprise-only feature), or No access. |
| Weave | Free | Usage based |

### Invite a user

Admins can invite users to their organization, as well as to specific teams within the organization.

> [tab] Multi-tenant Cloud
>
> 1. In the upper right corner of the header, open your account menu.
> 2. Select **Users**.
> 3. Select **Invite new user**.
> 4. In the modal that appears, provide the email or username of the user in the **Email or username** field.
> 5. (Recommended) Add the user to a team from the **Choose teams** dropdown menu.
> 6. From the **Select role** dropdown, select the organization role to assign to the user. You can change the user's role at a later time. See the table in [Assign or update a user's role](#assign-or-update-a-users-role) for possible roles.
> 7. Click the **Send invite** button.
>
> After you select the **Send invite** button, Forge sends an invite link to the user's email using a third-party email server. A user can access your organization once they accept the invite.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. Navigate to `https://<org-name>.io/console/settings/`. Replace `<org-name>` with your organization name.
> 2. Select the **Add user** button.
> 3. Within the modal that appears, provide the email of the new user in the **Email** field.
> 4. Select a role to assign to the user from the **Role** dropdown. You can change the user's role at a later time. See the table in [Assign or update a user's role](#assign-or-update-a-users-role) for possible roles.
> 5. Check the **Send invite email to user** box if you want Forge to send an invite link using a third-party email server to the user's email.
> 6. Select the **Add new user** button.

### Auto provision users

Auto-provisioning streamlines onboarding by letting users join your organization automatically through SSO, so admins don't need to send individual invitations. This is Forge's equivalent of just-in-time (JIT) provisioning: an account is created the first time a user with a matching email domain signs in through SSO.

If you configure SSO and your SSO provider permits it, a Forge user with a matching email domain can log in to your Forge organization with Single Sign-On (SSO). SSO is available for all Enterprise licenses.

> [!NOTE]
>
> **Enable SSO for authentication**
>
> Forge recommends that users authenticate using Single Sign-On (SSO). Contact your Forge team to enable SSO for your organization.
>
> For more information about how to set up SSO with Dedicated Cloud or Self-Managed instances, see [SSO with OIDC](https://docs.coreweave.com/products/wandb/platform/hosting/iam/sso.md) or [SSO with LDAP](https://docs.coreweave.com/products/wandb/platform/hosting/iam/ldap.md).

Forge assigns auto-provisioning users "Member" roles by default. You can change the role of auto-provisioned users at any time.

Auto-provisioning users with SSO is on by default for Dedicated Cloud instances and Self-Managed deployments. You can turn off auto provisioning. Turning auto provisioning off lets you selectively add specific users to your Forge organization.

The following tabs describe how to turn off SSO based on deployment type:

> [tab] Multi-tenant Cloud
>
> Auto provisioning with SSO isn't configurable for Multi-tenant Cloud. Contact your Forge team for assistance.

> [tab] Dedicated Cloud and Self-Managed
>
> For Dedicated Cloud instances, contact your Forge team if you want to turn off auto provisioning with SSO.
>
> For Self-Managed deployments, use the W\&B Console to turn off auto provisioning with SSO:
>
> 1. Navigate to `https://<org-name>.io/console/settings/`. Replace `<org-name>` with your organization name.
> 2. Select **Security**.
> 3. Select the **Disable SSO Provisioning** to turn off auto provisioning with SSO.

> [!NOTE]
>
> Auto provisioning with SSO is useful for adding users to an organization at scale because organization admins don't need to generate individual user invitations.

### Domain capture

Domain capture lets you automatically add people with a company email address, such as `@example.com`, to Forge. This helps all your employees join the right organization and ensures that new users don't create assets outside your company jurisdiction.

> [!NOTE]
>
> Domain capture is not available on free or trial plans.

Domains must be unique; you can't use a domain that's already in use by another organization.

> [tab] Multi-tenant Cloud
>
> This table summarizes the behavior of new and existing users with and without domain capture enabled:
>
> | | With domain capture | Without domain capture |
> | - | - | - |
> | New users | Users who sign up for Forge from verified domains are automatically added as members to your organization's default team. They can choose additional teams to join at sign up, if you enable team joining. They can still join other organizations and teams with an invitation. | Users can create Forge accounts without knowing a centralized organization is available. |
> | Invited users | Invited users automatically join your organization when accepting your invite. Invited users aren't automatically added as members to your organization's default team. They can still join other organizations and teams with an invitation. | Invited users automatically join your organization when accepting your invite. They can still join other organizations and teams with an invitation. |
> | Existing users | Existing users with verified email addresses from your domains can join your organization's teams within the W\&B App. All data that existing users create before joining your organization remains. Forge doesn't migrate the existing user's data. | Existing Forge users may be spread across multiple organizations and teams. |
>
> To automatically assign non-invited new users to a default team when they join your organization:
>
> 1. In the upper right corner of the header, open your account menu.
> 2. Select **Settings**.
> 3. Within the **Settings** tab, select **General**.
> 4. Click the **Claim domain** button within **Domain capture**.
> 5. Select the team that you want new users to automatically join from the **Default team** dropdown. If no teams are available, update team settings. See the instructions in [Add and manage teams](#add-and-manage-teams).
> 6. Click the **Claim email domain** button.
>
> You must enable domain matching within a team's settings before you can automatically assign non-invited new users to that team.
>
> 1. In Forge, open the dashboard of the team for which you want to enable domain matching.
> 2. Click the **Settings** tab.
> 3. In the **Privacy** section, turn on **Automatically recommend new users with matching email domains join this team upon signup**.

> [tab] Dedicated Cloud and Self-Managed
>
> Contact your Forge Account Team to configure domain capture. Afterward, when a user creates a Forge account with a company email address, your deployment automatically prompts them to contact your admin to request access.
>
> | | With domain capture | Without domain capture |
> | - | - | - |
> | New users | Users who sign up for Forge on Multi-tenant Cloud from verified domains are automatically prompted to contact an admin with an email address you customize. They can still create an organization on Multi-tenant Cloud to trial the product. | Users can create W\&B Multi-tenant Cloud accounts without learning that their company has a centralized dedicated instance. |
> | Existing users | Existing Forge users may be spread across multiple organizations and teams. | Existing Forge users may be spread across multiple organizations and teams. |

### Assign or update a user's role

A user's organization role controls what they can do across the organization, such as inviting other users, managing teams, or viewing content. Assign or update roles to give each user the appropriate level of administrative authority.

Every member in an organization has an organization role and seat for both Forge and Weave. The type of seat they have determines both their billing status and the actions they can take in each product line.

When you invite a user to your organization, you assign them an organization role. You can change any user's role later from the **Org role** dropdown.

The **Org role** dropdown includes the following roles:

| Role | Descriptions |
| - | - |
| Admin | An organization admin who can add users to the organization or remove them, change user roles, manage custom roles, add teams and more. Forge recommends ensuring there is more than one admin in the event that your admin is unavailable. |
| Member | A regular user of the organization, invited by an organization admin. An organization member cannot invite other users or manage existing users in the organization. |
| Viewer (Enterprise-only feature) | A view-only user of your organization, invited by an organization admin. A viewer only has read access to the organization and the underlying teams that they are a member of. |
| Billing only (Multi-tenant Cloud) | A billing-focused role for Multi-tenant Cloud organizations. You can assign this role only to the organization's billing user. Billing-only users can manage billing workflows, such as subscriptions, invoices, and payment methods, but they can't invite users, manage teams, or perform non-billing admin actions. Billing-only users are also removed from all organization teams and always have **No access** for both Models and Weave. |

Custom roles don't appear in the **Org role** dropdown. An organization admin creates custom roles in organization settings. A team admin uses the **Team role** dropdown to assign them to members of a specific team. Creating or assigning a custom role doesn't change a user's organization role. For more information, see [Add and manage custom roles](#add-and-manage-custom-roles).

### Organization role permissions

Organization roles control administrative actions at the organization scope. They're separate from these other sets of roles:

* [Team roles](#assign-or-update-a-team-members-role) control what a user can do inside a specific team.
* [Registry roles](https://docs.coreweave.com/products/registry/configure_registry.md#details-about-registry-roles) control what a user can do in a given registry.
* [Models seats and Weave access](#assign-or-update-a-users-access) control product access.

The following tables summarize what **Member** and **Admin** users can do at the organization level. For team-scoped actions such as logging runs or editing reports, see [Team roles and permissions](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md#team-roles-and-permissions). For registry-scoped actions, see [Registry role permissions](https://docs.coreweave.com/products/registry/configure_registry.md#role-permissions).

> [!NOTE]
>
> The **Viewer** organization role and custom team roles are Enterprise-only features. A **Viewer** has read-only access to teams they belong to and can't perform write actions at the organization or team level. Custom team roles inherit from **Viewer** or **Member** and add team-level permissions.

#### User management

| Permission | Permission group | Member | Admin |
| - | - | :-: | :-: |
| View the organization user list | Read | X | X |
| Invite users to the organization | Admin | | X |
| Remove users from the organization | Admin | | X |
| Assign or change a user's organization role | Admin | | X |
| Assign or change a user's Models seat or Weave access | Admin | | X |
| Export the organization user list as CSV | Admin | | X |
| View organization activity and usage trends | Read | X | X |

When **Enforce team visibility restrictions** is enabled, non-admin members can view profiles only for themselves or for users who share a team with them. Organization admins can view all member profiles. For more information, see [Privacy settings](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#enforce-privacy-settings-for-all-teams).

#### Teams

| Permission | Permission group | Member | Admin |
| - | - | :-: | :-: |
| Create teams in the organization | Admin | | X |
| Join teams when invited or through domain capture | Read | X | X |
| View team membership for teams the user belongs to | Read | X | X |
| View team membership for teams the user doesn't belong to | Read | | X |
| Invite users to a team without being a member of that team | Admin | | X |
| Add themselves to a team | Admin | | X |

> [!NOTE]
>
> On Self-Managed deployments, instance admins can optionally enable team creation for non-admin users. This option is managed at the instance level, not in organization settings. If you don't know whether your instance has this option enabled, contact your instance admin or Forge support.

Organization admins are assigned the **Admin** role in [registries](https://docs.coreweave.com/products/registry/configure_registry.md#role-permissions) that are visible at the organization level.

#### Organization settings

| Permission | Permission group | Member | Admin |
| - | - | :-: | :-: |
| Change the organization name (Multi-tenant Cloud) | Admin | | X |
| Configure domain capture and SSO auto-provisioning | Admin | | X |
| Enforce organization-wide [privacy settings](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#enforce-privacy-settings-for-all-teams) | Admin | | X |
| Create, edit, and delete custom roles (Enterprise) | Admin | | X |
| Connect external storage buckets at the organization level (Enterprise) | Admin | | X |

#### Billing

| Permission | Permission group | Member | Admin |
| - | - | :-: | :-: |
| Assign the billing admin | Admin | | X |
| Manage subscriptions, payment methods, and plan upgrades | Billing | | X |
| Cancel subscriptions | Billing | | X |
| Configure usage alerts | Billing | | X |

Billing actions, including configuring usage alerts, depend on the user's **organization role**, not on who is designated the billing admin. A user needs the **Admin** or **Billing only** role to reach the **Billing** and **Usage & Alerts** tabs. A billing admin whose organization role is **Member** does not see them. Unless they are also an organization admin, a billing admin can't perform other organization admin actions such as inviting users or creating teams.

On Multi-tenant Cloud, you can optionally assign the billing admin the **Billing only** organization role. This role is restricted to the billing user, removes team membership, and enforces **No access** for both Models and Weave while preserving billing administration capabilities.

#### Security and automation

| Permission | Permission group | Member | Admin |
| - | - | :-: | :-: |
| Authenticate to the [SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md) | Admin | | X |
| Create and manage organization-scoped service accounts | Admin | | X |
| View and manage all organization API keys | Admin | | X |

Organization-scoped service accounts used for SCIM automation have admin-equivalent access for SCIM operations.

To change a user's role:

1. In the upper right corner of the header, open your account menu.
2. Select **Users**.
3. Find the user in the list. You can filter by name or email in the search bar.
4. Select a role from the **Org role** dropdown next to the name of the user.

### Assign or update a user's access

A user within an organization has a **Models seat** and **Weave access** level. Each is one of **Full**, **Viewer**, or **No access**. These are separate from the organization **Viewer** role, which controls organization-wide permissions.

| Seat or access level | Description |
| - | - |
| Full | Full access to read, write, and export in Models or Weave for that user. |
| Viewer | Read-only access to Models or Weave for that user. |
| No access | No access to Models or Weave for that user. |

Models seat and Weave access are defined at the organization level and inherited by the team. To change them, navigate to the organization user list and use the following steps:

1. For Multi-tenant Cloud users, navigate to your organization's settings at `https://forge.coreweave.com/account-settings/[ORGANIZATION]/settings`. Replace `[ORGANIZATION]` with your organization name. For Dedicated Cloud and Self-Managed deployments, navigate to `https://[YOUR-INSTANCE].wandb.io/org/dashboard`.
2. Select the **Users** tab.
3. From the **MODELS SEAT** and **WEAVE ACCESS** dropdowns for that user, select the levels you want to assign.

> [!NOTE]
>
> The organization role and subscription type determine which seat types are available within your organization.

### Remove a user

1. In the upper right corner of the header, open your account menu.
2. Select **Users**.
3. Provide the name or email of the user in the search bar.
4. Select the **action ()** menu when it appears.
5. From the dropdown, choose **Remove member**.

### Assign the billing admin

1. In the upper right corner of the header, open your account menu.
2. Select **Users**.
3. Provide the name or email of the user in the search bar.
4. Under the **Billing admin** column, choose the user you want to assign as the billing admin.

## Add and manage teams

Teams group related users together so they can collaborate on projects and share resources within the organization. The following sections describe how to create teams, invite users to them, and manage team membership and roles.

Use your organization's dashboard to create and manage teams within your organization. An organization admin or a team admin can:

* Invite users to a team or remove users from a team.
* Manage a team member's roles.
* Automate the addition of users to a team when they join your organization.
* Manage team storage from the team's dashboard in Forge.

### Create a team

Create a team from the **Teams** section of the Weights & Biases sidebar. You can't change a team's name or storage settings after you create the team.

> [tab] Multi-tenant Cloud
>
> 1. In Forge, open the product launcher and select **Weights & Biases**. The Weights & Biases home page opens, with a sidebar that lists your projects and teams.
>
>    The sidebar appears only on the Weights & Biases home page. If you don't see it, widen your browser window.
> 2. In the sidebar, under **Teams**, click **Create a team to collaborate**.
>
>    ![The Teams section of the Weights & Biases home page sidebar, with Create a team to collaborate highlighted](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/create_new_team.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=ba2b465a5e0f9e0cbfbf0c5c4624174e)
> 3. In the drawer that opens, enter a name for the team in the **Team Name** field.
> 4. Under **Storage Type**, select **W\&B cloud storage**, or select **External storage** to store the team's data in your own bucket. External storage requires an Enterprise plan. For setup details, see [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md).
> 5. (Optional) In the **Invite team members** field, enter the email addresses or usernames of the users to invite, separated by commas.
> 6. Click **Create team**.
>
> Forge opens the new team's page.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. From any page, click the Weights & Biases logo in the upper left corner of the header to open the navigation sidebar. On the home page in a wide browser window, the sidebar is already open.
> 2. In the sidebar, under **Teams**, click **Create new team**.
> 3. In the **Create a team** modal, enter a name for the team in the **Team name** field.
> 4. Under **Storage type**, choose where to store the team's data.
> 5. Click **Create team**.
>
> The modal closes, and the new team appears in the sidebar under **Teams**.

Once you have a team, you can add users to that team.

### Invite users to a team

Invite users to a team in your organization. Use the team's dashboard to invite users using their email address or Forge username if they already have a Forge account.

1. In Forge, open the team's page.
2. Click the **Users** tab. On some teams, this tab is named **Members**.

   ![A team page in Forge, with the Users tab highlighted](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/team_settings.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d5e661891bff07925edaf5ada363a797)
3. Click **Invite new user**.
4. In the **Add a user to a team** panel, enter the user's email address or username in the **Email or username** field, and select the role to assign from the **Select team role** dropdown. For more information about roles a user can have in a team, see [Team roles](#assign-or-update-a-team-members-role).
5. Click **Send invite**.

By default, only a team or instance admin can invite members to a team. To change this behavior, see [Team settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md#privacy).

Besides inviting users manually with email invites, you can automatically add new users to a team if the new user's [email matches the domain of your organization](#domain-capture).

### Match members to a team organization during sign up

Allow new users within your organization to discover teams within your organization when they sign up. New users must have a verified email domain that matches your organization's verified email domain. Verified new users can view a list of verified teams that belong to an organization when they sign up for a Forge account.

An organization admin must enable domain claiming. To enable domain capture, see the steps described in [Domain capture](#domain-capture).

### View team member status

> [!NOTE]
>
> The **Status** column is available on Dedicated Cloud and Self-Managed deployments only.

The **Status** column in a team's member list shows whether each member can sign in. Use it to tell an active member apart from one who hasn't accepted their invitation yet or whose account an organization admin deactivated.

To view the status of a team's members:

1. Open the team's page.
2. Click the **Users** tab. On some teams, this tab is named **Members**.

Each member's status is one of the following:

| Status | Definition |
| - | - |
| Active | The member accepted their invitation and can sign in. |
| Invite pending | Forge sent an invitation, but the member hasn't accepted it yet. |
| Deactivated | An organization admin deactivated the account. The member can't sign in to the organization or any of its teams. |

Deactivated members remain in a team's member list, and any runs they logged to the team remain attributed to them. For a deactivated member, the **Team Role**, **Models Seat**, and **Weave Access** columns also read **Deactivated** instead of a role or seat, and you can't change their role or copy a team invite link.

To filter the list by status, enter a status such as **Deactivated** in the search field.

To review the status of every user in the organization rather than a single team, see [View organization activity](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/org_dashboard.md#view-user-status-and-activity). From here, an organization admin can deactivate or reactivate a user.
To deactivate or reactivate a user with SCIM instead, see [Deactivate user](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#deactivate-user) and [Reactivate user](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#reactivate-user).

### Assign or update a team member's role

A team member's role determines what they can do within the team, such as managing other members, contributing content, or viewing data only. Update a team member's role when their responsibilities within the team change.

1. Open the team's page.
2. Click the **Users** tab. On some teams, this tab is named **Members**.
3. In the team member's row, click the dropdown in the **Team Role** column.
4. Select the role to assign. Forge applies the change immediately.

You can't change the role of a member whose invitation is still pending, a deactivated member, or a service account. Their **Team Role** column shows **Invited**, **Deactivated**, or **Service** instead of a dropdown.

This table lists the roles you can assign to a member of a team:

| Role | Definition |
| - | - |
| Admin | A user who can add and remove other users in the team, change user roles, and configure team settings. |
| Member | A regular user of a team, invited by email or their organization-level username by the team admin. A member user can't invite other users to the team. |
| View-Only (Enterprise plans on Multi-tenant Cloud; always available on Dedicated Cloud and Self-Managed) | A view-only user of a team, invited by email or their organization-level username by the team admin. A view-only user only has read access to the team and its contents. |
| Custom Roles (Enterprise-only feature) | Custom roles let organization admins compose new roles by inheriting from the preceding View-Only or Member roles and adding additional permissions to achieve fine-grained access control. Team admins can then assign any of those custom roles to users in their respective teams. For more information, see the [custom roles announcement](https://forge.coreweave.com/wandb/wandb_fc/announcements/reports/Introducing-Custom-Roles-for-W-B-Teams--Vmlldzo2MTMxMjQ3). |

> [!NOTE]
>
> Service accounts aren't users, but rather non-human identities used for automation. **Service accounts** provide API keys for automated workflows and don't consume user licenses. For more information about creating and managing service accounts, see [Use service accounts to automate workflows](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md).

### Remove users from a team

Remove a user from a team using the team's dashboard. Forge preserves runs created in a team, even if the member who created the runs is no longer on that team.

1. Open the team's page.
2. Click the **Users** tab. On some teams, this tab is named **Members**.
3. Next to the user you want to remove, click the **action ()** menu.
4. Select **Remove user**.

## Add and manage custom roles

Custom roles let you tailor permissions beyond the built-in roles when the standard View-Only, Member, and Admin roles don't match your organization's access requirements. Use custom roles to grant specific permissions while still building on a familiar base role.

> [!NOTE]
>
> Custom roles require an Enterprise plan or license. They are available on Multi-tenant Cloud, Dedicated Cloud, and Self-Managed.

Organization admins can compose a new role based on either the **Viewer** or **Member** predefined role and add additional permissions to achieve fine-grained access control. When an organization admin creates a custom role, it becomes available to teams in the organization. It doesn't appear in the **Org role** dropdown or change any user's organization role. A team admin assigns the custom role to individual members from a team's **Team role** dropdown.

To create a custom role:

> [tab] Multi-tenant Cloud
>
> 1. In the upper right corner of the header, open your account menu.
> 2. Select **Settings**.
> 3. Click **Roles**.
> 4. In the **Custom roles** section, click **Create a role**.
> 5. Provide a name for the role. Optionally provide a description.
> 6. Choose the role to base the custom role on, either **Viewer** or **Member**.
> 7. To add permissions, click the **Search permissions** field, then select one or more permissions to add.
> 8. Review the **Custom role permissions** section, which summarizes the permissions the role has.
> 9. Click **Create Role**.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. Navigate to `https://<org-name>.wandb.io/org/settings/`. Replace `<org-name>` with your organization name.
> 2. In the **Custom roles** section, click **Create a role**.
> 3. Provide a name for the role. Optionally provide a description.
> 4. Choose the role to base the custom role on, either **Viewer** or **Member**.
> 5. To add permissions, click the **Search permissions** field, then select one or more permissions to add.
> 6. Review the **Custom role permissions** section, which summarizes the permissions the role has.
> 7. Click **Create Role**.

A team admin can now [assign the custom role to members of a team](#assign-or-update-a-team-members-role).
