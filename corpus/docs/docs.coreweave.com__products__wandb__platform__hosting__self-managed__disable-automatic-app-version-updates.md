# Disable automatic updates for W&B Server

Source: https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/disable-automatic-app-version-updates

# Disable automatic updates for W&B Server

> Learn how to disable automatic updates for W&B Server.

This page shows administrators of Self-Managed Weights & Biases deployments how to disable automatic version upgrades for W\&B Server and pin its version to a specific release. Pinning a version gives you control over when upgrades happen. This control is useful when you need to coordinate upgrades with internal change management processes or validate a release in a staging environment before you roll it out. These instructions work only for deployments managed by the [W\&B Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md).

> [!NOTE]
>
> Weights & Biases supports a major W\&B Server release for 12 months from its initial release date. Customers with **Self-Managed** instances are responsible for upgrading in time to maintain support. Avoid staying on an unsupported version. Weights & Biases recommends that customers with **Self-Managed** instances update their deployments with the latest release at least once per quarter to maintain support and to receive the latest features, performance improvements, and fixes.

## Requirements

* W\&B Kubernetes Operator `v1.13.0` or newer
* System Console `v2.12.2` or newer, or `v2.18.16` or newer if your license is supplied through a Kubernetes secret rather than set inline

To verify that you meet these requirements, refer to the W\&B Custom Resource or Helm chart for your instance. Check the `version` values for the `operator-wandb` and `system-console` components.

Your deployment must also be assigned to a release channel, which determines the versions you can pin to. Weights & Biases assigns new deployments to the stable channel automatically. If your deployment predates July 2026, it might not have a channel yet.

## Disable automatic updates

To disable automatic updates, use the System Console to pin W\&B Server to a specific version, then check the Operator reconciliation logs to confirm that version pinning is active.

1. Log in to Forge as a user with the `admin` role.
2. Click the user icon at the top, then click **System Console**.
3. Go to **Settings** > **Advanced**, then select the **Other** tab.
4. In the **Disable Auto Upgrades** section, turn on **Pin specific version**.
5. Click the **Select a version** drop-down list, then select a W\&B Server version.
6. Click **Save**.

   ![System Console showing Pin specific version turned on with a selected W\&B Server version](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/disable_automatic_updates_saved_and_enabled.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=192af361aa161f0179c9144c1701dec2)

   Automatic upgrades are turned off and W\&B Server is pinned at the version you selected.
7. Verify that automatic upgrades are turned off. Go to the **Operator** tab and search the reconciliation logs for the string `Version pinning is enabled`.

```text theme={"system"}
│info 2025-04-17T17:24:16Z wandb default No changes found
│info 2025-04-17T17:24:16Z wandb default Active spec found
│info 2025-04-17T17:24:16Z wandb default Desired spec
│info 2025-04-17T17:24:16Z wandb default License
│info 2025-04-17T17:24:16Z wandb default Version Pinning is enabled
│info 2025-04-17T17:24:16Z wandb default Found Weights & Biases instance, processing the spec...
│info 2025-04-17T17:24:16Z wandb default === Reconciling Weights & Biases instance...
```

## Troubleshooting

If the **Disable Auto Upgrades** section reports an error instead of letting you select a version, match the message below.

### "Please provide a valid license, check your license key and try again"

The System Console can't read your license. If you supply the license through a Kubernetes secret (`global.licenseSecret`) instead of setting `global.license` inline, upgrade System Console to `v2.18.16` or newer. Earlier versions read only the inline value, so they send an empty license when they request the list of available releases.

### "Please contact your Weights & Biases Solutions Architect to configure a release channel"

Your deployment isn't assigned to a release channel, so the System Console has no versions to offer. Contact your Weights & Biases Solutions Architect or [Support](mailto:forge-support@coreweave.com) to have your deployment assigned to a channel.
