# Run jobs on Grace CPU instances

Source: https://docs.coreweave.com/products/sunk/run_workloads/run-jobs-on-grace-cpu

# Run jobs on Grace CPU instances

> Run SUNK jobs on Arm-based Grace CPU instances (GB200, GB300, GH200), including page-size and binary compatibility

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page explains how to run SUNK jobs on CoreWeave's Grace CPU instances and how to avoid the binary compatibility problems that come from their Arm architecture and 64 KiB memory page size. The material on this page applies to jobs running on GB200, GB300, or GH200 instances.

CoreWeave's [GB200](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md), [GB300](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md), and [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) instances pair NVIDIA GPUs with the NVIDIA Grace CPU. The Grace CPU is an Arm v9 (aarch64) processor, not x86\_64. Most failures on these instances trace back to two architecture differences: the CPU is Arm, and it uses a larger memory page size than x86\_64.

## Target Grace nodes in a job

SUNK adds each NodeSet's name to its nodes as a Slurm feature and, by default, creates a partition with the same name for each NodeSet. It doesn't add a CPU architecture feature, so there's no built-in `aarch64` constraint. Steer a job to Grace nodes with the partition or the feature of the NodeSet that holds them:

```bash theme={"system"}
#SBATCH --partition=[GRACE-NODESET]
```

To select by feature instead, use `#SBATCH --constraint=[GRACE-NODESET]`. To list partitions, their nodes, and the features on those nodes:

```bash theme={"system"}
# Show each partition's nodes and their Slurm features.
sinfo -o "%P %N %f"
```

On SUNK Standard, administrators can add their own features, such as `aarch64`, with `staticFeatures` on the NodeSet. See [Node-specific options](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md#node-specific-options).

## Symptoms

A job that runs fine on x86\_64 instances fails on a GB200, GB300, or GH200 instance with an `Illegal instruction` crash (SIGILL), a segmentation fault, an out-of-memory error that doesn't match the node's actual free memory, an "exec format error," or inconsistent crashes in a prebuilt binary or Python wheel. These symptoms often look like memory or hardware problems but are usually architecture or page-size incompatibility.

## Confirm the architecture and page size

Run these read-only checks inside a job on the instance to see what you're running on:

```bash theme={"system"}
# Print the CPU architecture. Grace reports aarch64.
uname -m

# Print the memory page size in bytes. Grace reports 65536.
getconf PAGESIZE
```

`uname -m` returns `aarch64` on Grace instances and `x86_64` on Intel or AMD instances.

The Grace CPU uses 64 KiB memory pages, so `getconf PAGESIZE` returns `65536`. That's larger than the 4 KiB page size standard on x86\_64 and on most other Arm systems, where most aarch64 Linux distributions, including Ubuntu and Debian, build their packages for 4 KiB pages. RHEL and Rocky Linux ship 64 KiB kernels. Software that was compiled assuming 4 KiB pages can behave incorrectly when it runs on a larger page size.

## Why prebuilt binaries fail on Grace

Two distinct compatibility problems cause most Grace failures:

* **Architecture mismatch.** A binary compiled for x86\_64 can't run on aarch64. If the top-level executable is x86\_64, you get an "exec format error." A Python package that ships x86\_64 `.so` extensions fails at import with a "cannot open shared object file" error. When native code compiled for another CPU actually runs, the process crashes with `Illegal instruction` (SIGILL, often shown as exit code -4). Documented triggers are DeepSpeed or Triton JIT kernel caches shared across architectures on network storage, checkpoints saved on x86\_64 nodes that embed compiled ops, and, on GB200 and GH200, dataloader workers using numpy or BLAS builds suspected of carrying x86 SIMD code. You must use aarch64 builds, and keep JIT caches and checkpoints separate per architecture.

* **Page-size assumptions.** A binary or library that's built for aarch64 but compiled with a hardcoded 4 KiB page-size assumption can segfault, report misleading out-of-memory errors, or behave inconsistently even though it's the right architecture. The crash looks like a memory bug but is a page-size bug.

The following are common sources of page-size-sensitive binaries:

* Runtimes with custom memory allocators, such as Node.js or other V8-based tools, which fail with out-of-memory errors that don't match the node's free memory, for example `Fatal process OOM in insufficient memory to create an Isolate`.
* Software linked against a `jemalloc` build that fixed a 4 KiB page size at build time. `jemalloc` detects the page size when it's configured, so a build from a 4 KiB host fails to start on Grace with `<jemalloc>: Unsupported system page size`.
* Container images built on a 4 KiB aarch64 host, such as most Ubuntu or Debian machines, when a build step bakes in the host's page size the way `jemalloc` does.

## Mitigations

Use the following approaches, in roughly this order of preference:

* **Build on Grace.** Compile your software, install Python wheels, or build container images on an aarch64 environment that matches the Grace page size. Building on a Grace login Pod or compute node produces binaries that match the target. The simplest option on any SUNK cluster is an interactive job on a Grace compute node, such as `srun --partition=[GRACE-NODESET] --pty bash`. On SUNK Standard, you can also pin login Pods to Grace nodes with [`login.common.pod.affinity`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#login--common--pod--affinity) so they serve as a persistent aarch64 build environment. On SUNK 7.x, the same setting is `login.nodeSelector.affinity`, and login Pods are managed as described in [Configure individual login Pods](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login.md). SUNK Self-Service clusters configure login Pods on the `SunkCluster` resource, which has no affinity setting, so use an interactive job instead.
* **Use page-size-independent builds.** Where a library offers a build option for transparent or configurable page sizes, prefer it over a binary with a hardcoded assumption.
* **Use containers built on Grace.** Run your workload with [Pyxis and Enroot](https://docs.coreweave.com/support/sunk/articles/how-do-i-run-containers-with-pyxis-and-enroot-in-slurm) using a container image that was built on an aarch64 host with a matching page size, rather than pulling a generic x86\_64 or 4 KiB-page image.
* **Tune the allocator as a stopgap.** For out-of-memory symptoms driven by glibc's `malloc`, setting `MALLOC_ARENA_MAX` to a small value can reduce per-thread arena over-allocation. It has no effect on programs that bring their own allocator, such as Node.js (V8) or anything linked against `jemalloc`. This is a workaround, not a fix, and doesn't address true architecture or page-size incompatibility.

```bash theme={"system"}
# Limit glibc malloc arenas as a stopgap for allocator-driven memory growth.
export MALLOC_ARENA_MAX=4
```

## Mixed-architecture SUNK clusters

A SUNK cluster can mix architectures. It's common and supported to run x86\_64 controllers and login Pods alongside aarch64 Grace compute nodes. Slurm itself doesn't require all nodes to share an architecture.

The practical consequence is that anything you build on an x86\_64 login Pod doesn't run on Grace compute nodes. If your users compile software or build wheels and container images for Grace targets, give them an aarch64 build environment so the build architecture and page size match the compute target. On SUNK Standard, pin login Pods to Grace nodes as described in [Mitigations](#mitigations). On SUNK Self-Service, build inside an interactive job on a Grace compute node instead.

## What this is not

The following points clarify what a Grace-specific failure is not:

* **A Grace out-of-memory error often isn't a true memory shortage.** Check `uname -m`, `getconf PAGESIZE`, and whether the binary was built for the right architecture and page size before requesting more memory or a larger instance.
* **An aarch64 build isn't automatically safe.** A binary can be the correct architecture and still carry a 4 KiB page-size assumption that breaks on Grace.
* **Page-size incompatibility isn't a CoreWeave platform defect.** It's a property of how the affected software was compiled.

## Verify the rebuild

After you rebuild, run the result inside a job on a Grace node and confirm the environment and the binary both match:

```bash theme={"system"}
# Confirm the job landed on a Grace node. Expect aarch64 and 65536.
uname -m
getconf PAGESIZE

# Confirm the rebuilt binary targets aarch64.
file [PATH-TO-BINARY]
```

`file` reports `ARM aarch64` for a correct build. Then run the command that failed before, for example `node --version` for a rebuilt Node.js runtime, or import the rebuilt Python extension. If it completes, the rebuild worked. If it still fails only on Grace, continue to the next section.

## When to file a support ticket

If a job fails only on Grace instances after you've confirmed the binary is aarch64, rebuilt it on a Grace environment, and ruled out a page-size assumption, open a ticket. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include `uname -m` and `getconf PAGESIZE` output and how the binary or image was built.

## Related pages

* [Optimize CPU binding and NUMA affinity for multi-GPU jobs](https://docs.coreweave.com/products/sunk/optimize_workloads/cpu-binding-numa-affinity.md): NUMA tuning, including Grace.
* [Configure individual login Pods](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login.md): provisioning an aarch64 build environment on SUNK Standard.
* [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md): placement on NVL72 racks.
