# Sandbox configuration

Source: https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration

# Sandbox configuration

> Configure sandbox resources, images, networking, timeouts, and storage.

This guide covers sandbox configuration options, including resources, mounted files, ports, annotations, and timeouts. Use it as a reference when you need to tailor a sandbox's runtime environment to match the requirements of a workload, such as reserving GPU capacity, exposing a service, or setting operation timeouts.

This page is for developers who use the `cwsandbox` Python SDK to launch and manage sandboxes.

## Choose authentication

Choose the credential for the account that owns your sandboxes. To obtain a Forge API key or CoreWeave API access token, see [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as a `sandbox_auth.py` file beside the Python script that uses it. This file stores only the authentication choice. Import `AUTH` from that file. When you create a sandbox or session, pass `AUTH` explicitly or set it in `SandboxDefaults`.

> [tab] Forge API key
>
> Use your Forge API key with the `wandb` integration in the software development kit (SDK). Replace `[WANDB-API-KEY]` with your API key:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Use the CoreWeave API access token for your organization. Replace `[API-ACCESS-TOKEN]` with your token:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

The examples use serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). For CKS placement, choose a CoreWeave API access token and [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md). Set `placement_mode="cks"` when you create a sandbox or in `SandboxDefaults`.

To authenticate a session and the sandboxes it owns, create the session with `auth=AUTH`. When you reconnect, list, or clean up sandboxes, keep the same credential.

## Overview

You can set sandbox configuration in three places, listed from broadest to most specific scope:

* **SandboxDefaults**: Shared defaults for all sandboxes in a session.
* **Sandbox.run() kwargs**: Per-sandbox overrides.
* **@session.function() kwargs**: Function-specific configuration.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import ResourceOptions, Sandbox, SandboxDefaults, Session

# Via SandboxDefaults
defaults = SandboxDefaults(
    container_image="python:3.11",
    max_lifetime_seconds=3600,
    resources=ResourceOptions(
        requests={"cpu": "2", "memory": "2Gi"},
        limits={"cpu": "2", "memory": "2Gi"},
    ),
)

# Via Sandbox.run() kwargs
sandbox = Sandbox.run(
    defaults=defaults,
    resources=ResourceOptions(
        requests={"cpu": "4", "memory": "4Gi"},
        limits={"cpu": "4", "memory": "4Gi"},
    ),
    auth=AUTH,
)

# Via @session.function() kwargs
with Session(defaults, auth=AUTH) as session:
    @session.function(resources={"cpu": "1", "memory": "1Gi"})
    def compute(x: int) -> int:
        return x * 2
```

The following sections describe each configuration area in detail.

## Resources

Configure CPU, memory, and GPU resources using the `ResourceOptions` dataclass or a plain dict. Serverless is the default placement mode. For serverless sandboxes, set equal CPU and memory requests and limits. For unequal requests and limits, use [CKS placement](#burstable-qos) with a runner whose policy permits them. To choose values, see [Size sandbox CPU and memory](https://docs.coreweave.com/products/sandboxes/resource-sizing.md).

Do not rely on serverless to normalize unequal values. Successful creation with unequal requests and limits does not establish support for resource bursting.

The following examples use equal requests and limits:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import ResourceOptions, Sandbox

# Using ResourceOptions
sandbox = Sandbox.run(
    resources=ResourceOptions(
        requests={"cpu": "2", "memory": "2Gi"},
        limits={"cpu": "2", "memory": "2Gi"},
    ),
    auth=AUTH,
)

# Using dict
sandbox = Sandbox.run(
    resources={
        "requests": {"cpu": "2", "memory": "2Gi"},
        "limits": {"cpu": "2", "memory": "2Gi"},
    },
    auth=AUTH,
)
```

Both forms are equivalent: the SDK automatically converts dicts to `ResourceOptions` internally.

`ResourceOptions` separates resource requests from limits. Requests tell the scheduler what the sandbox needs. Limits set the maximum it can use. For background on how Kubernetes uses requests and limits to assign [Quality of Service classes](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/), see the Kubernetes documentation.

### ResourceOptions fields

| Field | Type | Description |
| - | - | - |
| `requests` | `dict[str, str] \| None` | CPU and memory requests for scheduling (for example, `{"cpu": "500m", "memory": "512Mi"}`). |
| `limits` | `dict[str, str] \| None` | CPU and memory limits the sandbox cannot exceed (for example, `{"cpu": "2", "memory": "2Gi"}`). |
| `gpu` | `dict[str, Any] \| None` | GPU configuration (for example, `{"count": 1, "type": "H100"}`). |

All fields are optional in the client and default to `None`. The resolved allocation must satisfy the applicable policy. If you omit the resource allocation, complete, positive CPU and memory defaults from that policy supply both requests and limits.

### Guaranteed QoS

Guaranteed Quality of Service depends on the resources of every container in the Pod. With container-level allocations, each container must have positive CPU and memory requests, with matching limits for each resource. This includes init containers and sidecars. Equal values for your workload container alone do not establish the QoS class of the whole sandbox Pod. A sandbox that tries to use more CPU than its limit is still throttled.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import ResourceOptions, Sandbox

sandbox = Sandbox.run(
    resources=ResourceOptions(
        requests={"cpu": "2", "memory": "4Gi"},
        limits={"cpu": "2", "memory": "4Gi"},
    ),
    auth=AUTH,
)
```

For equal requests and limits, a flat dict shorthand is available. The SDK normalizes flat dicts by setting both requests and limits to the same values.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

# Flat dict shorthand: requests and limits are set to identical values
sandbox = Sandbox.run(
    resources={"cpu": "2", "memory": "4Gi"},
    auth=AUTH,
)
```

### Burstable QoS

On a CKS runner whose policy permits unequal requests and limits, lower requests give the sandbox a Burstable Quality of Service class. Lower requests let the scheduler bin-pack more sandboxes, but each sandbox can burst up to its limit if capacity is available.

Complete [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) and set `CWSANDBOX_API_KEY` to a CoreWeave API access token. Replace `[RUNNER-ID]` with the ID of a CKS runner whose policy permits these requests and limits:

```python theme={"system"}
from cwsandbox import AuthStrategy, ResourceOptions, Sandbox

sandbox = Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    placement_mode="cks",
    runner_ids=["[RUNNER-ID]"],
    resources=ResourceOptions(
        requests={"cpu": "500m", "memory": "512Mi"},
        limits={"cpu": "4", "memory": "4Gi"},
    ),
)
```

### CPU values

Specify CPU in millicores or whole cores. For details, see [Resource units in Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes).

| Value | Meaning |
| - | - |
| `"100m"` | 100 millicores (0.1 CPU) |
| `"500m"` | 500 millicores (0.5 CPU) |
| `"1000m"` or `"1"` | 1 full CPU core |
| `"2000m"` or `"2"` | 2 CPU cores |

### Memory values

Memory uses standard [Kubernetes memory units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory):

| Value | Meaning |
| - | - |
| `"128Mi"` | 128 mebibytes |
| `"512Mi"` | 512 mebibytes |
| `"1Gi"` | 1 gibibyte |
| `"4Gi"` | 4 gibibytes |

### GPU

Request GPU resources alongside CPU and memory. A GPU request reserves GPUs only, so set CPU and memory explicitly.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import ResourceOptions, Sandbox

sandbox = Sandbox.run(
    resources=ResourceOptions(
        requests={"cpu": "4", "memory": "16Gi"},
        limits={"cpu": "4", "memory": "16Gi"},
        gpu={"count": 1},
    ),
    auth=AUTH,
)
```

GPU configuration keys:

| Key | Type | Description |
| - | - | - |
| `count` | `int` | Number of GPUs to request. |
| `type` | `str` | GPU type, matched exactly against the types a runner advertises in [discovery](https://docs.coreweave.com/products/sandboxes/client/guides/discovery.md). Leave unset on serverless capacity, which assigns the GPU type for you. See [Run a GPU sandbox](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md). |
| `memory_gb` | `int` | Minimum GPU memory in GB. Selects a GPU type on the runner with at least this much memory. When more than one type qualifies, which one you get isn't defined. |

`type` and `memory_gb` are alternatives. Set at most one of them.

### Inspect confirmed resources

After a sandbox starts, inspect the confirmed resource allocation. This example uses unequal requests and limits on CKS. Complete the CKS setup and set `CWSANDBOX_API_KEY` to a CoreWeave API access token. Replace `[RUNNER-ID]` with the ID of a CKS runner that has GPU capacity and a policy that permits these resources:

```python theme={"system"}
from cwsandbox import AuthStrategy, ResourceOptions, Sandbox

with Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    placement_mode="cks",
    runner_ids=["[RUNNER-ID]"],
    resources=ResourceOptions(
        requests={"cpu": "500m", "memory": "512Mi"},
        limits={"cpu": "2", "memory": "2Gi"},
        gpu={"count": 1},
    ),
) as sb:
    print(sb.resource_requests)  # {"cpu": "500m", "memory": "512Mi"}
    print(sb.resource_limits)    # {"cpu": "2", "memory": "2Gi"}
    print(sb.resource_gpu)       # {"count": 1}
```

### Configuration library interop

All configuration types (`NetworkOptions`, `Secret`, `ResourceOptions`) accept either the dataclass or a plain dict. This means ML configuration libraries that resolve configs to dicts or dict-like objects can pass values directly to the SDK without manual conversion.

`SandboxDefaults.from_dict()` accepts a plain dict or an OmegaConf `DictConfig` and coerces nested fields automatically. It converts network and secret configurations to their SDK types and resource mappings to plain dicts. The SDK normalizes those resource dicts to `ResourceOptions` when it constructs a sandbox.

The following configuration uses the same PyTorch 2.8 and CUDA 12.8 image as the [GPU guide](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md#container-images). Before you run a training workload, use that guide's tensor check to confirm basic CUDA execution on the allocated GPU.

```yaml theme={"system"}
# sandbox.yaml
container_image: "pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime"
max_lifetime_seconds: 3600
tags:
  - training
  - experiment-42
resources:
  requests:
    cpu: "4"
    memory: "8Gi"
  limits:
    cpu: "4"
    memory: "8Gi"
  gpu:
    count: 1
network:
  egress:
    - dns_name: "pypi.org"
    - dns_name: "files.pythonhosted.org"
environment_variables:
  LOG_LEVEL: "info"
```

```python theme={"system"}
from sandbox_auth import AUTH
from omegaconf import OmegaConf
from cwsandbox import Sandbox, SandboxDefaults

cfg = OmegaConf.load("sandbox.yaml")
defaults = SandboxDefaults.from_dict(cfg)

with Sandbox.run(defaults=defaults, auth=AUTH) as sb:
    result = sb.exec(["python", "train.py"]).result()
```

Individual fields also accept dicts when you pass them directly to `Sandbox.run()` or `session.sandbox()`. The nested dict form for resources maps to `ResourceOptions` fields. The flat dict form (`{"cpu": "1", "memory": "1Gi"}`) sets matching CPU and memory requests and limits for the workload container. The [Guaranteed QoS requirements](#guaranteed-qos) still apply to every container in the Pod.

## Mounted files

Mounted files let you provide configuration files, scripts, or other read-only assets to the sandbox at startup, without baking them into a container image.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

sandbox = Sandbox.run(
    mounted_files=[
        {
            "mount_path": "/app/config.json",
            "file_content": b'{"debug": true}',
        },
        {
            "mount_path": "/app/script.py",
            "file_content": b"print('hello')",
        },
    ],
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
)

# Files are available immediately
result = sandbox.exec(["python", "/app/script.py"]).result()
```

### Mount options

| Field | Type | Description |
| - | - | - |
| `mount_path` | `str` | Absolute path in sandbox. |
| `file_content` | `bytes \| str` | File content. Strings are encoded as UTF-8. |

Mounted files are read-only. Use `write_file()` for files that require modification.

## Ports

Declare ports with `services=[Service(...)]`. A declaration such as `Service(port=8080, name="web")`, with neither `visibility` nor `endpoint` set, remains container-local and doesn't request external exposure.

To serve HTTP to internet clients, request a public HTTPS endpoint. This example runs on serverless capacity, starts an HTTP server on port `8080`, and requests its assigned HTTPS URL from your local machine. The platform terminates TLS and forwards HTTP to the container port.

The example uses `EndpointAuth.OPEN`, so anyone with the URL can access it without a credential. It uses the demonstration container's `/tmp` directory as its document root. The credential used with `auth=AUTH` authorizes sandbox creation and deletion. It isn't required for requests to this `OPEN` endpoint.

```python theme={"system"}
import time
from urllib.error import URLError
from urllib.request import urlopen

from sandbox_auth import AUTH
from cwsandbox import (
    Endpoint,
    EndpointAuth,
    EndpointKind,
    Sandbox,
    Service,
    ServiceProtocol,
    ServiceVisibility,
)

sandbox = Sandbox.run(
    "python", "-m", "http.server", "8080", "--directory", "/tmp",
    container_image="python:3.11",
    placement_mode="serverless",
    services=[
        Service(
            port=8080,
            name="web",
            protocol=ServiceProtocol.TCP,
            visibility=ServiceVisibility.PUBLIC,
            endpoint=Endpoint(kind=EndpointKind.HTTPS, auth=EndpointAuth.OPEN),
        ),
    ],
    resources={"cpu": "1", "memory": "1Gi"},
    max_lifetime_seconds=300,
    auth=AUTH,
)

try:
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        sandbox.get_status()
        if sandbox.service_urls:
            url = sandbox.service_urls[0][2]
            try:
                with urlopen(url, timeout=10) as response:
                    body = response.read().decode("utf-8")
                    assert response.status == 200
                    assert "Directory listing for /" in body
                    print("HTTP 200: directory listing received")
                    break
            except (URLError, TimeoutError):
                pass  # The URL can appear before the application is ready.
        time.sleep(2)
    else:
        raise TimeoutError("The HTTPS service did not become reachable")
finally:
    Sandbox.delete(sandbox.sandbox_id, auth=AUTH).result()
```

The script retries while the URL and HTTP server become ready, prints `HTTP 200: directory listing received` on success, and deletes the sandbox after the access attempt. The 5-minute lifetime also bounds how long it can run.

The `ports` parameter was removed in cwsandbox 1.x. Passing a value raises `TypeError`. Use `services=[Service(...)]` instead.

### Service fields

| Field | Type | Description |
| - | - | - |
| `port` | `int` | Port the workload listens on inside the sandbox. |
| `name` | `str \| None` | Optional service name. Must be unique within the sandbox. |
| `protocol` | `ServiceProtocol \| str \| None` | Layer 4 protocol. Defaults to TCP. Must be TCP or unset when `endpoint` is set. |
| `visibility` | `ServiceVisibility \| str \| None` | Reachability setting. Must be `PUBLIC` when `endpoint` is set. Plain services can also use `PRIVATE`, `PUBLIC`, or `CUSTOM`. Their reachability depends on the deployment. |
| `endpoint` | `Endpoint \| dict \| None` | Optional public HTTPS or TLS passthrough endpoint. Visibility alone doesn't request an HTTPS URL or TLS passthrough address. |

Each `sandbox.service_urls` entry is a `(port, name, url)` tuple. A URL can appear while the sandbox is still `CREATING`; an assigned URL does not guarantee that the application is listening.

A plain service has no `endpoint` value. For rules about combining plain services and endpoints in one sandbox, see [Declare an endpoint](https://docs.coreweave.com/products/sandboxes/public-endpoints.md#declare-an-endpoint).

For HTTPS, `EndpointAuth.OPEN` allows unauthenticated access. `EndpointAuth.SHARE_TOKEN` requires a share token returned at creation, Python SDK 1.16.0 or later, and a deployment that supports share-token HTTPS.

TLS passthrough leaves endpoint authentication unset. Your workload handles TLS termination and access control. Before you connect, prepare the TLS server, certificate, and private key. The server certificate must cover the assigned endpoint hostname for a client that verifies hostnames.

See [Public endpoints](https://docs.coreweave.com/products/sandboxes/public-endpoints.md) for endpoint routing and authentication. The generated [Service reference](https://docs.coreweave.com/products/sandboxes/client/ref/networking/services.md) and [Endpoint reference](https://docs.coreweave.com/products/sandboxes/client/ref/networking/endpoints.md) describe SDK version 1.14.2, which supports `OPEN` but predates `SHARE_TOKEN`.

## Network

Configure outbound and inbound traffic using the `NetworkOptions` dataclass or a plain dict. Egress and ingress rules grant access over a default-deny baseline. A nonempty `egress` list replaces the runner policy's default destination grants.

Hostname grants require a runner that supports hostname-based HTTPS egress and a policy that permits every requested destination. For CKS placement, ask your administrator to check the runner's [network constraints](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-network-access). For serverless placement, CoreWeave manages the pool and its policy. If the pool rejects these hostname rules, contact CoreWeave support.

To download packages from PyPI, allow both `pypi.org` for the package index and `files.pythonhosted.org` for package files. The `pypi.org` and `*.pypi.org` grants don't cover `files.pythonhosted.org`:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import EgressRule, NetworkOptions, Sandbox

# Using NetworkOptions
sandbox = Sandbox.run(
    network=NetworkOptions(
        egress=[
            EgressRule(dns_name="pypi.org"),
            EgressRule(dns_name="*.pypi.org"),
            EgressRule(dns_name="files.pythonhosted.org"),
        ],
    ),
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
)

# Using dict
sandbox = Sandbox.run(
    network={
        "egress": [
            {"dns_name": "pypi.org"},
            {"dns_name": "*.pypi.org"},
            {"dns_name": "files.pythonhosted.org"},
        ],
    },
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
)
```

Both forms are equivalent: the SDK automatically converts dicts to `NetworkOptions` internally.

### NetworkOptions fields

| Field | Type | Description |
| - | - | - |
| `deny_egress` | `bool \| None` | When `True`, suppresses default and declared egress destination grants. DNS access is controlled separately and remains allowed unless the policy denies DNS. Can't be combined with a nonempty `egress` list. An empty list is accepted. |
| `deny_ingress` | `bool \| None` | Denies declared and policy-default ingress to `CUSTOM` services when `True`. Don't combine with a non-empty `ingress` list. |
| `egress` | `Sequence[EgressRule \| dict] \| None` | Egress grants. A DNS name grants HTTPS (TCP 443) only. |
| `ingress` | `Sequence[IngressRule \| dict] \| None` | Ingress sources for `CUSTOM`-visibility ports. |

All fields are optional and default to `None`. An empty rule list with its deny flag unset or `False` uses the runner policy default. Port exposure uses `services`, not `NetworkOptions`. For every `EgressRule` and `IngressRule` field, see [Network rules](https://docs.coreweave.com/products/sandboxes/client/ref/networking/network-rules.md).

An `EgressRule` requires exactly one destination: `dns_name`, `cidr`, `tenant`, `any`, or `selector`. A DNS grant accepts an exact name or a single leftmost wildcard such as `*.pypi.org`. An `IngressRule` requires exactly one source: `cidr`, `tenant`, or `any`.

The `egress_mode`, `ingress_mode`, and `exposed_ports` fields are not supported in cwsandbox 1.x. Use the fields above and declare ports with `services`.

`deny_egress=True` isn't complete network isolation. Platform-required traffic can remain available, and outbound DNS is controlled separately. The Python `NetworkOptions` type doesn't expose `dnsEgress`. Use the [NetworkConfig API](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md) to change that mode where supported.

> [!NOTE]
>
> The Python SDK applies network options when it creates a sandbox and doesn't provide methods to update a running sandbox's network policy. For the API workflow, see [Dynamic network policies](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md). Exposed ports and service visibility remain creation-time settings.

### Set network in SandboxDefaults

Set a default network configuration for all sandboxes:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import EgressRule, NetworkOptions, SandboxDefaults, Session

defaults = SandboxDefaults(
    network=NetworkOptions(
        egress=[
            EgressRule(dns_name="pypi.org"),
            EgressRule(dns_name="files.pythonhosted.org"),
        ],
    ),
    resources={"cpu": "1", "memory": "1Gi"},
)

with Session(defaults, auth=AUTH) as session:
    # All sandboxes inherit the network config
    sb1 = session.sandbox()
    sb2 = session.sandbox()

    # Suppress destination grants for this sandbox. DNS is controlled separately
    sb3 = session.sandbox(network=NetworkOptions(deny_egress=True))
```

A per-sandbox `network` replaces the `SandboxDefaults.network` value rather than merging with it. In the example above, `sb3` suppresses destination grants; DNS remains controlled separately.

## Annotations

Add Kubernetes pod annotations to sandboxes. Annotations are key-value string pairs attached to the underlying pod, useful for integrations that read pod metadata, such as schedulers, cost-allocation tools, or external automation.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

sandbox = Sandbox.run(
    annotations={
        "team": "ml-infra",
        "experiment": "training-run-42",
    },
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
)
```

### Session-level defaults

Set default annotations for all sandboxes in a session:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import SandboxDefaults, Session

defaults = SandboxDefaults(
    annotations={
        "team": "ml-infra",
        "managed-by": "sandbox-sdk",
    },
    resources={"cpu": "1", "memory": "1Gi"},
)

with Session(defaults, auth=AUTH) as session:
    # Inherits default annotations
    sb1 = session.sandbox()

    # Merge: explicit annotations override defaults on key collision
    sb2 = session.sandbox(
        annotations={"experiment": "run-42", "team": "ml-research"},
    )
    # sb2 receives: team=ml-research, managed-by=sandbox-sdk, experiment=run-42
```

### Merge behavior

For single-container sandboxes created with `Sandbox.run()` or `session.sandbox()` without `template_id`, the SDK merges `SandboxDefaults.annotations` with per-sandbox `annotations`. Explicit per-sandbox values override defaults with the same key. The SDK merges `environment_variables` the same way for these sandboxes.

For template creation, the SDK doesn't merge `SandboxDefaults.annotations` or `SandboxDefaults.environment_variables` into the request. For template override rules, see the [`Sandbox.run_from_template()` reference](https://docs.coreweave.com/products/sandboxes/client/ref/core/sandbox#run_from_template).

`Sandbox.run_from_file()` merges default annotations with explicit `annotations`, but doesn't inherit `SandboxDefaults.environment_variables`. The Compose file supplies the container environment variables. See the [`Sandbox.run_from_file()` reference](https://docs.coreweave.com/products/sandboxes/client/ref/core/sandbox#run_from_file).

### SUNK integration

To pass Slurm context as pod annotations for SUNK integration, see the [SUNK Pod Scheduler integration guide](https://docs.coreweave.com/products/sandboxes/profiles/sunk-integration.md#step-4-control-placement-with-slurm-annotations).

### Validation

The SDK does not validate annotation keys or values. The server handles validation of reserved key prefixes, value format, and maximum entry count.

## Secrets

For Forge team secret injection, authentication requirements, and Python and TypeScript examples, see [Use Forge secrets](https://docs.coreweave.com/products/sandboxes/secrets.md).

## Timeouts

Three settings control how long a sandbox and its operations run. The names are similar, so the following table maps each one to what it bounds.

| Setting | Bounds | Enforced by | Default |
| - | - | - | - |
| `max_lifetime_seconds` | Total sandbox lifetime before automatic termination | Server | Runner-policy default, or 10 minutes if none is set |
| `timeout_seconds` | A single `exec()`, `read_file()`, or `write_file()` call | Client | Falls back to `request_timeout_seconds` |
| `request_timeout_seconds` | Client-side HTTP timeout for most remote procedure calls (RPCs) | Client | 300 seconds |

Only `max_lifetime_seconds` terminates a sandbox. The other two bound individual requests and leave the sandbox running.

The `max_timeout_seconds` parameter was removed in cwsandbox 1.x. Passing a value raises `TypeError`; use `request_timeout_seconds` for the client request timeout.

### max\_lifetime\_seconds

`max_lifetime_seconds` sets the total wall-clock lifetime of a sandbox. When a sandbox reaches this age, the platform terminates it even if work is still in progress.

If you don't set `max_lifetime_seconds`, the runner-policy default applies. If no positive policy default supplies a lifetime, the platform uses 10 minutes. Set the value explicitly for long-running work:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(
    max_lifetime_seconds=7200,  # 2 hours
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    sandbox.exec(["python", "train.py"], timeout_seconds=7000).result()
```

To apply one lifetime to every sandbox a session creates, set it in `SandboxDefaults`:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, SandboxDefaults

defaults = SandboxDefaults(
    container_image="python:3.11",
    max_lifetime_seconds=3600,  # 1 hour
    resources={"cpu": "1", "memory": "1Gi"},
)

with Sandbox.run(defaults=defaults, auth=AUTH) as sandbox:
    sandbox.exec(["python", "-c", "print('working')"]).result()
```

An explicit `max_lifetime_seconds` argument on `Sandbox.run()` takes precedence over the value in `defaults`. Because the argument's default is `None`, you can't use it to remove a lifetime that `defaults` already sets.

The longest lifetime you can request is 30 days (2,592,000 seconds), for both serverless and CKS placement. The platform rejects larger requests.

> [!WARNING]
>
> You can't change `max_lifetime_seconds` after a sandbox starts. No API extends the lifetime of a running sandbox, so choose the value when you create it. To keep working past the limit, capture what you need and start a new sandbox with a lifetime of up to 30 days.

For creation examples and CKS runner-policy defaults, see [Run long-running sandboxes](https://docs.coreweave.com/products/sandboxes/long-running-sandboxes.md).

#### Behavior when the lifetime expires

The platform enforces the lifetime with a deadline on the sandbox's underlying Kubernetes Job. Reaching the deadline triggers workload termination even if work is still in progress. Save results or checkpoints outside the sandbox before expiry.

The Python SDK exposes the backend-reported reason in `Sandbox.status_reason`, cached from the latest API response. Lifetime expiry can appear as a reason beginning with `DeadlineExceeded`. If the SDK raises `SandboxFailedError`, its `status_reason` attribute also carries the backend-reported reason. A reason can be absent, so track the age of long-lived sandboxes as well.

Set a lifetime that comfortably exceeds the work you expect. When you finish, [stop sandboxes explicitly](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md) rather than relying on expiry.

### timeout\_seconds

`timeout_seconds` bounds a single operation on a running sandbox:

```python theme={"system"}
result = sandbox.exec(
    ["python", "long_script.py"],
    timeout_seconds=300,  # 5 minutes
).result()
```

This controls how long the client waits for a response. If the wait exceeds the timeout, the SDK raises `SandboxTimeoutError`. The sandbox keeps running. The clock starts only after the sandbox reaches `RUNNING`, so startup time doesn't count against it.

Keep `timeout_seconds` below the sandbox's `max_lifetime_seconds`. A command whose timeout exceeds the sandbox's remaining lifetime stops when the sandbox terminates.

### request\_timeout\_seconds

`request_timeout_seconds` is the client-side HTTP timeout applied to most RPCs, and it's the fallback when a call doesn't pass its own `timeout_seconds`. Set it in `SandboxDefaults`:

```python theme={"system"}
from cwsandbox import SandboxDefaults

defaults = SandboxDefaults(
    request_timeout_seconds=600.0,
    resources={"cpu": "1", "memory": "1Gi"},
)
```

Status polling uses `poll_rpc_timeout_seconds` instead, so a stalled poll fails fast rather than blocking for the full request timeout. For the full set of client-side tuning options, see the [SandboxDefaults reference](https://docs.coreweave.com/products/sandboxes/client/ref/core/sandbox-defaults.md).

## Complete example

The following example combines defaults, per-sandbox overrides, mounted files, and service declarations. It downloads packages from PyPI and imports them to check the installation. The serverless pool must meet the [hostname grant requirements](#network).

This example declares a service port but doesn't start a server or create a public endpoint:

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import (
    EgressRule,
    NetworkOptions,
    ResourceOptions,
    Sandbox,
    SandboxDefaults,
    Service,
)

defaults = SandboxDefaults(
    container_image="python:3.11",
    max_lifetime_seconds=1800,  # 30 minutes
    tags=("production", "ml-pipeline"),
    resources=ResourceOptions(
        requests={"cpu": "4", "memory": "8Gi"},
        limits={"cpu": "4", "memory": "8Gi"},
    ),
    network=NetworkOptions(
        egress=[
            EgressRule(dns_name="pypi.org"),
            EgressRule(dns_name="*.pypi.org"),
            EgressRule(dns_name="files.pythonhosted.org"),
        ],
    ),
)

with Sandbox.run(
    defaults=defaults,
    mounted_files=[
        {
            "mount_path": "/app/config.yaml",
            "file_content": b"model: gpt-4\nmax_tokens: 1000",
        },
    ],
    services=[
        Service(port=8000, name="api"),
    ],
    auth=AUTH,
) as sandbox:
    # Install dependencies without cached downloads
    sandbox.exec(
        ["pip", "install", "--no-cache-dir", "fastapi", "uvicorn"],
        check=True,
    ).result()

    # Verify the installed dependencies
    result = sandbox.exec(
        ["python", "-c", "import fastapi, uvicorn; print('Dependencies imported')"],
        check=True,
        timeout_seconds=60,
    ).result()
    print(result.stdout)
```
