# Where the Weights & Biases docs moved

Source: https://docs.coreweave.com/forge-docs-whats-moved

# Where the Weights & Biases docs moved

> A map from the previous Weights & Biases documentation to its current location

The Weights & Biases documentation merged into the CoreWeave docs when CoreWeave launched Forge. Forge brings Weights & Biases together with Post-Training, Serverless Inference, CoreWeave Sandboxes, and other Forge products. The content you relied on is still here. It is reorganized into this site's navigation, and the old paths redirect.

This page maps each section of the old documentation site to its new location. For what changed in the product itself, such as addresses and the header, see [What moved in Forge](https://docs.coreweave.com/forge-whats-moved.md).

## How this site is organized

Tabs at the top of the page organize the site's content into the following areas:

* **Infrastructure** covers CoreWeave's cloud platform: Kubernetes, SUNK, storage, and networking.
* **Forge** holds the Weights & Biases documentation alongside the other Forge products. Its dropdown lists Forge Home, Platform (the shared admin and hosting surface), ARIA, Weights & Biases (which includes W\&B Weave), Post-Training, Agent Lens, Serverless Inference, Sandboxes, Notebooks, and Registry.
* **Reference**, **Release Notes**, and **Support** each split into an Infrastructure group and a Forge group. The Forge groups hold the former Weights & Biases reference, release notes, and support content.

## Where each section went

The old site used two generations of paths, and both redirect. The following table maps the major sections to their new locations.

| Previous section | Previous paths | Current location |
| - | - | - |
| Experiments | `/guides/track`, `/models/track` | [Experiments](https://docs.coreweave.com/products/wandb/track.md) |
| Sweeps | `/guides/sweeps`, `/models/sweeps` | [Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md) |
| Artifacts | `/guides/artifacts`, `/models/artifacts` | [Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md) |
| Registry | `/guides/registry`, `/models/registry` | [Registry](https://docs.coreweave.com/products/registry.md) |
| Reports | `/guides/reports`, `/models/reports` | [Reports](https://docs.coreweave.com/products/wandb/reports.md) |
| Integrations and tutorials | `/guides/integrations`, `/tutorials` | [Integrations](https://docs.coreweave.com/products/wandb/integrations.md) |
| W\&B Weave | `/weave` | [Weave](https://docs.coreweave.com/products/wandb/weave.md) |
| Platform, hosting, and IAM | `/guides/hosting`, `/platform/hosting` | [Hosting](https://docs.coreweave.com/products/wandb/platform/hosting.md) |
| Python SDK and CLI reference | `/ref/python`, `/ref/cli` | [Models reference](https://docs.coreweave.com/products/wandb/ref.md) |
| Notebooks | `/models/notebooks` | [Notebooks](https://docs.coreweave.com/products/notebooks.md) |
| Serverless Inference | `/inference` | [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md) |
| Serverless Training | `/serverless-training` | [Serverless Training](https://docs.coreweave.com/products/post-training/serverless-training.md) |
| Serverless Sandboxes | `/sandboxes` | [Sandboxes](https://docs.coreweave.com/products/sandboxes.md) |
| ARIA | `/aria` | [ARIA](https://docs.coreweave.com/products/aria.md) |
| Support | `/support/...` | [Support](https://docs.coreweave.com/support.md), same paths, under the Support tab |
| Release notes | `/release-notes` | [Release Notes](https://docs.coreweave.com/release-notes.md), in the Forge group |

## Where the SDK reference went

The SDK itself did not move or change: the `wandb` package, your imports, `wandb.login()`, and environment variables such as `WANDB_API_KEY` all work exactly as before. Only the documentation moved. The reference pages live in the **Reference** tab's Forge group, starting at the [reference overview](https://docs.coreweave.com/products/wandb/ref.md), and the Weights & Biases sidebar links to the same pages under **Reference**.

| Reference | Previous paths | Current location |
| - | - | - |
| W\&B Python SDK | `/ref/python` | [Python SDK](https://docs.coreweave.com/products/wandb/ref/python.md) |
| Command Line Interface (CLI) | `/ref/cli` | [CLI reference](https://docs.coreweave.com/products/wandb/ref/cli.md) |
| Query Expression Language | `/ref/query-panel` | [Query Expression Language](https://docs.coreweave.com/products/wandb/ref/query-panel.md) |
| W\&B Weave SDKs and service API | `/weave/reference` | [Weave references](https://docs.coreweave.com/products/wandb/weave/reference.md) |

## Finding things fast

* **Search.** The search bar at the top of every page searches the whole site, so a query finds Weights & Biases and CoreWeave infrastructure pages alike.
* **Ask AI.** The **Ask AI** button at the top of the page opens an assistant chat that answers questions from the documentation.
* **MCP server.** The site exposes a Model Context Protocol (MCP) server, so your coding assistant can query these docs from your development environment. See [Documentation MCP server](https://docs.coreweave.com/get-started.md#documentation-mcp-server).

## Previous links and repository

Every major path, link, and bookmark from the former Weights & Biases website redirects to the CoreWeave website. The [wandb/docs](https://github.com/wandb/docs) GitHub repository is archived and no longer accepts issues or pull requests. Documentation is now maintained in [coreweave/docs](https://github.com/coreweave/docs).

Unlike the old repository, which was public and took community pull requests, the `coreweave/docs` repo is private, and it does not accept community contributions.

If you find an error or issue in the documentation, [contact support](https://docs.coreweave.com/support/contact.md), or leave feedback from the **Was this page helpful?** section in the page footer. Click **Yes**  or **No** . Optionally, fill out a short form to tell us more, then click **Submit feedback**.

## Related

> [card] [Forge Home](https://docs.coreweave.com/forge-home.md)
>
> An overview of every product in CoreWeave Forge.

> [card] [What moved in Forge](https://docs.coreweave.com/forge-whats-moved.md)
>
> Where your projects, settings, and account moved in the Forge app.
