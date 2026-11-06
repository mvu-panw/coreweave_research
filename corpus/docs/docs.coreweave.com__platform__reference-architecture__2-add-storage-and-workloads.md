# 2. Add Node Pools and Storage

Source: https://docs.coreweave.com/platform/reference-architecture/2-add-storage-and-workloads

# 2. Add Node Pools and Storage

> Add Node Pools and DFS volumes, and optionally Object Storage, to your CoreWeave Terraform deployment

Phase 2 adds Node Pools and DFS volumes on top of the VPC and CKS cluster from [Phase 1](https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure.md). These resources are Kubernetes manifests that require a running cluster and kubeconfig.

This guide also covers the following optional configurations:

* CoreWeave AI Object Storage.
* OIDC Workload Identity Federation for Object Storage (instead of static CoreWeave API keys).

## Prerequisites

* A [CoreWeave account](https://console.coreweave.com/) with a **CoreWeave API token** ([create one in Console](https://console.coreweave.com/tokens)).
* `kubectl` (required for Node Pools and DFS volumes and optional for Object Storage).
* The kubeconfig you downloaded at the end of [Phase 1](https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure.md#download-kubeconfig).

## Node Pools and DFS volumes

Node Pools and DFS PVCs are managed as Kubernetes manifests, so Terraform needs [the kubeconfig you downloaded at the end of Phase 1](https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure.md#download-kubeconfig).

> [!NOTE]
>
> Your CoreWeave user or API token must have the **CKS Admin** IAM role. See the [prerequisites](https://docs.coreweave.com/platform/reference-architecture.md).

## Configuration

In this section, you'll set the kubeconfig path and enable Node Pools and DFS volumes.

### Set the kubeconfig path

In `terraform.tfvars`, set `cks_kubeconfig_path` to the path of the kubeconfig you downloaded at the end of Phase 1. Replace `[PATH-TO-DOWNLOADED-KUBECONFIG]` with that path:

```hcl theme={"system"}
cks_kubeconfig_path = "[PATH-TO-DOWNLOADED-KUBECONFIG]"
```

### Enable Node Pools and DFS

To enable Node Pools and DFS volumes, set the following variables in your `terraform.tfvars` file:

```hcl theme={"system"}
create_nodepool = true
create_dfs_pvc  = true
```

## Create and verify your Node Pools and DFS volumes

In this section, you'll apply your Terraform configuration to create your Node Pools and DFS volumes.

### Apply your Terraform configuration

To enable Node Pools and DFS volumes, plan and apply your changes:

```bash theme={"system"}
terraform plan
terraform apply
```

### Verify outputs

After `terraform apply` completes, verify the outputs to confirm your Node Pools and DFS volumes are in place:

```bash theme={"system"}
terraform output nodepools
terraform output dfs_pvcs
```

## Optional: Add Object Storage

The Object Storage module is an optional add-on that creates an Object Storage bucket with organization-level and optional bucket-level access policies. Object Storage resources don't require kubeconfig and can be included in either Phase 1 or Phase 2.

> [!NOTE]
>
> Your user or API token must have the **Object Storage Admin** IAM role. See the [prerequisites](https://docs.coreweave.com/platform/reference-architecture.md).

### Configure Object Storage access policies

In this section, you'll configure the Object Storage access policies for your Object Storage bucket. You need at least one organization access policy before creating buckets. Bucket access policies are optional.

The following policies are available in your `terraform.tfvars` file (copied from the `terraform.tfvars.example` file) as examples. Edit them to suit your needs.

#### Organization access policies

The `object_storage_org_access_policies` variable is a `map` (key = policy name), so you can create multiple policies for different concerns. At least one organization access policy must exist before creating buckets.

##### Open access (single policy)

A single policy granting full S3 and Object Storage API access to every principal in the organization. Suitable for development or test environments, or single-team setups where all users share the same level of access:

```hcl theme={"system"}
object_storage_org_access_policies = {
  "open-access" = {
    statements = [
      {
        name       = "allow-all-principals-full-access"
        effect     = "Allow"
        actions    = ["s3:*", "cwobject:*"]
        resources  = ["*"]
        principals = ["*"]
      }
    ]
  }
}
```

##### Scoped access (multiple policies)

Separate policies for different access patterns with named principals, least-privilege actions, independently manageable and auditable:

```hcl theme={"system"}
object_storage_org_access_policies = {
  "admin-access" = {
    statements = [
      {
        name       = "allow-admin-full-access"
        effect     = "Allow"
        actions    = ["s3:*", "cwobject:*"]
        resources  = ["*"]
        principals = ["admin@example.com", "platform-team@example.com"]
      }
    ]
  }

  "oidc-wif" = {
    statements = [
      {
        name       = "allow-oidc-key-creation"
        effect     = "Allow"
        actions    = ["cwobject:CreateAccessKeyOIDC"]
        resources  = ["*"]
        principals = ["role/https://idp.example.com:svc-data-ingest"]
      },
      {
        name       = "allow-s3-rw-training-bucket"
        effect     = "Allow"
        actions    = ["s3:GetObject", "s3:PutObject", "s3:ListBucket", "s3:DeleteObject"]
        resources  = ["training-data", "training-data/*"]
        principals = ["role/https://idp.example.com:svc-data-ingest"]
      }
    ]
  }
}
```

#### Optional: Bucket access policies

Bucket access policies control access to a single bucket. Both the requesting principal's organization access policy and the bucket access policy must allow the request. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation). Manage them with the `object_storage_bucket_policy_statements` variable. Replace `[BUCKET-NAME]` with the name of your bucket, and `[ORG-ID]` with your CoreWeave organization ID, found on the [Settings page](https://console.coreweave.com/account/settings) of your Cloud Console account.

```hcl theme={"system"}
object_storage_bucket_policy_statements = [
  {
    sid    = "allow-read-oidc-role"
    effect = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = ["arn:aws:s3:::[BUCKET-NAME]", "arn:aws:s3:::[BUCKET-NAME]/*"]
    principals = {
      "CW" = ["arn:aws:iam::[ORG-ID]:role/https://idp.example.com:svc-reader"]
    }
  }
]
```

> [!TIP]
>
> Key difference: Organization policies use short-form principals (for example, `role/https://idp.example.com:sub`), while bucket policies use full ARNs (for example, `arn:aws:iam::[ORG-ID]:role/https://idp.example.com:sub`).

### Create a bucket

To create your Object Storage bucket, follow these steps:

1. Set the bucket variables in `terraform.tfvars`:

   ```hcl theme={"system"}
   object_storage_bucket_name = "[BUCKET-NAME]"
   ```

   > [accordion] Bucket naming rules
   >
   > Bucket names must be globally unique and adhere to the following rules:
   >
   > * **Length:** 3 to 63 characters.
   > * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
   > * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
   > * **Prohibited patterns:** Cannot start with `xn--`.
   > * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

2. To create your Object Storage bucket, plan and apply your changes:

   ```bash theme={"system"}
   terraform plan
   terraform apply
   ```

3. After `terraform apply` completes, verify the outputs to confirm your Object Storage bucket is in place:

   ```bash theme={"system"}
   terraform output object_storage_bucket_name
   terraform output object_storage_org_access_policy_names
   ```

For full resource documentation, see the Terraform provider reference for [organization access policies](https://docs.coreweave.com/platform/terraform/resources/object_storage_organization_access_policy.md), [buckets](https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket.md), and [bucket policies](https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_policy.md).

## OIDC Workload Identity Federation for Object Storage

For production environments, OpenID Connect (OIDC) Workload Identity Federation (WIF) eliminates static API keys by exchanging short-lived JSON Web Tokens (JWT) from your identity provider for temporary Object Storage credentials.

CKS clusters expose an OIDC issuer URL for Kubernetes service account tokens. After [Phase 1](https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure.md#verify-outputs) completes, retrieve this URL from the Terraform output:

```bash theme={"system"}
terraform output cks_service_account_oidc_issuer_url
```

You can use this URL as the issuer when creating a WIF configuration in the Console, allowing CKS workloads to access Object Storage without static credentials. The derived role identity follows this format, where `[OIDC-ISSUER-URL]` is the URL you retrieved above, and `[NAMESPACE]` and `[SERVICE-ACCOUNT-NAME]` are the namespace and name of the Kubernetes ServiceAccount your workload runs as:

```text theme={"system"}
role/[OIDC-ISSUER-URL]:system:serviceaccount:[NAMESPACE]:[SERVICE-ACCOUNT-NAME]
```

Grant that role access in your organization access policy (see the preceding "Scoped access" example for the Terraform syntax).

> [!NOTE]
>
> Creating a WIF configuration requires the **IAM Admin** role. WIF configurations don't have a Terraform resource. Create them in [Console > Organization > IAM > Workload Federation](https://console.coreweave.com/organization/iam/workload-federation/oidc).

For the complete WIF setup walkthrough, including OIDC provider configuration, required JWT claims, environment variable setup, and troubleshooting, see [Using Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md). For background on how WIF works, see [Workload Identity Federation for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md).

## Migrate from an older repository layout

If you previously had `object_storage.tf`, `nodepool.tf`, or `dfs.tf` at the root level and are updating to the module layout, Terraform plans to destroy and recreate those resources unless you move state. After pulling the new layout, move state for these resources once:

```bash theme={"system"}
terraform state mv 'coreweave_object_storage_bucket.main[0]' \
  'module.object_storage.coreweave_object_storage_bucket.main[0]' 2>/dev/null || true

terraform state mv 'kubernetes_manifest.nodepool_example[0]' \
  'module.nodepool["example-nodepool"].kubernetes_manifest.nodepool' 2>/dev/null || true

terraform state mv 'kubernetes_manifest.dfs_pvc[0]' \
  'module.dfs["dfs-shared"].kubernetes_manifest.pvc' 2>/dev/null || true
```

Omit any line for resources not in your state. Then run `terraform plan` to confirm no changes for those resources.

## Next steps

* [Manage your CKS cluster nodes](https://docs.coreweave.com/products/cks/nodes/manage.md).
* [Create DFS volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md).
* [Configure Object Storage bucket lifecycle rules](https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_lifecycle_configuration.md).
* [Set up OIDC Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md).
