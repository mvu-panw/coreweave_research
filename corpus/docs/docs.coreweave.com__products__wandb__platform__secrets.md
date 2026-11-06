# Manage secrets

Source: https://docs.coreweave.com/products/wandb/platform/secrets

> Store API keys and tokens as personal or team secrets, and learn how Forge features choose between them.

# Manage secrets

Secret Manager lets you securely and centrally store, manage, and inject *secrets*, which are sensitive strings such as access tokens, bearer tokens, API keys, or passwords. Forge features can read secret values by name, which removes the need to paste them or store them in code, training scripts, or plain-text automation configuration.

Forge has two kinds of secrets:

| | Personal secrets | Team secrets |
| - | - | - |
| **Who can use it** | Only you. | Everyone on the team. |
| **Scope** | You, within one organization. | One team. |
| **Who manages it** | You, in your [user settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md). Organization admins can also manage them. | Team admins, in the [team settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md). |
| **Typical use** | Your own API keys and tokens, such as a model provider key or a GitHub token. | Credentials the whole team shares, such as a webhook's access token. |

Forge has no organization-level secrets. Organization admins can list the names of members' personal secrets, but never their values, and can delete them. On Dedicated Cloud and Self-Managed, organization admins can also create members' personal secrets and replace their values. Admins manage members' secrets through the API. User settings show only your own personal secrets.

After you save a secret, neither the UI nor the API shows its value again. You can see a secret's name and when it was last updated, but not its value. To change a value, replace the secret.

## How Forge chooses between a personal and a team secret

Forge features find a secret by its name. For example, W\&B Weave Playground looks for `OPENAI_API_KEY` to call OpenAI models. To make a credential available to a feature, store it under the name that feature expects.

A personal secret and a team secret can have the same name. When a feature looks up a secret on your behalf in a team's project, it resolves the name in this order:

1. Your personal secret with that name, in the organization the team belongs to. A team belongs to exactly one organization.
2. The team secret with that name, if you don't have a personal secret with that name.

Your personal secret *shadows* a team secret with the same name for work that runs as you, including remote scorers and monitors that the team configured to use the team secret. Your teammates keep using the team secret unless they create their own personal secret. A monitor runs as the user who saved its current version. If you saved it, the monitor uses your personal secrets for every trace it scores, including your teammates' traces.

If your personal secret holds an expired or incorrect value, the feature uses it anyway and doesn't fall back to the team secret. To return to the team secret, delete your personal secret.

Weave caches resolved secret values for up to 60 seconds. After you create, replace, or delete a personal or team secret, Weave might take up to a minute to use the change.

## Where personal secrets apply

Personal secrets apply wherever a feature looks up a secret on your behalf in a team's project. This includes:

* **Weave**: Playground, the project's **AI Providers** tab, [custom runtimes](https://docs.coreweave.com/products/wandb/weave/guides/tools/custom-runtimes.md), evaluations, and scorers, including [remote scorers](https://docs.coreweave.com/products/wandb/weave/guides/evaluation/remote-scorers.md).
* **[Sandboxes on serverless capacity](https://docs.coreweave.com/products/sandboxes/secrets.md)**: The sandbox resolves secrets for the user who owns the API key that created it.

Personal secrets don't apply in these cases:

* **Webhook automations**: A webhook uses only the team secrets you select when you configure it.
* **Work without a user**: Work that runs as a service account, such as a monitor that a service account saved, has no user whose personal secrets Forge can use. Remote scorers and LLM judge scorers in such a monitor use team secrets instead. An LLM judge scorer that uses a W\&B Inference model fails in such a monitor.
* **`WANDB_API_KEY`**: Weave never resolves `WANDB_API_KEY` from a personal secret.

[ARIA](https://docs.coreweave.com/products/aria/secrets.md) works differently. It receives only the personal secrets you grant it, as environment variables in its sandbox, and never falls back to a team secret.

The following table summarizes which kind of secret each feature can use:

| Feature | Personal secrets | Team secrets |
| - | - | - |
| Weave features in a team's project | Supported | Supported |
| Sandboxes on serverless capacity | Supported | Supported |
| ARIA | Supported, after you grant ARIA access | Not supported |
| Webhook automations | Not supported | Supported |

## Availability

> [tab] Multi-tenant Cloud
>
> Personal and team secrets are available by default.
>
> You can belong to more than one organization, and your personal secrets are scoped to one organization each. A personal secret in one organization isn't available in another, and you can create personal secrets with the same name in different organizations.

> [tab] Dedicated Cloud and Self-Managed
>
> Secrets require a secret store, which the `GORILLA_CUSTOMER_SECRET_STORE_SOURCE` [environment variable](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md) configures. If the variable is unset or set to `noop://`, secret storage is turned off, and neither the **Team secrets** section nor the **Personal secrets** section appears.
>
> Starting in W\&B Server v0.86.0, personal secrets are on by default on an instance with a configured secret store.
>
> ARIA isn't available on these deployments, so personal secrets can't be granted to ARIA.
>
> In Self-Managed deployments, you are responsible for configuring security measures that satisfy your security needs.
>
> * We recommend that you store your Forge deployment's secrets in a secrets manager from AWS, Google Cloud, or Azure. These services include advanced security capabilities.
> * We recommend against using a Kubernetes cluster as the backend of your secret store. Use a cluster only if you can't use a cloud secrets manager (AWS, Google Cloud, or Azure) and you understand how to prevent the security vulnerabilities that can occur.

## Manage personal secrets

Manage your personal secrets in the **Personal secrets** section of your user settings. To open the section:

1. Click the account selector in the upper-right corner.
2. Select **User settings**.
3. Scroll to **Personal secrets**.

On Multi-tenant Cloud, the section lists your personal secrets in the organization of your current account and shows a **Scoped to the organization** label. If your current account has no organization, the section doesn't appear. To manage the personal secrets of another organization, click the account selector in the upper-right corner and select the organization under **Other accounts**. To find a secret, enter part of its name in **Search by name**.

![The Personal secrets section of user settings, scoped to the organization, with a pencil icon and a trash icon on each secret's row](https://mintcdn.com/coreweave-dbfa0e8d/qRN22DiYaBHAl6F4/products/wandb/platform/_media/personal-secrets.png?fit=max\&auto=format\&n=qRN22DiYaBHAl6F4\&q=85\&s=a70416f4749f90254c04ba24ce7647ac)

### Create a personal secret

To create a personal secret:

1. In the **Personal secrets** section, click **New secret**. If you don't have any personal secrets yet, click **Create new secret** instead.
2. Enter a **Name** for the secret, in environment variable form: letters, digits, and underscores (`_`), not starting with a digit. For example, `GITHUB_TOKEN`.

   You can't reuse the name of another of your personal secrets in the same organization. If a team secret with the same name exists, the drawer shows **A team secret with this name exists** and lists the teams, but lets you save. Your personal secret then [takes precedence](#how-forge-chooses-between-a-personal-and-a-team-secret) over the team secret for you.
3. Paste the sensitive value into the **Value** field. To check what you pasted, click **Reveal secret value**. To hide it again, click **Hide secret value**.
4. On Multi-tenant Cloud, the drawer also includes **Allow ARIA to use this secret**, which is on by default. To store the secret without granting ARIA access, turn it off.
5. Click **Save secret**.

You can also save a model provider key as a personal secret directly from the Weave Playground provider drawer or a project's **AI Providers** tab. In those drawers, **Personal** is the default. Only team admins can save a key as **Team**. A provider that you configure with a personal key is used only for work that runs as you, including monitors whose current version you saved. Your teammates need their own personal key, or a team key.

### Replace the value of a personal secret

To replace a personal secret's value, such as when you rotate a token:

1. In the secret's row, click **Edit secret** (the pencil icon).
2. Paste the **New value**. You can't change the secret's name.
3. Click **Replace secret**.

### Delete a personal secret

Deleting a personal secret is permanent, whether you delete it or an organization admin does. Features that support personal secrets fall back to a team secret with the same name, if one exists, or stop working if none does. ARIA loses access to the secret.

To delete a personal secret:

1. In the secret's row, click **Delete secret** (the trash icon).
2. In **Enter the secret name to confirm**, type the secret's name.
3. Click **Delete**.

Removing a personal key from a provider on a project's **AI Providers** tab also deletes that personal secret from your user settings in that organization, not only from the provider.

## Manage team secrets

Team secrets live in each Forge team's Secret Manager, in the **Team secrets** section of the team settings. Only team admins can create, edit, or delete a team secret, and the **Team secrets** section appears only if you have permission to edit team settings.

### Add a secret

Add a team secret when you want to make a sensitive value available to the whole team without exposing it in code or configuration. After you complete these steps, the secret is available by name to the Weave and Sandboxes features listed in [Where personal secrets apply](#where-personal-secrets-apply), and to webhook automations that you configure to use it.

To add a team secret:

1. If an external service gives you a token or API key, obtain that value through that service's normal flow. If necessary, save the sensitive string securely, such as in a password manager, before you paste it into Secret Manager. Forge doesn't reveal the secret's value after creation.
2. Sign in to Forge and go to the team's **Settings** page.
3. In the **Team secrets** section, click **New secret**.
4. Provide a name for the secret, using letters, digits, and underscores (`_`). The name must start with a letter or an underscore.
5. Paste the sensitive string into the **Value** field.
6. Click **Add secret**.

When you configure a webhook for an automation, select which team secrets the webhook may use: at most one access token and one other secret. For field names, access tokens, and payload variables, see [Create a webhook automation](https://docs.coreweave.com/products/wandb/automations/create-automations/webhook.md).

> [!NOTE]
>
> After you configure a secret in a webhook, you can access that secret in the automation's payload using the format `${SECRET_NAME}`.

### Rotate a secret

Rotate a team secret when its value changes, for example, when an upstream credential is regenerated or when you suspect the existing value has been compromised. Because Forge doesn't reveal a secret's current value after creation, rotation is also the way to replace a value you no longer have a copy of.

To rotate a team secret and update its value:

1. To open the secret's details, click the pencil icon in the secret's row.
2. Set **New value** to the new value. Optionally, click **Reveal secret value** to verify the new value.
3. Click **Replace secret**.

The secret's value updates and no longer resolves to the previous value.

Rotating or replacing a team secret can affect every feature that still expects the old value. Before you rely on the new value everywhere, update webhook automations, sandboxes that inject the secret, Weave Playground, or other consumers. Team members who have a personal secret with the same name keep using their personal secret.

### Delete a secret

Delete a team secret when no team feature uses it. Because deletion is immediate and permanent, confirm that no automations, sandboxes, Playground providers, or other consumers still reference the secret before you proceed. Deleting a team secret affects every provider that uses it.

To delete a team secret:

1. In the secret's row, click the trash icon.
2. Read the confirmation dialog, then click **Delete**.
