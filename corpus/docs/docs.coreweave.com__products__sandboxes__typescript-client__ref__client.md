# Client and discovery

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client

# Client and discovery

> TypeScript declarations for client and discovery in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## SandboxClient

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxClient } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Public interface returned by all CWSandbox client factories. */
interface SandboxClient {
    create(options?: SandboxRunOptions): Promise<Sandbox>;
    run(command: CommandInput, options?: SandboxRunOptions): Promise<Sandbox>;
    get(sandboxId: SandboxId, options?: RequestOptions): Promise<GetSandboxResult>;
    fromId(sandboxId: SandboxId, options?: FromIdOptions): Promise<Sandbox>;
    list(options?: ListSandboxesOptions): Promise<ListSandboxesResult>;
    listSandboxes(options?: SandboxListOptions): SandboxList;
    listAll(options?: SandboxListOptions): Promise<readonly Sandbox[]>;
    delete(sandboxId: SandboxId, options?: DeleteOptions): Promise<void>;
    getSnapshot(snapshotId: string, options?: RequestOptions): Promise<FileSystemSnapshotResult>;
    listSnapshots(options?: ListSnapshotsOptions): Promise<readonly FileSystemSnapshotResult[]>;
    deleteSnapshot(snapshotId: string, options?: DeleteSnapshotOptions): Promise<void>;
    withSandbox<TResult>(callback: WithSandboxCallback<TResult>, options?: SandboxRunOptions): Promise<TResult>;
    withSandbox<TResult>(command: CommandInput, callback: WithSandboxCallback<TResult>, options?: SandboxRunOptions): Promise<TResult>;
    /**
     * Starts from an organization template. Omitted options preserve template
     * values unless `containerImage` is supplied.
     *
     * Non-empty top-level collections replace template values. Empty top-level
     * collections/maps (`tags: []`, `services: []`, `annotations: {}`,
     * `runnerIds: []`) mean "no override," not "clear." `maxLifetimeSeconds: 0`
     * similarly preserves the template. There is no general clear-to-empty
     * operation on this surface.
     *
     * Once `containerImage` is supplied, the entire container list is replaced
     * with one `main` container. Omitted or empty container fields result in
     * empty/default values rather than inheritance.
     *
     * If creation returns an accepted sandbox but the readiness wait rejects, the
     * SDK best-effort stops it and rethrows the original readiness error.
     * `waitUntilRunning: false` returns immediately after accept with no
     * automatic cleanup.
     *
     * @param templateId Non-empty organization-scoped UUID. Format validation is
     *   performed by the backend.
     */
    runFromTemplate(templateId: string, options?: SandboxRunFromTemplateOptions): Promise<Sandbox>;
    /**
     * Starts from an organization template and always stops the sandbox after the
     * callback returns or throws. A callback error is rethrown; a cleanup failure
     * after a successful callback is thrown; a cleanup failure after a callback
     * or readiness error does not replace that error.
     *
     * Overlay semantics match `runFromTemplate`. The helper accepts the sandbox
     * first, then waits (unless `waitUntilRunning: false`) before the callback so
     * a readiness failure still `stop`s and the callback is not run.
     *
     * @param templateId Non-empty organization-scoped UUID. Format validation is
     *   performed by the backend.
     */
    withSandboxFromTemplate<TResult>(templateId: string, callback: WithSandboxCallback<TResult>, options?: SandboxRunFromTemplateOptions): Promise<TResult>;
    /**
     * Starts from a Compose file. `contents` is a filesystem path (`string`) or
     * raw file bytes (`Uint8Array`). A string is always opened as a path;
     * encode Compose text with `new TextEncoder().encode(...)`. Bytes are sent
     * as-is, so whitespace is part of the request. The file is capped at 256 KiB.
     *
     * Compose is pull-only. Images must already be pullable or supplied in
     * `imageOverrides`. Leftover `build:` is not implemented.
     * `primaryService` is required and must name a service in the file.
     *
     * This surface does not accept volumes, published services, secrets,
     * mounted files, or container/image overlays. Use `create` / `run` for
     * those. CPU and memory may be set with `defaultResources` (no GPU).
     *
     * If creation returns an accepted sandbox but the readiness wait rejects, the
     * SDK best-effort stops it and rethrows the original readiness error.
     * `waitUntilRunning: false` returns immediately after accept with no
     * automatic cleanup.
     */
    runFromFile(contents: SandboxFileContents, options: SandboxRunFromFileOptions): Promise<Sandbox>;
    /**
     * Starts from a Compose file and always stops the sandbox after the callback
     * returns or throws. A callback error is rethrown; a cleanup failure after a
     * successful callback is thrown; a cleanup failure after a callback or
     * readiness error does not replace that error.
     *
     * Overlay semantics match `runFromFile`. The helper accepts the sandbox
     * first, then waits (unless `waitUntilRunning: false`) before the callback so
     * a readiness failure still `stop`s and the callback is not run.
     */
    withSandboxFromFile<TResult>(contents: SandboxFileContents, callback: WithSandboxCallback<TResult>, options: SandboxRunFromFileOptions): Promise<TResult>;
}
```

Related types: [`CommandInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinput), [`DeleteOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#deleteoptions), [`DeleteSnapshotOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#deletesnapshotoptions), [`FileSystemSnapshotResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#filesystemsnapshotresult), [`FromIdOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#fromidoptions), [`GetSandboxResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#getsandboxresult), [`ListSandboxesOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsandboxesoptions), [`ListSandboxesResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsandboxesresult), [`ListSnapshotsOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsnapshotsoptions), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`Sandbox`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandbox), [`SandboxFileContents`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxfilecontents), [`SandboxId`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxid), [`SandboxList`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxlist), [`SandboxListOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxlistoptions), [`SandboxRunFromFileOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxrunfromfileoptions), [`SandboxRunFromTemplateOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxrunfromtemplateoptions), [`SandboxRunOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxrunoptions), [`WithSandboxCallback`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#withsandboxcallback).

## SandboxList

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import { SandboxList } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
declare class SandboxList implements AsyncIterable<Sandbox> {
    constructor(listPage: ListPage, toSandbox: ToSandbox, options?: SandboxListOptions);
    [Symbol.asyncIterator](): AsyncGenerator<Sandbox, void, undefined>;
    byPage(): AsyncIterable<readonly Sandbox[]>;
    collect(): Promise<readonly Sandbox[]>;
}
```

Related types: [`ListSandboxesOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsandboxesoptions), [`ListSandboxesResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#listsandboxesresult), [`Sandbox`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandbox), [`SandboxInfo`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxinfo), [`SandboxListOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxlistoptions).

## WithSandboxCallback

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { WithSandboxCallback } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type WithSandboxCallback<TResult> = (sandbox: Sandbox) => Promise<TResult> | TResult;
```

Related types: [`Sandbox`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandbox).

## Supporting declarations

These types appear in the signatures above and are local to the declaration files. They are not named exports of this entry point.

### ListPage

```typescript theme={"system"}
type ListPage = (options: ListSandboxesOptions) => Promise<ListSandboxesResult>;
```

### ToSandbox

```typescript theme={"system"}
type ToSandbox = (info: SandboxInfo) => Sandbox;
```
