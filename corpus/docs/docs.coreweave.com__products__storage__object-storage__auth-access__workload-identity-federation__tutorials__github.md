# GitHub Actions

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/github

# GitHub Actions

> Configure GitHub Actions to access AI Object Storage with OIDC

GitHub Actions workflows can authenticate to CoreWeave AI Object Storage using [GitHub's OIDC tokens](https://docs.github.com/en/actions/concepts/security/openid-connect). This eliminates the need to store static credentials as repository secrets.

## Before you begin

Complete these setup steps before you run a workflow:

1. Create an OIDC Workload Identity Federation configuration in the Cloud Console. For GitHub-hosted runners, set **Issuer URL** to `https://token.actions.githubusercontent.com` and set **Client ID (Audience)** to `https://coreweave.com/iam` (recommended), or to another audience that matches the value your workflow requests. For the full Console workflow, see [Using Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md).
2. Create an organization access policy that grants the workflow's OIDC identity at least `cwobject:CreateAccessKeyOIDC`, plus any S3 actions the workflow needs. See [Example IAM policies](#example-iam-policies).

## Use within a workflow

The following example workflow uses the [`coreweave/actions-public/auth/caios-login`](https://github.com/coreweave/actions-public/tree/main/auth/caios-login) GitHub Action to configure AI Object Storage access as an [AWS profile](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html), then lists the buckets the workflow can access. Replace `[ORG-ID]` with your CoreWeave organization ID.

The job must grant `id-token: write` so the workflow can request a GitHub OIDC token. Without that permission, authentication fails. Because the example sets an explicit `permissions` block, it also grants `contents: read` so `actions/checkout` can run.

```yaml theme={"system"}
name: List AI Object Storage buckets

on:
  workflow_dispatch: {}

jobs:
  caios-ls:
    runs-on: ubuntu-latest
    name: List AI Object Storage buckets
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v5
      - id: login
        uses: coreweave/actions-public/auth/caios-login@v1.1.0
        with:
          region: US-EAST-04A
          org-id: [ORG-ID]

      - name: List buckets
        run: aws s3 ls
```

The action defaults the OIDC audience to `https://coreweave.com/iam`. Set the `audience` input only if your WIF configuration uses a different **Client ID (Audience)**.

## Example IAM policies

Before a GitHub Actions workflow can access AI Object Storage, you must grant the workflow's OIDC identity permission through an organization access policy. The following examples show how to allow temporary credential creation and full S3 access for all repositories in a GitHub organization, using either JSON or Terraform.

> [!WARNING]
>
> Always use the organization name with a trailing slash (`/`) in the `role/` bindings when using GitHub Actions. For example, `role/https://token.actions.githubusercontent.com:repo:octo-org/*` is safe, but `role/https://token.actions.githubusercontent.com:repo:octo-org*` is unsafe because an organization named `octo-org-hacks` could match.

> [tab] JSON
>
> ```json theme={"system"}
> {
>   "name": "allow-github-org-full-access",
>   "version": "v1alpha1",
>   "statements": [
>     {
>       "name": "admin-oidc-identity",
>       "effect": "Allow",
>       "actions": [
>         "cwobject:CreateAccessKeyOIDC",
>         "s3:*"
>       ],
>       "resources": [
>         "*"
>       ],
>       "principals": [
>         "role/https://token.actions.githubusercontent.com:repo:octo-org/*"
>       ]
>     }
>   ]
> }
> ```

> [tab] Terraform
>
> ```hcl theme={"system"}
> variable "github_org" {
>   type        = string
>   description = "The GitHub organization slug, for example octo-org"
> }
>
> resource "coreweave_object_storage_organization_access_policy" "test" {
>   name = "allow-github-org-full-access"
>   statements = [
>     {
>       name       = "admin-oidc-identity"
>       effect     = "Allow"
>       resources  = ["*"]
>       actions    = [
>         "cwobject:CreateAccessKeyOIDC",
>         "s3:*"
>       ]
>       principals = [
>         "role/https://token.actions.githubusercontent.com:repo:${var.github_org}/*"
>       ]
>     }
>   ]
> }
> ```
