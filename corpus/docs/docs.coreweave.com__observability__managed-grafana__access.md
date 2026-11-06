# Access and use CoreWeave Grafana dashboards

Source: https://docs.coreweave.com/observability/managed-grafana/access

# Access and use CoreWeave Grafana dashboards

> Learn how to access and use CoreWeave Grafana dashboards

CoreWeave Grafana dashboards provide visibility into the performance, usage, and cost of your CoreWeave resources. This page explains how to sign in, locate available dashboards, and navigate their panels.

For the relationship between identity, credentials, and IAM roles across CoreWeave, see the [CoreWeave authorization model](https://docs.coreweave.com/security/iam.md#authorization-model).

## Prerequisites

Before you begin, check these access requirements:

* You must sign in to the [Cloud Console](https://console.coreweave.com/) to access CoreWeave Grafana.
* You need the [Observability Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#observability-and-telemetry) role in an [IAM access policy](https://docs.coreweave.com/security/iam/access-policies.md) to access the metrics and logs used by dashboards. In the legacy CoreWeave permissions model, membership in the [`metrics` group](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions) grants equivalent access.
* To access the [Usage by Product and Zone dashboard](https://docs.coreweave.com/observability/managed-grafana/cost-usage/usage-product-zone.md), you need both the **Observability Viewer** and **Billing Viewer** roles in an [IAM access policy](https://docs.coreweave.com/security/iam/access-policies.md). In the legacy CoreWeave permissions model, membership in the [`metrics` and `billing_viewer` groups](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions) also grants this access.

Custom dashboards are in preview. To view, create, or edit your organization's custom dashboards, you also need [dashboard access](https://docs.coreweave.com/observability/managed-grafana.md#dashboard-access).

## Access CoreWeave Grafana dashboards

CoreWeave Grafana is hosted at [cks-grafana.coreweave.com](https://cks-grafana.coreweave.com).

To open a dashboard:

1. Sign in to the [Cloud Console](https://console.coreweave.com/) to authenticate, then go to the [Grafana](https://cks-grafana.coreweave.com) page. The dashboard is also linked in the left sidebar of the Cloud Console.

2. On the Grafana dashboard page, select **Home** and then **Dashboards**.

   ![CoreWeave Grafana dashboard example.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-home.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=73471586cbf760cb1dc148aa9c1e2a25)

3. From the dashboard menu, expand a folder and select a dashboard.

   ![CoreWeave Grafana dashboard example.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-dashboards.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=27296c1f7db651c44a837f6af125a0d9)

After you select a dashboard, it opens in the main view so you can explore its panels.

## Use CoreWeave Grafana dashboards

CoreWeave Grafana dashboards have three main areas:

* **Variables**: Variables let you select from options to refine your queries.
* **Panel group**: A panel group organizes related panels into a section.
* **Panels**: Panels visualize or list the data described in the panel name.

![CoreWeave Grafana dashboard example.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/dashboard-example.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=440318e34ebdfa769cb9dc050af8232a)

CoreWeave Grafana dashboard example.

For more information about Grafana dashboards, see the [Grafana documentation](https://grafana.com/docs/grafana/latest/).
