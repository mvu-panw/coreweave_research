# Serverless Training API reference

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference

# Serverless Training API reference

> Browse the Serverless Training API endpoints for chat completions, models, training jobs, and health checks with authentication details.

> [!NOTE]
>
> The Serverless Training API provides endpoints for managing training jobs, including serverless reinforcement learning (RL) and supervised fine-tuning (SFT). The API is OpenAI-compatible for chat completions.

Use this reference to look up authentication requirements, the base URL, and the available endpoints for chat completions, models, training jobs, and health checks.

## Authentication

All API requests require authentication using your Forge API key. Create an API key at [forge.coreweave.com/settings](https://forge.coreweave.com/settings).

Include your API key in the `Authorization` header:

```http theme={"system"}
Authorization: Bearer YOUR_API_KEY
```

## Base URL

```text theme={"system"}
https://forge.coreweave.com/api/training/v1
```

## Available endpoints

### chat-completions

* **[POST `/v1/chat/completions`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/chat-completions/create-chat-completion)** - Create Chat Completion

### models

* **[GET `/v1/preview/base-models`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/list-base-models)** - List Base Models
* **[POST `/v1/preview/models`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/create-model)** - Create Model
* **[DELETE `/v1/preview/models/{model_id}`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/delete-model)** - Delete Model
* **[DELETE `/v1/preview/models/{model_id}/checkpoints`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/delete-model-checkpoints)** - Delete Model Checkpoints
* **[GET `/v1/preview/models/{model_id}/checkpoints`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/list-model-checkpoints)** - List Model Checkpoints
* **[POST `/v1/preview/models/{model_id}/log`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/log)** - Log

### training-jobs

* **[POST `/v1/preview/sft-training-jobs`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/create-sft-training-job)** - Create SFT Training Job
* **[POST `/v1/preview/training-jobs`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/create-rl-training-job)** - Create RL Training Job
* **[GET `/v1/preview/training-jobs/{training_job_id}`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job)** - Get Training Job
* **[GET `/v1/preview/training-jobs/{training_job_id}/events`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job-events)** - Get Training Job Events

### health

* **[GET `/v1/health`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/health/health-check)** - Health Check
* **[GET `/v1/system-check`](https://docs.coreweave.com/products/post-training/serverless-training/api-reference/health/system-check)** - System Check

## Related resources

* [Serverless Training overview](https://docs.coreweave.com/products/post-training/serverless-training.md)
* [Serverless SFT](https://docs.coreweave.com/products/post-training/serverless-training/sft.md)
* [Use your trained models](https://docs.coreweave.com/products/post-training/serverless-training/rl.md#use-your-trained-models)
* [Available models](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md)
* [Usage limits](https://docs.coreweave.com/products/post-training/serverless-training/usage-limits.md)
