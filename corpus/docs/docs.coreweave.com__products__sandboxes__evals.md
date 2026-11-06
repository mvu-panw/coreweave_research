# Run evaluations on CoreWeave sandboxes

Source: https://docs.coreweave.com/products/sandboxes/evals

# Run evaluations on CoreWeave sandboxes

> Choose a benchmark workflow to evaluate code patches, coding agents, and tool-calling models in sandboxes.

Use CoreWeave Sandboxes to execute code and run benchmark tests in isolated environments. An evaluation harness prepares tasks, runs the agent or applies submitted outputs, checks the results, and collects scores. Sandboxes provide the compute and filesystem for those operations.

Choose a workflow based on whether you want to grade patches, evaluate a coding agent, or test a model on simulated business workflows.

## Choose an evaluation workflow

| Guide | Start with | Workflow |
| - | - | - |
| [SWE-bench](https://docs.coreweave.com/products/sandboxes/client/guides/swebench.md) | Model-generated patches or the dataset's gold patches | Apply each patch to its task repository, run tests in a sandbox, and collect the grading report. The example supports concurrent evaluations. |
| [DeepSWE v1.1](https://docs.coreweave.com/products/sandboxes/evals/deepswe.md) | Task prompts and a configured coding agent | Let the agent edit code in a task sandbox, collect its committed patch, and grade it in a fresh verifier sandbox. Start with one task, then expand to two. |
| [AutomationBench](https://docs.coreweave.com/products/sandboxes/evals/automationbench.md) | Business-workflow tasks and a configured model endpoint | Run simulated application tasks with Harbor scheduling and check their outcomes with the benchmark evaluator. Start with one task before increasing concurrency. |

The SWE-bench guide evaluates supplied patches. It doesn't generate them or call a model. The DeepSWE and AutomationBench guides include agent execution and model requests as part of the evaluation.

## Separate model inference from evaluation execution

The model provider generates responses. The agent harness uses those responses to select commands to run. CoreWeave Sandboxes executes the commands, and the benchmark verifier determines whether the result satisfies the task.

Model selection and inference hosting depend on your harness. The DeepSWE and AutomationBench guides use Serverless Inference as the example provider, which isn't required to run evaluations on CoreWeave Sandboxes. The AutomationBench recipe accepts another OpenAI-compatible model endpoint through its `.env` settings. The DeepSWE recipe includes provider-specific configuration, so changing providers there requires adapting its model connection and authentication.

Where the agent loop runs also depends on the integration. The DeepSWE recipe runs it on the machine that launches the evaluation and executes its shell actions in remote sandboxes. AutomationBench runs Harbor locally and its agent loop inside each trial sandbox. See [Agents](https://docs.coreweave.com/products/sandboxes/agents.md) for integrations that run agent processes inside a sandbox or connect a managed agent service.

## Run a sample and inspect the outcome

Follow the selected guide to configure credentials, install its dependencies, and run a small sample before increasing concurrency or task count. Keep the benchmark version, model, agent configuration, and execution limits with the results so you can identify what was evaluated.

Check infrastructure errors separately from benchmark scores. A sandbox startup failure doesn't establish whether an agent can solve the task. Inspect the task outputs and grading report for completed evaluations.

When the run finishes, use the guide's cleanup steps. For custom evaluation harnesses, see [command execution](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md), [file operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md), and [cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md).
