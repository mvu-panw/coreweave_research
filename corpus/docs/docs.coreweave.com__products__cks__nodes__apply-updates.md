# Apply Node Pool updates

Source: https://docs.coreweave.com/products/cks/nodes/apply-updates

# Apply Node Pool updates

> Apply Node Pool updates by queuing a reconfigure reboot

This page describes how to apply Node Pool updates by queuing a reconfigure reboot. Follow this procedure when you need to roll out an updated Node Pool configuration, such as a new system OS image or GPU driver, to existing Nodes in a CoreWeave Kubernetes Service (CKS) cluster.

You can manually reboot Nodes in two ways:

* **Standard Node reboot**: A typical reboot to apply a system update or other change.
* **Reconfigure reboot**: A reboot to apply an updated Node Pool configuration to existing Nodes.

Some Node Pool modifications require you to both reconfigure and reboot the Nodes to apply updates, for example, a new system OS image or GPU driver update. See [Manage Node Pool configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration) for more details.

To apply these updates, you can queue a reconfigure reboot for the necessary Nodes. If you need to reboot Nodes manually to apply a system update or other change, without reconfiguring the Node, see [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md).

A reconfigure reboot is the rollout step for several Node Pool changes. For the end-to-end procedure that surrounds it, see the following:

* [Node Pool image and ncore updates](https://docs.coreweave.com/products/cks/nodes/manage.md): inspect a pending configuration, promote it, batch the rollout, validate, and roll back.
* [Update the GPU driver](https://docs.coreweave.com/products/cks/nodes/gpu-driver-management/update-gpu-driver.md): pin a driver version, roll it out across a Node Pool, and keep live workloads running.

## Prerequisites

Before you begin, ensure you have:

* An active CoreWeave account.
* An [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md).
* The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) installed locally.

## Queue a reconfigure reboot

To queue a reconfigure reboot that waits for active workloads to stop, use the CoreWeave Intelligent CLI with the `--safe` and `--reconfigure` flags. Replace `[NODE-NAMES]` with a space-separated list of the Nodes you want to reboot:

```bash theme={"system"}
cwic node reboot --safe --reconfigure [NODE-NAMES]
```

The `--safe` flag queues the reboot until active workloads stop. CKS requests a cordon to prevent new workload scheduling while existing workloads finish. For more information about idle Nodes and pending reboots, see [Safe versus immediate reboots](https://docs.coreweave.com/products/cks/nodes/reboot.md#safe-versus-immediate-reboots).

The reconfiguration and reboot process can take more than an hour:

* During the reconfiguration and reboot, the Node `PhaseState` condition moves to
  `production-reconfigure-powercycle-test`, and the Node becomes unavailable.
* When the reconfiguration is complete, the Node `PhaseState` condition returns to `production` and the Node is uncordoned.

> [!WARNING]
>
> **Reboot Nodes in small batches**
>
> When you reboot Nodes, limit the number of Nodes you reboot at one time to avoid service interruptions. If you need to reboot 50 or more Nodes at a time, [contact support for assistance](https://docs.coreweave.com/support.md).

Once the reconfigure reboot completes for each Node, the updated Node Pool configuration is applied and the Node returns to service.

### Optional flags

The following sections describe how to skip post-reboot validation or request an immediate reboot.

#### Skip post-reboot validation

To skip validation, add the `--no-test` flag to the reconfigure command. This uses the Node lifecycle state
`production-reconfigure-powerreset`.

By default, a reconfigure reboot includes post-reboot validation. A single validation cycle typically takes about 30 minutes, but retries can extend the total duration.

#### Queue reboot to start immediately

To request an immediate reconfigure reboot without a confirmation prompt, omit `--safe` and use `--force`:

```bash theme={"system"}
cwic node reboot --reconfigure --force [NODE-NAMES]
```

An immediate reboot doesn't wait for active workloads to stop and can interrupt them. Without `--safe` or `--force`, the command also requests an immediate reboot, but prompts you if any selected Nodes are active. For the prompt options, see [Request a Node reboot](https://docs.coreweave.com/products/cks/nodes/reboot.md#request-a-node-reboot).
