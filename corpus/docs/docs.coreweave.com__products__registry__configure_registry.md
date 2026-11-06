# Configure registry access

Source: https://docs.coreweave.com/products/registry/configure_registry

# Configure registry access

> Configure Registry access by managing users and teams, assigning roles, and setting role-based permissions.

A registry admin can [configure registry roles](https://docs.coreweave.com/products/registry/configure_registry.md#configure-registry-roles), [add users](https://docs.coreweave.com/products/registry/configure_registry.md#add-a-user-or-a-team-to-a-registry), or [remove users](https://docs.coreweave.com/products/registry/configure_registry.md#remove-a-user-or-team-from-a-registry) from a registry by configuring the registry's settings.

## Manage users

### Add a user or a team

Registry admins can add individual users or entire teams to a registry. To add a user or team to a registry:

1. Navigate to **Registry**.
2. Select the registry you want to add a user or team to.
3. Click on the gear icon on the upper right hand corner to access the registry settings.
4. In the **Registry access** section, click **Add access**.
5. Specify one or more user names, emails, or the team names to the **Include users and teams** field.
6. Click **Add access**.

Learn more about [configuring user roles in a registry](https://docs.coreweave.com/products/registry/configure_registry.md#configure-registry-roles), or [registry role permissions](https://docs.coreweave.com/products/registry/configure_registry.md#role-permissions).

### Remove a user or team

A registry admin can remove individual users or entire teams from a registry. To remove a user or team from a registry:

1. Navigate to **Registry**.
2. Select the registry you want to remove a user from.
3. Click on the gear icon on the upper right hand corner to access the registry settings.
4. Navigate to the **Registry access** section and type in the username, email, or team you want to remove.
5. Click the **Delete** button.

> [!NOTE]
>
> Removing a user from a team also removes that user's access to the registry.

### Change the owner of a registry

A registry admin can designate any member as a registry's owner, including a **Restricted Viewer** or a **Viewer**. Registry ownership is primarily for accountability purposes and does not confer any additional permissions beyond those granted by the user's assigned role.

To change the owner:

1. Navigate to **Registry**.
2. Select the registry you want to configure.
3. Click the gear icon on the upper right hand corner.
4. Scroll to the **Registry members and roles** section.
5. Hover over the row for a member.
6. Click the **action ()** menu at the end of the row, then click **Make owner**.

## Configure Registry roles

This section shows how to configure roles for Registry members. For more information about Registry roles, including the cabilities of each role, order of precedence, defaults, and more, see [Details about Registry roles](#details-about-registry-roles).

1. Navigate to **Registry**.
2. Select the registry you want to configure.
3. Click the gear icon on the upper right hand corner.
4. Scroll to the **Registry members and roles** section.
5. Within the **Member** field, search for the user or team you want to edit permissions for.
6. In the **Registry role** column, click the user's role.
7. From the dropdown, select the role you want to assign to the user.

## Details about Registry roles

The following sections give more information about Registry roles.

> [!NOTE]
>
> A team's registry role is separate from each member's [team role](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md#team-roles-and-permissions). If you belong to a team that has been added to a registry, W\&B considers the team's assigned registry role, not your role within the team, when it calculates your effective registry role.

### Role types

Registry has the following roles:

* **Restricted Viewer**: Provides read-only access to registry artifact metadata. Restricted Viewers can view artifact details, but they cannot access artifact file contents or create, update, or delete collections, automations, or other registry resources. [This role is available for Dedicated Cloud and Self-Managed Server v0.75.0 or newer](https://docs.coreweave.com/products/registry/configure_registry.md#restricted-viewer-role-details).
* **Viewer**: Provides read-only access to registry artifacts with the ability to view collection details, view linked artifact details, download artifacts, and use artifacts with `wandb.Run.use_artifact()` in the W\&B SDK.
* **Member**: Provides permissions to create, update, and delete collections, automations, and other registry resources. Also provides read access to registry artifacts.
* **Admin**: Provides all permissions that a Member has, as well as permissions to manage registry settings and user roles.

See [Role permissions](#role-permissions) for more information about the permissions provided by each role.

### Role permissions

The following table lists each Registry role, along with the permissions provided by each role:

| Permission | Permission Group | Restricted Viewer (Multi-tenant Cloud, by invitation) | Viewer | Member | Admin |
| - | - | - | :-: | :-: | :-: |
| View a collection's details | Read | ✓ | ✓ | ✓ | ✓ |
| View a linked artifact's details | Read | ✓ | ✓ | ✓ | ✓ |
| Usage: Consume an artifact in a registry with use\_artifact | Read | | ✓ | ✓ | ✓ |
| Download a linked artifact | Read | | ✓ | ✓ | ✓ |
| Download files from an artifact's file viewer | Read | | ✓ | ✓ | ✓ |
| Search a registry | Read | ✓ | ✓ | ✓ | ✓ |
| View a registry's settings and user list | Read | ✓ | ✓ | ✓ | ✓ |
| Create a new automation for a collection | Create | | | ✓ | ✓ |
| Turn on Slack notifications for new version being added | Create | | | ✓ | ✓ |
| Create a new collection | Create | | | ✓ | ✓ |
| Create a new registry | Create | | | ✓ | ✓ |
| Edit collection card (description) | Update | | | ✓ | ✓ |
| Edit linked artifact description | Update | | | ✓ | ✓ |
| Add or delete a collection's tag | Update | | | ✓ | ✓ |
| Add or delete an alias from a linked artifact | Update | | | ✓ | ✓ |
| Add or delete a [protected alias](https://docs.coreweave.com/products/registry/aliases.md#protected-aliases) from a linked artifact | Update | | | | ✓ |
| Create or delete a [protected alias](https://docs.coreweave.com/products/registry/aliases.md#protected-aliases) | Update | | | | ✓ |
| Link a new artifact | Update | | | ✓ | ✓ |
| Edit allowed types list for a registry | Update | | | ✓ | ✓ |
| Edit registry name | Update | | | ✓ | ✓ |
| Delete a collection | Delete | | | ✓ | ✓ |
| Delete an automation | Delete | | | ✓ | ✓ |
| Unlink an artifact from a registry | Delete | | | ✓ | ✓ |
| Edit accepted artifact types for a registry | Admin | | | | ✓ |
| Change registry visibility (Organization or Restricted) | Admin | | | | ✓ |
| Add users to a registry | Admin | | | | ✓ |
| Assign or change a user's role in a registry | Admin | | | | ✓ |

### Default roles

W\&B automatically assigns a default **registry role** to a user or team when they are added to a registry. The default role is the starting role that appears in the registry's role dropdown. It is not always the user's final, effective role.

The default role depends on the deployment type and the entity type:

| Entity | Default registry role (Dedicated Cloud / Self-Managed) | Default registry role (Multi-tenant Cloud) |
| - | - | - |
| Team | Restricted Viewer (Server v0.75.0+) Viewer (Server v0.74.x and below) | Restricted Viewer |
| User (non admin) | Restricted Viewer (Server v0.75.0+) Viewer (Server v0.74.x and below) | Restricted Viewer |
| Service account (non admin) | Member<sup>[1](#service_account_footnote)</sup> | Member<sup>[1](#service_account_footnote)</sup> |
| Org admin | Admin | Admin |

1: Service accounts cannot have **Viewer** or **Restricted Viewer** roles. See [Service account access](#service-account-access) for how a service account's access is determined.

A registry admin can assign or modify roles for users and teams in the registry.
See [Configure user roles in a registry](https://docs.coreweave.com/products/registry/configure_registry.md#configure-registry-roles) for more information.

### Effective and inherited registry roles

A user's *effective registry role* is the role that determines what they can actually do in a registry. The registry's membership list shows this role in light gray next to the role dropdown in the user's row.

![Registry membership list showing the user's effective registry role](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/registry/_media/role_conflict.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=58bdc72510f9e1a3afacb9b7ba422801)

W\&B calculates the effective role by selecting the user's highest applicable role from these sources:

* The default registry role for the organization, if it is not a restricted registry.
* Their assigned role in the registry.
* The role(s) assigned in the registry to any team(s) they are a part of.

If a higher role comes from the default organization registry role or from a team that has been added to the registry, the user inherits that higher role. For example:

* A user with the **Viewer** role in a registry is effectively an **Admin** if they belong to a team that has the **Admin** role in that registry.
* A user with the **Viewer** role in a registry is effectively a **Member** if they belong to a team that has the **Member** role in that registry.
* A user with the **Member** role in a registry is effectively a **Member** even if they belong to a team that has the **Viewer** role in that registry.

In other words, the default or assigned registry role can be lower than the user's effective role.

> [!NOTE]
>
> Service accounts do not inherit elevated registry permissions from their teams. See [Service account access](#service-account-access) for more information.

### Service account access

Service accounts are an exception to inherited registry roles. A service account does not inherit elevated registry permissions from its team. For example, if a team has **Admin** access to a registry, service accounts on that team receive only the automatic service account access level, not **Admin** access.

A registry admin can explicitly grant a service account higher access by [adding the service account to the registry with a Member or Admin role](https://docs.coreweave.com/products/registry/configure_registry.md#role-types).

Automatic service account access depends on registry visibility:

* **Organization visibility**: A service account automatically has **Member** access.
* **Restricted visibility**: A service account automatically has **Member** access only if one of its teams has **Member** or **Admin** access to the registry. If all of the service account's teams have **Viewer** or **Restricted Viewer** access, the service account does not receive access automatically.

See [Visibility types](https://docs.coreweave.com/products/registry/create_registry.md#visibility-types) for more information about registry visibility types.

### Restricted Viewer role details

The **Restricted Viewer** role is Generally Available (GA). For Dedicated Cloud and Self-Managed, Server v0.75.0 or newer is required.

This role provides read-only access to registry artifacts without the ability to create, update, or delete collections, automations, or other registry resources.

Unlike a **Viewer**, a **Restricted Viewer**:

* Cannot download artifact files or access file contents.
* Cannot use artifacts with `wandb.Run.use_artifact()` in the W\&B SDK.

#### SDK compatibility

> [!NOTE]
>
> **SDK version requirement**
>
> To use the W\&B SDK to access artifacts as a **Restricted Viewer**, you must use W\&B SDK version 0.19.9 or higher. Otherwise, some SDK commands will result in permission errors.

When a **Restricted Viewer** uses the W\&B Python SDK, certain functions are not available or work differently.

The following methods are not available and result in permission errors:

* [`wandb.Run.use_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-run-use_artifact)
* [`wandb.Artifact.download()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-download)
* [`wandb.Artifact.file()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-file)
* [`wandb.Artifact.files()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-files)

The following methods are limited to artifact metadata:

* [`wandb.Artifact.get_entry()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-get_entry)
* [`wandb.Artifact.get_path()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-get_path)
* [`wandb.Artifact.get()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-get)
* [`wandb.Artifact.verify()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-verify)

### Cross-registry permissions

A user can have different roles in different registries. For example, a user can be a **Restricted Viewer** in Registry A and a **Viewer** in Registry B. In this case:

* The same artifact linked to both registries will have different access levels
* In Registry A, the user is a **Restricted Viewer** and cannot download files or use the artifact
* In Registry B, the user is a **Viewer** and can download files and use the artifact
* In other words, access is determined by the registry in which the artifact is accessed
