# Sessions

Source: https://docs.coreweave.com/products/sandboxes/client/guides/sessions

# Sessions

> Group and manage multiple sandboxes with sessions.

This guide covers using `Session` to manage multiple sandboxes with shared configuration. It's for client developers who need to coordinate groups of sandboxes, apply common defaults, and ensure consistent cleanup across a workload.

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

## Session overview

A `Session` provides:

* Shared default configuration for all sandboxes.
* Automatic cleanup when the session closes.
* A scope for the `@session.function()` decorator.

## Basic usage

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults

# Define shared configuration
defaults = SandboxDefaults(
    container_image="python:3.11",
    tags=("project-alpha",),
    resources={"cpu": "1", "memory": "1Gi"},
)

# Create a session with context manager
with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    # Create sandboxes through the session
    sb1 = session.sandbox()
    sb2 = session.sandbox()

    # Use the sandboxes
    result1 = sb1.exec(["echo", "sandbox 1"]).result()
    result2 = sb2.exec(["echo", "sandbox 2"]).result()

# All sandboxes automatically stopped when exiting context
```

## Create sandboxes

The following sections describe how to create sandboxes through a session and override session defaults.

### session.sandbox()

Creates a sandbox with session defaults. The sandbox doesn't start until first use:

```python theme={"system"}
from sandbox_auth import AUTH
with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    # sandbox() returns an unstarted sandbox
    sandbox = session.sandbox()

    # Operations auto-start the sandbox on first use
    result = sandbox.exec(["echo", "hello"]).result()
```

For explicit control over when the start RPC fires:

```python theme={"system"}
from sandbox_auth import AUTH
with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    sandbox = session.sandbox()
    sandbox.start().result()  # Explicit start
    sandbox.wait()            # Wait for startup or completion
    if sandbox.status != cwsandbox.SandboxStatus.RUNNING:
        raise RuntimeError(f"Sandbox is not running: {sandbox.status}")
    result = sandbox.exec(["echo", "hello"]).result()
```

### Override defaults

Pass additional arguments to override session defaults.

The following serverless example configures a deferred GPU sandbox with CPU and memory requests equal to their respective limits. To start it, call `gpu_sandbox.start().result()` or execute a command before leaving the session.

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import ResourceOptions, SandboxDefaults

# Session with base configuration
defaults = SandboxDefaults(
    container_image="python:3.11",
    tags=("my-project",),
    resources={"cpu": "1", "memory": "1Gi"},
)

with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    # Override image and resources for this sandbox
    gpu_sandbox = session.sandbox(
        command="sleep",
        args=["infinity"],
        container_image="pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime",
        resources=ResourceOptions(
            requests={"cpu": "4", "memory": "16Gi"},
            limits={"cpu": "4", "memory": "16Gi"},
            gpu={"count": 1},
        ),
        tags=["gpu-workload"],  # Merged with session tags
    )
```

See the [Sandbox configuration guide](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md) for all available options.

## Multiple sandbox management

Sessions work well for managing sandbox pools:

```python theme={"system"}
from sandbox_auth import AUTH
with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    # Create a pool of sandboxes
    sandboxes = [
        session.sandbox()
        for _ in range(5)
    ]

    # Distribute work across the pool
    processes = [
        sb.exec(["python", "-c", f"print({i})"])
        for i, sb in enumerate(sandboxes)
    ]

    # Collect results
    results = [p.result() for p in processes]

# All 5 sandboxes automatically cleaned up
```

To prepare sandboxes before requests arrive, see
[Implement a warm pool](https://docs.coreweave.com/products/sandboxes/warm-pools.md).
The recipe maintains a buffer of ready sandboxes, gives each workload a separate
sandbox, and replenishes the buffer as workloads claim them.

## Session lifecycle

The following sections describe how to close a session, what `close()` does, and how to handle errors.

### Manual close

When you don't use a context manager, close a session explicitly:

```python theme={"system"}
from sandbox_auth import AUTH
session = cwsandbox.Session(defaults=defaults, auth=AUTH)

sandbox = session.sandbox()
result = sandbox.exec(["echo", "hello"]).result()

# Close the session (stops all sandboxes)
session.close().result()
```

### What close() does

Calling `close()` starts stopping all sandboxes created through or adopted by the session and immediately returns an `OperationRef[None]`. Call `session.close().result()` to wait for cleanup to complete.

### Error handling

Sessions clean up even if exceptions occur:

```python theme={"system"}
from sandbox_auth import AUTH
with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    sandbox = session.sandbox()
    raise RuntimeError("Something went wrong!")
# Sandbox is still cleaned up
```

## Adopt external sandboxes

Bring sandboxes created outside the session under session management:

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import Sandbox

with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    # Find existing sandboxes
    existing = Sandbox.list(tags=["orphaned-work"], auth=AUTH).result()

    # Adopt them for cleanup
    for sandbox in existing:
        session.adopt(sandbox)

    # Now session.close() will clean them up too
```

## Session properties

Inspect session state with built-in properties such as `sandbox_count`:

```python theme={"system"}
from sandbox_auth import AUTH
session = cwsandbox.Session(defaults=defaults, auth=AUTH)

# Number of sandboxes tracked
print(session.sandbox_count)  # 0

sandbox = session.sandbox()
print(session.sandbox_count)  # 1
```

## When to use sessions

| Use case | Recommended approach |
| - | - |
| Single sandbox, simple task | `Sandbox.run()` with context manager |
| Multiple sandboxes, shared config | Session |
| Function decorator API | Session required |
| Pool of workers | Session |
| One-off command | Direct `Sandbox.run()` |

## Without sessions

You don't need sessions for single sandboxes:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

# Direct usage without session
with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    result = sandbox.exec(["echo", "hello"]).result()
# Cleanup handled by context manager
```
