# Chat completions

Source: https://docs.coreweave.com/products/inference/serverless/api-reference/chat-completions

# Chat completions

> Create chat completions using the OpenAI-compatible endpoint

Create a chat completion using the `/chat/completions` endpoint. This endpoint follows the OpenAI format for sending messages and receiving responses.

## Requirements

To create a chat completion, provide:

* The Serverless Inference service base URL: `https://api.inference.wandb.ai/v1`.
* Your CoreWeave Forge API key: `[YOUR-API-KEY]`.
* Your CoreWeave Forge team and Weights & Biases project: `[YOUR-TEAM]/[YOUR-PROJECT]` (optional).
* A model ID from the [available models](https://docs.coreweave.com/products/inference/serverless/models.md).

## Request examples

The following examples show how to send a chat completion request using Python and `curl`. Replace the placeholder values with your own API key, optional team and project, and a model ID.

> [tab] Python
>
> ```python theme={"system"}
> import openai
>
> client = openai.OpenAI(
>     # The custom base URL points to Serverless Inference
>     base_url='https://api.inference.wandb.ai/v1',
>
>     # Create an API key at https://forge.coreweave.com/settings
>     # Consider setting it in the environment as OPENAI_API_KEY instead for safety
>     api_key="[YOUR-API-KEY]",
>
>     # Optional: Team and project for usage tracking
>     project="[YOUR-TEAM]/[YOUR-PROJECT]",
> )
>
> # Replace [MODEL-ID] with any model ID from the available models list
> response = client.chat.completions.create(
>     model="[MODEL-ID]",
>     messages=[
>         {"role": "system", "content": "[YOUR-SYSTEM-PROMPT]"},
>         {"role": "user", "content": "[YOUR-PROMPT]"}
>     ],
> )
>
> print(response.choices[0].message.content)
> ```

> [tab] Bash
>
> ```bash theme={"system"}
> curl https://api.inference.wandb.ai/v1/chat/completions \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer [YOUR-API-KEY]" \
>   -H "OpenAI-Project: [YOUR-TEAM]/[YOUR-PROJECT]" \
>   -d '{
>     "model": "[MODEL-ID]",
>     "messages": [
>       { "role": "system", "content": "You are a helpful assistant." },
>       { "role": "user", "content": "Tell me a joke." }
>     ]
>   }'
> ```

## Response format

A successful request returns a response in the following OpenAI-compatible format, including the generated assistant message and token usage details.

```json theme={"system"}
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's a joke for you..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 50,
    "total_tokens": 75
  }
}
```
