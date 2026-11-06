# Introduction to CoreWeave Skills

Source: https://docs.coreweave.com/platform/coreweave-skills

# Introduction to CoreWeave Skills

> Agent Skills that let your coding agent carry out CoreWeave workflows on your behalf.

> [!NOTE]
>
> CoreWeave Skills are in public preview. The skills available and their behavior may change while
> the collection is in preview. To report a problem with a skill or request a new one, open an issue
> in the [coreweave/skills](https://github.com/coreweave/skills) repository or
> [contact support](https://docs.coreweave.com/support/contact.md).

CoreWeave Skills are [Agent Skills](https://agentskills.io), an open format for packaging the
instructions an AI coding agent needs to carry out a task. Each skill is a guided workflow for one
CoreWeave operation: it covers the prerequisites, the commands to run, and the checks that confirm
the result. You install the skills once, then describe what you want in plain language. Your agent
selects the skill that matches your request and runs it.

Skills are content, not a hosted CoreWeave service. Each one is a directory of Markdown
instructions, and sometimes supporting scripts and reference files, that stays inert until your own
coding agent loads it. From that point on, the agent runs on your machine with the
tools and credentials you have given it. Any CoreWeave resources it creates or changes belong to your
organization and bill to your account.

## Prerequisites

Before you install the skills, make sure you have the following:

* [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) or another agent that
  supports Agent Skills. CoreWeave publishes and tests the skills for Claude Code, and the install
  steps on this page use Claude Code's plugin marketplace. Other agents that read the format, such
  as Cursor and Codex, can load the same skill files, but CoreWeave does not document or test those
  install paths.
* A CoreWeave account.

Individual skills have their own requirements, such as a CoreWeave API token, `kubectl`, Terraform,
a Hugging Face account, or available quota. Skills that provision or change resources check their
prerequisites before they start and report anything that is missing.

## Install the skills

The [coreweave/skills](https://github.com/coreweave/skills) repository is the only official
distribution channel for CoreWeave Skills. Claude Code installs them from a plugin marketplace
served directly from the repository, so you don't need to clone it.

> [!WARNING]
>
> CoreWeave does not publish these skills through third-party marketplaces or skill directories.
> Treat forks, modified copies, and any other source as untrusted until you have reviewed them.

1. Add the CoreWeave marketplace. You do this once per machine.

   ```text theme={"system"}
   /plugin marketplace add coreweave/skills
   ```

2. Install each plugin you want, replacing `[PLUGIN]` with a plugin name. CoreWeave recommends
   `coreweave-platform-skills` alongside the plugins for the product lines you use.

   ```text theme={"system"}
   /plugin install [PLUGIN]@coreweave-skills
   ```

3. Load the new skills into your current session.

   ```text theme={"system"}
   /reload-plugins
   ```

The skills in the plugins you installed are now available in your session, and you can start one by
describing what you want in plain language.

For the full install and upgrade procedure, including how to trigger a skill by name, see the
[coreweave/skills README](https://github.com/coreweave/skills#install-the-skills).

### Install with the `skills` CLI

To install the skills with the
[`skills` CLI](https://www.npmjs.com/package/skills), run `npx skills add coreweave/skills`. The skills are then pulled from the `dist` branch of the
[coreweave/skills](https://github.com/coreweave/skills) repository. Start a new session with your agent to load them.

To update the skills you installed with the CLI, run `npx skills update`.

> Note that `npx skills update` will not pull new skills. You will need to rerun the `add` command to see the latest skills that were published to the
> [coreweave/skills](https://github.com/coreweave/skills) repository. By contrast, managing your skills by [using the plugin](#install-the-skills) will always pull the latest skills when the plugin is updated.

## Find the available skills

Skills are grouped into plugins: one plugin of cross-cutting platform skills, plus one plugin per
CoreWeave product line, so that you install only the skills your sessions require. For the plugins
available and the skills in each, see
[What's available](https://github.com/coreweave/skills#whats-available) in the repository.

The collection changes over time. CoreWeave adds skills, revises existing ones, and withdraws skills
that a newer workflow replaces. Each plugin is versioned and released independently and has its own
changelog. For what changed and when, see the
[releases](https://github.com/coreweave/skills/releases) in the repository. To list the skills you
have installed, ask your agent which CoreWeave skills are available.

## Run skills safely

A skill's prompts, checkpoints, and verification steps are guidance, not technical access controls.
The agent acts with whatever permissions you have given it. The decisions that keep a session safe
are yours: which credentials the agent can reach, which account and region it acts on, and which
actions you approve.

Before you load or run a skill, take the following precautions:

* Read the skill's `SKILL.md` file, which holds its instructions, and review any scripts it uses.
* Use the least-privileged credentials available.
* Prefer a non-production account or organization.
* Check the expected costs of anything the skill provisions.

Prompt injection can also affect skills and other content an agent processes. For the full guidance,
including your responsibilities for the resources and charges a skill produces, see
[License, safety, and responsibilities](https://github.com/coreweave/skills#license-safety-and-responsibilities)
in the repository.

## Licensing

CoreWeave Skills are proprietary and licensed only for use with CoreWeave products and services.
The repository is publicly viewable, but the skills are not open source. CoreWeave and the CoreWeave
logo are trademarks of CoreWeave, Inc. For the complete terms, including the restrictions on
redistribution and on use of CoreWeave's trademarks, see the
[LICENSE](https://github.com/coreweave/skills/blob/main/LICENSE) in the repository.

## Related resources

> [card] [coreweave/skills](https://github.com/coreweave/skills)
>
> The official repository: install instructions, the skill inventory, and safety guidance.

> [card] [Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md)
>
> Hosted read-only observability, cluster, and documentation tools for agents that support the
> Model Context Protocol (MCP).

> [card] [CoreWeave Terraform Provider](https://docs.coreweave.com/platform/terraform.md)
>
> Manage the same infrastructure declaratively as code instead of through an agent.

> [card] [Get started with CoreWeave](https://docs.coreweave.com/get-started.md)
>
> Account setup, environment setup, and the onboarding paths the skills automate.
