# Create a custom tag

Source: https://docs.coreweave.com/products/agent-lens/tags/create-tag

# Create a custom tag

> Create a custom Agent Lens tag and turn on AI evaluation to label agent turns automatically.

A tag labels an agent turn with a behavior you define, such as `user-frustration` or `refund-policy-violated`. When you turn on **AI enabled** for a tag, CoreWeave Agent Lens uses an LLM judge to evaluate every new turn against the tag's criteria and applies the tag when the criteria clearly apply. Tags appear on turns in the [Conversations tab](https://docs.coreweave.com/products/agent-lens/conversations/view-activity.md), in the **Tags** column of the conversations table, and in the **Tags** and **Trending tags** charts on the **Overview** tab.

This page shows you how to create a tag, configure it, test it against real conversations, and turn on AI evaluation.

![The Agent Lens Tags page, listing each tag with its conversation count, when it was last used, whether AI is enabled, and its criteria.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/agent-lens/_media/tags-list.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6d4b807085156c1ab715861326778077)

## Create a tag

To create a tag in your project:

1. Navigate to [CoreWeave Forge](https://forge.coreweave.com) and select Agent Lens from the product menu.
2. Select your project. Agent Lens opens the project you used most recently. To switch projects, use the project selector at the top of the side menu.
3. In the Agent Lens side menu, select **Tags**.
4. Select **New tag**. The **New tag** page opens.
5. In **Tag**, enter a name for the tag, for example `user-frustration`.
6. Optionally, turn on **AI enabled** to have Agent Lens tag matching turns automatically, and then fill in **Criteria** and, optionally, **Filter by agent name**. See [Configure the tag](#configure-the-tag) for details.
7. Select **Create tag**.

![The New tag page with AI enabled turned on, showing the Tag, Criteria, and Filter by agent name fields.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/agent-lens/_media/new-tag-form.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=182ed6ac13185fd319bfc7370541ddac)

> [!NOTE]
>
> You can also start a tag from the **Insights** tab. Select a category, select its actions menu (**...**), and then select **Tag conversations like these**.

## Configure the tag

The tag editor has the following settings on its **Configuration** tab. The **New tag** page has the same settings. To open the editor for an existing tag, see [Edit, disable, or delete a tag](#edit-disable-or-delete-a-tag). Select **Save** after you change any of them.

### Tag

The label that Agent Lens writes onto matching turns. Use lowercase letters, numbers, and hyphens, up to 64 characters, for example `frustration-handled`. Tag names must be unique within a project.

The colored dot in the **Tag** field shows the color the tag appears as in the Agent Lens UI. Color has no effect on evaluation.

### Apply with AI

Turns automatic evaluation on for this tag. While the toggle is off, nothing evaluates the tag, and it only appears on a turn if someone [manually applies it](#apply-a-tag-manually). While the toggle is on, the tag shows an **AI enabled** badge, and the LLM judge evaluates every new turn in the project against the criteria.

Keep the following in mind:

* The judge evaluates turns as they arrive. Turning on **AI enabled** doesn't evaluate conversations that already exist in the project.
* The judge runs once per new turn for each tag with **AI enabled** on. A project with many such tags evaluates each turn many times.
* Judge inference runs on CoreWeave Serverless Inference and is billed to the project of the user who created the tag.
* Turning the toggle off stops evaluation of new turns. It doesn't remove tags that the judge already applied.

The **Criteria** and **Filter by agent name** settings appear only while **AI enabled** is on.

### Criteria

A description of exactly when the tag should apply, up to 1,600 characters. The LLM judge receives your criteria verbatim, together with the turn's system instructions, user messages, agent responses, tool activity, and status, and applies the tag only when the criteria clearly apply.

Write criteria the way you would brief a reviewer:

* State what must be present in the turn, not what the tag is about, for example `The agent recognizes that the user is frustrated and changes its approach in response` is more precise than `Frustration handling`.
* Name the evidence the judge should look for, such as specific phrases, a refusal without a reason, or a tool call that returned an error the agent ignored.
* Specify what does not count.
* Keep it to one behavior per tag.

### Filter by agent name (optional)

Limits the judge to turns from the agents you list. Leave the field empty to evaluate every turn in the project.

When a new turn arrives, Agent Lens compares the agent name recorded on that turn to the names in this field. The comparison is an exact, case-sensitive string match. If the turn's agent name matches one of the listed names, or if the field is empty, the judge evaluates the turn. Otherwise, the judge skips the turn for this tag.

Use the filter when a project holds more than one agent and a tag only makes sense for some of them. For example, a `refund-policy-violated` tag belongs on a `support-agent`, not on a `research-agent` that shares the project.

Each name must match what your agent sends in its traces. To confirm the exact name, open any conversation from that agent on the **Conversations** tab, enable the **Agent** column, and check the agent name shown on its turns. The filter doesn't accept wildcards or partial matches, and it has no effect on tags applied by hand.

## Test a tag before you enable it

The **Alignment** tab lets you test the judge against turns you choose, without applying any tags, so you can tune the criteria before it evaluates live traffic.

The tab has four panes. **Test criteria** on the left holds a scratch copy of the tag's criteria that you can edit freely. **Test turns** lists the example turns you have added. The next pane shows the selected turn. **Test results** on the right shows your expected result for the turn, the tags the judge assigned, and the test status.

To test your judging criteria:

1. In the tag editor, select **Alignment**.
2. In **Test turns**, select **Add turns**. A list of your project's conversations opens.
3. Open a conversation and select the **+** icon beside each turn you want to add. Choose turns where you already know whether the tag should apply, and include some where it should not.

   ![A turn in the conversation draw with the + button highlighted.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/agent-lens/_media/add-a-turn-to-test-a-tag.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=439b64796c2d950a99d3d5c9092b9150)
4. For each test turn, set the expected result in **Test results**: under **Expected results**, select the tag name if the tag should apply, or **No tag** if it shouldn't.
5. Optionally edit the text in **Test criteria**. The test uses this text, not the saved criteria, so you can try a variation without changing the live tag.
6. Select **Run test**.

Agent Lens sends each example turn to the judge with the test criteria and compares the verdict to your expected result. Each example shows one of the following states:

| State | Meaning |
| - | - |
| **Pass** | The judge agreed with your expected result. |
| **Fail** | The judge disagreed with your expected result. |
| **Unlabeled** | You have not set an expected result for this example yet. |
| **Unscored** | The test has not run on this example yet. |

The footer of **Test turns** shows the pass rate across labeled examples. For any example, **Assigned tags** shows whether the judge applied the tag, and **Reasoning** shows the one-sentence rationale it gave. Use failing examples to refine the text in **Test criteria**, then run the test again.

You can also add a turn while you review a conversation.  On the **Conversations** page, after you select a conversation, select the turn's actions menu (**...**), and then select **Add to test turns**.

Edits in **Test criteria** are not saved to the tag. When the pass rate is where you want it, copy the final text into **Criteria** on the **Configuration** tab of the **Tags** page, turn on **AI enabled**, and select **Save**.

## Apply a tag manually

You can label a turn yourself, whether or not **AI enabled** is on for the tag:

1. On the **Conversations** tab, open a conversation.
2. On the **Thread** tab, find the turn and select **Add tag** in its header.
3. Search for an existing tag, or type a new label and select **Create** to add it.

Tags applied by hand are recorded separately from tags applied by the judge, and **Filter by agent name** does not apply to them. Labels you create this way do not become configured tags. To give a label criteria and a judge, create it from the **Tags** page instead.

## Edit, disable, or delete a tag

To edit or disable a tag:

1. On the **Tags** page, select the actions menu (**...**) beside the tag you want to manage, and then select **Edit**.
2. On the **Configuration** tab, update the tag's name or criteria. To stop automatic evaluation, turn off **AI enabled**.
3. Select **Save**.

To delete a tag, on the **Tags** page, select the actions menu (**...**) beside the tag, and then select **Delete**. Confirm the deletion when prompted.

## View tagged conversations and turns

When Agent Lens applies tags to your conversations, the tags appear in the **Tags** column of the **Conversations** tab. Tagged conversations also appear in the **Tags** and **Trending tags** panes in the **Overview** tab.

You can select a tag to filter the **Conversations** tab by that tag.
