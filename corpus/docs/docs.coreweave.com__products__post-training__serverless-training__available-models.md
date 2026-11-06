# Available models

Source: https://docs.coreweave.com/products/post-training/serverless-training/available-models

# Available models

> Browse foundation models, supported variants, and capabilities available with Serverless Training.

Serverless Training supports the following foundation models for both reinforcement learning (RL) and supervised fine-tuning (SFT).

To express interest in a particular model that isn't in the model catalog, contact [support](mailto:forge-support@coreweave.com).

## Model catalog

| Model | Model ID (for API usage) | Type | Context Window | Parameters | Description |
| - | - | - | - | - | - |
| Google Gemma 4 26B A4B Instruct | `google/gemma-4-26B-A4B-it` | Text, Vision | 262k | 4B-26B (Active-Total) | Gemma 4 26B A4B is a multimodal MoE model with LoRA support and function calling for agentic workflows. |
| Meta Llama 3.1 8B | `meta-llama/Llama-3.1-8B-Instruct` | Text | 131k | 8B (Total) | Efficient conversational model optimized for responsive multilingual chatbot interactions. |
| NVIDIA Nemotron 3.5 Lightning | `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | Text | 262k | 3B-30B (Active-Total) | Nemotron 3.5 Lightning is an MoE model built for fast, reliable agentic tasks across use cases such as financial services, cybersecurity, telecom, and retail. |
| Qwen3.8 27B | `Qwen/Qwen3.8-27B` | Text, Vision | 262k | 27B (Total) | Qwen3.8-27B is a dense multimodal model suited for coding, research, vision, and long-running agent tasks. |
| Qwen3.6 35B A3B | `Qwen/Qwen3.6-35B-A3B` | Text, Vision | 262k | 3B-35B (Active-Total) | Qwen3.6-35B-A3B is an MoE multimodal model with 262K context optimized for agentic coding workflows. |

## LoRA rank and alpha

Serverless Training sets the LoRA rank and alpha for each base model. You can't change them using the API or ART. The rank depends on the base model, not on the training method.

| Model ID (for API usage) | LoRA rank |
| - | - |
| `google/gemma-4-26B-A4B-it` | 1 |
| `meta-llama/Llama-3.1-8B-Instruct` | 8 |
| `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | 8 |
| `Qwen/Qwen3.6-35B-A3B` | 1 |
| `Qwen/Qwen3.8-27B` | 8 |

To check the rank and alpha of an adapter you trained, open the `adapter_config.json` file in its `lora` artifact and read the `r` and `lora_alpha` values.
