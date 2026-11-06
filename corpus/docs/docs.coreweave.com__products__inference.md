# About CoreWeave Inference

Source: https://docs.coreweave.com/products/inference

# About CoreWeave Inference

> Compare Serverless Inference, Dedicated Inference, and Inference on CKS to choose how to serve your models

# Serve AI models, your way

CoreWeave Inference serves models on NVIDIA GPUs. Choose how much of the stack you run, from fully managed Serverless Inference to Dedicated Inference to self-managed Inference on CKS.

CoreWeave offers three ways to serve AI models: Serverless Inference, Dedicated Inference, and Inference on CoreWeave Kubernetes Service (CKS), which you operate yourself. Use this guide to choose a starting point based on your model, traffic pattern, performance targets, and the serving infrastructure your team wants to operate.

## Choose a deployment option

Start with the model and runtime your application needs, then compare the operational responsibilities of each option.

> [card] [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md)
>
> Call open-weight models from a managed catalog, or serve your own LoRA adapters on supported base models. CoreWeave manages provisioning, routing, and scaling.

> [card] [Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md)
>
> Bring your own weights (BYOW), choose GPU resources and a supported runtime, and let CoreWeave operate the serving platform.

> [card] [Inference on CKS](https://docs.coreweave.com/products/inference/cks.md)
>
> Operate your serving stack on Kubernetes when you need control over runtimes, networking, and orchestration.

The following table compares what you configure and operate in each option:

| Consideration | Serverless Inference | Dedicated Inference | Inference on CKS |
| - | - | - | - |
| Model selection | Choose a catalog model, or serve a LoRA adapter on a supported base model. | Supply weights compatible with a supported runtime. | Deploy models and runtimes that you configure and operate. |
| Serving operations | CoreWeave operates the serving infrastructure. | CoreWeave operates the platform. You configure deployments, gateways, and scaling. | You operate the serving software, scaling, and application reliability on CKS. |
| Infrastructure control | Use the service through its API or the Playground. | Select supported GPU resources and Availability Zones. | Configure Kubernetes resources and workload networking. |
| Billing basis | Pay per token. Storage for LoRA adapters can incur separate charges. | GPU-hour or node-based billing, depending on your contract. | CKS compute billing, including applicable reservations. |
| Main tradeoff | Your workload must fit the catalog and service limits. | Your deployment must fit supported runtimes and platform configuration. | Your team takes responsibility for the serving stack. |

## Match the option to your workload

These recommendations are starting points for evaluation. A workload can fit more than one option. Model compatibility and measured performance determine the final choice. The following table maps common workloads to a starting option and what to evaluate before you commit:

| Workload | Starting point | What to evaluate |
| - | - | - |
| Prototype or application with variable traffic and a catalog model | Serverless Inference | Check model availability, concurrency limits, spending caps, and latency under expected demand. |
| Fully fine-tuned or custom model with recurring production traffic | Dedicated Inference | Confirm runtime compatibility, model memory requirements, and utilization across quiet and busy periods. For a LoRA adapter on a supported base model, also evaluate Serverless Inference. |
| Interactive application with a defined latency target | Dedicated Inference | Use it when you need configurable replicas and capacity claims. Benchmark response latency during traffic bursts and deployment changes. |
| Coding assistant, agent, or retrieval-augmented generation (RAG) application with a catalog model | Serverless Inference | Measure cache reuse, prompt lengths, and response latency. Serverless Inference applies prefix caching to its hosted models. For custom weights, evaluate Dedicated Inference. Choose Inference on CKS when required runtime or routing changes exceed managed configuration. |
| Batch generation or evaluation with a catalog model | Serverless Inference | Separate batch completion deadlines from interactive response targets, and account for concurrency limits. Neither Serverless Inference nor Dedicated Inference provides a batch ingestion endpoint. |
| Custom image, audio, or video pipeline | Inference on CKS | Use it when the pipeline requires custom serving software or orchestration. Verify protocols, preprocessing, storage access, and scaling requirements. Evaluate Dedicated Inference only if its supported runtime and API fit the workload. |
| Distributed serving or infrastructure-level tuning | Inference on CKS | Use it when you need to operate the serving architecture. Evaluate runtime support, communication between GPUs, and the engineering effort to operate the deployment. |

If your workload has data residency, isolation, encryption, or private connectivity requirements, verify each required control before choosing an option. Reserved GPU capacity or an Availability Zone selection doesn't, by itself, establish that all application requirements are met.

## Example deployment choices

The following hypothetical examples show how requirements affect the choice:

* A team testing a document assistant starts with Serverless Inference because a catalog model meets its needs. It measures quality and latency before deciding whether a LoRA adapter on Serverless Inference or full custom weights on Dedicated Inference is justified.
* A team serving a fine-tuned text model evaluates Dedicated Inference to keep control of weights and scaling without operating the serving platform. It [stages the artifacts in CoreWeave AI Object Storage](https://docs.coreweave.com/products/inference/models.md#bring-your-own-weights) and benchmarks the deployment against production traffic.
* A media application uses Inference on CKS to operate a custom model server alongside preprocessing workers and a queue. The team configures workload networking, scaling, and monitoring.
* An application with overnight generation and interactive requests evaluates the two traffic patterns separately. It can use different deployments or options when their latency, model, or orchestration requirements differ.

For runnable examples, see [Deploy Kimi K3 on Dedicated Inference](https://docs.coreweave.com/products/inference/tutorials/deploy-kimi-k3.md), [Deploy NVIDIA Dynamo on CKS](https://docs.coreweave.com/products/cks/tutorials/dynamo-inference.md), and [Deploy vLLM for inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md).

## Compare performance, capacity, and cost

Define success using traffic representative of your application. Include typical and peak request rates, input and output lengths, and repeated context. Measure time to first token, response latency (including slow requests), throughput, and cost per completed request or token.

For Dedicated Inference, tune concurrency against your latency and throughput targets. A setting that works for batch generation might not meet an interactive application's response target. Follow the [concurrency benchmarking guidance](https://docs.coreweave.com/products/inference/scaling.md#choose-a-concurrency-target) and repeat measurements when the model or traffic changes.

Autoscaling adjusts replica counts within available capacity, but it doesn't reserve GPUs. If you need reserved hardware, evaluate [capacity claims](https://docs.coreweave.com/products/inference/scaling.md#capacity-claims). Managed claims incur charges while they exist, including when their capacity is idle. Dedicated Inference doesn't support scale-to-zero, so account for its minimum running replicas when comparing costs.

### Pricing

Compare [Serverless Inference pricing](https://docs.coreweave.com/products/inference/serverless/usage-limits.md#pricing) with [Dedicated Inference billing](https://docs.coreweave.com/products/inference/billing.md) and [CoreWeave compute pricing](https://coreweave.com/pricing). Include expected utilization and the effort to operate a self-managed serving stack. Steady traffic is a reason to evaluate Dedicated Inference, but it doesn't establish a universal cost advantage.

## Key capabilities

Serverless Inference and Dedicated Inference expose OpenAI-compatible endpoints, so existing OpenAI client libraries, agents, and tooling can connect with minimal changes. On CKS, the serving software you deploy determines the API your application uses.

Check the selected product's documentation for model support, endpoint behavior, resource availability, and platform integrations. For Dedicated Inference, consult [supported engines](https://docs.coreweave.com/products/inference/models.md#supported-engines) before choosing a runtime.

## Access the API

You can configure Dedicated Inference resources through the Dedicated Inference API over REST, gRPC, or Connect, through the CoreWeave Intelligent CLI, or through Terraform. For more information, see the [Dedicated Inference API reference](https://docs.coreweave.com/products/inference/reference/api-overview.md) and [Deploy Dedicated Inference with Terraform](https://docs.coreweave.com/products/inference/deploy-with-terraform.md).

For Serverless Inference setup and request examples, see [Serverless Inference prerequisites](https://docs.coreweave.com/products/inference/serverless/api-reference.md#prerequisites) and [usage examples](https://docs.coreweave.com/products/inference/serverless/examples.md).

## Get started

Choose the guide for your deployment option:

* [Get started with Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md).
* [Deploy your first model with Dedicated Inference](https://docs.coreweave.com/products/inference/getting-started.md).
* [Choose an inference tutorial for CKS](https://docs.coreweave.com/products/inference/cks.md).
