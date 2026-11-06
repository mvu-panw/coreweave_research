# About access keys

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about

# About access keys

> Understand the two methods for creating access keys to authenticate against AI Object Storage

CoreWeave AI Object Storage uses access keys to authenticate requests for users and workloads. You can obtain access keys in three ways: by exchanging a CoreWeave API access token directly for temporary credentials, through Workload Identity Federation, or by creating a static key with an API access token.

## Direct access token exchange

> [!NOTE]
>
> To exchange a CoreWeave API access token directly for temporary AI Object Storage credentials, you need the `Object Storage Admin` role or an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) that grants `cwobject:CreateAccessKey`.

If you already authenticate with a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md), you can exchange it directly for temporary AI Object Storage credentials, without creating a separate static access key. CoreWeave recommends this method for principals that already have a CoreWeave API access token, because it removes the extra key-creation step and carries the principal's SCIM group memberships in the `iam:[ORG-ID]:groups` condition key for [group-based access control](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#attribute-based-access-control).

* **Duration**: Keys are ephemeral and refresh automatically through the AWS container credentials provider. The keys are valid for 30 minutes.
* **Identity format**: `coreweave/[UID]`.

For setup steps, see [Direct access token exchange](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md).

## Workload Identity Federation

CoreWeave recommends [Workload Identity Federation (WIF)](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for production workloads. Instead of storing long-lived credentials, your applications obtain tokens from your existing identity provider (IdP) and exchange them for short-lived access keys that automatically expire. OpenID Connect (OIDC) is the default for new WIF integrations. CoreWeave offers Security Assertion Markup Language (SAML) by request for organizations with an existing SAML requirement.

### Workload Identity Federation with OIDC

OIDC is the recommended method for cloud-native and Kubernetes workloads. It uses short-lived tokens from your identity provider, such as GitHub Actions, a Kubernetes service account, or any OIDC-capable IdP, and exchanges them for temporary access keys with a 30-minute lifespan. OIDC is the standard approach for machine-to-machine authentication in cloud environments.

To generate keys with OIDC tokens, follow [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md). The recommended AWS container-credentials integration obtains temporary keys automatically when AWS tooling needs credentials. For a direct API integration, use the [`CreateAccessKeyFromOIDC`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-oidc) `POST` operation.

* **Duration**: Keys are temporary with a 30-minute lifespan.
* **Identity format**: `role/[ISSUER-URL]:[SUBJECT-USER-ID]`.

### Workload Identity Federation with SAML

CoreWeave offers SAML by request to organizations with an existing SAML requirement. Before you use this method, contact your CoreWeave account team. SAML integrates with enterprise identity providers such as Active Directory Federation Services.

To generate keys with SAML assertions, submit API requests to [`CreateAccessKeyFromSAML`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-saml). These keys have the following characteristics:

* **Duration**: Keys are temporary with a maximum lifespan of 12 hours.
* **Identity format**: `role/[SAML-ROLE]`.
* **Requirements**: You must create a valid `configId` from a Workload Identity Federation configuration and pass it to the API request. For more information, see [Using Workload Identity Federation with SAML](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/saml-workload-federation.md).

## Static access keys

> [!NOTE]
>
> Creating static access keys requires the `Object Storage Admin` role or an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) that grants `cwobject:CreateAccessKey`.

You can use an API access token to create persistent or time-limited access keys for Object Storage. To create a static access key, follow the steps in [Create access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md).

To generate keys this way, submit API requests to [`CreateAccessKeyFromJWT`](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key). These keys have the following characteristics:

* **Duration**: Keys can be persistent, or they can be time-limited for up to 12 hours.
* **Identity format**: `coreweave/[PRINCIPAL-UID]`.
* **Requirements**: To create an access key, you need either the **Object Storage Admin** role or an organization access policy that grants `cwobject:CreateAccessKey`. The access key's subsequent S3-compatible operations are governed separately by [organization and bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md).

## Identity formats

You can use the access key format to audit and diagnose access. To find out how an access key was created, examine its identity format:

| Creation method | Identity format | Example |
| - | - | - |
| **OIDC tokens** | `role/[ISSUER-URL]:[SUBJECT]` | `role/https://oidc.cks.coreweave.com/id/3f9a2c14-7d6e-4b81-9a05-2c8e1f4b6d3a:system:serviceaccount:default:default` |
| **API access token** | `coreweave/[PRINCIPAL-UID]` | `coreweave/qT7mWZ4kRb9nXcVp2sLdH` |
| **CoreWeave internal tools** | `static/[KEY-ID]` | `static/audit-logs` |
| **SAML assertions** | `role/[SAML-ROLE]` | `role/SRE_ADMIN` |

## Types of access keys

Access keys fall into categories based on creation method:

**Static keys** come from an API access token and are intended for development, testing, and manual operations:

* **Permanent keys**: Don't expire. Require manual rotation.
* **Temporary keys**: Expire after a set duration of up to 12 hours.

Workload Identity Federation generates **WIF keys** for production workloads. They're always temporary, so you never need to store or rotate them:

* **OIDC-generated keys**: 30-minute lifespan. Your application automatically refreshes them.
* **SAML-generated keys**: CoreWeave offers these keys by request for existing SAML integrations. They have a lifespan of up to 12 hours.

For production environments, use OIDC Workload Identity Federation for automated key management. For less sensitive operations or for testing, you can use access keys created with an API access token.

## Manage your access keys

This section covers the full lifecycle of access key management:

* [Create access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md): Generate new keys for users and workloads.
* [Revoke access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/revoke-keys.md): Remove keys that are no longer needed.
