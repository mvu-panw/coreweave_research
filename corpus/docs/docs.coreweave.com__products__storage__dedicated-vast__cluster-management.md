# Cluster management

Source: https://docs.coreweave.com/products/storage/dedicated-vast/cluster-management

# Cluster management

> Manage your Dedicated VAST cluster with VMS, including user accounts, SSO, QoS policies, and quotas

This page describes how to manage a Dedicated VAST cluster as a single-tenant customer, including the VAST Management System (VMS), user accounts, single sign-on (SSO), Quality of Service (QoS) policies, storage quotas, software upgrades, and monitoring responsibilities. Use this page to understand which administration tasks you control directly and which are coordinated with CoreWeave and VAST.

## VAST Management System (VMS)

The VAST Management System (VMS) is the primary web-based interface for managing your Dedicated VAST cluster. As a single-tenant customer, you receive direct access to VMS to control cluster configuration, users, and policies.

Through VMS, you can perform the following tasks:

* Create and manage VAST users and access credentials.
* Configure Views (protocol export paths) for NFS, S3, block, and SQL access.
* Search and query file and object metadata using [VAST Catalog](https://docs.coreweave.com/products/storage/dedicated-vast/data-services.md#vast-catalog).
* Define and apply QoS policies and storage quotas per View or per User.
* Create and manage snapshot schedules and retention policies.
* Configure audit logging and review access logs.
* Monitor cluster health, capacity utilization, and performance metrics.
* Configure replication and Global Access policies (where applicable).

You access VMS through your cluster's management address, with automatic failover so VMS access remains available even if the primary node becomes unavailable.

## User management

CoreWeave provisions each Dedicated VAST cluster with a dedicated set of VAST user accounts scoped to your tenant. You can create additional users directly in VMS to match your team's access requirements.

Keep the following points in mind when managing users:

* **CSI driver credentials**: The VAST CSI drivers require dedicated VAST user accounts. Provision service accounts in VMS and supply those credentials when configuring the drivers.
* **S3 credentials**: S3 access keys are generated per user in VMS. A user must have S3 enabled on their account to receive S3 credentials.
* **Access scope**: User permissions in VMS control which Views, paths, and operations a given user can access.

For user management procedures, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## SSO and identity provider integration

Dedicated VAST supports SSO and SAML-based integration with external identity providers. This lets you federate VAST user authentication against your existing IdP rather than managing credentials natively in VMS.

Supported identity providers include Okta, Azure Active Directory, and any SAML 2.0-compliant provider.

For IdP configuration procedures, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## QoS and quotas

You configure VAST QoS policies and storage quotas in VMS at both the View level and the User level, giving you fine-grained control over how you allocate cluster resources across teams, workloads, or projects.

**QoS policies** let you set throughput limits (MB/s) and IOPS limits on a View or on individual Users. This prevents a single workload or user from saturating cluster bandwidth at the expense of others.

**Storage quotas** set capacity limits on a View or on individual Users within a View. Hard quotas block writes when the limit is reached. Soft quotas issue warnings.

You can apply and modify both without interrupting running workloads. For configuration details, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Software upgrades

CoreWeave, VAST, and you as the customer coordinate VAST software upgrades on your cluster. CoreWeave and VAST don't apply upgrades unilaterally. You're involved in scheduling and approving upgrades that affect your cluster.

This coordination ensures that CoreWeave and VAST test upgrades against your workloads, communicate any breaking changes in advance, and align maintenance windows with your operational requirements.

## Monitoring and observability

You have full access to the VAST monitoring stack for cluster-level alerting and observability. CoreWeave provides dashboards for cluster monitoring. For hardware-level alerts, CoreWeave and VAST handle monitoring and remediation. You don't need to configure hardware health checks.

The following table summarizes which party is responsible for each monitoring area, so you can plan where to focus your own configuration and alerting effort:

| Area | Responsible party |
| - | - |
| Hardware health | CoreWeave and VAST |
| Network monitoring | CoreWeave |
| VAST software, feature configuration, and cluster health | Customer and VAST |
| Capacity monitoring | Customer and VAST |
| Audit logging configuration | Customer |
