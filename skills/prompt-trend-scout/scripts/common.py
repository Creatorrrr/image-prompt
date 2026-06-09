from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parents[1]
TARGET_SKILL_DIR = PROJECT_ROOT / "skills" / "photo-prompt-image-generator"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_id(prefix: str = "scout") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_skill_path(path_text: str | None, default: Path) -> Path:
    if not path_text:
        return default
    p = Path(path_text)
    if not p.is_absolute():
        p = SKILL_DIR / p
    return p


def load_registry(path_text: str | None = None) -> dict[str, Any]:
    path = resolve_skill_path(path_text, SKILL_DIR / "assets" / "source_registry.json")
    return load_json(path)


def default_data_dir(path_text: str | None = None) -> Path:
    return resolve_skill_path(path_text, SKILL_DIR / "data")


def json_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.exists():
        return sorted(p for p in path.glob("*.json") if p.is_file())
    return []


def read_records(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError(f"Unsupported JSON record shape: {path}")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", text).strip("-").lower()
    return slug or "item"
