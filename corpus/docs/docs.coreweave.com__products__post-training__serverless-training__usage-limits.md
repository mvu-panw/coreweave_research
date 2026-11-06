# Usage information and limits

Source: https://docs.coreweave.com/products/post-training/serverless-training/usage-limits

# Usage information and limits

> Understand pricing, usage limits, and account restrictions for Serverless Training

This page describes the pricing model, concurrency limits, training sequence length, and geographic restrictions that apply to Serverless Training. Review this information to estimate costs and to understand the constraints that affect how you run training and inference workloads.

## Pricing

Pricing has three components, each billed separately: inference, training, and storage. For specific billing rates, see the [Post-Training pricing page](https://coreweave.com/forge-pricing/post-training). The following sections describe each component.

### Inference

Inference requests made during training, such as RL rollouts and evaluations, are billed at Serverless Inference rates. See [model-specific costs](https://coreweave.com/forge-pricing/inference-agents). Learn more about purchasing credits, account tiers, and usage caps in the [Serverless Inference docs](https://docs.coreweave.com/products/inference/serverless/usage-limits.md#purchase-more-credits).

### Training

At each training step, Serverless Training collects batches of trajectories that include your agent's outputs and associated rewards (calculated by your reward function). Serverless Training uses the batched trajectories to update the weights of a LoRA adapter that specializes a base model for your task. The training jobs to update these LoRAs run on dedicated GPU clusters that Serverless Training manages.

Training for Serverless SFT and Serverless RL is billed per GPU-hour, prorated by active training time. For the current rate, see the [Post-Training pricing page](https://coreweave.com/forge-pricing/post-training).

### Model storage

Serverless Training stores checkpoints of your trained LoRAs so you can evaluate, serve, or continue training them at any time. Storage is billed monthly based on total checkpoint size and your [pricing plan](https://coreweave.com/forge-pricing). Every plan includes at least 5 GB of free storage, which is enough for roughly 30 LoRAs. To save space, delete low-performing LoRAs. See the [ART SDK](https://art.openpipe.ai/features/checkpoint-deletion) for instructions.

## Limits

The following limits apply to Serverless Training usage. Review them when sizing workloads or when planning to use the service from a new region.

* **Training sequence length**: A training sequence can be up to 32,768 tokens after tokenization. Qwen3.6 35B A3B (`Qwen/Qwen3.6-35B-A3B`) and Qwen3.8 27B (`Qwen/Qwen3.8-27B`) accept up to 65,536 tokens. Serverless SFT drops longer examples, and Serverless RL skips longer trajectories. This limit is lower than the context window listed in [Available models](https://docs.coreweave.com/products/post-training/serverless-training/available-models.md), which applies to inference on Serverless Inference.

* **Inference concurrency limits**: By default, Serverless Training supports up to 2,000 concurrent requests per user and 6,000 per project. If you exceed your rate limit, the Inference API returns a `429 Concurrency limit reached for requests` response. To avoid this error, reduce the number of concurrent requests your training job or production workload makes at once. If you need a higher rate limit, request one at [forge-support@coreweave.com](mailto:forge-support@coreweave.com).

* **Geographic restrictions**: Serverless Training is only available in supported geographic locations. For more information, see the [Terms of Service](https://site.wandb.ai/terms/).
