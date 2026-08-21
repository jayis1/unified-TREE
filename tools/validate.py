#!/usr/bin/env python3
"""Validate the unified TREE registry and four-role topology."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"observe", "reason", "act", "coordinate"}


def main() -> int:
    devices = json.loads((ROOT / "devices.json").read_text())["devices"]
    platform = json.loads((ROOT / "platform.json").read_text())
    errors = []
    ids = [device["id"] for device in devices]
    roles = {role["id"] for role in platform["roles"]}

    if not ids:
        errors.append("registry must contain at least one device node")
    if len(ids) != len(set(ids)):
        errors.append("device node IDs are not unique")
    if roles != ROLES:
        errors.append(f"roles must be {sorted(ROLES)}")
    for device in devices:
        unknown = set(device["roles"]) - roles
        if not device["roles"]:
            errors.append(f"{device['id']}: no role")
        if unknown:
            errors.append(f"{device['id']}: unknown roles {sorted(unknown)}")
    for link in platform["links"]:
        if link["from"] not in roles or link["to"] not in roles:
            errors.append(f"invalid role link: {link}")

    if errors:
        print("unified TREE is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"unified TREE: {len(devices)} device nodes, {len(roles)} roles, "
          f"{len(platform['links'])} role links, valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
