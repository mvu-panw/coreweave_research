# Run long-running sandboxes

Source: https://docs.coreweave.com/products/sandboxes/long-running-sandboxes

# Run long-running sandboxes

> Configure sandbox lifetimes up to 30 days with Serverless or CKS placement.

CoreWeave sandboxes can run for up to 30 days (2,592,000 seconds) with either Serverless or CoreWeave Kubernetes Service (CKS) placement. Set the lifetime when you create the sandbox to give an agent, development environment, or batch workload enough time to finish.

This guide shows developers how to request a longer lifetime and administrators how to set a default for sandboxes on a CKS runner.

## Choose authentication

These examples run on serverless capacity unless a section specifies CKS. Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

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

## Choose a lifetime

The lifetime is an upper bound on how long the sandbox can run. The platform terminates it when the lifetime expires, even if work is still in progress. A workload that finishes or a sandbox that you stop can end sooner.

| Setting | Serverless | CKS |
| - | - | - |
| Per-sandbox lifetime | Set it in the software development kit (SDK) or sandbox create request. | Set it in the SDK or sandbox create request. |
| Runner-policy default | Managed by CoreWeave. | An administrator can set `constraints.lifecycle.default_lifetime_seconds` in the runner policy. |
| Maximum lifetime | 30 days. | 30 days, including on your own cluster. |

An explicit lifetime takes precedence over a runner-policy default. If you omit the lifetime, the platform uses the applicable policy default. If no positive default supplies a lifetime, the platform uses 10 minutes (600 seconds). Set the lifetime explicitly for long-running work instead of relying on a default.

The platform rejects requests above 30 days. A value of `0` doesn't mean unlimited runtime. A CKS policy can't raise the platform maximum.

You can't extend the lifetime after a sandbox starts. Choose enough time at creation, and plan to save your work before the deadline.

## Set the lifetime when creating a sandbox

Use `max_lifetime_seconds` in Python or `maxLifetimeSeconds` in TypeScript. The following examples request the full 30 days and print the sandbox ID so you can reconnect later. Choose the tab for your placement mode. CKS requires the CoreWeave credential and a configured runner. Replace `[RUNNER-ID]` with its ID:

> [tab] Serverless
>
> ```python Python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> sandbox = Sandbox.run(
>     "sleep", "infinity",
>     auth=AUTH,
>     placement_mode="serverless",
>     container_image="python:3.11",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=30 * 24 * 60 * 60,
> )
> sandbox.wait()
> print(sandbox.sandbox_id)
> ```
>
> ```typescript TypeScript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.run(["sleep", "infinity"], {
>   containerImage: "python:3.11",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 30 * 24 * 60 * 60,
> });
> console.log(sandbox.sandboxId);
> ```

> [tab] CKS
>
> ```python Python theme={"system"}
> from cwsandbox import AuthStrategy, Sandbox
>
> sandbox = Sandbox.run(
>     "sleep", "infinity",
>     auth=AuthStrategy.COREWEAVE_API_KEY,
>     placement_mode="cks",
>     runner_ids=["[RUNNER-ID]"],
>     container_image="python:3.11",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=30 * 24 * 60 * 60,
> )
> sandbox.wait()
> print(sandbox.sandbox_id)
> ```
>
> ```typescript TypeScript theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
>
> const client = createSandboxClientFromEnv();
> const sandbox = await client.run(["sleep", "infinity"], {
>   runnerIds: ["[RUNNER-ID]"],
>   containerImage: "python:3.11",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 30 * 24 * 60 * 60,
> });
> console.log(sandbox.sandboxId);
> ```

The script prints the sandbox ID. These examples keep the primary process alive with `sleep infinity` and leave the sandbox running after the script exits. When you finish using the sandbox, stop it.

The same lifetime is available through the other client interfaces:

| Interface | Lifetime configuration |
| - | - |
| Python SDK | `Sandbox.run(max_lifetime_seconds=2592000, ...)`. For shared client defaults, use `SandboxDefaults(max_lifetime_seconds=2592000)`. An explicit argument overrides the client default. |
| TypeScript SDK | Pass `maxLifetimeSeconds: 2592000` in the options to `client.run()`. |
| REST API | Set `spec.maxLifetimeSeconds` to `2592000` in the JSON body of `POST /v1/sandboxes`. |
| Compose file import | Set the top-level request field `maxLifetimeSeconds` to `2592000` on `POST /v1/sandboxes:createFromFile`. The lifetime is a request setting, not a Compose service property. |

For complete request formats, see the [API reference](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md) and [Create a sandbox from a Compose file](https://docs.coreweave.com/products/sandboxes/create-from-file.md). For Python client defaults, see [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md#max_lifetime_seconds).

## Set a default for a CKS runner

A runner-policy default applies to new sandboxes that don't request their own lifetime. Use this when workloads on a CKS runner should normally receive a longer lifetime. You need the `sandbox_admin` Identity and Access Management (IAM) action to edit the policy.

Policy updates replace the whole policy document. Don't submit the excerpt as a replacement for an existing policy: that would remove its other constraints.

1. In an interactive terminal, open the runner's current policy with the authenticated [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic):

   ```bash theme={"system"}
   cwic sandbox runner policy edit [RUNNER-ID]
   ```

2. Set `constraints.lifecycle.default_lifetime_seconds` to the desired number of seconds. The following YAML is an excerpt showing a 30-day default. Preserve the rest of the existing policy:

   ```yaml title="Runner policy excerpt" theme={"system"}
   constraints:
     lifecycle:
       default_lifetime_seconds: 2592000
   ```

3. Save and close the editor to submit the update. Retrieve the policy to verify the value:

   ```bash theme={"system"}
   cwic sandbox runner policy get [RUNNER-ID]
   ```

You can also update the policy through the managed-runner REST API. In JSON, the field is `policy.constraints.lifecycle.defaultLifetimeSeconds`. Follow [Update a policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy) for the full read, edit, and replace procedure.

The default applies to sandboxes created after the update. It doesn't extend running sandboxes. A sandbox can explicitly request a different lifetime up to 30 days. Don't add `max_lifetime_seconds` to the policy: the field was retired, and CoreWeave Intelligent CLI rejects a policy document that still contains it. The policy supplies a default, while the platform enforces the maximum.

## Keep working across client sessions

When a sandbox should outlive the Python script that launches it, create a standalone sandbox, as in the preceding examples. A `with Sandbox.run(...)` context stops the sandbox when the block exits, even if its configured lifetime is 30 days. A `Session` also manages cleanup of the sandboxes it owns. See [Cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md). In TypeScript, `client.run()` leaves the sandbox running, while `client.withSandbox()` stops it when its callback finishes.

To reconnect from another script, replace `[SANDBOX-ID]` with the ID printed at creation. Use the same credential as when you created the sandbox. Keep the same `sandbox_auth.py` or `sandbox-client.mts` configuration as at creation:

```python Python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

sandbox = Sandbox.from_id(
    "[SANDBOX-ID]",
    auth=AUTH,
).result()
result = sandbox.exec(["echo", "Connected"]).result()
print(result.stdout)
```

```typescript TypeScript theme={"system"}
import { client } from "./sandbox-client.mts";

const sandbox = await client.fromId("[SANDBOX-ID]");
const result = await sandbox.commands.run(["echo", "Connected"]);
console.log(result.stdout);
```

The command prints `Connected`. Reconnecting doesn't reset the lifetime. When you finish, stop the sandbox explicitly:

```python Python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

sandbox = Sandbox.from_id(
    "[SANDBOX-ID]",
    auth=AUTH,
).result()
sandbox.stop().result()
```

```typescript TypeScript theme={"system"}
import { client } from "./sandbox-client.mts";

const sandbox = await client.fromId("[SANDBOX-ID]");
await sandbox.stop();
```

## Plan for expiry

Save results or checkpoints outside the sandbox before its lifetime expires. If a workflow needs more than 30 days, create a replacement sandbox and resume from saved state. For supported storage and snapshot options, see [Sandbox volumes](https://docs.coreweave.com/products/sandboxes/volumes.md) and [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md).

The sandbox lifetime is separate from the timeout for a command or API request. Increasing `timeout_seconds` or `request_timeout_seconds` doesn't extend the sandbox lifetime. For the differences, see [Timeouts](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md#timeouts).
