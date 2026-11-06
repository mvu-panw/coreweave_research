# coreweave_inference_gateway_parameters (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/inference_gateway_parameters

# coreweave_inference_gateway_parameters (Data source)

> Terraform data source for querying available Managed Inference gateway parameters

Retrieve available [gateway](https://docs.coreweave.com/products/inference/gateways.md) parameters for CoreWeave Managed Inference.

## Example usage

```terraform theme={"system"}
data "coreweave_inference_gateway_parameters" "example" {}
```

## Schema

### Read-Only

* `zones` (Set of String) Available zones for inference gateways.
