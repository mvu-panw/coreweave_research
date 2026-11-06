# Hello world for NIM on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/hello-world-nims-on-cks

# Hello world for NIM on CKS

> Deploy an NVIDIA NIM on CoreWeave Kubernetes Service (CKS) and run your first inference request

In this tutorial, you deploy an [NVIDIA NIM](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/) on a CoreWeave Kubernetes Service (CKS) cluster. NIM microservices package optimized large language models (LLMs) as production-ready container images, which lets you serve GPU-accelerated inference without building a custom model server. This tutorial is for Kubernetes users who want to run LLM inference on CoreWeave. By the end, you have a running LLM inference endpoint and have queried it with the OpenAI-compatible chat completions API.

## Prerequisites

Before you start, you must have:

* A [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with at least one x86 (amd64) GPU node. NVIDIA NIM containers require x86 architecture. This tutorial uses an L40 GPU, but any NVIDIA GPU with 16 GB or more of VRAM works.
* [kubectl](https://kubernetes.io/docs/reference/kubectl/) installed and [connected to your cluster](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
* An [NVIDIA NGC](https://catalog.ngc.nvidia.com/) account and API key. To generate an API key, sign in to NGC and go to your **profile dropdown > Setup > API Keys**.

### Set your NGC API key

Export your NGC API key as an environment variable. The commands in this tutorial reference this variable when creating Kubernetes Secrets. Replace `[NGC-API-KEY]` with the API key you generated in the prerequisites.

```bash theme={"system"}
export NGC_API_KEY="[NGC-API-KEY]"
```

### Verify cluster access

Confirm that `kubectl` can reach your cluster and that GPU nodes are available:

```bash theme={"system"}
kubectl get nodes -o wide --no-headers | head -5
```

You should see output similar to the following:

```text theme={"system"}
g75d13e   Ready   <none>   209d   v1.32.4   10.176.196.197   <none>   Ubuntu 24.04.3 LTS   6.8.0-1022-nvidia-64k   containerd://1.7.2
```

Verify that at least one node has an NVIDIA GPU:

```bash theme={"system"}
kubectl describe nodes | grep -E "^Name:|nvidia.com/gpu:"
```

You should see output similar to the following, with at least one node showing `nvidia.com/gpu` in its capacity:

```text theme={"system"}
Name:               g75d13e
  nvidia.com/gpu:     1
```

## Create NGC secrets

NIM containers are hosted on NVIDIA's NGC registry (`nvcr.io`). To authenticate with NGC, you must create two Kubernetes Secrets: one to pull the container image, and one for the NIM runtime to download model weights.

```bash theme={"system"}
kubectl create secret docker-registry ngc-credentials \
    -n default \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password="$NGC_API_KEY"
```

You should see output similar to the following:

```text theme={"system"}
secret/ngc-credentials created
```

Create a second Secret to provide the NGC API key to the NIM runtime:

```bash theme={"system"}
kubectl create secret generic ngc-api-key \
    -n default \
    --from-literal=NGC_API_KEY="$NGC_API_KEY"
```

You should see output similar to the following:

```text theme={"system"}
secret/ngc-api-key created
```

With the Secrets in place, the cluster can authenticate to NGC to pull the NIM container image and download model weights.

## Deploy the NIM

With authentication configured, deploy the NIM itself. Save the following manifest as `nim-hello-world.yaml`. This manifest defines a single-replica Deployment with one GPU and a ClusterIP Service that exposes the inference API on port `8000`.

```yaml title="nim-hello-world.yaml" theme={"system"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nim-hello-world
  namespace: default
  labels:
    app: nim-hello-world
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nim-hello-world
  template:
    metadata:
      labels:
        app: nim-hello-world
    spec:
      nodeSelector:
        # Update this value to match an available GPU class in your cluster.
        # Run: kubectl get nodes -o jsonpath='{.items[*].metadata.labels.gpu\.nvidia\.com/class}'
        gpu.nvidia.com/class: L40
      imagePullSecrets:
        - name: ngc-credentials
      containers:
        - name: nim
          image: nvcr.io/nim/meta/llama3-8b-instruct:1.0.0
          ports:
            - containerPort: 8000
              name: http
          env:
            - name: NGC_API_KEY
              valueFrom:
                secretKeyRef:
                  name: ngc-api-key
                  key: NGC_API_KEY
          resources:
            limits:
              nvidia.com/gpu: 1
              cpu: "4"
              memory: "32Gi"
            requests:
              nvidia.com/gpu: 1
              cpu: "2"
              memory: "16Gi"
          volumeMounts:
            - name: nim-cache
              mountPath: /opt/nim/.cache
          readinessProbe:
            httpGet:
              path: /v1/health/ready
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /v1/health/live
              port: 8000
            initialDelaySeconds: 300
            periodSeconds: 15
      volumes:
        - name: nim-cache
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: nim-hello-world
  namespace: default
spec:
  selector:
    app: nim-hello-world
  ports:
    - name: http
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

> [!NOTE]
>
> If your cluster uses a different GPU type, adjust the `nodeSelector` to match. Use `kubectl get nodes -o jsonpath='{.items[*].metadata.labels.gpu\.nvidia\.com/class}'` to see available GPU classes.

Apply the manifest to create the Deployment and Service:

```bash theme={"system"}
kubectl apply -f nim-hello-world.yaml
```

You should see output similar to the following:

```text theme={"system"}
deployment.apps/nim-hello-world created
service/nim-hello-world created
```

### Wait for the NIM to become ready

The Deployment and Service exist, but the NIM container must download model weights before it can serve traffic. On first start, this can take several minutes depending on model size and network speed.

To check Pod status, list the Pods with the `nim-hello-world` label:

```bash theme={"system"}
kubectl get pods -n default -l app=nim-hello-world --no-headers
```

You should see output similar to the following once the model is loaded:

```text theme={"system"}
nim-hello-world-7c66bb6cf-78p4c   1/1   Running   0     75s
```

> [!NOTE]
>
> If the Pod restarts during startup, the liveness probe might trigger before the model finishes loading. Increase `initialDelaySeconds` on the liveness probe, or check logs with `kubectl logs -n default -l app=nim-hello-world --tail=50`.

Now that the NIM is running and healthy, you can send it inference requests.

## Query the NIM

Send a chat completion request to the NIM. The API is compatible with the [OpenAI Chat Completions format](https://developers.openai.com/api/reference/resources/chat).

Because the Service type is ClusterIP, you can only reach the endpoint from within the cluster. The following command uses a temporary Pod to send the request:

```bash theme={"system"}
kubectl run curl-test --rm -i --restart=Never \
    --image=curlimages/curl -- \
    curl -s http://nim-hello-world.default.svc.cluster.local:8000/v1/chat/completions \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "meta/llama3-8b-instruct",
      "messages": [{"role": "user", "content": "What is CoreWeave in one sentence?"}],
      "max_tokens": 128
    }'
```

You should see a JSON response similar to the following:

```json theme={"system"}
{
  "id": "cmpl-89a23df5d11b44f29008e04095f1da0d",
  "object": "chat.completion",
  "model": "meta/llama3-8b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "CoreWeave is a cloud-based HPC (High-Performance Computing) platform that enables researchers, scientists, and innovators to run demanding computational workloads, such as genomics, climate modeling, and artificial intelligence, using advanced technologies like AI, GPU acceleration, and multi-cloud deployment."
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

At this point, you have a working NIM inference endpoint running on your CKS cluster. You have authenticated to NGC, deployed the model, and confirmed it responds to chat completion requests.

## Clean up

When you're done, remove the Deployment, Service, and Secrets so the GPU node and credentials are no longer in use.

```bash theme={"system"}
kubectl delete -f nim-hello-world.yaml --ignore-not-found
kubectl delete secret ngc-credentials ngc-api-key -n default --ignore-not-found
```

## Next steps

Now that you have a working NIM deployment, explore these options:

* **Try a different model.** Replace the image and model name in the manifest to deploy any [NIM-supported model](https://build.nvidia.com/explore/discover).
* **Add autoscaling.** See the [Deploy vLLM for inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md) tutorial for patterns using KEDA and Prometheus-based autoscaling.
* **Expose externally.** Add an Ingress or LoadBalancer Service to serve inference requests from outside the cluster.
