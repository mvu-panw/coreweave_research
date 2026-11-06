# Use your own compute

Source: https://docs.coreweave.com/products/sandboxes/get-started-cks

# Use your own compute

> Enable sandboxes on your CoreWeave Kubernetes Service cluster and run your first command.

Run a sandbox on compute in your CoreWeave Kubernetes Service (CKS) cluster.

## Before you begin

You need a running cluster with at least one schedulable, Ready Node and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for the Python example.

## Run your first sandbox

**1. Grant access**

Ask your administrator to create or update an [Access Policy](https://console.coreweave.com/organization/iam/access-policies) granting you **Sandbox Admin** to enable a runner. Users who only run sandboxes need **Sandbox User**. See [Create an access policy](https://docs.coreweave.com/security/iam/access-policies/manage.md#create-an-access-policy).

> [!WARNING]
>
> The [Sandbox Admin](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox) role controls runner settings across the organization. On runners using legacy `v1beta2` profiles, this role can enable [privileged profile settings](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-allow-a-privileged-profile-posture). These settings include privileged containers, host namespaces, and mounts of the Node's filesystem. These settings can give sandboxes Node access comparable to that of a cluster administrator and put co-located workloads at risk. The v1 policy's `allow_privileged` setting governs in-guest privilege within the sandbox's isolation boundary.

**2. Enable a runner**

A runner schedules sandbox Pods on your cluster's compute. Each cluster can host one managed runner. If your administrator has already enabled a runner, use its ID.

1. Open the [Clusters](https://console.coreweave.com/clusters) page and select your cluster.
2. In the **Sandbox runner** card, click **Enable sandbox runner**.
3. Wait for **Status** to show **Ready** and **Connection** to show **Connected**, then select and copy the **Runner ID**.

CoreWeave configures a [default runner policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#set-a-default-policy-for-new-runners) in its service deployment. The gateway saves it when a runner without a policy connects, or when v1 placement first selects that runner. An existing runner keeps its saved policy.

**3. Get a credential**

On the [Tokens](https://console.coreweave.com/tokens) page, click **Create Token**, complete the token details, and click **Create**. Copy the **Token Secret**, which is shown only once, and set it in your terminal:

```bash theme={"system"}
export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
```

For token permissions and setup, see [CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#coreweave-api-access-token).

Before running a sandbox, ask your administrator to [review the runner's saved policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#read-the-current-policy), including its network rules. If no policy is configured, an administrator must [configure one](#optional-customize-the-sandbox-policy) before you continue. If you have **Sandbox Admin**, you can do this yourself.

**4. Run a sandbox**

Save the following as `hello.py`, replacing `[RUNNER-ID]` with your runner's ID. Set both `placement_mode="cks"` and `runner_ids` to target that runner:

```python title="hello.py" theme={"system"}
from cwsandbox import AuthStrategy, Sandbox

with Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    placement_mode="cks",
    runner_ids=["[RUNNER-ID]"],
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    print(sandbox.exec(["echo", "Hello!"]).result().stdout)
```

Run it with Python 3.11 and the sandbox client. The command installs them if needed:

```bash theme={"system"}
uv run --python 3.11 --with 'cwsandbox>=1.10.0' hello.py
```

The example prints the following output and stops the sandbox when it finishes:

```text title="Output" theme={"system"}
Hello!
```

Serverless is the default placement mode. Keep `placement_mode="cks"` on requests that must run on your cluster. For the TypeScript equivalent, see [Select a placement mode](https://docs.coreweave.com/products/sandboxes/placement.md#select-a-placement-mode).

## Optional: Manage runners with the CLI

The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic#installation) provides an alternative to the cloud console. Install it, then sign in with your API access token:

```bash theme={"system"}
cwic auth login "[API-ACCESS-TOKEN]"
```

The CLI saves the token locally. The Python client reads `CWSANDBOX_API_KEY` instead.

To enable a runner on another cluster, choose a runner ID and start the creation wizard:

```bash theme={"system"}
cwic sandbox runner create [RUNNER-ID]
```

Select your cluster and release channel, then review the runner configuration and policy in the editor before submitting.

Check the runner's status:

```bash theme={"system"}
cwic sandbox runner get [RUNNER-ID]
```

Wait for `INSTALL` to show `READY` and `CONN` to show `CONNECTED`. For REST API examples and deployment troubleshooting, see [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).

## Optional: Customize the sandbox policy

The runner's policy applies to sandboxes scheduled by that runner. The example policy replaces the runner's policy and differs from the service default. For an existing shared runner, coordinate changes with its administrator. To modify an existing policy while preserving its other settings and detecting concurrent changes, follow [Update a policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy).

Save this example as `policy.json`. It supplies CPU and memory defaults, limits resource requests, and leaves the default egress list empty. The lifetime default is 15 minutes. It isn't a maximum.

```json title="policy.json" theme={"system"}
{
  "displayName": "default",
  "constraints": {
    "resources": {
      "defaultCpu": "1",
      "defaultMemory": "2Gi",
      "maxCpu": "4",
      "maxMemory": "8Gi",
      "requireLimits": true
    },
    "network": {
      "defaultEgress": []
    },
    "security": {
      "allowPrivileged": false,
      "allowedRuntimeClasses": ["cw-kata-qemu"],
      "defaultCpuRuntimeClass": "cw-kata-qemu"
    },
    "lifecycle": { "defaultLifetimeSeconds": 900 }
  }
}
```

Apply it to the runner you enabled, then inspect the saved policy:

```bash theme={"system"}
cwic sandbox runner policy edit [RUNNER-ID] -f policy.json
cwic sandbox runner policy describe [RUNNER-ID]
```

To restrict which outbound destinations users can request, configure `allowedEgress`. The `defaultEgress` field alone sets defaults. See [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md).

## Optional: Disable the runner

Keep the runner enabled to create more sandboxes. When you no longer need it, stop its running sandboxes, then disable it using either interface:

> [tab] Cloud console
>
> 1. Open your cluster's **Sandbox runner** card.
> 2. Click **Disable sandbox runner** and confirm.

> [tab] CLI
>
> ```bash theme={"system"}
> cwic sandbox runner delete [RUNNER-ID]
> ```
>
> Confirm the deletion when prompted.

Disabling the runner removes it from the cluster. To use sandboxes there again, enable a runner.

## Next steps

Explore the following guides:

* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): customize resources, network access, and security settings.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): inspect, update, and troubleshoot runners.
* [Sandbox placement and spillover](https://docs.coreweave.com/products/sandboxes/placement.md): fall back between CKS and serverless capacity.
* [Python client](https://docs.coreweave.com/products/sandboxes/client.md): execute commands, work with files, and manage sandbox lifecycles.
