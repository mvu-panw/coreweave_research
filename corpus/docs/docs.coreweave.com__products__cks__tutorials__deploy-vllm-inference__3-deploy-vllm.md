# 3. Deploy vLLM inference service

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/3-deploy-vllm

# 3. Deploy vLLM inference service

> Deploy and configure your vLLM inference service with model caching and autoscaling

## Overview

Now that your infrastructure and monitoring are set up, you'll deploy the vLLM inference service to serve large language model completions from your CKS cluster. This step covers how to configure your deployment, deploy the service, and verify it's working correctly.

## Step 1: Configure your deployment

Choose from the example configurations in the `hack/` directory, or customize `values.yaml` for your specific model and requirements.

This guide deploys Llama 3.1 8B Instruct.

Navigate to the `inference/basic` directory, and run the following command to create a working copy of the example values file:

```bash theme={"system"}
cp hack/values-llama-small.yaml my-values.yaml
```

## Step 2: Update cluster-specific settings

These fields tell the chart which CoreWeave cluster and organization the deployment belongs to, so the Ingress hostname is generated correctly. Edit `my-values.yaml` and update the following required fields:

Replace `[CLUSTER-NAME]` with your CKS cluster name and `[ORG-ID]` with your organization ID.

```yaml theme={"system"}
ingress:
  clusterName: "[CLUSTER-NAME]"
  orgID: "[ORG-ID]"
```

* `orgID`: You can get your `orgID` on the [CoreWeave Console setting page](https://console.coreweave.com/account/settings).
* `clusterName`: You can get your cluster name on the [CoreWeave Console Cluster page](https://console.coreweave.com/clusters).

## Step 3: Deploy the vLLM service

Install the vLLM inference chart:

```bash theme={"system"}
helm install basic-inference ./ \
  --namespace inference \
  --create-namespace \
  -f my-values.yaml
```

You should see output similar to the following:

```text theme={"system"}
NAME: basic-inference
LAST DEPLOYED: Mon Aug 18:10:27
NAMESPACE: inference
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## Step 4: Monitor deployment progress

The Pod must reach `Running` status before the service can accept requests. To check Pod status, run:

```bash theme={"system"}
kubectl get pods -n inference -w
```

The initial deployment may take several minutes while the model weights download and cache.

You should see output similar to:

```text theme={"system"}
NAME                               READY   STATUS    RESTARTS   AGE
basic-inference-577c5675c8-vm2nc   1/1     Running   0          13m
```

When the Pod is running, exit the process and go to the next step.

> [!NOTE]
>
> **Debugging tip**
>
> If model downloads fail, check the following:
>
> * Ensure internet connectivity from worker Nodes.
> * Check Hugging Face token for gated models.
> * Verify sufficient storage in the model cache PersistentVolumeClaim (PVC).
>
> If Pods are stuck in a pending state, check the following:
>
> * Check GPU Node availability:
>
>   ```bash theme={"system"}
>   kubectl get nodes -l node-role.kubernetes.io/worker=true
>   ```
>
> * Verify resource requests don't exceed Node capacity.

## Step 5: Check Service and Ingress

Verify that the Service and Ingress are properly configured:

```bash theme={"system"}
kubectl get svc,ingress -n inference
```

You should see output similar to:

```text theme={"system"}
NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/basic-inference-vllm ClusterIP   10.96.123.45    <none>        8000/TCP  5m

NAME                                      CLASS    HOSTS                                         ADDRESS      PORTS     AGE
ingress.networking.k8s.io/basic-inference traefik  basic-inference.your-cluster.coreweave.cloud  ***.**       80, 443   5m
```

> [!NOTE]
>
> **Debugging tip**
>
> If the Ingress is not accessible, check the following:
>
> * Confirm Traefik is running:
>
>   ```bash theme={"system"}
>   kubectl get pods -n traefik
>   ```
>
> * Check `cert-manager` for certificate issues:
>
>   ```bash theme={"system"}
>   kubectl get certificates -n inference
>   ```
>
> * Verify DNS resolution to your cluster's load balancer.

## Step 6: Access and test your inference service

With the Service and Ingress confirmed, you can reach the model from outside the cluster and send it a request to confirm end-to-end functionality.

### Get the service endpoint

Retrieve the external URL for your vLLM service:

```bash theme={"system"}
export VLLM_ENDPOINT="$(kubectl get ingress basic-inference -n inference -o=jsonpath='{.spec.rules[0].host}')"
echo "Your vLLM endpoint: https://$VLLM_ENDPOINT"
```

### Test service health

Verify the service is responding:

```bash theme={"system"}
curl -s -o /dev/null -w "%{http_code}" https://$VLLM_ENDPOINT/health
```

You should see `200`.

### Get available models

List the loaded models:

```bash theme={"system"}
export VLLM_MODEL="$(curl -s https://$VLLM_ENDPOINT/v1/models | jq -r '.data[].id')"
echo "Available model: $VLLM_MODEL"
```

You should see the following output:

```text theme={"system"}
Available model: meta-llama/Llama-3.1-8B-Instruct
```

### Run inference

Test the model with a simple chat completion:

```bash theme={"system"}
curl -X POST "https://$VLLM_ENDPOINT/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "'"$VLLM_MODEL"'",
        "messages": [
          { "role": "system", "content": "You are a helpful AI assistant." },
          { "role": "user", "content": "Explain the benefits of GPU acceleration for LLM inference." }
        ],
        "max_tokens": 500,
        "temperature": 0.7
      }'
```

You should see the returned output in JSON.

## Monitor model download progress

The initial model download can take 10 to 30 minutes depending on the model size and network conditions. You can monitor the download progress in the Pod logs:

```bash theme={"system"}
kubectl logs -n inference -l app=basic-inference -f
```

## General debugging commands

If you need to debug your deployment, use the following commands:

```bash theme={"system"}
# Check vLLM pod logs
kubectl logs -n inference -l app=basic-inference

# Describe pod for events
kubectl describe pod -n inference -l app=basic-inference

# Check ingress status
kubectl describe ingress basic-inference -n inference

# Monitor resource usage
kubectl top pods -n inference
```

## What's next

Your vLLM inference service is now deployed and running. In the next step, you [monitor performance and test autoscaling](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/4-monitor-and-test.md).
