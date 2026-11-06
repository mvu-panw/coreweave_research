# Scaling

Source: https://docs.coreweave.com/products/inference/scaling

# Scaling

> Configure autoscaling and reserve capacity for inference deployments

Dedicated Inference supports autoscaling to match your workload demands. This page explains how to configure autoscaling and reserve GPU capacity for your inference deployments. Your models respond to changing traffic while the resources you need stay available. For pricing details, see [Billing](https://docs.coreweave.com/products/inference/billing.md).

## Autoscaling

Autoscaling adjusts the number of replicas serving a deployment so that capacity tracks demand without manual intervention. Configure each [deployment](https://docs.coreweave.com/products/inference/models.md) with autoscaling parameters that control how replicas scale in response to demand. CoreWeave manages the autoscaling logic, monitors request load, and adjusts replica count within your configured bounds.

### Scaling parameters

Use the following parameters to set the boundaries and behavior the autoscaler applies to your deployment. The `autoscaling` field on a deployment controls scaling behavior:

| Field | Required | Description |
| - | - | - |
| `min` | Yes | Minimum number of replicas that are always running. Must be at least `1`. Scale-to-zero is not supported. |
| `max` | Yes | Maximum number of replicas. Must be greater than or equal to `min`. To disable autoscaling, set `max` equal to `min`. |
| `priority` | No | Scaling priority relative to other deployments, from 0 to 1000. Higher values receive scaling preference during resource contention. |
| `concurrency` | No | Target concurrent requests per replica. Controls the latency-throughput tradeoff: lower values reduce latency, higher values increase throughput. Must be at least `1`. |
| `capacityClasses` | No | The capacity types to use for scaling. Options: `CAPACITY_CLASS_RESERVED`, `CAPACITY_CLASS_ON_DEMAND`. |

### How autoscaling works

CoreWeave uses request signals to determine when to add or remove replicas, and uses priority to break ties when deployments contend for GPUs. CoreWeave monitors request queue depth and active request counts across your deployment's replicas. When demand exceeds the current capacity, the autoscaler adds replicas up to `max`. When demand drops, the autoscaler removes replicas down to `min`.

Scaling priority (`priority`) determines which deployments scale first when multiple deployments contend for the same GPU resources. A deployment with `priority: 1000` scales before one with `priority: 100`.

### Choose a concurrency target

The autoscaler currently scales only on concurrent running and queued requests, not on serving metrics such as latency or throughput. CoreWeave recommends setting `autoscaling.concurrency` from your own benchmarks, then mapping the result onto a concurrent-request count.

Benchmark against a workload profile that matches your production traffic:

* **Input sequence length (ISL)**: the prompt sizes you expect, including any system prompt.
* **Output sequence length (OSL)**: how many tokens your responses generate.
* **Cache hit rate**: how often prefixes repeat across requests, as they do with a shared system prompt or multi-turn conversations.

Next, define the targets your deployment has to hold. These usually combine a per-request or per-user latency budget with an aggregate efficiency goal. Latency budgets are typically time to first token (TTFT) and time per output token (TPOT). Aggregate goals are typically tokens per minute per GPU (TPM/GPU) or cost per token.

Then raise concurrency until you find the knee: the point where a replica can no longer meet all your targets at once. `autoscaling.concurrency` is a per-replica target, so read the knee per replica rather than as a total across the deployment. Below it, each replica has headroom you aren't using. Above it, requests queue and latency degrades faster than throughput improves.

CoreWeave recommends benchmarking with at least two replicas. A second replica reduces downtime during deployment updates. It also lets the benchmark capture how requests spread across replicas, which sets your prefill cache hit rate. On the `dynamo-vllm` engine that routing is kv-cache aware, so a single-replica run can't reproduce the hit rate you see in production. See [Supported engines](https://docs.coreweave.com/products/inference/models.md#supported-engines).

Benchmarking also shows you where replicas start to churn. Any autoscaler adds and removes replicas repeatedly when sustained traffic sits close to its target, whether it tracks RPS or concurrency. Finding that point in a benchmark lets you set the target deliberately instead of discovering it in production.

If you have no benchmark data yet, estimate a starting point for the sweep. Multiply the expected requests per second (RPS) per replica by the average request duration in seconds:

```text theme={"system"}
estimated concurrent requests per replica = RPS per replica * average request duration in seconds
```

For example, a replica that receives 4 RPS with an average request duration of 5 seconds has an estimated concurrency of 20. Treat this only as a place to begin measuring. Prompt length, generated output length, batching, and runtime configuration all change request duration.

While you drive benchmark traffic, watch the **TTFT**, **TPOT**, **Request Duration**, **Output Tok/s**, and **Cache Hit** panels on the [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md) dashboard. See [View inference metrics](https://docs.coreweave.com/products/inference/getting-started.md#view-inference-metrics).

### Scaling stabilization

Dedicated Inference doesn't expose configurable scale-up or scale-down cooldown fields. The autoscaler evaluates scale-up requests without a stabilization delay, although provisioning a GPU instance and loading model weights still takes time. When demand falls, the autoscaler stabilizes scale-down recommendations for about 5 minutes before removing replicas. This delay avoids scaling down during short traffic dips.

To watch replica count change for a deployment, use the **Replicas** panel in the **Scaling** row of the [Inference Model Overview](https://docs.coreweave.com/observability/managed-grafana/dedicated-inference/inference-model-overview.md) dashboard.

### Best practices

Follow these guidelines to optimize autoscaling for your workloads:

* **Set `min` based on latency requirements.** A higher minimum avoids cold-start delays when new requests arrive during low-traffic periods. Each replica must load model weights before it can serve requests. Set `min` to at least `2` to avoid downtime during deployment updates.
* **Set `max` to control cost.** Each replica consumes GPU resources that are billed. Set the maximum to the highest replica count your budget allows.
* **Match GPU type to model size.** Choose an instance type with enough GPU memory to fit your model weights and the inference runtime's working memory. Over-provisioning wastes resources, and under-provisioning causes out-of-memory failures.
* **Use `concurrency` to tune latency.** For latency-sensitive workloads, set a lower concurrency target so the autoscaler adds replicas sooner. For throughput-oriented workloads, set a higher value to maximize GPU utilization per replica. Benchmark again when your workload profile changes, such as a new model, a longer system prompt, or different output lengths.

## Capacity claims

Autoscaling adjusts replica count within available resources, but doesn't guarantee that GPU capacity is available. For workloads that require guaranteed GPU capacity, create capacity claims to reserve hardware resources. Capacity claims ensure that infrastructure is available for your deployments, even during periods of high demand.

### How capacity claims work

A capacity claim reserves a specified number of GPU instances in an [Availability Zone](https://docs.coreweave.com/platform/regions/all-availability-zones.md). Reserving capacity is separate from using it: the claim only sets hardware aside, while a deployment's [`capacityClasses`](#scaling-parameters) setting controls scheduling.

### Capacity types

The `capacityType` field is required and must be set to `CAPACITY_TYPE_MANAGED`. You can't change it after the claim is created.

`CAPACITY_TYPE_MANAGED` reserves instances from CoreWeave's managed inference capacity pool. These instances are [billed on demand](https://docs.coreweave.com/products/inference/billing.md#billing-models) at GPU-hour rates, and you pay for the reserved instances for as long as the claim exists, whether or not a deployment is actively using them. Availability depends on the capacity CoreWeave has free in the requested zone.

> [!NOTE]
>
> `CAPACITY_TYPE_SERVERLESS` and `CAPACITY_TYPE_CUSTOMER` are no longer accepted values. `CAPACITY_TYPE_MANAGED` replaces the former `CAPACITY_TYPE_SERVERLESS`. Update any configuration that still sets either value.

### Capacity classes

A deployment's [`capacityClasses`](#scaling-parameters) setting controls which capacity its replicas can schedule onto. A claim sets capacity aside, but a replica runs on it only when the deployment's `capacityClasses` value allows it:

| `capacityClasses` value | Where replicas can schedule |
| - | - |
| `CAPACITY_CLASS_ON_DEMAND` | Unclaimed on-demand capacity only. |
| `CAPACITY_CLASS_RESERVED` | Reserved capacity from `CAPACITY_TYPE_MANAGED` claims. |
| Unset | All capacity: unclaimed on-demand, plus `CAPACITY_TYPE_MANAGED` claims. |

### Capacity claim configuration

Use the following fields to describe the hardware you want to reserve. The `resources` field on a capacity claim specifies what to reserve:

| Field | Required | Description |
| - | - | - |
| `instanceId` | Yes | The instance type to reserve (case-insensitive). Must be valid in the specified zone. |
| `instanceCount` | Yes | The number of instances to reserve. |
| `capacityType` | Yes | The capacity type. Must be `CAPACITY_TYPE_MANAGED`. See [Capacity types](#capacity-types). |
| `zones` | Yes | The Availability Zone to reserve in. A claim can currently specify only one zone. |

The `instanceId` must be an instance type that's available for capacity claims in the zone you request. Query the capacity claim parameters endpoint to see the available instance types per zone, returned under `zoneInstanceTypes`. Replace `[API-TOKEN]` with your [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md):

```bash theme={"system"}
curl "https://api.coreweave.com/v1alpha1/inference/capacityclaims/parameters" \
  -H "Authorization: Bearer [API-TOKEN]"
```

For the full list of GPU instance types and their specifications, see [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md).

### Capacity claim status

After creating a capacity claim, check its status to see how many instances are allocated:

| Field | Description |
| - | - |
| `allocatedInstances` | The number of instances currently allocated and available. |
| `pendingInstances` | The number of instances being provisioned (Nodes joining the cluster). |

### Update and delete behavior

You can change a capacity claim's instance count after it's created.

Reducing the instance count can take effect on a delay, because CoreWeave limits how often capacity claims can scale down. Pending changes appear in the claim's status.

Deleting a capacity claim releases its instances. Whether a deployment running on those instances keeps serving depends on its [`capacityClasses`](#scaling-parameters) setting:

* Deployments restricted to `CAPACITY_CLASS_RESERVED` are evicted, because reserved capacity is the only place their replicas can schedule.
* Deployments that also accept on-demand capacity, including those that leave `capacityClasses` unset, can keep serving by rescheduling onto unclaimed on-demand capacity when it's available.

### Manage capacity claims

Create, update, and delete capacity claims through the API rather than the deployment configuration. Manage capacity claims through the [Dedicated Inference API](https://docs.coreweave.com/products/inference/reference/api-overview.md). For request and response schemas, see the [CapacityClaimService](https://docs.coreweave.com/products/inference/reference/api-overview/capacityclaimservice/list-capacity-claims.md) pages in the API reference. The parameters endpoint returns the available instance types per zone under `zoneInstanceTypes`.
