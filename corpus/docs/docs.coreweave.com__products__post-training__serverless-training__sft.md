# Use Serverless SFT

Source: https://docs.coreweave.com/products/post-training/serverless-training/sft

# Use Serverless SFT

> Fine-tune models with Serverless SFT using OpenPipe's ART framework and the Serverless Training API for supervised learning.

Use Serverless SFT to fine-tune an LLM with supervised learning on curated input and output examples. Serverless SFT trains a low-rank adapter (LoRA) that specializes a base model for your task, stores the adapter as an artifact in your Weights & Biases account, and hosts every checkpoint on [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md). Serverless SFT is in public preview.

You run Serverless SFT through [OpenPipe's ART framework](https://art.openpipe.ai/getting-started/about) or directly through the Serverless Training API.

## Prerequisites

Before you start, make sure you have the following:

* **A Forge account.** If you don't have one, [sign up](https://id.coreweave.com/signup).
* **An API key.** In Forge, click the account selector, select **User settings**, and in the **API keys** section click **New key**. Name the key, then click **Create API key**. Copy the key when it is displayed, because you can't view it again. The examples in these docs read it from the `WANDB_API_KEY` environment variable; the ART quickstart shows where ART expects it.
* **A project in Weights & Biases** to record training metrics and store the trained adapter. See [Projects](https://docs.coreweave.com/products/wandb/track/project-page.md).
* **A dataset** of input and output examples that show the behavior you want the model to learn. The [ART Serverless SFT documentation](https://art.openpipe.ai/fundamentals/sft-training) describes the expected format.
* **The ART framework**, if you use it rather than calling the API directly. Follow the install steps in the [ART quickstart](https://art.openpipe.ai/getting-started/quick-start).

Also review [Usage information and limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md) to understand costs and restrictions, and choose a base model from the [available models](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md).

## When to use Serverless SFT

Serverless SFT is a good fit when you have, or can produce, examples of the behavior you want:

* **Distillation**: Transfer knowledge from a larger, more capable model into a smaller, faster one by training on the larger model's outputs.
* **Teaching output style and format**: Train a model to follow a specific response format, tone, or structure.
* **Warmup before RL**: Give a model supervised examples before refining it with [Serverless RL](https://docs.coreweave.com/products/post-training/serverless-training/rl.md).

If you can judge an outcome but cannot write out the ideal answer in advance, use Serverless RL instead.

## Train a model

> [tab] ART framework
>
> ART wraps the Serverless Training API and manages datasets, training runs, and checkpoints for you. It is the recommended way to start. Follow the [ART Serverless SFT documentation](https://art.openpipe.ai/fundamentals/sft-training) to prepare your dataset and start a training job.

> [tab] Serverless Training API
>
> Call the API directly when you want to integrate training into your own tooling:
>
> 1. Create a model with [`POST /v1/preview/models`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/create-model).
> 2. Start a job with [`POST /v1/preview/sft-training-jobs`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/create-sft-training-job).
> 3. Poll [`GET /v1/preview/training-jobs/{training_job_id}`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job) and read [job events](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job-events.md) to follow progress.
> 4. List checkpoints with [`GET /v1/preview/models/{model_id}/checkpoints`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/list-model-checkpoints).
>
> The API base URL and authentication details are in the [API overview](https://docs.coreweave.com/products/post-training/serverless-training/api-reference.md).

Serverless SFT [sets the LoRA rank and alpha for each base model](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md#lora-rank-and-alpha), and you can't configure them. The API rejects any field it doesn't support, such as `lora_rank`, with an HTTP `422` response.

## After training

Every checkpoint you train is hosted automatically. To send inference requests to it, construct the model endpoint from your team, project, model name, and training step as described in [Use your trained models](https://docs.coreweave.com/products/post-training/serverless-training/rl.md#use-your-trained-models). The same endpoint format applies to models trained with Serverless SFT and Serverless RL.

To save storage, delete checkpoints you no longer need. See [Usage information and limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md#model-storage)
