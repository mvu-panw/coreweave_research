# Available models

Source: https://docs.coreweave.com/products/inference/serverless/models

# Available models

> Browse the foundation models available through Serverless Inference


Serverless Inference provides access to several open source foundation models. Each model has different strengths and use cases.

## Generally available models

The following models are [generally available](https://docs.coreweave.com/products/inference/serverless/lifecycle.md#model-lifecycle-stages):

| Model | Model ID (for API usage) | Type | Context Window | Parameters | Description |
| - | - | - | - | - | - |
| DeepSeek V4.1-Flash | `deepseek-ai/DeepSeek-V4.1-Flash` | Text, Vision | 1049k | 16B-552B (Active-Total) | DeepSeek V4.1 Flash is a multimodal MoE model for coding, reasoning, and agentic workloads with long contexts. |
| DeepSeek V4.1-Flash-1017 | `deepseek-ai/DeepSeek-V4.1-Flash-1017` | Text, Vision | 1049k | 16B-763B (Active-Total) | DeepSeek V4.1 Flash 1017 is a multimodal MoE model for coding, reasoning, and faster agentic workflows with 1M context. |
| DeepSeek V4-Flash-0731 | `deepseek-ai/DeepSeek-V4-Flash-0731` | Text | 262k | 13B-284B (Active-Total) | DeepSeek V4-Flash-0731 is an MoE model great for coding, reasoning, and agentic workloads. |
| DeepSeek V4-Pro-0813 | `deepseek-ai/DeepSeek-V4-Pro-0813` | Text | 1049k | 49B-1.6T (Active-Total) | DeepSeek V4-Pro-0813 is a 1.6T-parameter MoE model excelling at advanced reasoning, coding, and complex agentic workloads. |
| DeepSeek V3.1 | `deepseek-ai/DeepSeek-V3.1` | Text | 161k | 37B-671B (Active-Total) | A large hybrid model that supports both thinking and non-thinking modes via prompt templates. |
| Google Gemma 4 31B | `google/gemma-4-31B-it` | Text, Vision | 262k | 31B (Total) | Gemma 4 31B Dense is designed for advanced reasoning, agentic workflows, and longer context and is natively trained on 140+ languages. |
| Google Gemma 4 26B A4B Instruct | `google/gemma-4-26B-A4B-it` | Text, Vision | 262k | 4B-26B (Active-Total) | Gemma 4 26B A4B is a multimodal MoE model with LoRA support and function calling for agentic workflows. |
| IBM Granite 4.2 8B | `ibm-granite/granite-4.2-8b` | Text | 131k | 8B (Total) | Granite 4.2 8B is an instruct model capable of enhanced tool calling, instruction following, and chat capabilities. |
| Meta Llama 3.3 70B | `meta-llama/Llama-3.3-70B-Instruct` | Text | 128k | 70B (Total) | Multilingual model excelling in conversational tasks, detailed instruction-following, and coding. |
| Meta Llama 3.1 8B | `meta-llama/Llama-3.1-8B-Instruct` | Text | 131k | 8B (Total) | Efficient conversational model optimized for responsive multilingual chatbot interactions. |
| MiniMax M3 | `MiniMaxAI/MiniMax-M3` | Text, Vision | 262k | 23B-428B (Active-Total) | MiniMax M3 is a multimodal MoE model with 23B active parameters optimized for coding and agentic workflows. |
| Moonshot AI Kimi K2.7 Code | `moonshotai/Kimi-K2.7-Code` | Text, Vision | 262k | 32B-1T (Active-Total) | Kimi K2.7 Code is a 1T-parameter MoE model with 32B active parameters purpose-built for long-horizon agentic coding and software engineering. |
| Moonshot AI Kimi K2.6 | `moonshotai/Kimi-K2.6` | Text, Vision | 262k | 32B-1T (Active-Total) | Kimi K2.6 is a multimodal Mixture-of-Experts language model featuring 32 billion activated parameters and a total of 1 trillion parameters. |
| NVIDIA Nemotron 3.5 Lightning | `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | Text | 262k | 3B-30B (Active-Total) | Nemotron 3.5 Lightning is an MoE model built for fast, reliable agentic tasks across use cases such as financial services, cybersecurity, telecom, and retail. |
| NVIDIA Nemotron 3.5 Super VL | `nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B` | Text, Vision | 1049k | 12B-120B (Active-Total) | Nemotron 3.5 Super VL is a multimodal MoE model built for visual understanding, reasoning, and agentic workflows. |
| NVIDIA Nemotron 3 Ultra | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B` | Text | 262k | 55B-550B (Active-Total) | Nemotron 3 Ultra is a powerful MoE model designed for long-running agents across coding, deep research, and enterprise automation. |
| OpenAI GPT OSS 120B | `openai/gpt-oss-120b` | Text | 131k | 5.1B-117B (Active-Total) | Efficient Mixture-of-Experts model designed for high-reasoning, agentic and general-purpose use cases. |
| OpenAI GPT OSS 20B | `openai/gpt-oss-20b` | Text | 131k | 3.6B-20B (Active-Total) | Lower latency Mixture-of-Experts model trained on OpenAI's Harmony response format with reasoning capabilities. |
| Qwen3.8 27B | `Qwen/Qwen3.8-27B` | Text, Vision | 262k | 27B (Total) | Qwen3.8-27B is a dense multimodal model suited for coding, research, vision, and long-running agent tasks. |
| Qwen3.6 35B A3B | `Qwen/Qwen3.6-35B-A3B` | Text, Vision | 262k | 3B-35B (Active-Total) | Qwen3.6-35B-A3B is an MoE multimodal model with 262K context optimized for agentic coding workflows. |
| Reflection Beam 1.0 | `reflection/Beam-1.0-501B-A23B` | Text | 1049k | 23B-501B (Active-Total) | Beam is a 501B-parameter MoE model with 23B active parameters built for coding, reasoning, and agentic workflows. |
| Z.AI GLM 5.3 | `zai-org/GLM-5.3` | Text | 1049k | 40B-744B (Active-Total) | GLM-5.3 is a 744B-parameter MoE model built for advanced reasoning, software engineering, and long-horizon agentic tasks. |
| Z.AI GLM 5.3 Flash | `zai-org/GLM-5.3-Flash` | Text, Vision | 1049k | 18B-320B (Active-Total) | GLM-5.3-Flash is a natively multimodal model with 320B total parameters and 18B active parameters. |
| Z.AI GLM 5.2 | `zai-org/GLM-5.2` | Text | 1049k | 40B-744B (Active-Total) | GLM-5.2 is a Mixture-of-Experts language model featuring 40 billion activated parameters and a total of 744 billion parameters. |

## Experimental models

The following models are [experimental](https://docs.coreweave.com/products/inference/serverless/lifecycle.md#model-lifecycle-stages):

*None currently*

## Deprecated models

The following models are [deprecated](https://docs.coreweave.com/products/inference/serverless/lifecycle.md#model-lifecycle-stages):

*None currently*

## Specify a model for inference

To specify a model when calling the API, use its `Model ID` from the preceding tables. For example:

```python theme={"system"}
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[...]
)
```

## Next steps

After you've chosen a model, continue with one of the following resources:

* Check [usage limits and pricing](https://docs.coreweave.com/products/inference/serverless/usage-limits.md) for each model.
* See the [API reference](https://docs.coreweave.com/products/inference/serverless/api-reference.md) for how to use these models.
* Try models in the [Playground](https://docs.coreweave.com/products/inference/serverless/ui-guide.md).
