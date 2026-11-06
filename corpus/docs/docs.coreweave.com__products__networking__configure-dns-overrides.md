# Configure DNS overrides on CKS

Source: https://docs.coreweave.com/products/networking/configure-dns-overrides

# Configure DNS overrides on CKS

> Add DNS forwarders and hostname mappings, preserve managed entries, and verify configuration reloads.

The `node-local-dns-overrides` ConfigMap lets you customize DNS resolution for Pods on CoreWeave Kubernetes Service (CKS). Use it to forward a private domain to your own resolvers or map a hostname to a specific IP address. You manage the override entries, and CoreWeave manages the DNS components that read them.

## Prerequisites

Before you update DNS overrides, you need:

* A configured [`kubectl` connection to your CKS cluster](https://docs.coreweave.com/products/cks/auth-access/managed-auth/kubeconfig).
* Kubernetes permissions to read and update the `node-local-dns-overrides` ConfigMap in `kube-system`, read `node-local-dns` Pod logs, and execute commands in your test Pod.
* For DNS forwarding, the IP addresses of upstream resolvers reachable from the cluster, such as through [CoreWeave Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md) or a [virtual private cloud (VPC)](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md).
* A test Pod with `nslookup` installed that uses cluster DNS. Use `dnsPolicy: ClusterFirst`, or `ClusterFirstWithHostNet` for a Pod with `hostNetwork: true`.

If network policies restrict DNS traffic, follow [Cilium network policy on CKS](https://docs.coreweave.com/products/networking/cilium-network-policy-cks-patterns.md#target-node-local-dns-for-dns-egress-not-kube-dns) to allow DNS egress to `node-local-dns`.

## Choose an override entry

Add entries to the ConfigMap's `data` field. The suffix of each key determines where CoreDNS imports the configuration:

| Key suffix | Purpose | Example |
| - | - | - |
| `.server` | Adds a CoreDNS server block for a DNS zone. | Forward `corp.example.com` to private resolvers. |
| `.include` | Adds directives inside the main `.` zone. | Add a `hosts` directive to map a hostname to an IP address. |

Preserve `placeholder.server` and `placeholder.include` exactly as they appear in the live ConfigMap. The platform reconciles these reserved entries and overwrites custom configuration stored under either key. Use distinct names for your own entries, such as `corp-example-com.server` or `custom-hosts.include`.

Every custom server block on port `53` must include `bind 0.0.0.0`, matching the managed server blocks. Mixing blocks with and without `bind` can create competing listeners and cause intermittent DNS failures, including `REFUSED` responses for unrelated domains. See the [CoreDNS bind plugin documentation](https://coredns.io/plugins/bind/#avoiding-listener-contention).

Use the override ConfigMap for your DNS customizations. Leave the managed `node-local-dns` configuration unchanged, and preserve cluster-internal zones such as `cluster.local` for Service discovery.

Start from the live ConfigMap so you preserve existing overrides and platform-managed entries:

1. Inspect the current configuration:

   ```bash theme={"system"}
   kubectl get configmap node-local-dns-overrides -n kube-system -o yaml
   ```

2. Edit the ConfigMap:

   ```bash theme={"system"}
   kubectl edit configmap node-local-dns-overrides -n kube-system
   ```

3. Add an entry to the existing `data` field using the [private-domain forwarding](#configure-private-domain-forwarding) or [hostname mapping](#configure-a-hostname-mapping) example. Replace the placeholders and keep all existing entries. The examples are `data` fragments, not complete ConfigMap manifests.

4. Save the ConfigMap, then [verify the configuration](#verify-the-configuration).

## Configure private-domain forwarding

To forward a private domain, add a `.server` entry. Replace `[PRIVATE-DOMAIN]` with the domain. Replace `[UPSTREAM-RESOLVER-1]` and `[UPSTREAM-RESOLVER-2]` with resolver IP addresses. List multiple resolvers on one `forward .` line. If you have only one resolver, use one address.

```yaml title="Private-domain forwarding: data fragment" theme={"system"}
data:
  corp-example-com.server: |
    [PRIVATE-DOMAIN]:53 {
      errors
      loop
      bind 0.0.0.0
      forward . [UPSTREAM-RESOLVER-1] [UPSTREAM-RESOLVER-2]
    }
```

To forward more than one domain, add another `.server` entry with a distinct key.

## Configure a hostname mapping

To map a hostname to an IP address, add a `.include` entry. Replace `[HOST-IP]` and `[HOSTNAME]` with the address and hostname. The `fallthrough` directive lets queries without a matching host entry continue through the existing DNS configuration.

```yaml title="Static hostname mapping: data fragment" theme={"system"}
data:
  custom-hosts.include: |
    hosts {
      [HOST-IP] [HOSTNAME]
      fallthrough
    }
```

The [CoreDNS hosts plugin](https://coredns.io/plugins/hosts/) can appear only once in a server block. If an existing `.include` entry already defines `hosts` in the main zone, add the mapping to that entry's `hosts` block.

## Optional: Manage overrides in version control

You can store the ConfigMap manifest in version control and apply it through your deployment workflow, such as Argo CD. Start with the live resource rather than create a replacement from a minimal example:

1. Export the ConfigMap:

   ```bash theme={"system"}
   kubectl get configmap node-local-dns-overrides -n kube-system -o yaml > node-local-dns-overrides.yaml
   ```

2. Prepare the manifest for version control. If present, remove server-generated metadata such as `uid`, `resourceVersion`, `creationTimestamp`, and `managedFields`. Preserve the resource name, namespace, platform labels, both placeholder entries, and existing overrides. Add or update your custom entries in `data`.

3. Review the change against the live configuration:

   ```bash theme={"system"}
   kubectl diff -f node-local-dns-overrides.yaml
   ```

4. Apply the reviewed manifest manually or through your deployment workflow. For a manual apply, run:

   ```bash theme={"system"}
   kubectl apply -f node-local-dns-overrides.yaml
   ```

Keep the version-controlled manifest aligned with the cluster's existing configuration. Configure your deployment workflow to preserve the platform-managed entries and other overrides. The ConfigMap already exists in the cluster. This procedure updates it in place.

For Argo CD, merge the following sync options into the ConfigMap's existing `metadata.annotations`:

```yaml title="Argo CD: metadata fragment" theme={"system"}
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false,Delete=false
```

`Prune=false` preserves the shared ConfigMap if you remove its manifest from the Application's source. `Delete=false` preserves it when you delete the Application. Preserve other annotations and sync options, and don't enable `Replace=true` or `Force=true` for this resource. See [Argo CD sync options](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/).

These sync options prevent deletion of the ConfigMap. They don't preserve individual entries during an update. Keep platform-managed entries and other overrides in the manifest.

## Verify the configuration

The CoreDNS process running inside each `node-local-dns` Pod imports the override entries and reloads changes automatically. A normal override update doesn't require a DaemonSet rollout restart. Allow time for the ConfigMap volume update and configuration reload. After you save the ConfigMap, some Nodes might still use the previous configuration.

1. Check the `node-local-dns` logs for reload messages and errors:

   ```bash theme={"system"}
   kubectl logs -n kube-system -l k8s-app=node-local-dns --tail=100 --prefix=true
   ```

2. Test the configured name from your test Pod. Replace `[POD-NAME]`, `[NAMESPACE]`, and `[HOSTNAME]` with your values. Use a fully qualified hostname with a trailing dot to avoid search-domain expansion:

   ```bash theme={"system"}
   kubectl exec [POD-NAME] -n [NAMESPACE] -- nslookup [HOSTNAME].
   ```

   For a forwarder, the answer should match the upstream resolver's record. For a static mapping, the answer should contain the configured IP address.

3. Confirm that unrelated DNS resolution still works:

   ```bash theme={"system"}
   kubectl exec [POD-NAME] -n [NAMESPACE] -- nslookup kubernetes.default.svc.cluster.local.
   kubectl exec [POD-NAME] -n [NAMESPACE] -- nslookup example.com.
   ```

The `node-local-dns` component runs on each Node. To check propagation across the cluster, repeat the tests from Pods on different Nodes.

## Troubleshoot an override

If the saved configuration doesn't produce the expected result, use the following checks:

| Symptom | What to check |
| - | - |
| Custom configuration disappears. | Move it out of `placeholder.server` or `placeholder.include` into a distinct key with the appropriate suffix. |
| Reload logs show a parsing or plugin error. | Check the entry suffix, CoreDNS syntax, and substituted values. A complete server block belongs in a `.server` entry, outside the main zone. |
| Queries intermittently return `REFUSED` after you add a zone. | Include `bind 0.0.0.0` in every custom server block on port `53`. A restart doesn't correct a missing directive. |
| A private name returns `SERVFAIL`. | Check reload errors and upstream resolver reachability. The response alone doesn't prove that the intended forwarder is active. |
| A private name returns `NXDOMAIN`. | Check that the zone matches the query, the entry has the correct suffix, and the upstream resolver has the requested record. |

If an override change causes failures, remove the custom entry or restore its previous value, preserve the placeholder entries, and repeat the verification steps. For broader DNS problems, see [Troubleshoot DNS resolution from a Pod](https://docs.coreweave.com/support/networking/articles/why-is-dns-resolution-failing-from-my-pod).

If failures persist, [contact CoreWeave Support](https://docs.coreweave.com/support.md). Include the override entry, queried hostname, resolver addresses, affected Pods and Nodes, lookup output, and reload logs. For other required details, see [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md).
