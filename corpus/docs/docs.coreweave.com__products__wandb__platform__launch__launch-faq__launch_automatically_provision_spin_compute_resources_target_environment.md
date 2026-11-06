# Can Launch automatically provision (and spin down) compute resources for me in the target environment?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/launch_automatically_provision_spin_compute_resources_target_environment

# Can Launch automatically provision (and spin down) compute resources for me in the target environment?

Whether Launch automatically provisions and scales compute resources depends on the target environment:

* **Amazon SageMaker and Vertex AI**: These platforms provision resources automatically.
* **Kubernetes**: Autoscalers adjust resources based on demand. Weights & Biases solution architects can help you configure your Kubernetes infrastructure to enable retries, autoscaling, and spot instance node pools.

For more information, contact [Support](mailto:forge-support@coreweave.com) or use your shared Slack channel.
