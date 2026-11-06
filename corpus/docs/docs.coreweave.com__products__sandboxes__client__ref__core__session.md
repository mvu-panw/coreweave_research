# Session

Source: https://docs.coreweave.com/products/sandboxes/client/ref/core/session

# Session

> Manages sandbox lifecycle and provides function execution.

Source: [src/cwsandbox/\_session.py:49](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_session.py#L49)

```python theme={"system"}
class Session(defaults: SandboxDefaults | Mapping[str, Any] | None = None, report_to: list[str] | None = None, *, auth: AuthConfig | None = None)
```

Manages sandbox lifecycle and provides function execution.

Use a session when:

* Creating multiple sandboxes with shared configuration
* Executing Python functions in sandboxes
* You want automatic cleanup of orphaned sandboxes

Metrics are automatically tracked when exec() completes on any sandbox
associated with this session. Use log\_metrics(step=N) to log metrics
at specific training steps.

## Properties

### sandbox\_count

```python theme={"system"}
@property
def sandbox_count(self) -> int
```

Number of sandboxes currently tracked by this session.

## Methods

### log\_metrics

```python theme={"system"}
log_metrics(step: int | None = None, *, reset: bool = True) -> bool
```

Log accumulated sandbox metrics to wandb.

Call this during training to correlate sandbox usage with training steps.
Metrics are automatically tracked when exec() completes, so users only
need to call log\_metrics() for step correlation.

Metrics are also logged automatically on session close.
**Parameters**

* `step` (`int | None`): Training step to associate with metrics. If provided, metrics are logged at this step number in wandb.
* `reset` (`bool`): If True (default), reset accumulated metrics after a successful log. Metrics are preserved if log() fails (no active wandb run). Set to False to keep accumulating regardless.

**Returns**

* `bool`: True if metrics were logged, False if no reporter configured
* `bool`: or no active wandb run.

**Examples**

```python theme={"system"}
with Session(defaults, report_to=["wandb"]) as session:
    for step in range(100):
        sb = session.sandbox(...)
        result = sb.exec(...).result()  # Metrics tracked automatically
        session.log_metrics(step=step)  # Log at each step
```

### get\_metrics

```python theme={"system"}
get_metrics() -> dict[str, Any]
```

Get current accumulated metrics.
**Returns**

* `dict[str, Any]`: Dictionary with cwsandbox/\* prefixed metric names and values.
* `dict[str, Any]`: Empty dict if no reporter is configured.

### close

```python theme={"system"}
close() -> OperationRef[None]
```

Stop all managed sandboxes, return OperationRef immediately.
**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block until all sandboxes stopped.

**Raises**

* `SandboxError`: If one or more running sandboxes failed to stop.

**Examples**

```python theme={"system"}
session.close().result()  # Block until all sandboxes stopped
```

### sandbox

```python theme={"system"}
sandbox(*, command: str | None = None, args: list[str] | None = None, container_image: str | None = None, tags: list[str] | None = None, runner_ids: list[str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: list[dict[str, Any]] | None = None, network: NetworkOptions | dict[str, Any] | None = None, services: list[Service] | tuple[Service, ...] | None = None, volumes: list[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any]] | tuple[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any], ...] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str | None = None, template_id: str | None = None, image_pull_credentials: ImagePullCredentials | dict[str, Any] | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, environment_variables: dict[str, str] | None = None, annotations: dict[str, str] | None = None, secrets: Sequence[Secret | dict[str, Any]] | None = None, request_timeout_seconds: float | None = None, data_plane_mode: DataPlaneMode | str | None = None, auth: AuthConfig | None = None, containers: Sequence[Container | Mapping[str, Any]] | None = None, **kwargs: Any = {}) -> Sandbox
```

Create an unstarted sandbox with session defaults.

Returns immediately without any network calls. The sandbox
auto-starts on first operation (exec, read\_file, write\_file,
wait), or can be started explicitly with start().result().
**Parameters**

* `command` (`str | None`): Command to run in sandbox
* `args` (`list[str] | None`): Arguments for the command
* `container_image` (`str | None`): Container image to use
* `tags` (`list[str] | None`): Tags for the sandbox (merged with session defaults, including when `template_id` is set, so `list()`/`adopt` can find the sandbox). Environment variables and annotations do not merge on the template path (template-owned spec).
* `profile_ids`: Removed in 1.x; passing a value raises `TypeError`.
* `profile_names`: Removed in 1.x; passing a value raises `TypeError`.
* `runner_ids` (`list[str] | None`): Optional CKS runner pin (incompatible with serverless and with `placement_spillover='serverless_then_cks'`)
* `resources` (`ResourceOptions | dict[str, Any] | None`): Resource configuration. Accepts ResourceOptions for separate requests/limits, or a flat dict for backward-compatible Guaranteed QoS.
* `mounted_files` (`list[dict[str, Any]] | None`): Files to mount into the sandbox at startup. Each dict should have `mount_path` (str) and `file_content` (bytes). Note: Mounted files are read-only at runtime. To modify a file, use `sandbox.write_file()` after the sandbox is running.
* `s3_mount`: Removed in 1.x; passing a value raises `TypeError`.
* `ports`: Removed in 1.x; use `services=[Service(...)]` instead.
* `network` (`NetworkOptions | dict[str, Any] | None`): `NetworkOptions` (or dict) with deny flags and optional create-time hostname grants. Port exposure uses `services=`.
* `file_system_snapshot` (`FileSystemSnapshotOptions | dict[str, Any] | None`): Convenience single-mount FSS options (`FileSystemSnapshotOptions` or dict). Prefer `volumes=` for multi-volume setups.
* `max_timeout_seconds`: Removed in 1.x; use `request_timeout_seconds`.
* `request_timeout_seconds` (`float | None`): Client-side HTTP timeout for sandbox RPCs. Defaults to the session's `SandboxDefaults.request_timeout_seconds`.
* `data_plane_mode` (`DataPlaneMode | str | None`): Override the session's data-plane transport policy.
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider. Overrides the session default for this sandbox.
* `environment_variables` (`dict[str, str] | None`): Environment variables to inject into the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive config only.
* `annotations` (`dict[str, str] | None`): Kubernetes pod annotations for the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive metadata only.
* `secrets` (`Sequence[Secret | dict[str, Any]] | None`): Secrets to inject as environment variables. Merged with session defaults (defaults first, then this list).
* `containers` (`Sequence[Container | Mapping[str, Any]] | None`): Multi-container spec. Mutually exclusive with single-container kwargs. Replaces session `defaults.secrets`, `environment_variables`, `security_context`, and `working_dir`; put those on each `Container`. Not used by `@session.function()`.

**Returns**

* `Sandbox`: An unstarted Sandbox registered with the session.

**Raises**

* `SandboxError`: If the session has been closed.

**Examples**

```python theme={"system"}
with Session(defaults) as session:
    # Auto-start: sandbox starts on first exec()
    sb = session.sandbox(command="sleep", args=["infinity"])
    result = sb.exec(["echo", "hello"]).result()

    # Explicit start for control over timing
    sb2 = session.sandbox(command="sleep", args=["infinity"])
    sb2.start().result()
    sb2.wait()
    result = sb2.exec(["echo", "hello"]).result()
```

### list

```python theme={"system"}
list(*, tags: list[str] | None = None, status: str | None = None, profile_ids: list[str] | None = None, profile_names: list[str] | None = None, runner_ids: list[str] | None = None, show_terminated: bool = False, adopt: bool = False, volume_ids: list[str] | tuple[str, ...] | None = None) -> OperationRef[list[Sandbox]]
```

List sandboxes, optionally adopting them into this session.

Automatically includes the session's default tags in the filter.
This makes it easy to find sandboxes created by this session or
a previous run with the same defaults.

By default, only active (non-terminal) sandboxes are returned.
Set `show_terminated=True` to widen the search to include terminal
sandboxes (completed, failed, terminated).
A terminal status filter (e.g. `status="completed"`) also widens
the search automatically.
**Parameters**

* `tags` (`list[str] | None`): Additional tags to filter by (merged with session's default tags)
* `status` (`str | None`): Filter by status
* `profile_ids` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `profile_names` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `runner_ids` (`list[str] | None`): Filter by runner IDs (defaults to session's runner\_ids if set)
* `volume_ids` (`list[str] | tuple[str, ...] | None`): Filter to sandboxes attached to these registered Volume IDs
* `show_terminated` (`bool`): If True, include terminal sandboxes (completed, failed, terminated). Defaults to False.
* `adopt` (`bool`): If True, register discovered sandboxes with this session so they are stopped when the session closes

**Returns**

* `OperationRef[list[Sandbox]]`: OperationRef\[list\[Sandbox]]: Use .result() to block for results,
* `OperationRef[list[Sandbox]]`: or await directly in async contexts.

**Examples**

```python theme={"system"}
# Session defaults include a tag for this application/run
defaults = SandboxDefaults(tags=("my-app", "run-abc123"))

with Session(defaults) as session:
    # Sync usage - automatically filters by ["my-app", "run-abc123"]
    orphans = session.list(adopt=True).result()

    # Can add additional filters
    running = session.list(status="running").result()

    # Include stopped sandboxes for cleanup or audit
    all_sandboxes = session.list(show_terminated=True).result()

# Async usage
async with Session(defaults) as session:
    orphans = await session.list(adopt=True)
```

### from\_id

```python theme={"system"}
from_id(sandbox_id: str, *, adopt: bool = True) -> OperationRef[Sandbox]
```

Attach to an existing sandbox, optionally adopting it into this session.
**Parameters**

* `sandbox_id` (`str`): The ID of the existing sandbox
* `adopt` (`bool`): If True (default), register the sandbox with this session

**Returns**

* `OperationRef[Sandbox]`: OperationRef\[Sandbox]: Use .result() to block for the Sandbox instance,
* `OperationRef[Sandbox]`: or await directly in async contexts.

**Examples**

```python theme={"system"}
with Session(defaults) as session:
    # Sync usage - reconnect to a sandbox
    sb = session.from_id("sandbox-abc123").result()
    result = sb.exec(["echo", "hello"]).result()
# sb is stopped when session exits

# Async usage
async with Session(defaults) as session:
    sb = await session.from_id("sandbox-abc123")
    result = await sb.exec(["echo", "hello"])
```

### adopt

```python theme={"system"}
adopt(sandbox: Sandbox) -> None
```

Adopt an existing Sandbox instance into this session for cleanup tracking.

Use this when you have a Sandbox from Sandbox.list() or Sandbox.from\_id()
that you want to be automatically stopped when the session closes.
**Parameters**

* `sandbox` (`Sandbox`): A Sandbox instance to track

**Raises**

* `SandboxError`: If the session is closed
* `ValueError`: If the sandbox has no sandbox\_id

**Examples**

```python theme={"system"}
with Session(defaults) as session:
    # Get sandboxes via class method
    sandboxes = Sandbox.list(tags=["my-job"]).result()

    # Adopt them into the session
    for sb in sandboxes:
        session.adopt(sb)

    # Now they'll be stopped when session closes
```

### function

```python theme={"system"}
function(*, container_image: str | None = None, temp_dir: str | None = None, runner_ids: list[str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: Sequence[dict[str, Any]] | None = None, network: NetworkOptions | dict[str, Any] | None = None, services: Sequence[Service] | None = None, volumes: Sequence[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any]] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, environment_variables: dict[str, str] | None = None, annotations: dict[str, str] | None = None, request_timeout_seconds: float | None = None, data_plane_mode: DataPlaneMode | str | None = None, **kwargs: Any = {}) -> Callable[[Callable[P, R]], RemoteFunction[P, R]]
```

Decorator to execute a Python function in a sandbox.

Each function call creates an ephemeral sandbox, executes the function,
and returns the result. The sandbox is automatically cleaned up.

The decorated function must be synchronous. Async functions are not supported.
**Parameters**

* `container_image` (`str | None`): Override session's default image for this function
* `temp_dir` (`str | None`): Override temp directory for payload/result files in sandbox. Defaults to session default. Created if missing.
* `profile_ids`: Removed in 1.x; passing a value raises `TypeError`.
* `profile_names`: Removed in 1.x; passing a value raises `TypeError`.
* `runner_ids` (`list[str] | None`): Optional CKS runner pin (incompatible with serverless and with `placement_spillover='serverless_then_cks'`)
* `resources` (`ResourceOptions | dict[str, Any] | None`): Resource configuration. Accepts ResourceOptions for separate requests/limits, or a flat dict for backward-compatible Guaranteed QoS.
* `mounted_files` (`Sequence[dict[str, Any]] | None`): Files to mount into the sandbox at startup. Each dict should have `mount_path` (str) and `file_content` (bytes). Note: Mounted files are read-only at runtime. To modify a file, use `sandbox.write_file()` after the sandbox is running.
* `s3_mount`: Removed in 1.x; passing a value raises `TypeError`.
* `ports`: Removed in 1.x; use `services=[Service(...)]` instead.
* `network` (`NetworkOptions | dict[str, Any] | None`): `NetworkOptions` (or dict) with deny flags and optional create-time hostname grants. Port exposure uses `services=`.
* `file_system_snapshot` (`FileSystemSnapshotOptions | dict[str, Any] | None`): Convenience single-mount FSS options (`FileSystemSnapshotOptions` or dict). Prefer `volumes=` for multi-volume setups.
* `max_timeout_seconds`: Removed in 1.x; use `request_timeout_seconds`.
* `request_timeout_seconds` (`float | None`): Client-side HTTP timeout for sandbox RPCs. Defaults to the session's `SandboxDefaults.request_timeout_seconds`.
* `data_plane_mode` (`DataPlaneMode | str | None`): Override the session's data-plane transport policy.
* `environment_variables` (`dict[str, str] | None`): Environment variables to inject into the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive config only.
* `annotations` (`dict[str, str] | None`): Kubernetes pod annotations for the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive metadata only.

**Returns**

* `Callable[[Callable[P, R]], RemoteFunction[P, R]]`: A decorator that wraps a function as a RemoteFunction

**Examples**

```python theme={"system"}
with Session(defaults) as session:
    @session.function()
    def compute(x: int, y: int) -> int:
        return x + y

    # Call .remote() to execute in sandbox
    ref = compute.remote(2, 3)  # Returns OperationRef immediately
    result = ref.result()       # Block for result
    print(result)  # 5

    # Or use await in async context
    result = await compute.remote(2, 3)

    # Execute locally for testing
    result = compute.local(2, 3)

    # Map over multiple inputs in parallel
    refs = compute.map([(1, 2), (3, 4), (5, 6)])
    results = [ref.result() for ref in refs]
```
