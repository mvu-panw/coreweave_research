# Workload Identity Federation for AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about

# Workload Identity Federation for AI Object Storage

> Secure access to AI Object Storage using external identity providers

Workload Identity Federation (WIF) enables your applications to access CoreWeave AI Object Storage using tokens from your existing identity provider (IdP). This approach eliminates the need to store long-lived credentials in your applications or configuration files. This page explains how WIF works, how its components fit together, and which setup guide to follow. OpenID Connect (OIDC) is the default protocol for new integrations.

## How it works

Instead of managing static API keys, your applications obtain tokens from your identity provider and exchange them for temporary CoreWeave access credentials. These credentials expire after a configurable duration, and your applications refresh them by exchanging new tokens as needed.

![Diagram showing the authentication flow from workloads, CI/CD pipelines, and people through identity providers to CoreWeave IAM and AI Object Storage](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/iam-caios-auth-relationship-flow.jpg?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=a3c961188be31f071e4bb88ac3717e2d)

Workload Identity Federation handles only authentication, which verifies that your workload is who it claims to be based on your IdP's tokens. Your [organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) authorize the WIF role as a principal in your organization. Add a [bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md) when you need to control a specific resource.

## Supported protocols

CoreWeave supports the following protocols for Workload Identity Federation:

* **OIDC** is the default for new integrations. It uses JSON Web Tokens (JWT) and supports programmatic access patterns for Kubernetes, cloud environments, and other workloads with an OIDC-capable identity provider.
* CoreWeave offers **Security Assertion Markup Language (SAML)** by request to organizations with an existing SAML requirement. It uses XML-based assertions and supports integrations with enterprise identity providers. Before you plan a SAML integration, contact your CoreWeave account team.

## Connect WIF to access policies

Workload Identity Federation issues temporary credentials tied to a role identity, and you must then create access policies that grant permissions to that role. This step is separate from the authentication process, and you must configure both.

Use an organization access policy to grant actions to the WIF role. Use a bucket access policy to control a specific resource, including access from other organizations. For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation).

## Get started

Follow [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) to configure WIF for your workloads.

The guide covers the full workflow: configure your IdP, create a WIF configuration in the Cloud Console, set up access policies, and exchange tokens for credentials.

If your organization requires SAML and your CoreWeave account team confirms availability, follow [Use Workload Identity Federation with SAML](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/saml-workload-federation.md).

For provider-specific OIDC setup, see [Common OIDC providers](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/intro.md), including [GitHub Actions](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/github.md) and [other Kubernetes clusters](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/kubernetes.md). For CKS clusters, see the [CKS Object Storage authentication tutorial](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md).
