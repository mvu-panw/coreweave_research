# Exceptions

Source: https://docs.coreweave.com/products/sandboxes/client/ref/exceptions/exceptions

# Exceptions

> Exception hierarchy for cwsandbox error handling.

All cwsandbox exceptions inherit from `CWSandboxError`.

## Hierarchy

```
CWSandboxError
    +-- CWSandboxAuthenticationError
    +-- CWSandboxValidationError
        +-- SandboxValidationError
        +-- DiscoveryValidationError
    +-- SandboxError
        +-- SandboxValidationError
        +-- SandboxNotRunningError
            +-- SandboxUnavailableError
                +-- SnapshotBackendThrottledError
                +-- VolumeRunnerUnavailableError
        +-- SandboxTimeoutError
            +-- SandboxRequestTimeoutError
            +-- SandboxCommandTimeoutError
            +-- SnapshotWaitTimeoutError
            +-- VolumeWaitTimeoutError
        +-- SandboxTerminatedError
        +-- SandboxFailedError
        +-- SandboxNotFoundError
        +-- SandboxExecutionError
            +-- SandboxStreamBackpressureError
            +-- SandboxStreamTruncatedError
        +-- SandboxFileError
        +-- SandboxResourceExhaustedError
        +-- SandboxTerminalStateUnavailableError
        +-- SandboxProtocolError
        +-- SandboxSnapshotError
            +-- SnapshotNotFoundError
            +-- SnapshotNotReadyError
            +-- SnapshotNotSupportedError
            +-- SnapshotSizeExceededError
            +-- SnapshotQuotaExceededError
            +-- SnapshotBucketMismatchError
            +-- SnapshotOnStopConflictError
        +-- VolumeError
            +-- VolumeNotFoundError
            +-- VolumeNotReadyError
            +-- VolumePlacementConflictError
            +-- VolumeTypeNotSupportedError
            +-- VolumeNotSnapshottableError
            +-- VolumeRunnerIneligibleError
            +-- VolumeBackendNotFoundError
            +-- VolumeInUseError
            +-- VolumeQuotaExceededError
            +-- VolumeRunnerUnavailableError
    +-- DiscoveryError
        +-- DiscoveryValidationError
        +-- RunnerNotFoundError
    +-- FunctionError
        +-- AsyncFunctionError
```

## Reference

### CWSandboxError

Source: [src/cwsandbox/exceptions.py:19](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L19)

Base exception for all CWSandbox operations.

**Attributes**

* `reason` (`str | None`): Structured error reason parsed from `google.rpc.ErrorInfo`
  (e.g. `"CWSANDBOX_FILE_NOT_FOUND"`), or `None` when the error
  did not carry AIP-193 details.
* `metadata` (`Mapping[str, str] | None`): Machine-readable metadata from `ErrorInfo.metadata`. Empty
  dict when the error carried no metadata.
* `retry_delay` (`timedelta | None`): Suggested client retry delay parsed from
  `google.rpc.RetryInfo`, or `None` when absent.

### CWSandboxAuthenticationError

Source: [src/cwsandbox/exceptions.py:52](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L52)

Raised when authentication fails.

### CWSandboxValidationError

Source: [src/cwsandbox/exceptions.py:64](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L64)

Raised when the backend returns field-level validation failures.

**Attributes**

* `field_violations` (`Sequence[FieldViolation] | None`): Field-level validation errors returned by the backend.

### SandboxValidationError

Source: [src/cwsandbox/exceptions.py:88](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L88)

Raised when a sandbox request fails field-level validation.

### DiscoveryValidationError

Source: [src/cwsandbox/exceptions.py:604](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L604)

Raised when a discovery request fails field-level validation.

### SandboxError

Source: [src/cwsandbox/exceptions.py:84](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L84)

Base exception for sandbox operations.

### SandboxValidationError

Source: [src/cwsandbox/exceptions.py:88](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L88)

Raised when a sandbox request fails field-level validation.

### SandboxNotRunningError

Source: [src/cwsandbox/exceptions.py:92](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L92)

Raised when an operation requires a running sandbox.

### SandboxUnavailableError

Source: [src/cwsandbox/exceptions.py:302](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L302)

Raised when the sandbox service is transiently unavailable.

### SnapshotBackendThrottledError

Source: [src/cwsandbox/exceptions.py:457](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L457)

Raised when the snapshot backend is transiently throttled or at capacity.

### VolumeRunnerUnavailableError

Source: [src/cwsandbox/exceptions.py:587](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L587)

Raised when the volume's runner is transiently unavailable.

### SandboxTimeoutError

Source: [src/cwsandbox/exceptions.py:96](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L96)

Raised when a sandbox operation times out.

### SandboxRequestTimeoutError

Source: [src/cwsandbox/exceptions.py:312](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L312)

Raised when a gRPC request exceeded its deadline.

### SandboxCommandTimeoutError

Source: [src/cwsandbox/exceptions.py:320](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L320)

Raised when the user's command inside the sandbox timed out.

### SnapshotWaitTimeoutError

Source: [src/cwsandbox/exceptions.py:434](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L434)

Raised when `wait_for_ready` exceeded its budget before the snapshot was READY.

**Attributes**

* `file_system_snapshot_id` (`str | None`): Snapshot ID that was still pending, or None.

### VolumeWaitTimeoutError

Source: [src/cwsandbox/exceptions.py:565](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L565)

Raised when `wait_until_ready` exceeded its budget before READY.

**Attributes**

* `volume_id` (`str | None`): Volume ID that was still pending, or None.

### SandboxTerminatedError

Source: [src/cwsandbox/exceptions.py:100](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L100)

Raised when a sandbox was terminated externally.

### SandboxFailedError

Source: [src/cwsandbox/exceptions.py:104](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L104)

Raised when a sandbox fails to start or encounters a fatal error.

### SandboxNotFoundError

Source: [src/cwsandbox/exceptions.py:108](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L108)

Raised when a sandbox is not found (e.g., already deleted).

**Attributes**

* `sandbox_id` (`str | None`): The ID of the sandbox that was not found, or None.

### SandboxExecutionError

Source: [src/cwsandbox/exceptions.py:128](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L128)

Raised when command execution fails inside a sandbox.

**Attributes**

* `exec_result` (`ProcessResult | None`): The `ProcessResult` from the failed execution, or None.
* `exception_type` (`str | None`): Python exception class name from sandbox stderr, or None.
* `exception_message` (`str | None`): Exception message from sandbox stderr, or None.

### SandboxStreamBackpressureError

Source: [src/cwsandbox/exceptions.py:154](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L154)

Raised when an output stream ended early because it was not being read

**Attributes**

* `stream_code` (`str | None`): The terminal `ExecStreamError.code` that triggered this
  exception (`"STREAM_BACKPRESSURE"`). This is a streaming-channel
  code, NOT an AIP-193 ErrorInfo `reason`: the two namespaces are
  kept distinct, so `.reason` is `None` here and callers should
  branch on the exception class (or `stream_code`) rather than
  `.reason`.

### SandboxStreamTruncatedError

Source: [src/cwsandbox/exceptions.py:217](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L217)

Raised when streamed output was cut short rather than delivered whole.

**Attributes**

* `stream_code` (`str | None`): The terminal `ExecStreamError.code` that triggered this
  exception (`"STREAM_TRUNCATED"`). This is a streaming-channel
  code, NOT an AIP-193 ErrorInfo `reason`: the two namespaces are
  kept distinct, so `.reason` is `None` here and callers should
  branch on the exception class (or `stream_code`) rather than
  `.reason`.

### SandboxFileError

Source: [src/cwsandbox/exceptions.py:279](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L279)

Raised when a file operation fails in the sandbox.

**Attributes**

* `filepath` (`str | None`): The path of the file that caused the error, or None.

### SandboxResourceExhaustedError

Source: [src/cwsandbox/exceptions.py:329](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L329)

Raised when the sandbox service is under resource pressure.

### SandboxTerminalStateUnavailableError

Source: [src/cwsandbox/exceptions.py:337](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L337)

Raised when the backend does not report a terminal state after stop.

### SandboxProtocolError

Source: [src/cwsandbox/exceptions.py:353](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L353)

Raised when the backend returned a response the client could not decode.

### SandboxSnapshotError

Source: [src/cwsandbox/exceptions.py:363](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L363)

Base exception for file-system snapshot (FSS) operation failures.

**Attributes**

* `file_system_snapshot_id` (`str | None`): The file-system snapshot ID involved, when known.

### SnapshotNotFoundError

Source: [src/cwsandbox/exceptions.py:388](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L388)

Raised when a snapshot ID is unknown, deleted, or owned by another org.

### SnapshotNotReadyError

Source: [src/cwsandbox/exceptions.py:395](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L395)

Raised when a snapshot is not in the READY state for the operation.

### SnapshotNotSupportedError

Source: [src/cwsandbox/exceptions.py:403](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L403)

Raised when file-system snapshots are not enabled for the organization.

### SnapshotSizeExceededError

Source: [src/cwsandbox/exceptions.py:412](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L412)

Raised when the requested mount size exceeds the configured maximum.

### SnapshotQuotaExceededError

Source: [src/cwsandbox/exceptions.py:419](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L419)

Raised when the organization's snapshot quota is exhausted.

### SnapshotBucketMismatchError

Source: [src/cwsandbox/exceptions.py:426](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L426)

Raised when a snapshot's bucket differs from the org's current bucket.

### SnapshotOnStopConflictError

Source: [src/cwsandbox/exceptions.py:466](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L466)

Raised when `stop(snapshot_on_stop=True)` cannot capture a snapshot.

### VolumeError

Source: [src/cwsandbox/exceptions.py:479](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L479)

Base exception for registered Volume operation failures.

**Attributes**

* `volume_id` (`str | None`): The volume ID involved, when known.

### VolumeNotFoundError

Source: [src/cwsandbox/exceptions.py:502](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L502)

Raised when a volume ID is unknown, deleted, or owned by another org.

### VolumeNotReadyError

Source: [src/cwsandbox/exceptions.py:509](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L509)

Raised when a volume is not READY for the requested operation.

### VolumePlacementConflictError

Source: [src/cwsandbox/exceptions.py:516](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L516)

Raised when attached volumes pin incompatible runners.

### VolumeTypeNotSupportedError

Source: [src/cwsandbox/exceptions.py:523](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L523)

Raised when the requested volume source is not available for the org.

### VolumeNotSnapshottableError

Source: [src/cwsandbox/exceptions.py:530](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L530)

Raised when a volume source cannot be snapshotted.

### VolumeRunnerIneligibleError

Source: [src/cwsandbox/exceptions.py:537](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L537)

Raised when the volume's runner cannot host the requested sandbox.

### VolumeBackendNotFoundError

Source: [src/cwsandbox/exceptions.py:544](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L544)

Raised when the volume's backing store (e.g. PVC) cannot be found.

### VolumeInUseError

Source: [src/cwsandbox/exceptions.py:551](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L551)

Raised when DeleteVolume is blocked by attached sandboxes.

### VolumeQuotaExceededError

Source: [src/cwsandbox/exceptions.py:558](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L558)

Raised when the organization's volume quota is exhausted.

### VolumeRunnerUnavailableError

Source: [src/cwsandbox/exceptions.py:587](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L587)

Raised when the volume's runner is transiently unavailable.

### DiscoveryError

Source: [src/cwsandbox/exceptions.py:595](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L595)

Base exception for discovery operations (runners, profiles).

### DiscoveryValidationError

Source: [src/cwsandbox/exceptions.py:604](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L604)

Raised when a discovery request fails field-level validation.

### RunnerNotFoundError

Source: [src/cwsandbox/exceptions.py:608](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L608)

Raised when a runner ID is not found.

**Attributes**

* `runner_id` (`str`): The ID of the runner that was not found.

### FunctionError

Source: [src/cwsandbox/exceptions.py:651](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L651)

Base exception for function execution operations.

### AsyncFunctionError

Source: [src/cwsandbox/exceptions.py:655](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L655)

Raised when an async function is passed to @session.function().
