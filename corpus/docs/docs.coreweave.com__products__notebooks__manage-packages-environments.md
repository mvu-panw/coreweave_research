# Manage packages

Source: https://docs.coreweave.com/products/notebooks/manage-packages-environments

# Manage packages

Install, view, update, or remove Python packages from the **Manage packages** sidebar or the notebook terminal.

> [!NOTE]
>
> The default notebook sandbox environment includes the [W\&B Python SDK](https://docs.coreweave.com/products/wandb/ref/python.md), [Reports and Workspaces API](https://docs.coreweave.com/products/wandb/ref/wandb_workspaces/reports.md), [marimo](https://docs.marimo.io/), and other commonly used packages.

## Install a package

Install Python packages using either the sidebar or the terminal.

> [tab] Sidebar
>
> To install a package from the sidebar:
>
> 1. From the notebook sidebar, select **Manage packages** ().
> 2. Enter the package name.
> 3. Select **Add**.

> [tab] Terminal
>
> Open the developer panel, then select the **Terminal** tab. Run the following command:
>
> ```bash theme={"system"}
> uv pip install [PACKAGE_NAME]
> ```

Refer to the [marimo documentation](https://docs.marimo.io/guides/package_management/).

## View installed packages

View installed packages using either the sidebar or the terminal.

> [tab] Sidebar
>
> To view installed packages:
>
> 1. In the notebook sidebar, select () **Manage packages**.
> 2. Select one of the following views:
>    * **List**: Displays a flat list of installed packages.
>    * **Tree**: Displays the package dependency hierarchy. Each dependency appears as a child of the package that requires it.
>
> The following image shows `wandb-workspaces` in the **Manage packages** sidebar. Packages nested under it are the dependencies of `wandb-workspaces`.
>
> ![Manage packages sidebar in the notebook](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/notebooks/_media/hello_package_management.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6eee83a1c34a2d8d98ce8d821341573a)

> [tab] Terminal
>
> Open the developer panel, then select the **Terminal** tab. Run the following command:
>
> ```bash theme={"system"}
> uv pip list
> ```

## Update a package

Update a package using either the sidebar or the terminal.

> [tab] Sidebar
>
> 1. Select **Manage packages** () from the notebook sidebar.
> 2. Type or search for the package.
> 3. Select **Upgrade**.

> [tab] Terminal
>
> Open the developer panel, then select the **Terminal** tab. Run the following command:
>
> ```bash theme={"system"}
> uv pip install --upgrade [PACKAGE_NAME]
> ```

## Remove a package

Remove a package using either the sidebar or with the notebook terminal.

> [tab] Sidebar
>
> 1. Select **Manage packages** () from the notebook sidebar.
> 2. Find the package you want to remove.
> 3. Select **Remove** next to the package name.

> [tab] Terminal
>
> Open the developer panel, then select the **Terminal** tab. Run the following command:
>
> ```bash theme={"system"}
> uv pip uninstall [PACKAGE_NAME]
> ```
