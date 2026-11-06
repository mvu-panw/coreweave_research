# Sandbox templates

Source: https://docs.coreweave.com/products/sandboxes/profiles/templates

# Sandbox templates

> Create reusable templates, start sandboxes from them, and add admin Pod settings on CoreWeave Kubernetes Service (CKS).

A sandbox template is an organization-scoped, reusable partial sandbox specification. Instead of repeating the same container image, resources, services, and network rules on every create request, you store them once as a template and start sandboxes from it, overriding only what differs per run.

Templates carry no authority. They're a starting point for a sandbox specification, and the runner's policy remains the only source of enforcement. A sandbox created from a template is validated against the policy exactly as if you had written the full specification by hand.

This page shows how to create and manage templates, how to start sandboxes from them, and complete template documents for common use cases. Replace `TEMPLATE_ID` with the template's universally unique identifier (UUID) and `SNAPSHOT_ID` with a file system snapshot ID. Replace `GITHUB_ORG` with your GitHub Container Registry organization or user name.

## Create a template

Organization admins manage templates. Write operations require the **Sandbox Admin** role. Every sandbox user in the organization can read templates and start sandboxes from them.

> [tab] CLI
>
> Create a template from a file:
>
> ```bash theme={"system"}
> cwic sandbox template create -f template.json
> ```
>
> Inspect and list existing templates:
>
> ```bash theme={"system"}
> cwic sandbox template describe TEMPLATE_ID
> ```
>
> ```bash theme={"system"}
> cwic sandbox template get
> ```

> [tab] curl
>
> ```bash title="Create a template" theme={"system"}
> curl -X POST https://api.coreweave.com/v1/sandboxTemplates \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d @template.json
> ```
>
> The request body is the template document itself, not a wrapper object.

A minimal development-box template looks like this:

```json title="template.json" theme={"system"}
{
  "displayName": "python-dev-box",
  "spec": {
    "containers": [
      {
        "name": "main",
        "image": "python:3.11",
        "resourceRequirements": {
          "requests": { "cpu": "1", "memory": "2Gi" },
          "limits": { "cpu": "1", "memory": "2Gi" }
        }
      }
    ],
    "maxLifetimeSeconds": 14400,
    "tags": ["dev-box"]
  }
}
```

The following rules apply to every template write:

* **`displayName` is required** and must be unique among the organization's active templates: 1 to 128 characters after trimming. Prefer names that aren't UUID-shaped, so they don't collide with ID-first lookup.
* **`spec` is a partial sandbox specification**, capped at 1 MiB. It uses the same fields as a create request, and everything in it can be overridden at create time.
* **`spec` can't select an instance type or attach sandbox networks yet**: A template that sets `instanceType` or `networkIds` is rejected as unimplemented.
* **Template contents are visible to every sandbox user in the organization**: A template isn't a secret-distribution channel. Literal credentials don't belong in one.

## Start a sandbox from a template

Start a sandbox from a template by ID. Selection is by UUID only. Display names work for lookup and listing, not for create.

```bash title="Create a sandbox from a template" theme={"system"}
curl -X POST https://api.cwsandbox.com/v1/sandboxes:createFromTemplate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "templateId": "TEMPLATE_ID" }'
```

To change something per run through the HTTP API, pass `overrides` with the same shape as a sandbox specification. Overrides replace whole fields:

* A message you set replaces the template's whole message. A message you omit keeps the template's value.
* A non-empty list replaces the template's whole list. An empty JSON list, such as `tags: []` or `services: []`, preserves the template's list. To remove some entries, send the full non-empty list you want to keep. An empty list can't clear an inherited list.
* A map you set replaces the template's whole map. For example, `annotations: {}` clears inherited annotations in a direct HTTP request. Software development kit (SDK) serialization can differ. See the version-specific TypeScript behavior in this section.
* Overriding any container field replaces the entire container list. A template container has no sparse patch, so an override that touches the container must carry the full container, including `image`.

```bash title="Override the container per run" theme={"system"}
curl -X POST https://api.cwsandbox.com/v1/sandboxes:createFromTemplate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "TEMPLATE_ID",
    "overrides": {
      "containers": [
        {
          "name": "main",
          "image": "python:3.12",
          "command": "sleep",
          "args": ["infinity"]
        }
      ]
    }
  }'
```

The sandbox stores the materialized specification at create time, together with the source template ID and revision. Editing or deleting the template later never changes sandboxes that already exist.

The Python and TypeScript clients wrap this endpoint as `Sandbox.run_from_template()` and `client.runFromTemplate()`. See the [Python client](https://docs.coreweave.com/products/sandboxes/client.md) for the Python workflow.

In version 1.0.0 of the TypeScript client, `tags: []`, `services: []`, `annotations: {}`, and `runnerIds: []` preserve template values. `network: {}` replaces the template network. For per-field override behavior, see [`SandboxRunFromTemplateOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/sandboxes#sandboxrunfromtemplateoptions).

## Example templates

The following examples are complete documents for `cwic sandbox template create -f template.json`. Unlike a policy, an organization can hold many templates, so these compose: create one per recurring workload shape.

### Web service with a public HTTPS endpoint

A template for sandboxes that serve HTTP to the public internet through a platform-issued HTTPS endpoint. The assigned URL is echoed on the sandbox after create.

```json title="template.json" theme={"system"}
{
  "displayName": "public-http-service",
  "spec": {
    "containers": [
      {
        "name": "main",
        "image": "python:3.11",
        "command": "python",
        "args": ["-m", "http.server", "8000"]
      }
    ],
    "services": [
      {
        "name": "http",
        "port": 8000,
        "visibility": "VISIBILITY_PUBLIC",
        "endpoint": {
          "kind": "ENDPOINT_KIND_HTTPS",
          "auth": "ENDPOINT_AUTH_OPEN"
        }
      }
    ]
  }
}
```

Public exposure is governed by the selected runner's advertised network capability, so this template only works on runners configured for public endpoints.

### Workspace restored from a snapshot

A template whose scratch volume starts from the same file system snapshot every time: a golden workspace that each sandbox forks privately.

```json title="template.json" theme={"system"}
{
  "displayName": "golden-workspace",
  "spec": {
    "containers": [
      {
        "name": "main",
        "image": "python:3.11",
        "volumeMounts": [{ "volume": "workspace", "mountPath": "/workspace" }]
      }
    ],
    "volumes": [
      {
        "name": "workspace",
        "scratch": {
          "size": "10Gi",
          "restoreFromSnapshotId": "SNAPSHOT_ID"
        }
      }
    ]
  }
}
```

See [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) for producing the snapshot this template restores from.

### Curated egress

A template that grants a fixed set of destinations: one classless inter-domain routing (CIDR) range on port `443` plus sibling sandboxes in the same organization. Every rule must fit inside the runner policy's `allowedEgress` envelope, or the create is rejected.

```json title="template.json" theme={"system"}
{
  "displayName": "curated-egress",
  "spec": {
    "containers": [{ "name": "main", "image": "python:3.11" }],
    "network": {
      "egress": [
        { "cidr": { "cidr": "140.82.112.0/20" }, "ports": [{ "port": 443 }] },
        { "tenant": "TENANT_SCOPE_SAME_ORG" }
      ]
    }
  }
}
```

A template with an empty or omitted `network.egress` opts into the policy's `defaultEgress` when `network.denyEgress` is unset or `false`. Keep the egress list on the template when the workload's destinations are known, and leave it empty when the policy default is the right posture.

With the [dynamic network configuration API](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md), each sandbox created from a template receives its own network configuration. Templates keep inline network rules and can't pin a `networkConfigId`. For the create-time override, see [Sandbox and template fields](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md#sandbox-and-template-fields).

### CKS-only: Pod attachments

On your own CKS cluster, an admin can put an `attachments` block on a template: a Kubernetes Pod-specification fragment applied to every sandbox created from it. This is how a template pins Node selection, tolerations, or a pull Secret that the sandbox specification itself has no fields for.

```json title="template.json" theme={"system"}
{
  "displayName": "gpu-training",
  "spec": {
    "containers": [
      {
        "name": "main",
        "image": "ghcr.io/GITHUB_ORG/train:latest",
        "resourceRequirements": {
          "requests": { "cpu": "8", "memory": "32Gi" },
          "limits": { "cpu": "8", "memory": "32Gi" }
        }
      }
    ]
  },
  "attachments": {
    "spec": {
      "nodeSelector": { "workload": "gpu" },
      "tolerations": [
        { "key": "nvidia.com/gpu", "operator": "Exists", "effect": "NoSchedule" }
      ],
      "imagePullSecrets": [{ "name": "regcred" }]
    },
    "metadata": {
      "labels": { "team": "ml" }
    }
  }
}
```

Attachments change how the template behaves:

* **A template with attachments is CKS-only**: Its `requiresCks` output field is `true`, and creating from it with `mode` set to `SANDBOX_MODE_SERVERLESS` fails with `FailedPrecondition`. An unset mode is treated as CKS.
* **Attachments are admin-owned**: Only `sandbox_admin` can write them, plain create requests can't supply them, and create-time overrides can't change or remove them.
* **The fragment uses Kubernetes JSON**, with camelCase keys under `spec` and `metadata`, unlike the sandbox specification fields elsewhere in the template. Unknown keys are rejected.
* **The allowed surface is deliberately narrow**: scheduling and runtime configuration such as `nodeSelector`, `tolerations`, `imagePullSecrets`, `volumes`, `topologySpreadConstraints`, `hostAliases`, DNS settings, and a single `containers` entry limited to `name`, `env`, `envFrom`, `volumeMounts`, and `volumeDevices`, plus Pod labels and annotations. Security-sensitive fields are rejected: `securityContext`, `runtimeClassName`, `initContainers`, `affinity`, host namespaces, `hostPath` volumes, and non-default ServiceAccounts, among others.
* **Attachments layer on top of the policy's `base` fragment**: List-valued fields combine with the policy base: `imagePullSecrets` and `tolerations` are deduplicated, while `topologySpreadConstraints`, `hostAliases`, and `readinessGates` append. Single-valued fields such as `nodeSelector` keys specialize the base. A same-name volume, environment variable, or mount-path conflict between the two layers rejects the create.

## Manage templates

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox template edit TEMPLATE_ID -f template.json
> ```
>
> ```bash theme={"system"}
> cwic sandbox template delete TEMPLATE_ID
> ```

> [tab] curl
>
> ```bash title="Update a template" theme={"system"}
> curl -X PATCH https://api.coreweave.com/v1/sandboxTemplates/TEMPLATE_ID \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -d @template.json
> ```
>
> ```bash title="Delete a template" theme={"system"}
> curl -X DELETE https://api.coreweave.com/v1/sandboxTemplates/TEMPLATE_ID \
>   -H "Authorization: Bearer $TOKEN"
> ```

The following rules apply when you read, update, or delete a template:

* **Reads accept an ID or a display name**: If the path segment parses as a UUID it's looked up by ID. Otherwise it's resolved as a display name among active templates.
* **Every successful update increments the template's `revision`**: Sandboxes record the revision they were created from, so you can tell which sandboxes predate a template change.
* **Delete is a soft delete**: Existing sandboxes are unaffected, new creates can no longer select the template, and the display name becomes reusable for a new template.

## Next steps

For related guidance, see the following pages:

* [Policy examples](https://docs.coreweave.com/products/sandboxes/profiles/profile-examples.md): complete runner policies to pair these templates with.
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): the constraint groups a template's spec is validated against.
* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how templates and policies divide the work profiles used to do.
* [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md): runner setup and your first sandbox.
