# W&B Mobile App (iOS)

Source: https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/mobile-app

# W&B Mobile App (iOS)

> Explore Weights & Biases projects, training runs, console logs, line plots, and system metrics on your iPhone or iPad.

> [!NOTE]
>
> Latest version: 26.31 (released October 26, 2026). [App Store release notes](https://apps.apple.com/us/app/6755162576).

![W\&B mobile app project panel with metric charts](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/project-panels.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=90a36835df6d77b96e87db70b738db93)

![ARIA tab and chat interface in the W\&B iOS app](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/aria-chat.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=a6b738df14e0244277ff75c8cc113700)

![W\&B mobile app Projects list and team picker](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/projects.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=953404f638b852ff7e901d51b6e540cb)

![W\&B mobile app runs list for a project](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/project-runs.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=bf46b1c3a24f247a1a1689d62da66272)

The W\&B Mobile App for iOS keeps you connected to your Weights & Biases projects wherever you go. Use it on your iPhone or iPad to track training runs and read run logs in real time, view line plots and system metrics, explore project histories, and follow your team's progress so you can monitor experiments without opening your laptop. This page describes the app's features and shows you how to set up notifications.

> [!NOTE]
>
> The mobile app is available for [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) accounts, and in preview for [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) accounts, by invitation only. To request access for your organization, contact [support](mailto:forge-support@coreweave.com) or your AISE. The mobile app isn't available for [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) deployments.

## Download W\&B Mobile

Install the app from the App Store to get started.

> [card] [Download on the App Store](https://apps.apple.com/us/app/6755162576)

## Log in

Follow these steps to sign in to Weights & Biases on iOS. How you log in depends on the deployment your Weights & Biases account belongs to. Select your deployment type to continue.

> [tab] Multi-tenant Cloud
>
> > [!TIP]
> >
> > You can't create a Weights & Biases account from the mobile app. Visit [Forge](https://forge.coreweave.com/wandb) on a desktop browser and click **Sign up**.
>
> To log in, follow these steps:
>
> 1. Open the app, then tap **Log in**.
> 2. Log in with the same credentials you use for Forge in your browser.
>
> Multi-tenant Cloud doesn't use login codes, so the **Log in on mobile** menu item doesn't appear in Weights & Biases.

> [tab] Dedicated Cloud
>
> > [!TIP]
> >
> > Access to W\&B Dedicated Cloud from a mobile device is available in preview by invitation only.
>
> To authenticate to a Dedicated Cloud instance, generate a code in W\&B App on your computer, then scan it with your mobile device. Have both devices available before you begin.
>
> 1. On your computer, sign in to Forge.
>
> 2. Select your profile image in the upper-right corner, then select **Log in on mobile**. If this option is unavailable, your organization is not enrolled in the preview. To request access for your organization, contact [support](mailto:forge-support@coreweave.com) or your AISE.
>
> 3. In the **Log in on mobile** dialog, click **Generate login code**. Weights & Biases displays the login code as a QR code and adds an API key named **W\&B iOS** to your [user settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md#api-keys). If Weights & Biases can't generate a key, an error appears in the dialog. If your organization restricts who can create API keys, ask your organization admin for help.
>
> 4. On your iPhone or iPad, open the app, then tap **Log in to Dedicated Cloud**. If prompted, allow the app to use your camera.
>
> 5. Point your device's camera at the QR code. The app logs you in to your Dedicated Cloud instance and closes the scanner.
>
> 6. On your computer, click **Done** to close the dialog.
>
> > [!WARNING]
> >
> > Treat a login code as sensitive information because it grants access to your Weights & Biases account. Protect it the same way you protect an API key or password. Don't take a screenshot of the code, save it, or share it. Close the dialog when you finish logging in. If a code might have been exposed, [delete the API key](https://docs.coreweave.com/products/wandb/platform/app/settings-page/user-settings.md#delete-an-api-key) immediately, then generate a new login code.
>
> Keep the following in mind when you log in to Dedicated Cloud:
>
> * Each login code you generate adds another **W\&B iOS** API key to your user settings, each with its own key ID. Because the keys share a name, rename a key to differentiate it, such as by including which device uses it. In your user settings, open the key's **action ()** menu, then click **Edit**.
> * A **W\&B iOS** key stays valid until you delete it. Deleting a key revokes access for the device that scanned the matching login code.
> * Logging in to Dedicated Cloud replaces the credentials of any account you were previously logged in to.
> * If you don't see **Log in to Dedicated Cloud** in the app, then confirm that your organization has access to the preview.

## Features

The following sections describe the features available in the mobile app.

### Projects and teams

Browse your projects and switch between teams. The app offers the following project features:

* **Explore projects**: Browse and search across your Weights & Biases projects.
* **Full project history**: Metric charts on project panels include data from the latest ten runs in the project, not only the latest run.
* **Star projects**: See your most important projects at a glance. Tap the star icon next to a project to star it. To filter the list to only starred projects, tap the **Starred** tab at the top of the list.
* **Switch teams**: Use the **team picker** to change teams.

### Runs

View run status, metrics, and line plots for your experiments in real time. The app offers the following run features:

* **Hide and show runs**: On a project's **Runs** tab, tap the **visibility ()** icon on a run to hide it. Hidden runs stay in the runs list with a **hidden ()** icon, so you can tap the icon again to show the run. Charts on the project's **Panels** tab plot only the runs that are visible. The app remembers which runs you hid in each project between launches.
* **Live updates**: Charts refresh as new data arrives. The **Runs** tab and project run lists update automatically when new runs start.
* **Run overview tab**: On each run, open the **Overview** tab for a dedicated summary of run details alongside metrics and logs. View the full run configuration and summary, including nested objects and arrays. Long config values wrap to multiple lines. Long-press a configuration value to copy it.
* **View system metrics**: On each run, open the **Metrics** tab to see how your hardware behaved during training. Weights & Biases automatically logs [metrics](https://docs.coreweave.com/products/wandb/ref/python/experiments/system-metrics.md) such as GPU utilization, CPU usage, memory, disk I/O, and network traffic. System metrics appear in a collapsible **System** section alongside your logged metrics. Each metric displays as a line chart with the same tooltip and search behavior as other metrics on the tab.
* **Stop runs**: When viewing an in-progress run, tap the **action ()** menu, then tap **Stop run**.
* **View console logs**: Read [logs](https://docs.coreweave.com/products/wandb/runs/view-logged-runs.md#logs) from active or completed runs, or download them once a run finishes. Colors from ANSI escape codes in your script output render faithfully and adapt to light and dark mode. The app polls active runs for new log lines every 5 seconds. Polling stops once a run finishes or crashes, which saves network and battery use. Even for runs with hundreds of thousands of log lines, the most recent output appears immediately, and older lines load in the background. Scrolling and log search stay responsive even for large outputs.

### Panels and metrics

Organize and find the panels and metrics that matter to you. The app offers the following panel and metric features:

* **Mobile-optimized panel grouping**: Panels are automatically grouped by name into collapsible sections. You can collapse the ungrouped metrics section to focus on named sections. Sections are a single level (not nested), and grouping follows the same rules as [workspace panels](https://docs.coreweave.com/products/wandb/app/features/panels.md) in the W\&B web app, so the layout stays consistent when you move between desktop and your phone.
* **Star panels**: See your most important panels at a glance. When viewing a run or a project, tap the star icon at the top of a panel to star it. To filter the list to only starred panels, tap the **Starred** tab at the top of the list.
* **Star metrics**: When viewing an important metric in detail view, tap the star icon to star it. Run cards on the **Runs** page prioritize your starred metrics when choosing which metric to display.
* **Search panels**: When viewing a run or a project, use the **panel search** field at the bottom of the screen to filter which runs appear in each chart. You can search with [RE2 syntax](https://github.com/google/re2/wiki/Syntax) to match patterns in run names.
* **Filter metrics**: Use the metric filter controls to narrow which metrics appear, so you can focus on the ones that matter.
* **View image metrics**: Images you log appear as panels you can interact with, on a run's **Metrics** tab and on a project's **Panels** tab. Tap to view a single image, then pinch to zoom or drag to pan. See [View image metrics](#view-image-metrics).

### Charts

Read and adjust the charts that plot your metrics. The app offers the following chart features:

* **Full fidelity**: When a chart has more data points than it can render, the app buckets the data and draws a shaded band around the line showing the minimum and maximum value in each bucket, so you can spot variance at a glance. This is the same [full fidelity](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/sampling.md#full-fidelity) rendering used in the W\&B web app. Turn on **Show bin range in tooltip** (see [Change line plot settings](#change-line-plot-settings)) to see a bucket's full range when you tap a point.
* **Chart tooltips**: On line charts, tooltips show metric values with up to four decimal places so you can read small changes accurately.
* **Zoom charts**: Pinch vertically or horizontally on a line chart to zoom in on either axis, or double-tap to step through zoom levels. The Y-axis rescales automatically to fit the visible portion of the curve, so small variations late in a run stay readable.
* **Chart detail view**: Tap a metric card to open its chart in a fullscreen detail view. A legend under the title lists each line in the chart, and the Y-axis uses evenly spaced ticks so values are easy to read.
* **Change line plot settings**: Choose the X-axis, switch a line plot to a logarithmic Y-axis, apply smoothing, and exclude outliers, for a single plot or for every plot in a run or project. See [Change line plot settings](#change-line-plot-settings).

### Notifications and ARIA

Stay on top of your experiments and get help from ARIA. The app offers the following features:

* **Stay informed**: Get updates on your experiments without opening your laptop using notifications. **Remove alerts** you no longer need from the **Notifications** tab by swiping them away. Tap a run state change push notification to open the run it refers to.
* **Chat with ARIA**: Use ARIA in the mobile app to ask questions, analyze runs, and take action without leaving your phone.

## View image metrics

Images you log to a run with [`wandb.Image`](https://docs.coreweave.com/products/wandb/track/log/media) appear on the run's **Metrics** tab, where each image metric has its own panel alongside your line plots. Image metrics also appear on a project's **Panels** tab, where each panel shows one tile per run so you can compare images across runs. The following actions are available for image metrics.

* **Scrub through steps**: Drag the step slider below the images to move through the steps the metric logged. When the metric logged only one step, the slider doesn't appear.
* **Jump to a step**: Tap the step value next to the slider, enter a step, then tap **Go to step**. The sheet shows the range of steps the metric logged, and your entry snaps to the nearest logged step.
* **Compare images within a step**: When a step logs more than one image, the panel arranges them in a grid that you swipe horizontally to page through. Dots below the grid show which page you're viewing.
* **Compare images across runs**: On a project's **Panels** tab, drag the step slider to move every run's tile to the same step. When a run logs more than one image per step, use the sample picker in the panel header (for example, **Sample #1**) to choose which image the tiles show. Tap a run's tile to open the image metric detail view for that run.
* **View an image full screen**: Tap the panel to open the detail view, then tap an image. Pinch to zoom and drag to pan, and swipe to move to the next or previous image in the step.
* **Read image captions**: Captions you log with an image appear on the detail view and in the full-screen viewer. Tap a long caption to expand it into a scrollable panel.
* **Star image metrics**: Tap the star icon on the panel to star an image metric, the same as other panels.

## Change line plot settings

Line plot settings control how the app draws a line plot. Open the settings in one of the following ways:

* On a run's **Metrics** tab or a project's **Panels** tab, tap the **line plot settings** button next to the metric filter. Changes apply to every line plot in that run or project.
* On a single chart's detail screen, tap the **line plot settings** button in the toolbar. Changes apply only to that plot.

The settings sheet names its scope below the title, so you can confirm what a change affects before you make it. The following settings are available.

* **X-axis**: Choose what the X-axis plots. Select a built-in axis (**Step**, **Relative time** (process runtime), or **Wall time**) or any other numeric metric your runs log. To find a metric, enter its name in the **Search X axis** field.
* **Log scale (Y)**: Draw the Y-axis logarithmically to compare a metric across orders of magnitude. A logarithmic axis can't plot zero or negative values. If a plot has no positive values to draw, the app replaces the chart with the message "No positive values to plot on a log scale".
* **Smoothing**: Apply [time-weighted exponential moving average (TWEMA)](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/smoothing.md#time-weighted-exponential-moving-average-twema-smoothing-default) smoothing, from `0` (off) to `0.99`. This algorithm is also the default in the W\&B web app.
* **Exclude outliers**: Frame the Y-axis to the lines alone, so a wide bin range can't flatten them. While on, the chart doesn't draw the shaded min-max band. Off by default.
* **Show bin range in tooltip**: Show the min and max values a bucket hides when you tap a point on a chart rendered with [full fidelity](#features). Off by default, matching the W\&B web app.

When you open the settings for a run or a project, a caption under a setting shows how many plots in scope override it, for example "2 panels override this." Tap **Clear** to remove those overrides for that one setting, so the run or project value applies to those plots again.

To restore the defaults, tap **Reset this line plot** or **Reset to defaults**, depending on the scope you opened the settings from.

The app saves your line plot settings between launches. When you change a setting on one plot, that setting also applies to plots of the same metric in your other runs and projects.

## Chat with ARIA

ARIA (AI Research & Iteration Agent) is your personalized research assistant in Weights & Biases. Use ARIA for tasks such as analyzing and running experiments, explaining results, identifying patterns across runs, recommending next steps, and building visualizations and reports.

To chat with ARIA, tap ![ARIA icon](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/aria-logo.svg?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=fa4501c0e6152282a6862e80fc93dd5c) in the bottom navigation.

In the mobile app, ARIA keeps context across multi-turn chats and shows reasoning and action details while it works.

* **Project context**: ARIA automatically detects which project you're viewing in the app and uses it as context, so answers come with the right project already in mind. You can also reference projects and runs directly in your chat messages.
* **In-chat panels**: When ARIA shares a Weights & Biases panel, it appears in the conversation as a native bar chart or run history line plot, drawn from your live run data.
* **Rich replies**: Replies stream in as ARIA writes them and render with rich Markdown formatting, including tables, headings, lists, and inline code. When ARIA asks questions, they render as an interactive view directly in the conversation.
* **Visible actions**: Shell steps show when ARIA takes an action, such as creating a panel, filtering runs, creating and running Python scripts, and more.
* **Approve network access requests**: When a task needs to reach a website, such as downloading a dataset, ARIA asks for permission directly in the conversation. The request shows ARIA's reason and the sites it wants to reach, and you can deselect any site before you grant or deny access, so tasks that need the network can continue from your phone. Past requests stay in the conversation as a summary you can expand.
* **Message drafts**: ARIA saves your unsent message, including any run mentions, so your draft is still there when you reopen ARIA.
* **Dismiss the keyboard**: Tap blank space or response text in a conversation to dismiss the keyboard.
* **Chat history**: Long-press a chat in your chat history to preview, rename, or delete it. Conversations older than 30 days are grouped by month. Tap the pin icon on a chat to keep it in the **Pinned** section at the top of your history. Chat history is kept in sync so you can move seamlessly between the web app and mobile app.

![ARIA tab and chat interface in the W\&B iOS app](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/aria-chat.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=a6b738df14e0244277ff75c8cc113700)

For a full overview of ARIA capabilities, see [ARIA overview](https://docs.coreweave.com/products/aria.md).

## Set up notifications

Configure notifications to receive updates about your experiments on your mobile device.

![W\&B mobile app Manage notifications screen](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/manage-alerts.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=7d3aa3f230a22b5b120fae427e488fb9)

The following sections describe the kinds of notifications you can configure. The **Manage notifications** screen lists both kinds of settings in one place, with short descriptions that explain what each section controls.

### Metric threshold alerts

Use metric threshold alerts to get notified when a metric crosses a value you specify.

1. Navigate to a run.
2. Tap the graph to enter full screen view.
3. Tap the bell icon in the top right.
4. Set notifications that trigger when future runs cross the specified metric threshold.

### Run failure alerts

Use run failure alerts to get notified when runs in a project fail.

1. Navigate to a project.
2. Tap the **action ()** menu in the top right.
3. Select **Run failed alert** to receive notifications for future run failures in that project.
