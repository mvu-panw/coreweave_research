# Enable streaming responses

Source: https://docs.coreweave.com/products/inference/serverless/response-settings/streaming

# Enable streaming responses

> Enable streaming output with Serverless Inference to receive model responses incrementally.

Setting the `stream` option to `true` returns the model's response incrementally as a stream of chunks, so you can display results as they arrive instead of waiting for the entire response. This is helpful when models take time to generate output.

All hosted models support streaming output. We recommend streaming for [reasoning models](https://docs.coreweave.com/products/inference/serverless/response-settings/reasoning.md), since non-streaming requests can time out if the model takes a long time to start producing output.

The following examples enable streaming for a chat completion request:

> [tab] Python
>
> ```python theme={"system"}
> import openai
>
> client = openai.OpenAI(
>     base_url='https://api.inference.wandb.ai/v1',
>     api_key="[YOUR-API-KEY]",  # Create an API key at https://forge.coreweave.com/settings
> )
>
> stream = client.chat.completions.create(
>     model="openai/gpt-oss-120b",
>     messages=[
>         {"role": "user", "content": "Tell me a rambling joke"}
>     ],
>     stream=True,
> )
>
> for chunk in stream:
>     if chunk.choices:
>         print(chunk.choices[0].delta.content or "", end="", flush=True)
>     else:
>         print(chunk) # Show CompletionUsage object
> ```

> [tab] Bash
>
> ```bash theme={"system"}
> curl https://api.inference.wandb.ai/v1/chat/completions \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer [YOUR-API-KEY]" \
>   -d '{
>     "model": "openai/gpt-oss-120b",
>     "messages": [
>       { "role": "user", "content": "Tell me a rambling joke" }
>     ],
>     "stream": true
>   }'
> ```
