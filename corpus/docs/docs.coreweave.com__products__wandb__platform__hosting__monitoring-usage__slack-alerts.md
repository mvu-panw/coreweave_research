# Configure Slack alerts

Source: https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/slack-alerts

# Configure Slack alerts

> Create and configure a Slack application to receive W&B Server alerts, notifications, and monitoring updates.

Integrate W\&B Server with [Slack](https://slack.com/) so that your Weights & Biases instance can dispatch alerts and notifications to a Slack workspace your team already uses. This page walks W\&B Server administrators through creating a Slack application, configuring its OAuth scopes and redirect URL, and registering the application with Weights & Biases.

> [!NOTE]
>
> Watch a [video demonstrating setting up Slack alerts on W\&B Dedicated Cloud deployment](https://www.youtube.com/watch?v=JmvKb-7u-oU) (6 min).

## Create the Slack application

W\&B Server uses a custom Slack application as the bridge for delivering alerts. Follow this procedure to create that application in the Slack workspace where you want to receive notifications.

1. Visit [https://api.slack.com/apps](https://api.slack.com/apps) and select **Create an App**.

   ![Create an App button](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/create_an_app.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=ed1aca2479584c6c4c0dd71dabe6d0ac)

2. Provide a name for your app in the **App Name** field.

3. Select a Slack workspace where you want to develop your app. Ensure that the Slack workspace you use is the same workspace you intend to use for alerts.

   ![App name and workspace selection](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/name_app_workspace.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8a7de757dedd59eea9e2c8d8fb76d017)

## Configure the Slack application

After you create the Slack application, grant it the permissions to post messages and accept the redirect from Weights & Biases during the OAuth handshake.

1. On the left sidebar, select **OAuth & Permissions**.

   ![OAuth & Permissions menu](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/add_an_oath.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=497443eecd810d63b9e03159c0b8ab0f)

2. In the **Scopes** section, grant the bot the `incoming_webhook` scope. Scopes give your app permission to perform actions in your development workspace.

   For more information about OAuth scopes for bots, see [Understanding OAuth scopes for bots](https://api.slack.com/legacy/oauth-scopes) in the Slack API documentation.

   ![Bot token scopes](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/save_urls.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=483aee2fd35cddaf11e52d1a420b8964)

3. Configure the **Redirect URL** to point to your Weights & Biases installation. Use the same URL that you set as your host URL in your local system settings. You can specify multiple URLs if you have different DNS mappings to your instance.

   ![Redirect URLs configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/redirect_urls.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=bb973addc666195b2cc6ee8d170393f0)

4. Select **Save URLs**.

5. Optional: Under **Restrict API Token Usage**, specify an IP or IP range to allowlist for your Weights & Biases instances. Limiting the allowed IP address helps secure your Slack application.

## Register your Slack application with Weights & Biases

Register the Slack application you configured with your Weights & Biases instance so that Weights & Biases can use it to dispatch alerts.

1. Navigate to the **System Settings** or **System Console** page of your Weights & Biases instance, depending on your deployment.

2. Depending on the System page you're on, follow one of the following options:

   * If you're in the **System Console**: go to **Settings** then to **Notifications**.

     ![System Console notifications](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/register_slack_app_console.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8dfc5ce6b4a8a5413b044ff8f60a13af)

   * If you're in the **System Settings**: toggle the **Enable a custom Slack application to dispatch alerts** to enable a custom Slack application.

     ![Enable Slack application toggle](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/register_slack_app.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=37485920bbf09c60632bd959dbb2e38b)

3. Supply your **Slack client ID** and **Slack secret**, then select **Save**. To find your application's client ID and secret, navigate to **Basic Information** in **Settings**.

4. To verify that everything works, set up a Slack integration in the W\&B app.

Your W\&B Server is now registered with the Slack application and can dispatch alerts to the configured Slack workspace.
