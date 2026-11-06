# File system snapshots

Source: https://docs.coreweave.com/products/sandboxes/file-system-snapshots

# File system snapshots

> Snapshot a sandbox's working directory to object storage, then restore or fork it into new sandboxes.

> [!NOTE]
>
> The TypeScript client supports snapshot mounts, restores, mid-life snapshots, and snapshot management, but not [snapshot-on-stop](#snapshot-on-stop).

File System Snapshots (FSS) let a sandbox write to a local working directory, capture that directory into object storage as an immutable snapshot, and later restore it into new sandboxes. Use FSS to suspend and resume a sandbox's filesystem across runs, or to fork one snapshot into several sandboxes that then diverge independently.

## Choose authentication

These examples run on serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Save the configuration for your language beside the scripts you run from this page. Python examples import `AUTH` from `sandbox_auth.py`. TypeScript examples import `client` from `sandbox-client.mts`. These files select authentication without storing your credential. For Python, use an [active virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment). For TypeScript, first install the client with `npm install @coreweave/cwsandbox@1.0.0`.

> [tab] Forge API key
>
> Use your Forge API key with the SDK's `wandb` integration. Replace `[WANDB-API-KEY]` with your API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> sandbox_headers=(-H "x-wandb-api-key: $WANDB_API_KEY")
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
> sandbox_headers=(-H "Authorization: Bearer $CWSANDBOX_API_KEY")
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

For the HTTP API examples, run the Bash commands from your credential tab in the same shell as the requests. The `sandbox_headers` array supplies the selected authentication header. The HTTP creation examples use serverless placement.

## How it works

A sandbox with FSS mounts a writable scratch filesystem at a path you choose. The runner backs this mount with an `EmptyDir`, not a direct object storage mount. Snapshot and restore operations copy a tarball between that local filesystem and an organization-scoped object storage bucket.

Each snapshot is a `FileSystemSnapshot` resource identified by a server-assigned `fileSystemSnapshotId`. Snapshots have three defining properties:

* **Immutable**: creating a snapshot writes one archive. Restoring a snapshot never changes the source snapshot, so a later restore always sees the original bytes.
* **Organization-scoped**: you can restore only snapshots created in your own organization. A teammate with sandbox access in the same organization can restore your snapshot using their own credentials. A snapshot ID from another organization is treated as not found.
* **Independent lifecycle**: snapshots are managed separately from sandboxes. Deleting a sandbox does not delete its snapshots, and deleting a snapshot does not affect sandboxes already running from it.

By default, CoreWeave provisions and manages the object storage bucket that holds your snapshots. To store snapshots in a bucket you own and control instead, see [Bring your own bucket](https://docs.coreweave.com/products/sandboxes/file-system-snapshots/bring-your-own-bucket.md) for the CoreWeave account and bucket prerequisites.

## Start a sandbox with a snapshot mount

A sandbox can start from one of two filesystem sources: a fresh, empty scratch filesystem, or a restore of an existing snapshot.

### Fresh scratch

A fresh scratch filesystem starts empty and can be snapshotted later. Use it for workflows that need writable local state during a run.

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox, FileSystemSnapshotOptions
>
> with Sandbox.run(
>     container_image="ubuntu:22.04",
>     file_system_snapshot=FileSystemSnapshotOptions(mount_path="/work", size="10Gi"),
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as sandbox:
>     sandbox.exec(["sh", "-c", "echo hello > /work/data.txt"]).result()
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> await client.withSandbox(
>   (sandbox) => sandbox.commands.run(["sh", "-c", "echo hello > /work/data.txt"], { check: true }),
>   {
>     containerImage: "ubuntu:22.04",
>     fileSystemSnapshot: { mountPath: "/work", size: "10Gi" },
>   },
> );
> ```

> [tab] HTTP API
>
> Set `fileSystem.mountPath` and `fileSystem.size`. Leave `fileSystemSnapshot` unset to start empty.
>
> ```bash theme={"system"}
> curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes \
>   "${sandbox_headers[@]}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "containerImage": "ubuntu:22.04",
>     "command": "sleep",
>     "args": ["3600"],
>     "fileSystem": {
>       "mountPath": "/work",
>       "size": "10Gi"
>     }
>   }'
> ```

### Restore from a snapshot

A restore starts the filesystem from an existing snapshot. Set the snapshot ID on the mount's snapshot source.

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox, FileSystemSnapshotOptions
>
> with Sandbox.run(
>     container_image="ubuntu:22.04",
>     file_system_snapshot=FileSystemSnapshotOptions(
>         mount_path="/work",
>         file_system_snapshot_id="fss_...",
>     ),
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as sandbox:
>     contents = sandbox.exec(["cat", "/work/data.txt"]).result()
>     print(contents.stdout)
> ```

> [tab] TypeScript
>
> Set the snapshot ID in `restoreFromSnapshotId`:
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const contents = await client.withSandbox(
>   (sandbox) => sandbox.commands.run(["cat", "/work/data.txt"]),
>   {
>     containerImage: "ubuntu:22.04",
>     fileSystemSnapshot: { mountPath: "/work", restoreFromSnapshotId: "fss_..." },
>   },
> );
> console.log(contents.stdout);
> ```

> [tab] HTTP API
>
> ```bash theme={"system"}
> curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes \
>   "${sandbox_headers[@]}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "containerImage": "ubuntu:22.04",
>     "command": "sleep",
>     "args": ["3600"],
>     "fileSystem": {
>       "mountPath": "/work",
>       "size": "10Gi",
>       "fileSystemSnapshot": {
>         "fileSystemSnapshotId": "fss_..."
>       }
>     }
>   }'
> ```

A snapshot must be `READY` before you restore it. Restoring a snapshot that is still `CREATING` fails. See [Snapshot status and failures](#snapshot-status-and-failures).

### Plan for restore time

A snapshot restore copies and extracts its archive before the sandbox can run your application. Large model snapshots can take several minutes to restore. Startup time depends on the following factors:

* Archive size
* File count
* Available CPU
* Local storage
* Network throughput
* Image startup work

The requested mount capacity alone doesn't predict restore time.

When choosing a startup deadline, measure cold launches with your image, snapshot, and resource requests. `CREATING` alone doesn't distinguish waiting for scheduling from restoring files. Before deleting a slow launch, check the sandbox's `status_reason` and retain its ID for support. A fixed deadline can bound your wait, but elapsed time alone doesn't establish that a restore has failed.

## Take a snapshot

You can capture a snapshot in two ways: on stop, when a sandbox shuts down, and mid-life, from a running sandbox.

### Snapshot on stop

To preserve a sandbox's filesystem when it shuts down, stop the sandbox with snapshot-on-stop enabled. This is the pattern for suspend and resume: stop with a snapshot, then later start a new sandbox that restores it.

> [tab] Python
>
> ```python theme={"system"}
> sandbox.stop(snapshot_on_stop=True).result()
> print(sandbox.file_system_snapshot_id)
> ```

> [tab] TypeScript
>
> The TypeScript client doesn't support snapshot-on-stop: `stop()` has no snapshot option. Take a [mid-life snapshot](#mid-life-snapshot) before you stop the sandbox instead. This capture isn't atomic. If you need consistent state, pause application writes during capture or use an application checkpoint. Writes made after `snapshot()` returns aren't captured.
>
> ```typescript theme={"system"}
> const { snapshotId } = await sandbox.snapshot();
> await sandbox.stop();
> console.log(snapshotId);
> ```

> [tab] HTTP API
>
> `StopSandbox` returns a `fileSystemSnapshotId` when the snapshot request is accepted. With `waitForReady` set to `true`, the call waits until the snapshot reaches `READY` or `FAILED`, bounded by `maxTimeoutSeconds`. Without it, the call can return while the snapshot is still `CREATING`. Replace `[SANDBOX-ID]` with the ID of the sandbox to stop.
>
> ```bash theme={"system"}
> curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes/[SANDBOX-ID]/stop \
>   "${sandbox_headers[@]}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "sandboxId": "[SANDBOX-ID]",
>     "fileSystemSnapshotOnStop": true,
>     "waitForReady": true,
>     "idempotencyKey": "stop-[SANDBOX-ID]-snapshot-1",
>     "maxTimeoutSeconds": 600
>   }'
> ```

### Mid-life snapshot

A mid-life snapshot captures a running sandbox without stopping it. The sandbox keeps running during and after capture. Capture scans the live filesystem and isn't atomic, so writes made during capture might not be captured consistently. If you need consistent state, pause application writes during capture or create an application checkpoint before capture.

> [tab] Python
>
> `snapshot()` waits until the snapshot is `READY` by default and returns the snapshot ID.
>
> ```python theme={"system"}
> snapshot_id = sandbox.snapshot().result()
> print(f"Created snapshot {snapshot_id}")
> ```

> [tab] TypeScript
>
> `snapshot()` waits until the snapshot's `state` is `"ready"` and returns the snapshot record, not only the ID.
>
> ```typescript theme={"system"}
> const snapshot = await sandbox.snapshot();
> console.log(`Created snapshot ${snapshot.snapshotId}`);
> ```

> [tab] HTTP API
>
> `CreateFileSystemSnapshot` accepts the same `idempotencyKey`, `waitForReady`, and `maxTimeoutSeconds` controls as snapshot-on-stop. Unlike `StopSandbox`, `waitForReady` defaults to `true`. Replace `[SANDBOX-ID]` with the ID of the running sandbox to snapshot.
>
> ```bash theme={"system"}
> curl -X POST https://api.cwsandbox.com/v1beta2/sandboxes/[SANDBOX-ID]/file-system-snapshots \
>   "${sandbox_headers[@]}" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "sandboxId": "[SANDBOX-ID]",
>     "waitForReady": true,
>     "maxTimeoutSeconds": 600
>   }'
> ```
>
> With `waitForReady` set to `false`, a successful response means the snapshot row was created and the snapshot command was dispatched. The archive may still be `CREATING`, and it can later become `FAILED`. Poll the snapshot before you restore it.

## Fork a snapshot

The same snapshot can be restored into more than one sandbox. Because each snapshot is immutable, the restored sandboxes start from identical bytes and then diverge as they write.

1. Create a `READY` snapshot, with either snapshot-on-stop or a mid-life snapshot.
2. Start sandbox A with `fileSystemSnapshotId` set to that snapshot.
3. Start sandbox B with the same `fileSystemSnapshotId`.
4. Writes in sandbox A and sandbox B diverge independently. The source snapshot is unchanged, so a later restore from the same ID still sees the original snapshot, not the writes from either fork.

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox, FileSystemSnapshotOptions
>
> # Restore the same snapshot into two independent sandboxes.
> with Sandbox.run(
>     file_system_snapshot=FileSystemSnapshotOptions(mount_path="/work", file_system_snapshot_id=snapshot_id),
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as fork_a, Sandbox.run(
>     file_system_snapshot=FileSystemSnapshotOptions(mount_path="/work", file_system_snapshot_id=snapshot_id),
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> ) as fork_b:
>     fork_a.exec(["sh", "-c", "echo a >> /work/data.txt"]).result()
>     fork_b.exec(["sh", "-c", "echo b >> /work/data.txt"]).result()
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
>
> // Restore the same snapshot into two independent sandboxes.
> await Promise.all(
>   ["a", "b"].map((name) =>
>     client.withSandbox(
>       (fork) => fork.commands.run(["sh", "-c", `echo ${name} >> /work/data.txt`], { check: true }),
>       { fileSystemSnapshot: { mountPath: "/work", restoreFromSnapshotId: snapshotId } },
>     ),
>   ),
> );
> ```

## Manage snapshots

List, fetch, and delete snapshots independently of the sandboxes that created them.

> [tab] Python
>
> ```python theme={"system"}
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> # List all snapshots in your organization.
> snapshots = Sandbox.list_snapshots(auth=AUTH).result()
>
> # Fetch one snapshot's details.
> snapshot = Sandbox.get_snapshot(snapshot_id, auth=AUTH).result()
> print(f"{snapshot.file_system_snapshot_id}: {snapshot.size_bytes} bytes")
>
> # Delete a snapshot. missing_ok makes the call idempotent.
> Sandbox.delete_snapshot(snapshot_id, missing_ok=True, auth=AUTH).result()
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
>
> // List all snapshots in your organization.
> const snapshots = await client.listSnapshots();
>
> // Fetch one snapshot's details.
> const snapshot = await client.getSnapshot(snapshotId);
> if (snapshot.sizeBytes !== undefined) {
>   console.log(`${snapshot.snapshotId}: ${snapshot.sizeBytes} bytes`);
> } else {
>   console.log(snapshot.snapshotId);
> }
>
> // Delete a snapshot. missingOk makes the call idempotent.
> await client.deleteSnapshot(snapshotId, { missingOk: true });
> ```

> [tab] HTTP API
>
> Replace `[SNAPSHOT-ID]` with the ID of the snapshot to fetch or delete.
>
> ```bash theme={"system"}
> # List org-scoped snapshots.
> curl https://api.cwsandbox.com/v1beta2/file-system-snapshots \
>   "${sandbox_headers[@]}"
>
> # Get one snapshot.
> curl https://api.cwsandbox.com/v1beta2/file-system-snapshots/[SNAPSHOT-ID] \
>   "${sandbox_headers[@]}"
>
> # Delete one snapshot.
> curl -X DELETE https://api.cwsandbox.com/v1beta2/file-system-snapshots/[SNAPSHOT-ID] \
>   "${sandbox_headers[@]}"
> ```

`list_snapshots()`, `get_snapshot()`, and `delete_snapshot()` also accept an `AuthHeaders` object through `auth`.

## Snapshot status and failures

Snapshots are created asynchronously. A snapshot request can succeed and return a `fileSystemSnapshotId` while the archive is still being written, and the snapshot can fail afterward. This happens most often when `waitForReady` is `false`, or when a client timeout occurs while the runner is still archiving.

To check progress through the HTTP API, fetch the snapshot and read these fields:

* `status`: the lifecycle state. The terminal values are `FILE_SYSTEM_SNAPSHOT_STATUS_READY` and `FILE_SYSTEM_SNAPSHOT_STATUS_FAILED`.
* `statusReason`: populated when `status` is `FILE_SYSTEM_SNAPSHOT_STATUS_FAILED`, explaining why.

In TypeScript, read `state` and `stateReason` from the snapshot record. The corresponding state values are `"ready"` and `"failed"`.

If readiness isn't already confirmed, poll `GetFileSystemSnapshot` until the snapshot reaches `READY` or `FAILED`. Restore only after it reaches `READY`.

The Python client's `snapshot()` waits for readiness by default when you wait for its result. `get_snapshot().result()` fetches the current snapshot record without waiting for readiness. If readiness is still unconfirmed, repeat that call until the record's `status` reaches `READY` or `FAILED`.

The TypeScript client's `snapshot()` waits until `state` is `"ready"` and throws if the snapshot fails.

### Recover from a failed snapshot request

While recovering from a mid-life snapshot failure, keep the source sandbox running. A snapshot remote procedure call (RPC) failure doesn't itself delete the sandbox or its mount. If you leave a Python sandbox context manager or run teardown code, the sandbox can stop. Data that hasn't reached a ready snapshot can be discarded. Handle the failure before that cleanup runs.

First-use bucket provisioning can return `CWSANDBOX_FSS_BUCKET_PROVISIONING`. The Python client retries transient snapshot RPC failures for a bounded budget. If provisioning outlasts that budget, retry with backoff while retaining the source sandbox. When retrying the same request after an ambiguous transport failure, reuse an explicit `request_id` so the server can deduplicate it. If a snapshot ID is available after a timeout, check that snapshot before requesting another archive. A snapshot that has reached `FAILED` requires a new request to capture the data again.

For Python client 1.19.6, transient snapshot failures can raise `SandboxUnavailableError`, while other snapshot failures raise `SandboxSnapshotError`. When preserving a build, handle both and use the error's `reason` to decide whether retrying is appropriate. Don't retry quota or configuration failures without addressing their cause.

The following table lists the common failure reasons and what to do about each.

| Reason | What it means | What to do |
| - | - | - |
| `CWSANDBOX_FSS_BUCKET_PROVISIONING` | The default snapshot bucket is still being provisioned. | Retry shortly. If the error persists, contact support. |
| `CWSANDBOX_FSS_AUTH_FAILED` | Credential exchange or bucket authorization failed. | Retry after the bucket or WIF policy is fixed. Contact support if this is a CoreWeave-managed bucket. |
| `CWSANDBOX_FSS_TRANSPORT_FAILED` | The runner could not reach object storage, or the archive transfer failed. | Retry. If it repeats, contact support with the snapshot ID. |
| `CWSANDBOX_FSS_BACKEND_THROTTLED` | Object storage returned sustained throttling or backend errors. | Retry later. |
| `CWSANDBOX_FSS_CREATE_TIMED_OUT` | The snapshot did not finish inside the configured timeout. | Retry with a higher `maxTimeoutSeconds`, or reduce the data size. |
| `CWSANDBOX_FSS_CANCELED` | The snapshot was canceled, usually by force-deleting the sandbox during in-flight work. | Retry the snapshot if you still need the data. |
| `CWSANDBOX_FSS_QUOTA_EXCEEDED` | The organization hit its snapshot count or storage cap. | Delete unused snapshots, or request a quota increase. |
| `CWSANDBOX_FSS_NOT_READY` | A restore referenced a snapshot that is not `READY`. | Poll until the snapshot is `READY`, or choose a different snapshot. |
| `CWSANDBOX_FSS_NOT_FOUND` | The snapshot does not exist in your organization. | Check the snapshot ID and the organization. |
| `CWSANDBOX_FSS_SIZE_EXCEEDED` | The requested filesystem size exceeds the supported scratch size. | Request a smaller filesystem, or contact support about limits. |

If a runner finishes uploading the archive but cannot record the result, the snapshot row can become `FAILED` even though an object exists in the bucket. Retry the snapshot in this case.

For asynchronous failures, the platform also emits a `sandbox.file_system_snapshot.async_fail` event, so downstream notification systems can react to snapshots that fail after the original call returned.

## Limitations

FSS version 1 provides snapshot-backed local scratch storage. It is not a shared filesystem and does not provide live, multi-writer mounts. Sandboxes do not read or write each other's filesystems while running. They share state only by snapshotting and restoring.

## SDK example

For a complete, runnable Python example that starts a sandbox, takes a mid-life snapshot, forks it, captures a snapshot on stop, and manages snapshots, see [`file_system_snapshots.py`](https://github.com/coreweave/cwsandbox-client/blob/main/examples/file_system_snapshots.py) in the `cwsandbox-client` repository. For TypeScript, [`file-system-snapshots.ts`](https://github.com/coreweave/cwsandbox-js/blob/main/examples/sdk/file-system-snapshots.ts) in the `cwsandbox-js` repository takes a mid-life snapshot, restores it, and manages snapshots.

## Related resources

* [Bring your own bucket for file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots/bring-your-own-bucket.md): store snapshots in a bucket you own.

* [Volumes](https://docs.coreweave.com/products/sandboxes/volumes.md): scratch volumes and registered Volumes that several sandboxes share.

* [Sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md): how `stop()` and the sandbox states work.

* [Python client](https://docs.coreweave.com/products/sandboxes/client.md): install the SDK and explore the API.
