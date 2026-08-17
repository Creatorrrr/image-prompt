#!/usr/bin/env python3
"""Compile explicit English composition carriers from canonical semantic targets.

The runtime must not copy non-English request fragments into an English image
prompt.  This compiler turns the canonical, literal-bound target inventory into
checked-in data.  Runtime code only performs exact lookups; it never translates
or guesses from a request at generation time.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping


PROFILE_KEY = "composition_literal_carrier_profiles"
CURRENT_HOLDOUT = "universal_scene_current_holdout_v2.jsonl"
SEMANTIC_ASSET = "illustration_universal_semantic_bindings_v1.json"
CANDIDATE_ASSET = "illustration_universal_scene_candidates_v1.json"
COMPATIBILITY_ASSET = "illustration_universal_compatibility_graph_v1.json"


# These are semantic rewrites, not euphemisms.  They remove contract bookkeeping
# words or make an otherwise opaque canonical value readable while preserving
# the positive/negative proposition that the carrier authenticates.
PHRASE_OVERRIDES: Mapping[str, str] = {
    "actor_01": "adult subject",
    "actor_01_and_actor_02": "adult diver and winged nonhuman guide",
    "actor_explicit_adult": "adult subject",
    "adult_equivalent_subject": "adult subject",
    "team_01": "three adult storm observers",
    "recipient_01": "intended recipient",
    "chain_as_unconnected_decoration": "unconnected decoration",
    "chain_single_event_use": "single event use",
    "chain_used_for_multiple_events": "used for multiple events",
    "evidence_transferred_while_mount_leaks": "evidence transfer and mount leak",
    "diagnosis_from_expression": "diagnosis inferred from expression",
    "personality_inference_from_expression": "personality inferred from expression",
    "single_true_inner_emotion_claim": "single true inner emotion claim",
    "replace_wooden_mallet_sense": "wooden mallet replaced by metal hammer or blunt weapon",
    "identity_or_scene_hijack": "weapon hijacks identity or scene",
    "identity_replacement": "identity replacement",
    "scene_promise_hijacking_element": "element that changes the scene promise",
    "human_face_added_to_cloud": "human face added to cloud",
    "human_hands_added_to_cloud": "human hands added to cloud",
    "visible_facial_expression_requirement": "visible facial expression requirement",
    "handoff_recipient_entailment": "handoff recipient",
    "actor_01_shared_attention_behavior": "first subject shares attention",
    "actor_02_shared_attention_behavior": "second subject shares attention",
    "three_member_task_topology": "three member task relationship",
    "actor_open_palm_and_other_hand": "open palm and other hand",
    "four_assigned_hands": "four assigned hands",
}

GROUP_OVERRIDES: Mapping[str, list[list[str]]] = {
    # Keep the subject and action as separate AND-groups.  This lets natural
    # English forms such as "No chain is used..." and "The chain is not used..."
    # prove the same forbidden proposition with correctly scoped negation.
    "chain_used_for_multiple_events": [
        ["chain"],
        ["used for multiple events"],
    ],
}

BOOKKEEPING_WORDS = {
    "actor",
    "explicit",
    "requirement",
    "entailment",
    "behavior",
    "role",
}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path.name} must contain JSON objects")
    return rows


def _carrier_phrase(target_id: str) -> str:
    override = PHRASE_OVERRIDES.get(target_id)
    if override is not None:
        return override
    words = [
        word
        for word in target_id.split("_")
        if word and not word.isdigit() and word not in BOOKKEEPING_WORDS
    ]
    phrase = " ".join(words)
    if not phrase or re.fullmatch(r"[a-z0-9]+(?: [a-z0-9]+)*", phrase) is None:
        raise ValueError(f"cannot compile a normalized English carrier for {target_id!r}")
    return phrase


def _profile_groups(target_id: str) -> list[list[str]]:
    override = GROUP_OVERRIDES.get(target_id)
    if override is not None:
        return copy.deepcopy(override)
    return [[_carrier_phrase(target_id)]]


def _ordered_unique(items: Iterable[tuple[str, ...]]) -> list[tuple[str, ...]]:
    return sorted(set(items))


def compile_profiles(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    identity_keys: list[tuple[str, str]] = []
    fixed_slot_keys: list[tuple[str, str]] = []
    event_role_keys: list[tuple[str, str]] = []
    for row in rows:
        contract = row["canonical_scene_contract"]
        identity = contract["identity_core"]
        for entity in identity["entities"]:
            identity_keys.extend(
                (str(fact["id"]), "asserted_presence")
                for fact in entity["feature_facts"]
            )
        identity_keys.extend(
            (str(fact["id"]), "asserted_presence")
            for fact in identity["scene_facts"]
        )
        identity_keys.extend(
            (str(fact["id"]), "forbidden")
            for fact in identity["forbidden_facts"]
        )
        for slot in contract["slot_states"]:
            if slot["state"] != "fixed":
                continue
            fixed_slot_keys.extend(
                (str(slot["slot_id"]), str(binding["value_id"]))
                for binding in slot["value_phrase_bindings"]
            )
        event_role_keys.extend(
            (str(role["role_id"]), str(role["value_id"]))
            for role in contract["event_roles"]
            if role["state"] == "fixed"
        )

    identity_profiles = [
        {
            "fact_id": fact_id,
            "polarity": polarity,
            "required_lexeme_groups": _profile_groups(fact_id),
        }
        for fact_id, polarity in _ordered_unique(identity_keys)
    ]
    fixed_slot_profiles = [
        {
            "slot_id": slot_id,
            "value_id": value_id,
            "required_lexeme_groups": _profile_groups(value_id),
        }
        for slot_id, value_id in _ordered_unique(fixed_slot_keys)
    ]
    event_role_profiles = [
        {
            "role_id": role_id,
            "value_id": value_id,
            "required_lexeme_groups": _profile_groups(value_id),
        }
        for role_id, value_id in _ordered_unique(event_role_keys)
    ]
    return {
        "identity_core": identity_profiles,
        "fixed_slots": fixed_slot_profiles,
        "event_roles": event_role_profiles,
    }


def _encoded(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8")


def _replace_bound_hash(raw: bytes, field: str, digest: str) -> bytes:
    pattern = re.compile(
        rb'("' + re.escape(field.encode("ascii")) + rb'"\s*:\s*")[0-9a-f]{64}("\s*[,}])'
    )
    updated, count = pattern.subn(
        lambda match: match.group(1) + digest.encode("ascii") + match.group(2),
        raw,
    )
    if count != 1:
        raise ValueError(f"expected exactly one {field} binding, found {count}")
    return updated


def compile_assets(asset_dir: Path) -> dict[Path, bytes]:
    semantic_path = asset_dir / SEMANTIC_ASSET
    candidate_path = asset_dir / CANDIDATE_ASSET
    compatibility_path = asset_dir / COMPATIBILITY_ASSET
    semantic = _load_json(semantic_path)
    _load_json(candidate_path)
    _load_json(compatibility_path)
    profiles = compile_profiles(_load_jsonl(asset_dir / CURRENT_HOLDOUT))

    updated_semantic: dict[str, Any] = {}
    inserted = False
    for key, value in semantic.items():
        if key == PROFILE_KEY:
            continue
        if key == "context_literal_profiles":
            updated_semantic[PROFILE_KEY] = profiles
            inserted = True
        updated_semantic[key] = copy.deepcopy(value)
    if not inserted:
        raise ValueError("semantic asset lacks the expected insertion anchor")
    counts = dict(updated_semantic["counts"])
    counts[PROFILE_KEY] = sum(len(records) for records in profiles.values())
    updated_semantic["counts"] = counts
    semantic_bytes = _encoded(updated_semantic)
    semantic_sha = hashlib.sha256(semantic_bytes).hexdigest()

    candidate_bytes = _replace_bound_hash(
        candidate_path.read_bytes(),
        "semantic_bindings_asset_sha256",
        semantic_sha,
    )
    candidate_sha = hashlib.sha256(candidate_bytes).hexdigest()
    compatibility_bytes = _replace_bound_hash(
        compatibility_path.read_bytes(),
        "candidate_asset_sha256",
        candidate_sha,
    )
    compatibility_bytes = _replace_bound_hash(
        compatibility_bytes,
        "semantic_bindings_asset_sha256",
        semantic_sha,
    )
    return {
        semantic_path: semantic_bytes,
        candidate_path: candidate_bytes,
        compatibility_path: compatibility_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare deterministic outputs without writing",
    )
    args = parser.parse_args()
    asset_dir = args.asset_dir.expanduser().resolve()
    outputs = compile_assets(asset_dir)
    stale = [path for path, encoded in outputs.items() if not path.is_file() or path.read_bytes() != encoded]
    if args.check and stale:
        raise SystemExit(
            "compiled universal composition-carrier assets are stale: "
            + ", ".join(path.name for path in stale)
        )
    if not args.check:
        for path, encoded in outputs.items():
            path.write_bytes(encoded)
    profiles = json.loads(outputs[asset_dir / SEMANTIC_ASSET])[PROFILE_KEY]
    print(
        json.dumps(
            {
                "check": args.check,
                "identity_core": len(profiles["identity_core"]),
                "fixed_slots": len(profiles["fixed_slots"]),
                "event_roles": len(profiles["event_roles"]),
                "semantic_sha256": hashlib.sha256(
                    outputs[asset_dir / SEMANTIC_ASSET]
                ).hexdigest(),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
