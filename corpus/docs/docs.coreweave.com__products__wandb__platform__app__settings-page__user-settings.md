# Manage user settings

Source: https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings

> Manage your profile information, account defaults, alerts, participation in public preview features, account activation, and create teams in your user settings.

# Manage user settings

Your user settings let you manage your profile, default team, API keys, alerts, integrations, and other account-level options. This page describes each section of the user settings and how to use it.

To open your user settings, click the account selector in the upper-right corner, then select **User settings**.

## Profile

In the **Profile** section, you can manage and modify your account name and institution. You can optionally add a biography, location, link to a personal or your institution's website, and upload a profile image.

### Edit your intro

Your intro appears at the top of your profile and is a good place to introduce yourself, link to projects, or share related accounts.

To edit your intro, click **Edit** at the top of your profile. The WYSIWYG editor that opens supports Markdown.

1. To edit a line, click it. To save time, type `/` and choose Markdown from the list.
2. To move an item, use its drag handles.
3. To delete a block, click the drag handle, then click **Delete**.
4. To save your changes, click **Save**.

Your updated intro is now visible on your profile.

#### Add social badges

To add a follow badge for the `@weights_biases` account on X, add a Markdown-style link with an HTML `<img>` tag that points to the badge image:

```markdown theme={"system"}
[![X: @weights_biases](https://img.shields.io/twitter/follow/weights_biases?style=social)](https://x.com/intent/follow?screen_name=weights_biases)
```

In an `<img>` tag, you can specify `width`, `height`, or both. If you specify only one, the image keeps its proportions.

## Default team

If you're a member of more than one team, the **Default team** section lets you configure the default team to use when a run or a Weave trace doesn't specify a team. If you're a member of only one team, that team is the default and this section doesn't appear.

The steps to set your default team differ depending on your deployment. Select the tab that matches your environment.

> [tab] Multi-tenant Cloud
>
> Next to **Default location to create new projects in**, click the dropdown, then select your default team.

> [tab] Dedicated Cloud and Self-Managed
>
> 1. Next to **Default location to create new projects in**, click the dropdown, then select your default team or your personal entity.
> 2. **Optional:** If an admin has turned on public projects in **Account** > **Settings** > **Privacy**, configure the default visibility for your new projects. Click the button next to **Default project privacy in your personal account**, then select **Private** (the default) or **Public**.
> 3. **Optional:** If an admin has turned on [default saving and diffing code](https://docs.coreweave.com/products/wandb/app/features/panels/code.md) in **Account** > **Settings** > **Privacy**, click **Enable code saving in your personal account** to turn it on for your runs.

> [!NOTE]
>
> To specify the default team when you're running a script in an automated environment, specify the default location with the `WANDB_ENTITY` [environment variable](https://docs.coreweave.com/products/wandb/track/environment-variables.md).

## Teams

The **Teams** section lists all of your teams.

* Click a team name to go to the team page.
* If you have permission to join additional teams, click **View teams** next to **We found teams for you to join**.
* **Optional:** Turn on **Hide teams in public profile**.

> [!NOTE]
>
> To create or manage a team, see [Manage teams](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md).

## API keys

The **Personal API keys** section lets you manage your personal API keys for authenticating with Weights & Biases services. From this section, you can review existing keys, create new ones, and revoke keys you no longer need.

> [!NOTE]
>
> This section shows only your personal API keys. To see every key you can manage in your organization, including organization API keys and service account keys, use the **API Keys** tab described in [Manage API keys](https://docs.coreweave.com/products/wandb/platform/hosting/iam/api-keys.md).

### View your API keys

The API keys table displays:

* **Key ID**: The first part of each API key, used for identification.
* **Name**: An optional descriptive name for the key.
* **Created**: When the key was created.
* **Last used**: The most recent usage timestamp.

> [!NOTE]
>
> For security, the table shows only the key ID (the first part of the key). The full secret API key appears only once, when you create it.

To filter the list of API keys, enter a partial key name or ID.

### Create a new API key

To create an API key, select the **Personal API key** or **Service Account API key** tab for details.

> [tab] Personal API key
>
> To create a personal API key owned by your user ID:
>
> 1. Log in to Forge, click the account selector in the upper-right corner, then select **User settings**.
> 2. Within **API keys**, select **New key**.
> 3. Provide a descriptive name for your API key.
> 4. Click **Create API key**.
> 5. Copy the displayed API key immediately and store it securely.

> [tab] Service account API key
>
> To create an API key owned by a service account:
>
> 1. In your team or organization settings, go to the **Service Accounts** tab.
> 2. Find the service account in the list.
> 3. Click the **action ()** menu, then click **Create API key**.
> 4. Provide a name for the API key, then click **Create**.
> 5. Copy the displayed API key immediately and store it securely.
> 6. Click **Done**.
>
> You can create multiple API keys for a single service account to support different environments or workflows.

> [!WARNING]
>
> W\&B shows the full API key only once, when you create it. After you close the dialog, you cannot view the full API key again. Your settings display only the key ID (the first part of the key). If you lose the full API key, you must create a new one.

For secure storage options, see [Store API keys securely](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md#store-and-handle-api-keys-securely).

### Rename an API key

To change an API key's display name without modifying the key material:

1. Find the key you want to delete in the API keys table.
2. Click the **action ()** menu and choose **Edit**.
3. Update the key's **Name**, then click **Save**.

### Delete an API key

Delete an API key when you no longer need it or when it may have been exposed. To revoke access by deleting an API key:

1. Find the key you want to delete in the API keys table.
2. Click the **action ()** menu and choose **Delete**.
3. Confirm the deletion.

Weights & Biases removes the key from the table, and you can no longer use it to authenticate.

> [!WARNING]
>
> Deleting an API key immediately revokes access for any scripts or services that use that key. Before you delete the old key, make sure you've updated all systems to use a new key.

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

## Personal secrets

The **Personal secrets** section lets you store API keys and tokens that only you can use, such as a model provider key or a GitHub token. Supported features, such as Weave Playground and sandboxes on serverless capacity, use your personal secret before a team secret with the same name. On Multi-tenant Cloud, personal secrets are scoped to the organization of your current account. To switch organizations, click the account selector in the upper-right corner and select the organization under **Other accounts**.

To create, replace, or delete a personal secret, see [Manage personal secrets](https://docs.coreweave.com/products/wandb/platform/secrets.md#manage-personal-secrets).

## Public preview features

In the **Public preview features** section, you can optionally enable add-ons and previews of products in development. Select the toggle switch next to the feature you want to enable. This section also contains **UI Display**, where you choose **Light mode**, **Dark mode**, or **System**.

## Alerts

> [!NOTE]
>
> Available only to organizations on a paid plan.

Get notified when your runs crash or finish, or set custom alerts with [`wandb.Run.alert()`](https://docs.coreweave.com/products/wandb/runs/alert). You receive notifications through email or Slack. Toggle the switch next to the event type you want to receive alerts for:

* **Run finished**: Notify you when a W\&B run successfully finishes.
* **Run crashed after**: Notify you when a run stops responding for longer than the number of minutes you set.

For more information about how to set up and manage alerts, see [Send alerts with `wandb.Run.alert()`](https://docs.coreweave.com/products/wandb/runs/alert).

## Delete your account

Select the **Delete Account** button to delete your account.

> [!WARNING]
>
> You can't reverse account deletion.

> [!NOTE]
>
> You can't delete a user account that is the **Billing admin** for an organization that has more than one member. Before deleting such an account, transfer the Billing admin role to another user from the [Billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md#billing-admin) page. If you are the organization's only member, deleting your account also deletes the organization.

To delete an entire organization account rather than a user account, see [How do I delete my organization account?](https://docs.coreweave.com/support/models/articles/how-do-i-delete-my-organization-account).
