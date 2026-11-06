# Edit a notebook

Source: https://docs.coreweave.com/products/notebooks/edit-notebook

# Edit a notebook

This page describes common notebook actions, including adding, editing, reordering, and deleting cells, as well as using interactive controls and displaying content.

## Edit modes

There are two edit modes:

* **Command mode**: Perform actions on cells, such as adding, deleting, and moving them. Press `Esc` to enter command mode.
* **Edit mode**: Change the contents of the selected cell. Press `Enter` to enter edit mode.

## Add a cell

Notebooks support [Python](#python-cell), [Markdown](#markdown-cell), and [SQL](#sql-cell) cells. Add a cell using the notebook UI or a keyboard shortcut.

> [tab] UI
>
> Within a notebook, select the `PYTHON`, `MARKDOWN`, or `SQL` button to create a cell of that type.

> [tab] Keyboard Shortcuts
>
> Press `Esc` to enter command mode then use one of the following shortcuts:
>
> | Action | Shortcut |
> | - | - |
> | Create a new cell above the current cell | **Command + Shift + O** |
> | Create a new cell below the current cell | **Command + Shift + P** |
>
> See [Keyboard Shortcuts](https://docs.marimo.io/guides/editor_features/overview/?h=keyboar#keyboard-shortcuts) for a full list of available shortcuts.

## Change cell order

Change the order of cells within a notebook using the drag handle or keyboard shortcuts.

> [tab] UI
>
> Select the drag handle () on the right side of the cell and moving it to the desired position.

> [tab] Keyboard Shortcuts
>
> Press `Esc` to enter command mode. Then use one of the following shortcuts:
>
> | Action | Shortcut |
> | - | - |
> | Move cell up | **Command + Shift + 9** |
> | Move cell down | **Command + Shift + 0** |

## Delete a cell

Delete a cell using the UI or a keyboard shortcut.

> [tab] UI
>
> Use either of the following methods:
>
> 1. Right-click the cell, then select **Delete** from the context menu.
> 2. Select the trash can icon next to the cell.

> [tab] Keyboard Shortcuts
>
> Use the following keyboard shortcut to delete a cell:
>
> 1. Press `Esc` to enter command mode.
> 2. Press **Command + Shift + Backspace** to delete the current cell.

## Add interactive controls

Add interactive elements, such as sliders, dropdowns, and buttons, to notebook cells. When you interact with an element, the notebook updates cells that depend on its value.

For example, copy the following code into a cell to create a basic interactive slider:

```python theme={"system"}
import marimo as mo

slider = mo.ui.slider(1, 10)
mo.md(f"Choose a value: {slider}")
```

For more information, see [Interactive elements](https://docs.marimo.io/guides/interactivity/) in the marimo documentation.
