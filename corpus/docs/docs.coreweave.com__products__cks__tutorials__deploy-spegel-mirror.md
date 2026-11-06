# Deploy Spegel, a P2P registry mirror on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-spegel-mirror

# Deploy Spegel, a P2P registry mirror on CKS

> Deploy Spegel, a stateless distributed OCI registry mirror for peer-to-peer image sharing across cluster Nodes on CKS

This tutorial shows you how to deploy [Spegel](https://spegel.dev/), a stateless peer-to-peer OCI registry mirror, on CoreWeave Kubernetes Service (CKS). Running Spegel speeds up container image pulls, reduces external registry dependencies, and improves cluster reliability by sharing images across Nodes. This tutorial is for cluster operators who manage CKS workloads and want to lower image-pull latency or insulate clusters from upstream registry outages.

> [!NOTE]
>
> **P2P distributed architecture**
>
> Spegel uses a Kademlia-based Distributed Hash Table (DHT) to enable peer-to-peer image sharing across cluster Nodes. Each Node advertises its locally cached images so other Nodes can pull layers directly from cluster peers instead of external registries. This stateless design requires no persistent storage. Spegel uses containerd's existing image cache on each Node.

In this tutorial, you will:

1. **Verify containerd configuration** to ensure registry mirroring is enabled.
2. **Deploy Spegel** with Helm as a DaemonSet across all Nodes.
3. **Verify P2P image sharing** by pulling images and observing peer-to-peer transfers.

> [card] What you'll need
>
> Before you start, you must have a working [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with at least two [CPU Nodes](https://docs.coreweave.com/platform/instances/cpu-instances.md) or [GPU Nodes](https://docs.coreweave.com/platform/instances/gpu-instances.md). P2P functionality requires multiple Nodes.
>
> You'll need the following tools on your local machine:
>
> * [kubectl](https://kubernetes.io/docs/reference/kubectl/) installed and [configured for your cluster](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * [kvaps node-shell](https://github.com/kvaps/kubectl-node-shell) to verify containerd configuration on your Nodes. Alternatively, use `kubectl exec` on those steps.
> * [Helm](https://helm.sh/docs/intro/install/) version 3.8+.

> [card] What you'll use
>
> You'll use these tools and technologies:
>
> * [**Spegel**](https://spegel.dev/): Peer-to-peer OCI registry mirror for the cluster.
> * [**Helm**](https://helm.sh/): Package manager that installs the Spegel chart from its OCI registry.
> * [**kubectl**](https://kubernetes.io/docs/reference/kubectl/): Kubernetes CLI for cluster access, verification, and optional port-forwarding to the Spegel debug UI.
> * [**kubectl node-shell**](https://github.com/kvaps/kubectl-node-shell): Plugin to check containerd settings on Nodes (optional if you use another method).

## Verify cluster access

Before you install Spegel, confirm that your local environment can reach the cluster and that the cluster has enough Nodes for peer-to-peer image sharing.

Verify that you can access your cluster with `kubectl`:

```bash theme={"system"}
kubectl cluster-info
```

You should see something similar to:

```text theme={"system"}
Kubernetes control plane is running at...
CoreDNS is running at...
node-local-dns is running at...
```

Verify your cluster has at least two Nodes:

```bash theme={"system"}
kubectl get nodes
```

You should see at least two Nodes:

```text theme={"system"}
NAME      STATUS   ROLES    AGE   VERSION
g8fb8e0   Ready    <none>   76d   v1.34.3
g8fd342   Ready    <none>   76d   v1.34.3
g8ff980   Ready    <none>   76d   v1.34.3
```

## Verify containerd configuration

Spegel requires specific containerd settings to work, as documented in the [Spegel compatibility requirements](https://spegel.dev/docs/getting-started/#compatibility). CoreWeave CKS clusters are pre-configured with these settings, but you can verify them with [kubectl node-shell](https://github.com/kvaps/kubectl-node-shell).

Get a Node name and check the containerd configuration:

```bash theme={"system"}
# Get a node name
NODE_NAME=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')

# Shell into the node and check containerd config
kubectl node-shell ${NODE_NAME} -- grep -E 'config_path|discard_unpacked_layers' /etc/containerd/config.toml
```

Verify the output contains these required settings:

```text theme={"system"}
config_path = "/etc/containerd/certs.d"
discard_unpacked_layers = false
```

> [!NOTE]
>
> **CoreWeave CKS clusters** are pre-configured with these settings, so you can proceed to deploying Spegel.

## Deploy Spegel

With containerd verified, you can install Spegel as a DaemonSet so that every Node runs a local mirror.

Install Spegel with the Helm chart from the OCI registry:

```bash theme={"system"}
helm upgrade --create-namespace --namespace spegel --install spegel \
  oci://ghcr.io/spegel-org/helm-charts/spegel
```

This command does the following:

* Creates the `spegel` namespace if it doesn't exist.
* Installs Spegel as a DaemonSet (one Pod per Node).
* Uses default configuration suitable for most clusters.

### Deploy on SUNK GPU Nodes

To run Spegel on [SUNK](https://docs.coreweave.com/products/sunk.md) GPU Nodes, configure memory resources to use the Burstable QoS class instead of the [upstream defaults](https://github.com/spegel-org/spegel/blob/main/charts/spegel/values.yaml) where requests equal limits. Setting requests equal to limits creates a Guaranteed QoS Pod, which can interfere with Slurm's thread counter on SUNK Nodes:

```bash theme={"system"}
helm upgrade --create-namespace --namespace spegel --install spegel \
  oci://ghcr.io/spegel-org/helm-charts/spegel \
  --set resources.requests.memory=128Mi \
  --set resources.limits.memory=256Mi
```

Alternatively, create a `values.yaml` file:

```yaml title="values.yaml" theme={"system"}
resources:
  requests:
    memory: 128Mi
  limits:
    memory: 256Mi
```

Then install with:

```bash theme={"system"}
helm upgrade --create-namespace --namespace spegel --install spegel \
  oci://ghcr.io/spegel-org/helm-charts/spegel \
  -f values.yaml
```

> [!NOTE]
>
> **Why Burstable QoS?** Kubernetes assigns the [Guaranteed QoS class](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/#guaranteed) when a Pod's resource requests equal its limits. On SUNK Nodes, Guaranteed QoS Pods can interfere with Slurm's thread counter, which tracks available CPU threads for job scheduling. When you set the memory limit higher than the request (256Mi versus 128Mi), the Pod receives the Burstable QoS class instead. This avoids the conflict while still providing resource constraints.

> [!NOTE]
>
> **Tolerations**: The [upstream Spegel chart](https://github.com/spegel-org/spegel/blob/main/charts/spegel/values.yaml) includes tolerations for all `NoExecute` and `NoSchedule` taints by default. This covers the SUNK Node lock taint (`sunk.coreweave.com/lock:NoExecute`), so no additional toleration configuration is needed.

The Spegel Helm chart automatically configures containerd registry mirrors on each Node. No additional containerd configuration is required after installation.

Verify the DaemonSet is running:

```bash theme={"system"}
kubectl get daemonset -n spegel
```

You should see the DaemonSet with the desired number matching your Node count:

```text theme={"system"}
NAME     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
spegel   3         3         3       3            3           kubernetes.io/os=linux   7s
```

After this section, Spegel is running as a DaemonSet on every Node and containerd is configured to use it as a registry mirror.

## Verify Spegel installation

Verify all Spegel Pods are running:

```bash theme={"system"}
kubectl get pods -n spegel -o wide
```

You should see one Pod per Node:

```text theme={"system"}
NAME           READY   STATUS    RESTARTS   AGE   IP           NODE      NOMINATED NODE   READINESS GATES
spegel-4sppw   1/1     Running   0          16s   10.0.0.112   g8fb8e0   <none>           <none>
spegel-h2fl2   1/1     Running   0          16s   10.0.1.126   g8fd342   <none>           <none>
spegel-qf5gw   1/1     Running   0          16s   10.0.0.246   g8ff980   <none>           <none>
```

## Verify Spegel works

A running DaemonSet confirms that the Pods are healthy, but it doesn't prove that P2P transfers are happening. The next steps exercise Spegel end-to-end so you can confirm that one Node serves image layers to another.

Follow the [official Spegel verification guide](https://spegel.dev/docs/getting-started/#verify-deployment) to confirm P2P image sharing is functioning. Pull an image on one Node, then pull the same image on a different Node. Verify that the second pull was served from the first Node through Spegel.

### Test P2P image distribution

The [official Spegel documentation](https://spegel.dev/docs/getting-started/#verify-deployment) recommends running these commands to test P2P functionality. The commands select random Spegel Pods on different Nodes, create test Pods that pull an image, then clean up.

> [!NOTE]
>
> The `shuf` command is part of GNU coreutils. On macOS, install it with `brew install coreutils`.

```bash theme={"system"}
# Select a random upstream node and pull an image there
UPSTREAM_POD_NAME=$(kubectl --namespace spegel -l app.kubernetes.io/name=spegel \
  get pods -o custom-columns=:metadata.name --no-headers | shuf -n 1)
UPSTREAM_NODE_NAME=$(kubectl --namespace spegel get pod ${UPSTREAM_POD_NAME} \
  -o jsonpath="{.spec.nodeName}")
kubectl --namespace default run upstream --image=ubuntu:25.04 --restart=Never \
  --overrides="{\"spec\":{\"nodeName\":\"${UPSTREAM_NODE_NAME}\",\"containers\":[{\"name\":\"ubuntu\",\"image\":\"ubuntu:25.04\",\"imagePullPolicy\":\"Always\",\"command\":[\"true\"]}]}}"

# Select a different node and pull the same image (should come from Spegel)
MIRROR_POD_NAME=$(kubectl --namespace spegel -l app.kubernetes.io/name=spegel \
  get pods -o custom-columns=:metadata.name --no-headers | grep -v "^${UPSTREAM_POD_NAME}$" | shuf -n 1)
MIRROR_NODE_NAME=$(kubectl --namespace spegel get pod ${MIRROR_POD_NAME} \
  -o jsonpath="{.spec.nodeName}")
kubectl --namespace default run mirror --image=ubuntu:25.04 --restart=Never \
  --overrides="{\"spec\":{\"nodeName\":\"${MIRROR_NODE_NAME}\",\"containers\":[{\"name\":\"ubuntu\",\"image\":\"ubuntu:25.04\",\"imagePullPolicy\":\"Always\",\"command\":[\"true\"]}]}}"

# Clean up test pods
kubectl --namespace default delete pod upstream mirror
```

### Verify with the debug page

Spegel includes a debug web interface that shows instance-level statistics. Port-forward to a Spegel Pod and check the debug page.

If you did not run the [preceding test commands](#test-p2p-image-distribution), choose any Spegel Pod name first:

```bash theme={"system"}
kubectl --namespace spegel port-forward ${MIRROR_POD_NAME} 9090
```

In a browser, navigate to `http://localhost:9090/debug/web` and check the **Last Mirror Success** field. If Spegel recently served an image from a peer, this field displays a duration (for example, `2m30s`) indicating how long ago. On a freshly deployed cluster, this field shows `Pending` until the first P2P transfer occurs.

### Test image pulls from the debug page

The debug page includes a **Measure Image Pull** feature at the bottom that lets you test P2P functionality directly. Enter an image reference (for example, `docker.io/library/nginx:latest`) and click **Pull** to see:

* **Lookup Result**: Shows discovered peers that have the image and lookup latency.
* **Pull Result**: Shows total pull duration, image size, and per-layer breakdown.

> [!WARNING]
>
> **Silent fallback behavior**: Spegel is designed to fall back silently to upstream registries when P2P transfer is unavailable. This means image pulls succeed even if Spegel isn't functioning, potentially masking configuration problems. Use the debug page to verify P2P transfers are occurring.

## Optional: Benchmark P2P performance

Use this section when you need quantitative evidence that Spegel improves pull times in your cluster, for example, before standardizing on it across an environment.

To measure Spegel's performance, use the official Spegel benchmark tool. This tool measures image pull times and provides reproducible metrics that compare P2P performance against direct registry pulls. The steps in this section require Go and a working `kubectl` context with permissions to create benchmark workloads in your cluster (see [Verify cluster access](#verify-cluster-access)).

### Install the benchmark tool

Install the benchmark tool with Go:

```bash theme={"system"}
go install github.com/spegel-org/benchmark@latest
```

This installs the `benchmark` binary to your `$GOPATH/bin` directory. Verify installation:

```bash theme={"system"}
benchmark --help
```

The output looks similar to:

```text theme={"system"}
Usage: benchmark <command> [<args>]

Options:
  --help, -h             display this help and exit

Commands:
  generate               Generate images for benchmarking.
  measure                Run benchmark measurement.
  suite                  Run the full suite of measurements.
  analyze                Analyze benchmark results.
```

### Run performance measurements

Create a results directory and run the benchmark with standardized test images:

```bash theme={"system"}
# Create results directory
mkdir -p ~/spegel-benchmark-results

# Run benchmark with 10MB test images
benchmark measure \
  --output-dir ~/spegel-benchmark-results \
  --namespace spegel-benchmark \
  --images ghcr.io/spegel-org/benchmark:v1-10MB-1 \
    ghcr.io/spegel-org/benchmark:v2-10MB-1
```

The benchmark does the following:

1. Deploys DaemonSets that force image pulls across all Nodes.
2. Measures initial pull times.
3. Measures update pull times.

For broader testing, run benchmarks with different image sizes:

```bash theme={"system"}
# Test 100MB images
benchmark measure \
  --output-dir ~/spegel-benchmark-results/100mb \
  --namespace spegel-benchmark \
  --images ghcr.io/spegel-org/benchmark:v1-100MB-1 \
    ghcr.io/spegel-org/benchmark:v2-100MB-1

# Test 1GB images
benchmark measure \
  --output-dir ~/spegel-benchmark-results/1gb \
  --namespace spegel-benchmark \
  --images ghcr.io/spegel-org/benchmark:v1-1GB-1 \
    ghcr.io/spegel-org/benchmark:v2-1GB-1
```

For more information, see the [Spegel benchmark documentation](https://spegel.dev/docs/benchmark/).

This creates performance charts that compare:

* Initial image pull times across Nodes.
* Rolling update pull times (which demonstrate P2P cache hits).
* Performance improvements when Spegel serves images from local peers.

> [!NOTE]
>
> **Benchmark best practices**: Run benchmarks on a cluster with at least 3 Nodes for meaningful P2P metrics. The benchmark tool uses standardized images with known sizes and layer counts to ensure reproducible results across different environments.

## How Spegel works

Understanding Spegel's architecture helps you troubleshoot and tune your deployment:

* **DaemonSet deployment**: Spegel runs on every Node as a local registry (port 5000).
* **Content advertisement**: Each Node periodically re-advertises its cached image layers to the cluster DHT. For the current advertisement time-to-live, see the [Spegel FAQ](https://spegel.dev/docs/faq/).
* **Registry mirroring**: When containerd pulls an image, it checks Spegel first (20ms timeout).
* **Peer discovery**: Spegel uses the Kademlia DHT to find which Nodes have the requested layers.
* **P2P transfer**: If found locally, layers stream from peer Nodes. Otherwise, layers fall back to the external registry.
* **Stateless operation**: No persistent storage. Spegel uses containerd's existing image cache.

> [!NOTE]
>
> **Timeout tuning**: The `mirrorResolveTimeout` (default 20ms) controls how long containerd waits for Spegel before falling back to external registries. Configure this through Helm:
>
> ```bash theme={"system"}
> helm upgrade --namespace spegel spegel oci://ghcr.io/spegel-org/helm-charts/spegel \
>   --set mirrorResolveTimeout=50ms
> ```
>
> Increase this value in high-latency environments, or decrease it if you prioritize pull speed over P2P cache hits. See the [Helm chart values.yaml](https://github.com/spegel-org/spegel/blob/main/charts/spegel/values.yaml) for all configurable options.

## Additional resources

* [Spegel documentation](https://spegel.dev/)
* [How Spegel works](https://spegel.dev/docs/overview/)
* [GitHub repository](https://github.com/spegel-org/spegel)
* [Verification guide](https://spegel.dev/docs/getting-started/#verify-deployment)
* [containerd registry mirror documentation](https://github.com/containerd/containerd/blob/main/docs/hosts.md)
* [About CKS](https://docs.coreweave.com/products/cks.md)
* [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md)
