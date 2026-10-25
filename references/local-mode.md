# Standalone personal/local packaging mode

This is an **adaptation** of the FlatPark technical playbook, **not** a FlatPark feature or publication path. It is for apps that the user wants to package for their own machine. Catalog eligibility rules (for example existing Flathub listings and FlatPark submission policy) do not automatically bar personal packaging. Licensing, provenance and technical sandbox limits still matter.

## Expected structure

Prefer `<project>/packaging/<app-id>/` or an explicitly requested standalone folder. Keep package build scaffolding: `<app-id>.yml`, `apply_extra.sh`, launcher wrapper, desktop entry, metainfo, icon, and when feasible `resolve-update.sh`. You may keep `flatpark.yml` as a human-readable descriptor, **but standard flatpak-builder does not consume it** and FlatPark CI will not run outside FlatPark's repository.

- The upstream app stays an `extra-data` source by default. This keeps redistribution out of the local repo and reproduces FlatPark's install-time behavior.
- For an artifact requiring an account or only found in a local file, **stop and ask** before generating a variant with build-time `type: file`. Make clear the binary would then be stored inside the exported Flatpak repository (unlike FlatPark's model), and check rights to redistribute if it will leave the user's device.
- Prefer an unoccupied, honest app ID. App IDs link to persistent user profiles. Check `flatpak list --app` and the target `~/.var/app/<id>` before build/install. If already installed with important data, isolate or ask; do not overwrite it.
- Pin real extra-data metadata `url`, `sha256`, **byte-size** and matching `filename`. A placeholder means *draft only*, not runnable.

## Read-only inventory examples

```sh
flatpak remotes --user
flatpak list --user --app
flatpak list --system --app
flatpak info --user APP_ID
ls -ld "$HOME/.var/app/APP_ID"
```

Replace `APP_ID` with the **verified** ID. An absent ref or profile is fine. These are observations, not a script to run unchanged.

## Local repository build example

After approving source/runtime/permissions and finding the actual manifest, adapt the following **inside a scratch folder whose paths the agent owns**:

```sh
flatpak-builder --force-clean --repo=./local-repo ./build-dir ./APP_ID.yml
flatpak build-update-repo ./local-repo
flatpak --user remote-add --no-gpg-verify APP_ID-test "$(realpath ./local-repo)"
flatpak --user install APP_ID-test APP_ID
flatpak --user run APP_ID
```

`APP_ID-test` is a **placeholder** for a checked, run-unique, unoccupied remote name; do not literally reuse an existing remote or existing user app. The local repo here is unsigned and `--no-gpg-verify` is appropriate **only for a trusted, local, user-controlled test**. For shared/public remotes, discuss signatures, provenance and distribution; do not normalize insecure remote use. `flatpak-builder` must be available (possibly via `flatpak run org.flatpak.Builder` with compatible mounts and flags—verify rather than assume). Runtime and SDK must exist or be installed only with user approval.

If the normal builder is available and a temporary install is enough, its `--user --install` path may be suitable, but prefer a repo-based install so `extra-data` gets exercised and tested as the official testing playbook expects.

**System install simulation:** a `--user` install is NOT proof `apply_extra.sh` handles an offline, capability-dropped root installation. The actual FlatPark repository provides `./scripts/check-apply-extra.sh <id>` for compatible registry entries. Do not pretend an unrelated standalone package is compatible with that script. If the validation is unavailable, mark it NOT TESTED rather than using `sudo` unexpectedly.

## Updates

A resolver script in the package is useful but **will not run automatically**. A normal `flatpak update` to a local repo only updates when *you have repinned and exported a newer commit*. On the next release, recheck official artifact, checksum, size and version; review format/layout changes; update manifest and metainfo; rerun unpack, repo-install and main-feature tests; export again. Ask before installing a cron, GitHub Action or automation.

## Cleanup

Record the exact resources created for this app. `flatpak kill APP_ID` after testing. Before removing the test app, remote, data or build directory, show the list. Never delete an existing user profile, existing Flatpak ref, local repo, or app data without informed approval. Prefer `flatpak --user uninstall APP_ID` **without** `--delete-data` for a known test-only install if user approves; otherwise leave in place. Never run blanket cleanup commands.
