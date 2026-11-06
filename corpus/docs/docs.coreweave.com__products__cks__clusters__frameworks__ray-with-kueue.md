# Run Ray with Kueue

Source: https://docs.coreweave.com/products/cks/clusters/frameworks/ray-with-kueue

# Run Ray with Kueue

> Install Ray and Kueue on CKS for distributed compute with efficient scheduling and job queuing

This guide shows ML engineers and platform operators how to set up [Ray](https://docs.ray.io/en/latest/) with [Kueue](https://kueue.sigs.k8s.io/) on CKS so that Kueue can schedule and queue distributed compute workloads on shared GPU resources. It covers the following:

* Install Ray and Kueue.
* Create Ray clusters that can queue jobs.
* Use helper scripts to manage distributed computing workloads.

By the end of this guide, you have a distributed compute environment where Ray executes jobs and Kueue schedules and queues those jobs inside your CKS cluster.

## Prerequisites

Before you begin, we recommend creating a PVC for shared use. This makes it easier for ML engineers working together to maintain persistent directories across ephemeral or autoscaling clusters. For information on creating a PVC, see [Create PVCs](https://docs.coreweave.com/products/storage/distributed-file-storage/manage-volumes.md#create-pvcs).

If you want to connect to your Pods using SSH, you need to build your Ray image with an SSH server.

## Install Ray

Ray provides the distributed compute runtime that executes your jobs across the cluster. Install the KubeRay operator on your CKS cluster to manage Ray clusters as Kubernetes resources.

To install Ray, complete the following steps:

1. Add the KubeRay Helm repository:

   ```bash theme={"system"}
   helm repo add kuberay https://ray-project.github.io/kuberay-helm/
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   "kuberay" has been added to your repositories
   ```

2. Install KubeRay on your CKS cluster:

   ```bash theme={"system"}
   helm install kuberay-operator kuberay/kuberay-operator --version 1.4.0
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   NAME: kuberay-operator
   LAST DEPLOYED: Tue Aug 19 14:46:56 2025
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   ```

## Install Kueue

With the KubeRay operator running, the next step is to install Kueue, which handles job queuing and quota-aware scheduling for the Ray clusters you create later in this guide.

To install Kueue, follow the [Kueue documentation](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue.md).

After you install Kueue, be sure to deploy the Kueue configuration file with `kubectl apply -f [KUEUE-CONFIG-FILE]`.

> [!NOTE]
>
> Kueue is configured to find the local queue in the default namespace. Work within the default namespace for this guide.

## Create a Ray cluster

With Ray and Kueue installed, you can now create a Ray cluster that submits its workloads through Kueue. To make it easier to create and manage a Ray cluster, we recommend using the following script: [`create_ray_box`](https://github.com/coreweave/reference-architecture/blob/main/ray-kueue/scripts/create_ray_box).

To use the script, complete the following steps:

1. Download the script using curl:

   ```bash theme={"system"}
   curl -o create_ray_box https://raw.githubusercontent.com/coreweave/reference-architecture/main/ray-kueue/scripts/create_ray_box
   ```

2. Make the script executable:

   ```bash theme={"system"}
   chmod +x create_ray_box
   ```

3. Modify the lines related to GPUs, CPUs, and memory so the Ray head Node's resource requests match the capacity of your Node Pool:

   ```text theme={"system"}
   # Set resource requests and limits for the Ray head node.
   resources:
     limits:
       # Modify CPU based on the CPUs in your Node Pool.
       cpu: "120"

       # Modify memory based on the memory in your Node Pool.
       memory: "2000G"

       # Modify the number of GPUs based on the GPUs in your Node Pool.
       nvidia.com/gpu: 8
       rdma/ib: "1"
     requests:
       # For production use-cases, we recommend specifying integer CPU requests and limits.
       # We also recommend setting requests equal to limits for both CPU and memory.

       # Modify CPU based on the CPUs in your Node Pool.
       cpu: "120"

       # Modify memory based on the memory in your Node Pool.
       memory: "2000G"

       # Modify the number of GPUs based on the GPUs in your Node Pool.
       nvidia.com/gpu: 8
       rdma/ib: "1"
   ```

You can now run `./create_ray_box` without arguments to see its options.

### Examples

The following two examples show how to create a Ray cluster.

> [tab] Using provided script
>
> The following example creates a Ray dev box with four worker Nodes and one head Node. Replace `[RAY-DOCKER-IMAGE]` with the Ray Docker image you want to use.
>
> ```bash theme={"system"}
> create_ray_box --nodes 4 --name mydevbox --image [RAY-DOCKER-IMAGE]
> ```
>
> The command uses the following options:
>
> * **`--nodes`**: The number of Nodes is the number of workers, in addition to the head Node. This example creates a Ray dev box with a total of four worker Nodes and one head Node. All Nodes can run jobs. If resources are insufficient, the cluster is queued.
>
> * **`--image`**: The Ray Docker image. We recommend building a custom Ray image using CoreWeave's [nccl-tests](https://github.com/coreweave/nccl-tests) as a base image for [InfiniBand](https://docs.coreweave.com/platform/instances/selecting-an-instance.md#the-role-of-nvlink-and-infiniband) support. If you don't include the `--image` option, the script uses the `rayproject/ray-ml:2.9.0-gpu` image.

> [tab] Using a YAML file
>
> You can also create a Ray cluster with only YAML files.
>
> If you haven't already created a PVC, apply the following manifest to create a shared PVC:
>
> ```bash theme={"system"}
> kubectl apply -f https://raw.githubusercontent.com/coreweave/reference-architecture/refs/heads/main/ray-kueue/yamls/pvc.yaml
> ```
>
> To create the Ray cluster, apply the [ray-cluster-sample](https://github.com/coreweave/reference-architecture/blob/main/ray-kueue/yamls/ray-cluster-sample.yaml) manifest:
>
> ```bash theme={"system"}
> kubectl apply -f https://raw.githubusercontent.com/coreweave/reference-architecture/refs/heads/main/ray-kueue/yamls/ray-cluster-sample.yaml
> ```

## Work with Ray clusters

After your Ray cluster is up, use the following commands to inspect clusters, log into Pods, and manage queued jobs.

| Task | Command | Notes |
| - | - | - |
| **List Ray clusters** | `kubectl get raycluster` | Shows all clusters in the namespace. |
| **List Pods** | `kubectl get pods` | Lists the head and worker Pods. |
| **Log into head Pod** | `kubectl exec -it [CLUSTER-NAME]-head -- /bin/bash` | Replace `[CLUSTER-NAME]` with your cluster's name. |
| **Log into worker Pod** | `kubectl exec -it [WORKER-POD-NAME] -- /bin/bash` | Replace `[WORKER-POD-NAME]` with the actual Pod name. |
| **List jobs in queue** | `kubectl get queue` | View pending and admitted workloads. |
| **Get queue details** | `kubectl describe queue` | Shows detailed information about the queue and jobs. |
| **Delete a Ray cluster** | `kubectl delete raycluster [CLUSTER-NAME]` | Replace `[CLUSTER-NAME]` with your cluster's name. |
| **Shared storage path** | `/mnt/vast` | Where shared storage is configured. |

## Test NCCL

Before running production workloads, we recommend verifying that NCCL communication over InfiniBand works correctly across your Ray Nodes. To test that InfiniBand is correctly configured with your container and cluster, you can run the script [`nccl-test/all_reduce_ray.py`](https://raw.githubusercontent.com/coreweave/reference-architecture/refs/heads/main/ray-kueue/nccl-test/all_reduce_ray.py).

## Additional helper scripts

In the [CoreWeave/reference-architecture](https://github.com/coreweave/reference-architecture/tree/main) repository, you can find [helper scripts](https://github.com/coreweave/reference-architecture/tree/main/ray-kueue/scripts) for working with Ray clusters. These utility Python scripts make it easier to work with a small team on a Ray cluster. For example, to view the Ray cluster capacity, navigate to the `ray-kueue` directory in the reference architecture repository and use the `capacity` script:

```bash theme={"system"}
python3 scripts/capacity
```
