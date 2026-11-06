# When multiple jobs in a Docker queue download the same artifact, is any caching used, or is it re-downloaded every run?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/docker_queues_run_multiple_jobs_download_same_artifact_useartifact

# When multiple jobs in a Docker queue download the same artifact, is any caching used, or is it re-downloaded every run?

Launch jobs share no cache. Each launch job runs independently. To share a cache, configure the queue or agent to mount one with Docker arguments in the queue configuration.

For specific use cases, you can also mount the W\&B artifacts cache as a persistent volume.
