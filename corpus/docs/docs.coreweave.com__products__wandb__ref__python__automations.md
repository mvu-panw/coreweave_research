# Automations overview

Source: https://docs.coreweave.com/products/wandb/ref/python/automations

# Automations overview

> Use the W&B Automations API to create and manage automated workflows in your ML pipelines

The W\&B Automations API enables programmatic creation and management of automated workflows that respond to events in your ML pipeline. Configure actions to trigger when specific conditions are met, such as model performance thresholds or artifact creation.

### Core classes

| Class | Description |
| - | - |
| [`Automation`](https://docs.coreweave.com/products/wandb/ref/python/automations/automation) | Represents a saved automation instance with its configuration. |
| [`NewAutomation`](https://docs.coreweave.com/products/wandb/ref/python/automations/newautomation) | Builder class for creating new automations. |

### Events (Triggers)

| Event | Description |
| - | - |
| [`OnRunMetric`](https://docs.coreweave.com/products/wandb/ref/python/automations/onrunmetric) | Trigger when a run metric satisfies a defined condition (threshold, change, etc.). |
| [`OnCreateArtifact`](https://docs.coreweave.com/products/wandb/ref/python/automations/oncreateartifact) | Trigger when a new artifact is created in a collection. |
| [`OnLinkArtifact`](https://docs.coreweave.com/products/wandb/ref/python/automations/onlinkartifact) | Trigger when an artifact is linked to a registry. |
| [`OnAddArtifactAlias`](https://docs.coreweave.com/products/wandb/ref/python/automations/onaddartifactalias) | Trigger when an alias is added to an artifact. |

### Actions

| Action | Description |
| - | - |
| [`SendNotification`](https://docs.coreweave.com/products/wandb/ref/python/automations/sendnotification) | Send notifications via Slack or other integrated channels. |
| [`SendWebhook`](https://docs.coreweave.com/products/wandb/ref/python/automations/sendwebhook) | Send HTTP webhook requests to external services. |
| [`DoNothing`](https://docs.coreweave.com/products/wandb/ref/python/automations/donothing) | Placeholder action for testing automation configurations. |

### Filters

| Filter | Description |
| - | - |
| [`MetricThresholdFilter`](https://docs.coreweave.com/products/wandb/ref/python/automations/metricthresholdfilter) | Filter runs based on metric value comparisons against thresholds. |
| [`MetricChangeFilter`](https://docs.coreweave.com/products/wandb/ref/python/automations/metricchangefilter) | Filter runs based on metric value changes over time. |

## Common use cases

### Model performance monitoring

* Alert when model accuracy drops below a threshold
* Notify team when training loss plateaus
* Trigger retraining pipelines based on performance metrics

### Artifact Management

* Send notifications when new model versions are created
* Trigger deployment workflows when artifacts are tagged
* Automate downstream processing when datasets are updated

### Experiment tracking

* Alert on failed or crashed runs
* Notify when long-running experiments complete
* Send daily summaries of experiment metrics

### Integration workflows

* Update external tracking systems via webhooks
* Sync model registry with deployment platforms
* Trigger CI/CD pipelines based on W\&B events

## Example usage

The following example creates an automation that sends a Slack notification whenever a metric called `custom-metric` exceeds 10. `custom-metric` is expected to be logged during training using `wandb.Run.log({"custom-metric": value })`.

```python theme={"system"}
import wandb
from wandb.automations import OnRunMetric, RunEvent, SendNotification

api = wandb.Api()

project = api.project("<my-project>", entity="<my-team>")

# Use the first Slack integration for the team
slack_hook = next(api.slack_integrations(entity="<my-team>"))

# Create a trigger event
event = OnRunMetric(
     scope=project,
     filter=RunEvent.metric("custom-metric") > 10,
)

# Create an action that responds to the event
action = SendNotification.from_integration(slack_hook)

# Create the automation
automation = api.create_automation(
     event >> action,
     name="my-automation",
     description="Send a Slack message whenever 'custom-metric' exceeds 10.",
)
```

For more information about using the Automations API, see the [Automations Guide](https://docs.coreweave.com/products/wandb/automations.md).
