# Manage Mission Control Agent settings

Source: https://docs.coreweave.com/observability/mission-control-agent/manage-settings

# Manage Mission Control Agent settings

> Control organization access to Mission Control Agent and manage available data-sharing preferences.

Organization administrators can manage CoreWeave Mission Control Agent access and data-sharing
preferences from the **Privacy and data** page in the Cloud Console. These settings apply to the
whole organization. After a setting update succeeds, the Cloud Console displays the saved state. If
an update fails, the control returns to its previous state and the Cloud Console displays an error.

## Prerequisites

You need the **IAM Admin** role to change Mission Control Agent settings. Users without this role
can view the page, but the controls are unavailable.

For information about assigning roles, see [Manage IAM access policies](https://docs.coreweave.com/security/iam/access-policies/manage.md).

## Turn Mission Control Agent on or off

To change access to Mission Control Agent, follow these steps:

1. In the Cloud Console, go to **Permissions > Privacy and data**.
2. Turn **Enable AI experiences** on or off.

When the **Enable AI experiences** setting is off, users who open **Ask Mission Control** see
**Mission Control is off**, with a message that their organization administrator has turned it off.
Turning the setting off also prevents users from continuing existing conversations. The Cloud
Console clears a conversation when it detects that the setting is off.

To restore access, turn **Enable AI experiences** on. Users can then start new conversations, but
cleared conversations don't return.

## Manage data sharing

The **Privacy and data** page can display the following organization-wide controls:

* **Enable data collection**: Lets Mission Control collect your organization's data for model
  training. This control appears only when CoreWeave has enabled the data-consent setting for your
  organization.
* **Enable data anonymization**: Sets your organization's anonymization preference for collected
  data. This control is unavailable when data collection is turned off, and turning off data
  collection also turns off anonymization.

To change data-sharing preferences, follow these steps:

1. In the Cloud Console, go to **Permissions > Privacy and data**.
2. If **Enable data collection** is available, turn it on or off.
3. Optional: Turn **Enable data anonymization** on or off. This control is unavailable while data
   collection is off.

> [!NOTE]
>
> The controls available to your organization can differ based on your organization's terms and
> Mission Control rollout configuration.

## Related resources

Use the following resources to learn more about Mission Control Agent settings:

* [Introduction to Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent.md): Understand how the
  agent works and how it uses your permissions.
* [Use Mission Control Agent](https://docs.coreweave.com/observability/mission-control-agent/use.md): Ask questions and verify
  responses in the Cloud Console.
* [CoreWeave privacy policy](https://docs.coreweave.com/policies/terms-of-service/privacy-policy.md): Review the policy that
  governs personal data.
