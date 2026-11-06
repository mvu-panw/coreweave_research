# Object storage access

Source: https://docs.coreweave.com/products/sandboxes/client/ref/workload/object-storage

# Object storage access

> Temporary object-storage credentials injected into a sandbox's containers.

## ObjectStorageAccess

Source: [src/cwsandbox/\_types.py:937](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L937)

```python theme={"system"}
class ObjectStorageAccess(*, buckets: Sequence[str] = (), permission: ObjectStoragePermission | str | None = None, object_prefix: str | None = None)
```

Temporary object-storage credentials injected into every user container.

**Attributes**

* `buckets` (`Sequence[str]`) : Bucket names the minted credential may access. Default: `()`.
* `permission` (`ObjectStoragePermission | str | None`) : `READ` or `READ_WRITE`. Unset uses the platform default.
* `object_prefix` (`str | None`) : Optional key prefix that scopes the credential.

***

## ObjectStoragePermission

Source: [src/cwsandbox/\_types.py:433](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L433)

```python theme={"system"}
class ObjectStoragePermission
```

* `UNSPECIFIED` = `'unspecified'`
* `READ` = `'read'`
* `READ_WRITE` = `'read_write'`

***
