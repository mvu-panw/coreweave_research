# coreweave_inference_capacity_claim_parameters (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/inference_capacity_claim_parameters

# coreweave_inference_capacity_claim_parameters (Data source)

> Terraform data source for querying available Managed Inference capacity claim parameters

Retrieve available [capacity claim](https://docs.coreweave.com/products/inference/scaling.md#capacity-claims) parameters for CoreWeave Managed Inference.

## Example usage

```terraform theme={"system"}
data "coreweave_inference_capacity_claim_parameters" "example" {}
```

## Schema

### Read-Only

* `zone_instance_types` (Attributes Map) Available instance types per zone (keyed by zone name). (see [below for nested schema](#nestedatt--zone_instance_types))

### Nested Schema for `zone_instance_types`

Read-Only:

* `instance_types` (Set of String) Instance type IDs that can be claimed in this zone.
