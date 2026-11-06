# Request options and defaults

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common

# Request options and defaults

> TypeScript declarations for request options and defaults in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## DataPlaneMode

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { DataPlaneMode } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Transport policy for exec, logs, and file operations. */
type DataPlaneMode = "auto" | "direct" | "gateway";
```

## DataPlaneOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { DataPlaneOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface DataPlaneOptions {
    /**
     * `auto` prefers a sandbox-scoped direct mTLS connection and falls back to
     * the gateway. `direct` requires that connection. Defaults to `auto`.
     */
    readonly dataPlaneMode?: DataPlaneMode;
}
```

Related types: [`DataPlaneMode`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplanemode).

## DEFAULT\_GRACEFUL\_SHUTDOWN\_SECONDS

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/defaults-DJSH7MC2.d.ts).

```typescript theme={"system"}
import { DEFAULT_GRACEFUL_SHUTDOWN_SECONDS } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Default stop grace period in seconds when `gracefulShutdownSeconds` is omitted. */
declare const DEFAULT_GRACEFUL_SHUTDOWN_SECONDS: 10;
```

## DEFAULT\_KEEP\_ALIVE\_COMMAND

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/defaults-DJSH7MC2.d.ts).

```typescript theme={"system"}
import { DEFAULT_KEEP_ALIVE_COMMAND } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
declare const DEFAULT_KEEP_ALIVE_COMMAND: readonly [
    "/bin/sh",
    "-lc",
    "trap 'exit 0' TERM INT; sleep infinity & wait"
];
```

## DEFAULT\_LIST\_ALL\_TIMEOUT\_MS

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/defaults-DJSH7MC2.d.ts).

```typescript theme={"system"}
import { DEFAULT_LIST_ALL_TIMEOUT_MS } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** Overall wall-clock budget for `listSandboxes()` / `listAll()` when `timeoutMs` is omitted. */
declare const DEFAULT_LIST_ALL_TIMEOUT_MS = 300000;
```

## DEFAULT\_SNAPSHOT\_TIMEOUT\_MS

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/defaults-DJSH7MC2.d.ts).

```typescript theme={"system"}
import { DEFAULT_SNAPSHOT_TIMEOUT_MS } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Public default `snapshot()` wait budget (Aviato archive timeout / Python
 * `DEFAULT_FSS_STOP_TIMEOUT_SECONDS`).
 */
declare const DEFAULT_SNAPSHOT_TIMEOUT_MS: 600000;
```

## Milliseconds

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Milliseconds } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type Milliseconds = number;
```

## RequestOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { RequestOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface RequestOptions {
    readonly signal?: AbortSignal;
    readonly timeoutMs?: Milliseconds;
}
```

Related types: [`Milliseconds`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#milliseconds).

## Seconds

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Seconds } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type Seconds = number;
```
