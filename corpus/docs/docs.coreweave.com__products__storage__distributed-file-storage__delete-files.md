# Delete files with VAST trash

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/delete-files

# Delete files with VAST trash

> Delete files from Distributed File Storage using the VAST trash directory

This guide explains how to delete files from Distributed File Storage by moving them to the VAST trash directory (`.vast_trash`), which is the recommended approach for bulk deletions. It's intended for cluster administrators with `root` (superuser) access to a CKS cluster that has a Distributed File Storage volume mounted.

You can delete files from Distributed File Storage using either the VAST trash directory or the `rm` command. The VAST trash directory supports asynchronous deletion of files and folders in bulk. Serial `rm -rf` on large directories is slow and can block, so moving files marked for removal to the trash folder (`.vast_trash`) is faster.

> [!NOTE]
>
> `.vast_trash` is only accessible from a full volume mount. Pods that use a Kubernetes `subPath` mount can't access `.vast_trash`. For details and migration options, see [Work with `subPath` mounts](#work-with-subpath-mounts).

## Prerequisites

* You have an active CKS cluster with a Distributed File Storage volume mounted.
* You have `root` user access to the cluster.

## Access VAST trash

The VAST trash directory (`.vast_trash`) is located at the root of each volume's mount point. For example, if your volume is mounted at `/mnt/vast`, the VAST trash directory is at `/mnt/vast/.vast_trash`.

`.vast_trash` doesn't appear in directory listings (`ls`). To verify it exists, replace `[VOLUME-MOUNT-PATH]` with the path where your volume is mounted (for example, `/mnt/vast`) and run:

```bash theme={"system"}
cd /[VOLUME-MOUNT-PATH]/.vast_trash
```

If this command succeeds, you have trash access. If you get an error like `No such file or directory`, you likely have a `subPath` mount, which means no `.vast_trash` directory exists. Use the full volume mount instead.

## Move files to VAST trash

Moving files to `.vast_trash` triggers asynchronous deletion by VAST, which avoids the long-running blocking behavior of `rm -rf` on large directories. The `root` user can delete files by moving them to the VAST trash directory. Replace `[PATH-TO-REMOVE]` with the path, without a leading slash, to the file or directory on the DFS volume mounted at `/mnt/vast`. The source and `.vast_trash` must be on the same volume:

```bash theme={"system"}
sudo mv /[PATH-TO-REMOVE] /mnt/vast/.vast_trash
```

If you need to update the ownership of the trash directory, [contact CoreWeave Support](https://coreweave.freshdesk.com/support/login).

An error like `mv: cannot overwrite non-directory '.vast_trash/<name>' with directory '<name>'` can occur if the same directory name was previously deleted and VAST is still finalizing metadata cleanup. Try a different directory name or wait a few seconds before retrying.

> [!WARNING]
>
> Once moved to `.vast_trash`, files are permanently deleted and can't be recovered.

Listing the contents of the trash directory returns an empty list, which confirms that the move succeeded and the contents are no longer addressable:

```bash theme={"system"}
ls -la /mnt/vast/.vast_trash
```

```text title="Example output" theme={"system"}
total 0
```

## Work with `subPath` mounts

`.vast_trash` isn't available when you use Kubernetes `subPath` mounts, because `subPath` only exposes a subdirectory of the volume, not the root where `.vast_trash` exists. If your workload relies on `subPath`, change how the volume is mounted before you use trash-based deletion.

If you need `.vast_trash` access but currently use a `subPath` mount, you can:

* Mount the full volume at a different location and then update your workloads to use the new mount point.
* Use symlinks to organize subdirectories within a full volume mount instead of `subPath`.

To check whether you use a `subPath` mount, replace `[NAMESPACE]` and `[POD-NAME]` with your namespace and pod name, then run:

```bash theme={"system"}
kubectl describe -n [NAMESPACE] pod [POD-NAME] | grep -A6 "Mounts:"
```

In the `Mounts` section, look for entries with `path="..."`. This indicates a `subPath` mount.

## Diagnose mixed `subPath` and full volume mounts

You might have a configuration where some directories are full volume mounts and others are `subPath` mounts. This can cause confusion when you use `.vast_trash`, because the trash directory appears to work in some locations but not others within the same pod.

In this example, you have a full volume mount at `/mnt/datasets` and a `subPath` mount at `/mnt/experiments`:

```text theme={"system"}
/mnt/datasets          # Full volume mount
├── .vast_trash/       # Trash accessible here
├── training-data/
└── validation/

/mnt/experiments       # subPath mount (pointing to experiments/ in another volume)
├── run-001/           # No .vast_trash visible
├── run-002/
└── checkpoints/
```

To verify your mount configuration, run the following command:

```bash theme={"system"}
kubectl describe -n [NAMESPACE] pod [POD-NAME] | grep -A6 "Mounts:"
```

The output looks like this:

```text title="Example output" theme={"system"}
    Mounts:
      /mnt/datasets from my-volume (rw)
      /mnt/experiments from my-volume (rw,path="experiments")
```

In the `Mounts` section, look for entries with `path="..."`. This indicates a `subPath` mount. In this example, `/mnt/experiments` is a `subPath` mount, so it doesn't have its own VAST trash directory.

When you delete files in this setup, the behavior depends on the mount type:

* Deleting from the full volume mount at `/mnt/datasets` works:

  ```bash theme={"system"}
  sudo mv /mnt/datasets/training-data/old-dataset /mnt/datasets/.vast_trash/
  ```

* Deleting from the `subPath` mount at `/mnt/experiments` fails:

  ```bash theme={"system"}
  sudo mv /mnt/experiments/run-001 /mnt/experiments/.vast_trash/
  # Error: No such file or directory
  ```

To delete files from a `subPath`, like the `experiments` directory, you have two options:

* Use standard deletion: `rm -rf /mnt/experiments/run-001`.
* Migrate to a full volume mount to gain trash access. See [Work with `subPath` mounts](#work-with-subpath-mounts).
