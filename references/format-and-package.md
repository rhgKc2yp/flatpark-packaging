# Format selection and FlatPark package mechanics

Read the **current** official [format selection](https://flatpark.org/docs/packagers/formats/) and [package file spec](https://flatpark.org/docs/packagers/basics/) before applying these notes.

## Packaging anatomy

In FlatPark's repository, each `registry/<app-id>/` contains:
- `flatpark.yml`: FlatPark registry descriptor, including app ID, display data, manifest path, architectures, upstream update command, proprietary status, declared high-risk privileges and packaging modifications.
- `<app-id>.yml`: flatpak-builder manifest and pinned `type: extra-data` with URL, `sha256` and byte `size`, plus files needed for build-time desktop export.
- `apply_extra.sh`: unpacks pinned upstream file under `/app/extra` **offline at installation**. Installs at `/app/bin/apply_extra`, but it **cannot rely on tools installed to `/app/bin`** when called in a system installation; helper binaries must be in the runtime or downloaded as another extra-data.
- `<name>-wrapper`: starts executable from a stable path under `/app/extra`; keep modifications minimal and documented.
- `<app-id>.desktop`, `.metainfo.xml`, `.png`/`.svg`: build-time exports, not extracted at install; include accurate launch metadata and a metainfo release matching pin.
- `resolve-update.sh`: current upstream release JSON resolver; prints no chatty output on stdout, only structured version/source metadata; the automated pin update is part of **FlatPark CI** and does not exist for standalone personal mode.

Managed source block comments are important to FlatPark's updater. Put **fixed support extra-data** outside the managed vendor-payload block. Never pin guessed hashes/sizes; verify both (use `verify_artifact.py` if file available). Specify `only-arches` to match each real upstream asset. Only advertise arm64 if the actual arm build is pinned and works.

## Select by evidence

- **tar/zip**: generally first choice for vendor-supplied portable trees. Inspect its top-level structure and how it changes with version. In `apply_extra.sh`, extract with `bsdtar --no-same-owner` into a staging directory, find/verify the actual executable, and rename to a stable directory. Do not copy `rm -rf` examples without confirming directory ownership; cleanup only the newly created stage.
- **.deb / .rpm**: inspect the archive; `Depends`, maintainer scripts and expected system directories are **not installed/executed** by extra-data. `bsdtar` handles the package archive; `.deb` normally needs extraction of `data.tar.*`. Inspect `postinst` and linked libs, and reproduce only what is actually required. Check official .deb guide: https://flatpark.org/docs/packagers/formats/deb/
- **AppImage**: type-2 is ELF + SquashFS. It should normally be **extracted, not executed via FUSE**; `appimage-offset` and `unsquashfs` come from an `appimage-tools` extra-data pin from `flatpark/prebuilt`. Do not assume tools can live under `/app/bin`. Copy up-to-date official compatible pins, never hardcode ones shown here. Official guide: https://flatpark.org/docs/packagers/formats/appimage/
- **Qt exception**: a Qt AppImage bundling its own Qt can be more reliable under freedesktop runtime than distro-linked `.deb`/tar builds under KDE; confirm actual libraries and launch behavior.
- **GTK/Tauri/WebKitGTK**: likely GNOME runtime; **Electron/Chromium** often freedesktop + Electron BaseApp; Qt linked to system Qt may require KDE. Runtime choices are **examples, not guarantees**; inspect ABI, upstream docs and runtime current versions.

Official format guide: https://flatpark.org/docs/packagers/formats/tar/
Prebuilt stack guide: https://flatpark.org/docs/packagers/prebuilt/
Toolkit problem checklist: https://flatpark.org/docs/packagers/solutions/by-stack/

## Fixed checklist

1. Official provenance, version, arch and licensing verified.
2. Manifest runtime/SDK and any BaseApp appropriate for the real binary; don't downgrade runtime to dodge faults.
3. `extra-data` URL, SHA-256, size and filename match download. Resolver matches asset exact architecture/file suffix; version/revision changes detectable.
4. `apply_extra.sh` offline, stable install path, clear errors, no archive UID/GID restoration; no system installation assumptions.
5. Wrapper executes **real** binary, works with sandbox; no undisclosed patch/code injection.
6. Proper desktop `Exec`, icon matching ID, window class/StartupWMClass, categories and valid AppStream release/version/description/license.
7. Permissions minimal and explained; optional capabilities as manual overrides.
8. Verified unpack, actual install-time download, GUI/main feature, persistence, and clear limitations.

If needing *two or more unrelated workarounds* to launch, stop and consult the user rather than accreting hacks.
