# CoreWeave Provider

Source: https://docs.coreweave.com/platform/terraform

# CoreWeave Provider

> Manage CKS, VPC, Object Storage, and Managed Inference resources as code with Terraform

The CoreWeave Terraform provider lets you manage CoreWeave infrastructure as code, including CKS clusters, VPC networking, AI Object Storage policies and buckets, and Managed Inference resources. This provider is a plugin for [Terraform](https://developer.hashicorp.com/terraform), an open-source infrastructure as code tool that lets you define and provision resources in a declarative configuration language.

Use the provider to deploy and manage [CKS clusters](https://docs.coreweave.com/products/cks/clusters/create.md), [VPCs](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md), [Object Storage resources](https://docs.coreweave.com/products/storage/object-storage.md), and [Managed Inference resources](https://docs.coreweave.com/products/inference.md). For detailed examples and resource documentation, see the [provider documentation](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs).

> [!TIP]
>
> * [View the CoreWeave Terraform provider documentation on the Terraform registry](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs).
> * [Use the CoreWeave Terraform provider in your OpenTofu configuration](https://search.opentofu.org/provider/coreweave/coreweave/latest).
> * Learn more about [CoreWeave's integration and partnership with Hashicorp](https://www.hashicorp.com/en/partners/tech/coreweave).

## Example usage

```terraform theme={"system"}
variable "coreweave_api_token" {
  type        = string
  sensitive   = true
  description = "CoreWeave API token in the form `CW-SECRET-[secret]`. Can also be set via the COREWEAVE_API_TOKEN environment variable."
}

provider "coreweave" {
  token = var.coreweave_api_token
}
```

## Schema

### Optional

* `endpoint` (String) CoreWeave API Endpoint. This can also be set via the COREWEAVE\_API\_ENDPOINT environment variable, which takes precedence. Defaults to `https://api.coreweave.com/`
* `http_timeout` (String) Timeout for each CoreWeave API and Object Storage S3 HTTP attempt. This can also be set via the COREWEAVE\_HTTP\_TIMEOUT environment variable, which takes precedence. When unset, CoreWeave API attempts default to 10 seconds and S3 attempts default to 30 seconds. Values near or below service latency can cause request timeouts.
* `s3_endpoint` (String) CoreWeave S3 Endpoint, used for CoreWeave Object Storage. This can also be set via the COREWEAVE\_S3\_ENDPOINT environment variable, which takes precedence. Defaults to `https://cwobject.com`
* `token` (String, Sensitive) CoreWeave API Token in the form `CW-SECRET-<secret>`. This can also be set via the COREWEAVE\_API\_TOKEN environment variable, which takes precedence.
