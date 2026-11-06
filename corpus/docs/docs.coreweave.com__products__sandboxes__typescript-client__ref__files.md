# Files

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files

# Files

> TypeScript declarations for files in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## FileChunkSource

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileChunkSource } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Chunk source for `files.writeStream` (no Web/Node stream types in v1). */
type FileChunkSource = Uint8Array | AsyncIterable<Uint8Array> | Iterable<Uint8Array>;
```

## FileContent

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileContent } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileContent = string | Uint8Array;
```

## FileReadResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileReadResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileReadResult = Readonly<Record<string, Uint8Array>>;
```

## FileTextReadResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileTextReadResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileTextReadResult = Readonly<Record<string, string>>;
```

## FileWrite

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileWrite } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface FileWrite {
    readonly content: FileContent;
    readonly path: string;
}
```

Related types: [`FileContent`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filecontent).

## FileWrites

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { FileWrites } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type FileWrites = readonly FileWrite[] | Readonly<Record<string, FileContent>>;
```

Related types: [`FileContent`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filecontent), [`FileWrite`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filewrite).

## MountedFile

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { MountedFile } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface MountedFile {
    readonly content: MountedFileContent;
    readonly path: string;
}
```

Related types: [`MountedFileContent`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#mountedfilecontent).

## MountedFileContent

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { MountedFileContent } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type MountedFileContent = string | Uint8Array;
```

## MountedFiles

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { MountedFiles } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type MountedFiles = readonly MountedFile[] | Readonly<Record<string, MountedFileContent>>;
```

Related types: [`MountedFile`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#mountedfile), [`MountedFileContent`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#mountedfilecontent).

## SandboxFiles

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxFiles } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxFiles {
    read(path: string, options?: RequestOptions): Promise<Uint8Array>;
    read(paths: readonly string[], options?: RequestOptions): Promise<FileReadResult>;
    /**
     * Incrementally read a remote file as binary chunks. Prefer this over
     * buffered `read` for large files. Drain promptly to avoid stream backpressure.
     *
     * `timeoutMs` is one wall-clock budget for the integrity `stat` and the
     * file transfer combined. The clock starts when iteration begins.
     */
    readStream(path: string, options?: RequestOptions): AsyncIterable<Uint8Array>;
    readText(path: string, options?: RequestOptions): Promise<string>;
    readText(paths: readonly string[], options?: RequestOptions): Promise<FileTextReadResult>;
    write(path: string, content: FileContent, options?: RequestOptions): Promise<void>;
    write(files: FileWrites, options?: RequestOptions): Promise<void>;
    /**
     * Incrementally write a remote file from a buffer or chunk iterable.
     * A mid-stream failure or abort may leave a partial remote file.
     */
    writeStream(path: string, source: FileChunkSource, options?: RequestOptions): Promise<void>;
}
```

Related types: [`FileChunkSource`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filechunksource), [`FileContent`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filecontent), [`FileReadResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filereadresult), [`FileTextReadResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filetextreadresult), [`FileWrites`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/files#filewrites), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).
