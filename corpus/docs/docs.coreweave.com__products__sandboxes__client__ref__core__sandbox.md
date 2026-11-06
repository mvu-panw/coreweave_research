# Sandbox

Source: https://docs.coreweave.com/products/sandboxes/client/ref/core/sandbox

# Sandbox

> CWSandbox client with sync/async hybrid API.

Source: [src/cwsandbox/\_sandbox.py:1688](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_sandbox.py#L1688)

```python theme={"system"}
class Sandbox(*, command: str | None = None, args: list[str] | None = None, defaults: SandboxDefaults | None = None, auth: AuthConfig | None = None, container_image: str | None = None, tags: list[str] | None = None, base_url: str | None = None, request_timeout_seconds: float | None = None, poll_retry_budget_seconds: float | None = None, poll_rpc_timeout_seconds: float | None = None, max_lifetime_seconds: float | None = None, profile_ids: list[str] | None = None, profile_names: list[str] | None = None, runner_ids: list[str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: list[dict[str, Any]] | None = None, s3_mount: dict[str, Any] | None = None, ports: list[dict[str, Any]] | None = None, network: NetworkOptions | dict[str, Any] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, max_timeout_seconds: int | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str | None = None, services: list[Service] | tuple[Service, ...] | None = None, volumes: list[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any]] | tuple[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any], ...] | None = None, template_id: str | None = None, image_pull_credentials: ImagePullCredentials | dict[str, Any] | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, environment_variables: dict[str, str] | None = None, annotations: dict[str, str] | None = None, secrets: Sequence[Secret | dict[str, Any]] | None = None, data_plane_mode: DataPlaneMode | str | None = None, containers: Sequence[Container | Mapping[str, Any]] | None = None)
```

CWSandbox client with sync/async hybrid API.

All methods return immediately and can be used in both sync and async contexts.
Operations are executed in a background event loop managed by \_LoopManager.

## Properties

### sandbox\_id

```python theme={"system"}
@property
def sandbox_id(self) -> str | None
```

The unique sandbox ID, or None if not yet started.

### returncode

```python theme={"system"}
@property
def returncode(self) -> int | None
```

Exit code if sandbox has completed, None if still running.

### runner\_id

```python theme={"system"}
@property
def runner_id(self) -> str | None
```

Runner where sandbox is running, or None if not started.

### status

```python theme={"system"}
@property
def status(self) -> SandboxStatus | None
```

Last known status of the sandbox.

### status\_updated\_at

```python theme={"system"}
@property
def status_updated_at(self) -> datetime | None
```

Timestamp when status was last confirmed.

### started\_at

```python theme={"system"}
@property
def started_at(self) -> datetime | None
```

Timestamp when the sandbox was started.

### runner\_group\_id

```python theme={"system"}
@property
def runner_group_id(self) -> str | None
```

Runner group ID where the sandbox is running.

### service\_urls

```python theme={"system"}
@property
def service_urls(self) -> tuple[tuple[int, str, str], ...]
```

Per-service URLs assigned by the backend.

### service\_endpoints

```python theme={"system"}
@property
def service_endpoints(self) -> tuple[HttpsEndpointStatus, ...]
```

HTTPS product endpoints echoed from create, Get, or list.

### service\_addresses

```python theme={"system"}
@property
def service_addresses(self) -> tuple[TlsPassthroughEndpointStatus, ...]
```

TLS passthrough endpoints echoed from create, Get, or list.

### containers

```python theme={"system"}
@property
def containers(self) -> tuple[Container, ...]
```

Create-time container spec echoed from the sandbox resource.

### container\_statuses

```python theme={"system"}
@property
def container_statuses(self) -> tuple[ContainerStatus, ...]
```

Per-container observed state. Sandbox `status` stays primary-owned.

### dns\_egress\_names

```python theme={"system"}
@property
def dns_egress_names(self) -> tuple[str, ...]
```

Hostnames granted at create, echoed from `status.effective_egress`.

### effective\_runtime\_class

```python theme={"system"}
@property
def effective_runtime_class(self) -> str | None
```

Runtime class applied by the backend, echoed from status.

### attached\_volume\_ids

```python theme={"system"}
@property
def attached_volume_ids(self) -> tuple[str, ...]
```

Registered Volume IDs attached to this sandbox, echoed from status.

### effective\_egress

```python theme={"system"}
@property
def effective_egress(self) -> tuple[EgressRule, ...]
```

Effective egress rules echoed from `status.effective_egress`.

### effective\_ingress

```python theme={"system"}
@property
def effective_ingress(self) -> tuple[IngressRule, ...]
```

Effective ingress rules echoed from `status.effective_ingress`.

### exposed\_ports

```python theme={"system"}
@property
def exposed_ports(self) -> tuple[tuple[int, str], ...] | None
```

Exposed `(container_port, name)` pairs derived from typed services.

### resource\_limits

```python theme={"system"}
@property
def resource_limits(self) -> dict[str, str] | None
```

Resource limits from the start response, or None for discovered sandboxes.

### resource\_requests

```python theme={"system"}
@property
def resource_requests(self) -> dict[str, str] | None
```

Resource requests from the start response, or None for discovered sandboxes.

### resource\_gpu

```python theme={"system"}
@property
def resource_gpu(self) -> dict[str, Any] | None
```

GPU config confirmed by the start response, or None for discovered sandboxes.

### file\_system\_snapshot\_id

```python theme={"system"}
@property
def file_system_snapshot_id(self) -> str | None
```

ID of the snapshot produced by `stop(snapshot_on_stop=True)`.

### exec\_stats

```python theme={"system"}
@property
def exec_stats(self) -> dict[str, int]
```

Execution statistics for this sandbox.

## Methods

### run

```python theme={"system"}
run(*args: str = (), container_image: str | None = None, defaults: SandboxDefaults | None = None, auth: AuthConfig | None = None, request_timeout_seconds: float | None = None, poll_retry_budget_seconds: float | None = None, poll_rpc_timeout_seconds: float | None = None, max_lifetime_seconds: float | None = None, tags: list[str] | None = None, profile_ids: list[str] | None = None, profile_names: list[str] | None = None, runner_ids: list[str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: list[dict[str, Any]] | None = None, s3_mount: dict[str, Any] | None = None, ports: list[dict[str, Any]] | None = None, network: NetworkOptions | dict[str, Any] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, max_timeout_seconds: int | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str | None = None, services: list[Service] | tuple[Service, ...] | None = None, volumes: list[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any]] | tuple[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any], ...] | None = None, template_id: str | None = None, image_pull_credentials: ImagePullCredentials | dict[str, Any] | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, environment_variables: dict[str, str] | None = None, annotations: dict[str, str] | None = None, secrets: Sequence[Secret | dict[str, Any]] | None = None, data_plane_mode: DataPlaneMode | str | None = None, containers: Sequence[Container | Mapping[str, Any]] | None = None) -> Sandbox
```

Create and start a sandbox, return immediately once backend accepts.

Does NOT wait for RUNNING status. Use .wait() to block until ready.
If positional args are provided, the first is the command and the rest
are its arguments. If no args are provided, uses a shell-trapped
keep-alive default that responds to SIGTERM on stop.
**Parameters**

* `*args` (`str`): Optional command and arguments (e.g., "echo", "hello", "world"). If omitted, uses default command from SandboxDefaults.
* `container_image` (`str | None`): Container image to use
* `defaults` (`SandboxDefaults | None`): Optional SandboxDefaults to apply
* `auth` (`AuthConfig | None`): Authentication mode or provider. Overrides `defaults.auth`.
* `request_timeout_seconds` (`float | None`): Timeout for API requests (client-side)
* `poll_retry_budget_seconds` (`float | None`): Wall-clock budget for retrying transient errors on the sandbox-status poll loop (default: 30s). Set to 0 to disable retry.
* `poll_rpc_timeout_seconds` (`float | None`): Per-call timeout for poll Get RPCs (default: 15s). Separate from request\_timeout\_seconds.
* `max_lifetime_seconds` (`float | None`): Max sandbox lifetime (server-side)
* `tags` (`list[str] | None`): Optional tags for the sandbox
* `profile_ids` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `profile_names` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `runner_ids` (`list[str] | None`): Optional CKS runner pin (incompatible with serverless and with `placement_spillover='serverless_then_cks'`).
* `resources` (`ResourceOptions | dict[str, Any] | None`): Resource configuration. Accepts ResourceOptions for separate requests/limits, or a flat dict for backward-compatible Guaranteed QoS.
* `mounted_files` (`list[dict[str, Any]] | None`): Files to mount into the sandbox at startup. Each dict should have `mount_path` (str) and `file_content` (bytes). Note: Mounted files are read-only at runtime. To modify a file, use `sandbox.write_file()` after the sandbox is running.
* `s3_mount` (`dict[str, Any] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `ports` (`list[dict[str, Any]] | None`): Removed in 1.x; use `services=[Service(...)]` instead.
* `network` (`NetworkOptions | dict[str, Any] | None`): `NetworkOptions` (or dict) with deny flags and optional create-time hostname grants (`egress=[EgressRule(dns_name=...)]`). Port exposure uses `services=`.
* `placement_mode` (`PlacementMode | str | None`): `PlacementMode` or string (`serverless` / `cks`).
* `placement_spillover` (`PlacementSpillover | str | None`): `PlacementSpillover` or string. Default `strict`. See `Sandbox.__init__`.
* `services` (`list[Service] | tuple[Service, ...] | None`): Typed service ports (`Service` list/tuple).
* `volumes` (`list[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any]] | tuple[ScratchVolumeOptions | RegisteredVolumeOptions | dict[str, Any], ...] | None`): Scratch or registered volumes (`ScratchVolumeOptions`, `RegisteredVolumeOptions`, or a `volume_id` dict).
* `runtime_class` (`str | None`): Optional runtime-class pin (e.g. `"gvisor"`).
* `security_context` (`SecurityContext | dict[str, Any] | None`): In-guest privilege for the primary container.
* `working_dir` (`str | None`): Working directory for the primary container command.
* `object_storage_access` (`ObjectStorageAccess | dict[str, Any] | None`): Temporary object-storage credentials.
* `file_system_snapshot` (`FileSystemSnapshotOptions | dict[str, Any] | None`): Convenience single-mount FSS options (`FileSystemSnapshotOptions` or dict). Prefer `volumes=` for multi-volume setups.
* `max_timeout_seconds` (`int | None`): Removed in 1.x; use `request_timeout_seconds`.
* `environment_variables` (`dict[str, str] | None`): Environment variables to inject into the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive config only.
* `annotations` (`dict[str, str] | None`): Kubernetes pod annotations for the sandbox. Merges with and overrides matching keys from the session defaults. Use for non-sensitive metadata only.
* `secrets` (`Sequence[Secret | dict[str, Any]] | None`): Secrets to inject as environment variables at create time. Merged with defaults (defaults first, then this list).
* `data_plane_mode` (`DataPlaneMode | str | None`): Transport policy for exec, logs, and file operations. `auto` prefers direct mTLS with gateway fallback.
* `containers` (`Sequence[Container | Mapping[str, Any]] | None`): Multi-container spec. Mutually exclusive with positional command/args and with `container_image`, `resources`, `mounted_files`, `secrets`, `image_pull_credentials`, `environment_variables`, `security_context`, and `working_dir`. This list replaces those single-container fields, including the same names on `SandboxDefaults`. Put secrets, env, and working\_dir on each `Container`.

Returns:
A Sandbox instance (start request sent, but may still be starting)
**Examples**

```python theme={"system"}
# Using defaults (shell-trapped keep-alive)
sb = Sandbox.run()

# Fire and forget style
sb = Sandbox.run("echo", "hello")
# sb.sandbox_id is set, but sandbox may still be starting

# Wait for ready if needed
sb = Sandbox.run("sleep", "infinity").wait()
result = sb.exec(["echo", "hello"]).result()

# Or use context manager for automatic cleanup
with Sandbox.run("sleep", "infinity") as sb:
    result = sb.exec(["echo", "hello"]).result()
```

### run\_from\_template

```python theme={"system"}
run_from_template(template_id: str, *args: str = (), command: str | None = None, defaults: SandboxDefaults | None = None, **kwargs: Any = {}) -> Sandbox
```

Create a sandbox from an organization template (CreateSandboxFromTemplate).
**Parameters**

* `template_id` (`str`): Organization-scoped template UUID.
* `*args` (`str`): Optional command args override. Honored without `command`. Sparse single-container overlays still require `container_image`.
* `command` (`str | None`): Optional command override. Requires `container_image` unless `containers=` replaces the whole list.
* `defaults` (`SandboxDefaults | None`): Optional SandboxDefaults.
* `**kwargs` (`Any`): Same advanced create kwargs as `run()`. Passing `container_image` replaces the whole template container (command, args, env, files, resources, name `main`); there is no fetch-and-merge. `containers=` is a full list replace and does not require `container_image`. Other container-field overlays (`command`, `args`, `environment_variables`, `secrets`, `resources`, `mounted_files`, `volumes`, `file_system_snapshot`, `image_pull_credentials`, `security_context`, `working_dir`) require `container_image` unless `containers=` replaces the list: the API replaces the whole container list and rejects a sparse patch. Session/default tags are merged and sent as a replace-on-presence override so `list()`/`adopt` can find the sandbox; environment variables and annotations are not merged (template-owned).

**Returns**

* `Sandbox`: Sandbox handle (lazy-start).

### run\_from\_file

```python theme={"system"}
run_from_file(contents: str | Path | bytes, *, primary_service: str, file_type: SandboxFileType | str = SandboxFileType.COMPOSE, image_overrides: Mapping[str, str] | None = None, default_resources: ResourceOptions | dict[str, Any] | None = None, defaults: SandboxDefaults | None = None, auth: AuthConfig | None = None, request_timeout_seconds: float | None = None, poll_retry_budget_seconds: float | None = None, poll_rpc_timeout_seconds: float | None = None, max_lifetime_seconds: float | None = None, tags: list[str] | None = None, runner_ids: list[str] | None = None, network: NetworkOptions | dict[str, Any] | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, annotations: dict[str, str] | None = None, request_id: str | None = None, data_plane_mode: DataPlaneMode | str | None = None, **kwargs: Any = {}) -> Sandbox
```

Create a sandbox from an uploaded file (CreateSandboxFromFile).

v1 Compose only, pull-only images. Reads `contents` as raw bytes and
does not normalize YAML: the same `request_id` with different bytes
(including whitespace-only edits) is `CWSANDBOX_REQUEST_ID_CONFLICT`.
Returns immediately once the backend accepts; reuse `wait()` for
RUNNING. Do not wait for `PREPARING`.

GetSandbox returns the translated spec, not the source file. A leftover
Compose `build:` is `CWSANDBOX_NOT_IMPLEMENTED`. Skip-build by
setting `image:` in the YAML or `image_overrides`.
**Parameters**

* `contents` (`str | Path | bytes`): Compose file path (`str` / `Path`) or raw YAML bytes. A `str` is always opened as a path; pass Compose text as `bytes` (`.encode("utf-8")`). Cap is 256 KiB. Bytes are sent as-is.
* `primary_service` (`str`): Compose service that is the sandbox primary.
* `file_type` (`SandboxFileType | str`): Document type. Defaults to `compose`.
* `image_overrides` (`Mapping[str, str] | None`): Per-service pullable image refs. Keys must be services in `contents`.
* `default_resources` (`ResourceOptions | dict[str, Any] | None`): CPU/memory copied onto each service that omitted `deploy.resources`. Per container, not a project budget. GPU is rejected locally (Gateway also rejects it).
* `defaults` (`SandboxDefaults | None`): Optional `SandboxDefaults`. Tags, network, `placement_mode`, `runner_ids`, annotations, object-storage access, and max lifetime are inherited. Container/volume/ service defaults are not. Non-strict `placement_spillover` on defaults is ignored (from-file is always strict). An explicit non-strict keyword argument raises.
* `request_id` (`str | None`): Optional idempotency token. Auto-generated when omitted.
* `**kwargs` (`Any`): Rejected. This RPC does not accept volumes, published services, `runtime_class`, `image_pull_credentials`, `network_ids`, or `build_contexts`.

**Returns**

* `Sandbox`: Sandbox handle (create accepted; may still be starting).

### session

```python theme={"system"}
session(defaults: SandboxDefaults | Mapping[str, Any] | None = None, *, auth: AuthConfig | None = None) -> Session
```

Create a session for managing multiple sandboxes.

Sessions provide:

* Shared configuration via defaults

* Automatic cleanup of orphaned sandboxes

* Function execution via @session.function() decorator
  **Parameters**

* `defaults` (`SandboxDefaults | Mapping[str, Any] | None`): Optional defaults to apply to sandboxes created via session

* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider. Overrides `defaults.auth` when provided.

**Returns**

* `Session`: A Session instance

**Examples**

```python theme={"system"}
session = Sandbox.session(defaults)
sb = session.create(command="sleep", args=["infinity"])

@session.function()
def compute(x, y):
    return x + y

await session.close()
```

### list

```python theme={"system"}
list(*, tags: list[str] | None = None, status: str | None = None, profile_ids: list[str] | None = None, profile_names: list[str] | None = None, runner_ids: list[str] | None = None, show_terminated: bool = False, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None, poll_retry_budget_seconds: float | None = None, poll_rpc_timeout_seconds: float | None = None, data_plane_mode: DataPlaneMode | str = DataPlaneMode.AUTO, volume_ids: list[str] | tuple[str, ...] | None = None) -> OperationRef[list[Sandbox]]
```

List existing sandboxes with optional filters.

Returns OperationRef that resolves to Sandbox instances usable for
operations like exec(), stop(), get\_status(), read\_file(), write\_file().

By default, only active (non-terminal) sandboxes are returned.
Set `show_terminated=True` to widen the search to include terminal
sandboxes (completed, failed, terminated).
A terminal status filter (e.g. `status="completed"`) also widens
the search automatically.
**Parameters**

* `tags` (`list[str] | None`): Filter by tags (sandboxes must have ALL specified tags)
* `status` (`str | None`): Filter by status ("running", "completed", "failed", etc.)
* `profile_ids` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `profile_names` (`list[str] | None`): Removed in 1.x; passing a value raises `TypeError`.
* `runner_ids` (`list[str] | None`): Filter by runner IDs
* `volume_ids` (`list[str] | tuple[str, ...] | None`): Filter to sandboxes attached to these registered Volume IDs
* `show_terminated` (`bool`): If True, include terminal sandboxes (completed, failed, terminated). Defaults to False.
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default)
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s)
* `poll_retry_budget_seconds` (`float | None`): Wall-clock budget for retrying transient errors on the sandbox-status poll loop (default: 30s). Set to 0 to disable retry. Applied to returned Sandbox instances.
* `poll_rpc_timeout_seconds` (`float | None`): Per-call timeout for poll Get RPCs (default: 15s). Separate from `timeout_seconds`. Applied to returned Sandbox instances.
* `data_plane_mode` (`DataPlaneMode | str`): Transport policy applied to returned sandboxes.

**Returns**

* `OperationRef[list[Sandbox]]`: OperationRef\[list\[Sandbox]]: Use .result() to block for results,
* `OperationRef[list[Sandbox]]`: or await directly in async contexts.

**Examples**

```python theme={"system"}
# Sync usage - active sandboxes only (default)
sandboxes = Sandbox.list(tags=["my-batch-job"]).result()
for sb in sandboxes:
    print(f"{sb.sandbox_id}: {sb.status}")
    sb.stop().result()

# Include stopped sandboxes
all_sandboxes = Sandbox.list(
    tags=["my-batch-job"], show_terminated=True
).result()

# Async usage
sandboxes = await Sandbox.list(status="running")
for sb in sandboxes:
    result = await sb.exec(["echo", "hello"])
```

### from\_id

```python theme={"system"}
from_id(sandbox_id: str, *, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None, poll_retry_budget_seconds: float | None = None, poll_rpc_timeout_seconds: float | None = None, data_plane_mode: DataPlaneMode | str = DataPlaneMode.AUTO) -> OperationRef[Sandbox]
```

Attach to an existing sandbox by ID.

Creates a Sandbox instance connected to an existing sandbox,
allowing operations like exec(), stop(), get\_status(), etc.
**Parameters**

* `sandbox_id` (`str`): The ID of the existing sandbox
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default)
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s)
* `poll_retry_budget_seconds` (`float | None`): Wall-clock budget for retrying transient errors on the sandbox-status poll loop (default: 30s). Set to 0 to disable retry. Applied to the returned Sandbox instance.
* `poll_rpc_timeout_seconds` (`float | None`): Per-call timeout for poll Get RPCs (default: 15s). Separate from `timeout_seconds`. Applied to the returned Sandbox instance.
* `data_plane_mode` (`DataPlaneMode | str`): Transport policy applied to the returned sandbox.

**Returns**

* `OperationRef[Sandbox]`: OperationRef\[Sandbox]: Use .result() to block for the Sandbox instance,
* `OperationRef[Sandbox]`: or await directly in async contexts.

**Raises**

* `SandboxNotFoundError`: If sandbox doesn't exist

**Examples**

```python theme={"system"}
# Sync usage
sb = Sandbox.from_id("sandbox-abc123").result()
result = sb.exec(["python", "-c", "print('hello')"]).result()
sb.stop().result()

# Async usage
sb = await Sandbox.from_id("sandbox-abc123")
result = await sb.exec(["python", "-c", "print('hello')"])
```

### delete

```python theme={"system"}
delete(sandbox_id: str, *, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None, missing_ok: bool = False) -> OperationRef[None]
```

Delete a sandbox by ID without creating a Sandbox instance.

This is a convenience method for cleanup scenarios where you
don't need to perform other operations on the sandbox.
**Parameters**

* `sandbox_id` (`str`): The sandbox ID to delete
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default)
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s)
* `missing_ok` (`bool`): If True, suppress SandboxNotFoundError when sandbox doesn't exist.

**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block until complete.
* `OperationRef[None]`: Raises SandboxNotFoundError if not found (unless missing\_ok=True),
* `OperationRef[None]`: SandboxError if deletion failed.

**Raises**

* `SandboxNotFoundError`: If sandbox doesn't exist and missing\_ok=False
* `SandboxError`: If deletion failed for other reasons

**Examples**

```python theme={"system"}
# Sync usage
Sandbox.delete("sandbox-abc123").result()

# Ignore if already deleted
Sandbox.delete("sandbox-abc123", missing_ok=True).result()

# Async usage
await Sandbox.delete("sandbox-abc123")
```

### get\_snapshot

```python theme={"system"}
get_snapshot(file_system_snapshot_id: str, *, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None) -> OperationRef[FileSystemSnapshot]
```

Fetch a file-system snapshot (FSS) record by ID.

Snapshots are org-scoped: any snapshot owned by your organization is
visible, regardless of which sandbox created it.
**Parameters**

* `file_system_snapshot_id` (`str`): The snapshot ID to fetch.
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default).
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s).

**Returns**

* `OperationRef[FileSystemSnapshot]`: OperationRef\[FileSystemSnapshot]: Use .result() to block or await.
* `OperationRef[FileSystemSnapshot]`: Raises SnapshotNotFoundError if the snapshot does not exist.

**Examples**

```python theme={"system"}
snap = Sandbox.get_snapshot("fss-abc123").result()
print(snap.status, snap.size_bytes)
```

### list\_snapshots

```python theme={"system"}
list_snapshots(*, source_sandbox_id: str | None = None, status: FileSystemSnapshotStatus | str | None = None, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None) -> OperationRef[list[FileSystemSnapshot]]
```

List file-system snapshots (FSS) for the organization.

Snapshots are org-scoped and the listing is auto-paginated. The
`source_sandbox_id` and `status` filters are applied client-side
(the backend list RPC does not filter), so all snapshots are fetched
before filtering.
**Parameters**

* `source_sandbox_id` (`str | None`): If set, only snapshots captured from this sandbox.
* `status` (`FileSystemSnapshotStatus | str | None`): If set, only snapshots in this status (FileSystemSnapshotStatus or its string value).
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default).
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s).

**Returns**

* `OperationRef[list[FileSystemSnapshot]]`: OperationRef\[list\[FileSystemSnapshot]]: Use .result() to block or await.

**Examples**

```python theme={"system"}
# All ready snapshots from a given sandbox
snaps = Sandbox.list_snapshots(
    source_sandbox_id=sb.sandbox_id,
    status=FileSystemSnapshotStatus.READY,
).result()
```

### delete\_snapshot

```python theme={"system"}
delete_snapshot(file_system_snapshot_id: str, *, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None, missing_ok: bool = False) -> OperationRef[None]
```

Delete a file-system snapshot (FSS) by ID.

Deleting a snapshot does not affect sandboxes already restored from it.
**Parameters**

* `file_system_snapshot_id` (`str`): The snapshot ID to delete.
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default).
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s).
* `missing_ok` (`bool`): If True, suppress SnapshotNotFoundError when the snapshot doesn't exist (already deleted).

**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block or await.
* `OperationRef[None]`: Raises SnapshotNotFoundError if not found (unless missing\_ok=True).

**Examples**

```python theme={"system"}
Sandbox.delete_snapshot("fss-abc123").result()
Sandbox.delete_snapshot("fss-abc123", missing_ok=True).result()
```

### get\_snapshot\_bucket\_config

```python theme={"system"}
get_snapshot_bucket_config(*, base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None) -> OperationRef[FileSystemSnapshotBucketConfig]
```

Fetch the organization's FSS object-storage bucket configuration.
**Parameters**

* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default).
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s).

**Returns**

* `OperationRef[FileSystemSnapshotBucketConfig]`: OperationRef\[FileSystemSnapshotBucketConfig]: Use .result() or await.

**Examples**

```python theme={"system"}
cfg = Sandbox.get_snapshot_bucket_config().result()
print(cfg.mode, cfg.effective_bucket_name)
```

### set\_snapshot\_bucket\_config

```python theme={"system"}
set_snapshot_bucket_config(*, bucket_name: str, region: str = '', base_url: str | None = None, auth: AuthConfig | None = None, timeout_seconds: float | None = None) -> OperationRef[FileSystemSnapshotBucketConfig]
```

Set the organization's FSS object-storage bucket configuration.

Provide a `bucket_name` to use a bring-your-own bucket; pass an empty
string to revert to the CoreWeave-managed bucket. This is an
admin-gated operation.
**Parameters**

* `bucket_name` (`str`): Bucket to archive snapshots to. Empty string reverts to the CoreWeave-managed bucket.
* `region` (`str`): Bucket region (required by some providers for BYO buckets).
* `base_url` (`str | None`): Override API URL (default: CWSANDBOX\_BASE\_URL env or default).
* `auth` (`AuthConfig | None`): Authentication strategy, resolved headers, or provider for this request.
* `timeout_seconds` (`float | None`): Request timeout (default: 300s).

**Returns**

* `OperationRef[FileSystemSnapshotBucketConfig]`: OperationRef\[FileSystemSnapshotBucketConfig]: The updated config.

**Examples**

```python theme={"system"}
# Bring-your-own bucket
Sandbox.set_snapshot_bucket_config(
    bucket_name="my-org-fss", region="us-east-1"
).result()

# Revert to CoreWeave-managed
Sandbox.set_snapshot_bucket_config(bucket_name="").result()
```

### get\_status

```python theme={"system"}
get_status() -> SandboxStatus
```

Get the current status of the sandbox.

For terminal sandboxes (COMPLETED/FAILED/TERMINATED), returns the cached
status without an API call. For active sandboxes, fetches from backend.
**Returns**

* `SandboxStatus`: SandboxStatus enum value

**Raises**

* `SandboxNotRunningError`: If sandbox has not been started

**Examples**

```python theme={"system"}
sb = Sandbox.run("sleep", "10")
status = sb.get_status()
print(f"Sandbox is {status}")  # SandboxStatus.PENDING or RUNNING
```

### start

```python theme={"system"}
start() -> OperationRef[None]
```

Send StartSandbox to backend, return OperationRef immediately.

Does NOT wait for RUNNING status. Use wait() to block until ready.
Call .result() to block until the start request is accepted.
**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block until backend accepts.

**Examples**

```python theme={"system"}
sandbox = Sandbox(command="sleep", args=["infinity"])
sandbox.start().result()
print(f"Started sandbox: {sandbox.sandbox_id}")
sandbox.wait()  # Block until RUNNING
```

### wait

```python theme={"system"}
wait(timeout: float | None = None) -> Sandbox
```

Block until sandbox reaches RUNNING or a terminal state.

Returns when sandbox is RUNNING or has already completed (COMPLETED/UNSPECIFIED).
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means use default timeout.

**Returns**

* `Sandbox`: Self for method chaining. Check .status to determine final state.

**Raises**

* `SandboxFailedError`: If sandbox fails to start
* `SandboxTerminatedError`: If sandbox was terminated externally
* `SandboxTimeoutError`: If timeout expires

**Examples**

```python theme={"system"}
sb = Sandbox.run("sleep", "infinity").wait()
result = sb.exec(["echo", "ready"]).result()
```

### wait\_until\_complete

```python theme={"system"}
wait_until_complete(timeout: float | None = None, *, raise_on_termination: bool = True) -> OperationRef[Sandbox]
```

Wait until sandbox reaches terminal state (COMPLETED/FAILED/TERMINATED).

Returns an OperationRef that resolves when the sandbox reaches a terminal state.
After resolving, returncode will be available when the backend
recorded one (see the `returncode` property for the cases where it
stays None).
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means use default timeout.
* `raise_on_termination` (`bool`): If True (default), raises SandboxTerminatedError when this client called stop() or the backend reports legacy TERMINATED status. External kills (infrastructure, lifetime limits, other clients) that result in COMPLETED are not detectable until the backend provides termination\_reason metadata. Set to False to suppress SandboxTerminatedError entirely.

**Returns**

* `OperationRef[Sandbox]`: OperationRef\[Sandbox]: Use .result() to block or await in async contexts.

**Raises**

* `SandboxTimeoutError`: If timeout expires
* `SandboxTerminatedError`: If sandbox was stopped by this client or reported as TERMINATED by backend (and raise\_on\_termination=True)
* `SandboxFailedError`: If sandbox failed

**Note:** `poll_retry_budget_seconds` is a hard sub-timeout inside the user's `timeout` parameter. A 30s retry budget with a 300s user timeout can surface budget-exhaustion errors around 30s. Callers that want longer retry should configure `poll_retry_budget_seconds` accordingly.

**Examples**

```python theme={"system"}
sb = Sandbox.run("python", "-c", "print('done')")
sb.wait_until_complete().result()
print(f"Exit code: {sb.returncode}")
```

### stop

```python theme={"system"}
stop(*, snapshot_on_stop: bool = False, graceful_shutdown_seconds: float = DEFAULT_GRACEFUL_SHUTDOWN_SECONDS, missing_ok: bool = False, wait_for_ready: bool = True, request_id: str | None = None) -> OperationRef[None]
```

Stop sandbox, return OperationRef immediately.

The sandbox transitions through TERMINATING (grace period draining)
before reaching a terminal state (COMPLETED or FAILED). The returned
OperationRef resolves when the backend confirms a terminal state, not
just when the stop RPC succeeds.

Multiple callers share the same underlying stop task: the first caller
creates it, subsequent callers join it. A `snapshot_on_stop=True`
request that would join (or observe) a stop that is not capturing a
snapshot, because the sandbox is already stopping, already stopped, or
a plain `stop()` is already in flight, raises
`SnapshotOnStopConflictError` instead of silently completing without
an archive. Plain stops always coalesce.

The sandbox is deregistered from its session regardless of whether
the stop was successful, since the sandbox is no longer usable.
**Parameters**

* `snapshot_on_stop` (`bool`): If True, capture a file-system snapshot (FSS) of the configured mount before shutdown. The resulting snapshot ID is available via the `file_system_snapshot_id` property after the returned OperationRef resolves. Requires the sandbox to have been started with a `file_system_snapshot` mount and the org to be enabled for FSS. Raises `SnapshotOnStopConflictError` if a stop is already in progress that will not capture a snapshot.
* `graceful_shutdown_seconds` (`float`): Time to wait for graceful shutdown. With `snapshot_on_stop=True` this is the post-archive pod-delete grace, applied *after* the snapshot completes, so the client deadline covers the archive budget plus this grace. In v1, `grace_period_seconds=0` means immediate termination (no backend grace substitute). The backend caps this at 300s for snapshot-on-stop.
* `missing_ok` (`bool`): If True, suppress SandboxNotFoundError when the sandbox does not exist. With `snapshot_on_stop=True` the flag is still sent as `allow_missing`; a missing sandbox or a server reject of that combination raises `SnapshotOnStopConflictError` rather than succeeding with no archive.
* `wait_for_ready` (`bool`): When `snapshot_on_stop` is True, block until the snapshot reaches READY (or FAILED) before the stop completes. Ignored when `snapshot_on_stop` is False.
* `request_id` (`str | None`): Optional client-supplied key to deduplicate the snapshot-on-stop request on retries. Ignored when `snapshot_on_stop` is False.

**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block until terminal.
* `OperationRef[None]`: Raises SandboxError on failure, SandboxNotFoundError if not found
* `OperationRef[None]`: (unless missing\_ok=True).

**Examples**

```python theme={"system"}
sb.stop().result()  # Block until terminal (COMPLETED/FAILED)

# Ignore if already deleted
sb.stop(missing_ok=True).result()

# Snapshot the configured mount on stop, then read the ID
sb.stop(snapshot_on_stop=True).result()
file_system_snapshot_id = sb.file_system_snapshot_id

# wait_until_complete() after stop() resolves when terminal
sb.stop()
sb.wait_until_complete().result()  # Polls through TERMINATING
```

### snapshot

```python theme={"system"}
snapshot(*, wait_for_ready: bool = True, request_id: str | None = None) -> OperationRef[str]
```

Capture a file-system snapshot (FSS) of the configured mount.

Snapshots the directory configured via `file_system_snapshot` on the
running sandbox, without stopping it. Starts the sandbox first if it has
not been started. Restore the snapshot into a new sandbox via
`Sandbox.run(file_system_snapshot=FileSystemSnapshotOptions(...,
file_system_snapshot_id=<id>))`.

Requires the sandbox to have been started with a `file_system_snapshot`
mount and the organization to be enabled for FSS.
**Parameters**

* `wait_for_ready` (`bool`): Block until the snapshot reaches READY (or FAILED) before returning. When False, returns once the snapshot is created (likely still CREATING).
* `request_id` (`str | None`): Optional client-supplied key to deduplicate the request on retries.

**Returns**

* `OperationRef[str]`: OperationRef\[str]: Use .result() to block (or await) for the new
* `OperationRef[str]`: snapshot's ID. Call `Sandbox.get_snapshot(id)` for the full record
* `OperationRef[str]`: (status, size, timestamps).

**Raises**

* `SandboxSnapshotError`: If the snapshot fails (see subclasses for `NOT_SUPPORTED` when the org is not enabled, quota/size, etc.).

**Examples**

```python theme={"system"}
with Sandbox.run(
    file_system_snapshot=FileSystemSnapshotOptions(mount_path="/workspace"),
) as sb:
    sb.exec(["sh", "-c", "echo hi > /workspace/note.txt"]).result()
    snapshot_id = sb.snapshot().result()
    # Inspect the full record if needed:
    snap = Sandbox.get_snapshot(snapshot_id).result()
```

### exec

```python theme={"system"}
exec(command: Sequence[str], *, cwd: str | None = None, check: bool = False, timeout_seconds: float | None = None, stdin: bool = False, container: str | None = None) -> Process
```

Execute command, return Process immediately.

Note: If sandbox is not yet RUNNING, this method waits for it first.
The timeout\_seconds parameter only applies to command execution, not to
the initial wait for RUNNING status.
**Parameters**

* `command` (`Sequence[str]`): Command and arguments to execute
* `cwd` (`str | None`): Working directory for command execution. Must be an absolute path. When specified, the command is wrapped with a shell cd.
* `check` (`bool`): If True, raise SandboxExecutionError on non-zero returncode
* `timeout_seconds` (`float | None`): Timeout for command execution (after sandbox is RUNNING). Does not include time waiting for sandbox to reach RUNNING status.
* `stdin` (`bool`): If True, enable stdin streaming. Process.stdin will be a StreamWriter that can send input to the command. If False (default), stdin is closed immediately and Process.stdin is None.
* `container` (`str | None`): Container name to exec into. Empty/None targets the primary.

**Returns**

* `Process`: Process handle with streaming stdout/stderr. Call .result() to block
* `Process`: for the final ProcessResult, or iterate over .stdout/.stderr for
* `Process`: real-time output. When stdin=True, Process.stdin is a StreamWriter.

**Raises**

* `ValueError`: If command is empty or cwd is invalid (empty or relative path)

**Examples**

```python theme={"system"}
# Get result directly
process = sb.exec(["echo", "hello"])
result = process.result()
print(result.stdout)

# With working directory
result = sb.exec(["ls", "-la"], cwd="/app").result()

# Stream output in real-time
process = sb.exec(["python", "script.py"])
for line in process.stdout:
    print(line)
result = process.result()

# With stdin streaming
process = sb.exec(["cat"], stdin=True)
process.stdin.write(b"hello world").result()
process.stdin.close().result()
result = process.result()

# Async usage
result = await sb.exec(["echo", "hello"])
```

### shell

```python theme={"system"}
shell(command: Sequence[str] | None = None, *, width: int | None = None, height: int | None = None, container: str | None = None) -> TerminalSession
```

Start an interactive TTY session in the sandbox.

Returns a TerminalSession optimized for interactive terminal use:
raw byte output (no decode/re-encode), no output buffering, and
fire-and-forget stdin.
**Parameters**

* `command` (`Sequence[str] | None`): Shell command to execute. Defaults to \["/bin/bash"]. Accepts a sequence like \["/bin/sh"] or \["/usr/bin/python3"].
* `width` (`int | None`): Initial terminal width in columns.
* `height` (`int | None`): Initial terminal height in rows.
* `container` (`str | None`): Container name for the TTY session. Empty/None targets the primary.

**Returns**

* `TerminalSession`: TerminalSession handle with .output (StreamReader\[bytes]),
* `TerminalSession`: .stdin (StreamWriter), and .resize(w, h).

**Raises**

* `ValueError`: If command is explicitly empty.

**Example**

```python theme={"system"}
session = sandbox.shell(width=80, height=24)
session.stdin.writeline("echo hello").result()
for chunk in session.output:
    sys.stdout.buffer.write(chunk)
exit_code = session.wait()
```

### read\_file

```python theme={"system"}
read_file(filepath: str, *, timeout_seconds: float | None = None, container: str | None = None) -> OperationRef[bytes]
```

Read file from sandbox, return OperationRef immediately.
**Parameters**

* `filepath` (`str`): Path to file in sandbox
* `timeout_seconds` (`float | None`): Timeout for the operation
* `container` (`str | None`): Container to read from. Empty/None targets the primary.

**Returns**

* `OperationRef[bytes]`: OperationRef\[bytes]: Use .result() to block and retrieve contents.

**Behavior:** Files up to \~32 MiB are read in a single unary call. Larger files (up to \~256 MiB) transparently fall back to a streaming read: the first such fallback per Sandbox logs once at INFO. When the server reports the file's size, files above \~256 MiB are refused with `CWSANDBOX_FILE_TOO_LARGE`; use `read_file_streaming` for those. The whole result is held in memory regardless of path. The client cannot always know the remote size in advance (e.g. when the backend signals the oversized read via resource exhaustion rather than a sized `CWSANDBOX_FILE_TOO_LARGE`), so a very large file can still be buffered in full rather than refused: prefer `read_file_streaming` for anything large to consume it incrementally and bound memory.

**Raises**

* `SandboxFileError`: with `reason == CWSANDBOX_FILE_TOO_LARGE` when the file exceeds the server cap and the server reported its size; or with `reason == CWSANDBOX_FILE_TRUNCATED` when a streamed read comes back short of the file's size (truncation detected against the pre-read size).
* `SandboxStreamBackpressureError`: when a large read falls back to streaming and the output is produced faster than the client reads it (a subclass of SandboxExecutionError).

**Examples**

```python theme={"system"}
data = sb.read_file("/output/result.txt").result()
```

### write\_file

```python theme={"system"}
write_file(filepath: str, contents: bytes, *, timeout_seconds: float | None = None, container: str | None = None) -> OperationRef[None]
```

Write file to sandbox, return OperationRef immediately.
**Parameters**

* `filepath` (`str`): Path to file in sandbox
* `contents` (`bytes`): File contents as bytes
* `timeout_seconds` (`float | None`): Timeout for the operation
* `container` (`str | None`): Container to write into. Empty/None targets the primary.

**Returns**

* `OperationRef[None]`: OperationRef\[None]: Use .result() to block until complete.

**Behavior:** Payloads up to \~32 MiB are written in a single unary call. Larger payloads (up to \~256 MiB) transparently fall back to a streaming write: the first such fallback per Sandbox logs once at INFO. Payloads above \~256 MiB are refused; use `write_file_streaming` for those.

**Raises**

* `SandboxFileError`: with `reason == CWSANDBOX_FILE_TOO_LARGE` when the payload exceeds the server cap, or (without that reason) if a streamed write fails mid-stream and may have left a partial file.
* `SandboxStreamBackpressureError`: when a large write falls back to streaming and the source produces data faster than it can be sent (a subclass of SandboxExecutionError).

**Examples**

```python theme={"system"}
sb.write_file("/input/data.txt", b"content").result()
```

### write\_file\_streaming

```python theme={"system"}
write_file_streaming(filepath: str, source: bytes | Iterable[bytes] | AsyncIterable[bytes], *, timeout_seconds: float | None = None, container: str | None = None) -> OperationRef[None]
```

Stream a file to the sandbox without materializing the full payload.

Prefer this over `write_file` for payloads larger than roughly
32 MiB, or any time the data is already an iterator (file handle,
generator, async producer).
**Parameters**

* `filepath` (`str`): Absolute path inside the sandbox.
* `source` (`bytes | Iterable[bytes] | AsyncIterable[bytes]`): Payload as `bytes`, a sync `Iterable[bytes]`, or an `AsyncIterable[bytes]`. Input is split into frame-safe chunks before transmission. Yielded items must be `bytes`, `bytearray`, or `memoryview`; anything else raises `TypeError`.
* `timeout_seconds` (`float | None`): Wall-clock timeout for the streaming write.

**Returns**

* `OperationRef[None]`: `OperationRef[None]`: call `.result()` to block until complete.

**Raises**

* `SandboxStreamBackpressureError`: if the source produces data faster than it can be sent and the stream is ended early. Yield from a source you can pace, or pre-chunk large uploads; see that exception's docstring for guidance.

**Caveats:** The destination is written directly (no temp-and-rename). A mid-stream cancel or transport error may leave a partial file. The streaming transfer also does not survive a sandbox restart. A synchronous source (e.g. a file handle from `open(...)`) is pulled on a worker thread, so a blocking `read` does not stall the SDK's event loop. An async source is awaited directly. Either is fine; pick whichever is more natural for your data.

### read\_file\_streaming

```python theme={"system"}
read_file_streaming(filepath: str, *, timeout_seconds: float | None = None, container: str | None = None) -> StreamReader[bytes]
```

Stream a file from the sandbox in chunks without buffering the whole payload.

Prefer this over `read_file` for files larger than roughly 32 MiB,
or any time you want to consume the file incrementally (write to
disk, hash on the fly, parse line by line).

For large files, the SDK captures the file's size *before* reading and,
once the stream finishes, verifies that at least that many bytes were
delivered. If fewer arrived, the iterator raises `SandboxFileError`
with reason `CWSANDBOX_FILE_TRUNCATED` so callers can detect a silent
short read rather than consuming a partial file. (Using the pre-read
size means a file appended to during the read is never mistaken for a
truncation.) The check is skipped for small files, where silent
truncation does not occur, and is best-effort when the size cannot be
determined.

If your loop reads chunks slower than the file streams (e.g. you do
slow work between iterations), the read may be ended early with
`SandboxStreamBackpressureError`. Iterate promptly and move slow work
off the read loop; see that exception's docstring for guidance.
**Parameters**

* `filepath` (`str`): Absolute path inside the sandbox.
* `timeout_seconds` (`float | None`): Wall-clock timeout for the streaming read.

**Returns**

* `StreamReader[bytes]`: `StreamReader[bytes]` yielding chunks in order. End-of-file is
* `StreamReader[bytes]`: signaled by normal iterator exhaustion. Errors (missing file,
* `StreamReader[bytes]`: permission denied, truncation, a too-slow reader) are re-raised
* `StreamReader[bytes]`: when the consumer iterates past them.

**Example**

```python theme={"system"}
with contextlib.closing(sb.read_file_streaming("/data/big.bin")) as reader:
    with open("local.bin", "wb") as f:
        for chunk in reader:
            f.write(chunk)
```

**Caveats:** The streaming transfer does not survive a sandbox restart; a long transfer that coincides with a restart will fail mid-stream. Callers should iterate the reader to completion or call `close()` on it. The SDK installs a finalizer to cancel the background task on garbage collection, but explicit close releases resources sooner. A bounded amount of output is buffered ahead of your loop to smooth out bursts and apply backpressure, but it is not a hard memory ceiling: resident memory still grows with how far behind your loop falls. Keep the read loop tight and move slow per-chunk work off it (see `examples/large_file_streaming.py`).

### stream\_logs

```python theme={"system"}
stream_logs(*, follow: bool = False, tail_lines: int | None = None, since_time: datetime | None = None, timestamps: bool = False, timeout_seconds: float | None = None, container: str | None = None) -> StreamReader[str]
```

Stream logs from the sandbox's main process.

Streams stdout/stderr from the sandbox's **main command**: the
entrypoint passed to `Sandbox.run()` (or the default shell-trapped
keep-alive). Output from commands started via `exec()` is **not**
included; use `Process.stdout`/`Process.stderr` for those.

.. note::

Sandboxes created with the default keep-alive command do not
produce any log output. To see logs here, pass a command that
writes to stdout/stderr when calling `Sandbox.run()`.

Returns a StreamReader that yields log lines as strings. The method
returns immediately; iteration on the StreamReader blocks until
data arrives.
**Parameters**

* `follow` (`bool`): If True, continuously stream new logs (like `tail -f`). If False, stream existing logs from the running sandbox and stop. Stopped sandboxes reject `StreamLogs`.
* `tail_lines` (`int | None`): Number of most recent lines to retrieve. If None, returns all available lines.
* `since_time` (`datetime | None`): Only return logs after this timestamp. Must be timezone-aware; naive datetimes raise `ValueError`.
* `timestamps` (`bool`): If True, prefix each line with an ISO 8601 timestamp from the server.
* `timeout_seconds` (`float | None`): Client-side deadline for the gRPC call. Defaults to `request_timeout_seconds` when `follow=False`, and `None` (no timeout) when `follow=True`.
* `container` (`str | None`): Container whose logs to stream. Empty/None targets the primary.

**Returns**

* `StreamReader[str]`: StreamReader yielding log lines as strings. Iterate synchronously
* `StreamReader[str]`: with `for line in reader` or asynchronously with
* `StreamReader[str]`: `async for line in reader`.

**Raises**

* `SandboxNotRunningError`: If `follow=True` and the sandbox has been stopped.
* `SandboxError`: If the log stream encounters an error.

**Example**

```python theme={"system"}
# One-shot: get recent logs
for line in sandbox.stream_logs(tail_lines=100):
    print(line, end="")

# Follow mode: stream continuously
for line in sandbox.stream_logs(follow=True):
    print(line, end="")

# Async usage
async for line in sandbox.stream_logs(follow=True):
    print(line, end="")
```
