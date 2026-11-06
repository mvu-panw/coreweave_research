# Remote functions

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/remote-functions

# Remote functions

> Run Python functions inside sandboxes with automatic serialization.

This tutorial shows you how to run Python functions inside a sandbox using remote functions. You can call sandbox-executed code as if it were a local function instead of constructing shell command strings. It's for developers who want to invoke compute in a sandbox directly from their Python code and collect typed results.

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

## Define and call a remote function

Decorate a function with `@session.function()` to call it inside the sandbox with `.remote()`. The call returns a reference you resolve with `.result()`:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxDefaults

with Sandbox.session(SandboxDefaults(
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH) as session:
    @session.function()
    def add(x: int, y: int) -> int:
        return x + y

    result = add.remote(2, 3).result()  # 5
```

## Run functions in parallel with `.map()`

Use `.map()` to dispatch many invocations at once and collect their results. Independent calls run concurrently instead of one at a time:

```python theme={"system"}
@session.function()
def square(x: int) -> int:
    return x * x

refs = square.map([(1,), (2,), (3,)])
results = [r.result() for r in refs]  # [1, 4, 9]
```

## Next steps

You can now invoke Python functions inside a sandbox as if they were local calls, and fan out work in parallel with `.map()`.

For argument and return types, `.local()` testing, and more, see the [Remote functions guide](https://docs.coreweave.com/products/sandboxes/client/guides/remote-functions.md).
