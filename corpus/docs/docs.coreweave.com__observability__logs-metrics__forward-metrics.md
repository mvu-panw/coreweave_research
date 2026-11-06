# Forward application metrics

Source: https://docs.coreweave.com/observability/logs-metrics/forward-metrics

# Forward application metrics

> Deploy a Prometheus Agent in a CKS cluster to forward application metrics to an external system

To forward CoreWeave Kubernetes Service (CKS) metrics to an external system, deploy the [Prometheus Agent](https://prometheus-operator.dev/docs/platform/prometheus-agent/) inside your CKS cluster and configure it to use remote-write.

> [!NOTE]
>
> CKS clusters deployed **before** July 7, 2025 have Prometheus Operator pre-installed.
>
> CKS clusters deployed **after** July 7, 2025 don't have Prometheus Operator pre-installed. Clusters deployed after this date must [install Prometheus Operator](https://prometheus-operator.dev/docs/getting-started/installation/) before proceeding with the following steps.

To deploy the Prometheus Agent in your CKS cluster, complete the following steps:

1. Choose a namespace to deploy the Prometheus Agent in. You can deploy the Prometheus Agent to an existing namespace, or create a new namespace with `kubectl`.

   To create a new namespace, replace `[NAMESPACE-NAME]` with your chosen namespace and run:

   ```bash theme={"system"}
   kubectl create namespace "[NAMESPACE-NAME]"
   ```

2. Configure the [Prometheus Agent CustomResource YAML file](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/getting-started/design.md#prometheus-agent) with your remote-write destination, as in the following example:

   ```yaml title="sample-prometheus-agent.yaml" theme={"system"}
   apiVersion: monitoring.coreos.com/v1alpha1
   kind: PrometheusAgent
   metadata:
     name: my-prom-agent
     namespace: "[NAMESPACE-NAME]"
   spec:
     remoteWrite:
       - url: "https://example-url/api/v1/write"
         ...
   ```

   For more information about `remoteWrite` configurations, see the [Prometheus Operator API reference](https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.RemoteWriteSpec).

3. To deploy the Prometheus Agent to your CKS cluster, replace `sample-prometheus-agent.yaml` with the appropriate filename and run:

   ```bash theme={"system"}
   kubectl apply -f sample-prometheus-agent.yaml
   ```

   Metrics generated within your CKS cluster now remote-write to your specified destination.
