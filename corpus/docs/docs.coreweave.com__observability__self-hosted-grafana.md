# Self-hosted Grafana

Source: https://docs.coreweave.com/observability/self-hosted-grafana

# Self-hosted Grafana

> Setting up a self-hosted Grafana instance inside CKS

This guide shows you how to deploy and configure a self-hosted Grafana instance inside a CoreWeave Kubernetes Service (CKS) cluster. If you need more customization and control than [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md) provides, you can deploy a self-hosted Grafana instance. CoreWeave Grafana supports [custom dashboards](https://docs.coreweave.com/observability/managed-grafana.md#custom-dashboards) in preview, but CoreWeave-provided dashboards are read-only and CoreWeave Grafana doesn't support custom alerting. With self-hosting, you can edit or export CoreWeave-provided dashboards, create custom alerts, and freely explore all available metrics in your environment.

[CoreWeave Charts](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction.md) deploys self-hosted Grafana instances. This handles most of the process of configuring data sources, but [authentication](#configure-coreweave-metrics-data-source-credentials) requires some manual configuration.

By the end of this guide, you have a running self-hosted Grafana instance connected to CoreWeave Metrics and CoreWeave Logs data sources.

## Prerequisites

To set up a self-hosted Grafana instance, you need the following:

* A [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md) for an active CKS account. The token's user needs the [**Observability Viewer**](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry) role to read metrics and logs data.
* A CKS cluster where you intend to self-host (deploy and manage) Grafana.
* [`kubectl`](https://kubernetes.io/docs/tasks/tools/) installed.
* [`helm`](https://helm.sh/docs/intro/install/) installed.

> [!WARNING]
>
> Customers who self-host a Grafana instance are responsible for all setup, maintenance, and resource costs associated with hosting. CoreWeave recommends using [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md).

## Install Grafana with CoreWeave Charts

This section installs the Grafana Helm chart into your cluster so the application is running and ready to configure.

1. Add the CoreWeave Charts repository:

   ```bash theme={"system"}
   helm repo add coreweave https://charts.core-services.ingress.coreweave.com
   ```

2. Install the `grafana` chart, pinning the chart version:

   ```bash theme={"system"}
   helm install -n "[MY-NAMESPACE]" grafana coreweave/grafana --version 1.61.0
   ```

> [!NOTE]
>
> The version pin is required. Versions 1.62.0 and later of the `grafana` chart fail to install with the error `Secret "sh.helm.release.v1.grafana.v1" is invalid: data: Too long: may not be more than 1048576 bytes`, because the Helm release record for the chart exceeds the Kubernetes Secret size limit. Version 1.61.0 is the latest version that installs successfully.

> [!TIP]
>
> The `grafana-dashboards` chart is a dependency of `grafana`, so it does not need to be installed independently.

## Log in to Grafana with admin credentials

With Grafana installed, the next step is to reach the application in your browser and sign in as the administrator so you can finish configuration. Before you log in to Grafana, you must port forward your Grafana service.

1. Port forward your Grafana service:

   ```bash theme={"system"}
   kubectl port-forward svc/grafana -n "[MY-NAMESPACE]" 8900:80
   ```

2. Navigate to `localhost:8900`. You see a login page similar to the following:

   ![Grafana login page.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-login.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=70480975f161d88ecbb07b47a2844560)

3. Obtain the admin password, which is required to log in to Grafana for the first time. This password is stored as a Kubernetes Secret. Retrieve the Secret value, replacing `[MY-NAMESPACE]` with your namespace ID:

   ```bash theme={"system"}
   kubectl get secret grafana -n "[MY-NAMESPACE]" -o=jsonpath='{.data.admin-password}' | base64 --decode
   ```

   Note: If you use a Mac, you might need to remove the trailing `%`.

4. Use the returned value as your password when you log in to Grafana with the following credentials:

   | Field | Value |
   | - | - |
   | Username | `admin` |
   | Password | `[MY-SECRET]` |

## Configure CoreWeave Metrics data source credentials

After you log in to Grafana with your admin credentials, you must configure credentials for the CoreWeave-provided data sources so Grafana can authenticate to the CoreWeave observability backend. First, configure the CoreWeave Metrics data source.

### Configure the data source HTTP headers

The following HTTP header values are required to connect to CoreWeave's data sources, where `[MY-TOKEN]` is your CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md).

| Field | Value |
| - | - |
| Header | `Authorization` |
| Value | `Bearer [MY-TOKEN]` |

To configure these headers, navigate to **Connections** from Grafana's left-hand menu to display the dropdown options. Then, click **Data sources** to proceed to the **Data sources** page. Select **CoreWeave Metrics** from the options listed to proceed to the **Settings** menu for the new data source.

![Grafana menu with data sources item indicated](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-connections-data-sources.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=b10aaffa81369d37a4e06d6bef134c25)

Next, navigate to the **Authentication** section. This is the only section that requires editing.

![Authentication section of Grafana data sources screen](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-authentication-http-header.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=aca6fdb003ea8dac7df918021c8d5a67)

Then, click the dropdown arrow on the right-hand side of the **HTTP headers** subsection to display the **+ Add header** button.

![HTTP headers section of Grafana data sources screen](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-authentication-add-http-header.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=c5a2ad79c682ea935953567b7b136dc9)

In the **Header** field, enter `Authorization`.

![Custom header section of Grafana data sources screen](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-http-header-fields.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=0e1a66ad66cd5b019bd27eb1f512f606)

In the **Value** field, provide the value `Bearer [MY-TOKEN]`, where `[MY-TOKEN]` is your CoreWeave [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md).

Configure the HTTP method to use `GET` by changing the HTTP dropdown method in the **Other** subsection to `GET`:

![Configure the HTTP method to use GET.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/configure-get.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=f5f9b5a25fd0a3b2602d30d0bc2b7d30)

## Configure the CoreWeave Logs data source

After the configuration for the **CoreWeave Metrics** data source is complete, repeat the preceding steps for the **CoreWeave Logs** data source. With both data sources configured, your self-hosted Grafana instance can query CoreWeave metrics and logs.

## Learn more

For more information, explore the following resources:

* [Custom GPU utilization alerts](https://docs.coreweave.com/observability/self-hosted-grafana/custom-alerts.md) to create Grafana-managed alert rules that monitor GPU utilization across your cluster.
* [Grafana documentation](https://grafana.com/docs/grafana/latest/) for guidance on tasks such as building dashboards, working with data sources, and exploring metrics.
* [Prometheus Query Language (PromQL) documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/) to learn how to query the **CoreWeave Metrics** data in both ad-hoc Explore queries and advanced dashboard panels.
