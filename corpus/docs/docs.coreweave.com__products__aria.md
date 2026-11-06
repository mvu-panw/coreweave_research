# ARIA

Source: https://docs.coreweave.com/products/aria

# ARIA

> Analyze and run experiments, explain results, and build reports with W&B's AI research agent.

ARIA, W\&B's AI Research and Iteration Agent, is your personalized research assistant that helps you analyze and run experiments, explain results, identify patterns across runs, recommend next steps, build visualizations and reports, and more in W\&B.

> [!NOTE]
>
> Available only in [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting.md#wb-multi-tenant-cloud).
>
> ARIA works in team projects, not in your personal entity. Your organization admin must also enable **Smart features**. See [Governance and security](https://docs.coreweave.com/products/aria/governance.md).

![Blank ARIA chat window](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/agent_empty_chat_window.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=42cbbdfb80efff27b38700c29a1a9260)

ARIA can help you:

* Analyze experiments to find patterns and insights.
* [Run experiments and sweeps to test new ideas](https://docs.coreweave.com/products/aria/autoresearch.md).
* Propose next steps, such as recommending hyperparameters to try.
* Create plots and panels to visualize your data.
* Build saved views and reports to share insights with your team.
* [Share a conversation with your organization](https://docs.coreweave.com/products/aria/chat.md#share-a-conversation) so its members can read your analysis.
* [Respond automatically to events in W\&B](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md), such as diagnosing a failed run or reviewing a new model version.

## Quick start

To [chat with ARIA](https://docs.coreweave.com/products/aria/chat.md):

1. From any project, click **Ask ARIA** at the upper right corner of the page.
2. In the chat window, type your question or request. If you are unsure what to ask, select a suggested prompt.
3. Click the **Send** button, the upward-pointing arrow in the lower-right corner of the chat window.

## Start ARIA from where you work

Besides **Ask ARIA** at the top of the page, you can start ARIA from buttons throughout W\&B. Most of these buttons open a new chat with a hint in the message box. You describe what you want before you send the message.

| Where | Button | What ARIA helps with |
| - | - | - |
| Crashed or failed run's page | **Debug with ARIA** | Explain why the run crashed or failed. This button starts a new chat and asks ARIA immediately. |
| Workspace **Runs** table toolbar | **Show most useful columns with ARIA** | Show, hide, pin, reorder, and resize columns in the **Runs** table. |
| **Manage columns** dialog in the **Runs** table | **Manage columns with ARIA** | Show, hide, pin, reorder, and resize columns in the **Runs** table. |
| **Filter** menu in the **Runs** table | **Describe the filters you want ARIA to create** text field | Filter the **Runs** table. Type a description of the runs you want and press **Enter**. ARIA proposes a **Run Filter**. Click it in the chat to apply it to your workspace. |
| Saved views menu | **Ask ARIA** | Create a saved view of your workspace. |
| Project's **Reports** tab | **Draft report with ARIA** | Create a new report. |
| A report you own | **Edit with ARIA** | Revise the report. ARIA saves its changes to the existing report. |

To give ARIA context about a specific run, workspace panel, or W\&B Weave trace or evaluation, see [Add context to a conversation](https://docs.coreweave.com/products/aria/chat.md#add-context-to-a-conversation).

## Follow ARIA's progress

While ARIA works, it streams its responses so you can follow its progress step by step rather than waiting for a finished answer. Depending on the complexity of your question, ARIA might take a few moments to finish. You can close the chat window while ARIA works and return to check the response later, or [queue your next message](https://docs.coreweave.com/products/aria/chat.md#queue-messages) without waiting. If ARIA needs more information, it asks you for clarification.

To help you stay in context, ARIA renders live, interactive panels from your Weights & Biases workspace directly in the chat, including the following:

* Line plots
* Bar charts
* Scatter plots
* Parallel coordinates
* Parameter importance
* Run comparer
* Media panels

When you hover over a run in the runs list on the **Workspace** or **Runs** tab, ARIA highlights the run's plots. When you hover over a panel in ARIA, the run is highlighted in the runs list on the **Workspace** tab. To learn about each panel type, see [View panels in the chat](https://docs.coreweave.com/products/aria/chat.md#view-panels-in-the-chat).

![Workspace with an ARIA loss plot in the chat, where the run hovered in the runs list is highlighted in both the ARIA plot and the workspace panels](https://mintcdn.com/coreweave-dbfa0e8d/TqJiI6Q_VIg7BlKk/products/aria/_media/aria-line-plot-interactions.png?fit=max\&auto=format\&n=TqJiI6Q_VIg7BlKk\&q=85\&s=669e97c9098cb6564cc6f3c1e14a3de6)

While ARIA works, you might see **Thinking** and **shell** steps:

* **Thinking** steps summarize how ARIA approaches your question.
* **shell** steps show when ARIA takes an action, such as creating a panel, filtering runs, creating and running Python scripts, and more.

Click on a **Thinking** or **shell** step to expand more details about ARIA's reasoning or the action it took.

For real-world examples, see [Example chats](https://docs.coreweave.com/products/aria.md#example-chats). For more information about managing chats, see [Chat with ARIA](https://docs.coreweave.com/products/aria/chat.md).

## View and manage project memories

ARIA remembers what it learns. As you work, ARIA writes *memories* scoped to your project so it doesn't need to rediscover your setup, conclusions, or preferences from scratch in every new session. Tell it once that your team prefers log-scale charts, and it sticks.

Each memory has a name and description so ARIA knows when to recall it, plus the memory text itself.

Anyone in the team that owns the project can view, edit, or delete memories:

1. In the ARIA chat window, click **** (**Reveal chat history**) to open the chat history sidebar.
2. In the **Customize** section, click **Project memory**. Each memory ARIA has about the project displays.
3. To edit a memory, click ****. Update the memory's **Name**, **Description**, or **Memory**, then click **Save**.
4. To delete a memory, click ****.

Without waiting for ARIA to learn new memories, you can create a project memory interactively. For example:

Remember that we prefer semantic coloring for charts.

Copy user prompt

I’ll check the existing project memories first so this preference is recorded under the right topic rather than duplicated ... Saved a new project memory: chart-coloring. It records that charts should use consistent, semantic colors based on series/category meaning or status rather than arbitrary palette order.

## Example chats

The following are examples of real chats with ARIA to illustrate how you can interact with ARIA and the types of responses you can expect.

> [accordion] Run experiments based on ARIA's recommendations
>
> Suppose you are an ML Engineer who has just completed a series of experiments. You want to understand what the next steps should be to improve your model's performance.
>
> To do this, you navigate to your project where you logged runs. You open ARIA and ask:
>
> ```text title="User prompt" theme={"system"}
> /recommend-next-experiment
> ```
>
> The following is an example of how ARIA responded to this question. First, ARIA makes reasoning steps to determine how to approach the question. For brevity, only a portion of ARIA's reasoning is shown below:
>
> ```text title="ARIA reasoning steps" theme={"system"}
> Recommendation: run one “longer-training + held-out-eval” experiment
> before changing model architecture or sweeping LR.
>
> Use the current best setup, but train longer:
>
> hyperparameter_config = {
>     "learning_rate": 0.1,          # keep fixed
>     "epochs": 2000,                # was 1000
>     "model_type": "Multivariate_neural_network_classifier",
>     "torch_seed": 0,               # add for reproducibility
> }
> Also add logging for the existing held-out split every epoch or
> every 10–50 epochs:
>
> train/train_loss
> train/train_acc
> test/test_loss
> test/test_acc
>
> and save the best checkpoint by test/test_loss, not only
> by training loss.
>
> Why this is the most promising next experiment
> The project has 16 finished runs, but only 4 are actual training runs;
> all four used the same training config:
>
> learning_rate = 0.1
> epochs = 1000
> same model: Multivariate_neural_network_classifier
>
> So there is no real hyperparameter comparison yet. The
> strongest signal is from the learning curves: all four
> training losses are still improving at the final epoch, and
> the minimum training loss occurs at epoch 1000 in every run.
>
> I’d run:
>
> learning_rate: 0.1
> epochs: 2000
> model_type: unchanged
> random_state: keep existing dataset split, 42
> add torch.manual_seed(0) and log it as torch_seed
> evaluate on X_test, y_test each epoch or every 10 epochs
> checkpoint on lowest test/test_loss
> ```
>
> You agree with ARIA's recommendation and ask ARIA to run the experiment for you:
>
> ```text title="User prompt" theme={"system"}
> Run that experiment for me.
> ```
>
> ARIA uses W\&B Launch to run the experiment in a sandbox environment. The following image shows ARIA's response after it has completed running the experiment:
>
> ![ARIA running an experiment](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/aria_experiment.gif?s=efb0641e6d5f23b3816b3114e50a4658)
>
> ARIA uses W\&B Launch to run experiments in a sandbox environment. See [Enable ARIA to run experiments](https://docs.coreweave.com/products/aria/autoresearch.md) for more information.

> [accordion] Gain insights on your experiments
>
> Suppose you are an ML Engineer who has just completed a series of runs for a new model. You want to understand how your model performed, identify potential issues, and decide on your next steps.
>
> To do this, you navigate to your project where you logged runs. You open ARIA and ask:
>
> ```text title="User prompt" theme={"system"}
> What patterns do you see across my runs?
> ```
>
> The following is an example of how ARIA might respond to this question. First, ARIA makes reasoning steps to determine how to approach the question:
>
> ```text title="ARIA reasoning steps" theme={"system"}
> I’m considering running a state breakdown scan with counts by state using
> specific server filters. I’ll look at the array of states: ['finished',
> 'running', 'crashed', 'failed', 'killed', 'pending', 'preempting'] and
> determine the length of each. Summing these metrics could provide
> useful insights. I should also focus on identifying objective metrics
> from sample keys while excluding those that start with "_" or "system/".
> It’s important to compute the best min/max for numeric summary metrics too.
> ```
>
> ARIA identifies that it needs to analyze the data across runs to answer the question. To do this, ARIA runs scripts in a sandbox environment that use the W\&B Python SDK to query previously logged runs and identify patterns in the data. Each step appears in the chat as it runs, and you can expand a step to see its details.
>
> ![ARIA thought process](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/agent_analyze_project.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b17fcef3080c1721c9ff778f9c9d7107)
>
> Next, ARIA uses the output to generate a summary of the patterns it found across the runs, which it shares in the chat.
>
> ![ARIA summary of patterns across runs](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/agent_analyze_summary_results.gif?s=ba700bea295669047612fe1e779af794)
>
> ARIA was able to identify that my current experiment does not log `validation/test` metrics and recommended logging those metrics in future runs to better understand the model's performance.
>
> As a next step, you can ask ARIA to help set up an experiment with validation metrics logged. For example, you can ask ARIA:
>
> ```text title="User prompt" theme={"system"}
> Can you help me update my Python script to also log validation metrics?
> ```
>
> ARIA can then generate the code to log validation metrics in your training script, which you can copy and paste into your codebase.

> [accordion] Get recommendations for hyperparameter tuning
>
> Suppose you are an ML Engineer who has just completed a series of runs for a new model. You want to understand how your model performed and get recommendations for how to improve your model's performance in future runs. You decide to ask ARIA for recommendations on hyperparameter tuning.
>
> You might ask ARIA:
>
> ```text title="User prompt" theme={"system"}
> I want to conduct a sweep to improve lower my training model's loss. Do you have suggestions on what hyperparameters I should try?
> ```
>
> ARIA might respond with the following reasoning steps:
>
> ```text title="ARIA reasoning steps" theme={"system"}
>  The user is looking for insights to improve training loss, so I
>  should suggest ranges for learning rate, optimizer, batch size,
>  weight decay, and other relevant parameters.
>
> Since the user wants to conduct a sweep, I need to show the code or
> instrumentation with a clear yet concise YAML or Python configuration.
> I might also suggest using random or Bayesian techniques for more
> effective hyperparameter selection.
> ```
>
> ARIA identifies that it needs to analyze the hyperparameters used in previous runs and their relationship to the training loss to provide recommendations for hyperparameter tuning.
>
> ARIA identifies that the given project used a learning rate of `0.01` for all runs. Based on these insights, ARIA recommends trying a lower learning rate, such as `0.001`, in future runs to see if that helps improve the model's performance.
>
> ARIA also identifies that all of the runs use the SGD optimizer. Based on this insight, ARIA recommends trying a different optimizer, such as Adam (Adaptive Moment Estimation), in future runs to see if that helps improve the model's performance.
>
> The following image shows a portion of ARIA's response with its recommendations for hyperparameter tuning:
>
> ![ARIA recommendations for hyperparameter tuning](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/agent_recommend_hyperparameter.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5c9bfe1262326e91484e95bacba5159a)

> [accordion] Create a report to share with my team
>
> Suppose you are a data scientist who has been analyzing your project's runs and identified interesting patterns in the data. You want to share these insights with your team in an easy-to-digest format. You decide to ask ARIA to help you create a [W\&B Report](https://docs.coreweave.com/products/wandb/reports.md).
>
> To do this, you open ARIA and ask:
>
> ```text title="User prompt" theme={"system"}
> Create a report to share my findings with my team.
> ```
>
> ARIA might respond with the following reasoning steps:
>
> ```text title="ARIA reasoning steps" theme={"system"}
> I’m looking to query the recent 50 runs, summarizing key frequencies 
> and counts by using api.runs to slice them down. I'll be counting
> lengths with lazy evaluation and weaving together the stats
> for a proper report.  I need to include a description that might
> require importing different report libraries.
> ```
>
> ARIA identifies that it needs to create a W\&B Report that summarizes the insights it found in the data. As part of its reasoning process, it generates a Python script that uses the W\&B SDK to create a report with the relevant data and insights. ARIA executes this script in a sandbox environment, which creates a W\&B Report in your project.
>
> The following image shows how ARIA creates a W\&B Report in the sandbox environment and then returns the link to the report in the chat:
>
> ![ARIA creates a report](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/aria/_media/agent_create_report.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=41f2b7ec4c157d0782660106cdbdf25d)
>
> > [!NOTE]
> >
> > Under the hood, ARIA creates a W\&B Report using the Workspaces and Reports API.
