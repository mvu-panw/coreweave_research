# Configure a sandbox policy

Source: https://docs.coreweave.com/products/sandboxes/profiles/configure

# Configure a sandbox policy

> Set sandbox policy constraints, defaults, and source IP access controls for managed runners.

This page shows how to author the policy that governs sandboxes on a cluster: bounding compute, images, network access, and security posture, and setting the defaults every sandbox inherits. It's written for administrators who manage runners. Policies also support [source IP access controls](#restrict-sandbox-api-access-by-source-ip) for Sandbox API requests.

A policy is carried on the runner, so you author it by updating the runner. A policy has no separate resource or endpoint.

## Before you begin

You need the **Sandbox Admin** role in your organization. Reading or writing a policy without it returns `PermissionDenied`.

> [!WARNING]
>
> The [Sandbox Admin](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox) role controls runner settings across the organization. On runners using legacy `v1beta2` profiles, this role can enable [privileged profile settings](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-allow-a-privileged-profile-posture). These settings include privileged containers, host namespaces, and mounts of the Node's filesystem. These settings can give sandboxes Node access comparable to that of a cluster administrator and put co-located workloads at risk. The v1 policy's `allow_privileged` setting governs in-guest privilege within the sandbox's isolation boundary.

The CLI examples use [CoreWeave Intelligent CLI version 1.49.0](https://github.com/coreweave/cwic/releases/tag/v1.49.0). Before you run the examples, install and authenticate the CLI.

To use the REST examples, you need a CoreWeave API access token. Examples use `$TOKEN` for that token and `prod-us-east-1` for the runner.

The file-based CLI and REST update examples also require `jq`.

A runner requires a stored policy before v1 sandbox placement. The policy can come from an administrator or a [deployment-configured default](#set-a-default-policy-for-new-runners). An empty policy is valid and supplies no base defaults or explicit constraints. Platform safety gates still apply, and an absent runtime-class allowlist permits no concrete `runtime_class` pin. See [Constrain security posture](#constrain-security-posture).

## Read the current policy

Start from what the runner has now, rather than from an empty document.

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner policy get prod-us-east-1
> ```
>
> Add `describe` for a detailed view, which names the not-configured state explicitly when a runner has no policy:
>
> ```bash theme={"system"}
> cwic sandbox runner policy describe prod-us-east-1
> ```
>
> With `-o json`, a runner that has never been configured returns `null` rather than `{}`, so automation can tell "never configured" apart from "configured with an empty policy".

> [tab] curl
>
> ```bash title="Read a runner and its policy" theme={"system"}
> curl https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1 \
>   -H "Authorization: Bearer $TOKEN"
> ```

## Update a policy

A policy is a field on the runner, so you set it by updating the runner with an update mask of `policy`.

**The examples on this page select the root `policy` mask and replace the entire document.** Read the current policy, change what you need, and send the whole document back with the `etag` from the same read. Omitted groups are cleared when you replace the root policy.

> [tab] CLI
>
> Edit the policy in `$EDITOR`, seeded with the runner's current document:
>
> ```bash theme={"system"}
> cwic sandbox runner policy edit prod-us-east-1
> ```
>
> For a file-based update, follow these steps:
>
> 1. Capture the policy and its `etag` from one read of the runner:
>
>    ```bash theme={"system"}
>    cwic sandbox runner get prod-us-east-1 -o json > runner.json
>    jq '.[0].policy' runner.json > policy.json
>    ```
>
> 2. Edit the `policy.json` file, then submit it with the `etag` from that same read:
>
>    ```bash theme={"system"}
>    cwic sandbox runner policy edit prod-us-east-1 -f policy.json \
>      --etag "$(jq -r '.[0].etag' runner.json)"
>    ```
>
> With `-f` and no `--etag`, `cwic` reads the runner's current revision as it submits. A file edited against an earlier read can therefore overwrite another administrator's change. Use `-f -` to supply the complete policy through stdin, and pass the `etag` from the same read as the document.
>
> Take the `etag` from the read that produced the document, never from a later one. `policy get` exports the policy without its `etag`. A `policy describe` run after the export can return a newer token. That token passes the check and lets your file overwrite the change made in between.
>
> In editor mode, the CLI sends the `etag` it read to seed the editor, so you don't need a flag. The `cwic sandbox runner edit` template also captures the policy and its `etag` together. The `--print-template` flag exports them with the mutable runner settings, and `-f` uses the value in the file.
>
> To export the current policy as YAML, or a scaffold if no policy is configured, print a template:
>
> ```bash theme={"system"}
> cwic sandbox runner policy edit prod-us-east-1 --print-template
> ```
>
> Before you send a document, check it:
>
> ```bash theme={"system"}
> cwic sandbox runner policy validate -f policy.yaml
> ```

> [tab] curl
>
> To update the policy with the REST API, follow these steps:
>
> 1. Read the runner to capture both its current policy and its `etag`:
>
>    ```bash theme={"system"}
>    curl -H "Authorization: Bearer $TOKEN" \
>      https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1 \
>      | jq '{policy, etag}' > policy-and-etag.json
>    ```
>
> 2. Edit the `policy` object in that file. Keep every field you want to preserve. Leave the `etag` unchanged, then send the file back:
>
>    ```bash title="Replace a runner's policy" theme={"system"}
>    curl -X PATCH "https://api.coreweave.com/v1/sandbox/managedRunners/prod-us-east-1?updateMask=policy" \
>      -H "Authorization: Bearer $TOKEN" \
>      -H "Content-Type: application/json" \
>      -d @policy-and-etag.json
>    ```

The following rules apply to every policy write:

* **Lifetime is bounded by the platform, not the policy**: A policy supplies only `constraints.lifecycle.defaultLifetimeSeconds`, used when a create request omits a lifetime. The platform rejects lifetimes above its maximum of 30 days at create time. Earlier policy versions carried a `maxLifetimeSeconds` cap. Current `cwic` rejects documents that still contain it.
* **A configured policy can't be cleared**: No delete operation exists, and the API rejects an update that sets the policy to `null`. To loosen a posture, replace the document with a more permissive one.
* **A policy document is capped at 256 KiB** once encoded.

> [!WARNING]
>
> A policy write is a read-modify-write. The API checks it against the `etag` from the read your edit is based on. If another administrator has updated the policy since that read, the API rejects your write with `FAILED_PRECONDITION` and changes nothing.
>
> Read the runner again, reapply your change to the returned document, and resubmit with the new `etag`. If you fetch a fresh `etag` and resend your unchanged document, the write passes the check but discards the other administrator's edit. The write still replaces the whole document.

For lifetime examples and the differences between Serverless and CoreWeave Kubernetes Service (CKS), see [Run long-running sandboxes](https://docs.coreweave.com/products/sandboxes/long-running-sandboxes.md).

Policy defaults and constraints resolve when a sandbox is created. A policy write doesn't automatically reconfigure running sandboxes. New placements and explicit [live network updates](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md) resolve against the gateway's current cached runner policy. Source IP access controls apply to new operations on existing sandboxes as well as new placements. The cached policy can lag briefly after an update.

> [!NOTE]
>
> In CoreWeave Intelligent CLI version 1.49.0, `cwic sandbox runner` commands, including `cwic sandbox runner policy`, use `v1`. Legacy `cwic sandbox profile` commands use `v1beta2`. Both use Connect RPC through the same `--api-url`. The `curl` examples use the `v1` REST surface. For CLI field names and update-mask behavior, see [Field masks on updates](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md#field-masks-on-updates).

## Restrict Sandbox API access by source IP

Use `control_plane_access.source_ip_allowlist` to restrict Sandbox API requests by source address. The client's observed source address must match an IPv4 or IPv6 classless inter-domain routing (CIDR) range. The allowlist supplements authentication, identity and access management (IAM) permissions, and organization ownership checks. It doesn't make the shared API endpoint private or restrict traffic sent directly to services exposed by a sandbox.

Use the public egress address that CoreWeave observes for the client making the API request. For a client in a CKS Pod using standard public network address translation (NAT) routing, use the [NAT Egress ranges for its Availability Zone](https://docs.coreweave.com/support/networking/articles/does-outbound-traffic-have-a-stable-public-ip). For a client on your corporate network or virtual private network (VPN), use your organization's public egress ranges. A private Pod or workstation address isn't a substitute for the observed source address.

To add an allowlist while preserving the runner's other policy settings, complete the following steps:

1. Open the current policy in your editor:

   ```bash theme={"system"}
   cwic sandbox runner policy edit prod-us-east-1
   ```

   Editor mode retains the `etag` from the read that opened the document, so another administrator's intervening policy update causes a conflict instead of being overwritten.

2. Add the following fragment at the top level of the current policy. Replace the placeholders with the actual public egress CIDRs for your clients. If your clients don't use an address family, omit it. Keep the other policy fields:

   ```yaml theme={"system"}
   control_plane_access:
     source_ip_allowlist:
       cidrs:
         - "PUBLIC_IPV4_CIDR"
         - "PUBLIC_IPV6_CIDR"
   ```

3. Save the complete document and exit the editor. If the API reports a stale `etag`, reopen the current policy and reapply your change before saving again.

The allowlist has the following semantics:

* An absent `source_ip_allowlist` adds no source-address restriction.
* A present allowlist requires the observed source address to match at least one CIDR.
* `0.0.0.0/0` permits every IPv4 address, and `::/0` permits every IPv6 address.
* Input is limited to 256 CIDRs and 16 KiB of CIDR text, before normalization. The API canonicalizes prefixes, removes duplicates, and removes prefixes covered by a broader entry.

> [!WARNING]
>
> A present but empty `source_ip_allowlist`, including `source_ip_allowlist: {}`, denies every public source address. To remove the restriction, remove the allowlist field rather than emptying it.

### Policy changes and request behavior

After the policy cache converges, the gateway checks the updated allowlist when selecting a runner and before new operations on existing sandboxes. This includes reads, commands, file transfers, lifecycle operations, snapshots, and streaming requests. New streams, resumed streams, and requests forwarded to another gateway are checked. Established streams remain connected.

List and discovery requests omit resources denied by source address. If the gateway can't evaluate a required policy, the request fails rather than returning resources without an access decision.

For requests other than stream resumes, the API distinguishes source denial from unavailable policy state:

| Request condition | Error |
| - | - |
| A request for an existing sandbox is source-denied, or every otherwise suitable creation candidate is source-denied. | `PermissionDenied` with `CWSANDBOX_SOURCE_IP_NOT_ALLOWED`. |
| The gateway can't evaluate the required policy. For creation, no allowed candidate remains and at least one candidate has an indeterminate access decision. | `Unavailable` with `CWSANDBOX_ACCESS_POLICY_UNAVAILABLE`. |

On stream resume, a source-address denial can appear as an in-stream `SESSION_NOT_FOUND` response. An unavailable access policy still returns `Unavailable` with `CWSANDBOX_ACCESS_POLICY_UNAVAILABLE`.

A creation request can still use another suitable runner that permits the source address. Authentication, resource fit, and capacity checks continue to apply.

### Restore unrestricted source access

Policy administration requires the **Sandbox Admin** role and isn't restricted by the runner's own source IP allowlist. To recover from a lockout, open the current policy with the previous editor command. Remove the `source_ip_allowlist` field or its enclosing `control_plane_access` field, and save the complete document. Preserve the other policy settings.

After the policy cache converges, new requests are no longer restricted by source address. Authentication and authorization still apply. For field types and validation rules, see [`control_plane_access` in the policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile#control_plane_access).

## Set a default policy for new runners

CoreWeave's service deployment configuration defines a default policy for runners without a stored policy. The gateway saves that policy when a runner connects or when v1 placement first selects a runner without a policy. A runner with an existing policy keeps it.

The service deployment configures the following defaults:

| Setting | Default |
| - | - |
| CPU request default | 1 CPU |
| Memory request default | 2 GiB (`2Gi`) |
| Sandbox lifetime, when omitted | 10 minutes (600 seconds) |
| Network egress default | IPv4 egress to `0.0.0.0/0`, with excluded address ranges. |

Explicit resource requests or limits take precedence over policy resource defaults. A sandbox that sets `deny_egress` suppresses default egress.

The `allowedEgress` and `defaultEgress` lists use the same exclusions, including private, loopback, and link-local IPv4 ranges. These exclusions apply both to requested egress rules and to default egress. Before you run workloads, review the runner's [current policy](#read-the-current-policy) for its full network rules and any administrator changes.

These values describe the service deployment configuration. The policy saved on a runner determines its behavior. The [quickstart's optional policy example](https://docs.coreweave.com/products/sandboxes/get-started-cks.md#optional-customize-the-sandbox-policy) replaces that document and uses different settings.

The v1 `CreateManagedRunner` API still requires a `policy` in the request. Automatic default assignment doesn't make that field optional.

The default lives in the gateway infrastructure configuration at `gateway.infraConfig.default_runner_policy`, and changing it requires a gateway restart. No built-in default exists. When the setting is absent or `null`, nothing is written and the sandbox is still rejected with `CWSANDBOX_POOL_POLICY_NOT_CONFIGURED`.

The default policy has the following behavior:

* **The default is a snapshot, not a link**: Once materialized onto a runner, the policy is an ordinary runner policy. Later changes to `default_runner_policy` don't reach runners that already have one. Update those with `UpdateManagedRunner`.
* **An invalid default degrades creation**: The gateway validates the configured policy at startup. If it doesn't validate, the gateway still starts, but sandbox creation fails with `CWSANDBOX_SERVERLESS_MISCONFIGURED`.

## Constrain compute

`resources` bounds what a container may request, and supplies the values used when a sandbox requests nothing.

```json theme={"system"}
{
  "constraints": {
    "resources": {
      "minCpu": "500m",
      "maxCpu": "8",
      "defaultCpu": "2",
      "minMemory": "1Gi",
      "maxMemory": "32Gi",
      "defaultMemory": "4Gi",
      "maxGpuCount": "2",
      "requireLimits": true
    }
  }
}
```

Set `requireLimits` to `true` to require limits in each container's resolved allocation. If a container omits its resource allocation, `defaultCpu` and `defaultMemory` supply both requests and limits when both defaults are set to values greater than zero. Incomplete defaults don't satisfy the requirement. This setting doesn't require limits to equal requests.

`maxCpu` and `maxMemory` bound each user container's request. Use `cpuCeiling` to cap the sum of resolved CPU requests across all user containers. Use `memoryCeiling` to cap the sum of their resolved memory requests plus the resolved sizes of memory-backed volumes. A sandbox with multiple user containers can satisfy each per-container maximum and still exceed a sandbox ceiling.

Ceilings are policy checks on one sandbox. Placement also accounts for runtime overhead, other workloads, and available capacity. [Node allocation budgets](https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets.md) bound aggregate sandbox requests on each Node. For sizing guidance, see [Size sandbox CPU and memory](https://docs.coreweave.com/products/sandboxes/resource-sizing.md).

`maxGpuCount` caps the GPUs each container may request. Leave it out to apply no cap. Set it to `0` to reject every GPU request, which is how you express a GPU-free pool. A request above the cap fails with `CWSANDBOX_RESOURCE_CEILING_EXCEEDED`. A `maxGpuCount` above your organization's maximum number of GPUs per sandbox doesn't raise that maximum. For more information, see [How GPU requests work](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md#how-gpu-requests-work).

## Constrain images

`image` restricts where sandbox images may come from. An empty group permits any image. Replace `GITHUB_ORG` with your GitHub Container Registry organization or user name.

```json theme={"system"}
{
  "constraints": {
    "image": {
      "allowedRegistries": ["ghcr.io/GITHUB_ORG"],
      "allowedImages": ["ghcr.io/GITHUB_ORG/agent-base:2024.11"]
    }
  }
}
```

## Constrain network access

Network constraints work as an envelope. When a sandbox declares egress, the policy accepts or rejects that declaration without widening it. When the sandbox declares no egress, the policy applies its egress defaults, unless the sandbox sets `deny_egress`.

Two settings do separate jobs:

* `allowedEgress` is the egress allowlist, checked when a sandbox is created. When it's non-empty, every rule the sandbox declares must fit inside it, and a rule outside it is rejected rather than narrowed. Empty means anything is declarable.
* `defaultEgress` is what an absent request means. It applies only when the sandbox declares no egress of its own and doesn't set `deny_egress`. Any declaration displaces it entirely.

A rule names one destination. Use `cidr` with optional `except` carve-outs, `tenant` for a relationship to other sandboxes, `selector` for workloads selected by label, `httpsHostname` for an HTTPS hostname, or `any`. Optional `ports` narrow the rule further. Hostname rules permit only TCP `443` and require a runner that supports them. They belong in `allowedEgress` and sandbox requests, not in `defaultEgress`.

```json theme={"system"}
{
  "constraints": {
    "network": {
      "allowedEgress": [
        { "cidr": { "cidr": "0.0.0.0/0", "except": ["10.0.0.0/8", "169.254.169.254/32"] } },
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ],
      "defaultEgress": [
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ]
    }
  }
}
```

The example permits the public internet while excluding private space and the instance metadata address, and permits sandboxes to reach other sandboxes in the same organization. A sandbox that declares nothing gets same-organization access only.

Tenant scopes are `TENANT_SCOPE_SAME_USER` and `TENANT_SCOPE_SAME_ORG`. A third value, `TENANT_SCOPE_SANDBOX_NETWORK`, isn't supported yet and an egress rule using it is rejected.

Ingress uses `allowedIngress` and `defaultIngress` for ports with `CUSTOM` visibility. A non-empty allowlist constrains every declared ingress rule. When a sandbox exposes a `CUSTOM` port without declaring ingress rules, `defaultIngress` applies, unless the sandbox sets `deny_ingress`. Explicit ingress rules replace that default. Ingress rules accept `cidr`, `tenant`, or `any`. They don't accept name-based sources.

Set `denyHttpsHostnameRules` to reject hostname-based HTTPS rules. This doesn't block DNS queries or HTTPS permitted by CIDR rules. Set `dnsEgress` to `DNS_EGRESS_MODE_DENY` to block outbound UDP/TCP port `53`. If omitted, DNS access to the platform resolver is allowed. Platform DNS and storage access are granted separately from destination rules. See [Network constraints](https://docs.coreweave.com/products/sandboxes/reference/profile.md#networkconstraints) for containment rules and DNS behavior.

## Constrain security posture

`security` governs in-guest privilege and the isolation the sandbox runs under.

```json theme={"system"}
{
  "constraints": {
    "security": {
      "allowPrivileged": false,
      "allowedCapabilities": ["NET_BIND_SERVICE"],
      "allowedSeccompProfiles": ["RuntimeDefault"],
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu"
    }
  }
}
```

`allowedRuntimeClasses` fails closed. An empty or absent list permits no concrete runtime class pin, so a sandbox can only pin a class when you list one explicitly. Set `defaultCpuRuntimeClass` and `defaultGpuRuntimeClass` to choose what a sandbox gets when it pins nothing.

Alternatively, set `runtimeClassMappings` to map portable runtime classes to execution targets. A non-empty mapping list enables selection through `runtime_class_selection` and rejects concrete `runtime_class` pins. You can't combine mappings with `allowedRuntimeClasses`, `defaultCpuRuntimeClass`, or `defaultGpuRuntimeClass`. For fields and selection rules, see [`RuntimeClassMapping`](https://docs.coreweave.com/products/sandboxes/reference/profile#runtimeclassmapping).

## Constrain instances, lifetime, metadata, and volumes

The remaining groups are small.

| Group | Fields | Effect |
| - | - | - |
| `instance` | `allowedInstanceTypes` | Restricts which Node instance types a sandbox may land on. |
| `lifecycle` | `defaultLifetimeSeconds` | The lifetime a sandbox gets when it asks for nothing. The platform maximum of 30 days bounds every sandbox. `maxLifetimeSeconds` was removed from the policy document and is rejected. |
| `metadata` | `deniedAnnotationPrefixes`, `maxAnnotationCount` | Rejects annotation keys by prefix and caps how many a sandbox may set. `0` means no limit. |
| `volumes` | `allowedMedia`, `maxSize` | Restricts storage media and caps per-volume size. Set `allowedMedia` to a non-empty list containing only `STORAGE_MEDIUM_DISK` to forbid RAM-backed volumes. An empty list permits any medium. |

```json theme={"system"}
{
  "constraints": {
    "lifecycle": { "defaultLifetimeSeconds": 3600 },
    "volumes": { "allowedMedia": ["STORAGE_MEDIUM_DISK"], "maxSize": "100Gi" }
  }
}
```

## The base layer

Constraints bound what a sandbox may ask for. The `base` layer supplies what every sandbox gets without asking: defaults and attachments such as the scheduler, Node selectors, tolerations, and image pull Secrets. Its shape depends on the runner runtime, and on a Kubernetes runner it's a Pod specification fragment. Non-default ServiceAccounts are rejected. For the allowed fields and restrictions, see [Pin admin defaults with the base layer](https://docs.coreweave.com/products/sandboxes/profiles/profile-examples.md#pin-admin-defaults-with-the-base-layer).

## Next steps

For related guidance, see the following pages:

* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how a sandbox resolves against a policy, and what changed from profiles.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): the runner lifecycle and the rest of the runner configuration.
* [Control plane API overview](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md): authentication, field masks, and the endpoint contract.
