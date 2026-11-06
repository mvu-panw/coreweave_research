# OperationRef

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/operation-ref

# OperationRef

> Generic ref for async operations with lazy result retrieval.

Source: [src/cwsandbox/\_types.py:26](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L26)

```python theme={"system"}
class OperationRef(future: concurrent.futures.Future[T])
```

Generic ref for async operations with lazy result retrieval.

OperationRef wraps a concurrent.futures.Future and provides a unified interface
for both synchronous and asynchronous result retrieval. This enables the
sync/async hybrid API where operations return immediately and results are
retrieved lazily.

## Methods

### result

```python theme={"system"}
result(timeout: float | None = None) -> T
```

Block until the result is ready and return it.
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means wait forever.

**Returns**

* `T`: The result of the operation.

**Raises**

* `concurrent.futures.TimeoutError`: If timeout expires before completion.
* `concurrent.futures.CancelledError`: If the operation was cancelled.
* `Exception`: Any exception raised by the operation.
