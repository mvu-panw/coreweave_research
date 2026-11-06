# Volumes

Source: https://docs.coreweave.com/products/sandboxes/volumes

# Volumes

> Give a sandbox writable scratch space, or mount a registered volume that several sandboxes share.

A volume is storage that a sandbox mounts at a path you choose. Sandboxes support two kinds. **Scratch volumes** belong to a single sandbox and disappear with it. **Registered Volumes** are volumes your organization registers once, and any number of sandboxes can then mount them.

This page is for developers who need a sandbox to write more than its container filesystem holds, or who want several sandboxes to read the same dataset. By the end, you can attach both kinds of volume and manage the registered Volume lifecycle.

## Choose authentication

These examples run on serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Save the configuration for your language beside the scripts you run from this page. Python examples import `AUTH` from `sandbox_auth.py`. TypeScript examples import `client` from `sandbox-client.mts`. These files select authentication without storing your credential. For Python, use an [active virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment). For TypeScript, first install the client with `npm install @coreweave/cwsandbox@1.0.0`.

> [tab] Forge API key
>
> Use your Forge API key with the SDK's `wandb` integration. Replace `[WANDB-API-KEY]` with your API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox[wandb]>=1.14.2'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.WANDB
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization. Replace `[API-ACCESS-TOKEN]` with your token:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox>=1.14.2'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.COREWEAVE_API_KEY
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. In TypeScript, choose the CoreWeave token and set a nonempty `runnerIds` array to select CKS. Creating a Python session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Choose a volume type

| | Scratch volume | Registered Volume |
| - | - | - |
| Declared by | `ScratchVolumeOptions` at sandbox create | `Volume.create()`, then `RegisteredVolumeOptions` at sandbox create |
| Lifetime | The sandbox's | Independent of any sandbox |
| Shared between sandboxes | No | Yes |
| Backing store | Local disk or memory | An existing PersistentVolumeClaim (PVC) in your cluster |
| Survives sandbox deletion | Only through a [file system snapshot](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) | Yes |

Use a scratch volume for working space inside one run. Use a registered Volume for data that outlives a sandbox or that several sandboxes read at once, such as a shared dataset or model weights.

## Scratch volumes

A scratch volume is created with the sandbox and destroyed with it. Declare one with `ScratchVolumeOptions` in the `volumes` list.

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox, ScratchVolumeOptions
>
> with Sandbox.run(
>     container_image="ubuntu:22.04",
>     volumes=[ScratchVolumeOptions(name="workspace", mount_path="/workspace", size="10Gi")],
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as sandbox:
>     sandbox.exec(["sh", "-c", "echo hello > /workspace/data.txt"]).result()
> ```

> [tab] TypeScript
>
> The TypeScript example uses the client from your selected credential configuration.
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> await client.withSandbox(
>   (sandbox) => sandbox.commands.run(["sh", "-c", "echo hello > /workspace/data.txt"], { check: true }),
>   {
>     containerImage: "ubuntu:22.04",
>     volumes: [{ name: "workspace", mountPath: "/workspace", size: "10Gi" }],
>   },
> );
> ```
>
> TypeScript scratch volumes accept `name`, `mountPath`, `size`, and `restoreFromSnapshotId`. The TypeScript client doesn't support `medium`, `sub_path`, `read_only`, or direct per-container mount configuration. Use the Python client for those options.

`ScratchVolumeOptions` accepts the following fields:

| Field | Description |
| - | - |
| `name` | Volume name within the sandbox. Mounts and snapshots reference this name. Required. |
| `mount_path` | Absolute path to mount on the primary container. Omit it to declare the volume without mounting it. |
| `size` | Volume size, such as `"10Gi"`. Omit it to use the platform default. |
| `medium` | Backing store: `StorageMedium.DISK` (the default) or `StorageMedium.MEMORY`. |
| `sub_path` | Relative path inside the volume to mount instead of its root. |
| `read_only` | Mount the volume read-only. Defaults to `False`. |
| `restore_from_snapshot_id` | Restore a [file system snapshot](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) into the volume at create time. |

### Choose a storage medium

`StorageMedium.DISK` backs the volume with local disk. `StorageMedium.MEMORY` backs it with tmpfs, which is faster but counts against the mounting container's memory request and against the policy's memory ceiling.

Because an unbounded RAM-backed volume could exhaust the node, a `MEMORY` volume must declare a `size`. It may do so as an absolute quantity, or as an integer percentage of the sandbox's resolved memory request, such as `"50%"`. The percentage form is valid only for `MEMORY`. A `DISK` volume must use an absolute size.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, ScratchVolumeOptions, StorageMedium

with Sandbox.run(
    container_image="ubuntu:22.04",
    volumes=[
        ScratchVolumeOptions(
            name="fast-cache",
            mount_path="/cache",
            size="50%",
            medium=StorageMedium.MEMORY,
        )
    ],
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    sandbox.exec(["sh", "-c", "df -h /cache"]).result()
```

### Mount a scratch volume on several containers

`mount_path` is a convenience that mounts the volume on the primary container. In a multi-container sandbox, omit `mount_path` and declare the mounts on each container instead, so that more than one container can reach the same volume.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Container, Sandbox, ScratchVolumeOptions, VolumeMount

with Sandbox.run(
    volumes=[ScratchVolumeOptions(name="shared", size="5Gi")],
    containers=[
        Container(
            name="app",
            image="ubuntu:22.04",
            primary=True,
            volume_mounts=[VolumeMount(volume="shared", mount_path="/data")],
            resources={"cpu": "1", "memory": "1Gi"},
        ),
        Container(
            name="sidecar",
            image="ubuntu:22.04",
            volume_mounts=[VolumeMount(volume="shared", mount_path="/data", read_only=True)],
            resources={"cpu": "1", "memory": "1Gi"},
        ),
    ],
    auth=AUTH,
) as sandbox:
    sandbox.exec(["sh", "-c", "echo shared > /data/note.txt"]).result()
```

## Registered Volumes

The PVC-backed registered Volumes in this guide require a CoreWeave API access token and registered Volumes enabled for your organization. The **Forge API key** tab in [Choose authentication](#choose-authentication) applies to scratch volumes. The following examples use a PVC in your CKS cluster and a CoreWeave API access token in `CWSANDBOX_API_KEY`. Complete [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) before registering or mounting a PVC-backed Volume.

A registered Volume points at a PersistentVolumeClaim (PVC) that already exists in one of your clusters. Registering it makes the claim mountable by sandboxes without granting them access to the cluster itself. The Volume is a metadata pointer: CoreWeave never copies the data, and deleting the Volume never touches the claim.

Every attach is a live view of the same claim, so a write from one sandbox is visible to every other sandbox mounting it.

The TypeScript client doesn't expose APIs to register or manage Volumes, or registered-volume mount options on `create()` and `run()`. Use the Python client for those operations.

In TypeScript client version 1.0.0, `runFromTemplate()` can inherit registered Volumes and their mounts from a [sandbox template](https://docs.coreweave.com/products/sandboxes/profiles/templates.md#start-a-sandbox-from-a-template). Omit `containerImage` to preserve the template's containers and mounts. When you set `containerImage`, it replaces the containers and drops their mounts. If registered Volumes remain without mounts, the request is rejected.

### Register a Volume

Registering, updating, or deleting a Volume requires **Sandbox Admin**. **Sandbox User** can list, read, validate, and mount registered Volumes. Sandbox Admin includes Sandbox User permissions. See [Sandbox roles](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox).

`Volume.create()` returns immediately with the Volume in the `VALIDATING` state, then the control plane checks that the claim exists and is usable. Poll with `wait_until_ready()` before you mount it.

```python theme={"system"}
from cwsandbox import AuthStrategy, PvcVolumeSource, Volume

volume = Volume.create(
    "team-data",
    auth=AuthStrategy.COREWEAVE_API_KEY,
    pvc=PvcVolumeSource(
        runner_id="[RUNNER-ID]",
        namespace="[NAMESPACE]",
        claim_name="[PVC-NAME]",
    ),
    description="Shared training data",
).result()

volume.wait_until_ready(timeout=120).result()
print(volume.state, volume.capacity, volume.access_modes)
```

You choose the volume ID yourself. It must be unique within your organization, and it is immutable after creation.

> [!NOTE]
>
> The source and the `read_only` flag are also immutable after creation. Only `description` can change later.

`PvcVolumeSource` takes these fields:

| Field | Description |
| - | - |
| `runner_id` | The runner whose cluster holds the claim. This also pins where sandboxes mounting the Volume are scheduled. Required. |
| `namespace` | Kubernetes namespace of the claim. Required. |
| `claim_name` | Name of the PersistentVolumeClaim. Required. |
| `sub_path` | Optional path inside the claim to treat as the Volume's root. |

Set `read_only=True` on `Volume.create()` to make read-only a property of the Volume itself. That setting is a floor, not a default: a mount can be read-only on a writable Volume, but no mount can write to a read-only Volume.

### Mount a registered Volume

Mount the Volume by ID with `RegisteredVolumeOptions`. The Volume must be `READY` at start, or the sandbox fails with `CWSANDBOX_VOLUME_NOT_READY`.

```python theme={"system"}
from cwsandbox import AuthStrategy, RegisteredVolumeOptions, Sandbox

with Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    placement_mode="cks",
    container_image="ubuntu:22.04",
    volumes=[
        RegisteredVolumeOptions(
            name="data",
            volume_id="team-data",
            mount_path="/data",
            read_only=True,
        )
    ],
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    listing = sandbox.exec(["ls", "/data"]).result()
    print(listing.stdout)
    print(sandbox.attached_volume_ids)
```

`RegisteredVolumeOptions` requires `name`, `volume_id`, and an absolute `mount_path` other than `/`. It also accepts `sub_path`, which combines with any `sub_path` set at registration, and `read_only`.

A sandbox echoes the Volumes it mounted in `attached_volume_ids`.

### Locality and placement

A Volume's `locality` reports whether it constrains placement:

* `cluster_local`: the Volume lives in one cluster, so sandboxes mounting it are scheduled onto that cluster's runner. PVC-backed Volumes are cluster-local.
* `global`: the Volume is reachable from any cluster and does not constrain placement.

Mounting two cluster-local Volumes from different clusters in one sandbox is unsatisfiable, and the start fails with `CWSANDBOX_VOLUME_PLACEMENT_CONFLICT`.

### Manage registered Volumes

Use the following operations to list, inspect, update, and deregister the Volumes in your organization.

```python theme={"system"}
from cwsandbox import AuthStrategy, Volume, VolumeState

# List the organization's Volumes, optionally filtered.
volumes = Volume.list(auth=AuthStrategy.COREWEAVE_API_KEY, states=[VolumeState.READY]).result()

# Fetch one Volume.
volume = Volume.get("team-data", auth=AuthStrategy.COREWEAVE_API_KEY).result()
print(volume.state, volume.attached_sandbox_count)

# Update the description. It is the only mutable field.
volume.update(description="Shared training data, 2026 refresh").result()

# Re-check the backing claim on demand.
volume.validate().result()

# Deregister the Volume. The backing PVC is untouched.
volume.delete(allow_missing=True).result()
```

`Volume.list()` paginates automatically and accepts `states` and `runner_ids` filters. `delete()` accepts `allow_missing=True`, which makes deleting an already-deleted Volume succeed instead of raising.

Deleting a Volume that non-terminal sandboxes still mount fails with `CWSANDBOX_VOLUME_IN_USE`, which the Python client raises as `VolumeInUseError`. Stop the attached sandboxes first.

### Volume states

A registered Volume moves through the following states over its lifecycle:

| State | Meaning |
| - | - |
| `VALIDATING` | The Volume was accepted and the control plane is checking the backing claim. |
| `READY` | Validation succeeded. The Volume can be mounted. |
| `ERROR` | Validation failed. Read `state_reason` for the cause. |
| `DELETING` | The Volume is being deregistered and can no longer be mounted. |

`wait_until_ready()` polls until `READY`. It raises `VolumeError` if the Volume reaches `ERROR` or `DELETING`, and `VolumeWaitTimeoutError` if the timeout elapses first.

## Failure reasons

Use this table to interpret the failure reasons that sandbox and Volume operations can return.

| Reason | What it means | What to do |
| - | - | - |
| `CWSANDBOX_VOLUME_NOT_FOUND` | No Volume with that ID exists in your organization. | Check the ID and the organization. |
| `CWSANDBOX_VOLUME_NOT_READY` | A sandbox start referenced a Volume that is not `READY`. | Poll until the Volume is `READY`, then retry the start. |
| `CWSANDBOX_VOLUME_IN_USE` | A delete was blocked because sandboxes are still attached. | Stop the attached sandboxes, then delete the Volume. |
| `CWSANDBOX_VOLUME_BACKEND_NOT_FOUND` | The backing claim is missing or no longer readable. | Confirm the claim still exists in the namespace, then call `validate()`. |
| `CWSANDBOX_VOLUME_PLACEMENT_CONFLICT` | The attached Volumes pin incompatible runners. | Mount Volumes that live in the same cluster. |
| `CWSANDBOX_VOLUME_QUOTA_EXCEEDED` | The organization hit its Volume limit. | Delete unused Volumes, or request a quota increase. |

## Related resources

For more on related sandbox features, see the following resources:

* [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md): persist and restore a sandbox's filesystem.
* [Grant sandboxes access to AI Object Storage](https://docs.coreweave.com/products/sandboxes/operations/object-storage-access.md): read and write buckets from inside a sandbox.
* [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md): the rest of the sandbox create options
* [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md): create the PersistentVolumeClaims that registered Volumes point at.
