# Serverless Inference

Source: https://docs.coreweave.com/products/inference/serverless

# Serverless Inference

> Access open-source foundation models through an OpenAI-compatible API

Serverless Inference gives you access to leading open-source foundation models through an OpenAI-compatible API. You can build AI applications and agents without signing up for a hosting provider or self-hosting a model.

## Try out inference in the UI

Navigate to [https://forge.coreweave.com/inference](https://forge.coreweave.com/inference) to explore available models and try them out in the Playground.

For more information on the web interface, see the [Try models in the Playground UI](https://docs.coreweave.com/products/inference/serverless/ui-guide.md).

## Use Serverless Inference through the API

This Python example uses Serverless Inference to send a chat completion request to an LLM.

```python lines theme={"system"}
import openai

client = openai.OpenAI(
    # The custom base URL points to Serverless Inference
    base_url='https://api.inference.wandb.ai/v1',

    # Create an API key at https://forge.coreweave.com/settings
    api_key="[YOUR-API-KEY]",

    # Optional: Team and project for usage tracking
    project="[YOUR-TEAM]/[YOUR-PROJECT]",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."}
    ],
)

print(response.choices[0].message.content)
```

## Next steps

* Review the [available models](https://docs.coreweave.com/products/inference/serverless/models.md).
* Use the service through the [API](https://docs.coreweave.com/products/inference/serverless/api-reference.md) or [Playground UI](https://docs.coreweave.com/products/inference/serverless/ui-guide.md).
* Try the [usage examples](https://docs.coreweave.com/products/inference/serverless/examples.md).
* For information about pricing and usage limits, see [Usage Information and Limits](https://docs.coreweave.com/products/inference/serverless/usage-limits.md).
