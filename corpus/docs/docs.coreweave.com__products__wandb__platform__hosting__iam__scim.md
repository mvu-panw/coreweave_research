# Manage users, groups, and roles with SCIM

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/scim

# Manage users, groups, and roles with SCIM

> Use the SCIM API to automate provisioning of users, groups, and custom roles in an organization.

> [!NOTE]
>
> Watch a [video demonstrating SCIM in action](https://www.youtube.com/watch?v=Nw3QBqV0I-o) (12 min)

## Overview

This page describes how instance and organization admins use the System for Cross-domain Identity Management (SCIM) API to automate identity management in Weights & Biases. With the SCIM API, you can provision and deprovision users, manage team membership, and define custom roles programmatically through an identity provider or CI/CD pipeline instead of clicking through the W\&B App. SCIM groups map to Weights & Biases Teams.

> [!NOTE]
>
> In multi-tenant Forge, SCIM provisioning is separate from CoreWeave Automated User Provisioning. Provision and deprovision users in each system separately. See [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md).

Weights & Biases's SCIM API is compatible with identity providers such as Okta and Microsoft Entra. For SSO configuration with Okta, Microsoft Entra, and other identity providers, see the [SSO documentation](https://docs.coreweave.com/products/wandb/platform/hosting/iam/sso.md).

For practical Python examples that demonstrate how to interact with the SCIM API, visit the [`wandb-scim`](https://github.com/wandb/examples/tree/master/wandb-scim) repository.

### Supported features

The SCIM API supports the following features:

* **Filtering**: The API supports filtering for `/Users` and `/Groups` endpoints.
* **PATCH operations**: Supports `PATCH` for partial resource updates.
* **ETag support**: Conditional updates using ETags for conflict detection.
* **Service account authentication**: Organization service accounts can access the API.
* **Service account lifecycle**: Provision and deprovision [team-scoped and organization-scoped service accounts](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md). Supported on **Multi-tenant Cloud** and on **Dedicated Cloud** and **Self-Managed** v0.81.0+.

> [!NOTE]
>
> If you're an admin of multiple Enterprise [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) organizations, configure the organization that receives SCIM API requests so that requests made with your API key affect the correct organization. Click the account selector in the upper-right corner, click **User settings**, then check the **Default API organization** setting.
>
> The chosen hosting option determines the value for the `[HOST-URL]` placeholder used in the examples on this page.
>
> Examples use user IDs such as `abc` and `def`. Real requests and responses use hashed values for user IDs.

## Authentication

Every SCIM request must be authenticated as an admin principal. Organization admins can authenticate with a **Bearer token** or **HTTP Basic** credentials. Either style uses the *same API key string* where a key applies. Choose a user identity or an organization-scoped service account after reviewing the key differences in the following section.

### Key differences

The following list compares user credentials and service account credentials for SCIM authentication:

* Who should use it: Users are best for interactive, one-off admin actions. Service accounts are best for automation and integrations (CI/CD, provisioning tools).
* Credentials: Users send username and API key for Basic auth. Service accounts send only an API key (no username) for Basic auth. For Bearer auth, send only the API key in the header (no username).
* Bearer versus Basic: Bearer uses `Authorization: Bearer [API-KEY]` with the key verbatim. Basic uses `Authorization: Basic <base64(...)>` (users encode `username:API-KEY`, and service accounts encode `:API-KEY` with a leading colon and empty username).
* Scope and permissions: Use an API key from an instance or organization admin user, or from an [organization-scoped service account](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#organization-scoped-service-accounts). Keys from [team-scoped service accounts](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#team-scoped-service-accounts) can't authenticate to the SCIM API. Service accounts that use SCIM are organization-scoped and headless, which supports clearer audit trails for automation.
* Where to get credentials: Users copy their API key from **User settings**. Organization-scoped service account keys are in the organization dashboard under the **Service account** tab.
* Multi-tenant Cloud: If you have access to more than one Multi-tenant Cloud organization, you must set the Default API organization to ensure that SCIM API calls are routed to the intended organization.

### Bearer token

Send the API key as a Bearer token:

```bash theme={"system"}
Authorization: Bearer [API-KEY]
```

The `[API-KEY]` value is the same string you'd use as the password in HTTP Basic authentication for that principal. Don't Base64-encode the key for Bearer requests.

> [!NOTE]
>
> Bearer authentication for the SCIM API is available in W\&B Multi-tenant Cloud, and in Dedicated Cloud and Self-Managed v0.79.0 and later.

The following examples use `[API-KEY]` as a placeholder. Replace it with a real key from an admin user or an organization-scoped service account.

**List users**

```bash theme={"system"}
curl -s -S \
  -H "Authorization: Bearer [API-KEY]" \
  -H "Content-Type: application/scim+json" \
  "[HOST-URL]/scim/Users"
```

**Create a user**

```bash theme={"system"}
curl -s -S -X POST \
  -H "Authorization: Bearer [API-KEY]" \
  -H "Content-Type: application/scim+json" \
  "[HOST-URL]/scim/Users" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName": "dev-user2",
    "emails": [{"primary": true, "value": "dev-user2@example.com"}]
  }'
```

For more information, see [Create user](#create-user).

### Users

Use your personal admin credentials when you perform interactive admin tasks. Construct the HTTP `Authorization` header as `Basic <base64(username:API-KEY)>`.

For example, authorize as `demo:p@55w0rd`:

```bash theme={"system"}
Authorization: Basic ZGVtbzpwQDU1dzByZA==
```

### Service accounts

Use an organization-scoped service account for automation or integrations. Construct the HTTP `Authorization` header as `Basic <base64(:API-KEY)>` (note the leading colon and empty username). Find service account API keys in the organization dashboard under the **Service account** tab. Refer to [Organization-scoped service accounts](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#organization-scoped-service-accounts).

For example, authorize with API key `sa-p@55w0rd`:

```bash theme={"system"}
Authorization: Basic OnNhLXBANTV3MHJk
```

## Microsoft Entra ID configuration

Use this section when you configure automatic user and group provisioning from Microsoft Entra ID to Weights & Biases through the SCIM API.

For Entra SSO setup, see [Configure SSO with Entra](https://docs.coreweave.com/products/wandb/platform/hosting/iam/sso.md).

### Tenant URL

In your Entra enterprise application's provisioning settings, set **Tenant URL** to your W\&B SCIM base URL with the Entra feature flag query parameter `aadOptscim062020` appended:

```text theme={"system"}
[HOST-URL]/scim?aadOptscim062020
```

For example, if your instance is at `https://wandb.example.com`, set the tenant URL to `https://wandb.example.com/scim?aadOptscim062020`.

The `aadOptscim062020` parameter enables Entra-specific handling in the W\&B SCIM API. Without it, Entra can send user deactivation requests with string boolean values (`"False"` or `"True"`) instead of JSON booleans (`false` or `true`), which can cause deactivation to fail.

Set **Secret Token** to the API key from an organization admin user or an organization-scoped service account. See [Authentication](#authentication).

> [!NOTE]
>
> When you append `aadOptscim062020` to the tenant URL, user deactivation from Entra's **Provision on demand** UI in the Microsoft Entra admin center might not work because that UI still sends string boolean values. To test deactivation manually, send a SCIM `PATCH` request using the `PatchOp` `Operations` format that replaces `active` with `false` (see [Deactivate user](#deactivate-user)).

### Team names

Name Entra groups that map to Weights & Biases teams using lowercase letters and hyphens, for example `ml-platform` or `data-science`. Avoid spaces, underscores, and other special characters in group display names that you sync to Weights & Biases.

### User attribute mappings

Configure the following attribute mappings in Entra for SCIM user provisioning:

| Weights & Biases custom app attribute | Source attribute (Entra) | Apply this mapping | Match objects using this attribute |
| - | - | - | - |
| `emails[type eq "work"].value` | `mail` | Always | Yes |
| `active` | `Not([IsSoftDeleted])` | Always | |
| `displayName` | `displayName` | Always | |
| `userName` | `displayName` | Only on object creation | |

> [!NOTE]
>
> On **Multi-tenant Cloud**, a user's account isn't managed by the organization. Weights & Biases doesn't support updating `displayName` through SCIM on Multi-tenant Cloud. See [Update user display name](#update-user-display-name).

### Group attribute mappings

Configure the following attribute mappings in Entra for SCIM group (team) provisioning:

| Weights & Biases custom app attribute | Source attribute (Entra) | Apply this mapping | Match objects using this attribute |
| - | - | - | - |
| `displayName` | `displayName` | Only on object creation | Yes |
| `members` | `members` | Always | |

## User management

The SCIM user resource maps to Weights & Biases users and service accounts. Use the endpoints in this section to provision, update, and remove users and service accounts in your organization, for example, when you onboard new employees, rotate service credentials, or remove access for departing users.

For service account concepts and UI workflows, see [Use service accounts to automate workflows](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md).

> [!NOTE]
>
> **Breaking change for integrations that parse SCIM User JSON**
>
> * In Dedicated Cloud and Self-Managed v0.80.1+, and in Multi-tenant Cloud deployments after April 30, 2026, responses from `/scim/Users` (including `GET` user, `GET` users, and `PATCH` responses that return a User) serialize `emails` as a JSON array of objects using lowercase field names (`value`, `primary`, and optional `type` or `display`), matching SCIM 2.0.
> * Deployments on older releases return `emails` as a single JSON object with PascalCase keys (`Value`, `Primary`, and similar).
>
> If your code reads `emails` from SCIM *responses*, treat `emails` as an array and read the primary entry (or the first element).
>
> Request bodies for creating or updating users already used the array form and are unchanged. The `list-users` filter `emails.value eq "..."` is also unchanged.

### Get user

Retrieves information for a specific user or service account in your organization by user ID, or for a user by email address.

Service account responses include `accountType` (`SERVICE` for team-scoped service accounts, `ORG_SERVICE` for organization-scoped service accounts). Service accounts don't include `emails`.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `GET`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |

#### Example

> [tab] Get User Request
>
> ```bash theme={"system"}
> GET /scim/Users/abc
> ```

> [tab] Get User Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "daysActive": 42,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "lastActiveAt": "2023-10-15T14:32:10Z",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1"
> }
> ```
>
> The response includes details about the user's activity in the organization:
>
> * **`daysActive`**: Total number of days the user has been active in the organization.
> * **`lastActiveAt`**: ISO 8601 timestamp of the user's most recent activity. Returns `null` if the user hasn't been active.
>
> The definition of "active" differs by deployment type:
>
> * **Dedicated Cloud / Self-Managed**: A user is active if they sign in, open any page in the W\&B App, log runs, use the SDK, or interact with the Weights & Biases server in any way.
> * **Multi-tenant Cloud**: A user is active if they perform any auditable action scoped to the organization after May 8, 2025. See [Audit logging actions](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/audit-logging.md#actions) for the full list.

### List users

Retrieves a list of all users and service accounts in your organization. Each resource includes `accountType` (`USER`, `SERVICE`, or `ORG_SERVICE`).

#### Filter users

The `/Users` endpoint supports filtering users by username or email:

* `userName eq "value"`: Filter by username.
* `emails.value eq "value"`: Filter by email address.

##### Example

```bash theme={"system"}
GET /scim/Users?filter=userName eq "john.doe"
GET /scim/Users?filter=emails.value eq "john@example.com"
```

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users`
* **Method**: `GET`

#### Example

> [tab] List Users Request
>
> ```bash theme={"system"}
> GET /scim/Users
> ```

> [tab] List Users Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "Resources": [
>         {
>             "active": true,
>             "daysActive": 42,
>             "displayName": "Dev User 1",
>             "emails": [
>                 {
>                     "primary": true,
>                     "value": "dev-user1@example.com"
>                 }
>             ],
>             "id": "abc",
>             "lastActiveAt": "2023-10-15T14:32:10Z",
>             "meta": {
>                 "resourceType": "User",
>                 "created": "2023-10-01T00:00:00Z",
>                 "lastModified": "2023-10-01T00:00:00Z",
>                 "location": "Users/abc"
>             },
>             "schemas": [
>                 "urn:ietf:params:scim:schemas:core:2.0:User"
>             ],
>             "userName": "dev-user1"
>         }
>     ],
>     "itemsPerPage": 9999,
>     "schemas": [
>         "urn:ietf:params:scim:api:messages:2.0:ListResponse"
>     ],
>     "startIndex": 1,
>     "totalResults": 1
> }
> ```
>
> The response includes details about each user's activity in the organization:
>
> * **`daysActive`**: Total number of days the user has been active in the organization.
> * **`lastActiveAt`**: ISO 8601 timestamp of the user's most recent activity. Returns `null` if the user hasn't been active.
>
> The definition of "active" differs by deployment type:
>
> * **Dedicated Cloud / Self-Managed**: A user is active if they sign in, open any page in the W\&B App, log runs, use the SDK, or interact with the Weights & Biases server in any way.
> * **Multi-tenant Cloud**: A user is active if they perform any auditable action scoped to the organization after May 8, 2025. See [Audit logging actions](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/audit-logging.md#actions) for the full list.

### Create user

Creates a new user in your organization.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users`
* **Method**: `POST`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `emails` | array | Yes | Array of email objects. Must include a primary email |
| `userName` | string | Yes | The username for the new user |
| `modelsSeat` | string | No | Models seat level. One of `full`, `viewer`, or `none`. Defaults to `full`. |
| `weaveRole` | string | No | Weave role level. One of `full`, `viewer`, or `none`. Defaults to `full`. |
| `registryAccess` | string | No | Registry entitlement. One of `enabled` or `none`. When omitted, effective access is derived from `modelsSeat` and `weaveRole` at read time. Available in **Multi-tenant Cloud** and in **Dedicated Cloud** and **Self-Managed** v0.83.0+. |

#### Example

> [tab] Create User Request (Dedicated/Self-Managed)
>
> ```bash theme={"system"}
> POST /scim/Users
> ```
>
> ```json theme={"system"}
> {
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user2@example.com"
>         }
>     ],
>     "userName": "dev-user2",
>     "modelsSeat": "full",
>     "weaveRole": "full"
> }
> ```

> [tab] Create User Request (Multi-tenant)
>
> ```bash theme={"system"}
> POST /scim/Users
> ```
>
> ```json theme={"system"}
> {
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:teams:2.0:User"
>     ],
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user2@example.com"
>         }
>     ],
>     "userName": "dev-user2",
>     "modelsSeat": "full",
>     "weaveRole": "full",
>     "urn:ietf:params:scim:schemas:extension:teams:2.0:User": {
>         "teams": ["my-team"]
>     }
> }
> ```

#### Response

> [tab] Create User Response (Dedicated/Self-Managed)
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 2",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user2@example.com"
>         }
>     ],
>     "id": "def",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "location": "Users/def"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "modelsSeat": "full",
>     "weaveRole": "full",
>     "userName": "dev-user2"
> }
> ```

> [tab] Create User Response (Multi-tenant)
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 2",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user2@example.com"
>         }
>     ],
>     "id": "def",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "location": "Users/def"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:teams:2.0:User"
>     ],
>     "userName": "dev-user2",
>     "organizationRole": "member",
>     "modelsSeat": "full",
>     "weaveRole": "full",
>     "teamRoles": [
>         {
>             "teamName": "my-team",
>             "roleName": "member"
>         }
>     ],
>     "groups": [
>         {
>             "value": "my-team-id"
>         }
>     ]
> }
> ```

### Provision service account

Creates a team-scoped or organization-scoped service account in your organization. Use this endpoint to create headless identities for automation, CI/CD, or integrations that shouldn't be tied to a human user. Omit `accountType` to create a regular user instead. See [Create user](#create-user).

> [!NOTE]
>
> Available in **Dedicated Cloud** and **Self-Managed** v0.81.0+ and in **Multi-tenant Cloud**.
>
> * Set `userName` to the service account name. The API uses `userName` for the account's display name. The `displayName` field in the request body is ignored.
> * `emails` aren't required for service accounts.
> * `modelsSeat` and `weaveRole` aren't supported on create and return `400 Bad Request` if present.
> * Service accounts can't be updated with `PATCH` or `PUT`, can't be deactivated, and can't be assigned organization, team, or registry roles through SCIM. Create API keys in the W\&B App after provisioning.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users`
* **Method**: `POST`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `userName` | string | Yes | Unique name for the service account. |
| `accountType` | string | Yes | `SERVICE` for a [team-scoped service account](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#team-scoped-service-accounts), or `ORG_SERVICE` for an [organization-scoped service account](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#organization-scoped-service-accounts). |
| `urn:ietf:params:scim:schemas:extension:teams:2.0:User` | object | Yes | Teams extension object. |
| `defaultTeam` | string | Yes | Sub-field of the teams extension. Name of an existing Weights & Biases Team. The service account is created as a member of this team. For team-scoped service accounts, this is the only team they join. Organization-scoped service accounts are also added automatically to teams created later through SCIM. |
| `teams` | array | No | **Multi-tenant Cloud only.** Team names to add the account to. Include the same team as `defaultTeam` when you use this field. |

#### Example

> [tab] Provision Team Service Account Request
>
> ```bash theme={"system"}
> POST /scim/Users
> ```
>
> ```json theme={"system"}
> {
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:teams:2.0:User"
>     ],
>     "userName": "sa-deploy-bot",
>     "accountType": "SERVICE",
>     "urn:ietf:params:scim:schemas:extension:teams:2.0:User": {
>         "defaultTeam": "ml-platform"
>     }
> }
> ```

> [tab] Provision Org Service Account Request
>
> ```bash theme={"system"}
> POST /scim/Users
> ```
>
> ```json theme={"system"}
> {
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:teams:2.0:User"
>     ],
>     "userName": "sa-ci-runner",
>     "accountType": "ORG_SERVICE",
>     "urn:ietf:params:scim:schemas:extension:teams:2.0:User": {
>         "defaultTeam": "ml-platform"
>     }
> }
> ```

#### Response

> [tab] Provision Team Service Account Response
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "accountType": "SERVICE",
>     "active": true,
>     "displayName": "sa-deploy-bot",
>     "id": "xyz",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "location": "Users/xyz"
>     },
>     "organizationRole": "member",
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:wandb:2.0:User"
>     ],
>     "teamRoles": [
>         {
>             "teamName": "ml-platform",
>             "roleName": "member"
>         }
>     ],
>     "urn:ietf:params:scim:schemas:extension:wandb:2.0:User": {
>         "organizationRole": "member"
>     },
>     "userName": "sa-deploy-bot"
> }
> ```

> [tab] Provision Org Service Account Response
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "accountType": "ORG_SERVICE",
>     "active": true,
>     "displayName": "sa-ci-runner",
>     "id": "xyz",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "location": "Users/xyz"
>     },
>     "organizationRole": "member",
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User",
>         "urn:ietf:params:scim:schemas:extension:wandb:2.0:User"
>     ],
>     "teamRoles": [
>         {
>             "teamName": "ml-platform",
>             "roleName": "member"
>         }
>     ],
>     "urn:ietf:params:scim:schemas:extension:wandb:2.0:User": {
>         "organizationRole": "member"
>     },
>     "userName": "sa-ci-runner"
> }
> ```

For an organization-scoped service account, `accountType` is `ORG_SERVICE`.

In **Self-Managed** deployments, `organizationRole` is `service` or `org_service` instead of `member`, matching the account type.

If the response returns one of the following errors, check the request for these common problems:

* `409 Conflict`: The request includes duplicate `userName` keys for the same service account.
* `400 Bad Request`: The request is missing `defaultTeam` or sets it to an invalid value.

### Deprovision service account

Permanently deletes a service account and its organization membership. Use this endpoint when a service account is no longer needed (for example, after you retire an automation pipeline). This is a hard delete, and the account can't be reactivated through SCIM.

> [!NOTE]
>
> Available in **Dedicated Cloud** and **Self-Managed** v0.81.0+ and in **Multi-tenant Cloud**. Use the service account's SCIM user `id` from the provision response or from [Get user](#get-user). Deprovisioning doesn't delete API keys that were already issued. Revoke keys separately in the W\&B App if needed.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `DELETE`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the service account. |

#### Example

> [tab] Deprovision Service Account Request
>
> ```bash theme={"system"}
> DELETE /scim/Users/xyz
> ```

> [tab] Deprovision Service Account Response
>
> ```text theme={"system"}
> (Status 204)
> ```

### Delete user

> [!WARNING]
>
> **Maintain admin access**
>
> Ensure that at least one admin user always exists in your instance or organization. Otherwise, no user can configure or maintain your organization's Weights & Biases account. If an organization uses SCIM or another automated process to deprovision users from Weights & Biases, a deprovisioning operation could inadvertently remove the last remaining admin from the instance or organization.
>
> For assistance with developing operational procedures, or to restore admin access, contact [support](mailto:forge-support@coreweave.com).

Fully deletes a user from your organization. To delete a service account, see [Deprovision service account](#deprovision-service-account).

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `DELETE`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user to delete |

#### Example

> [tab] Delete User Request
>
> ```bash theme={"system"}
> DELETE /scim/Users/abc
> ```

> [tab] Delete User Response
>
> ```text theme={"system"}
> (Status 204)
> ```

> [!NOTE]
>
> To temporarily deactivate the user, refer to the [Deactivate user](#deactivate-user) API, which uses the `PATCH` endpoint.

### Update user email

Updates a user's primary email address.

**Not supported for Multi-tenant Cloud**, where a user's account isn't managed by the organization.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `emails` |
| `value` | array | Yes | Array with new email object |

#### Example

> [tab] Update Email Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "emails",
>             "value": [
>                 {
>                     "value": "newemail@example.com",
>                     "primary": true
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Update Email Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "newemail@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1"
> }
> ```

### Update user display name

Updates a user's display name.

**Not supported for Multi-tenant Cloud**, where a user's account isn't managed by the organization.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `displayName` |
| `value` | string | Yes | New display name |

#### Example

> [tab] Update Display Name Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "displayName",
>             "value": "John Doe"
>         }
>     ]
> }
> ```

> [tab] Update Display Name Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "John Doe",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2025-7-01T00:00:00Z",
>         "lastModified": "2025-7-01T00:00:00Z",
>         "location": "users/dev-user1"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1"
> }
> ```

### Deactivate user

Deactivates a user in your organization. The result differs by deployment type:

* **Dedicated Cloud** / **Self-Managed**: Sets the user's `active` field to `false`. To restore a deactivated user's access to your organization, see [Reactivate user](#reactivate-user).
* **Multi-tenant Cloud**: Removes the user from the organization. To restore the user's access, re-add them to your organization. See [Create user](#create-user-request-multi-tenant). In Multi-tenant Cloud, a user's account isn't managed by the organization.

> [!NOTE]
>
> This operation works for users only, not service accounts. Deactivating a service account isn't supported. Manage team service accounts in the settings for the Weights & Biases Team.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user to deactivate |
| `op` | string | Yes | `replace` |
| `value` | object | Yes | Object with `{"active": false}` |

#### Example

> [tab] Deactivate User Request (Dedicated/Self-Managed)
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "value": {"active": false}
>         }
>     ]
> }
> ```

> [tab] Deactivate User Request (Multi-tenant)
>
> ```bash theme={"system"}
> PATCH /scim/Users
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "value": {"active": false}
>         }
>     ]
> }
> ```

#### Response

> [tab] Deactivate User Response (Dedicated/Self-Managed)
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": false,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1"
> }
> ```

> [tab] Deactivate User Response (Multi-tenant)
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "value": {"active": true}
>         }
>     ]
> }
> ```

### Reactivate user

Reactivates a previously deactivated user in your organization.

> [!NOTE]
>
> * User reactivation works for users only, not service accounts. Reactivation isn't supported for service accounts. Manage service accounts in the settings for the Weights & Biases Team.
>
> * User reactivation isn't supported in [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md). To restore the user's access, re-add them to your organization. See [Create user](#create-user-request-multi-tenant). In Multi-tenant Cloud, a user's account isn't managed by the organization. An attempt to reactivate a user results in an HTTP `400` error. The `detail` field in the response body is returned verbatim from the API and may still use legacy product wording:
>   ```json theme={"system"}
>   {
>       "schemas": [
>           "urn:ietf:params:scim:api:messages:2.0:Error"
>       ],
>       "detail": "User reactivation operations are not supported in SaaS Cloud",
>       "status": "400"
>   }
>   ```

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user to reactivate |
| `op` | string | Yes | `replace` |
| `value` | object | Yes | Object with `{"active": true}` |

#### Example

> [tab] Reactivate User Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "value": {"active": true}
>         }
>     ]
> }
> ```

> [tab] Reactivate User Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1"
> }
> ```

### Assign organization role

Assigns an organization-level role to a user.

> [!NOTE]
>
> This operation works for users only, not service accounts. Custom roles aren't supported for service accounts.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `organizationRole` |
| `value` | string | Yes | Role name (`admin` or `member`) |

> [!NOTE]
>
> The organization-scoped `viewer` role is deprecated and can no longer be assigned in the UI. If you use SCIM to assign the `viewer` role to a user:
>
> * They're assigned the `member` role in the organization.
> * Their `modelsSeat` is set to `viewer` instead of `full`. This allows view-only access to Models and full access to Registry. If no Models seats are available, a `Seat limit reached` error is returned. This can be updated later if a seat is available.
> * Their `weaveRole` is set to `viewer` instead of `full`. This allows view-only access to Weave.
> * All of their existing team and project roles are set to `viewer`.
> * They're assigned the Registry `viewer` role in registries that are visible at the organization level.
>
> Assigning the `member` or `admin` organization role doesn't change the user's `modelsSeat` or `weaveRole`.

#### Example

> [tab] Assign Org Role Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "organizationRole",
>             "value": "admin"
>         }
>     ]
> }
> ```

> [tab] Assign Org Role Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "teamRoles": [
>         {
>             "teamName": "team1",
>             "roleName": "admin"
>         }
>     ],
>     "organizationRole": "admin"
> }
> ```

### Update Models seat

Updates a user's Models seat.

> [!NOTE]
>
> On **Multi-tenant Cloud** and on **Dedicated Cloud** and **Self-Managed** v0.83.0+, Registry access is decoupled from Models seats. Setting `modelsSeat` to `none` no longer revokes Registry access when the user has a non-`none` `weaveRole`. To revoke Registry access on those deployments, use [Update Registry access](#update-registry-access) and set `registryAccess` to `none`.
>
> On **Dedicated Cloud** and **Self-Managed** v0.82.0 and older, Registry access is still tied to `modelsSeat`. Set `modelsSeat` to `none` to revoke Registry access on those releases.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `modelsSeat` |
| `value` | string | Yes | Seat level (`full`, `viewer`, or `none`) |

#### Example

> [tab] Update Models Seat Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "modelsSeat",
>             "value": "full"
>         }
>     ]
> }
> ```

> [tab] Update Models Seat Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "organizationRole": "member",
>     "modelsSeat": "full",
>     "weaveRole": "full"
> }
> ```

### Update Weave role

Updates a user's Weave role.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `weaveRole` |
| `value` | string | Yes | Role level (`full`, `viewer`, or `none`) |

#### Example

> [tab] Update Weave Role Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "weaveRole",
>             "value": "full"
>         }
>     ]
> }
> ```

> [tab] Update Weave Role Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "organizationRole": "member",
>     "modelsSeat": "full",
>     "weaveRole": "full"
> }
> ```

### Update Registry access

Grants or revokes organization-level Registry access for a user. This entitlement is separate from [Registry roles](#add-to-registry) (`registryRoles`), which control per-registry permissions after a user is entitled.

On **Multi-tenant Cloud** and on **Dedicated Cloud** and **Self-Managed** v0.83.0+, users with a non-`none` `modelsSeat` or `weaveRole` are entitled to Registry by default. Set `registryAccess` to `none` to revoke Registry access without changing their Models seat or Weave role.

On **Dedicated Cloud** and **Self-Managed**, v0.82.0 and older, use [Update Models seat](#update-models-seat) and set `modelsSeat` to `none` to revoke Registry access. The `registryAccess` attribute isn't available on those releases.

When you omit `registryAccess` at create time, the API derives effective access from the user's `modelsSeat` and `weaveRole` when you read the user. An explicit `registryAccess` value overrides that derivation. Users with the billing-only organization role don't receive Registry access through this derivation.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `registryAccess` |
| `value` | string | Yes | Registry entitlement (`enabled` or `none`) |

#### Example

> [tab] Revoke Registry Access Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "registryAccess",
>             "value": "none"
>         }
>     ]
> }
> ```

> [tab] Revoke Registry Access Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "organizationRole": "member",
>     "modelsSeat": "none",
>     "weaveRole": "full",
>     "registryAccess": "none"
> }
> ```

### Assign team role

Assigns a team-level role to a user.

> [!NOTE]
>
> This operation works for users only, not service accounts. Custom roles aren't supported for service accounts.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `replace` |
| `path` | string | Yes | `teamRoles` |
| `value` | array | Yes | Array of objects with `teamName` and `roleName` |

#### Example

> [tab] Assign Team Role Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "teamRoles",
>             "value": [
>                 {
>                     "roleName": "admin",
>                     "teamName": "team1"
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Assign Team Role Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "teamRoles": [
>         {
>             "teamName": "team1",
>             "roleName": "admin"
>         }
>     ],
>     "organizationRole": "admin"
> }
> ```

### Add to Registry

Adds a user to a registry with an assigned registry-level role.

> [!NOTE]
>
> This operation works for users only, not service accounts. Custom roles aren't supported for service accounts.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `add` |
| `path` | string | Yes | `registryRoles` |
| `value` | array | Yes | Array of objects with `registryName` and `roleName` |

#### Example

> [tab] Add to Registry Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "registryRoles",
>             "value": [
>                 {
>                     "roleName": "admin",
>                     "registryName": "hello-registry"
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Add to Registry Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "registryRoles": [
>         {
>             "registryName": "hello-registry",
>             "roleName": "admin"
>         }
>     ],
>     "organizationRole": "admin"
> }
> ```

### Remove from Registry

Removes a user from a registry.

> [!NOTE]
>
> This operation removes a user from a specific registry. It doesn't revoke organization-level Registry access. To revoke Registry access entirely, use [Update Registry access](#update-registry-access).

> [!NOTE]
>
> * The remove operations follow RFC 7644 SCIM protocol specifications. Use the filter syntax `"registryRoles[registryName eq \"{registry_name}\"]"` to remove a user from a specific registry, or `"registryRoles"` to remove the user from all registries.
> * This operation works for users only, not service accounts. Remove service accounts from a registry in the settings for the Weights & Biases Team.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Users/{id}`
* **Method**: `PATCH`

#### Parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | string | Yes | The unique ID of the user |
| `op` | string | Yes | `remove` |
| `path` | string | Yes | `"registryRoles[registryName eq \"{registry_name}\"]"` or `"registryRoles"` |

#### Example

> [tab] Remove from Registry Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "registryRoles[registryName eq \"goodbye-registry\"]"
>         }
>     ]
> }
> ```

> [tab] Remove from Registry Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "registryRoles": [
>         {
>             "registryName": "hello-registry",
>             "roleName": "admin"
>         }
>     ],
>     "organizationRole": "admin"
> }
> ```

> [tab] Remove from ALL Registries Request
>
> ```bash theme={"system"}
> PATCH /scim/Users/abc
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "replace",
>             "path": "registryRoles"
>         }
>     ]
> }
> ```

> [tab] Remove from ALL Registries Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "active": true,
>     "displayName": "Dev User 1",
>     "emails": [
>         {
>             "primary": true,
>             "value": "dev-user1@example.com"
>         }
>     ],
>     "id": "abc",
>     "meta": {
>         "resourceType": "User",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Users/abc"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:User"
>     ],
>     "userName": "dev-user1",
>     "organizationRole": "admin"
> }
> ```

## Group resource

The SCIM group resource maps to a Weights & Biases Team. Use the endpoints in this section to create teams, manage team membership, and (optionally) configure team-level storage from your identity provider or automation. When you create a SCIM group in your IAM, it creates and maps to a Weights & Biases Team, and other SCIM group operations act on the team. To configure custom storage during team creation, include `storageBucket` in the request.

### Service accounts

When you create a Weights & Biases Team using SCIM, all organization-level service accounts are automatically added to the team, to maintain the service account's access to team resources.

### Filter groups

The `/Groups` endpoint supports filtering to search for specific teams.

#### Supported filters

The `/Groups` endpoint supports the following filter:

* `displayName eq "value"`: Filter by team display name.

#### Example

```bash theme={"system"}
GET /scim/Groups?filter=displayName eq "engineering-team"
```

### Get team

Retrieve team information by providing the team's unique ID.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Groups/{id}`
* **Method**: `GET`

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> GET /scim/Groups/ghi
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "acme-devs",
>     "id": "ghi",
>     "members": [
>         {
>             "Value": "abc",
>             "Ref": "",
>             "Type": "",
>             "Display": "dev-user1"
>         }
>     ],
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Groups/ghi"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### List teams

Retrieve a list of teams.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Groups`
* **Method**: `GET`

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> GET /scim/Groups
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "Resources": [
>         {
>             "displayName": "acme-devs",
>             "id": "ghi",
>             "members": [
>                 {
>                     "Value": "abc",
>                     "Ref": "",
>                     "Type": "",
>                     "Display": "dev-user1"
>                 }
>             ],
>             "meta": {
>                 "resourceType": "Group",
>                 "created": "2023-10-01T00:00:00Z",
>                 "lastModified": "2023-10-01T00:00:00Z",
>                 "location": "Groups/ghi"
>             },
>             "schemas": [
>                 "urn:ietf:params:scim:schemas:core:2.0:Group"
>             ]
>         }
>     ],
>     "itemsPerPage": 9999,
>     "schemas": [
>         "urn:ietf:params:scim:api:messages:2.0:ListResponse"
>     ],
>     "startIndex": 1,
>     "totalResults": 1
> }
> ```

### Create team

Creates a new team resource.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Groups`
* **Method**: `POST`

#### Supported fields

| Field | Type | Required |
| - | - | - |
| `displayName` | String | Yes |
| `members` | Multi-Valued Array | Yes (`value` sub-field is required and maps to a user ID) |
| `storageBucket` | Object | No |

You can configure team-level [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) during team creation by including a `storageBucket` object. If omitted, the team uses default or instance-level storage. Provision the bucket (policy, CORS, credentials) and determine the storage address format per provider using the BYOB guide. The `storageBucket` object has the following sub-fields:

* **Required**: `name` (bucket name), `provider` (one of `COREWEAVE`, `AWS`, `AZURE`, `GCP`, or `MINIO`). The value is case-sensitive. Use uppercase as shown.
* **Optional**: `path` (path prefix within the bucket), `kmsKeyId` (KMS key for encryption, for example for AWS), `awsExternalId` (AWS cross-account access), `azureTenantId` (Azure tenant ID), `azureClientId` (Azure managed identity client ID).

Weights & Biases validates that the bucket exists and is reachable before creating the team. If validation fails, the SCIM request fails and the team isn't created.

An invalid `provider` value returns `400 Bad Request` with a SCIM error that lists the allowed values.

#### Examples

These examples show how to create a team without custom storage and with BYOB storage on a specific provider. Select a tab for the desired storage configuration to see an example request, and select the **Response** tab for an example response.

> [tab] Request (no BYOB)
>
> ```bash theme={"system"}
> POST /scim/Groups
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>     "displayName": "wandb-support",
>     "members": [
>         {
>             "value": "def"
>         }
>     ]
> }
> ```

> [tab] CoreWeave
>
> ```bash theme={"system"}
> POST /scim/Groups
> Content-Type: application/scim+json
> ```
>
> ```json theme={"system"}
> {
>   "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>   "displayName": "ml-training-team",
>   "members": [
>     {
>       "value": "user@example.com",
>       "display": "user@example.com"
>     }
>   ],
>   "storageBucket": {
>     "name": "wandb-coreweave-bucket",
>     "provider": "COREWEAVE",
>     "path": "ml-training/experiments"
>   }
> }
> ```

> [tab] AWS S3
>
> ```bash theme={"system"}
> POST /scim/Groups
> Content-Type: application/scim+json
> ```
>
> ```json theme={"system"}
> {
>   "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>   "displayName": "ml-team",
>   "members": [
>     {
>       "value": "user@example.com",
>       "display": "user@example.com"
>     }
>   ],
>   "storageBucket": {
>     "name": "my-company-wandb-data",
>     "provider": "AWS",
>     "path": "ml-team/experiments",
>     "kmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012",
>     "awsExternalId": "wandb-external-id-abc123"
>   }
> }
> ```

> [tab] Azure
>
> ```bash theme={"system"}
> POST /scim/Groups
> Content-Type: application/scim+json
> ```
>
> ```json theme={"system"}
> {
>   "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>   "displayName": "research-team",
>   "members": [],
>   "storageBucket": {
>     "name": "wandbstorage",
>     "provider": "AZURE",
>     "path": "research/artifacts",
>     "azureTenantId": "12345678-1234-1234-1234-123456789012",
>     "azureClientId": "87654321-4321-4321-4321-210987654321"
>   }
> }
> ```

> [tab] GCP
>
> ```bash theme={"system"}
> POST /scim/Groups
> Content-Type: application/scim+json
> ```
>
> ```json theme={"system"}
> {
>   "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>   "displayName": "data-science-team",
>   "members": [
>     {
>       "value": "VXNlcjox",
>       "display": "jane.doe@example.com"
>     },
>     {
>       "value": "VXNlcjoy",
>       "display": "john.smith@example.com"
>     }
>   ],
>   "storageBucket": {
>     "name": "my-gcs-bucket",
>     "provider": "GCP",
>     "path": "data-science/runs"
>   }
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "wandb-support",
>     "id": "jkl",
>     "members": [
>         {
>             "Value": "def",
>             "Ref": "",
>             "Type": "",
>             "Display": "dev-user2"
>         }
>     ],
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:00:00Z",
>         "location": "Groups/jkl"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### Update team

Updates an existing team's membership list.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Groups/{id}`
* **Method**: `PATCH`
* **Supported operations**: `add` member, `remove` member, `replace` members.

> [!NOTE]
>
> * The remove operations follow RFC 7644 SCIM protocol specifications. Use the filter syntax `members[value eq "{user_id}"]` to remove a specific user, or `members` to remove all users from the team.
>
>   **User identification**: The `{user_id}` in member operations can be either of the following:
>
>   * A Weights & Biases user ID.
>   * An email address (for example, "[user@example.com](mailto:user@example.com)").
> * These operations work for users only, not service accounts. Update a team's service accounts in the settings for the Weights & Biases Team.

> [!NOTE]
>
> Replace `{team_id}` with the actual team ID and `{user_id}` with the actual user ID or email address in your requests.

### Replace team members

Replaces all members of a team with a new list.

> [!NOTE]
>
> This operation works for users only, not service accounts. Manage service accounts in the settings for the Weights & Biases Team.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Groups/{id}`
* **Method**: `PUT`

> [tab] Request
>
> ```bash theme={"system"}
> PUT /scim/Groups/{team_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
>     "displayName": "acme-devs",
>     "members": [
>         {
>             "value": "{user_id_1}"
>         },
>         {
>             "value": "{user_id_2}"
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "acme-devs",
>     "id": "ghi",
>     "members": [
>         {
>             "Value": "user_id_1",
>             "Ref": "",
>             "Type": "",
>             "Display": "user1"
>         },
>         {
>             "Value": "user_id_2",
>             "Ref": "",
>             "Type": "",
>             "Display": "user2"
>         }
>     ],
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:01:00Z",
>         "location": "Groups/ghi"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### Add a user to a team

Adds `dev-user2` to `acme-devs`:

> [!NOTE]
>
> This operation works for users only, not service accounts. Manage service accounts in the settings for the Weights & Biases Team.

> [tab] Request
>
> ```bash theme={"system"}
> PATCH /scim/Groups/{team_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "add",
>             "path": "members",
>             "value": [
>                 {
>                     "value": "{user_id}"
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "acme-devs",
>     "id": "ghi",
>     "members": [
>         {
>             "Value": "abc",
>             "Ref": "",
>             "Type": "",
>             "Display": "dev-user1"
>         },
>         {
>             "Value": "def",
>             "Ref": "",
>             "Type": "",
>             "Display": "dev-user2"
>         }
>     ],
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:01:00Z",
>         "location": "Groups/ghi"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### Remove a specific user from a team

Removes `dev-user2` from `acme-devs`:

> [!NOTE]
>
> This operation works for users only, not service accounts. Manage service accounts in the settings for the Weights & Biases Team.

> [tab] Request
>
> ```bash theme={"system"}
> PATCH /scim/Groups/{team_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "remove",
>             "path": "members[value eq \"{user_id}\"]"
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "acme-devs",
>     "id": "ghi",
>     "members": [
>         {
>             "Value": "abc",
>             "Display": "dev-user1"
>         }
>     ],
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:01:00Z",
>         "location": "Groups/ghi"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### Remove all users from a team

Removes all users from `acme-devs`:

> [!NOTE]
>
> This operation works for users only, not service accounts. Manage service accounts in the settings for the Weights & Biases Team.

> [tab] Request
>
> ```bash theme={"system"}
> PATCH /scim/Groups/{team_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "remove",
>             "path": "members"
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "displayName": "acme-devs",
>     "id": "ghi",
>     "members": null,
>     "meta": {
>         "resourceType": "Group",
>         "created": "2023-10-01T00:00:00Z",
>         "lastModified": "2023-10-01T00:01:00Z",
>         "location": "Groups/ghi"
>     },
>     "schemas": [
>         "urn:ietf:params:scim:schemas:core:2.0:Group"
>     ]
> }
> ```

### Delete team

The SCIM API doesn't support deleting teams because additional data is linked to teams. Delete teams from the W\&B App to confirm you want everything deleted.

## Role resource

The SCIM role resource maps to Weights & Biases custom roles. Use the endpoints in this section to create and maintain custom roles programmatically (for example, to keep role definitions in sync with your access policies). The `/Roles` endpoints aren't part of the official SCIM schema. Weights & Biases adds `/Roles` endpoints to support automated management of custom roles in organizations.

### Get custom role

Retrieve information for a custom role by providing the role's unique ID.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Roles/{id}`
* **Method**: `GET`

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> GET /scim/Roles/abc
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>     "description": "A sample custom role for example",
>     "id": "Um9sZTo3",
>     "inheritedFrom": "member", // indicates the predefined role
>     "meta": {
>         "resourceType": "Role",
>         "created": "2023-11-20T23:10:14Z",
>         "lastModified": "2023-11-20T23:31:23Z",
>         "location": "Roles/Um9sZTo3"
>     },
>     "name": "Sample custom role",
>     "organizationID": "T3JnYW5pemF0aW9uOjE0ODQ1OA==",
>     "permissions": [
>         {
>             "name": "artifact:read",
>             "isInherited": true // inherited from member predefined role
>         },
>         ...
>         ...
>         {
>             "name": "project:update",
>             "isInherited": false // custom permission added by admin
>         }
>     ],
>     "schemas": [
>         ""
>     ]
> }
> ```

### List custom roles

Retrieve information for all custom roles in the organization.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Roles`
* **Method**: `GET`

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> GET /scim/Roles
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> ```json theme={"system"}
> {
>    "Resources": [
>         {
>             "description": "A sample custom role for example",
>             "id": "Um9sZTo3",
>             "inheritedFrom": "member", // indicates the predefined role that the custom role inherits from
>             "meta": {
>                 "resourceType": "Role",
>                 "created": "2023-11-20T23:10:14Z",
>                 "lastModified": "2023-11-20T23:31:23Z",
>                 "location": "Roles/Um9sZTo3"
>             },
>             "name": "Sample custom role",
>             "organizationID": "T3JnYW5pemF0aW9uOjE0ODQ1OA==",
>             "permissions": [
>                 {
>                     "name": "artifact:read",
>                     "isInherited": true // inherited from member predefined role
>                 },
>                 ...
>                 ...
>                 {
>                     "name": "project:update",
>                     "isInherited": false // custom permission added by admin
>                 }
>             ],
>             "schemas": [
>                 ""
>             ]
>         },
>         {
>             "description": "Another sample custom role for example",
>             "id": "Um9sZToxMg==",
>             "inheritedFrom": "viewer", // indicates the predefined role that the custom role inherits from
>             "meta": {
>                 "resourceType": "Role",
>                 "created": "2023-11-21T01:07:50Z",
>                 "location": "Roles/Um9sZToxMg=="
>             },
>             "name": "Sample custom role 2",
>             "organizationID": "T3JnYW5pemF0aW9uOjE0ODQ1OA==",
>             "permissions": [
>                 {
>                     "name": "launchagent:read",
>                     "isInherited": true // inherited from viewer predefined role
>                 },
>                 ...
>                 ...
>                 {
>                     "name": "run:stop",
>                     "isInherited": false // custom permission added by admin
>                 }
>             ],
>             "schemas": [
>                 ""
>             ]
>         }
>     ],
>     "itemsPerPage": 9999,
>     "schemas": [
>         "urn:ietf:params:scim:api:messages:2.0:ListResponse"
>     ],
>     "startIndex": 1,
>     "totalResults": 2
> }
> ```

### Create custom role

Creates a new custom role in the organization.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Roles`
* **Method**: `POST`

#### Supported fields

| Field | Type | Required |
| - | - | - |
| `name` | String | Name of the custom role |
| `description` | String | Description of the custom role |
| `permissions` | Object array | Array of permission objects where each object includes a `name` string field that has value of the form `w&bobject:operation`. For example, a permission object for delete operation on W\&B runs would have `name` as `run:delete`. |
| `inheritedFrom` | String | The predefined role that the custom role inherits from. It can be either `member` or `viewer`. |

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> POST /scim/Roles
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Role"],
>     "name": "Sample custom role",
>     "description": "A sample custom role for example",
>     "permissions": [
>         {
>             "name": "project:update"
>         }
>     ],
>     "inheritedFrom": "member"
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 201)
> ```
>
> ```json theme={"system"}
> {
>     "description": "A sample custom role for example",
>     "id": "Um9sZTo3",
>     "inheritedFrom": "member", // indicates the predefined role
>     "meta": {
>         "resourceType": "Role",
>         "created": "2023-11-20T23:10:14Z",
>         "lastModified": "2023-11-20T23:31:23Z",
>         "location": "Roles/Um9sZTo3"
>     },
>     "name": "Sample custom role",
>     "organizationID": "T3JnYW5pemF0aW9uOjE0ODQ1OA==",
>     "permissions": [
>         {
>             "name": "artifact:read",
>             "isInherited": true // inherited from member predefined role
>         },
>         ...
>         ...
>         {
>             "name": "project:update",
>             "isInherited": false // custom permission added by admin
>         }
>     ],
>     "schemas": [
>         ""
>     ]
> }
> ```

### Update custom role

The following sections describe how to add or remove permissions on an existing custom role.

#### Add permissions to role

Adds permissions to an existing custom role.

##### Endpoint

* **URL**: `[HOST-URL]/scim/Roles/{id}`
* **Method**: `PATCH`

> [tab] Request
>
> ```bash theme={"system"}
> PATCH /scim/Roles/{role_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "add",
>             "path": "permissions",
>             "value": [
>                 {
>                     "name": "project:delete"
>                 },
>                 {
>                     "name": "run:stop"
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> Returns the updated role with new permissions added.

#### Remove a permission from a role

Removes permissions from an existing custom role.

##### Endpoint

* **URL**: `[HOST-URL]/scim/Roles/{id}`
* **Method**: `PATCH`

> [tab] Request
>
> ```bash theme={"system"}
> PATCH /scim/Roles/{role_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
>     "Operations": [
>         {
>             "op": "remove",
>             "path": "permissions",
>             "value": [
>                 {
>                     "name": "project:update"
>                 }
>             ]
>         }
>     ]
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> Returns the updated role with specified permissions removed.

### Replace custom role

Replaces an entire custom role definition.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Roles/{id}`
* **Method**: `PUT`

> [tab] Request
>
> ```bash theme={"system"}
> PUT /scim/Roles/{role_id}
> ```
>
> ```json theme={"system"}
> {
>     "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Role"],
>     "name": "Updated custom role",
>     "description": "Updated description for the custom role",
>     "permissions": [
>         {
>             "name": "project:read"
>         },
>         {
>             "name": "run:read"
>         },
>         {
>             "name": "artifact:read"
>         }
>     ],
>     "inheritedFrom": "viewer"
> }
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 200)
> ```
>
> Returns the replaced role definition.

### Delete custom role

Delete a custom role in the organization. **Use this operation with caution**. The predefined role that the custom role inherited from is reassigned to all users who held the custom role before the deletion.

#### Endpoint

* **URL**: `[HOST-URL]/scim/Roles/{id}`
* **Method**: `DELETE`

#### Example

> [tab] Request
>
> ```bash theme={"system"}
> DELETE /scim/Roles/abc
> ```

> [tab] Response
>
> ```text theme={"system"}
> (Status 204 No Content)
> ```

## Advanced features

The following sections describe optional capabilities (ETag-based concurrency control and standard error responses) that help SCIM integrations behave safely in production.

### ETag support

The SCIM API supports ETags for conditional updates to prevent concurrent modification conflicts. This matters when multiple admins or automated systems update the same resource, because it ensures that one update doesn't silently overwrite another. ETags are returned in the `ETag` response header and the `meta.version` field.

#### ETags

To use ETags, follow these steps:

1. **Get current ETag**: When you GET a resource, note the ETag header in the response.
2. **Conditional update**: Include the ETag in the `If-Match` header when updating.

#### Example

```text theme={"system"}
# Get user and note ETag
GET /scim/Users/abc
# Response includes: ETag: W/"xyz123"

# Update with ETag
PATCH /scim/Users/abc
If-Match: W/"xyz123"

{
    "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
    "Operations": [
        {
            "op": "replace",
            "path": "organizationRole",
            "value": "admin"
        }
    ]
}
```

A `412 Precondition Failed` error response indicates that the resource has been modified since you retrieved it.

### Error handling

The SCIM API returns standard SCIM error responses:

| Status Code | Description |
| - | - |
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful deletion) |
| `400` | Bad Request: invalid parameters or request body |
| `401` | Unauthorized: authentication failed |
| `403` | Forbidden: insufficient permissions |
| `404` | Not Found: resource doesn't exist |
| `409` | Conflict: resource already exists |
| `412` | Precondition Failed: ETag mismatch |
| `500` | Internal Server Error |

## Implementation differences per deployment type

Weights & Biases maintains two separate SCIM API implementations, and the features differ between them. Review the following table before you integrate with SCIM to confirm that the operations you rely on are available on your deployment type.

| Feature | Multi-tenant Cloud | Dedicated Cloud and Self-Managed |
| - | - | - |
| Update user email | - | ✓ |
| Update user display name | - | ✓ |
| User deactivation | ✓ | ✓ |
| User reactivation | - | ✓ |
| Multiple emails per user | ✓ | - |
| Set `modelsSeat` on create/update | ✓ | ✓ |
| Set `weaveRole` on create/update | ✓ | ✓ |
| Set `registryAccess` on create/update | ✓ | ✓ |
| Revoke Registry access with `modelsSeat: none` | - | ✓ |
| Revoke Registry access with `registryAccess: none` | ✓ | ✓ |

## Limitations

Keep the following constraints in mind when you design SCIM integrations:

* **Maximum results**: 9,999 items per request.
* **Dedicated Cloud and Self-Managed**: Only support one email per user.
* **Team deletion**: Not supported through SCIM (use the Weights & Biases web interface).
* **User reactivation**: Not supported in Multi-tenant Cloud environments.
* **Seat limits**: Operations may fail if organization seat limits are reached.
