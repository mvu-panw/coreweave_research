# Cert-manager

Source: https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager

# Cert-manager

> Install cert-manager and set up certificate issuers for Services and Gateways

| Chart reference | Description |
| - | - |
| `coreweave/cert-manager` | CoreWeave's Helm chart for deploying cert-manager on CKS clusters |

## About cert-manager

[cert-manager](https://cert-manager.io/) is an open-source tool that automates the management and issuance of TLS certificates in Kubernetes. CoreWeave provides a `cert-manager` Helm chart so you can deploy it on CKS clusters with sensible defaults. The chart supports Let's Encrypt and CoreWeave's DNS-based ACME solver. This page is for cluster operators who need to provision TLS certificates for workloads that run on CKS.

The CoreWeave cert-manager chart includes a `cert-issuers` subchart that creates cert-manager [Issuers and ClusterIssuers](https://cert-manager.io/docs/concepts/issuer/) after you deploy cert-manager.

> [!NOTE]
>
> Because `cert-issuers` depends on an existing `cert-manager` deployment, `cert-issuers` is disabled by default to prevent failed deployments. When you enable it, the subchart creates a self-signed `ClusterIssuer` and [Let's Encrypt](https://letsencrypt.org/) `ClusterIssuers` for both production and staging. You can override these with your preferred `Issuer` type.

## Usage

The CoreWeave `cert-manager` chart provides defaults that work for most CoreWeave users, and you can deploy it as-is. For all configuration options, see [the upstream cert-manager chart](https://github.com/cert-manager/cert-manager/tree/master/deploy/charts/cert-manager).

### ClusterIssuer for ACME and DNS01 challenges

The `ClusterIssuers` bundled with `cert-issuers` use a [DNS01 solver with cert-manager](https://cert-manager.io/docs/configuration/acme/dns01/), backed by a CoreWeave webhook at `acme.coreweave.com`.

When you request an ACME Certificate, `cert-manager` creates a [Custom Resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) called `Order` to initiate and track the request. `Order` then creates multiple Custom Resources called `Challenge` to validate that the requester owns the requested domain.

`DNS01` challenges provision a `TXT` record in the DNS zone for the requested domain. The ACME CA server resolves that record to validate your ownership of the domain. The CoreWeave webhook solver automates this step for domains that CoreWeave manages, so you don't need a public-facing Ingress or a temporary web server. After all challenges complete successfully, `cert-manager` receives the requested certificate and configures your Ingress to use the key.

> [!NOTE]
>
> Because the bundled Let's Encrypt `ClusterIssuer` uses the `DNS01` challenge type, it supports wildcard certificates in addition to single-host certificates.

> [!WARNING]
>
> Certificates for `.coreweave.app` names issued through `letsencrypt-prod` draw from a single Let's Encrypt quota of 50 new certificates per 168 hours, shared across all CoreWeave customers. To avoid failed issuance, request one wildcard certificate per cluster, and use `letsencrypt-staging` for development and CI. See [Why am I seeing "too many certificates already issued for coreweave.app"?](https://docs.coreweave.com/support/cks/articles/why-am-i-seeing-too-many-certificates-errors-for-coreweave-app)

### Gateway API support

cert-manager can issue certificates for [Gateway API](https://gateway-api.sigs.k8s.io/) `Gateways`, the same way it does for Ingresses. When a `Gateway` has a `cert-manager.io/cluster-issuer` or `cert-manager.io/issuer` annotation, cert-manager creates certificates for eligible HTTPS listeners, using the Secret names in `certificateRefs`. Gateway API support is deactivated by default.

Install the [Gateway API CRDs](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md#install-the-gateway-api-crds) before you enable Gateway API support. If the CRDs don't exist, the `cert-manager` controller fails to start and restarts repeatedly, with the error `the Gateway API CRDs do not seem to be present`.

To enable Gateway API support, add the following to your `cert-manager.yaml` values file. Keep your existing settings, including `cert-issuers.enabled: true` if you use the bundled issuers:

```yaml title="cert-manager.yaml" theme={"system"}
cert-manager:
  config:
    gatewayAPI:
      enabled: true
```

Then install or upgrade the chart:

```bash theme={"system"}
helm upgrade --install cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  -f cert-manager.yaml
```

cert-manager reads this setting and checks for the CRDs only when it starts. When an existing controller configuration changes, the chart doesn't restart cert-manager automatically. Restart cert-manager after you change an existing configuration or install the Gateway API CRDs after cert-manager:

```bash theme={"system"}
kubectl rollout restart deployment cert-manager -n cert-manager
kubectl rollout status deployment cert-manager -n cert-manager
```

To confirm that Gateway API support is active, check the cert-manager logs for the `gateway-shim` controller:

```bash theme={"system"}
kubectl logs deployment/cert-manager -n cert-manager | grep gateway-shim
```

You should see `"starting controller" ... controller="gateway-shim"`. If you see `"skipping disabled controller"` instead, check that Gateway API support is enabled and that controller selection or feature gates do not exclude `gateway-shim`. If you changed an existing configuration, restart cert-manager.

cert-manager creates a `Certificate` only for listeners that set a `hostname`, use TLS mode `Terminate`, and reference a `Secret` in `certificateRefs` in the namespace of the `Gateway`. For an example with Traefik, see [Traefik Gateway API](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md#gateway-api). For all options, see [the cert-manager Gateway API documentation](https://cert-manager.io/docs/usage/gateway/).

## Example chart

The following example shows a complete `cert-manager.yaml` values file. It defines the bundled `cert-issuers` subchart's Let's Encrypt production and staging `ClusterIssuers` and a self-signed `ClusterIssuer`.

The subchart is deactivated because a first install with it enabled fails. The release creates the cert-manager CRDs, so Helm can't create the `ClusterIssuers` in the same install and reports `no matches for kind "ClusterIssuer"`. After the first install, set `cert-issuers.enabled: true` and upgrade the chart to create the `ClusterIssuers`.

The example also shows the cert-manager values CoreWeave recommends for CKS clusters, with [Gateway API support](#gateway-api-support) deactivated. Use it as a starting point for your configuration.

```yaml title="cert-manager.yaml" theme={"system"}
cert-issuers:
  enabled: false
  clusterIssuers:
    - name: letsencrypt-prod
      annotations: {}
      labels: {}
      spec:
        acme:
          server: https://acme-v02.api.letsencrypt.org/directory
          privateKeySecretRef:
            name: letsencrypt-prod-account-key
          solvers:
            - dns01:
                webhook:
                  groupName: acme.coreweave.com
                  solverName: dns01
    - name: letsencrypt-staging
      annotations: {}
      labels: {}
      spec:
        acme:
          server: https://acme-staging-v02.api.letsencrypt.org/directory
          privateKeySecretRef:
            name: letsencrypt-staging-account-key
          solvers:
            - dns01:
                webhook:
                  groupName: acme.coreweave.com
                  solverName: dns01
    - name: selfsigned-cluster-issuer
      spec:
        selfSigned: {}
  issuers: []

cert-manager:
  global:
    podSecurityPolicy:
      enabled: false
  crds:
    enabled: true
    keep: true
  config:
    gatewayAPI:
      # Set to true to issue certificates for Gateway API Gateways.
      # Install the Gateway API CRDs first, or cert-manager fails to start.
      enabled: false
```

## Learn more

For more information about cert-manager usage, see:

* [cert-manager Issuer configuration](https://cert-manager.io/docs/configuration/)
