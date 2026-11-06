# Interact with SUNK using kubectl

Source: https://docs.coreweave.com/products/sunk/manage_sunk/interact-with-kubernetes

# Interact with SUNK using kubectl

> Use kubectl to interact with SUNK Kubernetes resources, access logs, and restart the Slurm Controller

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Kubernetes is a container orchestration platform that manages the underlying infrastructure for SUNK, including compute resources, networking, and storage. SUNK uses Kubernetes to provide a scalable, flexible, and high-performance computing environment for running Slurm workloads.

When you use SUNK, you can interact with Kubernetes using the `kubectl` command-line tool. This guide explains the key concepts, benefits, and best practices for using `kubectl` to interact with Kubernetes in the context of SUNK. By following this guide, you'll learn how to inspect cluster resources, access Slurm daemon logs, and restart the Slurm Controller and `slurmd` daemons when troubleshooting. This guide is for SUNK users and administrators who need to observe or manage the Kubernetes resources backing their Slurm cluster.

## Key concepts

The following terminology and concepts describe the relationship between Kubernetes and Slurm in the context of SUNK:

| Term | Description |
| - | - |
| **Kubernetes cluster and Nodes** | A Kubernetes cluster is a collection of Kubernetes Nodes, which are (in CKS) physical machines that run Kubernetes components and containerized applications. Kubernetes **Nodes** are capitalized as proper nouns. |
| **Kubernetes Pod** | A Kubernetes Pod is the smallest deployable unit in Kubernetes, representing a single instance of a running process, such as a Slurm node. Multiple Pods can run on a single Kubernetes Node. |
| **Slurm cluster and nodes** | A Slurm cluster is a collection of Slurm nodes, where each node is a Kubernetes Pod that runs a `slurmd` container. Slurm **nodes** are lowercase. |
| **`kubectl`** | `kubectl` is the command-line tool for interacting with Kubernetes clusters. It lets you inspect cluster resources, create, delete, and update objects, and view logs and events. |

When you use a Slurm cluster deployed by SUNK, you're operating within a Kubernetes environment. This means Kubernetes manages the underlying infrastructure, and you can observe and control many aspects of SUNK's operation using `kubectl`, the command-line tool for Kubernetes.

## Benefits

Here are some reasons why you might want to interact with Kubernetes through `kubectl`:

* **Visibility**: You can use `kubectl` to see the status of the Kubernetes Pods where your Slurm jobs run, which provides insight into the underlying execution environment. SUNK Standard deploys SUNK with Helm charts, and SUNK Self-Service deploys it through a `SunkCluster` resource. In both modes, the components run as Kubernetes resources that you can inspect with `kubectl`.
* **Debugging**: If you encounter issues, `kubectl` helps you inspect logs, events, and the state of the Pods, which aids troubleshooting.
* **Familiarity**: If you already have experience with Kubernetes, using `kubectl` to observe SUNK offers a familiar way to interact with the system.
* **Configuration**: Many aspects of SUNK's configuration are managed as Kubernetes resources (such as ConfigMaps and Secrets), which you can interact with using `kubectl`.

## Access logs

Because Slurm daemons run within Pods, you can view their logs using the `kubectl logs` command, optionally with the `-f` flag to follow the logs in real time. To access the logs of the Slurm Controller, which manages job submissions and scheduling, use this command:

```bash theme={"system"}
kubectl logs -f -l app.kubernetes.io/name=slurmctld -c slurmctld
```

To see what's happening on a specific Slurm compute node, list the `slurmd` logs for that Pod. The name of a Slurm node matches the name of its corresponding Kubernetes Pod, so you can get the logs by substituting the node's name for `[POD-NAME]` in the following:

```bash theme={"system"}
kubectl logs -f -c slurmd [POD-NAME]
```

## Restart the Slurm Controller

If your jobs are stuck in a `pending` state, you may need to restart the Slurm Controller. The Controller manages job submissions and scheduling, so restarting it can clear scheduling issues without disrupting active jobs. To restart the Slurm Controller, first find the name of the Controller deployment:

```bash theme={"system"}
kubectl get deployments -l app.kubernetes.io/component=controller
```

Now that you have the deployment name, restart it with the following command, replacing `[CONTROLLER-DEPLOYMENT-NAME]` with the name you found earlier:

```bash theme={"system"}
kubectl rollout restart deployment [CONTROLLER-DEPLOYMENT-NAME]
```

You can confirm that the restart is happening by checking the status of the rollout:

```bash theme={"system"}
kubectl rollout status deployment [CONTROLLER-DEPLOYMENT-NAME]
```

Restarting the Controller doesn't cancel active jobs, but can fix problems involving jobs that are stuck pending. It's a safe operation to perform when troubleshooting.

## Restart the Slurm daemon

If a Slurm compute node is misbehaving or needs to re-register with the Controller, restart its `slurmd` daemon by deleting the Kubernetes Pod that runs the Slurm node. Restarting the Kubernetes Pod removes the node from the Slurm pool of nodes, and re-registers it when the Pod is recreated.

To find the name of the Kubernetes Pod that runs the Slurm node, use the `get pod` command, replacing `[SLURM-NODE-NAME]` with the name of the Slurm node:

```bash theme={"system"}
kubectl -n tenant-slurm get pod -o wide [SLURM-NODE-NAME]
```

To delete the Pod, use the `delete pod` command, replacing `[POD-NAME]` with the name provided by the `get pod` command:

```bash theme={"system"}
kubectl -n tenant-slurm delete pod [POD-NAME]
```
