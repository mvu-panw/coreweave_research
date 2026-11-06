# Recover a deleted PVC

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/recover-deleted-pvc

# Recover a deleted PVC

> Rebind an existing Persistent Volume to a new PVC to recover data after accidental deletion

When a Distributed File Storage PVC is deleted, the underlying data is not immediately removed. The [Persistent Volume Management Operator (PVMO)](https://docs.coreweave.com/products/storage/distributed-file-storage/about-pvmo.md) enforces a 24-hour soft-delete window during which the PV and its data remain accessible. Within that window, you can recover the data by creating a new PVC that binds to the existing PV. When the new PVC binds to the PV, PVMO automatically removes the soft-delete marker and stops the deletion countdown.

## Prerequisites

* `kubectl` configured with access to the cluster where the PVC was deleted.
* Admin permissions on the cluster (`admin` Cluster RoleBinding).
* You know the name and namespace of the deleted PVC.
* The 24-hour soft-delete window has not yet elapsed since the PVC was deleted.

## Step 1: Find the original PV

Even after a PVC is deleted, its PV remains in the cluster until PVMO removes it. List all PVs to locate the one associated with the deleted PVC:

```bash theme={"system"}
kubectl get pv
```

Look for a PV in `Released` status. If you know the original PVC name, you can filter by the claim reference in the `CLAIM` column (for example, `[NAMESPACE]/[PVC-NAME]`).

Once you identify the PV, record its name. Replace `[PV-NAME]` with the PV name you found:

```bash theme={"system"}
kubectl get pv [PV-NAME] -o yaml
```

From the output, note the following fields. You will need all of them to create the replacement PV:

| Field | Example value |
| - | - |
| `spec.capacity.storage` | `4000Ti` |
| `spec.accessModes` | `[ReadWriteMany]` |
| `spec.storageClassName` | `shared-vast` |
| `spec.csi.driver` | `csi.vast.io` |
| `spec.csi.volumeHandle` | `pvc-a07727ce-9a7f-4f14-892d-0ea8f69712e9@prod-02` |

The `spec.csi.volumeHandle` value is the unique identifier for the volume on the VAST storage backend. You must use the original value, not the new PV name. Using the new PV name instead will cause the CSI driver to search for a volume that does not exist.

## Step 2: Create a new Persistent Volume

Create a new PV manifest that points to the same VAST volume handle. Replace the placeholder values with the values you recorded in step 1.

Replace `[NEW-PV-NAME]` with a unique name for the new PV (for example, `[ORIGINAL-PV-NAME]-recovered`):

```yaml title="new-pv.yaml" theme={"system"}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: [NEW-PV-NAME]
spec:
  capacity:
    storage: [ORIGINAL-CAPACITY]
  accessModes:
    - [ORIGINAL-ACCESS-MODE]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: [ORIGINAL-STORAGE-CLASS-NAME]
  volumeMode: Filesystem
  csi:
    driver: [ORIGINAL-CSI-DRIVER]
    volumeHandle: [ORIGINAL-VOLUME-HANDLE]
    readOnly: false
```

> [!NOTE]
>
> Set `persistentVolumeReclaimPolicy: Retain` on the new PV. This ensures that if the new PVC is deleted before PVMO's countdown on the original PV expires, the new PV itself is not immediately reclaimed.

Apply the manifest. Replace `[PV-MANIFEST-FILE]` with the path to your manifest:

```bash theme={"system"}
kubectl apply -f [PV-MANIFEST-FILE]
```

## Step 3: Create a new Persistent Volume Claim

Create a PVC manifest in the target namespace that binds explicitly to the new PV. Replace `[NEW-PVC-NAME]` and `[TARGET-NAMESPACE]` with your values:

```yaml title="new-pvc.yaml" theme={"system"}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: [NEW-PVC-NAME]
  namespace: [TARGET-NAMESPACE]
spec:
  accessModes:
    - [ORIGINAL-ACCESS-MODE]
  resources:
    requests:
      storage: [ORIGINAL-CAPACITY]
  storageClassName: [ORIGINAL-STORAGE-CLASS-NAME]
  volumeName: [NEW-PV-NAME]
```

The `volumeName` field explicitly binds this PVC to the PV you created in step 2. Without it, Kubernetes may bind to a different available PV.

Apply the manifest. Replace `[PVC-MANIFEST-FILE]` with the path to your manifest:

```bash theme={"system"}
kubectl apply -f [PVC-MANIFEST-FILE]
```

## Step 4: Verify the binding

Confirm that both the new PV and new PVC are in `Bound` status:

```bash theme={"system"}
kubectl get pv [NEW-PV-NAME]
kubectl get pvc [NEW-PVC-NAME] -n [TARGET-NAMESPACE]
```

```text title="Example output" theme={"system"}
NAME                   CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
my-volume-recovered    4000Ti     RWX            Retain           Bound    my-namespace/my-volume-recovered

NAME                   STATUS   VOLUME                  CAPACITY   ACCESS MODES   STORAGECLASS
my-volume-recovered    Bound    my-volume-recovered     4000Ti     RWX            shared-vast
```

Once both show `Bound`, you can mount the new PVC in a pod as you would any other PVC. The original VAST data is accessible through the new PVC.

## Step 5: Protect the PV from future deletion

After rebinding, add the protect label to the original PV to prevent PVMO from ever automatically deleting it. Replace `[PV-NAME]` with the name of the original PV from step 1:

```bash theme={"system"}
kubectl label pv [PV-NAME] pv.storage.coreweave.com/protect=true
```

Then remove the soft-delete timestamp label as an extra safety measure in case PVMO's watcher cycle has not yet run:

```bash theme={"system"}
kubectl label pv [PV-NAME] pv-failsafe.coreweave.cloud/deletion-timestamp-
```

> [!NOTE]
>
> The trailing `-` in the second command is `kubectl` syntax for removing a label.

## If the soft-delete window has elapsed

If the 24-hour soft-delete window has already passed before you attempt recovery, the PV and its backing storage may have been permanently deleted. Contact [CoreWeave Support](https://coreweave.freshdesk.com/support/login) to check whether a VAST snapshot is available for restoration.
