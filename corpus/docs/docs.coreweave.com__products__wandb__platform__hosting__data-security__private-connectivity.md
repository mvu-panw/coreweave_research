# Configure private connectivity to Dedicated Cloud

Source: https://docs.coreweave.com/products/wandb/platform/hosting/data-security/private-connectivity

# Configure private connectivity to Dedicated Cloud

> Connect to a W&B Dedicated Cloud instance over a private network using AWS PrivateLink, GCP, or Azure Private Link.

This document explains how to connect to a W\&B Dedicated Cloud instance over a cloud provider's secure private network, so that traffic between your environment and Weights & Biases avoids the public internet. It's intended for cloud and security administrators who manage Dedicated Cloud instances and want to harden network access for AI workloads and user traffic.

You can connect to your [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) instance over the cloud provider's secure private network. This applies to access from your AI workloads to the W\&B APIs and optionally from your user browsers to the W\&B app UI. When you use private connectivity, the relevant requests and responses don't transit through the public network or internet. This reduces exposure to the public internet and helps satisfy network isolation requirements for sensitive workloads.

> [!NOTE]
>
> Secure private connectivity is offered as an advanced security option with Dedicated Cloud.

Secure private connectivity is available on Dedicated Cloud instances on AWS, Google Cloud, and Azure:

* Use [AWS PrivateLink](https://aws.amazon.com/privatelink/) on AWS.
* Use [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) on Google Cloud.
* Use [Azure Private Link](https://azure.microsoft.com/products/private-link) on Azure.

After enabling private connectivity, Weights & Biases creates a private endpoint service for your instance and provides its DNS URI. Create private endpoints in your cloud accounts to route AI workload traffic from your VPC or VNet to that service.

To route browser traffic privately as well, configure DNS routing from your corporate network to those endpoints. Browser requests must resolve to the private endpoint instead of the public endpoint.

> [!NOTE]
>
> To use this feature, contact [Support](mailto:forge-support@coreweave.com).

You can use secure private connectivity with [IP allowlisting](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/ip-allowlisting.md) to combine network isolation with location-based access controls. If you combine the two, Weights & Biases recommends that you use secure private connectivity for all traffic from your AI workloads and for browser traffic from your users where possible, and use IP allowlisting for instance administration from privileged locations.
