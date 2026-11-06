# Other Kubernetes clusters

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/tutorials/kubernetes

# Other Kubernetes clusters

> Find the OIDC issuer URL for non-CKS Kubernetes clusters

Any Kubernetes cluster with an OIDC issuer can use Workload Identity Federation to authenticate to CoreWeave AI Object Storage. This guide is for administrators of non-CKS Kubernetes clusters who need to locate the OIDC issuer URL to configure Workload Identity Federation. It shows how to find that URL for common managed Kubernetes services so you can complete the federation setup.

For CKS clusters, see the [CKS Object Storage authentication tutorial](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md) instead.

## Find your cluster OIDC issuer URL

If you have the appropriate permissions, run the following command to retrieve the OIDC issuer URL from any Kubernetes cluster:

```bash theme={"system"}
kubectl get --raw /.well-known/openid-configuration | jq -r .issuer
```

### Amazon EKS

In the AWS Console, go to your EKS cluster details. The OIDC issuer URL is listed under **OpenID Connect provider URL**.

### Azure AKS

In the Azure Portal, go to your AKS cluster. The OIDC issuer URL is listed under the cluster's properties. Make sure the OIDC issuer is enabled on the cluster.

## Next steps

After you complete these steps, you have the OIDC issuer URL for your Kubernetes cluster. Use it to configure Workload Identity Federation for Object Storage.

Follow the [Using Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) guide to complete the setup. Set **Issuer URL** to the cluster's OIDC issuer URL. Set **Client ID (Audience)** to `https://coreweave.com/iam` (recommended), or to another audience that matches the `audience` value on your projected service account tokens.
