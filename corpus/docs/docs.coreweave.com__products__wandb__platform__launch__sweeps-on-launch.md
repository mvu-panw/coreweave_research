# Create sweeps with W&B Launch

Source: https://docs.coreweave.com/products/wandb/platform/launch/sweeps-on-launch

> Discover how to automate hyperparamter sweeps on launch.

# Create sweeps with W&B Launch

> [card] [Try in Colab](https://colab.research.google.com/drive/1WxLKaJlltThgZyhc7dcZhDQ6cjVQDfil#scrollTo=AFEzIxA6foC7)

This page describes how to create a hyperparameter tuning job ([sweeps](https://docs.coreweave.com/products/wandb/sweeps.md)) with W\&B Launch, so you can automate hyperparameter exploration on the same infrastructure that runs your other launch jobs. With sweeps on launch, a sweep scheduler is pushed to a Launch Queue with the specified hyperparameters to sweep over. The sweep scheduler starts as it is picked up by the agent, launching sweep runs onto the same queue with chosen hyperparameters. This continues until the sweep finishes or is stopped.

You can use the default W\&B Sweep scheduling engine or implement your own custom scheduler:

1. Standard sweep scheduler: Use the default W\&B Sweep scheduling engine that controls [W\&B Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md). The familiar `bayes`, `grid`, and `random` methods are available.
2. Custom sweep scheduler: Configure the sweep scheduler to run as a job. This option enables full customization. The following section shows an example of how to extend the standard sweep scheduler to include more logging.

> [!NOTE]
>
> This guide assumes that W\&B Launch has been previously configured. If W\&B Launch isn't configured, see the [how to get started](https://docs.coreweave.com/products/wandb/platform/launch.md#how-to-get-started) section of the launch documentation.

> [!NOTE]
>
> We recommend you create a sweep on launch using the `basic` method if you're a first-time user of sweeps on launch. Use a custom sweeps on launch scheduler when the standard Weights & Biases scheduling engine doesn't meet your needs.

## Create a sweep with a Weights & Biases standard scheduler

This section describes how to create W\&B Sweeps with Launch using the standard scheduling engine. You can create a sweep interactively with the W\&B App or programmatically with the W\&B CLI. For advanced configurations of Launch sweeps, including the ability to customize the scheduler, use the CLI.

> [!NOTE]
>
> Before you create a sweep with W\&B Launch, ensure that you first create a job to sweep over. See the [Create a Job](https://docs.coreweave.com/products/wandb/platform/launch/create-launch-job.md) page for more information.

> [tab] W\&B app
>
> Create a sweep interactively with the W\&B App.
>
> 1. Navigate to your Weights & Biases project on the W\&B App.
> 2. Select the sweeps icon in the project sidebar (broom image).
> 3. Select the **Create Sweep** button.
> 4. Click the **Configure Launch** button.
> 5. From the **Job** dropdown menu, select the name of your job and the job version you want to create a sweep from.
> 6. From the **Queue** dropdown menu, select a queue to run the sweep on.
> 7. From the **Job Priority** dropdown, specify the priority of your launch job. A launch job's priority is set to "Medium" if the launch queue doesn't support prioritization.
> 8. Optional: Configure override args for the run or sweep scheduler. For example, using the scheduler overrides, configure the number of concurrent runs the scheduler manages using `num_workers`.
> 9. Optional: From the **Destination Project** dropdown menu, select a project to save the sweep to.
> 10. Click **Save**.
> 11. Select **Launch Sweep**.
>
> ![Launch sweep configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/create_sweep_with_launch.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=e7be8107cf6a8db81411bba5bf750cca)

> [tab] CLI
>
> Programmatically create a W\&B Sweep with Launch with the W\&B CLI.
>
> 1. Create a Sweep configuration.
>
> 2. Specify the full job name within your sweep configuration.
>
> 3. Initialize a sweep agent.
>
> > [!NOTE]
> >
> > Steps 1 and 3 are the same steps you normally take when you create a W\&B Sweep.
>
> For example, the following code snippet specifies `'wandb/jobs/Hello World 2:latest'` for the job value:
>
> ```yaml theme={"system"}
> # launch-sweep-config.yaml
>
> job: 'wandb/jobs/Hello World 2:latest'
> description: sweep examples using launch jobs
>
> method: bayes
> metric:
>   goal: minimize
>   name: loss_metric
> parameters:
>   learning_rate:
>     max: 0.02
>     min: 0
>     distribution: uniform
>   epochs:
>     max: 20
>     min: 0
>     distribution: int_uniform
>
> # Optional scheduler parameters:
>
> # scheduler:
> #   num_workers: 1  # concurrent sweep runs
> #   docker_image: [BASE-IMAGE-FOR-THE-SCHEDULER]
> #   resource: [RESOURCE-TYPE-FOR-EXAMPLE-LOCAL-CONTAINER]
> #   resource_args:  # resource arguments passed to runs
> #     env: 
> #         - WANDB_API_KEY
>
> # Optional Launch Params
> # launch: 
> #    registry: [REGISTRY-FOR-IMAGE-PULLING]
> ```
>
> For information about how to create a sweep configuration, see the [Define sweep configuration](https://docs.coreweave.com/products/wandb/platform/launch/sweeps-on-launch.md) page.
>
> 4. Initialize a sweep. Provide the path to your config file, the name of your job queue, your Weights & Biases entity, and the name of the project.
>
> ```bash theme={"system"}
> wandb launch-sweep [PATH-TO-YAML-FILE] --queue [QUEUE-NAME] --entity [YOUR-ENTITY] --project [PROJECT-NAME]
> ```
>
> For more information about W\&B Sweeps, see the [Tune Hyperparameters](https://docs.coreweave.com/products/wandb/sweeps.md) chapter.

## Create a custom sweep scheduler

This section describes how to create a custom sweep scheduler when the standard scheduling engine doesn't meet your needs. You can create a custom sweep scheduler either with the Weights & Biases scheduler or a custom scheduler.

> [!NOTE]
>
> Using scheduler jobs requires `wandb` CLI version >= `0.15.4`

> [tab] Weights & Biases scheduler
>
> Create a launch sweep using the W\&B sweep scheduling logic as a job.
>
> 1. Identify the Weights & Biases scheduler job in the public wandb/sweep-jobs project, or use the job name:
>    `'wandb/sweep-jobs/job-wandb-sweep-scheduler:latest'`.
> 2. Construct a configuration yaml with an additional `scheduler` block that includes a `job` key pointing to this name, as shown in the following example.
> 3. Use the `wandb launch-sweep` command with the new config.
>
> Example config:
>
> ```yaml theme={"system"}
> # launch-sweep-config.yaml  
> description: Launch sweep config using a scheduler job
> scheduler:
>   job: wandb/sweep-jobs/job-wandb-sweep-scheduler:latest
>   num_workers: 8  # allows 8 concurrent sweep runs
>
> # training/tuning job that the sweep runs will execute
> job: wandb/sweep-jobs/job-fashion-MNIST-train:latest
> method: grid
> parameters:
>   learning_rate:
>     min: 0.0001
>     max: 0.1
> ```

> [tab] Custom scheduler
>
> Create custom schedulers by creating a scheduler-job. For the purposes of this guide, modify the `WandbScheduler` to provide more logging.
>
> 1. Clone the `wandb/launch-jobs` repo (specifically: `wandb/launch-jobs/jobs/sweep_schedulers`)
> 2. Modify the `wandb_scheduler.py` to achieve your desired increased logging. Example: Add logging to the function `_poll`. This is called once every polling cycle (configurable timing), before new sweep runs launch.
> 3. Run the modified file to create a job, with: `python wandb_scheduler.py --project [PROJECT] --entity [ENTITY] --name CustomWandbScheduler`
> 4. Identify the name of the job created, either in the UI or in the output of the previous call, which is a code-artifact job (unless otherwise specified).
> 5. Create a sweep configuration where the scheduler points to your new job.
>
> ```yaml theme={"system"}
> ...
> scheduler:
>   job: '[ENTITY]/[PROJECT]/job-CustomWandbScheduler:latest'
> ...
> ```

> [tab] Optuna scheduler
>
> Optuna is a hyperparameter optimization framework that uses a variety of algorithms to find the best hyperparameters for a given model (similar to Weights & Biases). In addition to the [sampling algorithms](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html), Optuna also provides a variety of [pruning algorithms](https://optuna.readthedocs.io/en/stable/reference/pruners.html) that you can use to terminate poorly performing runs early. This is useful when you run many runs, as it can save time and resources. The classes are configurable. Pass in the expected parameters in the `scheduler.settings.pruner/sampler.args` block of the config file.
>
> Create a launch sweep using Optuna's scheduling logic with a job.
>
> 1. First, create your own job or use a pre-built Optuna scheduler image job.
>    * See the [`wandb/launch-jobs`](https://github.com/wandb/launch-jobs/blob/main/jobs/sweep_schedulers) repo for examples on how to create your own job.
>    * To use a pre-built Optuna image, you can either navigate to `job-optuna-sweep-scheduler` in the `wandb/sweep-jobs` project or use the job name: `wandb/sweep-jobs/job-optuna-sweep-scheduler:latest`.
>
> 2. After you create a job, you can create a sweep. Construct a sweep config that includes a `scheduler` block with a `job` key pointing to the Optuna scheduler job, as shown in the following example.
>
>    ```yaml theme={"system"}
>      # optuna_config_basic.yaml
>      description: A basic Optuna scheduler
>      job: wandb/sweep-jobs/job-fashion-MNIST-train:latest
>      run_cap: 5
>      metric:
>        name: epoch/val_loss
>        goal: minimize
>
>      scheduler:
>        job: wandb/sweep-jobs/job-optuna-sweep-scheduler:latest
>        resource: local-container  # required for scheduler jobs sourced from images
>        num_workers: 2
>
>        # optuna specific settings
>        settings:
>          pruner:
>            type: PercentilePruner
>            args:
>              percentile: 25.0  # kill 75% of runs
>              n_warmup_steps: 10  # pruning turned off for first x steps
>
>      parameters:
>        learning_rate:
>          min: 0.0001
>          max: 0.1
>    ```
>
> 3. Finally, launch the sweep to an active queue with the `launch-sweep` command:
>
>    ```bash theme={"system"}
>    wandb launch-sweep [CONFIG-YAML] -q [QUEUE] -p [PROJECT] -e [ENTITY]
>    ```
>
> For the exact implementation of the Optuna sweep scheduler job, see [wandb/launch-jobs](https://github.com/wandb/launch-jobs/blob/main/jobs/sweep_schedulers/optuna_scheduler/optuna_scheduler.py). For more examples of what's possible with the Optuna scheduler, check out [wandb/examples](https://github.com/wandb/examples/tree/master/examples/launch/launch-sweeps/optuna-scheduler).

Examples of custom sweep scheduler jobs are available in the [wandb/launch-jobs](https://github.com/wandb/launch-jobs) repo under `jobs/sweep_schedulers`. This guide shows how to use the publicly available **Weights & Biases Scheduler Job**, and demonstrates a process for creating custom sweep scheduler jobs.

## Resume sweeps on launch

This section describes how to resume a launch-sweep from a previously launched sweep, which is useful when you want to continue exploring with updated scheduler settings or on a different queue. Although you can't change hyperparameters and the training job, you can change scheduler-specific parameters and the queue it is pushed to.

> [!NOTE]
>
> If the initial sweep used a training job with an alias like `latest`, resuming can lead to different results if the latest job version has changed since the last run.

1. Identify the sweep name/ID for a previously run launch sweep. The sweep ID is an eight-character string (for example, `hhd16935`) that you can find in your project on the W\&B App.
2. If you change the scheduler parameters, construct an updated config file.
3. In your terminal, execute the following command. Replace content wrapped in `[` and `]` with your information:

   ```bash theme={"system"}
   wandb launch-sweep [OPTIONAL-CONFIG-YAML] --resume_id [SWEEP-ID] --queue [QUEUE-NAME]
   ```
