# ResourceOptions

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/resources

# ResourceOptions

> Resource configuration for sandbox CPU, memory, and GPU.

Source: [src/cwsandbox/\_types.py:1151](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1151)

```python theme={"system"}
class ResourceOptions(*, requests: dict[str, str] | None = None, limits: dict[str, str] | None = None, gpu: dict[str, Any] | None = None)
```

Resource configuration for sandbox CPU, memory, and GPU.

Supports separate requests and limits for Burstable QoS pods.
GPU is a separate top-level field because GPU overcommit is not
supported by the backend.

Shallow immutability: dict fields prevent hashing but preserve
the frozen dataclass pattern used by NetworkOptions and Secret.

**Attributes**

* `requests` (`dict[str, str] | None`) : CPU/memory resource requests (e.g. \{"cpu": "1", "memory": "256Mi"}).
* `limits` (`dict[str, str] | None`) : CPU/memory resource limits (e.g. \{"cpu": "8", "memory": "2Gi"}).
* `gpu` (`dict[str, Any] | None`) : GPU configuration (e.g. \{"count": 1, "type": "A100"}).
