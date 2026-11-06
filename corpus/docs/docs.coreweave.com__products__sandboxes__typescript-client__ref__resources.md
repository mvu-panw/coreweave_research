# Resources and secrets

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources

# Resources and secrets

> TypeScript declarations for resources and secrets in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

Documentation comments include reviewed corrections. API signatures are unchanged.

## ResourceOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ResourceOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/** CPU and memory only. GPU is not supported on this options type. */
type ResourceOptions = ResourceSpec | ResourceRequestsAndLimits;
```

Related types: [`ResourceRequestsAndLimits`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourcerequestsandlimits), [`ResourceSpec`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourcespec).

## ResourceRequestsAndLimits

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ResourceRequestsAndLimits } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ResourceRequestsAndLimits {
    readonly limits: ResourceSpec;
    readonly requests: ResourceSpec;
}
```

Related types: [`ResourceSpec`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#resourcespec).

## ResourceSpec

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ResourceSpec } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ResourceSpec {
    readonly cpu?: string;
    readonly memory?: string;
}
```

## SecretInput

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SecretInput } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * A secret reference resolved server-side and injected as an environment variable.
 *
 * Shape matches the Python SDK `Secret` (`store`, `name`, `field`, `env_var`), with
 * camelCase `envVar` for TypeScript. Values are never sent by the client.
 *
 * Use `store: "wandb"` for the authenticated Forge team; no organization
 * secret-store registration is required. Other store names must match a
 * registered store. When `envVar` is omitted it defaults to `name`. On the
 * wire, `name` is sent as proto `SecretMapping.path`.
 */
interface SecretInput {
    readonly envVar?: string;
    readonly field?: string;
    readonly name: string;
    readonly store: string;
}
```

## Secrets

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Secrets } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type Secrets = readonly SecretInput[];
```

Related types: [`SecretInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/resources#secretinput).
