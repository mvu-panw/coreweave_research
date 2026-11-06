# Create a public DNS name

Source: https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name

# Create a public DNS name

> Use a fully qualified domain name (FQDN) for a LoadBalancer Service

The external address of a Kubernetes `LoadBalancer` Service can change when you re-create the Service or change its configuration. To get a stable human-readable address for publicly exposed Services, request a fully qualified domain name (FQDN) or wildcard record for your `LoadBalancer` Service. This page shows cluster operators how to request a name, how the resulting FQDN is constructed, and how to view the allocated record.

## Overview

The FQDN allocation workflow has the following steps:

* To allocate an FQDN for your `LoadBalancer` Service, set the `service.beta.kubernetes.io/external-hostname` annotation in your manifest using [short](#create-an-fqdn-using-short-format), [long](#create-an-fqdn-using-long-format), or [wildcard](#use-wildcard-format) format.
* In response, the External Hostname Controller creates a corresponding record in the `.coreweave.app` domain, which you can inspect with [kubectl](#view-the-allocated-record).

> [!WARNING]
>
> **Update (August 25, 2025)**
>
> The controller's handling of the annotation changed as follows:
>
> * **Before August 25, 2025:** The controller mutated the `service.beta.kubernetes.io/external-hostname` annotation to [long](#create-an-fqdn-using-long-format) format if you specified it in [short](#create-an-fqdn-using-short-format) format.
>
> * **Now:** The controller no longer mutates the annotation. Instead, the controller sets the FQDN and its allocation status in the `.status.conditions` field on the Service object, specifically under the `ExternalRecords` type.
>
> You don't need to change your manifests or annotations. Only [the method for retrieving the name](#view-the-allocated-record) has changed. Both [short](#create-an-fqdn-using-short-format) and [long](#create-an-fqdn-using-long-format) formats are still acceptable in the annotation.

## Create an FQDN using short format

To create a public FQDN for a `LoadBalancer` Service, set the `service.beta.kubernetes.io/external-hostname` annotation in your manifest with the desired hostname.

This manifest uses the short format to create the hostname `foo` for the `LoadBalancer` Service. The `service.beta.kubernetes.io/external-hostname` and `service.beta.kubernetes.io/coreweave-load-balancer-type` annotations control the FQDN allocation.

```yaml title="loadbalancer-with-DNS-example.yaml" highlight={5-6} theme={"system"}
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/external-hostname: foo
    service.beta.kubernetes.io/coreweave-load-balancer-type: public
  name: example-sshd
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  ports:
    - name: sshd
      port: 22
      protocol: TCP
      targetPort: sshd
  selector:
    app.kubernetes.io/name: sshd
```

The Service's FQDN follows this pattern, combining the hostname, the organization's [Org ID](https://docs.coreweave.com/security/authn-authz/orgs-users.md#organization-ids), and the cluster name:

```text theme={"system"}
[HOSTNAME].[ORG-ID]-[CLUSTER-NAME].coreweave.app
```

For example, assume the following values:

* An Org ID of `abc123`
* A cluster named `mycluster`
* An annotation of `service.beta.kubernetes.io/external-hostname` set to `foo`

The preceding manifest creates this FQDN:

```text theme={"system"}
foo.abc123-mycluster.coreweave.app
```

## Create an FQDN using long format

You can set the annotation using the long format (full FQDN) only if it exactly follows the preceding pattern and matches the Org ID and cluster name.

For Org ID `abc123` and cluster `mycluster`, these two hostname formats produce the same FQDN:

| `external-hostname` annotation | Format | FQDN |
| - | - | - |
| `foo` | Short format | `foo.abc123-mycluster.coreweave.app` |
| `foo.abc123-mycluster.coreweave.app` | Long format | `foo.abc123-mycluster.coreweave.app` |

However, if the Org ID and cluster name in the annotation don't match the actual values, the controller treats the annotation as short format.

Consider this erroneous scenario with the following values:

* Org ID `abc123`
* Cluster `mycluster`
* Annotation set to `foo.xyz456-mycluster.coreweave.app`

Because the Org ID in the annotation (`xyz456`) doesn't match the actual Org ID (`abc123`), the controller treats the entire annotation as short format.

The resulting FQDN is `foo.xyz456-mycluster.coreweave.app.abc123-mycluster.coreweave.app`, which is unintended.

## Use wildcard format

To create a wildcard DNS record for a `LoadBalancer` Service, set the `service.beta.kubernetes.io/external-hostname` annotation to `*`.

The controller creates a wildcard DNS record for the Service in the format `*.abc123-mycluster.coreweave.app`.

```yaml title="loadbalancer-wildcard-example.yaml" highlight={5-6} theme={"system"}
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/external-hostname: "*"
    service.beta.kubernetes.io/coreweave-load-balancer-type: public
  name: example-sshd
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  ports:
    - name: sshd
      port: 22
      protocol: TCP
      targetPort: sshd
  selector:
    app.kubernetes.io/name: sshd
```

## Secure the endpoint with TLS

Assigning a public DNS name to a Service doesn't automatically issue a TLS certificate. To secure the endpoint, use [`cert-manager`](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager) to obtain and manage a certificate for the FQDN or wildcard record.

## Add TLS to your DNS name

To serve HTTPS on the DNS name from this page, route traffic through a Traefik Ingress and let `cert-manager` issue the certificate. Traefik terminates TLS at the Ingress, so you don't expose each backend Service directly. This section combines the FQDN you allocate earlier with a `cert-manager`-issued certificate.

> [!WARNING]
>
> Let's Encrypt limits new certificates for `.coreweave.app` names to 50 per 168 hours, shared across all CoreWeave customers. To avoid failed issuance, request one wildcard certificate per cluster instead of one certificate per hostname, and keep hostnames stable so renewals stay exempt from the limit. See [Why am I seeing "too many certificates already issued for coreweave.app"?](https://docs.coreweave.com/support/cks/articles/why-am-i-seeing-too-many-certificates-errors-for-coreweave-app)

### Prerequisites

Before you add TLS, deploy the following charts to your cluster:

* Deploy CoreWeave's [Traefik](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md) chart so Traefik can serve as the `IngressClass` and route to Ingress hosts in the cluster.
* Deploy CoreWeave's [cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) chart and enable its `cert-issuers` subchart so a `ClusterIssuer` such as `letsencrypt-prod` exists. The bundled Let's Encrypt `ClusterIssuer` uses a `DNS01` challenge, so it can issue certificates for `.coreweave.app` names without a temporary public-facing Ingress.

### Create the Ingress

Set the host on the Ingress to the FQDN that this page allocates, and set the `cert-manager.io/cluster-issuer` annotation to the `ClusterIssuer` you want to use. The following manifest uses the host `ingress1.myorg-mycluster.coreweave.app` in both the `rules` and `tls` sections. Replace it in both places with the FQDN for your own Org ID and cluster name.

```yaml title="ingress-tls-example.yaml" highlight={6,12,22-26} theme={"system"}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    # This value must match a ClusterIssuer that exists in your cluster
    cert-manager.io/cluster-issuer: letsencrypt-prod
  name: ingress1
  namespace: namespace1
spec:
  ingressClassName: traefik
  rules:
  - host: ingress1.myorg-mycluster.coreweave.app
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
    - ingress1.myorg-mycluster.coreweave.app
    # cert-manager creates this secret for you
    secretName: ingress1-tls
```

`cert-manager` detects the `tls` block, requests a certificate for the host from the `ClusterIssuer`, and stores it in the `ingress1-tls` Secret. For more detail on this manifest and Traefik's Ingress behavior, see [Traefik](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md).

### Verify the DNS name, Ingress, and certificate

Confirm each piece in turn.

Confirm the DNS name resolved for the Traefik Service:

```bash theme={"system"}
kubectl get svc traefik -n traefik -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
```

Confirm the Ingress has an address and the expected host:

```bash theme={"system"}
kubectl describe ingress ingress1 -n namespace1
```

Confirm the certificate is issued and ready. The `Certificate` resource shows `Ready` once `cert-manager` completes the challenge:

```bash theme={"system"}
kubectl get certificate ingress1-tls -n namespace1
```

Example output:

```text theme={"system"}
NAME           READY   SECRET         AGE
ingress1-tls   True    ingress1-tls   2m
```

If the certificate stays `False`, inspect the `cert-manager` resources it creates to track the request:

```bash theme={"system"}
kubectl describe certificate ingress1-tls -n namespace1
```

## View the allocated record

To view the allocated FQDN for a Service, inspect the Service status conditions:

```bash theme={"system"}
kubectl get svc [MY-SERVICE] -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
```

Replace `[MY-SERVICE]` with the name of your Service, such as `example-sshd` from the example manifest.

## Observe the allocation through events and status

Beyond retrieving the FQDN itself, you can inspect Service events and status conditions to confirm that allocation succeeded or to diagnose problems. Services expose events and status conditions with information about DNS record allocation.

To view events and status conditions for a Service named `[MY-SERVICE]`:

```bash theme={"system"}
kubectl describe svc [MY-SERVICE]
```

The output includes:

```text theme={"system"}
Events:
  Type     Reason               Age   From                          Message
  ----     ------               ----  ----                          -------
  Normal   IPAMIPAllocationSet  3s    ipamOperator                  IPAllocation created for Service: example-sshd
  Warning  DomainNotAllowed     3s    external-hostname-controller  Domain foo is not allowed, appending orgid-cluster-name.coreweave.app
  Normal   DNSRecordUpdated     3s    external-hostname-controller  Updated DNS record for service default/example-sshd
```

To see the status conditions for the Service, look for the `status.conditions` field in the output:

```bash theme={"system"}
kubectl get svc [MY-SERVICE] -o yaml
```

The output includes:

```yaml theme={"system"}
status:
  conditions:
  - lastTransitionTime: "2025-08-18T16:07:35Z"
    message: successfully created ip allocations
    reason: IPAllocationSuccess
    status: "True"
    type: CoreWeaveLoadBalancerReady
  - lastTransitionTime: "2025-08-18T16:07:35Z"
    message: foo.orgid-cluster-name.coreweave.app
    reason: EndpointsUpdated
    status: "True"
    type: ExternalRecords
  - lastTransitionTime: "2025-08-18T16:07:35Z"
    message: 12.34.56.78
    reason: EndpointsUpdated
    status: "True"
    type: ExternalTargets
```

If any errors occur during record allocation, the controller reflects them in an event:

```text theme={"system"}
Events:
  Type     Reason               Age              From                          Message
  ----     ------               ----             ----                          -------
  Warning  HostnameConflict     1s (x2 over 1s)  external-hostname-controller  Skipping record creation - conflicting hostname orgid-cluster-name.coreweave.app found in service: default/example-sshd
```

The controller also creates a corresponding `False` status condition:

```yaml theme={"system"}
status:
  conditions:
  - lastTransitionTime: "2025-08-18T16:13:54Z"
    message: ""
    reason: EndpointsUpdated
    status: "False"
    type: ExternalRecords
  - lastTransitionTime: "2025-08-18T16:13:54Z"
    message: ""
    reason: EndpointsUpdated
    status: "False"
    type: ExternalTargets
```
