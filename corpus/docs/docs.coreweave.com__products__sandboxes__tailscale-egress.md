# Reach a tailnet service from a sandbox

Source: https://docs.coreweave.com/products/sandboxes/tailscale-egress

# Reach a tailnet service from a sandbox

> Route sandbox egress through a Tailscale proxy to reach a service that only exists on your tailnet.

Tailscale cluster egress lets a sandbox on your own CoreWeave Kubernetes Service (CKS) cluster connect to a device on your tailnet. Examples include an internal API, a database in your corporate network, and a model server on a workstation. The Tailscale Kubernetes Operator publishes the tailnet device as a Kubernetes Service. A sandbox egress rule grants the sandbox access to the proxy behind that Service.

This page is for administrators who run a managed sandbox runner on a CKS cluster. The example uses standalone egress, with the operator installed in the `tailscale` Namespace. The following platform behaviors shape the configuration:

* Exposing an in-cluster Service through the Tailscale operator lets tailnet devices connect to it. Outbound connections from a Pod to a tailnet device require [Tailscale's cluster egress feature](https://tailscale.com/kb/1438/kubernetes-operator-cluster-egress).
* Sandbox egress rules are allow-only over a default-deny baseline, and `EgressRule(any=True)` excludes cluster-internal addresses. An in-cluster destination such as a Tailscale proxy is reachable only through a `selector` or `tenant` rule.

## Prerequisites

Before you begin, you need the following:

* A CKS cluster with a managed sandbox runner whose `installStatus` is `RUNNER_INSTALL_STATUS_READY`. See [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md).
* The Tailscale Kubernetes Operator installed on that cluster, with your tailnet policy file configured for CKS.
* The MagicDNS name of the tailnet device you want to reach, such as `db-host.TAILNET_NAME.ts.net`, and the port your service listens on.
* A runner policy that permits this selector egress rule. An `any` entitlement never covers selectors. A policy with a nonempty `allowed_egress` must carry a `selector` entitlement that matches in form: it must also set `namespace_labels`. Its labels must be a subset of the ones the sandbox declares, and its port filter must cover TCP port `8080`. See [`SelectorBlock`](https://docs.coreweave.com/products/sandboxes/reference/profile#selectorblock).
* The `cwsandbox` Python software development kit (SDK) configured with [credentials for CKS placement](https://docs.coreweave.com/products/sandboxes/placement.md), and a sandbox image with `curl` and `getent` installed.
* `kubectl` access to create or update Services in the `default` Namespace and list Pods in the operator's Namespace.
* A tailnet policy that allows the egress proxy to connect to the target device and application port.

## Create a Tailscale egress Service

Create an `ExternalName` Service annotated with the tailnet device's MagicDNS name. The operator creates a proxy Pod and a headless Service in its own Namespace, then points the `ExternalName` Service at that headless Service. The examples use `tailscale`, as in the linked installation guide. If you installed the operator in another Namespace, update the commands and `namespace_labels` in the examples in this guide.

Replace `TAILNET_FQDN` with the device's MagicDNS name. This example creates the Service in `default` and uses its fully qualified DNS name so sandboxes can connect from other Namespaces. It assumes an HTTP service on port `8080` with a `/health` endpoint. Adjust the port and path for your service.

```yaml title="tailnet-egress.yaml" theme={"system"}
apiVersion: v1
kind: Service
metadata:
  name: internal-api
  namespace: default
  annotations:
    tailscale.com/tailnet-fqdn: "TAILNET_FQDN"
spec:
  type: ExternalName
  externalName: placeholder.tailscale.internal # Required by Kubernetes, overwritten by the operator
```

```bash theme={"system"}
kubectl apply -f tailnet-egress.yaml
```

Sandboxes connect to `internal-api.default.svc.cluster.local:8080`. The short name `internal-api:8080` works only from the Service's Namespace. If your cluster uses a DNS suffix other than `cluster.local`, replace that suffix in the examples.

Confirm that the operator created the proxy Pod:

```bash theme={"system"}
kubectl get pods -n tailscale \
  -l 'tailscale.com/parent-resource=internal-api,tailscale.com/parent-resource-ns=default'
```

Wait until the proxy is ready. Example output (the generated Pod name varies):

```text title="Example output" theme={"system"}
NAME                     READY   STATUS    RESTARTS   AGE
ts-internal-api-k4x7p-0  1/1     Running   0          32s
```

## Grant the sandbox egress to the proxy

Select the proxy Pod by label in an `EgressRule`. The rule requires both label sets:

* `pod_labels` identifies the proxy by the Service it fronts, through the operator's `tailscale.com/parent-resource` and `tailscale.com/parent-resource-ns` labels. Include the Namespace label so the rule doesn't also match a proxy for a same-named Service in another Namespace.
* `namespace_labels` selects the `tailscale` Namespace. Without it, the rule applies only to the sandbox's own Namespace and doesn't reach a proxy in another Namespace.

Set `ports` to the same port the service listens on. Replace `RUNNER_ID` with the ID of the runner on the cluster where you created the Service. Without `runner_ids`, CKS placement can use any eligible runner in your organization, including one on a cluster without the proxy.

```python theme={"system"}
from cwsandbox import EgressRule, NetworkOptions, Sandbox, SelectorBlock

tailscale_egress = EgressRule(
    selector=SelectorBlock(
        pod_labels={
            "tailscale.com/parent-resource": "internal-api",
            "tailscale.com/parent-resource-ns": "default",
        },
        namespace_labels={"kubernetes.io/metadata.name": "tailscale"},
    ),
    ports=[8080],
)

with Sandbox.run(
    placement_mode="cks",
    runner_ids=["RUNNER_ID"],
    network=NetworkOptions(egress=[tailscale_egress]),
) as sandbox:
    result = sandbox.exec([
        "curl", "-sS", "--include", "--max-time", "15",
        "http://internal-api.default.svc.cluster.local:8080/health",
    ]).result()
    print(result.stdout)
    print(result.stderr)
```

These selectors and ports are for standalone egress. An egress `ProxyGroup` uses shared proxy Pods and remaps ports, so this rule isn't a complete configuration for that mode. See [Tailscale's high-availability egress guide](https://tailscale.com/docs/kubernetes-operator/egress#high-availability-ha-egress).

Cluster DNS stays reachable unless the runner policy denies DNS egress on the `dns_egress` constraint, so the sandbox resolves the Service name without an additional rule.

## Verify the connection

The example prints the HTTP response headers and body, plus any `curl` errors. For a health endpoint that returns status `200`, expect a status line such as `HTTP/1.1 200 OK` followed by the service's health response. An HTTP error such as `401` or `404` shows that an HTTP server responded. Check application authentication or the requested path.

A timeout or connection error can occur between the sandbox and proxy, between the proxy and tailnet device, or at the application. To check DNS and the HTTP exchange separately, run this diagnostic example with your runner ID:

```python theme={"system"}
from cwsandbox import EgressRule, NetworkOptions, Sandbox, SelectorBlock

tailscale_egress = EgressRule(
    selector=SelectorBlock(
        pod_labels={
            "tailscale.com/parent-resource": "internal-api",
            "tailscale.com/parent-resource-ns": "default",
        },
        namespace_labels={"kubernetes.io/metadata.name": "tailscale"},
    ),
    ports=[8080],
)

with Sandbox.run(
    placement_mode="cks",
    runner_ids=["RUNNER_ID"],
    network=NetworkOptions(egress=[tailscale_egress]),
) as sandbox:
    dns_result = sandbox.exec([
        "getent", "hosts", "internal-api.default.svc.cluster.local",
    ]).result()
    print(dns_result.stdout)
    print(dns_result.stderr)
    http_result = sandbox.exec([
        "curl", "-sv", "--max-time", "15", "-o", "/dev/null",
        "http://internal-api.default.svc.cluster.local:8080/health",
    ]).result()
    print(http_result.stderr)
```

A successful DNS lookup prints at least one address. In the `curl` output, look for a connection to the proxy address and an HTTP response status. DNS success alone doesn't confirm that the proxy can reach the target.

## Troubleshoot

| Symptom | Possible cause | Fix |
| - | - | - |
| Create fails on the egress rule | A nonempty `allowed_egress` doesn't cover the selector's labels, Namespace labels, or requested ports. | Have the policy administrator permit the selector with matching Namespace form, a subset of the declared labels, and a port filter covering TCP `8080`. |
| The name doesn't resolve | The DNS name has the wrong Namespace or cluster suffix, the operator hasn't configured the Service yet, or DNS egress is denied. | Check the Service's `externalName`, use the full Service name, and check the runner's DNS egress policy. |
| The name resolves but the connection times out | The rule selects the wrong Pods or Namespace, the tailnet policy blocks the target, or the target isn't listening. | Check the proxy's labels and Namespace, tailnet access rules, and the target application's address and port. |
| The connection works on one port only | The egress rule's `ports` list omits the other ports. | Add the missing ports to the egress rule. |
| No proxy Pod appears in the `tailscale` Namespace | The operator is installed in another Namespace, reconciliation failed, or its credentials or tags aren't authorized. | Check the operator Namespace and logs, then see [Configure operator tags](https://docs.coreweave.com/products/cks/auth-access/tailscale-operator.md#configure-operator-tags). |

## Related pages

For related guidance, see the following pages:

* [Deploy the Tailscale Kubernetes Operator](https://docs.coreweave.com/products/cks/auth-access/tailscale-operator.md): deploy and configure the operator on CKS.
* [Network rules](https://docs.coreweave.com/products/sandboxes/client/ref/networking/network-rules.md): the full `EgressRule` and `SelectorBlock` reference.
* [Policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile.md): the policy entitlements a declared egress rule must fit inside.
* [Public endpoints](https://docs.coreweave.com/products/sandboxes/public-endpoints.md): give a service inside a sandbox a public address.
