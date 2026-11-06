# Developer tools

Source: https://docs.coreweave.com/products/notebooks/developer-tools

# Developer tools

Use the developer panel to troubleshoot notebook code, inspect execution, view logs, and access the terminal.

![Developer panel open at the bottom of the notebook editor](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/notebooks/_media/hello_world_dev_panel.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=e7aab6da8b6a2a0033e719e75883a566)

## Open the developer panel

Use one of the following methods:

* In the notebook footer, select **Developer panel**.
* Press **Command+J** on macOS or **Ctrl+J** on Windows or Linux. This shortcut opens or closes the panel.

## Inspect errors and warnings

The **Errors** tab shows errors and warnings throughout the notebook, including Python exceptions, syntax errors, cycles, invalid reactive dependencies, and variables defined in multiple cells.

## Use the scratchpad

Use the **Scratchpad** tab to run temporary Python code without adding it to the notebook's reactive graph. The scratchpad can access variables defined by notebook cells.

Unlike notebook cells, the scratchpad doesn't enforce unique global variable names. Code and variables defined in the scratchpad are not saved. Copy any code that you want to keep into a notebook cell.

To run the scratchpad code, press **Command+Enter** on macOS or **Control+Enter** on Windows or Linux. Alternatively, select **Run** ().

Scratchpad output appears to the right of the code.

![Code and output displayed in the Scratchpad tab](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/notebooks/_media/hello_world_scratchpad.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=3d48b9f897f99d71fac60bbb622dddaa)

## Inspect execution traces

Use the **Tracing** tab to inspect the order and duration of cell executions. Traces can help you identify slow or failed cells and determine which cells ran during a reactive execution event.

Each **Run** heading groups cells that ran during the same execution event. The horizontal bars show when each cell ran and compare its duration with other cells in the event. Each entry includes a cell link, code preview, duration, and status icon. The status icon indicates whether execution succeeded, failed, or was interrupted.

Short executions might display `0 ms` because durations are rounded. Hover over a trace entry to view precise start and end times. Select a cell link to open the corresponding notebook cell.

Select **Clear** to remove the displayed trace history. Clearing the history doesn't remove notebook cells or variables.

Enable **Inline chart** to display execution timing near the corresponding notebook cells.

The following image shows the "Hello World" notebook with the **Tracing** tab open in the developer panel. `cell-4` defines the variable pet, and `cell-5` uses it to produce the output "Do you have a cat?". Both cells completed successfully. The trace shows a duration of 14 ms for `cell-4` and `0 ms` for `cell-5`. A tooltip shows the precise start and end times for `cell-5`.

![Tracing tab showing cell execution order, status, and duration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/notebooks/_media/hello_world_tracing.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5cf2448675b25c41db5d9a107ce800c3)

## View logs

Use the **Logs** tab to view standard output (`stdout`) and standard error (`stderr`) from notebook cells and the scratchpad. Use the logs to investigate execution failures that don't produce a clear inline error.

The following image shows the output `"Do you have a cat?"` logged at `[5:42:51 PM]` by the corresponding notebook cell.

![Logs tab showing standard output and error output from the notebook](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/notebooks/_media/hello_world_logs.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=76ba2fe3ea3038089dc2b529951f42e1)

> [!NOTE]
>
> The **Logs** tab also includes output and errors from the [**Scratchpad**](https://docs.coreweave.com/products/notebooks/developer-tools.md#use-the-scratchpad). In the image, the entry at `[5:44:00 PM]` is identified as `cell--1` and comes from the scratchpad.

## Use the terminal

Use the **Terminal** tab to open a shell in the same sandbox environment as the notebook runtime. From the terminal, you can inspect files, run command-line tools, manage packages, and execute scripts. Changes made in the terminal apply to the same workspace as the notebook.
