# Console logs

Source: https://docs.coreweave.com/products/wandb/app/console-logs

# Console logs

> View and debug console log messages including info, warnings, and errors from your Weights & Biases experiment runs.

When you run an experiment, you might notice messages printed to your console. Weights & Biases captures console logs and displays them in the W\&B App. Use these messages to debug and monitor the behavior of your experiment.

The following sections describe how to view, configure, search, filter, download, and copy console logs for your runs.

## View console logs

View a run’s console logs in the W\&B App to inspect messages generated during the run.

1. Navigate to your project in the W\&B App.
2. Select a run from the **Runs** table.
3. Select the **Logs** tab on the run page.
4. Optional: For an actively streaming run, select **Jump to bottom** to return to the latest logs after scrolling up.

While logs are streaming, an ellipsis icon () appears in the upper-right corner. When log polling finishes, Weights & Biases replaces the icon with a download button ().

## Types of console logs

Weights & Biases captures three types of console logs and adds a prefix to indicate each log's severity. The prefix helps you scan logs and identify the messages most relevant to debugging. The following table summarizes each type, ordered from most to least severe.

| Severity | Prefix | Description | Example |
| - | - | - | - |
| Error | `ERROR` | Serious issues that might prevent the run from completing successfully. | `ERROR Failed to save notebook.` |
| Warning | `WARNING` | Potential issues that don't stop execution. | `WARNING Found .wandb file, not streaming tensorboard metrics.` |
| Info | `wandb:` | Updates about the run's progress and status. | `wandb: Starting Run: abc123` |

## Console log settings

To control which types of console output Weights & Biases captures and displays, pass a [`wandb.Settings`](https://docs.coreweave.com/products/wandb/ref/python/experiments/settings) object to `wandb.init()` when you initialize a run. The relevant parameters include `show_errors`, `show_warnings`, `show_info`, and `silent`. The [Settings reference](https://docs.coreweave.com/products/wandb/ref/python/experiments/settings.md) lists every parameter and is generated from the SDK, so it stays current as new options are added.

The example below toggles whether informational messages, warnings, and errors from Weights & Biases appear in the **Logs** tab. Set `silent=True` to suppress all Weights & Biases console output (useful when you want a quiet training script):

```python theme={"system"}
import wandb

settings = wandb.Settings(
    show_errors=True,
    silent=False,
    show_warnings=True,
)

with wandb.init(settings=settings) as run:
    run.log({"accuracy": 0.95})
```

For stdout and stderr capture (`console`), multipart uploads (`console_multipart`, `console_chunk_max_bytes`, `console_chunk_max_seconds`), and troubleshooting, see the sections below and the Settings reference. Distributed training and other edge cases are covered in [Why is console output not captured for my run?](https://docs.coreweave.com/support/models/articles/why-is-console-output-not-captured-for-my-run).

### Multipart console logging

By default, Weights & Biases stores your script's stdout and stderr as a single `output.log` file and uploads it *when the run finishes*. While a run is active, the **Logs** tab streams output for viewing, but `output.log` does not appear on the **Files** tab until the run completes.

Enable multipart console logging when you need downloadable logs while a run is still active, when a run may crash before it finishes, or when you resume a run and want to preserve log output from earlier sessions. Set `console_multipart=True` (SDK v0.22.3 or later) so the SDK writes timestamped chunks under `logs/` and uploads each chunk when it closes. Use `console_chunk_max_bytes` and `console_chunk_max_seconds` to control rollover; see the [Settings reference](https://docs.coreweave.com/products/wandb/ref/python/experiments/settings.md) for defaults and behavior when both are `0`.

> [!NOTE]
>
> Uploaded chunks are immutable. Terminal control sequences that modify previous lines (for example, progress bars that use carriage returns) only affect the current chunk.

```python theme={"system"}
import wandb

with wandb.init(
    project="my-project",
    settings=wandb.Settings(
        console_multipart=True,
        console_chunk_max_bytes=1_000_000,  # rotate at ~1 MB
        console_chunk_max_seconds=60,     # or every 60 seconds, whichever first
    ),
) as run:
    print("Logs upload in chunks while this run is active.")
```

You must set `console_multipart` at `wandb.init` time. Upload cadence cannot be changed after a run has started.

For troubleshooting (console capture disabled, distributed training, resumed runs, and display limits), see [Why is console output not captured for my run?](https://docs.coreweave.com/support/models/articles/why-is-console-output-not-captured-for-my-run) and [How do I download the console log file from a run?](https://docs.coreweave.com/support/models/articles/how-do-i-download-the-console-log-file-from-a-run).

## Custom logging

If you already have your own logging setup, you can continue to use it alongside Weights & Biases. Weights & Biases captures console logs from your application, but it doesn't interfere with your own logging setup. You can use Python's built-in `print()` function or the `logging` module to log messages.

```python theme={"system"}
import wandb

with wandb.init(project="my-project") as run:
    for i in range(100, 1000, 100):
        # Logs to W&B and prints to console
        run.log({"epoch": i, "loss": 0.1 * i})
        print(f"epoch: {i} loss: {0.1 * i}")
```

The console logs look similar to the following:

```text theme={"system"}
1 epoch:  100 loss: 1.3191105127334595
2 epoch:  200 loss: 0.8664389848709106
3 epoch:  300 loss: 0.6157898902893066
4 epoch:  400 loss: 0.4961796700954437
5 epoch:  500 loss: 0.42592573165893555
6 epoch:  600 loss: 0.3771176040172577
7 epoch:  700 loss: 0.3393910825252533
8 epoch:  800 loss: 0.3082585036754608
9 epoch:  900 loss: 0.28154927492141724
```

## Timestamps

Weights & Biases automatically adds timestamps to each console log entry. This lets you track when each log message was generated.

To show or hide timestamps in the console logs, select the **Timestamp visible** drop-down list on the console logs page.

## Search console logs

Use the search bar on the console logs page to find specific text, such as labels, keywords, or error messages.

As new logs stream in, Weights & Biases updates the match count.

## Filter with custom labels

> [!WARNING]
>
> Parameters prefixed by `x_` (such as `x_label`) are in public preview. Create a [GitHub issue in the Weights & Biases repository](https://github.com/wandb/wandb) to provide feedback.

You can filter console logs based on the labels you pass as arguments for `x_label` in `wandb.Settings`. Enter the label in the search bar on the console logs page.

```python theme={"system"}
import wandb

# Initialize a run in the primary node
with wandb.init(
    entity="[ENTITY-NAME]",
    project="[PROJECT-NAME]",
    settings=wandb.Settings(
        x_label="[CUSTOM-LABEL]"  # (Optional) Custom label for filtering logs
    )
) as run:
    # Your code here
```

## Download console logs

To save logs locally for offline analysis or sharing, download console logs for a run in the W\&B App:

1. Navigate to your project in the W\&B App.
2. Select a run within the **Runs** table.
3. Click the **Logs** tab in the project sidebar.
4. Click the download log file button () on the console logs page.

You might be temporarily unable to download logs while a run is actively streaming them. During streaming, Weights & Biases replaces the download button with an ellipsis icon (). Wait until the run finishes or stops streaming, and then try again.

## Copy console logs

To paste logs into another tool or message, copy console logs for a run in the W\&B App:

1. Navigate to your project in the W\&B App.
2. Select a run within the **Runs** table.
3. Click the **Logs** tab in the project sidebar.
4. Click the copy button on the console logs page.
