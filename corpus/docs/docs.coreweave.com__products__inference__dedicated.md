# About Dedicated Inference

Source: https://docs.coreweave.com/products/inference/dedicated

# About Dedicated Inference

> Deploy your own model weights on dedicated GPU infrastructure with full control over gateways, scaling, and capacity

Dedicated Inference is the bring-your-own-weights option in the [CoreWeave Inference](https://docs.coreweave.com/products/inference.md) family. You upload your model artifacts to CoreWeave AI Object Storage, choose a GPU type and inference runtime, and CoreWeave handles cluster operations, deployment, scaling, routing, and lifecycle management. Unlike [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md), which serves models from a CoreWeave-managed catalog, Dedicated Inference deploys the weights you provide on dedicated GPU resources.

To deploy your first model, see [Getting started with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md). To manage inference resources as code, see [Deploy Dedicated Inference with Terraform](https://docs.coreweave.com/products/inference/deploy-with-terraform.md). To load updated policy weights into a running deployment as part of a reinforcement learning training loop, see [RL Rollouts](https://docs.coreweave.com/products/inference/rl-rollouts.md). For a worked example that tunes a large mixture-of-experts model for GB300, see [Deploy Kimi K3 on Dedicated Inference](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md).

## Dedicated Inference key capabilities

Dedicated Inference exposes an [OpenAI-compatible endpoint](https://docs.coreweave.com/products/inference.md#key-capabilities), like Serverless Inference. It also gives you:

* **Bring Your Own Weights (BYOW)**: Upload custom model weights to CoreWeave AI Object Storage and deploy them without operating the underlying clusters.
* **Inference runtime selection**: Choose a supported inference runtime (`dynamo-vllm` or `vllm`) with version pinning.
* **Gateways with traffic management**: Configure authentication, body-based, header-based, or path-based routing, and load balancing across multiple deployments behind a single endpoint.
* **Capacity claims**: Reserve GPU capacity for your inference workloads.
* **Zone selection**: Deploy gateways into specific CoreWeave Availability Zones to optimize for latency, data locality, or compliance requirements.
* **Autoscaling**: Configure minimum and maximum replicas with concurrency targets.

## Core resources

Dedicated Inference is built around three resource types you create and manage through the [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md), either directly over REST, gRPC, or Connect, or through a [generated SDK](https://docs.coreweave.com/products/inference/reference/api-overview.md#schema-and-sdks):

* **Gateways** provide routable endpoints that handle authentication, load balancing, and traffic routing to your model deployments. When you create a gateway, you select a CoreWeave Availability Zone and a routing mode (body-based, header-based, or path-based). Each gateway exposes an external-facing API that your applications use to access your models.
* **Deployments** configure model serving instances, including the inference runtime, GPU type, model weights location in Object Storage, and autoscaling parameters. Each deployment runs your model on dedicated GPU infrastructure and attaches to one or more gateways.
* **Capacity claims** manage hardware resource reservations and provide reserved GPU capacity for your inference workloads independent of any single deployment.

## Manage endpoints

After you create your initial resources, you can manage the full lifecycle of your inference endpoints:

* **Create**: Deploy a model endpoint by creating a gateway and one or more deployments. Select your GPU type, inference runtime, model weights location, and scaling parameters.
* **Update**: Modify deployment configuration (scaling parameters, GPU type, or model weights) by sending a `PATCH` with the full updated specification. CoreWeave applies updates with rolling rollout where possible.
* **Delete**: Remove deployments and gateways to stop serving and release the associated resources. Delete deployments before their parent gateway.

## Observability

CoreWeave Grafana provides the **Inference Model Overview** dashboard. It covers request rate and success rate, queueing and load balancing, inference runtime latency, and autoscaling. Each replica of a deployment runs as one or more Kubernetes Pod(s), and the dashboard breaks out request distribution, GPU utilization, and GPU memory utilization for each one. These metrics cover only your own deployments' Pods, so the dashboard doesn't include Node-level metrics or a Pod-to-Node mapping.

To see data in the dashboard, you need the **Observability Viewer** role in an [IAM access policy](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry). For a description of every panel, see [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md). For step-by-step instructions, see [Observability](https://docs.coreweave.com/products/inference/getting-started.md#observability) in the getting started guide. For general Grafana access, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

## Pricing

Dedicated Inference bills either by node usage or by GPU usage:

* **Node-based billing**: For customers with existing reserved nodes, you can redirect reserved capacity to the inference platform at your existing rates.
* **GPU-based billing**: For on-demand workloads, you pay per GPU-hour. Choose the GPU type and view current rates on the [CoreWeave pricing page](https://coreweave.com/pricing).

For details on autoscaling, see [Scaling](https://docs.coreweave.com/products/inference/scaling.md). For pricing and cost-control patterns, see [Billing](https://docs.coreweave.com/products/inference/billing.md).
