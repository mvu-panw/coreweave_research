# Create custom images for SUNK Standard

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/custom-images

# Create custom images for SUNK Standard

> Customize published SUNK images with Dockerfiles and configure them for SUNK Standard compute and login nodes

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

When you use Slurm, it's common practice to create a custom image with task-specific software and dependencies installed. CoreWeave publishes SUNK images that you can customize at every stage of deployment.

This page explains how to build a custom SUNK image from a published base image and configure it for use on compute and login nodes. It's intended for cluster administrators who prepare SUNK deployments that require additional software or dependencies beyond the published images.

## Customize a published SUNK image

You can customize an existing SUNK image with a Dockerfile by following these steps.

1. Browse [the container registry](https://gitlab.com/coreweave/sunk/container_registry) for a published SUNK image that closely matches your requirements.

2. Create a Dockerfile using the `FROM` directive to specify the selected base image. For example:

   ```dockerfile theme={"system"}
   FROM coreweave/sunk-base:latest
   # Your customizations go here...
   ```

   > [!TIP]
   >
   > For more information about using the `FROM` instruction, see [the Docker documentation](https://docs.docker.com/engine/reference/builder/#from).

3. Add the needed software and dependencies by extending the Dockerfile with custom instructions.

4. To create a custom image, build the Dockerfile.

After this procedure, you have a custom container image based on a published SUNK image, ready to reference from your SUNK deployment configuration.

## Use custom images

After you customize a SUNK image with a Dockerfile, you must define the image in the appropriate section of the `values.yaml` file, depending on the type of node the image targets. This process is the same for all Slurm node types, including the Node Controller and database. The following examples demonstrate how to define SUNK images for a compute node and for a login node.

### Define a custom compute node image

Define custom images for compute nodes in the `compute.nodes.<node-type>` section of the `values.yaml` file.

Specify the custom image, including the repository and tag, for each compute node definition in `compute.nodes`, as in the following example:

```yaml theme={"system"}
compute:
  nodes:
    my-node-type:
      image:
        repository: custom-slurmd
        tag: 1.0.0
```

### Define a custom login node image

Define custom images for login nodes in the `login.image` section of the `values.yaml` file.

Specify the custom image, including the repository and tag, in `login.image`, as in the following example:

```yaml theme={"system"}
login:
  image:
    repository: custom-controller
    tag: 1.0.0
```
