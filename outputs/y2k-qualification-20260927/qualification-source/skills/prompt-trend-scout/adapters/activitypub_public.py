from __future__ import annotations

import json
import urllib.request
from typing import Any

from adapters.base import AdapterConfig, make_harvest_record


class ActivityPubPublicAdapter:
    name = "activitypub_public"

    def __init__(self, config: AdapterConfig):
        self.config = config

    def fetch(self, query: str = "", since: str = "", limit: int = 50) -> list[dict[str, Any]]:
        urls = self.config.config.get("urls", []) or []
        query = query or str(self.config.config.get("query") or "")
        records: list[dict[str, Any]] = []
        for url in urls:
            if len(records) >= limit:
                break
            req = urllib.request.Request(str(url), headers={"Accept": "application/activity+json, application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            items = payload.get("orderedItems") or payload.get("items") or payload.get("statuses") or []
            for item in items:
                if len(records) >= limit:
                    break
                text = str(item.get("content") or item.get("summary") or item.get("text") or "")
                if query and query.lower() not in text.lower():
                    continue
                records.append(
                    make_harvest_record(
                        adapter=self.name,
                        collection_method="allowed_feed",
                        platform="activitypub",
                        source_url=str(item.get("url") or item.get("id") or url),
                        raw_text=text,
                        post_id=str(item.get("id") or ""),
                        api_endpoint=str(url),
                    )
                )
        return records
