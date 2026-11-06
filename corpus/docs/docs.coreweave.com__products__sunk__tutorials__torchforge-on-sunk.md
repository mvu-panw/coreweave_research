# Run torchforge on SUNK

Source: https://docs.coreweave.com/products/sunk/tutorials/torchforge-on-sunk

# Run torchforge on SUNK

> Run Grouped Relative Policy Optimization (GRPO) training with torchforge on SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This tutorial shows you how to run Grouped Relative Policy Optimization (GRPO)
training with [torchforge](https://github.com/meta-pytorch/torchforge) using the
[Qwen3 1.7B model](https://huggingface.co/Qwen/Qwen3-1.7B) on a SUNK cluster.
GRPO is a reinforcement learning technique for fine-tuning language models, and
torchforge provides a PyTorch-based framework to run this training at scale.
By the end of this tutorial, you have a working torchforge environment, a
submitted Slurm batch job that runs GRPO training, and training metrics streamed
to Weights & Biases. This guide is intended for ML practitioners with access to
a SUNK cluster who want to experiment with reinforcement learning workflows.

> [!NOTE]
>
> **Experimental status and tested version**
>
> * torchforge is experimental. Expect potential bugs, incomplete features, and API changes.
> * This documentation and these instructions were tested with torchforge commit `8bd8d5d3c793ca6e2930b471b8ada67ce2458784`.

## Prerequisites

* Access to a SUNK cluster with GPU nodes.
* Minimum one H100 node for GRPO training.
* 10 GB available disk space.
* A [GitHub](https://github.com/) access token.
* A [Weights & Biases](https://wandb.ai/site) API key.
* [Conda](https://docs.conda.io/en/latest/).

## Initialize GitHub and Weights & Biases credentials

The torchforge installation pulls dependencies from GitHub, and the training job
reports metrics to Weights & Biases. Export your credentials so both services
are available during installation and training.

At a Slurm login node, run the following commands:

1. Export your GitHub token. Replace `[GITHUB-TOKEN]` with your GitHub access token:

   ```bash theme={"system"}
   export GH_TOKEN=[GITHUB-TOKEN]
   echo "export GH_TOKEN=$GH_TOKEN" >> ~/.bashrc
   ```

2. Export your Weights & Biases API key:

   Get your Weights & Biases API key from [wandb.ai](https://wandb.ai/site) (**User settings** > **API keys**). Replace `[WANDB-API-KEY]` with your API key:

   ```bash theme={"system"}
   export WANDB_API_KEY=[WANDB-API-KEY]
   echo "export WANDB_API_KEY=$WANDB_API_KEY" >> ~/.bashrc
   ```

## Install torchforge

Next, set up an isolated conda environment, clone the torchforge repository at
the tested commit, and run the project's installation script. Using a dedicated
conda environment keeps torchforge's dependencies separate from the rest of
the system.

To install torchforge, run the following commands:

1. Initialize conda:

   ```bash theme={"system"}
   /opt/conda/bin/conda init bash
   source ~/.bashrc
   ```

2. Create a conda environment:

   ```bash theme={"system"}
   conda create -n torchforge --yes python=3.10 pip
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   Downloading and Extracting Packages:
   Preparing transaction: done
   Verifying transaction: done
   Executing transaction: done

   To activate this environment, use

       $ conda activate torchforge

   To deactivate an active environment, use

       $ conda deactivate
   ```

3. Activate torchforge:

   ```bash theme={"system"}
   conda activate torchforge
   ```

4. Clone the repository:

   ```bash theme={"system"}
   git clone https://github.com/meta-pytorch/torchforge.git
   cd torchforge
   git checkout 8bd8d5d3c793ca6e2930b471b8ada67ce2458784
   ```

5. Run the installation script:

   The installation script takes 5 to 15 minutes to complete.

   ```bash theme={"system"}
   ./scripts/install.sh
   ```

   You should see output similar to the following.
   You don't need to re-activate the conda environment:

   ```text theme={"system"}
   [INFO] Installation completed successfully!

   [INFO] Re-activate the conda environment to make the changes take effect:
   [INFO]   conda deactivate && conda activate torchforge
   ```

6. Verify the installation:

   ```bash theme={"system"}
   python -c "import forge; print('torchforge imported successfully')"
   ```

   You should see output similar to the following:

   ```text theme={"system"}
   torchforge imported successfully
   ```

## Run GRPO training

With torchforge installed, you can launch a short GRPO training run as a
Slurm batch job. The following steps reduce the training step count for a quick
test, define a batch script that requests an H100 node, submit the job, and
tail the logs so you can watch training progress.

To run GRPO training, complete the following steps:

1. Edit the training configuration to reduce steps for testing:

   The default configuration runs for 1,000,000 steps. Lower this to 10
   steps to verify the end-to-end setup quickly without waiting for a
   full training run.

   ```bash theme={"system"}
   sed -i 's/steps: 1000000/steps: 10/' apps/grpo/qwen3_1_7b.yaml
   ```

2. Create a Slurm batch script `torchforge-training.sbatch`:

   ```bash theme={"system"}
   cat << 'EOF' > torchforge-training.sbatch
   #!/usr/bin/env bash
   #SBATCH --job-name=torchforge-grpo-training
   #SBATCH --output=output_torchforge.log
   #SBATCH --error=error_torchforge.log
   #SBATCH --ntasks=1
   #SBATCH --cpus-per-task=96
   #SBATCH --gpus=8
   #SBATCH --time=01:00:00
   #SBATCH --mem=0

   eval "$(/opt/conda/bin/conda shell.bash hook)"
   conda activate torchforge
   cd ~/torchforge
   python -m apps.grpo.main --config apps/grpo/qwen3_1_7b.yaml
   EOF
   ```

3. Submit the job:

   ```bash theme={"system"}
   sbatch torchforge-training.sbatch
   ```

4. Monitor logs:

   ```bash theme={"system"}
   tail -f output_torchforge.log
   ```

   Eventually, you see logs like the following:

   ```text theme={"system"}
   Warning: setting HYPERACTOR_CODEC_MAX_FRAME_LENGTH since this needs to be set to enable large RPC calls via Monarch
   INFO 10-21 03:23:23 [__init__.py:235] Automatically detected platform cuda.
   Launcher not provided, remote allocations will not work.
   Spawning actor DatasetActor
   Spawning service Generator
   Spawning actor RLTrainer
   Spawning actor ReplayBuffer
   Spawning actor ComputeAdvantages
   Spawning service ReferenceModel
   Spawning service RewardActor

   ... skipped for brevity ...

   WandbBackend: Logged 75 metrics at global_step 4
   === [global_reduce] - METRICS STEP 4 ===
     buffer/add/count_episodes_added: 16.0
     buffer/evict/avg_policy_age: 1.0
     buffer/evict/max_policy_age: 1.0
     buffer/evict/sum_episodes_evicted: 16.0
     buffer/sample/avg_data_utilization: 1.0
     buffer/sample/count_sample_requests: 1.0
     buffer_perf/sample/total_duration_avg_s: 0.001130327582359314
     buffer_perf/sample/total_duration_max_s: 0.001130327582359314
     dataset/sample/avg_sample_len: 411.0
     dataset/sample/count_samples_generated: 2.0
     generator/generate/avg_tokens_generated: 491.375
     generator/generate/count_requests: 2.0
     generator/generate/count_sequences_completed: 16.0
     generator/generate/sum_tokens_generated: 7862.0
     generator/update_weights/count_weight_updates: 1.0
     generator_perf/_fetch_weights/total_duration_avg_s: 1.6851447527296841
     generator_perf/_fetch_weights/total_duration_max_s: 1.6851447527296841
     generator_perf/generate/generate/duration_avg_s: 3.1858496093750004
     generator_perf/generate/generate/duration_max_s: 4.32051513671875
     generator_perf/generate/process_inputs/duration_avg_s: 0.0009907840192317963
     generator_perf/generate/process_inputs/duration_max_s: 0.0012066240310668946
     generator_perf/generate/total_duration_avg_s: 3.18701276139915
     generator_perf/generate/total_duration_max_s: 4.32185558475554
     generator_perf/update_weights/avg_pending_requests: 0.0
     generator_perf/update_weights/max_pending_requests: -inf
     generator_perf/waiting_for_fetch_weights/total_duration_avg_s: 1.685305270832032
     generator_perf/waiting_for_fetch_weights/total_duration_max_s: 1.685305270832032
     generator_worker_perf/update_weights_from_shared_memory/total_duration_avg_s: 0.6395906782709062
     generator_worker_perf/update_weights_from_shared_memory/total_duration_max_s: 0.6395906782709062
     reference_perf/forward/avg_sequence_length: 1024.0
     reference_perf/forward/compute_logprobs/duration_avg_s: 0.0001311039086431265
     reference_perf/forward/compute_logprobs/duration_max_s: 0.0001311260275542736
     reference_perf/forward/count_forward_passes: 2.0
     reference_perf/forward/forward/duration_avg_s: 0.012596684508025646
     reference_perf/forward/forward/duration_max_s: 0.012622143141925335
     reference_perf/forward/garbage_collection/duration_avg_s: 0.00033104955218732357
     reference_perf/forward/garbage_collection/duration_max_s: 0.00034371716901659966
     reference_perf/forward/memory_delta_end_start_avg_gb: 2.31842041015625
     reference_perf/forward/memory_peak_max_gb: 11.931992053985596
     reference_perf/forward/to_device/duration_avg_s: 7.077353075146675e-05
     reference_perf/forward/to_device/duration_max_s: 7.580406963825226e-05
     reference_perf/forward/total_duration_avg_s: 0.01313200336880982
     reference_perf/forward/total_duration_max_s: 0.013139839749783278
     reward/evaluate_response/avg_MathReward_reward: 0.38125
     reward/evaluate_response/avg_ThinkingReward_reward: 0.5
     reward/evaluate_response/avg_total_reward: 0.440625
     reward/evaluate_response/count_MathReward_calls: 16.0
     reward/evaluate_response/count_ThinkingReward_calls: 16.0
     reward/evaluate_response/std_MathReward_reward: 0.417161164899131
     reward/evaluate_response/std_ThinkingReward_reward: 0.3872983346207417
     reward/evaluate_response/sum_MathReward_reward: 6.1
     reward/evaluate_response/sum_ThinkingReward_reward: 8.0
     rl_trainer/avg_grpo_loss: 0.042646802961826324
     rl_trainer/count_training_steps: 1.0
     rl_trainer/learning_rate: 0.001
     rl_trainer_perf/push_weights/flatten_state_dict/duration_avg_s: 0.0004946370609104633
     rl_trainer_perf/push_weights/flatten_state_dict/duration_max_s: 0.0004946370609104633
     rl_trainer_perf/push_weights/memory_delta_end_start_avg_gb: 0.0
     rl_trainer_perf/push_weights/memory_peak_max_gb: 11.417872905731201
     rl_trainer_perf/push_weights/to_hf/duration_avg_s: 0.0004782499745488167
     rl_trainer_perf/push_weights/to_hf/duration_max_s: 0.0004782499745488167
     rl_trainer_perf/push_weights/total_duration_avg_s: 3.146173640154302
     rl_trainer_perf/push_weights/total_duration_max_s: 3.146173640154302
     rl_trainer_perf/push_weights/ts_save/duration_avg_s: 3.1451978851109743
     rl_trainer_perf/push_weights/ts_save/duration_max_s: 3.1451978851109743
     rl_trainer_perf/step/forward_backward/duration_avg_s: 0.34571166802197695
     rl_trainer_perf/step/forward_backward/duration_max_s: 0.34571166802197695
     rl_trainer_perf/step/memory_delta_end_start_avg_gb: 0.00022172927856445312
     rl_trainer_perf/step/memory_peak_max_gb: 31.65072727203369
     rl_trainer_perf/step/optimizer_step/duration_avg_s: 0.009929596912115812
     rl_trainer_perf/step/optimizer_step/duration_max_s: 0.009929596912115812
     rl_trainer_perf/step/save_checkpoint/duration_avg_s: 0.10817016521468759
     rl_trainer_perf/step/save_checkpoint/duration_max_s: 0.10817016521468759
     rl_trainer_perf/step/total_duration_avg_s: 0.46381334587931633
     rl_trainer_perf/step/total_duration_max_s: 0.46381334587931633
   ==============================

   ... skipped for brevity ...

   [0] [0] [ReferenceModel-0/1] 2025-10-21 03:32:06 INFO [GC] Performing periodic GC collection took 0.00 seconds
   Reached training limit (10 steps). Exiting continuous_training loop.
   Shutting down...
   Shutting down metric logger...
   WandbBackend global_reduce: Finished run
   Shutting down provisioner..
   Shutting down 3 service(s) and 4 actor(s)...
   Health loop stopped gracefully.
   Error stopping proc_mesh for replica 0: _fetcher_procs
   Health loop stopped gracefully.
   Health loop stopped gracefully.
   Shutdown completed successfully

   ```

You now have a completed GRPO training run on SUNK. The job produced
training logs locally and reported metrics to your Weights & Biases project,
where you can inspect loss, rewards, and other training statistics.

View training metrics in your Weights & Biases dashboard at [wandb.ai](https://wandb.ai/site).

## Additional resources

* [torchforge GitHub repository](https://github.com/meta-pytorch/torchforge)
* [PyTorch Documentation](https://docs.pytorch.org/docs/)
