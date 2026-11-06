# Manage Distributed File Storage volumes

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/manage-volumes

# Manage Distributed File Storage volumes

> How to manage, optimize, and maintain distributed file storage volumes on CKS

This page describes how to create, configure, and manage Distributed File Storage volumes on CKS so you can provision persistent storage for your workloads, adjust capacity over time, and clean up resources you no longer need. It's intended for CKS users and cluster administrators who manage storage for Pods and namespaces.

On CKS, you create Storage Volumes as [Persistent Volumes (PVs)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) by deploying [Persistent Volume Claims (PVCs)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#introduction).

To specify the type, size, and placement of Storage Volumes, configure the manifest for the Persistent Volume Claim.

## Persistent Volume Claims

Persistent Volume Claims are requests for Persistent Volume resources, which serve as storage volumes for workloads that require persistent storage.

To troubleshoot a PVC, see [Why is my PVC stuck in Pending?](https://docs.coreweave.com/support/storage/articles/why-is-my-pvc-stuck-in-pending) and [Why won't my PVC delete?](https://docs.coreweave.com/support/storage/articles/why-wont-my-pvc-delete).

### Volume attachments

When you create a Persistent Volume, Kubernetes binds the PV to a `StorageClass` defined in the PV's manifest. The `StorageClass` tells Kubernetes how to set up the storage volume, such as which [CSI plugin](https://docs.coreweave.com/products/cks/reference/cluster-components.md#storage) to use and any options that plugin might need. After Kubernetes creates the PV for the given `StorageClass`, it schedules a Pod on a Node. Kubernetes then takes a hash of the Node name, PV name, and CSI plugin name to create a Volume Attachment with its name as this hash.

> [!NOTE]
>
> `VolumeAttachment` objects don't belong to a namespace and can be accessed in the Cloud Console.

## Create PVCs

You can create PVCs using the Cloud Console or by deploying a PVC manifest using `kubectl`. The following sections describe both approaches.

### Create a PVC using the API

Use this method when you want to automate provisioning or check PVC definitions into source control. To create a Persistent Volume Claim, annotate the following YAML manifest to your specifications:

```yaml theme={"system"}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: new-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: shared-vast
```

Update these fields in the manifest:

| Field name | Field type | Description |
| - | - | - |
| `name` | string | The name of the PVC. |
| `namespace` | string | The namespace for the PVC. |
| `spec.accessModes` | list | Sets the [access mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) for the volume. [Distributed Filesystem Volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md) use `ReadWriteMany`. |
| `resources.requests.storage` | string | Determines the size of the volume, in Gi. |
| `storageClassName` | string | The storage class name is `shared-vast` for CKS. |

Configure the manifest as desired, save it to a `.yaml` file, and apply it with `kubectl`. Replace `[PVC-FILE]` with the path to your manifest file.

```bash theme={"system"}
kubectl apply -f [PVC-FILE]
```

To verify that the PVC is bound to a PV, replace `[PVC-NAME]` with the name you set in the manifest:

```bash theme={"system"}
kubectl get pvc [PVC-NAME]
```

```text title="Example output" theme={"system"}
NAME      STATUS   VOLUME                                 CAPACITY   ACCESS MODES   STORAGECLASS   AGE
new-pvc   Bound    pvc-b657b567-e-6b78-98347-67894349850  512Gi      RWO            shared-vast    1d
```

To get more detailed information about a PVC:

```bash theme={"system"}
kubectl describe pvc [PVC-NAME]
```

### Create a PVC with the Cloud Console

You need access to an active CKS cluster to create a PVC using the Cloud Console. If you don't have any clusters or don't have access to any clusters, you see the following message:

![Message if clusters cannot be loaded](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-no-clusters-error-message.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=64126e3ead795c102fd5839a6a23688f)

If an active cluster is available, choose **Create PVC** to begin.

![Create PVC Cloud Console page](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/create-pvc.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=14ed8641a3ad69840d9187fb55cf1eb2)

Enter details for the PVC, then click **Create**. After the PVC is created, the Console shows basic information about the PVC, including its name, age, size, and status.

![Persistent Volume Claims in Console UI](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-pvc-claims-dash.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=d919bb0d9248214573e8479675f99d8c)

## Manage PVCs

For creation, both API and Console approaches are common. For ongoing management tasks, the Console provides easier visualization and safety checks, so this section focuses on Console methods. The following sections describe permissions, editing, cloning, rebinding, and deletion.

### Work with PVCs

The groups you belong to dictate how you interact with PVC resources. As a non-admin, you can add PVCs through the UI or using the API, but your ability to access and edit them is limited to your permitted actions within your clusters.

Administrators have greater powers over PVC resources. Users with `admin`, `write`, and `read` Cluster RoleBindings can add and remove PVCs from the groups they're in. Also, the default `admin` privileges let them manage those PVCs collectively. They can also use the following Console Actions inside their cluster:

* Edit `RoleBindings`.
* Create and modify RBAC schemes that allow a chosen group or groups access to resources. These can be as general as a resource type, or as specific as a particular PVC.

### Edit volumes

To edit a PVC, click the three-dot menu on the far right of the PVCs listing on the Overview page, then click **Edit**. Enter the desired changes in the pop-up modal.

![Edit PVC modal](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-edit-pvc-screenshot.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=49dc23b130719d0f8210bf7d8d9f97a4)

> [!WARNING]
>
> **Shrinking volumes**
>
> You can't reduce PVCs in size. To use a smaller volume, create a new, smaller PVC and migrate your data manually.

### Clone PVCs

You can clone PVCs if you have write permissions.

Click the **Clone** button from the PVC's three-dot menu, and then enter a new name for the cloned PVC. Click **Confirm** to provision a copy of the PVC in the user's default namespace.

![Clone PVC modal](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-clone-pvc-screenshot.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=8b2f30cffd12975893acccc5d35f26ef)

### Bind a PVC to a new namespace

Rebinding a PVC makes an existing persistent volume's storage available in a different namespace. This is useful when you need to migrate workloads or share storage across namespaces while preserving your data.

CoreWeave provides the [`rebind-pvc.sh`](https://github.com/coreweave/reference-architecture/blob/main/storage/dfs-rebind-pvc/rebind-pvc.sh) utility script to automate this process. The script generates the necessary Kubernetes manifests to bind an existing PVC's underlying storage volume to a new namespace.

For complete instructions, including installation, usage examples, and important teardown procedures, see the [rebind-pvc.sh documentation on GitHub](https://github.com/coreweave/reference-architecture/blob/main/storage/dfs-rebind-pvc/README.md).

> [!CAUTION]
>
> **Important: Proper deletion order**
>
> When deleting rebound PVCs, always delete the child PVCs (in target namespaces) before deleting the original base PVC. CoreWeave's Persistent Volume Management Operator (PVMO) deletes the underlying storage when you delete the base PVC, which can cause child PVCs to have stale volume handles and prevent Pods from shutting down gracefully.
>
> See the [proper teardown procedure](https://github.com/coreweave/reference-architecture/blob/main/storage/dfs-rebind-pvc/README.md#proper-teardown-procedure) for details.

### Delete a storage volume through the Cloud Console

> [!NOTE]
>
> Only users with `admin` permissions can delete Storage Volumes.

From the three-dot menu, select **Delete**.

![Delete PVC menu](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-delete-pvc-screenshot.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=a3eec0ba0684b9a26596625cf38bd232)

When you delete a PVC, any PV linked to it is automatically soft-deleted. Soft-deleted PVs are deleted **permanently** after the soft delete window (24 hours after the original PVC deletion) expires. To delete a PVC, type the name of the desired volume in the confirmation modal, then click **Delete**.

![Confirm deletion modal](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/storage-confirm-delete-pvc-screenshot.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=5902036bdf605fc0bd8bf80e398623a1)

The volume is removed from the PVC overview menu when deletion is complete.

## Performance optimization

After your volumes are in place, the following recommendations can help you get the best performance out of Distributed File Storage for common workloads.

### Avoid `subPath` mounts when possible

CoreWeave recommends mounting Distributed File Storage volumes onto your Pods without using a Kubernetes [`subPath`](https://kubernetes.io/docs/concepts/storage/volumes/#using-subpath). Mounting with `subPath` exposes only a subdirectory of the volume to the Pod, making certain Distributed File Storage features unavailable from inside the mount. The most notable example is the `.vast_trash` directory, which enables asynchronous, non-conflicting bulk deletes. For more information about how `subPath` affects deletion, see [Delete Files with VAST trash](https://docs.coreweave.com/products/storage/distributed-file-storage/delete-files.md#work-with-subpath-mounts).

If you have a use case that requires `subPath` mounts, [contact CoreWeave Support](https://coreweave.freshdesk.com/support/login) for help.

### Git performance

Git performance with Distributed File Storage can sometimes be slower than desired. The following best practices help enhance Git performance on Distributed File Storage.

#### Enable parallel checkout

Enable [parallel checkout](https://git-scm.com/docs/parallel-checkout) by setting a desired number of parallel workers in your Git config (`checkout.workers`). The recommended number for working with Distributed File Storage is `16`.

```bash theme={"system"}
git config --global checkout.workers 16
```

#### Enable untracked cache

Enable Git's [untracked cache](https://git-scm.com/docs/git-update-index.html#_untracked_cache).

```bash theme={"system"}
git config --global core.untrackedCache true
```

### Define record sizes for TAR performance

When you use [TAR (`tar`)](https://www.man7.org/linux/man-pages/man1/tar.1.html) for compression, setting the record size to `1M` may help performance:

```bash theme={"system"}
tar --record-size=1M -cf archive.tar foo
```

> [!NOTE]
>
> Setting the record size can also make `rsync` more efficient. See [the `man` page for `tar`](https://www.man7.org/linux/man-pages/man1/tar.1.html) for more information.
