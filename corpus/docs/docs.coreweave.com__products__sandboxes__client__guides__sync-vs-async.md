# Sync versus async patterns

Source: https://docs.coreweave.com/products/sandboxes/client/guides/sync-vs-async

# Sync versus async patterns

> Choose between synchronous and asynchronous patterns in the CoreWeave sandbox Python SDK.

This guide helps you choose between synchronous and asynchronous patterns in the CoreWeave sandbox Python SDK (`cwsandbox`) and shows the sync and async form of each common operation.

The SDK has a single async implementation internally. The sync/async flexibility comes from how you consume results: use `.result()` for sync and `await` for async.

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

## Quick decision guide

| Use case | Pattern | Reason |
| - | - | - |
| Most operations | Sync | Simpler code, no asyncio boilerplate |
| Parallel execution | Sync | Operations are non-blocking by design |
| Jupyter notebooks | Sync | No `nest_asyncio` needed |
| Async codebase | Async | Integrates with existing async code |

**Rule of thumb**: Use sync patterns (`.result()`) for simplicity. Switch to `await` only when you're already
in an async codebase.

## Core concept: OperationRef

Most SDK methods return `OperationRef[T]`, a wrapper that is both `.result()`-able and awaitable.
Both paths raise the same exceptions.

```python theme={"system"}
ref = sandbox.read_file("/output/data.txt")

# Sync: block for the value
data = ref.result()

# Async: await instead
data = await ref
```

`Sandbox.exec()` returns `Process`, which extends `OperationRef[ProcessResult]` with streaming
and stdin.

> [!WARNING]
>
> Never use `.result()` in async contexts. Calling `.result()` blocks the thread. In an async context this blocks the event loop and
> can deadlock your application. Use `await` instead.

## Auto-start behavior

`session.sandbox()` returns an unstarted sandbox. The sandbox auto-starts on the first operation
that requires it:

**Triggers auto-start**: `exec()`, `read_file()`, `write_file()`, `wait()`, `wait_until_complete()`

**Does not auto-start**: `get_status()` (raises `SandboxNotRunningError`), `stop()` (no-op if never started)

## Operations

### Create sandboxes

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> # Context manager (recommended)
> with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sb:
>     result = sb.exec(["echo", "hello"]).result()
> # Automatically stopped on exit
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> # Construct, then use an async context manager for startup and cleanup
> sb = Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
> async with sb as sb:
>     result = await sb.exec(["echo", "hello"])
> # Automatically stopped on exit
> ```

`Sandbox.run()` calls `start().result()` internally, which blocks the event loop.
In async code, construct with `Sandbox(...)` and use `async with` to start the sandbox.
`exec()` waits for `RUNNING` before executing. To wait for startup separately, use
`await sandbox` and [check its status](#wait) before operations.

### start()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
> sb.start().result()  # Block until backend accepts
> print(sb.sandbox_id)
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
> await sb.start()  # Await until backend accepts
> print(sb.sandbox_id)
> ```

### exec()

> [tab] Sync
>
> ```python theme={"system"}
> result = sb.exec(["echo", "hello"]).result()
> print(result.stdout)  # "hello\n"
>
> # Raise on non-zero exit code
> result = sb.exec(["python", "-c", "exit(1)"], check=True).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> result = await sb.exec(["echo", "hello"])
> print(result.stdout)  # "hello\n"
>
> # Raise on non-zero exit code
> result = await sb.exec(["python", "-c", "exit(1)"], check=True)
> ```

### read\_file()

> [tab] Sync
>
> ```python theme={"system"}
> data = sb.read_file("/output/result.txt").result()
> print(data.decode())
> ```

> [tab] Async
>
> ```python theme={"system"}
> data = await sb.read_file("/output/result.txt")
> print(data.decode())
> ```

### write\_file()

> [tab] Sync
>
> ```python theme={"system"}
> sb.write_file("/input/data.txt", b"content").result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> await sb.write_file("/input/data.txt", b"content")
> ```

### stop()

> [tab] Sync
>
> ```python theme={"system"}
> sb.stop().result()
>
> # Ignore if already deleted
> sb.stop(missing_ok=True).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> await sb.stop()
>
> # Ignore if already deleted
> await sb.stop(missing_ok=True)
> ```

### wait()

`wait()` waits for startup status. For example, it can return when the sandbox is
`RUNNING` or `TERMINATING`, or after it completes successfully. It's sync-only. In async code,
`await sandbox` uses the same startup wait without blocking the event loop.

A normal return doesn't guarantee `RUNNING`. Check `status` before operations that require a
running sandbox. For terminal-state and error handling, see
[Wait for a sandbox](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#wait-for-a-sandbox).

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxStatus

# Sync: wait for startup status, then check status
sb = Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH).wait()
if sb.status == SandboxStatus.RUNNING:
    result = sb.exec(["echo", "ready"]).result()
```

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxStatus

# Async: await the same startup wait, then check status
sb = Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
await sb
if sb.status == SandboxStatus.RUNNING:
    result = await sb.exec(["echo", "ready"])
```

### wait\_until\_complete()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = Sandbox.run(
>     "python",
>     "-c",
>     "print('done')",
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> )
> sb.wait_until_complete().result()
> print(f"Exit code: {sb.returncode}")
>
> # Handle externally-terminated sandboxes without raising
> sb.wait_until_complete(raise_on_termination=False).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = Sandbox(
>     command="python",
>     args=["-c", "print('done')"],
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> )
> await sb.wait_until_complete()
> print(f"Exit code: {sb.returncode}")
>
> # Handle externally-terminated sandboxes without raising
> await sb.wait_until_complete(raise_on_termination=False)
> ```

### get\_status()

`get_status()` is sync-only. It fetches the current status from the API.

```python theme={"system"}
status = sb.get_status()
print(f"Sandbox is {status}")  # e.g. SandboxStatus.RUNNING
```

### Sandbox.list()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sandboxes = Sandbox.list(tags=["my-job"], auth=AUTH).result()
> for sb in sandboxes:
>     print(f"{sb.sandbox_id}: {sb.status}")
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sandboxes = await Sandbox.list(tags=["my-job"], auth=AUTH)
> for sb in sandboxes:
>     print(f"{sb.sandbox_id}: {sb.status}")
> ```

### Sandbox.from\_id()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = Sandbox.from_id("sandbox-abc123", auth=AUTH).result()
> result = sb.exec(["echo", "reconnected"]).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> sb = await Sandbox.from_id("sandbox-abc123", auth=AUTH)
> result = await sb.exec(["echo", "reconnected"])
> ```

### Sandbox.delete()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> Sandbox.delete("sandbox-abc123", auth=AUTH).result()
>
> # Ignore if already deleted
> Sandbox.delete("sandbox-abc123", missing_ok=True, auth=AUTH).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> await Sandbox.delete("sandbox-abc123", auth=AUTH)
>
> # Ignore if already deleted
> await Sandbox.delete("sandbox-abc123", missing_ok=True, auth=AUTH)
> ```

### session.list()

> [tab] Sync
>
> ```python theme={"system"}
> sandboxes = session.list().result()
> for sb in sandboxes:
>     print(f"{sb.sandbox_id}: {sb.status}")
> ```

> [tab] Async
>
> ```python theme={"system"}
> sandboxes = await session.list()
> for sb in sandboxes:
>     print(f"{sb.sandbox_id}: {sb.status}")
> ```

### session.from\_id()

> [tab] Sync
>
> ```python theme={"system"}
> sb = session.from_id("sandbox-abc123").result()
> result = sb.exec(["echo", "adopted"]).result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> sb = await session.from_id("sandbox-abc123")
> result = await sb.exec(["echo", "adopted"])
> ```

### Stream stdout

> [tab] Sync
>
> ```python theme={"system"}
> process = sb.exec(["python", "-c", "import time; [print(i) or time.sleep(0.1) for i in range(5)]"])
> for line in process.stdout:
>     print(line, end="")
> result = process.result()
> ```

> [tab] Async
>
> ```python theme={"system"}
> process = sb.exec(["python", "-c", "import time; [print(i) or time.sleep(0.1) for i in range(5)]"])
> async for line in process.stdout:
>     print(line, end="")
> result = await process
> ```

### Stream stdin

Enable stdin with `stdin=True`. Use `write()` for raw bytes, `writeline()` for text lines,
and `close()` to signal EOF.

> [tab] Sync
>
> ```python theme={"system"}
> process = sb.exec(["cat"], stdin=True)
> process.stdin.write(b"hello ").result()
> process.stdin.writeline("world").result()
> process.stdin.close().result()  # Signals EOF to the process
> result = process.result()
> print(result.stdout)  # "hello world\n"
> ```

> [tab] Async
>
> ```python theme={"system"}
> process = sb.exec(["cat"], stdin=True)
> await process.stdin.write(b"hello ")
> await process.stdin.writeline("world")
> await process.stdin.close()  # Signals EOF to the process
> result = await process
> print(result.stdout)  # "hello world\n"
> ```

### cwsandbox.results()

`cwsandbox.results()` is a sync-only batch helper. It calls `.result()` on one or more `OperationRef` objects.

```python theme={"system"}
import cwsandbox

# Single ref
data = cwsandbox.results(sandbox.read_file("/path"))

# Multiple refs
all_data = cwsandbox.results([sb.read_file(f) for f in files])
```

### cwsandbox.wait()

`cwsandbox.wait()` is sync-only. It waits for a sequence of `Sandbox`, `OperationRef`, or `Process`
objects and returns `(done, pending)`. For sandboxes, it uses the same startup wait as
`Sandbox.wait()`, rather than waiting for the main command to finish. A sandbox in `done`
isn't guaranteed to be `RUNNING`. For example, it may already be completed or terminating. Check
each sandbox's `status` before operations that require it to be running.

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox

# Wait for all sandbox startup waits to finish
sandboxes = [
    Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
    for _ in range(5)
]
done, pending = cwsandbox.wait(sandboxes)

# Wait for first 2 operations to complete
refs = [sb.read_file(f) for f in files]
done, pending = cwsandbox.wait(refs, num_returns=2)

# Wait with timeout
done, pending = cwsandbox.wait(procs, timeout=30.0)
```

### @session.function()

> [tab] Sync
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> with Session(defaults, auth=AUTH) as session:
>     @session.function()
>     def compute(x: int, y: int) -> int:
>         return x + y
>
>     result = compute.remote(2, 3).result()
>     print(result)  # 5
>
>     # Parallel map
>     refs = compute.map([(1, 2), (3, 4), (5, 6)])
>     results = [r.result() for r in refs]  # [3, 7, 11]
> ```

> [tab] Async
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> async with Session(defaults, auth=AUTH) as session:
>     @session.function()
>     def compute(x: int, y: int) -> int:
>         return x + y
>
>     result = await compute.remote(2, 3)
>     print(result)  # 5
>
>     # Parallel map
>     refs = compute.map([(1, 2), (3, 4), (5, 6)])
>     results = [await r for r in refs]  # [3, 7, 11]
> ```

## Parallel execution

The sync API supports parallel execution because operations are **non-blocking by design**. Methods
like `exec()`, `read_file()`, and `write_file()` return immediately. You only block when you call
`.result()`.

`Sandbox.run()` blocks until the backend accepts the start request (it calls `start().result()`
internally). For parallel startup, use `session.sandbox()` (auto-starts on first operation) or
collect `start()` refs:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, Session, SandboxDefaults

# Option 1: session.sandbox() - sandboxes auto-start on first exec()
with Session(
    SandboxDefaults(resources={"cpu": "1", "memory": "1Gi"}),
    auth=AUTH,
) as session:
    sandboxes = [session.sandbox() for _ in range(3)]
    processes = [sb.exec(["echo", f"sb-{i}"]) for i, sb in enumerate(sandboxes)]
    results = [p.result() for p in processes]

# Option 2: Sandbox() + collect start() refs
sandboxes = [
    Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
    for _ in range(3)
]
start_refs = [sb.start() for sb in sandboxes]
for ref in start_refs:
    ref.result()  # All starts proceed in parallel

processes = [sb.exec(["echo", f"sb-{i}"]) for i, sb in enumerate(sandboxes)]
results = [p.result() for p in processes]
for sb in sandboxes:
    sb.stop().result()
```

## Jupyter notebooks

The sync API works in Jupyter without `nest_asyncio` because the SDK runs its own background event
loop in a daemon thread:

```python theme={"system"}
from sandbox_auth import AUTH
# Cell 1 - Create sandbox
from cwsandbox import Sandbox, SandboxStatus
sandbox = Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
sandbox.wait()  # Wait for startup status

# Cell 2 - Check status before executing commands
if sandbox.status == SandboxStatus.RUNNING:
    result = sandbox.exec(["python", "-c", "print(1+1)"]).result()
    print(result.stdout)

# Cell 3 - Cleanup
sandbox.stop().result()
```

For async in Jupyter, `await` works directly since Jupyter has a built-in event loop:

```python theme={"system"}
from sandbox_auth import AUTH
# Works in Jupyter without asyncio.run()
sandboxes = await Sandbox.list(tags=["notebook"], auth=AUTH)
```

## Error handling

Both sync and async paths raise the same exceptions. `.result()` re-raises any exception
from the underlying operation, and `await` does the same. See [What do common sandbox SDK error messages mean?](https://docs.coreweave.com/support/sandboxes/articles/what-do-common-sandbox-sdk-errors-mean)
for the full exception hierarchy and recovery patterns.
