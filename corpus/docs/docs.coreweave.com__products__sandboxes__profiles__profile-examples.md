# Policy examples

Source: https://docs.coreweave.com/products/sandboxes/profiles/profile-examples

# Policy examples

> Five cluster policies for data science, agents, continuous integration (CI), and background workers.

This page collects five complete policies for common cluster postures, so you can start from a working document rather than build one from scratch.

A cluster has exactly one policy, so choose one example and adjust it for your cluster. Replace `GITHUB_ORG` in the image registry examples with your GitHub Container Registry organization or user name.

To apply an example, follow [Update a policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy). Read the current policy and its `etag` together, then prepare the complete policy document and submit it with the `etag` from that read. Replacing the root policy clears any omitted groups, so retain every setting you want to preserve.

## GPU data science cluster

A cluster for long-lived per-user work: generous compute, GPU Nodes, and internet access for pulling datasets and packages, with the instance metadata endpoint excluded.

```json title="policy.json" theme={"system"}
{
  "displayName": "Data science, GPU",
  "constraints": {
    "resources": {
      "defaultCpu": "4",
      "defaultMemory": "16Gi",
      "maxCpu": "16",
      "maxMemory": "128Gi",
      "maxGpuCount": "2",
      "requireLimits": true
    },
    "instance": { "allowedInstanceTypes": ["h100"] },
    "image": { "allowedRegistries": ["ghcr.io/GITHUB_ORG"] },
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "0.0.0.0/0", "except": ["169.254.169.254/32"] } }
      ],
      "defaultEgress": [
        { "cidr": { "cidr": "0.0.0.0/0", "except": ["169.254.169.254/32"] } }
      ]
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 86400 }
  }
}
```

This policy sets `cw-kata-qemu` as the default CPU runtime class and permits explicit runtime class pins only for `cw-kata-qemu`. For GPU sandboxes, leave `runtime_class` and `defaultGpuRuntimeClass` unset. Use it with the supported CoreWeave Kubernetes Service (CKS) GPU configuration described in [Run a GPU sandbox](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md#isolation-depends-on-the-placement-mode). GPU sandboxes in that configuration use `runc` without virtualization and must run only trusted code. Kata-based GPU runtime classes aren't supported on customer CKS clusters.

## Shared agent cluster with allowlisted egress

A multi-tenant cluster for agent workloads. Agents reach a fixed set of upstreams and each other within the organization, and nothing else.

```json title="policy.json" theme={"system"}
{
  "displayName": "Agents, allowlisted egress",
  "constraints": {
    "resources": {
      "defaultCpu": "1",
      "defaultMemory": "2Gi",
      "maxCpu": "4",
      "maxMemory": "8Gi",
      "requireLimits": true
    },
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "140.82.112.0/20" }, "ports": [{ "port": 443 }] },
        { "cidr": { "cidr": "151.101.0.0/16" }, "ports": [{ "port": 443 }] },
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ],
      "defaultEgress": [
        { "cidr": { "cidr": "140.82.112.0/20" }, "ports": [{ "port": 443 }] }
      ]
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 3600 }
  }
}
```

A sandbox that declares nothing gets the first classless inter-domain routing (CIDR) range only. A sandbox that needs to reach other sandboxes in the organization declares the tenant rule itself, and the policy permits it because the rule fits the envelope.

## Ephemeral CI cluster

Short-lived, small, and narrow. Sandboxes exist for the length of a test run.

```json title="policy.json" theme={"system"}
{
  "displayName": "CI",
  "constraints": {
    "resources": {
      "defaultCpu": "250m",
      "defaultMemory": "512Mi",
      "maxCpu": "2",
      "maxMemory": "4Gi",
      "requireLimits": true
    },
    "image": { "allowedRegistries": ["ghcr.io/GITHUB_ORG"] },
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "140.82.112.0/20" }, "ports": [{ "port": 443 }] }
      ],
      "defaultEgress": [
        { "cidr": { "cidr": "140.82.112.0/20" }, "ports": [{ "port": 443 }] }
      ]
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["gvisor"],
      "defaultCpuRuntimeClass": "gvisor",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 900 },
    "volumes": { "allowedMedia": ["STORAGE_MEDIUM_DISK"], "maxSize": "10Gi" }
  }
}
```

With the 15-minute default, a CI job that declares nothing self-terminates. The policy carries no lifetime cap. Requests above the platform maximum of 30 days are rejected at create time, and anything under it is allowed. Where a hard per-job bound matters, set `max_lifetime_seconds` on the create request.

## VM-isolated execution with no default egress

This policy requires virtual machine (VM) isolation, forbids GPU requests, and supplies no default egress rules. It blocks outbound DNS traffic on UDP/TCP port `53`, but permits sandboxes to declare other egress because `allowedEgress` is empty.

```json title="policy.json" theme={"system"}
{
  "displayName": "VM-isolated execution",
  "constraints": {
    "resources": {
      "defaultCpu": "500m",
      "defaultMemory": "512Mi",
      "maxCpu": "2",
      "maxMemory": "2Gi",
      "maxGpuCount": "0",
      "requireLimits": true
    },
    "image": { "allowedImages": ["ghcr.io/GITHUB_ORG/sandbox-base:pinned"] },
    "network": {
      "allowedEgress": [],
      "defaultEgress": [],
      "dnsEgress": "DNS_EGRESS_MODE_DENY"
    },
    "security": {
      "allowPrivileged": false,
      "allowedCapabilities": [],
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 300 },
    "metadata": { "maxAnnotationCount": 0 },
    "volumes": { "allowedMedia": ["STORAGE_MEDIUM_DISK"], "maxSize": "5Gi" }
  }
}
```

> [!WARNING]
>
> This policy doesn't enforce complete network isolation. An empty `allowedEgress` list permits explicit destination rules, and platform storage access is granted separately. `dnsEgress` blocks outbound port `53`, but doesn't block DNS over other permitted transports, such as HTTPS.

`allowedImages` pins one image rather than a registry, so a sandbox can't select an arbitrary image from a trusted registry.

## Internal worker cluster

Long-running background workers that other sandboxes in the organization reach over a service, with outbound access for third-party API calls.

```json title="policy.json" theme={"system"}
{
  "displayName": "Internal workers",
  "constraints": {
    "resources": {
      "defaultCpu": "1",
      "defaultMemory": "2Gi",
      "maxCpu": "8",
      "maxMemory": "16Gi",
      "requireLimits": true
    },
    "image": { "allowedRegistries": ["ghcr.io/GITHUB_ORG"] },
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "0.0.0.0/0", "except": ["10.0.0.0/8", "169.254.169.254/32"] } },
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ],
      "defaultEgress": [{ "tenant": "TENANT_SCOPE_SAME_ORG" }]
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 604800 }
  }
}
```

Egress is scoped so workers reach the public internet and sibling sandboxes in the organization, with private space and the metadata address carved out.

> [!NOTE]
>
> This example sets egress only. To constrain inbound access to `CUSTOM`-visibility ports, add `allowedIngress` and, if needed, `defaultIngress`. See [Constrain network access](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-network-access).

## Pin admin defaults with the base layer

Any of the previous policies can also carry a `base` fragment: admin attachments applied to every sandbox on the runner, whatever it asks for. This variant of the internal worker policy pins Node selection, a pull Secret for the private registry, and a cost-attribution label on all sandboxes.

```json title="policy.json" theme={"system"}
{
  "displayName": "Internal workers, pinned scheduling",
  "base": {
    "spec": {
      "nodeSelector": { "workload": "sandbox" },
      "tolerations": [
        { "key": "sandbox-only", "operator": "Exists", "effect": "NoSchedule" }
      ],
      "imagePullSecrets": [{ "name": "regcred" }]
    },
    "metadata": {
      "labels": { "cost-center": "sandboxes" }
    }
  },
  "constraints": {
    "resources": {
      "defaultCpu": "1",
      "defaultMemory": "2Gi",
      "maxCpu": "8",
      "maxMemory": "16Gi",
      "requireLimits": true
    },
    "image": { "allowedRegistries": ["ghcr.io/GITHUB_ORG"] },
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "0.0.0.0/0", "except": ["10.0.0.0/8", "169.254.169.254/32"] } },
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ],
      "defaultEgress": [{ "tenant": "TENANT_SCOPE_SAME_ORG" }]
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu",
      "allowedSeccompProfiles": ["RuntimeDefault"]
    },
    "lifecycle": { "defaultLifetimeSeconds": 604800 }
  }
}
```

The `base` fragment is a Kubernetes Pod-specification subset, and unknown keys are rejected. Both `base` and `constraints` use camelCase keys in this JSON example. It accepts scheduling and runtime configuration only: `nodeSelector`, `tolerations`, `imagePullSecrets`, `volumes`, `topologySpreadConstraints`, `hostAliases`, DNS settings, a single `containers` entry limited to `name`, `env`, `envFrom`, `volumeMounts`, and `volumeDevices`, and Pod labels and annotations. Security-sensitive fields are rejected: `securityContext`, `runtimeClassName`, `initContainers`, `affinity`, host namespaces, `hostPath` volumes, non-default ServiceAccounts, and `namespace`, which stays runner-owned. Typed concerns such as lifetime, images, and egress belong in `constraints`, not in `base`.

On a CKS cluster, [template attachments](https://docs.coreweave.com/products/sandboxes/profiles/templates.md#cks-only-pod-attachments) specialize this fragment per template: `imagePullSecrets` and `tolerations` are unioned and deduplicated, other lists append, map keys are overridden per key, and same-name conflicts reject the create. For the current enforcement status of `base`, see [the base layer](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#the-base-layer).

## Vary the posture across clusters

Because a policy belongs to a cluster, different postures are different clusters rather than different documents on one cluster. A team that needs both an open data science environment and a locked-down execution environment runs two clusters and gives each the matching policy.

To vary one dimension by region, apply the same policy to each cluster with the region-specific values changed. No shared or inherited policy document exists, so keep the source of truth in version control and apply it per cluster.

## See also

For related guidance, see the following pages:

* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): every constraint group, with the fields used in these examples.
* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how a sandbox resolves against a policy.
* [Agentic RL training](https://docs.coreweave.com/products/sandboxes/client/guides/rl-training.md): reward functions and multi-turn agent rollouts, with working Python.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): the rest of the runner configuration.
