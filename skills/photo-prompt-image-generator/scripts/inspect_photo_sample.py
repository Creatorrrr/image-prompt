#!/usr/bin/env python3
"""Maintenance-only sampler inspection. Output is not a composition pack."""
import sys
from generate_photo_prompt import main

if __name__ == "__main__":
    args = sys.argv[1:]
    candidates = "--diagnostic-candidates" in args
    args = [arg for arg in args if arg != "--diagnostic-candidates"]
    try:
        raise SystemExit(main(args, diagnostic=True, diagnostic_candidates=candidates))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
