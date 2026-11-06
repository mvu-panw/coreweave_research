# Sandboxes TypeScript client

Source: https://docs.coreweave.com/products/sandboxes/typescript-client

# Sandboxes TypeScript client

> Create sandboxes, run commands, and find the TypeScript software development kit (SDK) API.

The `@coreweave/cwsandbox` TypeScript client creates and manages CoreWeave sandboxes. Follow this guide to create a client, run a sandbox command, and handle SDK errors. The Sandboxes TypeScript examples and API reference use version 1.0.0. When following the guides, install this version.

## Prerequisites

Use Node.js 22 or later and an ECMAScript module (ESM) project. Save the examples as `.mts` files to run them with `tsx`.

Choose a credential from [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). The examples use serverless capacity. For CoreWeave Kubernetes Service (CKS) placement, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) and use a CoreWeave API access token with a non-empty `runnerIds` array.

Install the SDK:

```bash theme={"system"}
npm install @coreweave/cwsandbox@1.0.0
```

## Create a client

Choose the entry point for your credential. Both factories return a [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient). The root `@coreweave/cwsandbox` entry point exports types, constants, and errors. Create clients through `/wandb` or `/node`.

Save the code from your tab as a `sandbox-client.mts` file beside the other example files. It selects authentication and exports the client. The credential stays in your environment.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> ```typescript title="sandbox-client.mts" theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
>
> export const client = createSandboxClientFromEnv();
> ```
>
> To select a Forge team, set `WANDB_ENTITY`. For explicit options, see [Forge client factories](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb.md).

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your token:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```typescript title="sandbox-client.mts" theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
>
> export const client = createSandboxClientFromEnv();
> ```
>
> The factory also reads `CWSANDBOX_BASE_URL`, which defaults to `https://api.cwsandbox.com`. For explicit options, see [Node client factories](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/node.md).

## Run a command

For work that should stop when its callback finishes, use `withSandbox()`. It waits for sandbox readiness before calling the callback and stops the sandbox after the callback returns or throws.

```typescript title="hello.mts" theme={"system"}
import { client } from "./sandbox-client.mjs";

const result = await client.withSandbox(
  async (sandbox) => sandbox.commands.run(["echo", "Hello!"]),
  {
    containerImage: "python:3.11",
    resources: { cpu: "1", memory: "1Gi" },
  },
);

console.log(result.stdout);
```

Run the script:

```bash theme={"system"}
npx --yes --package=tsx tsx hello.mts
```

The script prints `Hello!` and stops the sandbox.

The `./sandbox-client.mjs` import resolves to the local `sandbox-client.mts` file when you run with `tsx` or compile with TypeScript.

`commands.run()` buffers standard output (stdout) and standard error (stderr) and returns a [`ProcessResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#processresult) with `exitCode`. For streaming output, use `commands.start()`.

To keep the sandbox across operations, use `client.create()`, then stop it in a `finally` block. See the [sandbox lifecycle reference](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes.md#sandbox).

## Handle errors

Use `isCWSandboxError()` to narrow an unknown error and inspect its `code`:

```typescript theme={"system"}
import { isCWSandboxError } from "@coreweave/cwsandbox";
import { client } from "./sandbox-client.mjs";

try {
  await client.withSandbox(async (sandbox) => {
    await sandbox.commands.run(["false"], { check: true });
  });
} catch (error) {
  if (isCWSandboxError(error)) {
    console.error(error.code, error.message);
  } else {
    throw error;
  }
}
```

With `check: true`, a nonzero command exit raises `CWSandboxExecutionError`. For the error hierarchy and available metadata, see [Errors](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/errors.md).

## API reference

The reference preserves the published declarations, including method overloads, parameter and return types, optional fields, and inherited types. SDK comments include reviewed corrections.

| Reference | Contents |
| - | - |
| [Client and discovery](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client.md) | Create, reconnect, list, clean up, and start from templates or Compose files. |
| [Sandboxes and lifecycle](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes.md) | Sandbox handles, start options, snapshots, and lifecycle states. |
| [Commands and terminals](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands.md) | Command execution, process handles, standard input (stdin), and interactive terminals. |
| [Files](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files.md) | Buffered and streaming file operations and mounted files. |
| [Logs](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs.md) | Read and stream sandbox logs. |
| [Networks and services](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network.md) | Network rules, services, and endpoints. |
| [Resources and secrets](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources.md) | Resource requests and limits and secret inputs. |
| [Request options and defaults](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common.md) | Timeouts, cancellation, data plane modes, and default constants. |
| [Errors](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/errors.md) | Error classes, codes, and backend reason constants. |
| [Node client factories](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/node.md) | CoreWeave token authentication and client construction. |
| [Forge client factories](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb.md) | Forge authentication and team selection. |

For a Compose example, see [Create a sandbox from TypeScript](https://docs.coreweave.com/products/sandboxes/create-from-file.md#create-a-sandbox-from-typescript).
