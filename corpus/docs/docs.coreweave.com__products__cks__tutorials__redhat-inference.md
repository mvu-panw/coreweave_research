# Deploy Red Hat AI inference and llm-d

Source: https://docs.coreweave.com/products/cks/tutorials/redhat-inference

# Deploy Red Hat AI inference and llm-d

> Deploy Red Hat AI inference and llm-d on CoreWeave Kubernetes Service (CKS)

This tutorial shows you how to deploy the [Red Hat AI Inference Stack for Kubernetes](https://github.com/opendatahub-io/rhaii-on-xks) on CoreWeave Kubernetes Service (CKS). The stack provides GPU-based LLM inference using llm-d, KServe, Istio, and the Gateway API so you can run and serve models such as GPT-OSS on your CKS cluster.

In this tutorial, you'll:

* Deploy the Red Hat AI Inference Stack (`cert-manager`, Istio, LWS operator, and KServe) on your CKS cluster.
* Create and verify the inference gateway for routing requests to models.
* Deploy a hello-world model (GPT-OSS) and send a chat completion inference request.

> [card] What you'll need
>
> Before you start, you must have:
>
> * A [Red Hat Registry service account](https://access.redhat.com/terms-based-registry/) or Red Hat pull secret for `registry.redhat.io`.
> * A CoreWeave Kubernetes Service (CKS) cluster with GPU Nodes.
> * `kubectl` installed and configured to access your cluster.
> * `KUBECONFIG` set to an absolute path (required by the deployment scripts).

> [card] What you'll use
>
> You'll use these tools:
>
> * **git**: To clone the rhaii-on-xks repository.
> * **make**: To deploy components and run validation.
> * **jq**: To copy the Red Hat pull secret into namespaces (used in later steps).

## Prerequisites

Before you start, confirm that you've completed the following.

### Cluster readiness

Your cluster is ready. To verify the available GPU Nodes, run:

```bash theme={"system"}
kubectl describe nodes | grep -A5 "nvidia.com/gpu"
```

You should see one or more Nodes listed with GPU capacity in the output.

### Red Hat access token

You need a Red Hat pull secret so the cluster can pull images from `registry.redhat.io`. To get a Red Hat service account:

1. Go to [https://access.redhat.com/terms-based-registry/](https://access.redhat.com/terms-based-registry/).

2. Click **New Service Account**.

3. Create the account and note the username (for example, `12345678|myserviceaccount`).

4. On the **OpenShift Secret** tab, download the service account token.

5. Convert the service account token to JSON:

   ```bash theme={"system"}
   yq e '.data.".dockerconfigjson"' PULL-SECRET.yaml | base64 -d > auth.json
   ```

   Replace `PULL-SECRET.yaml` with your file name.

   The `auth.json` file should look like the following:

   ```json theme={"system"}
    {
    "auths": {
     "registry.redhat.io": {
       "auth": "MjAyOTk4MTd8Y29yZXdlY*******"
       }
      }
     }
   ```

6. Create the directory and copy `auth.json` to `~/.config/containers`:

   ```bash theme={"system"}
   mkdir -p ~/.config/containers
   cp ~/auth.json ~/.config/containers/auth.json
   ```

### KUBECONFIG

Ensure `KUBECONFIG` is set to an absolute path:

```bash theme={"system"}
export KUBECONFIG="$HOME/.kube/config"
```

## Clone the repository

Clone the Red Hat AI Inference Stack repository and change into its directory:

```bash theme={"system"}
git clone https://github.com/opendatahub-io/rhaii-on-xks.git
cd rhaii-on-xks
```

## Deploy prerequisites

Use `make` to deploy all stack components that llm-d depends on (`cert-manager`, Istio, LWS operator, and KServe):

```bash theme={"system"}
make deploy-all
```

When the deployment finishes, run:

```bash theme={"system"}
make status
```

You should see output similar to the following, with components in `Running` state and readiness checks passing:

```text title="Expected output after make status" theme={"system"}
== Deployment Status ===
cert-manager-operator:
NAME                                                        READY   STATUS    RESTARTS   AGE
cert-manager-operator-controller-manager-6d46d864cf-6dc7z   1/1     Running   0          2m24s

cert-manager:
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-699cdbb7db-nc9jv              1/1     Running   0          2m11s
...

=== Readiness Checks ===
-n cert-manager webhook:
Ready

=== API Versions ===
-n InferencePool API:
v1 (inference.networking.k8s.io)
-n Istio version:
v1.27-latest
-n Istio status:
Healthy

-n GatewayClass 'istio':
Available
```

For full deployment details, see the [Red Hat guide on configuring the inference gateway](https://github.com/opendatahub-io/rhaii-on-xks/blob/main/docs/deploying-llm-d-on-managed-kubernetes.md#4-configuring-the-inference-gateway).

## Create the inference gateway

Deploy the inference gateway so you can route requests to your models:

```bash theme={"system"}
./scripts/setup-gateway.sh
```

Verify the gateway is programmed:

```bash theme={"system"}
kubectl get gateways -A
```

You should see the `inference-gateway` in the `opendatahub` namespace with an `ADDRESS` and `PROGRAMMED` set to `True`:

```text title="Expected gateway output" theme={"system"}
NAMESPACE     NAME                CLASS   ADDRESS     PROGRAMMED   AGE
opendatahub   inference-gateway   istio   10.**.**    True         18m
```

## Deploy and test a sample model

After the gateway is running, you can deploy a model and send inference requests. This section uses the [redhat-inference example from the CoreWeave doc-examples repository](https://github.com/coreweave/doc-examples/tree/main/cks/redhat-inference).

### Set up the namespace

Create a namespace for the deployment. This example uses `llm-d-rhaii`:

```bash theme={"system"}
export NAMESPACE=llm-d-rhaii
kubectl create namespace $NAMESPACE
```

Copy the Red Hat pull secret into the namespace and configure the default service account to use it:

```bash theme={"system"}
kubectl get secret redhat-pull-secret -n istio-system -o json | \
  jq 'del(.metadata.resourceVersion, .metadata.uid, .metadata.creationTimestamp, .metadata.annotations, .metadata.labels) | .metadata.namespace = "'$NAMESPACE'"' | \
  kubectl create -f -

kubectl patch serviceaccount default -n $NAMESPACE \
  -p '{"imagePullSecrets": [{"name": "redhat-pull-secret"}]}'
```

### Download and deploy the model

Clone the following repository:

```bash theme={"system"}
git clone https://github.com/coreweave/doc-examples.git
```

Navigate to the `redhat-inference` directory:

```bash theme={"system"}
cd doc-examples/cks/redhat-inference
```

Deploy the following files:

```bash theme={"system"}
kubectl apply -f gpt-oss-pvc.yaml
kubectl apply -f download-job.yaml
```

After the download job completes, deploy the model:

```bash theme={"system"}
kubectl apply -f deploy.yaml
```

### Send an inference request

In a separate terminal, port-forward the inference gateway:

```bash theme={"system"}
kubectl port-forward svc/inference-gateway-istio 8080:80 -n opendatahub
```

Send a chat completion request to the endpoint:

```bash theme={"system"}
curl http://localhost:8080/llm-d-rhaii/gpt-oss/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 50
  }'
```

You should receive a JSON response with the model output similar to the following:

```json title="Expected response" theme={"system"}
{"id":"chatcmpl-d66c36e3-3d96-4aa9-919d-***","object":"chat.completion","created":1773440761,"model":"openai/gpt-oss-120b","choices":[{"index":0,"message":{"role":"assistant","content":"Hello! How can I assist you today?","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":"The user says \"Hello!\". Probably just a greeting. The assistant should respond with a friendly greeting and perhaps ask how can I help."},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":71,"total_tokens":119,"completion_tokens":48,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
```

You've now deployed and tested a model with the Red Hat AI Inference Stack.

## Next steps

* [Deploy an open source LLM on CKS](https://docs.coreweave.com/products/cks/deploy-model.md) for a full walkthrough of creating a cluster, node pool, and serving a model with Open WebUI.
* [Deploy vLLM for inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md) to run another inference stack with monitoring, autoscaling, and Prometheus or Grafana.
* [Observability overview](https://docs.coreweave.com/observability.md) to add monitoring, metrics, and logging for your inference workloads.
* [Nodes and node pools](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md) to scale GPU capacity or adjust node pool configuration.
* [Secrets](https://docs.coreweave.com/products/cks/clusters/secrets.md) to manage image pull secrets and other sensitive configuration in your cluster.
