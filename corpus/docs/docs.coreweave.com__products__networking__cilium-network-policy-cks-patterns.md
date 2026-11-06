# Cilium network policy on CKS: cluster-specific patterns

Source: https://docs.coreweave.com/products/networking/cilium-network-policy-cks-patterns

# Cilium network policy on CKS: cluster-specific patterns

> Apply Cilium network policies on CKS without breaking platform access to DNS, the API server, and toFQDN rules

This page covers the CKS-specific rules you must follow when you deploy Cilium network policies, so that your policies don't accidentally block platform access. New CKS clusters run Cilium as the Container Network Interface (CNI), and several details differ from the generic Cilium examples you find online. A small number of older clusters created before Cilium became the default still run Calico; the patterns on this page apply to Cilium clusters. Apply these patterns whether you use a Kubernetes `NetworkPolicy`, a `CiliumNetworkPolicy` (CNP), or a `CiliumClusterwideNetworkPolicy` (CCNP).

For a step-by-step tutorial on a default-deny policy with a targeted allow rule, see [Deploy network policies with CKS](https://docs.coreweave.com/security/tutorials/deploying-network-policies.md). This page is the reference for the cluster-specific pitfalls that the tutorial summarizes.

## Allow the CoreWeave platform services CIDR

A default-deny policy must allow egress to the CoreWeave platform services CIDR `100.124.0.0/18`, or it breaks `kubectl` access and DNS. The [Deploy network policies with CKS](https://docs.coreweave.com/security/tutorials/deploying-network-policies.md) tutorial covers the rationale. The Cilium-specific detail is the syntax: Add the CIDR to your egress allow rules with `toCIDR`, and allow the whole range rather than enumerating ports, because specific ports within the range can change over time.

```yaml theme={"system"}
egress:
  - toCIDR:
      - 100.124.0.0/18
```

## Target node-local-dns for DNS egress, not kube-dns

CKS serves in-cluster DNS from the `node-local-dns` DaemonSet, not the standard `kube-dns` Service, so generic Cilium examples that target `kube-dns` don't work. Use the `node-local-dns` endpoint selector with the Cilium label format:

```yaml theme={"system"}
egress:
  - toEndpoints:
      - matchLabels:
          k8s:k8s-app: node-local-dns
          k8s:io.kubernetes.pod.namespace: kube-system
```

Two Cilium-specific mistakes break this rule:

* Omitting the `k8s:` prefix. Cilium network policies require the `k8s:` prefix on Kubernetes labels, so `k8s-app: node-local-dns` doesn't match. Use `k8s:k8s-app: node-local-dns`.
* Targeting a CoreDNS ClusterIP directly instead of the `node-local-dns` endpoints.

## Roll out with audit mode first

Cilium audit mode logs policy violations without enforcing them, so you can validate a policy against real traffic before you enforce it. CoreWeave manages Cilium on CKS, and you configure it through the `cilium-config` ConfigMap. Enable audit mode:

```bash theme={"system"}
# Enable Cilium policy audit mode. Logs violations without enforcing them.
kubectl -n cw-cilium-system patch configmap cilium-config \
  --type merge --patch '{"data":{"policy-audit-mode":"true"}}'
```

Cilium doesn't hot-reload the ConfigMap. After you patch it, restart the Cilium DaemonSet so the change takes effect:

```bash theme={"system"}
# Reload Cilium configuration. Should not disrupt running workloads,
# but may briefly delay the start of new Pods during the rollout.
kubectl -n cw-cilium-system rollout restart ds/cilium
```

Audit mode doesn't take effect until the agents reload. Reading the config value back doesn't confirm that the running agents have reloaded. Only a rollout restart applies the change.

## toFQDN policies require an L7 feature flag

Egress rules that match on a fully qualified domain name (FQDN), such as allowing traffic only to `*.example.com`, use Cilium's Layer 7 (L7) DNS proxy. On CKS, the L7 DNS proxy depends on the `enable-bpf-tproxy` setting being `false` in the `cilium-config` ConfigMap, which isn't the default. Because CoreWeave manages the Cilium configuration, you can't change this yourself. Open a support ticket to request `enable-bpf-tproxy=false` for your cluster. A Cilium DaemonSet rollout restart is required after CoreWeave applies the change.

Applying a `toFQDN` policy before this flag is set can break DNS resolution entirely rather than only filtering by FQDN. If your `toFQDN` policy isn't working, confirm the feature flag before you pursue other debugging.

## Validate policies with Hubble

Hubble provides real-time network flow visibility, which is the most direct way to see why a policy allows or drops a flow. Hubble isn't enabled by default on CKS clusters. To enable it, open a support ticket. Enabling Hubble triggers a Cilium agent rollout, and it increases resource consumption, so monitor your cluster after you enable it.

If you're enabling Hubble specifically to debug why a `toFQDN` policy isn't working, check the L7 feature flag first. The most common cause is the `enable-bpf-tproxy` setting, not a problem that Hubble would reveal.

## Choose between CNP and CCNP

The two Cilium policy types differ in scope:

* A `CiliumNetworkPolicy` (CNP) is namespaced and applies to Pods in one namespace.
* A `CiliumClusterwideNetworkPolicy` (CCNP) applies across the whole cluster.

Use a CCNP for baseline rules that should apply everywhere, such as a cluster-wide default-deny with the platform CIDR and DNS allowances. Use a CNP for application-specific rules within a namespace.

## Recommended rollout sequence

Follow this rollout sequence:

1. Start with a policy in a single namespace.
2. Enable audit mode and apply the policy, so violations are logged but not enforced.
3. Use Hubble to confirm the policy matches the traffic you expect.
4. Expand to cluster-wide policies once you're confident.
5. Always allow the platform services CIDR `100.124.0.0/18` and target `node-local-dns` for DNS.

## Related pages

* [Deploy network policies with CKS](https://docs.coreweave.com/security/tutorials/deploying-network-policies.md): step-by-step default-deny tutorial.
* [Networking support articles](https://docs.coreweave.com/support/networking.md): help for connectivity and DNS problems on CKS.
* [LoadBalancer Services: in-cluster vs external reachability](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md): reachability diagnostics.
* [eBPF observability](https://docs.coreweave.com/security/tutorials/ebpf-observability.md): deeper flow and runtime observability.
