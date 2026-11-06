# Rate limits

Source: https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/rate-limits

# Rate limits

> Optional rate limits on Self-Managed instances for stability

You can configure rate limits on your W\&B Self-Managed instance to maintain stability and prevent one user or workload from affecting others. These limits are optional. If you don't set them, the instance doesn't enforce any limits.

## Default limits and notification

The following default limits help maintain platform stability:

| Limit | Default | Scope |
| - | - | - |
| Filestream requests per second | 500 | Project |
| Filestream ingestion per second | 120 MB | Project |
| Filestream requests per second | 2 | Run |
| Run creation requests per second | 80 | Project |

When a limit is exceeded, the W\&B SDK returns HTTP response `429`, and the message `HTTP 429: rate limit exceeded` appears in the SDK logs. How the SDK responds depends on which limit was exceeded:

* Filestream rate limits don't cause logging to crash or fail. When the SDK receives a `429` response on a filestream request, it backs off and retries the rate-limited request as-is, while subsequent updates accumulate.

* Run creation rate limits block further training.

```text theme={"system"}
HTTP 429: rate limit exceeded
```

CoreWeave recommends these defaults for typical production workloads. If your workloads consistently exceed these limits, you can adjust them (or leave them unset) according to your instance size and shared usage. See [Set rate limits](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#set-rate-limits). Contact [Support](mailto:forge-support@coreweave.com) if you need help sizing these limits for your deployment.
