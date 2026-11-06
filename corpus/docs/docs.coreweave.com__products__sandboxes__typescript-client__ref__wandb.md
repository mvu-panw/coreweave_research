# Forge client factories

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb

# Forge client factories

> TypeScript declarations for Forge client factories in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox/wandb` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## createSandboxClient

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
export declare function createSandboxClient(options?: WandbSandboxClientOptions): SandboxClient;
```

Related types: [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient), [`WandbSandboxClientOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb#wandbsandboxclientoptions).

## createSandboxClientFromEnv

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
export declare function createSandboxClientFromEnv(env?: WandbSandboxEnvironment): SandboxClient;
```

Related types: [`SandboxClient`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/client#sandboxclient), [`WandbSandboxEnvironment`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb#wandbsandboxenvironment).

## DEFAULT\_WANDB\_SANDBOX\_BASE\_URL

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import { DEFAULT_WANDB_SANDBOX_BASE_URL } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
export declare const DEFAULT_WANDB_SANDBOX_BASE_URL = "https://api.cwsandbox.com";
```

## toWandbMetadata

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import { toWandbMetadata } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
export declare function toWandbMetadata(options?: WandbAuthOptions): WandbMetadata;
```

Related types: [`WandbSandboxEnvironment`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb#wandbsandboxenvironment).

## WandbSandboxClientOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import type { WandbSandboxClientOptions } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
interface WandbSandboxClientOptions {
    readonly apiKey?: string;
    readonly baseUrl?: string;
    readonly entity?: string;
    readonly env?: WandbSandboxEnvironment;
    readonly netrcPath?: string;
    readonly project?: string;
}
```

Related types: [`WandbSandboxEnvironment`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/wandb#wandbsandboxenvironment).

## WandbSandboxEnvironment

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/wandb/index.d.ts).

```typescript theme={"system"}
import type { WandbSandboxEnvironment } from "@coreweave/cwsandbox/wandb";
```

```typescript theme={"system"}
interface WandbSandboxEnvironment extends Readonly<Record<string, EnvironmentValue>> {
    readonly WANDB_API_KEY?: string;
    readonly WANDB_ENTITY?: string;
    readonly WANDB_PROJECT?: string;
    readonly WANDB_SANDBOX_BASE_URL?: string;
}
```

## Supporting declarations

These types appear in the signatures above and are local to the declaration files. They are not named exports of this entry point.

### EnvironmentValue

```typescript theme={"system"}
type EnvironmentValue = string | undefined;
```

### WandbAuthOptions

```typescript theme={"system"}
interface WandbAuthOptions {
    readonly apiKey?: string;
    readonly entity?: string;
    readonly env?: WandbSandboxEnvironment;
    readonly netrcPath?: string;
    readonly project?: string;
}
```

### WandbMetadata

```typescript theme={"system"}
type WandbMetadata = Readonly<Record<string, string>>;
```
