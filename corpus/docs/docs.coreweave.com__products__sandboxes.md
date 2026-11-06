# About CoreWeave Sandboxes

Source: https://docs.coreweave.com/products/sandboxes

# About CoreWeave Sandboxes

> Run agent tools, evaluations, and training workloads in isolated environments on CoreWeave.

# Run model-generated code safely, at scale

Run agent tool calls, reinforcement learning rollouts, and evaluations in isolated environments on CoreWeave-managed capacity or your own CKS clusters, using Python or TypeScript.

Sandboxes provide isolated compute environments for running untrusted code, agent tools, evaluations, and reinforcement learning (RL) workloads. Create an environment, run commands, work with files, and collect results through the Python or TypeScript software development kit (SDK).

Start on serverless capacity that CoreWeave operates, with no cluster to provision. When you need control over placement and policy, you can also run sandboxes on your own CoreWeave Kubernetes Service (CKS) clusters.

Serverless sandboxes are generally available, and usage is billed. Access is enabled per organization. To request access for your organization, contact [support](mailto:forge-support@coreweave.com).

## Get started

> [card] [Run your first sandbox](https://docs.coreweave.com/products/sandboxes/get-started.md)
>
> Authenticate and run a command with Python or TypeScript.

> [card] [Run coding agents](https://docs.coreweave.com/products/sandboxes/agents.md)
>
> Choose an integration for interactive coding or autonomous workers.

> [card] [Run evaluations](https://docs.coreweave.com/products/sandboxes/evals.md)
>
> Evaluate code patches, coding agents, and tool-calling models.

> [card] [Build RL workflows](https://docs.coreweave.com/products/sandboxes/client/guides/rl-training.md)
>
> Run model-generated code in sandboxes for reinforcement learning reward evaluation.

Connect [Claude Code](https://docs.coreweave.com/products/sandboxes/agents/claude-code.md), [Claude Managed Agents](https://docs.coreweave.com/products/sandboxes/agents/claude-managed-agents.md), or [Devin Outposts](https://docs.coreweave.com/products/sandboxes/agents/devin-outposts.md) to sandbox workspaces. For your own application, explore the [Python client](https://docs.coreweave.com/products/sandboxes/client.md) and [TypeScript SDK](https://github.com/coreweave/cwsandbox-js/tree/main/packages/cwsandbox).

Use sandboxes with [Harbor](https://github.com/harbor-framework/harbor), or explore the [Sandboxes recipes](https://github.com/coreweave/cwsandbox-recipes) for warm pool examples and the [`taubench-verl` RL training recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/taubench-verl). The [RL training guide](https://docs.coreweave.com/products/sandboxes/client/guides/rl-training.md) uses the [`examples/rl_training/` scripts](https://github.com/coreweave/cwsandbox-client/tree/main/examples/rl_training) in `cwsandbox-client`.

To run pull request tests in disposable sandboxes, see [Run pull request checks in sandboxes](https://docs.coreweave.com/products/sandboxes/tutorials/github-actions.md).

## Configure your sandboxes

Choose the features your workload needs:

* **Configure execution.** Choose your image, CPU, memory, and lifetime with [sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md), or create a multi-container sandbox from a supported [Docker Compose file](https://docs.coreweave.com/products/sandboxes/create-from-file.md).
* **Save and reuse files.** Capture a working directory on a scratch volume with [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md), then restore it into new sandboxes.
* **Attach storage.** Use [volumes](https://docs.coreweave.com/products/sandboxes/volumes.md) for scratch space. On CKS, registered volumes let sandboxes share existing storage.
* **Expose a service.** Give a sandbox application a public address with [public endpoints](https://docs.coreweave.com/products/sandboxes/public-endpoints.md).
* **Use GPUs.** Request [GPU sandboxes](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md) on serverless or CKS capacity. GPU sandboxes require separate access. Use serverless GPU sandboxes for untrusted code. GPU sandboxes on your own CKS cluster aren't virtualized and should run only trusted code.

## Choose where sandboxes run

CoreWeave operates serverless capacity and sets its policy. Serverless is the default. Follow the [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md) to choose a credential and start running sandboxes.

CKS uses clusters in your organization. Your administrator enables a runner and configures its [sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md). For deployment and scheduling details, see [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), [architecture](https://docs.coreweave.com/products/sandboxes/architecture.md), and [CoreWeave SUNK integration](https://docs.coreweave.com/products/sandboxes/profiles/sunk-integration.md).

## Migrate to `cwsandbox`

If you use the deprecated `wandb.sandbox` module, follow [Migrate from `wandb.sandbox`](https://docs.coreweave.com/products/sandboxes/client#migrate-from-wandbsandbox). The guide explains how to install the standalone Python client, retain your authentication choice, and review wrapper defaults.
