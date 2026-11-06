# Functions

Source: https://docs.coreweave.com/products/sandboxes/client/ref/discovery/functions

# Functions

> Query the runners visible to your organization.

## list\_runners

Source: [src/cwsandbox/\_discovery.py:289](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L289)

```python theme={"system"}
list_runners(*, auth: AuthConfig | None = None, runner_group_id: str | None = None, gpu_type: str | None = None, architecture: str | None = None, healthy_only: bool = False, include_resources: bool = False, min_available_cpu_millicores: int | None = None, min_available_memory_bytes: int | None = None, min_available_gpu_count: int | None = None, service_visibility: str | None = None) -> list[Runner]
```

List available runners, optionally filtered.
**Parameters**

* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `runner_group_id` (`str | None`): Restrict results to this runner group.
* `gpu_type` (`str | None`): Only return runners that support this GPU type.
* `architecture` (`str | None`): Only return runners that support this CPU architecture.
* `healthy_only` (`bool`): Only return healthy runners.
* `include_resources` (`bool`): If `True`, include live resource availability.
* `min_available_cpu_millicores` (`int | None`): Client-side filter on unreserved CPU.
* `min_available_memory_bytes` (`int | None`): Client-side filter on unreserved memory.
* `min_available_gpu_count` (`int | None`): Client-side filter on unreserved GPUs.
* `service_visibility` (`str | None`): Require a runner that can enforce this typed visibility (`public` / `private` / `custom`).

**Returns**

* `list[Runner]`: List of `Runner` objects matching the filters.

***

## get\_runner

Source: [src/cwsandbox/\_discovery.py:390](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L390)

```python theme={"system"}
get_runner(runner_id: str, *, organization_id: str, auth: AuthConfig | None = None) -> Runner
```

Get a single runner by `(organization_id, runner_id)`.

Always returns full details including resource availability when owned.
**Parameters**

* `runner_id` (`str`): Runner identifier (not globally unique alone).
* `organization_id` (`str`): Organization that owns the runner.
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.

**Returns**

* `Runner`: `Runner` with full details.

***

## format\_bytes

Source: [src/cwsandbox/\_discovery.py:39](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L39)

```python theme={"system"}
format_bytes(value: int) -> str
```

## Format bytes as a human-readable string using binary units.

## format\_cpu

Source: [src/cwsandbox/\_discovery.py:54](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_discovery.py#L54)

```python theme={"system"}
format_cpu(millicores: int) -> str
```

## Format CPU millicores as a human-readable string.
