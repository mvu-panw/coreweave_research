# What permissions does the agent require in Kubernetes?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/permissions_agent_require_kubernetes

# What permissions does the agent require in Kubernetes?

This page describes the Kubernetes permissions that the W\&B Launch agent requires to run jobs in your cluster. Use this information to configure role-based access control (RBAC) for the agent before you deploy it.

The following Kubernetes manifest creates a Role named `wandb-launch-agent` in the `wandb` namespace. This Role lets the agent create Pods, ConfigMaps, and Secrets, and access Pod logs in the `wandb` namespace. The `wandb-cluster-role` lets the agent create Pods, access Pod logs, create Secrets and Jobs, and check Job status across any specified namespace.
