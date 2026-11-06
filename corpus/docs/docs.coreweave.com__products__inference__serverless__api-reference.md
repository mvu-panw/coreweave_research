# Serverless Inference API reference

Source: https://docs.coreweave.com/products/inference/serverless/api-reference

# Serverless Inference API reference

> Explore the complete REST API reference for the Serverless Inference service, including endpoints and authentication.

This reference describes the Serverless Inference REST API, which lets you call foundation models programmatically from your own applications. Use it to integrate hosted inference into services, scripts, or notebooks without managing model infrastructure.

> [!NOTE]
>
> This API calls models hosted by Serverless Inference. To manage Dedicated Inference gateways, deployments, and capacity claims, see the [Dedicated Inference API reference](https://docs.coreweave.com/products/inference/reference/api-overview.md). To compare Serverless Inference, Dedicated Inference, and Inference on CKS, see [About CoreWeave Inference](https://docs.coreweave.com/products/inference.md#choose-a-deployment-option).

## Base URL

Access the Serverless Inference service at:

```plaintext theme={"system"}
https://api.inference.wandb.ai/v1
```

## Prerequisites

To call the Serverless Inference API, you need:

* A CoreWeave Forge account with Serverless Inference credits.
* A valid CoreWeave Forge API key.
* Install the required libraries:

  ```bash theme={"system"}
  pip install openai
  ```

If you belong to more than one team, or want to attribute your usage to a project, you'll also need team and project IDs. In code samples, these appear as `[YOUR-TEAM]/[YOUR-PROJECT]`. If you don't specify these, Serverless Inference uses your default entity and the project name `inference`.

## Available methods

The Serverless Inference API provides OpenAI-compatible endpoints for interacting with foundation models. The following methods are available:

* **[Chat Completions](https://docs.coreweave.com/products/inference/serverless/api-reference/chat-completions.md)**: Create chat completions using foundation models.
* **[List Models](https://docs.coreweave.com/products/inference/serverless/api-reference/list-models.md)**: Get all available models and their IDs.

## Authentication

All API requests require authentication using your CoreWeave Forge API key. Create an API key at [forge.coreweave.com/settings](https://forge.coreweave.com/settings).

Include your API key in the request headers:

* For the OpenAI SDK, set the `api_key` parameter.
* For direct API calls, use `Authorization: Bearer [YOUR-API-KEY]`.

## Error handling

For a complete list of error codes and how to resolve them, see [API errors](https://docs.coreweave.com/support/inference.md).

## Next steps

After you have your API key, continue with one of the following:

* Try the [usage examples](https://docs.coreweave.com/products/inference/serverless/examples.md) to see how the API works.
* Explore models in the [Serverless Inference UI](https://docs.coreweave.com/products/inference/serverless/ui-guide.md).
* Check [usage limits](https://docs.coreweave.com/products/inference/serverless/usage-limits.md) for your account.
