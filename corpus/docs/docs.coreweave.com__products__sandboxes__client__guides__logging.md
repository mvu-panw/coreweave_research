# Sandbox logging

Source: https://docs.coreweave.com/products/sandboxes/client/guides/logging

# Sandbox logging

> Stream container logs (stdout and stderr) from a sandbox's main process with stream_logs().

This guide shows how to capture container logs from a running sandbox to monitor the main process and debug failures. Retrieve logs before stopping the sandbox.

Container logs are stdout and stderr from a sandbox's **main process**. Stream them with `stream_logs()`, which captures output from the command passed to `Sandbox.run()`. Output from `exec()` commands isn't included. Use `Process.stdout` or `Process.stderr` for that.

`stream_logs()` returns a `StreamReader` that yields log lines. Iterate synchronously or asynchronously.

> [!NOTE]
>
> When you call `Sandbox.run()` without a command, the sandbox's default command doesn't write to stdout or stderr, so `stream_logs()` returns no output. Pass a command that writes to stdout or stderr.

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

## Retrieve recent logs

Use `tail_lines` to fetch the most recent log lines without streaming the entire history. This is useful for quick inspection of a running sandbox.

```python theme={"system"}
for line in sandbox.stream_logs(tail_lines=100):
    print(line, end="")
```

## Follow mode

Stream logs continuously, like `tail -f`. The iterator blocks until new data arrives.

```python theme={"system"}
for line in sandbox.stream_logs(follow=True):
    print(line, end="")
```

Press `Ctrl+C` to interrupt follow mode. Its effect on sandboxes depends on what the Python process
owns:

* In an observer process that only reconnects with `Sandbox.from_id()` and streams logs, `Ctrl+C`
  interrupts the log iterator without sending a stop request to the sandbox.
* In a process that owns session-managed sandboxes, the SDK's installed `SIGINT` handler also
  attempts to stop all sandboxes in registered sessions. Interrupting logs can therefore shut down
  other sandboxes that process owns.

Unless turned off beforehand, signal handlers in `cwsandbox>=1.15.0` activate on first sandbox ownership
and install only from Python's main thread. The global handlers don't stop standalone sandboxes,
though a sandbox context manager stops its sandbox when the block exits. If your
application disables or replaces signal handlers, its own shutdown behavior applies. See
[Global cleanup handlers](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md#global-cleanup-handlers).

## Filter by time

Pass `since_time` to retrieve only logs after a specific timestamp. This narrows output to a window of interest, such as logs since a deployment or incident.

```python theme={"system"}
from datetime import datetime, timezone

since = datetime(2026, 2, 20, 14, 0, 0, tzinfo=timezone.utc)
for line in sandbox.stream_logs(since_time=since):
    print(line, end="")
```

## Timestamps

Set `timestamps=True` to prefix each line with an ISO 8601 timestamp from the server. Server-side timestamps help correlate sandbox events with other systems.

```python theme={"system"}
for line in sandbox.stream_logs(tail_lines=10, timestamps=True):
    print(line, end="")
# Output: 2026-02-20T14:30:00Z some log line
```

## Async iteration

If your application uses `asyncio`, iterate over the same `StreamReader` with `async for` to avoid blocking the event loop.

```python theme={"system"}
async for line in sandbox.stream_logs(follow=True):
    print(line, end="")
```

## Retrieve logs before stopping

Log retrieval requires a running sandbox. Retrieve the logs you need before stopping it. Both the Python SDK and the [CLI](https://docs.coreweave.com/products/sandboxes/cli.md#view-logs) reject log retrieval after the sandbox stops.

## See also

* [Command execution](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md): Running commands and streaming their output with `exec()`
* [Sync vs async](https://docs.coreweave.com/products/sandboxes/client/guides/sync-vs-async.md): Iteration patterns
