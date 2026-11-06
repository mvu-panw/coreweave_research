# Process

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/process

# Process

> Handle for a running process with streaming stdout/stderr.

Source: [src/cwsandbox/\_types.py:1776](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1776)

```python theme={"system"}
class Process(future: concurrent.futures.Future[ProcessResult], command: list[str], stdout: StreamReader[str], stderr: StreamReader[str], stdin: StreamWriter | None = None, stats_callback: Callable[[ProcessResult | None, BaseException | None], None] | None = None)
```

Handle for a running process with streaming stdout/stderr.

Process inherits from OperationRef\[ProcessResult] and adds streaming
capabilities and process-specific methods. It wraps an async operation
that executes a command in a sandbox.

The process's output streams (stdout, stderr) can be iterated either
synchronously or asynchronously. The result() method blocks until
completion and returns the full ProcessResult.

## Properties

### returncode

```python theme={"system"}
@property
def returncode(self) -> int | None
```

The process exit code, or None if not yet complete.

### command

```python theme={"system"}
@property
def command(self) -> list[str]
```

The command that was executed.

## Methods

### poll

```python theme={"system"}
poll() -> int | None
```

Check if the process has completed without blocking.
**Returns**

* `int | None`: The exit code if the process has completed, None otherwise.

### wait

```python theme={"system"}
wait(timeout: float | None = None) -> int
```

Block until the process completes.
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means wait forever.

**Returns**

* `int`: The process exit code.

**Raises**

* `concurrent.futures.TimeoutError`: If timeout expires.
* `concurrent.futures.CancelledError`: If the operation was cancelled.
* `Exception`: Any exception from the execution.

### result

```python theme={"system"}
result(timeout: float | None = None) -> ProcessResult
```

Block until complete and return the full ProcessResult.
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means wait forever.

**Returns**

* `ProcessResult`: The ProcessResult containing stdout, stderr, and exit code.

**Raises**

* `concurrent.futures.TimeoutError`: If timeout expires.
* `concurrent.futures.CancelledError`: If the operation was cancelled.
* `Exception`: Any exception from the execution.

### cancel

```python theme={"system"}
cancel() -> bool
```

Attempt to cancel the process.
**Returns**

* `bool`: True if successfully cancelled, False otherwise.
