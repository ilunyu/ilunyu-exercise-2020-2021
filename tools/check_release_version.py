#!/usr/bin/env python3
"""Check that a release PR advances the resource version."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


def load(value: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("resource metadata must be a JSON object")
    return parsed


def validate_version(resource: dict[str, Any], label: str) -> tuple[str, int]:
    version_name = resource.get("versionName")
    version_code = resource.get("versionCode")
    if not isinstance(version_name, str) or VERSION_RE.fullmatch(version_name) is None:
        raise ValueError(f"{label}.versionName must use semantic versioning, for example 1.0.0")
    if not isinstance(version_code, int) or isinstance(version_code, bool) or version_code <= 0:
        raise ValueError(f"{label}.versionCode must be a positive integer")
    return version_name, version_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--previous-ref",
        required=True,
        help="Git revision containing the currently released resource.json",
    )
    args = parser.parse_args()
    try:
        current = load((ROOT / "resource.json").read_text(encoding="utf-8"))
        current_name, current_code = validate_version(current, "current resource")
        previous_text = subprocess.run(
            ["git", "show", f"{args.previous_ref}:resource.json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if previous_text.returncode != 0:
            print(f"Initial release version accepted: {current_name} ({current_code})")
            return 0
        previous = load(previous_text.stdout)
        previous_name, previous_code = validate_version(previous, "previous resource")
        if current_code <= previous_code:
            raise ValueError(f"versionCode must increase: {previous_code} -> {current_code}")
        if current_name == previous_name:
            raise ValueError(f"versionName must change from {previous_name}")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Release version check failed: {error}", file=sys.stderr)
        return 1
    print(
        f"Release version advances: {previous_name} ({previous_code}) -> "
        f"{current_name} ({current_code})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
