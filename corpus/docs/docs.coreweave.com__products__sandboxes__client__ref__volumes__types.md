# Types

Source: https://docs.coreweave.com/products/sandboxes/client/ref/volumes/types

# Types

> Enumerations describing volume state, locality, and backing store.

## VolumeState

Source: [src/cwsandbox/\_volume.py:59](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_volume.py#L59)

```python theme={"system"}
class VolumeState
```

* `UNSPECIFIED` = `'unspecified'`
* `VALIDATING` = `'validating'`
* `READY` = `'ready'`
* `ERROR` = `'error'`
* `DELETING` = `'deleting'`

***

## VolumeLocality

Source: [src/cwsandbox/\_volume.py:69](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_volume.py#L69)

```python theme={"system"}
class VolumeLocality
```

* `UNSPECIFIED` = `'unspecified'`
* `CLUSTER_LOCAL` = `'cluster_local'`
* `GLOBAL` = `'global'`

***

## StorageMedium

Source: [src/cwsandbox/\_types.py:425](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L425)

```python theme={"system"}
class StorageMedium
```

* `UNSPECIFIED` = `'unspecified'`
* `DISK` = `'disk'`
* `MEMORY` = `'memory'`

***
