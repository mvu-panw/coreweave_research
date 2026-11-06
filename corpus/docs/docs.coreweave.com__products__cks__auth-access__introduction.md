# Introduction to authentication and access control

Source: https://docs.coreweave.com/products/cks/auth-access/introduction

# Introduction to authentication and access control

> Choose how users authenticate to the Kubernetes API on CoreWeave Kubernetes Service (CKS) clusters

Use this page to understand how CoreWeave identity and access controls apply to CoreWeave Kubernetes Service (CKS), then choose how users authenticate to a cluster. Private API access, workload identity, and Object Storage federation live under **Secure your cluster**.

For the relationship between identity, credentials, platform IAM, and service-specific authorization across CoreWeave, see the [CoreWeave authorization model](https://docs.coreweave.com/security/iam.md#authorization-model).

> [!NOTE]
>
> If you're signing in to CoreWeave for the first time, see [Activate and sign in to your CoreWeave organization](https://docs.coreweave.com/security/authn-authz/activate-org.md).

## Platform identity and CKS permissions

CoreWeave platform identity and IAM determine which CKS resources a user can access. Use the Security documentation to configure identity and access:

* [Organizations and users](https://docs.coreweave.com/security/authn-authz/orgs-users.md)
* [Managed Auth](https://docs.coreweave.com/security/authn-authz/managed-auth/introduction.md) (recommended for most organizations)
* [SAML SSO](https://docs.coreweave.com/security/authn-authz/saml-sso/intro-saml-sso.md)
* [Manage API access tokens and kubeconfig files](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md)
* [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md) and [IAM roles](https://docs.coreweave.com/security/iam/access-policies/roles.md#cks-clusters)

CKS uses two product IAM roles:

| Role | CKS permissions |
| - | - |
| `CKS Admin` | Create, update, and delete clusters and VPC resources. |
| `CKS Viewer` | List and view clusters and VPC resources without changing them. |

CKS uses [Organization IDs](https://docs.coreweave.com/security/authn-authz/orgs-users.md#organization-ids) to enforce tenant isolation. CKS filters all user interactions and cluster requests by Organization ID.

Within a cluster, Kubernetes role-based access control (RBAC) determines what authenticated users can do. **Read** permissions include the `watch`, `get`, and `list` verbs. **Write** permissions include the `create` and `patch` verbs. For the full permissions model, including how legacy `admin`, `write`, and `read` groups map to IAM and Kubernetes roles, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md) and [Legacy User Permissions](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions.md).

## Choose an authentication method

After a cluster exists, choose how users authenticate to its Kubernetes API:

| Approach | When to use it | Start here |
| - | - | - |
| Managed Auth kubeconfig | Recommended default for Cloud Console users and API access tokens | [Managed Authentication in CKS](https://docs.coreweave.com/products/cks/auth-access/managed-auth/kubeconfig.md) |
| Unmanaged authentication | Bring your own OIDC provider, Service Account tokens, or authentication webhook | [Introduction to unmanaged authentication](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/introduction.md) and [Implement unmanaged authentication](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth.md) |

> [!TIP]
>
> Managed Auth is the recommended path for user authentication to CKS. You must use Managed Auth to create new CKS clusters or VPCs. Unmanaged authentication applies only to existing clusters.

## Secure your cluster

Not every organization needs private API access or workload credentials. Those optional paths live under **Secure your cluster**:

* [Access a CKS cluster through Tailscale VPN](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md) for private API access.
* [Introduction to OIDC Workload Identity for CKS](https://docs.coreweave.com/products/cks/auth-access/workload-identity/introduction.md) for short-lived workload credentials.
* [Access Google Cloud Storage from CKS Pods](https://docs.coreweave.com/products/cks/auth-access/workload-identity/oidc-gcp.md) for Google Cloud federation.
* [CKS Workload Federation for AI Object Storage](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md) for Object Storage federation.

Private clusters have no public API endpoint. Besides Tailscale, you can reach the API through [Traefik ingress](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md), often paired with [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md). Self-service cluster creation supports public clusters only. To set up a private cluster, [contact CoreWeave Support](https://docs.coreweave.com/support.md).
