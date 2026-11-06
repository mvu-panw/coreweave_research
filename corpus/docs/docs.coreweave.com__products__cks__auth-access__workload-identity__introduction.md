# Introduction to OIDC Workload Identity for CKS

Source: https://docs.coreweave.com/products/cks/auth-access/workload-identity/introduction

# Introduction to OIDC Workload Identity for CKS

> OIDC Workload Identity enables CKS workloads to authenticate to cloud services without static credentials

OIDC Workload Identity for CoreWeave Kubernetes Service (CKS) lets your workloads authenticate with services across multiple clouds using the [OpenID Connect (OIDC) protocol](https://openid.net/developers/how-connect-works/). OIDC addresses a common challenge for multi-cloud AI and Kubernetes users: it establishes identity and access management between CKS workloads and external services without the operational risks of managing long-lived credentials.

## When to use OIDC Workload Identity

OIDC Workload Identity helps applications that need to authenticate with multiple cloud providers or external services. Rather than managing static API keys or service account credentials across different environments, your workloads can use short-lived tokens that Kubernetes issues and rotates automatically. This removes credential distribution and rotation overhead while enabling fine-grained access control through each provider's built-in IAM systems.

This approach works well for both public and private clusters, because the OIDC metadata endpoints don't expose sensitive cluster information.

## How OIDC works

OIDC (OpenID Connect) is an [industry-standard protocol](https://openid.net/developers/how-connect-works/) for federated identity, widely supported by public cloud service providers (CSPs) and many SaaS platforms. On CoreWeave, each CKS cluster acts as an OIDC identity provider (IdP) that issues secure tokens to workloads running under specific Kubernetes Service Accounts. These tokens let workloads authenticate to any external service (including AWS, GCP, and many SaaS tools) configured to trust the CKS cluster's OIDC identity. This approach eliminates the need to manually generate, distribute, or rotate secrets.

### Your CKS cluster as a trusted OIDC IdP

Every CKS cluster publishes a public OIDC Document Discovery URL (such as `https://oidc.cks.coreweave.com/id/[CLUSTER-ID]`), where external services can discover identity metadata and cryptographic keys. This lets you configure AWS, GCP, or other services to recognize your cluster as an identity authority. The discovery URL serves the standard `/.well-known/openid-configuration` and JWKS (`/openid/v1/jwks`) endpoints.

You can find your cluster's issuer URL in any of these places:

* **Cloud Console**: open the cluster's **Overview** panel on the [Clusters](https://console.coreweave.com/clusters) page.
* **CKS API**: read the cluster's `serviceAccountIssuer` (`oidc.issuerUrl`) value.
* **Terraform**: read the `oidc` issuer attribute from the `coreweave_cks_cluster` data source.

> [!TIP]
>
> For step-by-step instructions on retrieving the issuer URL, see [Get the OIDC issuer URL from CKS](https://docs.coreweave.com/products/cks/auth-access/workload-identity/oidc-gcp.md#get-the-oidc-issuer-url-from-cks).

### Service account tokens

Workloads running in CKS acquire their identity through Kubernetes Service Account tokens that the cluster signs and issues. When configured for OIDC Workload Identity, these tokens contain claims that external CSPs recognize:

| Claim | Description | Example |
| - | - | - |
| `iss` | The issuer, which identifies the CKS cluster that signed the token. | `https://oidc.cks.coreweave.com/id/[CLUSTER-ID]` |
| `sub` | The subject, which identifies the Kubernetes ServiceAccount in `system:serviceaccount:<namespace>:<name>` form. | `system:serviceaccount:foo:bar` |
| `aud` | The audience the token is intended for. You set this per projected token, typically to the external provider that validates it. | `//iam.googleapis.com/projects/.../providers/k8s-provider` |
| `kubernetes.io` | A nested claim that carries the ServiceAccount namespace and name (and pod metadata). Providers can map these values to identity attributes. | `serviceaccount/namespace: foo`, `serviceaccount/name: bar` |
| `exp`, `iat` | Standard expiry and issued-at timestamps. Kubernetes keeps these tokens short-lived and rotates them automatically. | N/A |

To enforce least privilege, write IAM policies in the external provider that reference these claims so that only a specific ServiceAccount can assume a given role or principal. For example:

* In GCP, map `sub` and the `kubernetes.io` namespace and name claims to Workload Identity Pool attributes, then bind a service account to the `foo/bar` combination. See [Access Google Cloud Storage from CKS pods](https://docs.coreweave.com/products/cks/auth-access/workload-identity/oidc-gcp.md).
* In CoreWeave AI Object Storage, reference the ServiceAccount as the federated principal `role/[OIDC-ISSUER-URL]:system:serviceaccount:<namespace>:<name>`. See [Authenticate CKS workloads to AI Object Storage](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md).

### Federated authentication flow

Federated authentication ties these pieces together so workloads can reach external services using their cluster-issued identity. The flow has three parts:

* Register the CKS OIDC issuer URL in your target cloud or service provider (for example, as an OIDC provider in AWS or inside a GCP Workload Identity Pool).
* Authorize your Service Accounts to access specific resources by writing CSP IAM policies that reference claims from those tokens (such as Kubernetes namespace and ServiceAccount name).
* Allow workloads to authenticate to external APIs by presenting their CKS-issued token, with no external secrets required.

## Availability and enablement

OIDC Workload Identity is generally available and enabled by default on every CKS cluster, including sandbox clusters. No action is required to turn it on, and it can't be disabled.

* **Existing clusters**: CoreWeave enabled this feature on existing clusters with no downtime. Tokens and workloads that predate the feature continue to work. When a workload restarts or its token is refreshed, Kubernetes reissues the token with the public issuer URL, which remains backward compatible.
* **Private clusters**: CKS publishes a public OIDC Document Discovery URL even for clusters whose API endpoints aren't exposed to the internet. External providers must reach this discovery URL to validate tokens, and it doesn't expose sensitive or identifying information about your organization or cluster.

## Next steps

For end-to-end procedures that apply these concepts to specific cloud providers, see the following tutorials:

> [!TIP]
>
> Learn how to [secure access to Google Cloud Storage from CKS Pods using OIDC federation](https://docs.coreweave.com/products/cks/auth-access/workload-identity/oidc-gcp.md).

> [!TIP]
>
> Learn how to [authenticate CKS workloads to AI Object Storage using OIDC Workload Federation](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md).
