#!/usr/bin/env python3
"""Validate research, typed runtime assets, and frozen illustration holdouts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping

from illustration_runtime import (
    AssetValidationError,
    IllustrationRuntimeError,
    LEGACY_CONTRACT_VERSION,
    build_candidate_pack,
    canonical_json_bytes,
    default_asset_dir,
    load_runtime_assets,
    normalize_text,
    validate_assets,
)
from illustration_audit import audit_composed_prompt


RESEARCH_ROLE_VALUES = {"topic_matrix", "independent_source"}
PROVENANCE_VALUES = {"source_supported", "cross_source_synthesis", "design_inference"}
CANDIDATE_ROLE_VALUES = {"visual_atom", "router", "guard"}
GENERATION_RETRY_POLICY_SCHEMA = "subculture-illustration-generation-retry-policy/v1"
GENERATION_RETRY_PHASES = ["primary_generation", "fallback_repair_generation"]
GENERATION_RETRY_OUTCOMES = {
    "tool_error",
    "transport_error",
    "server_error",
    "rate_limit",
    "timeout",
    "empty_result",
    "inaccessible_result",
    "safety_refusal",
    "policy_refusal",
    "other_refusal",
}
GENERATION_RETRY_PRESERVED_FIELDS = {
    "prompt_en",
    "negative_en",
    "pack_id",
    "chosen_candidate_ids",
    "seed",
    "generation_parameters",
}
LEGACY_PROMPT_QUALIFICATION_RUNTIME_SHA256 = (
    "0b44e7ea63517a963d26e1b897d1561c724013eb4ce7b5d9f31a1b9310994e57"
)
LEGACY_PROMPT_QUALIFICATION_AUDIT_SHA256 = (
    "c1a4d21b6476d4b7acaeab189780c409b863ba650505737599ee534d5e79d159"
)
RUNTIME_NAME_GUARDS = (
    re.compile(r"\bin (?:the )?style of\b", re.IGNORECASE),
    re.compile(r"\bby (?:artist|illustrator|mangaka|studio)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:Pok[eé]mon|Pikachu|Naruto|One Piece|Gundam|Evangelion|Genshin Impact|Honkai|Disney|Marvel|Sanrio)\b",
        re.IGNORECASE,
    ),
)

CASE01_V2_SECOND_LOOK_PLAN = {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "render01_proposal_d",
    "reveal_phrase": (
        "Second look: the brass threshold and receiving mat already register the coat's "
        "arrival before the real handoff is complete."
    ),
    "review_scale_ids": ["native"],
    "primary_carrier": {
        "carrier_kind": "material_boundary",
        "carrier_phrase": "one broad pale seam",
        "protected_locus_phrase": (
            "the clear brass threshold strip beneath the closing doorway"
        ),
        "consequence_phrase": (
            "The pale luminous seam crosses the brass threshold before the real handoff "
            "is complete"
        ),
        "risk_flags": [],
    },
    "fallback_carrier": {
        "carrier_kind": "surface_state",
        "carrier_phrase": "one broad dry coat-length patch",
        "protected_locus_phrase": "the unoccupied receiving mat below the doorway",
        "consequence_phrase": (
            "Rain beads stop at a broad dry coat-length boundary on the unoccupied "
            "receiving mat"
        ),
        "risk_flags": [],
    },
}

CASE01_V3_SECOND_LOOK_PLAN = {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "render01_proposal_d",
    "reveal_phrase": (
        "Second look: the untouched closing bell is already swinging while the "
        "repaired coat and recipient hand remain separated."
    ),
    "review_scale_ids": ["native", "thumbnail_320px"],
    "primary_carrier": {
        "carrier_kind": "object_relation",
        "carrier_phrase": (
            "one large isolated brass closing bell already leaning on a taut crimson "
            "thread"
        ),
        "protected_locus_phrase": (
            "the clear black doorway above the untouched recipient hand"
        ),
        "consequence_phrase": (
            "The isolated brass closing bell leans and its displaced clapper swings "
            "while the repaired coat and recipient hand remain separated"
        ),
        "risk_flags": [],
    },
    "fallback_carrier": {
        "carrier_kind": "surface_state",
        "carrier_phrase": "one broad irregular dry coat-length patch",
        "protected_locus_phrase": (
            "the plain seamless dark receiving slab below the doorway"
        ),
        "consequence_phrase": (
            "Rain beads stop around one broad irregular dry coat-length patch that "
            "crosses the continuous grain of the plain dark receiving slab."
        ),
        "risk_flags": [],
    },
}


class ValidationFailure(ValueError):
    """Raised when a versioned asset violates the frozen contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        _require(isinstance(value, dict), f"{path.name}:{line_number} must be an object")
        rows.append(value)
    return rows


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strings(value: Any, label: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{label} must be a list")
    _require(all(isinstance(item, str) and item.strip() for item in value), f"{label} must contain strings")
    _require(len(value) >= minimum, f"{label} must contain at least {minimum} values")
    return list(value)


def validate_generation_retry_policy(asset_dir: Path) -> dict[str, Any]:
    policy = _load_json(asset_dir / "image_generation_retry_policy_v1.json")
    _require(isinstance(policy, dict), "generation retry policy must be an object")
    _require(
        policy.get("schema") == GENERATION_RETRY_POLICY_SCHEMA,
        "generation retry policy schema mismatch",
    )
    _require(
        policy.get("retry_budget_scope") == "per_generation_phase",
        "generation retry budget must be per phase",
    )
    _require(policy.get("phases") == GENERATION_RETRY_PHASES, "generation retry phases mismatch")
    _require(policy.get("initial_calls_per_phase") == 1, "generation phase must start with one call")
    _require(
        policy.get("max_unchanged_retries_after_initial") == 3,
        "generation phase must allow exactly three unchanged retries",
    )
    _require(policy.get("max_calls_per_phase") == 4, "generation phase must allow four total calls")
    outcomes = _strings(
        policy.get("retryable_no_image_outcomes"),
        "generation retry outcomes",
        minimum=1,
    )
    _require(set(outcomes) == GENERATION_RETRY_OUTCOMES, "generation retry outcomes mismatch")
    preserved = _strings(
        policy.get("preserve_exact_fields"),
        "generation retry preserved fields",
        minimum=1,
    )
    _require(
        set(preserved) == GENERATION_RETRY_PRESERVED_FIELDS,
        "generation retry preserved fields mismatch",
    )
    for field in (
        "stop_on_first_concrete_image",
        "retry_does_not_consume_pixel_repair_slot",
        "no_prompt_rewrite_between_retries",
        "no_policy_evasion",
        "higher_priority_platform_stop_applies",
    ):
        _require(policy.get(field) is True, f"generation retry policy requires {field}=true")
    _require(
        policy.get("exhausted_status") == "generation_failed_retries_exhausted",
        "generation retry exhausted status mismatch",
    )
    return {
        "schema": policy["schema"],
        "max_unchanged_retries_after_initial": policy["max_unchanged_retries_after_initial"],
        "max_calls_per_phase": policy["max_calls_per_phase"],
        "includes_safety_refusal": "safety_refusal" in outcomes,
        "includes_policy_refusal": "policy_refusal" in outcomes,
        "status": "pass",
    }


def validate_research(asset_dir: Path) -> dict[str, Any]:
    evidence_dir = asset_dir / "research_evidence_illustration"
    manifest = _load_json(evidence_dir / "manifest.json")
    _require(manifest.get("schema") == "subculture_illustration_research_manifest_v1", "research manifest schema mismatch")
    shards = manifest.get("shards")
    _require(isinstance(shards, list) and len(shards) == 6, "research manifest must list six shards")

    rows: list[dict[str, Any]] = []
    shard_results: list[dict[str, Any]] = []
    for entry in shards:
        _require(isinstance(entry, dict), "research shard entry must be an object")
        rel = entry.get("path")
        _require(isinstance(rel, str) and rel and Path(rel).name == rel, "research shard path must be one local filename")
        path = evidence_dir / rel
        _require(path.is_file(), f"missing research shard {rel}")
        digest = _sha256(path)
        _require(digest == entry.get("sha256"), f"research shard hash mismatch: {rel}")
        shard_rows = _load_jsonl(path)
        _require(len(shard_rows) == entry.get("record_count"), f"research shard row count mismatch: {rel}")
        rows.extend(shard_rows)
        shard_results.append({"path": rel, "record_count": len(shard_rows), "sha256": digest})

    _require(len(rows) == manifest.get("record_count") == 72, "research record count must be 72")
    record_ids = [row.get("id") for row in rows]
    _require(all(isinstance(item, str) and item for item in record_ids), "research record id must be nonempty")
    _require(len(record_ids) == len(set(record_ids)), "research record ids must be globally unique")
    live_record_ids = set(record_ids)

    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        topic_id = row.get("topic_id")
        _require(isinstance(topic_id, str) and topic_id, "research topic_id must be nonempty")
        _require(row.get("record_role") in RESEARCH_ROLE_VALUES, f"{topic_id} has invalid record_role")
        _require(row.get("status") == "approved", f"{topic_id} research row is not approved")
        by_topic[topic_id].append(row)
    _require(len(by_topic) == manifest.get("topic_count") == 24, "research topic count must be 24")

    all_candidate_ids: list[str] = []
    candidate_specs: dict[str, tuple[str, str, str]] = {}
    provenance_counts: Counter[str] = Counter()
    matrix_ids: dict[str, str] = {}
    for topic_id, topic_rows in by_topic.items():
        matrices = [row for row in topic_rows if row["record_role"] == "topic_matrix"]
        sources = [row for row in topic_rows if row["record_role"] == "independent_source"]
        _require(len(topic_rows) == 3 and len(matrices) == 1 and len(sources) == 2, f"{topic_id} must have one matrix and two sources")
        _require(len({row.get('source_url') for row in topic_rows}) == 3, f"{topic_id} must have three distinct URLs")
        matrix = matrices[0]
        matrix_ids[topic_id] = matrix["id"]
        source_ids = {row["id"] for row in sources}
        _require(set(matrix.get("synthesis_evidence_ids", [])) == source_ids, f"{topic_id} synthesis IDs mismatch")

        mechanisms = matrix.get("mechanisms")
        provenance = matrix.get("mechanism_provenance")
        _require(isinstance(mechanisms, list) and 6 <= len(mechanisms) <= 10, f"{topic_id} mechanism count/shape mismatch")
        _require(isinstance(provenance, list) and len(provenance) == len(mechanisms), f"{topic_id} provenance count mismatch")
        _require(all(isinstance(item, dict) and set(item) == {"id", "statement"} for item in mechanisms), f"{topic_id} mechanism shape mismatch")
        _require(all(isinstance(item, dict) and set(item) == {"mechanism_id", "provenance", "evidence_ids"} for item in provenance), f"{topic_id} provenance shape mismatch")
        mechanism_ids = [item["id"] for item in mechanisms]
        _require(mechanism_ids == [item["mechanism_id"] for item in provenance], f"{topic_id} mechanism/provenance order mismatch")
        _require(len(mechanism_ids) == len(set(mechanism_ids)), f"{topic_id} duplicate mechanism IDs")
        for item in provenance:
            kind = item["provenance"]
            provenance_counts[kind] += 1
            _require(kind in PROVENANCE_VALUES, f"{topic_id} invalid provenance kind {kind}")
            refs = _strings(item["evidence_ids"], f"{topic_id}.{item['mechanism_id']}.evidence_ids", minimum=1)
            _require(set(refs) <= live_record_ids, f"{topic_id} provenance has unknown record")
            if kind == "cross_source_synthesis":
                _require(source_ids <= set(refs), f"{topic_id} cross-source mechanism lacks both sources")

        candidate_ids = _strings(matrix.get("candidate_ids"), f"{topic_id}.candidate_ids", minimum=1)
        definitions = matrix.get("candidate_definitions")
        roles = matrix.get("candidate_roles")
        _require(isinstance(definitions, dict) and set(definitions) == set(candidate_ids), f"{topic_id} candidate definitions mismatch")
        _require(isinstance(roles, dict) and set(roles) == set(candidate_ids), f"{topic_id} candidate roles mismatch")
        _require(set(roles.values()) <= CANDIDATE_ROLE_VALUES, f"{topic_id} invalid candidate role")
        evidence_ids = _strings(matrix.get("illustration_evidence"), f"{topic_id}.illustration_evidence", minimum=1)
        evidence_definitions = matrix.get("illustration_evidence_definitions")
        _require(isinstance(evidence_definitions, dict) and set(evidence_definitions) == set(evidence_ids), f"{topic_id} illustration evidence definitions mismatch")
        _require(set(evidence_ids) <= set(candidate_ids), f"{topic_id} illustration evidence is not a candidate subset")
        _require(all(roles[item] == "visual_atom" for item in evidence_ids), f"{topic_id} illustration evidence must be visual")
        for field in ("compatibility", "conflicts", "counterexamples", "boundaries", "format_implications", "viewer_implications"):
            _strings(matrix.get(field), f"{topic_id}.{field}", minimum=4)
        all_candidate_ids.extend(candidate_ids)
        for candidate_id in candidate_ids:
            candidate_specs[candidate_id] = (definitions[candidate_id], roles[candidate_id], topic_id)

    _require(len(all_candidate_ids) == manifest.get("candidate_count") == 264, "research candidate count must be 264")
    _require(len(all_candidate_ids) == len(set(all_candidate_ids)), "research candidate IDs must be globally unique")
    expected_provenance = manifest.get("provenance_counts")
    _require(dict(provenance_counts) == expected_provenance, "research provenance counts do not match manifest")
    _require(sum(provenance_counts.values()) == manifest.get("mechanism_count") == 192, "research mechanism count must be 192")
    return {
        "record_count": len(rows),
        "topic_count": len(by_topic),
        "mechanism_count": sum(provenance_counts.values()),
        "candidate_count": len(all_candidate_ids),
        "candidate_ids": set(all_candidate_ids),
        "candidate_specs": candidate_specs,
        "matrix_ids": matrix_ids,
        "topic_record_ids": {topic_id: {row["id"] for row in topic_rows} for topic_id, topic_rows in by_topic.items()},
        "provenance_counts": dict(sorted(provenance_counts.items())),
        "shards": shard_results,
    }


def _runtime_texts(graph: Mapping[str, Any]) -> Iterable[tuple[str, str]]:
    for node in graph.get("runtime_nodes", []):
        if isinstance(node, dict):
            yield str(node.get("id") or ""), str(node.get("definition") or "")


def validate_holdouts(asset_dir: Path, assets: Any) -> dict[str, Any]:
    prompt_rows = _load_jsonl(asset_dir / "illustration_prompt_holdout_v1.jsonl")
    _require(len(prompt_rows) == 24, "prompt holdout must contain 24 rows")
    resolved: list[dict[str, str]] = []
    for row in prompt_rows:
        pack = build_candidate_pack(
            row["request_ko"],
            seed=row["seed"],
            creativity=0.85,
            assets=assets,
        )
        actual_topic = pack["request_contract"]["topic_id"]
        actual_format = pack["format_profile"]["variant_id"]
        _require(actual_topic == row["topic_id"], f"holdout {row['case_id']} route mismatch: {actual_topic}")
        _require(actual_format == row["expected_format"], f"holdout {row['case_id']} format mismatch: {actual_format}")
        nodes = pack["visual_grammar"]["runtime_nodes"]
        _require(sum(node["selected_role"] == "primary" for node in nodes) == 1, f"holdout {row['case_id']} primary mismatch")
        _require(len(nodes) <= 3 and all(node["node_type"] == "visual_atom" for node in nodes), f"holdout {row['case_id']} sparse visual mismatch")
        repeated = build_candidate_pack(row["request_ko"], seed=row["seed"], creativity=0.85, assets=assets)
        _require(pack == repeated, f"holdout {row['case_id']} is not deterministic")
        resolved.append({"case_id": row["case_id"], "topic_id": actual_topic, "variant_id": actual_format, "pack_id": pack["pack_id"]})

    render_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    _require(len(render_rows) == 6, "render holdout must contain six rows")
    render_topics = [topic for row in render_rows for topic in row.get("topic_ids", [])]
    _require(len(render_topics) == 24 and len(set(render_topics)) == 24, "render holdout must cover 24 topics exactly once")
    return {"prompt_case_count": len(prompt_rows), "render_case_count": len(render_rows), "resolved": resolved}


def _validate_prompt_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    directory_name: str,
    manifest_schema: str,
    contract_version: str | None,
    require_current_implementation_hashes: bool,
) -> dict[str, Any]:
    qualification_dir = asset_dir / directory_name
    manifest = _load_json(qualification_dir / "manifest.json")
    _require(manifest.get("schema") == manifest_schema, f"{directory_name} manifest schema mismatch")
    if require_current_implementation_hashes:
        _require(
            _sha256(Path(__file__).with_name("illustration_runtime.py"))
            == manifest.get("runtime_sha256"),
            f"{directory_name} runtime hash drift",
        )
        _require(
            _sha256(Path(__file__).with_name("illustration_audit.py"))
            == manifest.get("audit_sha256"),
            f"{directory_name} audit hash drift",
        )
    else:
        _require(
            manifest.get("runtime_sha256") == LEGACY_PROMPT_QUALIFICATION_RUNTIME_SHA256,
            "legacy prompt qualification runtime identity drift",
        )
        _require(
            manifest.get("audit_sha256") == LEGACY_PROMPT_QUALIFICATION_AUDIT_SHA256,
            "legacy prompt qualification audit identity drift",
        )
    shards = manifest.get("shards")
    _require(isinstance(shards, list) and len(shards) == 6, "prompt qualification must list six shards")
    records: list[dict[str, Any]] = []
    for entry in shards:
        _require(isinstance(entry, dict), "prompt qualification shard entry must be an object")
        path = qualification_dir / str(entry.get("path") or "")
        _require(path.is_file() and path.parent == qualification_dir, "invalid prompt qualification shard path")
        _require(_sha256(path) == entry.get("sha256"), f"prompt qualification shard hash mismatch: {path.name}")
        rows = _load_jsonl(path)
        _require(len(rows) == entry.get("record_count") == 4, f"prompt qualification shard count mismatch: {path.name}")
        records.extend(rows)

    holdout_rows = _load_jsonl(asset_dir / "illustration_prompt_holdout_v1.jsonl")
    holdout_by_case = {row["case_id"]: row for row in holdout_rows}
    _require(len(records) == manifest.get("case_count") == 24, "prompt qualification case count must be 24")
    case_ids = [record.get("case_id") for record in records]
    _require(len(case_ids) == len(set(case_ids)) and set(case_ids) == set(holdout_by_case), "prompt qualification case coverage mismatch")
    pack_ids: list[str] = []
    prompt_hashes: list[str] = []
    word_counts: list[int] = []
    for record in records:
        case = holdout_by_case[record["case_id"]]
        expected_pack = build_candidate_pack(
            case["request_ko"],
            seed=case["seed"],
            creativity=0.85,
            **({"contract_version": contract_version} if contract_version else {}),
            assets=assets,
        )
        pack = record.get("candidate_pack")
        composed = record.get("composed")
        stored_audit = record.get("audit")
        _require(isinstance(pack, dict) and pack == expected_pack, f"prompt qualification pack drift: {record['case_id']}")
        _require(isinstance(composed, dict), f"prompt qualification composed shape: {record['case_id']}")
        actual_audit = audit_composed_prompt(pack, composed)
        _require(actual_audit == stored_audit, f"prompt qualification audit drift: {record['case_id']}")
        _require(
            actual_audit.get("status") == "pass"
            and actual_audit.get("quality_status") == "pass"
            and not actual_audit.get("integrity_errors")
            and not actual_audit.get("failures")
            and not actual_audit.get("warnings"),
            f"prompt qualification is not clean: {record['case_id']}",
        )
        prompt = composed["prompt_en"]
        pack_ids.append(pack["pack_id"])
        prompt_hashes.append(hashlib.sha256(prompt.encode("utf-8")).hexdigest())
        word_counts.append(len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", prompt)))
    _require(len(pack_ids) == len(set(pack_ids)), "prompt qualification pack IDs must be unique")
    _require(len(prompt_hashes) == len(set(prompt_hashes)), "prompt qualification prompts must be unique")
    expected_words = manifest.get("word_count")
    _require(
        expected_words == {
            "minimum": min(word_counts),
            "maximum": max(word_counts),
            "mean": round(sum(word_counts) / len(word_counts), 1),
        },
        "prompt qualification word-count summary mismatch",
    )
    return {
        "schema": manifest_schema,
        "case_count": len(records),
        "unique_pack_count": len(set(pack_ids)),
        "minimum_words": min(word_counts),
        "maximum_words": max(word_counts),
        "mean_words": round(sum(word_counts) / len(word_counts), 1),
    }


def validate_legacy_prompt_qualification(asset_dir: Path, assets: Any) -> dict[str, Any]:
    """Verify immutable v1 prompt evidence against the explicit legacy path."""

    return _validate_prompt_qualification(
        asset_dir,
        assets,
        directory_name="prompt_qualification_v1",
        manifest_schema="subculture-illustration-prompt-qualification/v1",
        contract_version=LEGACY_CONTRACT_VERSION,
        require_current_implementation_hashes=False,
    )


def validate_prompt_qualification(asset_dir: Path, assets: Any) -> dict[str, Any]:
    """Verify the current v2 prompt qualification against current code."""

    return _validate_prompt_qualification(
        asset_dir,
        assets,
        directory_name="prompt_qualification_v2",
        manifest_schema="subculture-illustration-prompt-qualification/v2",
        contract_version=None,
        require_current_implementation_hashes=True,
    )


def validate_render_v2_preflight(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the separately authorized case-01 successor before any image call."""

    preflight_dir = asset_dir / "render_case01_v2_preflight"
    pack_path = preflight_dir / "candidate_pack.json"
    composed_path = preflight_dir / "composed_prompt.json"
    audit_path = preflight_dir / "audit.json"
    preflight_path = preflight_dir / "preflight.json"
    for path in (pack_path, composed_path, audit_path, preflight_path):
        _require(path.is_file(), f"missing render-v2 preflight artifact: {path.name}")
    _require(
        not any(path.suffix.lower() == ".png" for path in preflight_dir.iterdir()),
        "render-v2 preflight directory must not contain generated images",
    )

    pack = _load_json(pack_path)
    composed = _load_json(composed_path)
    stored_audit = _load_json(audit_path)
    preflight = _load_json(preflight_path)
    case_id = "illustration_render_01_single_narrative"
    _require(
        preflight.get("schema") == "subculture-illustration-render-preflight/v2",
        "render-v2 preflight schema mismatch",
    )
    _require(preflight.get("case_id") == case_id, "render-v2 preflight case mismatch")
    _require(
        preflight.get("status") == "ready_for_separately_authorized_generation"
        and preflight.get("qualification_phase") == "pre_render_only",
        "render-v2 preflight status mismatch",
    )
    _require(
        preflight.get("image_generated") is False
        and preflight.get("image_edited") is False
        and preflight.get("image_tool_invoked") is False,
        "render-v2 preflight must remain generation-free",
    )
    _require(
        preflight.get("approval_required_before_generation") is True
        and preflight.get("authorization_recorded_for_generation") is False,
        "render-v2 preflight must await separate user authority",
    )

    holdout_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v2 preflight lacks its frozen holdout")
    review = _load_json(asset_dir / "render_illustration_quality_visual_review_v1.json")
    historical_case = next(
        (case for case in review.get("cases", []) if case.get("case_id") == case_id),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v2 preflight lacks its v1 review")
    _require(
        historical_case.get("qualification_status") == "fail_repair_exhausted"
        and historical_case.get("attempt_count") == 2
        and historical_case.get("repair_count") == 1
        and historical_case.get("final_image") is None,
        "render-v2 preflight may only succeed the preserved exhausted v1 failure",
    )

    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        assets=assets,
    )
    _require(pack == expected_pack, "render-v2 preflight candidate pack drift")
    candidate_meta = preflight.get("candidate_pack")
    _require(isinstance(candidate_meta, dict), "render-v2 preflight candidate metadata missing")
    _require(candidate_meta.get("exact_source") == "candidate_pack.json", "render-v2 candidate source must be local")
    _require(candidate_meta.get("sha256") == _sha256(pack_path), "render-v2 candidate hash mismatch")
    _require(candidate_meta.get("pack_id") == pack.get("pack_id"), "render-v2 pack ID mismatch")
    _require(
        candidate_meta.get("contract_version") == pack.get("contract_version")
        and candidate_meta.get("seed") == historical_case["seed"]
        and candidate_meta.get("route_id") == historical_case["route_id"]
        and candidate_meta.get("format_profile") == historical_case["format_profile"]
        and candidate_meta.get("creativity") == 0.85
        and candidate_meta.get("safety_mode") == "automatic",
        "render-v2 candidate metadata drift",
    )

    _require(composed.get("pack_id") == pack.get("pack_id"), "render-v2 composed pack binding mismatch")
    actual_audit = audit_composed_prompt(pack, composed)
    _require(actual_audit == stored_audit, "render-v2 preflight audit drift")
    _require(
        actual_audit.get("status") == "pass"
        and actual_audit.get("quality_status") == "pass"
        and not actual_audit.get("integrity_errors")
        and not actual_audit.get("failures")
        and not actual_audit.get("warnings"),
        "render-v2 preflight prompt audit is not clean",
    )
    prompt = composed.get("prompt_en")
    _require(isinstance(prompt, str) and prompt and not prompt.endswith("\n"), "render-v2 prompt shape mismatch")
    prompt_bytes = prompt.encode("utf-8")
    prompt_meta = preflight.get("prompt")
    _require(isinstance(prompt_meta, dict), "render-v2 preflight prompt metadata missing")
    _require(
        prompt_meta.get("exact_source") == "composed_prompt.json#prompt_en"
        and prompt_meta.get("composed_source") == "composed_prompt.json",
        "render-v2 prompt source must be local",
    )
    _require(prompt_meta.get("composed_file_sha256") == _sha256(composed_path), "render-v2 composed hash mismatch")
    _require(prompt_meta.get("utf8_sha256") == hashlib.sha256(prompt_bytes).hexdigest(), "render-v2 prompt hash mismatch")
    _require(
        prompt_meta.get("utf8_with_single_trailing_lf_sha256")
        == hashlib.sha256(prompt_bytes + b"\n").hexdigest(),
        "render-v2 prompt trailing-LF hash mismatch",
    )
    _require(prompt_meta.get("utf8_byte_count") == len(prompt_bytes), "render-v2 prompt byte count mismatch")
    _require(prompt_meta.get("mutation_allowed_before_generation") is False, "render-v2 prompt must be frozen")
    _require(
        prompt_meta.get("negative_en") == composed.get("negative_en") == pack.get("negative_en"),
        "render-v2 negative prompt binding mismatch",
    )

    audit_meta = preflight.get("audit")
    _require(isinstance(audit_meta, dict), "render-v2 preflight audit metadata missing")
    _require(audit_meta.get("exact_source") == "audit.json", "render-v2 audit source must be local")
    _require(audit_meta.get("sha256") == _sha256(audit_path), "render-v2 audit hash mismatch")
    _require(
        audit_meta.get("status") == actual_audit["status"]
        and audit_meta.get("quality_status") == actual_audit["quality_status"]
        and audit_meta.get("failure_count") == len(actual_audit["failures"])
        and audit_meta.get("warning_count") == len(actual_audit["warnings"])
        and audit_meta.get("integrity_error_count") == len(actual_audit["integrity_errors"]),
        "render-v2 audit metadata drift",
    )

    plan = composed.get("second_look_plan")
    _require(plan == CASE01_V2_SECOND_LOOK_PLAN, "render-v2 second-look repair plan drift")
    execution = preflight.get("second_look_execution")
    _require(isinstance(execution, dict), "render-v2 second-look execution metadata missing")
    _require(
        execution.get("plan_source") == "composed_prompt.json#second_look_plan"
        and execution.get("plan_canonical_json_sha256")
        == hashlib.sha256(canonical_json_bytes(plan)).hexdigest()
        and execution.get("selected_proposal_id") == plan["selected_proposal_id"]
        and execution.get("review_scale_ids") == plan["review_scale_ids"],
        "render-v2 second-look execution binding mismatch",
    )
    initial = execution.get("future_initial_attempt")
    repair = execution.get("future_bounded_repair_if_needed")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("maximum_attempts") == 1
        and initial.get("carrier_kind") == plan["primary_carrier"]["carrier_kind"],
        "render-v2 initial attempt contract mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("maximum_attempts") == 1
        and repair.get("carrier_kind") == plan["fallback_carrier"]["carrier_kind"]
        and repair.get("requires_initial_pixel_failure") is True
        and repair.get("must_switch_from_primary_carrier") is True
        and repair.get("repeat_primary_carrier_forbidden") is True,
        "render-v2 fallback repair contract mismatch",
    )
    normalized_prompt = normalize_text(prompt)
    for legacy_fragment in ("clasped hand", "hand shadow", "thread shadow", "projected hand"):
        _require(legacy_fragment not in normalized_prompt, f"render-v2 prompt retains legacy fragile carrier: {legacy_fragment}")

    historical = preflight.get("historical_v1_artifacts")
    _require(isinstance(historical, dict), "render-v2 historical-v1 metadata missing")
    expected_directory = str(Path(historical_case["result_path"]).parent)
    _require(
        historical.get("immutable") is True
        and historical.get("modified_during_preflight") is False
        and historical.get("directory") == expected_directory
        and historical.get("qualification_status") == "final_fail_repair_exhausted",
        "render-v2 historical-v1 preservation metadata drift",
    )
    historical_hashes = historical.get("hashes")
    _require(isinstance(historical_hashes, dict), "render-v2 historical-v1 hashes missing")
    _require(
        historical_hashes.get("result.json") == historical_case["result_sha256"]
        and historical_hashes.get("initial.png") == historical_case["initial_image"]["sha256"]
        and historical_hashes.get("edit_candidate.png") == historical_case["repair_image"]["sha256"],
        "render-v2 historical-v1 review hashes drift",
    )
    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        historical_dir = local_repo_root / expected_directory
        for filename, digest in historical_hashes.items():
            historical_path = historical_dir / filename
            _require(historical_path.is_file(), f"missing historical v1 artifact: {filename}")
            _require(_sha256(historical_path) == digest, f"historical v1 artifact hash mismatch: {filename}")
        _require(not (historical_dir / "final.png").exists(), "failed historical v1 case must remain without final.png")

    return {
        "status": "historical_preflight_valid",
        "recorded_status": "ready_awaiting_user_approval",
        "case_id": case_id,
        "pack_id": pack["pack_id"],
        "prompt_sha256": prompt_meta["utf8_sha256"],
        "second_look_plan_sha256": execution["plan_canonical_json_sha256"],
        "initial_attempted_role": initial["attempted_role"],
        "repair_attempted_role": repair["attempted_role"],
        "image_generated": False,
        "historical_local_artifacts_verified": verify_local_images,
    }


def validate_render_v3_preflight(
    asset_dir: Path,
    assets: Any,
) -> dict[str, Any]:
    """Verify the authorized structural successor without rewriting v1/v2 history."""

    preflight_dir = asset_dir / "render_case01_v3_preflight"
    pack_path = preflight_dir / "candidate_pack.json"
    composed_path = preflight_dir / "composed_prompt.json"
    audit_path = preflight_dir / "audit.json"
    preflight_path = preflight_dir / "preflight.json"
    for path in (pack_path, composed_path, audit_path, preflight_path):
        _require(path.is_file(), f"missing render-v3 preflight artifact: {path.name}")
    _require(
        not any(path.suffix.lower() == ".png" for path in preflight_dir.iterdir()),
        "render-v3 preflight directory must not contain generated images",
    )

    pack = _load_json(pack_path)
    composed = _load_json(composed_path)
    stored_audit = _load_json(audit_path)
    preflight = _load_json(preflight_path)
    case_id = "illustration_render_01_single_narrative"
    _require(
        preflight.get("schema") == "subculture-illustration-render-preflight/v3",
        "render-v3 preflight schema mismatch",
    )
    _require(preflight.get("case_id") == case_id, "render-v3 preflight case mismatch")
    _require(
        preflight.get("status") == "authorized_ready_for_generation"
        and preflight.get("qualification_phase") == "pre_render_only",
        "render-v3 preflight status mismatch",
    )
    _require(
        preflight.get("image_generated") is False
        and preflight.get("image_edited") is False
        and preflight.get("image_tool_invoked") is False,
        "render-v3 preflight itself must remain generation-free",
    )
    _require(
        preflight.get("approval_required_before_generation") is True
        and preflight.get("authorization_recorded_for_generation") is True,
        "render-v3 preflight must record the explicit successor authority",
    )
    authorization = preflight.get("authorization")
    _require(isinstance(authorization, dict), "render-v3 authorization metadata missing")
    _require(
        authorization.get("initial_generation_maximum") == 1
        and authorization.get("fallback_edit_maximum") == 1
        and authorization.get("batch_selection_forbidden") is True
        and authorization.get("full_regression_only_after_pixel_pass") is True,
        "render-v3 authorization boundary mismatch",
    )

    holdout_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v3 preflight lacks its frozen holdout")
    historical_review = _load_json(asset_dir / "render_illustration_quality_visual_review_v1.json")
    historical_case = next(
        (case for case in historical_review.get("cases", []) if case.get("case_id") == case_id),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v3 preflight lacks its v1 review")
    v2_review = _load_json(asset_dir / "render_case01_v2_visual_review.json")
    _require(
        v2_review.get("qualification_status") == "fail_repair_exhausted"
        and v2_review.get("attempt_count") == 2
        and v2_review.get("repair_count") == 1
        and v2_review.get("final_image") is None,
        "render-v3 preflight must preserve the exhausted v2 failure",
    )

    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        assets=assets,
    )
    _require(pack == expected_pack, "render-v3 preflight candidate pack drift")
    candidate_meta = preflight.get("candidate_pack")
    _require(isinstance(candidate_meta, dict), "render-v3 candidate metadata missing")
    _require(
        candidate_meta.get("exact_source") == "candidate_pack.json"
        and candidate_meta.get("sha256") == _sha256(pack_path)
        and candidate_meta.get("pack_id") == pack.get("pack_id")
        and candidate_meta.get("contract_version") == pack.get("contract_version")
        and candidate_meta.get("seed") == historical_case["seed"]
        and candidate_meta.get("route_id") == historical_case["route_id"]
        and candidate_meta.get("format_profile") == historical_case["format_profile"]
        and candidate_meta.get("creativity") == 0.85
        and candidate_meta.get("safety_mode") == "automatic",
        "render-v3 candidate metadata drift",
    )

    _require(composed.get("pack_id") == pack.get("pack_id"), "render-v3 composed pack binding mismatch")
    actual_audit = audit_composed_prompt(pack, composed)
    _require(actual_audit == stored_audit, "render-v3 preflight audit drift")
    _require(
        actual_audit.get("status") == "pass"
        and actual_audit.get("quality_status") == "pass"
        and not actual_audit.get("integrity_errors")
        and not actual_audit.get("failures")
        and not actual_audit.get("warnings"),
        "render-v3 preflight prompt audit is not clean",
    )
    prompt = composed.get("prompt_en")
    _require(isinstance(prompt, str) and prompt and not prompt.endswith("\n"), "render-v3 prompt shape mismatch")
    prompt_bytes = prompt.encode("utf-8")
    prompt_meta = preflight.get("prompt")
    _require(isinstance(prompt_meta, dict), "render-v3 prompt metadata missing")
    _require(
        prompt_meta.get("exact_source") == "composed_prompt.json#prompt_en"
        and prompt_meta.get("composed_source") == "composed_prompt.json"
        and prompt_meta.get("composed_file_sha256") == _sha256(composed_path)
        and prompt_meta.get("utf8_sha256") == hashlib.sha256(prompt_bytes).hexdigest()
        and prompt_meta.get("utf8_with_single_trailing_lf_sha256")
        == hashlib.sha256(prompt_bytes + b"\n").hexdigest()
        and prompt_meta.get("utf8_byte_count") == len(prompt_bytes)
        and prompt_meta.get("mutation_allowed_before_initial_generation") is False,
        "render-v3 prompt hash/freeze metadata drift",
    )
    _require(
        prompt_meta.get("negative_en") == composed.get("negative_en") == pack.get("negative_en"),
        "render-v3 negative prompt binding mismatch",
    )
    audit_meta = preflight.get("audit")
    _require(isinstance(audit_meta, dict), "render-v3 audit metadata missing")
    _require(
        audit_meta.get("exact_source") == "audit.json"
        and audit_meta.get("sha256") == _sha256(audit_path)
        and audit_meta.get("status") == actual_audit["status"]
        and audit_meta.get("quality_status") == actual_audit["quality_status"]
        and audit_meta.get("failure_count") == len(actual_audit["failures"])
        and audit_meta.get("warning_count") == len(actual_audit["warnings"])
        and audit_meta.get("integrity_error_count") == len(actual_audit["integrity_errors"]),
        "render-v3 audit metadata drift",
    )

    plan = composed.get("second_look_plan")
    _require(plan == CASE01_V3_SECOND_LOOK_PLAN, "render-v3 second-look plan drift")
    execution = preflight.get("second_look_execution")
    _require(isinstance(execution, dict), "render-v3 second-look execution metadata missing")
    _require(
        execution.get("plan_source") == "composed_prompt.json#second_look_plan"
        and execution.get("plan_canonical_json_sha256")
        == hashlib.sha256(canonical_json_bytes(plan)).hexdigest()
        and execution.get("selected_proposal_id") == plan["selected_proposal_id"]
        and execution.get("review_scale_ids") == plan["review_scale_ids"],
        "render-v3 second-look execution binding mismatch",
    )
    initial = execution.get("future_initial_attempt")
    repair = execution.get("future_bounded_repair_if_needed")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("maximum_attempts") == 1
        and initial.get("carrier_kind") == "object_relation",
        "render-v3 initial attempt contract mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("maximum_attempts") == 1
        and repair.get("carrier_kind") == "surface_state"
        and repair.get("requires_initial_pixel_failure") is True
        and repair.get("must_switch_from_primary_carrier") is True
        and repair.get("repeat_primary_carrier_forbidden") is True,
        "render-v3 fallback repair contract mismatch",
    )
    normalized_prompt = normalize_text(prompt)
    for legacy_fragment in (
        "broad pale seam",
        "clear brass threshold strip",
        "unoccupied receiving mat",
        "broad dry coat-length boundary on the unoccupied receiving mat",
    ):
        _require(
            legacy_fragment not in normalized_prompt,
            f"render-v3 prompt retains failed v2 carrier: {legacy_fragment}",
        )
    for required_fragment in (
        "rigid ceiling chain",
        "bell body tilts",
        "clapper displaces",
        "no hand touches the bell",
        "no rug, mat, border, weave, tile, inlay",
        "continuous grain",
    ):
        _require(
            required_fragment in normalized_prompt,
            f"render-v3 prompt lacks structural carrier evidence: {required_fragment}",
        )

    historical = preflight.get("historical_artifacts")
    _require(isinstance(historical, list) and len(historical) == 2, "render-v3 historical metadata mismatch")
    _require(
        [item.get("generation") for item in historical if isinstance(item, dict)]
        == ["v1", "v2"]
        and all(item.get("immutable") is True for item in historical if isinstance(item, dict))
        and all(
            item.get("qualification_status") == "final_fail_repair_exhausted"
            for item in historical
            if isinstance(item, dict)
        ),
        "render-v3 must preserve both earlier exhausted outcomes",
    )

    return {
        "status": "authorized_preflight_valid",
        "recorded_status": "authorized_ready_for_generation",
        "case_id": case_id,
        "pack_id": pack["pack_id"],
        "prompt_sha256": prompt_meta["utf8_sha256"],
        "second_look_plan_sha256": execution["plan_canonical_json_sha256"],
        "initial_attempted_role": initial["attempted_role"],
        "repair_attempted_role": repair["attempted_role"],
        "image_generated_in_preflight": False,
    }


def _review_focus_map(value: Any, label: str) -> dict[str, str]:
    _require(isinstance(value, list) and value, f"{label} must be a nonempty list")
    result: dict[str, str] = {}
    for item in value:
        _require(isinstance(item, dict), f"{label} entries must be objects")
        focus = item.get("focus")
        outcome = item.get("outcome")
        _require(isinstance(focus, str) and focus, f"{label} focus must be nonempty")
        _require(isinstance(outcome, str) and outcome, f"{label} outcome must be nonempty")
        _require(focus not in result, f"{label} contains duplicate focus {focus}")
        result[focus] = outcome
    return result


def _png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    _require(
        len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR",
        f"{path} is not a canonical PNG",
    )
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def validate_render_v2_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the bounded v2 successor without promoting either failed role."""

    review_path = asset_dir / "render_case01_v2_visual_review.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version")
        == "subculture-illustration-render-successor-review/v2",
        "render-v2 successor review schema mismatch",
    )
    case_id = "illustration_render_01_single_narrative"
    _require(review.get("case_id") == case_id, "render-v2 successor case mismatch")
    _require(
        review.get("relationship_to_v1")
        == "continues_the_preserved_v1_failure_with_a_distinct_v2_contract",
        "render-v2 successor must not relabel the v1 failure",
    )

    holdout_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v2 successor lacks its frozen holdout")
    historical_review = _load_json(
        asset_dir / "render_illustration_quality_visual_review_v1.json"
    )
    historical_case = next(
        (case for case in historical_review.get("cases", []) if case.get("case_id") == case_id),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v2 successor lacks its v1 case")

    preflight_dir = asset_dir / "render_case01_v2_preflight"
    preflight_pack = _load_json(preflight_dir / "candidate_pack.json")
    preflight_composed = _load_json(preflight_dir / "composed_prompt.json")
    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        assets=assets,
    )
    _require(preflight_pack == expected_pack, "render-v2 successor pack drift")
    preflight = review.get("preflight")
    _require(isinstance(preflight, dict), "render-v2 successor preflight metadata missing")
    _require(
        preflight.get("directory") == "render_case01_v2_preflight"
        and preflight.get("pack_id") == preflight_pack["pack_id"]
        and preflight.get("prompt_sha256")
        == hashlib.sha256(preflight_composed["prompt_en"].encode("utf-8")).hexdigest()
        and preflight.get("second_look_plan_sha256")
        == hashlib.sha256(
            canonical_json_bytes(preflight_composed["second_look_plan"])
        ).hexdigest(),
        "render-v2 successor preflight binding mismatch",
    )

    _require(
        review.get("qualification_status") == "fail_repair_exhausted"
        and review.get("attempt_count") == 2
        and review.get("repair_count") == 1
        and review.get("final_image") is None,
        "render-v2 successor must preserve the exhausted failure",
    )
    initial = review.get("initial_image")
    repair = review.get("repair_image")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("pixel_status") == "fail",
        "render-v2 primary attempt record mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("pixel_status") == "fail",
        "render-v2 fallback attempt record mismatch",
    )

    focus = _review_focus_map(
        review.get("review_focus_results"), "render-v2.review_focus_results"
    )
    _require(
        set(frozen["required_pixel_focus"]) <= set(focus)
        and all(focus[item] == "pass" for item in frozen["required_pixel_focus"]),
        "render-v2 successor lost a frozen primary focus",
    )
    _require(
        focus.get("second_look_primary_carrier") == "fail"
        and focus.get("second_look_fallback_carrier") == "fail",
        "render-v2 successor must not promote a failed second-look carrier",
    )
    thumbnail = _review_focus_map(
        review.get("thumbnail_results"), "render-v2.thumbnail_results"
    )
    _require(
        set(thumbnail) == set(frozen["thumbnail_checks"])
        and set(thumbnail.values()) == {"pass"},
        "render-v2 successor thumbnail review mismatch",
    )
    forbidden = _review_focus_map(
        review.get("forbidden_convergence_results"),
        "render-v2.forbidden_convergence_results",
    )
    _require(
        set(forbidden) == set(frozen["forbidden_pixel_convergence"])
        and set(forbidden.values()) == {"absent"},
        "render-v2 successor forbidden-convergence mismatch",
    )

    second_look = review.get("second_look_pixel_review")
    _require(isinstance(second_look, dict), "render-v2 second-look review missing")
    expected_plan_sha = hashlib.sha256(
        canonical_json_bytes(preflight_composed["second_look_plan"])
    ).hexdigest()
    _require(
        second_look.get("plan_sha256") == expected_plan_sha
        and second_look.get("declared_review_scale_ids") == ["native"]
        and second_look.get("qualified_role") is None
        and second_look.get("qualification_status") == "fail_repair_exhausted",
        "render-v2 second-look summary mismatch",
    )
    attempts = second_look.get("attempts")
    _require(isinstance(attempts, list) and len(attempts) == 2, "render-v2 second-look attempts mismatch")
    _require(
        [attempt.get("attempted_role") for attempt in attempts]
        == ["primary_carrier", "fallback_carrier"],
        "render-v2 second-look role order mismatch",
    )
    for attempt in attempts:
        scale_results = attempt.get("scale_results")
        _require(
            isinstance(scale_results, list)
            and len(scale_results) == 1
            and scale_results[0].get("scale_id") == "native"
            and scale_results[0].get("status") == "fail"
            and isinstance(scale_results[0].get("evidence"), str)
            and scale_results[0]["evidence"],
            "render-v2 second-look scale result mismatch",
        )

    aggregate = review.get("aggregate_with_preserved_v1_passes")
    _require(isinstance(aggregate, dict), "render-v2 aggregate missing")
    _require(
        aggregate
        == {
            "case_count": 6,
            "passed_case_count": 5,
            "failed_case_count": 1,
            "failure_case_ids": [case_id],
            "outcome": "partial",
        },
        "render-v2 aggregate must remain five pass and one fail",
    )
    suite = review.get("post_render_full_suite")
    _require(
        isinstance(suite, dict)
        and suite.get("authorized") is True
        and suite.get("condition") == "pixel_qualification_passes"
        and suite.get("condition_met") is False
        and suite.get("executed") is False,
        "render-v2 conditional full-suite record mismatch",
    )

    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        result_rel = review.get("result_path")
        _require(isinstance(result_rel, str) and result_rel, "render-v2 result path missing")
        result_path = local_repo_root / result_rel
        _require(result_path.is_file(), "render-v2 local result is missing")
        _require(_sha256(result_path) == review.get("result_sha256"), "render-v2 result hash mismatch")
        result = _load_json(result_path)
        _require(
            result.get("schema") == "subculture-illustration-render-result/v2"
            and result.get("qualification_status") == "final_fail_repair_exhausted_v2"
            and result.get("attempt_count") == 2
            and result.get("repair_attempt_count") == 1
            and result.get("final_image") is None,
            "render-v2 local result status mismatch",
        )
        result_dir = result_path.parent
        local_pack = _load_json(result_dir / "candidate_pack.json")
        local_composed = _load_json(result_dir / "composed_prompt.json")
        local_audit = _load_json(result_dir / "audit.json")
        _require(local_pack == expected_pack, "render-v2 local pack drift")
        _require(local_composed == preflight_composed, "render-v2 local composed prompt drift")
        _require(
            audit_composed_prompt(local_pack, local_composed) == local_audit,
            "render-v2 local audit drift",
        )
        _require(
            local_audit.get("status") == "pass"
            and local_audit.get("quality_status") == "pass"
            and not local_audit.get("integrity_errors")
            and not local_audit.get("failures")
            and not local_audit.get("warnings"),
            "render-v2 local audit is not clean",
        )
        _require(
            result.get("second_look_pixel_review") == second_look,
            "render-v2 result/review second-look mismatch",
        )
        _require(
            result.get("post_render_full_suite", {}).get("executed") is False,
            "render-v2 result must not claim the conditional suite ran",
        )
        for record in (initial, repair):
            image_path = local_repo_root / record["path"]
            _require(image_path.is_file(), f"render-v2 local image missing: {record['path']}")
            _require(_sha256(image_path) == record["sha256"], f"render-v2 local image hash mismatch: {record['path']}")
            expected_dimensions = tuple(
                int(value) for value in record["dimensions"].split("x", 1)
            )
            _require(
                _png_dimensions(image_path) == expected_dimensions,
                f"render-v2 local image dimensions mismatch: {record['path']}",
            )
        for view in result.get("review_views", []):
            _require(isinstance(view, dict), "render-v2 review view must be an object")
            view_path = result_dir / str(view.get("path") or "")
            _require(view_path.is_file(), f"render-v2 review view missing: {view_path.name}")
            _require(_sha256(view_path) == view.get("sha256"), f"render-v2 review view hash mismatch: {view_path.name}")
            _require(
                _png_dimensions(view_path) == (view.get("width"), view.get("height")),
                f"render-v2 review view dimensions mismatch: {view_path.name}",
            )
        for attempt_key in ("initial_attempt", "fallback_attempt"):
            attempt = result.get(attempt_key)
            _require(isinstance(attempt, dict), f"render-v2 {attempt_key} missing")
            native_path = Path(str(attempt.get("native_tool_path") or ""))
            _require(native_path.is_file(), f"render-v2 native source missing: {attempt_key}")
            _require(_sha256(native_path) == attempt.get("sha256"), f"render-v2 native source hash mismatch: {attempt_key}")
            blind_path = result_dir / str(attempt.get("blind_observations_path") or "")
            _require(blind_path.is_file(), f"render-v2 blind observations missing: {attempt_key}")
            _require(
                _sha256(blind_path) == attempt.get("blind_observations_sha256"),
                f"render-v2 blind observation hash mismatch: {attempt_key}",
            )
        _require(not (result_dir / "final.png").exists(), "failed render-v2 case must not expose final.png")

    return {
        "qualification_status": "partial",
        "case_id": case_id,
        "attempt_count": 2,
        "repair_count": 1,
        "qualified_role": None,
        "passed_case_count": 5,
        "failed_case_count": 1,
        "full_suite_executed": False,
        "local_artifacts_verified": verify_local_images,
    }


def validate_render_v3_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the one-attempt v3 pass while retaining both prior failures."""

    review_path = asset_dir / "render_case01_v3_visual_review.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version")
        == "subculture-illustration-render-successor-review/v3",
        "render-v3 successor review schema mismatch",
    )
    case_id = "illustration_render_01_single_narrative"
    _require(review.get("case_id") == case_id, "render-v3 successor case mismatch")
    _require(
        review.get("relationship_to_history")
        == "continues_preserved_v1_and_v2_failures_with_a_structurally_distinct_v3_plan",
        "render-v3 successor must preserve rather than relabel historical failures",
    )
    v2_review = _load_json(asset_dir / "render_case01_v2_visual_review.json")
    _require(
        v2_review.get("qualification_status") == "fail_repair_exhausted"
        and v2_review.get("attempt_count") == 2
        and v2_review.get("repair_count") == 1
        and v2_review.get("final_image") is None,
        "render-v3 successor cannot rewrite the v2 exhausted failure",
    )

    holdout_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v3 successor lacks its frozen holdout")
    historical_review = _load_json(asset_dir / "render_illustration_quality_visual_review_v1.json")
    historical_case = next(
        (case for case in historical_review.get("cases", []) if case.get("case_id") == case_id),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v3 successor lacks its v1 case")

    preflight_dir = asset_dir / "render_case01_v3_preflight"
    preflight_pack = _load_json(preflight_dir / "candidate_pack.json")
    preflight_composed = _load_json(preflight_dir / "composed_prompt.json")
    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        assets=assets,
    )
    _require(preflight_pack == expected_pack, "render-v3 successor pack drift")
    preflight = review.get("preflight")
    _require(isinstance(preflight, dict), "render-v3 successor preflight metadata missing")
    _require(
        preflight.get("directory") == "render_case01_v3_preflight"
        and preflight.get("pack_id") == preflight_pack["pack_id"]
        and preflight.get("prompt_sha256")
        == hashlib.sha256(preflight_composed["prompt_en"].encode("utf-8")).hexdigest()
        and preflight.get("second_look_plan_sha256")
        == hashlib.sha256(
            canonical_json_bytes(preflight_composed["second_look_plan"])
        ).hexdigest(),
        "render-v3 successor preflight binding mismatch",
    )

    _require(
        review.get("qualification_status") == "pass"
        and review.get("attempt_count") == 1
        and review.get("repair_count") == 0
        and review.get("repair_image") is None,
        "render-v3 successor must record one pristine primary pass and no repair",
    )
    initial = review.get("initial_image")
    final = review.get("final_image")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("pixel_status") == "pass",
        "render-v3 primary attempt record mismatch",
    )
    _require(
        isinstance(final, dict)
        and final.get("byte_identical_to_initial") is True
        and final.get("sha256") == initial.get("sha256")
        and final.get("dimensions") == initial.get("dimensions"),
        "render-v3 final must be the byte-identical passing primary image",
    )

    focus = _review_focus_map(
        review.get("review_focus_results"), "render-v3.review_focus_results"
    )
    _require(
        set(frozen["required_pixel_focus"]) <= set(focus)
        and all(focus[item] == "pass" for item in frozen["required_pixel_focus"]),
        "render-v3 successor lost a frozen primary focus",
    )
    _require(
        focus.get("second_look_primary_carrier") == "pass"
        and focus.get("second_look_fallback_carrier") == "not_attempted",
        "render-v3 successor role qualification mismatch",
    )
    thumbnail = _review_focus_map(
        review.get("thumbnail_results"), "render-v3.thumbnail_results"
    )
    _require(
        set(thumbnail) == set(frozen["thumbnail_checks"])
        and set(thumbnail.values()) == {"pass"},
        "render-v3 successor thumbnail review mismatch",
    )
    forbidden = _review_focus_map(
        review.get("forbidden_convergence_results"),
        "render-v3.forbidden_convergence_results",
    )
    _require(
        set(forbidden) == set(frozen["forbidden_pixel_convergence"])
        and set(forbidden.values()) == {"absent"},
        "render-v3 successor forbidden-convergence mismatch",
    )

    second_look = review.get("second_look_pixel_review")
    _require(isinstance(second_look, dict), "render-v3 second-look review missing")
    expected_plan_sha = hashlib.sha256(
        canonical_json_bytes(preflight_composed["second_look_plan"])
    ).hexdigest()
    _require(
        second_look.get("plan_sha256") == expected_plan_sha
        and second_look.get("declared_review_scale_ids")
        == ["native", "thumbnail_320px"]
        and second_look.get("qualified_role") == "primary_carrier"
        and second_look.get("qualification_status") == "pass",
        "render-v3 second-look summary mismatch",
    )
    attempts = second_look.get("attempts")
    _require(
        isinstance(attempts, list)
        and len(attempts) == 1
        and attempts[0].get("attempted_role") == "primary_carrier",
        "render-v3 second-look attempt order mismatch",
    )
    scale_results = attempts[0].get("scale_results")
    _require(
        isinstance(scale_results, list)
        and [item.get("scale_id") for item in scale_results]
        == ["native", "thumbnail_320px"]
        and all(item.get("status") == "pass" for item in scale_results)
        and all(isinstance(item.get("evidence"), str) and item["evidence"] for item in scale_results),
        "render-v3 second-look scale evidence mismatch",
    )

    aggregate = review.get("aggregate_with_preserved_v1_v2_evidence")
    _require(
        aggregate
        == {
            "case_count": 6,
            "passed_case_count": 6,
            "failed_case_count": 0,
            "failure_case_ids": [],
            "outcome": "pass",
        },
        "render-v3 aggregate must qualify all six cases",
    )
    suite = review.get("post_render_full_suite")
    _require(isinstance(suite, dict), "render-v3 full-suite record missing")
    _require(
        suite.get("authorized") is True
        and suite.get("condition") == "pixel_qualification_passes"
        and suite.get("condition_met") is True,
        "render-v3 conditional full-suite boundary mismatch",
    )
    suite_executed = suite.get("executed")
    _require(isinstance(suite_executed, bool), "render-v3 full-suite execution flag must be boolean")
    if suite_executed:
        _require(
            suite.get("status") == "pass"
            and isinstance(suite.get("command"), str)
            and suite["command"]
            and isinstance(suite.get("test_count"), int)
            and suite["test_count"] > 0
            and suite.get("failure_count") == 0
            and suite.get("error_count") == 0,
            "render-v3 completed full-suite evidence mismatch",
        )
    else:
        _require(suite.get("status") == "pending", "render-v3 pending full-suite status mismatch")

    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        result_rel = review.get("result_path")
        _require(isinstance(result_rel, str) and result_rel, "render-v3 result path missing")
        result_path = local_repo_root / result_rel
        _require(result_path.is_file(), "render-v3 local result is missing")
        _require(_sha256(result_path) == review.get("result_sha256"), "render-v3 result hash mismatch")
        result = _load_json(result_path)
        _require(
            result.get("schema") == "subculture-illustration-render-result/v3"
            and result.get("qualification_status") == "pass_primary_carrier"
            and result.get("product_outcome") == "pass"
            and result.get("attempt_count") == 1
            and result.get("repair_attempt_count") == 0
            and result.get("fallback_attempt") is None,
            "render-v3 local result status mismatch",
        )
        result_dir = result_path.parent
        local_pack = _load_json(result_dir / "candidate_pack.json")
        local_composed = _load_json(result_dir / "composed_prompt.json")
        local_audit = _load_json(result_dir / "audit.json")
        local_preflight = _load_json(result_dir / "preflight.json")
        _require(local_pack == expected_pack, "render-v3 local pack drift")
        _require(local_composed == preflight_composed, "render-v3 local composed prompt drift")
        _require(
            local_preflight == _load_json(preflight_dir / "preflight.json"),
            "render-v3 local preflight drift",
        )
        _require(
            audit_composed_prompt(local_pack, local_composed) == local_audit,
            "render-v3 local audit drift",
        )
        _require(
            result.get("second_look_pixel_review") == second_look,
            "render-v3 result/review second-look mismatch",
        )
        _require(
            result.get("post_render_full_suite") == suite,
            "render-v3 result/review full-suite record mismatch",
        )
        for record in (initial, final):
            image_path = local_repo_root / record["path"]
            _require(image_path.is_file(), f"render-v3 local image missing: {record['path']}")
            _require(_sha256(image_path) == record["sha256"], f"render-v3 local image hash mismatch: {record['path']}")
            expected_dimensions = tuple(
                int(value) for value in record["dimensions"].split("x", 1)
            )
            _require(
                _png_dimensions(image_path) == expected_dimensions,
                f"render-v3 local image dimensions mismatch: {record['path']}",
            )
        _require(
            (local_repo_root / initial["path"]).read_bytes()
            == (local_repo_root / final["path"]).read_bytes(),
            "render-v3 final differs from the passing primary image",
        )
        for view in result.get("review_views", []):
            _require(isinstance(view, dict), "render-v3 review view must be an object")
            view_path = result_dir / str(view.get("path") or "")
            _require(view_path.is_file(), f"render-v3 review view missing: {view_path.name}")
            _require(_sha256(view_path) == view.get("sha256"), f"render-v3 review view hash mismatch: {view_path.name}")
            _require(
                _png_dimensions(view_path) == (view.get("width"), view.get("height")),
                f"render-v3 review view dimensions mismatch: {view_path.name}",
            )
        attempt = result.get("initial_attempt")
        _require(isinstance(attempt, dict), "render-v3 initial attempt missing")
        native_path = Path(str(attempt.get("native_tool_path") or ""))
        _require(native_path.is_file(), "render-v3 native source missing")
        _require(_sha256(native_path) == attempt.get("sha256"), "render-v3 native source hash mismatch")
        blind_path = result_dir / str(attempt.get("blind_observations_path") or "")
        _require(blind_path.is_file(), "render-v3 blind observations missing")
        _require(
            _sha256(blind_path) == attempt.get("blind_observations_sha256"),
            "render-v3 blind observation hash mismatch",
        )
        _require(not (result_dir / "edit_candidate.png").exists(), "passing render-v3 primary must not have a fallback edit")

    return {
        "qualification_status": "pass",
        "case_id": case_id,
        "attempt_count": 1,
        "repair_count": 0,
        "qualified_role": "primary_carrier",
        "passed_case_count": 6,
        "failed_case_count": 0,
        "full_suite_executed": suite_executed,
        "local_artifacts_verified": verify_local_images,
    }


def validate_render_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    review_path = asset_dir / "render_illustration_quality_visual_review_v1.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version") == "subculture-illustration-visual-review/v1",
        "render visual-review schema mismatch",
    )
    holdout_rows = _load_jsonl(asset_dir / "render_illustration_quality_holdout_v1.jsonl")
    holdout_by_id = {row["case_id"]: row for row in holdout_rows}
    cases = review.get("cases")
    _require(isinstance(cases, list) and len(cases) == 6, "render visual review must contain six cases")
    case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    _require(len(case_ids) == 6 and len(set(case_ids)) == 6, "render visual-review case IDs must be unique")
    _require(set(case_ids) == set(holdout_by_id), "render visual-review holdout coverage mismatch")

    passed = 0
    failed = 0
    local_repo_root = Path(__file__).resolve().parents[3]
    for case in cases:
        _require(isinstance(case, dict), "render visual-review case must be an object")
        case_id = case["case_id"]
        frozen = holdout_by_id[case_id]
        route_id = case.get("route_id")
        format_profile = case.get("format_profile")
        _require(route_id in frozen["topic_ids"], f"{case_id} primary route is outside frozen topic coverage")
        _require(format_profile == frozen["format_profile"], f"{case_id} format mismatch")
        seed = case.get("seed")
        _require(isinstance(seed, int) and not isinstance(seed, bool), f"{case_id} seed must be an integer")
        expected_pack = build_candidate_pack(
            frozen["request_ko"],
            topic=route_id,
            format_id=format_profile,
            seed=seed,
            creativity=0.85,
            contract_version=LEGACY_CONTRACT_VERSION,
            assets=assets,
        )
        _require(expected_pack["pack_id"] == case.get("pack_id"), f"{case_id} pack ID drift")

        required_focus = _review_focus_map(case.get("review_focus_results"), f"{case_id}.review_focus_results")
        _require(
            set(frozen["required_pixel_focus"]) <= set(required_focus),
            f"{case_id} omits frozen required pixel focus",
        )
        _require(
            all(required_focus[item] == "pass" for item in frozen["required_pixel_focus"]),
            f"{case_id} frozen required pixel focus is not fully passing",
        )
        thumbnail = _review_focus_map(case.get("thumbnail_results"), f"{case_id}.thumbnail_results")
        _require(set(thumbnail) == set(frozen["thumbnail_checks"]), f"{case_id} thumbnail coverage mismatch")
        _require(set(thumbnail.values()) == {"pass"}, f"{case_id} thumbnail review is not passing")
        forbidden = _review_focus_map(
            case.get("forbidden_convergence_results"),
            f"{case_id}.forbidden_convergence_results",
        )
        _require(
            set(forbidden) == set(frozen["forbidden_pixel_convergence"]),
            f"{case_id} forbidden-convergence coverage mismatch",
        )
        _require(set(forbidden.values()) == {"absent"}, f"{case_id} has forbidden pixel convergence")

        attempts = case.get("attempt_count")
        repairs = case.get("repair_count")
        _require(attempts in {1, 2} and repairs in {0, 1}, f"{case_id} attempt budget shape mismatch")
        _require(attempts == repairs + 1, f"{case_id} attempt and repair counts disagree")
        _require(attempts <= frozen["initial_generation_limit"] + frozen["repair_limit"], f"{case_id} exceeded image budget")
        status = case.get("qualification_status")
        is_pass = status in {"pass", "pass_after_single_bounded_edit"}
        failing_focus = [focus for focus, outcome in required_focus.items() if outcome == "fail"]
        final_image = case.get("final_image")
        if is_pass:
            passed += 1
            _require(isinstance(final_image, dict), f"{case_id} passing case lacks final image")
            _require(not failing_focus, f"{case_id} passing case contains failed review focus")
        else:
            failed += 1
            _require(status == "fail_repair_exhausted", f"{case_id} has unknown qualification status")
            _require(final_image is None, f"{case_id} failed case must not expose final image")
            _require(repairs == frozen["repair_limit"] == 1, f"{case_id} failed before exhausting bounded repair")
            _require(failing_focus, f"{case_id} failed case has no explicit failed review focus")

        if verify_local_images:
            result_rel = case.get("result_path")
            _require(isinstance(result_rel, str) and result_rel, f"{case_id} result path missing")
            result_file = local_repo_root / result_rel
            _require(result_file.is_file(), f"{case_id} local result is missing")
            _require(_sha256(result_file) == case.get("result_sha256"), f"{case_id} result hash mismatch")
            case_dir = result_file.parent
            local_pack = _load_json(case_dir / "candidate_pack.json")
            composed = _load_json(case_dir / "composed_prompt.json")
            stored_audit = _load_json(case_dir / "audit.json")
            _require(local_pack == expected_pack, f"{case_id} local candidate pack drift")
            _require(audit_composed_prompt(local_pack, composed) == stored_audit, f"{case_id} local prompt audit drift")
            _require(
                stored_audit.get("status") == "pass"
                and stored_audit.get("quality_status") == "pass"
                and not stored_audit.get("integrity_errors")
                and not stored_audit.get("failures")
                and not stored_audit.get("warnings"),
                f"{case_id} local prompt audit is not clean",
            )
            image_records = [value for key, value in case.items() if key.endswith("_image") and isinstance(value, dict)]
            for image_record in image_records:
                rel = image_record.get("path")
                _require(isinstance(rel, str) and rel, f"{case_id} local image path missing")
                image_file = local_repo_root / rel
                _require(image_file.is_file(), f"{case_id} local image is missing: {rel}")
                _require(_sha256(image_file) == image_record.get("sha256"), f"{case_id} local image hash mismatch: {rel}")
                dimensions = image_record.get("dimensions")
                _require(isinstance(dimensions, str) and "x" in dimensions, f"{case_id} image dimensions missing")
                expected_dimensions = tuple(int(value) for value in dimensions.split("x", 1))
                _require(_png_dimensions(image_file) == expected_dimensions, f"{case_id} image dimensions mismatch: {rel}")

    cross_case = review.get("cross_case_review")
    _require(isinstance(cross_case, dict), "render cross-case review must be an object")
    _require(cross_case.get("case_count") == len(cases), "render cross-case count mismatch")
    _require(cross_case.get("passed_case_count") == passed, "render passing-case count mismatch")
    _require(cross_case.get("failed_case_count") == failed, "render failed-case count mismatch")
    expected_outcome = "pass" if failed == 0 else "partial"
    _require(cross_case.get("outcome") == expected_outcome, "render cross-case outcome mismatch")
    _require(
        set(cross_case.get("failure_case_ids", []))
        == {case["case_id"] for case in cases if case["qualification_status"] == "fail_repair_exhausted"},
        "render cross-case failure IDs mismatch",
    )
    return {
        "qualification_status": expected_outcome,
        "case_count": len(cases),
        "passed_case_count": passed,
        "failed_case_count": failed,
        "local_artifacts_verified": verify_local_images,
    }


def validate_all(
    asset_dir: str | Path | None = None,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    research = validate_research(root)
    assets = load_runtime_assets(root)
    runtime = validate_assets(root)
    _require(set(assets.nodes_by_id) == research["candidate_ids"], "runtime node IDs must exactly equal research candidate IDs")
    route_alias_owner: dict[str, str] = {}
    for route_id, route in assets.routes_by_id.items():
        for phrases in route["aliases"].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = route_alias_owner.setdefault(normalized, route_id)
                _require(owner == route_id, f"normalized route alias collision: {phrase!r} -> {owner}, {route_id}")
    format_alias_owner: dict[str, str] = {}
    for variant_id, variant in assets.variants_by_id.items():
        for phrases in variant["aliases"].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = format_alias_owner.setdefault(normalized, variant_id)
                _require(owner == variant_id, f"normalized format alias collision: {phrase!r} -> {owner}, {variant_id}")
    for topic_id, route in assets.routes_by_id.items():
        _require(route["matrix_id"] == research["matrix_ids"][topic_id], f"route {topic_id} matrix provenance mismatch")
    for node_id, node in assets.nodes_by_id.items():
        definition, role, topic_id = research["candidate_specs"][node_id]
        _require(node["definition"] == definition, f"runtime definition drift: {node_id}")
        _require(node["role"] == role and node["topic_id"] == topic_id, f"runtime role/topic drift: {node_id}")
        provenance = node["provenance"]
        _require(provenance["matrix_id"] == research["matrix_ids"][topic_id], f"runtime matrix ref drift: {node_id}")
        _require(set(provenance["evidence_record_ids"]) <= research["topic_record_ids"][topic_id], f"runtime cross-topic evidence ref: {node_id}")
    for node_id, text in _runtime_texts(assets.graph):
        for pattern in RUNTIME_NAME_GUARDS:
            _require(not pattern.search(text), f"runtime definition contains protected/named-style text: {node_id}")
    holdouts = validate_holdouts(root, assets)
    legacy_prompt_qualification = validate_legacy_prompt_qualification(root, assets)
    prompt_qualification = validate_prompt_qualification(root, assets)
    render_v2_preflight = validate_render_v2_preflight(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v3_preflight = validate_render_v3_preflight(root, assets)
    render_qualification = validate_render_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v2_qualification = validate_render_v2_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v3_qualification = validate_render_v3_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    generation_retry_policy = validate_generation_retry_policy(root)
    research.pop("candidate_ids")
    research.pop("candidate_specs")
    research.pop("matrix_ids")
    research.pop("topic_record_ids")
    return {
        "status": "pass",
        "product_qualification_status": render_v3_qualification["qualification_status"],
        "research": research,
        "runtime": runtime,
        "generation_retry_policy": generation_retry_policy,
        "holdouts": holdouts,
        "legacy_prompt_qualification": legacy_prompt_qualification,
        "prompt_qualification": prompt_qualification,
        "render_v2_preflight": render_v2_preflight,
        "render_v3_preflight": render_v3_preflight,
        "render_qualification": render_qualification,
        "render_v2_qualification": render_v2_qualification,
        "render_v3_qualification": render_v3_qualification,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the illustration research, runtime assets, and frozen holdouts.")
    parser.add_argument("--asset-dir", help="override the sibling skill asset directory")
    parser.add_argument(
        "--verify-local-images",
        action="store_true",
        help="also verify ignored local render/result files, PNG dimensions, hashes, packs, and audits",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = validate_all(args.asset_dir, verify_local_images=args.verify_local_images)
    except (IllustrationRuntimeError, ValidationFailure, OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "fail", "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
