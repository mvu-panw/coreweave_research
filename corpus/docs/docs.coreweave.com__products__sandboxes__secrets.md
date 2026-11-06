# Use Forge secrets

Source: https://docs.coreweave.com/products/sandboxes/secrets

# Use Forge secrets

> Inject Forge team secrets into sandboxes on serverless capacity with Python or TypeScript.

Use Forge Secret Manager to make API tokens and other credentials available inside a sandbox on serverless capacity. Your application passes secret names to the Sandboxes API. When the API creates the sandbox, it resolves the values from your Forge team and injects them as environment variables.

## Before you begin

Forge secret injection requires a sandbox authenticated with a Forge API key. It's available for serverless sandboxes, but not for sandboxes on your own CoreWeave Kubernetes Service (CKS) cluster. CKS placement uses a CoreWeave API access token. You can't combine that token with a separate Forge API key to resolve secrets for a CKS sandbox.

| Sandbox placement | Sandbox credential | Forge secret injection |
| - | - | - |
| Serverless | Forge API key | Supported. Use the `wandb` store. |
| Serverless | CoreWeave API access token | Not supported. |
| Your CKS cluster | CoreWeave API access token | Not supported. Adding `WANDB_API_KEY` doesn't enable it. |

To follow the examples, you need the following:

* A Forge software-as-a-service (SaaS) account with [serverless sandbox access](https://docs.coreweave.com/products/sandboxes/get-started.md).
* A secret named `HF_TOKEN` in your Forge team's Secret Manager. If the secret doesn't exist, ask a Forge administrator to [add the secret](https://docs.coreweave.com/products/wandb/platform/secrets.md#add-a-secret).
* A Forge API key with access to that team.

Set `WANDB_API_KEY` in the environment of the process that creates the sandbox. Replace `[WANDB-API-KEY]` with your Forge API key:

```bash theme={"system"}
export WANDB_API_KEY="[WANDB-API-KEY]"
```

The examples use the API key's default team unless you set `WANDB_ENTITY`. If the secret belongs to another team, set `WANDB_ENTITY` to that team. Replace `[WANDB-ENTITY]` with the team name:

```bash theme={"system"}
export WANDB_ENTITY="[WANDB-ENTITY]"
```

The examples pass the key and team explicitly to the client. Setting these variables alone does not select W\&B authentication in the sandbox client.

Install the client for your language:

> [tab] Python
>
> Use Python 3.11 or later and [install `uv`](https://docs.astral.sh/uv/getting-started/installation/) if needed. In your Python environment, install the client:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> ```

> [tab] TypeScript
>
> Use Node.js 22 or later. Install the TypeScript client and `tsx` to run the examples:
>
> ```bash theme={"system"}
> npm install @coreweave/cwsandbox@1.0.0
> npm install --save-dev tsx
> ```
>
> Save the TypeScript example you want to run as `secrets.mts`, then run `npx tsx secrets.mts`.

## Inject a secret

Use `store="wandb"` in Python or `store: "wandb"` in TypeScript. This store resolves secrets for the authenticated Forge team. You don't need to register an organization secret store for this flow.

The following examples inject `HF_TOKEN` and check that it's present without printing its value. In the sandbox, the environment variable defaults to the secret's name.

> [tab] Python
>
> Pass the Forge API key and optional team through `AuthHeaders`:
>
> ```python theme={"system"}
> import os
> from cwsandbox import AuthHeaders, Sandbox, Secret
>
> forge_auth = AuthHeaders(
>     headers={
>         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
>         **({"x-entity-id": os.environ["WANDB_ENTITY"]} if os.environ.get("WANDB_ENTITY") else {}),
>     },
>     strategy="wandb_api_key",
> )
>
> with Sandbox.run(
>   auth=forge_auth,
>   placement_mode="serverless",
>   container_image="python:3.11",
>   resources={"cpu": "1", "memory": "1Gi"},
>   secrets=[Secret(store="wandb", name="HF_TOKEN")],
> ) as sandbox:
>   result = sandbox.exec([
>     "python", "-c",
>     "import os; assert os.environ.get('HF_TOKEN'); print('Secret is available')",
>   ]).result()
>   print(result.stdout)
> ```

> [tab] TypeScript
>
> Import the client from the Forge entry point. When you omit `runnerIds`, the client uses serverless placement:
>
> ```typescript theme={"system"}
> import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
>
> const client = createSandboxClient({
>   apiKey: process.env.WANDB_API_KEY,
>   entity: process.env.WANDB_ENTITY,
> });
>
> const result = await client.withSandbox(
>   async (sandbox) => sandbox.commands.run([
>     "python", "-c",
>     "import os; assert os.environ.get('HF_TOKEN'); print('Secret is available')",
>   ]),
>   {
>     containerImage: "python:3.11",
>     resources: { cpu: "1", memory: "1Gi" },
>     secrets: [{ store: "wandb", name: "HF_TOKEN" }],
>   },
> );
>
> console.log(result.stdout);
> ```

Both examples print `Secret is available` and stop the sandbox when the operation finishes. Code running inside the sandbox can read the value from `HF_TOKEN`.

Pass the secret's name, not its value, in `secrets`. The server resolves the value. Don't print it or write it to logs.

## Secret reference fields

Use these fields in a Python `Secret` or a TypeScript `secrets` entry:

| Python field | TypeScript field | Required | Description |
| - | - | - | - |
| `store` | `store` | Yes | Secret store name. Use `wandb` for Forge Secret Manager. |
| `name` | `name` | Yes | Name of the secret in the selected Forge team's Secret Manager. |
| `field` | `field` | No | Top-level key to select from a secret whose value is a JSON object. Omit it to inject the entire secret value. |
| `env_var` | `envVar` | No | Environment variable that receives the value. Defaults to `name`. |

## Use a custom environment variable name

To choose the environment variable that receives the secret, set `env_var` in Python or `envVar` in TypeScript. The following examples expose the `HF_TOKEN` secret as `HUGGINGFACE_TOKEN`:

> [tab] Python
>
> ```python theme={"system"}
> import os
> from cwsandbox import AuthHeaders, Sandbox, Secret
>
> forge_auth = AuthHeaders(
>     headers={
>         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
>         **({"x-entity-id": os.environ["WANDB_ENTITY"]} if os.environ.get("WANDB_ENTITY") else {}),
>     },
>     strategy="wandb_api_key",
> )
>
> with Sandbox.run(
>   auth=forge_auth,
>   placement_mode="serverless",
>   container_image="python:3.11",
>   secrets=[Secret(
>     store="wandb",
>     name="HF_TOKEN",
>     env_var="HUGGINGFACE_TOKEN",
>   )],
>   resources={"cpu": "1", "memory": "1Gi"},
> ) as sandbox:
>   result = sandbox.exec([
>     "python", "-c",
>     "import os; assert os.environ.get('HUGGINGFACE_TOKEN'); print('Secret is available')",
>   ]).result()
>   print(result.stdout)
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
>
> const client = createSandboxClient({
>   apiKey: process.env.WANDB_API_KEY,
>   entity: process.env.WANDB_ENTITY,
> });
>
> const result = await client.withSandbox(
>   async (sandbox) => sandbox.commands.run([
>     "python", "-c",
>     "import os; assert os.environ.get('HUGGINGFACE_TOKEN'); print('Secret is available')",
>   ]),
>   {
>     containerImage: "python:3.11",
>     secrets: [{
>       store: "wandb",
>       name: "HF_TOKEN",
>       envVar: "HUGGINGFACE_TOKEN",
>     }],
>   },
> );
>
> console.log(result.stdout);
> ```

Both examples print `Secret is available` after they check that `HUGGINGFACE_TOKEN` is present.

## Select a field from a structured secret

To inject one value from a JSON object, set `field` to its top-level key. Nested paths aren't supported. For a JSON string, the injected value has no surrounding JSON quotes.

For this example, add a team secret named `DB_CREDENTIALS` whose value is a JSON object such as `{"password":"[DB-PASSWORD]"}`. Replace `[DB-PASSWORD]` with the password before you save the secret. The examples inject its `password` field into `DB_PASSWORD`:

> [tab] Python
>
> ```python theme={"system"}
> import os
> from cwsandbox import AuthHeaders, Sandbox, Secret
>
> forge_auth = AuthHeaders(
>     headers={
>         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
>         **({"x-entity-id": os.environ["WANDB_ENTITY"]} if os.environ.get("WANDB_ENTITY") else {}),
>     },
>     strategy="wandb_api_key",
> )
>
> with Sandbox.run(
>   auth=forge_auth,
>   placement_mode="serverless",
>   container_image="python:3.11",
>   secrets=[Secret(
>     store="wandb",
>     name="DB_CREDENTIALS",
>     field="password",
>     env_var="DB_PASSWORD",
>   )],
>   resources={"cpu": "1", "memory": "1Gi"},
> ) as sandbox:
>   result = sandbox.exec([
>     "python", "-c",
>     "import os; assert os.environ.get('DB_PASSWORD'); print('Secret is available')",
>   ]).result()
>   print(result.stdout)
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
>
> const client = createSandboxClient({
>   apiKey: process.env.WANDB_API_KEY,
>   entity: process.env.WANDB_ENTITY,
> });
>
> const result = await client.withSandbox(
>   async (sandbox) => sandbox.commands.run([
>     "python", "-c",
>     "import os; assert os.environ.get('DB_PASSWORD'); print('Secret is available')",
>   ]),
>   {
>     containerImage: "python:3.11",
>     secrets: [{
>       store: "wandb",
>       name: "DB_CREDENTIALS",
>       field: "password",
>       envVar: "DB_PASSWORD",
>     }],
>   },
> );
>
> console.log(result.stdout);
> ```

Both examples print `Secret is available` without printing the password. Selecting a field fails if the secret isn't a JSON object, the key doesn't exist, or its value is `null`.

## Reuse secret references

For Python sessions, put shared secret references in `SandboxDefaults`. For TypeScript, reuse a `secrets` array when you create sandboxes:

> [tab] Python
>
> ```python theme={"system"}
> import os
> from cwsandbox import AuthHeaders, SandboxDefaults, Secret, Session
>
> forge_auth = AuthHeaders(
>     headers={
>         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
>         **({"x-entity-id": os.environ["WANDB_ENTITY"]} if os.environ.get("WANDB_ENTITY") else {}),
>     },
>     strategy="wandb_api_key",
> )
>
> defaults = SandboxDefaults(
>   auth=forge_auth,
>   placement_mode="serverless",
>   secrets=(Secret(store="wandb", name="HF_TOKEN"),),
>   resources={"cpu": "1", "memory": "1Gi"},
> )
>
> with Session(defaults) as session:
>   sandbox = session.sandbox()
>   result = sandbox.exec([
>     "python", "-c",
>     "import os; assert os.environ.get('HF_TOKEN'); print('Secret is available')",
>   ]).result()
>   print(result.stdout)
> ```
>
> The Python client merges session defaults with per-sandbox `secrets` and ignores exact duplicates. If different references target the same environment variable, the client raises `ValueError` before it creates the sandbox. For the Python type signature, see the [Secret reference](https://docs.coreweave.com/products/sandboxes/client/ref/configuration/secret.md).

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
>
> const client = createSandboxClient({
>   apiKey: process.env.WANDB_API_KEY,
>   entity: process.env.WANDB_ENTITY,
> });
> const secrets = [{ store: "wandb", name: "HF_TOKEN" }];
>
> const result = await client.withSandbox(
>   async (sandbox) => sandbox.commands.run([
>     "python", "-c",
>     "import os; assert os.environ.get('HF_TOKEN'); print('Secret is available')",
>   ]),
>   { containerImage: "python:3.11", secrets },
> );
>
> console.log(result.stdout);
> ```

## Troubleshoot secret injection

If the sandbox fails to start with a secret reference, use the error text to check authentication, the selected team, and placement:

| Error text | What to check |
| - | - |
| `secret store "wandb" not found` | Check whether the client selected CoreWeave authentication. For serverless placement, pass Forge credentials through `AuthHeaders` in Python or `createSandboxClient` from `@coreweave/cwsandbox/wandb` in TypeScript, as shown in the examples. Setting `WANDB_API_KEY` alone doesn't switch a CoreWeave-authenticated client to Forge. You don't need to register a store. |
| `one or more W&B secrets not found` | Check the secret name and the selected Forge team. Set `WANDB_ENTITY` if the secret belongs to a team other than the API key's default entity, and verify that your Forge account can access it. |
| `entity not found` | Check `WANDB_ENTITY` for a typo and verify that the team exists and your Forge account can access it. |
| `no eligible runner is available on this replica right now; retry shortly` | If you selected a CKS runner with Forge authentication, this is an unsupported combination. Retrying won't enable it. Use Forge authentication with serverless placement for secret injection. For a serverless request, this error can indicate temporary runner unavailability. |

Forge secret injection isn't available for CKS placement, including when you set both a CoreWeave API access token and a Forge API key.
