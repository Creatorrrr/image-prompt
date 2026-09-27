#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from adapters.base import AdapterConfig, ALLOWED_COLLECTION_METHODS
from adapters.activitypub_public import ActivityPubPublicAdapter
from adapters.local_inbox import LocalInboxAdapter
from adapters.rss_atom import RssAtomAdapter
from adapters.threads_official import ThreadsOfficialAdapter
from adapters.x_api import XApiAdapter
from common import SKILL_DIR, default_data_dir, load_registry, run_id, utc_now, write_json


ADAPTERS = {
    "local_inbox": LocalInboxAdapter,
    "rss_atom": RssAtomAdapter,
    "activitypub_public": ActivityPubPublicAdapter,
    "x_api": XApiAdapter,
    "threads_official": ThreadsOfficialAdapter,
}


def collect(
    *,
    registry_path: str | None = None,
    data_dir: str | None = None,
    adapters: list[str] | None = None,
    query: str = "",
    since: str = "",
    limit: int = 50,
    output: str | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    data_root = default_data_dir(data_dir)
    selected = set(adapters or registry.get("adapters", {}).keys())
    records: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    for name, config in registry.get("adapters", {}).items():
        if name not in selected:
            continue
        if name not in ADAPTERS:
            skipped.append({"adapter": name, "reason": "unknown_adapter"})
            continue
        if not config.get("enabled", False):
            skipped.append({"adapter": name, "reason": "disabled"})
            continue
        method = str(config.get("collection_method") or "")
        if method not in ALLOWED_COLLECTION_METHODS:
            raise SystemExit(f"Blocked collection method for {name}: {method}")
        missing_env = [env for env in config.get("required_env", []) if not os.environ.get(env)]
        if missing_env:
            skipped.append({"adapter": name, "reason": "missing_env:" + ",".join(missing_env)})
            continue
        rate_limit = int(config.get("rate_limit_per_run") or limit)
        adapter_limit = max(0, min(limit - len(records), rate_limit))
        if adapter_limit <= 0:
            break
        adapter = ADAPTERS[name](
            AdapterConfig(
                name=name,
                enabled=True,
                collection_method=method,
                config=config,
                skill_dir=SKILL_DIR,
                data_dir=data_root,
            )
        )
        try:
            fetched = adapter.fetch(query=query, since=since, limit=adapter_limit)
        except Exception as exc:  # Source failures should not corrupt other adapters.
            skipped.append({"adapter": name, "reason": f"error:{type(exc).__name__}:{exc}"})
            continue
        for record in fetched:
            record["collection_method"] = method
            records.append(record)
            if len(records) >= limit:
                break

    rid = run_id("harvest")
    out = Path(output) if output else data_root / "raw" / f"{rid}.json"
    write_json(
        out,
        {
            "run_id": rid,
            "generated_at": utc_now(),
            "records": records,
            "skipped": skipped,
        },
    )
    return {"run_id": rid, "output": str(out), "records": records, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only prompt trend source records.")
    parser.add_argument("--registry")
    parser.add_argument("--data-dir")
    parser.add_argument("--adapter", action="append", dest="adapters")
    parser.add_argument("--query", default="")
    parser.add_argument("--since", default="")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = collect(
        registry_path=args.registry,
        data_dir=args.data_dir,
        adapters=args.adapters,
        query=args.query,
        since=args.since,
        limit=args.limit,
        output=args.output,
    )
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
