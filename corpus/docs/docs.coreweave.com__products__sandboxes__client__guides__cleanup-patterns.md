# Cleanup patterns

Source: https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns

# Cleanup patterns

> Patterns for reliable sandbox cleanup and resource management.

This guide covers resource management and cleanup strategies for sandboxes. Reliable cleanup prevents orphaned sandboxes after a script exits, which keeps costs predictable and avoids unintentional compute resource usage. The patterns here apply to scripts that create one or many sandboxes, with or without an explicit session.

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

## Automatic cleanup

Automatic cleanup ties a sandbox's lifetime to a Python context manager or a session that the SDK closes when the process exits. The SDK releases resources without explicit `stop()` calls.

A sandbox you start with `Sandbox.run()` outside a session or context manager can keep running after your script exits. It stops when its main command exits successfully (exit status 0), you stop it, or its maximum lifetime expires. A nonzero exit can trigger automatic container restarts. The sandbox fails if it reaches the restart limit. See [Main command lifetime](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#main-command-lifetime).

### Context managers (recommended)

Context managers are the recommended pattern because they guarantee cleanup even if the enclosed code raises an exception. The SDK stops sandboxes when the context exits:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    result = sandbox.exec(["echo", "hello"]).result()
# sandbox.stop() called automatically
```

Sessions clean up all their sandboxes:

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults

with cwsandbox.Session(SandboxDefaults(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH) as session:
    sb1 = session.sandbox()
    sb2 = session.sandbox()
# Both sandboxes stopped automatically
```

### Global cleanup handlers

The SDK registers cleanup handlers that stop sandboxes owned by registered sessions when the process terminates. Standalone sandboxes created outside a session or context manager require explicit cleanup:

| Scenario | Behavior |
| - | - |
| Normal script exit | `atexit` handler stops sandboxes in registered sessions |
| Ctrl+C (`SIGINT`) | Signal handler stops sandboxes in registered sessions |
| `SIGTERM` | Signal handler stops sandboxes in registered sessions |
| Second Ctrl+C | Force exit (prevents unresponsive shutdown) |

In `cwsandbox>=1.15.0`, cleanup handlers activate when the process first owns a sandbox.
This includes standalone creation and session creation or adoption of a sandbox. Looking up an
existing sandbox with `Sandbox.from_id()` alone doesn't activate these handlers. The `SIGINT` and
`SIGTERM` handlers install only from Python's main thread. Activation on another thread registers
`atexit` and leaves signal installation pending for later ownership on the main thread.

If your application manages its own signals, call `cwsandbox.disable_signal_handlers()` or set `CWSANDBOX_DISABLE_SIGNAL_HANDLERS=1` before you create the first sandbox. The `atexit` handler still runs, but your application must stop sandboxes when a signal arrives.

## Manual cleanup

Use manual cleanup when you need explicit control over when to release a sandbox or session. Manual cleanup lets you pass stop options or coordinate cleanup across long-running code.

### Sandbox stop()

Choose plain stop or snapshot-on-stop before shutdown begins. Each example creates a separate
sandbox and waits for its command before stopping it. The context manager also attempts cleanup
if the work or stop call raises an exception.

> [tab] Plain stop
>
> Stop without capturing a snapshot. This example allows 30 seconds for graceful shutdown and
> uses `missing_ok=True` to tolerate a sandbox that is already gone:
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
>     result = sandbox.exec(["echo", "hello"]).result()
>     sandbox.stop(graceful_shutdown_seconds=30.0, missing_ok=True).result()
> ```

> [tab] Snapshot on stop
>
> Snapshot-on-stop requires an organization enabled for File System Snapshots (FSS) and a sandbox
> started with a `file_system_snapshot` mount. It captures that mount, not the entire sandbox
> filesystem. See [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) for setup.
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import FileSystemSnapshotOptions, Sandbox
>
> with Sandbox.run(
>     file_system_snapshot=FileSystemSnapshotOptions(mount_path="/work", size="10Gi"),
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as sandbox:
>     sandbox.exec(["sh", "-c", "echo hello > /work/data.txt"], check=True).result()
>     sandbox.stop(snapshot_on_stop=True).result()
>     print(sandbox.file_system_snapshot_id)
> ```

A `snapshot_on_stop=True` request raises `SnapshotOnStopConflictError` if a plain stop is already
in progress or the sandbox has already stopped without a captured snapshot. Request the snapshot
before plain cleanup begins. Repeated plain stops can share the same operation. See
[Stop a sandbox](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#stop) for stop behavior.

### Session close()

When you close a session, it stops all sandboxes it owns:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import SandboxDefaults

session = cwsandbox.Session(SandboxDefaults(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH)
sandbox = session.sandbox()
# ...
session.close().result()  # Stops all sandboxes
```

### Batch cleanup

The following example stops several sandboxes in parallel:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import results

sandboxes = [
    Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
    for _ in range(5)
]
# ... use sandboxes ...
results([sb.stop() for sb in sandboxes])  # Stop all in parallel
```

## Orphan management

Orphans are sandboxes left running unintentionally after the process that created them exits. A standalone sandbox that you keep running on purpose isn't an orphan, but it becomes one if you lose track of it. The following sections describe how to make orphans easy to find, how to query for them, and how to bring them back under managed cleanup.

### Tagging for discovery

Use tags to make any orphans discoverable later. For sandboxes in sessions and context managers, the SDK's automatic cleanup prevents most orphans. Those sandboxes can still keep running after forced shutdowns (`kill -9`) or network failures. The cleanup handlers never stop a standalone sandbox, so it becomes an orphan if you forget to stop it.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxDefaults

# Tag at creation time
defaults = SandboxDefaults(
    container_image="python:3.11",
    tags=("my-project", "batch-job-123"),
    resources={"cpu": "1", "memory": "1Gi"},
)

with Sandbox.run(defaults=defaults, auth=AUTH) as sandbox:
    result = sandbox.exec(["echo", "hello"]).result()
```

Use the following tags to make sandboxes discoverable:

* Project or application name (`my-project`)
* Job or run identifier (`batch-job-123`, `run-2024-01-15`)
* Environment (`dev`, `staging`, `prod`)

### Find orphaned sandboxes

Query by tags to find sandboxes from previous runs:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

orphans = Sandbox.list(tags=["my-project"], auth=AUTH).result()
for sandbox in orphans:
    sandbox.stop().result()
```

### Session adoption

Adopting an orphan attaches it to a session so the session governs its lifetime. The orphan then receives the same automatic cleanup guarantees as newly created sandboxes. `session.list()` adds the session's default tags to your filter, so it finds only sandboxes that carry them. To search without the session's tags, use `Sandbox.list()` and adopt each result, as in the [Sessions guide](https://docs.coreweave.com/products/sandboxes/client/guides/sessions.md#adopt-external-sandboxes):

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults

with cwsandbox.Session(SandboxDefaults(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH) as session:
    orphans = session.list(tags=["my-project"]).result()
    for sandbox in orphans:
        session.adopt(sandbox)
# All adopted sandboxes cleaned up with session
```

### Stop by ID

To stop a sandbox whose ID you saved from an earlier run, reconnect with the same credential. Replace `[SANDBOX-ID]` with the sandbox ID:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
sandbox.stop(missing_ok=True).result()
```

If the sandbox disappears before the stop request, the `missing_ok=True` option suppresses `SandboxNotFoundError`. It doesn't suppress a failed `Sandbox.from_id()` lookup. If the sandbox is already gone, that call still raises `SandboxNotFoundError`.

### Delete by ID

To use options such as `graceful_shutdown_seconds` or `snapshot_on_stop`, call `stop()` on a sandbox instance. `Sandbox.delete()` deletes directly by ID without creating an instance.

When you already know a sandbox's ID, you can delete it without listing or adopting it first:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

Sandbox.delete("sandbox-abc123", auth=AUTH).result()
Sandbox.delete("sandbox-abc123", missing_ok=True, auth=AUTH).result()  # Ignore if gone
```
