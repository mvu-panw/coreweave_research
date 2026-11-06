# What moved in Forge

Source: https://docs.coreweave.com/forge-whats-moved

# What moved in Forge

> Where to find your projects, settings, and account in Forge if you already use Weights & Biases

If you already use Weights & Biases, your work is still available in CoreWeave Forge. Your projects, runs, artifacts, and credentials are unchanged. On September 30, 2026, the address bar and the top of the screen changed.

This page is a map from where things were to where they are now. It applies to Multi-tenant Cloud. If you use Dedicated Cloud or Self-Managed, see [What did not change](#what-did-not-change).

## Addresses

The following table maps each address you used before to its Forge equivalent.

| What | Before | Now |
| - | - | - |
| Sign in and sign up | `wandb.ai/login` | `id.coreweave.com/login` and `/signup` |
| A project | `wandb.ai/[ENTITY]/[PROJECT]` | `forge.coreweave.com/wandb/[ENTITY]/[PROJECT]` |
| Your user settings | `wandb.ai/settings` | `forge.coreweave.com/settings` |
| Organization settings | `wandb.ai/account-settings/[ORG]/[TAB]` | `forge.coreweave.com/account-settings/[ORG]/[TAB]` |
| Your profile | `wandb.ai/[USERNAME]` | `forge.coreweave.com/profile/[USERNAME]` |
| Team settings | `wandb.ai/[TEAM]/settings` | `forge.coreweave.com/wandb/[TEAM]/settings` |
| Registry | `wandb.ai/orgs/[ORG]/registry/...` | `forge.coreweave.com/registry/...` |

Two details are worth remembering:

* **The Weights & Biases app sits under `/wandb`.** A link that used to read `wandb.ai/acme/my-project` is now `forge.coreweave.com/wandb/acme/my-project`. Old links redirect, so bookmarks keep working.
* **Settings and your profile don't sit under `/wandb`.** They sit at the top level of `forge.coreweave.com`, alongside the other Forge products. Team settings are the exception and stay with the app.

## The top of the screen

The global header is new and belongs to Forge rather than to Weights & Biases. The following table maps each action you took in the old header to its Forge equivalent.

| What you did before | What to do now |
| - | - |
| Used the app switcher | Use the launcher at the far left of the header. It lists every Forge product, and the app switcher no longer exists separately. |
| Clicked the bell for alerts | The bell is gone. A megaphone icon sits in roughly the same place, but it shows announcements, not alerts. |
| Opened ARIA from inside a project | [ARIA](https://docs.coreweave.com/products/aria.md) is in the header and available from anywhere. |
| Clicked your avatar for settings | The account selector is on the right of the header, with **Profile**, **User settings**, and per-organization entries. |

### Where alerts went

Alerts moved. You now configure them in three places:

* **User settings** > **Alerts**, for your own run notifications
* **Team settings** > **Team alerts**, for a team's Slack notifications
* **Organization settings** > **Usage & Alerts**, for usage and spending thresholds

## What did not change

The following did not change:

* **`api.wandb.ai` still works.** Existing SDK scripts, CI jobs, and the mobile app keep running without changes. You don't need to update the `WANDB_BASE_URL` environment variable.
* **Your credentials.** Sign in with the same account you used before.
* **Dedicated Cloud and Self-Managed.** If you use Dedicated Cloud or Self-Managed, your deployment URLs and sign-in page are unchanged.

## Related

> [card] [Forge Home](https://docs.coreweave.com/forge-home.md)
>
> An overview of every product in CoreWeave Forge.

> [card] [Get started with Weights & Biases](https://docs.coreweave.com/products/wandb.md)
>
> Follow a quickstart for experiment tracking or for tracing LLM applications with W\&B Weave.

> [card] [Forge and CoreWeave identity](https://docs.coreweave.com/security/forge-identity-and-access.md)
>
> For administrators: how the two identity systems relate, and where you manage each one.

> [card] [Infrastructure and Forge billing](https://docs.coreweave.com/billing/coreweave-and-forge-billing.md)
>
> For administrators: which types of charges belong in which billing system, and where each billing task belongs.
