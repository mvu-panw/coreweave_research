# Chat with ARIA

Source: https://docs.coreweave.com/products/aria/chat

# Chat with ARIA

> Start, share, and organize ARIA chats, view in-chat panels, queue messages, add context, and grant network access.

> [!NOTE]
>
> Available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud).

This page describes how to manage your conversations with ARIA: starting and resuming chats, queueing follow-up messages, adding context, granting network access, and giving feedback on responses. Context can include runs, workspace panels, W\&B Weave traces, and images. It also covers organizing your chat history by renaming, pinning, sharing, and deleting conversations.

## Start a new chat

To start a new chat, open ARIA, then click the pencil icon in the upper right corner of the chat window.

You can run multiple chats in parallel at a time. ARIA notifies you when it responds to a chat, even if you have closed the chat window.

Starting a new chat does not delete your previous conversations. To [view previous conversations](https://docs.coreweave.com/products/aria/chat.md#view-chat-history), click **** (**Reveal chat history**) to open the chat history sidebar.

## Send a message

Type a message and press **Enter** to send it.

* Press **Shift+Enter** to add new lines.
* Click **+** to add images.
* To add a run reference, type `@` and select a run from the list. Type to filter and fuzzy-search the list.
* For more flexibility, compose a more complex message in a text editor and paste it. Plain text is supported, and pasted `@` characters are not resolved to run references.

To cancel the current operation and *immediately* send the next [queued message](#queue-messages), press the stop icon to the right of the text input.

## View panels in the chat

ARIA can answer with workspace panels that it renders directly in the chat:

* [Line plots and bar charts](#line-plots-and-bar-charts)
* [Scatter plots](#scatter-plots)
* [Parallel coordinates](#parallel-coordinates)
* [Parameter importance](#parameter-importance)
* [Run comparer](#run-comparer)
* [Media panels](#media-panels)

ARIA chooses a panel to fit your question. To get a specific panel, name it in your request, such as `Show a parameter importance panel for val/accuracy`.

These panels are live and interactive. A panel queries your Weights & Biases project when it displays, so it shows the current data for a run. You can hover over, search, and step through a panel without leaving the chat.

ARIA chooses each panel's settings. Changes you make in the chat, such as turning on **diff only** in a run comparer, aren't saved. To change how a panel is set up, ask ARIA to redraw it.

### Line plots and bar charts

You can open line plots and bar charts in full-screen view. When you hover over a run in the runs list on the **Workspace** or **Runs** tab, ARIA highlights the run's plots. When you hover over a panel in ARIA, the run is highlighted in the runs list on the **Workspace** tab.

![Workspace with an ARIA loss plot in the chat, where the run hovered in the runs list is highlighted in both the ARIA plot and the workspace panels](https://mintcdn.com/coreweave-dbfa0e8d/TqJiI6Q_VIg7BlKk/products/aria/_media/aria-line-plot-interactions.png?fit=max\&auto=format\&n=TqJiI6Q_VIg7BlKk\&q=85\&s=669e97c9098cb6564cc6f3c1e14a3de6)

### Scatter plots

A scatter plot shows one point per run and plots two of each run's config or summary values against each other, such as a hyperparameter against a final metric. For example:

```text title="User prompt" theme={"system"}
Plot learning_rate against test/accuracy for the runs in this sweep.
```

Each point uses a run's single config or summary value, not its logged history. An axis can also show when each run was created or last sent a heartbeat. To show a metric over steps, ask for a line plot instead.

You can ask ARIA to set axis labels, ranges, and logarithmic scales, and to add a linear regression line.

A scatter plot includes up to the first 500 visible runs. To narrow it, filter the runs, hide some runs, or ask ARIA to filter or hide runs for you or tell it which runs you are interested in.

Hover over a point to see its run and values.

![Scatter plot in ARIA session with the cursor hovered over a point](https://mintcdn.com/coreweave-dbfa0e8d/DQ0io28yQjOf8RdU/products/aria/_media/aria-scatter-plot.png?fit=max\&auto=format\&n=DQ0io28yQjOf8RdU\&q=85\&s=a4c8032c14dd8663217b511a5c5bb281)

### Parallel coordinates

A parallel coordinates panel draws each run as a line across two or more vertical axes, one for each config or summary value. The lines show which combinations of settings lead to a result. Use it to trace how several hyperparameters relate to a final metric. For example:

```text title="User prompt" theme={"system"}
Show a parallel coordinates plot of learning_rate, batch_size, dropout, and optimizer against val/accuracy.
```

ARIA orders the axes from left to right as you list them. An axis can hold numbers or categories, such as an optimizer name. The panel includes up to 500 runs that match its filters.

![Parallel coordinates panel in an ARIA chat, with axes for learning rate, batch size, dropout, optimizer, and validation accuracy](https://mintcdn.com/coreweave-dbfa0e8d/IR5o6MfXQ-4jFOnp/products/aria/_media/aria-parallel-coordinates.png?fit=max\&auto=format\&n=IR5o6MfXQ-4jFOnp\&q=85\&s=7ab00b238207e57388c7a831cc41e83b)

### Parameter importance

A parameter importance panel ranks your config parameters by how much they affect one summary metric. For each parameter, it shows an importance score and the parameter's correlation with the metric, the same table as a workspace [parameter importance panel](https://docs.coreweave.com/products/wandb/app/features/panels/parameter-importance.md). For example:

```text title="User prompt" theme={"system"}
Show a parameter importance panel for val/accuracy.
```

By default, the panel scores every config parameter. To keep bookkeeping fields out of the table, tell ARIA which parameters to score. The panel uses up to 1,000 runs that match its filters and requires at least two. To score the runs from one sweep, tell ARIA which runs to include.

### Run comparer

A run comparer arranges runs side by side, one column per run, with a row for each config, summary, and metadata value. Use it to see how a few runs differ. For example:

```text title="User prompt" theme={"system"}
Show a run comparer for the best and worst runs, with only the rows that differ.
```

The panel shows up to 10 runs. In the chat, you can search the rows and turn **diff only** on or off to hide the rows that are the same across runs.

![Run comparer panel in an ARIA chat comparing the configs of two runs, with diff only turned on](https://mintcdn.com/coreweave-dbfa0e8d/IR5o6MfXQ-4jFOnp/products/aria/_media/aria-run-comparer.png?fit=max\&auto=format\&n=IR5o6MfXQ-4jFOnp\&q=85\&s=2c40fe25f2622e84d1b7f2e6b7b1ee37)

### Media panels

A media panel shows media that your runs logged, such as images, video, audio, HTML, 3D objects, and molecules. For example:

```text title="User prompt" theme={"system"}
Show the sample_predictions images that the best run logged.
```

A media panel shows up to five media keys, and includes only runs that logged at least one of them. Use the slider to step through the logged media, and open media in full-screen view. You can ask ARIA to arrange the media as a gallery or a grid with a set number of columns.

### Attach a panel screenshot

To ask ARIA about how a panel looks, such as overlapping lines or clipped labels:

1. Click **Attach panel screenshot** below the panel. ARIA adds an image of the panel to the message box without sending it.
2. Add your question, then send the message.

**Attach panel screenshot** appears below line plots, bar charts, scatter plots, and parallel coordinates panels.

## Queue messages

The message queue holds follow-up tasks and questions you send to ARIA while it works. ARIA runs each queued message in order using the full conversation as context. The next message runs as soon as the previous one finishes.

Use the queue to line up several steps at once and step away, rather than returning to the chat to send each one. For example, you might start with a comparison:

Compare the last 10 runs and tell me which hyperparameters mattered most.

Copy user prompt

Learning rate and batch size account for most of the variance in validation loss across those 10 runs. Details for each below.

While ARIA works, send additional requests to the chat window. W\&B adds pending requests to ARIA's queue.

This example sends two messages at once:

```text title="Queued messages" theme={"system"}
Chart validation loss against learning rate for those runs.

Write up the comparison as a report I can share with my team.
```

The queue header shows how many messages are waiting. Each queued message has three controls:

* **Pencil icon** (): Edit the message before ARIA runs it. ARIA moves the message into the message box and removes it from the queue, so send it again to requeue it. This control is unavailable while the message box already holds a draft.
* **Up arrow icon** (): Run the message now instead of waiting its turn. ARIA stops what it's working on and runs this message next. The other queued messages keep their order.
* **Trash can icon** (): Delete the message from the queue.

Queued messages keep the context you attached to them, including [run mentions](https://docs.coreweave.com/products/aria/chat.md#add-context-to-a-conversation) and [images](https://docs.coreweave.com/products/aria/chat.md#add-an-image-to-a-conversation).

Queueing begins after your first message in a chat, because a queue needs a conversation to run against. The first message you send, and any message you send to an idle chat with an empty queue, goes to ARIA immediately. Each chat keeps its own queue, and the queues in chats you close keep running.

If ARIA needs a clarifying answer or your permission before it continues, the queue pauses until you respond. To run a queued message without responding first, click the up arrow icon next to it.

## Jump to an earlier message

In a long conversation, use the turn rail to return to an earlier message without scrolling. After you send your second message in a conversation, the rail appears along the right edge of the chat window. The rail has one mark for each message you sent.

![ARIA chat window with a preview card beside the turn rail, showing the first message's prompt and the start of ARIA's response](https://mintcdn.com/coreweave-dbfa0e8d/TqJiI6Q_VIg7BlKk/products/aria/_media/aria-turn-rail.png?fit=max\&auto=format\&n=TqJiI6Q_VIg7BlKk\&q=85\&s=ab6200118a716de6a982e9a75b1f7cd0)

Use the rail to preview, jump to, and track your messages:

* **Preview a message**: Move the pointer along the rail. The marks near the pointer widen, and a card shows the start of your message and a preview of ARIA's response.
* **Jump to a message**: Click a mark. The chat scrolls until your message is at the top of the chat window.
* **See where you are**: The mark for the message at the top of the chat window stays highlighted as you scroll.

To use the keyboard, press **Tab** to move focus to a mark and show its preview card. Then press **Enter** to jump to its message.

## Manage conversations

The following sections describe how to view, rename, pin, share, and delete your conversations.

### View chat history

To view previous conversations:

1. Open ARIA.
2. Click **** (**Reveal chat history**) to open the chat history sidebar. It's collapsed by default. The same control reads **Collapse chat history** while the sidebar is open.
3. Select a conversation to resume it.

The sidebar lists conversations in this order:

1. **Pinned**: Conversations you pinned, not grouped by date.
2. **Shared with you**: Conversations that others [shared with you](#share-a-conversation).
3. Your other conversations, grouped **Today**, **Yesterday**, **Last 7 Days**, **Last 30 Days**, then by month, then by month and year for conversations older than a year. Within each group, the most recently active conversation appears first.

A shared conversation appears in **Shared with you** after you open it from its link. The group lists up to 10 shared conversations that you opened in the current browser, most recently opened first. A conversation you shared, or one shared with you, shows **** next to its title.

Hover over a conversation row, or focus it with the keyboard, to reveal two controls:

* **** (**Pin chat** / **Unpin chat**): see [Pin a conversation](#pin-a-conversation).
* **** (**Chat actions**): opens a menu with **Rename chat**, **Share chat**, and **Delete chat**. See [Rename a conversation](#rename-a-conversation), [Share a conversation](#share-a-conversation), and [Delete previous conversations](#delete-previous-conversations).

A conversation shared with you has no pin control, and its **Chat actions** menu offers only **Remove**, which removes the conversation from **Shared with you**.

The chat history sidebar's **Customize** section also lists the ARIA automations you've created. See [Use automations with ARIA](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md).

### Rename a conversation

When you send the first message in a new chat, ARIA generates a title for the conversation. The title shimmers in the chat history sidebar while ARIA writes it. If ARIA can't generate a title, the conversation keeps an excerpt of your first prompt as its title. ARIA titles a conversation only once. Follow-up messages don't change the title.

To give a conversation a different title:

1. In the chat history sidebar, hover over the conversation you want to rename.
2. Click **** (**Chat actions**), then select **Rename chat**. The title becomes an editable field.
3. Type a title, up to 255 characters.
4. Press **Enter** or click **** (**Save chat title**) to save. Press **Escape** or click **** (**Cancel rename**) to discard your change.

Clearing the field and saving replaces the title with an excerpt of your first prompt, or **Untitled conversation** if no excerpt exists. Saving whitespace-only input cancels the rename instead of clearing the title.

Renamed titles sync across your open browser tabs. You can also rename a chat from your phone. See [Chat with ARIA](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/mobile-app.md#chat-with-aria) in the mobile app docs.

### Pin a conversation

Pin a conversation to keep it at the top of the chat history sidebar instead of letting it slide down as new chats accumulate.

1. In the chat history sidebar, hover over the conversation you want to pin.
2. Click **** (**Pin chat**). The conversation moves under the **Pinned** header.
3. To unpin, click **** (**Unpin chat**) on a pinned conversation.

There's no limit on how many conversations you can pin, and pin changes sync across your open browser tabs. Pinning affects only your own conversation list.

### Share a conversation

Share a conversation to show your organization an analysis, or to show a teammate what ARIA can do. Conversations are private to you by default. When you share one, members of your organization who have the link can read the conversation, including its panels and any messages you add later.

To share a conversation:

1. Open the conversation you want to share. You can share only conversations you started, after you send the first message.
2. Click **** (**Share chat**) at the top of the chat window. You can also open the conversation's **** (**Chat actions**) menu in the chat history sidebar and select **Share chat**.
3. Under **Access**, select **Anyone at** followed by your organization's name. The conversation is shared with the organization it belongs to. If you belong to more than one organization, you can share a conversation only with the organization where you started it.
4. Click **Copy link**, then send the link to the people you want to read the conversation.

To stop sharing, open the **Share chat** dialog again and select **Only you**. Members of your organization can no longer open the conversation.

When a member of your organization opens a shared conversation, they get a read-only view:

* They can read the conversation and explore its panels. Panels load data from the conversation's project when they display, using the viewer's own access. If the viewer doesn't have access to that project, the panels don't load.
* They can't send messages to continue the conversation. In place of the message box, a line names the owner and the organization and reads **View only**.

### Delete previous conversations

To delete a previous conversation:

1. Open ARIA.
2. Click **** (**Reveal chat history**) to open the chat history sidebar.
3. Hover over the conversation you want to delete, click **** (**Chat actions**), then select **Delete chat**.
4. In the **Delete this chat?** dialog, click **Delete** to confirm. You can't undo this action.

## Undock chat window

You can undock the chat window into a separate window, which allows you to view ARIA's response side-by-side with your project data.

To undock the chat, click the undock icon in the upper right corner of the chat window next to the close (**X**) button.

## Add context to a conversation

Attach runs, workspace panels, and Weave traces and evaluations to a chat to give ARIA the exact context for your question. Each item appears in the message box as a removable tag. You can attach several items to a message. Adding context doesn't send the message on its own. When you're ready, click **Send**.

When you add context from a page, ARIA adds it to the conversation that's open in the chat window. If no conversation is open, ARIA starts a new one.

### Mention a run

Type `@` in the message box and select a run. For example, you can ask ARIA to analyze a specific run by including the run's name in your prompt:

```text title="User prompt" theme={"system"}
Analyze the run @run-20230615_123456-abcdefg and summarize the results
```

You can also add a run from the runs list on the **Workspace** or **Runs** tab. Hover over the run, click its **action ()** menu, then select **Ask ARIA**.

### Add a workspace panel

To attach a workspace panel to a chat:

1. In your workspace, hover over the panel and click its **action ()** menu.
2. Select **Ask ARIA**. ARIA opens with the panel attached.
3. Type your question, such as `Why does loss spike after step 2,000?`, then send it.

**Ask ARIA** appears in panel menus in workspaces you can edit. It doesn't appear in panels in reports.

### Add Weave traces and evaluations

In Weave, click the ARIA button to attach traces, evaluations, or evaluation results to a chat. Hover over the button to see its label, such as **Ask ARIA about this trace** or **Ask ARIA about these evals**. The button appears in these places:

* **Traces** or **Evals** table: Select one or more rows. The button appears in the table toolbar and attaches every selected row.
* **Trace or evaluation details page**: The button appears in the page header.
* **Evaluation comparison**: When you compare evaluations and view an example's details, the button attaches the predictions and scores for that example.

ARIA uses the attached traces and evaluations to answer your question. For example:

```text title="User prompt" theme={"system"}
Why did the model score lower on these examples than in the previous evaluation?
```

## Add an image to a conversation

Click the plus icon (`+`) in the lower left corner of the chat window to add an image to your conversation. You can then ask ARIA to analyze the image or provide information about it.

## Grant network access

When a task needs a domain that ARIA's sandbox blocks, ARIA asks you for network access and waits for your answer. For example, a task that installs a Python package needs `pypi.org` and `files.pythonhosted.org`. By default, the sandbox where ARIA runs code can reach W\&B services but blocks most other domains on the internet.

The request appears in the chat under **The agent is requesting network access**. It shows the reason for the request and lists the requested domains, all selected. Respond to the request in one of these ways:

* To grant access, clear any domains you don't want to allow, then click **Grant access**. ARIA continues its work and can reach the granted domains.
* To deny access, click **Deny**. ARIA continues without the extra access.

While a request is waiting, you can't send messages, and queued messages don't run.

> [!WARNING]
>
> Code that runs in the sandbox can send data to any domain you grant. Grant access only to domains you trust.

Granted domains stay available for the rest of the conversation until you revoke them. Each new chat starts with only the default access. You can't add domains yourself. ARIA requests them when a task needs them.

### Review or revoke network access

After you grant access in a conversation, **** (**Manage network access**) appears in the message box, next to the plus icon (`+`).

To revoke access:

1. Click **** (**Manage network access**). A list of the conversation's granted domains opens.
2. Clear the domains you want to revoke.
3. Click **Update access**.

W\&B sends ARIA a message listing the revoked domains, and ARIA runs without them from then on. You can't change network access while ARIA is working.

## Provide feedback

Click the thumbs up or thumbs down icon at the end of the response to provide feedback on ARIA's response. Your feedback helps W\&B improve ARIA's performance and accuracy.

For information about how W\&B handles data usage for ARIA, see [Governance and security](https://docs.coreweave.com/products/aria/governance.md).
