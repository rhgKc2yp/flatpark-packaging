#!/usr/bin/env python3
"""Read-only FlatPark-style packaging prerequisite report (stdlib only)."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess

TOOLS = {
    "flatpak": "install/run/inspect the resulting Flatpak",
    "flatpak-builder": "build and export manifests (or use org.flatpak.Builder)",
    "bsdtar": "inspect/unpack vendor archives; present in the relevant runtime",
    "readelf": "inspect dynamic ELF library dependencies",
    "file": "inspect vendor artifact type and architecture",
    "sha256sum": "cross-check extra-data checksum",
    "git": "inspect upstream or FlatPark checkout",
    "curl": "retrieve official upstream releases",
    "jq": "parse upstream release JSON",
    "appstreamcli": "validate AppStream metadata",
    "desktop-file-validate": "validate .desktop entries",
    "node": "run FlatPark registry descriptor scripts in submission mode",
    "ffmpeg": "optional GUI screenshot/test helper",
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="machine-readable report")
    a = p.parse_args()
    installed = {name: shutil.which(name) for name in TOOLS}
    builder_flatpak = None
    if installed["flatpak"]:
        try:
            result = subprocess.run(
                [installed["flatpak"], "list", "--app", "--columns=application"],
                capture_output=True, text=True, timeout=12, check=False,
            )
            if result.returncode == 0:
                builder_flatpak = "org.flatpak.Builder" in result.stdout.splitlines()
        except (OSError, subprocess.TimeoutExpired):
            pass
    report = {
        "architecture": platform.machine(),
        "tools": {name: {"available": path is not None, "path": path, "purpose": TOOLS[name]}
                  for name, path in installed.items()},
        "flatpak_builder_app_installed": builder_flatpak,
        "builder_available": bool(installed["flatpak-builder"] or builder_flatpak),
        "note": "Read-only discovery only; tools being present does not prove a package builds or works.",
    }
    if a.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Host architecture: {report['architecture']}")
        for name, info in report["tools"].items():
            status = "OK" if info["available"] else "missing / optional"
            print(f"  {name:22s} {status:20s} {info['path'] or ''}")
        print(f"org.flatpak.Builder installed: {builder_flatpak}")
        print(f"Builder available: {report['builder_available']}")
        print(report["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
