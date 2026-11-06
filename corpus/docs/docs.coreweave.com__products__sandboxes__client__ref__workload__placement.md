# Placement

Source: https://docs.coreweave.com/products/sandboxes/client/ref/workload/placement

# Placement

> Where a sandbox runs and how its data operations travel.

## PlacementMode

Source: [src/cwsandbox/\_types.py:115](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L115)

```python theme={"system"}
class PlacementMode
```

* `UNSPECIFIED` = `'unspecified'`
* `SERVERLESS` = `'serverless'`
* `CKS` = `'cks'`

***

## PlacementSpillover

Source: [src/cwsandbox/\_types.py:129](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L129)

```python theme={"system"}
class PlacementSpillover
```

* `STRICT` = `'strict'`
* `CKS_THEN_SERVERLESS` = `'cks_then_serverless'`
* `SERVERLESS_THEN_CKS` = `'serverless_then_cks'`

***

## DataPlaneMode

Source: [src/cwsandbox/\_types.py:168](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L168)

```python theme={"system"}
class DataPlaneMode
```

* `AUTO` = `'auto'`
* `GATEWAY` = `'gateway'`
* `DIRECT` = `'direct'`

***
