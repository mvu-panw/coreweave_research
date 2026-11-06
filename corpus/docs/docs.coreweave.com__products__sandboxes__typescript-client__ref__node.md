# Node client factories

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/node

# Node client factories

> TypeScript declarations for Node client factories in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox/node` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## createSandboxClient

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import { createSandboxClient } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export declare function createSandboxClient(options: NodeSandboxClientOptions): SandboxClient;
```

Related types: [`NodeSandboxClientOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/node#nodesandboxclientoptions), [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient).

## createSandboxClientFromEnv

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export declare function createSandboxClientFromEnv(env?: CWSandboxEnvironment): SandboxClient;
```

Related types: [`CWSandboxEnvironment`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/node#cwsandboxenvironment), [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient).

## CWSandboxEnvironment

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import type { CWSandboxEnvironment } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export interface CWSandboxEnvironment extends Readonly<Record<string, EnvironmentValue>> {
    readonly CWSANDBOX_API_KEY?: string;
    readonly CWSANDBOX_BASE_URL?: string;
}
```

## DEFAULT\_BASE\_URL

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import { DEFAULT_BASE_URL } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export declare const DEFAULT_BASE_URL = "https://api.cwsandbox.com";
```

## DEFAULT\_CONTAINER\_IMAGE

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import { DEFAULT_CONTAINER_IMAGE } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export declare const DEFAULT_CONTAINER_IMAGE = "python:3.11";
```

## NodeSandboxClientOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/node/index.d.ts).

```typescript theme={"system"}
import type { NodeSandboxClientOptions } from "@coreweave/cwsandbox/node";
```

```typescript theme={"system"}
export interface NodeSandboxClientOptions {
    readonly apiKey: string;
    readonly baseUrl?: string;
    readonly dataPlaneMode?: DataPlaneMode;
}
```

Related types: [`DataPlaneMode`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#dataplanemode).

## Supporting declarations

These types appear in the signatures above and are local to the declaration files. They are not named exports of this entry point.

### EnvironmentValue

```typescript theme={"system"}
type EnvironmentValue = string | undefined;
```
