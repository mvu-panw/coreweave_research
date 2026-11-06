# Speculative decoding

Source: https://docs.coreweave.com/products/inference/speculative-decoding

# Speculative decoding

> Speculate tokens with a draft model to cut decode latency on a Dedicated Inference deployment

Speculative decoding reduces per-user decode latency by producing more than one token per decode step. A small, fast draft model proposes several tokens at once, and the target model verifies them all in a single forward pass. Accepted tokens are returned together. Rejected tokens are discarded and generation continues from the last accepted token, so the output distribution is unchanged.

The gain depends on how many proposed tokens the target model accepts. A low acceptance rate makes decoding slower than no speculation at all, so measure acceptance on your own traffic before you keep a configuration.

On Dedicated Inference, you configure speculative decoding through the `engineConfig` map of a deployment. Some methods need no extra weights. Methods that use a draft model need that draft model stored inside your model path in [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md), because a deployment reads from exactly one bucket and path.

Use this page if you already have a working deployment and want to reduce decode latency. For the fields that define a deployment, see [Models and deployments](https://docs.coreweave.com/products/inference/models.md). For a worked example that stages a draft model and serves it end to end, see [Deploy Kimi K3 on Dedicated Inference](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md), which pairs Kimi K3 with a DSpark draft model on 16 GB300 GPUs.

## Prerequisites

Before you configure speculative decoding, make sure you have:

* An engine version that allows the keys you plan to set. See [Configuration keys](#configuration-keys).
* If you're adding speculative decoding to a deployment that already exists, the complete deployment specification. Update requests replace the whole specification, so start from your current configuration and add only the speculative decoding keys.
* A [bucket policy](https://docs.coreweave.com/products/inference/models.md#grant-inference-access-to-your-bucket) granting inference access to your weights bucket. This is already in place for any deployment that starts successfully.
* For draft model methods, a draft model trained against the same base model and quantization your deployment serves, uploaded to your weights bucket.

## Choose a method

Set `speculative-config.method` to the vLLM speculative method you want. The choice determines whether you need to stage extra weights and which other keys apply, so make it before you configure a deployment.

`mtp` and `eagle3` cover most deployments. The following methods are the ones CoreWeave runs in production:

| Method | Extra weights | Use when |
| - | - | - |
| `mtp` | None. The head ships inside the model. | Your model has a built-in multi-token prediction head, as recent DeepSeek, GLM, and Qwen3-Next models do. This is the cheapest method to try, because there's nothing to stage. |
| `eagle`, `eagle3` | An EAGLE head stored with your weights | Your model has no MTP head, or you have an EAGLE head trained against it. EAGLE-3 is the current version and the more common choice. |
| `dflash`, `dspark` | A draft model stored with your weights | You have a DFlash or DSpark draft model for your target model. Both configure the same way as EAGLE. |
| `ngram` | None | Your workload repeats content between prompt and output. See the caveat in [Speculate without extra weights](#speculate-without-extra-weights) before choosing this. |

vLLM supports further methods, including `draft_model`, which pairs the target with a separate smaller model of the same family. It's a distinct method from EAGLE and is rarely the better choice, because an EAGLE head is smaller and cheaper to run. For the full list, see [Speculative decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/) in the vLLM documentation. Which methods work depends on your model and engine version, and CoreWeave validates the ones in the preceding table.

## Configuration keys

The speculative decoding keys use the dotted form `speculative-config.[FIELD]`. vLLM assembles the dotted keys into a single speculative configuration. Setting `speculative-config.method` to `ngram` and `speculative-config.num_speculative_tokens` to `5` is equivalent to passing `--speculative-config '{"method": "ngram", "num_speculative_tokens": 5}'` on the vLLM command line. All `engineConfig` values are strings, so quote numeric values such as `"num_speculative_tokens": "5"` rather than passing them as JSON numbers.

CoreWeave allows a specific set of `engineConfig` keys for each engine and engine version, and the two engines differ. The following keys are allowed for speculative decoding:

| Key | `dynamo-vllm` | `vllm` | Description |
| - | - | - | - |
| `speculative-config.method` | Yes | Yes | The speculative method to use, such as `ngram` or `eagle3`. When you set `speculative-config.model`, vLLM detects the method from the draft model's configuration where possible. |
| `speculative-config.model` | Yes | Yes | Path to the draft model, EAGLE head, or additional weights. On Dedicated Inference, this is a path inside the deployment's model mount. See [Store the draft model with your weights](#store-the-draft-model-with-your-weights). Omit it for `mtp` and `ngram`, which need no separate weights. |
| `speculative-config.num_speculative_tokens` | Yes | Yes | The number of tokens the draft model proposes per step. Defaults to the value in the draft model's configuration. Required when the draft model's configuration does not set one. |
| `speculative-config.draft_tensor_parallel_size` | Yes | Yes | Tensor parallel size for the draft model. Must be either `1` or the target model's tensor parallel size, which CoreWeave derives from `resources.gpuCount`. |
| `speculative-config.draft_sample_method` | Yes | No | How the draft model selects the tokens it proposes. Set to `greedy` to always take the draft model's highest-probability token, or `probabilistic` to sample from the draft model's distribution. |
| `speculative-config` | Yes | No | The complete speculative configuration as a single JSON object. See [Set the whole configuration as JSON](#set-the-whole-configuration-as-json). |
| `speculative-config.prompt_lookup_min` | No | Yes | Minimum n-gram window size for the `ngram` method. Defaults to the value of `speculative-config.prompt_lookup_max`, or to `5` when neither key is set. |
| `speculative-config.prompt_lookup_max` | No | Yes | Maximum n-gram window size for the `ngram` method. Defaults to the value of `speculative-config.prompt_lookup_min`, or to `5` when neither key is set. Must be greater than or equal to `speculative-config.prompt_lookup_min`. |
| `speculative-config.moe_backend` | No | Yes | The draft model's equivalent of the top-level `moe-backend` key, setting the mixture-of-experts kernel backend for the draft model rather than the target model. Available on engine version `0.19.0` and later. |
| `speculative-config.kv_cache_dtype` | No | Yes | The draft model's equivalent of the top-level `kv-cache-dtype` key, setting the KV cache data type for the draft model rather than the target model. Available on engine version `0.26.0+crwv.0` and later. |

Both engines support the `ngram` method, but only `vllm` lets you tune the n-gram window. On `dynamo-vllm`, `ngram` uses the default window of `5`.

Which keys a given deployment accepts also depends on the engine version you select. To get the authoritative list, set `CW_BASE_URL` and `CW_API_TOKEN` as described in [Getting started](https://docs.coreweave.com/products/inference/getting-started.md), then query the deployment parameters endpoint:

```bash theme={"system"}
curl "${CW_BASE_URL}/v1alpha1/inference/deployments/parameters" \
  -H "Authorization: Bearer ${CW_API_TOKEN}"
```

The deployment parameters endpoint returns the allowed keys for each engine under `runtimeParameters.runtimeConfigOptions`, and the available versions under `runtimeParameters.runtimeVersions`.

## Store the draft model with your weights

Draft model methods need the draft model inside your model path, because a deployment reads from exactly one bucket and path.

A deployment specifies one `model.bucket` and one `model.path`. When a replica starts, CoreWeave downloads everything under `s3://[BUCKET-NAME]/[MODEL-PATH]` into the model mount at `/tmp/model` inside the container. vLLM then loads the target model from `/tmp/model`. There's no separate field for a draft model bucket or path.

Store the draft model in a subdirectory of your model path. CoreWeave downloads that subdirectory with the rest of the weights, and vLLM can then address the draft model at the matching path under `/tmp/model`.

```text theme={"system"}
s3://[BUCKET-NAME]/
└── [MODEL-PATH]/                    <- model.path, mounted at /tmp/model
    ├── config.json
    ├── tokenizer.json
    ├── model-00001-of-00030.safetensors
    └── speculator/
        └── [DRAFT-MODEL-DIR]/       <- /tmp/model/speculator/[DRAFT-MODEL-DIR]
            ├── config.json
            └── model.safetensors
```

With this layout, set `speculative-config.model` to `/tmp/model/speculator/[DRAFT-MODEL-DIR]`.

You choose the subdirectory name. Nothing detects the draft model automatically, because `speculative-config.model` always names the path explicitly. `speculator/` is the convention CoreWeave uses for its own deployments. Versioning the draft model directory, for example `speculator/[DRAFT-MODEL-DIR]/v1`, lets you stage a replacement draft model in the same bucket before you switch a deployment over to it.

> [!NOTE]
>
> Because the draft model lives under the same prefix as the model weights, the [bucket policy](https://docs.coreweave.com/products/inference/models.md#grant-inference-access-to-your-bucket) that grants inference access to your weights already covers it. If you narrowed the policy to a prefix, confirm that the prefix includes the draft model directory.

## Configure a deployment

Set the speculative decoding keys in `runtime.engineConfig`. You can include them in the request that creates a deployment, which avoids an extra rollout, or add them to a deployment that already exists.

Adding them to an existing deployment restarts its replicas, which re-download the model weights before serving traffic again. Update requests also require the complete deployment specification, so start from your current configuration and add only the speculative decoding keys. For the full update request, see [Update a deployment](https://docs.coreweave.com/products/inference/getting-started.md#update-a-deployment).

In the following examples, replace `[ENGINE-VERSION]` with a version for your engine from the `runtimeParameters.runtimeVersions` field of the deployment parameters response.

### Speculate with a built-in MTP head

Models that ship a multi-token prediction head speculate with no extra weights. Set the method and the number of proposed tokens, and omit `speculative-config.model`, because the head is already part of the model you deployed:

```json theme={"system"}
"runtime": {
  "engine": "dynamo-vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": {
    "speculative-config.method": "mtp",
    "speculative-config.num_speculative_tokens": "5"
  }
}
```

This is the first thing to try on a model that has an MTP head. There's nothing to stage, nothing to train, and nothing to keep in sync with the target model.

### Speculate with a draft model

Draft model methods propose tokens with a small trained model stored alongside your weights. They generalize beyond repeated content and work on models with no MTP head, but they require a draft model matched to your target model.

CoreWeave runs the following draft model methods in production:

* `eagle` and `eagle3`: EAGLE heads. EAGLE-3 is the current version and the more common choice, and the following example uses it.
* `dflash`: DFlash draft models.
* `dspark`: DSpark draft models. For a worked example, see [Deploy Kimi K3 on Dedicated Inference](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md), which stages a separate `Inferact/Kimi-K3-DSpark` draft model under the Kimi K3 model path and serves both together.

All of them configure the same way. Replace `[DRAFT-MODEL-DIR]` with the draft model subdirectory described in [Store the draft model with your weights](#store-the-draft-model-with-your-weights). These four keys are allowed on both engines, so the same `engineConfig` works for either one:

```json theme={"system"}
"runtime": {
  "engine": "dynamo-vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": {
    "speculative-config.method": "eagle3",
    "speculative-config.model": "/tmp/model/speculator/[DRAFT-MODEL-DIR]",
    "speculative-config.num_speculative_tokens": "3",
    "speculative-config.draft_tensor_parallel_size": "1"
  }
}
```

Start with a low `num_speculative_tokens` and raise it while watching the acceptance rate. Proposing more tokens per step increases the potential gain, but also the compute wasted on rejected tokens.

Expect to bring your own draft model. A model provider can bundle a DFlash or DSpark head into the base checkpoint the way MTP models bundle theirs, but that's the exception. When a checkpoint does bundle one, you can use it by setting the method and omitting `speculative-config.model`, as in [Speculate with a built-in MTP head](#speculate-with-a-built-in-mtp-head), or point `speculative-config.model` at a draft model of your own instead.

### Speculate without extra weights

The `ngram` method proposes tokens by matching recent content against the prompt, so it needs no extra weights and no MTP head.

Because it matches strings rather than predicting tokens, `ngram` gains the least of the available methods, and on some models it loses. CoreWeave's own testing found that `ngram` made a mixture-of-experts model slower than no speculation at all. Prefer `mtp` if your model has a head for it, and treat `ngram` as a fallback for models that support neither `mtp` nor a draft model.

On `dynamo-vllm`, set the method and the number of proposed tokens:

```json theme={"system"}
"runtime": {
  "engine": "dynamo-vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": {
    "speculative-config.method": "ngram",
    "speculative-config.num_speculative_tokens": "5"
  }
}
```

On `vllm`, you can also tune the n-gram window:

```json theme={"system"}
"runtime": {
  "engine": "vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": {
    "speculative-config.method": "ngram",
    "speculative-config.num_speculative_tokens": "5",
    "speculative-config.prompt_lookup_min": "3",
    "speculative-config.prompt_lookup_max": "5"
  }
}
```

### Set the whole configuration as JSON

On `dynamo-vllm`, the bare `speculative-config` key takes the complete speculative configuration as one JSON object. Use it to set fields that have no dedicated dotted key:

```json theme={"system"}
"runtime": {
  "engine": "dynamo-vllm",
  "version": "[ENGINE-VERSION]",
  "engineConfig": {
    "speculative-config": "{\"method\": \"eagle3\", \"model\": \"/tmp/model/speculator/[DRAFT-MODEL-DIR]\", \"num_speculative_tokens\": 3}"
  }
}
```

CoreWeave validates the `speculative-config` key itself but doesn't validate the fields inside the JSON object. A misspelled field passes the deployment request and reaches the engine, which rejects unknown fields and fails to start. The failure surfaces as a deployment that never reaches `STATUS_READY` rather than as an API error, so prefer the dotted keys when one exists for the field you need.

## Monitor the acceptance rate

Speculative decoding reduces latency only when the target model accepts most proposed tokens. Rejected tokens still cost draft model compute, so a low acceptance rate makes decoding slower rather than faster.

To find the metrics, open [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md) and open the [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md) dashboard in the **Inference** folder. Its **Speculative Decoding** panel plots two series:

* **Acceptance Rate**: The fraction of proposed tokens the target model accepts.
* **Mean Acceptance Length**: The average number of tokens emitted per decode step, including the token the target model would have produced on its own. A value of `1` means the target model accepts no proposed tokens.

Before you keep the configuration, measure tokens per second on your own traffic both with and without speculation. Acceptance depends on the workload, so a draft model that performs well on one prompt distribution can underperform on another.

## Troubleshooting

The following errors and symptoms are specific to speculative decoding configuration.

### Deployment request rejects a speculative-config key

The API rejects the request with `invalid runtime config: [speculative-config.model]`, naming the keys it wouldn't accept.

The request used a key that isn't allowed for the selected engine and version. Confirm the exact spelling of the key, then check it against `runtimeParameters.runtimeConfigOptions` in the deployment parameters response for the engine and version you selected. The two engines allow different keys, so a key that works on `vllm` can be rejected on `dynamo-vllm` and the reverse. Engine versions also add keys over time.

### Deployment fails to start after you set a draft model path

The deployment reaches `STATUS_ERROR` or `STATUS_FAILED` instead of `STATUS_READY`.

The most common cause is the path itself. vLLM resolves the draft model path inside the container, not in the bucket, so verify that the value starts with `/tmp/model/` and that the remainder matches the draft model's location relative to `model.path`.

If the path is correct, the draft model may be incompatible with the target model rather than missing. A draft model built for a different base model, or for a different quantization of the same base model, can fail to load outright instead of merely speculating poorly.

Check `status.conditions` on the deployment, and review the engine logs as described in [Observability](https://docs.coreweave.com/products/inference/getting-started.md#observability).

### Acceptance rate is near zero

The draft model doesn't match the target model closely enough. Confirm that the draft model was trained against the same base model and quantization that the deployment serves, and that `speculative-config.method` matches the draft model's architecture.

## Next steps

* [Deploy Kimi K3 on Dedicated Inference](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md): A worked example that stages a DSpark draft model alongside the model weights and serves both on 16 GB300 GPUs.
* [Models and deployments](https://docs.coreweave.com/products/inference/models.md): Model configuration, engine configuration options, and GPU selection.
* [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md): Create a gateway, deployment, and first request.
* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md): Upload and manage the bucket that holds your weights.
