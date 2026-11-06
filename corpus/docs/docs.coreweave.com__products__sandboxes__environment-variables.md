# Environment variables

Source: https://docs.coreweave.com/products/sandboxes/environment-variables

# Environment variables

> Environment variables CoreWeave sets inside every sandbox, and how to override them.

This page describes the environment variables CoreWeave sets inside every sandbox, and how to read them from code running in the sandbox. The platform sets them at creation time, in addition to any variables you supply yourself, so that your code can identify its own runtime.

To set your own variables, see [Set your own environment variables](https://docs.coreweave.com/products/sandboxes/client/guides/environment-variables.md).

## Choose authentication

These examples run on serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Save the configuration for your language beside the scripts you run from this page. Python examples import `AUTH` from `sandbox_auth.py`. TypeScript examples import `client` from `sandbox-client.mts`. These files select authentication without storing your credential. For Python, use an [active virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment). For TypeScript, first install the client with `npm install @coreweave/cwsandbox@1.0.0`.

> [tab] Forge API key
>
> Use your Forge API key with the SDK's `wandb` integration. Replace `[WANDB-API-KEY]` with your API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox[wandb]>=1.14.2'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.WANDB
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization. Replace `[API-ACCESS-TOKEN]` with your token:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox>=1.14.2'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.COREWEAVE_API_KEY
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. In TypeScript, choose the CoreWeave token and set a nonempty `runnerIds` array to select CKS. Creating a Python session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Variables

The platform sets the following variable in every sandbox:

| Variable | Value | Description |
| - | - | - |
| `CW_SANDBOX_ID` | UUID | The sandbox's own ID. Identical to the ID returned when the sandbox is created, and the ID you use in API and SDK calls that act on the sandbox. |

The platform sets these variables regardless of which SDK or API version you use.

> [!NOTE]
>
> Don't parse the hostname to obtain the sandbox ID. A sandbox's hostname begins with the sandbox ID, but it carries a generated suffix that changes if the underlying pod restarts. Use `CW_SANDBOX_ID` instead.

## Read a variable

Platform variables are available to each container's main process, to any process it starts, and to processes started with `exec` and streaming execution. The exception is a program that clears its environment before starting a child.

> [tab] Python
>
> ```python theme={"system"}
> import os
>
> sandbox_id = os.environ["CW_SANDBOX_ID"]
> print(f"running in sandbox {sandbox_id}")
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> const sandboxId = process.env.CW_SANDBOX_ID;
>
> console.log(`running in sandbox ${sandboxId}`);
> ```

> [tab] Shell
>
> ```bash theme={"system"}
> echo "$CW_SANDBOX_ID"
> ```

A common use is tagging logs or metrics emitted from inside the sandbox, so that you can later correlate records with the sandbox that produced them.

## Override a variable

Platform variables are defaults, not reserved names. If you set a variable of the same name on your sandbox, the sandbox uses your value and the platform does not apply its default.

Replace `[YOUR-VALUE]` with the value you want the sandbox to report:

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> sandbox = Sandbox.run(
>     container_image="ubuntu:22.04",
>     environment_variables={"CW_SANDBOX_ID": "[YOUR-VALUE]"},
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> )
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.create({
>   containerImage: "ubuntu:22.04",
>   environmentVariables: { CW_SANDBOX_ID: "[YOUR-VALUE]" },
> });
> ```

The following rules apply to overrides:

* **Any value counts, including an empty string.** Setting `CW_SANDBOX_ID` to `""` produces a variable that is present and empty. The platform does not treat an empty value as unset and does not replace it.

* **A policy cannot override platform variables.** The name is reserved against operator configuration, so a cluster's [policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md) cannot silently replace a value you set.

* **Secrets count as overrides.** A [secret](https://docs.coreweave.com/products/sandboxes/secrets.md) mapped to the same variable name suppresses the platform default in the same way a direct value does.

## Metadata only, not identity

`CW_SANDBOX_ID` is advisory metadata. Because it can be overridden, code inside a sandbox can report any value.

> [!WARNING]
>
> Do not use `CW_SANDBOX_ID` for authentication, authorization, or audit attribution. Your own systems recorded a sandbox ID when they created the sandbox. Treat that ID as the source of truth, not a value reported from inside the sandbox.

## Sandboxes with more than one container

Each container receives the value set on the sandbox's first container, unless that container sets `CW_SANDBOX_ID` itself. An explicit value takes precedence for the container that sets it.

This has two consequences:

* If you override the variable on the first container, every other container that sets nothing receives your override.
* If you override it to an empty string on the first container, the other containers do not receive the variable at all.

## Behavior across the sandbox lifecycle

`CW_SANDBOX_ID` behaves as follows across a sandbox's lifetime:

* **The value is fixed for the life of the sandbox.** The platform assigns it at creation, and it does not change if the underlying pod restarts.
* **A restored sandbox is a new sandbox.** Restoring from a file system snapshot creates a sandbox with a new ID. The platform sets `CW_SANDBOX_ID` to that new value unless you override the variable. Any earlier ID your application wrote into a snapshot mount persists as your own data and is not updated.
