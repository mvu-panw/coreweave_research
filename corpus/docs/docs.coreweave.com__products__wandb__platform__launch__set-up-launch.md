# Set up Launch

Source: https://docs.coreweave.com/products/wandb/platform/launch/set-up-launch

# Set up Launch

> Set up W&B Launch by configuring a queue and deploying an agent to submit jobs to your compute infrastructure.

This page describes the high-level steps required to set up W\&B Launch so that you can submit machine learning jobs to your own compute infrastructure (such as Kubernetes, Amazon SageMaker, or Vertex AI) directly from Weights & Biases. Setting up Launch enables your team to share compute resources, queue jobs, and reproduce runs across environments.

To set up Launch, you must complete the following:

1. **Set up a queue**: Queues are first-in, first-out (FIFO) and possess a queue configuration. A queue's configuration controls where and how jobs run on a target resource.
2. **Set up an agent**: Agents run on your machine or infrastructure and poll one or more queues for launch jobs. When the agent pulls a job, it ensures that the image is built and available. The agent then submits the job to the target resource.

After you complete both steps, your team can submit launch jobs to the queue and run them automatically on the target resource.

## Set up a queue

Configure launch queues to point to a specific target resource along with any additional configuration specific to that resource. For example, a launch queue that points to a Kubernetes cluster might include environment variables or set a custom namespace in its launch queue configuration. When you create a queue, you specify both the target resource you want to use and the configuration for that resource to use.

When an agent receives a job from a queue, it also receives the queue configuration. When the agent submits the job to the target resource, it includes the queue configuration along with any overrides from the job itself. For example, you can use a job configuration to specify the Amazon SageMaker instance type for that job instance only. In this case, it's common to use [queue config templates](https://docs.coreweave.com/products/wandb/platform/launch/setup-queue-advanced.md#configure-queue-template) as the end user interface.

### Create a queue

Create a queue to define where launch jobs run and how they're configured. To create a queue:

1. Navigate to Launch App at [https://forge.coreweave.com/wandb/launch](https://forge.coreweave.com/wandb/launch).
2. Click the **create queue** button on the top right of the screen.
3. From the **Entity** dropdown menu, select the entity the queue belongs to.
4. Provide a name for your queue in the **Queue** field.
5. From the **Resource** dropdown, select the compute resource you want jobs added to this queue to use.
6. Choose whether to allow **Prioritization** for this queue. If prioritization is enabled, a user on your team can define a priority for their launch job when they enqueue it. Higher priority jobs run before lower priority jobs.
7. Provide a resource configuration in either JSON or YAML format in the **Configuration** field. The structure and semantics of your configuration document depend on the resource type that the queue points to. For more details, see the dedicated set up page for your target resource.

![Creating a Launch queue](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/create-queue.gif?s=b1b45e0c25106d463208f8e8408bcd9d)

You now have a queue that can receive launch jobs and route them to your chosen target resource. Next, set up an agent to pull jobs from this queue.

## Set up a launch agent

Launch agents are long-running processes that poll one or more launch queues for jobs. Launch agents dequeue jobs in FIFO order or in priority order depending on the queues they pull from. When an agent dequeues a job from a queue, it optionally builds an image for that job. The agent then submits the job to the target resource along with configuration options specified in the queue configuration.

> [!NOTE]
>
> Agents are flexible and can be configured to support many use cases. The required configuration for your agent depends on your specific use case. See the dedicated page for [Docker](https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-docker.md), [Amazon SageMaker](https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-sagemaker.md), [Kubernetes](https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-kubernetes.md), or [Vertex AI](https://docs.coreweave.com/products/wandb/platform/launch/setup-vertex.md).

> [!NOTE]
>
> Weights & Biases recommends you start agents with a service account's API key, rather than a specific user's API key. Using a service account's API key has two benefits:
>
> * The agent isn't dependent on an individual user.
> * Launch views the author associated with a run created through Launch as the user who submitted the launch job, rather than the user associated with the agent.

### Agent configuration

Configure the launch agent so it knows which queues to poll, which entity to operate under, and how many jobs to run in parallel. Configure the launch agent with a YAML file named `launch-config.yaml`. By default, Weights & Biases checks for the config file in `~/.config/wandb/launch-config.yaml`. You can optionally specify a different directory when you activate the launch agent.

The contents of your launch agent's configuration file depend on your launch agent's environment, the launch queue's target resource, Docker builder requirements, cloud registry requirements, and so forth.

Independent of your use case, the launch agent has the following core configurable options:

* `max_jobs`: Maximum number of jobs the agent can execute in parallel.
* `entity`: The entity that the queue belongs to.
* `queues`: The name of one or more queues for the agent to watch.

> [!NOTE]
>
> You can use the W\&B CLI to specify universal configurable options for the launch agent (instead of the config YAML file): maximum number of jobs, Weights & Biases entity, and launch queues. See the [`wandb launch-agent`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-launch-agent) command for more information.

The following YAML snippet shows how to specify core launch agent config keys. Replace `[ENTITY-NAME]` with your Weights & Biases entity, and replace `[QUEUE-NAME]` with the name of a queue for the agent to poll.

```yaml title="launch-config.yaml" theme={"system"}
# Max number of concurrent runs to perform. -1 = no limit
max_jobs: -1

entity: [ENTITY-NAME]

# List of queues to poll.
queues:
  - [QUEUE-NAME]
```

### Configure a container builder

You can configure the launch agent to build images. You must configure the agent to use a container builder if you intend to use launch jobs created from git repositories or code artifacts. See [Create a launch job](https://docs.coreweave.com/products/wandb/platform/launch/create-launch-job.md) for more information on how to create a launch job.

W\&B Launch supports three builder options:

* Docker: The Docker builder uses a local Docker daemon to build images.
* [Kaniko](https://github.com/GoogleContainerTools/kaniko): Kaniko is a Google project that enables image building in environments where a Docker daemon is unavailable.
* Noop: The agent doesn't try to build jobs, and instead only pulls pre-built images.

> [!NOTE]
>
> Use the Kaniko builder if your agent is polling in an environment where a Docker daemon is unavailable (for example, a Kubernetes cluster).
>
> See [Set up Kubernetes](https://docs.coreweave.com/products/wandb/platform/launch/setup-launch-kubernetes.md) for details about the Kaniko builder.

To specify an image builder, include the builder key in your agent configuration. For example, the following code snippet shows a portion of the launch config (`launch-config.yaml`) that specifies to use Docker or Kaniko:

```yaml title="launch-config.yaml" theme={"system"}
builder:
  type: docker | kaniko | noop
```

### Configure a container registry

Sometimes, you might want to connect a launch agent to a cloud registry so it can pull pre-built images or push images it builds. Common scenarios for connecting a launch agent to a cloud registry include:

* You want to run a job in an environment other than where you built it, such as a powerful workstation or cluster.
* You want to use the agent to build images and run these images on Amazon SageMaker or Vertex AI.
* You want the launch agent to provide credentials to pull from an image repository.

To learn more about how to configure the agent to interact with a container registry, see the [Advanced agent setup page](https://docs.coreweave.com/products/wandb/platform/launch/setup-agent-advanced.md).

## Activate the launch agent

After you configure the agent, activate it so that it starts polling the queues you specified and dispatching jobs to your target resource. Activate the launch agent with the `launch-agent` W\&B CLI command. Replace `[QUEUE-1]` and `[QUEUE-2]` with the names of queues for the agent to poll:

```bash theme={"system"}
wandb launch-agent -q [QUEUE-1] -q [QUEUE-2] --max-jobs 5
```

Once the agent is running, the agent pulls any jobs submitted to the specified queues and forwards them to the target resource.

Sometimes, you might want to have a launch agent poll queues from within a Kubernetes cluster. See the [Advanced queue set up page](https://docs.coreweave.com/products/wandb/platform/launch/setup-queue-advanced.md) for more information.
