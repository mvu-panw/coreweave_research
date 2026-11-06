# Configuration

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/configuration

# Configuration

> Configure sandbox resources, images, and environment settings.

This tutorial shows you how to configure a sandbox at startup by passing options to `Sandbox.run()`. It's for developers who have already created a basic sandbox and want to control the container image, resource allocation, and pre-populated files for their workload.

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

## Pass configuration to `Sandbox.run()`

Configuration options control how the sandbox is provisioned. Pass them as keyword arguments directly to `Sandbox.run()`:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(
    container_image="python:3.11",
    max_lifetime_seconds=300,
    tags=["my-app"],
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    sandbox.exec(["python", "--version"]).result()
```

## Resources

Configure CPU and memory to match your workload's needs and avoid over-provisioning or under-provisioning. Use `ResourceOptions` to set requests and limits:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import ResourceOptions, Sandbox

with Sandbox.run(
    resources=ResourceOptions(
        requests={"cpu": "2", "memory": "2Gi"},
        limits={"cpu": "2", "memory": "2Gi"},
    ),
    auth=AUTH,
) as sandbox:
    sandbox.exec(["python", "compute.py"]).result()
```

`ResourceOptions` uses [Kubernetes resource syntax](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/):

| Resource | Format | Examples |
| - | - | - |
| CPU | Cores or millicores | `"1"`, `"2"`, `"500m"` (0.5 CPU) |
| Memory | Bytes with unit suffix | `"512Mi"`, `"1Gi"`, `"2Gi"` |

## Mounted files

Mounted files let you ship configuration, scripts, or other static content into the sandbox before it starts, so your workload has what it needs the moment it runs. Pre-populate files at sandbox startup:

```python theme={"system"}
from sandbox_auth import AUTH
with Sandbox.run(
    mounted_files=[
        {"mount_path": "/app/config.json", "file_content": b'{"debug": true}'},
        {"mount_path": "/app/script.py", "file_content": b"print('hello')"},
    ],
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    sandbox.exec(["python", "/app/script.py"]).result()
```

Each entry takes `mount_path`, the absolute path inside the sandbox, and `file_content`, the file's contents as bytes. A `str` is encoded as UTF-8 for you.

Mounted files are read-only. Use `write_file()` for files that need modification.

## Next steps

You now have a sandbox that starts with the container image, resource allocation, and pre-mounted files your workload requires.

For reusable configuration across multiple sandboxes, use `SandboxDefaults`. See the [sandbox configuration guide](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md) for all `ResourceOptions` fields, GPU resources, QoS classes, and config-library interop.
