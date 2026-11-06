# ProcessResult

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/process-result

# ProcessResult

> Result from a completed streaming exec operation.

Source: [src/cwsandbox/\_types.py:1487](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1487)

```python theme={"system"}
class ProcessResult(stdout: str, stderr: str, returncode: int, stdout_bytes: bytes = b'', stderr_bytes: bytes = b'', command: list[str] = list())
```

Result from a completed streaming exec operation.

Contains both the raw bytes and decoded strings for stdout/stderr,
along with the exit code and original command.

**Attributes**

* `stdout_bytes` (`bytes`) : Raw stdout bytes Default: `field(default=b'')`.
* `stderr_bytes` (`bytes`) : Raw stderr bytes Default: `field(default=b'')`.
* `command` (`list[str]`) : The command that was executed Default: `field(default_factory=list)`.
