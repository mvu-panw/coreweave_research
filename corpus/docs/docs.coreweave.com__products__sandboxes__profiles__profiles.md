# Policies overview

Source: https://docs.coreweave.com/products/sandboxes/profiles/profiles

# Policies overview

> How a sandbox resolves against the policy that governs its cluster, and what a policy can constrain.

One stored policy governs sandboxes placed on a cluster. It combines a permissive base layer of defaults that every sandbox inherits with typed constraints that bound what a sandbox may request. An administrator can supply it, or the gateway can save a [deployment-configured default](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#set-a-default-policy-for-new-runners) when the runner has no policy. Automatic assignment preserves an existing policy.

Users don't select a policy, and they don't need to know one exists. A user describes the sandbox they want. If the policy permits that sandbox, it launches. If the policy forbids part of it, the request is rejected and the error names what was denied.

## How a sandbox resolves against a policy

A sandbox resolves in two stages.

1. **Base**: The policy supplies runtime defaults and attachments, merged in the order runtime defaults, then policy base, then the sandbox spec. Your spec takes precedence for scalar defaults. Policy attachments still apply, and administrator-pinned Pod metadata takes precedence when annotation keys overlap.
2. **Constraints**: Typed clamps are validated against the fully resolved spec. A spec that violates a constraint is rejected, never silently rewritten.

Because constraints validate the resolved spec rather than the submitted one, a value the base supplied is checked on the same terms as a value you supplied.

An empty policy is valid and supplies no base defaults or explicit constraints. Platform safety gates still apply, and an absent runtime-class allowlist permits no concrete `runtime_class` pin. See [`SecurityConstraints`](https://docs.coreweave.com/products/sandboxes/reference/profile#securityconstraints).

## What a policy can constrain

Constraints are grouped by what they govern. Every group is optional. Omitting a group adds no explicit constraints of that kind, but platform safety gates and runtime-class restrictions still apply.

| Group | Governs |
| - | - |
| `resources` | CPU and memory minimums, maximums, defaults, and ceilings, and whether limits are required. |
| `image` | Which registries and images a sandbox may run. |
| `network` | The egress and ingress a sandbox may request, and what it gets when it requests none. |
| `security` | In-guest container privilege, Linux capabilities, seccomp profiles, and runtime classes. |
| `instance` | Which Node instance types a sandbox may land on. |
| `lifecycle` | The default lifetime when a sandbox doesn't request one. The [platform maximum](https://docs.coreweave.com/products/sandboxes/long-running-sandboxes.md#choose-a-lifetime) still applies. |
| `metadata` | Which annotation prefixes are denied. |
| `volumes` | Which storage media are permitted and the maximum volume size. |

Network constraints define allowlists for the access a sandbox can request. A sandbox declares the access it requires, and the policy validates that request against what the cluster permits. The policy separately defines what an absent request means. A sandbox also restricts itself through its access declaration. This is useful when you run an untrusted agent and want to narrow its reach below what the policy would allow.

## Source IP access controls

A policy can also restrict Sandbox API requests by the caller's source address through `control_plane_access.source_ip_allowlist`. The gateway evaluates this control when selecting a runner and before new operations on existing sandboxes, separately from create-time defaults and constraints.

Source IP restrictions supplement authentication and authorization. They don't restrict connections sent directly to a sandbox's exposed services. For configuration and recovery, see [Restrict Sandbox API access by source IP](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#restrict-sandbox-api-access-by-source-ip).

## What changed from profiles

Policies replace profiles with the following changes.

**Users no longer choose anything.** Under profiles, a user picked a profile by name, which meant knowing which profiles existed and having permission to look. When no profile fit, the user asked an administrator to author one. Under policies, the user declares the sandbox they want and the platform either allows it or explains what it denied.

Resolution runs the other way. A profile overrode the values in your sandbox spec. A policy lets your spec override scalar defaults, then constrains the result. Administrator-pinned Pod metadata and other policy attachments still apply.

> [!WARNING]
>
> The inverted resolution is a behavior change, not a rename. A request that a profile would have quietly reshaped might now be rejected outright. Review existing profile configurations against the constraint groups before you migrate them.

Policies are set per cluster. A cluster has no per-team or per-user granularity, so every user resolves against the same policy.

## Where reusable configuration lives

Profiles served a second purpose beyond governance. They were a convenient way to save a set of options and reuse it, one per team or per application.

That role now belongs to sandbox templates, which hold a reusable partial sandbox specification that you can override when you create a sandbox. Templates carry no authority: they're a starting point, and the policy remains the only source of enforcement. See [Sandbox templates](https://docs.coreweave.com/products/sandboxes/profiles/templates.md) for the workflow and complete example templates.

## See also

For related guidance, see the following pages:

* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): the resources that build a sandbox and the gateway that brokers every request.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): the runner lifecycle and the configuration a runner carries.
* [Control plane API overview](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md): authentication, field masks, heartbeats, and the endpoint contract.
