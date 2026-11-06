# NCCL configuration reference for CoreWeave fabrics

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference

# NCCL configuration reference for CoreWeave fabrics

> Canonical NCCL and UCX environment variables for InfiniBand and RoCE backend fabrics on CoreWeave

This page is the canonical reference for NCCL and UCX environment variables on CoreWeave high-performance backend fabrics. It covers the variables you set for InfiniBand clusters, the variables that differ on RoCE (Spectrum-X) clusters such as GB300, how NCCL chooses a network plugin, and the log lines that look alarming but are normal. Use it as the lookup target when a training or inference job needs fabric-specific tuning.

For the Pod scheduling and Multus configuration that exposes RDMA devices to your containers, see [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md) and [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md). For node placement using fabric labels, see [Read IB and RoCE node labels for placement](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md).

## What this reference is and is not

This page covers fabric-level NCCL and UCX settings: which interfaces NCCL uses, how to select host channel adapters, how NCCL chooses a network plugin, and how the transport differs between InfiniBand and RoCE on CoreWeave.

This page isn't a guide to collective algorithms, topology-aware ranks, or debugging distributed training hangs. Those belong to training documentation. This page also doesn't tune performance baselines or publish expected bandwidth numbers.

## InfiniBand cluster recipe

On InfiniBand clusters, set the following environment variables in your Pod spec or Slurm job. The values match the examples in [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md) and the current reference jobs in the [`nccl-tests` repository](https://github.com/coreweave/nccl-tests). Some older jobs in that repository still point `UCX_NET_DEVICES` at the InfiniBand devices.

The `UCX_NET_DEVICES` and `UCX_TLS` values below keep UCX off the RDMA fabric. Use them unless your stack runs UCX itself and needs UCX on that fabric, such as an MPI build that uses UCX for its own transfers. In that case, point `UCX_NET_DEVICES` at the InfiniBand devices and set `UCX_TLS` to the RDMA transports your stack needs instead of `tcp`. The transports that work depend on your stack and fabric, so confirm the values with a benchmark before you rely on them.

```bash theme={"system"}
# Front-end interface for NCCL control and out-of-band traffic.
# Safe to set; selects the primary Pod interface, not the RDMA path.
export NCCL_SOCKET_IFNAME=eth0

# InfiniBand host channel adapters NCCL uses for GPUDirect RDMA collectives.
# "ibp" matches the InfiniBand device naming on CoreWeave IB clusters.
export NCCL_IB_HCA=ibp

# Leave NCCL_NET_PLUGIN unset so NCCL loads the HPC-X network plugin, the
# recommended default on InfiniBand. Set it to "none" instead only if you
# have a measured reason to use the built-in transport. Every rank must
# match. See "NCCL network plugin guidance".

# UCX devices and transports. NCCL doesn't use UCX; these values keep UCX off
# the InfiniBand devices so it doesn't initialize a transport this job doesn't
# need. Stacks that run UCX themselves need different values. See the table below.
export UCX_NET_DEVICES=eth0
export UCX_TLS=tcp
```

| Variable | Purpose |
| - | - |
| `NCCL_SOCKET_IFNAME` | Selects the front-end interface for NCCL's TCP control and bootstrap traffic. Set to the primary Pod interface, usually `eth0`. |
| `NCCL_IB_HCA` | Selects the RDMA host channel adapters for collectives. Use `ibp` on CoreWeave InfiniBand clusters. |
| `NCCL_NET_PLUGIN` | Selects the NCCL network plugin. Leave unset to load the HPC-X network plugin, the recommended default. Set to `none` only if you have a measured reason to use the built-in InfiniBand verbs transport instead. Every rank in a job must use the same value. |
| `UCX_NET_DEVICES` | Devices UCX uses. Set to `eth0` to keep UCX off the InfiniBand devices. If your stack runs UCX over RDMA, point this at the InfiniBand devices instead. |
| `UCX_TLS` | Transports UCX is allowed to use. Set to `tcp` to keep UCX off the InfiniBand devices. If your stack runs UCX over RDMA, set the RDMA transports it needs instead. Leaving this unset lets UCX try every transport. |

## RoCE (Spectrum-X) cluster recipe

RoCE clusters such as GB300 use Ethernet-based RDMA. Several NCCL variables differ from InfiniBand because the address family is IPv6 and the traffic class is set explicitly. For interface attachment through Multus NADs and Pod configuration, see [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md).

`NCCL_IB_HCA` selects RDMA verbs devices. It doesn't select the Linux network interfaces that Multus creates, such as `net1` and `net2`. From inside the workload container, list the available RDMA devices:

```bash theme={"system"}
ibv_devices
```

The GB300 RoCE examples use `ibp` as a device-name prefix. Confirm that it matches the intended backend devices in the command output. If your cluster uses different names, set `NCCL_IB_HCA` to a matching prefix or a comma-separated list of RDMA device names. For selection syntax, see [`NCCL_IB_HCA` in the NVIDIA documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-ib-hca).

```bash theme={"system"}
# Front-end interface for control traffic, same as InfiniBand.
export NCCL_SOCKET_IFNAME=eth0

# GB300 RoCE RDMA device-name prefix. Confirm it against ibv_devices.
export NCCL_IB_HCA=ibp

# RoCE uses an IPv6 address family for RDMA, unlike InfiniBand.
export NCCL_IB_ADDR_FAMILY=AF_INET6

# Traffic class for RoCE. 96 is the value validated on GB300 RoCE.
export NCCL_IB_TC=96

# Load the Spectrum-X network plugin, which needs HPC-X 2.50 or newer.
# Leave NCCL_NET_PLUGIN unset so NCCL finds the plugin.
# Every rank must match. See "NCCL network plugin guidance".
unset NCCL_NET_PLUGIN
export LD_LIBRARY_PATH="/opt/hpcx/nccl_spectrum-x_plugin/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

### Variables that differ from InfiniBand

| Variable | InfiniBand | RoCE (Spectrum-X) |
| - | - | - |
| `NCCL_IB_ADDR_FAMILY` | Not required | `AF_INET6` (RoCE addressing on CoreWeave is IPv6) |
| `NCCL_IB_TC` | Not required | Set the RoCE traffic class, for example `96` on GB300 |
| `NCCL_NET_PLUGIN` | Leave unset for typical jobs to load the HPC-X plugin | Leave unset so NCCL loads the Spectrum-X plugin |
| `LD_LIBRARY_PATH` | No change needed | Prepend `/opt/hpcx/nccl_spectrum-x_plugin/lib` so NCCL finds the plugin |
| Interface attachment | Devices exposed directly | Attached through Multus NADs (see RoCE guide) |

For plugin selection and SHARP requirements, see [NCCL network plugin guidance](#nccl-network-plugin-guidance).

## NCCL network plugin guidance

`NCCL_NET_PLUGIN` selects the network plugin NCCL uses for communication between Nodes. A network plugin replaces NCCL's built-in transport, so every rank in a job must agree on the setting. The following sections describe how NCCL chooses a plugin, what the InfiniBand and RoCE plugins provide, and how to decide whether to use the InfiniBand plugin.

### How NCCL chooses a network plugin

When `NCCL_NET_PLUGIN` is unset, NCCL searches the library path for `libnccl-net.so` and uses that plugin if it finds one. NCCL falls back to its built-in transport when it finds no plugin it can use. Setting `NCCL_NET_PLUGIN=none` skips the search and forces the built-in transport.

Many CoreWeave compute environments include NVIDIA HPC-X, which installs the `nccl-rdma-sharp-plugins` build of `libnccl-net.so`. CoreWeave SUNK compute container images and the images built from the `nccl-tests` repository both bundle it. Where HPC-X is on the library path, NCCL loads the plugin unless you set `NCCL_NET_PLUGIN=none`. This is why the reference jobs in that repository set the variable explicitly instead of relying on a default.

Because the plugin ships in the container image rather than on the Node, whether a rank loads it depends on the image that rank runs.

### What the InfiniBand network plugin provides

The `nccl-rdma-sharp-plugins` network plugin is NVIDIA's plugin as bundled with HPC-X. It isn't a CoreWeave fork, and CoreWeave applies no source patches to it. The plugin replaces NCCL's built-in transport between Nodes and can also use CollNet and SHARP for the collectives that support them. NCCL's built-in InfiniBand verbs transport, which `NCCL_NET_PLUGIN=none` selects, has no SHARP path.

Loading the plugin doesn't enable SHARP on its own. `NCCL_COLLNET_ENABLE` defaults to `0`, and CoreWeave doesn't enable SHARP on its fabrics by default, so jobs fall back to point-to-point collectives. Loading the plugin and setting `NCCL_COLLNET_ENABLE=1` still aren't sufficient. SHARP also has to be enabled on the fabric itself, which CoreWeave does for you. To find out whether SHARP is enabled on your cluster, or to ask for it, contact your CoreWeave representative.

The `No Aggregation Manager sharp_am detected` line reports that fallback on InfiniBand as well as RoCE. For more information, see [Log lines that look alarming but are normal](#log-lines-that-look-alarming-but-are-normal).

Plugin versions differ between images, and the network plugin API version the plugin exposes must match what your NCCL build expects. A plugin your NCCL build can't use isn't a startup failure. NCCL logs that the external network plugin is unsupported, unloads it, and falls back to its built-in transport. A rank that falls back this way while other ranks keep the plugin creates the mixed configuration described in [Every rank must load the same network plugin](#every-rank-must-load-the-same-network-plugin). Instead of assuming a single fleet-wide version, check your container image tag to find the version your job uses.

### Every rank must load the same network plugin

Every rank in a job must load the same network plugin. The plugin transport and NCCL's built-in transport don't interoperate, so you can't run some ranks on one and some ranks on the other.

> [!WARNING]
>
> A mixed configuration, where some ranks use a plugin transport and other ranks use NCCL's built-in transport, isn't supported. It can cause faults during collectives, including memory faults during `broadcast`.

Two configurations are uniform, and either one is supported:

* Run every rank from the same container image and leave `NCCL_NET_PLUGIN` unset. All ranks load the same plugin from that image. This is the recommended default on InfiniBand.
* Set `NCCL_NET_PLUGIN=none` on every rank. All ranks use the built-in InfiniBand verbs transport instead. Use this only if you have a measured reason to avoid the plugin.

A common cause of a mixed configuration is that different ranks run different container images in one job. Building your own image on top of a CoreWeave base image can also change whether HPC-X is on the library path, for example when the new image replaces `LD_LIBRARY_PATH` instead of appending to it. A rank that used to load the plugin might stop loading it.

To confirm that ranks agree, set `NCCL_DEBUG=INFO` and compare the `Using network` line across ranks. Every rank must report the same network name. The `NET/Plugin` lines in the same output show which plugin libraries each rank searched for, and report the ones it couldn't find.

### Decide whether to use the InfiniBand plugin

Leave `NCCL_NET_PLUGIN` unset on InfiniBand so NCCL loads the HPC-X plugin. This is the recommended default, not just a SHARP prerequisite.

Set `NCCL_NET_PLUGIN=none` instead only if you have a measured reason to use the built-in transport for your workload. If you want to compare, measure with the paired reference jobs in the [`nccl-tests` repository](https://github.com/coreweave/nccl-tests). Those paired jobs differ as follows:

* The standard jobs set `NCCL_NET_PLUGIN=none` and use the built-in transport.
* The SHARP variants, whose filenames end in `-sharp`, leave the plugin loaded and set `NCCL_COLLNET_ENABLE=1` and `SHARP_COLL_ENABLE_PCI_RELAXED_ORDERING=1`.

Compare a pair while keeping the image, Nodes, placement, message sizes, and iteration count identical.

### The RoCE Spectrum-X plugin

The NVIDIA Spectrum-X NCCL plugin provides NIC-level hardware-accelerated collectives. Use it on RoCE clusters for jobs of any size. The plugin requires HPC-X 2.50 or newer, and CoreWeave images that bundle HPC-X ship it at `/opt/hpcx/nccl_spectrum-x_plugin`.

To load this plugin, prepend `/opt/hpcx/nccl_spectrum-x_plugin/lib` to `LD_LIBRARY_PATH` and leave `NCCL_NET_PLUGIN` unset, as shown in the RoCE cluster recipe on this page. As on InfiniBand, every rank in a job must load the same network plugin.

If your image ships an HPC-X version older than 2.50, upgrade the image or contact your CoreWeave representative. SHARP is an InfiniBand-only technology and isn't available on RoCE fabrics.

## NCCL\_IB\_RETRY\_CNT has a hard maximum of 7

`NCCL_IB_RETRY_CNT` is stored in a 3-bit register, so its maximum valid value is 7. Setting it to 8 or higher doesn't increase retries: the value wraps and is effectively treated as a small or zero count, which makes the fabric appear far less reliable than it is. If you want more retry tolerance, 7 is the ceiling. Don't set it above 7.

## Segment-size and channel knobs

Most workloads don't need to tune these. Change them only when you have a measured reason to, and change one at a time so you can attribute the effect.

| Variable | What it controls | When to consider changing it |
| - | - | - |
| `NCCL_BUFFSIZE` | Size of the per-connection staging buffer | Large-message collectives where the default underfills the link |
| `NCCL_MIN_NCHANNELS` / `NCCL_MAX_NCHANNELS` | Lower and upper bounds on the number of parallel channels (CUDA blocks) NCCL uses | Raise the minimum when throughput plateaus below the link rate on large messages; lower the maximum when NCCL consumes too many SMs |
| `NCCL_P2P_NET_CHUNKSIZE` | Chunk size for point-to-point network transfers, which back collectives like `all_to_all` | Lower it for small-message latency; raise it for large-message point-to-point bandwidth (CoreWeave GB300 RoCE baselines use `524288`) |

Tuning these without a baseline measurement usually makes performance worse, not better. Capture a baseline first, change one knob, re-measure, and keep the change only if it helps.

## UCX coexistence and GPUDirect RDMA

NCCL and UCX use different RDMA data paths, so a Node where NCCL tests pass doesn't guarantee that UCX-based workloads (NIXL, MPI) work. The UCX transport settings, the `rdma-core` version requirement for GB300 RoCE, and the UCX diagnostics live in [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md#ucx-and-gpudirect-rdma-on-gb300-roce).

For MPI workloads (for example, Intel MPI or Ansys), the relevant variables differ from NCCL. A common configuration is:

```bash theme={"system"}
# MPI fabric selection for shared memory plus OpenFabrics interfaces.
export I_MPI_FABRICS=shm:ofi

# OpenFabrics provider for NVIDIA fabrics.
export FI_PROVIDER=mlx
```

## Log lines that look alarming but are normal

When you enable `NCCL_DEBUG=INFO`, you see verbose output. The following messages don't indicate a failure:

* `No Aggregation Manager sharp_am detected`. This means SHARP isn't available, so NCCL falls back to point-to-point collectives. SHARP is an InfiniBand-only switch-side reduction technology and isn't available on RoCE (Spectrum-X) fabrics. On a RoCE cluster, this fallback is expected and not an error.
* Transport fallback notices during initialization. NCCL probes available transports and reports the ones it selects. These are informational.

## Enable debug logging

To diagnose RDMA or transport issues, increase NCCL verbosity. Debug logging increases log volume, so disable it after you finish.

```bash theme={"system"}
# Verbose NCCL logging. Increases log size; remove after debugging.
export NCCL_DEBUG=INFO

# Optional: restrict verbose output to the network subsystem.
export NCCL_DEBUG_SUBSYS=NET
```

For the full list of NCCL variables, see [`NCCL_DEBUG` in the NVIDIA NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-debug).

## When NCCL reports a vendor error

NCCL sometimes reports a vendor error code from the underlying RDMA stack. For what the individual codes mean, including the difference between `vendor err 249` and `vendor err 129`, see [What do NCCL errors mean?](https://docs.coreweave.com/support/sunk/articles/what-do-nccl-errors-mean#vendor-err-249-compared-to-vendor-err-129). Use the onset pattern to distinguish a fabric fault from a configuration problem. A sudden, multi-Node onset points to a fabric-level event. A consistent failure on a single Pod points to a container or configuration problem such as a UCX or `rdma-core` mismatch. For the RoCE diagnostics and the link-health check, see [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md#ucx-and-gpudirect-rdma-on-gb300-roce) and [Read IB and RoCE node labels for placement](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md).

## Related pages

* [Use GPUDirect RDMA with InfiniBand](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma.md): Pod scheduling and NCCL setup for IB.
* [Use GPUDirect RDMA with RoCE](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma-roce.md): Multus attachment, UCX requirements, and NCCL setup for RoCE.
* [Read IB and RoCE node labels for placement](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md): topology-aware placement and link-health checks.
* [About CoreWeave HPC interconnects](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md): fabric overview.
