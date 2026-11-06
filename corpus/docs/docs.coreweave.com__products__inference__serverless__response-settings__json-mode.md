# Enable JSON mode

Source: https://docs.coreweave.com/products/inference/serverless/response-settings/json-mode

# Enable JSON mode

> Configure JSON mode in Serverless Inference to get structured JSON output from model responses for easier parsing.

JSON mode is useful when you need to programmatically parse model responses without handling free-form text. Enabling JSON mode instructs the model to return the response in a valid JSON format, which makes it easier to consume the output in downstream code. However, the response's schema isn't guaranteed to be consistent or to follow a particular structure. For consistent, structured JSON responses, we recommend [structured output](https://docs.coreweave.com/products/inference/serverless/response-settings/structured-output.md) when possible.

To enable JSON mode, specify it as the `response_format` in the request:

> [tab] Python
>
> ```python theme={"system"}
> import json
> import openai
>
> client = openai.OpenAI(
>     base_url='https://api.inference.wandb.ai/v1',
>     api_key="[YOUR-API-KEY]",  # Create an API key at https://forge.coreweave.com/settings
> )
>
> response = client.chat.completions.create(
>     model="openai/gpt-oss-20b",
>     messages=[
>         {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
>         {"role": "user", "content": "Give me a list of three fruits with their colors."},
>     ],
>     response_format={"type": "json_object"}  # This enables JSON mode
> )
>
> content = response.choices[0].message.content
> parsed = json.loads(content)
> print(parsed)
> ```

> [tab] Bash
>
> ```bash theme={"system"}
> curl https://api.inference.wandb.ai/v1/chat/completions \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer [YOUR-API-KEY]" \
>   -d '{
>     "model": "openai/gpt-oss-20b",
>     "messages": [
>         {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
>         {"role": "user", "content": "Give me a list of three fruits with their colors."},
>     ],
>     "response_format": {"type": "json_object"}
>   }'
> ```
