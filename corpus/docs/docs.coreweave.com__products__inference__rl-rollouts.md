# RL Rollouts

Source: https://docs.coreweave.com/products/inference/rl-rollouts

# RL Rollouts

> Generate reinforcement learning rollouts and load updated policy weights into a running deployment

RL Rollouts is a [CoreWeave Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md) capability for serving reinforcement learning (RL) rollouts and hot-loading updated policy weights. This guide uses the following terms:

* **Rollout:** In RL post-training, a response, or a sequence of responses, that the current policy generates for scoring and training.
* **Policy:** The model being optimized.
* **Hot-load:** Loading full or delta checkpoints from [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) into a running deployment without restarting the inference processes or recreating their replicas. The [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md), the Cloud Console, and CoreWeave error messages all use this term.

Your trainer generates and scores samples, updates the model, and publishes checkpoints. Dedicated Inference serves the rollouts and loads each new checkpoint, so you don't operate the serving stack yourself. RL Rollouts uses NVIDIA Dynamo with vLLM, configured with the `dynamo-vllm` runtime engine.

This guide shows you how to create a hot-load-enabled deployment, generate rollouts, publish full and delta checkpoints, and confirm that every replica is serving the new weights. It's for ML engineers running RL post-training who want CoreWeave to serve rollouts and load new weights. To run the training loop from a framework, or to replace this guide's API calls with single commands, see [Use the Inference Cookbook](#use-the-inference-cookbook).

> [!NOTE]
>
> RL Rollouts is in preview. Hot-loading is enabled per organization and requires the `dynamo-vllm` engine. The Dedicated Inference API is versioned as `v1alpha1` and might change before general availability.

## Prerequisites

Before you begin, make sure you have:

* A CoreWeave account with Dedicated Inference access enabled.
* Hot-loading enabled for your organization. This is gated separately from Dedicated Inference access. To request it, contact your CoreWeave representative or [CoreWeave support](https://docs.coreweave.com/support.md) with your organization ID. Until it's enabled, creating a deployment with a `hotLoad` section fails with `hot-load is not enabled for this organization`.
* Inference GPU quota for the instance type you plan to deploy on. To request quota, [submit a support ticket](https://coreweave.freshdesk.com/support/login).
* A CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) with the [Inference Admin role](https://docs.coreweave.com/security/iam/access-policies/roles.md#inference) to create deployments and start hot-loads. Polling hot-load and replica status needs only the Inference Viewer role.
* A [gateway](https://docs.coreweave.com/products/inference/gateways.md) through which your trainer can submit inference requests. To create one, see [Create a gateway](https://docs.coreweave.com/products/inference/getting-started.md#create-a-gateway). If the deployment uses more than one gateway, all of them must be in the same [zone](https://docs.coreweave.com/products/inference/gateways.md#zones), or creating a hot-load fails.
* An AI Object Storage bucket holding your starting model weights. To make one, see [Create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md), then [grant the Dedicated Inference service account read access to it](https://docs.coreweave.com/products/inference/getting-started.md#grant-inference-access-to-your-bucket) so the service can read your weights. Your trainer writes each new checkpoint to this same bucket as training proceeds, so the bucket policy must also allow `s3:PutObject` for the credentials your trainer uploads with. If you publish with `cwtrain`, those credentials also need `s3:ListBucket`, `s3:GetObject`, and `s3:AbortMultipartUpload`. For policy syntax, see [Bucket policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md). For an example policy that grants access to both the service and your trainer, see [`bucket-policy.example.json`](https://github.com/coreweave/inference-cookbook/blob/main/k8s/bucket-policy.example.json) in the Inference Cookbook.
* The AWS CLI [configured for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) with a profile named `cw`, for uploading checkpoints.
* `curl` and [`jq`](https://jqlang.org) for the API examples.
* A trainer that writes checkpoints in `.safetensors` format and can start hot-loads and poll their status, through the Dedicated Inference API or `cwtrain`.

You create the deployment itself as part of this guide, because hot-loading has to be configured when the deployment is created.

## How hot-loading fits your training loop

Your trainer runs rollout generation and weight updates as one loop:

1. Send inference requests to generate rollouts from the current policy.
2. Score the generated responses with your reward function.
3. Compute updated model weights.
4. Publish a checkpoint to AI Object Storage and start a hot-load through the Dedicated Inference API.
5. Generate further rollouts as replicas adopt the updated policy, and repeat.

CoreWeave manages rollout serving and weight loading. You manage the trainer, reward computation, checkpoint creation, and the policy-consistency requirements of your training algorithm.

### Checkpoint identities

Each checkpoint you publish needs an identity: a name you choose that the service appends to the deployment's hot-load path prefix to locate that checkpoint's files. Identities are single path segments, and a training loop typically derives them from the step number. In the following example, `step-000420` is the identity, and the `s3://` scheme refers to your S3-compatible AI Object Storage bucket:

```text theme={"system"}
s3://[BUCKET-NAME]/[PATH-PREFIX]/step-000420/
```

The Dedicated Inference API calls a checkpoint a snapshot, so fields such as `previousSnapshotIdentity` and `snapshotChain` refer to checkpoints. A hot-load operation has its own ID, separate from the checkpoint identity. Retrying a checkpoint creates another operation that targets the same identity.

### Full and delta checkpoints

The following table compares the two checkpoint types and when to use each:

| Type | Contents | When to use it |
| - | - | - |
| Full checkpoint | The complete model weights, as `.safetensors` shards plus `config.json` and `model.safetensors.index.json`. | Establish a baseline or start a new checkpoint chain. |
| Delta checkpoint | Incremental exclusive OR (XOR) changes relative to a previous checkpoint, as `.safetensors` shards plus `model.safetensors.index.json`. Deltas must use Zstandard compression and Adler-32 checksums. | Transfer the changes between training steps instead of another full checkpoint. |

A delta inherits the model configuration from its base checkpoint and depends on that base to be reconstructed. A full checkpoint followed by a sequence of deltas forms a checkpoint chain. For example, a full checkpoint at `step-000420`, followed by deltas at `step-000430` and `step-000440`, forms a chain whose reconstructed result is the policy at `step-000440`. Keep the baseline and every delta in the chain available in the bucket.

A chain holds at most 63 deltas. When you reach that limit, publish a full checkpoint to start a new chain.

Prepare checkpoints in a format and precision compatible with the serving deployment. When it admits a hot-load request, the service checks that every checkpoint in the resolved chain has its required files.

### Policy consistency during an update

A hot-load runs asynchronously, and during the transition, replicas might serve different checkpoints. Existing replicas go through a rolling update: replicas that aren't updating keep serving, and requests on an updating replica pause while its weights load. Replicas that restart or are added by scaling after the hot-load starts load the target checkpoint directly.

The hot-load's `promptCachePolicy` controls whether the key-value (KV) cache computed under the earlier weights is kept:

* `PROMPT_CACHE_POLICY_PRESERVE`, the default, keeps the KV cache. Requests that have already begun prefill or decoding resume with their existing cache after the update, so a request that spans an update can include computation under two sets of weights.
* `PROMPT_CACHE_POLICY_RESET_ALL` discards the KV cache when the update completes, so no cache entry computed under the earlier weights is reused. Use it when the next rollout round needs to start clean.

You can also [isolate new requests by policy version](#isolate-the-kv-cache-between-policy-versions) with `nvext.cache_salt`, independently of whether the hot-load preserves or clears the KV cache.

Replica status reports the checkpoint each replica serves. It doesn't identify the policy used for each token in a response.

If your training algorithm tolerates samples from different policy versions, you can keep submitting rollout requests during an update. If it requires strictly on-policy samples, pause between rollout rounds as described in [Run strictly on-policy rounds](#run-strictly-on-policy-rounds).

## Create a hot-load-enabled deployment

Create the deployment with `runtime.engine` set to `dynamo-vllm` and a `hotLoad` section that names the bucket and path prefix for your checkpoints. `dynamo-vllm` is the only engine that supports hot-loading.

> [!WARNING]
>
> The `hotLoad` configuration is immutable after the deployment is created. To add or change it, create a new deployment. When you update the deployment, include the same `hotLoad` section, because an update that omits or changes it is rejected.

To create the deployment in the [Cloud Console](https://console.coreweave.com) instead, use the **Hot loading** section of the create deployment drawer. It has an enable toggle and a checkpoint URI field, which the Console parses into the bucket and path prefix. Hot-loading is available only with the Dynamo vLLM runtime, and selecting another runtime shows an inline error. In the edit drawer, the toggle and URI are read-only. After the Console creates the deployment, complete step 1 of the following procedure, run `export CW_DEPLOYMENT_ID="[DEPLOYMENT-ID]"` with the deployment's ID, and continue from step 4.

To create the deployment with the API, follow these steps:

1. Set your API access token and the management API URL. Replace `[API-TOKEN]` with your CoreWeave API access token. The rest of this guide reuses these variables:

   ```bash theme={"system"}
   export CW_API_TOKEN="[API-TOKEN]"
   export CW_BASE_URL="https://api.coreweave.com"
   ```

2. Create the deployment. Replace `[GATEWAY-ID]` with the ID of your gateway. The [deployment parameters endpoint](https://docs.coreweave.com/products/inference/getting-started.md#create-a-deployment) returns valid values for `[ENGINE-VERSION]` and `[INSTANCE-TYPE]`. Replace `[MODEL-NAME]`, `[MODEL-PATH]`, `[BUCKET-NAME]`, and `[PATH-PREFIX]` with the values for your model weights and checkpoint location:

   ```bash theme={"system"}
   curl --fail-with-body -sS -X POST "${CW_BASE_URL}/v1alpha1/inference/deployments" \
     -H "Authorization: Bearer ${CW_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -o deployment-response.json \
     -d '{
       "name": "rl-policy-deployment",
       "gatewayIds": ["[GATEWAY-ID]"],
       "runtime": { "engine": "dynamo-vllm", "version": "[ENGINE-VERSION]" },
       "resources": { "instanceType": "[INSTANCE-TYPE]", "gpuCount": 1 },
       "model": { "name": "[MODEL-NAME]", "bucket": "[BUCKET-NAME]", "path": "[MODEL-PATH]" },
       "autoscaling": { "min": 3, "max": 3 },
       "traffic": { "weight": 100 },
       "hotLoad": {
         "bucket": "[BUCKET-NAME]",
         "pathPrefix": "[PATH-PREFIX]",
         "transitionMode": "TRANSITION_MODE_ASYNC"
       }
     }'
   ```

   `model` points at the weights the deployment starts from, and `hotLoad` points at the checkpoints your trainer publishes later. This example keeps both in one bucket, separated by path, but they can be different buckets. `TRANSITION_MODE_ASYNC` is the only supported transition mode.

3. Save the deployment ID from the response:

   ```bash theme={"system"}
   export CW_DEPLOYMENT_ID="$(jq -r '.deployment.spec.id' deployment-response.json)"
   echo "Deployment ID: ${CW_DEPLOYMENT_ID}"
   ```

   If the ID prints as `null`, the request failed, and `deployment-response.json` contains the error.

4. Wait for the deployment to reach `STATUS_READY`. For a polling loop, see [Wait for the deployment to start](https://docs.coreweave.com/products/inference/getting-started.md#wait-for-the-deployment-to-start).

5. To send rollout requests, export your gateway's primary endpoint URL, which is the first entry in `gateway.status.endpoints`. Replace `[GATEWAY-ID]` with the ID of your gateway:

   ```bash theme={"system"}
   export CW_GATEWAY_ENDPOINT="$(curl -sS "${CW_BASE_URL}/v1alpha1/inference/gateways/[GATEWAY-ID]" \
     -H "Authorization: Bearer ${CW_API_TOKEN}" | jq -r '.gateway.status.endpoints[0]')"
   echo "Gateway endpoint: ${CW_GATEWAY_ENDPOINT}"
   ```

## Generate rollouts

Your trainer collects samples from the current policy by sending rollout requests to the deployment. The following example request returns token IDs and log probabilities for training, helps keep a multi-turn trajectory on one worker, and isolates the KV cache by policy version. The sections after the example describe each setting.

Send each request to your gateway endpoint through the OpenAI-compatible chat completions API. Replace `[MODEL-NAME]` with your deployment's model name and `[POLICY-VERSION]` with your current policy version, such as a training step or checkpoint identity. For multi-turn rollouts, replace `[TRAJECTORY-ID]` with your trajectory ID. Otherwise, omit the session header.

```bash theme={"system"}
curl -s -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Dynamo-Session-ID: [TRAJECTORY-ID]" \
  -d '{
    "model": "[MODEL-NAME]",
    "messages": [
      {
        "role": "user",
        "content": "What is 17 times 23?"
      }
    ],
    "temperature": 1.0,
    "top_p": 1.0,
    "max_tokens": 256,
    "logprobs": true,
    "top_logprobs": 2,
    "nvext": {
      "cache_salt": "[POLICY-VERSION]"
    }
  }' | jq
```

Choose `top_p` for your sampling policy. This example uses `1.0` to disable nucleus sampling.

In the following response to the preceding request, the generated text and per-token details are truncated:

```json theme={"system"}
{
  "model": "[MODEL-NAME]",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's a thinking process:\n\n1.  **Identify the user's question:**..."
      },
      "logprobs": {
        "content": [
          {
            "token": "Here",
            "token_id": 11745,
            "logprob": -1.811964830267243e-05,
            "top_logprobs": [
              { "token": "Here", "logprob": -1.811964830267243e-05 },
              { "token": "The", "logprob": -11.250018119812012 }
            ]
          }
        ]
      }
    }
  ]
}
```

`message.content` contains the generated text. Your trainer computes rewards separately from the inference response.

For a mixture-of-experts (MoE) model, a deployment with routing capture enabled can also return the experts the router selected for each token. See [Return MoE routing data](#return-moe-routing-data).

### Token IDs and log probabilities

Set `temperature` above `0` and enable `logprobs`. Read the sampled token IDs from `choices[].logprobs.content[].token_id` and their log probabilities from the adjacent `logprob` field. Use these IDs directly for training.

Each `logprobs.content` entry describes a sampled token, and `top_logprobs` lists the top candidates at that position.

### Keep a trajectory on one worker

To help reuse the KV cache in multi-turn rollouts, send the same `X-Dynamo-Session-ID` on every request in a trajectory. Session affinity isn't guaranteed.

### Isolate the KV cache between policy versions

Set `nvext.cache_salt` to your current policy version. Reuse it while sampling that version, and change it after loading new weights to prevent reuse of KV cache from an earlier policy.

Changing the salt isolates new requests without clearing the KV cache. The hot-load setting `PROMPT_CACHE_POLICY_RESET_ALL` clears that cache when the update completes. You can use both controls together. For coordinating rollout rounds, follow [Run strictly on-policy rounds](#run-strictly-on-policy-rounds).

### Return MoE routing data

For an MoE model, the deployment can return the experts the router selected for every token, so your trainer can replay the same routing when it computes gradients. Routing capture is off by default. To turn it on, add `enable-return-routed-experts` with an empty value to `runtime.engineConfig` when you create or update the deployment:

```json theme={"system"}
"runtime": {
  "engine": "dynamo-vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": { "enable-return-routed-experts": "" }
}
```

When updating an existing deployment, keep its `hotLoad` section unchanged and wait for the deployment to become ready before requesting routing data.

You can't combine this option with pipeline parallelism, context parallelism, or a KV cache connector, such as one used for prefill and decode disaggregation.

To receive the routing data for a request, add `routed_experts` to `nvext.extra_fields`. This example also requests `completion_token_ids` to return sampled token IDs without enabling `logprobs`. That field requires one generated choice per request:

```bash theme={"system"}
curl -s -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "[MODEL-NAME]",
    "messages": [
      {
        "role": "user",
        "content": "What is 17 times 23?"
      }
    ],
    "temperature": 1.0,
    "max_tokens": 32,
    "nvext": { "extra_fields": ["routed_experts", "completion_token_ids"] }
  }' | jq '{usage, nvext}'
```

The response carries the routing data in the top-level `nvext.routed_experts` object. In this response, the base64 data and the token ID list are truncated:

```json theme={"system"}
{
  "usage": {
    "prompt_tokens": 26,
    "completion_tokens": 32,
    "total_tokens": 58
  },
  "nvext": {
    "completion_token_ids": [11745, 1681, 1261, "..."],
    "routed_experts": {
      "data": "AAAAAAAAJ28uADlDAAAAAAAA...",
      "shape": [57, 52, 6],
      "start": 0,
      "dtype": "uint8"
    }
  }
}
```

The `routed_experts` object has the following fields:

| Field | Data |
| - | - |
| `data` | The expert IDs as base64-encoded raw bytes in row-major order. |
| `shape` | `[tokens, layers, top_k]`. `tokens` is `prompt_tokens + completion_tokens - 1`, because the final sampled token is never run through the model. `layers` counts every decoder layer, and layers without an MoE block, such as the attention or Mamba layers of a hybrid model, contain zeros. `top_k` is the number of experts the router selects for each token. |
| `start` | The index of the first prompt token covered. A value of `0` means the routing data includes the full prompt. |
| `dtype` | `uint8` for models with at most 256 experts, `uint16` otherwise. |

Decode the array with NumPy:

```python theme={"system"}
import base64

import numpy as np

routed = response["nvext"]["routed_experts"]
experts = np.frombuffer(base64.b64decode(routed["data"]), dtype=routed["dtype"]).reshape(routed["shape"])
```

Routing data arrives on the final response or, in a streaming response, on the chunk that carries `finish_reason`.

## Load a full checkpoint

A full checkpoint starts a checkpoint chain, so the first checkpoint you hot-load onto a deployment is a full checkpoint. This example loads a full checkpoint with the identity `step-000420`.

1. Upload the checkpoint's `.safetensors` shards, `config.json`, and `model.safetensors.index.json` to a directory named for its identity. Replace `[LOCAL-CHECKPOINT-DIR]` with the local directory your trainer wrote the checkpoint to. Keep the files at the top level of that directory, because the service doesn't look for them in subdirectories:

   ```bash theme={"system"}
   aws s3 cp --recursive --profile cw \
     "[LOCAL-CHECKPOINT-DIR]" \
     "s3://[BUCKET-NAME]/[PATH-PREFIX]/step-000420/"
   ```

   If your trainer runs in a CoreWeave cluster, you can upload through the LOTA endpoint instead by adding `--endpoint-url http://cwlota.com` to the command. For endpoint settings, see [Configure endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md).

2. Write the `CreateHotLoad` request to `hot-load.json`:

   ```bash theme={"system"}
   cat > hot-load.json <<EOF
   {
     "deploymentId": "${CW_DEPLOYMENT_ID}",
     "identity": "step-000420",
     "type": "SNAPSHOT_TYPE_FULL",
     "promptCachePolicy": "PROMPT_CACHE_POLICY_PRESERVE"
   }
   EOF
   ```

   `identity` names the checkpoint directory beneath the configured path prefix. The bucket and path prefix come from the deployment configuration, so the request doesn't include a storage URL. `PROMPT_CACHE_POLICY_PRESERVE` keeps the KV cache through the transition, which is also the default if you omit `promptCachePolicy`. To discard the cache when the update completes, set `PROMPT_CACHE_POLICY_RESET_ALL`. For how each policy affects requests, see [Policy consistency during an update](#policy-consistency-during-an-update).

3. Submit the request and save the hot-load operation ID. The deployment must be in `STATUS_READY`, and no other hot-load can be running on it:

   ```bash theme={"system"}
   curl --fail-with-body -sS \
     -X POST "${CW_BASE_URL}/v1alpha1/inference/hotLoads" \
     -H "Authorization: Bearer ${CW_API_TOKEN}" \
     -H "Content-Type: application/json" \
     --data-binary @hot-load.json \
     -o hot-load-response.json

   export CW_HOT_LOAD_ID="$(jq -r '.hotLoad.spec.id' hot-load-response.json)"
   export CW_TARGET_IDENTITY="step-000420"
   echo "Hot-load ID: ${CW_HOT_LOAD_ID}"
   ```

   If the ID prints as `null`, the request failed, and `hot-load-response.json` contains the error. Receiving an operation ID means the service accepted the request, not that the replicas have loaded the weights.

4. [Wait for the hot-load to finish](#wait-for-the-hot-load-to-finish).

## Wait for the hot-load to finish

A hot-load is finished when the operation reaches a terminal state and every replica reports `READY` on the target identity. `GetHotLoad` reports the operation's aggregate state, and `ListHotLoadReplicas` reports each replica separately.

1. Poll the operation until it reaches a terminal state. This loop checks every 5 seconds and stops when the state is `HOT_LOAD_STATE_COMPLETED`, `HOT_LOAD_STATE_FAILED`, or `HOT_LOAD_STATE_CANCELED`, or after 15 minutes:

   ```bash theme={"system"}
   deadline=$(( $(date +%s) + 900 ))
   while [ "$(date +%s)" -lt "$deadline" ]; do
     state=$(curl --fail-with-body -sS "${CW_BASE_URL}/v1alpha1/inference/hotLoads/${CW_HOT_LOAD_ID}" \
       -H "Authorization: Bearer ${CW_API_TOKEN}" \
       | jq -r '.hotLoad.status.state // "UNKNOWN"')
     echo "Hot-load state: ${state}"
     case "${state}" in
       HOT_LOAD_STATE_COMPLETED|HOT_LOAD_STATE_FAILED|HOT_LOAD_STATE_CANCELED) break ;;
     esac
     sleep 5
   done
   case "${state}" in
     HOT_LOAD_STATE_COMPLETED) echo "Hot-load completed." ;;
     *) echo "Hot-load didn't complete. Last state: ${state}" ;;
   esac
   ```

   If the final state is `HOT_LOAD_STATE_FAILED` or `HOT_LOAD_STATE_CANCELED`, see [Recover a failed hot-load](#recover-a-failed-hot-load). If the operation is still `HOT_LOAD_STATE_PENDING` or `HOT_LOAD_STATE_IN_PROGRESS` when the loop stops, run the loop again.

2. Confirm that every replica serves the target checkpoint. Replica results are paginated, so this loop reads every page, prints each replica, and counts the replicas listed and the replicas that aren't ready on `CW_TARGET_IDENTITY`:

   ```bash theme={"system"}
   page_token=""
   total=0
   not_ready=0
   while true; do
     page=$(curl --fail-with-body -sS --get \
       "${CW_BASE_URL}/v1alpha1/inference/hotLoads/${CW_HOT_LOAD_ID}/replicas" \
       -H "Authorization: Bearer ${CW_API_TOKEN}" \
       --data-urlencode "maxPageSize=1000" \
       --data-urlencode "pageToken=${page_token}") || { echo "Request failed: ${page}"; not_ready="unknown"; break; }
     jq -r '(.replicas // [])[] | [.name, .state, .currentSnapshotIdentity, (.errorReason // "")] | @tsv' <<< "${page}"
     total=$(( total + $(jq '(.replicas // []) | length' <<< "${page}") ))
     not_ready=$(( not_ready + $(jq --arg id "${CW_TARGET_IDENTITY}" \
       '[(.replicas // [])[] | select(.state != "READY" or .currentSnapshotIdentity != $id)] | length' <<< "${page}") ))
     page_token=$(jq -r '.nextPageToken // ""' <<< "${page}")
     [ -z "${page_token}" ] && break
   done
   echo "Replicas listed: ${total}. Not ready on ${CW_TARGET_IDENTITY}: ${not_ready}"
   ```

   When at least one replica is listed and the not-ready count is `0`, every replica is serving the new checkpoint. A replica in `ERROR` state prints its `errorReason` in the last column.

For the full response bodies, see [Example responses](#example-responses).

## Load a delta checkpoint

Compute each delta checkpoint against a checkpoint that you already hot-loaded on the same deployment. This example loads `step-000430` as a delta against `step-000420`.

Your trainer writes the delta checkpoint. The following implementations write the format RL Rollouts accepts:

* **slime and miles:** These open source RL post-training frameworks write deltas from their disk-delta weight update mode. For slime's implementation, see its [delta checkpoint writer](https://github.com/THUDM/slime/blob/main/slime/backends/megatron_utils/update_weight/update_weight_from_disk_delta.py) and [Delta Weight Sync guide](https://github.com/THUDM/slime/blob/main/docs/en/advanced/delta-weight-sync.md). With either framework, set `--update-weight-delta-encoding xor` and `--update-weight-delta-checksum adler32`, because slime also supports encodings and checksums that RL Rollouts doesn't accept. The [slime recipe](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/slime) and [miles recipe](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/miles) in the Inference Cookbook list the full set of flags each framework needs.
* **Other trainers:** If your trainer saves full Hugging Face checkpoints, the `write_delta()` function in the `cwtrain.hotload.delta` module computes the delta between two of them. The [NeMo RL recipe](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/nemo-rl) uses it. To install `cwtrain`, see [Use the Inference Cookbook](#use-the-inference-cookbook).

A delta checkpoint directory holds one or more `.safetensors` shards and a `model.safetensors.index.json` file:

```text theme={"system"}
step-000430/
├── model-00000-of-00001.safetensors
└── model.safetensors.index.json
```

* **Shards:** Each changed tensor is stored as a byte-level XOR delta against the same tensor in the base checkpoint, compressed as its own Zstandard frame. The shard's safetensors `__metadata__` header maps each changed tensor's name to the Adler-32 checksum of its new full weight, which the service uses to verify the reconstructed tensor.
* **Index:** `weight_map` lists only the tensors that changed, and `metadata` describes the delta. The service identifies the delta and its base by the `identity` and `previousSnapshotIdentity` in your hot-load request, not by `version` and `base_version`, so those fields can hold other values, such as the zero-padded version numbers that slime writes:

  ```json theme={"system"}
  {
    "metadata": {
      "version": "step-000430",
      "base_version": "step-000420",
      "delta_encoding": "xor",
      "compression_format": "zstd",
      "checksum_format": "adler32"
    },
    "weight_map": {
      "model.language_model.embed_tokens.weight": "model-00000-of-00001.safetensors",
      "model.language_model.layers.0.mlp.down_proj.weight": "model-00000-of-00001.safetensors"
    }
  }
  ```

To check a delta directory before you upload it, you can run `cwtrain hotload inspect`. It validates the required files, the index, and the delta format offline, without credentials, but it doesn't verify checksums. Replace `[LOCAL-DELTA-DIR]` with the local directory your trainer wrote the delta to:

```bash theme={"system"}
cwtrain hotload inspect "[LOCAL-DELTA-DIR]" --previous-identity step-000420
```

To load the delta, follow these steps:

1. Upload the delta's `.safetensors` shards and `model.safetensors.index.json`. Replace `[LOCAL-DELTA-DIR]` with the local directory your trainer wrote the delta to, and keep the files at the top level of that directory:

   ```bash theme={"system"}
   aws s3 cp --recursive --profile cw \
     "[LOCAL-DELTA-DIR]" \
     "s3://[BUCKET-NAME]/[PATH-PREFIX]/step-000430/"
   ```

2. Write the request to `hot-load.json`:

   ```bash theme={"system"}
   cat > hot-load.json <<EOF
   {
     "deploymentId": "${CW_DEPLOYMENT_ID}",
     "identity": "step-000430",
     "type": "SNAPSHOT_TYPE_INCREMENTAL",
     "promptCachePolicy": "PROMPT_CACHE_POLICY_PRESERVE",
     "incrementalSnapshotMetadata": {
       "previousSnapshotIdentity": "step-000420",
       "compressionFormat": "COMPRESSION_FORMAT_ZSTD",
       "checksumFormat": "CHECKSUM_FORMAT_ADLER32"
     }
   }
   EOF
   ```

   `previousSnapshotIdentity` must name the checkpoint the delta was computed against, and that checkpoint must have a completed hot-load on this deployment. `COMPRESSION_FORMAT_ZSTD` and `CHECKSUM_FORMAT_ADLER32` are the only formats the service accepts, and your delta artifacts must use them.

3. Submit the request and save the new operation ID. If the ID prints as `null`, check `hot-load-response.json` for the error:

   ```bash theme={"system"}
   curl --fail-with-body -sS \
     -X POST "${CW_BASE_URL}/v1alpha1/inference/hotLoads" \
     -H "Authorization: Bearer ${CW_API_TOKEN}" \
     -H "Content-Type: application/json" \
     --data-binary @hot-load.json \
     -o hot-load-response.json

   export CW_HOT_LOAD_ID="$(jq -r '.hotLoad.spec.id' hot-load-response.json)"
   export CW_TARGET_IDENTITY="step-000430"
   echo "Hot-load ID: ${CW_HOT_LOAD_ID}"
   ```

4. To confirm that the delta loaded, run both loops in [Wait for the hot-load to finish](#wait-for-the-hot-load-to-finish) again.

## Run strictly on-policy rounds

If your training algorithm requires every sample in a round to come from one policy, coordinate the boundary between rounds:

1. Stop submitting new rollout requests and wait for the current round's requests and multi-turn trajectories to finish.
2. Publish the next checkpoint and start a hot-load, as in [Load a full checkpoint](#load-a-full-checkpoint) or [Load a delta checkpoint](#load-a-delta-checkpoint). To keep the next round from reusing KV cache computed under the previous policy, set `promptCachePolicy` to `PROMPT_CACHE_POLICY_RESET_ALL`.
3. [Wait for the hot-load to finish](#wait-for-the-hot-load-to-finish), including the replica check.
4. Resume rollout generation only after every replica is ready on the target checkpoint.

## Recover a failed hot-load

If an update stops before every replica loads the target checkpoint, the operation reaches `HOT_LOAD_STATE_FAILED`, and the replicas might serve different policy versions.

> [!WARNING]
>
> Keep on-policy rollout generation paused until every replica reports the target checkpoint. Replicas serving mixed checkpoints produce samples from more than one policy.

To recover, follow these steps:

1. Run the replica loop in [Wait for the hot-load to finish](#wait-for-the-hot-load-to-finish) to see each replica's loaded identity and `errorReason`.
2. Address the reported issue, such as an inaccessible checkpoint or a missing base artifact.
3. Start a new hot-load for the same checkpoint identity, or for another compatible checkpoint, such as a full checkpoint. A deployment runs one hot-load at a time, so the previous operation must be in a terminal state first, and the deployment must be in `STATUS_READY`. The same restriction blocks deployment configuration updates while a hot-load is running.
4. Repeat both checks in the wait procedure before you resume on-policy generation.

## Monitor hot-loads in the Cloud Console

The Console shows hot-load configuration and progress, and polls while an operation is running. It's read-only: start hot-loads through the API.

To track checkpoint adoption across replicas, follow these steps:

1. Open your deployment in the [Cloud Console](https://console.coreweave.com).
2. In the deployment details drawer, select the **Hot loads** tab.
3. Review the hot-load configuration: whether hot-loading is enabled, the checkpoint URI, and the transition behavior.
4. Review the operation. **Current hot load** covers pending and in-progress operations, and **Latest hot load** shows the newest completed, failed, or canceled one. Each reports the target checkpoint, snapshot type, status, and timestamps in your browser's local time.
5. Review **Replica convergence** for the count of ready replicas against the total, then the replica table for each replica's name, state, served checkpoint, zone, transition time, and error reason.

When no operation is running, the tab reports that no checkpoint update is in progress. If **Replica convergence** shows replicas on different checkpoints after an operation ends, see [Recover a failed hot-load](#recover-a-failed-hot-load).

## View hot-load history

To list a deployment's hot-loads, newest first:

```bash theme={"system"}
curl --fail-with-body -sS --get "${CW_BASE_URL}/v1alpha1/inference/hotLoads" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  --data-urlencode "parentDeploymentId=${CW_DEPLOYMENT_ID}" | jq
```

The history response is paginated. To retrieve the next page, pass the response's `nextPageToken` as `pageToken`, and keep the same `parentDeploymentId` filter. The final page omits `nextPageToken`.

## Use the Inference Cookbook

The [CoreWeave Inference Cookbook](https://github.com/coreweave/inference-cookbook) is an open source repository of RL recipes that train against a hot-load-enabled deployment. It also contains `cwtrain`, the Python library and CLI that the recipes share. `cwtrain` creates the deployment, publishes checkpoints, starts hot-loads, and waits until every replica serves the new weights, so your trainer doesn't make the API calls in this guide itself.

The cookbook has the following recipes:

| Recipe | What it runs |
| - | - |
| [miles](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/miles) | GRPO training with miles, synchronously or one step ahead. |
| [slime](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/slime) | GRPO training with slime. |
| [NeMo RL](https://github.com/coreweave/inference-cookbook/tree/main/training/recipes/nemo-rl) | GRPO training with NeMo RL. |
| [NeMo Gym](https://github.com/coreweave/inference-cookbook/tree/main/recipes/evaluation/nemo-gym) | Scored evaluation rollouts with NeMo Gym, against a deployment without hot-loading. |

The training recipes run on Kubernetes and include their own manifests. Each recipe's README lists the tested framework version and links to examples with prerequisites and deployment requests. The examples use [shared Kubernetes and storage files](https://github.com/coreweave/inference-cookbook/tree/main/k8s), including an example bucket policy.

### Publish checkpoints from your own training loop

To publish checkpoints from a training loop that the recipes don't cover, use `cwtrain` directly:

1. Install `cwtrain` from [PyPI](https://pypi.org/project/cwtrain/). It requires Python 3.12 or later:

   ```bash theme={"system"}
   pip install cwtrain
   ```

2. Configure access to your bucket. `cwtrain` reads the API access token from `CW_API_TOKEN`, which this guide exports, unless `COREWEAVE_API_TOKEN` is set. It reads your AI Object Storage credentials from the standard AWS configuration. To use the `cw` profile from the prerequisites, set `AWS_PROFILE`, and set `AWS_REGION` to your bucket's Availability Zone. Replace `[AVAILABILITY-ZONE]` with the zone, such as `US-EAST-04A`:

   ```bash theme={"system"}
   export AWS_PROFILE="cw"
   export AWS_REGION="[AVAILABILITY-ZONE]"
   ```

3. Save the deployment request body from [Create a hot-load-enabled deployment](#create-a-hot-load-enabled-deployment) as `deployment.json`. Then create the deployment, wait until it's ready, and save its ID. If you already created the deployment, export its ID as `CW_DEPLOYMENT_ID` instead:

   ```bash theme={"system"}
   export CW_DEPLOYMENT_ID="$(cwtrain deployment create --file deployment.json --wait | jq -r '.id')"
   echo "Deployment ID: ${CW_DEPLOYMENT_ID}"
   ```

4. Check that your credentials have the permissions `cwtrain` needs on the deployment's hot-load path prefix: `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`, and `s3:AbortMultipartUpload`. The check leaves no objects in the bucket, and if a permission is missing, its error names that permission:

   ```bash theme={"system"}
   cwtrain hotload check --deployment "${CW_DEPLOYMENT_ID}"
   ```

The following `cwtrain` commands replace the hot-load API calls in this guide. Each prints its result as JSON:

| Task | Command |
| - | - |
| Upload a full checkpoint, start its hot-load, and wait for every replica | `cwtrain hotload publish --deployment "${CW_DEPLOYMENT_ID}" --checkpoint "[LOCAL-CHECKPOINT-DIR]" --identity step-000420` |
| Upload a delta checkpoint, start its hot-load, and wait for every replica | `cwtrain hotload publish --deployment "${CW_DEPLOYMENT_ID}" --checkpoint "[LOCAL-DELTA-DIR]" --identity step-000430 --previous-identity step-000420` |
| Start a hot-load for a full checkpoint that's already in the bucket | `cwtrain hotload trigger --deployment "${CW_DEPLOYMENT_ID}" --identity step-000420` |
| [Wait for the hot-load to finish](#wait-for-the-hot-load-to-finish) | `cwtrain hotload wait "${CW_HOT_LOAD_ID}"` |
| Show each replica's state and served checkpoint | `cwtrain hotload status "${CW_HOT_LOAD_ID}"` |
| [View hot-load history](#view-hot-load-history) | `cwtrain hotload list --deployment "${CW_DEPLOYMENT_ID}"` |

`publish` validates the checkpoint directory and uploads it under the deployment's hot-load path prefix before it starts the hot-load. To start a hot-load for a delta with `trigger`, add `--previous-identity`. To discard the KV cache when the update completes, add `--reset-prompt-cache` to `publish` or `trigger`, which sets `PROMPT_CACHE_POLICY_RESET_ALL`.

`publish` and `trigger` wait for the hot-load by default. To return as soon as the service accepts it, add `--no-wait`, and pass the hot-load ID from the output's `spec.id` field to `wait` later. If a hot-load fails, the command exits with status `1`.

`list` shows the 20 most recent hot-loads. To show more, add `--limit`.

To publish from Python instead, use `HotLoader`. Replace `[LOCAL-CHECKPOINT-DIR]` with the local directory your trainer wrote the checkpoint to:

```python theme={"system"}
import os

from cwtrain import HotLoader, InferenceClient

loader = HotLoader(InferenceClient(), deployment_id=os.environ["CW_DEPLOYMENT_ID"])
hot_load = loader.publish("[LOCAL-CHECKPOINT-DIR]", identity="step-000420")
print(hot_load.state.name)
```

`publish()` returns when the hot-load reaches `COMPLETED`, which means every replica serves the checkpoint. If the hot-load fails, is canceled, or times out, `publish()` raises an exception instead. For every command, option, and Python class, see the [`cwtrain` README](https://github.com/coreweave/inference-cookbook/blob/main/libs/cwtrain/README.md). To report a problem with the recipes or `cwtrain`, open an issue in the [Inference Cookbook repository](https://github.com/coreweave/inference-cookbook/issues).

## Reference

The following sections list the hot-load API operations and states, with example responses.

### Hot-load API endpoints

The management API at `https://api.coreweave.com` defines these hot-load operations:

| Operation | Method | Path |
| - | - | - |
| `CreateHotLoad` | `POST` | `/v1alpha1/inference/hotLoads` |
| `GetHotLoad` | `GET` | `/v1alpha1/inference/hotLoads/{id}` |
| `ListHotLoadReplicas` | `GET` | `/v1alpha1/inference/hotLoads/{hotLoadId}/replicas` |
| `ListHotLoads` | `GET` | `/v1alpha1/inference/hotLoads` |

### Hot-load states

`hotLoad.status.state` reports the operation's aggregate state:

| State | Meaning |
| - | - |
| `HOT_LOAD_STATE_PENDING` | Accepted, but replica transitions haven't started. |
| `HOT_LOAD_STATE_IN_PROGRESS` | Replica transitions are underway. |
| `HOT_LOAD_STATE_COMPLETED` | Every replica serves the target checkpoint. Terminal. |
| `HOT_LOAD_STATE_FAILED` | The operation stopped before every replica reached the target checkpoint. Terminal. |
| `HOT_LOAD_STATE_CANCELED` | Canceled before completion. Terminal. Replicas might serve different checkpoints until a later hot-load completes. |

### Replica states

Each entry in a `ListHotLoadReplicas` response reports one replica's `state`:

| State | Meaning |
| - | - |
| `PENDING_UPDATE` | The replica serves a different checkpoint, and its transition hasn't started. |
| `UPDATING` | The replica's transition is in progress. |
| `READY` | The replica serves the target checkpoint. |
| `ERROR` | The replica's transition failed. The entry includes an `errorReason`. |

### Example responses

These examples show a delta hot-load for `step-000430` partway through the update.

`GetHotLoad` returns the operation's specification, the resolved checkpoint chain (`snapshotChain`), and the aggregate state. The chain lists the full baseline first, followed by each delta needed to reconstruct the target. It doesn't include replica status:

```json theme={"system"}
{
  "hotLoad": {
    "spec": {
      "id": "d4e5f6a7-b8c9-0123-def0-234567890123",
      "deploymentId": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "organizationId": "[ORG-ID]",
      "identity": "step-000430",
      "type": "SNAPSHOT_TYPE_INCREMENTAL",
      "incrementalSnapshotMetadata": {
        "previousSnapshotIdentity": "step-000420",
        "compressionFormat": "COMPRESSION_FORMAT_ZSTD",
        "checksumFormat": "CHECKSUM_FORMAT_ADLER32"
      },
      "promptCachePolicy": "PROMPT_CACHE_POLICY_PRESERVE",
      "snapshotChain": [
        {
          "identity": "step-000420",
          "type": "SNAPSHOT_TYPE_FULL",
          "hotLoadId": "c3d4e5f6-a7b8-9012-cdef-123456789012"
        },
        {
          "identity": "step-000430",
          "type": "SNAPSHOT_TYPE_INCREMENTAL",
          "compressionFormat": "COMPRESSION_FORMAT_ZSTD",
          "checksumFormat": "CHECKSUM_FORMAT_ADLER32",
          "hotLoadId": "d4e5f6a7-b8c9-0123-def0-234567890123"
        }
      ]
    },
    "status": {
      "createdAt": "2026-09-14T20:14:58Z",
      "updatedAt": "2026-09-14T20:17:41Z",
      "state": "HOT_LOAD_STATE_IN_PROGRESS"
    }
  }
}
```

`ListHotLoadReplicas` reports the checkpoint each replica currently serves, so a rolling update shows replicas in different states:

```json theme={"system"}
{
  "replicas": [
    {
      "name": "replica-e5f6a7b8-c9d0-1234-ef01-345678901234",
      "currentSnapshotIdentity": "step-000430",
      "state": "READY",
      "zone": "US-EAST-04A",
      "startedAt": "2026-09-14T20:15:04Z",
      "finishedAt": "2026-09-14T20:17:40Z",
      "transitionedAt": "2026-09-14T20:17:40Z"
    },
    {
      "name": "replica-f6a7b8c9-d0e1-2345-f012-456789012345",
      "currentSnapshotIdentity": "step-000420",
      "state": "UPDATING",
      "zone": "US-EAST-04A",
      "startedAt": "2026-09-14T20:17:41Z",
      "transitionedAt": "2026-09-14T20:17:41Z"
    },
    {
      "name": "replica-a7b8c9d0-e1f2-3456-0123-567890123456",
      "currentSnapshotIdentity": "step-000420",
      "state": "PENDING_UPDATE",
      "zone": "US-EAST-04A",
      "transitionedAt": "2026-09-14T20:12:03Z"
    }
  ]
}
```

## Next steps

* [CoreWeave Inference Cookbook](https://github.com/coreweave/inference-cookbook): Run RL recipes for miles, slime, and NeMo RL against a hot-load-enabled deployment, and publish checkpoints with `cwtrain`.
* [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md): Create the gateway and grant the bucket access that this guide depends on.
* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md): Configure the bucket that holds your checkpoints.
* [Run torchforge on SUNK](https://docs.coreweave.com/products/sunk/tutorials/torchforge-on-sunk.md): Run a GRPO training loop on CoreWeave.
* [Scaling](https://docs.coreweave.com/products/inference/scaling.md): Autoscaling and capacity behavior for the deployment you hot-load into.
