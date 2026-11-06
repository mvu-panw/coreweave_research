# 2. Configure monitoring and observability

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/2-set-up-monitoring

# 2. Configure monitoring and observability

> Set up Prometheus and Grafana for monitoring your vLLM inference deployment

## Overview

This is the second step in the [Deploy vLLM inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md) tutorial series. Before starting, complete [step 1: set up infrastructure dependencies](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/1-set-up-infrastructure.md).

Monitoring and observability are important for production inference workloads. This step sets up Prometheus for metrics collection and Grafana for visualization, giving you insights into your vLLM deployment's performance. You also prepare the storage and authentication resources that the vLLM deployment in the next step depends on.

The monitoring stack provides metrics for the following areas:

* Request throughput and latency
* GPU utilization and memory usage
* KV cache performance
* Queue depth and autoscaling metrics

> [!CAUTION]
>
> **Resource allocation**
>
> The monitoring stack requires additional cluster resources. Ensure your CKS cluster has at least one CPU Node for Prometheus and Grafana to deploy to.

## Step 1: Install Prometheus and Grafana

Clone the reference architecture repository:

```bash theme={"system"}
git clone https://github.com/coreweave/reference-architecture.git
```

Navigate to the `hack` folder:

```bash theme={"system"}
cd reference-architecture/observability/basic/hack
```

Get your cluster org and cluster name by going to the Cloud Console. Update the `values.yaml` file by replacing the `orgID`, `clusterName`, and `hosts` sections with your information.

* `orgID`: You can get your `orgID` on the [CoreWeave Console settings page](https://console.coreweave.com/account/settings).
* `clusterName`: You can get your cluster name on the [CoreWeave Console Cluster page](https://console.coreweave.com/clusters).

Add your information to the following sections:

```text theme={"system"}
orgID: cw0000 # REPLACE WITH YOUR ACTUAL ORGID
clusterName: inference # REPLACE WITH YOUR ACTUAL CLUSTER NAME

grafana:
  enabled: true
  grafana:
    ingress:
      hosts: [&host "grafana.cw0000-inference.coreweave.app"] # REPLACE WITH YOUR ACTUAL GRAFANA HOSTNAME, USING YOUR ORGID AND CLUSTERNAME
      tls:
        - secretName: grafana-tls
          hosts:
            - *host
```

For example, if your `orgID` is `cw99` and your cluster name is `my-inference-cluster`, the `values.yaml` would look like the following:

```text theme={"system"}
orgID: cw99
clusterName: my-inference-cluster

grafana:
  enabled: true
  grafana:
    ingress:
      hosts: [&host "grafana.cw99-my-inference-cluster.coreweave.app"]
      tls:
        - secretName: grafana-tls
          hosts:
            - *host
```

> [!WARNING]
>
> Depending on when you created your cluster, you might need to comment out the rest of the file.

Because the example cluster was created after **2025-07-04**, the `values.yaml` looks like the following:

```yaml theme={"system"}
orgID: cw99
clusterName: inference-guide

grafana:
  enabled: true
  grafana:
    ingress:
      hosts: [&host "grafana.cw99-my-inference-cluster.coreweave.app"]
      tls:
        - secretName: grafana-tls
          hosts:
            - *host

# If your cluster was created BEFORE 2025-07-04, you MUST use the values below.
# If your cluster was created AFTER 2025-07-04, you can comment these values out.
#prometheus:
#  prometheusOperator:
#    enabled: false
#  defaultRules:
#    create: false
#  prometheus:
#    # Can also add agent mode if you only want to forward metrics
#    prometheusSpec:
#      # remoteWrite: FILL IF NEEDED
#      image:
#        registry: quay.io
#        repository: prometheus/prometheus
#        tag: v2.54.0
#      version: 2.54.0
```

Add the Prometheus and Grafana Helm repositories and update the local cache:

```bash theme={"system"}
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

You should see output similar to the following:

```text theme={"system"}
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "coreweave" chart repository
...Successfully got an update from the "grafana" chart repository
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Navigate to the `observability/basic` directory and deploy the monitoring stack from the `observability/basic` directory:

```bash theme={"system"}
helm dependency build
```

You should see something similar to the following:

```text theme={"system"}
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "coreweave" chart repository
...Successfully got an update from the "grafana" chart repository
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⎈Happy Helming!⎈
Saving 2 charts
Downloading grafana from repo https://charts.core-services.ingress.coreweave.com
Downloading kube-prometheus-stack from repo https://prometheus-community.github.io/helm-charts
Deleting outdated charts
```

Install the observability chart into the `monitoring` namespace:

```bash theme={"system"}
helm install observability ./ \
  --namespace monitoring \
  --create-namespace \
  --values ./hack/values.yaml
```

You should see output similar to the following:

```text theme={"system"}
NAME: observability
LAST DEPLOYED: Mon Aug 17:46:02
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
```

## Step 2: Verify monitoring deployment

List the Pods in the `monitoring` namespace:

```bash theme={"system"}
kubectl get pods -n monitoring
```

You should see output similar to the following:

```text theme={"system"}
NAME                                                 READY   STATUS    RESTARTS   AGE
observability-grafana-9868b99df-vsfxl                1/2     Running   0          40s
observability-prometheus-operator-65d54479b7-b62zd   1/1     Running   0          40s
prometheus-observability-prometheus-prometheus-0     2/2     Running   0          37s
```

## Step 3: Get Grafana credentials

Retrieve the auto-generated Grafana admin password:

```bash theme={"system"}
kubectl get secret observability-grafana -n monitoring \
  -o=jsonpath='{.data.admin-password}' | base64 --decode; echo
```

Save this password for accessing the Grafana dashboard.

## Step 4: Create model cache storage

In this step, you create a namespace for the inference workload and a persistent volume claim that caches downloaded model weights so later Pod restarts don't re-download large model files.

Navigate to the `inference/basic` directory:

```bash theme={"system"}
cd ../../inference/basic
```

Create the inference namespace:

```bash theme={"system"}
kubectl create namespace inference
```

Create the model cache PVC:

```bash theme={"system"}
kubectl apply -f hack/huggingface-model-cache.yaml
```

## Step 5: Optional: Set up Hugging Face authentication

For models that require authentication, like the Llama 3.1 8B Instruct, create a secret with your Hugging Face token. Replace `[HUGGINGFACE-TOKEN]` with your actual Hugging Face access token.

```bash theme={"system"}
export HF_TOKEN="[HUGGINGFACE-TOKEN]"

kubectl create secret generic hf-token \
  -n inference \
  --from-literal=token="$HF_TOKEN"
```

You should see output similar to the following:

```text theme={"system"}
secret/hf-token created
```

## Step 6: Create Grafana dashboard for vLLM

Add the vLLM monitoring dashboard to Grafana:

```bash theme={"system"}
kubectl apply -f hack/manifests-grafana.yaml -n inference
```

You should see output similar to the following:

```text theme={"system"}
configmap/vllm created
```

This creates a ConfigMap that Grafana automatically detects and loads as a dashboard.

## Step 7: Optional: Install autoscaling support

For production workloads, install KEDA to enable automatic scaling based on demand:

```bash theme={"system"}
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda \
  --namespace keda \
  --create-namespace
```

Verify KEDA is running:

```bash theme={"system"}
kubectl get pods -n keda
```

You should see output similar to the following:

```text theme={"system"}
NAME                                              READY   STATUS    RESTARTS        AGE
keda-admission-webhooks-7fc99cdd4d-vbkx2          1/1     Running   0               6m48s
keda-operator-54ffcbbfd6-fmhxw                    1/1     Running   1 (6m46s ago)   6m48s
keda-operator-metrics-apiserver-c5b6f8b88-pzjjv   1/1     Running   0               6m48s
```

## What's next

Your monitoring and observability stack is now configured, and the namespace, model cache, Hugging Face secret, and Grafana dashboard required by the inference workload are in place. In the next step, you [deploy the vLLM inference service](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/3-deploy-vllm.md).
