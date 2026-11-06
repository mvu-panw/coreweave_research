# Use service accounts to automate workflows

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/service-accounts

> Manage automated or non-interactive workflows using org and team scoped service accounts

# Use service accounts to automate workflows

A service account represents a non-human or machine user that can automatically perform common tasks across projects within a team or across teams. Service accounts are ideal for CI/CD pipelines, automated training jobs, and other machine-to-machine workflows.

This page explains the scopes available for service accounts, walks through how to create and manage them, and outlines best practices for using them safely in production automation. It's intended for organization and team admins who provision credentials for automated systems.

> [!NOTE]
>
> In multi-tenant Forge, service accounts and their API keys grant access only within Forge. They don't grant access to CoreWeave Infrastructure. See [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md).

## Key benefits

Key benefits of service accounts:

* **No license consumption**: Service accounts don't consume user seats or licenses.
* **Dedicated API keys**: Secure credentials for automated workflows.
* **User attribution**: Optionally attribute automated runs to human users.
* **Enterprise-ready**: Built for production automation at scale.
* **Delegated operations**: Service accounts operate on behalf of the user or organization that creates them.

## Overview

Service accounts provide a secure way to automate Weights & Biases workflows without using personal user credentials or hardcoded credentials. You can create them at two scopes:

* **Organization-scoped**: Created by org admins, with access across all teams.
* **Team-scoped**: Created by team admins, with access limited to a specific team.

> [!NOTE]
>
> An organization-scoped service account is not the same as an [organization API key](https://docs.coreweave.com/products/wandb/platform/hosting/iam/api-keys.md#types-of-api-keys). A service account is a non-human identity that holds its own keys. An organization API key belongs to a person and authenticates that person within a single organization.

A service account's API key lets the caller read from or write to projects within the service account's scope. This enables centralized management of automated workflows for experiment tracking in Weights & Biases or logging traces in W\&B Weave.

Service accounts are useful for:

* **CI/CD pipelines**: Automatically log model training runs from GitHub Actions, GitLab CI, or Jenkins.
* **Scheduled jobs**: Nightly model retraining, periodic evaluation runs, or data validation workflows.
* **Production monitoring**: Log inference metrics and model performance from production systems.
* **Jupyter notebooks**: Shared notebooks in JupyterHub or Google Colab environments.
* **Kubernetes jobs**: Automated workflows running in Kubernetes clusters.
* **Airflow/Prefect/Dagster**: ML pipeline orchestration tools.

> [!NOTE]
>
> Service accounts are available on [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), [Self-Managed instances](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) with an enterprise license, and enterprise accounts in [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md).

## Organization-scoped service accounts

Use an organization-scoped service account when your automation needs to read or write across projects in multiple teams. Service accounts scoped to an organization have permissions to read and write in all projects in the organization, regardless of the team, with the exception of [restricted projects](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects.md#visibility-scopes). Before an organization-scoped service account can access a restricted project, an admin of that project must explicitly add the service account to the project.

### Create an organization-scoped service account

To create a new organization-scoped service account and API key:

1. Log in to W\&B.
2. Click your user profile icon, then go to **Service Accounts**:
   * **Dedicated Cloud** or **Self-Managed**: Click **Organization Dashboard**, then click **Service Accounts**.
   * **Multi-tenant Cloud**: Click **Service Accounts**.
3. Click **Create service account**.
4. Provide a name and select a default team.
5. Click **Create**.
6. Find the service account you just created, then click the **action ()** menu and click **Create API key**.
7. Provide a name for the API key, then click **Create**.
8. Copy the API key and store it securely.
9. Click **Done**.

> [!WARNING]
>
> W\&B shows the full API key only once, when you create it. After you close the dialog, you cannot view the full API key again. Your settings display only the key ID (the first part of the key). If you lose the full API key, you must create a new one.

> [!NOTE]
>
> An organization-scoped service account requires a default team, even though it has access to non-restricted projects owned by all teams within the organization. This helps to prevent a workload from failing if the `WANDB_ENTITY` variable isn't set in the environment for your model training or generative AI app. To use an organization-scoped service account for a project in a different team, you must set the `WANDB_ENTITY` environment variable to that team.

## Team-scoped service accounts

Use a team-scoped service account when you want to limit automation to a single team's projects, following the principle of least privilege. A team-scoped service account can read and write in all projects within its team, except to [restricted projects](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects.md#visibility-scopes) in that team. Before a team-scoped service account can access a restricted project, an admin of that project must explicitly add the service account to the project.

> [!NOTE]
>
> On [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) and [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) v0.83.0+, admins can prevent the creation of team-scoped service accounts by setting the `GORILLA_DISABLE_TEAM_SERVICE_ACCOUNT_CREATION` environment variable to `true` on the instance. See [Advanced IAM configuration](https://docs.coreweave.com/products/wandb/platform/hosting/iam/advanced_env_vars.md).

### Create a team-scoped service account

To create a new team-scoped service account and API key:

1. In your team's settings, click **Service Accounts**.
2. Click **New Team Service Account**.
3. Provide a name for the service account.
4. Set **Authentication Method** to **Generate API key** (default). If you select **Federated Identity**, the service account can't own API keys.
5. Click **Create**.
6. Find the service account you created, then click its **action ()** menu and click **Create API key**.
7. Provide a name for the API key, then click **Create**.
8. Copy the API key and store it securely.
9. Click **Done**.

> [!WARNING]
>
> W\&B shows the full API key only once, when you create it. After you close the dialog, you cannot view the full API key again. Your settings display only the key ID (the first part of the key). If you lose the full API key, you must create a new one.

### Create additional API keys for a service account

To create an API key owned by a service account:

1. In your team or organization settings, go to the **Service Accounts** tab.
2. Find the service account in the list.
3. Click the **action ()** menu, then click **Create API key**.
4. Provide a name for the API key, then click **Create**.
5. Copy the displayed API key immediately and store it securely.
6. Click **Done**.

You can create multiple API keys for a single service account to support different environments or workflows.

> [!WARNING]
>
> W\&B shows the full API key only once, when you create it. After you close the dialog, you cannot view the full API key again. Your settings display only the key ID (the first part of the key). If you lose the full API key, you must create a new one.

### Delete a service account API key

To delete an API key owned by an organization or team service account:

1. Go to [Organization settings](https://forge.coreweave.com/account-settings/), then click **API Keys**.
2. Find the API key. The list includes all API keys owned by organization and team service accounts. You can search or filter by key name or ID, and sort by any column.
3. Click the delete button.

If you don't configure a team in your model training or generative AI app environment that uses a team-scoped service account, the model runs or weave traces log to the named project within the service account's parent team. In such a scenario, user attribution using the `WANDB_USERNAME` or `WANDB_USER_EMAIL` variables *doesn't work* unless the referenced user is part of the service account's parent team.

> [!WARNING]
>
> A team-scoped service account can't log runs to a [team or restricted-scoped project](https://docs.coreweave.com/products/wandb/platform/hosting/iam/access-management/restricted-projects.md#visibility-scopes) in a team different from its parent team, but it can log runs to an open visibility project within another team.

### External service accounts

If you'd prefer to issue credentials through your own identity provider instead of managing Weights & Biases-native API keys, use external service accounts. In addition to built-in service accounts, Weights & Biases also supports team-scoped external service accounts with the W\&B SDK and CLI using [Identity federation](https://docs.coreweave.com/products/wandb/platform/hosting/iam/identity_federation.md#external-service-accounts) with identity providers (IdPs) that issue JSON Web Tokens (JWTs).

## Best practices

After you create the service accounts you need, follow these recommendations to ensure secure and efficient use of service accounts in your organization:

* **Use a secrets manager**: Store service account API keys in a secure secrets management system (for example, AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) rather than in plain text configuration files.

* **Principle of least privilege**: Create team-scoped service accounts when possible, rather than organization-scoped accounts, to limit access to only necessary projects.

* **Unique service accounts per use case**: Create separate service accounts for different automation workflows (for example, one for CI/CD, another for scheduled retraining) to improve auditability and enable granular access control.

* **Regular audits**: Periodically review active service accounts and remove those no longer in use. Check the audit logs to monitor service account activity.

* **Secure API key handling**:
  * Never commit API keys to version control.
  * Use environment variables to pass keys to applications.
  * Rotate keys if they're accidentally exposed.

* **Naming conventions**: Use descriptive names that indicate the service account's purpose:
  * Good: `ci-model-training`, `nightly-eval-pipeline`, `prod-inference-monitor`
  * Avoid: `service-account-1`, `test-sa`, `temp`

* **User attribution**: When multiple team members use the same automation workflow, set `WANDB_USERNAME` or `WANDB_USER_EMAIL` to track who triggered each run:
  ```bash theme={"system"}
  export WANDB_API_KEY="[SERVICE_ACCOUNT_KEY]"
  export WANDB_USERNAME="john.doe@company.com"
  ```

* **Environment configuration**: For team-scoped service accounts, always set the `WANDB_ENTITY` to ensure runs log to the correct team:
  ```bash theme={"system"}
  export WANDB_ENTITY="ml-team"
  export WANDB_PROJECT="production-models"
  ```

* **Error handling**: Implement proper error handling and alerts for failed authentication to identify issues with service account credentials quickly.

* **Documentation**: Maintain documentation of:
  * Which service accounts exist and their purposes.
  * Which systems or workflows use each service account.
  * Contact information for the team responsible for each account.

## Troubleshooting

If a service account isn't behaving as expected, check the following common issues and solutions:

* **"Unauthorized" errors**: Verify the API key is correctly set and the service account has access to the target project.
* **Runs not appearing**: Check that `WANDB_ENTITY` is set to the correct team name.
* **User attribution not working**: Ensure the user specified in `WANDB_USERNAME` is a member of the team.
* **Access denied to restricted projects**: Explicitly add the service account to the restricted project's access list.
