# Three-layer orchestration model

Source: https://docs.coreweave.com/products/sunk/discover_sunk/three-layers-of-orchestration

# Three-layer orchestration model

> Understand CoreWeave's three-layer orchestration model

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

"Orchestration" refers to the management of distinct but interconnected functionalities, each with its own requirements and best practices. Orchestration for large-scale HPC clusters presents challenges and requires a thoughtful approach. CoreWeave uses a three-layer orchestration model to help simplify this process.

When you understand the orchestration model and its associated options, you can craft full-stack solutions based on your specific requirements while maximizing the benefits each solution provides. This page is for architects, platform engineers, and HPC practitioners who are evaluating how to combine systems like Kubernetes, Slurm, and Ray on CoreWeave.

This article outlines CoreWeave's three-layer orchestration model and solutions that use various combinations of Kubernetes, Slurm, and Ray. By the end, you understand the responsibilities of each layer and how several common stacks map onto them.

## The three layers of orchestration

The following sections describe the three layers and the responsibilities of each. CoreWeave's orchestration model defines the following layers:

| Layer | Purpose |
| - | - |
| Compute | Manages physical resources available to customers |
| Workload | Manages the workloads running on the available resources |
| Process | Controls the code that executes across your resources |

### Compute orchestration

> [!TIP]
>
> **Compute** refers to the physical resources that CoreWeave makes available to customers.

The Compute layer manages the Node lifecycle. It takes action when a hardware failure occurs, preempts spot Nodes, and autoscales to provide additional compute during periods of high demand. A strong solution on this layer ensures on-demand access to the best-performing Nodes.

### Workload orchestration

The Workload layer manages the lifecycle of the actual workloads that run on the Nodes provided by the Compute layer. Workload lifecycle management includes scaling up replicas to meet increases in demand, gang scheduling, ordering jobs by priority within a queue, and assigning resources to jobs based on physical topologies.

### Process orchestration

The process orchestrator controls the code that executes across your resources. This can address simple cases, such as single-GPU or single-Node workloads, or large-scale distributed workloads, such as training LLMs.

A process orchestrator must be flexible and intuitive enough to handle complex dataflows, such as those in Reinforcement Learning jobs, while maximizing the Compute allocated to your workload.

## Example stacks

With the three layers established, the following sections describe how real systems map onto them. A single system can span multiple layers, or you can combine different systems across these layers. This allows you to assign each system to the layer it best suits.

The following examples discuss different stacks including Kubernetes, Slurm, and Ray. You can apply each as an orchestrator to any of these three layers.

### Full Kubernetes stack

Kubernetes is a popular choice for orchestration across each of the three layers.

A full Kubernetes stack is arranged as follows:

| Layer | Solution | Mechanism |
| - | - | - |
| Compute allocation | Kubernetes | `kubelet` |
| Workload allocation | Kubernetes | `kube-scheduler`, `Kueue`, `Volcano` |
| Process allocation | Kubernetes | `Pod.spec.command` |

The Compute Nodes run `kubelet`, which makes their resources available for scheduling. Managed providers, such as [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md), also come fully equipped with lifecycle controllers for triaging issues, and systems for autoscaling, spot instances, and more.

The wide range of different resources you can submit, each with its own lifecycle behaviors, handles workload allocation. Third-party add-ons are also available to extend this functionality.

The container image's entry point handles process allocation, or commands and arguments in the Kubernetes resource's configuration override it.

For example, a `kind: JobSet` for training ResNet might resemble the following:

```yaml theme={"system"}
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: pytorch
  labels:
    kueue.x-k8s.io/queue-name: training
spec:
  replicatedJobs:
    - name: workers
      template:
        spec:
          parallelism: 4
          completions: 4
          backoffLimit: 0
          template:
           spec:
            containers:
            - name: pytorch
              image: gcr.io/k8s-staging-jobset/pytorch-resnet:latest
              ports:
              - containerPort: 3389
              env:
              - name: MASTER_ADDR
                value: "pytorch-workers-0-0.pytorch"
              - name: MASTER_PORT
                value: "3389"
              command:
              - bash
              - -xc
              - |
                torchrun --nproc_per_node=1 --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT resnet.py --backend=gloo

```

After you submit it, `Kueue` handles quota management, `kube-scheduler` assigns the resources to each of the four replicas, and the containers start training by running the specified `torchrun` command.

Many CoreWeave customers use a full Kubernetes orchestration stack to use large-scale Compute clusters. However, to help support large-scale training, CoreWeave adds several Kubernetes-native workload orchestration features (`Kueue` and `JobSets`, in this example) to the ecosystem.

### SUNK

[Slurm](https://slurm.schedmd.com/) is a strong solution for workload orchestration, particularly for batch jobs on large-scale Compute clusters, and has been the trusted choice of many of the largest HPC clusters in the world for years.

Although Slurm and Kubernetes are both standard solutions for orchestration, they have typically remained two separate systems, without combination.

CoreWeave developed [SUNK](https://docs.coreweave.com/products/sunk.md) to address the needs of large-scale LLM training by harnessing the strengths of both Slurm and Kubernetes. Since SUNK's release, this use of Kubernetes for Compute and Slurm for workload orchestration has become a standard, and industry reports like [SemiAnalysis's ClusterMAX](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard?open=false#%C2%A7slurm-on-kubernetes) recognize it.

The SUNK stack is arranged as shown in the following table:

| Layer | Solution | Mechanism |
| - | - | - |
| Compute allocation | Kubernetes | `kubelet` |
| Workload allocation | Slurm | `slurmctld` |
| Process allocation | Slurm | `srun` |

In this stack, a Kubernetes cluster orchestrates the Compute Nodes and runs `slurmd` on each Node as a Kubernetes resource.

Users submit their Slurm jobs to the Slurm controller, `slurmctld`, which handles the workload allocation.

Within the definition of the submitted Slurm jobs, the `srun` Slurm command launches the specified processes across the Compute Nodes assigned to each job.

### Ray on Kubernetes

Anyscale's open-source [Ray Core library](https://docs.ray.io/en/latest/ray-core/walkthrough.html) provides an alternative process orchestrator to Slurm. It uses the Actor paradigm, which implements the [actor model](https://en.wikipedia.org/wiki/Actor_model) through RPC calls wrapped under Python abstractions.

With Ray as a process orchestrator, users submit a "driver" program that uses the Ray library to instantiate Actors across the Compute allocated to the workload, and triggers different processes to run within each.

With Ray on Kubernetes, the stack is arranged as follows:

| Layer | Solution | Mechanism |
| - | - | - |
| Compute allocation | Kubernetes | `kubelet` |
| Workload allocation | Kubernetes | `kube-scheduler` |
| Process allocation | Ray | `raylet` |

Resources like `JobSet` schedule `raylet` across the Compute allocated to a workload, as demonstrated in the following pseudocode:

```yaml theme={"system"}
kind: JobSet
metadata:
  name: ray-cluster-example
spec:
  replicatedJobs:
  - name: ray-head
    template:
      spec:
        command: ["ray", "start", "--head"]
  - name: ray-workers
    replicas: 2
    template:
      spec:
        command: ["ray", "start", "--address", "ray-head-0.ray-cluster-example.default.svc:6379"]

```

After the Ray cluster starts, you submit a driver program similar to Slurm's `sbatch` into the Ray cluster, as shown in the following pseudocode:

```python theme={"system"}
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ray",
# ]
# [tool.uv]
# exclude-newer = "2025-10-06T00:00:00Z"
# ///
import ray


@ray.remote
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

    def get_counter(self):
        return self.value


if __name__ == "__main__":
    ray.init()
    counter = Counter.remote()
    for _ in range(5):
        print(ray.get(counter.get_counter.remote()))
        counter.increment.remote()


```

### Ray on SUNK

The final example combines the previous two stacks. As discussed earlier, Slurm can take the role of the workload orchestrator from Kubernetes. You can combine this functionality with the previous Ray on Kubernetes stack.

Ray on SUNK provides a stack with a separate system used for each layer, where each system uses its unique strengths in its respective layer.

With Ray on SUNK, the layers function as follows:

| Layer | Solution | Mechanism |
| - | - | - |
| Compute allocation | Kubernetes | `kubelet` |
| Workload allocation | Slurm | `slurmctld` |
| Process allocation | Ray | `raylet` |

Instead of using a `JobSet` or a `kind: RayCluster` to orchestrate the creation of a Ray cluster, you modify Slurm's `sbatch` directive to create a Ray cluster within the job before submitting a driver program in a similar fashion.

For a full example of this stack, see the [Run Ray on SUNK](https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk.md) guide.
