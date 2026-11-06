# TerminalResult

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/terminal-result

# TerminalResult

> Result from a completed terminal session.

Source: [src/cwsandbox/\_types.py:2010](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L2010)

```python theme={"system"}
class TerminalResult(returncode: int, command: list[str] = list())
```

Result from a completed terminal session.

Unlike ProcessResult, does not contain captured stdout/stderr because
TTY sessions do not buffer output.

**Attributes**

* `command` (`list[str]`) : The command that was executed. Default: `field(default_factory=list)`.
