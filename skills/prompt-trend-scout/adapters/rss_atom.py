from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from adapters.base import AdapterConfig, make_harvest_record


class RssAtomAdapter:
    name = "rss_atom"

    def __init__(self, config: AdapterConfig):
        self.config = config

    def fetch(self, query: str = "", since: str = "", limit: int = 50) -> list[dict[str, Any]]:
        feeds = self.config.config.get("feeds", []) or []
        query = query or str(self.config.config.get("query") or "")
        records: list[dict[str, Any]] = []
        for feed_url in feeds:
            if len(records) >= limit:
                break
            with urllib.request.urlopen(feed_url, timeout=20) as response:
                body = response.read()
            root = ET.fromstring(body)
            items = root.findall(".//item")
            if not items:
                items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
            for item in items:
                if len(records) >= limit:
                    break
                title = _text(item, "title")
                summary = _text(item, "description") or _text(item, "{http://www.w3.org/2005/Atom}summary")
                link = _text(item, "link")
                if not link:
                    atom_link = item.find("{http://www.w3.org/2005/Atom}link")
                    link = atom_link.attrib.get("href", "") if atom_link is not None else ""
                text = f"{title}\n{summary}".strip()
                if query and query.lower() not in text.lower():
                    continue
                records.append(
                    make_harvest_record(
                        adapter=self.name,
                        collection_method="allowed_feed",
                        platform="rss_atom",
                        source_url=link or str(feed_url),
                        raw_text=text,
                        api_endpoint=str(feed_url),
                    )
                )
        return records


def _text(node: ET.Element, name: str) -> str:
    child = node.find(name)
    return "".join(child.itertext()).strip() if child is not None else ""
