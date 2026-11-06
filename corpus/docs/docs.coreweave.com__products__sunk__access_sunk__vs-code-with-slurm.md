# Tunnel VS Code for development on Slurm

Source: https://docs.coreweave.com/products/sunk/access_sunk/vs-code-with-slurm

# Tunnel VS Code for development on Slurm

> Use VS Code tunnels with SUNK to develop on compute nodes

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

With SUNK, you can develop on Slurm compute nodes through the [Tunnel functionality](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server) in Visual Studio Code (VS Code). This guide is for developers who want to use VS Code as their editing environment while running and debugging workloads on a SUNK Slurm cluster.

With this method, you can connect to any Slurm-allocated compute nodes using a VS Code [Remote Tunnel](https://code.visualstudio.com/docs/remote/tunnels), which you can manage through VS Code or the [`code` Command Line Interface (CLI)](https://code.visualstudio.com/docs/configure/command-line) on your workstation. A tunnel lets you edit code on the compute node directly, keep your development environment close to your data and GPUs, and avoid copying files back and forth between your workstation and the cluster.

This guide walks through the steps required to set up a VS Code Tunnel to connect to your Slurm compute nodes. By the end, you have the `code` CLI installed in your cluster's shared storage, an interactive Slurm allocation on a compute node, and an active tunnel you can open in either VS Code in the browser or VS Code Desktop.

## Prerequisites

To follow along with this guide, you need:

* An active CoreWeave account and an existing Slurm cluster.
* A GitHub or Microsoft account to connect to VS Code Tunnel.
* The [Microsoft Remote Tunnels extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server) installed and enabled in VS Code to connect to the compute node from a remote workstation.

## VS Code CLI

The `code` CLI is the component that creates and manages the tunnel on the compute node. Install it once into your cluster's shared storage so it is available from any compute node you allocate.

### Download and install the VS Code CLI

> [!NOTE]
>
> The commands in the following examples demonstrate the process for a GPU node with an Intel processor.

1. Navigate to the [Visual Studio Code Downloads page](https://code.visualstudio.com/Download) and select the appropriate option for your architecture. To download the `code` CLI as a standalone without the VS Code UI, select from the files on the line labeled **CLI**.

   ![Download VS Code](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/vs-code-download-cli.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=4371297488ea643fa8b155ac8fb2d02c)

2. Click the `x64` download link for **CLI** in the Linux section. The file downloads to your local workstation's download directory, but you can ignore or delete this copy.

3. Click the **direct download link** in the banner at the top of the screen and copy the URL. This is the URL you paste into the following `curl` command.

   ![Download confirmation](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/vs-code-download.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=48549b92138eabd9e36ce64034dd7fc5)

4. Navigate to your desired location in your cluster's shared storage, such as the home directory or `/mnt/data`.

   ```bash theme={"system"}
   cd /mnt/data
   ```

5. Download the file with `curl` using the URL obtained from the direct download link in Step 3.

   ```bash theme={"system"}
   curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
   ```

6. Make a `/bin` directory in your `$HOME` folder, if it does not already exist.

   ```bash theme={"system"}
   mkdir -p $HOME/bin
   ```

7. Unpack the file into the `$HOME/bin` directory.

   ```bash theme={"system"}
   tar -x --file=vscode_cli.tar.gz --directory=$HOME/bin
   ```

8. Export `$HOME/bin` to your `$PATH`. This step ensures that the `code` executable is in your system path every time you log in.

   ```bash theme={"system"}
   echo "export PATH=$PATH:$HOME/bin" >> ~/.bashrc
   ```

## Connect to the compute node with a tunnel

With the `code` CLI installed in shared storage, you can now allocate a compute node through Slurm and start a tunnel on it.

> [!WARNING]
>
> Use the login node only to gain access to the cluster, not to run resource-intensive workloads directly. Use `srun` from the login node to allocate a compute node, then run resource-intensive commands there.

1. Log in to your Slurm cluster's login node.

2. Use `srun` to create an interactive session to a compute node of your choice. The following example specifies one node in the `h100` partition and launches `bash`.

   ```bash theme={"system"}
   srun -p h100 -N 1 --pty bash -i
   ```

   * `-p h100` specifies the `h100` partition.
   * `-N 1` specifies one node as the target.
   * `--pty bash -i` launches `bash` with an interactive session on the specified Slurm node.

3. Create the tunnel on the compute node. Authenticate with your choice of GitHub or Microsoft, and provide a name for the machine. The default name is the name of the compute node.

   ```bash theme={"system"}
   code tunnel
   ```

After the tunnel is running, you can connect to it from either VS Code in the browser or VS Code Desktop. The following sections describe both options.

## VS Code in browser

After you run the `code tunnel` command, the CLI returns a URL to the remote machine, similar to the following:

```text theme={"system"}
Open this link in your browser
https://vscode.dev/tunnel/slurm-h100-209-189
```

Click this URL to open VS Code in a client of your choice.

## VS Code Desktop

After [creating the tunnel with the `code tunnel` command](#connect-to-the-compute-node-with-a-tunnel), you can connect to it with VS Code from your local machine for ease of development. The Desktop version of VS Code requires the [Microsoft Remote - Tunnels extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server) for VS Code to use this functionality.

You can interact with the [Remote-Tunnels functionality](https://code.visualstudio.com/docs/remote/tunnels) through either the **Remote Explorer** tab or the **Command Palette**. The following sections describe both approaches. Choose whichever fits your workflow.

### Remote Explorer

You can view and connect to tunnels with the Remote Explorer in VS Code.

1. Click the **Remote Explorer** icon on the VS Code Activity Bar.

   ![A screenshot of the VS Code Activity Bar with the Remote Explorer icon highlighted](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/remote-explorer-tab.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=a9b6f6e28bb4e74afe4792854b0439e2)

2. When prompted, specify whether you used GitHub or Microsoft to authenticate.

   ![A screenshot of the Remote Explorer window in Visual Studio Code](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/remote-explorer.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=e1fe944ff6fadd89ab7b3f8ecd15d292)

3. After you authenticate with the appropriate service, select the node you want to connect to.

### Command Palette

Access the Remote Tunnels functionality with VS Code's Command Palette.

1. Open the Command Palette with `Ctrl-Shift-P` for Windows and Linux, or `Shift-Command-P` on macOS.

2. Click **Remote-Tunnels: Connect to Tunnel** in the Command Palette.

   ![VS Code command palette](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/vs-code-command-palette-connect.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=86a93072a526dee25e2ccf535c8d382c)

3. When prompted, specify whether you used GitHub or Microsoft to authenticate.

   ![VS Code authentication selection](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/vs-code-command-palette-auth.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=f3bdcc883a605291fb6f2063de27cec0)

4. After you authenticate with the appropriate service, select the node you want to connect to.
