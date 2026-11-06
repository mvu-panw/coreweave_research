# Connect to a Node

Source: https://docs.coreweave.com/products/cks/nodes/connect

# Connect to a Node

> Connect to a CKS Node using kubectl debug Pods to troubleshoot network, storage, and other issues

This guide explains how to connect to a Node using a debug Pod for troubleshooting. This approach is useful for diagnosing and resolving issues with a Node that isn't functioning as expected. Common scenarios for connecting to a Node include investigating problems with the Node's network connectivity or local storage.

## Prerequisites

Before you begin, ensure you have:

* An active CoreWeave account.
* `kubectl` installed locally.
* A [Kubeconfig](https://docs.coreweave.com/products/cks/auth-access/managed-auth/kubeconfig.md) with access to the desired Node.

## About debug Pods

To connect to a Node, you create a debug Pod that runs on the Node you want to troubleshoot. The debug Pod lets you interact with the Node's filesystem and network interfaces, and run diagnostic commands such as `ip`, `ifconfig`, `nc`, `ping`, and `ps`. You can install additional tools, such as `mtr`, `tcpdump`, and `curl`, using the Node's package manager. When you use a debug Pod, keep the following in mind:

* `kubectl debug` automatically creates a new Pod name based on the Node name.
* The root filesystem of the Node is mounted at `/host`.
* Debug Pods aren't privileged, so commands such as `chroot /host` that are restricted to superusers fail. If you need a privileged Pod, create it manually or use the `--profile=sysadmin` flag.
* You can set specific properties such as [securityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) on a debug Pod by applying [Debugging Profiles](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#debugging-profiles).

## Connect to a Node

To connect to a Node, use `kubectl debug node`. The following example creates a debug Pod on a Node named `mynode` with the `ubuntu` image and an interactive shell:

```bash theme={"system"}
kubectl debug node/mynode -i -t --image=ubuntu
```

The output is similar to the following:

```text theme={"system"}
Creating debugging Pod `node-debugger-mynode-pdx84` with container debugger on Node `mynode`.
If you don't see a command prompt, try pressing enter.
root@mynode:/#
```

Use this shell to run diagnostic commands and troubleshoot issues on the Node.

### Command-line explanation

* `kubectl debug node/mynode`: Create a debug Pod on the Node named `mynode`.
* `-i`: Keep stdin open on the container in the Pod, even if nothing is attached.
* `-t`: Allocate a TTY for the debug container.
* `--image=ubuntu`: Use the Ubuntu container image for the debug Pod.

## Clean up

When you no longer need the debug Pod, delete it. First, list your Pods to find the debug Pod's name:

```bash theme={"system"}
kubectl get pods
```

The output is similar to the following:

```text theme={"system"}
NAME                          READY   STATUS       RESTARTS   AGE
node-debugger-mynode-pdx84    0/1     Completed    0          8m1s
```

Delete the debug Pod by name:

```bash theme={"system"}
kubectl delete pod node-debugger-mynode-pdx84 --now
```

The output confirms deletion:

```text theme={"system"}
pod "node-debugger-mynode-pdx84" deleted
```

## View Node system logs

You can read Node-level logs, such as `kubelet` and `containerd` logs, from inside a debug Pod. The root filesystem of the Node is mounted at `/host`, so its log files are available under `/host/var/log/`.

For example, after attaching to the debug Pod:

```bash theme={"system"}
# List available system logs on the Node.
ls /host/var/log/

# Tail the journal files on disk (binary format, requires journalctl).
ls /host/var/log/journal/
```

To read systemd unit logs such as `kubelet` or `containerd`, use `journalctl` with the `--root` flag to point it at the Node's filesystem:

```bash theme={"system"}
# Install journalctl if it isn't already in the debug image, then:
journalctl --root=/host -u kubelet --no-pager | tail -n 200
journalctl --root=/host -u containerd --no-pager | tail -n 200
```

If `journalctl --root` isn't available in your debug image, launch the debug Pod with `--profile=sysadmin` and use `chroot /host` to run `journalctl` inside the Node's filesystem:

```bash theme={"system"}
kubectl debug node/mynode -i -t --profile=sysadmin --image=ubuntu
# Inside the debug Pod:
chroot /host journalctl -u kubelet --no-pager | tail -n 200
```

## More options

`kubectl debug node` offers many other command-line options to customize the debug Pod's namespace, container name, and image. You can also issue commands to the Pod or copy an existing Pod's configuration. Use `--help` for a full list of options with examples:

```bash theme={"system"}
kubectl debug node --help
```

## Other references

To learn more, see *[Debugging Kubernetes Nodes With Kubectl](https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/)* in the Kubernetes documentation.
