# Volumes

Source: https://docs.coreweave.com/products/sandboxes/client/ref/volumes/volumes

# Volumes

> Registered volumes, scratch volumes, and how they mount into containers.

## Volume

Source: [src/cwsandbox/\_volume.py:107](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_volume.py#L107)

```python theme={"system"}
class Volume(*, volume_id: str, pvc: PvcVolumeSource | None = None, read_only: bool = False, description: str = '', state: VolumeState = VolumeState.UNSPECIFIED, state_reason: str = '', locality: VolumeLocality = VolumeLocality.UNSPECIFIED, access_modes: tuple[str, ...] = (), capacity: str = '', attached_sandbox_count: int = 0, created_at: datetime | None = None, updated_at: datetime | None = None, last_validated_at: datetime | None = None, base_url: str | None = None, timeout_seconds: float | None = None, auth: AuthConfig | None = None)
```

An org-registered shared volume.

Create returns immediately in `VALIDATING`; poll with
`wait_until_ready()` or `get()` until `READY` / `ERROR`.
Mount via `RegisteredVolumeOptions` on `Sandbox.run(volumes=...)`.

***

## VolumeMount

Source: [src/cwsandbox/\_types.py:878](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L878)

```python theme={"system"}
class VolumeMount(*, volume: str, mount_path: str, read_only: bool = False, sub_path: str | None = None)
```

Mount of a sandbox-level volume into one container.

**Attributes**

* `read_only` (`bool`) : When True, mount the volume read-only. Default: `False`.
* `sub_path` (`str | None`) : Optional path within the volume to mount.

***

## PvcVolumeSource

Source: [src/cwsandbox/\_volume.py:77](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_volume.py#L77)

```python theme={"system"}
class PvcVolumeSource(*, runner_id: str, namespace: str, claim_name: str, sub_path: str | None = None)
```

Existing PersistentVolumeClaim referenced by a registered Volume.

***

## RegisteredVolumeOptions

Source: [src/cwsandbox/\_types.py:819](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L819)

```python theme={"system"}
class RegisteredVolumeOptions(*, name: str, volume_id: str, mount_path: str, sub_path: str | None = None, read_only: bool = False)
```

Mount a registered Volume into the sandbox.

**Attributes**

* `sub_path` (`str | None`) : Relative path inside the volume to mount instead of its root.
  Combined with any volume-level prefix set at registration.
* `read_only` (`bool`) : Mount the volume read-only. Default: `False`.

***

## ScratchVolumeOptions

Source: [src/cwsandbox/\_types.py:765](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L765)

```python theme={"system"}
class ScratchVolumeOptions(*, name: str, mount_path: str | None = None, size: str | None = None, restore_from_snapshot_id: str | None = None, medium: StorageMedium | str | None = None, sub_path: str | None = None, read_only: bool = False)
```

Named scratch volume for snapshot/restore workflows.

Volumes are sandbox-level. `mount_path` is a convenience that mounts
this volume on the primary container. For multi-container sandboxes,
omit `mount_path` and declare mounts on `Container.volume_mounts`.

**Attributes**

* `mount_path` (`str | None`) : Absolute path to mount into the primary container. None
  declares the volume without mounting it.
* `size` (`str | None`) : Volume size (e.g. `"10Gi"`). None uses the platform default.
* `restore_from_snapshot_id` (`str | None`) : When set, restore this snapshot at create.
* `medium` (`StorageMedium | str | None`) : Backing store. Unset uses disk. `MEMORY` is tmpfs and
  counts against container memory.
* `sub_path` (`str | None`) : Relative path inside the volume to mount instead of its root.
* `read_only` (`bool`) : Mount the volume read-only. Default: `False`.

***
