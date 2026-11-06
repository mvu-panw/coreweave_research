# Deploy models to a sandbox

Source: https://docs.coreweave.com/products/registry/deploy_models

# Deploy models to a sandbox

> Learn how to deploy models from Registry to CoreWeave Sandboxes.

Deploy a model from Registry to an isolated environment in [CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes.md) for testing and iteration. Send inference requests to the deployment endpoint with tools such as curl or a Python HTTP client.

> [!NOTE]
>
> Deploying models from Registry to sandboxes is in private preview and currently requires GPU-enabled sandboxes. To request access, contact your account team or email [support@coreweave.com](mailto:support@coreweave.com).

Each sandbox has a limited lifetime and stops when it expires. When a sandbox expires, CoreWeave releases its compute resources and its endpoint becomes unavailable. To create another sandbox, [clone](https://docs.coreweave.com/products/registry/deploy_models.md#clone-a-deployment) the deployment. Cloning creates a new sandbox with a new generated endpoint URL.

Deployments are scoped to your organization and associated with the team you select. To create, clone, stop, or otherwise manage deployments, you must have a [Registry role with write access](https://docs.coreweave.com/products/registry/configure_registry.md#details-about-registry-roles) in the organization. Your organization must also have access to sandboxes and GPU sandboxes, available sandbox quota, and sufficient sandbox compute.

## Deploy a model

Follow the steps below to deploy a model to a sandbox:

1. Navigate to **Registry**.
2. Select a registry.
3. Select a collection.
4. Select a model version.
5. Select the action menu (), then select **Deploy**.
6. From the **Version** dropdown, select the model version to deploy.
7. Enter a name for the deployment for the **Deployment** name field.
8. Select **Next**.
9. Select the team to associate with the deployment.
10. Select a [compute resource](https://docs.coreweave.com/products/registry/deploy_models.md#compute-resources).
11. From the **Lifetime** dropdown, select how long the sandbox can run.
12. Configure the **Serving engine**. The default and currently supported engine is `vLLM`.
13. Select **Next**.
14. Review the deployment details, then select **Deploy**.

## Compute resources

The compute resource determines the CPU, memory, and GPU resources allocated to the sandbox.

| Type | Description |
| - | - |
| CPU (vCPU) | The number of virtual CPUs allocated to the sandbox. |
| Memory (GiB) | The amount of system memory allocated to the sandbox. |
| GPU | The number of GPUs allocated to the sandbox. |

> [!NOTE]
>
> GPU sandboxes must be enabled for your organization. Until GPUs are enabled, a request that includes a GPU fails with `CWSANDBOX_GPU_NOT_ALLOWED` and the message `this organization is not entitled to create GPU sandboxes`.

## Sandbox states

A sandbox can have one of the following states:

| State | Description |
| - | - |
| Starting | CoreWeave is creating the sandbox and deploying the model. |
| Running | The sandbox is running and available for use. |
| Stopping | CoreWeave is stopping the sandbox. |
| Stopped | A user stopped the sandbox. Its endpoint is no longer available. |
| Expired | The sandbox reached its expiration time. Its endpoint is no longer available. |
| Failed | An error prevented the deployment from starting. |

## View a deployment

View the status, expiration time, configuration, and other details for a deployed sandbox.

1. Navigate to **Registry**.
2. Select a registry.
3. Select a collection.
4. Select a model version.
5. Select the **Deployments** tab.
6. Open the deployment details by doing one of the following:
   * Select the name of the deployed sandbox.
   * Select the action menu () and choose **View deployment details**.

### Deployment overview

The deployment overview includes the following information:

* **Status**: The current [state](https://docs.coreweave.com/products/registry/deploy_models.md#sandbox-states) of the sandbox.
* **Created by**: The user who created the deployment.
* **Created at**: When the deployment was created.

### Sandbox configuration

The sandbox configuration includes the following information:

* **Instance name**: The name of the sandbox instance.
* **Serving engine**: The engine that serves the model.
* **Team**: The team that created the sandbox.
* **Compute resources**: CPU, memory, and GPU resources allocated to the sandbox.
* **Expires in**: The remaining time before the sandbox expires.
* **Endpoint address**: The address used to send requests to the deployed sandbox.
* **curl example**: An example request to the deployment endpoint using `curl`.

## Access a deployed model

Send requests to a deployed model by using the endpoint address in the sandbox configuration. The endpoint remains available until the sandbox expires or you stop the deployment.

> [!WARNING]
>
> Sandbox endpoints are publicly accessible and don't support Forge API key authentication. Anyone with the endpoint URL can send requests to the deployed model. Don't use a sandbox endpoint for models or data that require access controls.

### Find the endpoint address

You can find the endpoint address for your deployed sandbox in the sandbox configuration section of the deployment overview.

1. Open the [deployment details](https://docs.coreweave.com/products/registry/deploy_models.md#view-a-deployment).
2. In **Sandbox configuration**, find **Endpoint address**.

### Test the deployment

Send a chat completion request to verify that the deployment can serve inference requests.

> [tab] Python
>
> Copy and paste the following Python code to test your deployed sandbox. Set `base_url` to the endpoint address of your deployment and install `httpx` if you haven't already done so by running `pip install httpx`.
>
> ```python theme={"system"}
> import httpx
>
> base_url = "sandbox-url"
>
> response = httpx.post(
>     f"{base_url}/v1/chat/completions",
>     headers={
>         "Content-Type": "application/json",
>     },
>     json={
>         "model": "local",
>         "messages": [
>             {
>                 "role": "user",
>                 "content": "Reply with OK."
>             },
>         ],
>         "temperature": 0,
>         "max_tokens": 5,
>     },
>     timeout=60,
> )
>
> response.raise_for_status()
> print(response.json()["choices"][0]["message"]["content"])
> ```

> [tab] curl
>
> Copy and paste the following curl command to send a test request to your deployed sandbox. Replace `sandbox-url` with the endpoint address of your deployment:
>
> ```bash theme={"system"}
> curl --fail-with-body \
>   "sandbox-url/v1/chat/completions" \
>   --header "Content-Type: application/json" \
>   --data '{
>     "model": "local",
>     "messages": [
>       {
>         "role": "user",
>         "content": "Reply with OK."
>       }
>     ],
>     "temperature": 0,
>     "max_tokens": 5
>   }'
> ```

## Clone a deployment

Clone a deployment to create a new sandbox with its own generated endpoint URL. By default, the cloned deployment uses the original deployment name with `-clone` appended. You can change this name before confirming the deployment.

Deployment names must be unique among deployments that are starting or running. You can reuse a name after the existing deployment stops or expires.

To clone a deployment, follow these steps:

1. Navigate to the Registry.
2. Select a registry.
3. Select a collection.
4. Select a model version.
5. Select the **Deployments** tab.
6. Select the **action** () menu, then select **Clone deployment**.
7. Review or update the deployment settings, then confirm the deployment.

## Stop a deployment

Stop a running deployment. You can't restart a stopped deployment, and its endpoint becomes unavailable. To serve the model again, create a new deployment.

To stop a running sandbox deployment, follow these steps:

1. Navigate to **Registry**.
2. Select a registry.
3. Select a collection.
4. Select a model version.
5. Select the **Deployments** tab.
6. Select a deployment.
7. Select the action menu (), then select **Stop deployment**.

## Billing and usage

Deploying a model to a sandbox consumes compute from CoreWeave Sandboxes. Model workflows can also incur product-specific usage when they use Weave, Serverless Inference, or Serverless Training.

Organization and billing admins can review plan details, monitor usage, configure usage and spending alerts, manage payment methods, and access invoices from [Billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md).

If your account has insufficient sandbox compute, you might need to purchase additional usage, upgrade your plan, or contact CoreWeave support at [support@coreweave.com](mailto:support@coreweave.com).
