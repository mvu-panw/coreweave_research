# Run custom scripts with s6

Source: https://docs.coreweave.com/products/sunk/run_workloads/run-scripts-with-s6

# Run custom scripts with s6

> Run custom longrun and oneshot scripts on SUNK compute and login nodes using the s6 service manager

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

SUNK can run custom scripts on Compute and Login nodes with s6 using s6-rc, a service manager for s6-based systems available at `https://skarnet.org/software/s6-rc/`. This guide explains how to set up and run [two types of scripts](#determine-the-appropriate-script-type): `longrun` for continuous processes and `oneshot` for tasks that execute and terminate.

This guide is for cluster administrators who need to automate custom scripts on Compute and Login nodes within a SUNK cluster. Whether you install packages or keep services running, this method provides a straightforward way to manage processes.

## Define scripts in `values.yaml`

Define scripts in the appropriate sections of the Slurm chart's `values.yaml` file. Define Compute node scripts in the [`compute.s6`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) section, and Login node scripts in the [`login.s6`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) section. Each script needs a name, type, and the script itself. The following example shows a script definition within a Compute node:

```yaml theme={"system"}
compute:
  s6:
    install-nginx:
      type: oneshot
      timeoutUp: 300000 # 5 minutes
      script: |
        #!/usr/bin/env bash
        apt -y update
        apt -y install nginx
    nginx:
      type: longrun
      timeoutUp: 30000 # 30 seconds
      timeoutDown: 0
      script: |
        #!/usr/bin/env bash
        nginx -g "daemon off;"
```

The preceding example includes two scripts:

* `install-nginx`: This `oneshot` script installs `nginx` using the package manager.
* `nginx`: A `longrun` script that starts the `nginx` process and keeps it running.

Each script sets a [`timeoutUp`](#set-timeouts-for-scripts) in milliseconds: the install has up to 5 minutes to finish, and `nginx` has up to 30 seconds to start.

## Define and schedule different script types

The following sections explain how to choose the right script type for your task and how to avoid scheduling conflicts that can occur when scripts extend node startup time.

### Determine the appropriate script type

Decide whether the script is a `longrun` or a `oneshot` based on its purpose:

* Use `longrun` for scripts that should run continuously, like a web server.
* Use `oneshot` for scripts that run once to perform a setup task, like installing software.

### Avoid scheduling conflicts

If your `oneshot` job installs many packages or performs tasks that otherwise extend startup time, you must account for this by modifying the value of the `orphanedPodDelay` parameter in the `syncer` configuration section of the [Slurm `values.yaml` chart](https://docs.coreweave.com/products/sunk/reference/slurm-parameters).

The full path for this parameter is `syncer.config.syncer.orphanedPodDelay`. By default, the value of `orphanedPodDelay` is `120s`, or 120 seconds.

If the time required for a `oneshot` job to run exceeds the value set in `orphanedPodDelay`, increase the value to avoid scheduling conflicts.

## Set timeouts for scripts

Timeouts prevent scripts from hanging indefinitely and help keep nodes healthy. The `timeoutUp` parameter sets the time allowed for the script to start, and `timeoutDown` sets the time allowed for it to stop. Both are in milliseconds.

Every script-based `oneshot` must set `timeoutUp`, and every `longrun` must set `timeoutUp`, `timeoutDown`, or both. A service that omits its timeout is rejected with `timeoutUp is required for oneshot scripts unless installing packages`. A `oneshot` that installs packages through the `packages` key is exempt, because the controller derives a minimum timeout from the package count.

> [!WARNING]
>
> Without a configured timeout, the s6 script can become unresponsive indefinitely and cause the `slurmd` Pod to stay in a `Not Ready` state.

* For `oneshot` scripts, only `timeoutUp` is relevant as it's the maximum completion time for the script.
* For `longrun` scripts, both `timeoutUp` and `timeoutDown` control how long the process has to start and stop.

## Define behavior for failed scripts

When a user-defined script fails, the container can continue running silently, provide an error message, or stop. In SUNK, containers stop on script failure by default.

You can control this behavior with the `S6_BEHAVIOUR_IF_STAGE2_FAILS` parameter in the appropriate `env` section of the `values.yaml` file.

* For **Login nodes**, change the value of the parameter in the `login.env` section of the `values.yaml` file.
* For **Compute nodes**, change the value of the parameter in the `compute.nodes.[TARGET-NODE].env` sections of the `values.yaml` file.

The `S6_BEHAVIOUR_IF_STAGE2_FAILS` parameter can contain the following values:

| Value | Behavior |
| - | - |
| `0` | If a script fails, the container continues to run silently, without providing an error message. |
| `1` | If a script fails, the container continues to run, but provides an error message warning about the failure. |
| `2` | If a script fails, the container stops running. This is the default setting on SUNK. |

For more information about the values for `S6_BEHAVIOUR_IF_STAGE2_FAILS`, see the [s6-overlay](https://github.com/just-containers/s6-overlay?tab=readme-ov-file#customizing-s6-overlay-behaviour) customization options.

## Raise the open-file limit cluster-wide

A common use of a `oneshot` script is to raise the open-file descriptor limit (`nofile`) for every job on the cluster. SUNK container images set the soft limit to `16384` in `/etc/bash.bashrc`:

```bash theme={"system"}
ulimit -Sn 16384
```

The `-S` flag sets only the soft limit, so a non-root user can raise it up to the hard limit. To raise the limit for a single job without administrator help, set it at the top of the `sbatch` script before `srun`:

```bash theme={"system"}
# Raise the soft open-file limit for this job. 65536 is a typical starting point;
# 262144 suits heavy I/O with many shards and workers. The ceiling is the hard
# limit on the node, which you can check with `ulimit -Hn`.
ulimit -n 65536
```

To change the default for every job and shell, add a `oneshot` script in the `compute.s6` section that removes the hardcoded line and raises the limit:

```yaml title="values.yaml" theme={"system"}
compute:
  s6:
    ulimit:
      type: oneshot
      timeoutUp: 30000 # 30 seconds
      script: |
        #!/bin/sh
        sed -i -e 's/^ulimit/#ulimit/g' /etc/bash.bashrc
```

Commenting out the line is the whole change. Once the `16384` soft cap no longer applies, shells inherit the container's own limits, which are typically `1048576`. Don't add `ulimit` commands to the script itself: a `ulimit` call changes only the process that runs it, so it has no effect on the shells and job steps that start later.

Nodes pick up the change when their Pods are replaced. Adding a new s6 block changes the Pod spec, so the NodeSet rolls the `slurmd` Pods on its own. Editing the script inside an existing block only updates a ConfigMap, which leaves the Pod spec untouched and doesn't roll anything, so you have to replace the Pods yourself. If you need to know how running jobs are handled, coordinate the rollout with your cluster administrator. Verify on a compute node:

```bash theme={"system"}
# Confirm the hardcoded line is commented and the limits are raised. Safe; read-only.
grep ulimit /etc/bash.bashrc
ulimit -Sn
ulimit -Hn
```

Both `ulimit` commands should report the container default, typically `1048576`, rather than `16384`. Confirm that a non-root user can now raise the limit by running `ulimit -n 65536` and checking `ulimit -Sn` again.

Raising the limit isn't a fix for a descriptor leak. If a job's open-file count grows without bound, the application leaks descriptors, and a higher limit only delays the failure.
