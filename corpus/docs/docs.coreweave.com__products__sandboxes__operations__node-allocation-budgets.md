# Configure Node allocation budgets

Source: https://docs.coreweave.com/products/sandboxes/operations/node-allocation-budgets

# Configure Node allocation budgets

> Limit sandbox CPU and memory requests across all Nodes, selected Node Pools, or groups of Nodes

Node allocation budgets control how much of each Node's allocatable CPU and memory sandboxes can request.

This guide shows cluster administrators how to configure and enable budgets for all Nodes, selected Node Pools, or groups of Nodes.

For example, a Node has 32 allocatable CPUs and 128 GiB of allocatable memory. A 50% budget allows aggregate sandbox requests of 16 CPUs and 64 GiB.

Percentages apply to resource requests, rather than measured utilization. Existing sandboxes aren't evicted when a budget decreases.

Budgets bound the aggregate. To bound what an individual sandbox requests, see [Size sandbox CPU and memory](https://docs.coreweave.com/products/sandboxes/resource-sizing.md).

## Before you begin

Before you configure budgets, complete the following prerequisites:

* Confirm with CoreWeave that Node allocation budget support and its required permissions are enabled for your cluster.
* [Apply any required managed runner update](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#trigger-an-on-demand-runner-update) and wait for the runner to become ready and connected.
* Use [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) v1.44.0 or later, authenticated to the correct organization with Sandbox administrator permissions.
* Install `jq`.
* Have Kubernetes access to inspect Node labels and published budgets. Before you decrease a budget, you also need permission to cordon and uncordon the affected Nodes.
* Use the default Kubernetes scheduler, or confirm that your scheduler enforces the budget extended resources.
* If sandboxes select a RuntimeClass, confirm with your cluster administrator that it declares a nonempty `overhead.podFixed` map. A runtime with no overhead must declare explicit zero values. Sandboxes without a RuntimeClass don't require this setting.

CoreWeave Intelligent CLI v1.44.0 supports the environment-only workflow in this guide. A runner update doesn't enable budgets until you apply the configuration.

All logical runners sharing the same physical Kubernetes cluster must use the same budget configuration and mode. Separate clusters can use different configurations.

## Identify the runner and Node labels

Identify the runner to update and the Node labels to use in your budget selectors.

List available runners:

```bash theme={"system"}
cwic sandbox runner get
```

Optional: Filter by cluster. Replace `[CLUSTER-ID]` with your CoreWeave Kubernetes Service (CKS) cluster ID:

```bash theme={"system"}
cwic sandbox runner get --cluster "[CLUSTER-ID]"
```

Choose the runner and Kubernetes context. Replace `[RUNNER-ID]` with the runner ID and `[KUBE-CONTEXT]` with its Kubernetes context:

```bash theme={"system"}
export RUNNER_ID="[RUNNER-ID]"
export KUBE_CONTEXT="[KUBE-CONTEXT]"
```

Inspect Node Pool and hostname labels:

```bash theme={"system"}
kubectl --context "$KUBE_CONTEXT" get nodes \
  -L compute.coreweave.com/node-pool,kubernetes.io/hostname
```

CKS Nodes can expose these labels:

| Label | Purpose |
| - | - |
| `compute.coreweave.com/node-pool` | Select Nodes by Node Pool name |
| `compute.coreweave.com/node-pool-uid` | Select a particular Node Pool identity |
| `kubernetes.io/hostname` | Select individual Nodes |
| A custom label | Select an arbitrary group of Nodes |

Use the label keys and values present in your cluster.

A budget selector selects Kubernetes Nodes. It doesn't select API runner groups or override sandbox placement constraints, taints, tolerations, or RuntimeClasses.

## Create a budget configuration

Save one of the following examples as the `node-budget.json` file.

Start with `"mode": "prepare"`. Preparation publishes budget resources. Enforcement is enabled in a later step.

### 95% CPU and memory on every Node

An empty selector matches all Nodes.

```json theme={"system"}
{
  "version": 1,
  "mode": "prepare",
  "managedNodes": {
    "selector": {},
    "defaultBudget": {
      "cpuPercent": 95,
      "memoryPercent": 95
    }
  }
}
```

Both percentages are required and must be integers from `0` through `100`. A value of `0` means zero sandbox capacity.

### 50% on selected Node Pools only

This selects Nodes in either of two Node Pools. Replace `[BATCH-POOL]` and `[INTERACTIVE-POOL]` with their Node Pool label values:

```json theme={"system"}
{
  "version": 1,
  "mode": "prepare",
  "managedNodes": {
    "selector": {
      "matchExpressions": [
        {
          "key": "compute.coreweave.com/node-pool",
          "operator": "In",
          "values": [
            "[BATCH-POOL]",
            "[INTERACTIVE-POOL]"
          ]
        }
      ]
    },
    "defaultBudget": {
      "cpuPercent": 50,
      "memoryPercent": 50
    }
  }
}
```

Nodes outside `managedNodes.selector` receive zero sandbox budget. Once enforcement is enabled, sandboxes that require budget tokens can't use those Nodes.

Preview the selection:

```bash theme={"system"}
kubectl --context "$KUBE_CONTEXT" get nodes \
  -l 'compute.coreweave.com/node-pool in ([BATCH-POOL],[INTERACTIVE-POOL])'
```

To preserve sandbox capacity on other Nodes, use [Node Pool and group overrides](#different-budgets-for-node-pools-and-custom-groups).

### Different budgets for Node Pools and custom groups

This configuration provides the following budgets:

* 95% CPU and memory by default.
* 50% CPU and memory for Nodes in the `[CPU-POOL]` Node Pool.
* 25% CPU and 40% memory for Nodes labeled `[BUDGET-GROUP-LABEL]=[TRAINING-GROUP]`.

Replace `[CPU-POOL]` with the Node Pool label value. Replace `[BUDGET-GROUP-LABEL]` with a custom label key and `[TRAINING-GROUP]` with its value.

```json theme={"system"}
{
  "version": 1,
  "mode": "prepare",
  "managedNodes": {
    "selector": {},
    "defaultBudget": {
      "cpuPercent": 95,
      "memoryPercent": 95
    },
    "overrides": [
      {
        "name": "shared-cpu",
        "selector": {
          "matchLabels": {
            "compute.coreweave.com/node-pool": "[CPU-POOL]"
          }
        },
        "budget": {
          "cpuPercent": 50,
          "memoryPercent": 50
        }
      },
      {
        "name": "training",
        "selector": {
          "matchLabels": {
            "[BUDGET-GROUP-LABEL]": "[TRAINING-GROUP]"
          }
        },
        "budget": {
          "cpuPercent": 25,
          "memoryPercent": 40
        }
      }
    ]
  }
}
```

Selectors have the following behavior:

* A matching override replaces the default percentages.
* If multiple overrides match, the minimum percentage in each dimension wins.
* Rule order doesn't establish priority.
* Overlap is reported as `selector_conflict`. Prefer disjoint groups when overlap is unintended.
* Entries in `matchLabels` and separate expressions must all match.
* Values within one `In` expression are alternatives.

In this example, a Node matching both overrides receives 25% CPU and 40% memory.

For custom groups, configure labels through your Node Pool configuration where possible so replacement Nodes inherit them.

### 50% on specific Nodes

Replace `[HOSTNAME-A]` and `[HOSTNAME-B]` with the observed `kubernetes.io/hostname` label values for the Nodes you want to select:

```json theme={"system"}
{
  "version": 1,
  "mode": "prepare",
  "managedNodes": {
    "selector": {
      "matchExpressions": [
        {
          "key": "kubernetes.io/hostname",
          "operator": "In",
          "values": [
            "[HOSTNAME-A]",
            "[HOSTNAME-B]"
          ]
        }
      ]
    },
    "defaultBudget": {
      "cpuPercent": 50,
      "memoryPercent": 50
    }
  }
}
```

Hostname label values may differ from Node object names.

Other Nodes receive zero sandbox budget. Node Pool or custom-group selectors are preferable when replacement Nodes should inherit the configuration automatically.

## Apply the configuration

Store the configuration as a JavaScript Object Notation (JSON) `string` in the following field:

```text theme={"system"}
spec.overrides.env.SANDBOX_NODE_BUDGET_CONFIG
```

Select the configuration file to apply:

```bash theme={"system"}
export BUDGET_FILE=node-budget.json
```

The following commands read the current runner and preserve its existing deployment override fields and environment variables. You don't need the original runner configuration or policy file. Reuse this block after changing `BUDGET_FILE` to apply a different configuration:

```bash theme={"system"}
umask 077

# cwic returns an array, even when fetching one runner.
cwic sandbox runner get "$RUNNER_ID" -o json > current-runner.json

jq --slurpfile budget "$BUDGET_FILE" '
  if length != 1 then
    error("expected one runner")
  else
    .[0]
  end |
  {
    spec: {
      overrides: (
        (.spec.overrides // {}) |
        .env = (
          (.env // {}) + {
            SANDBOX_NODE_BUDGET_CONFIG: ($budget[0] | tojson)
          }
        )
      )
    }
  }
' current-runner.json > node-budget-patch.json

cwic sandbox runner edit "$RUNNER_ID" -f node-budget-patch.json
cwic sandbox runner describe "$RUNNER_ID"
```

Repeat this process for every logical runner in the same physical cluster. Read each runner before you construct its patch.

`spec.overrides` is replaced as an object, so preserving its sibling fields is necessary.

For CoreWeave Intelligent CLI v1.44.0, use this environment-only patch. That release's older policy schema can't fully export the renamed HTTPS hostname fields from newer servers. If you reapply a full runner document, you could therefore replace its policy with incomplete data. The preceding patch doesn't include or update the policy.

Keep runner exports private and remove temporary files afterward:

```bash theme={"system"}
rm current-runner.json node-budget-patch.json
```

## Verify preparation

Preparation publishes these extended resources on Node status:

```text theme={"system"}
sandbox.coreweave.com/cpu-millicores
sandbox.coreweave.com/memory-bytes
```

Inspect their capacity and allocatable values:

```bash theme={"system"}
kubectl --context "$KUBE_CONTEXT" get nodes -o json | jq '
  .items[] | {
    node: .metadata.name,
    cordoned: (.spec.unschedulable // false),
    physical: {
      cpu: .status.allocatable.cpu,
      memory: .status.allocatable.memory
    },
    budgetCapacity: {
      cpuMillicores:
        .status.capacity["sandbox.coreweave.com/cpu-millicores"],
      memoryBytes:
        .status.capacity["sandbox.coreweave.com/memory-bytes"]
    },
    budgetAllocatable: {
      cpuMillicores:
        .status.allocatable["sandbox.coreweave.com/cpu-millicores"],
      memoryBytes:
        .status.allocatable["sandbox.coreweave.com/memory-bytes"]
    }
  }'
```

Wait for capacity and allocatable to agree for both budget resources on every Node.

Budget accounting includes the following details:

* Existing bound sandboxes without budget tokens are subtracted from the published budget until they finish.
* Other workloads consume physical resources, so available sandbox capacity can be lower than the configured budget.
* Sandbox charges include helper containers, init-container peaks, and RuntimeClass overhead.
* CPU and memory percentages don't divide GPU capacity.

Where metrics are available, check the following metrics:

```text theme={"system"}
sandbox_runner_node_budget_ready
sandbox_runner_node_budget_writer
sandbox_runner_node_budget_nodes{state="converged"}
sandbox_runner_node_budget_policy
```

The `sandbox_runner_node_budget_policy` metric exposes `mode` and `policy_hash` labels. Check that every runner in the cluster reports `mode="prepare"` and the same `policy_hash` value. If you don't have access to these metrics, ask CoreWeave to verify readiness before enabling enforcement.

## Enable enforcement

After preparation is healthy, change only the mode:

```bash theme={"system"}
jq '.mode = "enforce"' node-budget.json > node-budget-enforce.json
export BUDGET_FILE=node-budget-enforce.json
```

Repeat the read/build-patch/apply commands from [Apply the configuration](#apply-the-configuration) for every runner in the cluster.

Use `cwic sandbox runner describe "$RUNNER_ID"` to check the runner rollout, and ask CoreWeave to confirm the cluster admission transition is complete. This transition coordinates when the cluster starts enforcing budgets. It includes retiring old shards and allowing pending workloads from before enforcement to bind or terminate.

To verify enforcement, complete the following steps:

1. Create a small sandbox on each runner.
2. Confirm its Pod requests both budget resources.
3. If you perform a controlled saturation test, verify that new allocations stop when either the CPU or memory budget is exhausted.
4. Delete the test sandboxes.

The following capacity-exhaustion reason is expected:

```text theme={"system"}
CWSANDBOX_RUNNER_CAPACITY_EXHAUSTED
```

## Configure Terraform-managed runners

If Terraform manages the runner, merge the following `spec.overrides.env` setting into its existing `coreweave_sandbox_managed_runner` resource:

```hcl theme={"system"}
spec = {
  overrides = {
    env = {
      # Preserve other configured environment variables.
      SANDBOX_NODE_BUDGET_CONFIG = file("${path.module}/node-budget.json")
    }

    # Preserve other configured override fields.
  }

  # Preserve other configured spec fields.
}
```

After preparation is healthy, update the JSON file from `prepare` to `enforce` and apply the corresponding Terraform change.

If Terraform manages the runner, keep changes in Terraform so subsequent applies retain the intended configuration.

## Reduce budgets or change Node membership

Nodes aren't automatically cordoned or drained.

Before you reduce percentages or change selectors or labels in a way that reduces capacity, complete the following steps:

1. Cordon the affected Nodes.
2. Apply the updated configuration to every runner in that cluster.
3. Wait for budget convergence.
4. Uncordon only the Nodes you cordoned for this change.

Cordon prevents new scheduling and leaves existing Pods running. Existing allocations can remain above the new ceiling until they finish. A budget reduction doesn't evict them.

An uncordoned reduction is logged as the following message:

```text theme={"system"}
decrease_without_cordon
```

To disable budgets entirely, coordinate the retirement procedure with CoreWeave. Removing the environment variable or disabling the feature gate directly doesn't perform the required rollback sequence.

## See also

For more information, see the following pages:

* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md).
