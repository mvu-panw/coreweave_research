# Address nodes in the INVAL state

Source: https://docs.coreweave.com/products/sunk/manage_sunk/inval-node-state

# Address nodes in the INVAL state

> Troubleshoot Slurm nodes in the INVAL state caused by configuration mismatches between slurm.conf and slurmd

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

When [checking the state of a Slurm node](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md), you might encounter nodes in the `INVAL` state. This page describes what causes the `INVAL` state and how to resolve it.

The `INVAL` state often indicates a mismatch between the `slurm.conf` file and the `slurmd` daemon running on the Compute node. This mismatch can occur for several reasons:

* **Resource mismatch:** The `slurm.conf` file might declare that a certain number of CPUs, memory, or GPUs are available, but when the `slurmd` on that node starts, it reports a different number of these resources. For example, the `slurm.conf` file declares `RealMemory=128000` (128 GB), but the node's `slurmd` reports only `RealMemory=96000` (96 GB) after checking the system. This can happen because other processes on the node are using memory. The `slurm.conf` file might also have been updated to reflect a change in CPUs or memory, but the `slurmd` daemon hasn't been restarted to apply the change.
* **Hardware feature mismatch:** If the `slurm.conf` file specifies a hardware feature, such as `Features=gpu`, but the node's `slurmd` can't detect that feature, the node enters the `INVAL` state.
* **Networking and hostname issues:** Problems with a node's hostname, IP address, or network connectivity can cause the `slurmctld` to receive invalid or incomplete registration information from `slurmd`, resulting in the `INVAL` state.

## Troubleshoot an `INVAL` node

To troubleshoot an `INVAL` node, first examine the `slurmctld` logs on the controller node and the `slurmd` logs on the Compute node. These logs often contain explicit error messages detailing why the node's configuration is invalid.

For a detailed report of the node's configuration, run the `slurmd -C` command on the Compute node:

```bash theme={"system"}
slurmd -C
```

Compare this output with the node's entry in your `slurm.conf` file. If the configurations differ, update the `slurm.conf` file to match the `slurmd` configuration.

After you make changes, restart the `slurmctld` on the controller node and the `slurmd` daemon on the Compute node so they re-register with the correct information.

For detailed instructions, see [Restart the Slurm Controller](https://docs.coreweave.com/products/sunk/manage_sunk/interact-with-kubernetes.md#restart-the-slurm-controller) and [Restart the Slurm daemon](https://docs.coreweave.com/products/sunk/manage_sunk/interact-with-kubernetes.md#restart-the-slurm-daemon).

> [!WARNING]
>
> **Restart required**
>
> You must restart the `slurmctld` and `slurmd` for changes made to the `slurm.conf` file to take effect.
