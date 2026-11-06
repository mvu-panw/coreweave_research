# Gateways

Source: https://docs.coreweave.com/products/inference/gateways

# Gateways

> How gateways provide authentication, routing, and traffic management for inference deployments

A gateway is the entry point for inference requests in Dedicated Inference. Each gateway provides a routable endpoint that handles authentication, request routing, load balancing, and traffic splitting across one or more model [deployments](https://docs.coreweave.com/products/inference/models.md).

This page explains how gateways work and how to configure their authentication, routing strategies, zones, endpoints, and traffic splitting. Use it to decide which options fit your inference workload.

## What gateways do

When you create a gateway, CoreWeave provisions an external-facing endpoint that clients use to send inference requests. The gateway manages several responsibilities:

* **Authentication**: Validates incoming requests using the configured authentication provider before forwarding them to model deployments.
* **Request routing**: Directs requests to the correct deployment based on the configured routing strategy.
* **Load balancing**: Distributes requests across multiple replicas of a deployment to optimize throughput and latency.
* **Traffic splitting**: Splits traffic across multiple deployments that share the same model name, enabling A/B testing and canary rollouts between model versions.

## Authentication

Configure each gateway with exactly one authentication type. Choose the option that matches how your clients already obtain credentials.

### CoreWeave IAM authentication

CoreWeave IAM authentication (`coreWeaveAuth`) validates requests using CoreWeave API access tokens. This is the same token you use to manage inference resources through the [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md). No additional configuration is required.

```json theme={"system"}
{
  "coreWeaveAuth": {}
}
```

### W\&B authentication

W\&B authentication (`weightsAndBiasesAuth`) validates requests using W\&B SaaS credentials. This option supports optional usage reporting and rate limiting through the W\&B platform.

> [!NOTE]
>
> W\&B authentication requires a W\&B SaaS account. W\&B self-hosted (non-SaaS) isn't supported. W\&B SaaS authentication is in preview. If you encounter errors, contact [CoreWeave support](https://docs.coreweave.com/support.md).

```json theme={"system"}
{
  "weightsAndBiasesAuth": {
    "enableUsageReports": true,
    "enableRateLimiting": false
  }
}
```

| Field | Description |
| - | - |
| `enableUsageReports` | Send inference usage data to W\&B for tracking. |
| `enableRateLimiting` | Enable W\&B-controlled rate limiting for inference requests. |

## Routing strategies

Configure each gateway with exactly one routing strategy. The routing strategy determines how the gateway identifies which deployment handles each request.

| Strategy | Where the model name comes from | Use when |
| - | - | - |
| [Body-based routing](#body-based-routing) | The `model` field in the JSON request body. | You want OpenAI-compatible behavior. This is the default. |
| [Path-based routing](#path-based-routing) | The first segment of the URL path. | You need to route without inspecting the request body. |
| [Header-based routing](#header-based-routing) | A custom HTTP header you specify on the gateway. | You want to route on a header value separate from the request body or URL. |

### Body-based routing

Body-based routing extracts the model name from the `model` field in the JSON request body. This is the default routing strategy and is compatible with OpenAI API conventions.

```json theme={"system"}
{
  "bodyBasedRouting": {
    "apiType": "API_TYPE_OPENAI"
  }
}
```

With body-based routing, clients send requests to the gateway endpoint directly. The gateway reads the `model` field to determine which deployment handles the request:

```bash theme={"system"}
curl -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "my-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Path-based routing

Path-based routing uses the model name as the first segment of the URL path. This approach is useful when you need to route requests without inspecting the request body.

```json theme={"system"}
{
  "pathBasedRouting": {}
}
```

With path-based routing, the model name appears in the URL. If the model name contains special characters, URL-encode it before inserting it into the path (for example, `my%2Fmodel` for `my/model`).

```bash theme={"system"}
curl -X POST "${CW_GATEWAY_ENDPOINT}/my-model/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "my-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Header-based routing

Header-based routing uses a custom HTTP header to identify the target deployment. You specify the header name when creating the gateway.

```json theme={"system"}
{
  "headerBasedRouting": {
    "headerName": "X-Model-Name"
  }
}
```

The `headerName` field accepts values between 1 and 100 characters. With header-based routing, clients include the model name in the specified header:

```bash theme={"system"}
curl -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Model-Name: my-model" \
  -d '{
    "model": "my-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Zones

When you create a gateway, you must specify the CoreWeave Availability Zone where the gateway is deployed. Placing a gateway close to its model deployments reduces request latency. The `zones` field accepts an array, but each gateway supports only one zone.

To list the available zones, query the gateway parameters endpoint:

```bash theme={"system"}
curl "${CW_BASE_URL}/v1alpha1/inference/gateways/parameters" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

## Gateway endpoints

After a gateway reaches `STATUS_READY`, the `status.endpoints` field lists one or more endpoint URLs that CoreWeave generates for you. The default endpoint URL follows this pattern, where `[GATEWAY-NAME]` is the gateway's name and `[ORG-ID]` is your CoreWeave organization ID. Any additional DNS names you set in `endpointConfiguration.additionalDns` are listed after it:

```text theme={"system"}
https://[GATEWAY-NAME].[ORG-ID].gw.cwinference.com
```

Retrieve the endpoint URL by querying the gateway:

```bash theme={"system"}
curl "${CW_BASE_URL}/v1alpha1/inference/gateways/${CW_GATEWAY_ID}" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

To configure additional DNS names for a gateway, use the `endpointConfiguration.additionalDns` field. If you configure additional DNS names, you must manually point them to the gateway endpoint.

## Traffic splitting

Traffic splitting lets you route a portion of requests to different deployments of the same model, which is useful for A/B testing and canary rollouts. When multiple deployments share the same model name and use the same gateway, the gateway splits traffic between them based on the `traffic.weight` field on each deployment. The gateway normalizes weights into percentages.

For example, the following weights configure a canary deployment:

* **Production deployment**: `traffic.weight` = 90 (receives 90% of traffic).
* **Canary deployment**: `traffic.weight` = 10 (receives 10% of traffic).

For more information about traffic weights, see [Models and deployments](https://docs.coreweave.com/products/inference/models.md#traffic-weights).

## Gateway lifecycle

A gateway moves through several states from creation to deletion. Use the current status to determine whether a gateway is ready to receive traffic or requires attention:

| Status | Description |
| - | - |
| `STATUS_CREATING` | CoreWeave is provisioning the gateway. |
| `STATUS_READY` | The gateway is ready to receive traffic. |
| `STATUS_UPDATING` | CoreWeave is updating the gateway configuration. |
| `STATUS_DELETING` | CoreWeave is removing the gateway. |
| `STATUS_ERROR` | The gateway has an error. Check `status.conditions` for details. |
| `STATUS_FAILED` | The gateway failed. Check `status.conditions` for details. |

## Manage gateways

Manage gateways through the [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md). For per-operation request and response schemas, see the [GatewayService](https://docs.coreweave.com/products/inference/reference/api-overview/gatewayservice/list-gateways.md) pages in the API reference.

For a complete walkthrough of creating a gateway, see the [Getting started](https://docs.coreweave.com/products/inference/getting-started.md) guide.
