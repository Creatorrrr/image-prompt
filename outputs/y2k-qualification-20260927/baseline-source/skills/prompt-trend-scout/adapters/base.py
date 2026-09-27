from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


ALLOWED_COLLECTION_METHODS = {"official_api", "allowed_feed", "local_inbox"}


class CollectionError(RuntimeError):
    pass


@dataclass(frozen=True)
class AdapterConfig:
    name: str
    enabled: bool
    collection_method: str
    config: dict[str, Any]
    skill_dir: Path
    data_dir: Path


class SourceAdapter(Protocol):
    name: str

    def fetch(self, query: str = "", since: str = "", limit: int = 50) -> list[dict[str, Any]]:
        """Return harvest records. This is the only source action exposed."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(*parts: str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()[:24]


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def media_record(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower().lstrip(".") or "octet-stream"
    media_type = f"image/{suffix}" if suffix in {"png", "jpg", "jpeg", "webp", "gif"} else "application/octet-stream"
    return {
        "local_path": str(path),
        "media_type": media_type,
        "sha256": file_sha256(path) if path.exists() and path.is_file() else "",
    }


def make_harvest_record(
    *,
    adapter: str,
    collection_method: str,
    platform: str,
    source_url: str,
    raw_text: str,
    media: list[dict[str, Any]] | None = None,
    post_id: str = "",
    author_handle_raw: str = "",
    api_endpoint: str = "",
    image_description: str = "",
) -> dict[str, Any]:
    if collection_method not in ALLOWED_COLLECTION_METHODS:
        raise CollectionError(f"Blocked collection method: {collection_method}")
    media = media or []
    media_key = "|".join(item.get("sha256", "") or item.get("local_path", "") for item in media)
    record_id = stable_hash(adapter, source_url, raw_text, media_key)
    flags: list[str] = []
    return {
        "id": record_id,
        "collected_at": utc_now(),
        "adapter": adapter,
        "collection_method": collection_method,
        "source_url": source_url,
        "source": {
            "adapter": adapter,
            "platform": platform,
            "post_id": post_id,
            "url": source_url,
            "api_endpoint": api_endpoint,
            "author_handle_raw": author_handle_raw,
        },
        "raw_text": raw_text,
        "image_description": image_description,
        "media": media,
        "license_signals": {
            "explicit_no_repost": False,
            "watermark_detected": False,
            "credit_required": False,
        },
        "flags": flags,
    }
