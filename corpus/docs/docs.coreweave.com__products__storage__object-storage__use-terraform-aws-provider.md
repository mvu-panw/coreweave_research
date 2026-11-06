# Manage AI Object Storage with Terraform

Source: https://docs.coreweave.com/products/storage/object-storage/use-terraform-aws-provider

# Manage AI Object Storage with Terraform

> Use Terraform to manage CoreWeave AI Object Storage infrastructure as code

[Terraform providers](https://developer.hashicorp.com/terraform/language/providers) are plugins that let Terraform manage infrastructure resources across different platforms.

You can use Terraform to manage access policies and configure bucket lifecycles and versioning. Because CoreWeave AI Object Storage is S3-compatible, you can manage it with either the [CoreWeave Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs) or [the official Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). Both providers translate Terraform's declarative syntax into S3-compatible API calls.

To manage data and objects, you can use any S3-compatible tool. See [How-To: Manage Objects](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) to learn how to use CoreWeave AI Object Storage with `s3cmd`, Boto3, or the AWS CLI.

## Configure Terraform

These examples show how to set up the Terraform provider with CoreWeave AI Object Storage.

> [!NOTE]
>
> **Endpoint selection**
>
> Choose an endpoint based on where Terraform runs:
>
> * Use the LOTA endpoint, `http://cwlota.com`, when Terraform runs inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for lower-latency access.
> * Use the primary endpoint, `https://cwobject.com`, when Terraform runs outside of a CoreWeave cluster.

The AWS provider example configuration includes the required overrides for compatibility with CoreWeave AI Object Storage, while the native CoreWeave provider example configuration doesn't require these overrides.

> [tab] CoreWeave Provider
>
> ```hcl lines theme={"system"}
> terraform {
>   required_providers {
>     coreweave = {
>       source  = "coreweave/coreweave"
>       version = ">= 0.3.0"
>     }
>   }
>   required_version = ">= 1.2.0"
> }
>
> provider "coreweave" {
>   token = env.COREWEAVE_API_TOKEN
>   s3_endpoint = env.COREWEAVE_S3_ENDPOINT # If using LOTA, set to http://cwlota.com
> }
>
> ```
>
> Some aspects to note in this example:
>
> * `token` is set as an environment variable for security. Get your [API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md) from the [CoreWeave Access Tokens page in Cloud Console](https://console.coreweave.com/tokens).
> * `s3_endpoint` defaults to `https://cwobject.com`, which is the primary CoreWeave AI Object Storage endpoint. To use LOTA, set this value to `http://cwlota.com`.
> * `version` is set to `>= 0.3.0` because `0.3.0` is the first version to support AI Object Storage.

> [tab] AWS Provider
>
> ```hcl lines highlight={18-19,22-23,31-32} theme={"system"}
> terraform {
>   required_providers {
>     aws = {
>       source  = "hashicorp/aws"
>       version = "5.67.0"
>     }
>   }
>
>   required_version = ">= 1.2.0"
> }
>
> provider "aws" {
>   access_key = env.AWS_ACCESS_KEY
>   secret_key = env.AWS_ACCESS_SECRET
>   region     = local.region
>
>   # These two values must be true so Terraform doesn't attempt STS authentication.
>   skip_credentials_validation = true
>   skip_requesting_account_id  = true
>
>   # CoreWeave uses different region names, so validation must be skipped.
>   skip_region_validation      = true
>   s3_use_path_style           = false
>
>   endpoints {
>     s3 = local.endpoint
>   }
> }
>
> locals {
>     region   = "US-EAST-03A"
>     endpoint = "https://cwobject.com"
> }
>
> ```
>
> Some aspects to note in this example, highlighted in the preceding configuration:
>
> * `access_key` and `secret_key` are set as environment variables for security.
> * `skip_credentials_validation`, `skip_requesting_account_id`, and `skip_region_validation`
>   options are set to `true` to bypass AWS-specific validation checks.
> * In this example, `region` is set to `US-EAST-03A`. CoreWeave AI Object Storage uses different
>   [region names](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) than AWS.
> * `endpoint` is set to `https://cwobject.com`, which is the
>   CoreWeave AI Object Storage endpoint.
> * The `s3_use_path_style` option is set to `false` to use virtual-hosted-style URLs.

## Object Storage resources

After you configure the provider, you can use Terraform to manage organization access policies and bucket access policies,
and configure bucket lifecycles and versioning. For detailed examples and documentation,
see the [CoreWeave provider registry documentation](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs).

## Known issues

### CoreWeave provider 0.7.0 silently drops `NoncurrentVersionTransitions`

Version 0.7.0 of the [CoreWeave Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs) silently drops the `NoncurrentVersionTransitions` block when applying a `coreweave_object_storage_bucket_lifecycle_configuration` resource. The plan reports success, but the rule applied to the bucket does not include the noncurrent-version transition action.

**This bug was fixed in v0.7.1.** Upgrade to v0.7.1 or later (current release: v0.13.0). If you cannot upgrade immediately, apply lifecycle configurations that use `NoncurrentVersionTransitions` directly with the AWS CLI or Boto3. See [Apply a lifecycle configuration](https://docs.coreweave.com/products/storage/object-storage/buckets/lifecycle-policies.md#apply-a-lifecycle-configuration).

To verify whether a previously applied configuration was affected, read back the active lifecycle configuration with [`s3:GetBucketLifecycleConfiguration`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3#s3getbucketlifecycleconfiguration) and compare it to the configuration in your Terraform code.

## Additional resources

* To learn more about using the Terraform AWS provider with Object Storage, see
  the [S3 section of the official documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket).
* To learn more about the CoreWeave Terraform provider, see the
  [CoreWeave provider documentation](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs).
* To use the CoreWeave provider with OpenTofu, see the [OpenTofu provider documentation](https://search.opentofu.org/provider/coreweave/coreweave/latest).
