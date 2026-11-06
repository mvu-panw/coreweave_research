# Create and configure Prolog and Epilog scripts

Source: https://docs.coreweave.com/products/sunk/run_workloads/create-prolog-epilog

# Create and configure Prolog and Epilog scripts

> Create Kubernetes ConfigMaps with Prolog and Epilog scripts and configure SUNK to run them with Slurm jobs

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

In a Slurm environment, Prolog and Epilog scripts are tools that run automatically at the start (Prolog) and end (Epilog) of every job. You can use these scripts for tasks such as preparing the environment or cleaning up after a job. This guide shows you how to deploy and configure these scripts in SUNK using Kubernetes ConfigMaps, so you can standardize per-job setup and teardown across your cluster.

First, you create separate ConfigMaps for your Prolog and Epilog scripts. Each ConfigMap should contain all the scripts you plan to use. Then, you configure SUNK to use the scripts in the ConfigMaps. After you complete this guide, your SUNK deployment runs your Prolog before each job and your Epilog after each job.

## Create a Prolog ConfigMap

Consider this example Prolog script, which runs before every job.

```bash theme={"system"}
#!/usr/bin/env bash
set -e

echo "Prolog test executed"
```

Convert that script into a Kubernetes ConfigMap, like this:

```yaml theme={"system"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: slurm-prolog
data:
  prolog-test.sh: |
    #!/usr/bin/env bash
    set -e

    echo "Prolog test executed"
```

Replace `prolog-test.sh` with your script's name and the content with your actual script.

Save this YAML as `slurm-prolog-configmap.yaml`. Now apply the ConfigMap to your Kubernetes cluster:

```bash theme={"system"}
kubectl apply -f slurm-prolog-configmap.yaml
```

This step creates the ConfigMap in your cluster, but doesn't activate it in SUNK yet. You activate it in [Configure SUNK to use the scripts](#configure-sunk-to-use-the-scripts).

## Create an Epilog ConfigMap

Creating an Epilog ConfigMap is similar to creating the Prolog. Here's an example Epilog script that runs after every job:

```bash theme={"system"}
#!/usr/bin/env bash
set -e

echo "Epilog test executed"
```

Convert that script into a Kubernetes ConfigMap, like this:

```yaml theme={"system"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: slurm-epilog
data:
  epilog-test.sh: |
    #!/usr/bin/env bash
    set -e

    echo "Epilog test executed"
```

Replace `epilog-test.sh` with your script's name and the content with your actual script.

Save this YAML as `slurm-epilog-configmap.yaml`, then apply the ConfigMap to your Kubernetes cluster:

```bash theme={"system"}
kubectl apply -f slurm-epilog-configmap.yaml
```

As before, this creates the ConfigMap, but it's not yet active in SUNK.

## Configure SUNK to use the scripts

After the scripts are in ConfigMaps, configure SUNK to locate them so the `slurmd` daemon can mount and execute them with each job.

In the Slurm chart `values.yaml` for the SUNK deployment, set the `compute.prologConfigMap` and `compute.epilogConfigMap` values to the ConfigMap names. Each accepts a single name or a list of names.

Here's an example:

```yaml theme={"system"}
compute:
  prologConfigMap: slurm-prolog
  epilogConfigMap: slurm-epilog
```

Replace `slurm-prolog` and `slurm-epilog` with the names of your ConfigMaps.

After updating `values.yaml`, apply the changes to the deployment:

```bash theme={"system"}
helm upgrade my-sunk-deployment chart/path -f values.yaml
```

Replace `my-sunk-deployment` with the name of your Slurm deployment and `chart/path` with the path to your Slurm chart. From the root of the SUNK repository, the command looks like this:

```bash theme={"system"}
helm upgrade slurm chart/slurm -f values.yaml
```
