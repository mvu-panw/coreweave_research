# Save and diff code

Source: https://docs.coreweave.com/products/wandb/app/features/panels/code

# Save and diff code

> Enable code saving, compare code across W&B runs with the code comparer, and capture Jupyter session history.

Use Weights & Biases to save your code, compare code across runs, view local changes, and capture Jupyter session history.

## Enable code saving

Configure code saving for your team or organization. Team and organization controls are documented in [Configure privacy settings](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md).

> [!NOTE]
>
> By default, Weights & Biases disables code saving for all teams. Before you can turn it on for a team, an organization admin must leave **Disable default code saving** turned off for the organization. See the [Organization](#organization) section.

### Team

To enable code saving for a team as a team admin, navigate to the **Settings** page, then go to the **Privacy** section, and configure **Enable code saving by default** for runs in that team. This option is available only when an organization admin has not turned on **Disable default code saving** for the whole organization. For navigation steps, see [Configure privacy settings for a team](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#configure-privacy-settings-for-a-team).

### Organization

As an organization admin, navigate to **Settings**, select **Privacy**, then use **Disable default code saving** in the **Project and content security** section to control whether code saving is off by default for every team. While that setting is on, team admins can't turn on **Enable code saving by default** for their team. For the full list of organization controls, see [Enforce privacy settings for all teams](https://docs.coreweave.com/products/wandb/platform/hosting/privacy-settings.md#enforce-privacy-settings-for-all-teams).

## Save code

Capture source code that produced a run as an [artifact](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md). The code artifact is viewable within your project's workspace.

There are two ways to save code: a fine-grained approach and an automatic approach.

### Fine grain control

Use `wandb.Run.log_code()` to log specific files or directories as an [artifact](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md).

By default, Weights & Biases walks through the current directory and logs all files that end with `.py`.

The following example shows how to use `wandb.Run.log_code()` to log the current directory:

```python theme={"system"}
import wandb

with wandb.init() as run:
    # Log the current directory as a code artifact
    run.log_code(root=".")
```

The following example shows how to use `wandb.Run.log_code()` with `include_fn=` and `exclude_fn=` parameters to specify which files to include and exclude when you log code:

```python theme={"system"}
import wandb

with wandb.init() as run:
    run.log_code(
         root="../",
         include_fn=lambda path: path.endswith(".py") or path.endswith(".ipynb"),
         exclude_fn=lambda path, root: os.path.relpath(path, root).startswith(
             "cache/"
         ),
    )
```

For more control over the types and locations of source code files that Weights & Biases saves, see the [reference docs](https://docs.coreweave.com/products/wandb/ref/python/experiments/run.md#log_code).

### Automatically capture code

Use `wandb.init(settings=wandb.Settings(code_dir=))` to automatically capture all code in the current directory and subdirectories. By default, Weights & Biases captures:

* Files ending in `.py`
* requirements.txt
* Dockerfile
* Excludes anything under `wandb/` or `.wandb/`

The following example shows how capture all code in the current directory and subdirectories:

```python theme={"system"}
import wandb

with wandb.init(settings=wandb.Settings(code_dir=".")) as run:
    # Your training code here
```

You can also specify a different directory by replacing `.` with the path to the directory that you want to capture.

## View local changes

Weights & Biases generates diff files when you log code with staged or unstaged changes in your Git repository, and you can view the changes in the W\&B UI.

Weights & Biases names the diff files `diff.patch` or `diff_<sha>.patch`. These files contain local code changes that are not yet committed to Git, relative to `HEAD`.

To view diff files:

1. Navigate to your project's workspace.
2. In the left sidebar, click **Workspace**.
3. In the run selector, select the run whose diff you want to view.
4. On the run **Overview** page, select the **Files** tab.
5. From the list of files, select the `diff.patch` or `diff_<sha>.patch` file.
6. Select a file from the list to expand the diff for that file.

Weights & Biases supports two modes for viewing the diff across runs: *unified* and *split*.

* Unified view shows the diff in a single pane:

  ![Diff patch unified view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diff_unified_view.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=e9e70ee524d46ab1fad4f4acd6496168)

* Split view shows the diff in two panes, side-by-side:

  ![Diff patch split view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diff_split_view.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=9a13d394d56b24dab5a524183c37c44d)

Toggle between the two views by selecting either the **Unified** or **Split** buttons in the upper right corner of the diff view, below the **Download** button.

## Jupyter session history

Weights & Biases saves the history of code executed in your Jupyter notebook session. When you call `wandb.init()` inside of Jupyter, Weights & Biases adds a hook to automatically save a Jupyter notebook containing the history of code executed in your current session.

1. Navigate to your project's workspace that contains your code.
2. Select the **Artifacts** tab in the project sidebar.
3. Expand the **code** artifact.
4. Select the **Files** tab.

![Jupyter session history](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/jupyter_session_history.gif?s=f3d7f95da48784cb05e41a1b854f8ec9)

This displays the cells that ran in your session along with any outputs created by calling IPython's `display` method. This lets you see exactly what code ran within Jupyter in a given run. When possible, Weights & Biases also saves the most recent version of the notebook, which you find in the code directory as well.

![Jupyter session output](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/jupyter_session_history_display.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8be116a89181083f0c994627894adaee)

## Compare code across runs

Compare code used in different W\&B runs:

1. Select the **Add panels** button in the top right corner of the page.
2. Expand **TEXT AND CODE** dropdown and select **Code**.

![Code comparer panel](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/code_comparer.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=fe09c2fd7401fcf13e1cada70c0f2d50)
