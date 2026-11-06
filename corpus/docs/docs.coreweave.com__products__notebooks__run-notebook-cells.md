# Run notebook cells

Source: https://docs.coreweave.com/products/notebooks/run-notebook-cells

# Run notebook cells

Run individual cells, all stale cells, or every cell in a notebook. Notebooks use a reactive execution model that determines execution order from variable dependencies rather than cell position.

## Run all stale cells

Run all [stale cells](https://docs.coreweave.com/products/notebooks/reactive-info.md#understand-stale-and-blocked-cells) without re-running cells that already use the latest code and inputs.

> [tab] UI
>
> Click **Run all stale cells** () in the lower-right corner of the notebook.

> [tab] Keyboard shortcut
>
> Press `Esc` to enter command mode, then press **Command+Shift+R** on macOS or **Control+Shift+R** on Windows or Linux.

## Rerun all cells

Rerun every cell in the notebook:

1. Press **Command+K** on macOS or **Control+K** on Windows or Linux to open the command palette.
2. Select **Re-run all cells**.

## Stop a running cell

> [tab] UI
>
> Click **Stop** () in the cell's toolbar to stop the running cell.

> [tab] Keyboard shortcut
>
> Press **Command+I** on macOS or **Control+I** on Windows or Linux to stop the running cell.

## Disable or enable a cell

Disable a cell to prevent both the cell and its dependencies from running.

1. Press `Esc` to enter command mode.
2. To open the command palette, press **Command+P** on macOS or **Control+P** on Windows.
3. From the dropdown menu, select **Disable execution**.

## Restart the notebook runtime

Restart the runtime to clear the notebook's variables and other in-memory state.

1. Click the **action (  )** menu in the upper-right corner of the notebook.
2. From the dropdown menu, select **Restart kernel**.

For more information, see [Disabling cells](https://docs.marimo.io/guides/reactivity/#disabling-cells).
