# Types

Source: https://docs.coreweave.com/products/sandboxes/client/ref/snapshots/types

# Types

> Enumerations describing snapshot status, trigger, and bucket ownership.

## FileSystemSnapshotStatus

Source: [src/cwsandbox/\_types.py:1322](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1322)

```python theme={"system"}
class FileSystemSnapshotStatus
```

* `UNSPECIFIED` = `'unspecified'`
* `CREATING` = `'creating'`
* `READY` = `'ready'`
* `FAILED` = `'failed'`
* `DELETING` = `'deleting'`

***

## FileSystemSnapshotTrigger

Source: [src/cwsandbox/\_types.py:1343](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1343)

```python theme={"system"}
class FileSystemSnapshotTrigger
```

* `UNSPECIFIED` = `'unspecified'`
* `ON_DELETE` = `'on_delete'`
* `MANUAL` = `'manual'`

***

## FileSystemSnapshotBucketMode

Source: [src/cwsandbox/\_types.py:1357](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1357)

```python theme={"system"}
class FileSystemSnapshotBucketMode
```

* `UNSPECIFIED` = `'unspecified'`
* `CW_MANAGED` = `'cw_managed'`
* `BRING_YOUR_OWN` = `'bring_your_own'`

***
