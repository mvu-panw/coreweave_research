# Security

Source: https://docs.coreweave.com/products/storage/dedicated-vast/security

# Security

> Data isolation, encryption, audit logging, and the shared responsibility model for Dedicated VAST clusters

This page describes the security controls that protect data on Dedicated VAST clusters and clarifies which responsibilities belong to CoreWeave, VAST, and the customer. Review it to understand which protections are enabled by default, which controls you must configure, and where to find more VAST documentation.

The following sections cover physical isolation, encryption, audit logging, access control, and the shared responsibility model.

## Physical data isolation

CoreWeave provisions each Dedicated VAST cluster on hardware exclusive to a single tenant. All cluster hardware is dedicated to your organization and isn't shared with other CoreWeave customers. Your data resides only on your cluster's storage and doesn't pass through or reside on any shared storage infrastructure.

## Encryption at rest

Encryption at rest protects data on the cluster's storage media without requiring customer configuration. It's enabled on every Dedicated VAST cluster at provisioning time. VAST provisions unique encryption keys per cluster, so your encryption keys aren't shared with any other CoreWeave tenant.

Key characteristics:

* **AES-based encryption** at the storage layer, applied transparently to all stored data.
* **Keys provisioned at cluster launch**: Encryption is enabled before any customer data is written.
* **Key management**: VAST provisions and manages keys during cluster setup. Customers don't manage keys directly.

For details on VAST's encryption implementation, see the [VAST Security documentation](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Encryption in transit

Encryption in transit is the customer's responsibility to implement and enforce. CoreWeave and VAST don't enforce in-transit encryption by default on cluster protocols.

Options depend on the protocol in use:

* **NFS**: NFSv4.1 supports Kerberos-based integrity and encryption (krb5i, krb5p). You can configure TLS transport for NFS over TLS where supported.
* **S3**: Configure your S3 endpoint to require HTTPS. Don't use plain HTTP endpoints for sensitive data.
* **SQL**: Configure TLS on your database connection.

Refer to the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1) for protocol-specific in-transit encryption configuration.

## Audit logging

Customers control VAST audit logging services through VMS. Audit logging can capture:

* File access events (reads, writes, deletes, metadata operations).
* User authentication and authorization events.
* VMS configuration changes and administrative actions.
* S3 API operations.

The customer manages audit log configuration in VMS, including what is logged, log verbosity, and log export destinations. CoreWeave doesn't configure or retain audit logs on your behalf.

> [!WARNING]
>
> You're responsible for configuring audit logging and retaining logs per your organization's compliance requirements. Audit logging isn't enabled by default. Configure log policies in VMS after cluster provisioning.

For audit log configuration, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Access control

Access control determines who can read or modify data on the cluster and which credentials they use. VAST VMS user accounts control access to data on the cluster. The same user identity governs NFS file access, S3 object access, and SQL access. No separate credential store exists for each protocol.

The following list summarizes the access control mechanisms available on Dedicated VAST clusters:

* **User management**: Customer-managed in VMS. See [Cluster management](https://docs.coreweave.com/products/storage/dedicated-vast/cluster-management.md) for details.
* **SSO and SAML**: Dedicated VAST supports federation with external identity providers (Okta, Azure AD, and other SAML 2.0 providers). See [Cluster management](https://docs.coreweave.com/products/storage/dedicated-vast/cluster-management.md) for details.
* **S3 credentials**: VMS generates S3 access keys per user account. Access key scope is tied to the user's permissions in VMS.
* **Network access**: CoreWeave provisions network connectivity between your GPU cluster and the VAST cluster IPs. CoreWeave handles the network layer that restricts which cluster nodes can reach VAST. VMS user credentials provide the application-layer access control.

## Shared responsibility model

The following table summarizes security and operational responsibilities across CoreWeave, VAST, and the customer.

> [!NOTE]
>
> CoreWeave provides a formal Shared Responsibility Model (SRM) document for Dedicated VAST. Contact your CoreWeave account team to obtain the current SRM.

| Responsibility | CoreWeave | VAST | Customer |
| - | - | - | - |
| Physical hardware security | ✓ | | |
| Data center physical access | ✓ | | |
| Network infrastructure and monitoring | ✓ | | |
| Hardware health monitoring | ✓ | ✓ | |
| VAST software maintenance and upgrades | | ✓ (coordinated) | ✓ (coordinated) |
| Cluster software monitoring | | ✓ | ✓ |
| Capacity monitoring | | | ✓ |
| Encryption at rest (key provisioning) | | ✓ | |
| Encryption in transit | | | ✓ |
| User account management | | | ✓ |
| Access control configuration | | | ✓ |
| Audit log configuration and retention | | | ✓ |
| Data protection and disaster recovery | | | ✓ |
| Snapshot policy configuration | | | ✓ |
