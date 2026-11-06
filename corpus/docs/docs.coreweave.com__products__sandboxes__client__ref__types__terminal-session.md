# TerminalSession

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/terminal-session

# TerminalSession

> Handle for an interactive TTY session in a sandbox.

Source: [src/cwsandbox/\_types.py:2026](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L2026)

```python theme={"system"}
class TerminalSession(future: concurrent.futures.Future[TerminalResult], command: list[str], output: StreamReader[bytes], stdin: StreamWriter, resize_queue: asyncio.Queue[tuple[int, int] | None])
```

Handle for an interactive TTY session in a sandbox.

TerminalSession is purpose-built for interactive use cases where a local
terminal is connected to a remote shell. Unlike Process:

* Output is raw bytes (StreamReader\[bytes]), preserving ANSI sequences
* No output buffering -- safe for long-running sessions
* result() returns TerminalResult (exit code only, no captured output)

## Properties

### command

```python theme={"system"}
@property
def command(self) -> list[str]
```

The command that was executed.

### returncode

```python theme={"system"}
@property
def returncode(self) -> int | None
```

The exit code, or None if the session is still active.

## Methods

### resize

```python theme={"system"}
resize(width: int, height: int) -> None
```

Send terminal resize. Fire-and-forget.
**Parameters**

* `width` (`int`): New terminal width in columns.
* `height` (`int`): New terminal height in rows.

**Raises**

* `SandboxExecutionError`: If the session has ended.

### result

```python theme={"system"}
result(timeout: float | None = None) -> TerminalResult
```

Block until the terminal session ends and return the result.
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means wait forever.

**Returns**

* `TerminalResult`: TerminalResult with the exit code.

**Raises**

* `concurrent.futures.TimeoutError`: If timeout expires.
* `Exception`: Any exception from the session.

### wait

```python theme={"system"}
wait(timeout: float | None = None) -> int
```

Block until the session ends and return exit code.
**Parameters**

* `timeout` (`float | None`): Maximum seconds to wait. None means wait forever.

**Returns**

* `int`: The process exit code.

**Raises**

* `concurrent.futures.TimeoutError`: If timeout expires.
* `Exception`: Any exception from the session.
