# Run SkyPilot on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/skypilot

# Run SkyPilot on CKS

> Install and configure SkyPilot on CKS for simplified AI workload execution and inference deployment

[SkyPilot](https://docs.skypilot.ai/en/latest/docs/index.html) is an open source framework that simplifies, optimizes, and unifies the execution of AI, LLM, and batch workloads. SkyPilot runs across a variety of compute infrastructure, including CoreWeave Kubernetes Service (CKS).

SkyPilot abstracts the complexities of provisioning, scheduling, and managing underlying resources, so you can define your jobs once and then run them. SkyPilot includes features such as the ability to `ssh` into containers, fuse mount and configure access to object storage, and monitor execution.

## Overview

This guide shows how to install and configure SkyPilot for use with CKS. It covers the initial setup and walks through several common use cases. Examples include creating a development cluster, testing network performance, and deploying an inference service.

### Prerequisites

Before you start, you'll need the following:

* A working [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with GPU Nodes.
* [Conda](https://docs.conda.io/en/latest/) installed on your local machine.
* Optional: The ability to create [CoreWeave AI Object Storage buckets](https://docs.coreweave.com/products/storage/object-storage/about.md) and configure access permissions.
* Optional: The [AWS CLI](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#install-tools) installed and configured on your local machine.

## Install SkyPilot

Install the SkyPilot CLI in an isolated Conda environment, then verify that SkyPilot can detect your CKS cluster.

1. Create an isolated Conda environment and install the SkyPilot CLI with CoreWeave support to avoid package conflicts:

   ```bash theme={"system"}
   conda create -y -n sky python=3.10
   conda activate sky
   pip install "skypilot[coreweave]"
   ```

   > [!NOTE]
   >
   > * CKS requires SkyPilot version 0.10.1 or later.
   > * SkyPilot requires Python 3.7 to 3.13.

2. Verify that SkyPilot detects your CKS cluster:

   ```bash theme={"system"}
   sky check
   ```

   The output lists your allowed contexts, which are the names of your CoreWeave CKS clusters. In this example, the context is `cks-usw04`:

   ```text theme={"system"}
   🎉 Enabled infra 🎉
     CoreWeave [storage]
     Kubernetes [compute]
       Allowed contexts:
       └── cks-usw04
   ```

For full installation instructions and directions for installing from source, see [SkyPilot's installation documentation](https://docs.skypilot.ai/en/latest/getting-started/installation.html).

With SkyPilot installed and able to see your cluster, you can now use it to launch workloads on CKS.

## Use SkyPilot to create a development cluster

This section walks through launching an interactive development Pod ("devpod") on CKS so you can iterate on code in a GPU-backed container.

To create a cluster with a specific container, use the [simple-devpod.yaml](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/simple-devpod.yaml) configuration YAML. Full YAML specifications are described in the [SkyPilot YAML specification reference](https://docs.skypilot.ai/en/latest/reference/yaml-spec.html).

> [!NOTE]
>
> This example uses a [development container from the CoreWeave ML team](https://github.com/coreweave/ml-containers?tab=readme-ov-file#pytorch-extras).

### Launch a devpod

To launch a development cluster using the [simple-devpod.yaml](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/simple-devpod.yaml) configuration YAML, complete the following steps:

1. Download the file and complete the following tasks:

   * Run `sky show-gpus` and note the GPU type in your context.
   * Update `accelerators` to your GPU type.

   ```yaml theme={"system"}
   resources:
     # Modify this below to request different resources
     # Change to your GPU type.
     accelerators: H100_NVLINK_80GB:1  # Use 1 H100
     # You can use your own container, but we recommend using a CW one because they are optimized for networking.
     image_id: docker:ghcr.io/coreweave/ml-containers/nightly-torch-extras:8b6c417-base-25110205-cuda12.9.1-ubuntu22.04-torch2.10.0a0-vision0.25.0a0-audio2.10.0a0
     memory: 32+  # Request at least 32GB of RAM
   ```

   The `accelerators` value must match the GPU shown in the output after running `sky show-gpus`. SkyPilot won't schedule the job if the `accelerators` value and the output from `sky show-gpus` don't match.

2. Deploy the configuration to launch the devpod:

   ```bash theme={"system"}
   sky launch -c mysimpledevpod simple-devpod.yaml
   ```

   > [!TIP]
   >
   > If you modify any configuration settings, or if you run into problems, for example, SkyPilot can't find the bucket, stop and start the API server, then re-run the `launch` command:
   >
   > ```bash theme={"system"}
   > sky api stop
   > sky api start
   > sky check coreweave kubernetes
   > sky launch -c mysimpledevpod simple-devpod.yaml
   > ```

3. Stream the provisioning logs to monitor progress:

   ```bash theme={"system"}
   sky logs --provision mysimpledevpod
   ```

4. Launch the SkyPilot dashboard to see the status of your clusters:

   ```bash theme={"system"}
   sky dashboard
   ```

   From the dashboard, use the commands to `ssh` into your cluster, connect with VSCode or Cursor, or terminate the Pod.

   For example, to `ssh` into the Pod:

   ```bash theme={"system"}
   ssh mysimpledevpod
   ```

   To automatically stop the development machine after a period of idle time, for example, after five hours:

   ```bash theme={"system"}
   sky autostop -i 300 mysimpledevpod
   ```

   For more information about starting and stopping a development server, see [SkyPilot's interactive development guide](https://docs.skypilot.ai/en/latest/examples/interactive-development.html#autostop).

## Optional: Set up CoreWeave AI Object Storage and launch a devpod

> [accordion] Optional: Launch a devpod with storage configured
>
> To set up [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md), complete the following steps in the [Cloud Console](https://console.coreweave.com/clusters):
>
> 1. Get AI Object Storage access keys by following the instructions to [create access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md). Be sure to save the `Key Id` and `Key Secret` so you can access them later.
>
> 2. If you don't already have one, create an AI Object Storage organization access policy by following the instructions to [manage organization access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md). You must have at least one organization access policy set before you can use AI Object Storage.
>
> 3. Create an AI Object Storage bucket by following the instructions to [create a bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md).
>
> ### Configure your development environment for AI Object Storage
>
> 1. Create a `cw` profile in `~/.coreweave/`:
>
>    ```bash theme={"system"}
>    AWS_SHARED_CREDENTIALS_FILE=~/.coreweave/cw.credentials aws configure --profile cw
>    ```
>
>    When prompted, enter your CoreWeave Object Storage credentials. Replace `[ACCESS-KEY-ID]` with your access key ID and `[SECRET-ACCESS-KEY]` with your secret access key.
>
>    ```text theme={"system"}
>    AWS Access Key ID [None]: [ACCESS-KEY-ID]
>    AWS Secret Access Key [None]: [SECRET-ACCESS-KEY]
>    Default region name [None]:
>    Default output format [None]: json
>    ```
>
>    > [!NOTE]
>    >
>    > SkyPilot's CoreWeave adaptor [hardcodes `~/.coreweave/` as the credential and config location](https://github.com/skypilot-org/skypilot/blob/master/sky/adaptors/coreweave.py). These paths are specific to SkyPilot and differ from the standard `~/.aws/` paths used in the rest of the CoreWeave docs.
>
> 2. Configure the CoreWeave storage endpoint and set the addressing style to virtual:
>
>    ```bash theme={"system"}
>    AWS_CONFIG_FILE=~/.coreweave/cw.config aws configure set endpoint_url https://cwobject.com --profile cw
>    AWS_CONFIG_FILE=~/.coreweave/cw.config aws configure set s3.addressing_style virtual --profile cw
>    ```
>
>    > [!NOTE]
>    >
>    > **Endpoint selection**
>    >
>    > Use `https://cwobject.com` so the bucket's endpoint is accessible from anywhere and uses secure HTTPS. This endpoint supports uploading local data.
>    >
>    > **Always use** `http://cwlota.com` if you don't need to upload local data to the bucket. The LOTA endpoint provides faster access within CoreWeave's network. For more information, see [About LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md).
>    >
>    > To configure the LOTA endpoint:
>    >
>    > ```bash theme={"system"}
>    > AWS_CONFIG_FILE=~/.coreweave/cw.config aws configure set endpoint_url http://cwlota.com --profile cw
>    > AWS_CONFIG_FILE=~/.coreweave/cw.config aws configure set s3.addressing_style virtual --profile cw
>    > ```
>
> 3. Verify that SkyPilot detects your CKS cluster:
>
>    ```bash theme={"system"}
>    sky check
>    ```
>
>    The output lists your allowed contexts, which are the names of your CoreWeave CKS clusters. In this example, the context is `cks-usw04`:
>
>    ```text theme={"system"}
>    🎉 Enabled infra 🎉
>      CoreWeave [storage]
>      Kubernetes [compute]
>        Allowed contexts:
>        └── cks-usw04
>    ```
>
> In this example, the CoreWeave AI Object Storage bucket you specify is fuse mounted at `/my_data`. The code in the `my-code` directory is copied to `~/sky_workdir` on the container.
>
> This example also installs the AWS CLI and configures it to find configuration files and credentials in the relevant CoreWeave locations, enabling AWS S3 API access to CoreWeave storage. This is only for convenience. To access files using LOTA cache acceleration, use the LOTA endpoint and S3 interface.
>
> ### Launch a devpod with storage configured
>
> To launch a development cluster with storage configured, use the [mydevpod.yaml](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/mydevpod.yaml) configuration YAML and complete the following steps:
>
> 1. Download the file and modify the `accelerators` and `source` fields:
>
>    * Run `sky show-gpus` and note the GPU type in your context.
>    * Update `accelerators` to your GPU type.
>
>    ```yaml theme={"system"}
>    resources:
>      # Modify this below to request different resources
>      # Change to your GPU type.
>      accelerators: H100_NVLINK_80GB:1  # Use 1 H100
>      image_id: docker:ghcr.io/coreweave/ml-containers/nightly-torch-extras:8b6c417-base-25110205-cuda12.9.1-ubuntu22.04-torch2.10.0a0-vision0.25.0a0-audio2.10.0a0
>      memory: 32+  # Request at least 32GB of RAM
>
>    file_mounts:
>      /my_data: # Mount storage bucket to /my_data in the container
>        # Change to your bucket name.
>        source: cw://skypilot # Change this to be your bucket name
>        mode: MOUNT  # MOUNT or COPY or MOUNT_CACHED. Defaults to MOUNT. Optional.
>    # Sync data in my-code/ on local machine to ~/sky_workdir in the container
>    # Be sure this directory is created on your local machine.
>    workdir: ./my-code
>    ```
>
>    Be sure to create a directory on your local machine called `my-code`.
>
> 2. Deploy the configuration to launch the devpod:
>
>    ```bash theme={"system"}
>    sky launch -c mydevpod mydevpod.yaml
>    ```
>
>    > [!TIP]
>    >
>    > If you run into problems, for example, SkyPilot can't find the bucket, stop and start the API server, then re-run the `launch` command:
>    >
>    > ```bash theme={"system"}
>    > sky api stop
>    > sky api start
>    > sky check coreweave kubernetes
>    > sky launch -c mydevpod mydevpod.yaml
>    > ```
>
> 3. Stream the provisioning logs to monitor progress:
>
>    ```bash theme={"system"}
>    sky logs --provision mydevpod
>    ```
>
> 4. Launch the SkyPilot dashboard to see the status of your clusters:
>
>    ```bash theme={"system"}
>    sky dashboard
>    ```
>
>    For more information about starting and stopping a development server, see [SkyPilot's interactive development guide](https://docs.skypilot.ai/en/latest/examples/interactive-development.html#autostop).

## Test network performance

After your devpod is running, you can validate that the high-performance network fabric is working as expected before scaling out to multi-Node workloads.

The CoreWeave network fabric is optimized for high-performance workloads, and CoreWeave InfiniBand support for SkyPilot is configured automatically when you specify the `network_tier: best` configuration option.

To test network performance for collective operations, you can use the [CoreWeave-specific SkyPilot example](https://docs.skypilot.ai/en/latest/examples/performance/coreweave_infiniband.html) as a framework. This example deploys one of the CoreWeave example images that is configured with tested drivers and software to be a base for any HPC application. For more information about CoreWeave NCCL tests, see the [nccl-test GitHub repository](https://github.com/coreweave/nccl-tests).

## Deploy an inference service

This section shows how to move from interactive development to serving a model behind an HTTP endpoint using SkyPilot's launch and serve workflows.

You can deploy an inference service on Kubernetes using SkyPilot. The following example uses a [CoreWeave configuration YAML for vllm](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/vllm.yaml).

1. To launch the inference service, download the [vllm.yaml file](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/vllm.yaml) and modify the `accelerators` field to match your GPU type:

   ```yaml theme={"system"}
   # Change to your GPU type.
   accelerators: H100_NVLINK_80GB:1  # Use 1 H100
   ```

2. Launch the service:

   ```bash theme={"system"}
   sky launch -c vllm-test vllm.yaml
   ```

3. Capture the service endpoint in an environment variable:

   ```bash theme={"system"}
   ENDPOINT=$(sky status --endpoint 8000 vllm-test)
   ```

4. Send a test request to the service:

   ```bash theme={"system"}
   curl http://${ENDPOINT}/v1/completions  -H "Content-Type: application/json" \
     -d '{
       "model": "facebook/opt-125m",
       "prompt": "Once upon a time, there lived a princess who",
       "max_tokens": 20
     }'
   ```

5. To scale the inference service, use the `sky serve` command:

   ```bash theme={"system"}
   sky serve up -n vllm-serve vllm.yaml
   ```

For more serving examples, see [SkyPilot's serving examples](https://docs.skypilot.ai/en/latest/examples/serving/index.html).

## Deploy a multinode training job

For training workloads that span multiple Nodes, SkyPilot can launch a distributed job that takes advantage of CoreWeave's InfiniBand fabric.

To launch a multinode training job, you can use the [CoreWeave distributed training configuration YAML](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/distributed_training.yaml) that's based on the [SkyPilot distributed training with PyTorch example](https://docs.skypilot.ai/en/latest/examples/training/distributed-pytorch.html).

The CoreWeave example specifies using `network_tier: best`, which automatically configures optimal InfiniBand support and is configured with tested drivers and software as a base for high-performance training jobs.

When using the [distributed\_training.yaml](https://github.com/coreweave/reference-architecture/blob/main/skypilot/config-examples/distributed_training.yaml), be sure to change the `accelerators` field to match your GPU type:

```yaml theme={"system"}
# Change to your GPU type.
accelerators: H100_NVLINK_80GB:1  # Use 1 H100
```

## Set up a production API server

When you're ready to share SkyPilot resources across a team rather than run it per user, use the SkyPilot API server.

All of the preceding examples assume clusters are isolated to individual users. If your team wants to use SkyPilot to share resources, follow the instructions to create a [SkyPilot API server](https://docs.skypilot.ai/en/latest/reference/api-server/api-server.html#sky-api-server).

## Next steps

If your SkyPilot jobs use large inline `run` or `setup` scripts, see [Why am I hitting request limits with the Kubernetes API?](https://docs.coreweave.com/support/cks/articles/why-am-i-hitting-request-limits-with-the-kubernetes-api) to avoid errors caused by oversized Kubernetes API requests.

To learn more about SkyPilot, see the [SkyPilot documentation](https://docs.skypilot.ai/en/latest/docs/index.html).

You can also deploy [marimo](https://marimo.io/) reactive notebooks with SkyPilot for interactive GPU development or batch processing. See the [marimo SkyPilot deployment guide](https://docs.marimo.io/guides/deploying/deploying_skypilot/) for details.
