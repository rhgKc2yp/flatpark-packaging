# Permissions, security and ask-first gates

Official sources:
- https://flatpark.org/docs/packagers/permissions/
- https://flatpark.org/docs/packagers/can-it-be-packaged/
- https://flatpark.org/docs/packagers/solutions/

## Principle

Grant just enough for the main feature. For supplementary features, give the user the precise `flatpak override --user ... APP_ID` and corresponding reversal **as documentation** instead of applying the override silently. Any broad or privileged setting must be tied to a concrete test failure and explicitly approved.

Examples needing careful justification: `--filesystem=home` or `host`, `--filesystem=~/.ssh` (especially write), `--device=all`, `--socket=system-bus`, `--talk-name` to privileged services, unrestricted host process execution, nested sandbox bypass, disabling Chromium sandbox, exposing real home or secrets. A personal-only build is **not** exempt from these risks.

Prefer XDG portal file dialogs to broad home access; for automatic output grants use the narrowest target (e.g. `xdg-pictures`). A program writing `$HOME/.app` may lose settings when sandbox home is ephemeral; inspect `XDG_*` behavior, test restart and prefer safe dedicated variable/`--persist=.app` where suitable. Don't blindly use `--filesystem=~/.app.json` when software uses atomic replacement; granting parent directory may be required. `--persist` and `--filesystem=home` interact; consult current docs.

Host capabilities may simply not exist in Flatpak (CAP_NET_ADMIN/TUN/VPN, certain raw sockets, direct system administration, arbitrary namespaces). A private-only package **does not circumvent** these limits. If the app's main feature cannot run inside Flatpak, say so and ask whether to stop or knowingly package only a subset of features; don't claim success.

## Stop and ask, with evidence

- Artifact offered only at unofficial mirror or requiring auth; vendor checksum cannot be established.
- License/TOS uncertain or vendor forbids use/distribution contemplated.
- Unclear choice of .deb vs AppImage, runtime/version or app ID affecting compatibility/user profile.
- Need broad grants, host file access, secrets, devices or disabling a sandbox.
- Installer needs privileged host operations/third-party scripts; repository already has user data.
- Workarounds grow into multiple unexplained compatibility hacks.
- Need `sudo`, system-wide Flatpak changes or app-data cleanup.
- Can't actually test core feature (account, subscription, hardware) or GUI; mark incomplete and ask for help or explicit scoped limitation.
- Any network outward publication, public PR, upstream issue, release, upload, CI secrets or credentials.

A good question cites the observed issue, 1–2 safe options and recommendation. Never quietly choose a less secure workaround just to complete the task.
