# Expose a Service

Source: https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns

# Expose a Service

> Use a LoadBalancer Service to expose Pods on CKS to the public Internet

This page explains how to expose Pods running on CoreWeave Kubernetes Service (CKS) to the public Internet by creating a `LoadBalancer` Service. Use this approach when you need workloads in your cluster to be reachable from outside the cluster over a public IPv4 address, and optionally a public DNS name.

One way to expose Pods on CKS to the public Internet is to use a [`LoadBalancer` Service](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer). These Services expose Pods to the Internet through public IPv4 addresses. You can also assign public DNS names to them.

## HTTP and HTTPS quickstart

Choose the approach that matches the traffic you need to expose:

* **Plain TCP, or HTTP without edge TLS:** use a **`LoadBalancer` Service**, which exposes a Pod over a public IPv4 address on any TCP or UDP port. Use this for plain TCP workloads such as SSH, or for HTTP services that don't need TLS termination at the edge. The [`LoadBalancer` Service manifest](#create-the-manifest) on this page covers the HTTP case: set `port` and `targetPort` to your application's HTTP port instead of the SSH port shown.
* **HTTP or HTTPS routed by hostname, with TLS termination:** use a **Traefik Ingress**, which routes traffic by hostname with TLS termination. Traefik terminates TLS using a certificate that `cert-manager` issues, so you don't expose each backend Service directly. For setup, see [Traefik](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md) and [Cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md). To assign a stable public DNS name, see [Create a public DNS name](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md).

The rest of this page walks through the `LoadBalancer` Service.

## Create a Load Balancer Service

To expose your Pods, you must create a `LoadBalancer` Service manifest and deploy it to your cluster. The following sections walk through each part of that process.

### Create the manifest

To create a Service of `type: LoadBalancer`, deploy a Service manifest onto CKS. The following sample manifest defines a `LoadBalancer` Service that exposes an `sshd` Pod on port 22:

```yaml title="loadbalancer-example.yaml" highlight={5,8} theme={"system"}
apiVersion: v1
kind: Service
metadata:
  annotations:
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

In the preceding example:

* The Service (`example-sshd`) is configured as `type: LoadBalancer`.
* The `coreweave-load-balancer-type` annotation is `public`.

This creates a publicly accessible Load Balancer Service.

> [!NOTE]
>
> The public address assigned to the Service comes from CoreWeave's public LoadBalancer address pool for the Region and remains stable for the lifetime of the Service. This pool is separate from the Region's NAT egress range, which governs only outbound traffic.

### Deploy the manifest

After you save the manifest, apply it to your cluster so that CKS provisions the Load Balancer. Apply the manifest with `kubectl`. For example:

```bash theme={"system"}
kubectl apply -f example-sshd.yaml
```

### Locate the IPv4 address

After you deploy the Service, you need its assigned public IPv4 address to reach the Pods from outside the cluster. After you apply the manifest, use `describe` to see the deployed Service. For example:

```bash theme={"system"}
kubectl describe services example-sshd
```

Find the assigned public IPv4 address under the `LoadBalancer Ingress` field. With this address, the Pods that the Service selects are now reachable from the public Internet on the ports that the manifest defines.

> [!NOTE]
>
> For more information, see [the official Kubernetes documentation](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#finding-your-ip-address).

## Choose public or private addressing

The `service.beta.kubernetes.io/coreweave-load-balancer-type` annotation controls whether the Service gets a public or a private address:

* `public`: assigns an internet-facing public IP from the Region's public LoadBalancer pool. Use this when external clients must reach the Service.
* Annotation absent: assigns a private (RFC 1918) address. This address is reachable from within the cluster, and over a connected VPC or Direct Connect, but not from the public Internet.

Don't set the value to `internal`. CoreWeave doesn't recognize `internal` as a value, and a Service with that value can stay in `<Pending>` indefinitely. To request a private address, omit the annotation entirely.

## Pin a Service to an address pool

On clusters with multiple LoadBalancer address pools, the first pool is the default and Services allocate from it automatically. To allocate from a non-default pool, add the address-pool label to the Service. Replace `[POOL-NAME]` with the name of the address pool:

```yaml theme={"system"}
metadata:
  labels:
    lb.coreweave.com/address-pool: "[POOL-NAME]"
```

If a Service requests a specific IP from a non-default pool without this label, the Service reports `pool_selector_mismatch` and the condition `cilium.io/IPAMRequestSatisfied: False`. Add the `lb.coreweave.com/address-pool` label that selects the pool containing the IP.

To request a specific IP, use the Cilium annotation. Replace `[SPECIFIC-IP]` with the IP address you want to assign:

```yaml theme={"system"}
metadata:
  annotations:
    lbipam.cilium.io/ips: "[SPECIFIC-IP]"
```

A single Service can't statically assign both an IPv4 and an IPv6 address from named pools. For dual-stack static addressing, create one Service per IP family.

Some early clusters use a legacy MetalLB pool selected with the `metallb.universe.tf/address-pool: public` annotation. On those clusters, if the dedicated pool is exhausted, you can switch a Service to the shared pool by replacing that annotation with `service.beta.kubernetes.io/coreweave-load-balancer-type: public`.

### LoadBalancer IP stability

A LoadBalancer Service IP is pinned for the lifetime of the Service object. The following actions release the IP, with no guarantee that you get the same address back:

* Deleting the Service.
* Changing the Service type away from `LoadBalancer`.
* Removing the `coreweave-load-balancer-type: public` annotation from a public Service.

If you need a stable address, keep the Service object in place.

## Layer 4 and Layer 7 traffic

CoreWeave LoadBalancer Services operate at Layer 4 (TCP and UDP). For Layer 7 features such as path-based routing or TLS termination, run an ingress controller such as Traefik behind the LoadBalancer.

## Troubleshoot an unreachable service

If the Service doesn't respond after you deploy it, check the following:

* **No external IP yet.** Run `kubectl describe services example-sshd` and confirm the `LoadBalancer Ingress` field shows an address. CKS assigns the address from the Region's public LoadBalancer address pool. If the field is empty, the Load Balancer is still provisioning. Confirm the `service.beta.kubernetes.io/coreweave-load-balancer-type: public` annotation is present so the Service requests a public address.
* **Wrong `externalTrafficPolicy`.** With `externalTrafficPolicy: Local`, traffic only reaches Nodes that run a Pod the Service selects. Confirm the Service `selector` matches your Pod labels and that at least one selected Pod is running and `Ready`. If no selected Pod runs on a Node, that Node drops the traffic.
* **DNS not resolved.** If you assigned a public DNS name, the fully qualified domain name (FQDN) can take time to propagate. Confirm the record resolves before you rely on it, and retrieve the allocated name from the Service status. For details, see [Create a public DNS name](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md).

## Troubleshoot in-cluster versus external reachability

If the LoadBalancer IP works from inside the cluster but external clients can't reach it, the cause is usually that the Service has a private address when it needs a public one, or a platform-side route advertisement issue. Test the same IP from a Pod and from outside the cluster, then match your result to the discriminator table.

Test from inside the cluster. Replace `[LB-IP]` and `[PORT]` with the LoadBalancer's IP address and port:

```bash theme={"system"}
# Run a temporary client Pod and curl the LoadBalancer IP.
# Safe to run; creates and deletes a short-lived Pod.
kubectl run lb-test --rm -it --image=curlimages/curl --restart=Never -- \
  curl -sv --max-time 10 http://[LB-IP]:[PORT]
```

Test from outside the cluster, for example from your laptop:

```bash theme={"system"}
# Replace with your LoadBalancer IP and port.
curl -sv --max-time 10 http://[LB-IP]:[PORT]
```

| In-cluster result | External result | What it means | What to do |
| - | - | - | - |
| Fails | Fails | Application or Service problem | Confirm the Service is `type: LoadBalancer`, that backing Pods are `Ready`, that endpoints exist, and that no NetworkPolicy blocks the traffic. |
| Works | Fails | The Service expects a public address but is not externally routable | Confirm the `coreweave-load-balancer-type: public` annotation is present and the IP is from the public pool. If both are correct, this is a platform-side routing issue: open a support ticket. |
| Fails | Works | Unusual | Usually an endpoint or selector mismatch affecting in-cluster routing. Recheck the Service selector and endpoints. |
