# Getting started with Dedicated Inference

Source: https://docs.coreweave.com/products/inference/getting-started

# Getting started with Dedicated Inference

> Create a gateway, deploy a model, and send your first Dedicated Inference request

This guide walks you through deploying your first model on [CoreWeave Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md), the Bring Your Own Weights (BYOW) option for serving models on dedicated GPU infrastructure. It targets developers and ML engineers who want to serve their own model weights on managed GPU instances without operating the underlying serving stack. By the end, you have a running inference endpoint that responds to prompts through the OpenAI-compatible API. You can then integrate the endpoint into applications that already target OpenAI-style chat completions. For an overview of CoreWeave's inference offerings, see the [Inference introduction](https://docs.coreweave.com/products/inference.md).

## Prerequisites

Before you begin, verify that you have the following:

* A CoreWeave account with Dedicated Inference access enabled.
* Inference GPU quota for the instance type you plan to deploy on. This quota is granted per organization and per instance type, and doesn't vary by zone, so one grant covers every zone your gateways target. Without it, creating a deployment fails with `organization has no GPU quota for it`, and setting `capacityClasses` doesn't waive the requirement. To request quota, [submit a support ticket](https://coreweave.freshdesk.com/support/login). This is separate from the [CKS instance quota](https://docs.coreweave.com/products/cks/clusters/quotas.md), which is dimensioned by zone and compute class.
* A CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) with the [Inference Admin role](https://docs.coreweave.com/security/iam/access-policies.md).
* Model weights uploaded to a [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) bucket. Dedicated Inference uses a bring-your-own-weights (BYOW) model. Download model weights from your model provider and upload them to AI Object Storage before starting.
* The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`), which this guide uses for its primary examples. The guide also shows the equivalent `curl` requests and a [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md) configuration, so you can use `curl` or Terraform instead.
* `curl`, which the final inference request uses even if you create resources with the CLI or Terraform.
* [Terraform](https://developer.hashicorp.com/terraform/install) or [OpenTofu](https://opentofu.org/docs/intro/install/), only if you use the Terraform path. Running `terraform init` installs the [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md) from the registry.

> [!NOTE]
>
> Want to interact with the API programmatically? See the [Dedicated Inference API reference](https://docs.coreweave.com/products/inference/reference/api-overview.md) for the REST, gRPC, and Connect interfaces, or install a generated client from the [Inference SDKs](https://buf.build/coreweave/inference/sdks/main%3Aconnectrpc).

## Set your API token

Set your API token as an environment variable so that subsequent commands can authenticate with the CoreWeave API. Replace `[API-TOKEN]` with your token. For details about creating a token, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

```bash theme={"system"}
export CW_API_TOKEN="[API-TOKEN]"
export CW_BASE_URL="https://api.coreweave.com"
```

> [tab] CoreWeave Intelligent CLI
>
> Authenticate `cwic` once. It stores the token in `~/.cwic/config.json` and reuses it for every subsequent `cwic inference` command.
>
> ```bash theme={"system"}
> cwic auth login "${CW_API_TOKEN}"
> ```
>
> To open `console.coreweave.com/tokens` in your browser and paste a different token interactively, run the command without an argument:
>
> ```bash theme={"system"}
> cwic auth login
> ```
>
> Verify you're authenticated:
>
> ```bash theme={"system"}
> cwic auth whoami
> ```

> [tab] curl
>
> The exported `CW_API_TOKEN` and `CW_BASE_URL` variables authenticate the `curl` examples in this guide.

## Grant inference access to your bucket

Dedicated Inference reads model weights from CoreWeave AI Object Storage using the Dedicated Inference service account. Attach a bucket policy to your weights bucket so the service can list and read its contents.

Attaching any bucket policy changes how requests to the bucket are evaluated. With no policy, requests allowed by your organization access policies are *implicitly* allowed. Once you attach a policy, only requests it explicitly allows are permitted, including requests from users in your own organization. A policy that grants only the inference service account therefore locks your own users out of the bucket with `AccessDenied` errors, including in the Cloud Console's bucket viewer.

To keep your own access, include a statement for your organization, as shown in the following example. If you do get locked out anyway, you can still overwrite the policy, because `s3:PutBucketPolicy` is evaluated only against organization access policies. For details, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

Replace `[BUCKET-NAME]` with the name of the bucket containing your model weights. Replace `[ORG-ID]` with your CoreWeave organization ID, which you can find on the [Settings page](https://console.coreweave.com/account/settings) of the Cloud Console. This policy grants read access to the inference service account and to all users in your organization:

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
> Always include the `Condition` block in the `AllowOrgUsers` statement when using `"Principal": "*"`. Without it, the bucket is readable by anyone on the internet, not just principals in your organization.

If you don't need your own organization's users to access the bucket directly, you can omit the `AllowOrgUsers` statement.

Save the policy to a file (for example, `inference-bucket-policy.json`) and apply it with the AWS CLI. If you have configured a [named AWS CLI profile](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md#set-coreweave-specific-configurations) for CoreWeave (for example, `cw`), pass it with `--profile [PROFILE-NAME]`. Omit `--profile` if your CoreWeave credentials are in the `default` profile.

```bash theme={"system"}
aws s3api put-bucket-policy \
  --bucket [BUCKET-NAME] \
  --policy file://inference-bucket-policy.json \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

Policy changes can take a few moments to propagate. Confirm the policy applied by fetching it back:

```bash theme={"system"}
aws s3api get-bucket-policy \
  --bucket [BUCKET-NAME] \
  --endpoint-url https://cwobject.com \
  --profile [PROFILE-NAME]
```

The response includes both the `AllowInference` and `AllowOrgUsers` statements once the policy propagates. At that point, the inference service account can list and read the bucket's contents, and your organization's users retain access if you kept the `AllowOrgUsers` statement.

> [!NOTE]
>
> The `Principal` in the `AllowInference` statement is the canonical Dedicated Inference service account and is the same for all customers. A missing bucket policy is the most common cause of deployments that fail to load weights. For tooling alternatives (s3cmd, Boto3, Terraform), how to scope access to a specific path prefix, and notes on the Cloud Console, see [Grant inference access to your bucket](https://docs.coreweave.com/products/inference/models.md#grant-inference-access-to-your-bucket).

## Create a gateway

With the bucket policy in place, provision the gateway. A [gateway](https://docs.coreweave.com/products/inference/gateways.md) provides the external endpoint that routes traffic to your model deployments. It handles authentication and load balancing.

> [!NOTE]
>
> Prefer to manage both resources as code? Skip ahead to [Deploy with Terraform](#deploy-with-terraform). You still run the `parameters` queries in this section and [Create a deployment](#create-a-deployment) to choose valid zone, instance type, and engine version values.

First, query the available zones so you can place the gateway in a region where Dedicated Inference capacity is offered:

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference gateway parameters
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/gateways/parameters" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```
>
> The response's `zones` array lists the zones currently available for gateway creation.

> [!NOTE]
>
> If this first request fails, check the `message` field. Both of the following errors return gRPC code `7` (HTTP 403):
>
> * `"organization is not allowed to perform this operation"`: your organization isn't enabled for Dedicated Inference yet. Contact your CoreWeave representative or [CoreWeave support](https://docs.coreweave.com/support.md) with your organization ID to request access.
> * `"insufficient permissions for this operation"`: your API access token is missing the [Inference Admin role](https://docs.coreweave.com/security/iam/access-policies.md). Add the role to the token's identity, then retry.

Then create a gateway in one of the available zones listed in the previous step. Replace `[ZONE-NAME]` with a zone from the response.

The gateway `name` must be a valid hostname label containing no more than 38 letters, digits, or hyphens. It must begin and end with a letter or digit, and it cannot contain dots. The 38-character limit accommodates DNS and TLS certificate constraints. If the hostname-label validation fails, you receive `validation error: name: must be a valid hostname label`.

This example creates a gateway with CoreWeave IAM authentication and body-based routing, which routes requests based on the `model` field in the request body. Body-based routing is the default and follows OpenAI API conventions.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference gateway create \
>   --name my-first-gateway \
>   --zones [ZONE-NAME] \
>   --auth coreweave \
>   --routing body \
>   --api-type openai
> ```
>
> The output is a table with the new gateway's `ID`, `NAME`, `ZONES`, `AUTH`, `ROUTING`, `STATUS`, and `ENDPOINTS` columns. Save the value from the `ID` column for the next step. You need this ID to associate deployments with the gateway. Add `-o json` to get the same fields as machine-readable JSON.

> [tab] curl
>
> ```bash theme={"system"}
> curl -s -X POST "${CW_BASE_URL}/v1alpha1/inference/gateways" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "name": "my-first-gateway",
>     "zones": ["[ZONE-NAME]"],
>     "coreWeaveAuth": {},
>     "bodyBasedRouting": {
>       "apiType": "API_TYPE_OPENAI"
>     }
>   }' | jq
> ```
>
> The response includes the gateway specification and creation timestamps. The `status.status` and `endpoints` fields appear on subsequent `GET` requests once the gateway is provisioned.
>
> ```json theme={"system"}
> {
>   "gateway": {
>     "spec": {
>       "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
>       "name": "my-first-gateway",
>       "organizationId": "[ORG-UID]",
>       "zones": ["US-EAST-04A"],
>       "coreWeaveAuth": {},
>       "bodyBasedRouting": {
>         "apiType": "API_TYPE_OPENAI"
>       }
>     },
>     "status": {
>       "createdAt": "2026-04-14T12:00:00Z",
>       "updatedAt": "2026-04-14T12:00:00Z"
>     }
>   }
> }
> ```
>
> Save the gateway ID from `gateway.spec.id` for the next step. You need this ID to associate deployments with the gateway.

> [!NOTE]
>
> If the create request returns `{"code":8, "message":"gateway quota exceeded: maximum is 0"}` (HTTP 429), your organization has no inference gateway quota. Contact your CoreWeave representative or [CoreWeave support](https://docs.coreweave.com/support.md) to request inference quota for your organization.

Either way, export the gateway ID:

```bash theme={"system"}
export CW_GATEWAY_ID="[GATEWAY-ID]"
```

You now have a gateway that can accept inference traffic but doesn't yet route to any model. The next section attaches a deployment to it.

> [!NOTE]
>
> The gateway may take a few moments to become ready. You can check its status with a `GET` request to `/v1alpha1/inference/gateways/{id}`, or with `cwic inference gateway get [GATEWAY-ID]`.

### View all gateways

You can view all existing gateways with the following command. Use it to confirm your gateway was created correctly.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference gateway list
> ```

> [tab] curl
>
> Parse the output with [`jq`](https://jqlang.org) to make the response more readable.
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/gateways" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```

## Create a deployment

A [deployment](https://docs.coreweave.com/products/inference/models.md) configures a model serving instance with your chosen runtime, GPU type, and model weights. Attaching the deployment to the gateway you just created makes the model reachable through the gateway endpoint.

First, query the available instance types and runtime versions so you can pick a GPU type and runtime that match your model:

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment parameters
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/deployments/parameters" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```

The response lists the gateway IDs that can be referenced by a new deployment under `gatewayIds`. It also groups the available options into two objects: `resourceParameters.instanceTypes` lists the GPU instance types you can deploy on, and `runtimeParameters.runtimeVersions` lists the available versions for each engine (such as `vllm` and `dynamo-vllm`).

Use these to choose a valid `[GATEWAY-ID]`, `[INSTANCE-TYPE]`, and `[ENGINE-VERSION]` below. If `resourceParameters` or `instanceTypes` is empty, no instance type is currently available for the request. Confirm that your organization has an eligible gateway and inference quota. When you filter by gateway IDs, also confirm that the selected gateways share an available instance type. Additional environment variables (such as `VLLM_*`) can be set through the deployment's runtime configuration to tune logging, compilation, and networking. The parameters endpoint returns the exact allow list for each engine version.

Then create a deployment that references your gateway. Replace the placeholder values:

* `[GATEWAY-ID]`: The gateway ID from the previous step (creating the gateway, or the `inference/gateways` list command).
* `[INSTANCE-TYPE]`: An instance type from the `inference/deployments/parameters` response in the previous step. For details on each type, see [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md).
* `[MODEL-NAME]`: A name for your model (from 4 to 63 characters). The gateway uses this name to route inference requests to this deployment.
* `[BUCKET-NAME]`: The CoreWeave AI Object Storage bucket containing the model weights.
* `[MODEL-PATH]`: The path within the bucket to the model directory.
* `[ENGINE-VERSION]`: The `vllm` or `dynamo-vllm` runtime version to serve your model with. The `inference/deployments/parameters` response (above) returns the available versions.

The deployment and model names serve different purposes and follow different validation rules:

* **Deployment `name`**: Identifies the deployment in the management API. It must be a valid hostname label containing no more than 63 letters, digits, or hyphens. It must begin and end with a letter or digit, and it cannot contain dots.
* **Model `name`**: Identifies the model in inference requests. It must be 4 to 63 characters long and can include letters, digits, periods, underscores, colons, slashes, and hyphens.

If the deployment `name` fails validation, you receive `validation error: name: must be a valid hostname label`.

> [!NOTE]
>
> An S3 path breaks down into `[BUCKET-NAME]` and `[MODEL-PATH]`. For example, `s3://test-bucket/raw/Qwen/Qwen3.5-0.8B/2fc06364715b967f1860aea9cf38778875588b17` breaks down into:
>
> ```text theme={"system"}
> [BUCKET-NAME]  test-bucket
> [MODEL-PATH]   raw/Qwen/Qwen3.5-0.8B/2fc06364715b967f1860aea9cf38778875588b17
> ```

If you receive `{"code":3, "message":"model path has no objects: path ..."}`, the model path is invalid or inaccessible.

If you receive `{"code":3, "message":"model bucket is not accessible..."}`, the bucket is invalid or inaccessible.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment create \
>   --name my-first-deployment \
>   --gateway-ids ${CW_GATEWAY_ID} \
>   --engine vllm \
>   --engine-version [ENGINE-VERSION] \
>   --instance-type [INSTANCE-TYPE] \
>   --gpu-count 1 \
>   --model-name [MODEL-NAME] \
>   --model-bucket [BUCKET-NAME] \
>   --model-path [MODEL-PATH] \
>   --min 1 \
>   --max 1 \
>   --traffic-weight 100
> ```
>
> The `--traffic-weight` flag has no effect for a single deployment: it controls traffic splitting only when two or more deployments share the same model name on a gateway. Leave the value at `100` for this guide. For details, see [Traffic weights](https://docs.coreweave.com/products/inference/models.md#traffic-weights).
>
> The output is a table that includes the new deployment's `ID` and `STATUS` columns. Save the value from the `ID` column so subsequent commands can reference the deployment. Add `-o json` to get the same fields as machine-readable JSON.

> [tab] curl
>
> ```bash theme={"system"}
> curl -s -X POST "${CW_BASE_URL}/v1alpha1/inference/deployments" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "name": "my-first-deployment",
>     "gatewayIds": ["[GATEWAY-ID]"],
>     "runtime": {
>       "engine": "vllm",
>       "version": "[ENGINE-VERSION]"
>     },
>     "resources": {
>       "instanceType": "[INSTANCE-TYPE]",
>       "gpuCount": 1
>     },
>     "model": {
>       "name": "[MODEL-NAME]",
>       "bucket": "[BUCKET-NAME]",
>       "path": "[MODEL-PATH]"
>     },
>     "autoscaling": {
>       "min": 1,
>       "max": 1
>     },
>     "traffic": {
>       "weight": 100
>     }
>   }' | jq
> ```
>
> The `traffic.weight` field has no effect for a single deployment: it controls traffic splitting only when two or more deployments share the same model name on a gateway. Leave the value at `100` for this guide. For details, see [Traffic weights](https://docs.coreweave.com/products/inference/models.md#traffic-weights).
>
> The response includes the deployment ID and creation timestamps. The `status.status` field appears when you poll the deployment with a `GET` request.
>
> ```json theme={"system"}
> {
>   "deployment": {
>     "spec": {
>       "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
>       "name": "my-first-deployment",
>       "organizationId": "[ORG-UID]",
>       "gatewayIds": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
>       "runtime": { "engine": "vllm", "version": "[ENGINE-VERSION]" },
>       "resources": { "instanceType": "gd-8xh100ib-i128", "gpuCount": 1 },
>       "model": { "name": "my-model", "bucket": "my-bucket", "path": "models/my-model/" },
>       "autoscaling": { "min": 1, "max": 1 },
>       "traffic": { "weight": 100 }
>     },
>     "status": {
>       "createdAt": "2026-04-14T12:10:00Z",
>       "updatedAt": "2026-04-14T12:10:00Z"
>     }
>   }
> }
> ```
>
> Save the deployment ID from `deployment.spec.id` so subsequent commands can reference the deployment.

Either way, export the deployment ID:

```bash theme={"system"}
export CW_DEPLOYMENT_ID="[DEPLOYMENT-ID]"
```

The deployment is registered, but the inference engine isn't yet serving traffic. The next section covers monitoring it until it becomes ready.

### View all deployments

You can view all existing deployments with the following command. Use it to confirm your deployment was created correctly.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment list
> ```

> [tab] curl
>
> Parse the output with [`jq`](https://jqlang.org) to make the response more readable.
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/deployments" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```

## Configure the engine

Two engines are supported: `dynamo-vllm` \[recommended] and `vllm`. The `dynamo-vllm` engine wraps vLLM with the [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) orchestrator. It accepts many of the same core vLLM options as the `vllm` engine (see [Engine configuration options](https://docs.coreweave.com/products/inference/models.md#engine-configuration-options)), with enhancements such as kv-cache-aware routing and many others. For models that need reasoning or tool-call parsing, `dynamo-vllm` also supports Dynamo-specific keys such as `dyn-reasoning-parser` and `dyn-tool-call-parser`. Note that the `vllm` engine is scheduled for deprecation.

Select the engine by setting `runtime.engine` to `dynamo-vllm` or `vllm` and their engine configurations using `runtime.engineConfig` and `runtime.engineEnv` when creating a deployment. Query the available `runtimeVersions.<engine>.versions` and the full allowed key list from the deployment parameters endpoint (`/v1alpha1/inference/deployments/parameters`). The response returns the entire list under `runtimeParameters.runtimeConfigOptions.<engine>.allowedKeys`, and `runtimeParameters.engineEnvOptions.<engine>.allowedNames`.

Set `[REASONING-PARSER]` and `[TOOL-CALL-PARSER]` to the parser names that match your model, such as `qwen3` or `deepseek_r1` for reasoning and `llama3_json` or `qwen3_coder` for tool calls. See [Runtime configuration](https://docs.coreweave.com/products/inference/models.md#runtime-configuration) for the full list.

> [!WARNING]
>
> In-place update of `runtime.engine` will incur brief service disruption. To ensure zero downtime, create a new deployment with the new runtime and the same gateway and model.name, then shift traffic from the old deployment to the new deployment via `traffic-weight`.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment create \
>   --name my-dynamo-deployment \
>   --gateway-ids ${CW_GATEWAY_ID} \
>   --engine dynamo-vllm \
>   --engine-version [ENGINE-VERSION] \
>   --instance-type [INSTANCE-TYPE] \
>   --gpu-count 1 \
>   --model-name [MODEL-NAME] \
>   --model-bucket [BUCKET-NAME] \
>   --model-path [MODEL-PATH] \
>   --min 1 \
>   --max 1 \
>   --traffic-weight 100
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -s -X POST "${CW_BASE_URL}/v1alpha1/inference/deployments" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "name": "my-dynamo-deployment",
>     "gatewayIds": ["[GATEWAY-ID]"],
>     "runtime": {
>       "engine": "dynamo-vllm",
>       "version": "[ENGINE-VERSION]",
>       "engineConfig": {
>         "dyn-reasoning-parser": "[REASONING-PARSER]",
>         "dyn-tool-call-parser": "[TOOL-CALL-PARSER]",
>         "max-model-len": "262144"
>       }
>     },
>     "resources": { "instanceType": "[INSTANCE-TYPE]", "gpuCount": 1 },
>     "model": { "name": "[MODEL-NAME]", "bucket": "[BUCKET-NAME]", "path": "[MODEL-PATH]" },
>     "autoscaling": { "min": 1, "max": 1, "concurrency": 32 },
>     "traffic": { "weight": 100 }
>   }'
> ```

## Deploy with Terraform

The previous two sections created a gateway and a deployment by calling the API directly. If you manage infrastructure as code, you can define both resources in a single [Terraform](https://docs.coreweave.com/platform/terraform.md) configuration and apply them together instead. This section shows a minimal configuration. For the full Terraform workflow, including multiple deployments, importing resources you created outside Terraform, and state management, see [Deploy Dedicated Inference with Terraform](https://docs.coreweave.com/products/inference/deploy-with-terraform.md).

> [!NOTE]
>
> If you already created your gateway and deployment with the CLI or `curl`, skip this section and continue at [Wait for the deployment to start](#wait-for-the-deployment-to-start). If you are starting here, first run the gateway and deployment `parameters` queries from [Create a gateway](#create-a-gateway) and [Create a deployment](#create-a-deployment) to choose valid zone, instance type, and engine version values.

When prompted, enter values corresponding to `[ZONE-NAME]`, `[ENGINE-VERSION]`, `[INSTANCE-TYPE]`, `[MODEL-NAME]`, `[BUCKET-NAME]`, and `[MODEL-PATH]`, using the same guidance as the API examples above.

The configuration declares each value as a required variable. When you run `terraform apply`, Terraform prompts you to enter the corresponding value without the brackets.

```terraform title="main.tf" theme={"system"}
terraform {
  required_providers {
    coreweave = {
      source = "coreweave/coreweave"
    }
  }
}

variable "zone_name" {
  type        = string
  description = "Zone returned by the inference gateway parameters endpoint."
}

variable "engine_version" {
  type        = string
  description = "vLLM version returned by the inference deployment parameters endpoint."
}

variable "instance_type" {
  type        = string
  description = "GPU instance type returned by the inference deployment parameters endpoint."
}

variable "model_name" {
  type        = string
  description = "Model name used to route inference requests."
}

variable "bucket_name" {
  type        = string
  description = "Object Storage bucket containing the model weights."
}

variable "model_path" {
  type        = string
  description = "Path to the model directory within the bucket."
}

resource "coreweave_inference_gateway" "example" {
  name  = "my-first-gateway"
  zones = [var.zone_name]

  auth = {
    coreweave = {}
  }

  routing = {
    body_based = {
      api_type = "API_TYPE_OPENAI"
    }
  }
}

resource "coreweave_inference_deployment" "example" {
  name        = "my-first-deployment"
  gateway_ids = [coreweave_inference_gateway.example.id]

  runtime = {
    engine  = "vllm"
    version = var.engine_version
  }

  resources = {
    instance_type = var.instance_type
    gpu_count     = 1
  }

  model = {
    name   = var.model_name
    bucket = var.bucket_name
    path   = var.model_path
  }

  autoscaling = {
    min = 1
    max = 1
  }

  traffic = {
    weight = 100
  }
}

output "gateway_id" {
  value = coreweave_inference_gateway.example.id
}

output "gateway_endpoint" {
  value = one(coreweave_inference_gateway.example.endpoints)
}

output "deployment_id" {
  value = coreweave_inference_deployment.example.id
}
```

Because the deployment's `gateway_ids` field references the gateway resource's `id` attribute, Terraform creates the gateway first and the deployment second, even though both are defined in the same configuration.

```bash theme={"system"}
export COREWEAVE_API_TOKEN="${CW_API_TOKEN}"
terraform init
terraform apply
```

Export the resulting IDs so you can continue with the rest of this guide:

```bash theme={"system"}
export CW_GATEWAY_ID=$(terraform output -raw gateway_id)
export CW_DEPLOYMENT_ID=$(terraform output -raw deployment_id)
```

For the full resource schema, including optional fields like autoscaling capacity classes and gateway routing modes, see the [`coreweave_inference_gateway`](https://docs.coreweave.com/platform/terraform/resources/inference_gateway) and [`coreweave_inference_deployment`](https://docs.coreweave.com/platform/terraform/resources/inference_deployment) resource references.

## Wait for the deployment to start

After creation, the deployment loads model weights and starts the inference engine. Poll the deployment status until it reaches `STATUS_READY`. This typically takes several minutes. Larger models on more GPUs take longer, and the inference engine has up to an hour to finish starting.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment get ${CW_DEPLOYMENT_ID}
> ```
>
> Repeat the command and check the `STATUS` column until it shows `READY`.

> [tab] curl
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```
>
> Check `deployment.status.status` in the response. Continue polling until you see `STATUS_READY`:
>
> ```json theme={"system"}
> {
>   "deployment": {
>     "status": {
>       "status": "STATUS_READY"
>     }
>   }
> }
> ```
>
> To poll automatically, use this loop. It stops when the deployment reaches `STATUS_READY`, fails with `STATUS_FAILED`, or reaches the 15-minute timeout, and then prints the result. `STATUS_ERROR` can clear on its own, so the loop keeps polling through it. If the loop times out while the deployment is still starting, run it again:
>
> ```bash theme={"system"}
> deadline=$(( $(date +%s) + 900 ))
> while [ "$(date +%s)" -lt "$deadline" ]; do
>   status_deployment=$(curl -sS "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
>     -H "Authorization: Bearer ${CW_API_TOKEN}" \
>     | jq -r '.deployment.status.status // "UNKNOWN"')
>   echo "Status: $status_deployment"
>   case "$status_deployment" in
>     STATUS_READY|STATUS_FAILED) break ;;
>   esac
>   sleep 30
> done
>
> case "$status_deployment" in
>   STATUS_READY) echo "Deployment is ready." ;;
>   STATUS_FAILED) echo "Deployment failed." ;;
>   *) echo "Timed out waiting for the deployment to become ready. Last status: $status_deployment" ;;
> esac
> ```
>
> This loop uses [`jq`](https://jqlang.org) to parse the response. Install `jq` with your package manager (for example, `brew install jq` on macOS or `apt install jq` on Debian or Ubuntu).

Once the deployment is running, retrieve the gateway endpoint URL:

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference gateway get ${CW_GATEWAY_ID}
> ```
>
> The endpoint URL appears in the `ENDPOINTS` column.

> [tab] curl
>
> ```bash theme={"system"}
> curl -s "${CW_BASE_URL}/v1alpha1/inference/gateways/${CW_GATEWAY_ID}" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" | jq
> ```

The `gateway.status.endpoints` field contains an array of endpoint URLs for inference requests. The first entry is the primary endpoint:

```json theme={"system"}
{
  "gateway": {
    "status": {
      "status": "STATUS_READY",
      "endpoints": ["https://my-first-gateway.[ORG-ID].gw.cwinference.com"]
    }
  }
}
```

Export the endpoint for the next step. Replace `[GATEWAY-ENDPOINT]` with the endpoint URL from the response above:

```bash theme={"system"}
export CW_GATEWAY_ENDPOINT="[GATEWAY-ENDPOINT]"
```

> [!NOTE]
>
> The gateway's public DNS record and TLS certificate provision asynchronously while the gateway is created. Wait until the gateway reaches `STATUS_READY` and exposes an endpoint. If your first inference request fails with an SSL handshake error or DNS resolution failure, wait a few minutes and retry.

## Send an inference request

With the deployment ready and the gateway endpoint exported, you can now send your first inference request to verify the end-to-end path. The gateway exposes an OpenAI-compatible API. With body-based routing, the gateway routes requests based on the `model` field in the request body. Send a chat completion request using the model name from your deployment:

```bash theme={"system"}
curl -s -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${CW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "[MODEL-NAME]",
    "messages": [
      {
        "role": "user",
        "content": "What is CoreWeave?"
      }
    ],
    "max_tokens": 256
  }' | jq
```

The same CoreWeave API access token used for the management API authenticates inference requests when the gateway uses `coreWeaveAuth`.

The response is an OpenAI-compatible chat completion. Beyond the standard fields, vLLM also returns several engine-specific fields (`token_ids`, `prompt_logprobs`, `kv_transfer_params`, and others). These are typically `null` for normal requests, so you can ignore them.

```json theme={"system"}
{
  "id": "chatcmpl-bcbcbae71847bf87",
  "object": "chat.completion",
  "created": 1777477750,
  "model": "[MODEL-NAME]",
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

A successful response confirms that your gateway and deployment are working. Alternatively, use the Python `openai` library:

```python theme={"system"}
from openai import OpenAI

client = OpenAI(
    base_url="[GATEWAY-ENDPOINT]/v1/",
    api_key="[API-TOKEN]",
)

response = client.chat.completions.create(
    model="[MODEL-NAME]",
    messages=[
        {"role": "user", "content": "What is CoreWeave?"},
    ],
    max_tokens=256,
)
print(response.choices[0].message.content)
```

## Update a deployment

Over time, you may need to adjust capacity, swap the GPU type, or point the deployment at new model weights. To change a deployment's configuration, send a `PATCH` request with the complete deployment specification. All fields are required, not just the ones you change. Omitting a field either fails validation (for required fields) or reverts it to its default, so start from the command you used to create the deployment and change only the fields you want to update. If the deployment has a `hotLoad` section for RL Rollouts, include it unchanged, because an update that omits or changes it is rejected.

This example increases the autoscaling maximum from 1 to 4:

> [!WARNING]
>
> Changing `model.name` changes the route key that clients send to the gateway. Update clients to use the new model name after the deployment update completes.
>
> In-place updates of `model.name` and `model.path` recreate routing and incur service disruption. Changing `model.path` reloads model weights and can also disrupt serving. To avoid downtime, create a new deployment then shift traffic to the new deployment.

> [tab] CoreWeave Intelligent CLI
>
> Like the REST `PATCH` request, `cwic inference deployment update` sends the complete deployment specification. Omitted flags revert to their default, so re-specify every flag from the create command and change only the ones you want to update. The CLI has no flag for the `hotLoad` section, so update a deployment that has one with the REST `PATCH` request instead:
>
> ```bash theme={"system"}
> cwic inference deployment update ${CW_DEPLOYMENT_ID} \
>   --name my-first-deployment \
>   --gateway-ids ${CW_GATEWAY_ID} \
>   --engine vllm \
>   --engine-version [ENGINE-VERSION] \
>   --instance-type [INSTANCE-TYPE] \
>   --gpu-count 1 \
>   --model-name [MODEL-NAME] \
>   --model-bucket [BUCKET-NAME] \
>   --model-path [MODEL-PATH] \
>   --min 1 \
>   --max 4 \
>   --traffic-weight 100
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -s -X PATCH "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "id": "[DEPLOYMENT-ID]",
>     "name": "my-first-deployment",
>     "gatewayIds": ["[GATEWAY-ID]"],
>     "runtime": {
>       "engine": "vllm",
>       "version": "[ENGINE-VERSION]"
>     },
>     "resources": {
>       "instanceType": "[INSTANCE-TYPE]",
>       "gpuCount": 1
>     },
>     "model": {
>       "name": "[MODEL-NAME]",
>       "bucket": "[BUCKET-NAME]",
>       "path": "[MODEL-PATH]"
>     },
>     "autoscaling": {
>       "min": 1,
>       "max": 4
>     },
>     "traffic": {
>       "weight": 100
>     }
>   }' | jq
> ```

> [!NOTE]
>
> If you created the deployment with Terraform, change the `coreweave_inference_deployment` resource block and run `terraform apply` instead of calling the API directly.

## Observability

CoreWeave Grafana provides an inference dashboard and access to deployment logs. Any user signed in to the Cloud Console can open Grafana, but seeing metrics and logs data requires the **Observability Viewer** role in an [IAM access policy](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry). Without this role, dashboards show no data. The Administrator, User, and Viewer [default access policies](https://docs.coreweave.com/security/iam/access-policies.md#default-access-policies) include **Observability Viewer**.

### View inference metrics

To view the Inference Model Overview dashboard:

1. Sign in to the [Cloud Console](https://console.coreweave.com) and open **Grafana** under **Observability**.

2. In Grafana, select **Home**, then **Dashboards**.

3. Open the **Inference** folder and select **Inference Model Overview**.

4. Use the dashboard variables to select your zone, gateway, model, and deployment.

The dashboard groups its panels into the following rows. For a description of every panel, see [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md).

* **Overview**: request rate (**RPS**), **Model Success Rate**, **Instances Active**, **Output Tok/s**, **Request Duration**, **Completed Request Rate**, **Running Requests**, and average cache usage.
* **Queue & Load Balancing**: **Queue Success Rate**, the rates of expired, failed, and canceled requests, and **Cumulative Queue Backlog**.
* **VLLM**: **Request Queue Time**, **Prefill Time**, **Decode Time**, **E2E Latency**, **TTFT** (time to first token), **TPOT** (time per output token), and prompt and generation token counts.
* **Scaling**: **Replicas**, **Instances Active (Count)**, and **Instances Active (Percent)**, which show the autoscaling behavior described in [Scaling](https://docs.coreweave.com/products/inference/scaling.md).
* **Per Pod**: running and waiting requests for each Pod, cache usage and cache hit rate, and **GPU Utilization** and **GPU Memory Utilization**.

GPU metrics are scoped to the Pods in your deployment, so the dashboard doesn't include Node-level metrics or a Pod-to-Node mapping. For programmatic access to the underlying metrics, see [Query logs and metrics](https://docs.coreweave.com/observability/logs-metrics/introduction.md).

### View deployment logs

The dashboard links directly to your logs. Set **Log Source** to **CoreWeave Logs**, then select **vLLM Logs** at the top of the dashboard, alongside the dashboard variables. Grafana opens Explore in a new tab with a query already scoped to your current **Deployment** selection.

The **Log Source** variable has no default, and its list includes audit log data sources that don't hold deployment logs. If Explore returns no results, confirm that **Log Source** names a deployment log source.

To write the query yourself instead:

1. Sign in to the [Cloud Console](https://console.coreweave.com) and open **Grafana** under **Observability**.

2. In Grafana, select **Explore** in the left navigation, then select **CoreWeave Logs** from the data source dropdown.

3. In the query builder, select **Code**, then enter the following query:

   ```text theme={"system"}
   {cluster="cwinference", container="vllm-server"}
   ```

4. Select **Run query** in the top-right corner to view the logs.

This query returns logs for every deployment in your organization. To narrow it to one deployment, add a `deployment` matcher. Replace `[DEPLOYMENT-ID]` with the ID returned when you created the deployment:

```text theme={"system"}
{cluster="cwinference", container="vllm-server", deployment="[DEPLOYMENT-ID]"}
```

## Clean up

When you no longer need the inference endpoint, delete the resources to stop incurring charges. You must delete deployments before their associated gateway.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference deployment delete ${CW_DEPLOYMENT_ID}
> ```
>
> ```bash theme={"system"}
> cwic inference gateway delete ${CW_GATEWAY_ID}
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -X DELETE "${CW_BASE_URL}/v1alpha1/inference/deployments/${CW_DEPLOYMENT_ID}" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}"
> ```
>
> ```bash theme={"system"}
> curl -X DELETE "${CW_BASE_URL}/v1alpha1/inference/gateways/${CW_GATEWAY_ID}" \
>   -H "Authorization: Bearer ${CW_API_TOKEN}"
> ```

> [!NOTE]
>
> If you created these resources with Terraform, run `terraform destroy` instead.

After the deployment and gateway are deleted, the inference resources from this guide no longer incur usage charges.

## Next steps

You now have a working baseline: a gateway, a deployment serving a model, and a successful inference response. Explore these resources to learn more about Dedicated Inference and to take the deployment beyond a single-replica baseline.

* [Deploy Kimi K3](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md): Follow a worked example that serves a large mixture-of-experts model with expert parallelism and speculative decoding.
* [Gateways](https://docs.coreweave.com/products/inference/gateways.md): Configure authentication, routing strategies, and traffic splitting.
* [Models and deployments](https://docs.coreweave.com/products/inference/models.md): Learn about runtime configuration, GPU selection, and deployment options.
* [Scaling](https://docs.coreweave.com/products/inference/scaling.md): Configure autoscaling and reserve GPU capacity.
* [Billing](https://docs.coreweave.com/products/inference/billing.md): Understand pricing and optimize inference costs.
* [Dedicated Inference API reference](https://docs.coreweave.com/products/inference/reference/api-overview.md): Explore the full API surface.
* [Schema and SDKs](https://docs.coreweave.com/products/inference/reference/api-overview.md#schema-and-sdks): Install a generated client for Go, Python, TypeScript, or another supported language instead of calling the API with `curl`.
* [CoreWeave Provider](https://docs.coreweave.com/platform/terraform.md): Explore the full Terraform resource and data source schema for Inference.
