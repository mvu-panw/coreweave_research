# About serverless training

Source: https://docs.coreweave.com/products/post-training/serverless-training

# About serverless training

> Post-train and fine-tune LLMs on managed serverless infrastructure with Serverless RL and Serverless SFT.

Use Serverless RL and Serverless SFT to post-train and fine-tune LLMs on managed, serverless infrastructure. Forge provisions the training infrastructure on CoreWeave for you while leaving you full flexibility in how you set up your environment. You get instant access to a managed training cluster that auto-scales to dozens of GPUs. Serverless Training is in public preview.

We offer two serverless training methods:

* **[Serverless RL](https://docs.coreweave.com/products/post-training/serverless-training/rl.md)**: Post-train models with reinforcement learning so they learn new behaviors and improve reliability, speed, and cost on multi-turn agentic tasks. You define a reward function that scores your agent's outputs. Serverless RL splits the workflow into inference and training phases and multiplexes them across jobs to increase GPU utilization and reduce your training time and costs.
* **[Serverless SFT](https://docs.coreweave.com/products/post-training/serverless-training/sft.md)**: Fine-tune models with supervised learning on curated input and output examples. Use SFT for distillation, for teaching output style and format, or to warm up a model before applying RL.

Both methods train low-rank adapters (LoRAs) that specialize a base model for your task. Serverless Training sets the rank of each adapter by base model; see [LoRA rank and alpha](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md#lora-rank-and-alpha). Forge stores the LoRAs you train as artifacts in your Weights & Biases account, and you can also save them locally or to a third party for backup. [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md) automatically hosts every checkpoint you train, so you can send requests to a trained model as soon as a training step finishes.

## When to use each method

Serverless RL suits tasks where you can judge an outcome but cannot write out the ideal answer in advance, such as:

* Voice agents
* Deep research assistants
* On-prem models
* Content marketing analysis agents

Serverless SFT suits tasks where you have, or can produce, examples of the behavior you want:

* **Distillation**: Transfer knowledge from a larger, more capable model into a smaller, faster one.
* **Teaching output style and format**: Train a model to follow a specific response format, tone, or structure.
* **Warmup before RL**: Give a model supervised examples before refining it with reinforcement learning.

## Why Serverless Training

* **Lower training costs**: Serverless training multiplexes shared infrastructure across many users, skips the setup process for each job, and scales your GPU costs down to zero when you aren't training. This reduces training costs significantly.
* **Faster training time**: Serverless training splits inference requests across many GPUs and provisions training infrastructure the moment you need it, so jobs finish sooner and you iterate faster.
* **Automatic deployment**: Serverless training deploys every checkpoint you train, so you don't set up hosting infrastructure. You can access and test trained models immediately in local, staging, or production environments.

## How Serverless Training uses Forge services

Serverless training combines the following Forge components:

* [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md): Runs your models, including every trained checkpoint.
* [Weights & Biases](https://docs.coreweave.com/products/wandb.md): Tracks performance metrics while a LoRA adapter trains.
* [Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md): Stores and versions the LoRA adapters.
* [Weave](https://docs.coreweave.com/products/wandb/weave.md) (optional): Shows how the model responds at each step of the training loop.

Explore a [public demo workspace](https://forge.coreweave.com/wandb/wandb/demo-project-qwen-email-agent-with-art-weave-models/workspace) that demonstrates the following:

* Train a Qwen model with OpenPipe RULER and [Weave Scorers](https://docs.coreweave.com/products/wandb/weave/guides/evaluation/scorers.md#create-your-own-scorers).
* Track training progress and [create custom plots](https://docs.coreweave.com/products/wandb/app/features/custom-charts.md) in Weights & Biases.
* Evaluate the final results on a [Weave leaderboard](https://docs.coreweave.com/products/wandb/weave/cookbooks/leaderboard_quickstart.md#leaderboard-quickstart).

> [!NOTE]
>
> Serverless RL and Serverless SFT are in public preview. Training is billed per GPU-hour of active training time, and inference and artifact storage are billed separately. See [Usage information and limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md).

## Next steps

1. Check the [available models](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md).
2. Follow [Use Serverless SFT](https://docs.coreweave.com/products/post-training/serverless-training/sft.md) or [Use Serverless RL](https://docs.coreweave.com/products/post-training/serverless-training/rl.md). Each starts with its prerequisites: a Forge account, an API key, and a project.
3. Look up endpoints in the [Serverless Training API reference](https://docs.coreweave.com/products/post-training/serverless-training/api-reference.md).
