# Traefik

Source: https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik

# Traefik

> Deploy CoreWeave's Traefik Helm chart on CKS for Ingress, Kubernetes API proxying, and Gateway API

| Chart reference | Description |
| - | - |
| `coreweave/traefik` | CoreWeave's Helm chart for deploying Traefik on CKS clusters |

## About Traefik

The CoreWeave Traefik Helm chart is based on [the upstream Traefik chart](https://github.com/traefik/traefik-helm-chart). The CoreWeave chart includes additional templating for configurations commonly used in CKS clusters.

The chart's default values are set to work best on the CoreWeave platform. All code examples in this repository assume the default values. If you install the chart with different namespaces or resource names, update the values to match.

## Configuration

The following sections describe the chart's default Ingress behavior and how to enable TLS on Ingresses.

### Ingress DNS

By default, the chart applies a wildcard hostname through a `service.beta.kubernetes.io/external-hostname` annotation:

```text theme={"system"}
service.beta.kubernetes.io/external-hostname: '*'
```

This lets Traefik route to Ingress hosts within the CKS cluster. CKS automatically suffixes the wildcard hostname (`*`) with the appropriate domain name for your cluster. For Services that don't route through Traefik, specific DNS hostnames still take precedence.

To retrieve the applied value at any time, use `kubectl`:

```bash theme={"system"}
kubectl get svc traefik -n traefik -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
```

> [!NOTE]
>
> For more information on exposing Services, see [How to: Expose a Service](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md).

### IngressRouteTCP and Kubernetes API proxy

The chart's default values include a [Traefik IngressRouteTCP](https://doc.traefik.io/traefik/routing/providers/kubernetes-crd/#kind-ingressroutetcp) TCP router for your cluster's Kubernetes API server. This Service proxies HTTP traffic to your cluster over [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md) and provides TLS passthrough.

To locate the hostname of this Service, run the following command:

```bash theme={"system"}
kubectl get svc traefik-k8s -n traefik -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
```

> [!WARNING]
>
> When you reach the Kubernetes API server over Direct Connect, use the publicly resolvable hostname from the `traefik-k8s` Service, not the private load balancer IP. The API server certificate includes a DNS subject alternative name (SAN) for this hostname, but it doesn't include the `traefik-k8s` load balancer IP. Connecting by IP causes TLS verification errors.
>
> For example, `k8s.[ORG-ID]-[CLUSTER-NAME].coreweave.app`. This hostname resolves to the private load balancer IP.

#### Configure client trust and authentication

The Traefik API proxy passes TLS through without terminating it, so clients connect directly to the Kubernetes API server. The API server presents a certificate signed by the cluster certificate authority (CA) and authenticates each request itself. A Managed Auth kubeconfig instead relies on a publicly trusted certificate and uses a CoreWeave API access token. If you change only the kubeconfig's `server` value, certificate verification fails with an error such as `x509: certificate signed by unknown authority` on Linux and Windows, or `certificate is not trusted` on macOS. Adding the cluster CA fixes verification, but the API server still rejects the CoreWeave API access token.

CKS publishes the cluster CA in the `cluster-info` ConfigMap in the `kube-public` namespace, which you can read without credentials. On a public cluster, read it from the [unmanaged endpoint](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth.md):

```bash theme={"system"}
CA_DATA=$(curl -s https://api.[ORG-ID]-[CLUSTER-HASH].k8s.[ZONE].coreweave.com/api/v1/namespaces/kube-public/configmaps/cluster-info \
  | jq -r '.data.kubeconfig | capture("certificate-authority-data:\\s*(?<ca>\\S+)") | .ca')
```

If you already have a kubeconfig context that reaches the cluster, such as a Managed Auth kubeconfig through the Tailscale proxy in [CoreWeave Managed Auth](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md#coreweave-managed-auth) mode on a private cluster, read it with `kubectl` instead. Replace `[CONTEXT]` with that context's name:

```bash theme={"system"}
CA_DATA=$(kubectl --context [CONTEXT] get configmap cluster-info --namespace kube-public --output json \
  | jq -r '.data.kubeconfig | capture("certificate-authority-data:\\s*(?<ca>\\S+)") | .ca')
```

Add a cluster entry for the `traefik-k8s` hostname that uses the CA as its `certificate-authority-data`. Then create a context that pairs it with a user that authenticates through OIDC or an authentication webhook, such as the `kubelogin` user from [Configure a kubectl context with kubelogin](https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth.md#step-5-configure-a-kubectl-context-with-kubelogin). Replace `[USER]` with that user's name:

```bash theme={"system"}
kubectl config set-cluster cks-traefik \
  --server=https://k8s.[ORG-ID]-[CLUSTER-NAME].coreweave.app
kubectl config set clusters.cks-traefik.certificate-authority-data "$CA_DATA"
kubectl config set-context cks-traefik --cluster=cks-traefik --user=[USER]
```

Requests through the Traefik API proxy don't pass through Managed Auth, so CoreWeave IAM access policies don't apply to them. Kubernetes RBAC authorizes them.

### Create Ingresses with TLS

> [!WARNING]
>
> An Ingress with TLS requires `cert-manager` to create and manage the certificates. If you don't have an existing deployment, you can deploy CoreWeave's [cert-manager and its subchart, cert-issuer](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) for this purpose.

After you deploy the chart, you can use Traefik as the `IngressClass` for a Kubernetes Ingress with TLS. To create the TLS certificate, `cert-manager` uses the `ClusterIssuer` specified by the `cert-manager.io/cluster-issuer` annotation on the `Ingress` object.

## Example chart

In this example manifest, the Ingress uses the default Let's Encrypt `ClusterIssuer` from CoreWeave's [cert-issuer](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) chart. You can also configure your own TLS certificate solution.

```yaml title="ingress-example.yaml - An example using Traefik with TLS and DNS" highlight={5-7,13-14,27-28} theme={"system"}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    # This value must match either the ClusterIssuer created by Traefik,
    # or another pre-existing ClusterIssuer
        cert-manager.io/cluster-issuer: letsencrypt-prod
  name: ingress1
  namespace: namespace1
spec:
  ingressClassName: traefik
  rules:
  # The FQDN used to access this Ingress via the Traefik Service
  - host: &host ingress1.myorg-mycluster.coreweave.app
    http:
      paths:
      - backend:
          service:
            name: my-service
            port:
              number: 80
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - *host
    # This secret will be automatically created for you
    secretName: ingress1-tls
```

> [!NOTE]
>
> For more information on Traefik as a Kubernetes Ingress provider, see [the official Traefik documentation](https://doc.traefik.io/traefik/providers/kubernetes-ingress/).

## Gateway API

The chart can also run Traefik as a [Gateway API](https://gateway-api.sigs.k8s.io/) controller. When you enable the Gateway API provider, the chart creates a `GatewayClass` named `traefik` and a `Gateway` named `traefik-gateway` in the `traefik` namespace.

The Gateway uses the same `traefik` LoadBalancer Service as Ingress. Gateway API routes and Ingresses share one IP address and the cluster's wildcard DNS name, so you can run both on the same Traefik Pods and move workloads from Ingress to Gateway API one at a time.

The Traefik version in the chart supports the Gateway API standard channel, including `HTTPRoute`, `GRPCRoute`, `TLSRoute`, and `BackendTLSPolicy`. The standard channel CRDs on this page don't support `TCPRoute` with Traefik. To use `TCPRoute`, install the experimental channel CRDs instead and set `traefik.providers.kubernetesGateway.experimentalChannel: true`. For details, see [the Traefik Kubernetes Gateway API provider documentation](https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-gateway/).

To follow these steps, you need `kubectl` and `helm` access to the cluster, with permissions to create cluster-scoped resources such as CRDs and the `GatewayClass`.

> [!NOTE]
>
> Each CKS cluster has one wildcard DNS name, and the `traefik` Service claims it. Don't install a second Gateway API controller that creates its own LoadBalancer Service with the wildcard hostname, because only one Service can hold it. The second Service reports a `HostnameConflict`. See [Why is my Service not getting a DNS name?](https://docs.coreweave.com/support/networking/articles/why-is-my-service-not-getting-a-dns-name)

### Install the Gateway API CRDs

Gateway API adds resource types through cluster-wide Custom Resource Definitions (CRDs) that every controller in the cluster shares. Install them before you enable the provider.

> [tab] Separate install (recommended)
>
> Apply the standard channel CRDs from the [Gateway API release](https://github.com/kubernetes-sigs/gateway-api/releases):
>
> ```bash theme={"system"}
> kubectl apply --server-side \
>   -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.3/standard-install.yaml
> ```
>
> Before you upgrade the chart, check the Requirements section of [Traefik's Kubernetes Gateway provider documentation](https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-gateway/) for the Gateway API version that the new Traefik version supports, and upgrade the CRDs to match.
>
> The CRDs stay in the cluster if you later uninstall or reconfigure Traefik.
>
> If another component, such as Cilium or a service mesh, already installed a compatible Gateway API CRD bundle, skip this step. Otherwise, coordinate the CRD upgrade with the component that manages them. To check the installed bundle version, run:
>
> ```bash theme={"system"}
> kubectl get crd gateways.gateway.networking.k8s.io \
>   -o jsonpath='{.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}'
> ```

> [tab] Bundled with the chart
>
> The chart can install the CRDs as part of the Traefik release, through the optional `gateway-crds-helm` dependency. The bundled CRDs use the standard channel.
>
> > [!WARNING]
> >
> > When the chart installs the CRDs, the Traefik release owns them. If you uninstall Traefik or disable the `gateway-crds-helm` dependency in an upgrade, Helm deletes the CRDs. Kubernetes then deletes every Gateway API resource in the cluster, including resources that belong to other controllers. If cert-manager's Gateway API support is enabled, cert-manager also fails to start on its next restart until you reinstall the CRDs.
> >
> > If an upgrade deletes the CRDs, the release still contains the `Gateway` and `GatewayClass`, so `helm uninstall traefik` fails with `no matches for kind "Gateway"`. To uninstall, first reinstall the CRDs with the `kubectl apply` command in the **Separate install** tab.
> >
> > The install also fails if the CRDs already exist in the cluster, with the error `exists and cannot be imported into the current release`.
>
> Add the following to your values file. Keep it in the file for every later upgrade:
>
> ```yaml title="traefik-gateway-values.yaml" theme={"system"}
> gateway-crds-helm:
>   crds:
>     gatewayAPI:
>       enabled: true
>       channel: standard
> ```
>
> Helm checks every resource kind in a release before it creates any of them, so the release that installs the CRDs can't also create the `Gateway` and `GatewayClass`. Install the chart once with creation of those two resources turned off:
>
> ```bash theme={"system"}
> helm upgrade --install traefik coreweave/traefik \
>   --namespace traefik \
>   --create-namespace \
>   -f traefik-gateway-values.yaml \
>   --set traefik.gateway.enabled=false \
>   --set traefik.gatewayClass.enabled=false
> ```
>
> Then continue with [Enable the Gateway API provider](#enable-the-gateway-api-provider), which creates them.

### Enable Gateway API support in cert-manager

As with Ingresses, cert-manager issues the TLS certificate for the Gateway from an annotation. Enable cert-manager's Gateway API support and provide an existing issuer. The example uses `letsencrypt-prod`, which CoreWeave's [cert-manager chart](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) creates when you enable the `cert-issuers` subchart. See [Gateway API support](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md#gateway-api-support) on the cert-manager page.

The chart doesn't automatically restart cert-manager when you change values in an existing controller configuration. After you change an existing configuration or install the CRDs after cert-manager, restart cert-manager and confirm that its `gateway-shim` controller is running, as described on that page.

### Enable the Gateway API provider

Add the provider, certificate annotation, and listener configuration to your Traefik values file. Keep your existing chart settings, including the CRD values if you use the bundled installation. Replace `[ORG-ID]` and `[CLUSTER-NAME]` with your organization ID and cluster name:

```yaml title="traefik-gateway-values.yaml" theme={"system"}
traefik:
  providers:
    kubernetesGateway:
      enabled: true
  gateway:
    annotations:
      # This value must match an existing ClusterIssuer
      cert-manager.io/cluster-issuer: letsencrypt-prod
    listeners:
      web:
        port: 8000
        protocol: HTTP
        namespacePolicy:
          from: All
      websecure:
        port: 8443
        protocol: HTTPS
        hostname: "*.[ORG-ID]-[CLUSTER-NAME].coreweave.app"
        certificateRefs:
          - kind: Secret
            name: gateway-wildcard-tls
        namespacePolicy:
          from: All
```

The configuration has the following settings and behavior:

* Each listener `port` is a Traefik container port: `8000` for `web` and `8443` for `websecure`. The `traefik` Service publishes them on ports `80` and `443`. The chart rejects listener ports that aren't declared in `traefik.ports`. For a user-created Gateway, a listener whose port doesn't match a configured Traefik entry point reports `Accepted=False` with the reason `PortUnavailable`.
* `namespacePolicy.from: All` lets routes in any namespace attach to the Gateway. By default, a Gateway accepts routes only from its own namespace.
* With the `cert-manager.io/cluster-issuer` annotation, cert-manager creates a `Certificate` for the `websecure` listener's hostname and stores it in the `gateway-wildcard-tls` Secret. The listener terminates TLS with that Secret.
* This example requests one wildcard certificate for the Gateway listener. It covers every route hostname under `*.[ORG-ID]-[CLUSTER-NAME].coreweave.app`, so routes don't need their own certificates. For the Let's Encrypt quota that applies to `.coreweave.app` certificates, see [cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md#clusterissuer-for-acme-and-dns01-challenges).

Install or upgrade the chart with the values file:

```bash theme={"system"}
helm upgrade --install traefik coreweave/traefik \
  --namespace traefik \
  --create-namespace \
  -f traefik-gateway-values.yaml
```

Verify that Traefik accepted the `GatewayClass` and programmed the `Gateway`:

```bash theme={"system"}
kubectl get gatewayclass traefik
kubectl get gateway -n traefik
```

You should see output similar to the following:

```text theme={"system"}
NAME      CONTROLLER                      ACCEPTED   AGE
traefik   traefik.io/gateway-controller   True       11s

NAME              CLASS     ADDRESS          PROGRAMMED   AGE
traefik-gateway   traefik   [IP-ADDRESS]     True         11s
```

The `ADDRESS` is the IP address of the `traefik` LoadBalancer Service.

> [!NOTE]
>
> Traefik doesn't create Pods or a Service for each Gateway. Every Gateway with `gatewayClassName: traefik` configures the same Traefik Pods and reports the `traefik` Service's address. Its listener ports must match Traefik's entry points. You can create your own Gateways instead of, or in addition to, the one the chart creates. To disable the chart's Gateway, set `traefik.gateway.enabled: false`.

Wait for cert-manager to issue the certificate. cert-manager creates the `Certificate` in the `traefik` namespace, with the same name as the Secret:

```bash theme={"system"}
kubectl wait certificate/gateway-wildcard-tls -n traefik --for=condition=Ready --timeout=300s
kubectl get certificate -n traefik
```

You should see output similar to the following:

```text theme={"system"}
NAME                   READY   SECRET                 AGE
gateway-wildcard-tls   True    gateway-wildcard-tls   14s
```

Until the Secret exists, the `websecure` listener reports `ResolvedRefs: False` with the reason `InvalidCertificateRef`. If no `Certificate` appears, check that cert-manager's Gateway API support is enabled. To check the status of each listener, run:

```bash theme={"system"}
kubectl get gateway traefik-gateway -n traefik \
  -o jsonpath='{range .status.listeners[*]}{.name}{": "}{range .conditions[*]}{.type}={.status} {end}{"\n"}{end}'
```

After the certificate is ready, both listeners report `Programmed=True`:

```text theme={"system"}
web: Accepted=True ResolvedRefs=True Programmed=True
websecure: Accepted=True ResolvedRefs=True Programmed=True
```

### Route traffic with an HTTPRoute

Before you create the route, deploy a backend Service named `my-service` in `namespace1` that serves HTTP on port `80`, or replace those values with an existing Service and namespace. Replace `[ORG-ID]` and `[CLUSTER-NAME]` in the examples with your organization ID and cluster name.

An `HTTPRoute` attaches to the Gateway through `parentRefs` and sends requests for its hostnames to a backend Service. In this example, the route sends traffic for `app.[ORG-ID]-[CLUSTER-NAME].coreweave.app` to the `my-service` Service on port `80`:

```yaml title="httproute-example.yaml" theme={"system"}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
  namespace: namespace1
spec:
  parentRefs:
    - name: traefik-gateway
      namespace: traefik
  hostnames:
    - app.[ORG-ID]-[CLUSTER-NAME].coreweave.app
  rules:
    - backendRefs:
        - name: my-service
          port: 80
```

Without a `sectionName`, the route attaches to both listeners and serves HTTP and HTTPS. Because the wildcard DNS name and wildcard certificate cover the hostname, you don't need a DNS record or a certificate for each route.

Apply the route and check that the Gateway accepted it:

```bash theme={"system"}
kubectl apply -f httproute-example.yaml
kubectl get httproute my-app -n namespace1 \
  -o jsonpath='{range .status.parents[*].conditions[*]}{.type}={.status} {end}{"\n"}'
```

You should see `Accepted=True ResolvedRefs=True`. Then send a request:

```bash theme={"system"}
curl https://app.[ORG-ID]-[CLUSTER-NAME].coreweave.app
```

#### Redirect HTTP to HTTPS

To serve a hostname over HTTPS only, attach one route to the `web` listener that redirects requests, and another to the `websecure` listener that sends them to the backend. The `sectionName` field selects the listener:

```yaml title="httproute-https-redirect.yaml" theme={"system"}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app-redirect
  namespace: namespace1
spec:
  parentRefs:
    - name: traefik-gateway
      namespace: traefik
      sectionName: web
  hostnames:
    - app.[ORG-ID]-[CLUSTER-NAME].coreweave.app
  rules:
    - filters:
        - type: RequestRedirect
          requestRedirect:
            scheme: https
            statusCode: 301
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
  namespace: namespace1
spec:
  parentRefs:
    - name: traefik-gateway
      namespace: traefik
      sectionName: websecure
  hostnames:
    - app.[ORG-ID]-[CLUSTER-NAME].coreweave.app
  rules:
    - backendRefs:
        - name: my-service
          port: 80
```
