# Customize cluster behavior with Lua plugins on SUNK Standard

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/lua-plugins

# Customize cluster behavior with Lua plugins on SUNK Standard

> Use Slurm's custom job submit script to enforce rules and control job submissions on SUNK Standard clusters

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

SUNK supports Slurm's custom job submit script functionality to control cluster behavior and user job submissions. When a user submits a Slurm job to the SUNK cluster, the script evaluates the job's attributes before accepting it into the job queue. The script can enforce resource limitations, redirect jobs to specific queues, and require specific fields for job submissions.

You can customize the script to enforce rules based on specific job attributes, such as partition, GPU count, time limit, or user account.

## Deploy a custom job submit script to SUNK

To make a custom Lua script available to Slurm, deploy the script to the cluster and configure Slurm to load it at startup:

1. Deploy the script in a Kubernetes ConfigMap with the key `job_submit.lua`.
2. Add the name of the ConfigMap in the Slurm `values.yaml` file at `controller.etcConfigMap`.
3. Set the `slurmConfig.JobSubmitPlugins: [lua]` parameter to enable the use of Lua scripts in the Slurm cluster.

After these steps, Slurm evaluates incoming job submissions against your script before adding them to the job queue.

> [!WARNING]
>
> The Lua script must be named `job_submit.lua` and must reside in the default configuration directory. An invalid script crashes `slurmctld`.

## Example script

The following script is an example from the [Slurm source code](https://github.com/SchedMD/slurm/blob/master/contribs/lua/job_submit.lua) that sets a partition for user jobs.

```lua theme={"system"}
--[[

 Example lua script demonstrating the Slurm job_submit/lua interface.
 This is only an example, not meant for use in its current form.

 For testing, copy this script into a file named "job_submit.lua"
 in the same directory as the Slurm configuration file, slurm.conf.

--]]

function slurm_job_submit(job_desc, part_list, submit_uid)
  if job_desc.account == nil then
    local account = "***TEST_ACCOUNT***"
    slurm.log_info("slurm_job_submit: job from uid %u, setting default account value: %s",
        submit_uid, account)
    job_desc.account = account
  end
--  If no default partition, set the partition to the highest
--  priority partition this user has access to
  if job_desc.partition == nil then
    local new_partition = nil
    local top_priority  = -1
    local last_priority = -1
    local inx = 0
    for name, part in pairs(part_list) do
      slurm.log_info("part name[%d]:%s", inx, part.name)
      inx = inx + 1
      if part.flag_default ~= 0 then
        top_priority = -1
        break
      end
      last_priority = part.priority
      if last_priority > top_priority then
        top_priority = last_priority
        new_partition = part.name
      end
    end
    if top_priority >= 0 then
      slurm.log_info("slurm_job_submit: job from uid %u, setting default partition value: %s",
          job_desc.user_id, new_partition)
      job_desc.partition = new_partition
    end
  end

  return slurm.SUCCESS
end

function slurm_job_modify(job_desc, job_rec, part_list, modify_uid)
  if job_desc.comment == nil then
    local comment = "***TEST_COMMENT***"
    slurm.log_info("slurm_job_modify: for job %u from uid %u, setting default comment value: %s",
        job_rec.job_id, modify_uid, comment)
    job_desc.comment = comment
  end

  return slurm.SUCCESS
end

slurm.log_info("initialized")
return slurm.SUCCESS
```
