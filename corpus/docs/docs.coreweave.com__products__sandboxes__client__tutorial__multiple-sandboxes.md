# Multiple sandboxes

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/multiple-sandboxes

# Multiple sandboxes

> Tutorial for managing multiple CoreWeave sandbox instances using sessions with shared defaults

This example shows how to run multiple CoreWeave sandboxes in parallel using a session. A session applies shared defaults across the sandboxes and cleans them up automatically when the block exits. Use this pattern to coordinate work across several sandboxes without managing each lifecycle individually.

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

## Run sandboxes in a session

Sessions manage multiple sandboxes with shared defaults and automatic cleanup:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxDefaults

defaults = SandboxDefaults(
    container_image="python:3.11",
    tags=("my-app",),
    resources={"cpu": "1", "memory": "1Gi"},
)

with Sandbox.session(defaults, auth=AUTH) as session:
    sb1 = session.sandbox()
    sb2 = session.sandbox()

    p1 = sb1.exec(["echo", "one"])
    p2 = sb2.exec(["echo", "two"])

    print(p1.result().stdout, p2.result().stdout)
# All sandboxes cleaned up
```

For sandbox pools, adoption patterns, and lifecycle management, see the [Sessions guide](https://docs.coreweave.com/products/sandboxes/client/guides/sessions.md).
