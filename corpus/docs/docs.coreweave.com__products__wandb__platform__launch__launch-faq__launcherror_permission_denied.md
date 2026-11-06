# How do I fix a "permission denied" error in Launch?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/launcherror_permission_denied

# How do I fix a "permission denied" error in Launch?

If you see the error `Launch Error: Permission denied`, you don't have permission to log to the project. Review the following causes and resolutions:

* You aren't logged in on this machine. Run [`wandb login`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-login) in the command line.
* The specified entity doesn't exist. The entity must be your username or the name of an existing team. If necessary, create a team on the [Subscriptions page](https://forge.coreweave.com/subscriptions).
* You lack project permissions. Ask the project creator to change the privacy setting to **Open** so you can log runs to the project.
