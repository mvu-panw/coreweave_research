# Run commands in a sandbox environment

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/running-commands

# Run commands in a sandbox environment

> Execute commands inside a sandbox and capture output.

In this part of the tutorial, you execute commands inside a sandbox and capture their output. The following examples show common patterns, including error checking, timeouts, and working directories.

```python theme={"system"}
# Basic command
sandbox.exec(["echo", "Hello"]).result()

# Raise SandboxExecutionError if command returns non-zero exit code
sandbox.exec(["ls", "/nonexistent"], check=True).result()

# Raise SandboxTimeoutError if command exceeds timeout
sandbox.exec(["sleep", "60"], timeout_seconds=5).result()

# Run in a specific directory
sandbox.exec(["ls"], cwd="/app").result()
```

## Parallel execution

Run multiple commands in parallel when you don't need to wait for each one to finish before starting the next. This reduces total runtime when commands are independent.

```python theme={"system"}
import cwsandbox

# exec() returns a Process immediately without waiting for the command to finish
p1 = sandbox.exec(["sleep", "1"])
p2 = sandbox.exec(["sleep", "1"])
p3 = sandbox.exec(["sleep", "1"])

# Call .result() when you need the output - ~1 second total, not 3
cwsandbox.result([p1, p2, p3])
```

For streaming, error handling, and process control, see the [Execution guide](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md).
