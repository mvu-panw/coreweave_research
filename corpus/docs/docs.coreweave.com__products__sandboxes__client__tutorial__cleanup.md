# Cleanup

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/cleanup

# Cleanup

> Terminate sandboxes and manage cleanup with context managers, explicit stops, and global atexit handlers.

This page shows how to terminate sandboxes reliably so resources are released when your code finishes or exits unexpectedly. Use these patterns to avoid leaving orphaned sandboxes running after your script completes.

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

## Clean up sandboxes

Use a context manager to handle cleanup automatically:

```python theme={"system"}
from cwsandbox import Sandbox
from sandbox_auth import AUTH

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    sandbox.exec(["echo", "hello"]).result()
# Stopped automatically
```

For sandboxes created without a context manager, call `.stop()` explicitly:

```python theme={"system"}
from cwsandbox import Sandbox
from sandbox_auth import AUTH

sandbox = Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH)
sandbox.exec(["echo", "hello"]).result()
sandbox.stop().result()
```

As a safety net, the SDK registers global cleanup handlers for `atexit` and signals (Ctrl+C, `SIGTERM`). These handlers stop sandboxes that belong to a [`Session`](https://docs.coreweave.com/products/sandboxes/client/guides/sessions), so session-managed sandboxes stop even on unexpected exits.

A sandbox created directly with `Sandbox.run()` isn't part of a session, so it can keep running after the process exits. It still ends when its ordinary main command exits successfully, you stop it, its maximum lifetime expires, or it fails. A nonzero main-command exit can trigger automatic restarts before failure. See [Main command lifetime](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#main-command-lifetime) for lifecycle end conditions and Compose exceptions. [Set up Claude Code with the Sandboxes SDK](https://docs.coreweave.com/products/sandboxes/agents/claude-code.md#set-up-with-the-sandbox-sdk) shows a workflow that keeps a sandbox running after the client exits.

For batch cleanup, tagging strategies, and orphan recovery, see the [Cleanup patterns guide](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md).
