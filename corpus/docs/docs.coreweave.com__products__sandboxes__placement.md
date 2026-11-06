# Sandbox placement and spillover

Source: https://docs.coreweave.com/products/sandboxes/placement

# Sandbox placement and spillover

> Compare serverless and CKS sandboxes, select where they run, and configure fallback between modes.

Placement determines which compute runs your sandbox. Serverless uses CoreWeave-managed compute. CoreWeave Kubernetes Service (CKS) placement uses compute in a CKS cluster in your organization. Spillover retries sandbox creation in the other mode when the initial placement fails.

## Compare placement modes

Choose a mode based on who manages the capacity and policy:

| | Serverless | CKS |
| - | - | - |
| Where sandboxes run | CoreWeave-managed compute | Compute in your CKS cluster |
| Who configures the policy | CoreWeave | Your administrators |
| Setup | Authenticate with a Forge or CoreWeave credential | Enable a runner on the cluster |
| Placement control | Platform-managed. You don't select a cluster. | Python can use any eligible cluster. Specify runner IDs to restrict placement. TypeScript requires runner IDs. |
| Resources | Choose CPU and memory for each sandbox | Choose CPU and memory within your cluster's policy |
| Credentials | Forge API key or CoreWeave API access token | CoreWeave API access token |
| When to use it | Run sandboxes without managing cluster capacity | Use your cluster's capacity and control resource and network policies |

Follow the [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md) or [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) to create your first sandbox.

## Choose and get credentials

Your credential determines which account owns the sandbox and is billed for its usage. Forge API keys support serverless sandboxes. CoreWeave API access tokens support both serverless and cluster sandboxes.

The environment variable and authentication strategy identify the credential, independently of the placement mode:

| Credential | Environment variable | Python strategy | Placement |
| - | - | - | - |
| Forge API key (W\&B authentication) | `WANDB_API_KEY` | `AuthStrategy.WANDB` | Serverless |
| CoreWeave API access token | `CWSANDBOX_API_KEY` | `AuthStrategy.COREWEAVE_API_KEY` | Serverless or CKS |

Choose one credential explicitly, even if both variables are set. Use the same account to create, reconnect to, list, and stop a sandbox.

> [tab] Forge API key
>
> Choose a Forge API key if you don't have a CoreWeave console account or prefer Forge billing:
>
> 1. Open [Forge API key settings](https://forge.coreweave.com/settings#apikeys). Sign in, or create an account through the same link.
> 2. Copy your API key and set it in the terminal where you run the client:
>
>    ```bash theme={"system"}
>    export WANDB_API_KEY="[WANDB-API-KEY]"
>    ```
>
> In Python, install `cwsandbox[wandb]` and select `auth=AuthStrategy.WANDB`. In TypeScript, use the `@coreweave/cwsandbox/wandb` entry point. Setting `WANDB_API_KEY` alone does not switch the Python client from its CoreWeave default. The [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md) includes complete examples.

> [tab] CoreWeave API access token
>
> Choose CoreWeave to use your CoreWeave organization's billing or run sandboxes on its cluster:
>
> 1. Ask your administrator to create or update an [Access Policy](https://console.coreweave.com/organization/iam/access-policies) granting you the **Sandbox User** role to run sandboxes. Administrators who enable runners and configure their policies need **Sandbox Admin**, which includes sandbox execution permissions. See [Create an access policy](https://docs.coreweave.com/security/iam/access-policies/manage.md#create-an-access-policy) and [Sandbox roles](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox).
> 2. On the [Tokens](https://console.coreweave.com/tokens) page, click **Create Token**, complete the token details, and click **Create**.
> 3. Copy the **Token Secret** and set it in the terminal where you run the client:
>
>    ```bash theme={"system"}
>    export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
>    ```
>
> If you can't create a token, ask your administrator for the **Access Token User** role. The token secret is shown only once. For more information, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
>
> In Python, select `AuthStrategy.COREWEAVE_API_KEY`. In TypeScript, import the client from `@coreweave/cwsandbox/node`.

## Select a placement mode

Both Python and TypeScript support serverless and CKS placement. Serverless is the default. The [`PlacementMode` reference](https://docs.coreweave.com/products/sandboxes/client/ref/workload/placement#placementmode) lists the supported mode values.

Both CKS examples read `CWSANDBOX_API_KEY`. Complete [credential setup](#coreweave-api-access-token). Then follow [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) to enable a runner or the [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md) to install the TypeScript client.

Select CKS placement explicitly:

> [tab] Python
>
> Use `placement_mode="cks"`. Add `runner_ids` to restrict placement to particular runners:
>
> ```python theme={"system"}
> from cwsandbox import AuthStrategy, Sandbox
>
> with Sandbox.run(
>     auth=AuthStrategy.COREWEAVE_API_KEY,
>     placement_mode="cks",
>     runner_ids=["[RUNNER-ID]"],
>     resources={"cpu": "1", "memory": "1Gi"},
> ) as sandbox:
>     print(sandbox.exec(["echo", "Hello!"]).result().stdout)
> ```
>
> Without `runner_ids`, CKS placement can use any eligible runner in your organization. For serverless, omit both fields or set `placement_mode="serverless"` without `runner_ids`.

> [tab] TypeScript
>
> Use the CoreWeave entry point and a nonempty `runnerIds` array to select CKS placement:
>
> ```typescript theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
>
> const client = createSandboxClientFromEnv();
> const result = await client.withSandbox(
>   async (sandbox) => sandbox.commands.run(["echo", "Hello!"]),
>   {
>     runnerIds: ["[RUNNER-ID]"],
>     resources: { cpu: "1", memory: "1Gi" },
>   },
> );
> console.log(result.stdout);
> ```
>
> Omit `runnerIds` for serverless placement.

## Spill over between modes

Automatic spillover is available in the Python client. The TypeScript client supports selecting either placement mode, but doesn't provide automatic spillover.

Spillover retries sandbox creation once in the alternate mode for eligible placement failures, such as unavailable capacity or no suitable runner. It doesn't move a running sandbox between modes.

Use a CoreWeave API access token for an organization with both serverless access and a configured CKS runner. A Forge API key alone doesn't provide CKS access.

To prefer CKS and fall back to serverless, set `placement_spillover="cks_then_serverless"`:

```python theme={"system"}
from cwsandbox import AuthStrategy, Sandbox

with Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    placement_spillover="cks_then_serverless",
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    print(sandbox.exec(["echo", "Hello!"]).result().stdout)
```

The example specifies CPU and memory for both attempts. Each mode applies its own policy, so a request must satisfy the policy of the mode where it runs.

Set `placement_spillover` to one of the following options to control fallback:

| Option | First attempt | Fallback | Constraints |
| - | - | - | - |
| `strict` (default) | The selected placement mode | None | Required when creating from a template or with `run_from_file()` |
| `cks_then_serverless` | CKS | Serverless | `placement_mode` must be `"cks"` or omitted |
| `serverless_then_cks` | Serverless | CKS | `placement_mode` must be `"serverless"` or omitted. Can't be combined with `runner_ids`. |

For the supported fallback values, see the [`PlacementSpillover` reference](https://docs.coreweave.com/products/sandboxes/client/ref/workload/placement#placementspillover). For resource and timeout settings, see [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md).
