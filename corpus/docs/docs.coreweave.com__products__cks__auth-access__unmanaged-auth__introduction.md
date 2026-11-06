# Introduction to unmanaged authentication

Source: https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/introduction

# Introduction to unmanaged authentication

> Understand how CKS implements unmanaged authentication

In CKS, unmanaged authentication refers to the use of user identities and credentials that aren't managed within the CoreWeave cloud platform.

## API endpoint

CKS provides a Kubernetes API endpoint for implementing unmanaged authentication. This endpoint lets you authenticate with the Kubernetes API without relying on CoreWeave's [Managed Auth service](https://docs.coreweave.com/security/authn-authz/managed-auth/introduction.md).

Each public CKS cluster exposes a managed and an unmanaged endpoint. The unmanaged endpoint adds an `api.` prefix to the cluster's `apiServerEndpoint` and accepts unmanaged credentials such as OIDC, Service Account, and webhook tokens. Without the prefix, `kubectl` connects to the managed endpoint, which rejects those tokens. Private paths that pass TLS through to the API server, such as the [Traefik API proxy](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md#ingressroutetcp-and-kubernetes-api-proxy) and the Tailscale proxy in [Direct Auth](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md#direct-auth) mode, also accept unmanaged credentials. To learn how to construct and verify the unmanaged endpoint URL, see [Implement unmanaged authentication](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth.md).

Use this endpoint if you prefer to manage your own authentication mechanisms for CKS clusters, such as OIDC, Service Account tokens, and authentication webhooks. The endpoint provides flexibility if you have specific authentication requirements that can't be met through CoreWeave-managed authentication.

The unmanaged auth API endpoint works best in the following scenarios:

* **OIDC authentication**: Integrate standard OIDC IdPs for authentication to your CKS clusters.
* **Service Account authentication**: Use Kubernetes Service Account tokens to authenticate with your CKS clusters.
* **Custom authentication providers**: Integrate with enterprise identity systems not supported by standard OIDC.
* **Multi-factor authentication**: Implement custom MFA workflows.

> [!NOTE]
>
> Unmanaged auth can be configured on existing clusters without requiring cluster recreation.

## Customer-managed webhook authentication

If you use webhook authentication, you operate the webhook service. When its TLS certificate expires, every authentication request through that webhook fails. A sudden cluster-wide authentication outage with no configuration change is a strong signal that a webhook TLS certificate expired. Monitor the certificate and renew it before expiry.

To learn how to implement unmanaged auth, see [Implement unmanaged authentication](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth.md).
