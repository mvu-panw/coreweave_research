# Automate user and team management

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/automate_iam

# Automate user and team management

> Automate your deployment's user and team management at scale using the SCIM API and the Python SDK API.

This page describes how to automate user and team management at scale using the [SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md) and the [Python SDK API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md).

## SCIM API

Use the W\&B SCIM API to manage your organization's users and teams at scale through an identity provider (IdP) like Okta or Microsoft Entra.

For more information, see [Authentication](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#authentication) on the SCIM reference page.

> [!TIP]
>
> Weights & Biases's implementation includes endpoints for creating and managing custom roles and for assigning built-in and custom roles. Role endpoints aren't part of the official SCIM schema. Weights & Biases adds role endpoints to support automated management of custom roles.

The following sections describe each category of the SCIM API.

### User SCIM API

The [User SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#user-resource) lets you create, deactivate, fetch, and list users in an organization, and assign predefined or custom roles. For complete request and response examples, see the [SCIM reference](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#user-management).

> [!NOTE]
>
> To deactivate a user, send `PATCH /scim/Users/{id}` with `{"active": false}`. The hosting option determines the outcome: Dedicated Cloud and Self-Managed deployments retain the user record, while Multi-tenant Cloud removes the user from the organization. Reactivation isn't available in Multi-tenant Cloud. Re-add the user instead. See [Deactivate user](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#deactivate-user) and [Reactivate user](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#reactivate-user).

### Group SCIM API

The [Group SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#group-resource) lets you manage Weights & Biases teams, including creating or removing teams in an organization. To add or remove users in an existing team, use `PATCH Group`.

> [!NOTE]
>
> Weights & Biases has no notion of a "group of users having the same role." A Weights & Biases team closely resembles a group and lets users with different roles work collaboratively on a set of related projects. Teams can consist of different groups of users. Assign each user in a team a role: team admin, member, viewer, or a custom role.
>
> Weights & Biases maps Group SCIM API endpoints to Weights & Biases teams because of the similarity between groups and Weights & Biases teams.

### Custom role SCIM API

The [Custom Role SCIM API](https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim.md#role-resource) lets you manage custom roles, including creating, listing, or updating custom roles in an organization.

> [!WARNING]
>
> Delete a custom role with caution.
>
> To delete a custom role within an organization, use the `DELETE Role` endpoint. Weights & Biases assigns the inherited predefined role to all users who had the custom role before deletion.
>
> To update the inherited role for a custom role, use the `PUT Role` endpoint. This operation doesn't affect any existing non-inherited custom permissions in the custom role.

## W\&B Python SDK API

Use the [W\&B Python SDK API](https://docs.coreweave.com/products/wandb/ref/python/public-api/api.md) to manage organization users, teams, and team membership through the following classes:

* [`User`](https://docs.coreweave.com/products/wandb/ref/python/public-api/user)
* [`Team`](https://docs.coreweave.com/products/wandb/ref/python/public-api/team)
* [`Member`](https://docs.coreweave.com/products/wandb/ref/python/public-api/member)
