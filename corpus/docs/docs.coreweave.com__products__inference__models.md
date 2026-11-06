# Models and deployments

Source: https://docs.coreweave.com/products/inference/models

# Models and deployments

> Configure model deployments with custom weights, GPU selection, and inference runtimes

A deployment in Dedicated Inference configures a model serving instance that runs your model on dedicated GPU infrastructure. Each deployment specifies the model weights, inference runtime, GPU type, and scaling parameters.

This page is for users who create or manage Dedicated Inference deployments. It covers how to configure model weights, select an inference runtime, choose GPU resources, and manage traffic across deployments so you can serve your models reliably on dedicated infrastructure.

## Bring your own weights

Dedicated Inference uses a Bring Your Own Weights (BYOW) model. You provide the model artifacts, and CoreWeave handles the infrastructure required to serve them.

Model weights must be stored in a [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) bucket. When you create a deployment, you must specify the bucket name and the path to the model directory within the bucket.

When a deployment starts, CoreWeave loads your model weights onto the selected GPU infrastructure and serves requests through the associated [gateway](https://docs.coreweave.com/products/inference/gateways.md).

> [!NOTE]
>
> Dedicated Inference doesn't pull model weights directly from external sources such as Hugging Face. Download your model weights and upload them to an AI Object Storage bucket before creating a deployment.

### Grant inference access to your bucket

Dedicated Inference reads your model weights from AI Object Storage using the Dedicated Inference service account. Attach the following bucket policy to your weights bucket so the service can list and read its contents.

> [!WARNING]
>
> Attaching a bucket policy removes the implicit access your organization's users had to the bucket. This policy grants access only to the service account, so on its own it locks your users out with `AccessDenied` errors. To keep their access, add the `AllowOrgUsers` statement from [Grant inference access to your bucket](https://docs.coreweave.com/products/inference/getting-started.md#grant-inference-access-to-your-bucket). For trainers that publish RL Rollouts checkpoints, also grant the [checkpoint publishing permissions](https://docs.coreweave.com/products/inference/rl-rollouts.md#prerequisites).

Replace `[BUCKET-NAME]` with the name of the bucket containing your model weights.

```json theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowInference",
      "Effect": "Allow",
      "Principal": {
        "CW": [
          "arn:aws:iam::cw4637:coreweave/uvAGGQSxxXeeQBJzcGsD9"
        ]
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ]
    }
  ]
}
```

If you store models only under a specific prefix, you can narrow object access to that prefix:

```json theme={"system"}
"Resource": [
  "arn:aws:s3:::[BUCKET-NAME]",
  "arn:aws:s3:::[BUCKET-NAME]/path/to/models/*"
]
```

The bucket-level ARN (`arn:aws:s3:::[BUCKET-NAME]`) must remain as-is for `s3:ListBucket`.

Save the policy to a file (for example, `inference-bucket-policy.json`) and apply it with the AWS CLI. If you've configured a [named AWS CLI profile](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#set-coreweave-specific-configurations) for CoreWeave, pass it with `--profile [PROFILE-NAME]`. Omit the flag if your CoreWeave credentials are in the `default` profile.

```bash theme={"system"}
aws s3api put-bucket-policy \
  --bucket [BUCKET-NAME] \
  --policy file://inference-bucket-policy.json \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

For other tools (`s3cmd`, Boto3, Terraform) and the full reference, see [Manage bucket policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md).

> [!WARNING]
>
> The Cloud Console doesn't support setting bucket policies. Apply the policy with the AWS CLI, an S3 SDK, or Terraform. Organization access policies in the Console are a different mechanism and won't grant the inference service account access to your bucket.

> [!NOTE]
>
> The `Principal` value in the preceding policy is the canonical Dedicated Inference service account and is the same for all customers. If a deployment fails to load weights with a 520 or timeout despite reaching `STATUS_READY`, a missing bucket policy is the most common cause.

After the policy is in place, deployments can read model weights from the bucket when they start.

### Model configuration

The `model` field in a deployment specifies where to find the model weights and what name to use for routing:

| Field | Required | Description |
| - | - | - |
| `name` | Yes | The model name used to route inference requests and listed in the `/models` endpoint. Must be 4-63 characters. |
| `bucket` | Yes | The Object Storage bucket containing the model weights. |
| `path` | Yes | The path within the bucket to the model and configuration files. |

The model `name` is how clients identify which deployment should handle their request. For body-based routing, the `model` field in the request body must match this name. For path-based routing, the model name is the first segment of the URL path.

## Inference runtimes

The inference runtime is the engine that loads your model weights and serves requests. CoreWeave manages the inference runtime. The `runtime` field configures which engine and version to use. You must specify an engine when you create a deployment.

### Supported engines

| Engine | Description |
| - | - |
| `dynamo-vllm` | (Recommended) Inference engine that wraps vLLM with the [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) orchestrator, and supports enhancements such as kv-cache-aware routing and many others. |
| `vllm` | Inference engine for large language models. Supports continuous batching, paged attention, and tensor parallelism. Note that the `vllm` engine is scheduled for deprecation. |

### Runtime configuration

| Field | Required | Description |
| - | - | - |
| `engine` | Yes | The inference engine. Supported value: `dynamo-vllm`, `vllm`. |
| `version` | Yes | The engine version in semantic versioning (SemVer) format. Must be one of the versions the deployment parameters endpoint returns. |
| `engineConfig` | No | A map of engine-specific configuration options as key-value pairs. |

Query the available runtime versions and configuration options from the deployment parameters endpoint:

```bash theme={"system"}
curl "${CW_BASE_URL}/v1alpha1/inference/deployments/parameters" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

### Engine configuration options

The `engineConfig` field accepts engine-specific key-value pairs that control model serving behavior. Examples of supported keys for `dynamo-vllm` and `vllm`:

| Key | Description |
| - | - |
| `max-model-len` | Maximum sequence length (context window) the model can handle. Reduce this to decrease memory usage for workloads with shorter sequences. |
| `reasoning-parser` | Parser for structured reasoning output from thinking models. Set to the parser matching your model (for example, `qwen3`, `deepseek_r1`). |
| `enable-auto-tool-choice` | Enables automatic tool selection for tool-calling models. Set the value to an empty string to enable. |
| `tool-call-parser` | Parser for tool call output format. Set to the parser matching your model (for example, `llama3_json`, `qwen3_coder`). |
| `max-num-batched-tokens` | Maximum number of tokens processed in a single batch. Controls the throughput and latency tradeoff. |
| `structured-outputs-config.backend` | Backend for structured output generation. Options: `guidance`, `xgrammar`. |
| `speculative-config.[FIELD]` | Speculative decoding keys (for example, `speculative-config.method`, `speculative-config.num_speculative_tokens`). Allowed keys differ between `dynamo-vllm` and `vllm`. See [Speculative decoding](https://docs.coreweave.com/products/inference/speculative-decoding.md). |

The deployment parameters endpoint returns the full list of allowed configuration keys for each engine under `runtimeParameters.runtimeConfigOptions`.

## GPU selection

Deployments run on dedicated GPU infrastructure. The `resources` field configures the hardware allocation that each replica uses to serve your model.

| Field | Required | Description |
| - | - | - |
| `instanceType` | Yes | The GPU instance type. Query available types from the deployment parameters endpoint. |
| `gpuCount` | Yes | The number of GPUs allocated to each replica. Allowed values: `1`, `2`, `4`, `8`, `16`. CoreWeave automatically assigns CPU and RAM based on GPU count. |

Query the available instance types from the deployment parameters endpoint:

```bash theme={"system"}
curl "${CW_BASE_URL}/v1alpha1/inference/deployments/parameters" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

The response includes the available instance types under `resourceParameters.instanceTypes`.

### Choose an instance type

Match the instance type to your model's requirements:

* **Model size**: Choose a GPU with enough memory to fit your model weights and the inference runtime's working memory (KV cache).
* **Throughput**: Higher-end GPUs (H200, B200) provide more compute and memory bandwidth for faster inference.
* **Multi-GPU**: For models that exceed a single GPU's memory, increase `gpuCount` to allocate additional GPUs per replica.

## Traffic weights

The `traffic.weight` field controls how a gateway distributes requests across deployments that serve the same model name. It takes effect only when two or more deployments share a model name on the same gateway. A single deployment receives all of its model's traffic regardless of its weight, so you can leave the example value of `100` in place until you add a second deployment for that model.

| Field | Description |
| - | - |
| `weight` | An integer from 0 to 1000. The gateway normalizes weights across all deployments with the same model name into percentages. |

When multiple deployments share a model name, the gateway splits requests between them in proportion to their weights, which supports canary releases and A/B testing:

* Two deployments with equal weights (for example, `100` each) each receive approximately half of the requests over time. The gateway doesn't guarantee strict request-by-request alternation.
* If deployment A has `weight: 90` and deployment B has `weight: 10`, deployment A receives 90% of traffic and deployment B receives 10%.

Setting `weight` to `0` stops traffic to a deployment without deleting it.

Traffic weights are separate from the load balancing a gateway performs within a single deployment. Across the replicas of one deployment, the gateway balances requests to optimize throughput and latency. Across multiple deployments that share a model name, `traffic.weight` controls the share of traffic each deployment receives.

## Disable a deployment

Set the `disabled` field to `true` to stop a deployment from serving traffic without deleting it. A disabled deployment retains its configuration. To re-enable it, set `disabled` to `false`.

## Deployment lifecycle

A deployment reports its current state through the `status` field so you can track provisioning, updates, and failures. Deployments go through the following states:

| Status | Description |
| - | - |
| `STATUS_CREATING` | CoreWeave is provisioning the deployment and loading model weights. |
| `STATUS_READY` | The deployment is ready and serving requests. |
| `STATUS_UPDATING` | CoreWeave is updating the deployment configuration. Existing replicas continue serving traffic during updates. |
| `STATUS_DELETING` | CoreWeave is removing the deployment. Existing requests have a grace period to complete. |
| `STATUS_ERROR` | The deployment encountered an error. Check `status.conditions` for details. |
| `STATUS_FAILED` | The deployment failed to start. Check `status.conditions` for details. |

## Manage deployments

Manage deployments through the [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md). For per-operation request and response schemas, see the [DeploymentService](https://docs.coreweave.com/products/inference/reference/api-overview/deploymentservice/list-deployments.md) pages in the API reference.

> [!WARNING]
>
> Update requests (`PATCH`) require the complete deployment specification, not just the fields you're changing. Omitted fields revert to their defaults, except the `hotLoad` section: omitting or changing it is rejected, so resend it unchanged.

For a step-by-step walkthrough, see the [Getting started](https://docs.coreweave.com/products/inference/getting-started.md) guide.
