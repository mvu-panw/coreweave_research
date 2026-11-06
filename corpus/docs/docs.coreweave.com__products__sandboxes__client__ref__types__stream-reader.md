# StreamReader

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/stream-reader

# StreamReader

> Sync and async iterable stream reader.

Source: [src/cwsandbox/\_types.py:1520](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1520)

```python theme={"system"}
class StreamReader(queue: asyncio.Queue[_S | Exception | None], loop_manager: _LoopManager, *, cancel: Callable[[], object] | None = None)
```

Sync and async iterable stream reader.

StreamReader wraps an asyncio.Queue and provides both synchronous and
asynchronous iteration interfaces. This enables streaming output to be
consumed in both sync and async contexts.

Used as `StreamReader[str]` for text streams (exec stdout/stderr, logs)
and `StreamReader[bytes]` for raw byte streams (TTY output).

The stream uses None as a sentinel value to signal end-of-stream.
Exception instances in the queue are re-raised to the consumer.

## Methods

### close

```python theme={"system"}
close() -> None
```

Cancel the background producer and mark the stream as exhausted.

Safe to call multiple times. After close(), iteration will raise
StopIteration/StopAsyncIteration on the next call.

Puts a None sentinel on the queue to unblock any consumer currently
waiting inside `queue.get()`.
