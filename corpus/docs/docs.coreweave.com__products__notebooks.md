# Notebooks overview

Source: https://docs.coreweave.com/products/notebooks

# Notebooks overview

> Use Notebooks to develop, debug, and share interactive model workflows in Forge.

Use Notebooks to create interactive, reactive Python notebooks. Notebooks are useful for exploring data, prototyping model workflows, analyzing Weights & Biases runs and artifacts, and sharing reproducible work with collaborators.

Notebooks is in public preview in Forge.

Each notebook runs in a temporary sandbox provided by [CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes.md), with isolated compute for notebook cells, packages, files, and terminal commands.

Notebooks use [marimo](https://docs.marimo.io/) as the notebook runtime and editor. Unlike traditional notebooks that run from top to bottom, Notebooks track dependencies between cells. When a value changes, the notebook can identify the downstream cells that depend on it and keep outputs consistent with the current notebook state.

## Get started

If you are new to notebooks, start with the [Get started](https://docs.coreweave.com/products/notebooks/get-started.md) guide. The guide walks you through creating a notebook, running code, viewing logged metrics in a Weights & Biases workspace, and sharing the result.

If you already know the workflow you want, use the following pages:

> [card] [Create and manage notebooks](https://docs.coreweave.com/products/notebooks/create-notebook.md)
>
> Create, rename, duplicate, or delete notebooks from a team overview page or project workspace.

> [card] [Edit a notebook](https://docs.coreweave.com/products/notebooks/edit-notebook.md)
>
> Add Python, Markdown, and SQL cells; reorder cells; delete cells; and add interactive controls.

> [card] [Run notebook cells](https://docs.coreweave.com/products/notebooks/run-notebook-cells.md)
>
> Run stale cells, rerun every cell, stop a running cell, disable execution, or restart the runtime.

> [card] [Manage packages](https://docs.coreweave.com/products/notebooks/manage-packages-environments.md)
>
> Install, view, update, and remove Python packages from the notebook sidebar or terminal.

## Understand the notebook model

Notebooks are reactive. A cell runs based on the variables it defines and references, not only on where it appears in the notebook. This model helps keep outputs current, but it also means that notebook structure matters:

* Define each global name in only one cell.
* Avoid mutating shared objects across cells.
* Use runtime settings to choose whether downstream cells run automatically or become stale.
* Use the dependency tools to inspect how cells relate to each other.

For a deeper explanation, see [Understand reactive execution](https://docs.coreweave.com/products/notebooks/reactive-info.md) and [Configure a notebook](https://docs.coreweave.com/products/notebooks/configure-notebook.md).

## Debug and inspect notebooks

Use the developer panel to investigate notebook behavior without leaving the editor. The panel includes errors and warnings, a scratchpad for temporary code, execution traces, logs, and a terminal connected to the notebook workspace.

For details, see [Developer tools](https://docs.coreweave.com/products/notebooks/developer-tools.md).

## Billing and usage

Notebooks use Forge storage and compute from CoreWeave Sandboxes. Notebook data contributes to your organization's storage usage, while running a notebook consumes sandbox compute. Notebook workflows can also create product-specific usage when they use Weave, Serverless Inference, or Serverless Training.

Organization and billing admins can review plan details, monitor usage, configure usage and spending alerts, manage payment methods, and access invoices from [Billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md).

If your account does not have sufficient storage or sandbox capacity, you may need to free storage, purchase additional usage, upgrade your plan, or visit the [Contact Us page](https://coreweave.com/contact-us).

## Next steps

* [Get started](https://docs.coreweave.com/products/notebooks/get-started.md)
* [Understand reactive execution](https://docs.coreweave.com/products/notebooks/reactive-info.md)
* [Create and manage notebooks](https://docs.coreweave.com/products/notebooks/create-notebook.md)
* [Developer tools](https://docs.coreweave.com/products/notebooks/developer-tools.md)
