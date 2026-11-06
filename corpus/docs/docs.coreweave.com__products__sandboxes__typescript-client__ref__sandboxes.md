# Sandboxes and lifecycle

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes

# Sandboxes and lifecycle

> TypeScript declarations for sandboxes and lifecycle in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## DeleteOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { DeleteOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface DeleteOptions extends RequestOptions {
    /**
     * When true, treat a missing sandbox (gRPC `NOT_FOUND` or trusted
     * `CWSANDBOX_SANDBOX_NOT_FOUND`) as success. Defaults to `false`.
     */
    readonly missingOk?: boolean;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## DeleteSnapshotOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { DeleteSnapshotOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface DeleteSnapshotOptions extends RequestOptions {
    /**
     * When true, treat a missing snapshot (gRPC `NOT_FOUND` or trusted
     * `CWSANDBOX_FSS_NOT_FOUND`) as success. Defaults to `false`.
     */
    readonly missingOk?: boolean;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## EnvironmentVariables

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { EnvironmentVariables } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type EnvironmentVariables = Readonly<Record<string, string>>;
```

## FileSystemSnapshotOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileSystemSnapshotOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Convenience single-mount scratch volume for snapshot/restore.
 *
 * Maps to a scratch volume named `workspace` mounted at `mountPath` on the
 * primary container. Snapshots archive that mount, not the whole container.
 * Mutually exclusive with `volumes`.
 */
interface FileSystemSnapshotOptions {
    /**
     * Absolute directory to mount (not `/`). Must satisfy Gateway mount-path
     * rules (canonical, ≤256 chars, not a reserved system prefix).
     */
    readonly mountPath: string;
    /** Kubernetes resource quantity (e.g. `"10Gi"`). Omit for the platform default. */
    readonly size?: string;
    /** Restore this snapshot at start. Omit or empty for an empty volume. */
    readonly restoreFromSnapshotId?: string;
}
```

## FileSystemSnapshotResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileSystemSnapshotResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Org-scoped file-system snapshot record from Get/List, and from `snapshot()` once READY. */
interface FileSystemSnapshotResult {
    readonly snapshotId: string;
    readonly state: FileSystemSnapshotState;
    readonly trigger: FileSystemSnapshotTrigger;
    /** Archive size when Get reports a safe integer; omitted otherwise. */
    readonly sizeBytes?: number;
    readonly stateReason?: string;
    readonly objectBucket?: string;
    readonly sourceSandboxId?: string;
    readonly sourceVolumeName?: string;
    readonly requestId?: string;
    readonly createdAt?: Date;
    readonly updatedAt?: Date;
    readonly completedAt?: Date;
}
```

Related types: [`FileSystemSnapshotState`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotstate), [`FileSystemSnapshotTrigger`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshottrigger).

## FileSystemSnapshotState

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileSystemSnapshotState } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileSystemSnapshotState = "creating" | "ready" | "failed" | "deleting" | "unspecified";
```

## FileSystemSnapshotTrigger

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileSystemSnapshotTrigger } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileSystemSnapshotTrigger = "unspecified" | "manual" | "on_delete";
```

## FromIdOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FromIdOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface FromIdOptions extends RequestOptions, DataPlaneOptions {
}
```

Related types: [`DataPlaneOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplaneoptions), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## GetSandboxResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { GetSandboxResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface GetSandboxResult extends SandboxMetadata {
    readonly status: SandboxStatus;
}
```

Related types: [`SandboxMetadata`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxmetadata), [`SandboxStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxstatus).

## ListSandboxesOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ListSandboxesOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ListSandboxesOptions extends RequestOptions {
    readonly pageSize?: number;
    readonly pageToken?: string;
    readonly runnerIds?: readonly string[];
    /**
     * When true, include terminal sandboxes (completed, failed, terminated).
     * Listing defaults to active-only.
     */
    readonly showTerminated?: boolean;
    readonly status?: SandboxStatus;
    readonly tags?: readonly SandboxTag[];
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`SandboxStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxstatus), [`SandboxTag`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxtag).

## ListSandboxesResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ListSandboxesResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ListSandboxesResult {
    readonly nextPageToken?: string;
    readonly sandboxes: readonly SandboxInfo[];
}
```

Related types: [`SandboxInfo`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxinfo).

## ListSnapshotsOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ListSnapshotsOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ListSnapshotsOptions extends RequestOptions {
    /** Client-side filter after a full collect. Not sent on the List RPC. */
    readonly sourceSandboxId?: string;
    /** Client-side filter after a full collect (Python `status`). */
    readonly state?: FileSystemSnapshotState;
}
```

Related types: [`FileSystemSnapshotState`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotstate), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## ObjectStoragePermission

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ObjectStoragePermission } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type ObjectStoragePermission = "read" | "read-write";
```

## Sandbox

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Sandbox } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Public instance interface returned by client factories. */
interface Sandbox {
    readonly commands: SandboxCommands;
    readonly files: SandboxFiles;
    readonly logs: SandboxLogs;
    readonly sandboxId: SandboxId;
    readonly dnsEgressNames: readonly string[] | undefined;
    readonly endpointShareToken?: string | undefined;
    readonly exitCode: number | undefined;
    readonly exposedPorts: readonly SandboxExposedPort[] | undefined;
    readonly resourceLimits: SandboxResourceSpec | undefined;
    readonly resourceRequests: SandboxResourceSpec | undefined;
    readonly runnerGroupId: string | undefined;
    readonly runnerId: string | undefined;
    readonly serviceAddresses: readonly TlsPassthroughEndpointStatus[] | undefined;
    readonly serviceEndpoints: readonly HttpsEndpointStatus[] | undefined;
    readonly serviceUrls: readonly ServiceUrl[] | undefined;
    readonly startedAt: Date | undefined;
    readonly status: SandboxStatus | undefined;
    readonly statusReason: string | undefined;
    exec(command: CommandInput, options?: ExecOptions): Promise<ProcessResult>;
    inspect(options?: RequestOptions): Promise<GetSandboxResult>;
    getStatus(options?: RequestOptions): Promise<SandboxStatus>;
    shell(options?: ShellOptions): Promise<TerminalSession>;
    wait(options?: WaitOptions): Promise<Sandbox>;
    /**
     * Snapshot the sandbox's scratch volume and wait until READY or FAILED.
     *
     * Returns the READY Get record (not only the ID). Default `timeoutMs` is 600s
     * (plus 5s internal observation slack). Snapshots outlive sandbox stop/delete;
     * call `client.deleteSnapshot` to remove them. Inspect without waiting with
     * `client.getSnapshot` / `client.listSnapshots`.
     *
     * One inherited scratch (for example after `runFromTemplate` with no volume
     * overlay) can infer the volume. Multiple inherited scratches are a backend
     * error.
     */
    snapshot(options?: RequestOptions): Promise<FileSystemSnapshotResult>;
    stop(options?: StopOptions): Promise<void>;
    delete(options?: DeleteOptions): Promise<void>;
    [Symbol.asyncDispose](): Promise<void>;
}
```

Related types: [`CommandInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinput), [`DeleteOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#deleteoptions), [`ExecOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#execoptions), [`FileSystemSnapshotResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotresult), [`GetSandboxResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#getsandboxresult), [`HttpsEndpointStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#httpsendpointstatus), [`ProcessResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#processresult), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`SandboxCommands`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#sandboxcommands), [`SandboxExposedPort`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxexposedport), [`SandboxFiles`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#sandboxfiles), [`SandboxId`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxid), [`SandboxLogs`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#sandboxlogs), [`SandboxResourceSpec`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxresourcespec), [`SandboxStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxstatus), [`ServiceUrl`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#serviceurl), [`ShellOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#shelloptions), [`StopOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#stopoptions), [`TerminalSession`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#terminalsession), [`TlsPassthroughEndpointStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#tlspassthroughendpointstatus), [`WaitOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#waitoptions).

## SandboxAnnotations

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxAnnotations } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type SandboxAnnotations = Readonly<Record<string, string>>;
```

## SandboxExposedPort

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxExposedPort } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxExposedPort {
    readonly name?: string;
    readonly port: number;
    readonly protocol?: ServiceProtocol;
}
```

Related types: [`ServiceProtocol`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#serviceprotocol).

## SandboxFileContents

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxFileContents } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Filesystem path (`string`) or raw file bytes. A string is always a path. */
type SandboxFileContents = string | Uint8Array;
```

## SandboxFileType

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxFileType } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Document type for `runFromFile`. Compose is pull-only. */
type SandboxFileType = "compose";
```

## SandboxId

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxId } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type SandboxId = string;
```

## SandboxInfo

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxInfo } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxInfo extends SandboxMetadata {
    readonly status: SandboxStatus;
}
```

Related types: [`SandboxMetadata`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxmetadata), [`SandboxStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxstatus).

## SandboxListOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxListOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Options for `SandboxClient.listSandboxes()` and `SandboxClient.listAll()`.
 *
 * Omits `pageToken` because the helper owns pagination. `timeoutMs` is a
 * wall-clock budget across all pages (default 300s), not a per-page RPC timeout.
 */
type SandboxListOptions = Omit<ListSandboxesOptions, "pageToken"> & DataPlaneOptions;
```

Related types: [`DataPlaneOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplaneoptions), [`ListSandboxesOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsandboxesoptions).

## SandboxMetadata

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxMetadata } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxMetadata {
    readonly dnsEgressNames?: readonly string[];
    readonly exitCode?: number;
    readonly exposedPorts?: readonly SandboxExposedPort[];
    readonly resourceLimits?: SandboxResourceSpec;
    readonly resourceRequests?: SandboxResourceSpec;
    readonly runnerGroupId?: string;
    readonly runnerId?: string;
    readonly sandboxId: SandboxId;
    readonly serviceAddresses?: readonly TlsPassthroughEndpointStatus[];
    readonly serviceEndpoints?: readonly HttpsEndpointStatus[];
    readonly serviceUrls?: readonly ServiceUrl[];
    readonly startedAt?: Date;
    readonly status?: SandboxStatus;
    readonly statusReason?: string;
}
```

Related types: [`HttpsEndpointStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#httpsendpointstatus), [`SandboxExposedPort`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxexposedport), [`SandboxId`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxid), [`SandboxResourceSpec`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxresourcespec), [`SandboxStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxstatus), [`ServiceUrl`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#serviceurl), [`TlsPassthroughEndpointStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#tlspassthroughendpointstatus).

## SandboxObjectStorageAccess

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxObjectStorageAccess } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Temporary object-storage credentials for the sandbox (OSA / CAIOS).
 * Independent of file-system snapshots.
 */
interface SandboxObjectStorageAccess {
    readonly buckets: readonly string[];
    readonly permission: ObjectStoragePermission;
    /**
     * Optional prefix that scopes the minted credential. Must satisfy Gateway
     * OSA prefix rules when set (alphanumeric start, trailing `/`, no `..`).
     */
    readonly objectPrefix?: string;
}
```

Related types: [`ObjectStoragePermission`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#objectstoragepermission).

## SandboxResourceSpec

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxResourceSpec } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type SandboxResourceSpec = ResourceSpec;
```

Related types: [`ResourceSpec`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourcespec).

## SandboxRunFromFileOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxRunFromFileOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Options for `runFromFile`. Volumes, published services, secrets, mounted
 * files, and container/image overlays are not fields here; those callers use
 * `create` / `run`.
 */
interface SandboxRunFromFileOptions extends RequestOptions, DataPlaneOptions {
    /**
     * Compose service that is the sandbox primary. Required. Must name a
     * service in `contents`.
     */
    readonly primaryService: string;
    /** Document type. Defaults to `"compose"`. */
    readonly fileType?: SandboxFileType;
    /**
     * Per-service pullable image refs. Keys must be services in `contents`.
     * Use this when a service would otherwise need a build.
     */
    readonly imageOverrides?: Readonly<Record<string, string>>;
    /**
     * CPU and memory copied onto each service that omitted deploy resources.
     * Per container, not a project budget. GPU is not supported.
     */
    readonly defaultResources?: ResourceOptions;
    readonly annotations?: SandboxAnnotations;
    readonly maxLifetimeSeconds?: Seconds;
    readonly network?: NetworkOptions;
    readonly objectStorageAccess?: SandboxObjectStorageAccess;
    /**
     * Non-empty input pins CKS runners. There is no `placementMode` option;
     * CKS placement is only via non-empty `runnerIds`.
     */
    readonly runnerIds?: readonly string[];
    readonly tags?: readonly SandboxTag[];
    /**
     * Wait for the sandbox to reach `running` before resolving creation helpers.
     *
     * Defaults to `true`. Set to `false` only when you need a handle as soon as
     * the backend accepts the start request.
     */
    readonly waitUntilRunning?: boolean;
}
```

Related types: [`DataPlaneOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplaneoptions), [`NetworkOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#networkoptions), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`ResourceOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourceoptions), [`SandboxAnnotations`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxannotations), [`SandboxFileType`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxfiletype), [`SandboxObjectStorageAccess`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxobjectstorageaccess), [`SandboxTag`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxtag), [`Seconds`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#seconds).

## SandboxRunFromTemplateOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxRunFromTemplateOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Overlays for `runFromTemplate`. Omitted options preserve template values
 * unless `containerImage` is supplied.
 *
 * Replacement is per field, not a merge. Empty top-level maps/lists mean
 * inherit, not clear, except `network: {}`, which replaces the template
 * network. See each property.
 */
interface SandboxRunFromTemplateOptions extends RequestOptions, DataPlaneOptions {
    /**
     * Non-empty input replaces the complete template map; it does not merge
     * keys. Empty `{}` means inherit, not clear.
     */
    readonly annotations?: SandboxAnnotations;
    /**
     * Replaces the complete template container list with one `main` container.
     * All omitted container settings are cleared, including
     * `imagePullCredentials`. A template using private-image credentials works
     * only while its container is inherited unchanged. Replacement credentials
     * are not supported.
     */
    readonly containerImage?: string;
    /**
     * Requires `containerImage`. When replacing the container, omitted values
     * are not inherited from the template.
     */
    readonly command?: CommandInput;
    /**
     * A non-empty map becomes the replacement environment. Omitted or empty
     * produces an empty replacement environment when `containerImage` is set.
     * Empty `{}` without `containerImage` means inherit.
     */
    readonly environmentVariables?: EnvironmentVariables;
    /**
     * Requires `containerImage`. When replacing the container, supplying this
     * replaces spec volumes and the replacement container's mounts. Omitting it
     * keeps template volumes and drops mounts on the new container. Inherited
     * registered volumes that lose their mounts are rejected by Gateway;
     * inherited scratch volumes can remain unmounted.
     */
    readonly fileSystemSnapshot?: FileSystemSnapshotOptions;
    /**
     * Requires `containerImage`. When replacing the container, supplying this
     * replaces spec volumes and the replacement container's mounts. Omitting it
     * keeps template volumes and drops mounts on the new container. Inherited
     * registered volumes that lose their mounts are rejected by Gateway;
     * inherited scratch volumes can remain unmounted. `volumes: []` is rejected.
     */
    readonly volumes?: readonly ScratchVolumeOptions[];
    /**
     * Non-zero replaces the template scalar. `0` means inherit, not clear.
     */
    readonly maxLifetimeSeconds?: Seconds;
    /**
     * Requires `containerImage`. When replacing the container, omitted values
     * are not inherited from the template.
     */
    readonly mountedFiles?: MountedFiles;
    /**
     * Any defined `network`, including `{}`, replaces the complete template
     * network. Omitted members are not inherited.
     */
    readonly network?: NetworkOptions;
    /**
     * Requires `containerImage`. When replacing the container, omitted values
     * are not inherited from the template. CPU and memory only; GPU is not
     * supported on `ResourceOptions`.
     */
    readonly resources?: ResourceOptions;
    /**
     * Non-empty input replaces the complete list. Empty `[]` means inherit,
     * not clear. Co-emits CKS mode on the wire. There is no `placementMode`
     * option; CKS placement is only via non-empty `runnerIds`.
     */
    readonly runnerIds?: readonly string[];
    /**
     * Non-empty input replaces the complete list. Empty `[]` means inherit,
     * not clear.
     */
    readonly services?: readonly Service[];
    /**
     * Requires `containerImage`. When replacing the container, omitted values
     * are not inherited from the template. `secrets: []` still requires
     * `containerImage`.
     */
    readonly secrets?: Secrets;
    /**
     * Non-empty input replaces the complete list. Empty `[]` means inherit,
     * not clear.
     */
    readonly tags?: readonly SandboxTag[];
    /**
     * Wait for the sandbox to reach `running` before resolving creation helpers.
     *
     * Defaults to `true`. Set to `false` only when you need a handle as soon as
     * the backend accepts the start request.
     */
    readonly waitUntilRunning?: boolean;
}
```

Related types: [`CommandInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinput), [`DataPlaneOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplaneoptions), [`EnvironmentVariables`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#environmentvariables), [`FileSystemSnapshotOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotoptions), [`MountedFiles`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#mountedfiles), [`NetworkOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#networkoptions), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`ResourceOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourceoptions), [`SandboxAnnotations`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxannotations), [`SandboxTag`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxtag), [`ScratchVolumeOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#scratchvolumeoptions), [`Seconds`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#seconds), [`Secrets`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#secrets), [`Service`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#service).

## SandboxRunOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxRunOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxRunOptions extends RequestOptions, DataPlaneOptions {
    readonly annotations?: SandboxAnnotations;
    readonly containerImage?: string;
    readonly environmentVariables?: EnvironmentVariables;
    readonly fileSystemSnapshot?: FileSystemSnapshotOptions;
    /**
     * Named scratch volumes. Mutually exclusive with `fileSystemSnapshot`.
     * Must be non-empty. `snapshot()` fails client-side when this process
     * created more than one scratch.
     */
    readonly volumes?: readonly ScratchVolumeOptions[];
    readonly maxLifetimeSeconds?: Seconds;
    readonly mountedFiles?: MountedFiles;
    readonly network?: NetworkOptions;
    readonly objectStorageAccess?: SandboxObjectStorageAccess;
    readonly resources?: ResourceOptions;
    readonly runnerIds?: readonly string[];
    readonly services?: readonly Service[];
    /**
     * Secret-store references to resolve server-side and inject as environment variables.
     *
     * Do not put secret values in `environmentVariables`, annotations, or tags.
     */
    readonly secrets?: Secrets;
    readonly tags?: readonly SandboxTag[];
    /**
     * Wait for the sandbox to reach `running` before resolving creation helpers.
     *
     * Defaults to `true`. Set to `false` only when you need a handle as soon as
     * the backend accepts the start request.
     */
    readonly waitUntilRunning?: boolean;
}
```

Related types: [`DataPlaneOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplaneoptions), [`EnvironmentVariables`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#environmentvariables), [`FileSystemSnapshotOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotoptions), [`MountedFiles`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#mountedfiles), [`NetworkOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#networkoptions), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`ResourceOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourceoptions), [`SandboxAnnotations`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxannotations), [`SandboxObjectStorageAccess`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxobjectstorageaccess), [`SandboxTag`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxtag), [`ScratchVolumeOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#scratchvolumeoptions), [`Seconds`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#seconds), [`Secrets`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#secrets), [`Service`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#service).

## SandboxStatus

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxStatus } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type SandboxStatus = "pending" | "creating" | "running" | "paused" | "terminating" | "completed" | "failed" | "terminated" | "unspecified";
```

## SandboxTag

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxTag } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type SandboxTag = string;
```

## ScratchVolumeOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ScratchVolumeOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Named scratch volume for snapshot/restore. Prefer `volumes` when the sandbox
 * needs a non-`workspace` name or more than one mount.
 *
 * Snapshots archive these mounts, not the whole container. `snapshot()` cannot
 * choose among multiple scratches created in this process.
 */
interface ScratchVolumeOptions {
    /** Unique name within the sandbox (Gateway: 1-63 `[A-Za-z0-9_-]`). */
    readonly name: string;
    /**
     * Absolute directory to mount (not `/`). Must satisfy Gateway mount-path
     * rules (canonical, ≤256 chars, not a reserved system prefix).
     */
    readonly mountPath: string;
    /** Kubernetes resource quantity (e.g. `"10Gi"`). Omit for the platform default. */
    readonly size?: string;
    /** Restore this snapshot at start. Omit or empty for an empty volume. */
    readonly restoreFromSnapshotId?: string;
}
```

## StartSandboxResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { StartSandboxResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface StartSandboxResult extends SandboxMetadata {
    /**
     * Create-only share token for `auth: "share_token"` HTTPS URLs. Get, list,
     * and `fromId` omit it. A live handle keeps a create-time value across
     * `wait` / `inspect`.
     */
    readonly endpointShareToken?: string;
}
```

Related types: [`SandboxMetadata`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxmetadata).

## StopOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { StopOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface StopOptions extends RequestOptions {
    /**
     * Seconds to wait for a graceful shutdown. Defaults to 10. Pass `0` to kill
     * immediately. Standalone `delete()` does not use this default.
     */
    readonly gracefulShutdownSeconds?: Seconds;
    /**
     * When true, treat a missing sandbox (gRPC `NOT_FOUND` or trusted
     * `CWSANDBOX_SANDBOX_NOT_FOUND`) as success. Defaults to `false`.
     */
    readonly missingOk?: boolean;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`Seconds`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#seconds).

## WaitOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { WaitOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface WaitOptions extends RequestOptions {
    readonly targetStatus?: WaitTargetStatus;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`WaitTargetStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#waittargetstatus).

## WaitTargetStatus

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { WaitTargetStatus } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type WaitTargetStatus = "completed" | "paused" | "running" | "terminal";
```
