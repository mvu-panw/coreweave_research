# Common OIDC providers

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/intro

# Common OIDC providers

> Guides for configuring Workload Identity Federation with common OIDC providers

[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/) is a widely used standard for authenticating and sharing identities across platforms. CoreWeave AI Object Storage supports OIDC-based [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md), allowing you to authenticate both human users and machine workloads without managing static credentials.

OIDC integration follows three common patterns:

* **Human users** authenticate through a browser, re-authenticating periodically.
* **Long-lived workloads** such as servers and functions run in a cloud provider or Kubernetes cluster that provides an automatically rotated OIDC token.
* **Short-lived jobs** such as CI/CD pipelines receive an OIDC token at the start of the job.

For the general setup process that applies to all providers, see [Using Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md).

## Provider-specific guides

> [card] [CKS clusters](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md)
>
> Connect CoreWeave Kubernetes Service (CKS) clusters to AI Object Storage with automatic or manual OIDC configuration.

> [card] [GitHub Actions](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/github.md)
>
> Authenticate GitHub Actions workflows to AI Object Storage using GitHub's OIDC tokens.

> [card] [Other Kubernetes clusters](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/kubernetes.md)
>
> Find the OIDC issuer URL for EKS, AKS, and other Kubernetes clusters.
