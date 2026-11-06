# 1. Set up infrastructure dependencies

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/1-set-up-infrastructure

# 1. Set up infrastructure dependencies

> Install Traefik ingress controller and cert-manager for your vLLM inference deployment

## Overview

Before you deploy vLLM, set up the infrastructure components that handle external traffic routing and TLS certificate management. This step installs Traefik (for ingress) and `cert-manager` (for automatic SSL certificates), so that the vLLM service you deploy in later steps is reachable from outside the cluster over HTTPS.

This page is for cluster operators who have already provisioned a CKS cluster and have `helm` and `kubectl` configured to target it.

## Step 1: Add CoreWeave Helm repository

The CoreWeave Helm repository hosts the Traefik and cert-manager charts used throughout this tutorial. Add it to your local Helm configuration so that subsequent `helm install` commands can resolve those charts:

```bash theme={"system"}
helm repo add coreweave https://charts.core-services.ingress.coreweave.com
helm repo update
```

You should see output similar to the following:

```text theme={"system"}
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kedacore" chart repository
...Successfully got an update from the "coreweave" chart repository
...Successfully got an update from the "grafana" chart repository
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⎈Happy Helming!⎈
```

## Step 2: Install Traefik ingress controller

Deploy Traefik to handle external traffic routing and TLS termination:

```bash theme={"system"}
helm install traefik coreweave/traefik \
  --namespace traefik \
  --create-namespace
```

You should see something like the following:

```text theme={"system"}
NAME: traefik
LAST DEPLOYED: Mon Aug 16:17:22
NAMESPACE: traefik
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Verify the installation by checking that all Traefik Pods are running:

```bash theme={"system"}
kubectl get pods -n traefik
```

You should see output similar to the following:

```text theme={"system"}
NAME                       READY   STATUS    RESTARTS   AGE
traefik-6b7c8d9f4b-abc12   1/1     Running   0          2m
```

## Step 3: Install and enable cert-manager

Install `cert-manager` for automatic TLS certificate management:

```bash theme={"system"}
helm install cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --create-namespace
```

You should see output similar to the following:

```text theme={"system"}
NAME: cert-manager
LAST DEPLOYED: Mon Aug 16:21:38
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Enable the `cert-manager` cluster issuers:

```bash theme={"system"}
helm upgrade cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --set cert-issuers.enabled=true
```

You should see output similar to the following:

```text theme={"system"}
Release "cert-manager" has been upgraded. Happy Helming!
NAME: cert-manager
LAST DEPLOYED: Mon 16:25:47
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 2
TEST SUITE: None
```

To verify that `cert-manager` is running, use the following command:

```bash theme={"system"}
kubectl get pods -n cert-manager
```

You should see output similar to the following:

```text theme={"system"}
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-6b7c8d9f4b-def34              1/1     Running   0          1m
cert-manager-cainjector-6b7c8d9f4b-ghi56   1/1     Running   0          1m
cert-manager-webhook-6b7c8d9f4b-jkl78      1/1     Running   0          1m
```

## Step 4: Verify infrastructure setup

Before you move on to monitoring setup, confirm that Traefik and `cert-manager` are both healthy and that the expected cluster issuers are available. Check that all components are installed and running:

```bash theme={"system"}
kubectl get svc -n traefik
```

You should see output similar to the following:

```text theme={"system"}
NAME          TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)                                    AGE
traefik       LoadBalancer   10.16.3.150   166.00.0.00   80:37187/TCP,443:33016/TCP,443:33016/UDP   12m
traefik-k8s   LoadBalancer   10.16.2.181   10.16.4.0     443:36556/TCP                              12m
```

To check `cert-manager` services, run the following command:

```bash theme={"system"}
kubectl get svc -n cert-manager
```

You should see output similar to the following:

```text theme={"system"}
NAME                      TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)            AGE
cert-manager              ClusterIP   10.16.1.116   <none>        9402/TCP           10m
cert-manager-cainjector   ClusterIP   10.16.3.76    <none>        9402/TCP           10m
cert-manager-webhook      ClusterIP   10.16.2.145   <none>        443/TCP,9402/TCP   10m
```

To verify that certificate issuers are available, run the following command:

```bash theme={"system"}
kubectl get clusterissuer
```

You should see output similar to the following:

```text theme={"system"}
NAME                        READY   AGE
letsencrypt-prod            True    7h4m
letsencrypt-staging         True    7h4m
selfsigned-cluster-issuer   True    7h4m
```

## What's next

Your cluster now has Traefik handling ingress and TLS termination, and `cert-manager` issuing certificates through the `letsencrypt-prod`, `letsencrypt-staging`, and `selfsigned-cluster-issuer` cluster issuers. With these infrastructure dependencies in place, you can expose the vLLM service securely after you deploy it.

In the next step, you [configure monitoring and observability](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference/2-set-up-monitoring.md) for your vLLM deployment.

> [!TIP]
>
> If you encounter issues with the installation, check the Pod logs for troubleshooting information.
>
> ```bash theme={"system"}
> kubectl logs -n traefik -l app.kubernetes.io/name=traefik
> kubectl logs -n cert-manager -l app.kubernetes.io/name=cert-manager
> ```
