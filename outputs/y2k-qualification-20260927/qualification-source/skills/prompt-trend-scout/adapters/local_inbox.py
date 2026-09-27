from __future__ import annotations

from pathlib import Path
from typing import Any

from adapters.base import AdapterConfig, load_json, make_harvest_record, media_record


class LocalInboxAdapter:
    name = "local_inbox"

    def __init__(self, config: AdapterConfig):
        self.config = config

    def fetch(self, query: str = "", since: str = "", limit: int = 50) -> list[dict[str, Any]]:
        inbox = Path(self.config.config.get("path", "data/raw/inbox"))
        if not inbox.is_absolute():
            inbox = self.config.skill_dir / inbox
        if not inbox.exists():
            return []

        records: list[dict[str, Any]] = []
        for path in sorted(inbox.glob("*.json")):
            payload = load_json(path)
            items = payload if isinstance(payload, list) else [payload]
            for index, item in enumerate(items):
                if len(records) >= limit:
                    return records
                raw_text = str(item.get("raw_text") or item.get("prompt") or item.get("caption") or "")
                image_description = str(item.get("image_description") or item.get("visual_note") or "")
                if query and query.lower() not in f"{raw_text} {image_description}".lower():
                    continue
                media = []
                for media_path in item.get("media_paths", []) or []:
                    p = Path(media_path)
                    if not p.is_absolute():
                        p = path.parent / p
                    media.append(media_record(p))
                source_url = str(item.get("source_url") or f"local://{path.name}#{index}")
                records.append(
                    make_harvest_record(
                        adapter=self.name,
                        collection_method="local_inbox",
                        platform=str(item.get("platform") or "local"),
                        source_url=source_url,
                        raw_text=raw_text,
                        media=media,
                        post_id=str(item.get("post_id") or path.stem),
                        author_handle_raw=str(item.get("author_handle_raw") or ""),
                        image_description=image_description,
                    )
                )
        return records
