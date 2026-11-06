# Secrets in ARIA

Source: https://docs.coreweave.com/products/aria/secrets

# Secrets in ARIA

> Store personal secrets, such as API tokens, and let ARIA use them as environment variables in its sandbox.

> [!NOTE]
>
> Available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud).

*Personal secrets* store sensitive values, such as API tokens, that are private to you. When you grant ARIA access to a personal secret, the secret becomes an environment variable in the sandbox where ARIA runs code, so ARIA can authenticate to an outside service on your behalf. For example, you can store a GitHub personal access token and let ARIA read your repositories, commit to a branch, or open a pull request. See [Connect a GitHub repository](#connect-a-github-repository).

Personal secrets are scoped to you and to one organization: If you store your GitHub token as a personal secret, other members of your team can't use it. ARIA can use only your personal secrets, not team secrets. To learn how personal and team secrets differ and which other features use them, see [Manage secrets](https://docs.coreweave.com/products/wandb/platform/secrets.md).

## How ARIA uses a granted secret

When you grant ARIA access to a personal secret, ARIA's sandbox receives an environment variable named exactly as the secret, starting with the next message you send in a conversation. You don't need to start a new chat. Revoking access works the same way: the variable is gone from the sandbox starting with your next message.

Keep in mind:

* The secret's value is redacted from the sandbox output that appears in the chat.
* A granted secret can't replace a managed environment variable, such as `WANDB_API_KEY`. A secret whose name collides with a managed variable, or isn't a valid environment variable name, is skipped and doesn't reach the sandbox.
* ARIA can use only the personal secrets you grant, in the organization the conversation belongs to. It doesn't fall back to a team secret with the same name.

> [!WARNING]
>
> A granted secret is available to any code ARIA runs in its sandbox on your behalf. The credential's permissions set what ARIA can do with it: a GitHub token with read access lets ARIA read code and results, and one with write and pull request permissions also lets it commit changes and open pull requests.

## Create a personal secret for ARIA

Create the secret in the **Personal secrets** section of your user settings. For the full steps, see [Create a personal secret](https://docs.coreweave.com/products/wandb/platform/secrets.md#create-a-personal-secret). The **Allow ARIA to use this secret** switch in the drawer is on by default, so ARIA can use the secret as soon as you save it. To store the secret without granting ARIA access, turn the switch off.

![The Create new secret drawer, with Name, Value, and the Allow ARIA to use this secret toggle](https://mintcdn.com/coreweave-dbfa0e8d/wtrJ2D-kpZzEJkTy/products/aria/_media/aria-secrets-new-secret-drawer.png?fit=max\&auto=format\&n=wtrJ2D-kpZzEJkTy\&q=85\&s=5e4561e5ce0a68dcfeedaed7f2970b1a)

## Grant or revoke ARIA's access

You can change which of your personal secrets ARIA can use at any time, from your user settings or from the ARIA panel. Either way, the change takes effect with your next message in a conversation.

### From your user settings

In the **Personal secrets** section of your user settings, each secret's row includes an **ARIA access** switch. Turn it on to grant ARIA access to that secret, or off to revoke it.

![The Personal secrets section of user settings, with an ARIA access switch on each secret's row](https://mintcdn.com/coreweave-dbfa0e8d/wtrJ2D-kpZzEJkTy/products/aria/_media/aria-secrets-personal-secrets.png?fit=max\&auto=format\&n=wtrJ2D-kpZzEJkTy\&q=85\&s=8d7c9a1e2b378aa129380fdd81b3b2f5)

### From the ARIA panel

1. In the ARIA chat window, open the chat history sidebar if it's hidden: click **** (**Reveal chat history**).
2. In the **Customize** section, click **Secrets**. The pane lists your personal secrets in the current organization, and the summary shows how many are available to ARIA.
3. Turn a secret's switch on to grant ARIA access, or off to revoke it.

To create and manage the secrets themselves, click **** (**Manage personal secrets in settings**) at the top of the pane to open the **Personal secrets** section of your user settings.

![The ARIA Secrets pane, showing 2 of 3 secrets available to ARIA and a switch for each secret](https://mintcdn.com/coreweave-dbfa0e8d/wtrJ2D-kpZzEJkTy/products/aria/_media/aria-secrets-customize-pane.png?fit=max\&auto=format\&n=wtrJ2D-kpZzEJkTy\&q=85\&s=bcc4f9799ae1d22dcf079b197a89b640)

## Connect a GitHub repository

The most common use for secrets in ARIA is connecting GitHub. With a GitHub personal access token stored as a personal secret, ARIA can read code from your repositories and, when the token allows it, commit to a branch and open pull requests. Nothing is installed or authorized on GitHub's side beyond the token, so what ARIA can do is decided by the token you create.

To get started, click the **Connect my GitHub repo** suggestion chip in the chat window, or send `/connect-github`. The chip appears on most pages, such as a project's workspace, but not in the standalone ARIA view. ARIA asks which repository you want to connect and whether it should be able to write to it, then walks you through the following steps.

![ARIA's suggestion chips, including Connect my GitHub repo](https://mintcdn.com/coreweave-dbfa0e8d/wtrJ2D-kpZzEJkTy/products/aria/_media/aria-secrets-connect-github-chip.png?fit=max\&auto=format\&n=wtrJ2D-kpZzEJkTy\&q=85\&s=ababbe153859c039cedb598ee1c1197e)

### 1. Create a GitHub personal access token

In GitHub, go to **Settings** > **Developer settings** > **Personal access tokens** and create a token:

* **Fine-grained token** (recommended): Set the resource owner to your account or to the organization that owns the repository, limit **Repository access** to the repositories you want to connect, and set **Repository permissions** based on what ARIA should do: **Contents** Read-only for reading, or Read and write for committing, and **Pull requests** Read and write for opening pull requests. GitHub adds read-only **Metadata** access automatically. An organization owner might need to approve the token before it works.
* **Classic token**: The `repo` scope covers reading, committing, branches, and pull requests on private repositories; `public_repo` covers public ones. In an organization that uses SAML SSO, also authorize the token for that organization with **Configure SSO**.

GitHub shows the token's value once, at creation time, so copy it before you leave the page.

### 2. Save the token as a personal secret and grant ARIA access

Follow the steps in [Create a personal secret for ARIA](#create-a-personal-secret-for-aria) to store the token. Name it `GITHUB_TOKEN`, the conventional name, or any valid environment variable name, and make sure ARIA's access to it is turned on.

The token arrives in ARIA's sandbox as an environment variable with the name you chose, starting with your next message.

### 3. Approve network access to GitHub

By default, the sandbox where ARIA runs code can reach Weights & Biases services but blocks most other domains, so reaching GitHub also requires a network access grant. When ARIA needs to reach GitHub, it asks in the chat for access to the domains the task needs, explains why, and waits for your answer: `api.github.com` for GitHub API calls, and `github.com` to clone or push. Click **Grant access** to approve, or **Deny** to decline. A grant applies for the rest of the current chat session, not just the message that prompted it, and it doesn't carry over to your other chats. See [Grant network access](https://docs.coreweave.com/products/aria/chat.md#grant-network-access).

![ARIA requesting network access to api.github.com, with Deny and Grant access buttons](https://mintcdn.com/coreweave-dbfa0e8d/wtrJ2D-kpZzEJkTy/products/aria/_media/aria-secrets-network-access.png?fit=max\&auto=format\&n=wtrJ2D-kpZzEJkTy\&q=85\&s=4406a25305c421eb133b8a3d3892f748)

### What ARIA can do once connected

With the token granted and network access approved, ask ARIA to work with the repository in plain language. Depending on the token's permissions, ARIA can:

* Read and analyze code, such as cloning a repository or fetching specific files.
* Commit changes to a branch and push them.
* Open a pull request with its changes.

For example, after connecting a repository you might ask:

```text title="User prompt" theme={"system"}
Clone my-org/training-scripts, add validation metrics to train.py, and open a pull request.
```

### Troubleshoot the connection

If a GitHub request fails, ARIA reports the error from GitHub and suggests a fix. Common causes:

* **`401 Bad credentials`**: GitHub rejected the token. It might be mistyped, expired, or revoked. Create a new token, update the secret's value in **Personal secrets**, and send your request again.
* **`404 Not Found` for a repository you know exists**: GitHub returns 404, not 403, when a token can't see a private repository. Check that the token can reach it:
  * For a fine-grained token, the resource owner is the account or organization that owns the repository, the repository is included under **Repository access**, and an organization owner has approved the token if the organization requires approval.
  * For a classic token, it has the `repo` scope and, in an organization that uses SAML SSO, is authorized for that organization.
* **`403 Forbidden` when committing or opening a pull request**: The token can read the repository but lacks write permission. Grant **Contents** Read and write, and **Pull requests** Read and write, or use a classic token with the `repo` scope.
* **ARIA says the secret isn't set**: Turn on the secret's **ARIA access** switch, then send another message. A secret granted after your last message isn't visible to ARIA until your next one.
