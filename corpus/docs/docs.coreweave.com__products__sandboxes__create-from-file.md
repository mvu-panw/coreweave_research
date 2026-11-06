# Create a sandbox from a Compose file

Source: https://docs.coreweave.com/products/sandboxes/create-from-file

# Create a sandbox from a Compose file

> Start a multi-container sandbox by uploading a Docker Compose file to the sandbox API.

`POST /v1/sandboxes:createFromFile` starts a sandbox from an uploaded file. You send a file type and the file bytes. The sandbox gateway translates the document into a sandbox spec and runs the same create path as `POST /v1/sandboxes`.

Docker Compose (`SANDBOX_FILE_TYPE_COMPOSE`) is the only accepted file type. Every service in the file becomes a container in a single sandbox, and one service you name becomes the sandbox primary. The gateway doesn't store the file bytes. `GET /v1/sandboxes/{sandboxId}` returns the translated spec.

This guide covers Compose files that use prebuilt, pullable images with platform-controlled containers (`CONTROL_PLATFORM`, the default). Before you import an existing project, read [Compose support](#compose-support).

## Before you begin

Choose a credential from [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). Run the commands from one tab in Bash, then run the requests in the same shell. For serverless placement, use a credential for an account with serverless sandbox access. CoreWeave Kubernetes Service (CKS) placement requires a CoreWeave token with the **Sandbox User** role and a configured runner in the same organization.

> [tab] Forge API key
>
> Replace `WANDB_API_KEY_VALUE` with your API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="WANDB_API_KEY_VALUE"
> sandbox_headers=(-H "x-wandb-api-key: $WANDB_API_KEY")
> ```
>
> To use a Forge team other than your default, replace `WANDB_ENTITY` with the team name and append `-H "x-entity-id: WANDB_ENTITY"` to the array.

> [tab] CoreWeave API access token
>
> Replace `API_ACCESS_TOKEN` with your token:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="API_ACCESS_TOKEN"
> sandbox_headers=(-H "Authorization: Bearer $CWSANDBOX_API_KEY")
> ```

The requests in the Create the sandbox section use the sandbox runtime API at `https://api.cwsandbox.com` with serverless placement and the selected authentication header. The runner administration API uses `https://api.coreweave.com` and requires a CoreWeave token with the **Sandbox Admin** role.

## Request fields

The following fields configure the workflow in this guide.

| Field | Required | Description |
| - | - | - |
| `type` | Yes | Document kind. Use `SANDBOX_FILE_TYPE_COMPOSE`. |
| `contents` | Yes | The file bytes, base64-encoded in JSON. UTF-8, max 256 KiB. |
| `primaryService` | Conditional | Required with `CONTROL_PLATFORM`: names the service that becomes the sandbox primary. Must name a service in `contents`. Omit it with `CONTROL_CONTAINER_ENGINE`. |
| `imageOverrides` | No | Per-service image references. Keys must name services in the file. Use this to supply a pullable image for a service that would otherwise need a build. |
| `defaultResources` | Conditional | CPU and memory copied onto each service that omits `deploy.resources`. Per container, not a project budget. GPU here is rejected. Required when the file has more than one service and any service omits `deploy.resources`. |

The request also accepts `mode`, `maxLifetimeSeconds`, `tags`, `network`, `objectStorageAccess`, `annotations`, `runnerIds`, and `requestId`, with the same meaning as on `POST /v1/sandboxes`. `networkIds` returns `UNIMPLEMENTED`.

For CKS placement, choose the CoreWeave token tab and [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md). Change `mode` to `"SANDBOX_MODE_CKS"` in the `jq` object in the creation example. To target a specific runner, also add `runnerIds: ["RUNNER_ID"]`, replacing the placeholder with its ID. For the object storage prerequisites, see [Grant sandboxes access to AI Object Storage](https://docs.coreweave.com/products/sandboxes/operations/object-storage-access.md).

The endpoint also accepts `displayName`, `control`, image-pull credentials, and build options such as `buildContexts`, `buildContextObjects`, and `builderSizes`. Support depends on deployment enablement and the selected control mode. With `CONTROL_PLATFORM`, `imagePullCredentials` can authenticate pulls of prebuilt images, but can't be combined with services that still need a build. See the [request reference](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/create-sandbox-from-file.md) for field details and restrictions.

## Create the sandbox

Write a Compose file:

```bash title="compose.yaml" theme={"system"}
cat > compose.yaml <<'EOF'
services:
  helper:
    image: docker.io/library/busybox:1.36
    command: ["sleep", "3600"]
    expose: ["8080"]
    healthcheck:
      test: ["CMD", "true"]
      interval: 1s
      timeout: 1s
      retries: 3
  main:
    image: docker.io/library/busybox:1.36
    command: ["sleep", "3600"]
    environment:
      HELPER_HOST: helper
    depends_on:
      helper:
        condition: service_healthy
EOF
```

Post it with `contents` base64-encoded:

```bash title="Create a sandbox from compose.yaml" theme={"system"}
jq -n --rawfile yaml compose.yaml '{
  type: "SANDBOX_FILE_TYPE_COMPOSE",
  contents: ($yaml | @base64),
  primaryService: "main",
  mode: "SANDBOX_MODE_SERVERLESS",
  defaultResources: { requests: { cpu: "100m", memory: "128Mi" } },
  maxLifetimeSeconds: 3600,
  tags: ["from-file"]
}' | curl -sS -X POST https://api.cwsandbox.com/v1/sandboxes:createFromFile \
  "${sandbox_headers[@]}" \
  -H "Content-Type: application/json" \
  -d @-
```

The response is a sandbox in `STATE_CREATING`. Poll its `sandboxId` until it reaches `STATE_RUNNING` or a terminal state. Replace `SANDBOX_ID_VALUE` with that ID:

```bash title="Poll the sandbox" theme={"system"}
export SANDBOX_ID="SANDBOX_ID_VALUE"

curl -sS "https://api.cwsandbox.com/v1/sandboxes/$SANDBOX_ID" \
  "${sandbox_headers[@]}"
```

The returned spec has two containers, `main` marked primary, and `HELPER_HOST` still set to `helper`. Inside the sandbox, `helper` resolves to `127.0.0.1`.

To retry a create safely, send `requestId`. The same `requestId` with the same declared inputs returns the existing sandbox. The same `requestId` with different bytes, including a whitespace-only change, returns `ALREADY_EXISTS` with reason `CWSANDBOX_REQUEST_ID_CONFLICT`.

## Create a sandbox from TypeScript

The TypeScript software development kit (SDK) 1.0.0 supports Compose through `runFromFile()` and `withSandboxFromFile()`. Complete [TypeScript client setup](https://docs.coreweave.com/products/sandboxes/typescript-client.md#create-a-client) first and save the `sandbox-client.mts` file beside this script.

Use the `compose.yaml` file from [Create the sandbox](#create-the-sandbox). `withSandboxFromFile()` waits for the sandbox to be ready, runs the callback, and stops the sandbox after the callback returns or throws:

```typescript title="compose.mts" theme={"system"}
import { client } from "./sandbox-client.mjs";

await client.withSandboxFromFile(
  "./compose.yaml",
  async (sandbox) => {
    const result = await sandbox.commands.run(["echo", "Compose sandbox ready"]);
    console.log(result.stdout);
  },
  {
    primaryService: "main",
    defaultResources: { cpu: "100m", memory: "128Mi" },
    maxLifetimeSeconds: 3600,
  },
);
```

From the directory containing these files, run the script:

```bash theme={"system"}
npx --yes --package=tsx tsx compose.mts
```

The script prints `Compose sandbox ready` and stops the sandbox.

A string argument is always a file path. To supply inline YAML, pass UTF-8 bytes with `new TextEncoder().encode(yaml)`. The SDK sends bytes without reformatting them. Keep the file within the API's 256 KiB limit.

In version 1.0.0, `primaryService` is required and must name a service in the file. `defaultResources` supplies CPU and memory per service, not for the whole project. It doesn't support GPU resources. Use `imageOverrides` to supply pullable images for services that would otherwise need a build. The Compose support restrictions also apply to the SDK.

For manual lifecycle management, `runFromFile()` returns a sandbox handle. Stop it in a `finally` block. For both method signatures, see [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient). For the supported options, see [`SandboxRunFromFileOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxrunfromfileoptions).

## Compose support

All services share one Pod and one network namespace. Service names resolve to `127.0.0.1`, so values such as `HELPER_HOST: helper` and `API_BASE: http://main:8080` work without rewriting the file. The sandbox has no per-service IP addresses, bridge networks, or replicas.

Lifecycle depends on the control mode. With `CONTROL_PLATFORM`, the primary container follows
[Main command lifetime](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md#main-command-lifetime):
A successful exit completes the sandbox, and a nonzero exit can trigger automatic restarts.

With `CONTROL_CONTAINER_ENGINE`, the sandbox doesn't end solely because a service exits. An engine
failure fails the sandbox without a platform restart or retry.

With `CONTROL_PLATFORM`, the following behavior differs from Docker Compose:

* **Startup is serial**: Every non-primary service starts one after another, before the primary. Size `maxLifetimeSeconds` for that. A service that never becomes ready leaves the sandbox in `STATE_CREATING`.
* **`RUNNING` tracks the primary only**: A helper that crashes after start doesn't fail the sandbox.
* **`healthcheck` becomes an exec-only startup probe**: `test` must be a string, `CMD`, `CMD-SHELL`, or `NONE`, and durations must be whole seconds. When the probe exhausts its retries, the container is stopped rather than marked unhealthy.
* **Ports stay in the Pod**: `expose` and `ports` declare listen ports, but nothing is published externally.
* **Use prebuilt images for this workflow**: Supply a pullable image for every service through `image:` in the file or an entry in `imageOverrides`. Deployments with Compose builds enabled can build services that need `build:`. Without that support, these requests return `UNIMPLEMENTED`. For failed build logs, see [Read failed Compose build logs](https://docs.coreweave.com/products/sandboxes/reference/protos.md#read-failed-compose-build-logs).
* **`command` and `entrypoint` follow Docker's shell and exec forms**: Omit them to use the image defaults. Explicit `null` and `[]` are rejected.
* **GPUs are primary-only**, through `deploy.resources.reservations.devices` with the `gpu` capability and a positive integer count.
* **Names must be DNS-1123 labels** (`my-app`, not `My_App`), and can't use the reserved `cw-object-store-agent`, `cw-object-store-agent-restore`, or `dns-egress` prefixes.

### Unsupported keys

The document must be self-contained: the gateway doesn't read your disk and doesn't expand your environment. Unrecognized keys are rejected with the offending field path rather than ignored.

| Rejected | Notes |
| - | - |
| `$VAR` and `${VAR}` interpolation | Write `$$` for a literal `$`. |
| `include`, `extends`, `env_file` | Inline `environment` or `env` only. Bare keys and `null` values are also rejected. |
| `volumes`, `tmpfs`, `configs`, `secrets`, bind mounts | Named-volume projects can't be imported. |
| `restart`, `logging`, `profiles`, `stdin_open`, `tty`, `scale` | Not implemented on this runtime. |
| `network_mode`, `pid`, `ipc`, `extra_hosts`, named networks | One Pod, one namespace. |
| Host-to-container port mappings, bind addresses, port ranges, non-TCP protocols, duplicate ports across services | One TCP listen port per entry, unique across the sandbox. |
| `depends_on: service_completed_successfully`, or any `depends_on` targeting the primary | `service_healthy` and `service_started` can target non-primary services. `service_healthy` requires an effective healthcheck on the target. |
| Compose memory spellings (`512m`, `2g`, `512mb`) | Use Kubernetes quantities such as `512Mi` or `1Gi`. |
| Named `user` values (`nobody`) | Use a numeric user ID (UID). |

The gateway ignores `version`, project `name`, `labels`, and `x-*` extension keys. Don't rely on `labels` reaching the sandbox.

## Common errors

Field violations arrive as `BadRequest` details naming the path and the limit. They don't quote your document.

| Situation | Code and reason | Field |
| - | - | - |
| Omitted `type` | `INVALID_ARGUMENT`, `CWSANDBOX_INVALID_REQUEST` | `type` |
| Type other than Compose | `UNIMPLEMENTED`, `CWSANDBOX_NOT_IMPLEMENTED` | `type` |
| Omitted or unknown `primaryService` with `CONTROL_PLATFORM` | `INVALID_ARGUMENT`, `CWSANDBOX_INVALID_REQUEST` | `primary_service` |
| Service with neither `image:` nor `build:` | `INVALID_ARGUMENT`, `CWSANDBOX_INVALID_REQUEST` | `contents.services.<name>` |
| Service that still needs `build:` on a deployment without Compose build support | `UNIMPLEMENTED`, `CWSANDBOX_NOT_IMPLEMENTED` | `contents.services.<name>.build` |
| File over 256 KiB, or not a single UTF-8 YAML document | `INVALID_ARGUMENT`, `CWSANDBOX_INVALID_REQUEST` | `contents` |
| Unsupported Compose key | `INVALID_ARGUMENT`, `CWSANDBOX_INVALID_REQUEST` | The key path |
| Same `requestId`, different bytes | `ALREADY_EXISTS`, `CWSANDBOX_REQUEST_ID_CONFLICT` | None |

## See also

For related guidance, see the following pages:

* [Get started](https://docs.coreweave.com/products/sandboxes/get-started.md): create your first sandbox from a spec.
* [Runner administration API](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md): manage runners with a CoreWeave API access token and the **Sandbox Admin** role.
* [Sandbox environment variables](https://docs.coreweave.com/products/sandboxes/environment-variables.md): what the platform injects into every container.
