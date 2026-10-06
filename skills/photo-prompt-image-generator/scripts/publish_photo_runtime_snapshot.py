#!/usr/bin/env python3
"""Validate and publish one immutable local photo runtime generation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from photo_runtime_sources import SKILL_ROOT, SnapshotPublisher, complete_source_update


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", type=Path, default=SKILL_ROOT)
    parser.add_argument("--runtime-store", type=Path)
    parser.add_argument("--complete-update", action="store_true", help="Explicitly finish an interrupted maintenance revision before revalidation.")
    args = parser.parse_args(argv)
    if args.complete_update:
        complete_source_update(args.source_root, args.runtime_store)
    pointer = SnapshotPublisher(args.source_root, args.runtime_store).publish()
    print(json.dumps(pointer, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
