# Share credentials across processes

Source: https://docs.coreweave.com/products/storage/object-storage/using-object-storage/share-credentials-across-processes

# Share credentials across processes

> Share one refreshable credential across every process on a host or Pod to avoid credential-request storms

When many processes on one host or Pod each initialize an S3 client, they don't share an in-memory credential cache. Each process exchanges an [OpenID Connect (OIDC) token](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) or a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md) for temporary Access Keys on its own, which can produce a burst of credential requests per refresh cycle.

To avoid credential-request storms, use the following approaches to let every process share a single refreshable credential:

| Approach | How processes get credentials | Best for |
| - | - | - |
| [CoreWeave Intelligent CLI credential process](#coreweave-intelligent-cli-credential-process) | Each process runs `cwic`, which returns credentials from a shared on-disk cache. | Tools that read `~/.aws/config` (AWS CLI, boto3, most SDKs), and container images you can add binaries to. |
| [IMDS credential server](#imds-credential-server) | Each process reads credentials from a local metadata endpoint served by one process. | Third-party tools and images that you can't add binaries to. |

## CoreWeave Intelligent CLI credential process

In the AWS config file (`~/.aws/config`), you specify a [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) command that the AWS client [runs](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html) to obtain credentials. Instead of passing your own script to `credential_process`, use a `cwic auth accesskey` command.

> [!NOTE]
>
> The `cwic auth accesskey` commands require CoreWeave Intelligent CLI version 1.37.0 or later. Install `cwic` by following the [installation instructions](https://github.com/coreweave/cwic#installation), then authenticate once with `cwic auth login`.

The following sections provide example configurations with the `cwic auth accesskey` commands to [exchange a CoreWeave API access token](#exchange-a-coreweave-api-access-token) and [an OIDC token](#exchange-an-oidc-token).

The `cwic auth accesskey` commands print credentials to `stdout` in the JSON format S3 clients expect, and they reuse a cached result until 80% of the credential lifetime has elapsed. The cache lives in `~/.cwic/cache` by default. Set `--cache-dir` or `$CWIC_CACHE_DIR` to change the location. A first successful request does not prove the client will refresh; test across at least one full credential lifetime before production.

When you omit the `--storage` flag, the CoreWeave Intelligent CLI uses the backend recorded for that organization by `cwic auth login`, and falls back to disk when none is recorded. On a workstation, you can [store the cache in your system keyring](#store-the-cache-in-your-system-keyring).

### Exchange a CoreWeave API access token

When your processes authenticate with a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md), use the `cwic auth accesskey api-token` command.

Add a line to your AWS config file (`~/.aws/config`) that invokes `cwic auth accesskey api-token`. The `cwic` command reads `COREWEAVE_API_TOKEN`, or the token stored by `cwic auth login`. Credentials are cached per token.

```ini title="Configuration for a CoreWeave API access token" highlight="4" theme={"system"}
[profile coreweave]
region = US-EAST-04A
endpoint_url = https://cwobject.com
credential_process = cwic auth accesskey api-token
s3 =
    addressing_style = virtual
```

> [!NOTE]
>
> These examples use the primary endpoint, `https://cwobject.com`. When your processes run inside a CoreWeave cluster, switch to the [Local Object Transport Accelerator (LOTA) endpoint](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) for better performance. Set `endpoint_url` to `http://cwlota.com`.

### Exchange an OIDC token

When your processes authenticate with [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), use the `cwic auth accesskey oidc` command. The command runs a command of your choosing to obtain an OIDC token, exchanges it for temporary credentials, and prints them.

Add a line to your AWS config file (`~/.aws/config`) that invokes `cwic auth accesskey oidc`.

Separate `cwic` flags from your token command with `--`. Everything after `--` is passed to that command unchanged. The `cwic` command accepts a raw token or a `client.authentication.k8s.io` ExecCredential JSON object with a `.status.token` field, which is what plugins such as `kubelogin` emit.

The `credential_process` value must be a single line. The `--org-id` flag is optional. When omitted, `cwic` uses the active organization from `cwic auth login`. Credentials are cached per organization and token command, so changing the token command gives you a separate cache entry. `cwic` caches the exchanged Access Keys. The OIDC token itself is managed by whatever produces it: the kubelet for a projected service account token or the plugin's own cache for `kubelogin`.

The token command depends on where the process runs: in a Kubernetes Pod or on a workstation.

Your **Org ID** is a short hexadecimal string (for example, `ab1cd2`). Find it on the [Settings page](https://console.coreweave.com/account/settings) of your Cloud Console account.

> [tab] In a Kubernetes Pod
>
> The token is the projected service account token that the cluster already mounts, so the token command reads it from disk. In CoreWeave Kubernetes Service (CKS), the [Pod Identity Webhook](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/pod-identity-webhook.md) projects a token scoped to the `https://coreweave.com/iam` audience:
>
> ```ini title="Configuration for OIDC token exchange in a Kubernetes Pod" highlight="4" theme={"system"}
> [profile coreweave]
> region = US-EAST-04A
> endpoint_url = http://cwlota.com
> credential_process = cwic auth accesskey oidc --org-id [ORG-ID] -- cat /var/run/secrets/cks.coreweave.com/serviceaccount/cks-pod-identity-token
> s3 =
>     addressing_style = virtual
> ```
>
> Replace `[ORG-ID]` with your CoreWeave organization ID. Because the kubelet refreshes the projected token in place, each `cwic` invocation that misses the cache reads the current token without any interactive step.

> [tab] On a workstation
>
> Complete an interactive OIDC login. The token command is often a credential plugin that obtains a token from your identity provider:
>
> ```ini title="Configuration for OIDC token exchange on a workstation" highlight="4" theme={"system"}
> [profile coreweave]
> region = US-EAST-04A
> endpoint_url = https://cwobject.com
> credential_process = cwic auth accesskey oidc --org-id [ORG-ID] --storage=keyring -- kubelogin get-token --oidc-issuer-url=[ISSUER-URL] --oidc-client-id=[CLIENT-ID] --oidc-extra-scope=openid,email,profile --oidc-pkce-method S256
> s3 =
>     addressing_style = virtual
> ```
>
> Replace `[ISSUER-URL]` and `[CLIENT-ID]` with your identity provider's values.

### Store the cache in your system keyring

On a workstation, `cwic` can hold its cache in the operating system credential store instead of the disk cache (the files under `~/.cwic/cache`). This keeps your CoreWeave API access token and the exchanged Access Keys out of plaintext on disk, at the cost of requiring a credential store that only a desktop session has. It's an opt-in alternative to the disk cache for local development.

> [!WARNING]
>
> Use the disk cache on servers, in containers, and in Pods. A keyring is only reachable from a desktop session, so `cwic` can't use it on a headless host or in a container.

`cwic` uses the native credential store on each platform:

| Platform | Credential store |
| - | - |
| macOS | Keychain, through Security.framework |
| Linux and BSD | freedesktop Secret Service, over D-Bus |
| Windows | Credential Manager |

Pass `--storage keyring` to an individual command:

```bash title="Use the keyring for a single command" theme={"system"}
cwic auth accesskey api-token --storage keyring
```

To avoid repeating the flag, record the choice for your organization at login. Later `cwic auth accesskey` commands follow the backend recorded for that organization, so your `credential_process` line needs no `--storage` flag:

```bash title="Record the keyring as your backend" theme={"system"}
cwic auth login --storage keyring
```

Entries are grouped in the credential store under the `coreweave.com:cwic` service prefix, so you can inspect or remove them with your platform's credential manager.

On macOS, keychain calls carry the identity of the `cwic` binary that makes them. After you upgrade `cwic`, macOS prompts you to re-allow access to entries the previous binary created. This continues until `cwic` ships signed and notarized with an Apple certificate.

## IMDS credential server

The [IMDS credential server](https://github.com/coreweave/imds-credential-server) implements the [EC2 instance metadata service (IMDSv2)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) interface. AWS SDKs read it through their [IMDS credential provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-imds-credentials.html), so pointing them at the server needs no client code changes. The server holds one refreshable credential and vends it to every process that queries the endpoint. Processes make no credential-exchange calls of their own: only the server refreshes, so an entire host or Pod converges on a handful of exchanges regardless of how many processes run.

Back the server with a CoreWeave credential source, such as a profile that uses the [CoreWeave Intelligent CLI credential process](#coreweave-intelligent-cli-credential-process) or the [direct token exchange](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md).

### Install the server

To run the server in a container, use the published image, `ghcr.io/coreweave/imds-credential-server`. Its entrypoint is the server binary, so the port is the only argument you pass. Pin a release tag rather than using `latest`:

```bash title="Pull the IMDS credential server container image" theme={"system"}
docker pull ghcr.io/coreweave/imds-credential-server:1.0.4
```

Alternatively, to run the server directly on a host, download the archive for your platform from the [releases page](https://github.com/coreweave/imds-credential-server/releases), extract it, and place the `imds-credential-server` binary on your `PATH`. Verify the install:

```bash title="Check the installed version" theme={"system"}
imds-credential-server version
```

### Run the server

Start the server with a port. It binds to localhost by default. Use the `HOST:PORT` form if you need a different address.

```bash title="Start the IMDS credential server" theme={"system"}
imds-credential-server 8081
```

### Point processes at the server

Set [`AWS_EC2_METADATA_SERVICE_ENDPOINT`](https://docs.aws.amazon.com/sdkref/latest/guide/feature-imds-credentials.html) for every process that should use the shared credential. Include the trailing slash, which the AWS CLI and some SDKs require.

```bash title="Use the local metadata endpoint" theme={"system"}
export AWS_EC2_METADATA_SERVICE_ENDPOINT=http://localhost:8081/
```

Do not also give those processes a `credential_process` profile, Container Credentials, or static Access Keys. Those sources rank above IMDS in the [credential provider chain](#overriding-and-changing-a-credential-source), so the process never queries the server.

Temporary Access Keys last 30 minutes. If requests succeed for the first few minutes and then return an invalid-key error, the client is most likely failing to refresh rather than failing to authenticate. Confirm that your client supports credential refresh against the metadata endpoint, and check the server logs for the refresh attempt. Testing across at least one full credential lifetime surfaces this before production does.

### Run the server as a sidecar

In Kubernetes, run the server as a sidecar instead of on the host. Containers in a Pod share a network namespace, so they still reach it at `http://localhost:8081/`. Give the sidecar a CoreWeave credential source, such as Container Credentials from the [Pod Identity Webhook](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/pod-identity-webhook.md) or a `cwic` profile. Application containers need only `AWS_EC2_METADATA_SERVICE_ENDPOINT`.

> [!WARNING]
>
> Give the Container Credentials variables to the sidecar only. The webhook injects them into every container in the Pod by default, and container credentials rank above the metadata endpoint in the [credential provider chain](#overriding-and-changing-a-credential-source). An application container that receives them exchanges credentials on its own and never queries the sidecar, which leaves the per-process requests exactly as they were.

Exclude your application containers from injection with the `caios.coreweave.com/skip-containers` Pod annotation, a comma-separated list of container names that applies to both `initContainers` and `containers`.

> [accordion] Example Pod spec with an IMDS credential server sidecar
>
> This Pod runs the credential server as a [native sidecar](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/), which is an init container with `restartPolicy: Always`. The sidecar starts before the application container and keeps running alongside it. The webhook injects the Container Credentials variables into the sidecar, which is the only container that exchanges credentials. The application container is excluded from injection and reads the shared credential from the sidecar instead.
>
> ```yaml title="imds-sidecar-pod.yaml" highlight={6-7,16-19,29-34} theme={"system"}
> apiVersion: v1
> kind: ServiceAccount
> metadata:
>   name: shard-loader
>   annotations:
>     # Activates the Pod Identity Webhook for Pods using this ServiceAccount.
>     caios.coreweave.com/inject: "true"
> ---
> apiVersion: v1
> kind: Pod
> metadata:
>   name: shard-loader
>   annotations:
>     # Keep the Container Credentials variables out of the application
>     # container so it falls through to the sidecar's metadata endpoint.
>     caios.coreweave.com/skip-containers: "loader"
> spec:
>   serviceAccountName: shard-loader
>   initContainers:
>   - name: imds
>     image: ghcr.io/coreweave/imds-credential-server:1.0.4
>     # restartPolicy: Always makes this a native sidecar: it starts before
>     # the application container and runs for the life of the Pod.
>     restartPolicy: Always
>     args: ["8081"]
>   containers:
>   - name: loader
>     image: [APPLICATION-IMAGE]
>     env:
>     # The trailing slash is required.
>     - name: AWS_EC2_METADATA_SERVICE_ENDPOINT
>       value: http://localhost:8081/
>     - name: AWS_REGION
>       value: US-EAST-04A
>     - name: AWS_ENDPOINT_URL_S3
>       value: http://cwlota.com
> ```
>
> Replace `[APPLICATION-IMAGE]` with your workload image. The sidecar image entrypoint is the server binary, so the port is the only argument it needs.
>
> Because the application container is skipped, it doesn't receive the `AWS_REGION` value the webhook would otherwise inject, so this spec sets `AWS_REGION` and `AWS_ENDPOINT_URL_S3` explicitly. The webhook does not inject an S3 endpoint. It uses the LOTA endpoint, `http://cwlota.com`, because the Pod runs inside a CoreWeave cluster.

## Overriding and changing a credential source

If a process never queries the metadata endpoint, or it keeps exchanging credentials on its own, a higher-ranked source is still configured. Configure **one** credential source per process.

To switch a process from `credential_process` to the container or metadata endpoint, change the profile, not only the environment. Point `AWS_PROFILE` at a profile without `credential_process`, or remove the setting from the profile in use.

### Credential source evaluation order

S3-compatible clients that use the AWS SDKs follow the [credential provider chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html), stopping at the first source that yields credentials. The exact chain varies by SDK, but the AWS CLI, boto3, and the AWS SDK for Java 2.x agree on the relative order of the sources this page uses:

| Order | Source | Where to set |
| - | - | - |
| 1 | Static credentials | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` |
| 2 | Web identity token (unused by CoreWeave) | `AWS_WEB_IDENTITY_TOKEN_FILE` |
| 3 | Shared config and credentials files | `credential_process` in `~/.aws/config` |
| 4 | Container credentials | `AWS_CONTAINER_CREDENTIALS_FULL_URI`, `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` |
| 5 | IMDS | `AWS_EC2_METADATA_SERVICE_ENDPOINT` |

In boto3 and the AWS CLI, naming a profile explicitly with `--profile` or `profile_name=` removes the environment-variable provider from the chain entirely, so the static credentials row no longer applies. Selecting a profile through the `AWS_PROFILE` environment variable does not have this effect.

`AWS_CONTAINER_CREDENTIALS_FULL_URI` and `AWS_EC2_METADATA_SERVICE_ENDPOINT` are both consulted *after* the shared config file. If the active profile sets `credential_process`, it wins, and setting either variable has no effect. Only the static credential variables in row 1 override the config file.
