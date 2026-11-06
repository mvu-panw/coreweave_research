# Manage access control for projects

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects

> Manage project access using visibility scopes and project-level roles

# Manage access control for projects

Define the scope of a Weights & Biases project to limit who can view, edit, and submit runs to it. This page is for team and organization admins, and project owners, who need to control access to sensitive workflows or limit collaboration to a specific group of users.

You can combine two controls to configure the access level for any project within a Weights & Biases team. **Visibility scope** is the higher-level mechanism. Use it to control which groups of users can view or submit runs in a project. For a project with *Team* or *Restricted* visibility scope, you can then use **Project level roles** to control the level of access that each user has within the project.

> [!NOTE]
>
> The owner of a project or a team admin can set or edit a project's visibility.

## Visibility scopes

Visibility scope determines which users in your organization can see and contribute to a project. You can choose from four project visibility scopes. From most public to most private, they are:

| Scope | Icon | Description |
| - | - | - |
| Open | | Anyone who knows about the project can view it and submit runs or reports. |
| Public | | Anyone who knows about the project can view it. Only your team can submit runs or reports. |
| Team | | Only members of the parent team can view the project and submit runs or reports. Anyone outside the team can't access the project. |
| Restricted | | Only invited members from the parent team can view the project and submit runs or reports. |

> [!NOTE]
>
> Set a project's scope to **Restricted** if you want to collaborate on workflows related to sensitive or confidential data. When you create a restricted project within a team, you can invite or add specific members from the team to collaborate on relevant experiments, artifacts, and reports.
>
> Unlike other project scopes, all members of a team don't get implicit access to a restricted project. At the same time, team admins can join restricted projects if needed.

### Set visibility scope on a new or existing project

Set a project's visibility scope when you create a project or when you edit it later. The following sections describe both workflows.

> [!NOTE]
>
> * Only the owner of the project or a team admin can set or edit its visibility scope.
> * When a team admin enables **Make all future team projects private (public sharing not allowed)** within a team's privacy setting, that turns off **Open** and **Public** project visibility scopes for that team. In this case, your team can only use **Team** and **Restricted** scopes.

#### Set visibility scope when you create a project

To set the visibility scope for a new project:

1. Navigate to your Weights & Biases organization on a W\&B Multi-tenant Cloud, Dedicated Cloud, or Self-Managed instance.

2. Click the **Create a new project** button in the left-hand sidebar's **My projects** section. Alternatively, navigate to the **Projects** tab of your team and click the **Create new project** button in the upper right-hand corner.

3. After you select the parent team and enter the name of the project, select the desired scope from the **Project visibility** dropdown.

   Complete the following step if you select **Restricted** visibility.

4. Provide names of one or more Weights & Biases team members in the **Invite team members** field. Add only those members who are essential to collaborate on the project, since other team members don't get implicit access to a restricted project.

   ![Restricted project configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/restricted_project_2.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=998cd5824f0133b2425e03c5f05a6619)

   > [!NOTE]
   >
   > You can add or remove members in a restricted project later, from its **Project Roles** tab.

Weights & Biases creates the project with the selected visibility scope, and only the invited members (for a restricted project) or in-scope users can access it.

#### Edit visibility scope of an existing project

To change the visibility scope of an existing project:

1. Navigate to your Weights & Biases project.
2. Click **Project** in the left navigation to open the project **Overview** page. The **Project visibility** field on the **Details** tab shows the current scope.
3. In the upper right of the **Overview** page, click **Edit**. The **Edit project** drawer opens.
4. From the **Project visibility** dropdown, select the desired scope, then click **Save**. See [Visibility scopes](#visibility-scopes).

   > [!NOTE]
   >
   > If you select **Restricted** visibility, you must complete the next step.

   Weights & Biases updates the project's visibility scope, and access reflects the new scope.
5. To share a restricted project:
   1. On the project **Overview** page, select the **Project Roles** tab.
   2. Click **Add user** and select one or more specific users to invite them to the project.

If you can't edit the project, you don't have permission to change its visibility. Ask the project owner or a team admin to change it for you.

If you can edit the project but the scope you want is missing from the **Project visibility** dropdown, a setting is limiting the available scopes:

* **Open** and **Public** don't appear when a team admin has turned on **Make all future team projects private (public sharing not allowed)** for the team.
* **Open** and **Public** don't appear for a project that is currently **Restricted**. Change the project to **Team** first, save, and then edit it again.

In a project that belongs to your personal entity rather than a team, the **Team** scope is labeled **Private**: only you can access the project.

> [!WARNING]
>
> * All members of a team lose access to a project if you change its visibility scope from **Team** to **Restricted**, and you must invite team members to give them access.
> * All members of a team get access to a project if you change its visibility scope from **Restricted** to **Team**.
> * If you remove a team member from the user list for a restricted project, they lose access to that project.

### Other key things to note for restricted scope

Keep the following behaviors in mind when working with restricted projects:

* If you want to use a team-level service account in a restricted project, you must invite or add it specifically to the project. Otherwise a team-level service account can't access a restricted project by default.
* You can't move runs from a restricted project, but you can move runs from a non-restricted project to a restricted one.
* You can convert the visibility of a restricted project to only **Team** scope, irrespective of the team privacy setting **Make all future team projects private (public sharing not allowed)**.
* If the owner of a restricted project isn't part of the parent team anymore, the team admin must change the owner to maintain access to the project.

## Project level roles

After you set a project's visibility scope, you can further refine each user's permissions inside the project by assigning a project level role. For *Team* or *Restricted* scoped projects in your team, you can assign a specific role to a user, which can differ from that user's team level role. For example, if a user has *Member* role at the team level, you can assign the *View-Only*, *Admin*, or any available custom role to that user within a *Team* or *Restricted* scope project in that team.

> [!NOTE]
>
> Project level roles are in preview on W\&B Multi-tenant Cloud, Dedicated Cloud, and Self-Managed instances.

### Assign a project level role to a user

To assign a project level role:

1. Navigate to your Weights & Biases project.
2. In the project sidebar, click **Project**.
3. Navigate to the **Project Roles** tab in the project.
4. Click the currently assigned role for the relevant user in the **Project Role** field, which opens a dropdown listing the other available roles.
5. Select another role from the dropdown. The change saves instantly.

> [!NOTE]
>
> When you change the project level role for a user to be different from their team level role, the project level role includes a **\*** to indicate the difference.

### Other key things to note for project level roles

Keep the following behaviors in mind when assigning or changing project level roles:

* By default, project level roles for all users in a *Team* or *Restricted* scoped project **inherit** their respective team level roles.
* You **can't** change the project level role of a user who has *View-Only* role at the team level.
* If the project level role for a user within a particular project **is the same as** the team level role, and a team admin later changes the team level role, Weights & Biases automatically changes the relevant project role to track the team level role.
* If you change the project level role for a user within a particular project such that **it differs from** the team level role, and a team admin later changes the team level role, the relevant project level role remains as is.
* If you remove a user from a *Restricted* project when their project level role differed from the team level role, and you then add the user back to the project later, they inherit the team level role due to the default behavior. If needed, change the project level role again to differ from the team level role.
