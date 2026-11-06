# Logs

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs

# Logs

> TypeScript declarations for logs in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## LogEntry

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogEntry } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogEntry {
    readonly line: string;
    readonly offset?: string;
    readonly sessionId?: string;
    readonly timestamp?: Date;
}
```

## LogEntryStream

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogEntryStream } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogEntryStream extends AsyncIterable<LogEntry> {
    readonly closed: boolean;
    readonly offset: string | undefined;
    readonly sessionId: string | undefined;
    cancel(options?: RequestOptions): Promise<void>;
    close(options?: RequestOptions): Promise<void>;
}
```

Related types: [`LogEntry`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logentry), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## LogRawChunk

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogRawChunk } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogRawChunk {
    readonly data: Uint8Array;
    readonly offset?: string;
    readonly sessionId?: string;
    readonly text: string;
    readonly timestamp?: Date;
}
```

## LogRawStream

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogRawStream } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogRawStream extends AsyncIterable<LogRawChunk> {
    readonly closed: boolean;
    readonly offset: string | undefined;
    readonly sessionId: string | undefined;
    cancel(options?: RequestOptions): Promise<void>;
    close(options?: RequestOptions): Promise<void>;
}
```

Related types: [`LogRawChunk`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#lograwchunk), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## LogReadOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogReadOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogReadOptions extends Omit<LogStreamOptions, "follow"> {
    readonly follow?: false;
}
```

Related types: [`LogStreamOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logstreamoptions).

## LogResumeCursor

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogResumeCursor } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogResumeCursor {
    readonly offset: bigint | number | string;
    readonly sessionId: string;
}
```

## LogStream

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogStream } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogStream extends AsyncIterable<string> {
    readonly closed: boolean;
    readonly offset: string | undefined;
    readonly sessionId: string | undefined;
    cancel(options?: RequestOptions): Promise<void>;
    close(options?: RequestOptions): Promise<void>;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## LogStreamMode

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogStreamMode } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type LogStreamMode = "entries" | "lines" | "raw";
```

## LogStreamOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { LogStreamOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface LogStreamOptions extends RequestOptions {
    readonly follow?: boolean;
    readonly resume?: LogResumeCursor;
    readonly sinceTime?: Date | string;
    readonly tailLines?: number;
    readonly timestamps?: boolean;
}
```

Related types: [`LogResumeCursor`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logresumecursor), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## SandboxLogs

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxLogs } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxLogs {
    read(options?: LogReadOptions): Promise<string[]>;
    stream(options?: LogStreamOptions): Promise<LogStream>;
    streamEntries(options?: LogStreamOptions): Promise<LogEntryStream>;
    streamRaw(options?: LogStreamOptions): Promise<LogRawStream>;
}
```

Related types: [`LogEntryStream`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logentrystream), [`LogRawStream`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#lograwstream), [`LogReadOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logreadoptions), [`LogStream`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logstream), [`LogStreamOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/logs#logstreamoptions).
