# Bring your own LoRA adapter

Source: https://docs.coreweave.com/products/inference/serverless/lora

# Bring your own LoRA adapter

> Bring your own custom LoRA for serving fine-tuned models on Serverless Inference.


This page explains how to serve your own custom LoRA adapters on Serverless Inference. It's for developers and ML practitioners who want to deploy fine-tuned variants of supported base models without managing infrastructure.

LoRA (Low-Rank Adaptation) lets you customize large language models by training and storing only a lightweight add-on instead of a full new model. This reduces the size and cost of customization.

You can train or upload a LoRA to give a base model new capabilities, such as specializing it for customer support, creative writing, or a particular technical field. This lets you adapt the model's behavior without retraining or redeploying the entire model.

## Why use Serverless Inference for LoRAs

Serverless Inference for LoRAs offers the following benefits:

* Upload once, deploy without managing servers.
* Track which version is live with artifact versioning.
* Update models by swapping small LoRA files instead of full model weights.

## Workflow

At a high level, serving a custom LoRA involves three steps:

1. Upload your LoRA weights as a Weights & Biases artifact.
2. Reference the artifact URI as your model name in the API.
3. CoreWeave dynamically loads your weights for inference.

The following example shows how to call your custom LoRA model using Serverless Inference. Replace the placeholder values with your own API key, team, and project. The following sections describe how to upload or train the LoRA referenced here.

```python theme={"system"}
from openai import OpenAI

model_name = "wandb-artifact:///[YOUR-TEAM]/[YOUR-PROJECT]/qwen_lora:latest"

client = OpenAI(
    base_url="https://api.inference.wandb.ai/v1",
    api_key="[YOUR-API-KEY]",
    project="[YOUR-TEAM]/[YOUR-PROJECT]",
)

resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": "Say 'Hello World!'"}],
)
print(resp.choices[0].message.content)
```

See this [getting started notebook](https://wandb.me/lora_nb) for an interactive demonstration of how to create a LoRA and upload it to Weights & Biases as an artifact.

## Prerequisites

You need the following:

* A [CoreWeave Forge API key](https://docs.coreweave.com/products/wandb/integrations/add-wandb-to-any-library.md#create-an-api-key).
* A [Weights & Biases project](https://docs.coreweave.com/products/wandb/track/project-page.md).
* Python 3.8+ with the `openai` and `wandb` packages: `pip install wandb openai`.

## Add and use LoRAs

You can add LoRAs to your CoreWeave Forge account and start using them with the following methods. Choose the tab that matches where your LoRA was trained:

> [tab] Upload a LoRA you trained elsewhere
>
> Upload your own custom LoRA directory as a Weights & Biases artifact. Use this method if you trained your LoRA elsewhere (local environment, cloud provider, or partner service).
>
> This Python code uploads your locally stored LoRA weights to Weights & Biases as a versioned artifact. It creates a `lora` type artifact with the required metadata (base model and storage region), adds your LoRA files from a local directory, and logs it to your Weights & Biases project for use with inference.
>
> ```python theme={"system"}
> import wandb
>
> run = wandb.init(entity="[YOUR-TEAM]", project="[YOUR-PROJECT]")
>
> artifact = wandb.Artifact(
>     "qwen_lora",
>     type="lora",
>     metadata={"wandb.base_model": "OpenPipe/Qwen3-14B-Instruct"},
>     storage_region="coreweave-us",
> )
>
> artifact.add_dir("[PATH-TO-LORA-WEIGHTS]")
> run.log_artifact(artifact)
> ```
>
> ### Key requirements for using an existing LoRA
>
> To use your own LoRAs with Serverless Inference, ensure the following:
>
> * The LoRA must have been trained using one of the models listed in the [Supported base models](#supported-base-models) section.
> * The LoRA rank must not exceed the **Maximum LoRA Rank** for its base model in the [Supported base models](#supported-base-models) table.
> * A LoRA saved in PEFT format as a `lora` type artifact in your CoreWeave Forge account.
> * The LoRA must be stored in the `storage_region="coreweave-us"` for low latency.
> * When you upload, include the name of the base model you trained it on (for example, `meta-llama/Llama-3.1-8B-Instruct`). This ensures Serverless Inference loads it with the correct model.

> [tab] Train a new LoRA with Serverless RL
>
> Train a new LoRA with [Serverless RL](https://docs.coreweave.com/products/post-training/serverless-training.md). Your LoRA automatically becomes a Weights and Biases artifact that you can use directly.
>
> For detailed information on how to train your own LoRA, see [OpenPipe's ART quickstart](https://art.openpipe.ai/getting-started/quick-start).
>
> After training completes, your LoRA is automatically available as an artifact.

> [tab] Train a new LoRA with supervised fine-tuning
>
> Follow the [Creating a fine-tuned LoRA](https://docs.coreweave.com/products/inference/serverless/tutorials/creating-lora.md) tutorial to fine-tune a base model with supervised fine-tuning (SFT) using the TRL library, then upload the result to Weights & Biases as an artifact.

After you add your LoRA to your project as an artifact, regardless of which method you used, you can reference it from any inference call by passing its URI as the model name:

```python theme={"system"}
# After training completes, use your artifact directly
model_name = "wandb-artifact:///[YOUR-TEAM]/[YOUR-PROJECT]/your_trained_lora:latest"
```

## Supported base models

Your LoRA must be trained against one of the following base models. Use the exact model ID string when setting `wandb.base_model` so Serverless Inference can pair your adapter with the correct base model at inference time.

The **Maximum LoRA Rank** column is the largest adapter that Serverless Inference can load for each base model. It’s a limit for adapters you train elsewhere and upload, not a training setting. Adapters from Serverless SFT and Serverless RL use a fixed rank that’s always within this limit. See [LoRA rank and alpha](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md#lora-rank-and-alpha).

| Model ID (for API usage) | Maximum LoRA Rank |
| - | - |
| `google/gemma-4-26B-A4B-it` | 16 |
| `meta-llama/Llama-3.1-8B-Instruct` | 16 |
| `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | 16 |
| `Qwen/Qwen3.8-27B` | 16 |
| `Qwen/Qwen3.6-35B-A3B` | 16 |

## Pricing

You pay only for storage and the inference you run, rather than for always-on servers or dedicated GPU instances. Pricing has two components:

* [**Storage**](https://coreweave.com/forge-pricing): You're billed for the storage that holds your LoRA weights.
* **Serverless Inference usage**: Calls that use LoRA artifacts are billed at the same rates as [standard model inference](https://docs.coreweave.com/products/inference/serverless/usage-limits.md#account-tiers-and-default-usage-caps).
