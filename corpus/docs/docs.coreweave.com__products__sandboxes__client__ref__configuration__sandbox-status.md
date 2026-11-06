# SandboxStatus

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/sandbox-status

# SandboxStatus

> Sandbox lifecycle status values.

Source: [src/cwsandbox/\_sandbox.py:286](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_sandbox.py#L286)

Sandbox lifecycle status values.

Lifecycle: CREATING | PREPARING -> RUNNING -> TERMINATING -> COMPLETED | FAILED

## Members

* `RUNNING` = `'running'`
* `CREATING` = `'creating'`
* `PREPARING` = `'preparing'`
* `PENDING` = `'pending'`
* `PAUSED` = `'paused'`
* `TERMINATING` = `'terminating'`
* `COMPLETED` = `'completed'`
* `FAILED` = `'failed'`
* `TERMINATED` = `'terminated'`
* `UNSPECIFIED` = `'unspecified'`

## Methods

### from\_proto

```python theme={"system"}
from_proto(proto_status: int) -> SandboxStatus
```

Convert protobuf State enum to SandboxStatus.

### to\_proto

```python theme={"system"}
to_proto() -> int
```

Convert SandboxStatus to protobuf State enum.
