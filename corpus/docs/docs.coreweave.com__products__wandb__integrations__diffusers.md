# Hugging Face Diffusers

Source: https://docs.coreweave.com/products/wandb/integrations/diffusers

# Hugging Face Diffusers

> Use Weights & Biases autolog with Diffusers to track prompts, generated media, configs, and pipeline architecture.

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/diffusers/lcm-diffusers.ipynb)

[Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index) is a library of pre-trained diffusion models for generating images, audio, and 3D structures of molecules. The Weights & Biases integration adds experiment tracking, media visualization, pipeline architecture tracking, and configuration management to interactive centralized dashboards.

## Log experiments in two lines

To log all the prompts, negative prompts, generated media, and configs associated with your experiment, add the following two lines of code:

```python theme={"system"}
# import the autolog function
from wandb.integration.diffusers import autolog

# call the autolog before calling the pipeline
autolog(init=dict(project="diffusers_logging"))
```

![Experiment results logging](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diffusers-autolog-4.gif?s=ff4cf1aebe661ffb46f0f9b8646ab7f3)

An example of how W\&B logs the results of your experiment.

## Get started

1. Install `diffusers`, `transformers`, `accelerate`, and `wandb`.

   * Command line:

     ```bash theme={"system"}
     pip install --upgrade diffusers transformers accelerate wandb
     ```

   * Notebook:

     ```bash theme={"system"}
     !pip install --upgrade diffusers transformers accelerate wandb
     ```

2. Call `autolog()` with the `init` parameter, which accepts a dictionary of parameters required by [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init). `autolog()` initializes a W\&B run and automatically tracks the inputs and outputs from [all supported pipeline calls](https://github.com/wandb/wandb/blob/main/wandb/integration/diffusers/autologger.py#L12-L72):

   * Each pipeline call is tracked into its own [table](https://docs.coreweave.com/products/wandb/tables.md) in the workspace, and the configs associated with the pipeline call are appended to the list of workflows in the configs for that run.
   * The prompts, negative prompts, and generated media are logged in a [`wandb.Table`](https://docs.coreweave.com/products/wandb/tables).
   * All other configs associated with the experiment, including seed and pipeline architecture, are stored in the config section for the run.
   * The generated media for each pipeline call are also logged in [media panels](https://docs.coreweave.com/products/wandb/track/log/media.md) in the run.

   > [!NOTE]
   >
   > Find a [list of supported pipeline calls](https://github.com/wandb/wandb/blob/main/wandb/integration/diffusers/autologger.py#L12-L72). To request a new feature of this integration or report a bug, open an issue on the [Weights & Biases GitHub issues page](https://github.com/wandb/wandb/issues).

## Examples

The following examples show `autolog` in typical diffusion workflows so you can adapt them to your own pipelines.

### Autolog example

The following is an end-to-end example of `autolog`:

> [tab] Script
>
> ```python theme={"system"}
> import torch
> from diffusers import DiffusionPipeline
>
> # import the autolog function
> from wandb.integration.diffusers import autolog
>
> # call the autolog before calling the pipeline
> autolog(init=dict(project="diffusers_logging"))
>
> # Initialize the diffusion pipeline
> pipeline = DiffusionPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16
> ).to("cuda")
>
> # Define the prompts, negative prompts, and seed.
> prompt = ["a photograph of an astronaut riding a horse", "a photograph of a dragon"]
> negative_prompt = ["ugly, deformed", "ugly, deformed"]
> generator = torch.Generator(device="cpu").manual_seed(10)
>
> # call the pipeline to generate the images
> images = pipeline(
>     prompt,
>     negative_prompt=negative_prompt,
>     num_images_per_prompt=2,
>     generator=generator,
> )
> ```

> [tab] Notebook
>
> ```python theme={"system"}
> import torch
> from diffusers import DiffusionPipeline
>
> import wandb
>
> # import the autolog function
> from wandb.integration.diffusers import autolog
>
> run = wandb.init()
>
> # call the autolog before calling the pipeline
> autolog(init=dict(project="diffusers_logging"))
>
> # Initialize the diffusion pipeline
> pipeline = DiffusionPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16
> ).to("cuda")
>
> # Define the prompts, negative prompts, and seed.
> prompt = ["a photograph of an astronaut riding a horse", "a photograph of a dragon"]
> negative_prompt = ["ugly, deformed", "ugly, deformed"]
> generator = torch.Generator(device="cpu").manual_seed(10)
>
> # call the pipeline to generate the images
> images = pipeline(
>     prompt,
>     negative_prompt=negative_prompt,
>     num_images_per_prompt=2,
>     generator=generator,
> )
>
> # Finish the experiment
> run.finish()
> ```

The following images show what gets logged to Weights & Biases:

* The results of a single experiment:

  ![Experiment results logging](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diffusers-autolog-2.gif?s=21c13de7b55777b3ea951887983e4828)

* The results of multiple experiments:

  ![Experiment results logging](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diffusers-autolog-1.gif?s=5b3e18828704632fe6fa4d88de8b5b41)

* The config of an experiment:

  ![Experiment config logging](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diffusers-autolog-3.gif?s=1eb5be9619698ee9365b1e325641e1cb)

> [!NOTE]
>
> You must explicitly call [`wandb.Run.finish()`](https://docs.coreweave.com/products/wandb/ref/python/functions/finish) when you run the code in IPython notebook environments after calling the pipeline. This is not necessary when you run Python scripts.

### Track multi-pipeline workflows

The following example demonstrates `autolog` with a typical [Stable Diffusion XL + Refiner](https://huggingface.co/docs/diffusers/using-diffusers/sdxl#base-to-refiner-model) workflow, in which the refiner refines the latents generated by the [`StableDiffusionXLPipeline`](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl).

> [tab] Script
>
> ```python theme={"system"}
> import torch
> from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusionXLPipeline
> from wandb.integration.diffusers import autolog
>
> # initialize the SDXL base pipeline
> base_pipeline = StableDiffusionXLPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-xl-base-1.0",
>     torch_dtype=torch.float16,
>     variant="fp16",
>     use_safetensors=True,
> )
> base_pipeline.enable_model_cpu_offload()
>
> # initialize the SDXL refiner pipeline
> refiner_pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-xl-refiner-1.0",
>     text_encoder_2=base_pipeline.text_encoder_2,
>     vae=base_pipeline.vae,
>     torch_dtype=torch.float16,
>     use_safetensors=True,
>     variant="fp16",
> )
> refiner_pipeline.enable_model_cpu_offload()
>
> prompt = "a photo of an astronaut riding a horse on mars"
> negative_prompt = "static, frame, painting, illustration, sd character, low quality, low resolution, greyscale, monochrome, nose, cropped, lowres, jpeg artifacts, deformed iris, deformed pupils, bad eyes, semi-realistic worst quality, bad lips, deformed mouth, deformed face, deformed fingers, deformed toes standing still, posing"
>
> # Make the experiment reproducible by controlling randomness.
> # The seed would be automatically logged to WandB.
> seed = 42
> generator_base = torch.Generator(device="cuda").manual_seed(seed)
> generator_refiner = torch.Generator(device="cuda").manual_seed(seed)
>
> # Call WandB Autolog for Diffusers. This would automatically log
> # the prompts, generated images, pipeline architecture and all
> # associated experiment configs to W&B, thus making your
> # image generation experiments easy to reproduce, share and analyze.
> autolog(init=dict(project="sdxl"))
>
> # Call the base pipeline to generate the latents
> image = base_pipeline(
>     prompt=prompt,
>     negative_prompt=negative_prompt,
>     output_type="latent",
>     generator=generator_base,
> ).images[0]
>
> # Call the refiner pipeline to generate the refined image
> image = refiner_pipeline(
>     prompt=prompt,
>     negative_prompt=negative_prompt,
>     image=image[None, :],
>     generator=generator_refiner,
> ).images[0]
> ```

> [tab] Notebook
>
> ```python theme={"system"}
> import torch
> from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusionXLPipeline
>
> import wandb
> from wandb.integration.diffusers import autolog
>
> run = wandb.init()
>
> # initialize the SDXL base pipeline
> base_pipeline = StableDiffusionXLPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-xl-base-1.0",
>     torch_dtype=torch.float16,
>     variant="fp16",
>     use_safetensors=True,
> )
> base_pipeline.enable_model_cpu_offload()
>
> # initialize the SDXL refiner pipeline
> refiner_pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
>     "stabilityai/stable-diffusion-xl-refiner-1.0",
>     text_encoder_2=base_pipeline.text_encoder_2,
>     vae=base_pipeline.vae,
>     torch_dtype=torch.float16,
>     use_safetensors=True,
>     variant="fp16",
> )
> refiner_pipeline.enable_model_cpu_offload()
>
> prompt = "a photo of an astronaut riding a horse on mars"
> negative_prompt = "static, frame, painting, illustration, sd character, low quality, low resolution, greyscale, monochrome, nose, cropped, lowres, jpeg artifacts, deformed iris, deformed pupils, bad eyes, semi-realistic worst quality, bad lips, deformed mouth, deformed face, deformed fingers, deformed toes standing still, posing"
>
> # Make the experiment reproducible by controlling randomness.
> # The seed would be automatically logged to WandB.
> seed = 42
> generator_base = torch.Generator(device="cuda").manual_seed(seed)
> generator_refiner = torch.Generator(device="cuda").manual_seed(seed)
>
> # Call WandB Autolog for Diffusers. This would automatically log
> # the prompts, generated images, pipeline architecture and all
> # associated experiment configs to W&B, thus making your
> # image generation experiments easy to reproduce, share and analyze.
> autolog(init=dict(project="sdxl"))
>
> # Call the base pipeline to generate the latents
> image = base_pipeline(
>     prompt=prompt,
>     negative_prompt=negative_prompt,
>     output_type="latent",
>     generator=generator_base,
> ).images[0]
>
> # Call the refiner pipeline to generate the refined image
> image = refiner_pipeline(
>     prompt=prompt,
>     negative_prompt=negative_prompt,
>     image=image[None, :],
>     generator=generator_refiner,
> ).images[0]
>
> # Finish the experiment
> run.finish()
> ```

The following image shows an example of a Stable Diffusion XL + Refiner experiment:

![Stable Diffusion XL experiment tracking](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/diffusers-autolog-6.gif?s=a4f2130cde06f6b6ca7f7654c338105d)

## More resources

* [A Guide to Prompt Engineering for Stable Diffusion](https://forge.coreweave.com/wandb/geekyrakshit/diffusers-prompt-engineering/reports/A-Guide-to-Prompt-Engineering-for-Stable-Diffusion--Vmlldzo1NzY4NzQ3)
* [PIXART-α: A Diffusion Transformer Model for Text-to-Image Generation](https://forge.coreweave.com/wandb/geekyrakshit/pixart-alpha/reports/PIXART-A-Diffusion-Transformer-Model-for-Text-to-Image-Generation--Vmlldzo2MTE1NzM3)
