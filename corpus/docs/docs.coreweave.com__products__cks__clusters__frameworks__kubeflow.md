# Run Kubeflow

Source: https://docs.coreweave.com/products/cks/clusters/frameworks/kubeflow

# Run Kubeflow

> Set up and deploy Kubeflow on CKS for machine learning workflows with certificate management

[Kubeflow](https://www.kubeflow.org/) is an open source machine learning platform that runs on Kubernetes, providing tools for the complete ML lifecycle from development to deployment.

This guide is for cluster administrators and ML platform engineers who want to run Kubeflow on a CoreWeave Kubernetes Service (CKS) cluster to support end-to-end ML workflows, from experimentation through deployment.

This guide shows you how to set up Kubeflow on CKS by covering the following:

* Configure your cluster for Kubeflow compatibility.
* Install certificate management components.
* Deploy Kubeflow with the default OSS manifests.
* Access the Kubeflow dashboard.

## Prerequisites

Before you install Kubeflow, ensure you have the following:

* A Kubernetes cluster on CoreWeave accessible with `kubectl`.
* `kustomize` installed and configured to work with your cluster.

## Setup

1. Clone the Kubeflow manifests repository and navigate to it by running the following commands:

   ```bash theme={"system"}
   git clone --depth 1 --branch v1.10.1 https://github.com/kubeflow/manifests.git
   cd manifests
   ```

2. Edit the [Cilium config](https://github.com/cilium/cilium) to handle Kubeflow's service traffic in a way that's compatible with CKS networking:

   ```bash theme={"system"}
   kubectl edit -n cw-cilium-system cm cilium-config
   ```

   Add the following value, then save and exit:

   ```yaml theme={"system"}
   bpf-lb-sock-hostns-only: "true"
   ```

   For example, the `cilium-config` file section should look similar to this:

   ```yaml highlight={3} theme={"system"}
   bpf-lb-mode: dsr
   bpf-lb-sock: "false"
   bpf-lb-sock-hostns-only: "true"
   bpf-lb-sock-terminate-pod-connections: "false"
   bpf-map-dynamic-size-ratio: "0.0025"
   bpf-policy-map-max: "16384"
   ```

   Apply the changes:

   ```bash theme={"system"}
   kubectl rollout restart -n cw-cilium-system ds cilium
   ```

   Note: Disregard deprecation warnings.

3. Install `cert-manager` and the `cert-issuer` so Kubeflow components can request and manage the TLS certificates they require:

   ```bash theme={"system"}
   kustomize build common/cert-manager/base | kubectl apply -f -
   kustomize build common/cert-manager/kubeflow-issuer/base | kubectl apply -f -
   ```

4. Install Kubeflow with the OSS default manifests. The loop retries the apply until all resources are accepted, because some custom resources depend on CRDs that are still being registered:

   ```bash theme={"system"}
   while ! kustomize build example | kubectl apply --server-side --force-conflicts -f -; do echo "Retrying to apply resources"; sleep 20; done
   ```

After completing these steps, you have a Kubeflow installation running on your CKS cluster, with `cert-manager` configured and the default Kubeflow components deployed.

## Use Kubeflow

After you install Kubeflow, you can access the dashboard and other components. The default namespace for Kubeflow is `kubeflow`.

To start using Kubeflow, port-forward the main dashboard service:

```bash theme={"system"}
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

To view the Kubeflow dashboard, go to [http://localhost:8080](http://localhost:8080).

The default credentials are used for basic authentication. Access the dashboard with the following credentials:

User: `user@example.com`
Password: `12341234`
