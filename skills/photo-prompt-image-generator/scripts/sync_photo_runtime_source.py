#!/usr/bin/env python3
"""Fetch an explicit remote into runtime-owned storage and validate its source."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from photo_runtime_sources import RuntimeSnapshotProvider


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--remote", required=True)
    parser.add_argument("--ref", default="main")
    parser.add_argument("--runtime-store", type=Path)
    args = parser.parse_args(argv)
    provider = RuntimeSnapshotProvider(store=args.runtime_store, mode="remote_before_retrieval", remote=args.remote, ref=args.ref)
    snapshot = provider.acquire()
    print(json.dumps({"generation_id": snapshot.generation_id, "observation": provider.last_observation,
                      "cache_status": snapshot.cache_status}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
