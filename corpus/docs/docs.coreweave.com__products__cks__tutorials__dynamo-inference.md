# Deploy NVIDIA Dynamo on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/dynamo-inference

# Deploy NVIDIA Dynamo on CKS

> Deploy NVIDIA Dynamo on CKS for cluster-wide inference with Kai scheduler and Grove orchestration

[Dynamo](https://github.com/ai-dynamo/dynamo) provides deployment and orchestration for inference workloads. This tutorial shows you how to deploy Dynamo on CoreWeave Kubernetes Service (CKS) for cluster-wide inference, install its custom resources and platform components, and run an inference model. By the end, you have a working Dynamo deployment on your CKS cluster that serves a model through a local endpoint, which you can adapt to run other inference workloads at scale.

This tutorial is for cluster administrators and ML engineers who want to run distributed inference on CKS with GPU Nodes.

In this tutorial, you:

1. **Install Dynamo CRDs.**
2. **Install the Dynamo platform** with the Kubernetes AI (Kai) scheduler and Grove enabled.
3. **Deploy an inference model** using an example from the Dynamo repository and a Hugging Face token.
4. **List and delete deployments** when you're done.

> [card] What you'll need
>
> Before you start, you must have:
>
> * A [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with GPU Nodes.
> * `kubectl` installed and configured to access your cluster.
> * `helm` installed.
> * A [Hugging Face access token](https://huggingface.co/docs/hub/en/security-tokens) for model access.

> [card] What you'll use
>
> You use these tools and components:
>
> * **Dynamo**: Cluster-wide inference orchestration from the [Dynamo repository](https://github.com/ai-dynamo/dynamo).
> * **Helm**: To install Dynamo CRDs and platform charts from NVIDIA NGC.
> * **Kubernetes AI (Kai) scheduler and Grove**: Enabled in the platform install for scheduling and routing.

## Set environment

Set the namespace where Dynamo is installed and the Dynamo release version. The remaining steps reference these variables, so setting them once keeps the commands consistent.

```bash theme={"system"}
export NAMESPACE=dynamo-system
export RELEASE_VERSION=0.9.0
```

You use these variables in the following steps. Verify with `echo $NAMESPACE` and `echo $RELEASE_VERSION` if needed.

## Install CRDs

Dynamo requires custom resource definitions (CRDs) on the cluster before the platform components can run. Skip this step if Dynamo CRDs are already installed on the cluster.

1. Fetch and install the Dynamo CRDs chart:

   ```bash theme={"system"}
   helm fetch https://helm.ngc.nvidia.com/nvidia/ai-dynamo/charts/dynamo-crds-${RELEASE_VERSION}.tgz

   helm install dynamo-crds dynamo-crds-${RELEASE_VERSION}.tgz --namespace default
   ```

2. When the install completes without error, the CRDs are installed. Optionally verify with:

   ```bash theme={"system"}
   kubectl get crd | grep dynamo
   ```

## Install the platform

Install the Dynamo platform into the chosen namespace with the Kubernetes AI (Kai) scheduler and Grove enabled.

1. Fetch the Dynamo platform chart:

   ```bash theme={"system"}
   helm fetch https://helm.ngc.nvidia.com/nvidia/ai-dynamo/charts/dynamo-platform-${RELEASE_VERSION}.tgz
   ```

2. Install the Dynamo platform:

   ```bash theme={"system"}
   helm install dynamo-platform dynamo-platform-${RELEASE_VERSION}.tgz --namespace ${NAMESPACE} --create-namespace \
   --set "grove.enabled=true" \
   --set "kai-scheduler.enabled=true" \
   --set "dynamo-operator.controllerManager.manager.image.tag=${RELEASE_VERSION}" \
   --set "dynamo-operator.controllerManager.kubeRbacProxy.image.repository=registry.k8s.io/kubebuilder/kube-rbac-proxy" \
   --set "dynamo-operator.controllerManager.kubeRbacProxy.image.tag=v0.15.0"
   ```

   The output is similar to the following:

   ```text theme={"system"}
    I0312 13:13:13.800378    5735 warnings.go:110] "Warning: tls: failed to find any PEM data in certificate input"
    NAME: dynamo-platform
    LAST DEPLOYED: Thu Mar 12 13:12:16 2026
    NAMESPACE: dynamo-system
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
    SPDX-License-Identifier: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
   ```

3. When the install completes, Dynamo platform components run in `${NAMESPACE}`. Verify with:

   ```bash theme={"system"}
   kubectl get pods -n ${NAMESPACE}
   ```

   Ensure the expected Pods are running before you deploy a model.

## Deploy an inference model

With the platform running, you can now deploy a model for inference. This tutorial uses the `Qwen3-0.6B` model, which you deploy using the [`agg.yaml` from the Dynamo repository](https://github.com/ai-dynamo/dynamo/blob/main/examples/backends/vllm/deploy/agg.yaml).

1. Download the [`agg.yaml`](https://github.com/ai-dynamo/dynamo/blob/main/examples/backends/vllm/deploy/agg.yaml) and modify the image value by changing `my-tag` to `0.9.1` on lines 16 and 30:

   ```yaml theme={"system"}
   image: nvcr.io/nvidia/ai-dynamo/vllm-runtime:0.9.1
   ```

2. Create a Kubernetes Secret with your Hugging Face token. Replace `[HF-TOKEN]` with your Hugging Face token:

   ```bash theme={"system"}
   kubectl create secret generic hf-token-secret --from-literal=HF_TOKEN="[HF-TOKEN]" -n ${NAMESPACE}
   ```

3. Apply the `agg.yaml` to your cluster:

   ```bash theme={"system"}
   kubectl apply -f agg.yaml -n ${NAMESPACE}
   ```

   **More example models**

   More example models and manifests are available in the [Dynamo repository](https://github.com/ai-dynamo/dynamo). If you use one of these example models, create a Kubernetes Secret for your Hugging Face token (same as the preceding step). If you're deploying an example model instead of the `agg.yaml`, you might need to configure storage:

   * **Configure storage for the example.** In your chosen example, edit `model-cache/cache.yaml` and replace every instance of `your-storage-class` with `shared-vast` so the model cache uses CoreWeave storage.

   * **Apply the model download manifest** to download the model data:

     ```bash theme={"system"}
     kubectl apply -f model-cache/model-download.yaml
     ```

   When the download job completes, the model is cached and ready for inference. Follow any additional instructions in the example for running or exposing the model.

## Run inference

With the model deployed, you can send inference requests to it from your local machine. In another terminal, forward the `vllm-agg-frontend` service:

```bash theme={"system"}
kubectl port-forward service/vllm-agg-frontend 8000:8000 -n $NAMESPACE
```

To test the deployment, run:

```bash theme={"system"}
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-0.6B",
    "messages": [
      {
        "role": "user",
        "content": "Hello, how are you?"
      }
    ],
    "stream": false,
    "max_tokens": 100
  }'
```

The response includes a JSON body with a `choices` array containing the model reply.

## Clean up

When you no longer need the deployment, remove it to free cluster resources. To list Dynamo graph deployments in your namespace, run:

```bash theme={"system"}
kubectl get dynamographdeployment -n $NAMESPACE
```

To delete a deployment, use the resource kind and the deployment name. For example, to delete a deployment named `vllm-agg-router`:

```bash theme={"system"}
kubectl delete dynamographdeployment vllm-agg-router -n $NAMESPACE
```

The deployment is removed when the command succeeds.
