# Post-Training

Source: https://docs.coreweave.com/products/post-training

# Post-Training

> Adapt models to your tasks with distillation, reinforcement learning, and supervised fine-tuning on managed infrastructure.

Post-Training is the set of CoreWeave Forge services that adapt an existing model to your task. Each service trains on infrastructure that Forge provisions and scales for you, and each deploys what it trains so you can use the result from your application right away.

> [card] [Model Distillation](https://docs.coreweave.com/model-distillation.md)
>
> Collect training data from your application's real traffic, train a smaller model that matches a larger one, compare them, and gradually deploy the winner.

> [card] [Serverless RL](https://docs.coreweave.com/products/post-training/serverless-training/rl.md)
>
> Post-train a model with reinforcement learning so an agent improves at multi-turn tasks that you score with a reward function.

> [card] [Serverless SFT](https://docs.coreweave.com/products/post-training/serverless-training/sft.md)
>
> Fine-tune a model on curated input and output examples to teach it a task, a style, or a format.

## Choose a service

* **Model Distillation** is a guided workflow with a UI. Connect your application through the distillation proxy, and it collects examples, trains candidate models, evaluates them, and routes traffic to the one you pick. Start here if you already have an LLM feature in production and want a cheaper, faster model for it. Model Distillation is in private preview. Request access from the **Post-Training** page in Forge.
* **Serverless RL** and **Serverless SFT** are programmatic. You drive them from code through the [OpenPipe ART framework](https://art.openpipe.ai/getting-started/about) or the Serverless Training API, and you bring your own reward function or dataset. Both are in public preview. See [About Serverless Training](https://docs.coreweave.com/products/post-training/serverless-training.md) for how they compare and what they share.
