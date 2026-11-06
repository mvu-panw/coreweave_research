# Use Serverless RL

Source: https://docs.coreweave.com/products/post-training/serverless-training/rl

# Use Serverless RL

> Post-train models with Serverless RL using OpenPipe's ART framework and the Serverless Training API, then send requests to them.

Use Serverless RL to post-train an LLM with reinforcement learning. You define a reward function that scores your agent's outputs. Serverless RL collects batches of trajectories, updates a low-rank adapter (LoRA) so higher-scoring behavior becomes more likely, stores the adapter as an artifact in your Weights & Biases account, and hosts every checkpoint on [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md). Serverless RL is in public preview.

You run Serverless RL through [OpenPipe's ART framework](https://art.openpipe.ai/getting-started/about) or directly through the Serverless Training API.

## Prerequisites

Before you start, make sure you have the following:

* **A Forge account.** If you don't have one, [sign up](https://id.coreweave.com/signup).
* **An API key.** In Forge, click the account selector, select **User settings**, and in the **API keys** section click **New key**. Name the key, then click **Create API key**. Copy the key when it is displayed, because you can't view it again. The examples on this page read it from the `WANDB_API_KEY` environment variable; the ART quickstart shows where ART expects it.
* **A project in Weights & Biases** to record training metrics and store the trained adapter. See [Projects](https://docs.coreweave.com/products/wandb/track/project-page.md).
* **A reward function** that scores your agent's outputs. Serverless RL trains toward whatever this function rewards, so it defines the task. The [ART quickstart](https://art.openpipe.ai/getting-started/quick-start) shows how to write one.
* **The ART framework**, if you use it rather than calling the API directly. Follow the install steps in the [ART quickstart](https://art.openpipe.ai/getting-started/quick-start).

Also review [Usage information and limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md) to understand costs and restrictions, and choose a base model from the [available models](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md).

## Train an agent

> [tab] ART framework
>
> ART wraps the Serverless Training API and manages rollouts, rewards, and checkpoints for you. It is the recommended way to start. Work through the [ART quickstart](https://art.openpipe.ai/getting-started/quick-start), or open the [example notebook](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/2048/2048.ipynb), which trains an agent to play 2048 end to end.

> [tab] Serverless Training API
>
> Call the API directly when you want to integrate training into your own tooling:
>
> 1. Create a model with [`POST /v1/preview/models`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/create-model).
> 2. Generate rollouts by sending chat completions to the model's current checkpoint with [`POST /v1/chat/completions`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/chat-completions/create-chat-completion), and score them with your reward function.
> 3. Log the scored trajectories with [`POST /v1/preview/models/{model_id}/log`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/log).
> 4. Start a training step with [`POST /v1/preview/training-jobs`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/create-rl-training-job), then poll [`GET /v1/preview/training-jobs/{training_job_id}`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job) to follow it.
>
> The API base URL and authentication details are in the [API overview](https://docs.coreweave.com/products/post-training/serverless-training/api-reference.md).

## Use your trained models

After you train a model, it is automatically available for inference. This section shows you how to construct the endpoint for a trained model and send requests to it, so you can integrate the model into your application or evaluation workflows. The same steps apply to models trained with [Serverless SFT](https://docs.coreweave.com/products/post-training/serverless-training/sft.md).

To send requests to your trained model, you need the following:

* Your API key. Create one in Forge under [**User settings**](https://forge.coreweave.com/settings).
* The Serverless Training API base URL, `https://forge.coreweave.com/api/training/v1/`.
* Your model's endpoint.

The model's endpoint uses the following schema:

```text theme={"system"}
wandb-artifact:///[ENTITY]/[PROJECT]/[MODEL-NAME]:[STEP]
```

The schema consists of:

* Your entity, which is the name of your team.
* The name of the project associated with your model.
* The trained model's name.
* The training step of the model you want to deploy. This is usually the step where the model performed best in your evaluations.

For example, if your team is named `email-specialists`, your project is called `mail-search`, your trained model is named `agent-001`, and you want to deploy it on step 25, the endpoint looks like this:

```text theme={"system"}
wandb-artifact:///email-specialists/mail-search/agent-001:step25
```

After you have your endpoint, you can integrate it into your normal inference workflows. The following examples show how to make inference requests to your trained model using a cURL request or the [Python OpenAI SDK](https://github.com/openai/openai-python). Choose the example that matches your environment.

### cURL

```bash theme={"system"}
curl https://forge.coreweave.com/api/training/v1/chat/completions \
    -H "Authorization: Bearer $WANDB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
            "model": "wandb-artifact:///[ENTITY]/[PROJECT]/[MODEL-NAME]:[STEP]",
            "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize our training run."}
            ],
            "temperature": 0.7,
            "top_p": 0.95
        }'
```

### OpenAI SDK

```python theme={"system"}
from openai import OpenAI

WANDB_API_KEY = "[API-KEY]"
ENTITY = "[ENTITY]"
PROJECT = "[PROJECT]"

client = OpenAI(
    base_url="https://forge.coreweave.com/api/training/v1",
    api_key=WANDB_API_KEY
)

response = client.chat.completions.create(
    model=f"wandb-artifact:///{ENTITY}/{PROJECT}/[MODEL-NAME]:[STEP]",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize our training run."},
    ],
    temperature=0.7,
    top_p=0.95,
)

print(response.choices[0].message.content)
```

To save storage, delete checkpoints you no longer need. See [Usage information and limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md#model-storage).
