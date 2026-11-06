# Profile Python applications on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/profiling-python-apps-in-kubernetes

# Profile Python applications on SUNK

> Profile Python applications running in Slurm jobs using py-spy and Linux perf tools

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This tutorial shows you how to profile Python applications running in Slurm jobs on SUNK using `py-spy` and Linux `perf` tools. Profiling helps you identify performance bottlenecks in CPU usage, function calls, and native code so you can optimize your application. The guidance is aimed at developers and operators who already have a working SUNK deployment with an active Slurm job to profile.

SUNK `slurmd` Pods already have the `SYS_PTRACE` capability, so profilers can attach to processes without additional Pod configuration.

The following sections describe the prerequisite kernel configuration, how to use each profiler, a comparison of the two tools, and troubleshooting guidance.

## Prerequisites

Before you profile, you must configure the kernel parameters that `perf` requires on each Kubernetes Node. To use `perf`, the Kubernetes Nodes must have the `kernel.yama.ptrace_scope=0` and `kernel.perf_event_paranoid=-1` kernel parameters set. Deploy a DaemonSet that runs a privileged container on each Node to configure these parameters.

* The `kernel.yama.ptrace_scope=0` kernel parameter lets processes attach and read memory from other processes.
* The `kernel.perf_event_paranoid=-1` kernel parameter allows unprivileged access to performance monitoring.

> [!NOTE]
>
> If you only plan to use `py-spy`, the `ptrace_scope` parameter is the only one required. The `perf_event_paranoid` parameter is only needed for Linux `perf`.

1. Create a file called `py-perf-ds.yaml` with the following content:

   ```yaml title="py-perf-ds.yaml" highlight={23-29} theme={"system"}
   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     name: perf-debug
     namespace: tenant-slurm
   spec:
     selector:
       matchLabels:
         name: perf-debug
     template:
       metadata:
         labels:
           name: perf-debug
       spec:
         tolerations:
           - key: "sunk.coreweave.com/lock"
             operator: "Exists"
           - key: "sunk.coreweave.com/node"
             operator: "Exists"
         containers:
         - name: perf-debug
           image: busybox
           command:
             - /bin/sh
             - -c
             - >
               sysctl -w kernel.perf_event_paranoid=-1 &&
               sysctl -w kernel.yama.ptrace_scope=0 &&
               sleep infinity # Set the kernel parameters, then sleep to keep the container running.
           securityContext:
             privileged: true
   ```

   This DaemonSet sets the required kernel parameters on every Node.

   * It uses `sleep infinity` to keep the container running so that the kernel parameters persist while the container is running.
   * The `securityContext` section runs the container in privileged mode to let it set the kernel parameters.

2. Deploy the DaemonSet.

   ```bash theme={"system"}
   kubectl apply -f py-perf-ds.yaml
   ```

3. Verify the DaemonSet is running on all Nodes.

   ```bash theme={"system"}
   kubectl get ds perf-debug -n tenant-slurm
   ```

4. Verify the Pods are running.

   ```bash theme={"system"}
   kubectl get pods -n tenant-slurm -l name=perf-debug
   ```

5. Verify the kernel parameters are set on one of the Pods. Replace `[POD-NAME]` with one of the Pod names from the previous step.

   ```bash theme={"system"}
   kubectl exec -n tenant-slurm [POD-NAME] -- \
             sysctl kernel.perf_event_paranoid kernel.yama.ptrace_scope
   ```

The output shows the kernel parameters set to `-1` and `0` respectively.

```text theme={"system"}
kernel.perf_event_paranoid = -1
kernel.yama.ptrace_scope = 0
```

With the kernel parameters set on every Node, the cluster is ready for profiling.

## Use `py-spy`

`py-spy` is a sampling profiler designed for Python. It shows Python-level stack traces with function names, file paths, and line numbers. The following sections describe how to install `py-spy` in a debug container, view live profiling data, record flamegraphs, and configure common options.

### Install `py-spy`

To install `py-spy`, start a debug container attached to the `slurmd` Pod where your Slurm job is running, then install `py-spy` in the debug container.

1. Identify the `slurmd` Pod running your job. In SUNK, the Slurm node name matches the Kubernetes Pod name. Use `squeue` from a login node to find the node, then use that name as the Pod name.

   ```bash theme={"system"}
   squeue -u $USER -o "%.18i %.9P %.8j %.8T %.10M %.6D %R"
   ```

2. Set the Pod name from the `squeue` output.

   ```bash theme={"system"}
   COMPUTE_POD=[SLURM-NODE-NAME]
   ```

3. Start a debug container attached to the `slurmd` Pod.

   ```bash theme={"system"}
   kubectl debug $COMPUTE_POD -n tenant-slurm \
     --target=slurmd \
     --image=python:3.12-slim \
     --profile=general \
     -it -- bash
   ```

4. Inside the debug container, install `py-spy`.

   ```bash theme={"system"}
   pip install py-spy
   ```

### Show live top view in `py-spy`

> [!NOTE]
>
> In SUNK `slurmd` Pods, PID 1 is `slurmd`, not your Python application. Find your Python process PID with `ps aux | grep python` and use that PID in the following commands.

To show a live top view of the profiling data, updated continuously, use the `py-spy top` command.

```bash theme={"system"}
py-spy top --pid [PYTHON-PID]
```

The output shows the real-time profiling data.

```text theme={"system"}
Collecting samples from 'python /app.py' (pid: 42)
Total Samples 1000
GIL: 100%, Active: 100%, Threads: 1

  %Own   %Total  OwnTime  TotalTime  Function (filename:line)
  45.00%  45.00%   4.50s     4.50s   compute_hash (app.py:7)
  30.00%  75.00%   3.00s     7.50s   process_data (app.py:11)
  15.00%  15.00%   1.50s     1.50s   dumps (json/__init__.py:231)
   5.00%  95.00%   0.50s     9.50s   main (app.py:18)
   5.00%   5.00%   0.50s     0.50s   sleep (time.py:123)
```

The output shows the following:

* `%Own`: Percentage of time spent in this function itself.
* `%Total`: Percentage of time spent in this function and the functions it calls.
* `OwnTime`: Total time spent in this function itself.
* `TotalTime`: Total time spent in this function and the functions it calls.
* `GIL`: Percentage of time holding the Global Interpreter Lock.
* `Function (filename:line)`: Function name, filename, and line number.

### Record to SVG flamegraph

To record profiling data and generate an SVG flamegraph:

1. Run the following command:

   ```bash theme={"system"}
   py-spy record --pid [PYTHON-PID] --duration 30 -o /tmp/profile.svg
   ```

   The output shows that the profiling data is written to the `/tmp/profile.svg` file.

   ```text theme={"system"}
   py-spy> Sampling process 100 times a second for 30 seconds. Press Control-C to exit early.
   py-spy> Wrote flamegraph data to '/tmp/profile.svg'. Samples: 3000
   ```

2. Open a new terminal in your local machine and copy the SVG file to your local machine.

   ```bash theme={"system"}
   kubectl cp tenant-slurm/$COMPUTE_POD:/tmp/profile.svg ./profile.svg -c slurmd
   ```

3. Open `profile.svg` in a browser to see the flamegraph.

### Record to Speedscope format

Speedscope is a web-based viewer for performance profiles. To record profiling data and generate a Speedscope JSON file:

1. Run the following command:

   ```bash theme={"system"}
   py-spy record --pid [PYTHON-PID] --duration 30 --format speedscope -o /tmp/profile.speedscope.json
   ```

2. Open a new terminal in your local machine and copy the JSON file to your local machine.

   ```bash theme={"system"}
   kubectl cp tenant-slurm/$COMPUTE_POD:/tmp/profile.speedscope.json ./profile.speedscope.json -c slurmd
   ```

3. Upload the JSON file to [Speedscope](https://www.speedscope.app/) for analysis.

### Show thread activity

To show what each thread is doing, use the `py-spy dump` command.

```bash theme={"system"}
py-spy dump --pid [PYTHON-PID]
```

The output shows the thread activity.

```text theme={"system"}
Process 1: python /app.py
Thread 1 (active): "MainThread"
    compute_hash (app.py:7)
    process_data (app.py:11)
    main (app.py:18)
    <module> (app.py:28)
```

### Only show threads holding the GIL

The GIL (Global Interpreter Lock) is a mutex that protects the Python interpreter from concurrent execution. It ensures that only one thread executes Python code at a time. Monitoring the GIL helps you understand Python CPU usage (ignoring I/O wait).

To show only the threads holding the GIL, use the `--gil` flag with `py-spy top`.

```bash theme={"system"}
py-spy top --pid [PYTHON-PID] --gil
```

### `py-spy` options

`py-spy` has several options you can use to configure the profiling data.

#### `rate` option

Use the `rate` option to set the sampling rate. The default is 100 Hz. To sample at a higher rate, such as 500 Hz, pass `--rate 500`.

```bash theme={"system"}
py-spy record --pid [PYTHON-PID] --rate 500 -o profile.svg
```

#### `native` option

Use the `native` option to show native (C/C++) extensions.

```bash theme={"system"}
py-spy record --pid [PYTHON-PID] --native -o profile.svg
```

#### `idle` option

Use the `idle` option to show idle threads.

```bash theme={"system"}
py-spy record --pid [PYTHON-PID] --idle -o profile.svg
```

#### `nonblocking` option

Use the `nonblocking` option to run in non-blocking mode, which doesn't pause the target process.

```bash theme={"system"}
py-spy record --pid [PYTHON-PID] --nonblocking -o profile.svg
```

## Use `perf`

Linux perf is a performance analysis tool that shows system-level and native code performance. The following sections describe how to install `perf` in a debug container, view live profiling data, record reports and flamegraph data, and configure common options.

### Install `perf`

To install `perf`, start a debug container attached to the `slurmd` Pod where your Slurm job is running, then install `perf` in the debug container.

1. If you have not already identified the `slurmd` Pod, find it using `squeue` from a login node and set the Pod name.

   ```bash theme={"system"}
   COMPUTE_POD=[SLURM-NODE-NAME]
   ```

2. Start a debug container with Ubuntu. The Ubuntu distribution has `perf` tools available.

   ```bash theme={"system"}
   kubectl debug $COMPUTE_POD -n tenant-slurm \
     --target=slurmd \
     --image=ubuntu:22.04 \
     --profile=general \
     -it -- bash
   ```

3. Inside the debug container, install `perf`.

   ```bash theme={"system"}
   apt-get update && apt-get install -y linux-tools-generic
   ```

4. Locate the `perf` binary. The location varies by kernel version.

   ```bash theme={"system"}
   PERF=$(find /usr/lib/linux-tools -name perf | head -1)
   ```

### Show live top view in `perf`

To show real-time usage by function, use the `perf top` command.

```bash theme={"system"}
$PERF top -p [PYTHON-PID]
```

The output shows the real-time usage by function.

```text theme={"system"}
Samples: 8K of event 'cycles', 4000 Hz, Event count (approx.): 2841251931 lost: 0/0 drop: 0/0
Overhead  Shared Object        Symbol
  12.50%  python3.12           [.] _PyEval_EvalFrameDefault
   8.30%  python3.12           [.] PyObject_GetAttr
   6.20%  [kernel]             [k] copy_user_enhanced_fast_string
   5.10%  python3.12           [.] _PyObject_GenericGetAttrWithDict
   4.80%  _hashlib.so          [.] EVP_MD_CTX_copy_ex
   3.90%  python3.12           [.] PyDict_GetItem
   3.20%  libc.so.6            [.] __memcpy_avx_unaligned
   2.80%  python3.12           [.] PyUnicode_AsUTF8AndSize
```

The output shows the following:

* `Overhead`: CPU time percentage.
* `Shared Object`: The library or binary (python3.12, kernel, libc).
* `Symbol`: Function name.
* `[.]`: User-space function.
* `[k]`: Kernel function.

### Record and generate a report

To record for a specific duration, then generate a report, use the `record` command, then the `report` command.

This records at 99 Hz for 30 seconds with call graphs.

```bash theme={"system"}
$PERF record -F 99 -p [PYTHON-PID] -g -- sleep 30
```

Use the `report` command to view the report.

```bash theme={"system"}
$PERF report
```

The `report` command shows output similar to the following:

```text theme={"system"}
# Samples: 2K of event 'cycles'
# Event count (approx.): 1984327896
#
# Overhead  Command  Shared Object     Symbol
# ........  .......  ................  .................................
#
    15.23%  python   python3.12        [.] _PyEval_EvalFrameDefault
            |
            ---_PyEval_EvalFrameDefault
               |--45.00%--compute_hash
               |--30.00%--process_data
               |--15.00%--json_dumps

     8.91%  python   _hashlib.so       [.] EVP_DigestUpdate
            |
            ---EVP_DigestUpdate
               HASH_Update
               _hashlib_openssl_sha256_update
```

Use the arrow keys to navigate the report and press Enter to expand call chains.

### Generate a text report

To generate a text report to save or share results, use the `report` command with the `--stdio` option.

```bash theme={"system"}
$PERF report --stdio > perf_report.txt
```

### View detailed statistics

To view detailed statistics, use the `stat` command. This shows statistics for the process with the given PID for the specified duration.

```bash theme={"system"}
$PERF stat -p [PYTHON-PID] -- sleep 10
```

The output shows the statistics.

```text theme={"system"}
 Performance counter stats for process id '42':

         10,234.56 msec task-clock                #    1.023 CPUs utilized
             1,234      context-switches          #  120.567 /sec
                45      cpu-migrations            #    4.398 /sec
               123      page-faults               #   12.024 /sec
    38,456,789,012      cycles                    #    3.758 GHz
    24,123,456,789      instructions              #    0.63  insn per cycle
     5,678,901,234      branches                  #  554.932 M/sec
        12,345,678      branch-misses             #    0.22% of all branches

      10.003456789 seconds time elapsed
```

### Generate flamegraph data

To generate flamegraph data, use the `record` command, then the `script` command. This outputs the data as a script that you can use with the [FlameGraph](https://github.com/brendangregg/FlameGraph) tool.

1. Record the data. This records at 99 Hz for 30 seconds with call graphs.

   ```bash theme={"system"}
   $PERF record -F 99 -p [PYTHON-PID] -g -- sleep 30
   ```

2. Use the `script` command to output the data as a script.

   ```bash theme={"system"}
   # Output as script format
   $PERF script > perf.data.script
   ```

3. Copy the script file to your local machine.

   ```bash theme={"system"}
   kubectl cp tenant-slurm/$COMPUTE_POD:/path/to/perf.data.script ./perf.data.script -c slurmd
   ```

4. Use the [FlameGraph](https://github.com/brendangregg/FlameGraph) tool to generate a flamegraph from the script file.

### `perf` options

`perf` has several options you can use to configure the profiling data.

#### `-F` option

Use the `-F` option to set the sampling rate. The default is 99 Hz. To sample at a higher rate, such as 999 Hz, pass `-F 999`.

```bash theme={"system"}
$PERF record -F 999 -p [PYTHON-PID] -g -- sleep 30
```

Use the `-a` option to record all CPUs.

```bash theme={"system"}
$PERF record -F 99 -a -g -- sleep 30
```

Use the `-e` option to record specific events.

```bash theme={"system"}
$PERF record -e cycles,instructions -p [PYTHON-PID] -g -- sleep 30
```

Use the `--call-graph` option to record with a call-graph using dwarf, which is more accurate but also incurs more overhead.

```bash theme={"system"}
$PERF record -F 99 -p [PYTHON-PID] --call-graph dwarf -- sleep 30
```

## Compare `py-spy` and `perf`

`py-spy` and `perf` are two different tools for profiling Python applications in Kubernetes. They have different strengths and weaknesses. The following table and guidance help you decide which tool to use for a given investigation.

| Feature | py-spy | perf |
| - | - | - |
| **Focus** | Python code only | All code (Python, C, kernel) |
| **Output** | Function names, file:line | Native symbols, may need debug symbols |
| **Ease of use** | Easy, Python-specific | More complex, general purpose |
| **Overhead** | Low (about 1% to 2%) | Low (about 1% to 5%) |
| **Best for** | Python performance issues | System or native code issues, CPU and cache analysis |
| **GIL detection** | Yes, built-in | No |
| **Multi-threaded** | Shows Python threads clearly | Shows all threads |
| **Setup** | Install py-spy | Need kernel tools, may need debug symbols |
| **Output formats** | SVG, speedscope, text | Text report, script for flamegraphs |

Use `py-spy` when you need to profile pure Python code. It provides a quick, easy-to-read view of the Python code. It has low overhead, so it's suitable to use in production. It's a good fit when you need to see Python function names and line numbers, or want to understand GIL contention.

Use `perf` when you need to profile system-level performance. It provides a detailed view of the C extensions and kernel code, including CPU cache, branch prediction, and hardware counter data. It's a good fit when you suspect issues in native libraries (such as numpy or pandas C code), or need to correlate Python and kernel activity.

Use both tools when you need to profile complex performance issues and get a complete picture of the performance. This is useful if your code uses C extensions.

## Troubleshoot "Process not found" errors

Both `py-spy` and `perf` can return a "Process not found" error when you profile a process.

Both tools must attach to the target process. If the target process is not running, or the PID is incorrect, the tools fail with a "Process not found" error.

To fix this, verify the target process is running and the PID is correct.

1. Verify the target process is running: `ps aux | grep python`
2. Verify you're in the right container and namespace: `kubectl get pods -n tenant-slurm`
3. If you use `kubectl debug`, verify that `--target` is set to `slurmd`.

## Troubleshoot `py-spy`

### "Permission Denied" error

You might see a "Permission Denied" error when you profile a process with `py-spy`.

For example:

```text theme={"system"}
Error: Permission Denied: Try running again with elevated permissions
```

SUNK `slurmd` Pods already have the `SYS_PTRACE` capability, so this error usually means the kernel parameters are not set correctly. Verify the DaemonSet is running and the `ptrace_scope` parameter is configured.

1. Verify the DaemonSet is running: `kubectl get pods -n tenant-slurm -l name=perf-debug`

2. Check the kernel parameters:

   ```bash theme={"system"}
   kubectl exec -n tenant-slurm -l name=perf-debug -- \
     sysctl kernel.yama.ptrace_scope
   ```

   The output shows the kernel parameter set to `0`.

   ```text theme={"system"}
   kernel.yama.ptrace_scope = 0
   ```

3. Use `--profile=general` when you run `kubectl debug`.

### "Failed to find python version" error

You might see a "Failed to find python version" error when you profile a process with `py-spy`. This means the target PID is not a Python process.

For example:

```text theme={"system"}
Error: Failed to find python version from target process
```

In SUNK `slurmd` Pods, PID 1 is usually `slurmd`, not your Python application. Find the correct Python PID first:

```bash theme={"system"}
ps aux | grep python
```

Then, use that PID to profile the application.

```bash theme={"system"}
py-spy top --pid [PYTHON-PID]
```

## Troubleshoot `perf`

### "failed with EPERM" error

You might see a "failed with EPERM" error when you profile a process with `perf`.

```text theme={"system"}
Error: perf_event_open(...) failed with EPERM
```

To fix this, verify that the DaemonSet is running.

```bash theme={"system"}
kubectl get pods -n tenant-slurm -l name=perf-debug
```

Next, verify the kernel parameters are set correctly.

```bash theme={"system"}
kubectl exec -n tenant-slurm -l name=perf-debug -- \
          sysctl kernel.perf_event_paranoid
```

The output should show `kernel.perf_event_paranoid` is set to `-1`.

### No symbols found

If `perf` shows hex addresses instead of function names, the debug symbols are not installed.

To fix this, install the debug symbols for Python.

```bash theme={"system"}
apt-get install python3-dbg
```

Use the `--call-graph dwarf` option for better stack traces.

```bash theme={"system"}
$PERF record --call-graph dwarf -p [PYTHON-PID] -- sleep 30
```

## Tips for successful profiling

* Start with `py-spy`. It's easier to use than `perf` and usually sufficient for Python issues.
* Use low sampling rates in production. A rate from 99 Hz to 100 Hz is enough resolution for most applications.
* Record for at least 30 seconds. This gives representative samples.
* Profile during representative load. Idle or startup profiles aren't useful.
* Copy profiles out immediately. Debug containers are ephemeral and are deleted after the profiling session.
* Don't leave the DaemonSet running in production long-term. It uses privileged access, and leaving it running after the profiling session is a security risk.
* Use flamegraphs. They're easier to understand than text output. Flamegraphs show the most time-consuming functions and their callers, making it easier to identify bottlenecks.
* Compare before and after. Profile before optimization to establish a baseline. This helps you understand the impact of your optimizations.

## Typical workflow

The following workflow shows a typical end-to-end profiling session for a Python application running in a Slurm job on SUNK. Use it as a reference for combining the steps in this tutorial.

1. Deploy the DaemonSet to set the kernel parameters on all Nodes. See the example DaemonSet file in the [Prerequisites](#prerequisites) section. Deploy the DaemonSet:

   ```bash theme={"system"}
   kubectl apply -f py-perf-ds.yaml
   ```

2. Find the `slurmd` Pod running your Slurm job. From a login node, use `squeue` to identify the Slurm node, then start a profiling session.

   ```bash theme={"system"}
   COMPUTE_POD=[SLURM-NODE-NAME]
   kubectl debug $COMPUTE_POD -n tenant-slurm \
     --target=slurmd \
     --image=python:3.12-slim \
     --profile=general \
     -it -- bash
   ```

3. Inside the debug container, install `py-spy`, find your Python process, and check the top view.

   ```bash theme={"system"}
   pip install py-spy
   ps aux | grep python
   py-spy top --pid [PYTHON-PID]
   ```

4. Record a flamegraph for analysis.

   ```bash theme={"system"}
   py-spy record --pid [PYTHON-PID] --duration 60 -o /tmp/profile.svg
   ```

5. From another terminal, copy the flamegraph to your local machine. This is important because the debug container is deleted after the profiling session.

   ```bash theme={"system"}
   kubectl cp tenant-slurm/$COMPUTE_POD:/tmp/profile.svg ./profile.svg -c slurmd
   ```

6. If needed, dive deeper with `perf`.

   ```bash theme={"system"}
   apt-get update && apt-get install -y linux-tools-generic
   PERF=$(find /usr/lib/linux-tools -name perf | head -1)
   $PERF record -F 99 -p [PYTHON-PID] -g -- sleep 60
   $PERF report
   ```

7. Clean up the DaemonSet when done. Removing the DaemonSet reduces the security exposure of leaving privileged Pods running on the cluster.

   ```bash theme={"system"}
   kubectl delete -f py-perf-ds.yaml
   ```

After completing this workflow, you have flamegraph and report data you can analyze locally to identify performance bottlenecks in your Python application.

## Helpful references for profiling

* [py-spy Documentation](https://github.com/benfred/py-spy)
* [Linux perf Wiki](https://perfwiki.github.io/)
* [Brendan Gregg's Perf Examples](https://www.brendangregg.com/perf.html)
* [FlameGraph Tools](https://github.com/brendangregg/FlameGraph)
* [Speedscope](https://www.speedscope.app/)
