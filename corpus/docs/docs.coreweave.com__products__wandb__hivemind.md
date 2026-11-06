# HiveMind

Source: https://docs.coreweave.com/products/wandb/hivemind

# HiveMind

> A shared dashboard for AI coding sessions. Track activity, spend, and outcomes across Claude Code, Cursor, Codex, Gemini CLI, and more with leaderboards, team views, and efficiency insights.

HiveMind is a shared dashboard for AI coding sessions. The dashboard shows what your team is doing with agents, what that work costs, and what it produces, with leaderboards, team views, efficiency insights, and more. A lightweight HiveMind daemon runs on each developer's machine, watches for coding-agent activity, and sends session transcripts to the HiveMind service. You can use the hosted service at [hivemind.wandb.tools](https://hivemind.wandb.tools) or an instance that you [host yourself](#self-host-hivemind).

HiveMind is designed for a dual audience:

* **Developers and AI practitioners** can review past sessions, search their team's history, and improve how they work with coding agents.
* **Engineering leaders** can track AI coding adoption, spend, and outcomes across teams and repositories.

## Quickstart

> [!TIP]
>
> HiveMind and its documentation live on a dedicated site: [hivemind.wandb.tools](https://hivemind.wandb.tools).

### 1. Install the HiveMind daemon

On each team member's local system, install the client, authenticate, and start the daemon. Choose the method that fits your platform.

> [tab] Install script (macOS or Linux)
>
> Download and run the HiveMind install script:
>
> ```bash theme={"system"}
> curl -fsSL https://hivemind.wandb.tools/install | sh
> hivemind start
> ```
>
> * On macOS, the install script requires Apple Silicon. On an Intel Mac, use `uv` instead.
>
> * On an Apple Silicon Mac with Homebrew, the script installs the `wandb-hivemind` Homebrew cask. Everywhere else, it downloads a signed binary to `~/.local/bin`.
>
> * Privileged access (`sudo`) is not required.
>
> * `hivemind start` walks you through the terms of service and sign-in, then registers a background service (launchd on macOS, systemd on Linux) so the daemon keeps running and starts on login.
>
> * The daemon upgrades itself, with no action required.
>
> > [!TIP]
> >
> > For details about distributing and installing the standalone binary with fleet rollout tools like JAMF, Intune, Mosyle, Kandji, or Workspace ONE, see [MDM](https://hivemind.wandb.tools/docs/mdm) in the HiveMind documentation.

> [tab] uv (macOS or Linux)
>
> Install with `uv` on macOS or Linux:
>
> ```bash theme={"system"}
> uv tool install wandb-hivemind
> hivemind start
> ```
>
> * `uv` automatically selects the correct binary for the operating system. Use `uv` on an Intel Mac or on Windows, where the install script doesn't apply.
> * `hivemind start` walks you through the terms of service and sign-in, then registers a background service (launchd on macOS, systemd on Linux) so the daemon keeps running and starts on login.
> * Upgrade with `uv tool upgrade wandb-hivemind`.

You can sign in with GitHub or through your organization's single sign-on (SSO). After you sign in, the HiveMind daemon watches for coding-agent activity and sends session transcripts to the HiveMind service.

To pause syncing without uninstalling the daemon, run `hivemind config set daemon.disabled true`. The background service stays loaded, so launchd and mobile device management (MDM) presence checks still pass. However, the daemon idles instead of uploading sessions, and `hivemind status` reports `Disabled`. To resume syncing, set `daemon.disabled` back to `false`.

To exclude specific repositories or directories from HiveMind, add them to `sessions.ignore_repos` or `sessions.ignore_paths`. The daemon never uploads a matching session. For example:

```bash theme={"system"}
hivemind config add sessions.ignore_repos "myorg/secret-project"
hivemind config add sessions.ignore_paths "~/clients"
```

For details, see [Permissions](https://hivemind.wandb.tools/docs/permissions#never-upload-a-repo-or-directory) in the HiveMind documentation.

### 2. Access the HiveMind dashboard

After the HiveMind service starts receiving information from your team, access the [HiveMind dashboard](https://hivemind.wandb.tools) to track, understand, and refine your team's AI usage over time.

From the HiveMind dashboard, your team can:

* **See sessions across agents**: One daemon captures sessions from every supported agent, with no per-agent configuration. A session that an agent starts as a subprocess is linked to its parent, so fan-out appears as a tree rather than as unrelated sessions.
* **Organize and filter sessions**: Attach key-value labels and tags to a session, then narrow the **Sessions** page to what you care about. A set of `hivemind.*` labels is derived from every session automatically, so filtering is useful before anyone tags anything by hand. To tag the session you're in, run `hivemind tag`. You can also edit tags from the **Labels** card in the session insights sidebar. To let a coding agent tag its own session, install the `hivemind-tag` skill. For details, see [Labels and tags](https://hivemind.wandb.tools/docs/labels) in the HiveMind documentation.
* **Track spend and usage**: View estimated cost over time, cost by model and team, token usage, and cost per merged pull request. A session's **Timeline** tab shows how its work spread across sub-agents and workflow runs, and what each part cost. Cost figures are estimates from published model pricing and session token counts, not billed amounts from your AI vendors. To report your own token usage and cost from the command line, run `hivemind usage`.
* **Measure outcomes**: Connect agent activity to pull requests, merge rates, and how much agent-written code survives.
* **Track skills and slash commands**: A sortable, paginated table shows what your team invokes and how widely each one is used, with category badges and multi-select category filters. Preview a definition, then copy or download it.
* **Reuse past work**: Use `@hivemind` inside Claude Code, Codex, or Cursor to search your team's session history and bring relevant context into your current session.
* **Learn from history**: Import existing sessions from local tools like Claude Code or Cursor to gain new insights from prior AI usage.

These screenshots show example pages in the HiveMind dashboard, including leaderboards, usage and cost breakdowns, session details, and more. Click a screenshot to view details.

![HiveMind adoption leaderboard](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-dashboard-leaderboard.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=e268b8dc904dff14053dfe9bbe6d6d72)

![HiveMind usage dashboard](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-dashboard-usage.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=a866f69a81aaf2556a2c6dfbf2e78784)

![HiveMind cost dashboard](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-dashboard-cost.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=a440f1b7198f06347b5014ac2e651262)

![HiveMind recent sessions](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-recent-sessions.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=d73c48a392d92b9e3a5ef2900030889f)

![HiveMind session details](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-session-insights.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=8b1c4d8edecd10c700b0f9595a152ca9)

![HiveMind session Timeline tab showing sub-agent runs](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-session-timeline.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=564ec448799499e020d67f11a355ec05)

![HiveMind agents by harness](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-agents-by-harness.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=8bfdc142f0683331e79574b433400ad9)

![HiveMind agents by model](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-agents-by-model.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=1ec419453cf4df415b73e27cc4bd8ac2)

![HiveMind skills dashboard](https://mintcdn.com/coreweave-dbfa0e8d/adLpVDUDyumcIn9O/products/wandb/_media/hivemind-skills.png?fit=max\&auto=format\&n=adLpVDUDyumcIn9O\&q=85\&s=b221169d067c3def4b83311f5d004c59)

## Supported agents

HiveMind captures sessions from many coding agents, with no agent-specific configuration required. For example:

* Claude Code
* Codex
* Cursor
* Gemini CLI
* GitHub Copilot CLI
* OpenCode
* Pi
* Devin

For the full list, see [hivemind.wandb.tools](https://hivemind.wandb.tools).

With the daemon running, your session appears on the dashboard within around 30 seconds of using a supported agent.

## Self-host HiveMind

To run HiveMind on your own infrastructure instead of using the hosted service, install the `hivemind` CLI on a Linux host that runs Docker with the Compose plugin. For a small team, the host requires at least 4 GB of RAM and 2 vCPUs. Then run:

```bash theme={"system"}
hivemind serve up
```

On first run, a setup wizard configures network access, GitHub sign-in, the database, storage, and the large language model (LLM) that powers AI features. The wizard then starts the stack and prints a one-time URL for creating the first admin account.

If your developers use GitHub Enterprise Server or GitHub Enterprise Cloud with data residency, provide your GitHub Enterprise hostname in the setup wizard. Sign-in, the GitHub App, organization and team sync, and pull request enrichment then use your GitHub Enterprise host instead of `github.com`. Daemons get the host from your server with no extra configuration. If a GitHub Enterprise Server appliance uses a private CA, each developer must also set `HIVEMIND_GITHUB_CA_BUNDLE` to the local PEM path.

To connect your team, each developer runs the install script that your instance serves, which points the daemon at your server. Replace `[YOUR-HIVEMIND-DOMAIN]` with the domain of your HiveMind instance:

```bash theme={"system"}
curl -fsSL https://[YOUR-HIVEMIND-DOMAIN]/install | sh
hivemind login
hivemind start
```

For sizing, backups, upgrades, and the configuration reference, see [Self-Hosting](https://hivemind.wandb.tools/docs/self-hosting) in the HiveMind documentation.

## HiveMind and Weave

If you already use W\&B Weave, it works together with HiveMind. They cover different stages and answer different questions.

* Weave observes what your AI application does in production, tracking LLM and agent traces, evaluations, and quality.
* HiveMind observes how your team builds software with AI coding agents, tracking sessions, spend, and productivity.

## Next steps

See the [HiveMind documentation](https://hivemind.wandb.tools/docs/overview) for full details about setup, permissions, the CLI reference, troubleshooting, and more.
