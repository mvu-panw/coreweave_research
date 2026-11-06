# Keyboard shortcuts

Source: https://docs.coreweave.com/products/wandb/app/keyboard-shortcuts

> Learn about the keyboard shortcuts available in Weights & Biases.

# Keyboard shortcuts

Weights & Biases supports keyboard shortcuts to help you navigate and interact with experiments, workspaces, and data more efficiently. This guide covers keyboard shortcuts for the W\&B App and the W\&B LEET (Lightweight Experiment Exploration Tool) terminal UI.

> [tab] App
>
> The W\&B App includes a keyboard shortcuts drawer that lists all available shortcuts for the current context. Open it with **Cmd+/** (macOS) or **Ctrl+/** (Windows/Linux), or select **Keyboard shortcuts** from the **?** (help) menu in the top navigation. Use the search field in the drawer to filter shortcuts by name.
>
> The **Workspace** and **Media browser modal** sections are context-sensitive, appearing only when the corresponding area is active.
>
> ## Essentials
>
> | Shortcut | Description |
> | - | - |
> | **Cmd+/** (macOS) / **Ctrl+/** (Windows/Linux) | Open the keyboard shortcuts drawer. |
> | **Cmd+K** (macOS) / **Ctrl+K** (Windows/Linux) | Open the global search dialog. |
> | **Alt+M** | Toggle between light and dark app theme. |
>
> ## Workspace
>
> | Shortcut | Description |
> | - | - |
> | **Cmd+Z** (macOS) / **Ctrl+Z** (Windows/Linux) | Undo the most recent workspace action. |
> | **Cmd+Shift+Z** (macOS) / **Ctrl+Shift+Z** (Windows/Linux) | Redo the most recently undone workspace action. |
> | **Cmd+S** (macOS) / **Ctrl+S** (Windows/Linux) | Save the current workspace. |
> | **Cmd+J** (macOS) / **Ctrl+J** (Windows/Linux) | Expand or collapse the runs sidebar. |
> | **Cmd+.** (macOS) / **Ctrl+.** (Windows/Linux) | Toggle the minimized run selector. |
> | **Alt+V** | Show only runs currently visualized in panels. |
>
> ## Media browser modal
>
> These shortcuts are available when viewing media in the fullscreen modal.
>
> | Shortcut | Description |
> | - | - |
> | **Cmd++** (macOS) / **Ctrl++** (Windows/Linux) | Zoom in. |
> | **Cmd+-** (macOS) / **Ctrl+-** (Windows/Linux) | Zoom out. |
> | **Cmd+0** (macOS) / **Ctrl+0** (Windows/Linux) | Reset zoom to 100%. |
> | **Shift+1** | Zoom to fit the viewport. |

> [tab] LEET
>
> These keyboard shortcuts work in the W\&B LEET (Lightweight Experiment Exploration Tool) terminal UI. To launch LEET, run `wandb leet` in your terminal.
>
> Press `h` or `?` inside LEET to open the in-app help overlay for the current view. For a product overview and launch paths, see [LEET terminal UI](https://docs.coreweave.com/products/wandb/app/leet-tui.md).
>
> ### Workspace
>
> | Key | Action |
> | - | - |
> | `h`, `?` | Toggle help. |
> | `q`, `ctrl+c` | Quit. |
> | `alt+r` | Restart LEET. |
> | `esc` | Leave the active filter or fullscreen media, then focus the runs list (or clear focus if it's hidden). |
> | `enter` | Open the highlighted run in single-run view when the runs list is focused. |
> | `1` | Toggle metrics grid. |
> | `[` | Toggle runs sidebar. |
> | `2` | Toggle system metrics pane. |
> | `]` | Toggle run overview sidebar. |
> | `3` | Toggle media pane. |
> | `4` | Toggle console logs pane. |
> | `0` | Reset pane and overview section sizes for this view. |
> | `f` | Filter runs by name or metadata. |
> | `ctrl+f` | Clear runs filter. |
> | `space` | Select or deselect run. |
> | `p` | Pin or unpin run. |
> | `ctrl+a` | Select all runs matching the runs filter. Press `y` to confirm or `esc` to cancel. |
> | `x` | Deselect all runs except the pinned one. |
> | `/` | Filter metrics, or console logs when the logs pane is focused. |
> | `\` | Filter system metrics. |
> | `ctrl+/`, `ctrl+l` | Clear metrics filter, or console filter when the logs pane is focused. |
> | `ctrl+\` | Clear system metrics filter. |
> | `o` | Filter run overview items. |
> | `ctrl+o` | Clear overview filter. |
> | `y` | Cycle focused chart mode. |
> | `g` | Cycle chart guides: off, dots, horizontal. |
> | `c` | Set columns for focused grid. |
> | `r` | Set rows for focused grid. |
> | `tab`, `shift+tab` | Cycle focus across visible panes. |
> | `w`, `a`, `s`, `d` or arrow keys | Move within the focused pane. In media, arrows scrub frames and WASD selects tiles. |
> | `N`, `pgup` | Previous page. |
> | `n`, `pgdown` | Next page. |
> | `home` | Jump to first item, first page, or first media frame. |
> | `end` | Jump to last item, last page, or latest media frame. |
>
> ### Single-run
>
> | Key | Action |
> | - | - |
> | `h`, `?` | Toggle help. |
> | `q`, `ctrl+c` | Quit. |
> | `alt+r` | Restart LEET. |
> | `esc` | Leave the active filter or fullscreen media, then clear pane focus, then return to the local workspace. |
> | `i` | Open the record inspector for the current local run. |
> | `1` | Toggle metrics grid. |
> | `[` | Toggle run overview sidebar. |
> | `]`, `2` | Toggle system metrics sidebar. |
> | `3` | Toggle media pane. |
> | `4` | Toggle console logs pane. |
> | `0` | Reset pane and overview section sizes for this view. |
> | `/` | Filter metrics, or console logs when the logs pane is focused. |
> | `\` | Filter system metrics. |
> | `ctrl+/`, `ctrl+l` | Clear metrics filter, or console filter when the logs pane is focused. |
> | `ctrl+\` | Clear system metrics filter. |
> | `l` | Link or unlink the console logs and the charts when the logs pane is focused. |
> | `o` | Filter run overview items. |
> | `ctrl+o` | Clear overview filter. |
> | `y` | Cycle focused chart mode. |
> | `g` | Cycle chart guides: off, dots, horizontal. |
> | `c` | Set columns for focused grid. |
> | `r` | Set rows for focused grid. |
> | `tab`, `shift+tab` | Cycle focus across visible panes. |
> | `w`, `a`, `s`, `d` or arrow keys | Move within the focused pane. In media, arrows scrub frames and WASD selects tiles. |
> | `N`, `pgup` | Previous page. |
> | `n`, `pgdown` | Next page. |
> | `home` | Jump to first item, first page, or first media frame. |
> | `end` | Jump to last item, last page, or latest media frame. |
>
> ### SYMON
>
> | Key | Action |
> | - | - |
> | `h`, `?` | Toggle help. |
> | `q`, `ctrl+c` | Quit. |
> | `alt+r` | Restart. |
> | `[` | Toggle the sidebar. |
> | `0` | Reset the sidebar width. |
> | `t` | Sort the processes by CPU or by memory. |
> | `f` | Filter the processes by name or PID. |
> | `ctrl+f` | Clear the processes filter. |
> | `tab`, `shift+tab` | Switch focus between the process list and the charts. |
> | `y` | Cycle focused chart mode. |
> | `g` | Cycle chart guides: off, dots, horizontal. |
> | `\` | Filter system metrics. |
> | `ctrl+\` | Clear system metrics filter. |
> | `c`, `C` | Set grid columns. |
> | `r`, `R` | Set grid rows. |
> | `w`, `a`, `s`, `d` or arrow keys | Move chart focus, or the process cursor when the list has focus. |
> | `N`, `pgup` | Previous page of charts or processes. |
> | `n`, `pgdown` | Next page of charts or processes. |
> | `home` | First page. |
> | `end` | Last page. |
>
> ### Media
>
> These shortcuts apply when the media pane is focused in workspace or single-run view.
>
> | Key | Action |
> | - | - |
> | `w`, `a`, `s`, `d` | Select an image tile. |
> | Left arrow, right arrow | Scrub backward or forward one frame. |
> | Up arrow, down arrow | Scrub backward or forward 10 frames. |
> | `home`, `end` | First or latest frame. |
> | `N`, `pgup` / `n`, `pgdown` | Previous or next page of image series. |
> | `enter` | Toggle fullscreen for the selected image. |
> | `esc` | Leave fullscreen media. |
> | `l` | Toggle linked scrubbing across image series. |
> | `k` | Toggle ANSI and high-resolution rendering in terminals that support the Kitty graphics protocol. |
>
> ### Record inspector
>
> Open the inspector with `wandb leet inspect` or press `i` in single-run view for a local run.
>
> | Key | Action |
> | - | - |
> | `h`, `?` | Toggle help. |
> | `q`, `ctrl+c` | Quit LEET. |
> | `esc` | Leave filter editing, then focus the record list. From the list, return to the run if opened with `i`. |
> | `tab`, `shift+tab` | Switch focus between the record list and detail pane. |
> | `w`, `s`, up arrow, down arrow | Select a record or scroll the detail pane. |
> | `N`, `pgup` / `n`, `pgdown` | Previous or next page. |
> | `home` | First record or top of the detail pane. |
> | `end` | Last record or bottom of the detail pane. At the last record, follow live updates. |
> | `/` | Filter records by type or summary. |
> | `ctrl+/` | Clear the record filter. |
> | `0` | Reset inspector pane sizes. |
>
> ### Filter editing
>
> These shortcuts apply while a filter input is active.
>
> | Key | Action |
> | - | - |
> | `tab` | Switch between regex and glob matching. |
> | `enter` | Apply the filter and leave editing. |
> | `esc` | Discard the draft query and leave editing. |
>
> ### Mouse
>
> | Input | Action |
> | - | - |
> | Click | Focus a chart or select a media tile. |
> | Left-click and drag a border or separator | Resize panes, sidebars, or run overview sections. |
> | Wheel | Zoom the focused chart. |
> | Right-click and drag | Inspect the nearest point on a chart. With console logs linked, also select the nearest console line. |
> | `alt` plus right-click and drag | Inspect visible charts in the same grid in sync. Metric charts must share an X-axis. |
> | `shift` plus drag | Select terminal text. |
