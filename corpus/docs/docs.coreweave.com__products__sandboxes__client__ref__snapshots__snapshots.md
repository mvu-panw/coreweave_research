# Snapshots

Source: https://docs.coreweave.com/products/sandboxes/client/ref/snapshots/snapshots

# Snapshots

> File-system snapshot records, mount options, and archive bucket configuration.

## FileSystemSnapshot

Source: [src/cwsandbox/\_types.py:1415](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1415)

```python theme={"system"}
class FileSystemSnapshot(*, file_system_snapshot_id: str, status: FileSystemSnapshotStatus, status_reason: str = '', size_bytes: int = 0, source_sandbox_id: str = '', trigger: FileSystemSnapshotTrigger = FileSystemSnapshotTrigger.UNSPECIFIED, request_id: str = '', object_bucket: str = '', source_volume_name: str = '', created_at: datetime | None = None, updated_at: datetime | None = None, completed_at: datetime | None = None)
```

An immutable, org-scoped file-system snapshot record.

Returned by `Sandbox.get_snapshot()` and `Sandbox.list_snapshots()`
(`Sandbox.snapshot()` returns just the snapshot ID). To restore, pass the
`file_system_snapshot_id` to `ScratchVolumeOptions` /
`FileSystemSnapshotOptions` on create.

**Attributes**

* `status_reason` (`str`) : Human-readable detail, typically set for FAILED snapshots. Default: `''`.
* `size_bytes` (`int`) : Archive size in bytes (0 until READY). Default: `0`.
* `source_sandbox_id` (`str`) : The sandbox the snapshot was captured from. Default: `''`.
* `trigger` (`FileSystemSnapshotTrigger`) : Whether the snapshot was taken on delete or via a MANUAL request. Default: `FileSystemSnapshotTrigger.UNSPECIFIED`.
* `request_id` (`str`) : Client-supplied create request id, if any. Default: `''`.
* `object_bucket` (`str`) : The object-storage bucket the archive landed in. Default: `''`.
* `source_volume_name` (`str`) : Scratch volume name the snapshot was taken from. Default: `''`.
* `created_at` (`datetime | None`) : When the snapshot record was created (UTC), or None.
* `updated_at` (`datetime | None`) : When the snapshot record was last updated (UTC), or None.
* `completed_at` (`datetime | None`) : When the snapshot reached a terminal status (UTC), or None.

***

## FileSystemSnapshotOptions

Source: [src/cwsandbox/\_types.py:1371](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1371)

```python theme={"system"}
class FileSystemSnapshotOptions(*, mount_path: str | None = None, size: str | None = None, file_system_snapshot_id: str | None = None, name: str = 'workspace')
```

Convenience single-mount wrapper over a named scratch volume.

Prefer `ScratchVolumeOptions` / `volumes=` for multi-volume sandboxes.
This helper maps to a scratch volume named `workspace` (or `name`).
`mount_path` is optional: omit it to declare the volume without
mounting, and attach it via `Container.volume_mounts`.

**Attributes**

* `mount_path` (`str | None`) : Absolute directory to mount (e.g. "/workspace"). None
  declares the volume without a convenience mount.
* `size` (`str | None`) : Mount size as a Kubernetes resource quantity (e.g. "10Gi").
* `file_system_snapshot_id` (`str | None`) : When set, restore this snapshot at start.
* `name` (`str`) : Scratch volume name (default `"workspace"`). Default: `'workspace'`.

***

## FileSystemSnapshotBucketConfig

Source: [src/cwsandbox/\_types.py:1466](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1466)

```python theme={"system"}
class FileSystemSnapshotBucketConfig(*, mode: FileSystemSnapshotBucketMode = FileSystemSnapshotBucketMode.UNSPECIFIED, bucket_name: str = '', region: str = '', effective_bucket_name: str = '')
```

Per-organization object-storage bucket configuration for FSS archives.

Returned by `Sandbox.get_snapshot_bucket_config()` and
`Sandbox.set_snapshot_bucket_config()`.

**Attributes**

* `mode` (`FileSystemSnapshotBucketMode`) : Bucket ownership mode (CW-managed or bring-your-own). Default: `FileSystemSnapshotBucketMode.UNSPECIFIED`.
* `bucket_name` (`str`) : The configured bucket name (empty when CW-managed). Default: `''`.
* `region` (`str`) : The configured bucket region (empty when CW-managed). Default: `''`.
* `effective_bucket_name` (`str`) : The bucket snapshots are actually archived to,
  resolved server-side from `mode` and `bucket_name`. Default: `''`.

***
