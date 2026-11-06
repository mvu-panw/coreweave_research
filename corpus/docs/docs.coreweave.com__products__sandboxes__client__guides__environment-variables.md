# Environment variables

Source: https://docs.coreweave.com/products/sandboxes/client/guides/environment-variables

# Environment variables

> Set and manage environment variables in CWSandbox instances, including session-level defaults

This guide shows you how to set and manage environment variables in CWSandbox instances. Use environment variables to pass non-sensitive configuration values, such as log levels or project identifiers, into your sandboxes. You can set them on individual sandboxes, share them across sandboxes in a session, or scope them to remote functions.

> [!WARNING]
>
> Don't hardcode API keys, passwords, or other credentials in `environment_variables`, or print them to logs. Prefer secret references over passing raw credentials. Keep sensitive values in a secret manager, even when Forge secret injection isn't available. This guidance applies to both serverless and CKS sandboxes.

For serverless sandboxes authenticated with Forge, use [Forge secrets](https://docs.coreweave.com/products/sandboxes/secrets.md). The server resolves these references and injects the values as environment variables. Forge secret injection is not available for CKS placement or sandboxes authenticated with a CoreWeave API access token. For CKS, use your organization's approved method for delivering secrets to workloads.

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

## Basic usage

To make values available to processes running inside the sandbox, pass an `environment_variables` dictionary to `Sandbox.run`:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(
    environment_variables={"LOG_LEVEL": "info"},
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    result = sandbox.exec([
        "python",
        "-c",
        "import os; print(os.environ.get('LOG_LEVEL'));",
    ]).result()
    print(result.stdout.strip())  # "info"
```

## Session-level defaults

When you need the same variables in several sandboxes, define them once on a session instead of repeating them per sandbox. Individual sandboxes can override session defaults or add their own variables:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import SandboxDefaults, Session

defaults = SandboxDefaults(
    environment_variables={
        "PROJECT_ID": "my-project",
        "LOG_LEVEL": "info",
    },
    resources={"cpu": "1", "memory": "1Gi"},
)

with Session(defaults, auth=AUTH) as session:
    with session.sandbox() as sb1:
        result = sb1.exec([
            "python",
            "-c",
            "import os; print(os.environ.get('LOG_LEVEL'));",
        ]).result()
        print(result.stdout.strip())  # "info"

    # Override LOG_LEVEL and add new variable
    with session.sandbox(
        environment_variables={
            "LOG_LEVEL": "debug",  # Override session default
            "MODEL_NAME": "gpt-4",  # Add new variable
        }
    ) as sb2:
        result = sb2.exec([
            "python",
            "-c",
            "import os; "
            "print(os.environ.get('PROJECT_ID')); "
            "print(os.environ.get('LOG_LEVEL')); "
            "print(os.environ.get('MODEL_NAME'));",
        ]).result()
        lines = result.stdout.strip().split("\n")
        print(lines)  # ["my-project", "debug", "gpt-4"]
```

## Remote functions

Remote functions inherit environment variables from the session and can declare their own through the `@session.function` decorator. The SDK merges function-level variables with session defaults at call time:

```python theme={"system"}
from sandbox_auth import AUTH
with Session(defaults, auth=AUTH) as session:
    @session.function(environment_variables={"MODEL_VERSION": "v2.0"})
    def process(task_id: int) -> dict:
        import os
        return {
            "task": task_id,
            "project": os.environ.get("PROJECT_ID"),  # From session defaults
            "version": os.environ.get("MODEL_VERSION"),  # From function decorator
        }

    result = process.remote(42).result()
    print(result)  # {"task": 42, "project": "my-project", "version": "v2.0"}
```

> [!WARNING]
>
> Environment variables are passed by reference. Subsequent function calls reflect mutations to the dictionary after decoration, as shown in the following example.

```python theme={"system"}
env_vars = {"MODEL_VERSION": "v2.0"}

@session.function(environment_variables=env_vars)
def process(task_id: int) -> dict:
    import os
    return {"version": os.environ.get("MODEL_VERSION")}

result = process.remote(42).result()  # version: "v2.0"

env_vars["MODEL_VERSION"] = "v3.0"  # Mutate the dictionary

result = process.remote(42).result()  # version: "v3.0" (changed)
```
