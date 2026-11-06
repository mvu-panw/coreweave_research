# Deploy an open source LLM on CKS

Source: https://docs.coreweave.com/products/cks/deploy-model

# Deploy an open source LLM on CKS

> Step-by-step guide for deploying Meta's Llama 3.1 model on CKS with cluster and Node Pool setup

This tutorial walks you through deploying Meta's Llama 3.1 8B Instruct open source LLM on CoreWeave Kubernetes Service (CKS), so you can run inference against a hosted model from your own cluster. It's for developers and ML practitioners who are new to CKS and want a complete, end-to-end example of provisioning GPU infrastructure and serving a model.

> [!WARNING]
>
> Keep Open WebUI authentication enabled. Never set `WEBUI_AUTH` to `"false"` when Open WebUI is exposed to the internet. Disabling authentication lets anyone who can reach the service access Open WebUI and use your model. Publicly exposed instances with authentication disabled have been compromised and used to deploy cryptominers.

Before deploying, set `WEBUI_AUTH` to `"true"` in the example manifest. Use the localhost port-forward in this guide to create your administrator account before exposing the service publicly.

You'll complete the following steps:

* Create a cluster in CKS.
* Create a Node Pool.
* Connect to your cluster and schedule a GPU Pod using `kubectl`.
* Deploy and interact with an LLM using [Open WebUI](https://docs.openwebui.com/).

## Before you begin

Before completing the steps in this guide, you must have the following:

* `kubectl` installed on your machine. `kubectl` is the command-line tool for interacting with Kubernetes clusters. If needed, see the [kubectl installation instructions](https://kubernetes.io/docs/tasks/tools/).
* Access to the CoreWeave Cloud Console. For more information, see [Activate and sign in to your CoreWeave organization](https://docs.coreweave.com/security/authn-authz/activate-org.md).
* A Hugging Face access token. See the Hugging Face instructions at [User access tokens](https://huggingface.co/docs/hub/en/security-tokens). Be sure to copy and store the token in a secure location. You will need it later in this guide.
* Access to the `Llama-3.1-8B-Instruct` model at Hugging Face. Go to [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) and request access. Note that approval for restricted models can take a few hours or longer.

> [!WARNING]
>
> **Cost and security disclaimer**
>
> * Using resources, such as compute, incurs charges. Monitor your resource usage to avoid unexpected charges.
> * CoreWeave is not responsible for the security of the Llama model provided by Hugging Face or the Open Web UI container image.

## Create a CKS cluster and Node Pool

CKS clusters and Node Pools are the core infrastructure for running and managing workloads. To create a cluster and Node Pool, complete the following steps:

**1. Open the Clusters page**

Log in to the Cloud Console and navigate to the [Clusters](https://console.coreweave.com/clusters) page.

**2. Create Cluster**

Click the **Create Cluster** button.

**3. Name the cluster and enable API access**

In the **Create a Cluster** dialog, give the cluster a name, select the latest Kubernetes version, and verify the box is checked for **Enable access to the Kubernetes API via the Internet**. Click **Next**.

![Create a cluster in the console.](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/create-a-cluster.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=c2d4786ebeeff339fe47080fcc6cf8ce)

**4. Select a region with GPU quota**

Create the cluster where you have GPU quota available. Verify the box is checked for **Create a default VPC**, and then click **Next**.

![Select the region where you have GPU quota.](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/gpu-quota.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=7eb268af32f9455189ab76bda84a4ea6)

**5. Skip authentication options**

Leave the authentication boxes unchecked and click **Next**.

![Cluster authentication options in the create cluster flow.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/products/cks/_media/auth.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=2ca76f5a68e2b3894564406ab2942f8c)

**6. Submit the cluster**

On the deploy page, click **Submit**.

**7. Create a Node Pool**

On the **Success!** dialog box, click **Create a Node Pool**.

**8. Configure the Node Pool**

Verify the cluster you just created is selected, and do the following:

* Name the Node Pool.
* Pick a GPU instance.
* Set **Target Nodes** to `1`.
* Leave all other fields empty.
* Click **Submit**.

Node Pool creation can be delayed while the cluster is being created. Then, Node Pool provisioning can take up to 15 minutes. When the Node Pool status is `Healthy`, your cluster has GPU capacity ready to serve the model, and you can continue to the following steps.

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.

## Generate a CoreWeave access token

Access tokens let you authenticate to your Kubernetes resources through `kubectl`. You must create one for the cluster you just provisioned before you can run commands against it.

To create an access token, complete the following steps:

**1. Open the Tokens page**

In the Cloud Console, navigate to the [Tokens](https://console.coreweave.com/tokens) page and click the **Create Token** button.

**2. Name the token and set an expiration**

Enter a name and expiration and then click **Create**.

**3. Select the cluster and download**

In the **Create API Token** dialog, select the cluster you just created from the **Select current-context** dropdown menu, and then click **Download**.

![Create API Token dialog with current-context and download.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/products/cks/_media/access-tokens.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=a62c696026e2db334dad98ff64cac470)

## Use `kubectl` with your cluster

To communicate with your cluster using `kubectl`, complete the following steps:

**1. Set the KUBECONFIG environment variable**

Make a `KUBECONFIG` environment variable that points to the `kubeconfig` file you just downloaded. Replace `[CW-KUBECONFIG-FILENAME]` with the name of the file you downloaded in the previous step:

```bash theme={"system"}
export KUBECONFIG=~/Downloads/[CW-KUBECONFIG-FILENAME]
```

**2. Confirm the connection**

Confirm you can connect to the cluster with the following command:

```bash theme={"system"}
kubectl cluster-info
```

You should see cluster information like the following:

```text theme={"system"}
Kubernetes Control Plane is running at https://****.k8s.us-east-02a.coreweave.com
CoreDNS is running at https://****.k8s.us-east-02a.coreweave.com/api/v1/namespaces/kube-system/services/coredns:dns/proxy
node-local-dns is running at https://****.k8s.us-east-02a.coreweave.com/api/v1/namespaces/kube-system/services/node-local-dns:dns/proxy
```

## Schedule a GPU Pod

A GPU Pod requests GPU resources with `nvidia.com/gpu` and selects an instance type with the `node.coreweave.cloud/type` Node label. Before deploying the model, run a Pod that checks whether it can access a GPU.

Use the instance type you provisioned in your Node Pool:

| GPU instance | `node.coreweave.cloud/type` value |
| :- | :- |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | `gd-8xh100ib-i128` |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) | `b200-8x` |
| [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | `rtxp6000-8x` |

The instance type identifies the hardware on the Node. The GPU resource request determines how many GPUs the container receives. These instances each have eight GPUs, but the following Pod requests only one.

**1. Save the GPU Pod manifest**

Save the following manifest as `gpu-check.yaml`. The example selects an H100 Node. For B200 or RTX PRO 6000, replace `gd-8xh100ib-i128` with the corresponding value from the table.

```yaml title="gpu-check.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: gpu-check
spec:
  restartPolicy: Never
  nodeSelector:
    node.coreweave.cloud/type: gd-8xh100ib-i128
  containers:
    - name: gpu-check
      image: nvidia/cuda:12.8.1-base-ubuntu22.04
      command: ["nvidia-smi"]
      resources:
        requests:
          nvidia.com/gpu: 1
        limits:
          nvidia.com/gpu: 1
```

When you specify both GPU `requests` and `limits`, their values must be equal. A `nodeSelector` restricts the Pod to Nodes with the matching label. It doesn't provision a Node or reserve a GPU by itself. For more detail, see [Target specific GPUs or CPUs](https://docs.coreweave.com/products/cks/nodes/manage.md#target-specific-gpus-or-cpus).

**2. Apply the manifest and check GPU access**

Create the Pod and check its status:

```bash theme={"system"}
kubectl apply -f gpu-check.yaml
kubectl get pod gpu-check -o wide
```

When the GPU check succeeds, its status is `Completed`. Read its output:

```bash theme={"system"}
kubectl logs gpu-check
```

The `nvidia-smi` output lists the GPU available to the container, including its name and driver version.

If the Pod stays `Pending`, inspect its events:

```bash theme={"system"}
kubectl describe pod gpu-check
```

Check that your Node Pool is healthy, its instance type matches the selector, and a matching Node has a free GPU. For more scheduling guidance, see [Workload scheduling](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md).

**3. Remove the test Pod**

Delete the completed Pod before continuing to the model deployment:

```bash theme={"system"}
kubectl delete pod gpu-check
```

## Create a Hugging Face secret

For CKS to download the `llama-3.1-8B-Instruct` model from Hugging Face, you must create a Kubernetes secret that holds your Hugging Face access token. The model deployment in the next section reads this secret at runtime to authenticate with Hugging Face.

Complete the following steps to create the secret:

**1. Create the secret**

Run the following command to create a Hugging Face secret:

```bash theme={"system"}
kubectl create secret generic hf-token-secret --from-literal=api_token=[HUGGING-FACE-TOKEN]
```

* `[HUGGING-FACE-TOKEN]`: This is the token Hugging Face provides you. For more information about creating a Hugging Face token, see [User access tokens](https://huggingface.co/docs/hub/en/security-tokens).

## Download and apply a YAML configuration file

Kubernetes uses YAML files to configure resources. The [example manifest](https://raw.githubusercontent.com/coreweave/doc-examples/refs/heads/main/cks/llm-on-cks.yaml) defines four resources that together deploy the model and a chat interface, so you can create them all with a single command:

* **`llama-3-1-8b-deployment`** runs the model. Its `vllm-server` container starts the [vLLM](https://docs.vllm.ai/en/latest/) inference server with `vllm serve`, loads the model named in the `MODEL` environment variable (`meta-llama/Llama-3.1-8B-Instruct`), and reads your Hugging Face token from the `hf-token-secret` you created. The container requests one GPU and mounts a 2Gi `/dev/shm` volume that vLLM uses for shared memory.
* **`llama-3-1-8b-svc`** is a `ClusterIP` Service that exposes the model inside the cluster on port `11434` and forwards to the container's port `8000`. Open WebUI reaches the model through this Service at `http://llama-3-1-8b-svc:11434/v1`.
* **`open-webui`** runs the [Open WebUI](https://docs.openwebui.com/) chat interface. Its environment variables point it at the model Service, so the UI sends inference requests to the deployed model.
* **`open-webui-svc`** is a `ClusterIP` Service that exposes Open WebUI inside the cluster on port `80` and forwards to the container's port `8080`.

Both Services use the default `ClusterIP` type, so they're reachable only from inside the cluster. Later steps use `kubectl port-forward` to reach Open WebUI from your machine. To expose it on the internet instead, see [Expose Open WebUI publicly](#expose-open-webui-publicly-optional).

> [!NOTE]
>
> The `vllm-server` container uses the `ghcr.io/coreweave/ml-containers/vllm-tensorizer` image, which CoreWeave builds in the [`ml-containers`](https://github.com/coreweave/ml-containers) repository. It packages the open source [vLLM](https://github.com/vllm-project/vllm) inference server on CoreWeave's CUDA and PyTorch base image and integrates CoreWeave's [tensorizer](https://github.com/coreweave/tensorizer) library for fast model loading from storage.

The model container and test Pod both set `nvidia.com/gpu: 1` under `requests` and `limits`. Add the same instance selector to the model Deployment so its Pods use your chosen hardware.

To deploy the `Llama-3.1-8B-Instruct` model, complete the following steps:

**1. Download the manifest**

Download the manifest so you can configure authentication and select the hardware before deploying:

```bash theme={"system"}
curl -fsSL https://raw.githubusercontent.com/coreweave/doc-examples/refs/heads/main/cks/llm-on-cks.yaml -o llm-on-cks.yaml
```

**2. Enable Open WebUI authentication**

In the `llm-on-cks.yaml` file, set `WEBUI_AUTH` to `"true"` in the `open-webui` Deployment's container environment variables. Keep `ENABLE_SIGNUP` and `ENABLE_LOGIN_FORM` set to `"true"` for initial account setup:

```yaml title="Open WebUI environment excerpt" theme={"system"}
- name: WEBUI_AUTH
  value: "true"
- name: ENABLE_SIGNUP
  value: "true"
- name: ENABLE_LOGIN_FORM
  value: "true"
```

Keep `open-webui-svc` as a `ClusterIP` Service while you create the administrator account. Don't apply a manifest with `WEBUI_AUTH` set to `"false"`.

**3. Select the model GPU instance**

In the `llm-on-cks.yaml` file, add `nodeSelector` under `spec.template.spec` of `llama-3-1-8b-deployment`, alongside `volumes` and `containers`. Use the same instance type as the test Pod. The following excerpt selects an H100 Node:

```yaml title="Model Deployment excerpt" theme={"system"}
spec:
  template:
    spec:
      nodeSelector:
        node.coreweave.cloud/type: gd-8xh100ib-i128
```

Keep the existing Deployment fields, including the container's GPU `requests` and `limits`. For B200 or RTX PRO 6000, use the corresponding selector from [Schedule a GPU Pod](#schedule-a-gpu-pod). Add the selector only to the model Deployment. Open WebUI doesn't request a GPU.

**4. Apply the manifest**

Apply the edited local file:

> [!CAUTION]
>
> Before running the command, confirm you have access to the `Llama-3.1-8B` model. Visit the [`meta-llama/Llama-3.1-8B-Instruct` page](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) to verify your access.

```bash theme={"system"}
kubectl apply -f llm-on-cks.yaml
```

**5. Confirm the resources deployed**

Confirm Kubernetes deployed the resources by running the following commands:

```bash theme={"system"}
kubectl get pods
```

Verify all Pods are ready and running. The output should look like the following:

```text theme={"system"}
NAME                                       READY   STATUS    RESTARTS   AGE
llama-3-1-8b-deployment-77f4559f9f-wdvpj   1/1     Running   0          2m53s
open-webui-5b464664d8-942cg                1/1     Running   0          2m53s
```

> [!NOTE]
>
> **Pod creation time**
>
> Creating Pods can take up to five minutes.

**6. Verify the services are working**

Verify the services are working by running the following commands:

```bash theme={"system"}
kubectl logs [LLAMA-POD-NAME]
```

* `[LLAMA-POD-NAME]`: The Pod name beginning with `llama-*` that `kubectl get pods` returns.

* In the logs, look for the following line: `INFO:     Application startup complete.`

## Verify the model endpoint

The model runs an OpenAI-compatible inference server. Before you open Open WebUI, confirm the model responds to a chat completion request. The model Service (`llama-3-1-8b-svc`) is a `ClusterIP` Service, so you can only reach it from inside the cluster. The following command runs a temporary Pod that sends a request to the in-cluster Service:

```bash theme={"system"}
kubectl run curl-test --rm -i --restart=Never \
    --image=curlimages/curl -- \
    curl -s http://llama-3-1-8b-svc:11434/v1/chat/completions \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "meta-llama/Llama-3.1-8B-Instruct",
      "messages": [{"role": "user", "content": "What is CoreWeave in one sentence?"}],
      "max_tokens": 128
    }'
```

You should see a JSON response similar to the following:

```text theme={"system"}
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "CoreWeave is a cloud platform that provides GPU-accelerated infrastructure for AI, machine learning, and other compute-intensive workloads."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 19,
    "total_tokens": 78,
    "completion_tokens": 59
  }
}
```

A response with a `choices` array confirms the model is serving inference. If the request fails, recheck the Pod status and logs from the previous step before continuing.

## Get the Open WebUI endpoint

The Open WebUI service is not exposed to the internet. To access [Open WebUI](https://docs.openwebui.com/) from your machine, use port-forwarding:

**1. Start port-forwarding**

Run the following command to forward local port 8080 to the Open WebUI service:

```bash theme={"system"}
kubectl port-forward svc/open-webui-svc 8080:80
```

**2. Open the UI in your browser**

Leave the command running and open `http://localhost:8080` in your browser.

**3. Create your administrator account**

Through the localhost connection, create the first Open WebUI account, which becomes the administrator account. Use a strong, unique password. Before exposing the service publicly, complete account setup.

Sign out, then confirm that Open WebUI requires you to sign in before you can chat with the model. If you can access the chat without signing in, stop and check that `WEBUI_AUTH` is set to `"true"` in the `open-webui` Deployment.

The port-forward lets you access Open WebUI from your machine. Both Services remain accessible inside the cluster.

You should now see the Open WebUI site, where you can chat with the deployed Llama 3.1 model:

![Open WebUI site](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/open-webui.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=8eb001273ba48d507b46912f7263af82)

### Expose Open WebUI publicly (optional)

> [!WARNING]
>
> Never expose Open WebUI publicly with `WEBUI_AUTH` set to `"false"`. Anyone who can reach an unauthenticated instance can access Open WebUI and use your model. Exposed instances have been compromised and used to deploy cryptominers.

The port-forward provides local access without making the Service public. To expose Open WebUI publicly, complete the following steps:

**1. Verify authentication before public exposure**

Confirm that `WEBUI_AUTH` is set to `"true"` in the `open-webui` Deployment in `llm-on-cks.yaml`. If you changed the value, apply the edited manifest while `open-webui-svc` is still a `ClusterIP` Service:

```bash theme={"system"}
kubectl apply -f llm-on-cks.yaml
kubectl rollout status deployment/open-webui
```

Before exposing Open WebUI publicly, complete administrator account setup and the sign-in check in [Get the Open WebUI endpoint](#get-the-open-webui-endpoint).

**2. Change the Service to a public LoadBalancer**

In the manifest, set the Service `type` to `LoadBalancer` and add the CoreWeave public load balancer annotation:

```yaml theme={"system"}
apiVersion: v1
kind: Service
metadata:
  name: open-webui-svc
  annotations:
    service.beta.kubernetes.io/coreweave-load-balancer-type: public
spec:
  type: LoadBalancer
  selector:
    app: open-webui
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

**3. Reapply and get the external address**

Reapply the manifest, then get the Service's external address:

```bash theme={"system"}
kubectl apply -f llm-on-cks.yaml
kubectl get service open-webui-svc
```

The `coreweave-load-balancer-type: public` annotation provisions a public IP for the Service. For more detail, including how to assign a public DNS name, see [Expose a Service](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md).

## Use a different model

This guide deploys `Llama-3.1-8B-Instruct`, but the same manifest works for other models that vLLM serves. To deploy a different model, edit the [manifest](https://raw.githubusercontent.com/coreweave/doc-examples/refs/heads/main/cks/llm-on-cks.yaml) before you apply it:

**1. Change the model ID**

In the `llama-3-1-8b-deployment`, change the `MODEL` environment variable to the Hugging Face model ID you want to serve. If the model is gated, make sure the Hugging Face token in your `hf-token-secret` has access to it.

**2. Scale GPUs for larger models**

For a larger model that needs more than one GPU, raise `TENSOR_PARALLEL_SIZE` to the number of GPUs to shard the model across, and set the `nvidia.com/gpu` `requests` and `limits` to the same number. Choose a Node Pool GPU instance that provides those GPUs.

**3. Point Open WebUI at the model**

In the `open-webui` deployment, the `OPENAI_API_BASE_URL` environment variable points at the model Service (`http://llama-3-1-8b-svc:11434/v1`). Update it only if you rename the model Service or change its port.

> [!NOTE]
>
> The Deployment and Service names in the manifest, such as `llama-3-1-8b-svc`, are labels only. You can keep them as-is for any model, or rename them for clarity. If you rename the model Service, update the endpoint references in the `open-webui` deployment to match.

## Next steps

You've deployed an LLM on CKS and confirmed it serves inference. Consider these next steps:

* **Monitor your workload.** Use CoreWeave's managed Grafana to track GPU usage and model performance. See [Managed Grafana](https://docs.coreweave.com/observability/managed-grafana.md).
* **Scale your cluster.** Add Node autoscaling so capacity grows and shrinks with demand. See [Node autoscaling](https://docs.coreweave.com/products/cks/nodes/autoscaling.md).
* **Run batch and burst workloads.** Use CoreWeave SUNK to run Slurm on Kubernetes for training and HPC jobs. See [SUNK](https://docs.coreweave.com/products/sunk.md).
* **Manage infrastructure as code.** Provision clusters and Node Pools with Terraform. See [Terraform](https://docs.coreweave.com/platform/terraform.md).
* **Learn more about CKS clusters.** See [Introduction to clusters](https://docs.coreweave.com/products/cks/clusters/introduction.md).
* **Learn more about Node Pools.** See [Introduction to Node Pools](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md).
