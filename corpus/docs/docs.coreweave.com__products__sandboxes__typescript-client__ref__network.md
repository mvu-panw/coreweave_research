# Networks and services

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network

# Networks and services

> TypeScript declarations for networks and services in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

Documentation comments include reviewed corrections. API signatures are unchanged.

## EgressRule

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { EgressRule } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * One create-time HTTPS (TCP 443) hostname grant.
 *
 * Exact names (`pypi.org`) or a single leftmost wildcard (`*.pypi.org`).
 * `"*"` is a policy ceiling, not a sandbox grant.
 */
interface EgressRule {
    readonly dnsName: string;
}
```

## Endpoint

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Endpoint } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type Endpoint = HttpsEndpoint | TlsPassthroughEndpoint;
```

Related types: [`HttpsEndpoint`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#httpsendpoint), [`TlsPassthroughEndpoint`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#tlspassthroughendpoint).

## EndpointAuth

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { EndpointAuth } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type EndpointAuth = "open" | "share_token";
```

## EndpointKind

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { EndpointKind } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type EndpointKind = "https" | "tls_passthrough";
```

## HttpsEndpoint

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { HttpsEndpoint } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface HttpsEndpoint {
    readonly auth: EndpointAuth;
    readonly kind: "https";
    /**
     * Server-side HTTPS request clock on this product endpoint (504 while the
     * sandbox stays alive). Not `timeoutMs` on `client.run` / RPCs. Omit or `0`
     * is the platform default (15s on serverless). The SDK requires a
     * non-negative integer; Aviato currently accepts `0` or `[15, 900]`.
     */
    readonly requestTimeoutSeconds?: number;
}
```

Related types: [`EndpointAuth`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#endpointauth).

## HttpsEndpointStatus

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { HttpsEndpointStatus } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Applied HTTPS product endpoint echoed on `serviceEndpoints`.
 *
 * Present when proto `requestTimeoutSeconds` is greater than 0. `url` may be
 * `""` when the API suppresses the hostname (for example a terminal Get).
 */
interface HttpsEndpointStatus {
    readonly auth: EndpointAuth;
    readonly kind: "https";
    readonly name: string;
    readonly port: number;
    readonly requestTimeoutSeconds: number;
    readonly url: string;
}
```

Related types: [`EndpointAuth`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#endpointauth).

## NetworkOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { NetworkOptions } from "@coreweave/cwsandbox";
```

To change a running sandbox's network rules, see [Dynamic network policies](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md). TypeScript SDK 1.0.0 doesn't expose `NetworkConfig` operations.

```typescript theme={"system"}
interface NetworkOptions {
    /**
     * When true, suppress declared and default destination egress grants.
     * Platform DNS and storage traffic are controlled separately. When omitted,
     * the fleet policy default applies.
     * Mutually exclusive with a non-empty `egress` list.
     */
    readonly denyEgress?: boolean;
    /**
     * When true, deny inbound traffic to CUSTOM-visibility ports. No-op when the
     * sandbox has no CUSTOM ports. Does not hide a public HTTPS endpoint.
     */
    readonly denyIngress?: boolean;
    /**
     * Initial hostnames the sandbox can reach over HTTPS (TCP 443).
     * This SDK version exposes these only as creation options.
     * Empty or omitted leaves the fleet policy default. A wildcard is one
     * leftmost label only (`*.pypi.org` does not include apex `pypi.org`).
     */
    readonly egress?: readonly EgressRule[];
}
```

Related types: [`EgressRule`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#egressrule).

## Service

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Service } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface Service {
    readonly endpoint?: Endpoint;
    readonly name?: string;
    readonly port: number;
    readonly protocol?: ServiceProtocol;
    readonly visibility?: ServiceVisibility;
}
```

Related types: [`Endpoint`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#endpoint), [`ServiceProtocol`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#serviceprotocol), [`ServiceVisibility`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#servicevisibility).

## ServiceProtocol

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ServiceProtocol } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type ServiceProtocol = "sctp" | "tcp" | "udp";
```

## ServiceUrl

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ServiceUrl } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ServiceUrl {
    readonly name: string;
    readonly port: number;
    readonly url: string;
}
```

## ServiceVisibility

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ServiceVisibility } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type ServiceVisibility = "custom" | "private" | "public";
```

## TlsPassthroughEndpoint

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { TlsPassthroughEndpoint } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * TLS passthrough product endpoint. The platform forwards TLS by SNI to the
 * container. `auth` and `requestTimeoutSeconds` must be omitted. The assigned
 * target is `host:port` on `serviceAddresses`. Use the host as TLS SNI. The
 * workload owns certs.
 */
interface TlsPassthroughEndpoint {
    readonly kind: "tls_passthrough";
}
```

## TlsPassthroughEndpointStatus

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { TlsPassthroughEndpointStatus } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
/**
 * Applied TLS passthrough endpoint echoed on `serviceAddresses`.
 *
 * `address` is `host:port`. Use the host as TLS SNI. The workload owns certs.
 */
interface TlsPassthroughEndpointStatus {
    readonly address: string;
    readonly kind: "tls_passthrough";
    readonly name: string;
    readonly port: number;
}
```
