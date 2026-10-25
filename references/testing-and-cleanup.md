# Real testing and reversible cleanup

Follow the CURRENT https://flatpark.org/docs/reviewers/testing-playbook/ . For cleanup use https://flatpark.org/docs/packagers/cleanup/ . Official FlatPark requires actual live usage, not just a successful build.

## Pre-launch guard

- Identify installed refs (`flatpak list --user --app`, `flatpak list --system --app`), per-user existing remotes, and `~/.var/app/<id>`; never touch earlier user data without asking.
- Examine existing global user overrides (e.g. `~/.local/share/flatpak/overrides/global`) and target app overrides; they can fake required permissions during testing.
- Record home listing and relevant autostart/application desktop files **before** starting.
- If using Xwayland/private display, know which display belongs to this run; don't kill another session's display. Don't assume a virtual display supports every portal. Clear problematic inherited variables (notably Electron flags) only for the test process.

## Required checks — capture a short evidence result for each

| Check | Required evidence |
| --- | --- |
| Unpack as system install | Actual FlatPark `check-apply-extra.sh` when compatible. Otherwise mark *not run*; per-user install is insufficient proof. |
| User install from local repo | Actual pinned download hash/size and successful install-time `apply_extra`; check no accidental native execution. |
| Startup/render | App starts and shows real usable GUI (not blank/transparent); mention Wayland and/or X11. |
| Persistence | Change a setting/data, quit, kill, reopen; still present. For brand-new package, test initial creation without writing over older profiles. |
| Host cleanliness | Diff home, autostart and local desktop entries; no unintended host pollution. |
| Window class | Compare actual WM class/App ID with `.desktop` StartupWMClass; test launch behavior. |
| D-Bus and special UI | Tray, MPRIS, single-instance/second launch and Secret Service if relevant. |
| Core function | Do what the app is for: open/save, playback, connect, screenshot etc. If login/hardware missing, explicitly mark untested. |
| Permissions | Ensure manifest grants only needed capabilities and global overrides didn't mask missing rights. |
| Update behavior | For an update, verify current pin/resolver/size/checksum, reinstall and check persistent data migration. |

Do NOT fake screenshots, keyboard interactions, D-Bus registrations, manual app usage, or `sudo`-mode root tests. If no graphical session is available, report partial validation and ask for a user-led GUI test.

## During test

- Track test app PID/name, test remote, local repo path, build directory, screenshots, downloaded artifacts, created files and potential secrets.
- After using an instance, terminate **that exact instance** (`flatpak kill <id>`), not `pkill -f` and not wildcard process termination.
- Account-based tests can leave credentials in the host Secret Service; ask before using a real account and preserve existing entries.

## Cleanup policy

Inventory with **read-only** commands. Remove only what this specific task created, once the user approves. Never delete old `~/.var/app/<id>`, reset another application's permissions, remove pre-existing user remotes, delete all unused runtimes, nuke build caches or delete other worktrees. Never `rm -rf` dynamically assembled paths based on guessed IDs.

Include three cleanup report categories: **removed**, **kept intentionally**, **not ours / pre-existing**. When a test-only app is uninstalled (with approval), do not use `--delete-data` unless the user explicitly says the profile was created solely for the test and may be deleted.
