# Discover available runners

Source: https://docs.coreweave.com/products/sandboxes/client/guides/discovery

# Discover available runners

> List the runners in your organization, read the hardware they advertise, and check free capacity.

Use the discovery API to list the runners registered to your organization, read the
hardware and features each one advertises, and check live capacity before you place a
sandbox on it.

A runner is a deployment in a CKS cluster. It registers with CoreWeave's managed
control plane and bridges the cluster's compute into the sandbox platform. A
runner's advertised capabilities reflect the cluster's hardware and configuration.

Discovery applies to CKS placement. A serverless sandbox doesn't run on a runner you
own, so there's nothing to discover: describe the sandbox you want and the platform
places it. See [Sandbox placement](https://docs.coreweave.com/products/sandboxes/placement.md).

Discovery reports advertised capabilities. A capability value doesn't grant
permission to use that feature: the runner's admission policy still bounds what an
individual sandbox may request. See [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md).

> [!NOTE]
>
> **Coming from profiles?** The client no longer exports `Profile`,
> `list_profiles()`, `get_profile()`, or `ProfileNotFoundError`. `profile_names` and
> `profile_ids` survive as parameter names on `Sandbox`, `Session`, and their `list()`
> methods, but passing a value raises `TypeError`. Target a runner with `runner_ids`
> instead. Policies replaced profiles as the governance model, and you don't select
> one: see [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md).

## List runners

`list_runners()` returns every runner your credentials can see:

```python theme={"system"}
from cwsandbox import AuthStrategy, Runner, list_runners

runners: list[Runner] = list_runners(auth=AuthStrategy.COREWEAVE_API_KEY)

for runner in runners:
    print(runner)
```

`Runner` has a built-in representation that prints the runner ID, the owning
organization, health, CPU and memory in human-readable units, the GPU count, and the
service visibilities the runner can enforce.

Sample output:

```text theme={"system"}
Runner(runner_id='prod-us-east-1', organization_id='1a2b3c4d', healthy=True, cpu=512.0 vCPU, memory=4.0 TiB, gpus=64, visibilities=['public', 'private'])
```

## Read runner capabilities

Each runner advertises its hardware and supported features. Read these attributes to
find a runner with the capabilities your sandbox needs:

```python theme={"system"}
from cwsandbox import AuthStrategy, list_runners

for runner in list_runners(auth=AuthStrategy.COREWEAVE_API_KEY):
    print(runner.runner_id)
    print(f"  gpu types:     {', '.join(runner.supported_gpu_types) or 'none'}")
    print(f"  max gpus:      {runner.max_gpu_count}")
    print(f"  architectures: {', '.join(runner.supported_architectures)}")
    print(f"  storage:       {', '.join(runner.available_storage_classes)}")
```

`supported_gpu_types` holds the exact strings to pass as the `type` key of a GPU
request. Matching is case-sensitive, so `B200` and `b200` aren't the same type. See
[Run a GPU sandbox](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md).

`max_gpu_count` is the runner's reported aggregate GPU capacity, not a per-sandbox
cap. The runner's policy uses `maxGpuCount` to cap the GPUs each container may
request. GPU requests are supported only on the primary container. The
request must also fit within your organization's maximum number of GPUs per sandbox
and the free GPUs on a single Node.

### Runner attributes

A `Runner` carries the following attributes:

| Attribute | Type | Description |
| - | - | - |
| `runner_id` | `str` | Identifier for the runner within its organization. Not globally unique. |
| `organization_id` | `str` | Organization that owns the runner. |
| `runner_group_id` | `str` | Group the runner belongs to. |
| `tags` | `tuple[str, ...]` | Tags on the runner. |
| `healthy` | `bool` | Whether the runner is currently healthy. |
| `is_shared` | `bool` | `True` when the runner belongs to a shared organization. |
| `connected_at` | `datetime` | When the runner connected, as a UTC-aware datetime. |
| `max_cpu_millicores` | `int` | Reported aggregate CPU capacity, in millicores. |
| `max_memory_bytes` | `int` | Reported aggregate memory capacity, in bytes. |
| `max_gpu_count` | `int` | Reported aggregate GPU capacity. |
| `supported_gpu_types` | `tuple[str, ...]` | GPU types the runner's Nodes carry. |
| `supported_architectures` | `tuple[str, ...]` | CPU architectures the runner supports, such as `amd64`. |
| `supports_privileged` | `bool` | Whether the runner reports support for privileged containers. A `True` value doesn't grant permission to run them. The runner's policy still applies. |
| `available_storage_classes` | `tuple[str, ...]` | Kubernetes storage classes available on the cluster. |
| `supported_service_visibilities` | `tuple[str, ...]` | Service visibilities the runner can enforce: `public`, `private`, or `custom`. See [`ServiceVisibility`](https://docs.coreweave.com/products/sandboxes/client/ref/networking/services#servicevisibility). |
| `resources` | `RunnerResources \| None` | Live resource availability, or `None` when the runner doesn't report it. |

A `max_*` value of `0` can mean the runner doesn't disclose or report that capacity, not
that it has no resources. Shared runners return `0` because their capacity is withheld,
and CPU and memory values can exclude reserved capacity.

## Check live capacity

By default, `list_runners()` returns capability data only. Pass
`include_resources=True` to populate `Runner.resources` with live availability. Use
`format_bytes()` and `format_cpu()` to print the values in human-readable units:

```python theme={"system"}
from cwsandbox import AuthStrategy, format_bytes, format_cpu, list_runners

runners = list_runners(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    include_resources=True,
)

for r in runners:
    print(f"{r.runner_id}  healthy={r.healthy}")
    print(f"  max: {format_cpu(r.max_cpu_millicores)}, {format_bytes(r.max_memory_bytes)}")
    if r.resources:
        free_cpu = format_cpu(r.resources.available_cpu_millicores)
        free_mem = format_bytes(r.resources.available_memory_bytes)
        print(f"  free:  {free_cpu}, {free_mem}, {r.resources.available_gpu_count} GPUs")
        print(f"  running sandboxes: {r.resources.running_sandboxes}")
```

`resources` is `None` when a runner doesn't report availability, so guard on it
before you read the values.

### RunnerResources attributes

A `RunnerResources` object carries the following attributes:

| Attribute | Type | Description |
| - | - | - |
| `available_cpu_millicores` | `int` | Unreserved CPU, in millicores. |
| `available_memory_bytes` | `int` | Unreserved memory, in bytes. |
| `available_gpu_count` | `int` | Unreserved GPUs. |
| `running_sandboxes` | `int` | Sandboxes currently running on the runner. |

## Filter the list

Combine filters to narrow the list to runners that can take your workload. The
following call returns healthy runners that carry a given GPU type and have at least
two GPUs free. Replace `[GPU-TYPE]` with a value from `supported_gpu_types`:

```python theme={"system"}
from cwsandbox import AuthStrategy, list_runners

runners = list_runners(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    gpu_type="[GPU-TYPE]",
    healthy_only=True,
    min_available_gpu_count=2,
)

for r in runners:
    print(f"{r.runner_id}: {r.resources.available_gpu_count} GPUs free")
```

The discovery service applies `runner_group_id`, `gpu_type`, `architecture`,
`healthy_only`, and `service_visibility`. The client applies the three
`min_available_*` filters after the results arrive. Those three turn on
`include_resources` for you, and they drop any runner that reports no resource data,
so `resources` is always populated on what they return.

### Parameters

The following parameters are available on `list_runners()`. All are keyword-only.

| Parameter | Type | Description |
| - | - | - |
| `auth` | `AuthConfig \| None` | Authentication strategy, resolved headers, or provider for this request. |
| `runner_group_id` | `str \| None` | Restrict results to this runner group. |
| `gpu_type` | `str \| None` | Only return runners that support this GPU type. |
| `architecture` | `str \| None` | Only return runners that support this CPU architecture. |
| `healthy_only` | `bool` | Only return healthy runners. Defaults to `False`. |
| `include_resources` | `bool` | Include live resource availability on each runner. Defaults to `False`. |
| `min_available_cpu_millicores` | `int \| None` | Minimum unreserved CPU millicores. Enables `include_resources` automatically. |
| `min_available_memory_bytes` | `int \| None` | Minimum unreserved memory bytes. Enables `include_resources` automatically. |
| `min_available_gpu_count` | `int \| None` | Minimum unreserved GPU count. Enables `include_resources` automatically. |
| `service_visibility` | `str \| None` | Only return runners that can enforce this service visibility: `public`, `private`, or `custom`. |

## Get a single runner

`get_runner()` takes a runner ID and the organization that owns it. A runner ID is
unique within its organization rather than globally, so both are required. The call
always returns full details, but resource availability is included only for runners
your organization owns. Replace `[RUNNER-ID]` and `[ORGANIZATION-ID]` with the runner
you want and the organization that owns it:

```python theme={"system"}
from cwsandbox import AuthStrategy, RunnerNotFoundError, get_runner

try:
    runner = get_runner(
        "[RUNNER-ID]",
        organization_id="[ORGANIZATION-ID]",
        auth=AuthStrategy.COREWEAVE_API_KEY,
    )
    print(f"{runner.runner_id}  healthy={runner.healthy}")
    if runner.resources:
        print(f"  running sandboxes: {runner.resources.running_sandboxes}")
except RunnerNotFoundError as e:
    print(f"Runner not found: {e.runner_id}")
```

Every runner you list carries its own `organization_id`, so pass
`runner.organization_id` when you look up a runner you found in an earlier result.

## Create a sandbox on a discovered runner

Set `placement_mode="cks"` and pass the runner you selected to `runner_ids`. Replace
`[GPU-TYPE]` with a value from `supported_gpu_types`:

```python theme={"system"}
from cwsandbox import AuthStrategy, ResourceOptions, Sandbox, list_runners

runners = list_runners(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    gpu_type="[GPU-TYPE]",
    min_available_gpu_count=1,
)

if runners:
    with Sandbox.run(
        auth=AuthStrategy.COREWEAVE_API_KEY,
        placement_mode="cks",
        runner_ids=[runners[0].runner_id],
        resources=ResourceOptions(
            requests={"cpu": "2", "memory": "8Gi"},
            limits={"cpu": "2", "memory": "8Gi"},
            gpu={"count": 1, "type": "[GPU-TYPE]"},
        ),
        max_lifetime_seconds=3600,
    ) as sandbox:
        print(sandbox.exec(["nvidia-smi", "-L"]).result().stdout)
```

Without `runner_ids`, CKS placement can use any eligible runner in your organization.
`runner_ids` is incompatible with serverless placement and with
`placement_spillover="serverless_then_cks"`.

### Apply a runner to every sandbox in a session

Use `SandboxDefaults` to send every sandbox in a session to the same runner:

```python theme={"system"}
from cwsandbox import AuthStrategy, SandboxDefaults, Session, list_runners

runners = list_runners(auth=AuthStrategy.COREWEAVE_API_KEY, healthy_only=True)

if runners:
    defaults = SandboxDefaults(
        auth=AuthStrategy.COREWEAVE_API_KEY,
        placement_mode="cks",
        runner_ids=(runners[0].runner_id,),
    )

    with Session(defaults) as session:
        sb = session.sandbox()
        print(sb.exec(["echo", "running on a discovered runner"]).result().stdout)
```

For the rest of the sandbox options, see the
[sandbox configuration guide](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md).

## Error reference

Discovery calls can raise the following exceptions.

| Exception | Cause |
| - | - |
| `RunnerNotFoundError` | No runner matches the given `runner_id` and `organization_id`. |
| `DiscoveryValidationError` | A discovery request failed field-level validation. |
| `DiscoveryError` | Network or service error during a discovery operation. Base class for the two above. |
| `CWSandboxAuthenticationError` | Invalid or missing credentials. |

When `runner_id` or `organization_id` is empty, `get_runner()` raises `ValueError`
before it makes a request.

For the full exception hierarchy, see the
[exceptions reference](https://docs.coreweave.com/products/sandboxes/client/ref/exceptions/exceptions.md).
For common troubleshooting steps, see the
[Sandboxes support articles](https://docs.coreweave.com/support/sandboxes.md).
