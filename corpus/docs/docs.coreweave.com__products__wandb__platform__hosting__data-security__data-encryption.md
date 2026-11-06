# Data encryption in Dedicated Cloud

Source: https://docs.coreweave.com/products/wandb/platform/hosting/data-security/data-encryption

# Data encryption in Dedicated Cloud

> Learn how Weights & Biases encrypts Dedicated Cloud data with cloud-native keys and handles customer-managed keys.

This page explains database and object storage encryption in [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), including the policy on customer-managed keys. It is intended for security and compliance teams evaluating the service for sensitive AI workloads.

Weights & Biases manages the keys that encrypt each Dedicated Cloud instance's database and object storage. It uses the cloud provider's customer-managed encryption key (CMEK) capability, acting as the provider's customer on your behalf.

Each instance has a unique key, which provides an additional layer of isolation between tenants. This capability is available on AWS, Azure, and Google Cloud.

> [!NOTE]
>
> Dedicated Cloud instances on AWS have used the Weights & Biases-managed cloud-native key for encryption since before August 2024.
>
> On Google Cloud and Azure, instances created in August 2024 or later use a key managed by Weights & Biases to encrypt the database and object storage. Earlier instances use the default key managed by the cloud provider.

Customer-provided keys are generally not allowed for the managed database and object storage. A team with access to your cloud infrastructure could inadvertently remove the key or revoke access, potentially corrupting all data in the instance beyond recovery.

If using your own key is a requirement for adopting Dedicated Cloud, you can request an exception from Weights & Biases. Approved exceptions follow the W\&B Dedicated Cloud shared responsibility model.

> [!WARNING]
>
> If any user in your organization removes your key or revokes Weights & Biases's access to it at any point when your Dedicated Cloud instance is live, Weights & Biases isn't liable for any resulting data loss or corruption and isn't responsible for recovery of the data.
