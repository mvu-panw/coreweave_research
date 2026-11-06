# Policy reference

Source: https://docs.coreweave.com/products/sandboxes/reference/profile

# Policy reference

> Every field in a sandbox policy, with types, defaults, and validation rules.

This page documents every field in a sandbox policy. A policy is carried on a managed runner as the `policy` field and governs the sandboxes placed on that runner.

## Top-level fields

| Field | Type | Description |
| - | - | - |
| `display_name` | `string` | Human-readable name for the posture this policy describes. |
| `base` | object | Runtime defaults and attachments applied before the sandbox spec. See [`base`](#base). |
| `constraints` | `PolicyConstraints` | Typed clamps validated against the resolved spec. See [`constraints`](#constraints). |
| `control_plane_access` | `ControlPlaneAccessPolicy` | Request-time source IP controls for Sandbox API operations. See [`control_plane_access`](#control_plane_access). |

An empty policy is valid and supplies no base defaults or explicit constraints. Platform safety gates still apply, and an absent runtime-class allowlist permits no concrete `runtime_class` pin. The `base`, `constraints`, and `control_plane_access` groups are optional. An absent source IP allowlist adds no source-address restriction.

## Resolution order

A sandbox resolves in two stages:

1. **Base**: Runtime defaults, then `base`, then the sandbox spec. The sandbox takes precedence for scalar defaults. List attachments from `base` are always applied, and administrator-pinned Pod metadata takes precedence when annotation keys overlap.
2. **Constraints**: Clamps are validated against the fully resolved spec. A violation is rejected, never silently rewritten.

Because constraints validate the resolved spec rather than the submitted one, a value that `base` supplied is checked on the same terms as a value the sandbox supplied.

## `base`

A fragment of runtime defaults and attachments. On a Kubernetes runner, this is a Pod specification fragment.

`base` is where infrastructure settings live that a sandbox has no business declaring: the scheduler, Node selectors, tolerations, PriorityClass, topology spread, image pull Secrets, platform volumes, DNS configuration, and Pod metadata such as pinned annotations. Security-sensitive fields are rejected outright, including the following:

* `affinity`
* Pod and container `securityContext`.
* `runtimeClassName`
* `initContainers`
* Host namespaces.
* `hostPath` volumes.
* Non-default ServiceAccounts.

## `control_plane_access`

`ControlPlaneAccessPolicy` restricts Sandbox API requests that select a runner or target a sandbox placed on it. These controls supplement authentication and authorization. They don't restrict traffic sent directly to services exposed by a sandbox.

| Field | Type | Description |
| - | - | - |
| `source_ip_allowlist` | `SourceIpAllowlist` | Optional source-address allowlist. Absent means unrestricted by source address. Present but empty denies every public source. |

### `SourceIpAllowlist`

| Field | Type | Description |
| - | - | - |
| `cidrs` | `string` list | IPv4 and IPv6 classless inter-domain routing (CIDR) prefixes matched against the client address observed at the API edge. The API accepts at most 256 entries and 16 KiB of CIDR text before normalization. |

The API canonicalizes prefixes, removes duplicates, and removes prefixes covered by a broader entry. Invalid CIDRs, including zone-qualified IPv6 addresses, are rejected. `0.0.0.0/0` explicitly permits every IPv4 source. `::/0` explicitly permits every IPv6 source.

Access controls are evaluated at request time, separately from create-time specification resolution. Changes apply to new operations on existing sandboxes after policy-cache propagation. Policy administration remains available to administrators regardless of the allowlist. For configuration, stream behavior, errors, and recovery, see [Restrict Sandbox API access by source IP](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#restrict-sandbox-api-access-by-source-ip).

## `constraints`

`PolicyConstraints` groups the typed clamps a policy enforces. Every group is optional. Omitting a group adds no explicit constraints of that kind, but platform safety gates and the runtime-class restrictions in [`SecurityConstraints`](#securityconstraints) still apply.

| Group | Type | Governs |
| - | - | - |
| `resources` | `ResourceConstraints` | CPU, memory, and GPU bounds and defaults. |
| `image` | `ImageConstraints` | Which images a sandbox may run. |
| `network` | `NetworkConstraints` | Egress and ingress allowlists and defaults. |
| `security` | `SecurityConstraints` | Privilege, capabilities, and isolation. |
| `instance` | `InstanceConstraints` | Which Node instance types a sandbox may land on. |
| `lifecycle` | `LifecycleConstraints` | How long a sandbox may live. |
| `metadata` | `MetadataConstraints` | Annotation keys and count. |
| `volumes` | `VolumeConstraints` | Storage media and per-volume size. |

## `ResourceConstraints`

| Field | Type | Description |
| - | - | - |
| `max_cpu` | `string` | Maximum CPU a container may request, as a Kubernetes quantity. |
| `max_memory` | `string` | Maximum memory a container may request. |
| `min_cpu` | `string` | Minimum CPU a container may request. |
| `min_memory` | `string` | Minimum memory a container may request. |
| `default_cpu` | `string` | Default CPU per container. When a container declares neither requests nor limits, a positive default also supplies its CPU limit. |
| `default_memory` | `string` | Default memory per container. When a container declares neither requests nor limits, a positive default also supplies its memory limit. |
| `max_gpu_count` | `int64` | Maximum GPUs per container. Omitted means no cap. Explicit `0` forbids GPU requests. |
| `cpu_ceiling` | `string` | Cap on the sum of resolved CPU requests across all user containers. |
| `memory_ceiling` | `string` | Cap on resolved memory requests across all user containers plus resolved memory-backed volume sizes. |
| `require_limits` | `bool` | When `true`, requires every container to have limits after defaults are applied. |

`max_cpu` and `max_memory` bound each user container's request. A sandbox with multiple user containers can satisfy each per-container maximum and still exceed `cpu_ceiling` or `memory_ceiling`. The memory ceiling also includes the resolved sizes of memory-backed volumes.

Ceilings are policy checks on one sandbox. Placement also accounts for runtime overhead, other workloads, and available capacity. [Node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md) bound aggregate sandbox requests on each Node. For sizing guidance, see [Size sandbox CPU and memory](https://docs.coreweave.com/products/sandboxes/resource-sizing.md).

## `ImageConstraints`

| Field | Type | Description |
| - | - | - |
| `allowed_registries` | `string` list | Registries a sandbox image may come from. Empty permits any. |
| `allowed_images` | `string` list | Exact images a sandbox may run. Empty permits any. |

## `NetworkConstraints`

Network constraints define allowlists for the access a sandbox can request. When a sandbox declares egress, the policy accepts or rejects that declaration without widening it. When the sandbox declares no egress, the policy applies `default_egress`, unless the sandbox sets `deny_egress`. Platform DNS and storage access are granted separately. The same constraints bound [dynamic network updates](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md).

| Field | Type | Description |
| - | - | - |
| `allowed_egress` | `EgressRule` list | Egress allowlist, checked when a sandbox is created and during live network updates. When non-empty, every declared rule must fit inside it. Empty permits anything declarable. |
| `default_egress` | `EgressRule` list | Applied when the sandbox declares no egress, unless it sets `deny_egress`. Displaced entirely by any declaration. Must fit `allowed_egress` and must not contain `https_hostname` rules. |
| `allowed_ingress` | `IngressRule` list | Ingress allowlist for `CUSTOM`-visibility ports, checked when a sandbox is created and during live network updates. When non-empty, every declared rule must fit inside it. Empty permits anything declarable. |
| `default_ingress` | `IngressRule` list | Applied when a sandbox exposes a `CUSTOM`-visibility port and declares no ingress, unless it sets `deny_ingress`. Displaced entirely by explicit ingress rules. Must fit `allowed_ingress`. |
| `deny_https_hostname_rules` | `bool` | When `true`, rejects `https_hostname` rules in `allowed_egress` and sandbox requests. Doesn't block DNS queries or HTTPS permitted by CIDR rules. |
| `dns_egress` | `DNSEgressMode` | Controls outbound DNS traffic on UDP/TCP port `53`. Unspecified defaults to `DNS_EGRESS_MODE_ALLOW`. A sandbox can choose `DNS_EGRESS_MODE_DENY`, but can't request `ALLOW` when the policy requires `DENY`. |

When an allowlist is non-empty, containment is checked by destination or source type and port. A declared CIDR must fit the combined allowed CIDR ranges or an `any` rule. A declared tenant scope requires a matching tenant rule or an `any` rule, while declaring `any` requires an `any` rule.

### `EgressRule`

Each rule names exactly one destination, optionally narrowed by port.

| Field | Type | Description |
| - | - | - |
| `cidr` | `CidrBlock` | An address range, with optional carve-outs. |
| `https_hostname` | `string` | An HTTPS hostname, exact or with a single leftmost wildcard label, such as `*.example.com`. Requires a runner that supports hostname-based HTTPS rules. In `allowed_egress`, `*` permits any hostname declaration. |
| `https_hostname_except` | `string` list | Hostnames excluded from this rule. Valid only with `https_hostname` in `allowed_egress`. Uses the same hostname patterns, except `*`. |
| `tenant` | `TenantScope` | Other sandboxes, selected by relationship. |
| `any` | `bool` | All reachable destinations except platform-internal ranges. Use tenant or selector rules to reach other sandboxes or cluster workloads. |
| `selector` | `SelectorBlock` | Workloads selected by label. |
| `ports` | `PortRange` list | Ports the rule applies to. Omit for all ports, except for `https_hostname` rules, which permit only TCP `443`. |

Hostname rules authorize HTTPS access, not DNS queries. When `allowed_egress` is non-empty, a declared hostname must fit an allowed hostname pattern, after its exclusions, or an `any` rule. A CIDR-only allowlist doesn't permit hostname declarations. Put reusable hostname grants in a [sandbox template](https://docs.coreweave.com/products/sandboxes/profiles/templates.md), not in `default_egress`.

`dns_egress` controls outbound UDP/TCP port `53` independently. `DNS_EGRESS_MODE_ALLOW` permits access to the platform resolver. Other resolvers require an egress rule. `DNS_EGRESS_MODE_DENY` blocks outbound port `53` even when another rule permits it. It doesn't block locally answered lookups or DNS over other permitted transports, such as HTTPS.

### `IngressRule`

| Field | Type | Description |
| - | - | - |
| `cidr` | `CidrBlock` | An address range, with optional carve-outs. |
| `tenant` | `TenantScope` | Other sandboxes, selected by relationship. |
| `any` | `bool` | Any source. |
| `ports` | `PortRange` list | Ports the rule applies to. Omit for all `CUSTOM`-visibility ports. |

Ingress rules apply to existing `CUSTOM`-visibility ports. They don't change service visibility and can't select sources by hostname or label.

### `CidrBlock`

| Field | Type | Description |
| - | - | - |
| `cidr` | `string` | Required. The address range, such as `10.0.0.0/8`. |
| `except` | `string` list | Ranges carved out of `cidr`. A carve-out narrows only its own rule. |

### `PortRange`

| Field | Type | Description |
| - | - | - |
| `protocol` | `string` | Optional. Defaults to TCP. |
| `port` | `int32` | Required. The port, or the start of a range. |
| `end_port` | `int32` | Optional. The end of a range. |

### `TenantScope`

| Value | Selects |
| - | - |
| `TENANT_SCOPE_SAME_USER` | Sandboxes owned by the same user. |
| `TENANT_SCOPE_SAME_ORG` | Sandboxes in the same organization. |
| `TENANT_SCOPE_SANDBOX_NETWORK` | Sandboxes on the same sandbox network. Not supported yet. An egress rule using it is rejected. |

### `SelectorBlock`

| Field | Type | Description |
| - | - | - |
| `pod_labels` | `string` map | Required. Labels matched on the destination Pod. |
| `namespace_labels` | `string` map | Optional. Labels matched on the destination Namespace. |

Matching uses exact label pairs, but declarations may add labels. When the egress allowlist is non-empty, a declared selector must carry every label pair in a matching selector rule. Both selectors must omit Namespace labels, or both must include them, with the declaration carrying every required Namespace label pair. An `any` rule never covers selectors, but an empty allowlist permits selector declarations.

## `SecurityConstraints`

| Field | Type | Description |
| - | - | - |
| `allow_privileged` | `bool` | Whether a container may run privileged within the sandbox's isolation boundary. |
| `allowed_capabilities` | `string` list | Linux capabilities a container may add. |
| `allowed_seccomp_profiles` | `string` list | Permitted seccomp profiles, such as `RuntimeDefault` or `Unconfined`. |
| `allowed_runtime_classes` | `string` list | Runtime classes a sandbox may pin. Fails closed: empty permits no pin at all. |
| `default_cpu_runtime_class` | `string` | Runtime class applied to a CPU sandbox that pins none. |
| `default_gpu_runtime_class` | `string` | Runtime class applied to a GPU sandbox that pins none. |
| `runtime_class_mappings` | `RuntimeClassMapping` list | Maps portable runtime classes to execution targets. See [`RuntimeClassMapping`](#runtimeclassmapping). |

Host namespaces aren't configurable through `v1` policy security fields. The former `allow_host_network` and `allow_host_pid` fields have been removed. For legacy `v1beta2` profiles, see [Example: allow a privileged profile posture](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-allow-a-privileged-profile-posture).

`allowed_runtime_classes` fails closed: an empty or absent list permits no concrete `runtime_class` pin. Portable class selection through `runtime_class_selection` uses `runtime_class_mappings` instead.

The policy bounds the in-guest privileges a sandbox may request and the runtime classes it may select.

### `RuntimeClassMapping`

A non-empty `runtime_class_mappings` list enables portable runtime class selection. Each mapped class is available for caller selection. `RUNTIME_CLASS_CPU_DEFAULT` and `RUNTIME_CLASS_GPU_DEFAULT` also supply automatic selection for their resource family. Omitting either default class turns off automatic selection for that family. Unmapped classes are unavailable, and concrete `runtime_class` pins are rejected.

Mappings can't be combined with `allowed_runtime_classes`, `default_cpu_runtime_class`, or `default_gpu_runtime_class`. Each portable class can appear at most once.

| Field | Type | Description |
| - | - | - |
| `runtime_class` | `RuntimeClass` | Required portable class. Use one of the following values. |
| `kubernetes_runtime_class_name` | `string` | Non-empty Kubernetes RuntimeClass name. Set exactly one of this field or `node_default`. |
| `node_default` | `bool` | Set to `true` to use the Node's default container runtime. Permitted only for `RUNTIME_CLASS_CPU_DEFAULT` or `RUNTIME_CLASS_GPU_DEFAULT`, and only for CoreWeave Kubernetes Service (CKS) placement outside the shared serverless pool. |

| `RuntimeClass` value | Execution requirement |
| - | - |
| `RUNTIME_CLASS_CPU_DEFAULT` | Default execution without GPU resources. |
| `RUNTIME_CLASS_CPU_NESTED_VIRT` | CPU execution with nested virtualization. |
| `RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE` | CPU execution with virtual machine (VM) state snapshot and restore. File-system snapshots are a separate capability. |
| `RUNTIME_CLASS_GPU_DEFAULT` | Default execution with GPU resources. |

## `InstanceConstraints`

| Field | Type | Description |
| - | - | - |
| `allowed_instance_types` | `string` list | Node instance types a sandbox may land on. Empty permits any. |

## `LifecycleConstraints`

| Field | Type | Description |
| - | - | - |
| `default_lifetime_seconds` | `int32` | Lifetime applied when the sandbox requests none. |

The policy carries no lifetime cap. The platform maximum of 30 days bounds every sandbox: a create request above it is rejected. The `max_lifetime_seconds` field was removed from the policy document, and `cwic` rejects a policy that still carries it.

## `MetadataConstraints`

| Field | Type | Description |
| - | - | - |
| `denied_annotation_prefixes` | `string` list | Annotation key prefixes that are rejected. |
| `max_annotation_count` | `int32` | Maximum annotations a sandbox may set. `0` means no limit. |

## `VolumeConstraints`

| Field | Type | Description |
| - | - | - |
| `allowed_media` | `StorageMedium` list | Permitted storage media. Empty permits any. |
| `max_size` | `string` | Maximum size per volume, such as `100Gi`. |

### `StorageMedium`

| Value | Description |
| - | - |
| `STORAGE_MEDIUM_UNSPECIFIED` | Invalid in `allowed_media`. On scratch-volume requests, omission or this value defaults to disk-backed storage. |
| `STORAGE_MEDIUM_DISK` | Disk-backed. |
| `STORAGE_MEDIUM_MEMORY` | RAM-backed, counting against the container's memory. |

To forbid RAM-backed volumes, set a non-empty `allowed_media` list containing only `STORAGE_MEDIUM_DISK`. An empty list permits any storage medium.

## Validation rules

A policy is rejected when any of the following hold:

* The encoded document exceeds 256 KiB.
* The policy is `null`. A configured policy can't be cleared, only replaced.
* `default_egress` contains `https_hostname` rules.
* Default egress or ingress rules fall outside the corresponding allowlist.
* A source IP allowlist contains an invalid IPv4 or IPv6 CIDR, more than 256 entries, or more than 16 KiB of CIDR text.

## See also

For related guidance, see the following pages:

* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): the task-oriented walkthrough for every group on this page.
* [Policy examples](https://docs.coreweave.com/products/sandboxes/profiles/profile-examples.md): five complete policies for common cluster postures.
* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how a sandbox resolves against a policy.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): where the policy lives and how to set it.
