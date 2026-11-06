# Team settings

Source: https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams

> Collaborate with your colleagues, share results, and track all the experiments across your team. Manage team settings including members, alerts, and privacy.

# Team settings

Use Teams as a central workspace for your ML team. This page explains how organization admins and team admins can create a team, configure its members and privacy, and assign roles so that collaborators can share experiments and reports while keeping sensitive work appropriately scoped.

A Team can do the following:

* **Track all the experiments** your team has tried so you never duplicate work.
* **Save and reproduce** previously trained models.
* **Share progress** and results with your boss and collaborators.
* **Catch regressions** and immediately get alerted when performance drops.
* **Benchmark model performance** and compare model versions.

![Teams workspace overview](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/teams_overview.webp?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5000a7729160c093ad034e4030cb8c9d)

> [!NOTE]
>
> Only Administration account types can change team settings or remove a member from a team.

## Create a collaborative team

Follow these steps to create a new team and invite your first collaborators. After the team exists, you can refine membership, alerts, and privacy in [Team configuration](#team-configuration).

1. [Sign up or log in](https://id.coreweave.com/signup) to Forge.
2. In the left navigation, click **Create a team to collaborate**.
3. Create your team and invite collaborators.
4. Configure your team using the settings described in the following sections.

> [!NOTE]
>
> Only the admin of an organization can create a new team.

## Team configuration

You can configure settings for your team, including its membership, alerts, and privacy settings. The following sections describe each settings category.

To manage your team's settings, navigate to the **Teams** section in the left menu and click the team you want to change settings for.

### Members

The Members section shows a list of all pending invitations and the members who have accepted the invitation to join the team. The list displays each member's name, username, email, team role, and access privileges to Models and W\&B Weave, which are inherited from the organization. You can choose from the standard team roles **Admin**, **Member**, and **View-Only**. If your organization has created [custom roles](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-custom-roles), you can assign a custom role instead.

On Dedicated Cloud and Self-Managed deployments, the list also includes a **Status** column that shows whether each member is active, has an invitation pending, or has an account that an organization admin deactivated. See [View team member status](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#view-team-member-status).

See [Add and Manage teams](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/manage-organization.md#add-and-manage-teams) for information on how to create a team, manage teams, and manage team membership and roles. To configure who can invite new members and configure other privacy settings for the team, refer to [Privacy](#privacy).

To remove a team member, admins can open the team settings page and click the delete button next to the departing member's name. Any runs logged to the team remain after a user leaves.

### Avatar

A team avatar helps members and visitors recognize the team across the W\&B app. To set an avatar for your team:

1. Navigate to the **Teams** section in the left menu and click the team you want to add an avatar for. This opens the team's overview page.
2. Hover over the team's default avatar image in the upper-left corner of the page and click the **Upload photo** button. This opens a file prompt.
3. From the file prompt, select the image you want to use and then click **Open**. This uploads the photo to your team and sets it as your team's avatar.

### Alerts

Alerts keep your team informed about run status without requiring anyone to watch the dashboard. You can set up alerts to notify your team when runs crash and finish. Weights & Biases sends alerts through email or Slack, and you can customize them to meet your needs.

In the **Team alerts** section, toggle the switch next to the event type you want to receive alerts from. Weights & Biases provides the following event type options:

* **Run finished**: A W\&B run successfully finishes.
* **Run crashed after**: A run stops responding for longer than the number of minutes you set.
* **wandb.alert()**: A custom scriptable alert. See [Send alerts with `wandb.Run.alert()`](https://docs.coreweave.com/products/wandb/runs/alert) for more information.

### Slack channel integrations

Configure Slack destinations where your team's [automations](https://docs.coreweave.com/products/wandb/automations.md) can send notifications when an event occurs in a registry or a project, such as when a new artifact is created or when a run metric meets a defined threshold. Refer to [Create a Slack automation](https://docs.coreweave.com/products/wandb/automations/create-automations/slack.md).

> [!NOTE]
>
> This feature isn't available on Community Edition.

### Webhooks

Configure webhooks that your team's [automations](https://docs.coreweave.com/products/wandb/automations.md) can run when an event occurs in a registry or a project, such as when a new artifact is created or when a run metric meets a defined threshold. Refer to [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md).

> [!NOTE]
>
> This feature isn't available on Community Edition.

### Privacy

Team privacy settings control visibility, invitations, report sharing, and defaults such as code saving for runs in the team. Team admins can change these options on the team **Settings** page unless an organization admin has [enforced the same category of policy](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#enforce-privacy-settings-for-all-teams) for all teams. Organization admins can still open the team **Settings** page to review configuration.

You can change the following privacy settings:

* Hide this team from all non-members.
* Make all future team projects private (public sharing not allowed).
* Allow any team member to invite other members (not just admins).
* Disable public sharing to outside of team for reports in private projects. This disables existing magic links.
* Automatically recommend new users with matching email domains join this team upon signup.
* Enable code saving by default.

For step-by-step navigation and how organization enforcement interacts with team toggles, see [Configure privacy settings](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md).

To change these settings, open the team's dashboard in Weights & Biases, select **Team settings** in the left navigation, then open the **Privacy** section.

### Usage

The **Usage** section describes the total memory usage the team has consumed on Weights & Biases. The default storage plan is 100 GB. For more information about storage and pricing, see the [Pricing](https://coreweave.com/forge-pricing) page.

### External Storage

The **Storage** section describes the cloud storage bucket configuration that the team's data uses. For more information, see [Secure Storage Connector](#secure-storage-connector) or check out our [W\&B Server](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) docs if you are self-hosting.

## Create a team profile

A team profile is a public-facing page that helps your team attract collaborators and highlight its work. You can customize your team's profile page to show an introduction and showcase reports and projects that are visible to the public or team members. Present reports, projects, and external links.

Use a team profile to do the following:

* **Highlight your research** to visitors by showcasing your best public reports.
* **Showcase the most active projects** to make it easier for teammates to find them.
* **Find collaborators** by adding external links to your company or research lab's website and any papers you've published.

## Team roles and permissions

Team roles determine what each member can see and do within the team, from viewing reports to managing other members. Select a team role when you invite colleagues to join a team. The following team role options are available:

* **Admin**: Team admins can add and remove other admins or team members. They have permissions to modify all projects and full deletion permissions. This includes, but is not limited to, deleting runs, projects, artifacts, and sweeps.
* **Member**: A regular member of the team. By default, only an admin can invite a team member. To change this behavior, refer to [Privacy settings](#privacy).
* **View-Only**: View-Only members can view assets within the team such as runs, reports, and workspaces. They can follow and comment on reports, but they can't create, edit, or delete project overview, reports, or runs.
* **Custom roles (Enterprise-only feature)**: Custom roles let organization admins compose new roles based on either of the **View-Only** or **Member** roles, together with additional permissions to achieve fine-grained access control. Team admins can then assign any of those custom roles to users in their respective teams. Refer to [Introducing Custom Roles for Teams](https://forge.coreweave.com/wandb/wandb_fc/announcements/reports/Introducing-Custom-Roles-for-W-B-Teams--Vmlldzo2MTMxMjQ3) for details.

A team member can delete only runs they created. Suppose you have two members A and B. Member B moves a run from team B's project to a different project owned by Member A. Member A cannot delete the run Member B moved to Member A's project. An admin can manage runs and sweep runs created by any team member.

### Service accounts

In addition to user roles, teams can also use **service accounts** for automation. Service accounts aren't users, but rather non-human identities used for automated workflows. Refer to [Use service accounts to automate workflows](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md) for detailed information.

> [!NOTE]
>
> CoreWeave recommends assigning more than one admin in a team to ensure that admin operations can continue when the primary admin isn't available.

### Team settings

The following table summarizes which roles can manage team membership and team-wide settings. Team settings let you manage the settings for your team and its members. With these privileges, you can effectively oversee and organize your team within Weights & Biases.

| Permissions | View-Only | Team Member | Team Admin |
| - | - | - | - |
| Add team members | | | X |
| Remove team members | | | X |
| Manage team settings | | | X |

### Reports

Report permissions grant access to create, view, and edit reports. The following table lists permissions that apply to all reports across a given team.

| Permissions | View-Only | Team Member | Team Admin |
| - | - | - | - |
| View reports | X | X | X |
| Create reports | | X | X |
| Edit reports | | X (team members can only edit their own reports) | X |
| Delete reports | | X (team members can only edit their own reports) | X |

### Experiments

The following table lists permissions that apply to all experiments across a given team.

| Permissions | View-Only | Team Member | Team Admin |
| - | - | - | - |
| View experiment metadata (includes history metrics, system metrics, files, and logs) | X | X | X |
| Edit experiment panels and workspaces | | X | X |
| Log experiments | | X | X |
| Delete experiments | | X (team members can only delete experiments they created) | X |
| Stop experiments | | X (team members can only stop experiments they created) | X |

### Artifacts

The following table lists permissions that apply to all artifacts across a given team.

| Permissions | View-Only | Team Member | Team Admin |
| - | - | - | - |
| View artifacts | X | X | X |
| Download artifacts | X | X | X |
| Create artifacts | | X | X |
| Delete artifacts | | X | X |
| Edit metadata | | X | X |
| Edit aliases | | X | X |
| Delete aliases | | X | X |

### System settings (W\&B Server only)

This section applies only to self-hosted W\&B Server deployments. Use system permissions to create and manage teams and their members and to adjust system settings. These privileges enable you to effectively administer and maintain the Weights & Biases instance.

| Permissions | View-Only | Team Member | Team Admin | System Admin |
| - | - | - | - | - |
| Configure system settings | | | | X |
| Create or delete teams | | | | X |

### Team service account behavior

* When you configure a team in your training environment, you can use a service account from that team to log runs in either of private or public projects within that team. Additionally, you can attribute those runs to a user if `WANDB_USERNAME` or `WANDB_USER_EMAIL` variable exists in your environment and the referenced user is part of that team.
* When you do not configure a team in your training environment and use a service account, the runs log to the named project within that service account's parent team. In this case as well, you can attribute the runs to a user if `WANDB_USERNAME` or `WANDB_USER_EMAIL` variable exists in your environment and the referenced user is part of the service account's parent team.
* A service account can't log runs to a private project in a team different from its parent team. A service account can log runs to a project only if the project visibility is set to `Open`.

## Team trials

See the [pricing page](https://coreweave.com/forge-pricing) for more information on Forge plans. You can download all your data at any time, either using the dashboard UI or the [Export API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md).

## Advanced configuration

The following advanced options are available to teams with additional data residency or compliance requirements.

### Secure storage connector

The team-level secure storage connector lets teams use their own cloud storage bucket with Weights & Biases. This provides greater data access control and data isolation for teams with highly sensitive data or strict compliance requirements. Refer to [Secure Storage Connector](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) for more information.
