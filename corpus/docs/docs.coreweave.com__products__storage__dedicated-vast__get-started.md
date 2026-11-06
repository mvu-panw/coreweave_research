# Get started with Dedicated VAST

Source: https://docs.coreweave.com/products/storage/dedicated-vast/get-started

# Get started with Dedicated VAST

> Post-provisioning checklist for connecting your CKS workloads to a Dedicated VAST cluster.

This guide walks through the steps to go from a newly provisioned Dedicated VAST cluster to running workloads that read and write data on VAST. By following it, administrators and platform engineers connect their CKS workloads to VAST storage, configure initial user access, and verify that Pods can read and write through the VAST CSI driver.

## Prerequisites

* A Dedicated VAST cluster provisioned by CoreWeave. [Contact Sales](https://www.coreweave.com/contact-us) if you haven't yet started the provisioning process.
* A CoreWeave Kubernetes Service (CKS) cluster in the same data center as your VAST cluster.
* `kubectl` configured to access your CKS cluster.

CoreWeave installs the VAST CSI driver on your CKS cluster during the provisioning process.

## What you receive after provisioning

After CoreWeave provisions your Dedicated VAST cluster, you receive an endpoint and admin credentials to access your cluster. No additional setup is required to gain access.

CoreWeave establishes network access between your CKS cluster nodes and the VAST cluster IPs. No additional network configuration is required.

After you receive the admin account credentials, you have full control over RBAC and user management. The next step is to log in to the VAST Management System (VMS) and verify cluster health.

## Step 1: Log in to VMS and verify cluster health

Confirm that your cluster is reachable and healthy before configuring access for users or workloads.

1. Open the VMS URL provided by CoreWeave in your browser.
2. Log in using the initial admin credentials.
3. Verify that the cluster health dashboard shows all components in a healthy state.

For a full overview of VMS capabilities, see [Cluster management](https://docs.coreweave.com/products/storage/dedicated-vast/cluster-management.md).

## Step 2: Create user accounts

User accounts in VMS control who can access VAST directly and which workloads can authenticate to the S3 endpoint. Create VAST user accounts in VMS for your team members and workloads:

1. **Team users**: Create individual user accounts for team members who need direct NFS, S3, or SQL access. See the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1) for user management procedures.
2. **S3 service accounts**: Optional. If workloads access data through the S3 protocol, enable S3 on the relevant user accounts and generate S3 access keys.

## Step 3: Create a View (optional)

A View maps a filesystem path to one or more protocols such as NFS, S3, block, and SQL. Your cluster may already have a default View configured. If you need a custom View for your workloads:

1. In VMS, navigate to the Views configuration.
2. Create a new View with a filesystem path (for example, `/data`) and enable the protocols your workloads require.
3. Configure access permissions for the View.

For details on View configuration, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Step 4: Create a PVC

A PersistentVolumeClaim (PVC) is what makes VAST storage available to a Pod. CoreWeave deploys the VAST CSI driver and creates a default VAST StorageClass on your CKS cluster during provisioning. Reference this StorageClass in your PVCs to provision volumes backed by your Dedicated VAST cluster. To request a custom StorageClass, contact [CoreWeave support](https://docs.coreweave.com/support.md).

Create a PVC using the default StorageClass:

```yaml theme={"system"}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vast-test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: vast-dedicated
  resources:
    requests:
      storage: 100Gi
```

## Step 5: Mount in a workload and verify

This step confirms that the full path from your CKS Pods to VAST storage works before you move production workloads onto the cluster. Create a test Pod that mounts the PVC and verify that reads and writes succeed:

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: vast-test-pod
spec:
  containers:
    - name: test
      image: busybox
      command: ["sh", "-c", "echo 'hello from VAST' > /data/test.txt && cat /data/test.txt && sleep 3600"]
      volumeMounts:
        - name: vast-volume
          mountPath: /data
  volumes:
    - name: vast-volume
      persistentVolumeClaim:
        claimName: vast-test-pvc
```

```bash theme={"system"}
kubectl apply -f vast-test-pod.yaml
kubectl logs vast-test-pod
```

If the Pod logs show `hello from VAST`, your CKS cluster is connected to Dedicated VAST. At this point, admin access, user accounts, a View (default or custom), and a verified CSI mount path are all in place.

## Next steps

With your cluster connected and verified, configure Dedicated VAST to match your workload requirements:

* **Set up QoS and quotas**: Allocate cluster resources across teams and workloads. See [Cluster management](https://docs.coreweave.com/products/storage/dedicated-vast/cluster-management.md#qos-and-quotas).
* **Configure snapshot policies**: Set up automated backup schedules. See [Data services](https://docs.coreweave.com/products/storage/dedicated-vast/data-services.md#snapshots).
* **Enable audit logging**: Configure logging for compliance and monitoring. See [Security](https://docs.coreweave.com/products/storage/dedicated-vast/security.md#audit-logging).
* **Configure S3 access**: Enable S3 protocol access for workloads that use the S3 API. This is your cluster's native S3 endpoint, separate from [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md). See [Protocols and data access](https://docs.coreweave.com/products/storage/dedicated-vast/protocols-and-access.md#s3-access).
* **Explore VAST Catalog**: Search and query file and object metadata across your cluster. See [Data services](https://docs.coreweave.com/products/storage/dedicated-vast/data-services.md#vast-catalog).
