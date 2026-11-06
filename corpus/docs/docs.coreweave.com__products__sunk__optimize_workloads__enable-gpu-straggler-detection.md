# Enable GPU Straggler Detection

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection

# Enable GPU Straggler Detection

> Turn GPU Straggler Detection on or off in SUNK and confirm the plugin loads, so you can find GPUs that fall behind.

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

[GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md) tracks each GPU in a distributed training job and flags the rank that falls out of sync, so you can drain the offending node before it degrades job performance further. It also provides continuous NVIDIA Collective Communications Library (NCCL) metrics on latency, bandwidth, and message sizes, plus rank-level attribution through the straggler tables. Dedicated [Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) surface all of this.

The plugin is on by default on SUNK Self-Service and on SUNK Standard v8.0.0 and later. This guide shows how to check its status, turn it on or off, and verify that it loads in your jobs. After you complete this guide, your cluster surfaces NCCL performance data in Grafana and reports GPU stragglers, including ranks that stall outright.

## Prerequisites

Before you begin, confirm your environment meets the following requirements:

* On SUNK Standard, SUNK v7.4.0 or later.
* NCCL 2.28.2 or later loaded by the job at runtime. For container jobs, that's the NCCL in your container image. For jobs without a container, it's the NCCL in the compute node image. A Python virtual environment that bundles its own NCCL, as `pip install torch` does, takes precedence over the image's.
* At least 2 CPUs allocated per task.

## Enable the plugin

> [tab] SUNK Standard
>
> On SUNK v8.0.0 and later, the plugin is on by default. The Slurm Helm chart leaves `compute.gpusd.enabled` unset, and the operator defaults it to `true`. To opt out, set `compute.gpusd.enabled` to `false` in your cluster's `values.yaml`.
>
> On SUNK v7.4.x, the plugin is off until you enable it. In your cluster's `values.yaml`, set `compute.gpusd.enabled` to `true`. See [Slurm parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for more information.
>
> ```yaml theme={"system"}
> compute:
>   gpusd:
>     enabled: true
> ```

> [tab] SUNK Self-Service
>
> The plugin is on by default. It stays on unless the `SunkCluster` sets `spec.features.gpusd.enabled` to `false`, so a manifest that omits the `features` block, or the `gpusd` block inside it, gets the plugin without any change.
>
> The [out-of-band operator](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md) applies this default when it reconciles the cluster, not in the `SunkCluster` resource itself. If your manifest omits the field, `kubectl get sunkcluster -o yaml` doesn't show `enabled: true`. To confirm the value the operator applied, read it from the `SlurmCluster` that it generates:
>
> ```bash theme={"system"}
> kubectl get slurmcluster [CLUSTER-NAME] -n tenant-slurm -o jsonpath='{.spec.compute.gpusd.enabled}'
> ```
>
> Replace `[CLUSTER-NAME]` with the name of your `SunkCluster`. The `SlurmCluster` that the operator generates has the same name. The command prints `true` when the plugin is on.
>
> To turn the plugin off, set `spec.features.gpusd.enabled` to `false` in your `SunkCluster` manifest and reapply it:
>
> ```yaml theme={"system"}
> spec:
>   features:
>     gpusd:
>       enabled: false
> ```
>
> Changing this setting, in either direction, triggers a rolling restart of the compute NodeSets. The restart drains each node first, so a node that's running a job keeps its Pod until the job finishes.
>
> The `spec.features.gpusd` block accepts the following fields:
>
> | Field | Type | Default | Description |
> | - | - | - | - |
> | `enabled` | boolean | `true` | Turns GPU Straggler Detection on. Set to `false` to opt out. |
> | `version` | string | Unset | Pins the GPUSD package version, for example `1.2.3`. Leave unset to use the version that SUNK ships. |

When the plugin is enabled, SUNK automatically:

* Downloads and installs the GPUSD package on compute nodes at startup.
* Exposes ports `10400-10407` on `slurmd` Pods for metrics collection.
* Exposes port `10500` on `slurmd` Pods on SUNK Self-Service and on SUNK Standard v8.2.0 and later, when the GPUSD package is version 1.1.0 or later, which is the default on those versions.
* Deploys a VMPodScrape resource to scrape NCCL plugin metrics.

For jobs launched with `--container` or `--container-image`, an Enroot hook automatically mounts the plugin into the container and sets `NCCL_PROFILER_PLUGIN` in the job environment. Container-based jobs don't need additional configuration.

For jobs running without a container, add the following environment variable to your batch job script:

```bash theme={"system"}
export NCCL_PROFILER_PLUGIN=/usr/lib/libnccl-profiler-gpusd.so
```

### Enable debugging information

To confirm the plugin loaded successfully and to capture useful logs during initial validation, enable NCCL debug output.

On first run, enable `export NCCL_DEBUG=INFO` to print debugging information. If you've correctly loaded the plugin, the output includes a line resembling the following:

```text theme={"system"}
h200-205-187:1189647:1189647 [0] NCCL INFO Successfully loaded external profiler plugin /usr/lib/libnccl-profiler-gpusd.so
```

You can set the following optional environment variables to control performance metrics collection and logging verbosity:

| Variable | Purpose |
| - | - |
| `GPUSD_PERF_DEBUG=0` | Disable performance metrics (Straggler Detection only) |
| `GPUSD_PERF_DEBUG=1` | Enable performance metrics (always on) |
| `GPUSD_PERF_DEBUG=2` | Toggle metrics with `SIGUSR1` (on) or `SIGUSR2` (off) |
| `GPUSD_DEBUG=VERSION` | Minimal logging |
| `GPUSD_DEBUG=INFO` | Standard logging |
| `GPUSD_DEBUG=TRACE` | Verbose logging |

## View metrics in Grafana

The [Slurm Job Metrics](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) dashboard in CoreWeave Grafana surfaces Straggler Detection data across several panels:

| Panel | Description |
| - | - |
| **GPU Straggler** | Table that identifies the rank and node that fell behind the rest of the job |
| **Slow NCCL Operations** | Table that identifies ranks whose algorithmic bandwidth (AlgoBW) dropped, and the collective affected |
| **NCCL BusBW** and **NCCL Latency** | Bandwidth and collective latency, one panel per process-group size |
| **NCCL Message Size** | Average payload size per collective operation |
| **GPU Straggler** annotation | Marks the intervals where a straggler was flagged on the **Job State Timeline** and **Current FP8 FLOPS** panels |
| **Slow NCCL Operations** annotation | Overlays slow collective operations onto the **NCCL BusBW** panels |

All of these panels are in the **NCCL Metrics** row, below **Node Resources**. The exceptions are the **GPU Straggler** and **Slow NCCL Operations** annotations, which you toggle from the top of the dashboard.

With the plugin enabled and metrics flowing, you can use these dashboards to identify straggler and slow GPUs during training runs and [drain affected nodes](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md) before they impact job completion.
