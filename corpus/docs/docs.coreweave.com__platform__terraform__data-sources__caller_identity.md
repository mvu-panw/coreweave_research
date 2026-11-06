# coreweave_caller_identity (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/caller_identity

# coreweave_caller_identity (Data source)

> Terraform data source for the organization and principal IDs of the configured CoreWeave API token

Retrieve the organization and principal identifiers associated with the configured CoreWeave API token.

Comparable identity data sources in other HashiCorp cloud providers include [aws\_caller\_identity](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity), [azurerm\_client\_config](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config), and [google\_client\_openid\_userinfo](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_openid_userinfo). Each data source reflects its provider's identity model and exports different attributes.

## Example usage

```terraform theme={"system"}
data "coreweave_caller_identity" "current" {}
```

## Schema

### Read-Only

* `organization_id` (String) The unique identifier of the organization associated with the configured CoreWeave API token.
* `principal_id` (String) The unique identifier of the principal associated with the configured CoreWeave API token.
