# Use sandboxes with W&B Dedicated Cloud

Source: https://docs.coreweave.com/products/sandboxes/dedicated-cloud

# Use sandboxes with W&B Dedicated Cloud

> Authenticate sandboxes on serverless capacity with an API key from your W&B Dedicated Cloud instance.

If your organization uses W\&B Dedicated Cloud, authenticate sandboxes on serverless capacity with an API key from your dedicated instance instead of `wandb.ai`. The Python client sends your key and instance hostname to the CoreWeave Sandboxes service, which validates the key against your instance. Pass your instance hostname with the key to select the correct instance for authentication.

## Before you begin

You need the following:

* Sandbox access enabled for your Dedicated Cloud instance. Contact your account team to confirm that your instance has the required server updates and to request access.
* The URL of your Dedicated Cloud instance, for example `https://[INSTANCE].wandb.io`. The hostname must end in `.wandb.io`. Instances on custom domains aren't supported.
* Python 3.11 or newer.

W\&B Self-Managed deployments, including air-gapped installations, aren't supported. The TypeScript client doesn't support Dedicated Cloud instances yet, so use the Python client.

## Get an API key from your instance

Create a personal API key on your dedicated instance, not on [forge.coreweave.com/settings#apikeys](https://forge.coreweave.com/settings#apikeys):

1. Sign in to your Dedicated Cloud instance.
2. Click the account selector in the upper-right corner, then click **User settings**.
3. In the **API keys** section, click **New key**. Name the key, then click **Create API key**.

Your instance shows the full key only once, when you create it. For more information, see [How do I find my API key?](https://docs.coreweave.com/support/models/articles/how-do-i-find-my-api-key#personal-api-key) in the Forge documentation.

## Configure instance authentication

Install the Python client:

```bash theme={"system"}
uv pip install 'cwsandbox>=1.14.2'
```

Set your instance hostname and API key. Replace `[INSTANCE]` with your instance's hostname prefix and `[WANDB-API-KEY]` with the key you created:

```bash theme={"system"}
export FORGE_HOST="[INSTANCE].wandb.io"
export WANDB_API_KEY="[WANDB-API-KEY]"
```

The example passes the hostname in the `x-wandb-host` header. Use the hostname without `https://` or a path. The Sandbox API endpoint stays unchanged.

## Run a sandbox

Pass the key and dedicated instance hostname through `AuthHeaders`:

```python theme={"system"}
import os
from cwsandbox import AuthHeaders, Sandbox

forge_auth = AuthHeaders(
    headers={
        "x-wandb-api-key": os.environ["WANDB_API_KEY"],
        "x-wandb-host": os.environ["FORGE_HOST"],
    },
    strategy="wandb_api_key",
)

with Sandbox.run(
    auth=forge_auth,
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    result = sandbox.exec(["echo", "Hello!"]).result()
    print(result.stdout)
```

If the command succeeds, `Hello!` appears in the output.

If authentication fails, confirm that `FORGE_HOST` matches the instance where you created the key. A key from a dedicated instance doesn't authenticate against `wandb.ai`, and a `wandb.ai` key doesn't authenticate against a dedicated instance.

## Next steps

* [Sandbox placement and spillover](https://docs.coreweave.com/products/sandboxes/placement.md) covers placement modes, credentials, and spillover.
* The [Python client](https://docs.coreweave.com/products/sandboxes/client.md) documentation covers lifecycle, execution, file operations, and other SDK patterns.
