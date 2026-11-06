# Does Launch support parallelization? How can I limit the resources consumed by a job?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/launch_support_parallelization_limit_resources_consumed_job

# Does Launch support parallelization? How can I limit the resources consumed by a job?

Launch supports scaling jobs across multiple GPUs and nodes. For details, see the [Volcano integration guide](https://docs.coreweave.com/products/wandb/integrations.md).

Each launch agent has a `max_jobs` parameter that sets the maximum number of simultaneous jobs the agent can run. Multiple agents can point to a single queue, as long as they connect to a launching infrastructure that supports them.

You can set limits on CPU, GPU, memory, and other resources at the queue or job run level in the resource configuration. For information about setting up queues with resource limits on Kubernetes, see the [Kubernetes setup guide](https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-kubernetes.md).

For sweeps, include the following block in the queue configuration to limit the number of concurrent runs:

```yaml title="queue config" theme={"system"}
  scheduler:
    num_workers: 4
```
