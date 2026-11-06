# RemoteFunction

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/remote-function

# RemoteFunction

> Wrapper for remote function execution in sandboxes.

Source: [src/cwsandbox/\_function.py:41](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_function.py#L41)

```python theme={"system"}
class RemoteFunction(fn: Callable[P, R], *, session: Session, container_image: str | None = None, temp_dir: str = DEFAULT_TEMP_DIR, runner_ids: list[str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: list[dict[str, Any]] | None = None, network: NetworkOptions | dict[str, Any] | None = None, services: list[Any] | None = None, volumes: list[Any] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, placement_mode: Any | None = None, placement_spillover: PlacementSpillover | str | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, environment_variables: dict[str, str] | None = None, annotations: dict[str, str] | None = None, request_timeout_seconds: float | None = None, data_plane_mode: DataPlaneMode | str | None = None)
```

Wrapper for remote function execution in sandboxes.

RemoteFunction wraps a Python function for execution in a sandbox.
It provides methods to execute remotely, locally (for testing), and
map over multiple inputs in parallel.

The wrapped function must be synchronous. Async functions are not supported.

## Methods

### remote

```python theme={"system"}
remote(*args: P.args = (), **kwargs: P.kwargs = {}) -> OperationRef[R]
```

Execute the function in a sandbox, return OperationRef immediately.
**Parameters**

* `*args` (`P.args`): Positional arguments to pass to the function.
* `**kwargs` (`P.kwargs`): Keyword arguments to pass to the function.

**Returns**

* `OperationRef[R]`: OperationRef\[R]: Use .result() to block until result is ready.

**Examples**

```python theme={"system"}
ref = compute.remote(2, 3)
result = ref.result()  # Block for result
# Or in async context:
result = await ref
```

### map

```python theme={"system"}
map(items: Iterable[tuple[Any, ...]]) -> list[OperationRef[R]]
```

Execute the function for each item, return OperationRefs immediately.

Each item should be a tuple of positional arguments for the function.
All executions are launched in parallel.
**Parameters**

* `items` (`Iterable[tuple[Any, ...]]`): Iterable of argument tuples to pass to the function.

**Returns**

* `list[OperationRef[R]]`: List of OperationRef\[R], one for each item.

**Examples**

```python theme={"system"}
# Execute add(1, 2), add(3, 4), add(5, 6) in parallel
refs = add.map([(1, 2), (3, 4), (5, 6)])
results = [ref.result() for ref in refs]  # [3, 7, 11]
```

### local

```python theme={"system"}
local(*args: P.args = (), **kwargs: P.kwargs = {}) -> R
```

Execute the function locally without a sandbox.

Useful for testing and debugging. Runs the original function
directly in the current Python process.
**Parameters**

* `*args` (`P.args`): Positional arguments to pass to the function.
* `**kwargs` (`P.kwargs`): Keyword arguments to pass to the function.

**Returns**

* `R`: The result of the function execution.

**Examples**

```python theme={"system"}
# Test without sandbox overhead
result = compute.local(2, 3)
assert result == 5
```
