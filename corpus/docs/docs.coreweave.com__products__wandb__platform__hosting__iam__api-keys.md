# Manage API keys

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/api-keys

# Manage API keys

> Find, create, and delete Forge API keys, and restrict how members of your organization create and use them.

A Forge API key authenticates a person or a service account to Weights & Biases. This page describes the kinds of API keys Weights & Biases issues, where to find and manage them, and the organization settings that restrict how members create and use them. It's intended for organization admins and team admins who govern credentials, and for members who manage their own keys.

> [!NOTE]
>
> In multi-tenant Forge, a Forge API key doesn't grant access to CoreWeave Infrastructure, and a CoreWeave API access token doesn't grant access to Forge. See [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md).

To store keys safely once you have them, see [Store and handle API keys securely](#store-and-handle-api-keys-securely).

## Types of API keys

API keys can be issued to both people and service accounts.

| Key type | Belongs to | Access |
| - | - | - |
| Personal API key | A user | Every organization the user belongs to |
| Organization API key | A user | Resources the user can access within one organization |
| [Team service account](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#team-scoped-service-accounts) key | A service account | One team |
| [Organization service account](https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts.md#organization-scoped-service-accounts) key | A service account | All teams in the organization |

An organization API key authenticates a person within one organization. An organization service account key authenticates a non-human identity used for automation.

Organization API keys are available in Multi-tenant Cloud. They aren't available in Dedicated Cloud or Self-Managed.

## Find and manage API keys

Organization admins, team admins, and members manage keys from the **API Keys** tab.

> [tab] Multi-tenant Cloud
>
> 1. Click your profile icon in the upper right, then select your organization.
> 2. Navigate to `https://forge.coreweave.com/account-settings/[ORGANIZATION]/api-keys`. Replace `[ORGANIZATION]` with your organization name.
>
>    The **API Keys** tab lists the keys you have permission to see.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. Navigate to the **Organization Dashboard**:
>    * **Dedicated Cloud**: `https://[ORG-NAME].io/org/dashboard/`. Replace `[ORG-NAME]` with your organization name.
>    * **Self-Managed**: `https://[YOUR-W&B-SERVER-IP]/org/dashboard`. Replace `[YOUR-W&B-SERVER-IP]` with your deployment's IP address.
> 2. Click the **API Keys** tab.
>
>    The tab lists the keys you have permission to see.

To find only your own personal API keys, click the account selector in the upper-right corner, then click **User settings** and scroll to **API keys**. See [User settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md#api-keys).

> [!NOTE]
>
> In Multi-tenant Cloud, users whose organization role is billing admin can't see the **API Keys** tab. In Dedicated Cloud and Self-Managed, the tab isn't restricted by billing role.

### Key visibility by role

The keys listed in the **API Keys** tab depend on your role:

| Role | Can see |
| - | - |
| Member | Their own organization API keys |
| Team admin | Their own organization API keys, and keys for service accounts in teams they administer. |
| Organization admin | All organization API keys in the organization, including organization service account keys. |
| Billing admin | In Multi-tenant Cloud, nothing. The **API Keys** tab is hidden for this role. In Dedicated Cloud and Self-Managed, the same keys as a member. |

### Read the API keys table

The table lists each key with the following columns:

* **Key name**: The descriptive name given to the key when it was created.
* **Key ID**: The first part of the key, used for identification.
* **Owner**: The user or service account that owns the key.
* **Last used**: When the key most recently authenticated a request.
* **Created on**: When the key was created.

> [!NOTE]
>
> For security, the table shows only the key ID. Weights & Biases displays the full secret key once, when you create it. If you no longer have the full secret for a key, [rotate the key](#rotate-an-api-key).

To narrow the list, type in the search field to match a key name, key ID, or owner, or click **Filters** to filter by attributes such as key type.

### Create an API key

1. Go to the **API Keys** tab.
2. Click **New key**.
3. Give the key a descriptive name.
4. Click **Create**.
5. Copy the key immediately and store it securely.

Forge API keys retain the `wandb_v1_` prefix. Copy and use the entire key, including this prefix.

> [!WARNING]
>
> W\&B shows the full API key only once, when you create it. After you close the dialog, you cannot view the full API key again. Your settings display only the key ID (the first part of the key). If you lose the full API key, you must create a new one.

In Multi-tenant Cloud, keys you create from this tab belong to the organization you're viewing. Create a separate key for each organization you work in.

### Rename an API key

Rename a key to record what uses it, which makes an unfamiliar key easier to trace later. Renaming doesn't change the key's secret and doesn't interrupt anything that uses it.

1. Find the key in the table.
2. Click the actions menu at the end of the key's row, then click **Edit**.
3. Enter a new name, then save.

### Delete API keys

Delete a key when you no longer need it, or immediately if it may have been exposed.

To delete a single key, find it in the table, click the actions menu at the end of its row, then click **Delete** and confirm.

To delete several keys at once:

1. Select the checkbox next to each key you want to delete.
2. Click **Delete**. The button shows the number of keys you selected.
3. Confirm the deletion.

> [!WARNING]
>
> Deleting a key immediately revokes access for any script or service that uses it. Update your systems to use a replacement key before you delete the old one.

### Rotate an API key

Rotate a key on a schedule that matches your security policy, and immediately if a key may have been exposed. Rotate a key rather than delete it when the workloads that use it must keep running.

Weights & Biases has no single rotate action. Because a key's full secret is shown only at creation, you rotate a key by replacing it:

1. Create a new API key. Give it a name that distinguishes it from the key you're replacing.
2. Update every script, job, and stored secret that uses the old key. For storage options, see [Store and handle API keys securely](#store-and-handle-api-keys-securely).
3. Confirm that your workloads authenticate with the new key.
4. Delete the old key.

Until you complete the last step, both keys work. This overlap is what lets you rotate without downtime, so keep it short.

> [!WARNING]
>
> If a key was exposed publicly, delete it immediately rather than waiting to update your systems. An exposed key stays valid until you delete it.

## Restrict how members use API keys

Organization admins can restrict key creation and use from the organization settings in the W\&B App. These restrictions limit which keys can reach your organization's resources and who can create new ones. The following sections describe the available restrictions, which differ by deployment type.

### Enforce organization-scoped API keys

Available in **Multi-tenant Cloud** for non-academic Enterprise organizations.

When enforced, only organization API keys and keys that belong to service accounts in the organization can reach the organization's resources. A personal API key that a member uses across several organizations no longer works against this organization, which prevents a key leaked from elsewhere from reaching your data.

> [!WARNING]
>
> Personal API keys lose read and write access to the organization as soon as you enforce this setting, and any integration that uses a personal key stops working. Notify your users before you enforce it.

To enforce organization-scoped API keys, complete the following steps:

1. Sign in as an organization admin.
2. Open your organization settings, then select **Authentication** in the left navigation.
3. Next to **Enforce organization-scoped API keys**, click **Enforce**.
4. Type your organization name to confirm, then click **Enforce Organization-Scoped API Keys**.

Weights & Biases then shows an **Enforced** label next to the setting. To stop enforcing it, return to **Authentication** and click **Disable**.

### Disable API key creation

Available in **Dedicated Cloud** and **Self-Managed** v0.84.0 and above.

When enabled, users and team service accounts can't create new API keys. Organization service accounts can still create keys, and existing keys keep working, so turning this on doesn't interrupt running jobs. Use it when your organization issues keys through a controlled process and you want to prevent members from creating their own.

To disable API key creation, complete the following steps:

1. Sign in as an organization admin.
2. Open your organization dashboard, then select **Privacy** in the left navigation.
3. In the **Access Control** section, turn on **Disable API key creation**.

Weights & Biases saves the change immediately. For the other settings on this tab, see [Configure privacy settings](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#enforce-privacy-settings-for-all-teams).

While the setting is on, the **API Keys** tab disables the **New key** button and shows the following message:

```text theme={"system"}
API key creation has been disabled by your organization administrator. You can still edit, delete, and use existing API keys.
```

To restrict service account creation as well, see [`GORILLA_DISABLE_TEAM_SERVICE_ACCOUNT_CREATION`](https://docs.coreweave.com/products/wandb/platform/hosting/iam/advanced_env_vars), which prevents the creation of new team-scoped service accounts in Dedicated Cloud and Self-Managed v0.83.0 and above.

## Availability

API key capabilities differ by deployment type and, in Multi-tenant Cloud, by subscription. The following table summarizes where each capability is available.

| Capability | Multi-tenant Cloud | Dedicated Cloud | Self-Managed |
| - | - | - | - |
| Search and filter the API keys table | Yes | v0.84.0+ | v0.84.0+ |
| Create a key from the **API Keys** tab | Yes | v0.84.0+ | v0.84.0+ |
| Delete several keys at once | Yes | v0.84.0+ | v0.84.0+ |
| Disable API key creation | Not available | v0.84.0+ | v0.84.0+ |

## Store and handle API keys securely

API keys provide access to your W\&B account and should be protected like passwords. The following sections describe recommended storage methods, practices to avoid, how to pass keys to your code, and SDK version requirements for newer keys.

### Recommended storage methods

Use one of the following methods to store your API key securely.

* **Secrets manager**: Use a dedicated secrets management system such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), [HashiCorp Vault](https://developer.hashicorp.com/vault), [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault), or [Google Secret Manager](https://cloud.google.com/security/products/secret-manager).
* **Password manager**: Use a reputable password manager application.
* **OS-level keychains**: Store keys in macOS Keychain, Windows Credential Manager, or Linux secret service. Not suggested for production.

### What to avoid

Avoid the following practices, which can expose your API key:

* Never commit API keys to version control systems such as Git.
* Don't store API keys in plain text configuration files.
* Don't pass API keys on the command line, because they're visible in the output of OS commands like `ps`.
* Avoid sharing API keys through email, chat, or other unencrypted channels.
* Don't hard-code API keys in your source code.

If an API key is exposed, delete the API key from your W\&B account immediately and contact [support](mailto:forge-support@coreweave.com) or your AISE.

### Environment variables

When you use API keys in your code, pass them through environment variables:

```bash theme={"system"}
export WANDB_API_KEY="[YOUR-API-KEY]"
```

This approach keeps keys out of your source code and makes it easier to rotate them when needed.

> [!WARNING]
>
> Avoid setting the environment variable in line with the command, because it's visible in the output of OS commands like `ps`:
>
> ```bash theme={"system"}
> # Avoid this pattern, which can expose the API key in process managers
> export WANDB_API_KEY="[YOUR-API-KEY]" ./my-script.sh
> ```

### SDK version compatibility

If you use a newer API key, confirm that your SDK version supports it. Newer API keys are longer than legacy keys. When you authenticate with older versions of the `wandb` or `weave` SDKs, you may encounter an API key length error.

**Solution**: Update to a newer SDK version:

* `wandb` SDK v0.22.3+

  ```bash theme={"system"}
  pip install --upgrade wandb==0.22.3
  ```
* `weave` SDK v0.52.17+

  ```bash theme={"system"}
  pip install --upgrade weave==0.52.17
  ```

If you can't upgrade the SDK immediately, set the API key using the `WANDB_API_KEY` environment variable as a workaround.
