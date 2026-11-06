# etcd Secrets encryption at rest

Source: https://docs.coreweave.com/products/cks/clusters/secrets

# etcd Secrets encryption at rest

> How CoreWeave CKS clusters encrypt Secrets at rest

CoreWeave provides encryption at rest for `etcd` data in CoreWeave Kubernetes Service (CKS) clusters using a KMS-backed setup. For new CKS clusters created after June 24, 2025, this feature is enabled by default and requires no action from you.

> [!NOTE]
>
> For existing CKS clusters created on or before June 24, 2025, you must rotate your existing Kubernetes Secrets once. After that, CoreWeave handles the lifecycle for you.

In Kubernetes, [Secrets are stored unencrypted in `etcd` by default](https://kubernetes.io/docs/concepts/security/secrets-good-practices/#configure-encryption-at-rest).
You typically configure encryption at rest manually using a [Key Management Service (KMS) provider](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/).

With CKS, CoreWeave sets up and maintains this for you automatically.

## Rotate Secrets in existing clusters

If your CKS cluster was created before June 24, 2025, your existing Secrets might not yet be encrypted. To ensure full encryption coverage,
[replace the existing Secrets](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/#ensuring-all-secrets-are-encrypted) once. Going forward, CoreWeave encrypts any new Secrets you create automatically.

The following command rotates your Secrets in place by replacing each existing Secret with itself, which triggers the KMS provider to encrypt them:

```bash theme={"system"}
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

After this command completes, CKS rewrites your existing Secrets through the KMS provider and stores them encrypted in `etcd` alongside any new Secrets you create.

## Comparison to upstream Kubernetes

This section summarizes how CKS Secrets encryption differs from a self-managed upstream Kubernetes setup, so you can see which responsibilities CoreWeave handles for you.

While Kubernetes [offers encryption at rest as an optional config](https://kubernetes.io/docs/concepts/security/secrets-good-practices/#configure-encryption-at-rest),
CoreWeave enables it by default. Your CKS clusters have Secrets encryption at rest, without the operational burden.

| **Concept** | **Upstream Kubernetes** | **CoreWeave CKS** |
| - | - | - |
| KMS provider | You choose and configure the provider | CoreWeave |
| Who manages your keys | You manage your keys | CoreWeave |
| Plugin config | You write and deploy it manually | CoreWeave provisions and injects it automatically |
| Encryption scope | You choose what to encrypt | CoreWeave encrypts Secrets by default |
| Key rotation, unseal, backup | Manual setup and maintenance | Automated by CoreWeave |
