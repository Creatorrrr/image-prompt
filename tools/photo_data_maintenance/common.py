from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

RECIPES = {"tool": "photo-data-maintenance/v1", "normalization": "nfc-casefold-whitespace/v1",
           "entity": "complete-compiled-record/v1", "links": "explicit-bundle-paths/v1"}


class MaintenanceError(ValueError):
    def __init__(self, state: str, message: str):
        self.state = state
        super().__init__(f"{state}: {message}")


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value) -> str:
    return sha(canonical(value))


def decode(raw: bytes):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f"non-finite JSON number: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).casefold()).strip()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic(path: Path, raw: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def code_binding() -> dict:
    return {path.name: sha(path.read_bytes()) for path in sorted(Path(__file__).parent.glob("*.py"))}


LOADED_TOOL_CODE = code_binding()


def require_tool():
    if code_binding() != LOADED_TOOL_CODE:
        raise MaintenanceError("tool_restart_required", "maintenance implementation changed on disk")


def finding(rule: str, severity: str, entities: list[str], message: str, **details) -> dict:
    return {"id": "finding:" + digest([rule, sorted(entities), details.get("field", "")])[:24],
            "rule": rule, "severity": severity, "entity_ids": sorted(entities), "message": message,
            "details": details}
