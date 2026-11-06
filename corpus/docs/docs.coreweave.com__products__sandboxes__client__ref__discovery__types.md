# Types

Source: https://docs.coreweave.com/products/sandboxes/client/ref/discovery/types

# Types

> Data types returned by discovery functions.

## Runner

Source: [src/cwsandbox/\_discovery.py:76](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L76)

```python theme={"system"}
class Runner(*, runner_id: str, organization_id: str, runner_group_id: str, tags: tuple[str, ...], healthy: bool, is_shared: bool, connected_at: datetime, max_cpu_millicores: int, max_memory_bytes: int, max_gpu_count: int, supported_gpu_types: tuple[str, ...], supported_architectures: tuple[str, ...], supports_privileged: bool, available_storage_classes: tuple[str, ...], supported_service_visibilities: tuple[str, ...], resources: RunnerResources | None = None)
```

A runner registered with the discovery service.

**Attributes**

* `resources` (`RunnerResources | None`) : Live resource availability, or None if not reported.

***

## RunnerResources

Source: [src/cwsandbox/\_discovery.py:59](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L59)

```python theme={"system"}
class RunnerResources(*, available_cpu_millicores: int, available_memory_bytes: int, available_gpu_count: int, running_sandboxes: int)
```

Live resource availability for a runner.

***
