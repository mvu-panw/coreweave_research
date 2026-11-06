# Rate limits

Source: https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud/rate-limits

# Rate limits

> Default rate limits on Dedicated Cloud and how to request changes

W\&B Dedicated Cloud applies rate limits to maintain instance stability. CoreWeave can adjust limits when you scale up training or need higher throughput. Use this page to understand the default limits that apply to your Dedicated Cloud instance and how to request an increase if your workloads need more capacity.

## Default limits and notification

The following section lists the default rate limits and describes how the W\&B SDK behaves when you exceed a limit.

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

CoreWeave recommends these defaults for typical production workloads. If your workloads consistently exceed these limits, contact [Support](mailto:forge-support@coreweave.com) or your Account Solutions Engineer (AISE) to request higher limits. Provide details of your experimental setup and usage patterns so that CoreWeave can scope an appropriate adjustment.
