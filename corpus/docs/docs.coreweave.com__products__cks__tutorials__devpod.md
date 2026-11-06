# Deploy development environments with DevPod

Source: https://docs.coreweave.com/products/cks/tutorials/devpod

# Deploy development environments with DevPod

> Create development environments with DevPod using CKS resources

[DevPod](https://devpod.sh/) lets you create development environments by running Pods on your existing CKS resources. This tutorial teaches you how to set up and use DevPod for both basic and Docker-enabled development environments, so you can develop directly against cluster resources without provisioning separate infrastructure. It's intended for developers who already have access to a CKS cluster and a Virtual Server.

In this tutorial, you:

1. **Learn how DevPod integrates with CKS** to create development environments.
2. **Set up DevPod on CKS** using either:
   * **[Basic setup without Docker](#basic-setup-without-docker)**: A basic development environment without Docker, suitable for most development tasks.
   * **[Advanced setup with Docker](#advanced-setup-with-docker)**: A development environment with Docker support, enabling containerized development.
3. **Access and verify your development environment** using both SSH and web-based interfaces.
4. **Understand how to manage and clean up** DevPod workspaces.

> [card] What you'll need
>
> Before you start, you must have:
>
> * A CKS cluster with available CPU or GPU resources.
> * `kubectl` installed and configured to access your CKS cluster.
> * A Virtual Server with access to your CKS cluster.
> * DevPod CLI installed on your Virtual Server.

> [card] What you'll use
>
> You'll use these tools and technologies:
>
> * **DevPod CLI**: For creating and managing development environments.
> * **Kubernetes Pod manifests**: For defining your development environment configuration.
> * **PyTorch container image**: As the base development environment.
> * **Docker-in-Docker (DinD)**: For Docker-enabled environments (advanced setup).
> * **VS Code**: For development (either the browser-based or the desktop version).

## Know before you go

### Key concepts

* **DevPod**: A tool that creates development environments as Kubernetes Pods so you can develop directly on your CKS cluster resources.
* **Pod manifest template**: A Kubernetes Pod specification that DevPod uses to create your development environment.
* **Docker-in-Docker (DinD)**: A sidecar container that provides Docker functionality within your development environment.

> [!NOTE]
>
> The DevPod CLI assumes that `kubectl` is in your `PATH`, and that the `kubectl` context is set to the cluster you want to use.

### Environment setup and assumptions

* **SUNK environment**: The examples in this tutorial assume [a SUNK environment](https://docs.coreweave.com/products/sunk.md) for toleration specification. If you aren't using a SUNK environment, adjust the toleration specification accordingly.
* **PyTorch base image**: You use a PyTorch image as the base image, regardless of whether you're using CPU or GPU resources.
* **Namespace organization**: Use the `devpod` namespace to keep your DevPod environments organized. This is the default namespace for the Kubernetes provider in DevPod.

> [!TIP]
>
> Although Pods require elevated privileges to function properly, you don't need additional, cluster-wide permissions beyond what's typically granted to users. This means you can set up your development environment securely without providing administrative access.

## Install the DevPod CLI

Install the DevPod CLI on your Virtual Server by following the [DevPod installation guide](https://devpod.sh/docs/getting-started/install#install-devpod-cli). The DevPod CLI must be installed and running on a Virtual Server that has access to your CKS cluster, because DevPod uses the local `kubectl` context to provision Pods.

## Select a setup path

With the CLI installed, choose the configuration that matches your development needs:

* **[Basic setup without Docker](#basic-setup-without-docker)**: A basic development environment without Docker, suitable for most development tasks.
* **[Advanced setup with Docker](#advanced-setup-with-docker)**: A development environment with Docker support, enabling containerized development.

> [!TIP]
>
> For most development tasks, use the basic setup.

## Basic setup without Docker

If your development environment doesn't require Docker, use this configuration.

### 1. Create the configuration files

First, create a directory for your DevPod configuration files. Then, create the following example configuration files:

* [`pod_manifest_template.yaml`](#create-the-pod-manifest-template): A Kubernetes Pod manifest that DevPod uses as a template to provision your development environment.
* [`run_demo_gpu_cwsa.sh`](#create-the-setup-script): A script that creates and starts your DevPod environment.
* [`.devcontainer/devcontainer.json`](#create-the-devcontainer-configuration): A configuration file for the DevContainer IDE.

In this tutorial, the files are stored in `~/devpod-gpu-sidecar/`.

#### Create the Pod manifest template

Create a file named `pod_manifest_template.yaml` with the following content:

```yaml title="pod_manifest_template.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  namespace: devpod
spec:
  tolerations:
  - key: sunk.coreweave.com/nodes
    operator: Exists
  - key: is_cpu_compute
    operator: Exists
  containers:
  - name: devpod
    image: pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime
    volumeMounts:
    - name: shared-tools
      mountPath: /shared
    securityContext:
      privileged: true
  volumes:
  - name: shared-tools
    emptyDir: {}
```

In this example manifest:

* The `pod_manifest_template.yaml` file defines a Kubernetes Pod manifest that DevPod uses as a template to provision your development environment.
* The Pod is created in the `devpod` namespace to keep DevPod resources logically separated from other workloads.
* The manifest specifies tolerations for both `sunk.coreweave.com/nodes` and `is_cpu_compute` [Node labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md) so the Pod can be scheduled on Nodes with these taints.
* The **primary** container uses the `pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime` image, mounts a shared `emptyDir` volume at `/shared`, and runs in a [privileged security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to enable advanced development workflows that require elevated permissions.

#### Create the setup script

Next, create a file named `run_demo_gpu_cwsa.sh` with the following content:

```bash title="run_demo_gpu_cwsa.sh" theme={"system"}
#!/bin/bash

# Create namespace if it doesn't exist
kubectl create namespace devpod --dry-run=client -o yaml | kubectl apply -f -

# Configure DevPod provider
devpod provider use kubernetes
devpod provider set-options kubernetes -o POD_MANIFEST_TEMPLATE="$(pwd)/pod_manifest_template.yaml"

# Set resource requirements. Adjust these based on your needs.
# For CPU-only environments, remove the GPU limits line
devpod provider set-options kubernetes -o RESOURCES="requests.cpu=16,requests.memory=32Gi,limits.nvidia.com/gpu=8"
devpod provider set-options kubernetes -o DISK_SIZE="100Gi"
devpod provider set-options kubernetes -o KUBERNETES_PULL_SECRETS_ENABLED="false"
devpod provider set-options kubernetes -o STRICT_SECURITY="true"

# Start the DevPod environment
# The debug flag is optional, but recommended until the script is
# verified to be working properly
devpod up . --debug --ide openvscode
```

> [!TIP]
>
> This tutorial explicitly specifies the `openvscode` IDE to ensure consistent behavior. This provides a browser-based VS Code interface, which is why you see `openvscode` in the IDE column when you run `devpod ls`.

#### Create the `.devcontainer` configuration

Create a `.devcontainer` directory, then add a `devcontainer.json` file with the following content:

```json title=".devcontainer/devcontainer.json" theme={"system"}
{
    "name": "DevPod"
}
```

### 2. Start the DevPod environment

Run the setup script to start your DevPod environment:

```bash theme={"system"}
chmod +x run_demo_gpu_cwsa.sh
./run_demo_gpu_cwsa.sh
```

Leave this terminal window open. After the script is running, cancel it with `Ctrl+C`. Remove the debug flag in the script after you've verified that the setup works properly.

Monitor the Pod status to ensure the container is ready:

```bash theme={"system"}
kubectl get pods -n devpod -o wide
```

The output should look similar to:

```text theme={"system"}
NAME                      READY   STATUS    RESTARTS   AGE    IP           NODE      NOMINATED NODE   READINESS GATES
devpod-default-de-c24f8   2/2     Running   0          127m   10.0.87.91   g778056   <none>           <none>
```

> [!TIP]
>
> **Troubleshooting Pod creation**
>
> If the Pod fails to start, verify the following:
>
> * Your CKS cluster has sufficient resources.
> * Your `kubectl` context is set to the correct cluster.
> * The tolerations in the Pod manifest match your cluster configuration.
> * The targeted namespace exists, and you have permissions to create Pods in it.

### 3. Access your DevPod environment

Open another terminal in your Virtual Server, then list your DevPod workspaces using `devpod ls`:

```bash theme={"system"}
devpod ls
```

The output should look similar to the following:

```text theme={"system"}
           NAME        |                 SOURCE                 | MACHINE |  PROVIDER  |    IDE     | LAST USED |   AGE   |  PRO
  ---------------------+----------------------------------------+---------+------------+------------+-----------+---------+--------
    devpod-gpu-sidecar | local:/home/gabrams/devpod-gpu-sidecar |         | kubernetes | openvscode | 2h6m13s   | 2h6m47s | false
```

Next, connect to your DevPod environment using `devpod ssh`:

```bash theme={"system"}
devpod ssh devpod-gpu-sidecar
```

> [!NOTE]
>
> **IDE access**
>
> When you run `devpod ssh`, DevPod automatically opens a browser-based VS Code IDE in your Virtual Server's browser. This happens because the workspace is configured to use `openvscode` as the IDE (as shown in the `devpod ls` output).
>
> If the browser-based IDE doesn't open automatically:
>
> * Ensure your Virtual Server has a browser installed and accessible.
> * Check that the DevPod workspace runs properly.
> * You can also access the IDE manually by running `devpod open` in a separate terminal.
>
> Alternatively, [use the full VS Code IDE](#use-the-full-vs-code-ide).

### 4. Verify GPU access

Because PyTorch is the base image, `nvidia-smi` works on GPU systems. Use this to verify GPU access:

```bash theme={"system"}
nvidia-smi
```

> [!TIP]
>
> **Troubleshooting GPU access**
>
> If `nvidia-smi` doesn't work:
>
> * Verify your cluster has GPU Nodes available.
> * Check that the GPU limits are set correctly in the resources configuration.
> * Ensure the PyTorch image includes CUDA support (this is the default).
> * Verify the Pod is scheduled on a GPU Node by running `kubectl get pods -n devpod -o wide`.

You now have a basic DevPod environment running on your CKS cluster, accessible through SSH and a browser-based VS Code IDE.

## Advanced setup with Docker

If your development environment requires Docker, use this advanced configuration, which includes a Docker-in-Docker (DinD) [sidecar container](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/).

### 1. Create the Docker-enabled configuration files

#### Create the Pod manifest template with Docker sidecar

Create a file named `pod_manifest_template.yaml` with the following content:

```yaml title="pod_manifest_template.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  namespace: devpod
spec:
  tolerations:
  - key: sunk.coreweave.com/nodes
    operator: Exists
  - key: is_cpu_compute
    operator: Exists
  containers:
  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    args:
      - "--host=tcp://0.0.0.0:2375"
      - "--tls=false"
    volumeMounts:
    - name: docker-graph-storage
      mountPath: /var/lib/docker
    - name: devpod
      mountPath: /workspace
      subPath: dind-workspace
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
  - name: devpod
    image: pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime
    volumeMounts:
    - name: shared-tools
      mountPath: /shared
    env:
    - name: DOCKER_HOST
      value: "tcp://localhost:2375"
    securityContext:
      privileged: true
  volumes:
  - name: docker-graph-storage
    emptyDir: {}
  - name: shared-tools
    emptyDir: {}
```

This example manifest does the following:

* The `pod_manifest_template.yaml` file defines a Kubernetes Pod manifest that DevPod uses as a template to provision your development environment.
* The Pod is created in the `devpod` namespace to keep DevPod resources logically separated from other workloads.
* The manifest specifies tolerations for both `sunk.coreweave.com/nodes` and `is_cpu_compute` [Node labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md) so the Pod can be scheduled on Nodes with these taints.
* The **primary** container uses the `pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime` image, mounts a shared `emptyDir` volume at `/shared`, and runs in a [privileged security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to enable advanced development workflows that require elevated permissions.
* The manifest configures a [Docker-in-Docker (DinD)](https://hub.docker.com/_/docker) sidecar container (`containers.dind`) so the primary container can run Docker commands inside the Pod.
* The DinD container exposes the Docker daemon on `tcp://0.0.0.0:2375` without TLS and disables Docker's default TLS certificate directory for easier local development.
* The `devpod` container sets the `DOCKER_HOST` environment variable to connect to the DinD sidecar, which enables Docker CLI usage.
* Both containers mount a shared workspace volume (`devpod`) so files can be accessed between the DinD and primary containers.
* The manifest uses `emptyDir` volumes for both Docker storage and shared tools to provide ephemeral, fast local storage within the Pod.
* Both containers run in privileged mode, which is required for Docker-in-Docker and some advanced development workflows, but should be used with caution in production environments.

#### Create the setup script with Docker

Create a file named `run_demo_gpu_cwsa.sh` with the following content:

```bash title="run_demo_gpu_cwsa.sh" theme={"system"}
#!/bin/bash

# Create namespace if it doesn't exist
kubectl create namespace devpod --dry-run=client -o yaml | kubectl apply -f -

# Clean up any existing workspace
devpod delete devpod-gpu-sidecar

# Configure DevPod provider
devpod provider use kubernetes
devpod provider set-options kubernetes -o POD_MANIFEST_TEMPLATE="$(pwd)/pod_manifest_template.yaml"

# Set resource requirements. Adjust these based on your needs.
# For CPU-only environments, remove the GPU limits line
devpod provider set-options kubernetes -o RESOURCES="requests.cpu=16,requests.memory=32Gi,limits.nvidia.com/gpu=8"
devpod provider set-options kubernetes -o DISK_SIZE="100Gi"
devpod provider set-options kubernetes -o KUBERNETES_PULL_SECRETS_ENABLED="false"
devpod provider set-options kubernetes -o STRICT_SECURITY="true"

# Start the DevPod environment
# The debug flag is optional, but recommended until the script is
# verified to be working properly
devpod up . --debug --ide openvscode
```

> [!TIP]
>
> **IDE configuration**
>
> This tutorial explicitly specifies the `openvscode` IDE to ensure consistent behavior. This provides a browser-based VS Code interface, which is why you see `openvscode` in the IDE column when you run `devpod ls`.

#### Create the devcontainer configuration

Create a `.devcontainer` directory, then add a `devcontainer.json` file:

```json title=".devcontainer/devcontainer.json" theme={"system"}
{
    "name": "DinD"
}
```

### 2. Start the DevPod environment with Docker

Run the setup script to start your DevPod environment:

```bash theme={"system"}
chmod +x run_demo_gpu_cwsa.sh
./run_demo_gpu_cwsa.sh
```

Leave this terminal window open until the script is running, then cancel it with `Ctrl+C`. After you've verified that the setup works properly, remove the debug flag from the script.

Monitor the Pod status to ensure both containers are ready:

```bash theme={"system"}
kubectl get pods -n devpod -o wide
```

The output should look similar to the following:

```text theme={"system"}
NAME                      READY   STATUS    RESTARTS   AGE    IP           NODE      NOMINATED NODE   READINESS GATES
devpod-default-de-c24f8   2/2     Running   0          127m   10.0.87.91   g778056   <none>           <none>
```

### 3. Access your DevPod environment

Open another terminal in your Virtual Server, then list your DevPod workspaces using `devpod ls`:

```bash theme={"system"}
devpod ls
```

The output should look similar to:

```text theme={"system"}
           NAME        |                 SOURCE                 | MACHINE |  PROVIDER  |    IDE     | LAST USED |   AGE   |  PRO
  ---------------------+----------------------------------------+---------+------------+------------+-----------+---------+--------
    devpod-gpu-sidecar | local:/home/gabrams/devpod-gpu-sidecar |         | kubernetes | openvscode | 2h6m13s   | 2h6m47s | false
```

Connect to your DevPod environment using `devpod ssh`:

```bash theme={"system"}
devpod ssh devpod-gpu-sidecar
```

> [!NOTE]
>
> **IDE access**
>
> When you run `devpod ssh`, DevPod automatically opens a browser-based VS Code IDE in your Virtual Server's browser. This happens because the workspace is configured to use `openvscode` as the IDE (as shown in the `devpod ls` output).
>
> If the browser-based IDE doesn't open automatically:
>
> * Ensure your Virtual Server has a browser installed and accessible.
> * Check that the DevPod workspace runs properly.
> * You can also access the IDE manually by running `devpod open` in a separate terminal.
>
> Alternatively, [use the full VS Code IDE](#use-the-full-vs-code-ide).

### 4. Install Docker CLI

Use `apt` to install the Docker CLI that connects to the Docker sidecar. This is required to run Docker commands from the primary container.

```bash theme={"system"}
sudo -i
apt update
apt upgrade
apt install docker.io
exit
```

### 5. Verify Docker connection

Test that Docker works and connects to the sidecar container by running `docker ps`:

```bash theme={"system"}
docker ps
```

You should see an empty list of containers, which indicates that Docker connects to the sidecar but no containers are running yet.

Test Docker by running a basic container using `docker run hello-world`:

```bash theme={"system"}
docker run --rm hello-world
```

This command downloads and runs a test container to verify that Docker can pull images and run containers through the sidecar connection.

> [!TIP]
>
> **Troubleshooting Docker connection**
>
> If you can't connect to Docker from the main container:
>
> * Verify the sidecar container is running:
>
>   ```bash theme={"system"}
>   kubectl get pods -n devpod -o wide
>   ```
>
> * Check that the `DOCKER_HOST` environment variable is set correctly.
>
> * Ensure the Docker daemon runs in the sidecar container.
>
> * Check the sidecar container logs. Replace `[POD-NAME]` with the Pod name from the previous command:
>
>   ```bash theme={"system"}
>   kubectl logs -n devpod [POD-NAME] -c dind
>   ```

### 6. Verify GPU access

Because PyTorch is the base image, `nvidia-smi` should work on GPU systems. Run `nvidia-smi` to verify GPU access:

```bash theme={"system"}
nvidia-smi
```

You now have a Docker-enabled DevPod environment running on your CKS cluster, with a DinD sidecar that lets you build and run containers from inside the workspace.

## Install full Docker with buildx support

If you need multi-platform image builds or other features beyond the basic `docker.io` package, install the full Docker Engine with buildx support. Follow the official Docker installation steps:

Update the package index:

```bash theme={"system"}
sudo apt-get update
```

Install packages to allow apt to use a repository over HTTPS:

```bash theme={"system"}
sudo apt-get install ca-certificates curl gnupg -y
```

Add Docker's official GPG key to the Apt keyring:

```bash theme={"system"}
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

Add the repository to Apt sources:

```bash theme={"system"}
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package index again to pick up the new repository:

```bash theme={"system"}
sudo apt-get update
```

Install Docker Engine and its associated plugins:

```bash theme={"system"}
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

## Use the full VS Code IDE

If you prefer the desktop VS Code application over the browser-based `openvscode` IDE, you can switch the DevPod workspace to use it. To use the full VS Code IDE for either setup path, first ensure VS Code is installed on the same local client that starts the DevPod. Then, modify your `run_demo_gpu_cwsa.sh` file to include the following changes for either setup path.

```bash title="run_demo_gpu_cwsa.sh" theme={"system"}
#!/bin/bash

# Create namespace if it doesn't exist
kubectl create namespace devpod --dry-run=client -o yaml | kubectl apply -f -

# Clean up any existing workspace
devpod delete devpod-gpu-sidecar

# Configure DevPod provider
devpod provider use kubernetes
devpod provider set-options kubernetes -o POD_MANIFEST_TEMPLATE="$(pwd)/pod_manifest_template.yaml"
devpod provider set-options kubernetes -o RESOURCES="requests.cpu=16,requests.memory=32Gi,limits.nvidia.com/gpu=8"
devpod provider set-options kubernetes -o DISK_SIZE="100Gi"
devpod provider set-options kubernetes -o KUBERNETES_PULL_SECRETS_ENABLED="false"
devpod provider set-options kubernetes -o STRICT_SECURITY="true"

# Configure context to prevent timeout
devpod context set-options -o EXIT_AFTER_TIMEOUT=false

# Start the DevPod environment with VS Code IDE
devpod up . --debug --ide vscode
```

Run the modified script:

```bash theme={"system"}
./run_demo_gpu_cwsa.sh
```

Open VS Code, then connect to the DevPod workspace using `devpod open`.

```bash theme={"system"}
devpod open
```

## Clean up

When you're finished with your DevPod environment, remove it to free cluster resources. Delete the workspace using `devpod delete`:

```bash theme={"system"}
devpod delete devpod-gpu-sidecar
```

To clean up the namespace and all resources, run `kubectl delete namespace`:

```bash theme={"system"}
kubectl delete namespace devpod
```

## Additional resources

* [DevPod official documentation: Installation](https://devpod.sh/docs/getting-started/install)
* [DevPod official documentation: Workspace management](https://devpod.sh/docs/developing-in-workspaces/what-are-workspaces)
