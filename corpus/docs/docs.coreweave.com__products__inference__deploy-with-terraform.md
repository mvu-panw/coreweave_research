# Deploy Dedicated Inference with Terraform

Source: https://docs.coreweave.com/products/inference/deploy-with-terraform

# Deploy Dedicated Inference with Terraform

> Manage Dedicated Inference gateways and deployments as code with the CoreWeave Terraform provider

This guide shows how to deploy a model on [CoreWeave Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md) using [Terraform](https://developer.hashicorp.com/terraform) instead of individual API calls. You describe the gateway and the deployment you want, and Terraform creates them, tracks them, and tears them down in the right order. This guide supplements [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md), which walks through the same resources using the CoreWeave Intelligent CLI and `curl`.

By the end, you have a running inference endpoint managed as code: a *gateway* that provides the public, OpenAI-compatible endpoint, and a *deployment* that serves your model behind it. Because the deployment references the gateway's `id` attribute, Terraform creates the gateway first and destroys it last.

## Prerequisites

Before you begin, verify that you have the following:

* A CoreWeave account with Dedicated Inference access enabled.
* A CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) with the [Inference Admin role](https://docs.coreweave.com/security/iam/access-policies/roles.md#inference).
* Model weights uploaded to a [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) bucket. To create a bucket, see [Create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md).
* A bucket policy that grants the inference service account read and list access to your weights bucket. Follow [Grant inference access to your bucket](https://docs.coreweave.com/products/inference/getting-started.md#grant-inference-access-to-your-bucket) before you continue. A missing bucket policy is the most common cause of deployments that fail to load weights.
* [Terraform](https://developer.hashicorp.com/terraform/install) 1.5 or later, or [OpenTofu](https://opentofu.org/docs/intro/install/). The [Adopt existing resources](#adopt-existing-resources) section uses `import` blocks and configuration generation, which require Terraform 1.5.
* `curl` to send a test inference request, and [`jq`](https://jqlang.org) to format JSON responses in the `curl` examples.
* Optional: The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`). This guide shows `cwic` commands and equivalent `curl` requests for the steps that query the CoreWeave API directly.

## Set your API token

Set your API token as an environment variable. The [CoreWeave Terraform provider](https://docs.coreweave.com/platform/terraform.md) reads `COREWEAVE_API_TOKEN` automatically, so you don't need to reference the token anywhere in your configuration. Replace `[API-TOKEN]` with your token.

```bash theme={"system"}
export COREWEAVE_API_TOKEN="[API-TOKEN]"
```

Don't put the token in a `.tf` file or commit it to version control. Your token determines which organization Terraform operates on.

## Check available parameters

Zones, instance types, and engine versions differ by organization and change over time, so don't copy values from documentation. Query the parameters endpoints and use the results when you fill in variable values in the next section.

> [tab] CoreWeave Intelligent CLI
>
> ```bash theme={"system"}
> cwic inference gateway parameters
> cwic inference deployment parameters
> ```

> [tab] curl
>
> ```bash theme={"system"}
> curl -s "https://api.coreweave.com/v1alpha1/inference/gateways/parameters" \
>   -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}" | jq
>
> curl -s "https://api.coreweave.com/v1alpha1/inference/deployments/parameters" \
>   -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}" | jq
> ```

The gateway parameters response lists the available zones. The deployment parameters response lists the available instance types under `resourceParameters.instanceTypes`, the available versions for each engine under `runtimeParameters.runtimeVersions`, and the allowed `engine_config` keys under `runtimeParameters.runtimeConfigOptions`. For guidance on interpreting these values, see [Create a deployment](https://docs.coreweave.com/products/inference/getting-started.md#create-a-deployment) in the Getting started guide.

> [!NOTE]
>
> The provider also exposes these queries as data sources, so you can read them from within a Terraform configuration. See the [`coreweave_inference_gateway_parameters`](https://docs.coreweave.com/platform/terraform/data-sources/inference_gateway_parameters) and [`coreweave_inference_deployment_parameters`](https://docs.coreweave.com/platform/terraform/data-sources/inference_deployment_parameters) references.

## Create the configuration

Create a new directory with four files. Splitting the configuration this way keeps versions, inputs, resources, and outputs separate as your configuration grows. However, Terraform reads all `.tf` files in the directory regardless of how you divide them.

### `versions.tf`

Pins the Terraform and provider versions, and configures the provider. The provider block is empty because the provider reads your token from the `COREWEAVE_API_TOKEN` environment variable.

```terraform title="versions.tf" theme={"system"}
terraform {
  required_version = ">= 1.5"

  required_providers {
    coreweave = {
      source  = "coreweave/coreweave"
      version = "~> 0.19"
    }
  }
}

provider "coreweave" {}
```

### `variables.tf`

Declares the values that differ by organization and model. Terraform prompts for each value when you run `terraform plan` or `terraform apply`, or reads them from a `terraform.tfvars` file if you create one.

```terraform title="variables.tf" theme={"system"}
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
```

To avoid retyping values on every run, create a `terraform.tfvars` file. Replace the bracketed placeholders with values from [Check available parameters](#check-available-parameters) and the location of your model weights. An S3 path such as `s3://test-bucket/raw/Qwen/Qwen3.5-0.8B/2fc06364715b967f1860aea9cf38778875588b17` breaks down into a `bucket_name` of `test-bucket` and a `model_path` of `raw/Qwen/Qwen3.5-0.8B/2fc06364715b967f1860aea9cf38778875588b17`.

```terraform title="terraform.tfvars" theme={"system"}
zone_name      = "[ZONE-NAME]"
engine_version = "[ENGINE-VERSION]"
instance_type  = "[INSTANCE-TYPE]"
model_name     = "[MODEL-NAME]"
bucket_name    = "[BUCKET-NAME]"
model_path     = "[MODEL-PATH]"
```

### `main.tf`

Declares the gateway and the deployment. This is the file you edit to add or change models.

```terraform title="main.tf" theme={"system"}
resource "coreweave_inference_gateway" "main" {
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

resource "coreweave_inference_deployment" "main" {
  name        = "my-first-deployment"
  gateway_ids = [coreweave_inference_gateway.main.id]

  model = {
    name   = var.model_name
    bucket = var.bucket_name
    path   = var.model_path
  }

  runtime = {
    engine  = "vllm"
    version = var.engine_version

    engine_config = {
      "max-model-len" = "8192"
    }
  }

  resources = {
    instance_type = var.instance_type
    gpu_count     = 1
  }

  autoscaling = {
    min         = 1
    max         = 3
    concurrency = 16
  }

  traffic = {
    weight = 100
  }
}
```

> [!WARNING]
>
> Always set `runtime.version` explicitly. The provider schema marks it as optional and documents a default of the latest available version, but the API rejects configurations that omit it. The `terraform plan` step succeeds and `terraform apply` fails with `Error: invalid_argument: validation error: runtime.version: value is required`.

### `outputs.tf`

Surfaces the endpoint URL, resource IDs, and deployment status after apply.

```terraform title="outputs.tf" theme={"system"}
output "gateway_id" {
  value = coreweave_inference_gateway.main.id
}

output "gateway_endpoint" {
  value = one(coreweave_inference_gateway.main.endpoints)
}

output "deployment_id" {
  value = coreweave_inference_deployment.main.id
}

output "deployment_status" {
  value = coreweave_inference_deployment.main.status
}
```

### Configuration notes

The following table explains the configuration fields that most often need attention:

| Field | Notes |
| - | - |
| `zones` | Where the gateway lives. Limits where deployments associated with the gateway can run. |
| `auth.coreweave = {}` | Selects CoreWeave IAM authentication. The empty braces are the selection, not a placeholder. Exactly one of `coreweave` or `weights_and_biases` must be set. |
| `routing.body_based` | Routes requests by the `model` field in the request body, following OpenAI API conventions. The alternatives are `header_based` and `path_based`. See [Gateways](https://docs.coreweave.com/products/inference/gateways.md). |
| `model.name` | The name clients send in the `model` field of inference requests. It's independent of the storage path. |
| `engine_config` | Engine-specific options. All values are strings, and an empty string passes the key as a valueless flag. Keys are validated against the engine version, so a key that is valid on a newer engine version might be rejected on an older one. |
| `gpu_count` | GPUs per replica, not the size of the underlying node. Must be 1, 2, 4, 8, or 16. Size it to the model, not to the instance type name. |
| `autoscaling.concurrency` | Target in-flight requests per replica. Lower values favor latency, and higher values favor throughput. See [Scaling](https://docs.coreweave.com/products/inference/scaling.md). |
| `traffic.weight` | Has no effect for a single deployment. When two or more deployments share a model name on a gateway, the gateway normalizes their weights (0 to 1000) into percentages and splits traffic in that proportion. Setting a weight of `0` stops traffic to a deployment without deleting it. For details, see [Traffic weights](https://docs.coreweave.com/products/inference/models.md#traffic-weights). |

> [!NOTE]
>
> This example uses the `vllm` engine. For the `dynamo-vllm` engine and its configuration keys, see [Configure the engine](https://docs.coreweave.com/products/inference/getting-started.md#configure-the-engine) in the Getting started guide. For the full resource schema, see the [`coreweave_inference_gateway`](https://docs.coreweave.com/platform/terraform/resources/inference_gateway) and [`coreweave_inference_deployment`](https://docs.coreweave.com/platform/terraform/resources/inference_deployment) references.

## Deploy

With the four configuration files in place, run the standard Terraform workflow from the configuration directory:

```bash theme={"system"}
terraform init
terraform plan
terraform apply
```

The `terraform init` command downloads the provider. The `terraform plan` command previews the changes without making any, and it's safe to run at any time. The `terraform apply` command shows the same preview and prompts for confirmation before creating anything.

Read the plan before every apply. A `+` means create, `~` means update in place, and `-/+` means destroy and recreate. A destroy-and-recreate on a deployment means downtime for that model.

The apply waits until each resource is ready before returning, so a first deployment can take several minutes while the model weights load:

```text title="Example output" theme={"system"}
coreweave_inference_gateway.main: Creating...
coreweave_inference_gateway.main: Creation complete after 9s [id=a1b2c3d4-e5f6-7890-abcd-ef1234567890]
coreweave_inference_deployment.main: Creating...
coreweave_inference_deployment.main: Still creating... [00m10s elapsed]
coreweave_inference_deployment.main: Still creating... [02m50s elapsed]
coreweave_inference_deployment.main: Creation complete after 3m12s [id=b2c3d4e5-f6a7-8901-bcde-f12345678901]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

deployment_id = "b2c3d4e5-f6a7-8901-bcde-f12345678901"
deployment_status = "STATUS_READY"
gateway_endpoint = "https://my-first-gateway.[ORG-ID].gw.cwinference.com"
gateway_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

> [!NOTE]
>
> The gateway's public DNS record and TLS certificate provision asynchronously and can take several minutes to resolve after the apply completes. If your first inference request fails with an SSL handshake error or DNS resolution failure, wait a few minutes and retry.

## Verify the deployment

First, check Terraform's view of the resources:

```bash theme={"system"}
terraform output
```

The `deployment_status` output should be `STATUS_READY`.

Next, confirm that the gateway serves your model. Export the endpoint and list the models available on it:

```bash theme={"system"}
export CW_GATEWAY_ENDPOINT=$(terraform output -raw gateway_endpoint)

curl -s "${CW_GATEWAY_ENDPOINT}/v1/models" \
  -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}"
```

The response lists every model served on this endpoint. If the endpoint responds but the list is empty, the gateway is up and the deployment isn't ready yet.

Then send a real request. Replace `[MODEL-NAME]` with the value you set for the `model_name` variable:

```bash theme={"system"}
curl -s -X POST "${CW_GATEWAY_ENDPOINT}/v1/chat/completions" \
  -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "[MODEL-NAME]",
    "messages": [{"role": "user", "content": "What is CoreWeave?"}],
    "max_tokens": 128
  }'
```

A response with a `choices` array containing generated text confirms that the gateway and deployment work.

Finally, confirm Terraform is in sync with what's deployed:

```bash theme={"system"}
terraform plan
```

Expect `No changes.` That means your files match the deployed resources, which is the state you should be in before you finish.

### Troubleshooting

The following table lists common failures during deployment and verification, and where to look first:

| Symptom | Where to look |
| - | - |
| `apply` fails immediately with a validation error | The error message names the field. A common cause is a value that isn't offered in your organization. Recheck [Check available parameters](#check-available-parameters). |
| `apply` runs for a long time, then fails | The model couldn't be loaded. Verify the `bucket_name` and `model_path` values, and confirm the inference service account [can read the bucket](https://docs.coreweave.com/products/inference/getting-started.md#grant-inference-access-to-your-bucket). |
| The endpoint returns `401` | The token isn't set or lacks inference access. See [Set your API token](#set-your-api-token). |
| `/v1/models` returns an empty list | The deployment isn't ready. Check the `deployment_status` output, or poll the deployment as described in [Wait for the deployment to start](https://docs.coreweave.com/products/inference/getting-started.md#wait-for-the-deployment-to-start). |
| `plan` shows changes you didn't make | Someone changed the resource outside Terraform. Reconcile the difference before applying. |

## Add another deployment

To serve another model, add another `resource` block to `main.tf`. Each deployment can use its own model, engine version, and hardware, and several deployments can share one gateway.

The following listing shows the complete `main.tf` with the second deployment block highlighted. Declare the two new variables, `second_model_name` and `second_model_path`, in `variables.tf`, and add their values to `terraform.tfvars`, following the same pattern as the existing variables.

```terraform title="main.tf" lines highlight={51-79} theme={"system"}
resource "coreweave_inference_gateway" "main" {
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

resource "coreweave_inference_deployment" "main" {
  name        = "my-first-deployment"
  gateway_ids = [coreweave_inference_gateway.main.id]

  model = {
    name   = var.model_name
    bucket = var.bucket_name
    path   = var.model_path
  }

  runtime = {
    engine  = "vllm"
    version = var.engine_version

    engine_config = {
      "max-model-len" = "8192"
    }
  }

  resources = {
    instance_type = var.instance_type
    gpu_count     = 1
  }

  autoscaling = {
    min         = 1
    max         = 3
    concurrency = 16
  }

  traffic = {
    weight = 100
  }
}

resource "coreweave_inference_deployment" "second_model" {
  name        = "my-second-deployment"
  gateway_ids = [coreweave_inference_gateway.main.id]

  model = {
    name   = var.second_model_name
    bucket = var.bucket_name
    path   = var.second_model_path
  }

  runtime = {
    engine  = "vllm"
    version = var.engine_version
  }

  resources = {
    instance_type = var.instance_type
    gpu_count     = 2
  }

  autoscaling = {
    min = 1
    max = 2
  }

  traffic = {
    weight = 100
  }
}
```

To create the new deployment, run the same plan and apply workflow from [Deploy](#deploy).

Clients select between models with the `model` field in the request body. Two deployments that share the same `model.name` split traffic according to their relative `traffic.weight` values, which is how you run a canary rollout. For weight semantics, see the [Configuration notes](#configuration-notes).

## Make changes

To change a resource, edit the file and re-apply:

```bash theme={"system"}
terraform plan
terraform apply
```

To remove everything this configuration manages, run:

```bash theme={"system"}
terraform destroy
```

Terraform deletes deployments before the gateway automatically, matching the required deletion order.

## Adopt existing resources

If you already created gateways or deployments through the API, the CLI, or the Cloud Console, you don't have to recreate them. You also don't have to write the configuration by hand. Terraform can import the resources and generate matching configuration.

1. List your existing resources and note their IDs:

   > [tab] CoreWeave Intelligent CLI
   >
   > ```bash theme={"system"}
   > cwic inference gateway list
   > cwic inference deployment list
   > ```

   > [tab] curl
   >
   > ```bash theme={"system"}
   > curl -s "https://api.coreweave.com/v1alpha1/inference/gateways" \
   >   -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}" | jq
   >
   > curl -s "https://api.coreweave.com/v1alpha1/inference/deployments" \
   >   -H "Authorization: Bearer ${COREWEAVE_API_TOKEN}" | jq
   > ```

2. Add an `import` block for each resource. Replace `[GATEWAY-ID]` and `[DEPLOYMENT-ID]` with IDs from the previous step. The label after the resource type is yours to choose. It doesn't have to match the resource's name in the API, but the `to` address must not already exist in your configuration or state. If you completed the earlier sections in this directory, use new labels, as this example does with `imported`.

   ```terraform title="imports.tf" theme={"system"}
   import {
     to = coreweave_inference_gateway.imported
     id = "[GATEWAY-ID]"
   }

   import {
     to = coreweave_inference_deployment.imported
     id = "[DEPLOYMENT-ID]"
   }
   ```

   You can import several deployments behind one gateway, and you can import into a directory that already manages other resources. Existing resources are untouched.

3. Generate the configuration:

   ```bash theme={"system"}
   terraform plan -generate-config-out=generated.tf
   ```

   Terraform writes a matching `resource` block for every import, with the fields filled in from the live resource.

4. Move the generated blocks into `main.tf`, refine them, and confirm:

   ```bash theme={"system"}
   terraform plan
   ```

   Repeat until the plan reports only imports and no changes. That's the signal that your configuration matches the live resources.

5. Run `terraform apply` to record the imported resources in state.

6. Delete the `import` blocks. They're one-time instructions.

> [!WARNING]
>
> After you import a resource, `terraform destroy` deletes the live resource. Make sure your state file is stored somewhere safe first. See [Manage state](#manage-state).

## Manage state

Terraform records what it manages in `terraform.tfstate`.

* Don't commit state files to version control. They can contain sensitive values. Do commit `.terraform.lock.hcl`, which pins provider checksums.
* Deleting state doesn't delete infrastructure. Terraform loses track of the resources, which keep running and accruing charges.
* For teams, use a [remote backend](https://developer.hashicorp.com/terraform/language/backend) so that two people can't apply conflicting changes at once.

The following is a typical `.gitignore` for a Terraform directory:

```text title=".gitignore" theme={"system"}
.terraform/
*.tfstate
*.tfstate.*
crash.log
```

## Next steps

To learn more about Dedicated Inference and the Terraform provider, explore these resources:

* [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md): The same workflow using the CoreWeave Intelligent CLI and `curl`, plus observability and engine configuration.
* [Gateways](https://docs.coreweave.com/products/inference/gateways.md): Authentication, routing strategies, and traffic splitting.
* [Models and deployments](https://docs.coreweave.com/products/inference/models.md): Runtime configuration, GPU selection, and deployment options.
* [Scaling](https://docs.coreweave.com/products/inference/scaling.md): Autoscaling and reserved GPU capacity.
* [CoreWeave Terraform provider reference](https://docs.coreweave.com/platform/terraform.md): Provider configuration, resources, and data sources.
