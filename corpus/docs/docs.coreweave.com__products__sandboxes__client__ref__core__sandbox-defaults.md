# SandboxDefaults

Source: https://docs.coreweave.com/products/sandboxes/client/ref/core/sandbox-defaults

# SandboxDefaults

> Immutable configuration defaults for sandbox creation.

Source: [src/cwsandbox/\_defaults.py:261](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_defaults.py#L261)

```python theme={"system"}
class SandboxDefaults(container_image: str = DEFAULT_CONTAINER_IMAGE, command: str = DEFAULT_COMMAND, args: tuple[str, ...] = DEFAULT_ARGS, base_url: str = DEFAULT_BASE_URL, auth: AuthConfig | None = None, request_timeout_seconds: float = DEFAULT_REQUEST_TIMEOUT_SECONDS, poll_retry_budget_seconds: float = DEFAULT_POLL_RETRY_BUDGET_SECONDS, poll_rpc_timeout_seconds: float = DEFAULT_POLL_RPC_TIMEOUT_SECONDS, max_lifetime_seconds: float | None = DEFAULT_MAX_LIFETIME_SECONDS, temp_dir: str = DEFAULT_TEMP_DIR, tags: tuple[str, ...] = tuple(), runner_ids: tuple[str, ...] | None = None, placement_mode: PlacementMode | str | None = None, placement_spillover: PlacementSpillover | str = PlacementSpillover.STRICT, resources: ResourceOptions | dict[str, Any] | None = None, network: NetworkOptions | None = None, services: tuple[Service, ...] | None = None, volumes: tuple[ScratchVolumeOptions | RegisteredVolumeOptions, ...] | None = None, runtime_class: str | None = None, security_context: SecurityContext | dict[str, Any] | None = None, working_dir: str | None = None, object_storage_access: ObjectStorageAccess | dict[str, Any] | None = None, file_system_snapshot: FileSystemSnapshotOptions | dict[str, Any] | None = None, containers: tuple[Container, ...] | None = None, secrets: tuple[Secret, ...] | None = None, environment_variables: dict[str, str] = dict(), annotations: dict[str, str] = dict(), data_plane_mode: DataPlaneMode | str = DataPlaneMode.AUTO)
```

Immutable configuration defaults for sandbox creation.

All fields have sensible defaults. Override only what you need.

There are two separate timeout concepts:

* request\_timeout\_seconds: How long to wait for API responses (client-side)
* max\_lifetime\_seconds: How long the sandbox runs before auto-termination (server-side)
  If not set, the backend controls the default lifetime.

Tags enable filtering and organizing sandboxes. They are propagated to
the backend and can be used to query sandboxes by tag.

**Attributes**

* `container_image` (`str`) : Docker image for the sandbox container. Default: `DEFAULT_CONTAINER_IMAGE`.
* `command` (`str`) : Entrypoint command to run. Default: `DEFAULT_COMMAND`.
* `args` (`tuple[str, ...]`) : Arguments passed to the command. Default: `DEFAULT_ARGS`.
* `base_url` (`str`) : CWSandbox API endpoint URL. Default: `DEFAULT_BASE_URL`.
* `auth` (`AuthConfig | None`) : Authentication selection. Accepts an `AuthStrategy`, resolved
  `AuthHeaders`, or an `AuthProvider`. `None` preserves a
  legacy process-global override when installed and otherwise uses
  `AuthStrategy.COREWEAVE_API_KEY`. Default: `field(default=None, repr=False)`.
* `request_timeout_seconds` (`float`) : Client-side HTTP timeout in seconds for most
  RPCs. Poll Get RPCs use `poll_rpc_timeout_seconds` instead. Default: `DEFAULT_REQUEST_TIMEOUT_SECONDS`.
* `poll_retry_budget_seconds` (`float`) : Wall-clock budget per retry burst (one trip
  to a stable status).  The budget resets on any successful response,
  so a long-lived sandbox that hits a transient error, recovers, then
  hits another much later gets a fresh budget each time.  Retryable
  transient codes are UNAVAILABLE, DEADLINE\_EXCEEDED, and
  RESOURCE\_EXHAUSTED.  Set to 0.0 to disable retries entirely. Default: `DEFAULT_POLL_RETRY_BUDGET_SECONDS`.
* `poll_rpc_timeout_seconds` (`float`) : Per-call timeout for poll Get RPCs. Kept
  separate from `request_timeout_seconds` so a wedged poll fails
  fast instead of blocking on the broader request timeout. Default: `DEFAULT_POLL_RPC_TIMEOUT_SECONDS`.
* `max_lifetime_seconds` (`float | None`) : Server-side sandbox lifetime limit in seconds.
  None lets the backend control the default. Default: `DEFAULT_MAX_LIFETIME_SECONDS`.
* `temp_dir` (`str`) : Temp directory path inside the sandbox. Default: `DEFAULT_TEMP_DIR`.
* `tags` (`tuple[str, ...]`) : Tags for filtering and organizing sandboxes. Default: `field(default_factory=tuple)`.
* `runner_ids` (`tuple[str, ...] | None`) : Restrict to specific runner IDs (CKS). Pass an empty list to
  explicitly clear any default; pass None (the default) to inherit
  any configured default. Incompatible with serverless placement.
* `placement_mode` (`PlacementMode | str | None`) : `PlacementMode` (`serverless` / `cks`) or string.
* `placement_spillover` (`PlacementSpillover | str`) : `PlacementSpillover` policy for a one-shot create
  retry on the alternate mode when the primary fails with a spillable
  capacity/placement reason. Default `STRICT` (no spill). Template
  sandboxes require `STRICT`. Default: `PlacementSpillover.STRICT`.
* `resources` (`ResourceOptions | dict[str, Any] | None`) : Resource configuration. Accepts `ResourceOptions` for separate
  requests/limits, or a flat dict for backward-compatible Guaranteed QoS.
* `network` (`NetworkOptions | None`) : Deny-flag network options and optional create-time hostname
  grants via `NetworkOptions`.
* `services` (`tuple[Service, ...] | None`) : Typed service ports (`Service`) for PUBLIC/PRIVATE/CUSTOM.
* `volumes` (`tuple[ScratchVolumeOptions | RegisteredVolumeOptions, ...] | None`) : Scratch or registered volumes (`ScratchVolumeOptions` or
  `RegisteredVolumeOptions`).
* `runtime_class` (`str | None`) : Optional runtime-class pin (e.g. `"gvisor"`).
* `security_context` (`SecurityContext | dict[str, Any] | None`) : In-guest privilege for the single-container path.
  Not applied when `containers=` or `defaults.containers` is used.
* `working_dir` (`str | None`) : Working directory for the single-container path.
  Not applied when a container list is used.
* `object_storage_access` (`ObjectStorageAccess | dict[str, Any] | None`) : Temporary object-storage credentials.
* `file_system_snapshot` (`FileSystemSnapshotOptions | dict[str, Any] | None`) : Convenience single-mount FSS options via
  `FileSystemSnapshotOptions`. Shareable mount defaults (mount\_path,
  size); an explicit `run()` value replaces it wholesale. Prefer
  `volumes=` for multi-volume setups.
* `containers` (`tuple[Container, ...] | None`) : Optional multi-container spec (`Container`). Mutually
  exclusive with single-container fields on `Sandbox.run()`.
  When this list is used, `secrets`, `environment_variables`,
  `security_context`, and `working_dir` on these defaults
  are not applied; set them on each `Container`.
* `secrets` (`tuple[Secret, ...] | None`) : Secrets for the single-container path. Not applied when
  `containers=` or `defaults.containers` is used.
* `environment_variables` (`dict[str, str]`) : Environment variables for the single-container
  path. Not applied when a container list is used. Default: `field(default_factory=dict)`.
* `annotations` (`dict[str, str]`) : Kubernetes pod annotations (key-value string pairs).
  Merged with per-sandbox annotations; explicit values override defaults.
  Use for non-sensitive metadata only. Default: `field(default_factory=dict)`.
* `data_plane_mode` (`DataPlaneMode | str`) : Transport policy for exec, logs, and file operations.
  `auto` (default) prefers direct mTLS and falls back to the gateway;
  `gateway` disables direct access; `direct` requires it. Default: `DataPlaneMode.AUTO`.

## Methods

### merge\_tags

```python theme={"system"}
merge_tags(additional: Iterable[str] | None) -> list[str]
```

Combine default tags with additional tags.

Tags from both sources are included. Order is: defaults first,
then additional tags appended.

### merge\_environment\_variables

```python theme={"system"}
merge_environment_variables(additional: dict[str, str] | None) -> dict[str, str]
```

Combine default environment variables with additional ones.

Additional environment variables override defaults with the same key.

### merge\_annotations

```python theme={"system"}
merge_annotations(additional: dict[str, str] | None) -> dict[str, str]
```

Combine default annotations with additional ones.

Additional annotations override defaults with the same key.

### with\_overrides

```python theme={"system"}
with_overrides(**kwargs: Any = {}) -> SandboxDefaults
```

Create new defaults with some values overridden.

### from\_dict

```python theme={"system"}
from_dict(d: Mapping[str, Any] | None) -> SandboxDefaults
```

Build `SandboxDefaults` from a mapping, coercing nested fields.

Accepts plain dicts or OmegaConf `DictConfig` objects.  Unknown
keys are silently ignored so callers can pass a config section
that may contain extra fields.

Coercions applied:

* `network` dict -> `NetworkOptions`
* `secrets` list of dicts -> tuple of `Secret`
* `services` list of dicts -> tuple of `Service`
* `volumes` list of dicts -> tuple of scratch/registered volume options
* `containers` list of dicts -> tuple of `Container`
* `security_context` dict -> `SecurityContext`
* `object_storage_access` dict -> `ObjectStorageAccess`
* `args`, `tags`, `runner_ids`, `services`, `volumes`,
  `containers` lists -> tuples
* `resources`, `environment_variables` -> plain `dict`
