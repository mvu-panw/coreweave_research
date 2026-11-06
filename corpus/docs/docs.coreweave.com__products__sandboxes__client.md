# Sandboxes Python client

Source: https://docs.coreweave.com/products/sandboxes/client

# Sandboxes Python client

> Python SDK for creating and managing CoreWeave sandbox environments.

The `cwsandbox` Python client provides a high-level SDK for creating and managing CoreWeave sandbox environments. It supports both synchronous and asynchronous workflows through a unified API.

## Prepare your Python environment

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/). In your project directory, activate an existing Python 3.11 or later virtual environment, or create one:

```bash theme={"system"}
uv venv --python 3.12
source .venv/bin/activate
```

Run the installation commands and example scripts from this environment.

## Choose authentication

These examples run on serverless capacity unless a section specifies CKS. Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

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

## Quick start

Create a sandbox, run a command, and retrieve the result:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

# Context manager for automatic cleanup
with Sandbox.run(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sb:
    result = sb.exec(["python", "-c", "print(2 + 2)"]).result()
    print(result.stdout)  # 4
```

In async code, use `Sandbox(...)` with `async with` to start the sandbox without blocking the event loop. `Sandbox.run()` calls `start().result()` internally, which blocks during startup. See [Sync versus async patterns](https://docs.coreweave.com/products/sandboxes/client/guides/sync-vs-async.md#create-sandboxes).

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

async with Sandbox(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sb:
    result = await sb.exec(["python", "-c", "print(2 + 2)"])
    print(result.stdout)  # 4
```

## Migrate from `wandb.sandbox`

`wandb.sandbox` is deprecated. Use `cwsandbox` directly and select authentication explicitly. For account setup, follow the [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md#choose-a-credential).

### Install and retain Forge authentication

These examples use a Forge SaaS API key on serverless capacity. For a dedicated instance, follow [Use sandboxes with W\&B Dedicated Cloud](https://docs.coreweave.com/products/sandboxes/dedicated-cloud.md).

In your active Python environment, install the standalone client and set your key. Replace `[WANDB-API-KEY]` with your Forge API key:

```bash theme={"system"}
uv pip install 'cwsandbox>=1.14.2'
export WANDB_API_KEY="[WANDB-API-KEY]"
```

When you import the deprecated wrapper, it selects Forge authentication:

```python title="Before: wandb.sandbox" theme={"system"}
from wandb.sandbox import Sandbox

with Sandbox.run(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    result = sandbox.exec(["python", "-c", "print(2 + 2)"]).result()
    print(result.stdout)
```

With `cwsandbox`, pass the key through `AuthHeaders`. This route doesn't require the optional `wandb` dependency:

```python title="After: cwsandbox" theme={"system"}
import os
from cwsandbox import AuthHeaders, Sandbox

forge_auth = AuthHeaders(
    headers={"x-wandb-api-key": os.environ["WANDB_API_KEY"]},
    strategy="wandb_api_key",
)

with Sandbox.run(
    auth=forge_auth,
    placement_mode="serverless",
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
    max_lifetime_seconds=43200,
) as sandbox:
    result = sandbox.exec(["python", "-c", "print(2 + 2)"]).result()
    print(result.stdout)
```

Save the migrated example as a file named `migrated_sandbox.py`, then run it:

```bash theme={"system"}
python migrated_sandbox.py
```

Both examples print `4` and stop the sandbox when the `with` block exits.

The migrated example sets `max_lifetime_seconds=43200` explicitly to retain the wrapper's 12-hour default. If your previous configuration selected a team or project, add `x-entity-id` or `x-project-name` to `headers`.

Alternatively, follow [Choose authentication](#choose-authentication) to use the `AuthStrategy.WANDB` route. Install `cwsandbox[wandb]`, import `AuthStrategy`, and pass `auth=AuthStrategy.WANDB`. This route uses the `wandb` dependency to resolve a configured session, `WANDB_API_KEY`, or credentials saved by `wandb login`. If no credential is configured, it can prompt you. It supports user API keys.

The explicit `AuthHeaders` example reads `WANDB_API_KEY` through `os.environ`. That variable alone doesn't change the client's default authentication.

### Review wrapper defaults

An import change alone doesn't preserve all wrapper behavior:

| Behavior | Migration action |
| - | - |
| Authentication | Pass `auth` explicitly. Without an explicit choice or an installed legacy override, `cwsandbox` reads a CoreWeave API access token from `CWSANDBOX_API_KEY`. The `wandb.sandbox` import installs a process-wide Forge authentication override. Remove remaining wrapper imports. |
| Maximum lifetime | If you need the wrapper's 12-hour default, set `max_lifetime_seconds` on a sandbox or in `SandboxDefaults`. Otherwise, the server determines the default. |
| Secrets | The wrapper's `Secret` defaults `store` to `"wandb-team-secrets"`. `cwsandbox.Secret` requires an explicit store. For Forge team secrets, use `Secret(store="wandb", name="[SECRET-NAME]")` with Forge authentication and serverless placement. See [Use Forge secrets](https://docs.coreweave.com/products/sandboxes/secrets.md). |

A CoreWeave API access token supports both serverless and CKS placement. For placement options and account requirements, see [Sandbox placement and spillover](https://docs.coreweave.com/products/sandboxes/placement.md).

If your code uses profile selectors or discovery APIs, follow [What changed from profiles](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md#what-changed-from-profiles) and [Discover available runners](https://docs.coreweave.com/products/sandboxes/client/guides/discovery.md).

## Next steps

Use the [CLI guide](https://docs.coreweave.com/products/sandboxes/cli.md) to manage existing sandboxes from your terminal.

> [card] [Get started](https://docs.coreweave.com/products/sandboxes/get-started.md)
>
> Authenticate and run your first serverless sandbox with the SDK.

> [card] [Tutorial](https://docs.coreweave.com/products/sandboxes/client/tutorial/configuration.md)
>
> Learn to configure sandboxes, run commands, transfer files, and clean up with the Python SDK.

> [card] [Guides](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md)
>
> In-depth guides about specific topics including lifecycle management, file operations, execution patterns, and troubleshooting.
