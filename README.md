# flatpark-packaging — Codex Skill (Personal-Use First)

`flatpark-packaging` is an **independent, unofficial Codex Skill** based on FlatPark's official [Packaging Playbook](https://flatpark.org/docs/packagers/playbook/). It helps package upstream Linux application binaries as Flatpaks using FlatPark's `extra-data` approach.

The default mode is **personal use**: build, install, and test a Flatpak for yourself, even if the application is not eligible for listing in FlatPark. The skill **does not submit packages to FlatPark or Flathub, contact upstream developers, or publish anything** unless you explicitly request a separate submission workflow and approve the relevant actions.

> **Not affiliated with FlatPark.** This is a set of Codex instructions, references, and small verification tools—not a replacement for Flatpak Builder or FlatPark's own infrastructure.

## Installation

Extract the **entire** `flatpark-packaging/` folder into one of Codex's skill directories:

- **Global (all projects):** `~/.agents/skills/flatpark-packaging/`
- **Project-specific:** `<your-project>/.agents/skills/flatpark-packaging/`

If you downloaded the ZIP containing a top-level `flatpark-packaging/` folder, install it on Linux with:

```bash
mkdir -p ~/.agents/skills
unzip flatpark-packaging.zip -d ~/.agents/skills/
```

Start Codex and invoke the skill with **`$flatpark-packaging`**. If it is not discovered, restart Codex and verify that `SKILL.md` is located at `~/.agents/skills/flatpark-packaging/SKILL.md` (or the corresponding project path).

**Keep all files together.** The `SKILL.md` instructions reference supporting documents and Python utilities in this package. Copying `SKILL.md` alone is not sufficient.

## Example prompts

### Package an application for personal use

```text
$flatpark-packaging Package <official upstream release URL> as a Flatpak
for my own use.

Follow FlatPark's Packaging Playbook and prefer the vendor-binary
extra-data workflow. Do not submit to FlatPark or Flathub, contact
the upstream maintainers, or overwrite any existing Flatpak or app data.

First investigate the download source, license, dependencies,
runtime, app ID, and sandbox permissions. If something is uncertain,
ask me instead of guessing. Do not add risky permissions without my
approval.

After packaging, perform an actual installation, GUI launch, core
functionality test, and restart/persistence test. Clearly report
anything that could not be verified.
```

### Audit an existing package without modifying it

```text
$flatpark-packaging Review this local Flatpak manifest and
apply_extra.sh against FlatPark's Testing Playbook.
Do not modify files. Give me a prioritized list of findings first.
```

### Prepare a FlatPark submission (opt-in only)

```text
$flatpark-packaging I want to submit this application to FlatPark.
Check the latest eligibility rules and full Packaging Playbook.
Prepare a PR draft only; do not open the PR or contact upstream
without my separate approval.
```

## How it works

1. **Inspect before acting:** verify the official upstream download, version, architecture, checksum, byte size, license, existing app IDs, and local tooling.
2. **Plan the package:** select a compatible runtime and packaging format; review any necessary permissions before writing the manifest.
3. **Build using `extra-data`:** define a pinned vendor download and an offline `apply_extra.sh` to unpack it during Flatpak installation; provide a launcher, desktop entry, and AppStream metadata.
4. **Build and test locally:** use a dedicated local repository and a **per-user** test install. Verify install-time extraction, application launch, an actual feature, and settings/data persistence.
5. **Report and maintain:** document test evidence, limitations, permissions, update instructions, and any remaining local resources. Updates to personal packages require a new version pin, build, and test; FlatPark's scheduled publishing is **not** included.

For submissions, the skill additionally applies FlatPark's current catalog rules. That mode is **never enabled by default**.

## Safety and decision-making

The skill is explicitly designed to **ask rather than guess** when a material choice cannot be verified, including:

- Untrusted download sources, unclear licenses, or incompatible runtime/architecture choices.
- Conflicts with installed Flatpak IDs or existing data under `~/.var/app/<app-id>`.
- Broad filesystem/device access, sandbox bypasses, unexpected patches or workarounds.
- Use of a private/embedded binary instead of the FlatPark-style public `extra-data` workflow.
- System-wide installs, destructive cleanup, contacting upstream, or publishing a package.

It does **not** automatically remove app data, reset permissions, or replace an existing installation. A successful build alone does **not** count as a successful end-to-end package test. Unavailable tests must be marked **NOT TESTED**, not assumed to pass.

## Package contents

```text
flatpark-packaging/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── references/
│   ├── official-docs.md
│   ├── local-mode.md
│   ├── format-and-package.md
│   ├── permissions-and-safety.md
│   ├── testing-and-cleanup.md
│   └── submission-mode.md
├── scripts/
│   ├── preflight.py
│   └── verify_artifact.py
└── assets/
    └── report-template.md
```

- **`SKILL.md`** — the core instructions read by Codex (in English).
- **`references/official-docs.md`** — links to official FlatPark playbook sections and related documentation.
- **`references/local-mode.md`** — building a local repository, installing privately, and updating manually.
- **`references/format-and-package.md`** — handling tar/zip, DEB, RPM, AppImage, `extra-data`, and release updates.
- **`references/permissions-and-safety.md`** — least-privilege permissions, constraints, and when to ask the user.
- **`references/testing-and-cleanup.md`** — runtime verification, protecting existing user data, and safe cleanup.
- **`references/submission-mode.md`** — additional procedures used **only** for an explicitly requested FlatPark submission.
- **`scripts/preflight.py`** — read-only checks of local development tools.
- **`scripts/verify_artifact.py`** — verifies the SHA-256 checksum and exact byte size of a downloaded file.
- **`assets/report-template.md`** — template for build, security, and testing results.

## Requirements and limitations

You will need a **Linux environment** with the Flatpak toolchain, a real upstream release artifact, and ideally a working graphical desktop for launch tests. Some packages may require additional utilities or runtimes; Codex should identify these from the actual application and current documentation rather than assume they are installed.

This skill does **not** package a particular application by itself, guarantee that any upstream binary will work inside Flatpak, perform an unattended real-world GUI test, or automatically track upstream releases. If the environment is incomplete, results must be reported as **partial / unverified**.

For personal-use packages, not all FlatPark catalog eligibility requirements apply, but security, licensing, binary compatibility, and sandbox constraints still matter.

## References

- [FlatPark Packaging Playbook](https://flatpark.org/docs/packagers/playbook/)
- [Flatpak Builder documentation](https://docs.flatpak.org/en/latest/flatpak-builder.html)

Prepared: **2026-10-25**. Always consult the **latest** official documentation before packaging, as FlatPark policies, runtimes, and tooling can change.
