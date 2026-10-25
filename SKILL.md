---
name: flatpark-packaging
description: Package upstream Linux binaries as personal-use Flatpaks using FlatPark's official extra-data Packaging Playbook; optionally prepare a FlatPark submission on explicit request. Use for .deb, .rpm, tarballs, zip, AppImage, manifests, app updates, sandbox permissions, local Flatpak tests, and FlatPark registry packaging. Default to private/local mode; never publish or alter existing app data without approval.
---

# FlatPark-style Flatpak packaging (Codex skill)

Use the **current official FlatPark Packaging Playbook**, not remembered rules. Start by reading `references/official-docs.md` and the relevant pages linked there. FlatPark's individual topic pages take precedence over its top-level playbook when they differ. If offline, use the accompanying references conservatively, disclose that official rules could not be refreshed, and do not guess at unstable specifics (runtime versions, CLI flags, checksum, upstream assets, stacks).

This skill is an **independent community adaptation**, not an official FlatPark product. It deliberately adds **personal/local packaging**; that mode is not a FlatPark catalog submission, not necessarily catalog-compliant, and not automatically maintained by FlatPark CI.

## Operating contract

- **Default mode: `personal`.** Build/install/test locally for the user, even where catalog listing rules would exclude the application. Do not contact upstream, open an issue or PR, push, publish, redistribute, create public remotes, or claim FlatPark affiliation.
- Only enter **`submission`** mode after the user expressly requests packaging **for submission to FlatPark**. Read `references/submission-mode.md`; apply *all* current FlatPark listing/review rules. Treat opening a PR and contacting upstream as separate actions, each needing specific approval after showing the exact draft.
- Do not silently switch away from FlatPark's **vendor-binary `extra-data`** model. If the source is only local, login-gated, no longer publicly downloadable, or technically unsuitable for extra-data, explain why and **ask** whether the user wants a private `type: file`/embedded-payload alternative (not FlatPark-equivalent). Never redistribute a proprietary payload without confirmed authorization.
- Work only in the user-specified directory. If absent, create a dedicated package work folder only after finding a sensible safe location within the current project; never rearrange an existing repository. Inspect `AGENTS.md` and other local instructions if working inside a repository.
- Prefer read-only reconnaissance. Do not invoke destructive cleanup, install to system-wide Flatpak, change system permissions, add broad filesystem grants, download from unofficial mirrors, or run untrusted installers without a specific reason and permission.
- **Ask rather than improvise** for a material unresolved choice: unverified source or license, competing download formats with meaningful tradeoffs, architecture/runtime incompatibility, ID collision, extra permissions, missing testing prerequisites, unexpected home-profile data, extra workaround(s), security/sandbox bypass, cleanup touching existing files, or publication. Ask one focused question with observed evidence, your recommended options, and the consequence. Stop at the affected step; continue independent safe work if possible.
- Do not claim checks were performed when they were not. A build or successful static lint **does not mean** the application works.

## Step-by-step workflow

### 0. Scope, inventory and plan

1. Identify app name, official upstream/homepage, desired version, platform/arch (`uname -m`), desired target, and existing Flatpak IDs/remotes. Only ask for critical details that cannot be inferred reliably. `personal` is assumed unless submission was expressly requested.
2. Before making a manifest, inspect project docs and the official Playbook (link map in `references/official-docs.md`). Use `python3 scripts/preflight.py` (path relative to this skill) for a **read-only** prerequisite report when helpful.
3. Explain intended mode, source artifact, runtime, app ID, permissions, profile collision status, and testing approach. Mark anything not yet verified.
4. Maintain a run-specific inventory of created files, downloads, worktrees, remotes, Flatpak installations, settings, screenshots and processes so cleanup can be selective.

### 1. Find and vet the upstream artifact

1. Confirm **official provenance**, stable public direct download, version, Linux architecture, payload type, checksum and **byte size**. Prefer direct vendor releases. Never invent a URL, SHA-256, size, tag, license, or release metadata. Download only when required and approved by local environment policy. Optionally use `python3 scripts/verify_artifact.py ARTIFACT --sha256 HEX --size BYTES` to confirm an actual local download.
2. Read any provided license/terms for the intended *personal download and use*. Check sandbox feasibility. Record which FlatPark catalog rules do not apply in personal mode (such as prior Flathub publication), and which technical restrictions still apply (Linux ABI, portals, capabilities).
3. Prefer portable tar/zip, then `.deb`/`.rpm`, then AppImage **unless inspection gives a better reason** (Qt AppImage exception). Check upstream `Depends`, maintainer scripts, installed layout, `readelf -d`, architecture, and format-specific packaging pages in `references/format-and-package.md`.
4. Identify the app ID. First inspect the app's real metadata and any existing Flatpak installation. **Ask before reusing an ID** whose `~/.var/app/<id>` or installed ref contains real user data. Do not invent domain ownership or copy another vendor's ID uncritically.

### 2. Prepare package files — vendor binary stays extra-data

For a FlatPark-style package, create the package directory with:

```
<app-id>/
  flatpark.yml                # FlatPark-specific descriptor; optional in purely local build
  <app-id>.yml               # Flatpak Builder manifest
  apply_extra.sh             # install-time offline unpack into /app/extra
  <command>-wrapper          # launch official binary from stable /app/extra path
  <app-id>.desktop
  <app-id>.metainfo.xml
  <app-id>.png or <app-id>.svg
  resolve-update.sh          # release resolver, if upstream update API supports it
```

- Check current runtime and SDK versions from the *current catalog* and the payload's library requirements, not from stale examples. Match runtime/SDK, architecture and any Electron BaseApp. If unsure, **ask** before selecting an older runtime merely to make it build.
- Use manifest `type: extra-data` sources with an **actual vendor URL, SHA-256, size, filename, arch constraint**; install `/app/bin/apply_extra` (exact path) and export the wrapper, icon, desktop and metainfo **at build time**. AppStream version must correspond to the pinned download; do not invent app metadata or state an upstream endorsement.
- If compatible with the FlatPark updater, keep its `# BEGIN MANAGED EXTRA-DATA` / `# END MANAGED EXTRA-DATA` source block for the *upstream app artifact*. Put pinned fixed support downloads **outside** that managed region. Never edit a managed block in a way that the updater would silently discard. Inspect real registry examples from upstream before copying details.
- `apply_extra.sh` must be safe offline, execute in `/app/extra`, check input and expected executable, unpack without restoring archive ownership (`bsdtar --no-same-owner`), use a stable output directory, and fail clearly on unexpected layouts. A **system** install cannot use `/app/bin` helpers in `apply_extra`; AppImage extraction tools must be available through extra-data rather than `/app/bin`.
- Wrapper should only set necessary environment/flags and `exec` the vendor binary. Disclose any shim, preloading, copied configuration, binary patch or sandbox change. Never quietly disable a vendor's sandbox or updater.
- **Least privilege**: justify each `finish-args` group. Prefer portals, targeted dirs, and per-user opt-in `flatpak override` for optional access; broad `home`/`host`, `--device=all`, system-bus access, host-spawn and bypassing nested sandboxes require explicit user approval, with alternatives and risk explanation.
- `resolve-update.sh`, when meaningful, must return JSON only on stdout with `version`, optional release date, and per-arch source URL/filename (not made-up checksums). **Personal mode has no FlatPark scheduled resolver/auto publishing.** Document manual rebuild/re-pin steps and never imply normal `flatpak update` fetches a new upstream artifact unless the local repo was refreshed.

Read `references/format-and-package.md` and `references/permissions-and-safety.md` for the detailed traps and links. Do not use a generic executable, runtime pin, icon, or updater template without checking the actual upstream package.

### 3. Build and install from a local repo

- **Submission in an actual `flatpark/flatpark` checkout**: use *current upstream scripts* per `references/submission-mode.md`, including descriptor checks, `check-apply-extra.sh`, and `publish.sh --verify`; never assume a registry script exists in a standalone personal project.
- **Personal standalone**: use the upstream Flatpak Builder CLI to export the selected manifest to a **dedicated, app-specific local repo** and install a **per-user** test ref. See `references/local-mode.md` for commands. Never use a generic remote name that might collide; inspect user remotes first. If a signed repo is needed for distribution, that is a separate discussion.
- Confirm extra-data was actually downloaded and unpacked on **install**. Check source hashes and byte sizes; a successful builder run alone does not exercise the install-time download/unpack path.
- Where available, use FlatPark's `./scripts/check-apply-extra.sh <id>` inside its repository to reproduce system-style extraction (root without capabilities, offline). A user install **cannot substitute** for that check. When not available, explicitly mark the system-install simulation **not run**, do not fake it or elevate privileges without permission.

### 4. Run the whole testing playbook

Read `references/testing-and-cleanup.md` and the current official Testing Playbook. Test the local **Flatpak**, not the native host binary. At minimum: real unpack/install; launch and visible rendering; one genuine core feature; app data survives quit/restart; check host home / autostart pollution; correct desktop window class; relevant tray, MPRIS, and second-launch D-Bus behavior. Inspect global overrides so leaked host permissions don't mask missing manifest permissions. Test the relevant Wayland/X11 path.

**Critical profile guard:** before first run, inspect the existing app ref and `~/.var/app/<id>`. If user data exists, stop and ask for an isolated profile/test ID strategy; never remove, overwrite, or `--delete-data` it. A private display also needs consent/appropriate setup; if unavailable, report limitations.

After each run, `flatpak kill <id>` if that is the tested instance. Never auto-delete the user's home folder, portal permissions, remotes, overrides or shared builder cache. Keep track of what this particular run created.

### 5. Report, maintain or submit

- Report outputs with an evidence table: checks PASS / FAIL / NOT TESTED and reasons; resulting manifest and command paths; source URL/version/hash/size; chosen runtime/arch; permissions; divergences from FlatPark; update policy; exactly what exists locally and how to install it.
- If `personal`, stop after local artifact and testing. **No PR, contacting upstream, or publication.** If maintenance requested, re-resolve upstream, re-pin checksum and size, rebuild and re-test before updating the local repo.
- If `submission`, follow all 8 top-level playbook stages (candidate, eligibility, package, test, PR, tell upstream, handle response, ongoing updates). Present drafted PR or upstream message for separate explicit approval; follow delisting/no-contact requests. See `references/submission-mode.md`.
- Clean up **only created test resources** once approved, or report what remains. Never do blanket `flatpak uninstall --unused`, `flatpak permission-reset`, `rm -rf ~/.var/app/<id>`, or `git clean` as a shortcut.

## Definition of done

A **working personal package** is built, installed from the intended local repo, actually launched, its main feature and persistence tested, and results reported. If any step cannot be performed, label the result **partial / unverified** and ask for the smallest missing permission, equipment, account or decision. A **submission-ready package** additionally meets the current FlatPark catalog and review requirements; a PR is **not opened without approval**.
