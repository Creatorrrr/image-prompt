from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any

from adapters.base import AdapterConfig, make_harvest_record


class ThreadsOfficialAdapter:
    name = "threads_official"

    def __init__(self, config: AdapterConfig):
        self.config = config

    def fetch(self, query: str = "", since: str = "", limit: int = 50) -> list[dict[str, Any]]:
        token = os.environ.get("THREADS_ACCESS_TOKEN")
        endpoint = str(self.config.config.get("search_endpoint") or "")
        query = query or str(self.config.config.get("query") or "")
        if not token or not endpoint or not query:
            return []
        params = {"q": query, "limit": str(min(limit, 50))}
        url = endpoint + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        records = []
        for item in payload.get("data", [])[:limit]:
            text = str(item.get("text") or item.get("caption") or "")
            item_id = str(item.get("id") or "")
            records.append(
                make_harvest_record(
                    adapter=self.name,
                    collection_method="official_api",
                    platform="threads",
                    source_url=str(item.get("permalink") or item.get("url") or ""),
                    raw_text=text,
                    post_id=item_id,
                    author_handle_raw=str(item.get("username") or ""),
                    api_endpoint=endpoint,
                )
            )
        return records
