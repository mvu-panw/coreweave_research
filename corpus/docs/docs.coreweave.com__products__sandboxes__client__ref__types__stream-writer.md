# StreamWriter

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/stream-writer

# StreamWriter

> Sync and async writer for streaming input to a process.

Source: [src/cwsandbox/\_types.py:1642](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1642)

```python theme={"system"}
class StreamWriter(queue: asyncio.Queue[bytes | None], loop_manager: _LoopManager)
```

Sync and async writer for streaming input to a process.

StreamWriter wraps a bounded asyncio.Queue and provides both synchronous and
asynchronous write interfaces. This enables streaming input to be sent in
both sync and async contexts.

The stream uses None as a sentinel value to signal end-of-stream (EOF).
The queue is bounded (\~16 items for \~1MB with 64KB chunks) to provide
backpressure.

**Attributes**

* `QUEUE_SIZE` : Default: `16`.

## Properties

### closed

```python theme={"system"}
@property
def closed(self) -> bool
```

True if close() has been called.

## Methods

### write

```python theme={"system"}
write(data: bytes) -> OperationRef[None]
```

Write raw bytes to the stream.

Queues the data to be sent to the process stdin. Blocks (via OperationRef.result())
if the queue is full, providing backpressure.
**Parameters**

* `data` (`bytes`): The bytes to write.

**Returns**

* `OperationRef[None]`: An OperationRef that completes when the data is queued.

**Raises**

* `SandboxExecutionError`: If the stream is closed or has failed.

### writeline

```python theme={"system"}
writeline(text: str, encoding: str = 'utf-8') -> OperationRef[None]
```

Write a line of text to the stream.

Encodes the text, appends a newline, and queues it for sending.
**Parameters**

* `text` (`str`): The text to write.
* `encoding` (`str`): The text encoding to use. Defaults to "utf-8".

**Returns**

* `OperationRef[None]`: An OperationRef that completes when the data is queued.

**Raises**

* `SandboxExecutionError`: If the stream is closed or has failed.

### close

```python theme={"system"}
close() -> OperationRef[None]
```

Close the stream, sending EOF sentinel.

The EOF sentinel is queued at the end, so pending writes complete first.
Multiple calls to close() are idempotent and return immediately.
**Returns**

* `OperationRef[None]`: An OperationRef that completes when EOF is queued.

### set\_exception

```python theme={"system"}
set_exception(exception: BaseException) -> None
```

Store an exception to be raised on subsequent writes.

Called internally when the stream fails (e.g., process exits).
**Parameters**

* `exception` (`BaseException`): The exception to store.
