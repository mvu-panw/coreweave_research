# Artifact data privacy and compliance

Source: https://docs.coreweave.com/products/wandb/artifacts/data-privacy-and-compliance

> Learn where Weights & Biases files are stored by default. Explore how to save, store sensitive information.

# Artifact data privacy and compliance

When you log artifacts, Weights & Biases uploads the files to a Google Cloud bucket. The contents of the bucket are encrypted at rest and in transit. Only users with access to the project can see the files.

![GCS W\&B Client Server diagram](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/data_and_privacy_compliance_1.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6f7a8cad3265b5907252acc9729ad815)

When you delete a version of an artifact, it is marked for soft deletion in our database and removed from your storage cost. When you delete an entire artifact, it is queued for permanent deletion and all of its contents are removed from the Weights & Biases bucket. If you have specific needs around file deletion, reach out to [Customer Support](mailto:forge-support@coreweave.com).

By default, deleted artifacts are retained for 7 days and can be restored during this period, which is configurable for Dedicated Cloud. Learn more about data retention in [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md#data-retention-policy) or [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md#data-retention-policy).

For sensitive datasets that cannot reside in a multi-tenant environment, you can use [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [reference artifacts](https://docs.coreweave.com/products/wandb/artifacts/track-external-files.md). Reference artifacts track references to private buckets without sending file contents to Weights & Biases. Reference artifacts maintain links to files on your buckets or servers. Weights & Biases only keeps track of the metadata associated with the files, not the files themselves.

![W\&B Client Server Cloud diagram](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/data_and_privacy_compliance_2.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d1c05173b40da95b087aa9ee74f94328)

For more information about deployment options, see [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md). To discuss your specific requirements, [contact CoreWeave](https://www.coreweave.com/contact-us).
