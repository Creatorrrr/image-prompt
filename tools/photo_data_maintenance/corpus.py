from __future__ import annotations

import copy
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

from .common import MaintenanceError, decode, digest, finding, sha

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = PROJECT / "skills/photo-prompt-image-generator"
BASE = {"photo_prompt_tags.json": "candidate", "photo_prompt_visual_obligations.json": "visual_profile",
        "photo_prompt_quality_layers.json": "quality_policy"}


def runtime(root: Path):
    root = Path(root).resolve()
    code_root = root if (root / "scripts/photo_source_manifest.py").is_file() else DEFAULT_ROOT
    directory = str(code_root / "scripts")
    if directory not in sys.path:
        sys.path.insert(0, directory)
    # One process uses one runtime implementation. Alternate corpora may use
    # that implementation, but a different code version needs a fresh worker.
    module = importlib.import_module("photo_runtime_sources")
    from .common import sha
    actual = module.code_inventory(code_root)
    if actual != module.LOADED_CODE:
        raise MaintenanceError("runtime_restart_required", "source code differs from the imported runtime")
    return module, importlib.import_module("prompt_generator"), importlib.import_module("photo_source_manifest")


def observation(root: Path) -> dict:
    def git(*args):
        try:
            return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    return {"source_root": str(root.resolve()), "commit_observed": git("rev-parse", "HEAD"),
            "dirty_observed": bool(git("status", "--porcelain", "--untracked-files=no"))}


def _scan(root: Path, manifest_api) -> tuple[dict, dict, list]:
    assets = root / "assets"
    findings = []
    names = dict(BASE)
    manifest = assets / "photo_prompt_source_manifest.json"
    names[manifest.name] = "registration"
    try:
        inventory = manifest_api.SourceInventory.load(assets)
        for name, kind, required, _ in inventory.rows:
            names[name] = kind
            if required and not (assets / name).is_file():
                findings.append(finding("required_source_missing", "error", [], f"required file missing: {name}", field=name))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        findings.append(finding("source_manifest_invalid", "error", [], str(exc), field=manifest.name))
        # Diagnose accessible declarations without adopting an invalid inventory.
        try:
            rows = decode(manifest.read_bytes()).get("sources", [])
            for row in rows:
                name = row.get("file", "") if isinstance(row, dict) else ""
                if re.fullmatch(r"photo_prompt_[a-z0-9_]+\.json", name):
                    names[name] = row.get("kind", "unknown")
        except (OSError, ValueError, TypeError, AttributeError):
            pass
    discovered = {p.name for pattern in ("photo_prompt_*_extension.json", "photo_prompt_visual_obligations_*.json")
                  for p in assets.glob(pattern) if p.is_file()}
    for name in sorted(discovered - names.keys()):
        findings.append(finding("unregistered_source", "error", [], f"unregistered source: {name}", field=name))
    raw = {}
    for name in sorted(names):
        path = assets / name
        if path.is_symlink():
            findings.append(finding("source_symlink", "error", [], f"symlink source: {name}", field=name))
            raw[name] = None
        else:
            raw[name] = path.read_bytes() if path.is_file() else None
    return names, raw, findings


def _records(raw: dict, names: dict, findings: list) -> dict:
    values = {}
    for name, value in raw.items():
        if value is None:
            if name in BASE or name == "photo_prompt_source_manifest.json":
                findings.append(finding("base_source_missing", "error", [], f"missing base source: {name}", field=name))
            continue
        try:
            data = decode(value)
            if not isinstance(data, dict):
                raise ValueError("source root must be an object")
            values[name] = data
        except (ValueError, UnicodeError) as exc:
            findings.append(finding("source_json_invalid", "error", [], str(exc), field=name))
    return values


def raw_entities(values: dict, kinds: dict, findings: list) -> tuple[dict, dict]:
    records, sources = {}, {}

    def add(node_id, kind, record, name, pointer, slot=None):
        ref = {"file": name, "pointer": pointer}
        if node_id in records:
            findings.append(finding("duplicate_entity_id", "error", [node_id], "duplicate entity identity",
                                    field=node_id, sources=[*sources[node_id], ref]))
        else:
            records[node_id] = {"id": node_id, "kind": kind, "slot": slot, "record": record}
        sources.setdefault(node_id, []).append(ref)

    for name, value in sorted(values.items()):
        try:
            if kinds.get(name) == "candidate":
                slots = value.get("slots", {})
                if not isinstance(slots, dict):
                    raise ValueError("slots must be an object")
                for slot, rows in slots.items():
                    if not isinstance(rows, list):
                        raise ValueError(f"slots.{slot} must be an array")
                    escaped = str(slot).replace("~", "~0").replace("/", "~1")
                    for index, row in enumerate(rows):
                        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                            raise ValueError(f"slots.{slot}[{index}] requires an id")
                        add(f"slot:{slot}:{row['id']}", "candidate", row, name, f"/slots/{escaped}/{index}", slot)
                for index, row in enumerate(value.get("visual_semantics") or []):
                    if not isinstance(row, dict) or not row.get("id"):
                        raise ValueError(f"visual_semantics[{index}] requires an id")
                    add("bundle:" + row["id"], "bundle", row, name, f"/visual_semantics/{index}")
            if kinds.get(name) == "visual_profile":
                for index, row in enumerate(value.get("profiles") or []):
                    if not isinstance(row, dict) or not row.get("id"):
                        raise ValueError(f"profiles[{index}] requires an id")
                    add("profile:" + row["id"], "profile", row, name, f"/profiles/{index}")
        except (ValueError, TypeError, KeyError) as exc:
            findings.append(finding("source_records_invalid", "error", [], str(exc), field=name))
    for name, value in sorted(values.items()):
        updates = value.get("existing_slot_context_extensions") or {}
        if not isinstance(updates, dict):
            continue
        for slot, additions in updates.items():
            if not isinstance(additions, dict):
                continue
            for entry_id in additions:
                node_id = f"slot:{slot}:{entry_id}"
                if node_id in sources:
                    escape = lambda text: str(text).replace("~", "~0").replace("/", "~1")
                    sources[node_id].append({"file": name, "pointer": f"/existing_slot_context_extensions/{escape(slot)}/{escape(entry_id)}"})
    return records, sources


def make_inventory(records: dict, sources: dict, data=None, registry=None) -> dict:
    if data is not None:
        records = {}
        for slot, rows in data["slots"].items():
            for row in rows:
                node_id = f"slot:{slot}:{row['id']}"
                records[node_id] = {"id": node_id, "kind": "candidate", "slot": slot, "record": row}
        for row in data.get("candidate_bundles") or []:
            node_id = "bundle:" + row["id"]
            # source_sha256 describes the authored bundle, not a semantic field.
            record = {key: value for key, value in row.items() if key != "source_sha256"}
            records[node_id] = {"id": node_id, "kind": "bundle", "slot": None, "record": record}
        for row in registry["profiles"]:
            node_id = "profile:" + row["id"]
            records[node_id] = {"id": node_id, "kind": "profile", "slot": None, "record": row}
    nodes = []
    for node_id, node in sorted(records.items()):
        row = json.loads(json.dumps(node))
        row["source_refs"] = sources.get(node_id, [])
        row["entity_sha256"] = digest([node["kind"], node["slot"], node["record"]])
        nodes.append(row)
    return {"schema": "photo-data-inventory/v1", "nodes": nodes,
            "counts": {kind: sum(node["kind"] == kind for node in nodes) for kind in ("candidate", "bundle", "profile")}}


def capture_draft(root: Path, *, runtime_store: Path | None = None, after_capture=None) -> dict:
    root = root.resolve()
    rt, pg, source_api = runtime(root)
    revision_path = rt.SnapshotPublisher(root, runtime_store).directory / "SOURCE.json"
    revision = decode(revision_path.read_bytes()) if revision_path.is_file() else None
    kinds, raw, findings = _scan(root, source_api)
    values = _records(raw, kinds, findings)
    records, sources = raw_entities(values, kinds, findings)
    data = registry = None
    try:
        inv = source_api.SourceInventory.load(root / "assets")
        inv.validate()
        data = pg.load_json(root / "assets/photo_prompt_tags.json", inventory=inv)
        registry = pg.load_visual_obligation_registry(root / "assets/photo_prompt_visual_obligations.json", inventory=inv)
        validator = importlib.import_module("validate_photo_prompt_dictionary")
        for error in validator.validate_source_corpus(root, data, inv):
            findings.append(finding("authored_contract_invalid", "error", [], error, field=error.split(":", 1)[0]))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        findings.append(finding("authored_contract_invalid", "error", [], str(exc)))
        # Native loaders can fail after partially assembling malformed drafts.
        # Diagnose the captured raw records instead of adopting a partial corpus.
        data = registry = None
    if after_capture:
        after_capture()
    kinds2, raw2, findings2 = _scan(root, source_api)
    revision2 = decode(revision_path.read_bytes()) if revision_path.is_file() else None
    runtime(root)
    if revision2 != revision or kinds2 != kinds or raw2 != raw or findings2 != [row for row in findings if row["rule"] in {"required_source_missing", "source_manifest_invalid", "unregistered_source", "source_symlink"}]:
        raise MaintenanceError("capture_changed", "source registration/presence/content changed while collecting draft")
    return {"inventory": make_inventory(records, sources, data, registry) if data is not None and registry is not None else make_inventory(records, sources),
            "findings": findings, "source_files": raw,
            "binding": {"input_mode": "draft", **observation(root), "generation_id": None,
                        "cooperative_revision": revision, "editing_pending": bool((revision or {}).get("editing")),
                        "source_fingerprint": digest({name: sha(value) if value is not None else None for name, value in raw.items()}),
                        "source_manifest_sha256": sha(raw.get("photo_prompt_source_manifest.json") or b"")}}


def capture_generation(root: Path, store: Path, generation: str) -> dict:
    rt, pg, source_api = runtime(root)
    snapshot = rt.RuntimeSnapshotProvider(root, store).load_generation(generation, independent_audit=True)
    kinds, raw, findings = _scan(snapshot.root, source_api)
    values = _records(raw, kinds, findings)
    records, sources = raw_entities(values, kinds, findings)
    registry = snapshot.data[pg.VISUAL_OBLIGATIONS_DATA_KEY]
    return {"inventory": make_inventory(records, sources, snapshot.data, registry), "findings": findings,
            "source_files": raw,
            "binding": {"input_mode": "generation", **observation(root), "generation_id": generation,
                        "source_fingerprint": snapshot.manifest["source_fingerprint"],
                        "source_manifest_sha256": sha(raw["photo_prompt_source_manifest.json"]),
                        "runtime_algorithm_sha256": snapshot.manifest["algorithm_sha256"]}}


def current_generation(root: Path, store: Path):
    rt, _, _ = runtime(root)
    return rt.RuntimeSnapshotProvider(root, store).acquire(bootstrap=False)
