# Get started with CoreWeave Sandboxes

Source: https://docs.coreweave.com/products/sandboxes/get-started

# Get started with CoreWeave Sandboxes

> Run your first sandbox on serverless capacity with a Forge API key or CoreWeave API access token.

Run a command in a sandbox on serverless capacity and print its output. No cluster setup is required.

## Before you begin

Serverless sandboxes are generally available, and usage is billed. Access is enabled per organization. To request access for your organization, contact [support](mailto:forge-support@coreweave.com).

If your organization uses W\&B Dedicated Cloud, follow [Use sandboxes with W\&B Dedicated Cloud](https://docs.coreweave.com/products/sandboxes/dedicated-cloud.md).

## Run your first sandbox

Choose the credential for the account that owns and is billed for your sandbox. A Forge API key supports serverless placement. A CoreWeave API access token supports serverless and CoreWeave Kubernetes Service (CKS) placement. For account requirements, see [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). Choose a credential tab, then [verify the result](#verify-the-result).

> [tab] Forge API key
>
> Get your [Forge API key](https://forge.coreweave.com/settings#apikeys). If you don't have an account, sign up through the same link. Then set the key in your terminal. These examples explicitly select W\&B authentication:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> > [tab] Python
> >
> > With [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed, save this as `hello.py`:
> >
> > ```python title="hello.py" theme={"system"}
> > from cwsandbox import AuthStrategy, Sandbox
> >
> > with Sandbox.run(
> >     auth=AuthStrategy.WANDB,
> >     resources={"cpu": "1", "memory": "1Gi"},
> > ) as sandbox:
> >     print(sandbox.exec(["echo", "Hello!"]).result().stdout)
> > ```
> >
> > Run it with Python 3.11 and the sandbox client. The command installs them if needed:
> >
> > ```bash theme={"system"}
> > uv run --python 3.11 --with 'cwsandbox[wandb]>=1.14.2' hello.py
> > ```
>
> > [tab] TypeScript
> >
> > With Node.js 22 or later installed, install the client:
> >
> > ```bash theme={"system"}
> > npm install @coreweave/cwsandbox@1.0.0
> > ```
> >
> > Save this as `hello.mts`:
> >
> > ```typescript title="hello.mts" theme={"system"}
> > import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
> >
> > const client = createSandboxClient({
> >   apiKey: process.env.WANDB_API_KEY,
> > });
> > const result = await client.withSandbox(
> >   async (sandbox) => sandbox.commands.run(["echo", "Hello!"]),
> >   { resources: { cpu: "1", memory: "1Gi" } },
> > );
> > console.log(result.stdout);
> > ```
> >
> > Run it with `tsx`:
> >
> > ```bash theme={"system"}
> > npx --yes --package=tsx tsx hello.mts
> > ```
>
> The Forge API key uses the SDK's existing W\&B identifiers: `WANDB_API_KEY`, `AuthStrategy.WANDB`, and the TypeScript `/wandb` entry point.

> [tab] CoreWeave API access token
>
> Ask your administrator to create or update an [Access Policy](https://console.coreweave.com/organization/iam/access-policies) granting you the **Sandbox User** role. See [Create an access policy](https://docs.coreweave.com/security/iam/access-policies/manage.md#create-an-access-policy) for the steps.
>
> Create an API access token on the [Tokens](https://console.coreweave.com/tokens) page, copy its **Token Secret**, and set it in your terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > With [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed, save this as `hello.py`:
> >
> > ```python title="hello.py" theme={"system"}
> > from cwsandbox import AuthStrategy, Sandbox
> >
> > with Sandbox.run(
> >     auth=AuthStrategy.COREWEAVE_API_KEY,
> >     resources={"cpu": "1", "memory": "1Gi"},
> > ) as sandbox:
> >     print(sandbox.exec(["echo", "Hello!"]).result().stdout)
> > ```
> >
> > Run it with Python 3.11 and the sandbox client. The command installs them if needed:
> >
> > ```bash theme={"system"}
> > uv run --python 3.11 --with 'cwsandbox>=1.10.0' hello.py
> > ```
>
> > [tab] TypeScript
> >
> > With Node.js 22 or later installed, install the client:
> >
> > ```bash theme={"system"}
> > npm install @coreweave/cwsandbox@1.0.0
> > ```
> >
> > Save this as `hello.mts`:
> >
> > ```typescript title="hello.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > const client = createSandboxClientFromEnv();
> > const result = await client.withSandbox(
> >   async (sandbox) => sandbox.commands.run(["echo", "Hello!"]),
> >   { resources: { cpu: "1", memory: "1Gi" } },
> > );
> > console.log(result.stdout);
> > ```
> >
> > Run it with `tsx`:
> >
> > ```bash theme={"system"}
> > npx --yes --package=tsx tsx hello.mts
> > ```

### Verify the result

The example prints the following output and stops the sandbox when it finishes:

```text title="Output" theme={"system"}
Hello!
```

The sandbox has 1 CPU and 1 GiB of memory. The flat `resources` dictionary sets CPU and memory requests and limits to the same values. Change `resources` to choose its CPU and memory.

For concurrent quotas, rate limits on create requests, and quota errors, see [Limits and quotas](https://docs.coreweave.com/products/sandboxes/reference/limits-and-quotas.md).

## Next steps

Continue with the guide for your workload:

* [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md): enable a runner on your cluster and run a sandbox there.
* [Sandbox placement and spillover](https://docs.coreweave.com/products/sandboxes/placement.md): compare serverless and CKS capacity and configure fallback.
* [Run coding agents](https://docs.coreweave.com/products/sandboxes/agents.md): connect a coding agent to a sandbox.
* [GPU sandboxes](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md): request GPU access and run a GPU workload.
* [Python client](https://docs.coreweave.com/products/sandboxes/client.md): execute commands, work with files, and configure sandboxes.
* [TypeScript client](https://docs.coreweave.com/products/sandboxes/typescript-client.md): run commands, use Compose files, and look up the SDK API.
