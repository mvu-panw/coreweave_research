# Command execution

Source: https://docs.coreweave.com/products/sandboxes/client/guides/execution

# Command execution

> Run commands in sandboxes with streaming, process control, and error handling.

This guide shows you how to run commands in sandboxes using the `exec()` method. Use it when you need to run shell commands, scripts, or interactive interpreters inside a sandbox and want to capture their output, stream it in real time, send input on stdin, or control how non-zero exit codes are handled. The guide is for developers who already work with the `cwsandbox` Python client.

## Choose authentication

These examples run on serverless capacity unless a section specifies CKS. Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as `sandbox_auth.py` beside the Python scripts you run from this page. It stores the authentication choice, not your credential. The examples import `AUTH` from that file and pass it explicitly to each new sandbox or session.

> [tab] Forge API key
>
> Use your Forge API key through the SDK's W\&B authentication strategy:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. Creating a session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Run a basic command

Start with a single command that runs to completion and returns its captured output. The `exec()` method returns a `Process` handle:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    # Run a command and get the result
    result = sandbox.exec(["echo", "Hello, World!"]).result()

    print(result.stdout)      # "Hello, World!\n"
    print(result.returncode)  # 0
```

## Get results

`exec()` returns immediately so you can decide how to wait for the command. Call `.result()` on the `Process` handle to block for the output:

```python theme={"system"}
# Returns Process immediately
process = sandbox.exec(["python", "-c", "print('hello')"])

# Block for result
result = process.result()
print(result.stdout)      # "hello\n"
print(result.stderr)      # ""
print(result.returncode)  # 0

# One-liner pattern
result = sandbox.exec(["ls", "-la"]).result()
```

## Stream output

Blocking on `.result()` waits for the command to finish before you see any output. To observe progress as it happens, iterate over `process.stdout` before calling `.result()`:

```python theme={"system"}
# Returns Process immediately
process = sandbox.exec(["python", "long_script.py"])

# Stream stdout line by line
for line in process.stdout:
    print(f"[stdout] {line}", end="")

# Get final result
result = process.result()
print(f"Exit code: {result.returncode}")
```

Use streaming when you need to:

* Monitor long-running processes.
* Process output as it arrives.
* Implement progress indicators.

## Stream input to stdin

Some commands need input written to stdin while they run, such as pipelines, interactive interpreters, or tools that read until EOF. Send input to running commands by enabling stdin with `stdin=True`:

```python theme={"system"}
from sandbox_auth import AUTH
with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    process = sandbox.exec(["cat"], stdin=True)

    process.stdin.write(b"hello world\n").result()
    process.stdin.close().result()

    result = process.result()
    print(result.stdout)  # "hello world\n"
```

### StreamWriter methods

When `stdin=True`, `process.stdin` is a `StreamWriter` with three methods:

* **`write(data: bytes)`**: Write raw bytes. Returns `OperationRef[None]`.
* **`writeline(text: str)`**: Write text with a trailing newline (encodes to UTF-8). Returns `OperationRef[None]`.
* **`close()`**: Signal EOF. The system completes pending writes first. Returns `OperationRef[None]`.

When `stdin=False` (the default), `process.stdin` is `None`.

### Send multiple writes

Send data incrementally before closing:

```python theme={"system"}
process = sandbox.exec(["cat"], stdin=True)

process.stdin.writeline("line 1").result()
process.stdin.writeline("line 2").result()
process.stdin.writeline("line 3").result()
process.stdin.close().result()

result = process.result()
print(result.stdout)  # "line 1\nline 2\nline 3\n"
```

### Run interactive Python through stdin

Feed Python code to an interactive interpreter:

```python theme={"system"}
process = sandbox.exec(["python3"], stdin=True)

process.stdin.writeline("x = 40 + 2").result()
process.stdin.writeline("print(f'answer: {x}')").result()
process.stdin.close().result()

result = process.result()
print(result.stdout)  # "answer: 42\n"
```

### Combine stdin and stdout streaming

Stream output while sending input:

```python theme={"system"}
process = sandbox.exec(["cat"], stdin=True)

# Send input
process.stdin.writeline("hello").result()
process.stdin.writeline("world").result()
process.stdin.close().result()

# Stream output as it arrives
for line in process.stdout:
    print(f"[out] {line}", end="")

result = process.result()
```

### Handle EOF-dependent commands

Some commands (like `sort`) read all input before producing output. Close stdin to signal EOF:

```python theme={"system"}
process = sandbox.exec(["sort"], stdin=True)

process.stdin.writeline("banana").result()
process.stdin.writeline("apple").result()
process.stdin.writeline("cherry").result()
process.stdin.close().result()  # sort requires EOF before producing output

result = process.result()
print(result.stdout)  # "apple\nbanana\ncherry\n"
```

### Use stdin in async contexts

In async contexts, use `Sandbox(...)` so the async context manager starts the sandbox without blocking the event loop. Use `await` for each `OperationRef`:

```python theme={"system"}
from sandbox_auth import AUTH
async with Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    process = sandbox.exec(["cat"], stdin=True)

    await process.stdin.write(b"async hello\n")
    await process.stdin.close()

    result = await process
    print(result.stdout)  # "async hello\n"
```

### When to use stdin=True compared with stdin=False

| Scenario | stdin | Reason |
| - | - | - |
| Run a command with arguments | `False` | Input comes from args, not stdin |
| Pipe data into a command | `True` | The command reads from stdin |
| Interactive interpreter | `True` | The interpreter reads commands from stdin |
| Process that reads until EOF | `True` | Requires `close()` to signal EOF |
| Fire-and-forget command | `False` | No input needed |

## Set the working directory

By default, commands run from the sandbox's default working directory. Override that with `cwd`:

```python theme={"system"}
result = sandbox.exec(
    ["ls", "-la"],
    cwd="/app/data",
).result()
```

The path must be absolute.

## Set a timeout

For a longer attached command, pass an explicit `timeout_seconds` value to `exec()`, such as `1800` for a 30-minute bootstrap. Consume the process output with the methods in [Stream output](#stream-output). The default exec request timeout is 300 seconds. The sandbox's lifetime must also cover the command. A longer exec timeout doesn't make the command durable across a client disconnect.

To stop a command that might freeze or run longer than you expect, set a timeout with `timeout_seconds`:

```python theme={"system"}
from cwsandbox import SandboxTimeoutError

try:
    result = sandbox.exec(
        ["sleep", "60"],
        timeout_seconds=5.0,
    ).result()
except SandboxTimeoutError:
    print("Command timed out")
```

## Handle errors with check

The `check` parameter controls error behavior for non-zero exit codes:

### Default behavior with check=False

Returns the result regardless of exit code:

```python theme={"system"}
result = sandbox.exec(["false"]).result()
print(result.returncode)  # 1 (no exception)
```

### Raise on failure with check=True

Raises `SandboxExecutionError` on non-zero exit:

```python theme={"system"}
from cwsandbox import SandboxExecutionError

try:
    result = sandbox.exec(
        ["python", "-c", "raise ValueError('oops')"],
        check=True,
    ).result()
except SandboxExecutionError as e:
    print(f"Command failed: {e.exec_result.returncode}")
    print(f"stderr: {e.exec_result.stderr}")
```

## Run Python code

Sandboxes are commonly used to run Python code, either as short one-liners or as longer scripts passed inline:

```python theme={"system"}
# One-liner
result = sandbox.exec(
    ["python", "-c", "import sys; print(sys.version)"],
).result()

# Script from string
code = '''
import json
data = {"result": 42}
print(json.dumps(data))
'''
result = sandbox.exec(["python", "-c", code]).result()
output = json.loads(result.stdout)
```

## Sequential compared with parallel execution

Choose sequential execution when later commands depend on earlier ones, and parallel execution when commands are independent and you want them to run concurrently across sandboxes.

### Run commands sequentially when order matters

```python theme={"system"}
# Dependencies require sequential execution
sandbox.exec(["pip", "install", "requests"]).result()
sandbox.exec(["python", "script_using_requests.py"]).result()
```

### Run independent commands in parallel

Use a session to own every sandbox, and wait for each creation request to finish before starting
parallel commands. Exiting the session attempts to stop all its sandboxes, including when creation
of a later sandbox fails or a command raises an exception.

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults

with cwsandbox.Session(SandboxDefaults(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH) as session:
    # Register all sandboxes before starting work
    sandboxes = [session.sandbox() for _ in range(3)]

    # Wait for each creation request before submitting any commands
    for sb in sandboxes:
        sb.start().result()

    # Run independent commands in parallel
    processes = [
        sb.exec(["python", "-c", f"print({i})"], check=True)
        for i, sb in enumerate(sandboxes)
    ]

    # Collect all results before the session closes
    results = [p.result() for p in processes]
    for result in results:
        print(result.stdout)
```

`start().result()` waits for creation to be accepted, not for the sandbox to reach `RUNNING`.
Each `exec()` operation waits for its sandbox to be ready. Waiting for starts one at a time keeps
a pending creation response from arriving after another operation has already triggered cleanup.

Session cleanup attempts every stop even if another stop fails. If cleanup fails, exiting the
`with` block or calling `Session.close().result()` raises `SandboxError`. Some sandboxes can
remain running. A failed creation request can also leave a sandbox behind if the server created it
but the client didn't receive its ID. See
[Cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md) for recovery options.

### Wait for N of M processes to complete

Use `cwsandbox.wait()` to wait for a subset of processes. In the preceding example, replace the
result-collection code with this excerpt inside the session's `with` block:

```python theme={"system"}
# Wait for first 2 to complete
done, pending = cwsandbox.wait(processes, num_returns=2)

# Process completed ones immediately
for p in done:
    print(p.result().stdout)

# Wait for remaining
for p in pending:
    print(p.result().stdout)
```

## Control processes

When a command keeps running after the `exec()` call returns, you can check on it without blocking or wait for it to finish on your own terms. The `Process` handle provides methods for monitoring and control:

```python theme={"system"}
process = sandbox.exec(["python", "server.py"])

# Check if running (non-blocking)
if process.poll() is None:
    print("Still running")

# Wait for completion
exit_code = process.wait()
print(f"Exited with code: {exit_code}")
```
