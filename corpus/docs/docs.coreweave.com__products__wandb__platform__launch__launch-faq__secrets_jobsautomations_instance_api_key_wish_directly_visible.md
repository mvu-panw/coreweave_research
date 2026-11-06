# Can you specify secrets for jobs or automations? For instance, an API key which you do not wish to be directly visible to users?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/secrets_jobsautomations_instance_api_key_wish_directly_visible

# Can you specify secrets for jobs or automations? For instance, an API key which you do not wish to be directly visible to users?

Yes. Follow these steps:

1. Create a Kubernetes Secret in the designated namespace for the runs:\
   `kubectl create secret -n [NAMESPACE] generic [SECRET-NAME] [SECRET-VALUE]`

2. After you create the secret, configure the queue to inject the secret when runs start. Only cluster administrators can view the secret. End users cannot see it.
