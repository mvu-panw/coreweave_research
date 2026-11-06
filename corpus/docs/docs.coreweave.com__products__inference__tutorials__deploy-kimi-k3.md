# Deploy Kimi K3 on Dedicated Inference

Source: https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3

# Deploy Kimi K3 on Dedicated Inference

> Serve Moonshot AI's Kimi K3 on GB300 GPUs with expert parallelism and speculative decoding

This tutorial shows you how to deploy [Kimi K3](https://huggingface.co/moonshotai/Kimi-K3) on [CoreWeave Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md) and send your first request. [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md) covers the same workflow, but leaves the GPU, engine, and tuning choices to you. This tutorial supplies the values CoreWeave validated for Kimi K3 on GB300.

Kimi K3 is a large mixture-of-experts (MoE) model, and serving it well takes more than the defaults. The configuration in this tutorial spreads the model across 16 GB300 GPUs, enables expert parallelism and an FP8 KV cache, and pairs the model with a DSpark draft model for [speculative decoding](https://docs.coreweave.com/products/inference/speculative-decoding.md). By the end, you have an OpenAI-compatible endpoint serving Kimi K3.

In this tutorial, you complete the following steps:

1. **Stage the Kimi K3 weights and the DSpark draft model** in a CoreWeave AI Object Storage bucket.
2. **Grant the Dedicated Inference service account access** to that bucket.
3. **Create a gateway** to expose the model.
4. **Create the deployment** with the validated Kimi K3 engine configuration.
5. **Wait for the deployment** to load the weights and start the engine.
6. **Send an inference request** to verify the endpoint.
7. **Clean up** the gateway and deployment when you're done.

## Prerequisites

Before you begin, verify that you have the following:

* A CoreWeave account with Dedicated Inference access enabled.
* Inference GPU quota for `gb300-4x`, covering the 16 GPUs this tutorial deploys. Quota is granted per organization and per instance type. Without it, creating the deployment fails with `organization has no GPU quota for it`, and setting a capacity class doesn't waive the requirement. To request quota, [submit a support ticket](https://coreweave.freshdesk.com/support/login).
* A CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) with the [Inference Admin role](https://docs.coreweave.com/security/iam/access-policies/roles.md#inference).
* The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) installed and authenticated.
* A [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) bucket for the model weights.
* The Hugging Face CLI (`hf`) to download the model weights.
* The AWS CLI, configured with [Object Storage credentials](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#set-coreweave-specific-configurations), to upload weights and apply the bucket policy.
* `curl` and [`jq`](https://jqlang.org) for API requests and polling.

Set your API token and the CoreWeave API base URL, replacing `[API-TOKEN]` with your token:

```bash theme={"system"}
export CW_API_TOKEN="[API-TOKEN]"
export CW_BASE_URL="https://api.coreweave.com"
```

## Stage the model weights

Dedicated Inference uses a [bring-your-own-weights (BYOW)](https://docs.coreweave.com/products/inference/models.md#bring-your-own-weights) model and doesn't pull from Hugging Face directly. Before you create the deployment, download both models and upload them to your bucket.

Kimi K3 requires two sets of artifacts:

| Artifact | Hugging Face repository | Purpose |
| - | - | - |
| Main model | [`moonshotai/Kimi-K3`](https://huggingface.co/moonshotai/Kimi-K3) | The model that serves requests. |
| Draft model | [`Inferact/Kimi-K3-DSpark`](https://huggingface.co/Inferact/Kimi-K3-DSpark) | The DSpark speculator that proposes tokens for speculative decoding. |

Download both repositories, pinning the revisions CoreWeave validated:

```bash theme={"system"}
hf download moonshotai/Kimi-K3 \
  --revision c5d1dd4c428bd1ce8b88c5044f3b6ccde9e3b721 \
  --local-dir ./Kimi-K3

hf download Inferact/Kimi-K3-DSpark \
  --revision cf6b8244620e7ea4b0651d214f28e89eac75bed6 \
  --local-dir ./Kimi-K3-DSpark
```

Kimi K3 is a large model, so make sure the machine you download to has enough free disk space for both sets of weights.

In your bucket, both models go under a single prefix, with the draft model nested inside the main model's path:

```text theme={"system"}
s3://[BUCKET-NAME]/[MODEL-PATH]/                            ← main model
├── config.json
├── model-00001-of-000xx.safetensors
├── ...
└── speculator/
    └── Inferact/
        └── Kimi-K3-DSpark/
            └── cf6b8244620e7ea4b0651d214f28e89eac75bed6/    ← draft model
                ├── config.json
                └── ...
```

> [!WARNING]
>
> The draft model must live under the main model path, because only that prefix is copied into the serving container. When a deployment starts, CoreWeave mirrors everything under the model path into `/tmp/model`, preserving the directory structure, and `speculative-config` points at the resulting in-container path. This tutorial stages the draft model at `speculator/Inferact/Kimi-K3-DSpark/[COMMIT]/` to match the `speculative-config` value in [Create the deployment](#create-the-deployment). If you stage it somewhere else, update both to match, or the deployment fails to start.

Upload each model with the AWS CLI. Replace `[BUCKET-NAME]` with your bucket, `[MODEL-PATH]` with the prefix you want to store the model under, and `[PROFILE-NAME]` with your AWS CLI profile name. The `--exclude` flag keeps the metadata directory that `hf download` writes out of the model path:

```bash theme={"system"}
aws s3 sync ./Kimi-K3 s3://[BUCKET-NAME]/[MODEL-PATH]/ \
  --exclude ".cache/*" \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]

aws s3 sync ./Kimi-K3-DSpark \
  s3://[BUCKET-NAME]/[MODEL-PATH]/speculator/Inferact/Kimi-K3-DSpark/cf6b8244620e7ea4b0651d214f28e89eac75bed6/ \
  --exclude ".cache/*" \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

If your CoreWeave credentials are in the `default` AWS CLI profile, omit `--profile [PROFILE-NAME]`. For details about configuring a named profile, see [Get started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#set-coreweave-specific-configurations).

Confirm the nested layout before you continue, while a mistake is still cheap to fix. The following command lists the draft model's files under the `speculator/` prefix:

```bash theme={"system"}
aws s3 ls s3://[BUCKET-NAME]/[MODEL-PATH]/speculator/Inferact/Kimi-K3-DSpark/cf6b8244620e7ea4b0651d214f28e89eac75bed6/ \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

If that listing is empty, the draft model is in the wrong place and the deployment fails on startup.

The commit hashes in these paths pin the exact model revisions CoreWeave validated. If you stage a different revision of the draft model, update the directory name and the `speculative-config` value in the deployment command to match.

## Apply the bucket policy

Dedicated Inference reads weights from AI Object Storage through the Dedicated Inference service account, which needs a bucket policy granting it read access.

The following policy includes an `AllowOrgUsers` statement in addition to the inference grant. Don't remove it: once any policy is attached, only requests it explicitly allows are permitted, so a policy that grants only the inference service account locks your own users out of the bucket with `AccessDenied` errors, including in the Cloud Console's bucket viewer.

Replace `[BUCKET-NAME]` with your bucket name, and `[ORG-ID]` with your CoreWeave organization ID, which you can find on the [Settings page](https://console.coreweave.com/account/settings) of the Cloud Console. Leave the `Principal` in the `AllowInference` statement exactly as shown. It identifies the Dedicated Inference service account, is the same for every customer, and isn't a value you generate:

```json title="inference-bucket-policy.json" theme={"system"}
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
    },
    {
      "Sid": "AllowOrgUsers",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ],
      "Condition": {
        "StringEquals": {
          "cw:PrincipalOrgID": ["[ORG-ID]"]
        }
      }
    }
  ]
}
```

> [!CAUTION]
>
> Always include the `Condition` block in the `AllowOrgUsers` statement when using `"Principal": "*"`. Without it, the bucket is readable by anyone on the internet, not only principals in your organization.

Save the policy as `inference-bucket-policy.json` and apply it with the AWS CLI. Because `put-bucket-policy` replaces the existing bucket policy rather than merging with it, review any policy already on the bucket before you run this:

```bash theme={"system"}
aws s3api put-bucket-policy \
  --bucket [BUCKET-NAME] \
  --policy file://inference-bucket-policy.json \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

Policy changes take a few moments to propagate. Confirm the policy applied by fetching it back:

```bash theme={"system"}
aws s3api get-bucket-policy \
  --bucket [BUCKET-NAME] \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

The response includes both the `AllowInference` and `AllowOrgUsers` statements once the policy propagates. A missing or incorrect bucket policy is a common cause of deployments that fail while loading weights. For alternative tooling and how to scope access to a single prefix, see [Grant inference access to your bucket](https://docs.coreweave.com/products/inference/models.md#grant-inference-access-to-your-bucket).

## Create a gateway

A [gateway](https://docs.coreweave.com/products/inference/gateways.md) provides the external endpoint that routes traffic to your deployment, and it handles authentication and load balancing.

Query the zones where Dedicated Inference capacity is available:

```bash theme={"system"}
curl -s "${CW_BASE_URL}/v1alpha1/inference/gateways/parameters" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
```

Create the gateway in one of the returned zones, replacing `[ZONE-NAME]`:

```bash theme={"system"}
curl -s -X POST "${CW_BASE_URL}/v1alpha1/inference/gateways" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "kimi-k3-gateway",
    "zones": ["[ZONE-NAME]"],
    "coreWeaveAuth": {},
    "bodyBasedRouting": {
      "apiType": "API_TYPE_OPENAI"
    }
  }'
```

Body-based routing sends each request to the deployment whose model name matches the `model` field in the request body, following OpenAI API conventions.

Save the gateway ID from `gateway.spec.id` in the response. This is the ID, not the name you chose:

```bash theme={"system"}
export CW_GATEWAY_ID="[GATEWAY-ID]"
```

You now have a gateway with an external endpoint, but no deployment behind it yet. You create the deployment in the next section.

For the full set of gateway options, including path-based routing and custom authentication, see [Gateways](https://docs.coreweave.com/products/inference/gateways.md).

## Create the deployment

The following command creates a single-replica Kimi K3 deployment using the engine configuration CoreWeave validated on GB300. Replace `[DEPLOYMENT-NAME]` with a name for the deployment, and `[BUCKET-NAME]` and `[MODEL-PATH]` with the bucket and prefix you staged the weights under.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment create \
>     --name [DEPLOYMENT-NAME] \
>     --gateway-ids ${CW_GATEWAY_ID} \
>     --instance-type gb300-4x --gpu-count 16 \
>     --engine dynamo-vllm --engine-version 0.27.0+crwv.1 \
>     --model-name moonshotai/Kimi-K3 \
>     --model-bucket [BUCKET-NAME] \
>     --model-path [MODEL-PATH] \
>     --min 1 --max 1 --concurrency 32 --capacity-classes on-demand \
>     --engine-config 'attention-config={"mla_prefill_backend":"TRTLLM_RAGGED","use_prefill_query_quantization":true}' \
>     --engine-config 'compilation-config={"pass_config":{"fuse_allreduce_rms":false}}' \
>     --engine-config 'dyn-reasoning-parser=kimi_k3' \
>     --engine-config 'dyn-tool-call-parser=kimi_k3' \
>     --engine-config 'enable-expert-parallel' \
>     --engine-config 'enable-multimodal' \
>     --engine-config 'enable-prefix-caching' \
>     --engine-config 'kv-cache-dtype=fp8' \
>     --engine-config 'max-model-len=131072' \
>     --engine-config 'max-num-batched-tokens=32768' \
>     --engine-config 'max-num-seqs=32' \
>     --engine-config 'moe-backend=auto' \
>     --engine-config 'reasoning-parser=kimi_k3' \
>     --engine-config 'speculative-config={"model":"/tmp/model/speculator/Inferact/Kimi-K3-DSpark/cf6b8244620e7ea4b0651d214f28e89eac75bed6","num_speculative_tokens":7,"method":"dspark","attention_backend":"FLASHINFER_MLA","draft_sample_method":"probabilistic","rejection_sample_method":"block"}' \
>     --engine-env 'VLLM_ALLREDUCE_USE_FLASHINFER=1' \
>     --engine-env 'VLLM_USE_V2_MODEL_RUNNER=1'
> ```

> [tab] curl
>
> The REST equivalent passes the same options through `runtime.engineConfig` and `runtime.engineEnv`. Both fields are maps of strings, so the nested values are JSON-encoded strings, and the two boolean flags are empty strings.
>
> ```bash theme={"system"}
> curl -X POST "${CW_BASE_URL}/v1alpha1/inference/deployments" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "name": "[DEPLOYMENT-NAME]",
>     "gatewayIds": ["[GATEWAY-ID]"],
>     "runtime": {
>       "engine": "dynamo-vllm",
>       "version": "0.27.0+crwv.1",
>       "engineConfig": {
>         "attention-config": "{\"mla_prefill_backend\":\"TRTLLM_RAGGED\",\"use_prefill_query_quantization\":true}",
>         "compilation-config": "{\"pass_config\":{\"fuse_allreduce_rms\":false}}",
>         "dyn-reasoning-parser": "kimi_k3",
>         "dyn-tool-call-parser": "kimi_k3",
>         "enable-expert-parallel": "",
>         "enable-multimodal": "",
>         "enable-prefix-caching": "",
>         "kv-cache-dtype": "fp8",
>         "max-model-len": "131072",
>         "max-num-batched-tokens": "32768",
>         "max-num-seqs": "32",
>         "moe-backend": "auto",
>         "reasoning-parser": "kimi_k3",
>         "speculative-config": "{\"model\":\"/tmp/model/speculator/Inferact/Kimi-K3-DSpark/cf6b8244620e7ea4b0651d214f28e89eac75bed6\",\"num_speculative_tokens\":7,\"method\":\"dspark\",\"attention_backend\":\"FLASHINFER_MLA\",\"draft_sample_method\":\"probabilistic\",\"rejection_sample_method\":\"block\"}"
>       },
>       "engineEnv": {
>         "VLLM_ALLREDUCE_USE_FLASHINFER": "1",
>         "VLLM_USE_V2_MODEL_RUNNER": "1"
>       }
>     },
>     "resources": {
>       "instanceType": "gb300-4x",
>       "gpuCount": 16
>     },
>     "model": {
>       "name": "moonshotai/Kimi-K3",
>       "bucket": "[BUCKET-NAME]",
>       "path": "[MODEL-PATH]"
>     },
>     "autoscaling": {
>       "min": 1,
>       "max": 1,
>       "concurrency": 32,
>       "capacityClasses": ["CAPACITY_CLASS_ON_DEMAND"]
>     },
>     "traffic": {
>       "weight": 100
>     }
>   }'
> ```

The deployment name must be a valid hostname label: letters, digits, and hyphens only, starting and ending with a letter or digit, and no more than 63 characters. Dots aren't allowed.

### What the configuration does

The following table explains the settings that are specific to serving Kimi K3 on GB300. Rows without a leading `--` are keys passed through `--engine-config`.

| Setting | Value | Purpose |
| - | - | - |
| `--instance-type` | `gb300-4x` | [GB300 NVL72 instances](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md). Each instance provides 4 GPUs. |
| `--gpu-count` | `16` | 16 GPUs per replica, which is 4 instances. Each replica spans multiple Nodes. |
| `--engine` | `dynamo-vllm` | The [recommended engine](https://docs.coreweave.com/products/inference/models.md#supported-engines): vLLM with NVIDIA Dynamo orchestration and kv-cache-aware routing. |
| `--engine-version` | `0.27.0+crwv.1` | The CoreWeave build validated for Kimi K3. |
| `--concurrency` | `32` | Target in-flight requests per replica, matched to `max-num-seqs`. |
| `--capacity-classes` | `on-demand` | Uses on-demand GPUs. If you have a [capacity claim](https://docs.coreweave.com/products/inference/scaling.md#capacity-claims), change to `reserved`. |
| `enable-expert-parallel` | Enabled | Distributes the MoE experts across the 16 GPUs instead of replicating them. |
| `enable-multimodal` | Enabled | Enables multimodal inputs for Kimi K3. |
| `dyn-reasoning-parser` / `dyn-tool-call-parser` / `reasoning-parser` | `kimi_k3` | Parses Kimi K3 reasoning blocks and tool calls in model output. |
| `kv-cache-dtype` | `fp8` | Halves KV cache memory compared to BF16, leaving more headroom for long-context requests. |
| `max-model-len` | `131072` | A 128K-token context window. Raise it for longer prompts, at the cost of KV cache headroom for concurrency. |
| `enable-prefix-caching` | Enabled | Reuses the KV cache for shared prompt prefixes, which cuts time to first token for repeated system prompts. |
| `speculative-config` | DSpark, 7 tokens | [Speculative decoding](https://docs.coreweave.com/products/inference/speculative-decoding.md) with the DSpark draft model. The `model` value is the in-container path from [Stage the model weights](#stage-the-model-weights). |

The `--engine-version` value pins a specific runtime build. To see the versions available to your organization, run `cwic inference deployment parameters` or query the [deployment parameters endpoint](https://docs.coreweave.com/products/inference/getting-started.md#create-a-deployment). The deployment parameters response also lists the allowed configuration keys for each engine under `runtimeParameters.runtimeConfigOptions`.

Save the deployment ID, which the CoreWeave Intelligent CLI prints on success and the API returns in `deployment.spec.id`:

```bash theme={"system"}
export CW_DEPLOYMENT_ID="[DEPLOYMENT-ID]"
```

The deployment now exists and is attached to your gateway, but it can't serve traffic until it finishes starting up.

## Wait for the deployment to start

The deployment downloads the weights and starts the inference engine. Because Kimi K3 is a large model, expect this to take several minutes. The inference engine has up to an hour to finish starting, so the following loop polls for the same period. Poll until the status reaches `STATUS_READY`:

```bash theme={"system"}
deadline=$(( $(date +%s) + 3600 ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  status_deployment=$(curl -sS "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
    -H "Authorization: Bearer ${CW_API_TOKEN}" \
    | jq -r '.deployment.status.status // "UNKNOWN"')
  echo "Status: $status_deployment"
  case "$status_deployment" in
    STATUS_READY|STATUS_FAILED) break ;;
  esac
  sleep 30
done

case "$status_deployment" in
  STATUS_READY) echo "Deployment is ready." ;;
  STATUS_FAILED) echo "Deployment failed." ;;
  *) echo "Timed out waiting for the deployment to become ready. Last status: $status_deployment" ;;
esac
```

The loop stops when the deployment becomes ready, reaches `STATUS_FAILED`, or reaches the one-hour timeout. It keeps polling through `STATUS_ERROR`, which can clear on its own.

If the deployment reports `model path has no objects` or that the bucket isn't accessible, recheck the bucket policy, the bucket name, and the model path. If it reaches `STATUS_ERROR` while loading, check the engine logs as described in [Observability](#observability).

After the deployment is ready, retrieve the gateway endpoint from `gateway.status.endpoints`:

```bash theme={"system"}
curl -s "${CW_BASE_URL}/v1alpha1/inference/gateways/${CW_GATEWAY_ID}" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
```

Save the endpoint, replacing `[GATEWAY-ENDPOINT]` with the value from the response:

```bash theme={"system"}
export CW_GATEWAY_ENDPOINT="[GATEWAY-ENDPOINT]"
```

> [!NOTE]
>
> The gateway's DNS record and TLS certificate provision asynchronously and can take several minutes. If your first request fails with an SSL handshake or DNS resolution error, wait a few minutes and retry.

## Send an inference request

The gateway exposes an OpenAI-compatible API. With body-based routing, set the `model` field to the deployment's model name, `moonshotai/Kimi-K3`:

```bash theme={"system"}
curl -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "moonshotai/Kimi-K3",
    "messages": [
      {
        "role": "user",
        "content": "What is CoreWeave?"
      }
    ],
    "max_tokens": 256
  }'
```

A successful response is an OpenAI-compatible chat completion, which confirms the gateway and deployment are working end to end. Beyond the standard fields, vLLM also returns engine-specific fields such as `token_ids`, `prompt_logprobs`, and `kv_transfer_params`. These are typically `null` for normal requests, so you can ignore them.

```json theme={"system"}
{
  "id": "chatcmpl-bcbcbae71847bf87",
  "object": "chat.completion",
  "created": 1777477750,
  "model": "moonshotai/Kimi-K3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "CoreWeave is a cloud infrastructure provider...",
        "refusal": null,
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "logprobs": null,
      "finish_reason": "length",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "prompt_tokens": 24,
    "total_tokens": 104,
    "completion_tokens": 80,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```

You can also use the Python `openai` client, replacing `[GATEWAY-ENDPOINT]` with your gateway endpoint and `[API-TOKEN]` with your API token:

```python theme={"system"}
from openai import OpenAI

client = OpenAI(
    base_url="[GATEWAY-ENDPOINT]/v1/",
    api_key="[API-TOKEN]",
)

response = client.chat.completions.create(
    model="moonshotai/Kimi-K3",
    messages=[
        {"role": "user", "content": "What is CoreWeave?"},
    ],
    max_tokens=256,
)
print(response.choices[0].message.content)
```

## Observability

Engine logs are where startup and runtime errors surface, including the weight-loading failures described in [Wait for the deployment to start](#wait-for-the-deployment-to-start). Viewing them requires the **Observability Viewer** role in an [IAM access policy](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry). Without that role, you can still open Grafana from the Cloud Console, but you can't see metrics or logs data.

For the steps to open Grafana and run a log query, see [View deployment logs](https://docs.coreweave.com/products/inference/getting-started.md#view-deployment-logs). The default query returns logs for every deployment in your organization. To narrow it to this deployment, replace `[DEPLOYMENT-ID]` with the ID you saved earlier:

```text theme={"system"}
{cluster="cwinference", container="vllm-server", deployment="[DEPLOYMENT-ID]"}
```

For request rate, latency, and GPU utilization, see [View inference metrics](https://docs.coreweave.com/products/inference/getting-started.md#view-inference-metrics).

## Clean up

Delete the deployment before the gateway it's attached to. First, delete the deployment:

```bash theme={"system"}
curl -s -X DELETE "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

Then delete the gateway:

```bash theme={"system"}
curl -s -X DELETE "${CW_BASE_URL}/v1alpha1/inference/gateways/${CW_GATEWAY_ID}" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

After both commands succeed, no further charges accrue for the resources in this tutorial. The weights remain in your bucket, so if you no longer need them, delete them separately.

## Next steps

To take this deployment further, see the following resources:

* [Speculative decoding](https://docs.coreweave.com/products/inference/speculative-decoding.md): Apply the draft model pattern from this tutorial to your own model, including the keys each engine allows.
* [Models and deployments](https://docs.coreweave.com/products/inference/models.md): Tune runtime configuration, GPU selection, and traffic weights.
* [Scaling](https://docs.coreweave.com/products/inference/scaling.md): Move beyond a single replica with autoscaling and reserved capacity.
* [Gateways](https://docs.coreweave.com/products/inference/gateways.md): Configure authentication, routing strategies, and traffic splitting.
* [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md): Update a deployment, deploy with Terraform, and review the full API workflow.
* [Billing](https://docs.coreweave.com/products/inference/billing.md): Understand Dedicated Inference pricing.
