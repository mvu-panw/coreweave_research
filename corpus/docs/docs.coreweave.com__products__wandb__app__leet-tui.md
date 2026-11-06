# LEET terminal UI

Source: https://docs.coreweave.com/products/wandb/app/leet-tui

# LEET terminal UI

> Explore local W&B runs and remote run metrics from the terminal with the LEET terminal UI.

W\&B LEET (Lightweight Experiment Exploration Tool) is a keyboard-driven terminal UI for exploring W\&B runs. Use LEET to compare local metrics, inspect system utilization, browse logged images, and tail console output without opening a browser. LEET reads local `.wandb` transaction logs, so you can inspect runs before they sync to the cloud. You can also open a remote run by URL to view its scalar history and summary, or print a run's state from a script with `wandb leet inspect --summary`.

![W\&B LEET workspace view with runs, metrics, system metrics, media, console logs, and run overview panes.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/leet-workspace-all-panes.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=f0f8c555aa42a8db1666561a26569a4d)

## When to use LEET

LEET is built for engineers who spend most of their time in a terminal, especially on remote machines, clusters, or SSH sessions where a graphical browser is slow or unavailable.

| Surface | Best for |
| - | - |
| **LEET** | Local run folders on the machine that logged them; fast keyboard navigation; live monitoring while a job is still writing logs; SSH and `tmux` workflows. |
| **[W\&B App](https://docs.coreweave.com/products/wandb/runs/view-logged-runs.md)** | Full project workspaces, team collaboration, reports, sweeps, artifacts, and rich panel types across synced cloud runs. |
| **[Weights & Biases mobile app](https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/mobile-app.md)** | Lightweight monitoring and alerts for synced cloud projects on a phone (Available for Multi-tenant Cloud, in preview for Dedicated Cloud). |

LEET and Weights & Biases show the same underlying run data when that data exists locally and has been synced. LEET supports local run files, live updates from an active training process, and [limited remote-run exploration](#remote-runs).

## Prerequisites

Install or upgrade the W\&B CLI to the latest release using `pip` or `uv`:

> [tab] pip
>
> ```sh theme={"system"}
> pip install --upgrade wandb
> ```

> [tab] uv
>
> ```sh theme={"system"}
> uv pip install --upgrade wandb
> ```

This guide describes the latest CLI behavior.

> [!NOTE]
>
> In SDK v0.27.x and earlier, launch the LEET TUI with `wandb beta leet` instead of `wandb leet`.

## Launch LEET

From the directory that contains your `wandb/` folder, open the workspace. LEET selects the runs you selected the last time you opened the directory, plus the latest run if it started since then:

```sh theme={"system"}
wandb leet
```

You can pass an optional `PATH` that points to a workspace directory, a specific run directory, or a `.wandb` file:

```sh theme={"system"}
wandb leet ./wandb
wandb leet ./wandb/offline-run-20260403_145048-6ao9fhns
wandb leet ./wandb/offline-run-20260403_145048-6ao9fhns/run-6ao9fhns.wandb
```

Open the standalone system monitor (SYMON) to view host metrics without a run context:

```sh theme={"system"}
wandb leet symon --interval 2s
```

For command syntax and subcommands, see [`wandb leet`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-leet) in the CLI reference.

### Remote runs

To view a synced run, pass its URL. Replace `[ENTITY]`, `[PROJECT]`, and `[RUN-ID]` with the values from your run URL:

```sh theme={"system"}
wandb leet "https://forge.coreweave.com/wandb/[ENTITY]/[PROJECT]/runs/[RUN-ID]"
```

LEET also accepts run URLs from `wandb.ai` and from Dedicated Cloud and Self-Managed deployments. Remote runs require a network connection and API key authentication for the server that hosts the run. LEET uses your configured credentials or prompts you to log in.

Remote mode opens one run's scalar history and summary. It doesn't provide live updates, multi-run comparison, config, system metrics, media, console logs, custom X-axes, or the record inspector. Use local run files for those features.

## Views and pane layout

LEET has three main views: **workspace**, **single-run**, and **SYMON**. The **record inspector** provides a separate view of a local transaction log.

### Workspace view

Workspace view is the default. It is designed to compare multiple runs from the same local `wandb/` directory.

Typical panes include:

* **Runs sidebar** — browse and filter local run folders.
* **Metrics grid** — overlay selected runs on the same scalar charts.
* **System metrics** — charts for the highlighted run.
* **Media** — `wandb.Image` thumbnails rendered in the terminal.
* **Console logs** — assembled stdout and stderr for the highlighted run.
* **Run overview** — state, IDs, tags, notes, config, and summary values.

Use `space` to select or deselect a run for overlaid metrics. Selected runs have a filled icon. Use `p` to pin a run so its series stays on top in metric charts. Press `enter` on the highlighted run to open **single-run view**. Live runs keep updating in the workspace, so you can use LEET for both post-run analysis and monitoring an active job.

Press `ctrl+a` to select every run that matches the runs filter. The status bar shows how many runs LEET will load. Press `y` to confirm or `esc` to cancel. Press `x` to deselect all runs except the pinned one.

LEET remembers the selected and pinned runs for each `wandb/` directory in `.wandb-leet.json` and selects them again the next time you open it. It also selects the newest run if that run started after your last session, or if no remembered run is selected.

Live runs have animated markers in the runs list and a pulsing state indicator in the status bar. A running process writes its data to the `.wandb` file at least every 15 seconds, so LEET shows new values within that time even for runs that log infrequently. LEET marks a live local run as crashed after 10 minutes without transaction-log updates. If writes resume, LEET resumes live monitoring.

In narrow terminals, LEET temporarily hides the run overview sidebar, then the runs sidebar, to leave at least 24 columns for charts when possible. The sidebars return when the terminal has enough space.

### Single-run view

Single-run view focuses on one run with a metrics grid in the center, run overview on the left, and system metrics on the right. Media and console log panes open below the metrics grid when toggled on.

![W\&B LEET single-run view with run overview, metric charts, and system metrics panes.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/leet-single-run-view.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=bc1ecbf77d56f0fbaf00170c979d9339)

Press `esc` to leave the active filter or fullscreen media view, then clear pane focus. For a local run, press `esc` again with no pane focused to return to workspace view.

### SYMON

SYMON watches local CPU, memory, disk, network, and accelerator metrics. It uses the same chart engine as run-backed system metrics panes but is not tied to a W\&B run file.

![W\&B LEET system metrics view with GPU charts and bucketed heatmap mode.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/leet-system-metrics-heatmap.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=659c5bacf9a7ac474a07d35d4d43f249)

The header shows the hostname, uptime, and load average. The first page of charts has CPU utilization, memory, swap, network and disk throughput in bytes per second, CPU temperature, and GPU utilization, memory, temperature, and power. The remaining charts follow in title order. SYMON charts the utilization of every CPU core and, on Linux, the CPU temperature and swap usage.

The sidebar describes the machine: its chip or CPU model, core counts, memory, and GPUs. Below that, live meters show CPU, memory, swap, and disk usage and each GPU's utilization, temperature, memory, and power, followed by network and disk throughput and, where the host reports it, system power. The sidebar then lists the processes using the most CPU. Press `t` to sort them by memory instead, `f` to filter them by name or PID, and `ctrl+f` to clear the filter. `tab` and `shift+tab` move focus between the process list and the charts. Press `[` to hide or show the sidebar, drag its border to resize it, and press `0` to restore the default width. LEET saves the sidebar's visibility and width between sessions.

### Record inspector

Use the record inspector to examine the raw records in a local `.wandb` transaction log. In single-run view, press `i` to open it for the current run. You can also launch it directly:

```sh theme={"system"}
wandb leet inspect
wandb leet inspect ./wandb
wandb leet inspect ./wandb/offline-run-20260403_145048-6ao9fhns/run-6ao9fhns.wandb
```

The optional path accepts a `.wandb` file, a run directory, or a workspace directory. With no path or a workspace directory, LEET opens the latest run.

The record list shows record types and summaries alongside the selected record's full text. Press `/` to filter by type or summary, `tab` to switch between regex and glob modes while editing, and `ctrl+/` to clear the filter. With the record list focused, press `end` to follow new records from a live run. If you opened the inspector with `i`, press `esc` from the record list to return to the run.

To check on a run from a script or a coding agent, print a summary instead of opening the inspector:

```sh theme={"system"}
wandb leet inspect --summary
wandb leet inspect --summary --json
```

The summary lists the run's name and ID, project, state, start time, and last step, the latest summary and config values, and the last 20 console lines. With `--json`, it's one JSON object.

When stdout is piped or redirected, or with `--json`, the command prints the records instead: as Protocol Buffer text, or as one JSON object per line with the record number, type, and decoded payload. `--follow` keeps printing records as a running run writes them and exits when the run finishes or after 10 minutes without a write. Set `--idle-timeout` to change the wait, for example `--idle-timeout 30s`, or `0` to wait forever:

```sh theme={"system"}
wandb leet inspect | less
wandb leet inspect --json | grep '"type":"history"' | tail -n 5
wandb leet inspect --follow --json
```

## Key features

### Multi-run comparison

Select multiple runs in workspace view to compare scalar metrics on shared charts. Each run gets a stable color, and LEET reduces base color collisions so overlaid series stay distinguishable. Pinning is useful when many runs are selected and you want one series to render above the rest.

Press `f` to filter the runs list by name, project, tags, notes, config values, and other metadata. Bare terms search across run key, display name, run ID, project, tags, and notes. The filter also supports fielded queries:

| Query | Matches |
| - | - |
| `project:vision` | Project name. |
| `name:baseline` | Display name. Aliases: `run_name`, `display`, `display_name`. |
| `id:abc123` | Run ID. Alias: `run_id`. |
| `key:offline-run` | Run directory key. Aliases: `run_key`, `path`. |
| `tag:prod` | Tags. Alias: `tags`. |
| `note:debug` | Notes. Alias: `notes`. |
| `config:adamw` or `cfg:adamw` | Any flattened config key or value. |
| `cfg.lr>=1e-3` | A specific nested config path. `config.lr` also works. |
| `has:notes` or `exists:cfg.dataset` | Existence check. |

Supported operators are `:`, `=`, `!=`, `>`, `>=`, `<`, and `<=`. Numeric comparisons are useful for config values such as learning rate, batch size, or number of layers.

Use whitespace or `AND` for conjunction, `OR` or `|` for alternatives, and `-`, `!`, or `NOT` for negation. Use quotes for phrases with spaces.

```text theme={"system"}
transformer
project:vision tag:baseline
cfg.lr>=1e-3 cfg.optimizer=adamw
has:notes -tag:debug
project:vision tag:baseline cfg.lr>=1e-3 -note:debug | project:nlp
```

While editing a filter, press `tab` to switch between regex and glob modes. Regex mode behaves like a case-insensitive substring search unless the query contains regex metacharacters. Glob mode supports `*` for any sequence and `?` for any single character.

LEET saves run, metric, and system metric filters, including their match modes, and the selected and pinned runs in `.wandb-leet.json` inside each local `wandb/` directory. It restores them when you reopen that directory in workspace or single-run view. Clearing a filter also clears its saved value. Console log and run overview filters aren't saved between sessions.

### Metrics and system metrics

LEET renders scalar metrics as terminal line charts. Filter run metrics with `/` and system metrics with `\`. When the console logs pane has focus, `/` filters logs instead. Press `y` on a focused chart to cycle modes such as log-scale Y or bucketed heatmap views for percentage-based system metrics. The `CPU Core (%)` chart, which has one series per core, opens as a heatmap with one row per core. Press `y` to switch it to lines.

Press `g` to cycle chart guides between off, a dotted background, and horizontal lines aligned with Y-axis ticks. This setting applies across workspace, single-run, and SYMON views and is saved between sessions.

By default, LEET plots each metric against Weights & Biases' internal step metric (`_step`). For local runs, a custom X-axis defined with `run.define_metric()` takes precedence, including definitions that use glob patterns. For example, this run plots `train/loss` against `train/step`:

```python theme={"system"}
import wandb

with wandb.init(project="leet-example", mode="offline") as run:
    run.define_metric("train/*", step_metric="train/step")
    for step in range(10):
        run.log({"train/step": step * 100, "train/loss": 1 / (step + 1)})
```

The chart header and status bar show `[x: train/step]`. Rows without a finite value for the custom X-axis are omitted. Each chart uses one X-axis, so compare runs with the same axis definition. A custom axis replaces the default step axis, and series using a different axis aren't plotted on that chart.

Use the mouse wheel to zoom the focused chart. On live system metric charts, LEET defaults to a rolling tail window (10 minutes by default). Right-click and drag on a chart to inspect the nearest point. Hold `alt` while dragging to inspect visible charts in the same grid at the same X position. Metric charts synchronize only when they share the same X-axis.

### Media and console logs

The media pane shows `wandb.Image` series, including lists of images logged under one key, with one tile per image. Toggle it with `3` in workspace or single-run view.

With the media pane focused, use `w`, `a`, `s`, and `d` to select tiles. The left and right arrows move one frame, and the up and down arrows move 10 frames. Press `enter` for fullscreen media and `esc` to leave it. Press `l` to link scrubbing across image series so the arrows, `home`, and `end` move a shared cursor along their combined step timeline.

Press `k` to switch between ANSI thumbnails and high-resolution rendering in terminals that support the Kitty graphics protocol. LEET falls back to ANSI when the terminal doesn't support high-resolution rendering. Image padding uses the terminal background.

![W\&B LEET workspace view with the media pane showing several image series.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/leet-media-workspace.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cbc2915448158e2da6ec1c581460d427)

Toggle console logs with `4`. LEET rebuilds readable log lines from raw terminal output, including ANSI escape codes and carriage-return progress lines.

To filter console output, focus the logs pane, press `/`, and type a pattern. Press `tab` while editing to switch between regex and glob matching. Press `enter` to apply the filter or `esc` to discard the draft query. LEET displays matching lines and follows new matches when you're at the end of the log. With the logs pane focused, press `ctrl+/` or `ctrl+l` to clear the filter.

In single-run view, with the logs pane focused, press `l` to link the console logs to the charts. The charts show a crosshair at the time the selected line was logged: system metric charts at that time, and metric charts at the history step logged nearest to it. Inspecting a chart with the mouse selects the console line logged nearest to the inspected point. Metric charts with a custom X-axis aren't linked. Press `l` again to unlink.

For console log behavior in the W\&B App, see [Console logs](https://docs.coreweave.com/products/wandb/app/console-logs.md).

### Configuration

Persist layout, colors, default panes, and startup mode with the config editor:

```sh theme={"system"}
wandb leet config
```

LEET writes `wandb-leet.json` under `~/.config/wandb/` by default, or under `WANDB_CONFIG_DIR` when that variable is set. You can also resize grids from inside LEET with `c` and `r`.

Drag pane borders and separator lines to resize sidebars, stacked panes, and the Environment, Config, and Summary sections of the run overview. The active border is highlighted while you drag. LEET saves the proportions separately for workspace, single-run, and inspector views. Press `0` to reset sizes for the current view, including the run overview sections.

In the config editor, the field list scrolls with your selection to fit short terminals. Press `space` to toggle a boolean setting.

![W\&B LEET config editor showing grid settings, color schemes, visibility settings, and palette selection.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/leet-config-editor.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=2a5f5c7dca4f23fc723b4e19db574ea6)

### Common config keys

| Key | Default | Description |
| - | - | - |
| `startup_mode` | `workspace_latest` | Initial view when launched without a run path. |
| `chart_guides` | `off` | Line chart guides: `off`, `dots`, or `horizontal`. Cycle with `g`. |
| `metrics_grid.rows`, `metrics_grid.cols` | `4`, `3` | Single-run metrics grid size. |
| `system_grid.rows`, `system_grid.cols` | `6`, `2` | Single-run system metrics sidebar grid size. |
| `media_grid.rows`, `media_grid.cols` | `1`, `2` | Single-run media grid size. |
| `workspace_metrics_grid.rows`, `workspace_metrics_grid.cols` | `3`, `3` | Workspace metrics grid size. |
| `workspace_system_grid.rows`, `workspace_system_grid.cols` | `3`, `3` | Workspace system metrics grid size. |
| `workspace_media_grid.rows`, `workspace_media_grid.cols` | `1`, `2` | Workspace media grid size. |
| `symon_grid.rows`, `symon_grid.cols` | `3`, `3` | SYMON grid size. |
| `symon_sidebar_visible` | `true` | Show the SYMON sidebar by default. Toggle with `[`. |
| `color_scheme` | `wandb-vibe-10` | Palette for workspace run metrics and run list colors. |
| `per_plot_color_scheme` | `sunset-glow` | Palette for single-run charts when `single_run_color_mode` is `per_plot`. |
| `tag_color_scheme` | `wandb-vibe-10` | Palette for tag badges in the overview sidebar. |
| `system_color_scheme` | `wandb-vibe-10` | Palette for system metric charts. |
| `french_fries_color_scheme` | `viridis` | Palette for bucketed heatmap charts. |
| `single_run_color_mode` | `per_series` | Color single-run charts per series or per plot. |
| `system_color_mode` | `per_series` | Color system charts per series or per plot. |
| `system_tail_window_minutes` | `10` | Default live tail window for system charts. |
| `heartbeat_interval_seconds` | `15` | Polling heartbeat for live runs. |
| `workspace_overview_visible` | `true` | Show the workspace run overview sidebar by default. |
| `workspace_metrics_grid_visible` | `true` | Show the workspace metrics grid by default. |
| `workspace_system_metrics_visible` | `false` | Show the workspace system metrics pane by default. |
| `workspace_console_logs_visible` | `false` | Show the workspace console logs pane by default. |
| `workspace_media_visible` | `false` | Show the workspace media pane by default. |
| `left_sidebar_visible` | `true` | Show the single-run overview sidebar by default. |
| `right_sidebar_visible` | `true` | Show the single-run system metrics sidebar by default. |
| `metrics_grid_visible` | `true` | Show the single-run metrics grid by default. |
| `console_logs_visible` | `false` | Show the single-run console logs pane by default. |
| `media_visible` | `false` | Show the single-run media pane by default. |

Several color schemes are available, like `wandb-vibe-10`, `wandb-vibe-20`, `sunset-glow`, `blush-tide`, `gilded-lagoon`, `bootstrap-vibe`, `dusk-shore`, `clear-signal`, `traffic-light`, `viridis`, `plasma`, `inferno`, `magma`, and `cividis`.

* Palettes `dusk-shore` and `clear-signal` are colorblind-friendly.
* Sequential palettes such as `viridis`, `plasma`, `inferno`, `magma`, `cividis`, and `traffic-light` work well for bucketed heatmaps.

### Diagnostics and telemetry

LEET prints startup failures to stderr. To collect debug logs, launch it with `WANDB_DEBUG=true`:

```sh theme={"system"}
WANDB_DEBUG=true wandb leet
```

Debug output is written to `wandb-leet.debug.log` beside the global `wandb-leet.json` config file. LEET doesn't send usage telemetry when `WANDB_MODE=offline`, `WANDB_MODE=disabled`, or `WANDB_ERROR_REPORTING=false`.

## Navigate with the keyboard

LEET is designed for keyboard and mouse input. Press `h` or `?` inside LEET to open the in-app help overlay for the current view.

Across workspace and single-run views:

* `tab` and `shift+tab` cycle focus between visible panes.
* `w`, `a`, `s`, `d` and the arrow keys move within the focused pane (except in the media pane, where arrows scrub the X-axis and WASD moves between tiles).
* `home`, `end`, `pgup`, and `pgdown` jump within lists, chart pages, or media frames.
* `1`, `2`, `3`, and `4` toggle the metrics grid, system metrics, media, and console logs panes.
* `[` and `]` toggle sidebars (runs list, run overview, or system metrics depending on the view).

For the full shortcut tables for workspace, single-run, SYMON, media, record inspector, and mouse actions, see [Keyboard shortcuts](https://docs.coreweave.com/products/wandb/app/keyboard-shortcuts.md) (LEET tab).

## Limitations compared to the W\&B App

LEET complements the W\&B App but does not replicate every workspace capability.

| Capability | LEET | W\&B App |
| - | - | - |
| Data source | Local `wandb/` directories and `.wandb` files, or a remote run's scalar history and summary by URL | Synced cloud projects and teams |
| Run comparison | Multiple local runs in one directory | Full workspace tables, grouping, and saved views |
| Panel types | Scalar line charts, system metrics, `wandb.Image` media, console logs | Line, bar, scatter, parallel coordinates, media, code, query panels, custom charts, and more |
| Collaboration | Single-user terminal session | Sharing, comments, reports, and team features |
| Artifacts and files | Not available | Artifacts, Files, and Code tabs per run |
| Sweeps and registry | Not available | Sweep dashboards, registry, and automations |

If you need artifacts, sweep analysis, or panel types that LEET does not provide, open the run in the [W\&B App](https://docs.coreweave.com/products/wandb/runs/view-logged-runs.md) after syncing.

## Changelog

LEET was initially launched in beta in SDK v0.23.0, and graduated to GA in SDK v0.28.0. For details, refer to the [SDK release notes](https://docs.coreweave.com/release-notes/sdk-releases.md).

## Related resources

* [View a specific run](https://docs.coreweave.com/products/wandb/runs/view-logged-runs.md) in the W\&B App or LEET.
* [Keyboard shortcuts](https://docs.coreweave.com/products/wandb/app/keyboard-shortcuts.md) for the W\&B App and LEET.
* [`wandb leet`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-leet) command reference.
* [SDK release notes](https://docs.coreweave.com/release-notes/sdk-releases.md), including LEET changes.
