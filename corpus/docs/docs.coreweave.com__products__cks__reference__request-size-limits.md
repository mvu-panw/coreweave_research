# Request size limits

Source: https://docs.coreweave.com/products/cks/reference/request-size-limits

# Request size limits

> Gateway and Kubernetes API request size limits that apply to all CoreWeave Kubernetes Service traffic

CoreWeave applies request size limits at the platform gateway that all API traffic passes through, including calls to the Kubernetes API. These limits protect the stability of the gateway and apply globally across all clusters. They aren't adjustable per customer or per cluster.

The following table lists the two limits:

| Request component | Limit | Applies to |
| - | - | - |
| Combined URL and header size | Approximately 50 KB | All requests routed through the CoreWeave platform gateway, including Kubernetes API requests |
| Request body size | 100 MB (Kubernetes API default) | Kubernetes API create, update, patch, and delete operations |

> [!NOTE]
>
> These two limits govern different parts of a request. Automation failures typically come from oversized URLs or headers, not oversized bodies, so the gateway's URL and header limit is the one you're most likely to reach.

If you develop or operate automation, CLI tools, or workload launchers that call the Kubernetes API, see [Why am I hitting request limits with the Kubernetes API?](https://docs.coreweave.com/support/cks/articles/why-am-i-hitting-request-limits-with-the-kubernetes-api) for the errors these limits cause and how to avoid them.

For CKS cluster, instance, and storage quotas, see [Limits](https://docs.coreweave.com/policies/limits.md).
