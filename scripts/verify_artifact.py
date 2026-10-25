#!/usr/bin/env python3
"""Verify a downloaded *local* artifact's size and SHA-256 (no network / writes)."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path, help="the existing file to check")
    p.add_argument("--sha256", required=True, help="expected full 64-character SHA-256")
    p.add_argument("--size", type=int, required=True, help="expected size, in bytes")
    args = p.parse_args()
    if not re.fullmatch(r"[0-9a-fA-F]{64}", args.sha256):
        p.error("--sha256 must be exactly 64 hexadecimal characters")
    if args.size < 0:
        p.error("--size must be nonnegative")
    try:
        if not args.artifact.is_file():
            raise FileNotFoundError(str(args.artifact))
        actual_size = args.artifact.stat().st_size
        actual_sha = sha256(args.artifact)
    except OSError as exc:
        print(f"ERROR: cannot read local artifact: {exc}", file=sys.stderr)
        return 2
    size_ok = actual_size == args.size
    hash_ok = actual_sha.lower() == args.sha256.lower()
    print(f"file: {args.artifact}")
    print(f"bytes: {actual_size} | expected: {args.size} | {'PASS' if size_ok else 'FAIL'}")
    print(f"sha256: {actual_sha}")
    print(f"sha256 match: {'PASS' if hash_ok else 'FAIL'}")
    if size_ok and hash_ok:
        print("PASS: local file matches the expected byte-size and digest.")
        return 0
    print("FAIL: do not pin or install an artifact with mismatched metadata.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
