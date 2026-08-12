#!/usr/bin/env python3
"""Inventory scene-expression diversity in the taxonomy extensions.

This is deliberately a structural audit. It does not claim that a rendered
image is good. Baseline mode freezes each source extension in isolation;
``--current`` audits the fully merged runtime dictionary, including later
scene-expression overrides.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = SKILL_DIR / "assets"
EXTENSIONS = (
    ("research", ASSET_DIR / "photo_prompt_research_extension.json", "evidence_documentary"),
    ("subculture", ASSET_DIR / "photo_prompt_subculture_extension.json", "specialty_practice"),
    ("worldbuilding", ASSET_DIR / "photo_prompt_worldbuilding_extension.json", "narrative_world"),
    ("cjk_worldbuilding", ASSET_DIR / "photo_prompt_cjk_worldbuilding_extension.json", "narrative_world"),
    ("character_moe", ASSET_DIR / "photo_prompt_character_moe_extension.json", "character_grammar"),
)

OPERATIONAL_TERMS = {
    "administrator",
    "assessor",
    "audit",
    "auditor",
    "catalog",
    "check",
    "checking",
    "clerk",
    "compare",
    "comparing",
    "coordinate",
    "coordinating",
    "document",
    "grading",
    "handoff",
    "inspection",
    "inspector",
    "ledger",
    "monitor",
    "operator",
    "record",
    "registry",
    "review",
    "sorting",
    "staff",
    "verify",
    "verifying",
}

SCENE_FUNCTION_TERMS = {
    "confrontation": {"arbitration", "council", "dispute", "hearing", "trial"},
    "revelation": {"contradictory", "decode", "discover", "identity", "reveal", "revealing", "trace"},
    "threshold": {"arrival", "checkpoint", "crossing", "descent", "frontier", "gate", "transfer"},
    "controlled_action": {
        "assembly",
        "build",
        "constructing",
        "fabricating",
        "fitting",
        "interceptive",
        "practical",
        "repair",
        "repairing",
        "rescue",
        "sortie",
        "testing",
    },
    "aftermath": {"aftercare", "breach", "closeout", "damage", "post", "recovery", "return", "restoration"},
    "intimate_decision": {"betrothal", "host", "lineage", "patronage", "reputation", "succession"},
    "environmental_spectacle": {
        "anomaly",
        "aura",
        "condensation",
        "erosion",
        "field",
        "freeze",
        "kaiju",
        "pollinator",
        "storm",
        "transformation",
    },
    "community_performance": {"club", "concert", "dance", "event", "live", "perform", "performing", "session", "show"},
    "making_process": {"arranging", "assembling", "binding", "customizing", "kitbashing", "layering", "patching", "proofing", "rigging", "styling"},
}

PHASE_FUNCTIONS = {
    "active_process": "controlled_action",
    "care": "aftermath",
    "closeout": "aftermath",
    "fabrication": "making_process",
    "handoff": "operational_documentary",
    "maintenance": "controlled_action",
    "performance": "community_performance",
    "preparation": "making_process",
    "reactivation": "revelation",
    "rehearsal": "community_performance",
    "repair": "controlled_action",
    "setup": "making_process",
}


def tokens(*values: Any) -> set[str]:
    text_parts: list[str] = []
    for value in values:
        if isinstance(value, list):
            text_parts.extend(str(item) for item in value)
        elif value is not None:
            text_parts.append(str(value))
    return {part for part in re.split(r"[^a-z0-9]+", " ".join(text_parts).lower()) if part}


def entry_map(data: dict[str, Any], slot: str) -> dict[str, dict[str, Any]]:
    return {
        str(entry.get("id")): entry
        for entry in data.get("slots", {}).get(slot, [])
        if isinstance(entry, dict) and entry.get("id")
    }


def filter_ids(preset: dict[str, Any], slot: str) -> list[str]:
    raw = (preset.get("filters", {}).get(slot, {}) or {}).get("ids", [])
    return [str(item) for item in raw if str(item).strip()]


def classify_functions(
    preset: dict[str, Any],
    action_ids: Iterable[str],
    action_entries: dict[str, dict[str, Any]],
) -> tuple[list[str], list[dict[str, Any]]]:
    functions: set[str] = set()
    actions: list[dict[str, Any]] = []
    for action_id in action_ids:
        entry = action_entries.get(action_id, {})
        action_tokens = tokens(action_id, entry.get("en"), entry.get("aliases"), entry.get("tags"))
        matched = sorted(
            function
            for function, terms in SCENE_FUNCTION_TERMS.items()
            if action_tokens & terms
        )
        if action_tokens & OPERATIONAL_TERMS:
            matched.append("operational_documentary")
        if not matched:
            matched.append("controlled_action")
        matched = sorted(set(matched))
        functions.update(matched)
        actions.append(
            {
                "id": action_id,
                "functions": matched,
                "operational_term_hits": sorted(action_tokens & OPERATIONAL_TERMS),
            }
        )

    facets = preset.get("facets", {}) if isinstance(preset.get("facets"), dict) else {}
    for phase in facets.get("event_phase", []) or []:
        mapped = PHASE_FUNCTIONS.get(str(phase))
        if mapped:
            functions.add(mapped)
    render_contract = preset.get("render_contract") if isinstance(preset.get("render_contract"), dict) else {}
    scene_metadata = render_contract.get("scene_metadata") if isinstance(render_contract.get("scene_metadata"), dict) else {}
    for metadata in scene_metadata.values():
        if not isinstance(metadata, dict):
            continue
        functions.update(
            str(item)
            for item in metadata.get("scene_functions") or []
            if str(item).strip()
        )
    return sorted(functions), actions


def operational_hits(ids: Iterable[str], entries: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry_id in ids:
        entry = entries.get(entry_id, {})
        hits = sorted(tokens(entry_id, entry.get("en"), entry.get("aliases"), entry.get("tags")) & OPERATIONAL_TERMS)
        if hits:
            rows.append({"id": entry_id, "terms": hits})
    return rows


def audit_preset(
    source: str,
    route_type: str,
    preset: dict[str, Any],
    data: dict[str, Any],
) -> dict[str, Any]:
    subject_ids = filter_ids(preset, "subject")
    action_ids = filter_ids(preset, "action")
    location_ids = filter_ids(preset, "location")
    action_entries = entry_map(data, "action")
    functions, actions = classify_functions(preset, action_ids, action_entries)
    from prompt_generator import render_contract_resolved_scene_blueprints

    blueprints = render_contract_resolved_scene_blueprints(data, preset)
    if blueprints:
        functions = sorted(
            {
                str(function)
                for blueprint in blueprints
                for function in blueprint.get("scene_functions") or []
                if str(function).strip()
            }
        )
        actions = [
            {
                "id": str(blueprint.get("id") or ""),
                "functions": sorted(
                    str(function)
                    for function in blueprint.get("scene_functions") or []
                    if str(function).strip()
                ),
                "operational_term_hits": ["declared_operational"]
                if blueprint.get("operational")
                else [],
                "static_portrait": bool(blueprint.get("static_portrait")),
                "source": blueprint.get("source"),
            }
            for blueprint in blueprints
        ]
        scene_count = len(blueprints)
    else:
        scene_count = max(len(subject_ids), len(action_ids), len(location_ids))
    explicit_contract = isinstance(preset.get("render_contract"), dict)
    exceptions: list[str] = []
    failures: list[str] = []

    if route_type == "narrative_world":
        if scene_count < 4:
            failures.append("fewer_than_four_atomic_scenes")
        if len(functions) < 3:
            failures.append("fewer_than_three_scene_functions")
    elif route_type == "specialty_practice":
        if len(functions) < 2:
            failures.append("fewer_than_two_scene_functions")
    elif route_type == "character_grammar":
        if scene_count < 3:
            failures.append("fewer_than_three_atomic_scenes")
        if len(functions) < 2:
            failures.append("fewer_than_two_scene_functions")
        if actions and sum(1 for row in actions if row.get("static_portrait")) / len(actions) > 0.5:
            failures.append("static_portrait_majority")
    else:
        exceptions.append("evidence_focused_documentary_scope")

    operational_actions = sum(
        1
        for row in actions
        if "operational_documentary" in row["functions"]
        or bool(row.get("operational_term_hits"))
    )
    if route_type == "narrative_world" and actions and operational_actions / len(actions) > 0.5:
        failures.append("operational_action_majority")
    if not explicit_contract:
        failures.append("missing_explicit_render_contract")

    return {
        "source": source,
        "route_type": route_type,
        "preset_id": str(preset.get("id") or ""),
        "scene_count": scene_count,
        "scene_functions": functions,
        "resolved_scene_blueprint_count": len(blueprints),
        "actions": actions,
        "operational_subjects": operational_hits(subject_ids, entry_map(data, "subject")),
        "operational_locations": operational_hits(location_ids, entry_map(data, "location")),
        "render_contract_present": explicit_contract,
        "exceptions": exceptions,
        "failures": sorted(set(failures)),
        "status": "pass" if not failures else "fail",
    }


def merged_runtime_dictionary() -> dict[str, Any]:
    # Import the production merge path instead of maintaining a second merge
    # implementation in this audit.  The script directory is already on
    # sys.path when this file is executed directly.
    from prompt_generator import load_json

    return load_json(ASSET_DIR / "photo_prompt_tags.json")


def build_inventory(recorded_at: str, *, current: bool = False) -> dict[str, Any]:
    routes: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    runtime_data = merged_runtime_dictionary() if current else None
    runtime_presets = {
        str(preset.get("id")): preset
        for preset in (runtime_data or {}).get("presets", [])
        if isinstance(preset, dict) and str(preset.get("id") or "")
    }
    for source, path, route_type in EXTENSIONS:
        source_data = json.loads(path.read_text(encoding="utf-8"))
        if source == "character_moe" and not current:
            from prompt_generator import merge_research_extension

            scene_extension = json.loads(
                (ASSET_DIR / "photo_prompt_scene_expression_character_moe.json").read_text(
                    encoding="utf-8"
                )
            )
            source_data = merge_research_extension(source_data, scene_extension)
        audit_data = runtime_data or source_data
        for source_preset in source_data.get("presets", []) or []:
            if not isinstance(source_preset, dict):
                continue
            preset = runtime_presets.get(str(source_preset.get("id") or ""), source_preset)
            routes.append(audit_preset(source, route_type, preset, audit_data))
            source_counts[source] += 1
    failures = [route for route in routes if route["status"] == "fail"]
    return {
        "schema_version": (
            "photo-scene-expression-current/v1" if current else "photo-scene-expression-baseline/v1"
        ),
        "recorded_at": recorded_at,
        "classification_source": (
            "merged_runtime_dictionary_with_explicit_render_contract"
            if current
            else "legacy_keyword_and_declared_event_phase_inference"
        ),
        "product_warning": "Structural inventory only; rendered-image quality requires pixel review.",
        "thresholds": {
            "narrative_world": {
                "minimum_atomic_scenes": 4,
                "minimum_scene_functions": 3,
                "maximum_operational_action_ratio": 0.5,
            },
            "specialty_practice": {"minimum_scene_functions": 2},
            "character_grammar": {
                "minimum_atomic_scenes": 3,
                "minimum_scene_functions": 2,
                "maximum_static_portrait_ratio": 0.5,
            },
            "evidence_documentary": {"documented_exception_allowed": True},
            "all": {"explicit_render_contract_required": True},
        },
        "summary": {
            "route_count": len(routes),
            "source_route_counts": dict(sorted(source_counts.items())),
            "pass_count": len(routes) - len(failures),
            "fail_count": len(failures),
            "failed_route_ids": [route["preset_id"] for route in failures],
        },
        "routes": routes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recorded-at", default=datetime.now().astimezone().isoformat(timespec="seconds"))
    parser.add_argument("--compact", action="store_true")
    parser.add_argument(
        "--current",
        action="store_true",
        help="Audit the fully merged runtime dictionary instead of the frozen source-extension baseline.",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            build_inventory(args.recorded_at, current=args.current),
            ensure_ascii=False,
            indent=None if args.compact else 2,
            separators=(",", ":") if args.compact else None,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
