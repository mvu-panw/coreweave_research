# Tutorial: Set up W&B Launch on Kubernetes

Source: https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-kubernetes

# Tutorial: Set up W&B Launch on Kubernetes

> Set up W&B Launch on a Kubernetes cluster using Helm charts, Kaniko image building, and Kubernetes job specs.

This tutorial walks cluster administrators through setting up W\&B Launch on a Kubernetes cluster so ML engineers can submit and manage training workloads directly from Weights & Biases. You can use W\&B Launch to push ML workloads to a Kubernetes cluster, giving ML engineers an interface right in Weights & Biases to use the resources you already manage with Kubernetes.

Weights & Biases maintains an [official Launch agent image](https://hub.docker.com/r/wandb/launch-agent) that you can deploy to your cluster with a [Helm chart](https://github.com/wandb/helm-charts/tree/main/charts/launch-agent) that Weights & Biases maintains.

Weights & Biases uses the [Kaniko](https://github.com/GoogleContainerTools/kaniko) builder to let the Launch agent build Docker images in a Kubernetes cluster. To learn more about how to set up Kaniko for the Launch agent, or how to turn off job building and only use prebuilt Docker images, see [Advanced agent setup](https://docs.coreweave.com/products/wandb/platform/launch/setup-agent-advanced.md).

> [!NOTE]
>
> To install Helm and apply or upgrade the W\&B Launch agent Helm chart, you must have `kubectl` access to the cluster with sufficient permissions to create, update, and delete Kubernetes resources. Typically, this requires a user with `cluster-admin` or a custom role with equivalent permissions.

## Configure a queue for Kubernetes

A Launch queue defines the Kubernetes workload spec that the agent uses to run each job. The Launch queue configuration for a Kubernetes target resource resembles either a [Kubernetes job spec](https://kubernetes.io/docs/concepts/workloads/controllers/job/) or a [Kubernetes custom resource spec](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

You can control any aspect of the Kubernetes workload resource spec when you create a Launch queue.

> [tab] Kubernetes job spec
>
> ```yaml theme={"system"}
> spec:
>   template:
>     spec:
>       containers:
>         - env:
>             - name: MY_ENV_VAR
>               value: some-value
>           resources:
>             requests:
>               cpu: 1000m
>               memory: 1Gi
> metadata:
>   labels:
>     queue: k8s-test
> namespace: wandb
> ```

> [tab] Custom resource spec
>
> In some use cases, you might want to use `CustomResource` definitions. For example, `CustomResource` definitions are useful when you want to perform multi-node distributed training. See the tutorial for using Launch with multi-node jobs using Volcano for an example application. Another use case is when you want to use Launch with Kubeflow.
>
> The following YAML snippet shows a sample Launch queue config that uses Kubeflow:
>
> ```yaml theme={"system"}
> kubernetes:
>   kind: PyTorchJob
>   spec:
>     pytorchReplicaSpecs:
>       Master:
>         replicas: 1
>         template:
>           spec:
>             containers:
>               - name: pytorch
>                 image: '${image_uri}'
>                 imagePullPolicy: Always
>         restartPolicy: Never
>       Worker:
>         replicas: 2
>         template:
>           spec:
>             containers:
>               - name: pytorch
>                 image: '${image_uri}'
>                 imagePullPolicy: Always
>         restartPolicy: Never
>     ttlSecondsAfterFinished: 600
>   metadata:
>     name: '${run_id}-pytorch-job'
>   apiVersion: kubeflow.org/v1
> ```

For security reasons, Weights & Biases injects the following resources into your Launch queue if you don't specify them:

* `securityContext`
* `backOffLimit`
* `ttlSecondsAfterFinished`

The following YAML snippet shows how these values appear in your Launch queue:

```yaml title="example-spec.yaml" theme={"system"}
spec:
  template:
    backOffLimit: 0
    ttlSecondsAfterFinished: 60
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
      seccompProfile:
        type: "RuntimeDefault"
```

## Create a queue

Create a queue in the W\&B App that uses Kubernetes as its compute resource:

1. Navigate to the [Launch page](https://forge.coreweave.com/wandb/launch).
2. Click the **Create Queue** button.
3. Select the **Entity** in which you want to create the queue.
4. Provide a name for your queue in the **Name** field.
5. Select **Kubernetes** as the **Resource**.
6. Within the **Configuration** field, provide the Kubernetes job workflow spec or custom resource spec you configured in [Configure a queue for Kubernetes](#configure-a-queue-for-kubernetes).

## Configure a Launch agent with Helm

With a queue in place, you next deploy the Launch agent that pulls jobs from the queue and runs them on your cluster. Use the [Helm chart](https://github.com/wandb/helm-charts/tree/main/charts/launch-agent) provided by Weights & Biases to deploy the Launch agent into your Kubernetes cluster. Control the behavior of the Launch agent with the `values.yaml` [file](https://github.com/wandb/helm-charts/blob/main/charts/launch-agent/values.yaml).

Within the `launchConfig` key in the `values.yaml` file, specify the contents that you would normally define in your Launch agent config file (`~/.config/wandb/launch-config.yaml`).

For example, suppose you have a Launch agent config that lets you run a Launch agent in EKS that uses the Kaniko Docker image builder. Replace `[QUEUE-NAME]`, `[MAX-CONCURRENT-JOBS]`, `[MY-REGISTRY-URI]`, and `[S3-BUCKET-URI]` with your own values:

```yaml title="launch-config.yaml" theme={"system"}
queues:
  - [QUEUE-NAME]
max_jobs: [MAX-CONCURRENT-JOBS]
environment:
  type: aws
  region: us-east-1
registry:
  type: ecr
  uri: [MY-REGISTRY-URI]
builder:
  type: kaniko
  build-context-store: [S3-BUCKET-URI]
```

Within your `values.yaml` file, this might look like the following. Replace `[QUEUE-NAME]`, `[MAX-CONCURRENT-JOBS]`, `[AWS-REGION]`, `[MY-REGISTRY-URI]`, and `[S3-BUCKET-URI]` with your own values:

```yaml title="values.yaml" theme={"system"}
agent:
  labels: {}
  # W&B API key.
  apiKey: ''
  # Container image to use for the agent.
  image: wandb/launch-agent:latest
  # Image pull policy for agent image.
  imagePullPolicy: Always
  # Resources block for the agent spec.
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi

# Namespace to deploy launch agent into
namespace: wandb

# W&B api url (Set yours here)
baseUrl: https://api.wandb.ai

# Additional target namespaces that the launch agent can deploy into
additionalTargetNamespaces:
  - default
  - wandb

# This should be set to the literal contents of your launch agent config.
launchConfig: |
  queues:
    - [QUEUE-NAME]
  max_jobs: [MAX-CONCURRENT-JOBS]
  environment:
    type: aws
    region: [AWS-REGION]
  registry:
    type: ecr
    uri: [MY-REGISTRY-URI]
  builder:
    type: kaniko
    build-context-store: [S3-BUCKET-URI]

# The contents of a git credentials file. This will be stored in a k8s secret
# and mounted into the agent container. Set this if you want to clone private
# repos.
gitCreds: |

# Annotations for the wandb service account. Useful when setting up workload identity on gcp.
serviceAccount:
  annotations:
    iam.gke.io/gcp-service-account:
    azure.workload.identity/client-id:

# Set to access key for azure storage if using kaniko with azure.
azureStorageAccessKey: ''
```

For more information about registries, environments, and required agent permissions, see [Advanced agent setup](https://docs.coreweave.com/products/wandb/platform/launch/setup-agent-advanced.md).
