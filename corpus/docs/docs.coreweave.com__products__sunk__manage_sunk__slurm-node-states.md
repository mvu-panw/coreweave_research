# Monitor Slurm node states

Source: https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states

# Monitor Slurm node states

> Learn about the different states a Slurm node can be in, and how to check the state of a node.

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Monitoring node and job states is a key component of workload management. CoreWeave runs regular [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) tests on idle nodes in a cluster, but monitoring the health of your own cluster can help with early detection of issues that could result in failed jobs and underutilized hardware.

You have several options for monitoring Slurm node states. CoreWeave's [Slurm Cluster Grafana dashboard](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-cluster.md#cluster-nodes) is a graphical option that includes time-series graphs that track nodes by state. Slurm also has built-in monitoring tools, `sinfo` and `scontrol`, which you can run directly in the Slurm login node shell and [customize to provide your desired output](#see-an-overview-of-node-states-with-sinfo).

## Slurm node states versus job states

Slurm node states describe the availability and health of the compute hardware in the cluster, while [Slurm job states](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-cluster.md#slurm-jobs-running-jobs) track the lifecycle of a specific workload initiated by a user in the cluster.

The state of a Slurm node indicates whether the node is healthy and available to run workloads. For example, an `IDLE` Slurm node is healthy and available to run a Slurm job. An `ALLOCATED` Slurm node is healthy, but is already in use and isn't currently available for additional workloads. In contrast, a [Slurm node in the `DOWN` or `DRAINED` state](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes) isn't available for new jobs, possibly due to an issue that a [Node Health Check](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#node-health-check-nhc-drains) found after a job.

Slurm node states can provide context about Slurm job states. When a workload is working as expected, the Slurm node may be in the `ALLOCATED` state while the Slurm job on that node is `RUNNING`. If a Slurm job is stuck in the `PENDING` state, checking the node state may reveal that the job is on a `DOWN` node.

## Read a SUNK Slurm hostname

A SUNK Slurm hostname encodes the node's network address, not its physical location. Knowing how to read one keeps you from misidentifying a node when you investigate its state or report a problem with it.

A SUNK Slurm hostname is a prefix followed by two numbers:

```text theme={"system"}
[PREFIX]-[OCTET-3]-[OCTET-4]
```

SUNK takes `[PREFIX]` from the NodeSet, so it varies by cluster. CoreWeave clusters typically encode the region, environment, and GPU model in it, as in `slurm-eus-04a-prod-b200`.

The two trailing numbers are the third and fourth octets of the node's IP address, each zero-padded to three digits. They identify the node on the network, not its physical location. For example, in `slurm-eus-04a-prod-b200-192-103`, the trailing `192` and `103` are the last two octets of the node IP `10.104.192.103`, and a node at `10.104.12.2` ends in `012-002`.

When you report a hardware issue, don't read the trailing numbers as a rack number. To find the physical rack, read the `topology.kubernetes.io/zone` label on the Kubernetes Node that hosts the Slurm node's Pod.

## Slurm node states

The following table contains a complete list of possible Slurm node states:

| State | Meaning |
| - | - |
| `IDLE` | The node is available for use and does not currently have any jobs allocated to it. |
| `MIXED` or `mix` | Some of the node's CPUs are `ALLOCATED` and others are `IDLE`. Or the node has a suspended job allocated to some of its TRES (memory). |
| `ALLOCATED` or `alloc` | The node is allocated to one or more Slurm jobs. |
| `COMPLETING` | All jobs on the node have finished, but the node is still in use. In this state, the node is likely running an Epilog script. |
| `DRAINING` or `drng` | The node is in the process of being drained. Existing jobs run until completion, but no new jobs start on this node. |
| `DRAINED` or `drain` | The node has been removed from the available compute pool. No new jobs start on this node. |
| `DOWN` | The node is offline and unavailable for job scheduling. Jobs on the node may be requeued or canceled. The scheduler doesn't send any new jobs to this node. |
| `BLOCKED` | [Topology-aware scheduling](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md) attempts to place a job within a single block to optimize performance. When a job occupies a block, Slurm places any unallocated nodes in that block in the `BLOCKED` state, which prevents new jobs from being scheduled on them. This ensures that the entire block remains available for the current job, which may eventually require the unallocated resources, preventing potential resource fragmentation. This state only applies when using topology-aware scheduling, such as the `--exclusive=topo` flag. |
| `RESERVED` or `resv` | A user with the appropriate permissions has reserved this node in advance, for a defined time. Jobs cannot be scheduled on this node, even if it's currently idle. Jobs that require the reservation must be submitted with the `--reservation` flag and the name of the reservation. |
| `UNKNOWN` | The Slurm controller has just started and the node's state hasn't yet been determined. |
| `FAIL` | The node is unavailable. Slurm doesn't schedule new jobs, and terminates any job that was running on the node when it failed. |
| `FAILING` | The node is in the process of being made unavailable. Jobs currently running on the node run until completion, but no new jobs start on the node. |
| `FUTURE` | Slurm makes the node available, but it isn't yet ready to accept jobs. |
| `INVAL` | The node's configuration is invalid or inconsistent with the Slurm controller. Inconsistencies may exist between the `slurm.conf` file and the `slurmd` daemon running on the compute node. `scontrol show node` reports this state as the `INVALID_REG` flag in the `State` field. For troubleshooting information, see [nodes in the `INVAL` state](https://docs.coreweave.com/products/sunk/manage_sunk/inval-node-state). |
| `MAINT` | The node has been designated for planned maintenance and isn't currently available for job scheduling. |
| `REBOOT_REQUESTED` | An administrator has scheduled the node for a planned reboot. Any jobs currently running on this node continue to run until completion. |
| `REBOOT_ISSUED` | The node is actively in the process of shutting down and restarting. Once the node comes back online and its `slurmd` daemon successfully registers with `slurmctld`, Slurm automatically clears this flag, and the node returns to its normal state. |
| `PLANNED` | The node is planned by the backfill scheduler for a higher priority job. |
| `PERFCTRS (NPC)` | Network Performance Counters associated with this node are in use, rendering this node as not usable for any other jobs. |
| `POWER_DOWN` | An administrator has flagged the node to power down. |
| `POWERING_DOWN` | The node is in the process of powering down and isn't available for job scheduling. |
| `POWERED_DOWN` | The node is currently powered down and isn't capable of running any jobs. |
| `POWERING_UP` | The node is in the process of being powered up. |

Node state names may differ across Slurm versions. Refer to [SchedMD's Slurm documentation](https://slurm.schedmd.com/sinfo.html) for more information.

### Node state flags

Node states may also include *flags*, indicated by a special character appended to the state. For example, an asterisk `*` appended to any of the preceding states indicates that the node isn't responding.

| Flag | Meaning |
| - | - |
| `*` | The node isn't responding. Slurm doesn't allocate new work to this node. If the node remains unresponsive, it transitions to a `DOWN` state. |
| `$` | The node is currently in a reservation with a flag value of `maintenance`. |
| `-` | The node is planned for a higher priority job by the backfill scheduler. |
| `!` | The node is pending power down. |
| `%` | The node is in the process of powering down. |
| `~` | The node is powered off. |
| `#` | The node is in the process of powering up or is being configured. |
| `@` | The node is pending reboot. |
| `^` | The node reboot was issued. |

> [!NOTE]
>
> Nodes in a `drain*` or `down*` state have been removed from the cluster and you can ignore them. You may see this suffix if you checked the state while the pod wasn't yet fully connected.

## Check the state of a Slurm node

You can check the state of a Slurm node in multiple ways. The `scontrol` command provides a detailed view of node states, while `sinfo` provides a simple overview. Regardless of method used, you must connect to the Slurm login node and run all Slurm commands from the Slurm login node shell.

### Connect to the Slurm login node

To check node states with `scontrol` or `sinfo`, first [connect to the Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md#connect-through-ssh).

After connecting to the Slurm login node, you can use the following `scontrol` and `sinfo` commands to examine node states.

> [!TIP]
>
> Run all Slurm commands, including `scontrol` and `sinfo`, from within the Slurm login node shell.

## View detailed node states with `scontrol`

The `scontrol` command provides a detailed view of the node states.

```bash theme={"system"}
scontrol show node [NODE-NAME]
```

Replace `[NODE-NAME]` with the name of the node you want to check, or remove the `[NODE-NAME]` entirely to list all nodes.

### Command aliases for node monitoring

The SUNK login node image includes the following aliases and shell functions. They are available in every login node shell session by default.

| Alias | Description |
| - | - |
| `drain [NODE-NAME] [REASON]` | Drains a node with a reason, automatically prefixed with your username. |
| `undrain [NODE-NAME]` | Undrains (resumes) a single node. |
| `sn` | Shows detailed node information. Runs `scontrol show node`. |
| `dl` | Lists all nodes in the `drain` and `idle` states, with reasons. |
| `dld` | Lists all nodes in the `drain` state, with reasons, including nodes that are actively draining with running jobs. |
| `downl` | Lists all nodes in the `down` state, with reasons. |

The `dl` alias is equivalent to the following command:

```bash theme={"system"}
sinfo -t "drain&idle" -NO "NodeList:45,Comment:10,Timestamp:25,Reason:130" | uniq
```

The plain Slurm command `sinfo -R` isn't an alias, but it works on any Slurm cluster. It lists every node in the `down`, `drained`, `draining`, `fail`, or `failing` state with its reason:

```bash theme={"system"}
sinfo -R
```

## See an overview of node states with `sinfo`

`sinfo` reports the state of partitions and nodes managed by Slurm and provides filtering, sorting, and formatting options.

```bash theme={"system"}
sinfo
```

This command provides the following information:

| Field | Description |
| - | - |
| `PARTITION` | The name of the partition the node belongs to. |
| `AVAIL` | State of the partition. |
| `TIMELIMIT` | The maximum time limit for user jobs in `days-hours:minutes:seconds` format. |
| `NODES` | The number of nodes in the partition. |
| `STATE` | The state of the node. |
| `NODELIST` | The names of the nodes in this partition. |

Use the `--help` flag to view the help menu for the `sinfo` command.

> [!WARNING]
>
> `sinfo` sends a remote procedure call to `slurmctld`. Too many calls to the `slurmctld` daemon can lead to performance loss, and possibly result in a denial of service. Avoid calling `sinfo` in loops within shell scripts or other programs.

### Customize the output format of `sinfo`

By default, `sinfo` groups nodes with a common configuration into a single line. The configuration includes partition, state, CPU count, and amount of memory. You can change this behavior using format specifiers.

Slurm supports two options for customizing the output format of `sinfo`: `--format` and `--Format`. The syntax and capabilities of these options are different. This guide focuses on the `--format` option, as it provides greater flexibility and more granular control over the output format.

### Output format options

The syntax for `--format` is a `printf`-style format string. Enclose all format and type specifiers in double quotes `"`, and attach them to the `--format` flag with an `=` sign, as shown in the following example:

```bash theme={"system"}
sinfo --format="%[.][SIZE][TYPE][SUFFIX]"
```

See the following table for descriptions of each element of the preceding format string:

| Format specifier | Description |
| - | - |
| `%` | Indicates the start of a format specifier. |
| `.` | Place a period before the `[SIZE]` to specify right-justification (`%.10P`). Omit the period for the default, left-justified output. (`%10P`). |
| `[SIZE]` | The number specified is the minimum field width. If the actual text is shorter than the specified width, Slurm pads the field with spaces to meet this width. If the text is longer, the field expands to fit it. |
| `[TYPE]` | The field type specifier that determines which piece of node information to display, such as `P` for partition name or `T` for node state. See [Complete list of type specifiers](#complete-list-of-type-specifiers). |
| `[SUFFIX]` | Specifies a string to append to the field. |

Additional format options are detailed in the following table:

| Flag | Description |
| - | - |
| `--format` or `-o` | Full customization of the output format. Lets you specify a custom output format string to display specified fields in a specified order. |
| `--exact` or `-e` | Prevents node grouping unless the nodes are identical in every configuration aspect. Lists each node on a separate line, even if they're in the same partition or state. |
| `--Node` or `-N` | Node-oriented output. Displays one line per node instead of one line per partition. This prevents all grouping and provides a granular view of every node in the cluster, each on its own line. |
| `--states` or `-t` | Lists only nodes with the specified states, using the [Slurm node state names](#slurm-node-states). To view multiple states, use a comma-separated list. |
| `--partition` or `-p` | Specifies the partition to display information for. |
| `--noheader` or `-h` | Omits the header from the output. |
| `--help` | Displays the help menu for the `sinfo` command. |

### Format string syntax example

Here's an example of how to use the `--format` flag to customize the output format of `sinfo`:

```bash Group output by node state theme={"system"}
sinfo --format="%10P %20N %10T"
```

The format string in the preceding command uses the following specifiers:

* `%10P` - The partition name, with a width of 10 characters.
* `%20N` - The node list, with a width of 20 characters.
* `%10T` - The state of the node, in extended format, with a width of 10 characters.

### Complete list of type specifiers

Use field type specifiers to indicate the information you want to display.

Combine field type characters with format specifier flags to customize the output format.

Many type specifiers are available to use in the format string. Type specifiers are case-sensitive.

> [accordion] Type specifiers
>
> | Type specifier | Description |
> | - | - |
> | `%all` | Displays all fields. |
> | `%a` | State/availability of a partition. |
> | `%A` | Number of nodes by state in the format `allocated/idle`. Don't use this with a node state option (`%t` or `%T`), or Slurm places the different node states on separate lines. |
> | `%b` | Features currently active on the nodes. See also `%f`. |
> | `%B` | The max number of CPUs per node available to jobs in the partition. |
> | `%c` | The number of CPUs per node. |
> | `%C` | Number of CPUs by state in the format `allocated/idle/other/total`. Don't use this with a node state option (`%t` or `%T`), or Slurm places the different node states on separate lines. |
> | `%d` | Size of temporary disk space per node, in megabytes. |
> | `%D` | Number of nodes. |
> | `%e` | Total memory, in MB, currently free on the node as reported by the operating system. This value is for informational use only and is not used for scheduling. |
> | `%E` | The reason a node is unavailable. `down`, `drained`, or `draining` states. |
> | `%f` | Features currently active on the nodes. See also `%b`. |
> | `%g` | Groups that may use the nodes. |
> | `%G` | Generic resources associated with the nodes. |
> | `%h` | Print the OverSubscribe setting for the partition. |
> | `%H` | Print the timestamp of the reason a node is unavailable. |
> | `%i` | Print the name of a reservation for a node in advanced reservation. |
> | `%I` | Partition job priority weighting factor. |
> | `%l` | Maximum time for any job in the format `days-hours:minutes:seconds`. |
> | `%L` | Default time for any job in the format `days-hours:minutes:seconds`. |
> | `%m` | Size of memory per node, in megabytes. |
> | `%M` | PreemptionMode. |
> | `%n` | List of node hostnames. |
> | `%N` | List of node names. |
> | `%o` | List of node communication addresses. |
> | `%O` | CPU load of a node, as reported by the operating system. |
> | `%p` | Partition scheduling tier priority. |
> | `%P` | Partition name, followed by `*` for the default partition. See also `%R`. |
> | `%r` | Only user root may initiate jobs, `yes` or `no`. |
> | `%R` | Partition name. See also `%P`. |
> | `%s` | Maximum job size, in nodes. |
> | `%S` | Allowed allocating nodes. |
> | `%t` | State of nodes, in compact format. |
> | `%T` | State of nodes, in extended format. |
> | `%u` | Print the name of the user who set the reason a node is unavailable. |
> | `%U` | Print the name and UID of the user who set the reason a node is unavailable. |
> | `%v` | Print the version of the current `slurmd` daemon. |
> | `%V` | Print the cluster name if running in a federation. |
> | `%w` | Scheduling weight of the nodes. |
> | `%X` | Number of sockets per node. |
> | `%Y` | Number of cores per socket. |
> | `%z` | Extended processor information: number of sockets, cores, threads per node. |
> | `%Z` | Number of threads per core. |
